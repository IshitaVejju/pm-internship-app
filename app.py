import streamlit as st
import os
import json

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SmartAssigners", page_icon="📚", layout="wide")

# ---------- INDIAN FLAG BACKGROUND ----------
st.markdown(
    """
    <style>
    /* Whole page background in tricolour */
    .stApp {
        background: linear-gradient(to bottom, #FF9933, #FFFFFF, #138808);
    }

    /* White cards for readability */
    .stCard, .stForm, .stTextInput, .stNumberInput, .stTextArea {
        background-color: white !important;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    h2, h3, .stSubheader {
        color: #0b3d0b !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    """
    <div style="text-align:center; font-size:36px; font-weight:bold;
                background:linear-gradient(to right, #FF9933, #FFFFFF, #138808);
                padding:15px; border-radius:10px;">
        SmartAssigners 👩‍💻
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Welcome to **SmartAssigners** 💻 Your Internship Assistant Platform")

# ---------- DATA LOADERS ----------
@st.cache_data
def load_pm_internships():
    """Load official PM Internship Scheme opportunities from data/pm_internships.json"""
    p = os.path.join(os.path.dirname(__file__), "data", "pm_internships.json")
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error reading data/pm_internships.json: {e}")
            return []
    return []

# ---------- SESSION STATE ----------
if "internships" not in st.session_state:
    st.session_state.internships = []  # Runtime-added internships

if "pm_internships" not in st.session_state:
    st.session_state.pm_internships = load_pm_internships()

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 1])

# ---------- ADMIN SECTION ----------
with col1:
    st.subheader("👩‍💼 Admin: Add Internship Opportunity (Runtime)")
    with st.form("admin_form"):
        title = st.text_input("Internship Title")
        company = st.text_input("Company Name")
        min_percent = st.number_input("Minimum % required", min_value=0, max_value=100, value=60)
        submitted = st.form_submit_button("Add Internship")
        if submitted and title and company:
            st.session_state.internships.append({
                "title": title,
                "company": company,
                "min_percent": min_percent
            })
            st.success(f"Added internship: {title} at {company} (Min % {min_percent})")

    if st.session_state.internships:
        st.markdown("### 📌 Current Runtime Internships")
        for i in st.session_state.internships:
            st.markdown(f"- **{i['title']}** at {i['company']} (Min % {i['min_percent']})")

    if st.session_state.pm_internships:
        st.markdown("### 📌 Official PM Internship Opportunities")
        for i in st.session_state.pm_internships:
            st.markdown(f"- **{i['title']}** | {i['company']} | {i.get('location','-')} | "
                        f"{i.get('sector','-')} | Min%: {i['min_percent']} | Vacancies: {i.get('vacancies',1)}")
        st.info("These are official PM Internship Scheme opportunities — fixed from repo (pm_internships.json).")

# ---------- STUDENT SECTION ----------
with col2:
    st.subheader("🎓 Student: Check Eligibility & Get Matched")

    with st.form("student_form"):
        full_name = st.text_input("Full Name")
        skills = st.text_area("Your Skills (comma separated)")
        location = st.text_input("Preferred Location")
        experience = st.text_input("Experience (if any)")
        sector = st.text_input("Preferred Sector")
        student_percent = st.number_input("Enter your percentage", min_value=0, max_value=100, value=70)

        submitted = st.form_submit_button("Find My Internships")

        if submitted:
            eligible = []

            # Check runtime internships
            for i in st.session_state.internships:
                if student_percent >= i["min_percent"]:
                    eligible.append(i)

            # Check PM internships
            for i in st.session_state.pm_internships:
                if student_percent >= i["min_percent"]:
                    eligible.append(i)

            if eligible:
                st.success(f"{full_name}, based on your profile, you are eligible for:")
                for i in eligible:
                    st.write(f"- **{i['title']}** at {i['company']} (Min % {i['min_percent']})")
                
                # Placeholder for AI-based matchmaking
                st.info("🤖 Smart Matchmaking (AI-based) coming soon: "
                        "Comparing your skills, sector & location with both "
                        "**PM Internship Scheme opportunities** and **runtime-added internships**.")
            
            else:
                st.error("😔 Sorry, no internships match your percentage.")
