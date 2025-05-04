import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import base64

# Optional PDF export support
try:
    from fpdf import FPDF
    pdf_enabled = True
except ImportError:
    pdf_enabled = False

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="AI Startup Co-Founder Assistant", layout="centered")
st.markdown("<h1 style='text-align: center;'>🚀 AI Startup Co-Founder Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Turn your raw idea into a validated AI startup blueprint</p>", unsafe_allow_html=True)
st.markdown("---")

# Input layout
col1, col2 = st.columns([3, 1])
with col1:
    startup_idea = st.text_area("📝 Describe your AI startup idea:", height=200)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("🚀 Run Assistant")

# Sidebar module toggles
st.sidebar.markdown("### 🧭 Modules to Explore")
run_summary = st.sidebar.checkbox("💡 Idea Summary", value=True)
run_validation = st.sidebar.checkbox("🔍 Problem Validation")
run_persona = st.sidebar.checkbox("👤 Target User Persona")
run_ai_fit = st.sidebar.checkbox("🤖 AI Use Case Fit")
run_mvp = st.sidebar.checkbox("🛠️ MVP Feature List")
run_monetization = st.sidebar.checkbox("💸 Monetization Options")

# Result storage
results = {}

# Unified OpenAI call function
def get_response(prompt, system_message, max_tokens=400):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Run modules on button click
if run:
    if not startup_idea.strip():
        st.warning("Please enter your startup idea first.")
    else:
        with st.spinner("Thinking..."):

            if run_summary:
                st.subheader("💡 Idea Summary")
                content = get_response(
                    f"Rewrite the following startup idea clearly and concisely:\n\n{startup_idea}",
                    "You are a helpful AI startup advisor.",
                    max_tokens=300
                )
                edited = st.text_area("✏️ Edit Summary", value=content, height=200)
                results["Idea Summary"] = edited
                st.markdown("---")

            if run_validation:
                st.subheader("🔍 Problem Validation")
                content = get_response(
                    f"Validate if the following startup idea solves a real, significant problem:\n\n{startup_idea}",
                    "You are a helpful startup mentor who validates ideas."
                )
                edited = st.text_area("✏️ Edit Validation", value=content, height=200)
                results["Problem Validation"] = edited
                st.markdown("---")

            if run_persona:
                st.subheader("👤 Target User Persona")
                content = get_response(
                    f"Generate a user persona for this startup idea:\n\n{startup_idea}",
                    "You are a product strategist who creates detailed user personas."
                )
                edited = st.text_area("✏️ Edit Persona", value=content, height=200)
                results["Target User Persona"] = edited
                st.markdown("---")

            if run_ai_fit:
                st.subheader("🤖 AI Use Case Fit")
                content = get_response(
                    f"Is this idea a good use case for AI? If so, which techniques apply?\n\n{startup_idea}",
                    "You are an AI expert who evaluates startup ideas."
                )
                edited = st.text_area("✏️ Edit AI Fit", value=content, height=200)
                results["AI Use Case Fit"] = edited
                st.markdown("---")

            if run_mvp:
                st.subheader("🛠️ MVP Feature List")
                content = get_response(
                    f"Create a lean MVP feature roadmap for this idea:\n\n{startup_idea}",
                    "You are a product manager defining MVP features."
                )
                edited = st.text_area("✏️ Edit MVP Features", value=content, height=200)
                results["MVP Feature List"] = edited
                st.markdown("---")

            if run_monetization:
                st.subheader("💸 Monetization Options")
                content = get_response(
                    f"Suggest 3 monetization models for this AI startup:\n\n{startup_idea}",
                    "You are a startup monetization strategist."
                )
                edited = st.text_area("✏️ Edit Monetization", value=content, height=200)
                results["Monetization Options"] = edited
                st.markdown("---")

# Export options
if results:
    st.markdown("## 📥 Export Your Startup Report")

    # Markdown
    markdown_text = "# 🚀 AI Startup Co-Founder Assistant Report\n\n"
    for section, content in results.items():
        markdown_text += f"## {section}\n\n{content}\n\n"
    st.download_button("📄 Download Markdown Report", data=markdown_text, file_name="startup_report.md", mime="text/markdown")

    # JSON
    json_data = json.dumps(results, indent=2)
    st.download_button("💾 Download JSON", data=json_data, file_name="startup_data.json", mime="application/json")

    # PDF
    if pdf_enabled:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for section, content in results.items():
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(0, 10, section)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, content)
            pdf.ln()
        pdf_output = "startup_report.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as f:
            b64_pdf = base64.b64encode(f.read()).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="startup_report.pdf">📄 Download PDF Report</a>', unsafe_allow_html=True)
    else:
        st.info("🧱 PDF export requires `fpdf`. Install it via `pip install fpdf`.")
