"""
Vet Office Management Application
Streamlit app for managing clients, animals, appointments, and treatments
Includes AI-powered clinical decision support with Claude
"""

import streamlit as st
import pandas as pd
import os
import logging
from datetime import date, datetime, time, timedelta
from vet_office_system import (
    VetOffice, Client, Animal, Veterinarian, Appointment, 
    Treatment, Medication, MedicalRecord, Contact,
    AnimalSpecies, AppointmentStatus, TreatmentType
)
from vet_ai_assistant import VetAIAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Vet Office Manager",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .header {
        color: #2c3e50;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stat-box {
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3498db;
    }
    .success {
        color: #27ae60;
    }
    .warning {
        color: #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Initialize VetOffice in session state
if 'vet_office' not in st.session_state:
    office = VetOffice(
        name="Happy Paws Veterinary Clinic",
        address="123 Pet Street, Animal City, AC 12345",
        phone="(555) 123-4567",
        email="info@happypaws.vet"
    )
    
    # Add sample veterinarians
    vet1 = Veterinarian("Sarah", "Johnson", "VET123456", ["Small Animals", "Surgery"])
    vet2 = Veterinarian("David", "Chen", "VET789012", ["Exotic Animals", "Dentistry"])
    office.add_veterinarian(vet1)
    office.add_veterinarian(vet2)
    
    st.session_state.vet_office = office
    st.session_state.current_page = "Dashboard"

# Initialize AI Assistant
if 'ai_assistant' not in st.session_state:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    st.session_state.ai_assistant = VetAIAssistant(api_key=api_key)
    logger.info("AI Assistant initialized in session state")

vet_office = st.session_state.vet_office
ai_assistant = st.session_state.ai_assistant

# Sidebar navigation
with st.sidebar:
    st.markdown("---")
    st.markdown("# 🏥 Vet Office Manager")
    st.markdown("---")
    
    navigation = st.radio(
        "Navigation",
        ["Dashboard", "Clients", "Animals", "Appointments", "Treatments", "Staff", "🤖 AI Assistant"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Clients", vet_office.get_client_count())
    with col2:
        st.metric("Animals", vet_office.get_animal_count())

# Main content
st.markdown(f"<div class='header'>🏥 {vet_office.name}</div>", unsafe_allow_html=True)

if navigation == "Dashboard":
    # Dashboard
    st.subheader("Welcome to Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clients", vet_office.get_client_count())
    with col2:
        st.metric("Total Animals", vet_office.get_animal_count())
    with col3:
        st.metric("Veterinarians", len(vet_office.veterinarians))
    with col4:
        upcoming = vet_office.get_upcoming_appointments(7)
        st.metric("Upcoming Appointments", len(upcoming))
    
    st.markdown("---")
    
    # Upcoming appointments
    st.subheader("📅 Upcoming Appointments (Next 7 Days)")
    upcoming_apts = vet_office.get_upcoming_appointments(7)
    
    if upcoming_apts:
        apt_data = []
        for apt in upcoming_apts:
            apt_data.append({
                "Date": apt.appointment_date.strftime("%Y-%m-%d"),
                "Time": apt.appointment_time.strftime("%H:%M"),
                "Animal": apt.animal.name,
                "Owner": apt.animal.owner.full_name if apt.animal.owner else "Unknown",
                "Veterinarian": f"Dr. {apt.veterinarian.full_name}",
                "Reason": apt.reason or "Check-up",
                "Status": apt.status.value.replace("_", " ").title()
            })
        
        df = pd.DataFrame(apt_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("✅ No upcoming appointments in the next 7 days")

elif navigation == "Clients":
    st.subheader("👥 Client Management")
    
    tab1, tab2, tab3 = st.tabs(["View Clients", "Add New Client", "Client Details"])
    
    with tab1:
        st.markdown("#### All Clients")
        if vet_office.get_client_count() > 0:
            client_data = []
            for client in vet_office.clients:
                client_data.append({
                    "Name": client.full_name,
                    "Phone": client.contact.phone,
                    "Email": client.contact.email,
                    "Animals": len(client.animals),
                    "Joined": client.date_joined.strftime("%Y-%m-%d")
                })
            
            df = pd.DataFrame(client_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No clients registered yet.")
    
    with tab2:
        st.markdown("#### Register New Client")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Phone Number")
        with col2:
            email = st.text_input("Email Address")
        
        col1, col2 = st.columns(2)
        with col1:
            address = st.text_input("Address")
        with col2:
            city = st.text_input("City")
        
        col1, col2 = st.columns(2)
        with col1:
            state = st.text_input("State")
        with col2:
            zip_code = st.text_input("ZIP Code")
        
        notes = st.text_area("Additional Notes (optional)")
        
        if st.button("✅ Register Client", key="add_client"):
            if first_name and last_name and phone and email:
                contact = Contact(
                    phone=phone,
                    email=email,
                    address=address,
                    city=city,
                    state=state,
                    zip_code=zip_code
                )
                client = Client(first_name, last_name, contact)
                if notes:
                    client.notes = notes
                
                vet_office.add_client(client)
                st.success(f"✅ Client {client.full_name} registered successfully!")
            else:
                st.error("Please fill in all required fields.")
    
    with tab3:
        st.markdown("#### Search Client Details")
        search_name = st.text_input("Search by name (first last):")
        
        if search_name:
            parts = search_name.split()
            if len(parts) == 2:
                client = vet_office.find_client_by_name(parts[0], parts[1])
                if client:
                    st.markdown(f"### {client.full_name}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Phone:** {client.contact.phone}")
                    with col2:
                        st.markdown(f"**Email:** {client.contact.email}")
                    with col3:
                        st.markdown(f"**Joined:** {client.date_joined}")
                    
                    if client.contact.address:
                        st.markdown(f"**Address:** {client.contact.address}, {client.contact.city}, {client.contact.state} {client.contact.zip_code}")
                    
                    st.markdown("#### Animals")
                    if client.animals:
                        for animal in client.animals:
                            st.write(f"- **{animal.name}** ({animal.species.value}) - {animal.breed}, {animal.age_years:.1f} years old")
                    else:
                        st.info("No animals registered for this client.")
                else:
                    st.warning("Client not found.")

elif navigation == "Animals":
    st.subheader("🐾 Animal Management")
    
    tab1, tab2, tab3 = st.tabs(["View Animals", "Register Animal", "Animal Details"])
    
    with tab1:
        st.markdown("#### All Animals in System")
        if vet_office.get_animal_count() > 0:
            animal_data = []
            for animal in vet_office.animals:
                owner = animal.owner.full_name if animal.owner else "No owner"
                animal_data.append({
                    "Name": animal.name,
                    "Species": animal.species.value.title(),
                    "Breed": animal.breed,
                    "Age": f"{animal.age_years:.1f} years",
                    "Owner": owner,
                    "Status": "Active" if not animal.is_deceased else "Deceased"
                })
            
            df = pd.DataFrame(animal_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No animals registered yet.")
    
    with tab2:
        st.markdown("#### Register New Animal")
        
        # Select owner
        if vet_office.clients:
            client_names = [f"{c.full_name}" for c in vet_office.clients]
            selected_client = st.selectbox("Select Client (Owner)", client_names)
            selected_owner = vet_office.find_client_by_name(
                selected_client.split()[0], 
                " ".join(selected_client.split()[1:])
            )
        else:
            st.warning("Please register a client first.")
            st.stop()
        
        # Animal details
        col1, col2 = st.columns(2)
        with col1:
            animal_name = st.text_input("Animal Name")
        with col2:
            species = st.selectbox("Species", [s.value for s in AnimalSpecies])
        
        col1, col2 = st.columns(2)
        with col1:
            breed = st.text_input("Breed")
        with col2:
            dob = st.date_input("Date of Birth")
        
        col1, col2 = st.columns(2)
        with col1:
            microchip = st.text_input("Microchip ID (optional)")
        with col2:
            weight = st.number_input("Weight (kg)", min_value=0.1, value=5.0)
        
        allergies = st.text_area("Known Allergies (comma-separated)")
        notes = st.text_area("Medical Notes")
        
        if st.button("✅ Register Animal", key="add_animal"):
            if animal_name and breed and dob:
                animal = Animal(
                    name=animal_name,
                    species=AnimalSpecies(species),
                    breed=breed,
                    date_of_birth=dob,
                    microchip_id=microchip if microchip else ""
                )
                animal.weight_kg = weight
                
                if allergies:
                    animal.allergies = [a.strip() for a in allergies.split(",")]
                if notes:
                    animal.notes = notes
                
                selected_owner.add_animal(animal)
                vet_office.add_animal(animal)
                
                st.success(f"✅ {animal.name} registered successfully!")
            else:
                st.error("Please fill in required fields.")
    
    with tab3:
        st.markdown("#### Search Animal Details")
        if vet_office.animals:
            animal_names = [animal.name for animal in vet_office.animals]
            selected_animal_name = st.selectbox("Select Animal", animal_names)
            
            selected_animal = next(
                (a for a in vet_office.animals if a.name == selected_animal_name),
                None
            )
            
            if selected_animal:
                st.markdown(f"### {selected_animal.name}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Species:** {selected_animal.species.value.title()}")
                with col2:
                    st.markdown(f"**Breed:** {selected_animal.breed}")
                with col3:
                    st.markdown(f"**Age:** {selected_animal.age_years:.1f} years")
                
                if selected_animal.owner:
                    st.markdown(f"**Owner:** {selected_animal.owner.full_name}")
                
                if selected_animal.microchip_id:
                    st.markdown(f"**Microchip ID:** {selected_animal.microchip_id}")
                
                st.markdown(f"**Weight:** {selected_animal.weight_kg} kg")
                
                if selected_animal.allergies:
                    st.markdown(f"**🚨 Allergies:** {', '.join(selected_animal.allergies)}")
                
                if selected_animal.notes:
                    st.markdown(f"**Notes:** {selected_animal.notes}")
                
                st.markdown("#### Active Medications")
                active_meds = selected_animal.get_active_medications()
                if active_meds:
                    for med in active_meds:
                        st.write(f"- {med}")
                else:
                    st.info("No active medications.")
                
                st.markdown("#### Upcoming Appointments")
                upcoming_apts = selected_animal.get_upcoming_appointments()
                if upcoming_apts:
                    for apt in upcoming_apts:
                        st.write(f"- {apt.appointment_date.strftime('%Y-%m-%d')} at {apt.appointment_time.strftime('%H:%M')} with Dr. {apt.veterinarian.full_name}")
                else:
                    st.info("No upcoming appointments.")
        else:
            st.info("No animals to display.")

elif navigation == "Appointments":
    st.subheader("📅 Appointment Scheduling")
    
    tab1, tab2 = st.tabs(["Schedule Appointment", "View Appointments"])
    
    with tab1:
        st.markdown("#### Schedule New Appointment")
        
        if not vet_office.animals:
            st.warning("Please register an animal first.")
            st.stop()
        
        if not vet_office.veterinarians:
            st.warning("Please add a veterinarian first.")
            st.stop()
        
        # Select animal
        animal_names = [a.name for a in vet_office.animals]
        selected_animal_name = st.selectbox("Select Animal", animal_names)
        selected_animal = next(a for a in vet_office.animals if a.name == selected_animal_name)
        
        # Select veterinarian
        vet_names = [f"Dr. {v.full_name}" for v in vet_office.veterinarians]
        selected_vet_name = st.selectbox("Select Veterinarian", vet_names)
        selected_vet = next(v for v in vet_office.veterinarians if f"Dr. {v.full_name}" == selected_vet_name)
        
        # Appointment details
        col1, col2 = st.columns(2)
        with col1:
            apt_date = st.date_input("Appointment Date", min_value=date.today())
        with col2:
            apt_time = st.time_input("Appointment Time", value=time(10, 0))
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=15, value=30, step=15)
        with col2:
            reason = st.text_input("Reason for Visit")
        
        if st.button("✅ Schedule Appointment", key="schedule_apt"):
            if reason:
                apt = vet_office.schedule_appointment(
                    selected_animal, selected_vet, apt_date, apt_time, duration, reason
                )
                st.success(f"✅ Appointment scheduled for {selected_animal.name}!")
            else:
                st.error("Please provide a reason for the visit.")
    
    with tab2:
        st.markdown("#### View Appointments")
        
        date_filter = st.date_input("Filter by date", value=date.today())
        matching_apts = vet_office.get_appointments_by_date(date_filter)
        
        if matching_apts:
            apt_data = []
            for apt in matching_apts:
                apt_data.append({
                    "Time": apt.appointment_time.strftime("%H:%M"),
                    "Animal": apt.animal.name,
                    "Owner": apt.animal.owner.full_name if apt.animal.owner else "Unknown",
                    "Doctor": f"Dr. {apt.veterinarian.full_name}",
                    "Duration": f"{apt.duration_minutes} min",
                    "Reason": apt.reason or "Check-up",
                    "Status": apt.status.value.replace("_", " ").title()
                })
            
            df = pd.DataFrame(apt_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No appointments scheduled for {date_filter.strftime('%Y-%m-%d')}")

elif navigation == "Treatments":
    st.subheader("💊 Treatment Management")
    
    st.markdown("#### Add Treatment & Medication")
    
    if not vet_office.appointments:
        st.warning("Please schedule an appointment first.")
        st.stop()
    
    # Select completed or in-progress appointments
    available_apts = [apt for apt in vet_office.appointments 
                     if apt.status in [AppointmentStatus.SCHEDULED, AppointmentStatus.COMPLETED, AppointmentStatus.IN_PROGRESS]]
    
    if available_apts:
        apt_labels = [f"{apt.animal.name} - {apt.appointment_date} {apt.appointment_time} with Dr. {apt.veterinarian.full_name}" 
                     for apt in available_apts]
        selected_apt_label = st.selectbox("Select Appointment", apt_labels)
        selected_apt = available_apts[apt_labels.index(selected_apt_label)]
        
        # Treatment details
        treatment_type = st.selectbox("Treatment Type", [t.value for t in TreatmentType])
        treatment_name = st.text_input("Treatment Name")
        treatment_desc = st.text_area("Treatment Description")
        treatment_cost = st.number_input("Cost ($)", min_value=0.0, value=0.0, step=0.01)
        
        col1, col2 = st.columns(2)
        with col1:
            add_medication = st.checkbox("Add Medication Prescription")
        
        med_data = {}
        if add_medication:
            with col2:
                st.markdown("")  # Spacing
            
            med_name = st.text_input("Medication Name")
            med_dosage = st.text_input("Dosage (e.g., 500mg, 1 tablet)")
            med_frequency = st.text_input("Frequency (e.g., twice daily)")
            
            col1, col2 = st.columns(2)
            with col1:
                med_start = st.date_input("Start Date", value=date.today())
            with col2:
                med_end = st.date_input("End Date (optional)", value=None)
            
            med_data = {
                "name": med_name,
                "dosage": med_dosage,
                "frequency": med_frequency,
                "start": med_start,
                "end": med_end
            }
        
        if st.button("✅ Add Treatment", key="add_treatment"):
            if treatment_name:
                treatment = Treatment(treatment_name, TreatmentType(treatment_type), treatment_desc)
                treatment.cost = treatment_cost
                
                if add_medication and med_data["name"]:
                    med = Medication(
                        med_data["name"],
                        med_data["dosage"],
                        med_data["frequency"],
                        med_data["start"],
                        med_data["end"]
                    )
                    med.animal = selected_apt.animal
                    treatment.add_medication(med)
                    selected_apt.animal.add_medication(med)
                
                selected_apt.add_treatment(treatment)
                selected_apt.cost += treatment_cost
                
                st.success(f"✅ Treatment added to {selected_apt.animal.name}'s appointment!")
            else:
                st.error("Please enter a treatment name.")
    else:
        st.info("No appointments available.")

elif navigation == "Staff":
    st.subheader("👨‍⚕️ Veterinary Staff")
    
    tab1, tab2 = st.tabs(["View Staff", "Add Veterinarian"])
    
    with tab1:
        st.markdown("#### Staff Directory")
        if vet_office.veterinarians:
            staff_data = []
            for vet in vet_office.veterinarians:
                staff_data.append({
                    "Name": vet.full_name,
                    "License #": vet.license_number,
                    "Specialties": ", ".join(vet.specialties) if vet.specialties else "General Practice",
                    "Status": "Available" if vet.is_available else "Unavailable",
                    "Appointments": len(vet.appointments)
                })
            
            df = pd.DataFrame(staff_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No veterinarians on staff.")
    
    with tab2:
        st.markdown("#### Add New Veterinarian")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        license_num = st.text_input("License Number")
        specialties = st.multiselect(
            "Specialties",
            ["Small Animals", "Large Animals", "Exotic Animals", "Surgery", 
             "Dentistry", "Dermatology", "Cardiology", "Oncology"]
        )
        
        if st.button("✅ Add Veterinarian", key="add_vet"):
            if first_name and last_name and license_num:
                vet = Veterinarian(first_name, last_name, license_num, specialties)
                vet_office.add_veterinarian(vet)
                st.success(f"✅ Dr. {vet.full_name} added to staff!")
            else:
                st.error("Please fill in all required fields.")

elif navigation == "🤖 AI Assistant":
    st.subheader("🤖 AI Clinical Decision Support")
    
    # Check if AI is available
    if not ai_assistant.is_available():
        st.warning(
            "⚠️  **AI Assistant Not Configured**\n\n"
            "To enable AI features, set your ANTHROPIC_API_KEY environment variable:\n\n"
            "```bash\nexport ANTHROPIC_API_KEY='your-api-key-here'\nstreamlit run vet_app.py\n```\n\n"
            "Get your API key at: https://console.anthropic.com/"
        )
        st.info("AI features enabled: Symptom Analysis, Appointment Notes, Drug Interactions, Treatment Planning, Cost Estimation")
    
    st.markdown("""
    The AI Clinical Assistant uses Retrieval-Augmented Generation (RAG) to provide evidence-based clinical decision support.
    It retrieves the patient's medical history and analyzes current presentations to make informed recommendations.
    
    **Important**: AI recommendations should complement, not replace, professional veterinary judgment.
    """)
    
    st.divider()
    
    # AI Features tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Symptom Analysis",
        "Appointment Notes",
        "Drug Interactions",
        "Follow-up Planning",
        "Cost Estimation",
        "AI Status"
    ])
    
    with tab1:
        st.markdown("#### 🔍 Symptom Analysis & Diagnosis Support")
        st.markdown("Analyze symptoms and get differential diagnoses based on patient history.")
        
        if vet_office.animals:
            animal_names = [a.name for a in vet_office.animals]
            selected_animal = st.selectbox("Select Animal", animal_names, key="symptom_animal")
            target_animal = next(a for a in vet_office.animals if a.name == selected_animal)
            
            st.write(f"**Patient**: {target_animal.name} ({target_animal.species.value}), {target_animal.age_years:.1f} years old")
            
            symptoms = st.text_area("Describe the animal's symptoms:", placeholder="e.g., Lethargy, loss of appetite, vomiting for 2 days")
            additional_notes = st.text_area("Additional observations:", placeholder="e.g., Recent dietary changes, environmental factors")
            
            if st.button("🔬 Analyze Symptoms", key="analyze_symptoms"):
                if symptoms:
                    with st.spinner("Analyzing symptoms and retrieving medical history..."):
                        try:
                            recommendation = ai_assistant.analyze_symptoms(
                                target_animal, symptoms, vet_office, additional_notes
                            )
                            
                            if recommendation:
                                st.success("Analysis Complete!")
                                st.markdown(str(recommendation))
                                
                                with st.callout("info"):
                                    st.markdown("""
                                    **⚠️  Clinical Note**: This AI analysis is based on the patient's history and current presentation.
                                    Always perform appropriate diagnostic tests and use your professional judgment.
                                    """)
                            else:
                                st.warning("Could not complete analysis. Please check API key.")
                        except Exception as e:
                            st.error(f"Error during analysis: {str(e)}")
                            logger.error(f"Symptom analysis error: {e}")
                else:
                    st.error("Please describe the symptoms.")
        else:
            st.info("No animals registered yet.")
    
    with tab2:
        st.markdown("#### 📝 Generate Professional Appointment Notes")
        st.markdown("Auto-generate SOAP notes from appointment observations using patient history.")
        
        if vet_office.appointments:
            incomplete_apts = [apt for apt in vet_office.appointments 
                             if apt.status != AppointmentStatus.CANCELLED]
            
            if incomplete_apts:
                apt_labels = [f"{apt.animal.name} - {apt.appointment_date} - Dr. {apt.veterinarian.full_name}" 
                             for apt in incomplete_apts]
                selected_apt_idx = st.selectbox("Select Appointment", range(len(incomplete_apts)), 
                                               format_func=lambda i: apt_labels[i], key="notes_apt")
                selected_apt = incomplete_apts[selected_apt_idx]
                
                st.write(f"**Patient**: {selected_apt.animal.name}")
                st.write(f"**Appointment**: {selected_apt.appointment_date} at {selected_apt.appointment_time}  ")
                st.write(f"**Reason**: {selected_apt.reason}")
                
                observations = st.text_area(
                    "Clinical Observations:",
                    placeholder="Describe what you observed during the examination..."
                )
                
                if st.button("✍️ Generate Notes", key="gen_notes"):
                    if observations:
                        with st.spinner("Generating professional appointment notes..."):
                            try:
                                notes = ai_assistant.generate_appointment_notes(
                                    selected_apt.animal, selected_apt, observations
                                )
                                
                                if notes:
                                    st.success("Notes Generated!")
                                    st.markdown(notes)
                                    
                                    # Option to copy to appointment
                                    if st.button("📋 Copy to Appointment", key="copy_notes"):
                                        selected_apt.notes = notes
                                        st.success("Notes saved to appointment!")
                                else:
                                    st.warning("Could not generate notes. Please check API key.")
                            except Exception as e:
                                st.error(f"Error generating notes: {str(e)}")
                                logger.error(f"Note generation error: {e}")
                    else:
                        st.error("Please describe your observations.")
            else:
                st.info("No appointments available.")
        else:
            st.info("No appointments scheduled yet.")
    
    with tab3:
        st.markdown("#### 💊 Drug Interaction Checking")
        st.markdown("Check for potential interactions with current medications before prescribing.")
        
        if vet_office.animals:
            animal_names = [a.name for a in vet_office.animals]
            selected_animal = st.selectbox("Select Animal", animal_names, key="drug_animal")
            target_animal = next(a for a in vet_office.animals if a.name == selected_animal)
            
            st.write(f"**Patient**: {target_animal.name}")
            
            # Show current medications
            active_meds = target_animal.get_active_medications()
            if active_meds:
                st.markdown("**Current Medications**:")
                for med in active_meds:
                    st.write(f"- {med.name} {med.dosage}")
            else:
                st.info("No active medications.")
            
            new_med_name = st.text_input("New Medication to Prescribe:")
            new_med_dosage = st.text_input("Dosage and Frequency:", placeholder="e.g., 500mg twice daily")
            
            if st.button("⚠️  Check Interactions", key="check_interactions"):
                if new_med_name and new_med_dosage:
                    with st.spinner("Checking drug interactions..."):
                        try:
                            recommendation = ai_assistant.check_drug_interactions(
                                target_animal, new_med_name, new_med_dosage
                            )
                            
                            if recommendation:
                                st.markdown(str(recommendation))
                            else:
                                st.warning("Could not check interactions. Please check API key.")
                        except Exception as e:
                            st.error(f"Error checking interactions: {str(e)}")
                            logger.error(f"Interaction check error: {e}")
                else:
                    st.error("Please enter medication name and dosage.")
        else:
            st.info("No animals registered yet.")
    
    with tab4:
        st.markdown("#### 📅 Treatment Follow-Up Planning")
        st.markdown("Get AI recommendations for follow-up care and monitoring.")
        
        if vet_office.appointments:
            completed_apts = [apt for apt in vet_office.appointments 
                            if apt.status == AppointmentStatus.COMPLETED and apt.treatments]
            
            if completed_apts:
                apt_labels = [f"{apt.animal.name} - {apt.appointment_date} - {apt.treatments[0].name if apt.treatments else 'Unknown'}" 
                             for apt in completed_apts[-10:]]  # Last 10
                selected_apt_idx = st.selectbox("Select Completed Treatment", range(len(completed_apts)), 
                                               format_func=lambda i: apt_labels[i], key="followup_apt")
                selected_apt = completed_apts[selected_apt_idx]
                selected_treatment = selected_apt.treatments[0] if selected_apt.treatments else None
                
                if selected_treatment:
                    st.write(f"**Patient**: {selected_apt.animal.name}")
                    st.write(f"**Treatment**: {selected_treatment.name}")
                    st.write(f"**Date**: {selected_apt.appointment_date}")
                    
                    if st.button("🔮 Get Follow-up Recommendations", key="followup"):
                        with st.spinner("Planning follow-up care..."):
                            try:
                                recommendation = ai_assistant.recommend_followup(
                                    selected_apt.animal, selected_treatment, vet_office
                                )
                                
                                if recommendation:
                                    st.success("Follow-up Plan Generated!")
                                    st.markdown(str(recommendation))
                                else:
                                    st.warning("Could not generate plan. Please check API key.")
                            except Exception as e:
                                st.error(f"Error generating plan: {str(e)}")
                                logger.error(f"Follow-up planning error: {e}")
            else:
                st.info("No completed treatments to plan follow-up for.")
        else:
            st.info("No appointments available.")
    
    with tab5:
        st.markdown("#### 💰 Treatment Cost Estimation")
        st.markdown("Estimate treatment costs based on similar cases in your clinic.")
        
        if vet_office.animals:
            animal_names = [a.name for a in vet_office.animals]
            selected_animal = st.selectbox("Select Animal", animal_names, key="cost_animal")
            target_animal = next(a for a in vet_office.animals if a.name == selected_animal)
            
            st.write(f"**Patient**: {target_animal.name} ({target_animal.species.value})")
            
            treatments = st.multiselect(
                "Planned Treatments:",
                ["Vaccination", "Exam", "Dental Cleaning", "Blood Work", "Ultrasound", 
                 "X-Ray", "Surgery", "Wound Care", "Other"],
                key="treatment_list"
            )
            
            if st.button("💵 Estimate Costs", key="estimate_cost"):
                if treatments:
                    with st.spinner("Estimating treatment costs..."):
                        try:
                            estimate = ai_assistant.estimate_cost(
                                target_animal, treatments, vet_office
                            )
                            
                            if estimate:
                                st.success("Cost Estimate Generated!")
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Estimated Total", f"${estimate['total']:.2f}")
                                with col2:
                                    st.metric("Low Range", f"${estimate['range'][0]:.2f}")
                                with col3:
                                    st.metric("High Range", f"${estimate['range'][1]:.2f}")
                                
                                if estimate.get('notes'):
                                    st.info(f"**Notes**: {estimate['notes']}")
                            else:
                                st.warning("Could not estimate costs. Please check API key.")
                        except Exception as e:
                            st.error(f"Error estimating costs: {str(e)}")
                            logger.error(f"Cost estimation error: {e}")
                else:
                    st.error("Please select at least one treatment.")
        else:
            st.info("No animals registered yet.")
    
    with tab6:
        st.markdown("#### 📊 AI Assistant Status")
        
        status = ai_assistant.get_ai_status()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("AI Available", "✅ Yes" if status['available'] else "❌ No")
        with col2:
            st.metric("Model", status['model'])
        with col3:
            st.metric("Cache Size", status['cache_size'])
        
        st.divider()
        
        if status['available']:
            st.success("🚀 AI Clinical Assistant is ready for use!")
            st.markdown("""
            ### Features Available:
            - ✅ **Symptom Analysis** - Differential diagnosis with RAG
            - ✅ **Appointment Notes** - Auto-generate SOAP notes
            - ✅ **Drug Interactions** - Safety checking before prescription
            - ✅ **Follow-up Planning** - Post-treatment care recommendations
            - ✅ **Cost Estimation** - Price predictions based on cases
            
            ### How It Works:
            1. **Retrieval-Augmented Generation (RAG)**: AI retrieves the patient's complete medical history
            2. **Contextual Analysis**: Recommendations are based on specific patient data
            3. **Confidence Scoring**: Each recommendation includes reliability assessment
            4. **Safety Guardrails**: Allergies and drug interactions are checked automatically
            """)
        else:
            st.error("""
            ❌ **AI Assistant Not Available**
            
            Configure your ANTHROPIC_API_KEY to enable AI features.
            """)
        
        st.divider()
        st.markdown("### System Information")
        st.json({
            "model": status['model'],
            "available": status['available'],
            "rag_cache_items": status['cache_size']
        })

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>"
    "<p>Vet Office Management System with AI Clinical Decision Support | © 2024 Happy Paws Clinic</p>"
    "</div>",
    unsafe_allow_html=True
)

