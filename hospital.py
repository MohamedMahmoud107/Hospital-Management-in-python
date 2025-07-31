import pyodbc
from datetime import datetime, timedelta

class Person:
    def __init__(self, person_id, name, age, gender):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        return f"ID: {self.person_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

class Patient(Person):
    def __init__(self, person_id, name, age, gender, disease):
        super().__init__(person_id, name, age, gender)
        self.disease = disease

    def display_info(self):
        return super().display_info() + f", Disease: {self.disease}"

class Doctor(Person):
    specialty_counters = {}

    def __init__(self, name, age, gender, specialty):
        prefix = specialty[:2].upper()
        count = Doctor.specialty_counters.get(prefix, 0) + 1
        Doctor.specialty_counters[prefix] = count
        doctor_id = f"{prefix}{count:02d}"
        super().__init__(doctor_id, name, age, gender)
        self.specialty = specialty

    def display_info(self):
        return super().display_info() + f", Specialty: {self.specialty}"

class Appointment:
    def __init__(self, appointment_id, patient, doctor, date):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date

    def display_info(self):
        return f"Appointment ID: {self.appointment_id}, Date: {self.date}, Patient: {self.patient.name}, Doctor: {self.doctor.name}"

class HospitalManagementSystem:
    def __init__(self):
        self._doctors_data = []
        self._patients_data = []
        self._appointments_data = []
        self._conn = self._connect_to_db()
        self._ensure_tables_exist()

    def _connect_to_db(self):
        return pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-AJ3RLS3\SQLEXPRESS;'
            r'DATABASE=HospitalDB;'
            r'Trusted_Connection=yes;'
        )

    def _ensure_tables_exist(self):
        cursor = self._conn.cursor()

        def table_exists(name):
            cursor.execute("SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (name,))
            return cursor.fetchone() is not None

        tables = {
            'Doctors': '''
                CREATE TABLE Doctors (
                    person_id NVARCHAR(10) PRIMARY KEY,
                    name NVARCHAR(100),
                    specialty NVARCHAR(100)
                )''',
            'Patients': '''
                CREATE TABLE Patients (
                    person_id NVARCHAR(10) PRIMARY KEY,
                    name NVARCHAR(100),
                    age INT
                )''',
            'Appointments': '''
                CREATE TABLE Appointments (
                    appointment_id NVARCHAR(10) PRIMARY KEY,
                    patient_id NVARCHAR(10) FOREIGN KEY REFERENCES Patients(person_id),
                    doctor_id NVARCHAR(10) FOREIGN KEY REFERENCES Doctors(person_id),
                    date DATE
                )'''
        }

        for name, sql in tables.items():
            if not table_exists(name):
                cursor.execute(sql)

        self._conn.commit()

    def add_doctor(self, name, age, gender, specialty):
        doctor = Doctor(name, age, gender, specialty)
        self._doctors_data.append(doctor)

    def add_patient(self, person_id, name, age, gender, disease):
        patient = Patient(person_id, name, age, gender, disease)
        self._patients_data.append(patient)

    def book_appointment(self, appointment_id, patient_id, doctor_id, days_from_now=1):
        patient = next((p for p in self._patients_data if p.person_id == patient_id), None)
        doctor = next((d for d in self._doctors_data if d.person_id == doctor_id), None)
        if not patient or not doctor:
            raise ValueError("Doctor or Patient not found.")
        date = datetime.now().date() + timedelta(days=days_from_now)
        appointment = Appointment(appointment_id, patient, doctor, date)
        self._appointments_data.append(appointment)

    def export_to_database(self):
        cursor = self._conn.cursor()

        for d in self._doctors_data:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM Doctors WHERE person_id = ?) 
                INSERT INTO Doctors (person_id, name, specialty) VALUES (?, ?, ?)""",
                d.person_id, d.person_id, d.name, d.specialty)

        for p in self._patients_data:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM Patients WHERE person_id = ?) 
                INSERT INTO Patients (person_id, name, age) VALUES (?, ?, ?)""",
                p.person_id, p.person_id, p.name, p.age)

        for a in self._appointments_data:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM Appointments WHERE appointment_id = ?) 
                INSERT INTO Appointments (appointment_id, patient_id, doctor_id, date) VALUES (?, ?, ?, ?)""",
                a.appointment_id, a.appointment_id, a.patient.person_id, a.doctor.person_id, a.date)

        self._conn.commit()

    @property
    def doctors(self):
        return self._doctors_data

    @property
    def patients(self):
        return self._patients_data

    @property
    def appointments(self):
        return self._appointments_data
