import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for tasks if not already done
if "tasks" not in st.session_state:
    st.session_state.tasks = []

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
            "Troubleshooting Issues",
            "Assisting Staff with Technology-Related Needs",
            "Server Monitoring",
            "Workstation Monitoring",
            "Onsite Network Management",
            "Cloud Network Management",
            "System Updates & Patches",
            "Database Management for ERP/Epicor",
            "Configure Networking Routers",
            "Configure Network Switches",
            "Configure Network Firewalls",
            "Network Upgrades",
            "Internet Stability Monitoring",
            "Other IT-Related Duties",
        ],
    )
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    task_due_date = st.date_input("Due Date")
    task_assigned_to = st.text_input("Assigned To", placeholder="Enter team member's name")
    task_description = st.text_area("Description", placeholder="Provide task details")

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

    # Task Table
    st.dataframe(
        tasks_df.drop(columns=["Created"]), use_container_width=True
    )

    # Update task status
    st.subheader("Update Task Status")
    task_titles = tasks_df["Title"].tolist()
    selected_task = st.selectbox("Select Task to Update", ["---"] + task_titles)

    if selected_task != "---":
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
st.caption("Developed with Streamlit | Project Management Tool for IT Systems Administrators")
