"""
Vet Office Management System - Example Usage
Demonstrates how to use the system to manage a vet clinic's operations
"""

from datetime import date, time, timedelta
from vet_office_system import (
    VetOffice, Client, Animal, Veterinarian, Contact,
    AnimalSpecies, Appointment, Treatment, Medication, MedicalRecord,
    TreatmentType, AppointmentStatus
)


def create_sample_clinic():
    """Create a sample vet clinic with data"""
    
    # Create the clinic
    clinic = VetOffice(
        name="Happy Paws Veterinary Clinic",
        address="123 Pet Street",
        phone="(555) 123-4567",
        email="info@happypaws.vet"
    )
    
    print("=" * 60)
    print("VET OFFICE MANAGEMENT SYSTEM - EXAMPLE USAGE")
    print("=" * 60)
    print(f"\n📍 Created: {clinic}")
    
    # Create veterinarians
    print("\n" + "=" * 60)
    print("ADDING VETERINARY STAFF")
    print("=" * 60)
    
    dr_johnson = Veterinarian(
        "Sarah", "Johnson", 
        "VET123456", 
        ["Small Animals", "Surgery", "Dentistry"]
    )
    dr_chen = Veterinarian(
        "David", "Chen",
        "VET789012",
        ["Exotic Animals", "Avian Medicine"]
    )
    
    clinic.add_veterinarian(dr_johnson)
    clinic.add_veterinarian(dr_chen)
    
    print(f"✅ {dr_johnson}")
    print(f"✅ {dr_chen}")
    
    # Create clients
    print("\n" + "=" * 60)
    print("REGISTERING CLIENTS")
    print("=" * 60)
    
    contact1 = Contact(
        phone="(555) 111-2222",
        email="john.smith@email.com",
        address="456 Oak Ave",
        city="Pet City",
        state="CA",
        zip_code="90210"
    )
    
    client1 = Client("John", "Smith", contact1, date_joined=date(2023, 1, 15))
    client1.notes = "Prefers evening appointments"
    
    contact2 = Contact(
        phone="(555) 333-4444",
        email="emily.jones@email.com",
        address="789 Elm St",
        city="Pet City",
        state="CA",
        zip_code="90211"
    )
    
    client2 = Client("Emily", "Jones", contact2, date_joined=date(2023, 6, 20))
    
    clinic.add_client(client1)
    clinic.add_client(client2)
    
    print(f"✅ {client1}")
    print(f"✅ {client2}")
    
    # Register animals
    print("\n" + "=" * 60)
    print("REGISTERING ANIMALS")
    print("=" * 60)
    
    # Dog for John Smith
    dog = Animal(
        name="Max",
        species=AnimalSpecies.DOG,
        breed="Golden Retriever",
        date_of_birth=date(2020, 3, 15),
        microchip_id="123456789ABC"
    )
    dog.weight_kg = 32.5
    dog.allergies = ["Chicken"]
    dog.notes = "Very friendly, loves treats"
    
    client1.add_animal(dog)
    clinic.add_animal(dog)
    
    # Cat for John Smith
    cat = Animal(
        name="Whiskers",
        species=AnimalSpecies.CAT,
        breed="Siamese",
        date_of_birth=date(2019, 7, 22),
        microchip_id="987654321XYZ"
    )
    cat.weight_kg = 4.2
    cat.allergies = ["Fish-based foods"]
    
    client1.add_animal(cat)
    clinic.add_animal(cat)
    
    # Another dog for Emily Jones
    rabbit = Animal(
        name="Thumper",
        species=AnimalSpecies.RABBIT,
        breed="Holland Lop",
        date_of_birth=date(2021, 11, 10),
        microchip_id="555666777EEE"
    )
    rabbit.weight_kg = 2.1
    
    client2.add_animal(rabbit)
    clinic.add_animal(rabbit)
    
    print(f"✅ {dog}")
    print(f"✅ {cat}")
    print(f"✅ {rabbit}")
    
    # Schedule appointments
    print("\n" + "=" * 60)
    print("SCHEDULING APPOINTMENTS")
    print("=" * 60)
    
    # Appointment 1: Max's check-up today
    today = date.today()
    apt1 = clinic.schedule_appointment(
        animal=dog,
        veterinarian=dr_johnson,
        appointment_date=today,
        appointment_time=time(10, 0),
        duration_minutes=30,
        reason="Annual check-up and vaccination"
    )
    
    # Appointment 2: Whiskers' dental
    apt2 = clinic.schedule_appointment(
        animal=cat,
        veterinarian=dr_johnson,
        appointment_date=today,
        appointment_time=time(11, 0),
        duration_minutes=45,
        reason="Dental cleaning"
    )
    
    # Appointment 3: Thumper's visit (future)
    tomorrow = today + timedelta(days=1)
    apt3 = clinic.schedule_appointment(
        animal=rabbit,
        veterinarian=dr_chen,
        appointment_date=tomorrow,
        appointment_time=time(14, 0),
        duration_minutes=20,
        reason="Annual check-up"
    )
    
    print(f"✅ {apt1}")
    print(f"✅ {apt2}")
    print(f"✅ {apt3}")
    
    # Add treatments
    print("\n" + "=" * 60)
    print("RECORDING TREATMENTS")
    print("=" * 60)
    
    # Treatment for Max
    treatment1 = Treatment(
        name="Rabies Vaccination",
        treatment_type=TreatmentType.VACCINATION,
        description="Annual rabies vaccination"
    )
    treatment1.cost = 45.00
    apt1.add_treatment(treatment1)
    apt1.cost += treatment1.cost
    
    # Medication for Max
    med1 = Medication(
        name="Amoxicillin",
        dosage="500mg",
        frequency="twice daily",
        start_date=today,
        end_date=today + timedelta(days=7)
    )
    med1.prescribed_by = dr_johnson
    dog.add_medication(med1)
    treatment1.add_medication(med1)
    
    print(f"✅ Added treatment: {treatment1}")
    print(f"   └─ Prescribed medication: {med1}")
    
    # Treatment for Whiskers
    treatment2 = Treatment(
        name="Dental Cleaning & Extraction",
        treatment_type=TreatmentType.DENTAL,
        description="Professional cleaning with one tooth extraction"
    )
    treatment2.cost = 350.00
    apt2.add_treatment(treatment2)
    apt2.cost += treatment2.cost
    
    med2 = Medication(
        name="Tramadol",
        dosage="50mg",
        frequency="every 12 hours",
        start_date=today,
        end_date=today + timedelta(days=5)
    )
    med2.prescribed_by = dr_johnson
    cat.add_medication(med2)
    treatment2.add_medication(med2)
    
    print(f"✅ Added treatment: {treatment2}")
    print(f"   └─ Prescribed medication: {med2}")
    
    # Medical records
    print("\n" + "=" * 60)
    print("ADDING MEDICAL RECORDS")
    print("=" * 60)
    
    record1 = MedicalRecord(
        date_recorded=today,
        record_type="vaccination",
        details="Rabies vaccination administered, document received"
    )
    record1.recorded_by = dr_johnson
    dog.add_medical_record(record1)
    
    record2 = MedicalRecord(
        date_recorded=today,
        record_type="dental_exam",
        details="Significant tartar buildup. One lower molar extracted due to decay."
    )
    record2.recorded_by = dr_johnson
    cat.add_medical_record(record2)
    
    print(f"✅ {record1}")
    print(f"✅ {record2}")
    
    return clinic


def demonstrate_queries(clinic):
    """Demonstrate various queries and features"""
    
    print("\n" + "=" * 60)
    print("DEMONSTRATING QUERIES & FEATURES")
    print("=" * 60)
    
    # 1. Find clients
    print("\n📋 SEARCHING FOR CLIENTS")
    found_client = clinic.find_client_by_name("John", "Smith")
    if found_client:
        print(f"Found client: {found_client}")
        print(f"  Animals owned: {len(found_client.animals)}")
        for animal in found_client.animals:
            print(f"    - {animal.name} ({animal.species.value})")
    
    # 2. Get animal details
    print("\n🐾 ANIMAL DETAILS")
    animals = clinic.animals
    if animals:
        target_animal = animals[0]
        print(f"\nAnimal: {target_animal}")
        print(f"  Age: {target_animal.age_years:.1f} years")
        print(f"  Weight: {target_animal.weight_kg} kg")
        if target_animal.allergies:
            print(f"  ⚠️  Allergies: {', '.join(target_animal.allergies)}")
        
        # Active medications
        active_meds = target_animal.get_active_medications()
        print(f"  Active medications: {len(active_meds)}")
        for med in active_meds:
            print(f"    - {med}")
        
        # Upcoming appointments
        upcoming = target_animal.get_upcoming_appointments()
        print(f"  Upcoming appointments: {len(upcoming)}")
        for apt in upcoming:
            print(f"    - {apt.appointment_date} at {apt.appointment_time}")
    
    # 3. View veterinarian schedule
    print("\n👨‍⚕️ VETERINARIAN SCHEDULES")
    for vet in clinic.veterinarians:
        print(f"\n{vet}")
        upcoming = vet.get_upcoming_appointments(7)
        print(f"  Upcoming appointments (7 days): {len(upcoming)}")
        for apt in upcoming:
            print(f"    - {apt.animal.name} on {apt.appointment_date}")
    
    # 4. Clinic statistics
    print("\n📊 CLINIC STATISTICS")
    print(f"  Total Clients: {clinic.get_client_count()}")
    print(f"  Total Animals: {clinic.get_animal_count()}")
    print(f"  Veterinarians on Staff: {len(clinic.veterinarians)}")
    
    upcoming_apts = clinic.get_upcoming_appointments(7)
    print(f"  Upcoming Appointments (7 days): {len(upcoming_apts)}")
    
    # 5. Appointment details
    print("\n📅 UPCOMING APPOINTMENTS")
    for apt in clinic.get_upcoming_appointments(7):
        print(f"\n  {apt}")
        print(f"    Owner: {apt.animal.owner.full_name if apt.animal.owner else 'Unknown'}")
        print(f"    Duration: {apt.duration_minutes} minutes")
        if apt.treatments:
            print(f"    Treatments: {len(apt.treatments)}")
            for treat in apt.treatments:
                print(f"      - {treat}")


def demonstrate_workflow(clinic):
    """Demonstrate a typical workflow: checking in an appointment and completing it"""
    
    print("\n" + "=" * 60)
    print("DEMONSTRATING TYPICAL WORKFLOW")
    print("=" * 60)
    
    # Get first appointment
    upcoming = clinic.get_upcoming_appointments(7)
    if upcoming:
        appointment = upcoming[0]
        
        print(f"\n🔹 APPOINTMENT CHECK-IN")
        print(f"Animal: {appointment.animal.name}")
        print(f"Owner: {appointment.animal.owner.full_name}")
        print(f"Scheduled Time: {appointment.appointment_time}")
        
        # Mark as in progress
        appointment.status = AppointmentStatus.IN_PROGRESS
        print(f"✅ Status updated to: {appointment.status.value}")
        
        # Perform exam and update notes
        appointment.notes = "Animal examined thoroughly. Appears healthy and alert. Weight within normal range."
        print(f"📝 Exam notes recorded")
        
        # Mark as completed
        appointment.mark_completed()
        print(f"✅ Status updated to: {appointment.status.value}")
        print(f"✅ Appointment completed successfully!")


def main():
    """Main function to run all demonstrations"""
    
    # Create clinic with sample data
    clinic = create_sample_clinic()
    
    # Demonstrate various features
    demonstrate_queries(clinic)
    
    # Show typical workflow
    demonstrate_workflow(clinic)
    
    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE!")
    print("=" * 60)
    print("\nTo use the interactive web interface, run:")
    print("  streamlit run vet_app.py")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
