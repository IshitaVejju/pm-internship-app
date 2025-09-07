# PM Internship Smart Allocation — Demo (Streamlit)

This is a **ready-to-run prototype** for SIH Problem #25033.
It includes:
- `students.csv` (dummy applicants)
- `internships.csv` (dummy PM Internship slots)
- `app.py` (Streamlit web app)
- `requirements.txt`

---

## 0) Prerequisites
- **Python 3.9+** installed

Check version:
```
python --version
```
or
```
python3 --version
```

---

## 1) Create a project folder
Open Terminal / Command Prompt, then:
```
mkdir pm_internship_smart_allocation_demo
```
```
cd pm_internship_smart_allocation_demo
```

> Copy these four files into this folder: `app.py`, `students.csv`, `internships.csv`, `requirements.txt`

---

## 2) (Optional) Create a virtual environment
Windows:
```
python -m venv .venv
```
```
.venv\Scripts\activate
```
macOS / Linux:
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```

---

## 3) Install dependencies
```
pip install -r requirements.txt
```

If that fails, try:
```
pip install streamlit pandas scikit-learn
```

---

## 4) Run the app
```
streamlit run app.py
```

You will see:
```
  Local URL: http://localhost:8501
```
Open that link in your browser.

---

## 5) Demo Flow (exact steps you will perform on stage)

**A. Student Portal**
1. Click the **"🎓 Student Portal"** tab at the top.
2. In **Full Name**, type: `Aditi Sharma` (exact spacing as shown).
3. In **Your Skills (comma separated)**, paste exactly:  
   `Python, Machine Learning, Data Analysis`
4. In **Current City/District**, type: `Hyderabad`
5. In **Preferred Sector**, type: `AI/ML`
6. Click on the button **"🔎 Find Internships"**.
7. A table appears titled **"Top N recommendations"** showing columns: `Title, Sector, Location, Stipend, Capacity, MatchScore`.
8. Speak one line: *“This shows student-side recommendations ranked by AI similarity with boosts for preference and location.”*

**B. Admin Portal**
1. Click the **"🛠 Admin Portal"** tab.
2. Scroll to see **Applicants (Dummy Data)** and **Internship Pool** tables.
3. On the **left sidebar**, set the following sliders (for the demo):  
   - *Preference Boost*: `10`  
   - *Location Boost*: `8`  
   - *Skill Match Weight (%)*: `80`  
   - *CGPA Weight (%)*: `10`  
   - *Enable Rural-first balancing*: **checked**  
   - *Target Rural % (approx.)*: `30`
4. Click **"🚀 Run Auto-Allocation"**.
5. A table appears showing columns like: `Student, Category, CGPA, Allocated Internship, Sector, Location, Stipend, MatchScore`.
6. Mention: *“Capacity is respected; once an internship’s seats are used, the next best fit is chosen.”*
7. Show the **Summary** table by sector.

**C. Insights**
1. Click the **"📊 Insights"** tab.
2. Read out the counters and the **Capacity by Sector** table.

---

## 6) What to say (script)
- *“We built a **functional prototype** of an AI-based internship allocator for the PM Internship Scheme.”*
- *“Students get **top-N recommendations** with match scores, stipend, and location. Admins can **auto-allocate** with fairness toggles (rural-first balancing).”*
- *“This is **scalable** and **transparent**. We can integrate reservation policies and APIs in future work.”*

---

## 7) Customizing data
Open `students.csv` and `internships.csv` in Excel / Google Sheets and edit rows.  
**Keep the column headers the same**. Do not remove required columns.

---

## 8) Troubleshooting
- If Streamlit doesn’t open automatically, copy and paste the **Local URL** into your browser.
- If `sklearn` install fails, update pip:  
  `python -m pip install --upgrade pip`
- If fonts look big/small, adjust Zoom level in your browser (`Ctrl + +` / `Ctrl + -`).

---

## 9) Packaging (optional)
To freeze versions:
```
pip freeze > requirements.txt
```

To run again later:
```
pip install -r requirements.txt
streamlit run app.py
```

---

### Good luck! You now have a **presentable web demo** for your hackathon.
