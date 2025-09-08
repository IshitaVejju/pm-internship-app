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
    # Updated paths to handle different possible locations
    possible_paths = [
        "internships.csv",  # Same directory as app.py
        "data/internships.csv",  # In data folder
        "data /internships.csv",  # Handle space in folder name
        Path.cwd() / "internships.csv",
        Path.cwd() / "data" / "internships.csv",
        Path.cwd() / "data " / "internships.csv",  # Handle space in folder name
        Path(__file__).parent / "internships.csv",
        Path(__file__).parent / "data" / "internships.csv",
        Path(__file__).parent / "data " / "internships.csv"  # Handle space in folder name
    ]
    
    csv_path = None
    for path in possible_paths:
        try:
            path_obj = Path(path)
            if path_obj.exists():
                csv_path = path_obj
                break
        except Exception:
            continue

    if csv_path is None:
        # If no file found, create sample data
        st.warning("⚠️ Internships CSV not found. Using sample data for demo.")
        return create_sample_data()

    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            st.warning(f"⚠️ CSV file is empty: {csv_path}")
            return create_sample_data()
        return df.to_dict("records")
    except Exception as e:
        st.error(f"❌ Error reading CSV at {csv_path}: {e}")
        return create_sample_data()

def create_sample_data():
    """Create sample internship data if CSV is not found"""
    sample_data = [
        {
            "InternshipID": "I101",
            "Title": "AI Research Intern",
            "Sector": "Artificial Intelligence",
            "Location": "Delhi",
            "Requirements": "Python, AI, Machine Learning, Data Analysis",
            "Stipend": 8000,
            "Capacity": 5,
            "District": "Delhi",
            "MinPercent": 70
        },
        {
            "InternshipID": "I102",
            "Title": "Data Analyst Intern",
            "Sector": "Information Technology",
            "Location": "Bangalore",
            "Requirements": "SQL, Excel, Data Visualization, Statistics",
            "Stipend": 7000,
            "Capacity": 8,
            "District": "Bangalore",
            "MinPercent": 65
        },
        {
            "InternshipID": "I103",
            "Title": "Marketing Strategy Intern",
            "Sector": "Marketing & Advertising",
            "Location": "Mumbai",
            "Requirements": "Marketing, Content Writing, SEO, Social Media",
            "Stipend": 6000,
            "Capacity": 6,
            "District": "Mumbai",
            "MinPercent": 60
        },
        {
            "InternshipID": "I104",
            "Title": "Healthcare Policy Intern",
            "Sector": "Healthcare",
            "Location": "Hyderabad",
            "Requirements": "Healthcare, Policy Analysis, Communication",
            "Stipend": 8000,
            "Capacity": 5,
            "District": "Hyderabad",
            "MinPercent": 65
        },
        {
            "InternshipID": "I105",
            "Title": "Data Science Intern",
            "Sector": "Information Technology",
            "Location": "Hyderabad",
            "Requirements": "Python, Data Analysis, Machine Learning",
            "Stipend": 9000,
            "Capacity": 6,
            "District": "Hyderabad",
            "MinPercent": 75
        }
    ]
    return sample_data

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
            except (ValueError, TypeError):
                min_percent = 0

            # Eligibility check
            if student_percent >= min_percent:
                # Skill matching
                requirements = str(intern.get("Requirements", "")).lower()
                user_skills = [s.strip() for s in skills.split(",") if s.strip()]
                skill_matches = sum(1 for s in user_skills if s in requirements)

                # Location matching
                intern_location = str(intern.get("Location", "")).lower()
                location_match = 1 if preferred_location and preferred_location in intern_location else 0

                # Sector matching
                sector_match = 1 if preferred_sector and preferred_sector in str(intern.get("Sector", "")).lower() else 0

                # Calculate match score (improved weighted approach)
                base_score = min(100, (skill_matches * 30) + (sector_match * 40) + (location_match * 30))
                intern["MatchPercent"] = base_score
                matched_internships.append(intern)

        # ---------- DISPLAY RESULTS ----------
        if matched_internships:
            matched_internships.sort(key=lambda x: x["MatchPercent"], reverse=True)
            st.success(f"✅ {full_name}, here are your top internship matches:")
            
            # Display as a table for better presentation
            display_data = []
            for i in matched_internships[:10]:  # Show top 10 matches
                display_data.append({
                    "Title": i['Title'],
                    "Sector": i['Sector'],
                    "Location": i['Location'],
                    "Stipend": f"₹{i['Stipend']}",
                    "Capacity": i['Capacity'],
                    "Match %": f"{i['MatchPercent']}%"
                })
            
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, use_container_width=True)
            
            st.info(f"📊 Found {len(matched_internships)} matching internships based on your profile!")
        else:
            st.warning("⚠️ No internships match your profile based on eligibility & skills/sector.")
    else:
        st.error("❌ No internships available currently. Please check back later.")

# ---------- DEBUG INFO ----------
with st.expander("🔍 Debug Information (for developers)"):
    st.write(f"Total internships loaded: {len(internships)}")
    if internships:
        st.write("Sample internship data:")
        st.json(internships[0])
    
    # Show current working directory and file structure
    st.write(f"Current working directory: {Path.cwd()}")
    st.write("Files in current directory:")
    try:
        files = list(Path.cwd().iterdir())
        for file in files[:10]:  # Show first 10 files/folders
            st.write(f"- {file.name} ({'folder' if file.is_dir() else 'file'})")
    except Exception as e:
        st.write(f"Error listing files: {e}")
