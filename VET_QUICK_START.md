# Vet Office Management System - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd /Users/reihannaaa/ai-system-project
pip install streamlit pandas
```

### Step 2: Run the Web Application

```bash
streamlit run vet_app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 3: Start Using the System

#### First Time Setup
1. Navigate to the **Staff** tab and add veterinarians
2. Go to **Clients** and register your first client
3. Select **Animals** and register an animal for that client
4. Create **Appointments** by scheduling a visit

## 📋 Common Tasks

### Register a New Client
```
Clients → Add New Client → Fill form → Register Client
```

**What You Need:**
- First and last name
- Phone number
- Email address
- (Optional) Full address

### Add an Animal
```
Animals → Register Animal → Select Owner → Fill form → Register Animal
```

**What You Need:**
- Client (owner) name
- Animal name
- Species (Dog, Cat, etc.)
- Breed
- Date of birth

### Schedule an Appointment
```
Appointments → Schedule Appointment → Select animal → Select vet → Set date/time → Schedule
```

**What You Need:**
- Animal to be seen
- Veterinarian
- Date and time
- Duration (in 15-minute increments)
- Reason for visit

### Record a Treatment
```
Treatments → Select appointment → Enter treatment info → (Optional) Add medication → Add Treatment
```

**What You Need:**
- Appointment to attach treatment to
- Treatment name and type
- (Optional) Medication name, dosage, frequency, and dates

## 🎯 Key Features Overview

### Dashboard
Quick view of:
- Total clients and animals
- Veterinarians on staff
- Upcoming appointments this week

### Client Management
- Register new clients with contact info
- View all clients
- See animals associated with each client
- Track appointment history

### Animal Records
- Complete patient profiles
- Track weight, allergies, microchip ID
- View medical history
- Monitor active medications
- Schedule and track appointments

### Appointment System
- Schedule with specific date, time, and veterinarian
- Track status (scheduled, completed, cancelled)
- View upcoming appointments by date
- See appointment details with treatments

### Treatment & Medication
- Record treatments during appointments
- Prescribe medications with dosage and frequency
- Set medication start and end dates
- Automatically track active medications

### Staff Management
- Add veterinarians with specialties
- Track their appointment schedules
- Manage availability

## 💻 Command-Line Usage

### Run Example Script
```bash
python vet_office_example.py
```

This demonstrates all system features with sample data.

### Python API Example
```python
from vet_office_system import VetOffice, Client, Animal, Contact, AnimalSpecies
from datetime import date, time

# Create clinic
clinic = VetOffice("My Clinic", "123 Main St", "(555) 123-4567", "info@clinic.vet")

# Add client
contact = Contact("(555) 111-2222", "client@email.com")
client = Client("John", "Doe", contact)
clinic.add_client(client)

# Add animal
animal = Animal("Fluffy", AnimalSpecies.CAT, "Tabby", date(2020, 5, 15))
client.add_animal(animal)
clinic.add_animal(animal)

print(f"Registered: {animal} for {client.full_name}")
```

## 🔍 Finding Information

### Search Clients
```
Clients → Client Details → Type client name → View details
```

### View Animal Medical History
```
Animals → Animal Details → Select animal → View medications and appointments
```

### Check Veterinarian Schedule
```
Staff → View Staff → Click on veterinarian name
```

### Find Appointments by Date
```
Appointments → View Appointments → Select date
```

## ⚙️ Configuration

### Default Clinic Settings
The app comes pre-configured with "Happy Paws Veterinary Clinic" and two sample veterinarians. You can:
1. Modify clinic info (name, address, contact)
2. Add more veterinarians via the Staff tab
3. Register clients and animals

### Session State
All data is stored in Streamlit's session state for the current session. To persist data between sessions, consider:
- Adding database support (SQLite, PostgreSQL)
- Exporting data to CSV
- Implementing file-based storage

## 📱 Tips & Tricks

### Creating Recurring Appointments
While there's no automatic recurring feature, you can:
1. Create initial appointment
2. At completion, manually create the next one (e.g., in 1 month)

### Bulk Import Clients
To import multiple clients/animals, implement:
- CSV upload feature
- Manual data entry repeated for each client

### Printing Reports
Current implementation displays data in tables that can be:
- Copied to clipboard
- Exported via Streamlit's download feature

## ❓ Common Questions

**Q: Can I import existing client data?**
A: Currently, client data is entered manually. A CSV import feature can be added.

**Q: Where is data stored?**
A: Data is stored in Streamlit's session state (in-memory). Add database persistence to save long-term.

**Q: Can multiple users access simultaneously?**
A: Streamlit runs separate sessions per user. For multi-user concurrent access, add a database backend.

**Q: How do I backup my data?**
A: Export data to CSV files or implement database backups.

**Q: Can I delete clients/animals?**
A: The current system supports marking animals as deceased but doesn't have a delete feature. You can add this functionality.

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Please register a client first" | Go to Clients tab and add a client |
| "Please add a veterinarian first" | Go to Staff tab and add a vet |
| Appointments not showing | Check date filter, verify appointment date matches |
| Medication not showing as active | Verify medication start date is today or earlier and end date is today or later |

## 📚 Further Customization

### Add New Features
The system is designed for easy extension. Add features like:
- Insurance claim submission
- Vaccination reminder system
- Invoice/billing system
- SMS/Email notifications

### Database Integration
Replace session state with a database:
- SQLite for small clinics
- PostgreSQL for larger operations
- Connection code in separate module

### Authentication
Add login/logout:
- Different roles (admin, vet, receptionist)
- Data access controls
- Audit logging

## 📞 Support

For questions or issues:
1. Check the [VET_OFFICE_README.md](VET_OFFICE_README.md) for detailed documentation
2. Review [vet_office_example.py](vet_office_example.py) for usage examples
3. Examine [vet_office_system.py](vet_office_system.py) for class documentation

---

**Enjoy managing your veterinary practice!** 🐾
