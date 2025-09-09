import streamlit as st
from time import sleep

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="भारत CareerAI", page_icon="📚", layout="wide")

# ---------- HEADER ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        background: linear-gradient(to right, #FF9933, #000080, #138808);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        font-size: 16px;
        color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown('<div class="main-title">भारत CareerAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Empowering Indian Talent • स्मार्ट करियर मार्गदर्शन</div>', unsafe_allow_html=True)
with col2:
    st.success("🌏 Made in India")

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🎯 Internship Finder", "🚀 Career Advisor"])

# ---------- SAMPLE DATA ----------
internships = [
    {
        "id": "I101",
        "title": "AI Research Intern",
        "sector": "Artificial Intelligence",
        "location": "Delhi",
        "requirements": "Python, AI, Machine Learning, Data Analysis",
        "stipend": 8000,
        "capacity": 5,
        "minPercent": 70
    },
    {
        "id": "I102",
        "title": "Data Science Intern",
        "sector": "Information Technology",
        "location": "Hyderabad",
        "requirements": "Python, Data Analysis, Machine Learning",
        "stipend": 9000,
        "capacity": 6,
        "minPercent": 75
    },
    {
        "id": "I103",
        "title": "Digital Marketing Intern",
        "sector": "Marketing & Advertising",
        "location": "Mumbai",
        "requirements": "SEO, Social Media, Google Analytics",
        "stipend": 6000,
        "capacity": 4,
        "minPercent": 65
    },
    {
        "id": "I104",
        "title": "Blockchain Development Intern",
        "sector": "Information Technology",
        "location": "Bangalore",
        "requirements": "Blockchain, Python, Smart Contracts",
        "stipend": 8000,
        "capacity": 3,
        "minPercent": 70
    },
    {
        "id": "I105",
        "title": "Healthcare Policy Intern",
        "sector": "Healthcare",
        "location": "Chennai",
        "requirements": "Healthcare, Policy Analysis, Communication",
        "stipend": 8000,
        "capacity": 5,
        "minPercent": 65
    }
]

skill_suggestions = {
    "Software Engineer": ["JavaScript", "Python", "React", "Node.js", "Docker", "AWS", "Git", "SQL", "MongoDB", "TypeScript"],
    "Data Scientist": ["Python", "R", "Machine Learning", "SQL", "Tableau", "TensorFlow", "Statistics", "pandas", "scikit-learn", "Jupyter"],
    "Product Manager": ["Agile", "Scrum", "Analytics", "User Research", "Roadmapping", "A/B Testing", "Wireframing", "SQL", "JIRA", "Stakeholder Management"],
    "UX Designer": ["Figma", "Adobe XD", "Sketch", "User Research", "Prototyping", "Wireframing", "Usability Testing", "Design Systems", "HTML/CSS", "Information Architecture"],
    "Marketing Manager": ["Google Analytics", "SEO", "Content Marketing", "Social Media", "Email Marketing", "PPC", "CRM", "A/B Testing", "Brand Management", "Marketing Automation"]
}


# ---------- INTERNSHIP FINDER ----------
with tab1:
    st.subheader("Student Profile")
    name = st.text_input("Full Name")
    skills = st.text_area("Your Skills (comma separated)", placeholder="Python, Machine Learning, Data Analysis")
    percent = st.number_input("Percentage", 0, 100, 70)
    location = st.text_input("Preferred Location")
    sector = st.text_input("Preferred Sector")

    if st.button("🔍 Find My Internships"):
        if not name or not skills:
            st.warning("⚠️ Please enter your name and skills.")
        else:
            with st.spinner("AI is finding best matches for you..."):
                sleep(2)
                user_skills = [s.strip().lower() for s in skills.split(",") if s.strip()]
                matches = []
                for internship in internships:
                    if percent >= internship["minPercent"]:
                        reqs = internship["requirements"].lower()
                        skill_matches = sum(1 for s in user_skills if s in reqs)
                        loc_match = 20 if location and location.lower() in internship["location"].lower() else 0
                        sec_match = 30 if sector and sector.lower() in internship["sector"].lower() else 0
                        match_score = min(100, (skill_matches * 20) + sec_match + loc_match + 30)
                        if match_score > 30:
                            internship["matchScore"] = match_score
                            matches.append(internship)

                matches = sorted(matches, key=lambda x: x["matchScore"], reverse=True)

                if not matches:
                    st.info("No matching internships found. Try updating your profile.")
                else:
                    for idx, m in enumerate(matches, 1):
                        with st.container():
                            st.markdown(f"### #{idx} {m['title']} ({m['matchScore']}%)")
                            st.write(f"**Sector:** {m['sector']}")
                            st.write(f"**Location:** {m['location']}")
                            st.write(f"**Requirements:** {m['requirements']}")
                            st.write(f"**Stipend:** ₹{m['stipend']} per month")
                            st.divider()


# ---------- CAREER ADVISOR ----------
with tab2:
    st.subheader("Career Advisor")
    target_role = st.text_input("🎯 Target Role", placeholder="e.g., Data Scientist")
    experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior"])
    user_skills = st.text_area("Your Current Skills", placeholder="Python, SQL, Statistics...")

    if st.button("✨ Get Career Suggestions"):
        if not target_role or not user_skills:
            st.warning("⚠️ Please enter target role and skills.")
        else:
            with st.spinner("Analyzing your profile..."):
                sleep(2)
                current_skills = [s.strip().lower() for s in user_skills.split(",") if s.strip()]
                required_skills = [s.lower() for s in skill_suggestions.get(target_role, [])]
                missing = [s for s in required_skills if s not in current_skills]

                suggestions = [
                    {
                        "title": f"Master {missing[0] if missing else 'Advanced Programming'}",
                        "priority": "High",
                        "timeline": "3-6 months"
                    },
                    {
                        "title": f"Develop {missing[1] if len(missing) > 1 else 'Communication'} Skills",
                        "priority": "High",
                        "timeline": "2-4 months"
                    },
                    {
                        "title": f"Build Portfolio in {missing[2] if len(missing) > 2 else 'Your Domain'}",
                        "priority": "Medium",
                        "timeline": "1-3 months"
                    },
                    {
                        "title": "Industry Networking & Visibility",
                        "priority": "Medium",
                        "timeline": "Ongoing"
                    },
                    {
                        "title": f"Gain {'Internship' if experience == 'Entry' else 'Leadership'} Experience",
                        "priority": "Low",
                        "timeline": "6-12 months"
                    }
                ]

                for sug in suggestions:
                    color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[sug["priority"]]
                    st.markdown(f"### {color} {sug['title']}")
                    st.write(f"- **Priority:** {sug['priority']}")
                    st.write(f"- **Timeline:** {sug['timeline']}")
                    st.divider()
