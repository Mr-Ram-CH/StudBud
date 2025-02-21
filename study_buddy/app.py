import streamlit as st
from planner import study_planner_tab
from pdf_chatbot import pdf_chatbot_tab

# Main App
def main():
    st.set_page_config(page_title="Study Assistant", layout="wide")

    # Create tabs
    tab1, tab2 = st.tabs(["Study Planner", "PDF Chatbot"])

    # Study Planner Tab
    with tab1:
        study_planner_tab()

    # PDF Chatbot Tab
    with tab2:
        pdf_chatbot_tab()

if __name__ == "__main__":
    main()