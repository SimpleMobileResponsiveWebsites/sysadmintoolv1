import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for tasks if not already done
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "subtasks" not in st.session_state:
    st.session_state.subtasks = {}

if "temp_subtasks" not in st.session_state:
    st.session_state.temp_subtasks = []

# App title
st.title("IT Systems Administrator Project Management Tool")

# Sidebar for task input
st.sidebar.header("Add a New Task")

with st.sidebar.form("task_form"):
    task_title = st.text_input("Task Title", placeholder="Enter task name")
    task_category = st.selectbox(
        "Category",
        [
            "System Maintenance & Support",
            "Network Management",
            "Security & Compliance",
            "User Support & Training",
            "Backup & Disaster Recovery",
            "Project Management & Implementation",
            "Other IT-Related Duties",
        ],
    )
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    task_due_date = st.date_input("Due Date")
    task_assigned_to = st.text_input("Assigned To", placeholder="Enter team member's name")
    task_description = st.text_area("Description", placeholder="Provide task details")

    # Subtask Entry Section
    st.write("### Add Subtasks")
    subtask_title = st.text_input("Subtask Title", placeholder="Enter subtask name")
    if st.button("Add Subtask"):
        if subtask_title:
            st.session_state.temp_subtasks.append({"Subtask Title": subtask_title, "Status": "Pending"})
            st.success(f"Subtask '{subtask_title}' added.")
        else:
            st.error("Subtask Title is required.")

    # Display Current Subtasks
    if st.session_state.temp_subtasks:
        st.write("#### Current Subtasks:")
        for i, subtask in enumerate(st.session_state.temp_subtasks, 1):
            st.write(f"{i}. {subtask['Subtask Title']} - Status: {subtask['Status']}")

    # Submit Task
    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task_title and task_assigned_to:
            new_task = {
                "Title": task_title,
                "Category": task_category,
                "Priority": task_priority,
                "Due Date": task_due_date,
                "Assigned To": task_assigned_to,
                "Description": task_description,
                "Status": "Pending",
                "Created": datetime.now(),
            }
            st.session_state.tasks.append(new_task)
            st.session_state.subtasks[task_title] = st.session_state.temp_subtasks
            st.session_state.temp_subtasks = []  # Clear temporary subtasks
            st.success(f"Task '{task_title}' added successfully with subtasks!")
        else:
            st.error("Task Title and Assigned To are required fields.")

# Main section: Display tasks
st.header("Task Dashboard")

if st.session_state.tasks:
    # Convert tasks to a DataFrame for display
    tasks_df = pd.DataFrame(st.session_state.tasks)

    # Filters
    with st.expander("Filters", expanded=False):
        filter_category = st.multiselect(
            "Filter by Category", options=tasks_df["Category"].unique()
        )
        filter_priority = st.multiselect(
            "Filter by Priority", options=tasks_df["Priority"].unique()
        )
        filter_status = st.multiselect(
            "Filter by Status", options=tasks_df["Status"].unique()
        )

        if filter_category:
            tasks_df = tasks_df[tasks_df["Category"].isin(filter_category)]
        if filter_priority:
            tasks_df = tasks_df[tasks_df["Priority"].isin(filter_priority)]
        if filter_status:
            tasks_df = tasks_df[tasks_df["Status"].isin(filter_status)]

    # Task Table with Editing
    st.subheader("Task Table (Editable)")

    if not tasks_df.empty:
        updated_tasks_df = st.data_editor(
            tasks_df,
            use_container_width=True,
            hide_index=True,
            key="editable_task_table",
        )

        # Save updates back to the session state
        if not updated_tasks_df.equals(tasks_df):
            for index, updated_row in updated_tasks_df.iterrows():
                st.session_state.tasks[index] = updated_row.to_dict()
            st.success("Task updates saved successfully!")
    else:
        st.info("No tasks available to display.")

    # Update task status
    st.subheader("Update Task Status")
    task_titles = tasks_df["Title"].tolist()
    selected_task = st.selectbox("Select Task to Update", ["---"] + task_titles)

    if selected_task != "---":
        new_status = st.radio("Update Status", ["Pending", "In Progress", "Completed"], key="status_radio")
        if st.button("Update Status"):
            for task in st.session_state.tasks:
                if task["Title"] == selected_task:
                    task["Status"] = new_status
                    st.success(f"Task '{selected_task}' updated to '{new_status}'.")

    # Subtasks management
    st.subheader("Manage Subtasks")
    selected_task_for_subtasks = st.selectbox("Select Task to Manage Subtasks", ["---"] + task_titles, key="subtask_select")

    if selected_task_for_subtasks != "---":
        with st.form("subtask_form"):
            subtask_title = st.text_input("Subtask Title", placeholder="Enter subtask name")
            subtask_status = st.selectbox("Subtask Status", ["Pending", "In Progress", "Completed"], key="subtask_status")
            add_subtask = st.form_submit_button("Add Subtask")

            if add_subtask:
                if subtask_title:
                    st.session_state.subtasks[selected_task_for_subtasks].append({
                        "Subtask Title": subtask_title,
                        "Status": subtask_status,
                    })
                    st.success(f"Subtask '{subtask_title}' added to task '{selected_task_for_subtasks}'.")
                else:
                    st.error("Subtask Title is required.")

        st.write(f"### Subtasks for '{selected_task_for_subtasks}':")
        subtasks = st.session_state.subtasks[selected_task_for_subtasks]
        if subtasks:
            for i, subtask in enumerate(subtasks):
                st.write(f"{i + 1}. {subtask['Subtask Title']} - Status: {subtask['Status']}")
        else:
            st.info("No subtasks available for this task.")

else:
    st.info("No tasks available. Use the sidebar to add a new task.")

# Footer
st.markdown("---")
st.caption("Developed with Streamlit | Project Management Tool for IT Systems Administrators")
