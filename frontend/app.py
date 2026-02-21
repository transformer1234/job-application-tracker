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
status = st.sidebar.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
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

# -------- Filters & Sorting --------
st.subheader("🔎 Filters & Sorting")

col1, col2, col3 = st.columns(3)
with col1:
    status_filter = st.selectbox("Filter by Status", ["All", "Applied", "Interview", "Rejected", "Offer"])
with col2:
    search_company = st.text_input("Search by Company or Role")
with col3:
    sort_by = st.selectbox("Sort By", ["date_applied", "company", "role", "status"])

col4, col5 = st.columns(2)
with col4:
    sort_order = st.radio("Sort Order", ["DESC", "ASC"], horizontal=True)
with col5:
    page_size = st.selectbox("Results per Page", [5, 10, 20, 50], index=1)

col6, col7 = st.columns(2)
with col6:
    date_from = st.date_input("Date From", value=None)
with col7:
    date_to = st.date_input("Date To", value=None)

# -------- Pagination state --------
if "page" not in st.session_state:
    st.session_state.page = 1

# Reset to page 1 whenever filters change
filter_key = f"{status_filter}|{search_company}|{sort_by}|{sort_order}|{date_from}|{date_to}|{page_size}"
if "last_filter_key" not in st.session_state or st.session_state.last_filter_key != filter_key:
    st.session_state.page = 1
    st.session_state.last_filter_key = filter_key

# -------- Build API request --------
params = {
    "sort_by": sort_by,
    "sort_order": sort_order,
    "page": st.session_state.page,
    "page_size": page_size,
}
if status_filter != "All":
    params["status"] = status_filter
if search_company:
    params["search"] = search_company
if date_from:
    params["date_from"] = str(date_from)
if date_to:
    params["date_to"] = str(date_to)

response = requests.get(f"{API_URL}/applications", params=params)

if response.status_code == 200:
    result = response.json()
    rows = result["data"]
    total = result["total"]
    total_pages = max(1, -(-total // page_size))  # ceiling division
else:
    st.error("Could not fetch applications")
    rows = []
    total = 0
    total_pages = 1

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # -------- Pagination Controls --------
    st.markdown(f"**Page {st.session_state.page} of {total_pages}** &nbsp;|&nbsp; Total: {total} application(s)")
    pcol1, pcol2, _ = st.columns([1, 1, 6])
    with pcol1:
        if st.button("⬅ Prev") and st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()
    with pcol2:
        if st.button("Next ➡") and st.session_state.page < total_pages:
            st.session_state.page += 1
            st.rerun()

    st.download_button(
        label="⬇️ Download Current Page as CSV",
        data=df.to_csv(index=False),
        file_name="job_applications.csv",
        mime="text/csv"
    )

    # -------- Update Status --------
    st.subheader("✏️ Update Application Status")
    app_id = st.selectbox("Select Application ID", df["id"])
    new_status = st.selectbox("New Status", ["Applied", "Interview", "Rejected", "Offer"])

    if st.button("Update Status"):
        payload = {"status": new_status}
        upd_response = requests.put(f"{API_URL}/applications/{app_id}", json=payload)
        if upd_response.status_code == 200:
            st.success("Status updated!")
            st.rerun()
        else:
            st.error("Failed to update status")

    # -------- Delete --------
    st.subheader("🗑️ Delete Application")
    delete_id = st.selectbox("Select ID to Delete", df["id"], key="delete")

    if st.button("Delete Application"):
        del_response = requests.delete(f"{API_URL}/applications/{delete_id}")
        if del_response.status_code == 200:
            st.warning("Application deleted.")
            st.rerun()
        else:
            st.error("Failed to delete application")

    # -------- Analytics --------
    st.subheader("📊 Analytics")

    analytics_response = requests.get(f"{API_URL}/applications/all")
    if analytics_response.status_code == 200:
        all_df = pd.DataFrame(analytics_response.json())
        st.metric("Total Applications", len(all_df))
        status_counts = all_df["status"].value_counts()
        st.bar_chart(status_counts)
    else:
        st.error("Could not load analytics")