import streamlit as st

def main():
    st.sidebar.title("System Administrator Tool")
    
    # Pages for each job responsibility
    menu = [
        "System Maintenance & Support",
        "Network Management",
        "Security & Compliance",
        "User Support & Training",
        "Backup & Disaster Recovery",
        "Project Management & Implementation",
        "Other IT-Related Duties"
    ]

    choice = st.sidebar.selectbox("Select a Role", menu)

    if choice == "System Maintenance & Support":
        system_maintenance_support()
    elif choice == "Network Management":
        network_management()
    elif choice == "Security & Compliance":
        security_compliance()
    elif choice == "User Support & Training":
        user_support_training()
    elif choice == "Backup & Disaster Recovery":
        backup_disaster_recovery()
    elif choice == "Project Management & Implementation":
        project_management_implementation()
    elif choice == "Other IT-Related Duties":
        other_it_related_duties()

def system_maintenance_support():
    st.title("System Maintenance & Support")
    st.write("Manage, configure, and monitor servers, workstations, and networks.")
    if st.button("Perform System Update"):
        st.success("System updated successfully.")
    if st.button("Monitor Performance"):
        st.info("System performance is optimal.")
    st.text_area("Log System Issues", placeholder="Describe the issue here...")

def network_management():
    st.title("Network Management")
    st.write("Configure and maintain networking devices.")
    st.selectbox("Select Device to Configure", ["Router", "Switch", "Firewall"])
    if st.button("Check Network Status"):
        st.success("Network is stable.")
    st.slider("Bandwidth Usage", 0, 100, 50)

def security_compliance():
    st.title("Security & Compliance")
    st.write("Implement security measures and ensure compliance.")
    if st.button("Run Vulnerability Assessment"):
        st.warning("No critical vulnerabilities detected.")
    st.checkbox("Enable Firewall")
    st.checkbox("Enable Encryption")

def user_support_training():
    st.title("User Support & Training")
    st.write("Provide technical support and training to users.")
    st.text_input("Search User Issues", placeholder="Enter a keyword...")
    if st.button("Resolve Issue"):
        st.success("Issue resolved.")
    st.file_uploader("Upload Training Materials")

def backup_disaster_recovery():
    st.title("Backup & Disaster Recovery")
    st.write("Ensure backups and implement disaster recovery procedures.")
    if st.button("Initiate Backup"):
        st.success("Backup completed successfully.")
    if st.button("Test Disaster Recovery Plan"):
        st.info("Disaster recovery plan test passed.")

def project_management_implementation():
    st.title("Project Management & Implementation")
    st.write("Assist with IT projects and deployments.")
    st.text_input("Project Name", placeholder="Enter the project name...")
    st.date_input("Project Deadline")
    if st.button("Submit Project Update"):
        st.success("Project update submitted.")

def other_it_related_duties():
    st.title("Other IT-Related Duties")
    st.write("Handle miscellaneous IT tasks.")
    st.text_area("Describe Task", placeholder="Enter task details...")
    if st.button("Mark Task as Completed"):
        st.success("Task marked as completed.")

if __name__ == "__main__":
    main()
