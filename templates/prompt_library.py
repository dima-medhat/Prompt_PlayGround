# templates/prompt_library.py

prompts = {
    "zero_shot": {
        "name": "Zero-shot Prompting",
        "description": "Runs your prompt directly without showing any examples.",
        "system_instruction": "You are a helpful AI assistant. You must answer inside a JSON object.",
        "template": """Follow this instruction exactly.

User Prompt:
{user_prompt}

Return your answer in this exact JSON format:
{{
    "result": "<your answer here>"
}}"""
    },

    "one_shot": {
        "name": "One-shot Prompting",
        "description": "Shows the AI one example of how to format and answer.",
        "system_instruction": "You are an AI assistant that follows examples perfectly.",
        "template": """Here is an example of how to format your answer:

[EXAMPLE]
User Prompt: Extract the email and phone from: 'Contact sales at support@enterprise.com or call 555-0199.'
Answer:
{{
    "result": "Email: support@enterprise.com, Phone: 555-0199"
}}
[/EXAMPLE]

Now do the same thing for this prompt:

User Prompt:
{user_prompt}

Return your answer in this exact JSON format:
{{
    "result": "<your answer here>"
}}"""
    },

    "few_shot": {
        "name": "Few-shot Prompting",
        "description": "Shows the AI three different examples to teach it a pattern.",
        "system_instruction": "You are an AI assistant that matches formatting patterns perfectly.",
        "template": """Look at these examples to see how to answer:

[EXAMPLE 1 - CLASSIFY]
User Prompt: Is 'The server response times are too slow' a bad thing or a good thing?
Answer:
{{
    "result": "Bad Thing / Performance Issue"
}}
[/EXAMPLE 1]

[EXAMPLE 2 - SUMMARIZE]
User Prompt: Summarize 'The project milestone was missed due to unexpected shipping delays' in four words.
Answer:
{{
    "result": "Milestone missed: shipping delays."
}}
[/EXAMPLE 2]

[EXAMPLE 3 - QUESTION]
User Prompt: What is the main currency used in Germany?
Answer:
{{
    "result": "Euro (EUR)"
}}
[/EXAMPLE 3]

Now follow this pattern for the real prompt:

User Prompt:
{user_prompt}

Return your answer in this exact JSON format:
{{
    "result": "<your answer here>"
}}"""
    },

    "chain_of_thought": {
        "name": "Chain-of-Thought Prompting",
        "description": "Forces the AI to write out its thinking steps before giving the answer.",
        "system_instruction": "You are a smart AI that thinks out loud step-by-step before answering.",
        "template": """Think carefully about the prompt. Write out your steps, then give the final result.

User Prompt:
{user_prompt}

Return your answer in this exact JSON format:
{{
    "thinking_steps": [
        "Step 1: Write down your first thought...",
        "Step 2: Write down your second thought..."
    ],
    "result": "<your final answer here>"
}}"""
    }
}