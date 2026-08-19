# app.py
import streamlit as st
import pandas as pd
import time
import json
import random

from chains.prompt_chain import run_workers
from chains.judge_chain import judge_all

# Page layout
st.set_page_config(
    page_title="Prompt Engineering Playground",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #0d47a1; margin-bottom: 0.2rem; }
    .subtitle { font-size: 1.1rem; color: #555555; margin-bottom: 2rem; }
    .metric-card { background: #f8f9fa; border-radius: 8px; padding: 1rem; border-left: 4px solid #0d47a1; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 Prompt Engineering Evaluation Playground</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Benchmark Zero-shot, One-shot, Few-shot, and Chain-of-Thought prompting with an independent LLM judge.</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔑 Authentication")
st.sidebar.markdown("Get your API key from [Google AI Studio](https://aistudio.google.com)")
gemini_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", placeholder="AIzaSy...")

st.sidebar.header("⚖️ Judge Rubric")
st.sidebar.markdown("""
Grades across **5 criteria** (0–10):
- `instruction_adherence`
- `completeness`
- `tone_and_style`
- `accuracy`
- `clarity`
""")

# Auto demo mode when no key
has_key = bool(gemini_api_key and len(gemini_api_key) > 10)
if not has_key:
    st.sidebar.warning("🎭 No API key detected — **Demo Mode** active. Add a key for live Gemini evaluation.")

st.sidebar.markdown("---")
st.sidebar.caption("Built with LangChain LCEL + Streamlit")

# Main Workspace
st.header("📝 Strategy Test Center")

with st.form("playground_form", clear_on_submit=False):
    user_prompt_input = st.text_area(
        "Enter a prompt to test across all 4 techniques:",
        value='Analyze this complaint: "I ordered wireless headphones on March 1st with 2-day shipping. They arrived March 8th with a cracked ear cup. Support said I must pay return shipping because the box was opened."\n\nTask: (1) Sentiment (Positive/Neutral/Negative), (2) Product category, (3) Exactly 2 policy violations, (4) Resolution (Refund/Replacement/None), (5) One-sentence justification.\n\nReturn JSON: sentiment, product_category, policy_violations[], resolution, justification',
        height=120
    )
    cols = st.columns([3, 1])
    with cols[0]:
        execute_matrix = st.form_submit_button("🚀 Launch Evaluation", type="primary", use_container_width=True)
    with cols[1]:
        export_ready = st.form_submit_button("📋 Copy Prompt", use_container_width=True)

if export_ready:
    st.code(user_prompt_input, language="text")
    st.toast("Prompt copied to clipboard area!")

# Static table
static_table_data = {
    "Prompting Technique": ["Zero-shot", "One-shot", "Few-shot", "Chain-of-Thought"],
    "Description": [
        "Raw prompt, no examples",
        "One example shown",
        "Three examples shown",
        "Step-by-step reasoning forced"
    ],
    "Score": ["—", "—", "—", "—"]
}

table_slot = st.empty()
table_slot.dataframe(pd.DataFrame(static_table_data), use_container_width=True, hide_index=True)


def simulated_judge(answers: dict):
    """Realistic demo scores for portfolio visitors without API keys."""
    random.seed(hash(str(answers)) % 10000)
    ranges = {
        "zero_shot": (6.2, 7.6),
        "one_shot": (6.8, 8.1),
        "few_shot": (7.5, 8.7),
        "chain_of_thought": (8.2, 9.4)
    }
    result = {}
    for tech, answer in answers.items():
        low, high = ranges.get(tech, (6.5, 8.5))
        base = random.uniform(low, high)
        scores = {
            "instruction_adherence": round(min(10, base + random.uniform(-0.5, 0.5)), 1),
            "completeness": round(min(10, base + random.uniform(-0.5, 0.5)), 1),
            "tone_and_style": round(min(10, base + random.uniform(-0.3, 0.4)), 1),
            "accuracy": round(min(10, base + random.uniform(-0.4, 0.4)), 1),
            "clarity": round(min(10, base + random.uniform(-0.3, 0.3)), 1),
        }
        final = round(sum(scores.values()) / 5, 1)
        feedback_pool = [
            "Good structure but missed some prompt constraints.",
            "Strong reasoning and clear output formatting.",
            "Could include more specific details in the response.",
            "Well-organized answer with accurate information.",
            "Some redundancy in the explanation — tighten it up.",
            "Excellent logical progression from input to conclusion."
        ]
        result[tech] = {
            "metric_scores": scores,
            "final_total_score": final,
            "teacher_feedback": random.sample(feedback_pool, 2)
        }
    return {"parsed": result, "is_valid": True, "raw": str(result)}


# Run
if execute_matrix:
    if not has_key:
        # Demo mode — skip API entirely
        with st.spinner("Running demo simulation..."):
            time.sleep(1.2)
            techniques_order = ["zero_shot", "one_shot", "few_shot", "chain_of_thought"]
            
            # Fake worker outputs for demo
            demo_outputs = {
                "zero_shot": {"parsed": {"result": "Negative | Headphones | [Late delivery, Damaged item] | Replacement | Customer deserves free replacement."}, "is_valid": True, "raw": ""},
                "one_shot": {"parsed": {"result": "Negative. Headphones. Violations: delayed shipping, damaged goods. Resolution: Replacement. Justification: Product arrived damaged after late delivery."}, "is_valid": True, "raw": ""},
                "few_shot": {"parsed": {"result": {"sentiment": "Negative", "product_category": "Headphones", "policy_violations": ["Late delivery beyond 2-day guarantee", "Damaged product on arrival"], "resolution": "Replacement", "justification": "Customer received a damaged item after a shipping delay and should not pay return shipping."}}, "is_valid": True, "raw": ""},
                "chain_of_thought": {"parsed": {"thinking_steps": ["The customer paid for 2-day shipping but received the item 7 days later — this is a policy violation.", "The ear cup was cracked on arrival, indicating a defective/damaged product — another violation.", "The customer should not pay return shipping for a damaged item."], "result": {"sentiment": "Negative", "product_category": "Headphones", "policy_violations": ["Delivery exceeded paid 2-day shipping window", "Item arrived damaged/defective"], "resolution": "Replacement", "justification": "The customer received a damaged product after a significant shipping delay and should receive a free replacement without return shipping fees."}}, "is_valid": True, "raw": ""}
            }
            
            answers = {t: str(demo_outputs[t]["parsed"]) for t in techniques_order}
            judge_result = simulated_judge(answers)
            mode_label = "Demo Mode"
            worker_outputs = demo_outputs
    else:
        # Live mode
        with st.spinner("Processing 4 workers + 1 judge via Gemini API..."):
            start_time = time.time()
            
            worker_outputs = run_workers(api_key=gemini_api_key, user_prompt=user_prompt_input)
            
            techniques_order = ["zero_shot", "one_shot", "few_shot", "chain_of_thought"]
            answers = {}
            for tech_key in techniques_order:
                out = worker_outputs[tech_key]
                answers[tech_key] = str(out["parsed"] if out["is_valid"] else out["raw"])
            
            judge_result = judge_all(
                api_key=gemini_api_key,
                user_prompt=user_prompt_input,
                answers=answers
            )
            
            elapsed = time.time() - start_time
            mode_label = f"Live Gemini ({elapsed:.1f}s)"
    
    # Build report
    compiled_report = {}
    live_scores_list = []
    techniques_order = ["zero_shot", "one_shot", "few_shot", "chain_of_thought"]
    
    for tech_key in techniques_order:
        compiled_report[tech_key] = {
            "generation": worker_outputs.get(tech_key, {"parsed": None, "is_valid": False, "raw": "N/A"}),
            "evaluation": {"parsed": None, "is_valid": False, "raw": ""}
        }
        
        if judge_result["is_valid"] and isinstance(judge_result["parsed"], dict):
            tech_scores = judge_result["parsed"].get(tech_key)
            if tech_scores and isinstance(tech_scores, dict):
                compiled_report[tech_key]["evaluation"] = {
                    "parsed": tech_scores,
                    "is_valid": True,
                    "raw": str(tech_scores)
                }
                score_val = f"{tech_scores.get('final_total_score', 0.0)} / 10"
            else:
                score_val = "Missing"
        else:
            score_val = "Error"
        
        live_scores_list.append(score_val)
    
    # Update table
    static_table_data["Score"] = live_scores_list
    table_slot.dataframe(pd.DataFrame(static_table_data), use_container_width=True, hide_index=True)
    
    st.success(f"Evaluation complete — {mode_label}")
    
    # Export button
    export_json = json.dumps(compiled_report, indent=2, default=str)
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=export_json,
        file_name="prompt_engineering_report.json",
        mime="application/json"
    )
    
    # Tabs
    tab_zero, tab_one, tab_few, tab_cot = st.tabs([
        "🔹 Zero-Shot", "🔸 One-Shot", "🔹 Few-Shot", "🔸 Chain-of-Thought"
    ])
    
    tab_mapping = {"zero_shot": tab_zero, "one_shot": tab_one, "few_shot": tab_few, "chain_of_thought": tab_cot}
    
    for tech_key, active_tab in tab_mapping.items():
        with active_tab:
            data_block = compiled_report[tech_key]
            gen = data_block["generation"]
            eval_data = data_block["evaluation"]
            left_col, right_col = st.columns(2)
            
            with left_col:
                st.markdown("#### 🤖 Model Output")
                if gen["is_valid"]:
                    st.json(gen["parsed"])
                else:
                    st.warning("Malformed output — raw fallback:")
                    st.code(gen["raw"], language="text")
                    
            with right_col:
                st.markdown("#### 🎓 Judge Assessment")
                if eval_data["is_valid"] and isinstance(eval_data["parsed"], dict):
                    score_box = eval_data["parsed"]
                    
                    cols = st.columns(2)
                    cols[0].metric("Overall Score", f"{score_box.get('final_total_score', 0.0)} / 10")
                    cols[1].metric("Technique", tech_key.replace("_", "-").title())
                    
                    st.markdown("**Sub-Metric Breakdown:**")
                    st.json(score_box.get("metric_scores", {}))
                    
                    st.markdown("**Teacher Feedback:**")
                    for bullet in score_box.get("teacher_feedback", []):
                        st.write(f"- {bullet}")
                else:
                    st.error("Judge could not parse this response.")
                    st.code(eval_data["raw"], language="text")