
JUDGE_SYSTEM = """You are a strict, fair teacher. You must grade 4 different AI responses to the same user prompt.
Answer only in JSON format."""

JUDGE_TEMPLATE = """The user asked:
{user_prompt}
Here are 4 different AI responses. Grade each one from 0.0 to 10.0 across these 5 rules:
1. instruction_adherence: Did it follow every rule and constraint?
2. completeness: Did it finish the whole job?
3. tone_and_style: Right voice and professional feel?
4. accuracy: True, correct, no hallucinations?
5. clarity: Clean, sharp, easy to read?

[ZERO_SHOT RESPONSE]:
{zero_shot_answer}

[ONE_SHOT RESPONSE]:
{one_shot_answer}

[FEW_SHOT RESPONSE]:
{few_shot_answer}

[CHAIN_OF_THOUGHT RESPONSE]:
{chain_of_thought_answer}

Return your report in this exact JSON format:
{{
    "zero_shot": {{
        "metric_scores": {{
            "instruction_adherence": 0.0,
            "completeness": 0.0,
            "tone_and_style": 0.0,
            "accuracy": 0.0,
            "clarity": 0.0
        }},
        "final_total_score": 0.0,
        "teacher_feedback": ["note 1", "note 2"]
    }},
    "one_shot": {{
        "metric_scores": {{
            "instruction_adherence": 0.0,
            "completeness": 0.0,
            "tone_and_style": 0.0,
            "accuracy": 0.0,
            "clarity": 0.0
        }},
        "final_total_score": 0.0,
        "teacher_feedback": ["note 1", "note 2"]
    }},
    "few_shot": {{
        "metric_scores": {{
            "instruction_adherence": 0.0,
            "completeness": 0.0,
            "tone_and_style": 0.0,
            "accuracy": 0.0,
            "clarity": 0.0
        }},
        "final_total_score": 0.0,
        "teacher_feedback": ["note 1", "note 2"]
    }},
    "chain_of_thought": {{
        "metric_scores": {{
            "instruction_adherence": 0.0,
            "completeness": 0.0,
            "tone_and_style": 0.0,
            "accuracy": 0.0,
            "clarity": 0.0
        }},
        "final_total_score": 0.0,
        "teacher_feedback": ["note 1", "note 2"]
    }}
}}"""