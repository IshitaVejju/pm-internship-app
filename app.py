import streamlit as st
import pandas as pd
from time import sleep

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SmartAssigners", page_icon="🚀", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown(
    """
    <style>
    .stApp { background-color: #fdfdfb; }

    .title {
        font-size: 38px;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #555;
        margin-top: 5px;
        margin-bottom: 30px;
    }

    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        border: 2px solid #f1f1f1;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }

    .accent-saffron {border-top: 5px solid #FF9933;}
    .accent-green {border-top: 5px solid #138808;}
    .accent-blue {border-top: 5px solid #0055A4;}

    .stButton>button {
        background-color: #0055A4;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #003d73;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown("<p class='title'>SmartAssigners</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered Internship Allocation & Career Advisor</p>", unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🎓 Internship Finder", "💼 Career Advisor"])

# ---------- INTERNSHIP FINDER ----------
with tab1:
    st.subheader("Find Best Internship Matches")

    name = st.text_input("Your Name")
    skills = st.text_area("Enter your skills (comma separated)", placeholder="Python, Machine Learning, Data Analysis")
    location = st.selectbox("Preferred Location", ["Any", "Delhi", "Mumbai", "Hyderabad", "Bengaluru", "Chennai"])
    sector = st.selectbox("Preferred Sector", ["Any", "AI/ML", "Web Development", "Data Science", "Cybersecurity", "Business"])
    academics = st.slider("Academic Performance (in %)", 40, 100, 75)

    if st.button("🔍 Find Internships"):
        with st.spinner("Matching internships..."):
            sleep(1.5)

        internships = [
            {"Role": "AI/ML Internship", "Location": "Bengaluru", "Match Score": "92%", "Stipend": "₹12,000", "Sector": "AI/ML"},
            {"Role": "Data Science Internship", "Location": "Mumbai", "Match Score": "85%", "Stipend": "₹10,000", "Sector": "Data Science"},
            {"Role": "Web Development Internship", "Location": "Delhi", "Match Score": "80%", "Stipend": "₹8,000", "Sector": "Web Development"}
        ]

        st.success(f"✅ Found {len(internships)} great opportunities for you!")

        # ---- Show Comparison Table First ----
        st.markdown("### 📋 Compare Opportunities")
        df = pd.DataFrame(internships)
        st.dataframe(df, use_container_width=True)

        # ---- Show Deck of Cards Below ----
        st.markdown("### 🎴 Internship Deck")
        cols = st.columns(len(internships))
        for col, i in zip(cols, internships):
            with col:
                st.markdown(f"<div class='card accent-green'>", unsafe_allow_html=True)
                st.markdown(f"**{i['Role']}**")
                st.write(f"📍 {i['Location']}")
                st.write(f"📊 Match Score: {i['Match Score']}")
                st.write(f"💰 Stipend: {i['Stipend']}")
                st.write(f"🏷️ Sector: {i['Sector']}")
                st.markdown("</div>", unsafe_allow_html=True)

# ---------- CAREER ADVISOR ----------
with tab2:
    st.subheader("Get Career Guidance")

    role = st.text_input("Target Role (e.g., Data Scientist, Software Engineer)")
    experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior"])
    skills_list = st.text_area("Your Current Skills", placeholder="Python, SQL, Excel")

    if st.button("💡 Get Suggestions"):
        with st.spinner("Analyzing your profile..."):
            sleep(1.5)

        st.success("✅ Career roadmap ready!")

        st.markdown("<div class='card accent-green'>", unsafe_allow_html=True)
        st.write("**1. Strengthen Core Skills**")
        st.write("Focus on advanced Python, SQL, and Machine Learning projects.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card accent-saffron'>", unsafe_allow_html=True)
        st.write("**2. Build a Portfolio**")
        st.write("Publish projects on GitHub and write case studies on LinkedIn.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card accent-blue'>", unsafe_allow_html=True)
        st.write("**3. Networking**")
        st.write("Attend 2–3 tech meetups or webinars every month to expand connections.")
        st.markdown("</div>", unsafe_allow_html=True)
