import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# App title
st.title("Task Management Tool")

# Sidebar for task input
st.sidebar.header("Add a New Task")

with st.sidebar.form("task_form"):
    task_title = st.text_input("Task Title")
    task_category = st.selectbox("Category", ["System Maintenance", "Network Management", "Security", "Support"])
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    task_due_date = st.date_input("Due Date")
    task_assigned_to = st.text_input("Assigned To")
    task_description = st.text_area("Description")

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
            st.success(f"Task '{task_title}' added successfully!")
        else:
            st.error("Task Title and Assigned To are required fields.")

# Main section: Display tasks
st.header("Task Dashboard")

if st.session_state.tasks:
    tasks_df = pd.DataFrame(st.session_state.tasks)

    # Filters
    filter_category = st.multiselect("Filter by Category", tasks_df["Category"].unique())
    filter_priority = st.multiselect("Filter by Priority", tasks_df["Priority"].unique())
    filter_status = st.multiselect("Filter by Status", tasks_df["Status"].unique())

    if filter_category:
        tasks_df = tasks_df[tasks_df["Category"].isin(filter_category)]
    if filter_priority:
        tasks_df = tasks_df[tasks_df["Priority"].isin(filter_priority)]
    if filter_status:
        tasks_df = tasks_df[tasks_df["Status"].isin(filter_status)]

    # Display tasks table
    st.subheader("Task Table")
    st.dataframe(tasks_df)

    # Update task status
    st.subheader("Update Task Status")
    task_titles = tasks_df["Title"].tolist()
    selected_task = st.selectbox("Select Task", task_titles)

    if selected_task:
        new_status = st.radio("Update Status", ["Pending", "In Progress", "Completed"])
        if st.button("Update Status"):
            for task in st.session_state.tasks:
                if task["Title"] == selected_task:
                    task["Status"] = new_status
                    st.success(f"Task '{selected_task}' updated to '{new_status}'.")
else:
    st.info("No tasks available. Use the sidebar to add a new task.")

# Footer
st.markdown("---")
st.caption("Developed with Streamlit | Project Management Tool")
