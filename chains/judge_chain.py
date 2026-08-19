# chains/judge_chain.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from templates.judge import JUDGE_SYSTEM, JUDGE_TEMPLATE
from chains.safe_parser import parse_json

def judge_all(api_key: str, user_prompt: str, answers: dict):
    """One judge call. Grades all 4 responses at once."""
    gemini = ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-3.6-flash"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", JUDGE_SYSTEM),
        ("user", JUDGE_TEMPLATE)
    ])
    
    chain = prompt | gemini | parse_json
    
    return chain.invoke({
        "user_prompt": user_prompt,
        "zero_shot_answer": answers["zero_shot"],
        "one_shot_answer": answers["one_shot"],
        "few_shot_answer": answers["few_shot"],
        "chain_of_thought_answer": answers["chain_of_thought"]
    })