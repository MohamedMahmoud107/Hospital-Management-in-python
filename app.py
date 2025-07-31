import os
from hospital import Patient, Doctor, Appointment, HospitalManagementSystem

system = HospitalManagementSystem()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def main_menu():
    while True:
        print("\n🏥 Hospital Management System")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Create Appointment")
        print("4. List Patients")
        print("5. List Doctors")
        print("6. List Appointments")
        print("7. Export Patients to Database")
        print("8. Export Doctors to Database")
        print("9. Export Appointments to Database")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            add_doctor()
        elif choice == "3":
            create_appointment()
        elif choice == "4":
            list_patients()
        elif choice == "5":
            list_doctors()
        elif choice == "6":
            list_appointments()
        elif choice == "7":
            system.export_patients_to_db()
            print("✅ Patients exported to database.")
        elif choice == "8":
            system.export_doctors_to_db()
            print("✅ Doctors exported to database.")
        elif choice == "9":
            system.export_appointments_to_db()
            print("✅ Appointments exported to database.")
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

        again = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting...")
            break
        clear_screen()

def add_patient():
    pid = input("Patient ID: ")
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    disease = input("Disease: ")
    p = Patient(pid, name, age, gender, disease)
    system.add_patient(p)
    print("✅ Patient added successfully!")

def add_doctor():
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    specialty = input("Specialty: ")
    d = Doctor(name, age, gender, specialty)
    system.add_doctor(d)
    print(f"✅ Doctor added successfully with ID: {d.person_id}")

def create_appointment():
    aid = input("Appointment ID: ")
    pid = input("Patient ID: ")
    did = input("Doctor ID: ")
    date = input("Date (YYYY-MM-DD): ")

    patient = next((p for p in system.patients if p.person_id == pid), None)
    doctor = next((d for d in system.doctors if d.person_id == did), None)

    if patient and doctor:
        a = Appointment(aid, patient, doctor, date)
        system.create_appointment(a)
        print("✅ Appointment created successfully!")
    else:
        print("❌ Invalid patient or doctor ID!")

def list_patients():
    print("\n--- Patients List ---")
    for info in system.list_patients():
        print(info)

def list_doctors():
    print("\n--- Doctors List ---")
    for info in system.list_doctors():
        print(info)

def list_appointments():
    print("\n--- Appointments List ---")
    for info in system.list_appointments():
        print(info)

if __name__ == "__main__":
    main_menu()
