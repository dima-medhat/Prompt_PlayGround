# app.py
import streamlit as st
import pandas as pd
import time
import json

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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧪 Prompt Engineering Evaluation Playground</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A professional portfolio workspace built with LangChain (LCEL) and Google Gemini to benchmark advanced prompting techniques.</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔑 Authentication")
st.sidebar.markdown(
    "Get your secret API key from the official platform here: "
    "[Google AI Studio ↗](https://aistudio.google.com)"
)

gemini_api_key = st.sidebar.text_input(
    "Enter Gemini API Key", 
    type="password", 
    placeholder="AIzaSy..."
)

st.sidebar.header("⚖️ Active Judge Rubric Metrics")
st.sidebar.markdown("""
Our supervisor grades outputs across **5 core criteria**:
- `instruction_adherence`
- `completeness`
- `tone_and_style`
- `accuracy`
- `clarity`
""")

# Main Workspace
st.header("📝 Strategy Test Center")

with st.form("playground_form", clear_on_submit=False):
    user_prompt_input = st.text_area(
        "Enter a normal prompt instruction to execute across the engineering matrix (Press Ctrl+Enter or click Launch):",
        value="Categorize this text into Tech, Finance, or Health and state the core problem: 'The server database crashed at 3 AM causing a full checkout outage.'",
        height=80
    )
    execute_matrix = st.form_submit_button("🚀 Launch Parallel LCEL Matrix Execution", type="primary", use_container_width=True)

# Static table
static_table_data = {
    "Prompting Technique": ["Zero-shot Prompting", "One-shot Prompting", "Few-shot Prompting", "Chain-of-Thought Prompting"],
    "Core Execution Strength": [
        "Executes baseline raw directives with zero reference history overhead.",
        "Calibrates output style and length formatting patterns using a single anchor example.",
        "Establishes strict formatting safety boundaries using diverse case studies.",
        "Forces multi-step logical deduction checks before producing final output answers."
    ],
    "Optimal Use-Case Task": [
        "Simple commands / General task classifications",
        "Targeted styling constraints / Copywriting style matching",
        "Strict database formatting schema controls",
        "Complex logic problems, math processing, and analytical thinking"
    ],
    "Live Evaluation Score": ["Waiting for run...", "Waiting for run...", "Waiting for run...", "Waiting for run..."]
}

table_slot = st.empty()
table_slot.dataframe(pd.DataFrame(static_table_data), use_container_width=True, hide_index=True)

# Run
if execute_matrix:
    if not gemini_api_key:
        st.error("⚠️ Authentication Missing: Please provide a valid Google Gemini API Key in the sidebar control panel.")
    else:
        with st.spinner("Processing concurrent LCEL worker models and parsing teacher metrics..."):
            start_time = time.time()
            
            # Phase A: 4 workers in parallel
            worker_outputs = run_workers(api_key=gemini_api_key, user_prompt=user_prompt_input)
            
            compiled_report = {}
            live_scores_list = []
            techniques_order = ["zero_shot", "one_shot", "few_shot", "chain_of_thought"]
            
            # Build answers dict
            answers = {}
            for tech_key in techniques_order:
                out = worker_outputs[tech_key]
                answers[tech_key] = str(out["parsed"] if out["is_valid"] else out["raw"])
            
            # Phase B: ONE judge call for all 4
            judge_result = judge_all(
                api_key=gemini_api_key,
                user_prompt=user_prompt_input,
                answers=answers
            )
            
            # Process results
            for tech_key in techniques_order:
                compiled_report[tech_key] = {
                    "generation": worker_outputs[tech_key],
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
                        score_val = f"{tech_scores.get('final_total_score', 0.0)} / 10.0"
                    else:
                        score_val = "Missing"
                else:
                    score_val = "Parsing Error"
                
                live_scores_list.append(score_val)
                
            elapsed_duration = time.time() - start_time
            st.success(f"All pipelines processed concurrently and graded by the Judge in {elapsed_duration:.2f} seconds!")
            
            # Dynamic Update: Replace values with the real scores
            static_table_data["Live Evaluation Score"] = live_scores_list
            table_slot.dataframe(pd.DataFrame(static_table_data), use_container_width=True, hide_index=True)
            
            # Deep-Dive Workspace Tabs Rendering
            tab_zero, tab_one, tab_few, tab_cot = st.tabs([
                "Zero-Shot Breakdown", "One-Shot Breakdown", "Few-Shot Breakdown", "Chain-of-Thought Breakdown"
            ])
            
            tab_mapping = {"zero_shot": tab_zero, "one_shot": tab_one, "few_shot": tab_few, "chain_of_thought": tab_cot}
            
            for tech_key, active_tab in tab_mapping.items():
                with active_tab:
                    data_block = compiled_report[tech_key]
                    gen = data_block["generation"]
                    eval_data = data_block["evaluation"]
                    left_col, right_col = st.columns(2)
                    
                    with left_col:
                        st.markdown("#### 🤖 Generation Output Data")
                        if gen["is_valid"]:
                            st.json(gen["parsed"])
                        else:
                            st.warning("⚠️ Malformed structural data format intercepted. Displaying string fallback:")
                            st.code(gen["raw"], language="text")
                            
                    with right_col:
                        st.markdown("#### 🎓 Professional Teacher Assessment")
                        if eval_data["is_valid"] and isinstance(eval_data["parsed"], dict):
                            score_box = eval_data["parsed"]
                            st.metric(label="Overall Quality Score", value=f"{score_box.get('final_total_score', 0.0)} / 10.0")
                            st.markdown("**Sub-Metric Breakdown:**")
                            st.json(score_box.get("metric_scores", {}))
                            st.markdown("**Teacher Coaching Critiques:**")
                            for bullet in score_box.get("teacher_feedback", []):
                                st.write(f"- {bullet}")
                        else:
                            st.error("The Judge output encountered structural text anomalies and could not parse cleanly into JSON.")
                            st.code(eval_data["raw"], language="text")