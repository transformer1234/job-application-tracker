import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"


st.set_page_config(page_title="Job Application Tracker", layout="wide")

st.title("💼 Job Application Tracker")

# -------- Sidebar: Add Application --------
st.sidebar.header("Add New Application")

company = st.sidebar.text_input("Company")
role = st.sidebar.text_input("Role")
location = st.sidebar.text_input("Location")
date_applied = st.sidebar.date_input("Date Applied")
status = st.sidebar.selectbox(
    "Status", ["Applied", "Interview", "Rejected", "Offer"]
)
notes = st.sidebar.text_area("Notes")

if st.sidebar.button("➕ Add Application"):
    if company and role:
        payload = {
            "company": company,
            "role": role,
            "location": location,
            "date_applied": str(date_applied),
            "status": status,
            "notes": notes
        }

        response = requests.post(f"{API_URL}/applications", json=payload)

        if response.status_code == 200:
            st.sidebar.success("Application added!")
        else:
            st.sidebar.error("Failed to add application")

# -------- Main Section --------
st.subheader("📋 All Applications")

response = requests.get(f"{API_URL}/applications")

if response.status_code == 200:
    rows = response.json()
    #df = pd.DataFrame(rows)
else:
    st.error("Could not fetch applications")
    #df = pd.DataFrame()
print(rows)

if rows:
    print("loop")
    df = pd.DataFrame(
        rows,
    )
    #df.set_index("id" ,inplace=True)

    print(len(df))
    print(df.head())

    st.subheader("🔎 Filters")

    col1, col2 = st.columns(2)

    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Applied", "Interview", "Rejected", "Offer"]
        )

    with col2:
        search_company = st.text_input("Search by Company")

    filtered_df = df.copy()

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["status"] == status_filter]

    print(len(filtered_df))

    if search_company:
        filtered_df = filtered_df[
            filtered_df["company"].str.contains(search_company, case=False, na=False)
        ]

    print(len(filtered_df))

    st.dataframe(filtered_df, use_container_width=True)

    st.download_button(
        label="⬇️ Download Applications as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="job_applications.csv",
        mime="text/csv"
    )

    #st.dataframe(df, use_container_width=True)

    # -------- Update Status --------
    st.subheader("✏️ Update Application Status")
    app_id = st.selectbox("Select Application ID", filtered_df["id"])
    new_status = st.selectbox(
        "New Status", ["Applied", "Interview", "Rejected", "Offer"]
    )

    if st.button("Update Status"):
        payload = {"status": new_status}
        response = requests.put(
            f"{API_URL}/applications/{app_id}",
            json=payload
        )

        if response.status_code == 200:
            st.success("Status updated!")
            filtered_df[filtered_df["id"] == app_id]["status"] = new_status

            print(filtered_df[filtered_df["id"] == app_id])

        else:
            st.error("Failed to update status")


    # -------- Delete --------
    st.subheader("🗑️ Delete Application")
    delete_id = st.selectbox("Select ID to Delete", filtered_df["id"], key="delete")

    if st.button("Delete Application"):
        response = requests.delete(
            f"{API_URL}/applications/{delete_id}"
        )

        if response.status_code == 200:
            st.warning("Application deleted.")
        else:
            st.error("Failed to delete application")


    # -------- Analytics --------
    st.subheader("📊 Analytics")
    st.metric("Total Applications", len(df))

    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

else:
    st.info("No applications added yet.")
