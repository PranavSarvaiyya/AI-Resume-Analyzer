import streamlit as st
import engine
import pdfplumber

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.title("🚀 AI Resume Analyzer")
st.markdown("Analyze your resume against a Job Description to find missing skills and get AI-powered improvement tips!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Job Description")
    job_desc = st.text_area("Paste the Job Description here", height=250)

with col2:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])
    
    resume_text = ""
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + "\n"
            st.success("Resume uploaded and text extracted successfully!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

if st.button("🔍 Analyze Resume", use_container_width=True):
    if not job_desc.strip():
        st.warning("Please paste the Job Description.")
    elif not resume_text.strip():
        st.warning("Please upload a valid Resume.")
    else:
        with st.spinner("🧠 AI is analyzing your resume... Please wait."):
            # Semantic Match
            semantic_score = engine.get_semantic_match(resume_text, job_desc)
            
            # Hard Skills Analysis
            hard_score, missing_skills, found_skills = engine.get_hard_skills_analysis(resume_text, job_desc)
            
            # Generate Tips
            tips = engine.generate_tips(missing_skills)
            
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Display Scores
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.metric(label="ATS Percentage", value=f"{semantic_score}%")
            st.progress(min(semantic_score / 100, 1.0)) # Ensure it doesn't cross 1.0
            
        with score_col2:
            st.metric(label="Hard Skills Match Percentage", value=f"{hard_score}%")
            st.progress(min(hard_score / 100, 1.0))

        st.markdown("---")
        
        # Display Skills
        skill_col1, skill_col2 = st.columns(2)
        with skill_col1:
            st.subheader("✅ Matched Skills")
            if found_skills:
                # Add nice pill tags or simple comma separated text
                st.markdown(f"**{', '.join([s.title() for s in found_skills])}**")
            else:
                st.info("No matching skills found.")
                
        with skill_col2:
            st.subheader("❌ Missing Skills")
            if missing_skills:
                st.markdown(f"**{', '.join([s.title() for s in missing_skills])}**")
            else:
                st.success("No critical skills missing!")
                
        st.markdown("---")
        
        # Display Tips
        st.subheader("💡 Improvement Tips")
        for tip in tips:
            st.markdown(tip)
