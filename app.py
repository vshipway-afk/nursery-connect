import streamlit as st
import pandas as pd
from database import SessionLocal
import models

st.set_page_config(page_title="NurseryConnect Dashboard", layout="wide")

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

# 1. LOGIN SCREEN (If not logged in)
if not st.session_state.logged_in:
    st.title("🌟 NurseryConnect Dashboard")
    st.subheader("🔐 Please Log In to Access Nursery Portal")

    with st.form("login_form"):
        role = st.selectbox("Select Your Role", ["Staff / Practitioner", "Nursery Manager"], key="login_role_select")
        password = st.text_input("Password", type="password", key="login_password_input")
        submit_login = st.form_submit_button("Log In")

        if submit_login:
            if password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("Login successful! Loading dashboard...")
                st.rerun()
            else:
                st.error("Incorrect password. (Try 'admin123')")

# 2. MAIN DASHBOARD (Only shown after successful login)
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.role}**")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.rerun()

    # ALL FEATURES LISTED IN ONE SIDEBAR MENU
    menu = st.sidebar.selectbox(
        "Select Feature",
        [
            "View Children",
            "Register New Child",
            "Policies & Procedures",
            "Log Sleep Record",
            "Log Incident",
            "Daily Logs",
            "Medication Forms",
            "EYFS Observations",
            "Diet & Milk Plans",
            "Attendance Tracker",
            "Key Persons",
            "Emergency Contacts",
            "Invoices",
            "Garden Register",
            "New Joiners",
            "External Medications",
            "Health Care Plans",
            "Staff & Visitor Register",
            "Headcounts"
        ],
        key="unique_sidebar_menu_key"
    )

    st.title("🌟 NurseryConnect Comprehensive Dashboard")
    st.write("Manage all your nursery operations from one unified portal.")

    # --- VIEW CHILDREN SECTION ---
    if menu == "View Children":
        st.subheader("📋 Nursery Rooms & Children Directory")
        try:
            db = SessionLocal()
            children_records = db.query(models.Child).all()
            db.close()

            if children_records:
                children = [
                    {
                        "id": c.id,
                        "first_name": c.first_name,
                        "last_name": c.last_name,
                        "room_name": c.room_name,
                        "allergies": getattr(c, "allergies", "None")
                    }
                    for c in children_records
                ]

                search_query = st.text_input("🔍 Search child by name or room:", "").lower()

                filtered_children = [
                    c for c in children
                    if search_query in c['first_name'].lower()
                       or search_query in c['last_name'].lower()
                       or search_query.lower() in c.get('room_name', '').lower()
                ]

                if filtered_children:
                    df = pd.DataFrame(filtered_children)
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Child Register (CSV)",
                        data=csv_data,
                        file_name="nursery_children_register.csv",
                        mime="text/csv",
                    )
                    st.divider()

                    unique_rooms = set(c['room_name'] for c in filtered_children if c.get('room_name'))
                    for room in unique_rooms:
                        with st.expander(f"🚪 Room: {room}"):
                            room_children = [c for c in filtered_children if c.get('room_name') == room]
                            for child in room_children:
                                st.write(
                                    f"- **ID:** {child['id']} | **Name:** {child['first_name']} {child['last_name']} | **Allergies:** {child.get('allergies', 'None')}")
                else:
                    st.warning("No matching children or rooms found.")
            else:
                st.info("No children registered yet.")
        except Exception as e:
            st.error(f"Database error: {e}")

    # --- REGISTER NEW CHILD SECTION ---
    elif menu == "Register New Child":
        st.subheader("➕ Register a New Child")
        with st.form("register_child_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            room_name = st.text_input("Room Name (e.g., Ladybird, Preschool)")
            allergies = st.text_input("Allergies (if any)")
            submit_child = st.form_submit_button("Save Child Record")

            if submit_child:
                try:
                    db = SessionLocal()
                    new_child = models.Child(
                        first_name=first_name,
                        last_name=last_name,
                        room_name=room_name,
                        allergies=allergies
                    )
                    db.add(new_child)
                    db.commit()
                    db.close()
                    st.success("Child registered successfully!")
                except Exception as e:
                    st.error(f"Failed to register child: {e}")

    # --- POLICIES & PROCEDURES SECTION ---
    elif menu == "Policies & Procedures":
        st.subheader("📚 Nursery Policies & Procedures Manual")
        st.write("Search through official nursery operational guidelines, safeguarding rules, and safety procedures.")

        policies = [
            {
                "title": "Safeguarding and Child Protection Policy",
                "category": "Safety & Welfare",
                "summary": "Guidelines on recognizing signs of abuse, reporting procedures, and designated safeguarding leads (DSL) contact steps."
            },
            {
                "title": "Administering Medication Policy",
                "category": "Health & Medical",
                "summary": "Rules for storing, recording, and administering prescription and non-prescription medication with dual staff sign-off."
            },
            {
                "title": "Missing Child Procedure",
                "category": "Security",
                "summary": "Immediate action steps: lock down the building, search indoor/outdoor perimeters, check registers, and contact police/parents."
            },
            {
                "title": "Allergy and Dietary Management Policy",
                "category": "Health & Nutrition",
                "summary": "Procedures for cross-contamination prevention, kitchen communication, and identifying children with specific food allergies."
            },
            {
                "title": "Infection Control and Illness Exclusion",
                "category": "Health & Hygiene",
                "summary": "Required exclusion periods for sickness, diarrhoea, chickenpox, and hand-foot-mouth disease to prevent nursery outbreaks."
            }
        ]

        policy_search = st.text_input("🔍 Search policies (e.g., 'allergy', 'safeguarding', 'medication'):", "",
                                      key="policy_search_input")

        filtered_policies = [
            p for p in policies
            if policy_search.lower() in p['title'].lower()
               or policy_search.lower() in p['category'].lower()
               or policy_search.lower() in p['summary'].lower()
        ]

        if filtered_policies:
            for pol in filtered_policies:
                with st.expander(f"📖 {pol['title']} ({pol['category']})"):
                    st.write(f"**Overview:** {pol['summary']}")
                    st.info("Full PDF version available for download upon compliance audit review.")
        else:
            st.warning("No policies found matching your search term.")

    # --- PLACEHOLDERS FOR OTHER BACKEND FEATURES ---
    else:
        st.subheader(f"🛠️ {menu} Management Portal")
        st.write(f"This module manages records for **{menu}**.")
        st.info("Use the form inputs below to record or retrieve data for this category.")

        with st.form(f"form_{menu}"):
            notes = st.text_input(f"Enter details for {menu}:")
            submitted = st.form_submit_button(f"Submit {menu}")
            if submitted:
                st.success(f"Successfully recorded data for {menu}!")