# chains/safe_parser.py
import json
from langchain_core.runnables import RunnableLambda

def simple_json_parser(model_output):
    """
    Safely handles strings, lists, dicts, and Gemini's part-based responses.
    """
    # 1. Extract content from LangChain message objects
    if hasattr(model_output, "content"):
        data_content = model_output.content
    else:
        data_content = model_output

    # 2. NEW: Handle Gemini's part-based format [{type: "text", text: "..."}]
    if isinstance(data_content, list) and len(data_content) > 0:
        if isinstance(data_content[0], dict) and "text" in data_content[0]:
            data_content = data_content[0]["text"]
        elif all(isinstance(x, str) for x in data_content):
            data_content = "".join(data_content)

    # 3. If it's already a clean dict/list, return it
    if isinstance(data_content, (dict, list)):
        return {
            "parsed": data_content,
            "is_valid": True,
            "raw": str(data_content)
        }

    # 4. Work with a clean string
    raw_text = str(data_content).strip()
    
    # 5. Try standard JSON parse
    try:
        return {
            "parsed": json.loads(raw_text),
            "is_valid": True,
            "raw": raw_text
        }
    except Exception:
        # 6. Strip markdown fences if present
        cleaned_text = raw_text
        if cleaned_text.startswith("```"):
            lines = cleaned_text.splitlines()
            if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
                cleaned_text = "\n".join(lines[1:-1]).strip()
                try:
                    return {
                        "parsed": json.loads(cleaned_text),
                        "is_valid": True,
                        "raw": raw_text
                    }
                except Exception:
                    pass
                    
        return {
            "parsed": None,
            "is_valid": False,
            "raw": raw_text
        }

parse_json = RunnableLambda(simple_json_parser)