"""
Veterinary AI Clinical Assistant
Uses Claude AI with Retrieval-Augmented Generation (RAG) to provide clinical decision support
including symptom analysis, treatment recommendations, drug interaction checking, and note generation.
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import date, datetime
from dataclasses import dataclass
from enum import Enum
import json

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

from vet_office_system import Animal, VetOffice, Appointment, Treatment, Medication

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfidenceLevel(Enum):
    """Confidence levels for AI recommendations"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AIRecommendation:
    """Structure for AI recommendations"""
    title: str
    description: str
    rationale: str
    confidence: ConfidenceLevel
    warnings: List[str]
    references: List[str]  # Previous case references
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __str__(self) -> str:
        warnings_text = ""
        if self.warnings:
            warnings_text = f"\n⚠️  **Warnings**: {'; '.join(self.warnings)}"
        
        return (f"**{self.title}** (Confidence: {self.confidence.value.upper()})\n"
                f"{self.description}\n\n"
                f"**Rationale**: {self.rationale}{warnings_text}")


class VetAIAssistant:
    """
    AI-powered clinical assistant for veterinary practices.
    Uses Claude with RAG to provide clinical decision support.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI assistant.
        
        Args:
            api_key: Anthropic API key. If None, will read from ANTHROPIC_API_KEY environment variable.
        """
        self.api_key = api_key
        self.client = None
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
        self.rag_cache = {}  # Cache for retrieved medical histories
        
        if Anthropic:
            try:
                self.client = Anthropic(api_key=api_key)
                logger.info("✅ AI Assistant initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Claude client: {e}")
                self.client = None
        else:
            logger.warning("⚠️  Anthropic library not installed. AI features disabled.")

    def is_available(self) -> bool:
        """Check if AI assistant is properly initialized"""
        return self.client is not None

    def _retrieve_medical_history(self, animal: Animal) -> str:
        """
        RAG: Retrieve relevant medical history for an animal.
        
        This is the Retrieval-Augmented Generation component - it retrieves
        the animal's medical history before making recommendations.
        """
        if not animal:
            return ""

        # Check cache first
        cache_key = f"{animal.name}_{animal.owner.full_name if animal.owner else 'unknown'}"
        if cache_key in self.rag_cache:
            logger.debug(f"Using cached medical history for {cache_key}")
            return self.rag_cache[cache_key]

        history = []
        
        # Animal basic info
        history.append(f"**Patient**: {animal.name} ({animal.species.value}, {animal.breed})")
        history.append(f"**Age**: {animal.age_years:.1f} years")
        history.append(f"**Weight**: {animal.weight_kg} kg")
        
        if animal.allergies:
            history.append(f"**⚠️  ALLERGIES**: {', '.join(animal.allergies)}")
        
        # Current medications
        active_meds = animal.get_active_medications()
        if active_meds:
            history.append("\n**Current Medications**:")
            for med in active_meds:
                history.append(f"- {med.name} {med.dosage} ({med.frequency})")
        
        # Medical records
        if animal.medical_records:
            history.append("\n**Medical History**:")
            for record in animal.medical_records[-10:]:  # Last 10 records
                history.append(f"- {record.date_recorded}: {record.record_type}: {record.details}")
        
        # Recent appointments
        recent_apts = [apt for apt in animal.appointments if apt.status.value == "completed"]
        if recent_apts:
            history.append("\n**Recent Appointments**:")
            for apt in recent_apts[-5:]:  # Last 5
                history.append(f"- {apt.appointment_date}: {apt.reason} with Dr. {apt.veterinarian.full_name}")
                if apt.treatments:
                    for treat in apt.treatments:
                        history.append(f"  * {treat.name}")
        
        medical_history = "\n".join(history)
        self.rag_cache[cache_key] = medical_history
        logger.info(f"Retrieved medical history for {animal.name}")
        
        return medical_history

    def _find_similar_cases(self, vet_office: VetOffice, animal: Animal, 
                           condition: str) -> List[str]:
        """
        Find similar past cases from the clinic's database for comparison.
        Part of RAG - provides contextual examples.
        """
        similar = []
        
        # Find animals of same or similar species with similar treatments
        for other_animal in vet_office.animals:
            if other_animal.species == animal.species and other_animal != animal:
                for apt in other_animal.appointments:
                    for treat in apt.treatments:
                        # Simple keyword matching for condition similarity
                        if condition.lower() in treat.name.lower() or \
                           condition.lower() in (apt.reason or "").lower():
                            similar.append(f"{other_animal.name} ({other_animal.species.value})")
                            break
            if len(similar) >= 3:  # Limit to 3 similar cases
                break
        
        return similar

    def analyze_symptoms(self, animal: Animal, symptoms: str, 
                        vet_office: VetOffice, additional_notes: str = "") -> Optional[AIRecommendation]:
        """
        Analyze symptoms using RAG to retrieve medical history and suggest possible conditions.
        
        This is an agentic workflow that:
        1. Retrieves animal's medical history (RAG)
        2. Finds similar past cases
        3. Uses Claude to analyze symptoms in context
        4. Returns recommendations with confidence levels
        """
        if not self.is_available():
            logger.warning("AI Assistant not available")
            return None

        logger.info(f"Analyzing symptoms for {animal.name}: {symptoms}")

        # Step 1: Retrieve medical history (RAG)
        medical_history = self._retrieve_medical_history(animal)
        
        # Step 2: Find similar cases
        similar_cases = self._find_similar_cases(vet_office, animal, symptoms)
        
        # Step 3: Prepare context and query Claude
        context = f"""{medical_history}

New Presentation:
Symptoms: {symptoms}
Additional Notes: {additional_notes or "None"}

Similar Past Cases: {', '.join(similar_cases) if similar_cases else "None found"}
"""

        prompt = f"""You are a veterinary clinical decision support assistant. Analyze the following presentation:

{context}

Provide potential differential diagnoses with confidence levels. Format your response as JSON with this structure:
{{
    "primary_diagnosis": "Most likely condition",
    "confidence": "high/medium/low",
    "differential_diagnoses": ["condition1", "condition2"],
    "rationale": "Explanation based on the patient's history and presentation",
    "recommended_tests": ["test1", "test2"],
    "warnings": ["any red flags or concerns"]
}}

Focus on conditions relevant to a {animal.species.value} with this symptom presentation."""

        try:
            response = self._call_claude(prompt, system="You are an expert veterinary clinical decision support system. Provide evidence-based recommendations while emphasizing that AI suggestions should complement, not replace, professional veterinary judgment.")
            
            # Parse JSON response
            import json
            response_data = json.loads(response)
            
            diagnosis = response_data.get("primary_diagnosis", "Unknown")
            confidence = response_data.get("confidence", "medium").lower()
            rationale = response_data.get("rationale", "")
            warnings = response_data.get("warnings", [])
            
            # Add allergy warning if relevant
            if animal.allergies:
                warnings.insert(0, f"Patient has allergies to: {', '.join(animal.allergies)}")
            
            confidence_level = ConfidenceLevel[confidence.upper()] if confidence.upper() in ConfidenceLevel.__members__ else ConfidenceLevel.MEDIUM
            
            logger.info(f"Symptom analysis complete: {diagnosis} ({confidence_level.value})")
            
            return AIRecommendation(
                title=f"Suspected Condition: {diagnosis}",
                description=f"Recommended Tests: {', '.join(response_data.get('recommended_tests', []))}",
                rationale=rationale,
                confidence=confidence_level,
                warnings=warnings,
                references=similar_cases
            )
            
        except Exception as e:
            logger.error(f"Error analyzing symptoms: {e}")
            return None

    def generate_appointment_notes(self, animal: Animal, appointment: Appointment,
                                  observations: str) -> Optional[str]:
        """
        Generate professional appointment notes from observations.
        Uses the animal's history for context.
        """
        if not self.is_available():
            logger.warning("AI Assistant not available")
            return None

        logger.info(f"Generating appointment notes for {animal.name}")

        medical_history = self._retrieve_medical_history(animal)
        
        prompt = f"""Based on the following patient information and observations, generate professional veterinary appointment notes:

{medical_history}

Appointment Details:
- Reason: {appointment.reason}
- Date: {appointment.appointment_date}
- Clinician: Dr. {appointment.veterinarian.full_name}
- Observations: {observations}

Generate a professional SOAP note (Subjective, Objective, Assessment, Plan) format. Keep it concise but thorough."""

        try:
            notes = self._call_claude(prompt, system="You are an expert veterinary medical scribe. Generate clear, professional SOAP notes suitable for medical records.")
            logger.info("Appointment notes generated successfully")
            return notes
        except Exception as e:
            logger.error(f"Error generating notes: {e}")
            return None

    def check_drug_interactions(self, animal: Animal, new_medication: str,
                              dosage: str) -> Optional[AIRecommendation]:
        """
        Check for potential drug interactions with current medications.
        Uses RAG to retrieve current medication list.
        """
        if not self.is_available():
            logger.warning("AI Assistant not available")
            return None

        logger.info(f"Checking drug interactions for {animal.name}: {new_medication}")

        # Get current medications
        active_meds = animal.get_active_medications()
        current_meds_list = [f"{med.name} ({med.dosage})" for med in active_meds]
        
        prompt = f"""Check for drug interactions in a veterinary patient:

Patient: {animal.name} ({animal.species.value})
Current Medications: {', '.join(current_meds_list) if current_meds_list else "None"}
New Medication: {new_medication} {dosage}
Allergies: {', '.join(animal.allergies) if animal.allergies else "None"}

Provide a JSON response with this structure:
{{
    "safe_to_administer": true/false,
    "interaction_risk": "none/low/moderate/high",
    "interactions": ["list of potential interactions"],
    "warnings": ["any important warnings"],
    "contraindications": ["any conditions that contraindicate use"],
    "monitoring_required": ["what to monitor"]
}}
"""

        try:
            response = self._call_claude(prompt, system="You are an expert veterinary pharmacist. Provide accurate drug interaction information.")
            
            import json
            response_data = json.loads(response)
            
            safe = response_data.get("safe_to_administer", False)
            risk = response_data.get("interaction_risk", "unknown")
            interactions = response_data.get("interactions", [])
            warnings = response_data.get("warnings", [])
            monitoring = response_data.get("monitoring_required", [])
            
            if monitoring:
                warnings.extend([f"Monitor for: {item}" for item in monitoring])
            
            title = f"Drug Interaction Check: {new_medication}"
            description = f"Risk Level: {risk.upper()}"
            rationale = f"Safe to administer: {'Yes' if safe else 'No'}. Interactions: {'; '.join(interactions) if interactions else 'None identified'}"
            
            confidence = ConfidenceLevel.HIGH if risk == "none" else ConfidenceLevel.MEDIUM
            
            logger.info(f"Drug interaction check complete: {risk} risk")
            
            return AIRecommendation(
                title=title,
                description=description,
                rationale=rationale,
                confidence=confidence,
                warnings=warnings,
                references=current_meds_list
            )
            
        except Exception as e:
            logger.error(f"Error checking drug interactions: {e}")
            return None

    def recommend_followup(self, animal: Animal, treatment: Treatment,
                          vet_office: VetOffice) -> Optional[AIRecommendation]:
        """
        Recommend follow-up care based on treatment provided and animal history.
        Uses agentic workflow to plan next steps.
        """
        if not self.is_available():
            logger.warning("AI Assistant not available")
            return None

        logger.info(f"Recommending follow-up for {animal.name}: {treatment.name}")

        medical_history = self._retrieve_medical_history(animal)
        
        prompt = f"""Based on the patient's history and the treatment provided, recommend appropriate follow-up care:

{medical_history}

Treatment Delivered: {treatment.name}
Type: {treatment.treatment_type.value}
Description: {treatment.description}

Provide recommendations in JSON format:
{{
    "followup_needed": true/false,
    "timeframe": "days/weeks/months until next appointment",
    "followup_type": "type of examination or test",
    "monitoring_schedule": "how often to monitor",
    "warning_signs": ["signs that require immediate attention"],
    "recommended_tests": ["tests to perform at follow-up"],
    "home_care": ["care instructions for owner"]
}}
"""

        try:
            response = self._call_claude(prompt, system="You are an expert veterinary clinician providing evidence-based follow-up recommendations.")
            
            import json
            response_data = json.loads(response)
            
            followup_needed = response_data.get("followup_needed", False)
            timeframe = response_data.get("timeframe", "As recommended")
            followup_type = response_data.get("followup_type", "")
            warnings = response_data.get("warning_signs", [])
            home_care = response_data.get("home_care", [])
            tests = response_data.get("recommended_tests", [])
            
            if not followup_needed:
                title = "No follow-up monitoring required"
                description = "Patient appears stable"
            else:
                title = f"Follow-up Recommended: {followup_type}"
                description = f"Timeframe: {timeframe}"
            
            rationale = f"Home Care: {'; '.join(home_care) if home_care else 'Standard care'}"
            
            logger.info(f"Follow-up recommendation complete: {followup_needed}")
            
            return AIRecommendation(
                title=title,
                description=description,
                rationale=rationale,
                confidence=ConfidenceLevel.HIGH,
                warnings=warnings + [f"Monitor for: {test}" for test in tests],
                references=[]
            )
            
        except Exception as e:
            logger.error(f"Error recommending follow-up: {e}")
            return None

    def estimate_cost(self, animal: Animal, treatments: List[str],
                     vet_office: VetOffice) -> Optional[Dict[str, Any]]:
        """
        Estimate treatment costs based on similar cases in clinic database.
        Uses RAG to find comparable treatments.
        """
        if not self.is_available():
            logger.warning("AI Assistant not available")
            return None

        logger.info(f"Estimating cost for {animal.name}: {treatments}")

        # Find similar treatments from past appointments
        past_costs = {}
        for apt in vet_office.appointments:
            for treat in apt.treatments:
                treat_key = treat.name.lower().strip()
                if treat.cost > 0:
                    if treat_key not in past_costs:
                        past_costs[treat_key] = []
                    past_costs[treat_key].append(treat.cost)

        # Calculate average costs
        avg_costs = {k: sum(v) / len(v) for k, v in past_costs.items()}
        
        prompt = f"""Based on the following treatment costs from similar cases in the clinic, estimate the total cost:

Clinic Cost History (Averages):
{json.dumps(avg_costs, indent=2)}

Treatments Planned: {', '.join(treatments)}
Patient: {animal.name} ({animal.species.value})

Provide a JSON estimate:
{{
    "treatment_breakdown": {{"treatment_name": estimated_cost}},
    "total_estimated_cost": number,
    "cost_range_low": number,
    "cost_range_high": number,
    "notes": "any factors affecting cost"
}}
"""

        try:
            response = self._call_claude(prompt, system="You are a veterinary billing specialist. Provide accurate cost estimates.")
            
            import json
            estimate = json.loads(response)
            
            logger.info(f"Cost estimation complete: ${estimate.get('total_estimated_cost', 0):.2f}")
            
            return {
                "breakdown": estimate.get("treatment_breakdown", {}),
                "total": estimate.get("total_estimated_cost", 0),
                "range": (estimate.get("cost_range_low", 0), estimate.get("cost_range_high", 0)),
                "notes": estimate.get("notes", "")
            }
            
        except Exception as e:
            logger.error(f"Error estimating cost: {e}")
            return None

    def _call_claude(self, user_message: str, system: str = "") -> str:
        """
        Make a call to Claude API.
        Includes error handling and logging.
        """
        if not self.client:
            raise RuntimeError("Claude client not initialized")

        try:
            logger.debug(f"Calling Claude: {user_message[:100]}...")
            
            messages = [{"role": "user", "content": user_message}]
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system if system else "You are an expert veterinary clinical decision support system.",
                messages=messages
            )
            
            result = response.content[0].text
            logger.debug(f"Claude response received: {result[:100]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    def get_ai_status(self) -> Dict[str, Any]:
        """Get status information about the AI assistant"""
        return {
            "available": self.is_available(),
            "model": self.model,
            "conversation_history_length": len(self.conversation_history),
            "cache_size": len(self.rag_cache),
            "last_used": None  # Can be updated with timestamps
        }
