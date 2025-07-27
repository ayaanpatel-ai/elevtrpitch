
import streamlit as st
from flair.models import TextClassifier
from flair.data import Sentence

# Load Flair sentiment model
classifier = TextClassifier.load('en-sentiment')

# App configuration
st.set_page_config(page_title="ElevtrPitch", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #D4AF37;'>🚀 ElevtrPitch</h1>",
    unsafe_allow_html=True,
)
st.markdown("<h4 style='text-align: center; color: #800020;'>AI-Powered Pitch Analyzer</h4>", unsafe_allow_html=True)
st.markdown("---")

# Input section
pitch = st.text_area("🎤 Enter your elevator pitch:", height=200, placeholder="Write a startup pitch here...")

st.markdown("### 🎚️ Customize Your Metrics")
clarity = st.slider("Clarity", 0, 10, 5)
feasibility = st.slider("Feasibility", 0, 10, 5)
innovation = st.slider("Innovation", 0, 10, 5)

if st.button("🔍 Analyze Pitch"):
    if pitch.strip() == "":
        st.warning("Please enter a pitch to analyze.")
    else:
        sentence = Sentence(pitch)
        classifier.predict(sentence)
        sentiment = sentence.labels[0]
        sentiment_value = sentiment.score
        sentiment_label = sentiment.value

        # Normalize metrics to 0–1 scale
        clarity_norm = clarity / 10
        feasibility_norm = feasibility / 10
        innovation_norm = innovation / 10

        # Weighted average investment score (sentiment + logic)
        investment_score = round((sentiment_value + (clarity_norm + feasibility_norm + innovation_norm) / 3) / 2 * 100, 2)

        st.markdown("---")
        st.markdown("## 🧠 Analysis Results")
        st.metric("Sentiment", f"{sentiment_label} ({round(sentiment_value * 100, 1)}%)")
        st.metric("Investment Score", f"{investment_score} / 100")

        # Generate feedback
        feedback = []
        if clarity < 5:
            feedback.append("🔹 Improve how clearly your pitch communicates the idea.")
        if feasibility < 5:
            feedback.append("🔹 Provide more realistic execution details.")
        if innovation < 5:
            feedback.append("🔹 Emphasize what makes your solution unique or new.")

        if sentiment_value < 0.5:
            feedback.append("🔹 Strengthen your tone and confidence in the pitch.")

        st.markdown("### 📌 Feedback")
        if feedback:
            for tip in feedback:
                st.markdown(tip)
        else:
            st.success("✅ Your pitch looks strong across all metrics!")
