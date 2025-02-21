import streamlit as st
from planner import study_planner_tab
from pdf_chatbot import pdf_chatbot_tab
from task_tracker import task_tracker_tab

# Main App
def main():
    st.set_page_config(page_title="Study Assistant", layout="wide")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Study Planner", "Task Tracker","PDF Chatbot"])

    # Study Planner Tab
    with tab1:
        study_planner_tab()

    # Tasks Tracker Tab
    with tab2:
        task_tracker_tab()

    # PDF Chatbot Tab
    with tab3:
        pdf_chatbot_tab()

if __name__ == "__main__":
    main()