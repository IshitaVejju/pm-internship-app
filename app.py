import streamlit as st
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SmartAssigners", page_icon="🧑🏼‍💻", layout="centered")

# ---------- INDIAN FLAG THEME ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(to bottom, #FF9933, #FFFFFF, #138808); }
.stCard, .stForm, .stTextInput, .stNumberInput, .stTextArea {
    background-color: white !important;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
h2, h3, .stSubheader { color: #0b3d0b !important; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div style="text-align:center; font-size:36px; font-weight:bold;
            background:linear-gradient(to right, #FF9933, #FFFFFF, #138808);
            padding:15px; border-radius:10px;">
    SmartAssigners 👩‍💻
</div>
""", unsafe_allow_html=True)

st.write("Welcome to **SmartAssigners** 💻 Your Internship Assistant Platform")

# ---------- LOAD INTERNSHIPS ----------
@st.cache_data
def load_internships():
    try:
        df = pd.read_csv("data/internships.csv")  # Admin updates externally
        return df.to_dict("records")
    except FileNotFoundError:
        return []

internships = load_internships()

# ---------- STUDENT PORTAL ----------
st.subheader("🎓 Enter Your Details for Matching")

with st.form("student_form"):
    full_name = st.text_input("Full Name")
    skills = st.text_area("Your Skills (comma separated)").lower()
    location = st.text_input("Preferred Location").lower()
    experience = st.text_input("Experience (if any)").lower()
    sector = st.text_input("Preferred Sector").lower()
    student_percent = st.number_input("Enter your percentage", min_value=0, max_value=100, value=70)

    submitted = st.form_submit_button("Find My Internships")

    if submitted:
        if internships:
            matched_internships = []
            for i in internships:
                # Eligibility based on percentage
                if student_percent >= i.get("MinPercent", 0) if "MinPercent" in i else 0:
                    # Basic skill matching
                    reqs = i.get("Requirements", "").lower()
                    skill_matches = sum(1 for s in skills.split(",") if s.strip() in reqs)
                    sector_match = sector in i.get("Sector", "").lower()
                    total_matches = skill_matches + (1 if sector_match else 0)
                    # Calculate a simple matching percentage
                    match_percentage = min(100, total_matches * 25)  # 4 matches = 100%
                    i["MatchPercent"] = match_percentage
                    matched_internships.append(i)

            if matched_internships:
                # Sort by highest matching percentage
                matched_internships.sort(key=lambda x: x["MatchPercent"], reverse=True)
                st.success(f"{full_name}, here are your matched internships ranked by relevance:")
                for i in matched_internships:
                    st.write(f"- **{i['Title']}** at {i['Location']} ({i['Sector']}) | Match: {i['MatchPercent']}% | Stipend: ₹{i['Stipend']}")
            else:
                st.warning("No internships match your profile based on eligibility & skills/sector.")
        else:
            st.warning("No internships available currently. Please check back later.")
