import json

import requests
import streamlit as st
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000"

SAMPLE_DIALOGUE = """Doctor: Good morning, Mr. Rao. What brings you in today?
Patient: I've had a headache for about a week, mostly in the afternoons.
Doctor: Does anything make it better or worse?
Patient: It gets worse when I'm working on my laptop for a long time.
Doctor: How many hours do you sleep, and how much water do you drink?
Patient: Maybe five hours of sleep, and not much water, to be honest.
Doctor: That could explain it. I'd like you to sleep at least seven hours, drink more water, and take a short break from the screen every hour.
Patient: Okay, and if the headache doesn't go away?
Doctor: Come back in two weeks and we'll run some tests."""


def speak_button(text):
    """Show Listen / Stop buttons that read the text aloud using the browser's own voice."""
    # json.dumps makes a safe JavaScript string; replacing "<" keeps the text from ever breaking the page
    safe_text = json.dumps(text).replace("<", "\\u003c")
    html = f"""
    <button onclick="speak()" style="padding:6px 14px;font-size:15px;cursor:pointer;">Listen</button>
    <button onclick="window.speechSynthesis.cancel()" style="padding:6px 14px;font-size:15px;cursor:pointer;">Stop</button>
    <script>
    function speak() {{
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance({safe_text});
        u.lang = "en-US";
        u.rate = 1.0;
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    if hasattr(st, "iframe"):
        st.iframe(html, height=50)
    else:
        components.html(html, height=50)


def load_sample():
    st.session_state["text"] = SAMPLE_DIALOGUE


st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")
st.title("AI Text Summarizer")
st.caption("Paste a long text or a chat and get a short summary.")

with st.sidebar:
    st.subheader("Backend status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3).json()
        if health.get("model_loaded"):
            st.success("Backend is running and the model is loaded.")
        else:
            st.warning("Backend is running but the model is still loading.")
    except requests.exceptions.RequestException:
        st.error("Backend is not running. Start it first (see README).")

st.button("Use sample dialogue", on_click=load_sample)
text = st.text_area("Text to summarize", key="text", height=260)

if st.button("Summarize", type="primary"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Summarizing... this can take 10-60 seconds on a laptop CPU."):
                response = requests.post(f"{API_URL}/predict", json={"text": text}, timeout=600)
            if response.ok:
                result = response.json()
                st.subheader("Summary")
                st.info(result["summary"])
                speak_button(result["summary"])
                col1, col2, col3 = st.columns(3)
                col1.metric("Original words", result["original_words"])
                col2.metric("Summary words", result["summary_words"])
                col3.metric("Shorter by", f"{result['compression_percent']}%")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except ValueError:
                    detail = response.text
                st.error(f"The backend returned an error: {detail}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the backend. Start it with: uvicorn app:app --port 8000")
        except requests.exceptions.Timeout:
            st.error("The backend took too long. Try a shorter text, or lower num_beams in config/params.yaml.")