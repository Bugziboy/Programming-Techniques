
# counters for unique IDs
patient_counter = 1000
doctor_counter = 5000
appointment_counter = 9000

#person class
class Person:
    def __init__(self, name, age, gender):
        #initialize person attributes
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        #display person
        return f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

#patient class 
class Patient(Person):
    def __init__(self, name, age, gender):
        global patient_counter
        #calls person constuctors
        super().__init__(name, age, gender) 
        self.patient_id = f"P{patient_counter}"
        patient_counter += 1
        #create list for appointments
        self.appointment_list = []  

    def book_appointment(self, appointment):
        #add new appointment to patient list
        self.appointment_list.append(appointment)

    def view_profile(self):
        #display patient info, appointments
        print(f"\nPatient ID: {self.patient_id}\n{self.display_info()}")
        for appt in self.appointment_list:
            print(f"Appointment ID: {appt.appointment_id}, Doctor: {appt.doctor.name}, Date: {appt.date}, Time: {appt.time}, Status: {appt.status}")

#doctor class 
class Doctor(Person):
    def __init__(self, name, age, gender, specialty, schedule):
        global doctor_counter
        super().__init__(name, age, gender)  
        self.doctor_id = f"D{doctor_counter}"
        doctor_counter += 1
        #add specialty for doctor
        self.specialty = specialty  
        #chedule list of date and time
        self.schedule = schedule  

    def is_available(self, date, time):
        #check if  doctor is available for the date and time
        return (date, time) in self.schedule

    def view_schedule(self):
        #shows doctor schedule and profile
        print(f"\nDoctor ID: {self.doctor_id}\n{self.display_info()}\nSpecialty: {self.specialty}\nSchedule: {self.schedule}")

#appointment class
class Appointment:
    def __init__(self, patient, doctor, date, time):
        global appointment_counter
        self.appointment_id = f"A{appointment_counter}"
        appointment_counter += 1
        self.patient = patient  #patient object
        self.doctor = doctor  #doctor object
        self.date = date  #appointment date
        self.time = time  #appointment time
        self.status = "Confirmed"  

    def cancel(self):
        #change status to Cancelled
        self.status = "Cancelled"

# Hospital class 
class HospitalSystem:
    def __init__(self):
        self.patients = {}  #store patients by ID
        self.doctors = {}  #store doctors by ID
        self.appointments = []  #all appointments

    def add_patient(self, name, age, gender):
        try:
            age = int(age)  
            patient = Patient(name, age, gender)  #create  patient object
            self.patients[patient.patient_id] = patient  #add to the patients list
            print(f"Patient added with ID: {patient.patient_id}")
        except ValueError:
            print("Invalid age entered.")

    def add_doctor(self, name, age, gender, specialty, schedule):
        try:
            age = int(age)  
            doctor = Doctor(name, age, gender, specialty, schedule)  #create a doctor object
            self.doctors[doctor.doctor_id] = doctor  #add to doctors list
            print(f"Doctor added with ID: {doctor.doctor_id}")
        except ValueError:
            print("Invalid age entered.")

    def book_appointment(self, patient_id, doctor_id, date, time):
        #check if  patient and doctor exist
        if patient_id not in self.patients:
            print("Patient not found.")
            return
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return

        doctor = self.doctors[doctor_id]
        #check if doctor available
        if not doctor.is_available(date, time):
            print("Doctor not available at this time.")
            return

        #used to avoid double booking
        for appt in self.appointments:
            if appt.doctor.doctor_id == doctor_id and appt.date == date and appt.time == time:
                print("Time slot already booked.")
                return

        #book and confirm appointment
        appointment = Appointment(self.patients[patient_id], doctor, date, time)
        self.patients[patient_id].book_appointment(appointment)
        self.appointments.append(appointment)
        print(f"Appointment booked. ID: {appointment.appointment_id}")

    def cancel_appointment(self, appointment_id):
        #cancel an appointment by ID
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                appt.cancel()
                print("Appointment cancelled.")
                return
        print("Appointment ID not found.")

    def generate_bill(self, appointment_id, additional_fee):
        #print bill for sericves 
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                try:
                    
                    additional_fee = float(additional_fee)  
                    #Consultation fee + additional services where valid
                    total = 3000 + additional_fee 
                    print("\n********* CATABOO HOSPITAL RECEIPT *********")
                    print(f"Patient: {appt.patient.name}")
                    print(f"Doctor: {appt.doctor.name}")
                    print(f"Appointment Date: {appt.date} Time: {appt.time}")
                    print(f"Consultation Fee: JMD$ 3000.00")
                    print(f"Additional Services: JMD$ {additional_fee:.2f}")
                    print(f"TOTAL: JMD$ {total:.2f}")
                    print(f"\t Thank you")
                    print("********************************************")
                    return
                except ValueError:
                    print("Invalid fee entered.")
                    return
        print("Appointment ID not found.")
if __name__ == '__main__':
    hs = HospitalSystem()

    while True:
        print("\n\t\t Cataboo Hospital System Menu ")
        print("1. Register Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. Cancel Appointment")
        print("5. Generate Bill")
        print("6. View Patient Profile")
        print("7. View Doctor Schedule")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter patient's name: ")
                age = int(input("Enter patient's age: "))
                gender = input("Enter patient's gender: ")
                hs.add_patient(name, age, gender)

            elif choice == '2':
                name = input("Enter doctor's name: ")
                age = int(input("Enter doctor's age: "))
                gender = input("Enter doctor's gender: ")
                speciality = input("Enter speciality: ")
                schedule = []
                while True:
                    date = input("Enter available date (YYYY-MM-DD) or 'done': ")
                    if date.lower() == 'done':
                        break
                    time = input("Enter available time (HH:MM): ")
                    schedule.append((date, time))
                hs.add_doctor(name, age, gender, speciality, schedule)

            elif choice == '3':
                patient_id = input("Enter patient ID: ")
                doctor_id = input("Enter doctor ID: ")
                date = input("Enter appointment date (YYYY-MM-DD): ")
                time = input("Enter appointment time (HH:MM): ")
                hs.book_appointment(patient_id, doctor_id, date, time)

            elif choice == '4':
                appointment_id = input("Enter appointment ID to cancel: ")
                hs.cancel_appointment(appointment_id)

            elif choice == '5':
                appointment_id = input("Enter appointment ID for billing: ")
                additional_fee= input("Enter the additional fees owed:")
                hs.generate_bill(appointment_id, additional_fee)

            elif choice == '6':
                pid = input("Enter patient ID: ")
                if pid in hs.patients:
                    hs.patients[pid].view_profile()
                else:
                    print("Patient not found.")

            elif choice == '7':
                did = input("Enter doctor ID: ")
                if did in hs.doctors:
                    hs.doctors[did].view_schedule()
                else:
                    print("Doctor not found.")

            elif choice == '0':
                print("Exiting system. Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print(f"Error: {e}")
