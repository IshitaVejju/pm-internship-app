# PM Internship Smart Allocation — Streamlit Prototype
# Run: streamlit run app.py

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="PM Internship Smart Allocation", layout="wide")

# ---------------- UI THEME + SPACING ----------------
# (Minimal CSS to keep spacing consistent for your demo)
st.markdown(
    """
    <style>
    .small-note { font-size: 0.9rem; opacity: 0.85; }
    .pad-y { padding-top: 8px; padding-bottom: 8px; }
    .card { padding: 16px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    students = pd.read_csv("students.csv")
    internships = pd.read_csv("internships.csv")
    return students, internships

students_df, internships_df = load_data()

st.title("🇮🇳 PM Internship Smart Allocation (Prototype)")
st.write("")
st.write("This demo matches **students** to **PM Internship opportunities** using a simple AI similarity engine with skill, preference, and location boosts.")

st.divider()

# ---------------- Sidebar Controls ----------------
with st.sidebar:
    st.header("⚙️ Matching Controls")
    top_n = st.number_input("Show Top-N Recommendations", min_value=1, max_value=10, value=3, step=1)
    boost_pref = st.slider("Preference Boost (per exact sector match)", 0, 30, 10)
    boost_loc = st.slider("Location Boost (same city/district)", 0, 30, 8)
    skill_weight = st.slider("Skill Match Weight (%)", 10, 100, 80)
    cgpa_weight = st.slider("CGPA Weight (%)", 0, 50, 10)
    # Normalize later so the total influence remains interpretable

    st.subheader("🎯 Fair Allocation (Admin)")
    use_fairness = st.checkbox("Enable Rural-first balancing", value=True)
    target_rural_pct = st.slider("Target Rural % (approx.)", 0, 100, 30, step=5)

# ---------------- Utility: compute score ----------------
def compute_recommendation_scores(student_row, internships_df):
    """Return a copy of internships_df with a MatchScore column."""
    vec = TfidfVectorizer()
    # Fit on one student + all internship requirements
    combined = [str(student_row["Skills"])] + internships_df["Requirements"].astype(str).tolist()
    tfidf = vec.fit_transform(combined)
    sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()  # 0..1

    df = internships_df.copy()
    # Base from skill similarity -> convert to percent
    df["SkillMatch"] = (sim * 100.0)

    # Preference boost
    df["PrefBoost"] = df["Sector"].apply(lambda x: boost_pref if str(student_row["Preference"]).strip().lower() in str(x).strip().lower() else 0)
    # Location boost (city/district exact string match for demo)
    df["LocBoost"] = df.apply(lambda r: boost_loc if str(student_row["Location"]).strip().lower() in [str(r["Location"]).strip().lower(), str(r["District"]).strip().lower()] else 0, axis=1)

    # CGPA contribution as a flat addition scaled to 0..100 * weight
    cgpa = float(student_row.get("CGPA", 0))
    # Normalize cgpa (10-point scale) to 0..100
    cgpa_pct = min(max((cgpa/10.0)*100.0, 0), 100)

    # Combine using weights
    sw = skill_weight/100.0
    cw = cgpa_weight/100.0
    # Remaining weight proportion goes to boosts implicitly
    base = df["SkillMatch"] * sw + cgpa_pct * cw
    df["MatchScore"] = base + df["PrefBoost"] + df["LocBoost"]
    return df.sort_values("MatchScore", ascending=False)

# ---------------- Tabs Layout ----------------
tab1, tab2, tab3 = st.tabs(["🎓 Student Portal", "🛠 Admin Portal", "📊 Insights"])

# ---------------- STUDENT PORTAL ----------------
with tab1:
    st.subheader("Student Portal")
    st.write('<div class="small-note">Fill the form and click **Find Internships** to see your top matches.</div>', unsafe_allow_html=True)
    st.write("")

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1])
    with c1:
        name = st.text_input("Full Name", placeholder="e.g., Aditi Sharma")
    with c2:
        skills = st.text_area("Your Skills (comma separated)", height=90, placeholder="Python, Machine Learning, Data Analysis")
    with c3:
        location = st.text_input("Current City/District", placeholder="e.g., Ranchi")
    with c4:
        pref = st.text_input("Preferred Sector", placeholder="e.g., AI/ML / Software / Health / Electronics / Media")

    st.write("")
    find_btn = st.button("🔎 Find Internships", type="primary", use_container_width=True)

    st.write("")
    st.write("")

    if find_btn:
        if not skills.strip():
            st.error("Please enter your skills to get recommendations.")
        else:
            # Make a temporary student row
            temp_student = {
                "Skills": skills,
                "Location": location if location else "",
                "Preference": pref if pref else "",
                "CGPA": 8.0,  # default demo value
            }
            recs = compute_recommendation_scores(temp_student, internships_df)
            st.success(f"Top {top_n} recommendations for **{name or 'Student'}**")
            st.write("")
            st.dataframe(recs[["Title","Sector","Location","Stipend","Capacity","MatchScore"]].head(top_n), use_container_width=True)

            st.write("")
            st.info("Tip: In a full system, students could now **apply** to selected internships; this prototype focuses on the matching engine.")

# ---------------- ADMIN PORTAL ----------------
with tab2:
    st.subheader("Admin Portal")
    st.write('<div class="small-note">Use the controls in the left sidebar to tune matching weights and fairness.</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown("#### Applicants (Dummy Data)")
    st.dataframe(students_df, use_container_width=True, height=240)

    st.markdown("#### Internship Pool")
    st.dataframe(internships_df, use_container_width=True, height=240)

    st.write("")
    run_alloc = st.button("🚀 Run Auto-Allocation", type="primary", use_container_width=True)
    st.write("")

    if run_alloc:
        # Optional fairness: place rural students first to meet target proportion
        df_students = students_df.copy()
        if use_fairness:
            rural = df_students[df_students["Category"].str.lower()=="rural"]
            urban = df_students[df_students["Category"].str.lower()!="rural"]
            # Target number of rural allocations
            target = int(round((target_rural_pct/100.0) * len(df_students)))
            # Order: first min(target, len(rural)) rural, then remaining mix
            ordered = pd.concat([rural.head(target), pd.concat([rural.tail(max(len(rural)-target,0)), urban])], ignore_index=True)
            df_students = ordered
        # Else keep original order

        remaining_capacity = internships_df.set_index("InternshipID")["Capacity"].to_dict()

        allocations = []
        for _, s in df_students.iterrows():
            scored = compute_recommendation_scores(s, internships_df)
            # Pick best with remaining capacity
            chosen_row = None
            for _, row in scored.iterrows():
                iid = row["InternshipID"]
                if remaining_capacity.get(iid,0) > 0:
                    chosen_row = row
                    remaining_capacity[iid] -= 1
                    break
            if chosen_row is not None:
                allocations.append({
                    "StudentID": s["StudentID"],
                    "Student": s["Name"],
                    "Category": s["Category"],
                    "CGPA": s["CGPA"],
                    "Allocated Internship": chosen_row["Title"],
                    "Sector": chosen_row["Sector"],
                    "Location": chosen_row["Location"],
                    "Stipend": chosen_row["Stipend"],
                    "MatchScore": round(chosen_row["MatchScore"],2)
                })
            else:
                allocations.append({
                    "StudentID": s["StudentID"],
                    "Student": s["Name"],
                    "Category": s["Category"],
                    "CGPA": s["CGPA"],
                    "Allocated Internship": "— No Capacity —",
                    "Sector": "",
                    "Location": "",
                    "Stipend": "",
                    "MatchScore": 0
                })

        alloc_df = pd.DataFrame(allocations)
        st.success("Auto-allocation complete.")
        st.dataframe(alloc_df, use_container_width=True, height=300)

        st.write("")
        st.markdown("#### Summary")
        by_sector = alloc_df.groupby("Sector", dropna=False)["StudentID"].count().reset_index(name="Allocated Count")
        st.dataframe(by_sector, use_container_width=True)

# ---------------- INSIGHTS ----------------
with tab3:
    st.subheader("Insights")
    st.markdown("This section summarizes the current internship pool and applicants.")
    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Students", len(students_df))
    with c2:
        st.metric("Total Internships", len(internships_df))
    with c3:
        st.metric("Total Slots (Capacity)", int(internships_df["Capacity"].sum()))

    st.write("")
    st.markdown("**Internship Capacity by Sector**")
    cap_by_sector = internships_df.groupby("Sector")["Capacity"].sum().reset_index().sort_values("Capacity", ascending=False)
    st.dataframe(cap_by_sector, use_container_width=True)

st.divider()
st.caption("Prototype for SIH Problem #25033 — AI Smart Allocation for PM Internship • Built with Streamlit + pandas + scikit-learn")
