import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SmartAssigners",
    page_icon="🧑🏼‍💻",
    layout="centered"
)

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
    """
    Load internships data from CSV safely.
    Returns a list of internship records or an empty list if file is missing.
    """
    possible_paths = [
        Path.cwd() / "data" / "internships.csv",        # common local dev path
        Path(__file__).parent / "data" / "internships.csv"  # if running as a script
    ]
    
    csv_path = None
    for path in possible_paths:
        if path.exists():
            csv_path = path
            break

    if csv_path is None:
        st.error("""
        ⚠️ **Internships data not found!**  
        Please make sure `internships.csv` exists in one of these locations relative to your app:
        1. `./data/internships.csv` (recommended)
        2. Same folder as `app.py` inside a `data` folder  
        You can download or create a CSV with these columns:  
        `InternshipID, Title, Sector, Location, Requirements, Stipend, Capacity, District, MinPercent`
        """)
        return []

    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            st.warning(f"⚠️ CSV file is empty: {csv_path}")
            return []
        return df.to_dict("records")
    except Exception as e:
        st.error(f"❌ Error reading CSV at {csv_path}: {e}")
        return []

internships = load_internships()

# ---------- STUDENT PORTAL ----------
st.subheader("🎓 Student Portal - Find Your Internship Match")

with st.form("student_form"):
    full_name = st.text_input("Full Name")
    skills = st.text_area("Your Skills (comma separated)").lower()
    preferred_location = st.text_input("Preferred Location").lower()
    experience = st.text_input("Experience (if any)").lower()
    preferred_sector = st.text_input("Preferred Sector").lower()
    student_percent = st.number_input("Enter your percentage", min_value=0, max_value=100, value=70)
    submitted = st.form_submit_button("🔍 Find My Internships")

# ---------- MATCHING LOGIC ----------
if submitted:
    if internships:
        matched_internships = []
        for intern in internships:
            try:
                min_percent = int(intern.get("MinPercent", 0))
            except ValueError:
                min_percent = 0

            # Eligibility check
            if student_percent >= min_percent:
                # Skill matching
                requirements = str(intern.get("Requirements", "")).lower()
                skill_matches = sum(1 for s in skills.split(",") if s.strip() in requirements)

                # Sector matching
                sector_match = 1 if preferred_sector in str(intern.get("Sector", "")).lower() else 0

                # Calculate match score (basic weighted approach)
                match_score = min(100, (skill_matches + sector_match) * 25)
                intern["MatchPercent"] = match_score
                matched_internships.append(intern)

        # ---------- DISPLAY RESULTS ----------
        if matched_internships:
            matched_internships.sort(key=lambda x: x["MatchPercent"], reverse=True)
            st.success(f"✅ {full_name}, here are your top internship matches:")
            for i in matched_internships:
                st.write(
                    f"- **{i['Title']}** ({i['Sector']}) at {i['Location']} "
                    f"| 🎯 Match: {i['MatchPercent']}% "
                    f"| 💰 Stipend: ₹{i['Stipend']} "
                    f"| 👥 Capacity: {i['Capacity']}"
                )
        else:
            st.warning("⚠️ No internships match your profile based on eligibility & skills/sector.")
    else:
        st.error("❌ No internships available currently. Please check back later.")
