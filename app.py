import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=api_key)

def get_gemini_response(input_prompt, resume_content, job_description):
    
    model = genai.GenerativeModel('gemini-2.5-flash') 
    full_prompt = f"{input_prompt}\n\nJob Description: {job_description}\n\nResume Content: {resume_content}"
    response = model.generate_content(full_prompt)
    return response.text

def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

# --- Streamlit UI Design ---
st.set_page_config(page_title="AI Resume Analyzer Pro", layout="wide")

# CSS 
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3em; 
        background-color: #0d6efd; 
        color: white;
        font-weight: bold;
    }
    .stTextArea textarea { border-radius: 10px; }
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 20px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI-Powered Resume Analyzer")
st.write("Optimize your resume for Applicant Tracking Systems (ATS).")

col1, col2 = st.columns([1, 1])

with col1:
    jd = st.text_area("📋 Job Description", placeholder="Paste the job requirements here...", height=300)

with col2:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf", help="Please upload a PDF file")
    if uploaded_file:
        st.success("Resume uploaded successfully!")

# Analyze Button
submit = st.button("Analyze Resume")

# AI Prompt
input_prompt_template = """
As an experienced Technical Human Resource Manager and ATS (Applicant Tracking System) expert, 
your task is to evaluate the provided resume against the given job description. 

Please provide the following analysis in a professional format:
1. **Match Percentage:** Provide a percentage (%) indicating how well the resume matches the job.
2. **Key Missing Skills:** Identify specific keywords or technical skills mentioned in the JD that are missing from the resume.
3. **Professional Summary:** A brief overview of the candidate's suitability.
4. **Actionable Suggestions:** Provide 3-5 specific tips to improve the resume for this specific role.
5. **Verdict:** A final "Fit" or "Not Fit" recommendation.
"""

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner('Analyzing your resume against the JD...'):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                response_text = get_gemini_response(input_prompt_template, resume_text, jd)
                
                st.divider()
                st.subheader("📊 Analysis Report")
                st.markdown(response_text)
                
                # --- Download Section ---
                st.download_button(
                    label="📥 Download Analysis Report",
                    data=response_text,
                    file_name="ATS_Analysis_Report.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a resume and provide a job description to proceed.")

# --- Footer & Copyright Tag ---
st.markdown("""
    <div class="footer">
        <hr>
        <p>© 2026 Madhuranga Wijesooriya | All Rights Reserved | Powered by Gemini 2.5 Flash</p>
    </div>

    """, unsafe_allow_html=True)
