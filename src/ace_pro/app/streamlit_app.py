import streamlit as st
from pathlib import Path
from ace_pro.simulator import simulate_call
from ace_pro.tools.redaction import redact_text, default_redaction_config
from ace_pro.tools.summarize import summarize_extractive
from ace_pro.rag.store import VectorStore
st.set_page_config(page_title="AI Call Exchange (Pro)", layout="wide")

st.title("AI Call Exchange — Pro UI")
tab_sim, tab_notes = st.tabs(["Simulator", "Notes & Redaction"])

with tab_sim:
    st.subheader("Run a simulated call")
    scenario_file = st.file_uploader("Upload scenario.yaml", type=["yaml","yml"])
    top_k = st.slider("Summary bullets", 3, 12, 7)
    run = st.button("Run Simulation")
    if run and scenario_file:
        tmp = Path(st.secrets.get("TMP_DIR", ".")) / "ui_scenario.yaml"
        tmp.write_text(scenario_file.getvalue().decode("utf-8"))
        transcript = simulate_call(str(tmp))
        st.session_state["transcript"] = transcript
        st.success("Simulation complete.")
        st.code(transcript, language="markdown")

with tab_notes:
    st.subheader("Create notes and preview redaction")
    transcript_txt = st.text_area("Transcript", value=st.session_state.get("transcript",""), height=300)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Summarize"):
            bullets = summarize_extractive(transcript_txt, top_k=7)
            st.write("### Highlights")
            for b in bullets: st.markdown(f"- {b}")
    with col2:
        if st.button("Redact"):
            red = redact_text(transcript_txt, default_redaction_config())
            st.write("### Redacted Transcript")
            st.code(red, language="markdown")
