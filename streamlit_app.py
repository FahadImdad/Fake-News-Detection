import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="🔥 Fake News Radar", page_icon="🛰️", layout="wide")

# Load fancy Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

lottie_warning = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bhw1ul4g.json")
lottie_success = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_jbrw3hcz.json")
lottie_scan = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_ikvz7qhc.json")

# Custom CSS for crazy colors
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ffe259, #ffa751);
    }
    .stButton > button {
        background: linear-gradient(to right, #fc466b, #3f5efb);
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #fdf6ec;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1 style='text-align: center; color: #ff4b1f;'>🚨 Fake News Radar 🚨</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #333;'>Instantly scan news content with AI-powered detection</h5>", unsafe_allow_html=True)
if lottie_scan:
    st_lottie(lottie_scan, height=180, key="scan")

st.markdown("---")

# Example articles
examples = {
    "🛸 NASA lands new rover": (
        "NASA successfully lands new rover on Mars",
        "NASA's rover has landed safely on the red planet. It will collect rock samples and search for signs of ancient microbial life."
    ),
    "👑 Queen spotted in supermarket": (
        "Queen Elizabeth spotted shopping at Walmart",
        "Sources claim Queen Elizabeth was seen in disguise shopping at a Walmart in Florida, raising eyebrows around the world."
    ),
    "💉 Vaccine update": (
        "Pfizer announces new COVID booster",
        "Pfizer has released a new COVID-19 booster to tackle emerging variants more effectively in 2025."
    )
}

# Input fields
col1, col2 = st.columns(2)

with col1:
    example_key = st.selectbox("🧪 Choose Example or Write Your Own", ["✍️ Custom Input"] + list(examples.keys()))

with col2:
    available_models = [
    "Logistic Regression", "Multinomial NB", "Bernoulli NB",
    "Linear SVM", "KNN", "Gradient Boosting",
    "Random Forest", "Ridge Classifier"
    ]
    model_choice = st.selectbox("🤖 Select Model", available_models)


# Set title/content
if example_key != "✍️ Custom Input":
    title, content = examples[example_key]
else:
    title = st.text_input("📰 News Title", placeholder="e.g. NASA lands rover...")
    content = st.text_area("📝 News Content", placeholder="Paste the full article here", height=200)

# Predict button
if st.button("🎯 Analyze Now"):
    if not title.strip() or not content.strip():
        st.warning("⚠️ Please enter both title and content!")
    else:
        with st.spinner("Scanning article with neural power..."):
            try:
                payload = {"title": title, "content": content}
                response = requests.post("http://127.0.0.1:5000/predict", json=payload)

                if response.status_code == 200:
                    result = response.json()["predictions"].get(model_choice)

                    if result == 1:
                        st.success("✅ REAL NEWS DETECTED")
                        if lottie_success:
                            st_lottie(lottie_success, height=200)
                    else:
                        st.error("❌ FAKE NEWS ALERT!")
                        if lottie_warning:
                            st_lottie(lottie_warning, height=200)
                else:
                    st.error(f"🔌 Server error: {response.status_code}")
            except Exception as e:
                st.error(f"🚫 Connection failed: `{e}`")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.85em; color: gray;'>Made with 🧠 Streamlit + Flask + Lottie</p>", unsafe_allow_html=True)
