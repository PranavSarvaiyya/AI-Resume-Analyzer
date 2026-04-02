import streamlit as st
import engine
import pdfplumber

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0b1120;
    }
    
    /* Layout styling adjustments */
    header[data-testid="stHeader"] {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    
    /* Navbar Custom HTML styling */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 40px;
        background-color: #0b1120;
        border-bottom: 1px solid #1e293b;
        margin-top: -60px; /* Adjust for default streamlit padding */
    }
    .nav-brand {
        font-size: 1.3rem;
        font-weight: 700;
        color: #00d2ff;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .nav-links {
        display: flex;
        gap: 30px;
    }
    .nav-links a {
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
    }
    .nav-links a.active {
        color: #00d2ff;
        border-bottom: 2px solid #00d2ff;
        padding-bottom: 4px;
    }
    .nav-actions {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .nav-icon {
        color: #94a3b8;
        font-size: 1.2rem;
        cursor: pointer;
    }
    .sign-in-btn {
        background-color: #0edca2;
        color: #000;
        padding: 8px 24px;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    /* Header Section */
    .hero-section {
        text-align: center;
        margin-top: 50px;
        margin-bottom: 60px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 15px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 650px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Customization for text area and file uploader */
    div[data-testid="stTextArea"] label p {
        font-size: 1rem !important;
        font-weight: 700;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stFileUploader"] label p {
        font-size: 1rem !important;
        font-weight: 700;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    div[data-testid="stTextArea"] textarea {
        background-color: #121826;
        border: 1px solid #1e293b;
        border-radius: 10px;
        color: #cbd5e1;
    }
    div[data-baseweb="file-dropzone"] {
        background-color: #121826;
        border: 1px dashed #334155;
        border-radius: 10px;
        padding: 40px 20px;
    }
    
    /* Main Analyze Button */
    .stButton > button {
        background-color: #0bd0d9; /* teal/cyan color matching the image closely */
        color: #000000;
        border: none;
        padding: 8px 30px;
        font-weight: 700;
        border-radius: 8px;
        width: 300px;
        display: block;
        transition: all 0.2s ease;
    }
    .stButton > button p {
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0;
    }
    .stButton > button:hover {
        background-color: #09b8c0; /* darker hover */
        border: none;
        color: #000;
    }
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    
    /* Cards styling */
    .feature-card {
        background-color: #1a2234;
        border: none;
        border-radius: 12px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .feature-icon {
        color: #0bd0d9;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 16px;
    }
    .feature-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .feature-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Footer */
    .footer {
        border-top: 1px solid #1e293b;
        padding-top: 30px;
        margin-top: 60px;
        text-align: center;
        padding-bottom: 20px;
    }
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 15px;
    }
    .footer-links a {
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.85rem;
    }
    .footer-links a:hover {
        color: #cbd5e1;
    }
    .footer-copy {
        color: #64748b;
        font-size: 0.8rem;
    }

</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🚀 AI Resume Analyzer</div>
    <div class="hero-subtitle">Analyze your resume against a Job Description to find missing skills and get<br/>AI-powered improvement tips!</div>
</div>
""", unsafe_allow_html=True)

# Split view for input
col1, space, col2 = st.columns([1, 0.1, 1])

with col1:
    job_desc = st.text_area("📄 JOB DESCRIPTION", placeholder="Paste the Job Description here...", height=280)
    st.markdown("<p style='text-align: right; font-size: 0.75rem; color: #475569; margin-top: -20px; margin-bottom: 30px;'>Supports up to 5,000 characters</p>", unsafe_allow_html=True)

with col2:
    uploaded_file = st.file_uploader("⬆️ UPLOAD RESUME", type=["pdf"])
    
    resume_text = ""
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + "\n"
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# Call to Action Button
col1, col2, col3 = st.columns([3, 2, 3])
with col2:
    analyze_button = st.button("🔍 Analyze Resume", use_container_width=True)

if analyze_button:
    if not job_desc.strip():
        st.warning("Please paste the Job Description.")
    elif not resume_text.strip():
        st.warning("Please upload a valid Resume.")
    else:
        skip1, sp_col, skip2 = st.columns([1, 2, 1])
        with sp_col:
            with st.spinner("🧠 AI is analyzing your resume... Please wait."):
            # Reusing the existing engine API without changes
                semantic_score = engine.get_semantic_match(resume_text, job_desc)
                hard_score, missing_skills, found_skills = engine.get_hard_skills_analysis(resume_text, job_desc)
                tips = engine.generate_tips(missing_skills)
            
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Display Scores
        score_col1, score_col2 = st.columns(2)
        with score_col1:
            st.metric(label="ATS Match Score", value=f"{semantic_score}%")
            st.progress(min(semantic_score / 100, 1.0))
            
        with score_col2:
            st.metric(label="Hard Skills Match", value=f"{hard_score}%")
            st.progress(min(hard_score / 100, 1.0))

        st.markdown("---")
        
        # Display Skills
        skill_col1, skill_col2 = st.columns(2)
        with skill_col1:
            st.subheader("✅ Matched Skills")
            if found_skills:
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

else:
    # Feature Cards Section (Visible initially)
    fc1, fc2, fc3 = st.columns(3)
    
    with fc1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Skill Gap Analysis</div>
            <div class="feature-desc">Instantly identify missing technical and soft skills required for the role.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with fc2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Insights</div>
            <div class="feature-desc">Get semantic recommendations to rephrase your experience for ATS systems.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with fc3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Matching Score</div>
            <div class="feature-desc">A high-fidelity diagnostic score of your alignment with the job profile.</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">API Documentation</a>
    </div>
    <div class="footer-copy">© 2024 Precision Architect AI. Built for the Neon Observatory.</div>
</div>
""", unsafe_allow_html=True)
