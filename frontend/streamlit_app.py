import streamlit as st
import requests
import json

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Mini-Poe (Gemini)", layout="wide")
st.title("Mini-Poe (Gemini): Router + RAG + Agent + Eval")

def safe_json_display(obj):
    """
    Streamlit st.json() expects a dict/list.
    If backend returns eval as a JSON string, parse it.
    If it's plain text, show it as code.
    """
    if obj is None:
        st.info("No data available.")
        return

    if isinstance(obj, (dict, list)):
        st.json(obj)
        return

    if isinstance(obj, str):
        s = obj.strip()
        # Try parsing JSON string
        try:
            parsed = json.loads(s)
            if isinstance(parsed, (dict, list)):
                st.json(parsed)
            else:
                st.code(obj)
        except Exception:
            st.code(obj)
        return

    # Fallback for unexpected types (e.g., numbers)
    st.write(obj)

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Controls")
    if st.button("Ingest Docs"):
        try:
            r = requests.post(f"{API}/ingest", timeout=180)
            if r.status_code != 200:
                st.error(f"/ingest failed: {r.status_code}")
                st.code(r.text)
            else:
                out = r.json()
                st.success("Ingest complete.")
                safe_json_display(out)
        except requests.RequestException as e:
            st.error("Failed to call /ingest")
            st.code(str(e))

with col1:
    st.subheader("Ask")
    q = st.text_input("Ask something", placeholder="Try: Explain RAG and how chunking affects retrieval")

    if st.button("Ask") and q.strip():
        try:
            r = requests.post(f"{API}/ask", json={"query": q}, timeout=180)
            if r.status_code != 200:
                st.error(f"/ask failed: {r.status_code}")
                st.code(r.text)
            else:
                out = r.json()

                st.subheader("Answer")
                # markdown renders multi-paragraph output better than write()
                st.markdown(out.get("answer", ""))

                st.subheader("Routing")
                st.code(out.get("intent", ""))

                st.subheader("Latency")
                # show whatever the backend provides
                lat_obj = {
                    "latency_ms": out.get("latency_ms"),
                    "model_latency_ms": out.get("model_latency_ms"),
                }
                safe_json_display(lat_obj)

                st.subheader("Evaluation")
                safe_json_display(out.get("eval"))

                st.subheader("Retrieved Sources")
                safe_json_display(out.get("retrieved_sources"))

        except requests.RequestException as e:
            st.error("Failed to call /ask")
            st.code(str(e))