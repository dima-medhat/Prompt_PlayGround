# chains/prompt_chain.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from templates.prompt_library import prompts
from chains.safe_parser import parse_json

def run_workers(api_key: str, user_prompt: str):
    """Runs 4 prompting techniques in parallel."""
    gemini = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-3.6-flash"
    )
    
    techniques = ["zero_shot", "one_shot", "few_shot", "chain_of_thought"]
    chains = {}
    
    for tech in techniques:
        config = prompts[tech]
        template = ChatPromptTemplate.from_messages([
            ("system", config["system_instruction"]),
            ("user", config["template"])
        ])
        chains[tech] = template | gemini | parse_json

    parallel = RunnableParallel(**chains)
    return parallel.invoke({"user_prompt": user_prompt})