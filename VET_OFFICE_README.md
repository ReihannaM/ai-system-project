# Vet Office Management System

Transform your veterinary practice with a comprehensive digital management system designed to streamline client relations, appointment scheduling, treatment tracking, and medical records.

## Features

### 🏥 Core Management
- **Client Management**: Register and manage pet owners with complete contact information
- **Animal Records**: Maintain detailed health profiles for each patient including species, breed, age, microchip ID, weight, and medical history
- **Appointment Scheduling**: Schedule appointments with specific veterinarians, track status, and manage cancellations
- **Treatment Tracking**: Record treatments given during appointments with associated costs
- **Medication Management**: Prescribe medications with dosage, frequency, and duration tracking
- **Medical Records**: Maintain comprehensive medical history for each animal
- **Staff Management**: Manage veterinary staff with specialties and appointment tracking

### 📊 Key Capabilities

#### Client Management
- Register new clients with full contact details
- Track client's animals and appointment history
- Search and retrieve client information
- Maintain notes on client preferences and communication history

#### Animal Patient Records
- Complete patient profiles including species, breed, age, and weight
- Microchip ID tracking
- Allergy and special needs documentation
- Active medication tracking
- Medical record history
- Appointment scheduling and history

#### Appointment System
- Schedule appointments with date, time, duration, and reason
- Track appointment status (scheduled, confirmed, in-progress, completed, cancelled)
- View upcoming appointments by veterinarian
- Auto-sort appointments by date and time
- Support for multiple veterinarians

#### Treatment & Medication
- Record treatments during appointments with descriptions
- Track treatment costs
- Prescribe medications with specific dosage and frequency
- Set medication start and end dates
- Automatic active medication filtering
- Link medications to specific treatments

#### Veterinary Staff
- Register staff with license numbers and specialties
- Track appointments per veterinarian
- View staff availability and upcoming schedule
- Support for multiple specialties per veterinarian

## Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Pandas

### Installation

```bash
# Clone or navigate to the project directory
cd ai-system-project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install streamlit pandas

# Run the application
streamlit run vet_app.py
```

## Usage Guide

### Dashboard
The main dashboard provides at-a-glance statistics:
- Total clients in practice
- Total animals registered
- Number of veterinary staff
- Upcoming appointments for the next 7 days

### Managing Clients

**To Add a New Client:**
1. Navigate to **Clients** tab
2. Select **Add New Client**
3. Enter client information (name, phone, email, address)
4. Click **Register Client**

**To View Client Details:**
1. Navigate to **Clients** > **Client Details**
2. Search by client name (first + last name)
3. View animals associated with the client

### Managing Animals

**To Register an Animal:**
1. Navigate to **Animals** > **Register Animal**
2. Select the client (owner)
3. Enter animal details (name, species, breed, date of birth)
4. Optionally add weight, microchip ID, allergies, and notes
5. Click **Register Animal**

**To View Animal Details:**
1. Navigate to **Animals** > **Animal Details**
2. Select animal from dropdown
3. View complete profile including medications and appointments

### Scheduling Appointments

**To Schedule an Appointment:**
1. Navigate to **Appointments** > **Schedule Appointment**
2. Select the animal
3. Select veterinarian
4. Choose appointment date and time
5. Set duration (in 15-minute increments)
6. Enter reason for visit
7. Click **Schedule Appointment**

**To View Appointments:**
1. Navigate to **Appointments** > **View Appointments**
2. Select date to view appointments for that day
3. View all scheduled appointments with details

### Recording Treatments

**To Add Treatment and Medication:**
1. Navigate to **Treatments**
2. Select the appointment
3. Enter treatment name and type
4. Optionally add medication prescription with dosage and frequency
5. Set medication start and end dates
6. Click **Add Treatment**

### Managing Staff

**To Add a Veterinarian:**
1. Navigate to **Staff** > **Add Veterinarian**
2. Enter name and license number
3. Select specialties
4. Click **Add Veterinarian**

**To View Staff:**
1. Navigate to **Staff** > **View Staff**
2. View complete staff directory with specialties and appointment counts

## System Architecture

### Core Classes

#### `Contact`
Manages contact information for clients.
- Phone, email, address, city, state, zip code

#### `Client`
Represents pet owners.
- Contact information
- Associated animals
- Payment tracking
- Notes

#### `Animal`
Represents patient animals.
- Species, breed, age, weight
- Microchip ID
- Medical history
- Appointments
- Current medications
- Allergies

#### `Veterinarian`
Represents veterinary staff.
- License number
- Specialties
- Appointment schedule
- Availability status

#### `Appointment`
Represents scheduled vet visits.
- Date and time
- Duration
- Status tracking
- Associated treatments
- Cost tracking

#### `Treatment`
Represents medical treatments.
- Type of treatment
- Associated appointment
- Medications prescribed
- Cost

#### `Medication`
Represents prescribed medications.
- Dosage and frequency
- Start and end dates
- Associated animal
- Prescribing veterinarian

#### `MedicalRecord`
Represents medical history entries.
- Date recorded
- Record type and details
- Recording veterinarian

#### `VetOffice`
Main clinic management system.
- Manages all clients, animals, staff
- Handles appointment scheduling
- Generates reports and statistics
- Provides search functionality

## Key Features in Detail

### Recurring Task Automation
While the original PawPal system used recurring tasks for pet care, the Vet Office System adapts this concept to appointment patterns:
- Medications with duration create automatic tracking
- Future appointment scheduling for follow-ups
- Treatment plan management

### Conflict Detection
- Veterinarian availability checking
- Overlapping appointment detection
- Time slot management

### Search & Filtering
- Find clients by name
- Search animals by microchip ID
- Filter appointments by date or veterinarian
- View medication histories

### Reporting & Analytics
- Dashboard summary statistics
- Upcoming appointment overview
- Staff scheduling information
- Treatment and medication tracking
- Revenue tracking

## Data Models

### Enumerations

**AnimalSpecies**: Dog, Cat, Bird, Rabbit, Hamster, Guinea Pig, Reptile, Other

**AppointmentStatus**: Scheduled, Confirmed, In Progress, Completed, Cancelled, No-Show

**TreatmentType**: Vaccination, Check-up, Surgery, Dental, Grooming, Medication, Diagnostic, Emergency, Other

## Security & Best Practices

### Recommendations
1. **Data Privacy**: Implement secure login and role-based access control
2. **Backup**: Regular backups of patient records
3. **Compliance**: Ensure HIPAA-equivalent compliance for animal records
4. **Audit Trail**: Log all changes to medical records
5. **Encryption**: Use encrypted storage for sensitive data

### Suggested Enhancements
- Patient photo/medical imaging storage
- Vaccine tracking and reminders
- Insurance claim processing integration
- Payment processing and invoicing
- Multi-clinic support with centralized management
- Mobile app for appointment reminders
- SMS/Email notifications for clients
- Prescription printing and refill management

## File Structure

```
ai-system-project/
├── vet_office_system.py      # Core system classes and logic
├── vet_app.py                 # Streamlit web application
├── README.md                  # Original PawPal documentation
├── requirements.txt           # Python dependencies
└── vet_office_example.py     # Example usage and sample data
```

## Example Usage

Refer to `vet_office_example.py` for detailed examples of:
- Creating clients and animals
- Scheduling appointments
- Recording treatments
- Managing medications
- Querying the system

## Troubleshooting

**Issue**: "Please register a client first"
- **Solution**: Add a client before registering animals

**Issue**: "Please schedule an appointment first"
- **Solution**: Schedule appointments before adding treatments

**Issue**: Appointment not appearing in list
- **Solution**: Verify the date and that appointment isn't cancelled

## Future Enhancements

- [ ] Automated appointment reminders
- [ ] Prescription management system
- [ ] Inventory tracking for supplies and medications
- [ ] Financial reporting and invoicing
- [ ] Integration with payment systems
- [ ] Telemedicine capabilities
- [ ] Multi-location support
- [ ] Advanced analytics and reporting
- [ ] Client portal for record access
- [ ] Mobile app integration

## Support

For issues, feature requests, or questions about the Vet Office Management System, please contact the development team.

---

**Version**: 1.0  
**Last Updated**: April 2024  
**Status**: Active Development
