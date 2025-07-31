import streamlit as st
from hospital import HospitalManagementSystem

COMMON_DISEASES = [
    "Flu", "Diabetes", "Hypertension", "Asthma", "Covid-19", 
    "Allergy", "Cancer", "Heart Disease", "Migraine", "Fracture"
]

MEDICAL_SPECIALTIES = [
    "Cardiology", "Neurology", "Dermatology", "Pediatrics", "Orthopedics",
    "Psychiatry", "Radiology", "General Surgery", "Internal Medicine", "Ophthalmology"
]

if 'system' not in st.session_state:
    st.session_state.system = HospitalManagementSystem()

system = st.session_state.system

st.set_page_config(page_title="Hospital Management", layout="centered")
st.title("🏥 Hospital Management System")

menu = st.sidebar.selectbox("Navigation", [
    "Add Patient", "Add Doctor", "Create Appointment", 
    "View All", "Export to Database"
])

if menu == "Add Patient":
    st.subheader("➕ Add Patient")
    with st.form("patient_form"):
        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 100, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        disease = st.selectbox("Disease", ["Other"] + COMMON_DISEASES)
        submitted = st.form_submit_button("Add Patient")
        if submitted:
            if pid and name and gender and disease and age:
                system.add_patient(pid, name, age, gender, disease)
                st.success(f"✅ Patient {name} added.")
            else:
                st.error("❌ Please fill in all fields.")

elif menu == "Add Doctor":
    st.subheader("➕ Add Doctor")
    with st.form("doctor_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 25, 100)
        gender = st.selectbox("Gender", ["Male", "Female"])
        specialty = st.selectbox("Specialty", ["Other"] + MEDICAL_SPECIALTIES, index=1)
        submitted = st.form_submit_button("Add Doctor")
        if submitted:
            if name and gender and specialty and age is not None:
                system.add_doctor(name, age, gender, specialty)
                st.success(f"✅ Doctor {name} added.")
            else:
                st.error("❌ Please fill in all fields.")

elif menu == "Create Appointment":
    st.subheader("📅 Create Appointment")
    if not system.patients or not system.doctors:
        st.warning("⚠️ Add at least one patient and doctor first.")
    else:
        with st.form("appointment_form"):
            aid = st.text_input("Appointment ID")
            days = st.number_input("Schedule after how many days?", 1, 30, value=1)
            patient = st.selectbox("Select Patient", system.patients, format_func=lambda p: f"{p.name} ({p.person_id})")
            doctor = st.selectbox("Select Doctor", system.doctors, format_func=lambda d: f"{d.name} ({d.person_id})")
            submitted = st.form_submit_button("Create Appointment")
            if submitted:
                if aid and patient and doctor:
                    system.book_appointment(aid, patient.person_id, doctor.person_id, days_from_now=days)
                    st.success(f"✅ Appointment created between {patient.name} and Dr. {doctor.name} in {days} day(s).")
                else:
                    st.error("❌ Please fill in all fields.")

elif menu == "View All":
    st.subheader("📋 Patients")
    for p in system.patients:
        st.text(p.display_info())

    st.subheader("🩺 Doctors")
    for d in system.doctors:
        st.text(d.display_info())

    st.subheader("📅 Appointments")
    for a in system.appointments:
        st.text(a.display_info())

elif menu == "Export to Database":
    st.subheader("📤 Export All Data to SQL Server")
    if st.button("💾 Export All"):
        system.export_to_database()
        st.success("✅ All data exported to SQL Server.")
