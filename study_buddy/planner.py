import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from htmlTemplates import study_plan_template
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API key for Google Generative AI not found. Please set it in the .env file.")
genai.configure(api_key=api_key)


def generate_pdf(study_plan, filename="study_plan.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, study_plan)
    pdf.output(filename)
    return filename

# Study Planner Functions
def generate_study_plan(topic, hours, days):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        Create a detailed study plan for the topic: {topic}.
        Total available time: {hours} hours over {days} days.
        Break the plan into daily tasks and include time allocations for each task.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate study plan: {e}")
        return None

# Study Planner Tab
def study_planner_tab():
    st.header("AI Study Planner 📚")
    st.write("Generate a personalized study plan using Gemini AI!")

    # Input fields
    topic = st.text_input("Enter the topic you want to study:")
    days = st.number_input("Number of days:", min_value=1, max_value=30, value=7)

    # Dynamic hours limit: max_value = days * 24
    max_hours = days * 24
    hours = st.number_input(
        "Total hours available:",
        min_value=1,
        max_value=max_hours,  # Dynamic max_value based on days
        value=min(10, max_hours)  # Default value is 10 or max_hours, whichever is smaller
    )

    # Generate study plan
    if st.button("Generate Study Plan"):
        if topic:
            with st.spinner("Generating your study plan..."):
                study_plan = generate_study_plan(topic, hours, days)
                st.success("Study Plan Generated!")
                st.write(study_plan_template.replace("{{STUDY_PLAN}}", study_plan), unsafe_allow_html=True)
                pdf_buffer = generate_pdf(study_plan)
                st.download_button(
                    label="Download Study Plan as PDF",
                    data=pdf_buffer,
                    file_name="study_plan.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Please enter a topic.")
