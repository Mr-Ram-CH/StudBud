import streamlit as st
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def task_tracker_tab():
    st.header("📋 Study Task Tracker")

    # Initialize session state for tasks
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

    # Add a new task
    new_task = st.text_input("Add a new task:")
    if st.button("Add Task") and new_task:
        st.session_state.tasks.append({"task": new_task, "status": "Pending"})
        save_tasks(st.session_state.tasks)

    st.subheader("Your Tasks")

    # Display tasks
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        col1.write(f"{i+1}. {task['task']}")

        # Task status
        status = col2.selectbox(
            "Status",
            ["Pending", "In Progress", "Completed"],
            index=["Pending", "In Progress", "Completed"].index(task["status"]),
            key=f"status_{i}"
        )
        if status != task["status"]:
            if col2.button("Save Status", key=f"save_status_{i}"):
                st.session_state.tasks[i]["status"] = status
                save_tasks(st.session_state.tasks)

        # Edit task
        if col3.button("Edit", key=f"edit_{i}"):
            st.session_state.edit_index = i  # Store the task index being edited

        # Delete task
        if col4.button("Delete", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks(st.session_state.tasks)
            st.rerun()  # Rerun to refresh the UI

    # Task editing modal
    if "edit_index" in st.session_state:
        edit_index = st.session_state.edit_index
        task_to_edit = st.session_state.tasks[edit_index]
        updated_task = st.text_input(
            f"Edit Task {edit_index + 1}",
            task_to_edit["task"],
            key=f"edit_task_{edit_index}"
        )
        if st.button("Save Changes"):
            st.session_state.tasks[edit_index]["task"] = updated_task
            save_tasks(st.session_state.tasks)
            del st.session_state.edit_index  # Close the edit modal
            st.rerun()  # Rerun to refresh the UI

    # Progress tracker
    completed_tasks = sum(1 for task in st.session_state.tasks if task["status"] == "Completed")
    total_tasks = len(st.session_state.tasks)

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
        st.progress(progress / 100)
        st.write(f"### Progress: {completed_tasks}/{total_tasks} tasks completed ({progress}%)")
    else:
        st.write("No tasks added yet.")