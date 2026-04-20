"""
Vet Office Management System
A comprehensive system for veterinary clinics to manage clients, animals, 
appointments, and treatments.
"""

from enum import Enum
from datetime import date, datetime, timedelta, time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


class AnimalSpecies(Enum):
    """Types of animals treated at the vet clinic"""
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    HAMSTER = "hamster"
    GUINEA_PIG = "guinea_pig"
    REPTILE = "reptile"
    OTHER = "other"


class AppointmentStatus(Enum):
    """Status of vet appointments"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class TreatmentType(Enum):
    """Types of treatments provided"""
    VACCINATION = "vaccination"
    CHECK_UP = "check_up"
    SURGERY = "surgery"
    DENTAL = "dental"
    GROOMING = "grooming"
    MEDICATION = "medication"
    DIAGNOSTIC = "diagnostic"
    EMERGENCY = "emergency"
    OTHER = "other"


@dataclass
class Contact:
    """Contact information for clients"""
    phone: str
    email: str
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""

    def __str__(self) -> str:
        return f"{self.phone} | {self.email}"


class Client:
    """Represents a pet owner/client of the vet clinic"""

    def __init__(self, first_name: str, last_name: str, contact: Contact, 
                 date_joined: date = None):
        """Initialize a Client instance"""
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.date_joined = date_joined if date_joined else date.today()
        self.animals: List['Animal'] = []
        self.total_paid: float = 0.0
        self.notes: str = ""

    @property
    def full_name(self) -> str:
        """Return client's full name"""
        return f"{self.first_name} {self.last_name}"

    def add_animal(self, animal: 'Animal') -> None:
        """Add an animal to this client's account"""
        animal.owner = self
        self.animals.append(animal)

    def get_animals(self) -> List['Animal']:
        """Return all animals owned by this client"""
        return self.animals

    def get_active_animals(self) -> List['Animal']:
        """Return only active (not deceased) animals"""
        return [animal for animal in self.animals if not animal.is_deceased]

    def __str__(self) -> str:
        """Return string representation of the client"""
        animal_count = len(self.animals)
        animal_text = "animal" if animal_count == 1 else "animals"
        return f"{self.full_name} | {animal_count} {animal_text} | Joined: {self.date_joined}"


class Animal:
    """Represents a patient (animal) at the vet clinic"""

    def __init__(self, name: str, species: AnimalSpecies, breed: str, 
                 date_of_birth: date, microchip_id: str = ""):
        """Initialize an Animal instance"""
        self.name = name
        self.species = species
        self.breed = breed
        self.date_of_birth = date_of_birth
        self.microchip_id = microchip_id
        self.owner: Optional[Client] = None
        self.weight_kg: float = 0.0
        self.is_deceased: bool = False
        self.medical_records: List['MedicalRecord'] = []
        self.appointments: List['Appointment'] = []
        self.allergies: List[str] = []
        self.medications: List['Medication'] = []
        self.notes: str = ""

    @property
    def age_years(self) -> float:
        """Calculate animal's age in years"""
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def add_medical_record(self, record: 'MedicalRecord') -> None:
        """Add a medical record to this animal's history"""
        record.animal = self
        self.medical_records.append(record)

    def add_appointment(self, appointment: 'Appointment') -> None:
        """Add an appointment for this animal"""
        appointment.animal = self
        self.appointments.append(appointment)

    def add_medication(self, medication: 'Medication') -> None:
        """Add a current medication for this animal"""
        medication.animal = self
        self.medications.append(medication)

    def get_active_medications(self) -> List['Medication']:
        """Get all currently active medications"""
        today = date.today()
        return [med for med in self.medications 
                if med.start_date <= today and (not med.end_date or med.end_date >= today)]

    def get_upcoming_appointments(self) -> List['Appointment']:
        """Get upcoming appointments for this animal"""
        today = date.today()
        upcoming = [apt for apt in self.appointments 
                   if apt.appointment_date >= today and apt.status != AppointmentStatus.CANCELLED]
        return sorted(upcoming, key=lambda x: x.appointment_date)

    def get_appointment_history(self) -> List['Appointment']:
        """Get past appointments in chronological order"""
        today = date.today()
        history = [apt for apt in self.appointments 
                  if apt.appointment_date < today or apt.status == AppointmentStatus.COMPLETED]
        return sorted(history, key=lambda x: x.appointment_date, reverse=True)

    def __str__(self) -> str:
        """Return string representation of the animal"""
        owner = self.owner.full_name if self.owner else "Unknown"
        return f"{self.name} ({self.species.value}) - {self.breed}, {self.age_years:.1f} yrs | Owner: {owner}"


class Veterinarian:
    """Represents a veterinarian on staff"""

    def __init__(self, first_name: str, last_name: str, license_number: str, 
                 specialties: List[str] = None):
        """Initialize a Veterinarian instance"""
        self.first_name = first_name
        self.last_name = last_name
        self.license_number = license_number
        self.specialties = specialties if specialties else []
        self.is_available = True
        self.appointments: List['Appointment'] = []

    @property
    def full_name(self) -> str:
        """Return veterinarian's full name"""
        return f"{self.first_name} {self.last_name}"

    def get_appointments_by_date(self, target_date: date) -> List['Appointment']:
        """Get all appointments for a specific date"""
        return [apt for apt in self.appointments if apt.appointment_date == target_date]

    def get_upcoming_appointments(self, days_ahead: int = 30) -> List['Appointment']:
        """Get upcoming appointments within specified days"""
        today = date.today()
        cutoff = today + timedelta(days=days_ahead)
        upcoming = [apt for apt in self.appointments 
                   if today <= apt.appointment_date <= cutoff 
                   and apt.status != AppointmentStatus.CANCELLED]
        return sorted(upcoming, key=lambda x: x.appointment_date)

    def __str__(self) -> str:
        """Return string representation of the veterinarian"""
        spec_text = f" - Specialties: {', '.join(self.specialties)}" if self.specialties else ""
        return f"Dr. {self.full_name} (License: {self.license_number}){spec_text}"


class Appointment:
    """Represents a scheduled vet appointment"""

    def __init__(self, animal: Animal, veterinarian: Veterinarian, 
                 appointment_date: date, appointment_time: time, 
                 duration_minutes: int, reason: str = ""):
        """Initialize an Appointment instance"""
        self.animal = animal
        self.veterinarian = veterinarian
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.duration_minutes = duration_minutes
        self.reason = reason
        self.status = AppointmentStatus.SCHEDULED
        self.notes: str = ""
        self.treatments: List['Treatment'] = []
        self.cost: float = 0.0
        self.created_date = date.today()

    def add_treatment(self, treatment: 'Treatment') -> None:
        """Add a treatment to this appointment"""
        treatment.appointment = self
        self.treatments.append(treatment)

    def mark_completed(self) -> None:
        """Mark appointment as completed"""
        self.status = AppointmentStatus.COMPLETED

    def mark_cancelled(self, reason: str = "") -> None:
        """Cancel this appointment"""
        self.status = AppointmentStatus.CANCELLED
        if reason:
            self.notes = f"Cancelled: {reason}"

    def get_datetime(self) -> datetime:
        """Get appointment as datetime object"""
        return datetime.combine(self.appointment_date, self.appointment_time)

    @property
    def is_upcoming(self) -> bool:
        """Check if appointment is in the future"""
        return self.appointment_date >= date.today() and self.status != AppointmentStatus.CANCELLED

    def __str__(self) -> str:
        """Return string representation of the appointment"""
        time_str = self.appointment_time.strftime("%H:%M")
        return (f"{self.animal.name} with Dr. {self.veterinarian.full_name} "
                f"on {self.appointment_date} at {time_str} | Status: {self.status.value}")


class Treatment:
    """Represents a treatment given to an animal during an appointment"""

    def __init__(self, name: str, treatment_type: TreatmentType, 
                 description: str = ""):
        """Initialize a Treatment instance"""
        self.name = name
        self.treatment_type = treatment_type
        self.description = description
        self.appointment: Optional[Appointment] = None
        self.medications_prescribed: List['Medication'] = []
        self.follow_up_date: Optional[date] = None
        self.cost: float = 0.0

    def add_medication(self, medication: 'Medication') -> None:
        """Add a prescribed medication to this treatment"""
        self.medications_prescribed.append(medication)

    def __str__(self) -> str:
        """Return string representation of the treatment"""
        return f"{self.name} ({self.treatment_type.value})"


class Medication:
    """Represents a medication prescribed to an animal"""

    def __init__(self, name: str, dosage: str, frequency: str, 
                 start_date: date, end_date: Optional[date] = None):
        """Initialize a Medication instance"""
        self.name = name
        self.dosage = dosage  # e.g., "500mg", "1 tablet"
        self.frequency = frequency  # e.g., "twice daily", "every 8 hours"
        self.start_date = start_date
        self.end_date = end_date
        self.animal: Optional[Animal] = None
        self.prescribed_by: Optional[Veterinarian] = None
        self.notes: str = ""

    def is_active(self) -> bool:
        """Check if medication is currently active"""
        today = date.today()
        return self.start_date <= today and (not self.end_date or self.end_date >= today)

    def __str__(self) -> str:
        """Return string representation of the medication"""
        status = "Active" if self.is_active() else "Inactive"
        return f"{self.name} {self.dosage} - {self.frequency} ({status})"


class MedicalRecord:
    """Represents a medical record entry for an animal"""

    def __init__(self, date_recorded: date, record_type: str, details: str):
        """Initialize a MedicalRecord instance"""
        self.date_recorded = date_recorded
        self.record_type = record_type  # e.g., "vaccination", "surgery", "lab_result"
        self.details = details
        self.animal: Optional[Animal] = None
        self.recorded_by: Optional[Veterinarian] = None

    def __str__(self) -> str:
        """Return string representation of the medical record"""
        return f"{self.date_recorded} - {self.record_type}: {self.details[:50]}..."


class VetOffice:
    """Represents the veterinary clinic/office"""

    def __init__(self, name: str, address: str, phone: str, email: str):
        """Initialize a VetOffice instance"""
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.clients: List[Client] = []
        self.animals: List[Animal] = []
        self.veterinarians: List[Veterinarian] = []
        self.appointments: List[Appointment] = []
        self.total_revenue: float = 0.0

    def add_client(self, client: Client) -> None:
        """Register a new client"""
        self.clients.append(client)

    def add_animal(self, animal: Animal) -> None:
        """Register a new animal in the clinic"""
        if animal not in self.animals:
            self.animals.append(animal)

    def add_veterinarian(self, vet: Veterinarian) -> None:
        """Add a veterinarian to staff"""
        self.veterinarians.append(vet)

    def schedule_appointment(self, animal: Animal, veterinarian: Veterinarian,
                           appointment_date: date, appointment_time: time,
                           duration_minutes: int, reason: str = "") -> Appointment:
        """Schedule a new appointment"""
        appointment = Appointment(animal, veterinarian, appointment_date, 
                                 appointment_time, duration_minutes, reason)
        self.appointments.append(appointment)
        animal.add_appointment(appointment)
        veterinarian.appointments.append(appointment)
        return appointment

    def get_appointments_by_date(self, target_date: date) -> List[Appointment]:
        """Get all appointments for a specific date"""
        return [apt for apt in self.appointments if apt.appointment_date == target_date]

    def get_upcoming_appointments(self, days_ahead: int = 7) -> List[Appointment]:
        """Get upcoming appointments for the specified number of days"""
        today = date.today()
        cutoff = today + timedelta(days=days_ahead)
        upcoming = [apt for apt in self.appointments 
                   if today <= apt.appointment_date <= cutoff 
                   and apt.status != AppointmentStatus.CANCELLED]
        return sorted(upcoming, key=lambda x: (x.appointment_date, x.appointment_time))

    def find_client_by_name(self, first_name: str, last_name: str) -> Optional[Client]:
        """Search for a client by name"""
        for client in self.clients:
            if client.first_name.lower() == first_name.lower() and \
               client.last_name.lower() == last_name.lower():
                return client
        return None

    def find_animal_by_id(self, microchip_id: str) -> Optional[Animal]:
        """Search for an animal by microchip ID"""
        for animal in self.animals:
            if animal.microchip_id == microchip_id:
                return animal
        return None

    def get_client_count(self) -> int:
        """Return total number of clients"""
        return len(self.clients)

    def get_animal_count(self) -> int:
        """Return total number of animals"""
        return len(self.animals)

    def __str__(self) -> str:
        """Return string representation of the vet office"""
        return (f"{self.name}\n{self.address}\n"
                f"Phone: {self.phone}\nEmail: {self.email}\n"
                f"Clients: {self.get_client_count()} | Animals: {self.get_animal_count()} | "
                f"Staff: {len(self.veterinarians)}")
