import streamlit as st
import os
from utils.audio_utils import extract_audio
from transcription import transcribe_audio
import google.generativeai as genai

# ✅ Load Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ Streamlit UI setup
st.set_page_config(page_title="🎥 Video Q&A Agent", layout="centered")
st.title("🎥 Video Q&A Agent")
st.markdown("Upload a video, get its transcript, and auto-generate Q&A using Gemini!")

try:
    # 📁 Upload video file
    uploaded_file = st.file_uploader("📁 Upload a video file", type=["mp4", "mov", "avi"])

    if uploaded_file:
        # ✅ Save video to local uploads folder
        os.makedirs("uploads", exist_ok=True)
        video_path = os.path.join("uploads", uploaded_file.name)

        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.video(video_path)

        # 🔊 Extract audio from video
        st.info("🔊 Extracting audio...")
        audio_path = extract_audio(video_path)
        st.success("✅ Audio extracted!")

        # 📝 Transcribe audio using Whisper
        st.info("📝 Transcribing audio...")
        transcript = transcribe_audio(audio_path)
        st.text_area("📜 Transcript", transcript, height=250)

        # 🤖 Generate Q&A using Gemini
        st.markdown("---")
        st.markdown("### 🤖 Generate Questions using Transcript")
        if st.button("✨ Generate Q&A"):
            st.info("⏳ Generating questions using Gemini...")
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"Generate 5 short questions based on this transcript:\n\n{transcript}"
            response = model.generate_content(prompt)
            qa = response.text
            st.text_area("📘 Generated Q&A", qa, height=250)
            st.success("✅ Q&A generated!")

except Exception as e:
    st.error(f"⚠️ An error occurred:\n\n{e}")

# --------------------------------------------------------------
# 🤖 Copilot Chatbot Link Section
# --------------------------------------------------------------
st.markdown("---")
st.markdown("### 🤖 Want to Use the Transcript in a Chatbot?")
st.markdown("Use the transcript or questions above as content for your Microsoft Copilot Studio agent.")

copilot_link = "https://copilotstudio.microsoft.com/copilot/YOUR-AGENT-ID"  # Replace with your agent link

st.markdown(
    f"[🚀 Launch Microsoft Copilot Chatbot]({copilot_link})",
    unsafe_allow_html=True
)
