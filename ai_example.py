"""
Vet Office AI Assistant - Example Usage
Demonstrates RAG-powered clinical decision support features
"""

import os
import logging
from datetime import date, time, timedelta
from vet_office_system import (
    VetOffice, Client, Animal, Veterinarian, Contact, 
    AnimalSpecies, AppointmentStatus
)
from vet_ai_assistant import VetAIAssistant

# Configure logging to see AI operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_test_clinic():
    """Create a test clinic with sample data for AI examples"""
    
    print("=" * 70)
    print("VET OFFICE AI CLINICAL ASSISTANT - EXAMPLE USAGE")
    print("=" * 70)
    
    # Create clinic
    clinic = VetOffice(
        name="Demo Vet Clinic",
        address="123 Demo St",
        phone="(555) 999-0000",
        email="demo@vetclinic.com"
    )
    
    # Add veterinarians
    dr_smith = Veterinarian(
        "Jennifer", "Smith", "VET001",
        ["Small Animals", "Surgery", "Internal Medicine"]
    )
    clinic.add_veterinarian(dr_smith)
    
    # Create clients
    contact1 = Contact(
        phone="(555) 111-0000",
        email="jane@email.com",
        address="456 Oak Ave",
        city="Demo City",
        state="CA",
        zip_code="90000"
    )
    
    client1 = Client("Jane", "Doe", contact1)
    clinic.add_client(client1)
    
    # Register animals
    # Animal 1: Dog with history
    dog = Animal(
        name="Buddy",
        species=AnimalSpecies.DOG,
        breed="Labrador Retriever",
        date_of_birth=date(2020, 6, 15),
        microchip_id="123ABC"
    )
    dog.weight_kg = 32.0
    dog.allergies = ["Chicken"]
    
    client1.add_animal(dog)
    clinic.add_animal(dog)
    
    # Animal 2: Cat with history
    cat = Animal(
        name="Whiskers",
        species=AnimalSpecies.CAT,
        breed="Siamese",
        date_of_birth=date(2019, 3, 20),
        microchip_id="456XYZ"
    )
    cat.weight_kg = 4.2
    cat.allergies = ["Fish-based medications"]
    
    client1.add_animal(cat)
    clinic.add_animal(cat)
    
    # Create an appointment for dog
    today = date.today()
    apt1 = clinic.schedule_appointment(
        animal=dog,
        veterinarian=dr_smith,
        appointment_date=today,
        appointment_time=time(14, 0),
        duration_minutes=30,
        reason="Limping on back left leg"
    )
    
    print(f"\n✅ Created test clinic: {clinic.name}")
    print(f"   - {len(clinic.clients)} client(s)")
    print(f"   - {len(clinic.animals)} animal(s)")
    print(f"   - {len(clinic.veterinarians)} veterinarian(s)")
    
    return clinic, dog, cat, apt1


def demonstrate_symptom_analysis(ai_assistant, clinic, dog):
    """Show RAG in action: Symptom analysis with medical history retrieval"""
    
    print("\n" + "=" * 70)
    print("FEATURE 1: SYMPTOM ANALYSIS (Retrieval-Augmented Generation)")
    print("=" * 70)
    
    print(f"\n🐕 Analyzing symptoms for: {dog.name}")
    print(f"   Breed: {dog.breed}")
    print(f"   Age: {dog.age_years:.1f} years")
    print(f"   Allergies: {', '.join(dog.allergies)}")
    
    # This is what gets retrieved (RAG step)
    print("\n📋 [RAG Step 1] Retrieved Medical History:")
    print(f"   - No previous medical records")
    print(f"   - No current medications")
    print(f"   - Chicken allergy documented")
    
    # Symptom to analyze
    symptoms = "Limping on back left leg for 2 days, not putting weight on it"
    additional = "No trauma observed, incident happened while playing"
    
    print(f"\n🔍 [RAG Step 2] Analyzing Symptoms:")
    print(f"   Symptoms: {symptoms}")
    print(f"   Additional: {additional}")
    
    if ai_assistant.is_available():
        print(f"\n⚙️  [RAG Step 3] Generating Analysis with Claude...")
        
        recommendation = ai_assistant.analyze_symptoms(
            dog, symptoms, clinic, additional
        )
        
        if recommendation:
            print(f"\n✅ ANALYSIS RESULT:")
            print(recommendation)
        else:
            print("\n⚠️  Could not complete analysis (check API key)")
    else:
        print("\n⚠️  AI Assistant not available (API key not set)")
        print("   See AI_SETUP.md for configuration instructions")


def demonstrate_appointment_notes(ai_assistant, clinic, appointment):
    """Show auto-generation of medical notes from observations"""
    
    print("\n" + "=" * 70)
    print("FEATURE 2: AUTO-GENERATE APPOINTMENT NOTES")
    print("=" * 70)
    
    print(f"\n📝 Generating Notes for: {appointment.animal.name}")
    print(f"   Appointment: {appointment.appointment_date} at {appointment.appointment_time}")
    print(f"   Veterinarian: Dr. {appointment.veterinarian.full_name}")
    print(f"   Reason: {appointment.reason}")
    
    # Clinical observations
    observations = """
    Patient alert and responsive. Palpation of rear left leg reveals pain on 
    external rotation. No swelling noted. Muscle tenderness in hip area. 
    Normal weight-bearing on other three limbs. Gait appears to favor right side.
    No fever. Mucous membranes pink and moist. 
    Assessment: Likely muscle strain or mild hip dysplasia.
    """
    
    print(f"\n🔍 Clinical Observations Entered:")
    for line in observations.strip().split('\n'):
        print(f"   {line.strip()}")
    
    if ai_assistant.is_available():
        print(f"\n⚙️  Generating professional SOAP notes...")
        
        notes = ai_assistant.generate_appointment_notes(
            appointment.animal, appointment, observations
        )
        
        if notes:
            print(f"\n✅ GENERATED NOTES:")
            print(notes)
        else:
            print("\n⚠️  Could not generate notes (check API key)")
    else:
        print("\n⚠️  AI Assistant not available (API key not set)")


def demonstrate_drug_interactions(ai_assistant, clinic, dog):
    """Show drug interaction checking with guardrails"""
    
    print("\n" + "=" * 70)
    print("FEATURE 3: DRUG INTERACTION CHECKING")
    print("=" * 70)
    
    print(f"\n💊 Checking Drug Interactions for: {dog.name}")
    print(f"   Allergies: {', '.join(dog.allergies)}")
    print(f"   Current Meds: None")
    
    # New medication to check
    new_med = "Carprofen"
    dosage = "100mg twice daily for 10 days"
    
    print(f"\n🔍 New Medication to Prescribe:")
    print(f"   Drug: {new_med}")
    print(f"   Dosage: {dosage}")
    
    if ai_assistant.is_available():
        print(f"\n⚙️  Checking for interactions and contraindications...")
        
        recommendation = ai_assistant.check_drug_interactions(
            dog, new_med, dosage
        )
        
        if recommendation:
            print(f"\n✅ INTERACTION CHECK RESULT:")
            print(recommendation)
        else:
            print("\n⚠️  Could not check interactions (check API key)")
    else:
        print("\n⚠️  AI Assistant not available (API key not set)")


def demonstrate_cost_estimation(ai_assistant, clinic, dog):
    """Show treatment cost estimation based on clinic cases"""
    
    print("\n" + "=" * 70)
    print("FEATURE 4: TREATMENT COST ESTIMATION")
    print("=" * 70)
    
    print(f"\n💰 Estimating Costs for: {dog.name}")
    print(f"   Species: {dog.species.value}")
    print(f"   Age: {dog.age_years:.1f} years")
    print(f"   Weight: {dog.weight_kg} kg")
    
    # Planned treatments
    treatments = ["Exam", "X-Ray", "Pain Management"]
    
    print(f"\n🔍 Planned Treatments:")
    for treat in treatments:
        print(f"   - {treat}")
    
    if ai_assistant.is_available():
        print(f"\n⚙️  Analyzing similar cases and estimating costs...")
        
        estimate = ai_assistant.estimate_cost(dog, treatments, clinic)
        
        if estimate:
            print(f"\n✅ COST ESTIMATION RESULT:")
            print(f"   Estimated Total: ${estimate['total']:.2f}")
            print(f"   Range: ${estimate['range'][0]:.2f} - ${estimate['range'][1]:.2f}")
            if estimate.get('notes'):
                print(f"   Notes: {estimate['notes']}")
        else:
            print("\n⚠️  Could not estimate costs (check API key)")
    else:
        print("\n⚠️  AI Assistant not available (API key not set)")


def demonstrate_followup_planning(ai_assistant, clinic, appointment, dog):
    """Show follow-up care planning after treatment"""
    
    print("\n" + "=" * 70)
    print("FEATURE 5: FOLLOW-UP CARE PLANNING")
    print("=" * 70)
    
    print(f"\n📅 Planning Follow-up for: {dog.name}")
    print(f"   Previous Treatment: Rest with NSAIDs")
    
    # Create a treatment for the example
    from vet_office_system import Treatment, TreatmentType
    
    treatment = Treatment(
        "Pain Management with Rest",
        TreatmentType.MEDICATION,
        "Carprofen 100mg twice daily, strict rest recommended"
    )
    treatment.cost = 50.0
    
    print(f"\n🔍 Treatment Details:")
    print(f"   Name: {treatment.name}")
    print(f"   Type: {treatment.treatment_type.value}")
    print(f"   Description: {treatment.description}")
    
    if ai_assistant.is_available():
        print(f"\n⚙️  Generating follow-up recommendations...")
        
        recommendation = ai_assistant.recommend_followup(
            dog, treatment, clinic
        )
        
        if recommendation:
            print(f"\n✅ FOLLOW-UP PLAN:")
            print(recommendation)
        else:
            print("\n⚠️  Could not generate plan (check API key)")
    else:
        print("\n⚠️  AI Assistant not available (API key not set)")


def show_rag_explanation():
    """Explain how RAG works in this system"""
    
    print("\n" + "=" * 70)
    print("UNDERSTANDING RAG (Retrieval-Augmented Generation)")
    print("=" * 70)
    
    print("""
How the AI Clinical Assistant Works:

1️⃣  RETRIEVE
    ├─ Pull patient's medical history
    ├─ Get current medications
    ├─ Check allergies
    ├─ Find similar past cases
    └─ Compile all relevant context

2️⃣  AUGMENT
    ├─ Add current symptoms/observations
    ├─ Include veterinarian notes
    ├─ Add diagnostic findings
    └─ Prepare complete prompt for AI

3️⃣  GENERATE
    ├─ Send augmented prompt to Claude
    ├─ Claude analyzes with full context
    ├─ Returns evidence-based recommendation
    └─ Include confidence scores

Result: AI recommendations grounded in SPECIFIC patient data,
        not just generic knowledge

Example RAG Flow for Symptom Analysis:
────────────────────────────────────
Patient: Buddy (Labrador) with lameness

RETRIEVE:
- 6-year-old Labrador
- Allergic to Chicken
- No previous orthopedic issues
- Similar cases: 3 Labs with limping (diagnosed: muscle strain)

AUGMENT:
- Current symptom: Limping on back left leg for 2 days
- No trauma observed
- Playing when incident occurred

GENERATE (Claude analyzes with above context):
→ Primary diagnosis: Muscle strain (HIGH confidence)
  [Reason: Typical presentation for this breed/age, history of 
   similar cases, no trauma needed]

→ Differentials: Hip dysplasia, ligament injury
→ Tests: X-ray, orthopedic exam
→ Warnings: ⚠️  Chicken allergy noted

This personalized analysis is RAG in action!
""")


def check_ai_status(ai_assistant):
    """Display AI system status"""
    
    print("\n" + "=" * 70)
    print("AI SYSTEM STATUS")
    print("=" * 70)
    
    status = ai_assistant.get_ai_status()
    
    print(f"\n🔧 Status Information:")
    print(f"   AI Available: {'✅ YES' if status['available'] else '❌ NO'}")
    print(f"   Model: {status['model']}")
    print(f"   Cache Size: {status['cache_size']} cached histories")
    
    if not status['available']:
        print(f"\n⚠️  To enable AI features:")
        print(f"   1. Get API key: https://console.anthropic.com")
        print(f"   2. Set environment: export ANTHROPIC_API_KEY='sk-ant-...'")
        print(f"   3. Run: streamlit run vet_app.py")
        print(f"\n   See AI_SETUP.md for detailed instructions")


def main():
    """Run all AI demonstrations"""
    
    # Initialize AI Assistant (with or without API key - will show warnings if not configured)
    print("\n📍 Initializing AI Clinical Assistant...")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    ai_assistant = VetAIAssistant(api_key=api_key)
    
    # Create test data
    clinic, dog, cat, appointment = setup_test_clinic()
    
    # Show RAG explanation
    show_rag_explanation()
    
    # Check status
    check_ai_status(ai_assistant)
    
    if ai_assistant.is_available():
        print("\n✅ API key detected! Running AI demonstrations...\n")
        
        # Run demonstrations
        demonstrate_symptom_analysis(ai_assistant, clinic, dog)
        demonstrate_appointment_notes(ai_assistant, clinic, appointment)
        demonstrate_drug_interactions(ai_assistant, clinic, dog)
        demonstrate_cost_estimation(ai_assistant, clinic, dog)
        demonstrate_followup_planning(ai_assistant, clinic, appointment, dog)
        
        print("\n" + "=" * 70)
        print("✅ AI DEMONSTRATIONS COMPLETE!")
        print("=" * 70)
        print("""
All AI features demonstrated:
  ✅ Symptom Analysis with RAG
  ✅ Appointment Notes Generation
  ✅ Drug Interaction Checking
  ✅ Cost Estimation
  ✅ Follow-up Planning

Next Steps:
  1. Try the Streamlit UI: streamlit run vet_app.py
  2. Go to 🤖 AI Assistant tab
  3. Test each feature with your own data
  4. Check logs for AI operations

For more information:
  - VET_AI_GUIDE.md - Comprehensive AI documentation
  - AI_SETUP.md - Setup and troubleshooting
  - vet_ai_assistant.py - Source code with comments
""")
    else:
        print("\n⚠️  API key not configured")
        print("\nTo run AI demonstrations:")
        print("  1. Get free API key: https://console.anthropic.com")
        print("  2. Set environment: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("  3. Run this script again")
        print("\nSee AI_SETUP.md for detailed instructions")
        
        print("\n📚 Can still browse:")
        print("  - RAG explanation (shown above)")
        print("  - Feature descriptions")
        print("  - API structure without actual API calls")


if __name__ == "__main__":
    main()
