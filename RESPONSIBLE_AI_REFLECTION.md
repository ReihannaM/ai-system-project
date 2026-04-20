# Responsible AI Reflection

## Limitations & Biases

**RAG only knows what's in your database.** If you've never treated a condition, the AI can't help. If your clinic mostly treats dogs, cat recommendations may be weak. This is honest—we flag it with LOW confidence when data is sparse.

**Confidence scoring measures data richness, not accuracy.** Three similar cases means HIGH confidence... but what if all three were misdiagnosed? The system can't verify correctness without real outcomes. We mitigate this by requiring vet review and logging patterns over time.

**Allergies & drug interactions are only what's documented.** Unknown allergies stay unknown. New interactions discovered after your database was created won't be in the system. The vet must still review before administering anything.

**No cost or quality-of-life reasoning.** The system recommends based on medical efficacy, not whether that $10K surgery makes sense for a 16-year-old pet. The vet and owner must discuss this—AI is one input, not the decision.

**Data biases.** If your clinic's patients skew toward wealthy owners (more visits = more data), recommendations bias toward their patterns. If you're in a cold climate, disease prevalence reflects that. These aren't flaws we can "fix"—just reality about what the data represents.

**Only learns from documented cases.** Failures that went to other clinics or were euthanized aren't in the database. Success rates might be inflated because we only see the cases that stayed and succeeded.

---

## How This Could Be Misused & How We Prevent It

**Risk: AI replaces vet examination.** A staff member tells the owner "our AI says arthritis" and skips the physical exam. *Prevention:* Vet must review and approve all recommendations. Logging tracks sign-off. UI clearly shows "AI ASSISTED - Reviewed by Dr. Smith."

**Risk: Profit-driven clinic manipulates drug database.** Prices competitor's drugs as "unsafe" and recommends expensive alternatives. *Prevention:* System is auditable (can see what was changed and by whom). Multiple drug options usually exist. Vet can override.

**Risk: Reduced care standards.** Clinic uses AI to speed up consultations instead of improving them. 5-minute appointment: "AI said arthritis." *Prevention:* Vet review requirement can't be skipped. Logging creates accountability.

**Risk: Liability shifting.** Bad outcome → clinic blames AI to avoid responsibility. *Prevention:* Clear policy: "Veterinarian makes final decision." Vet's name logged on approval. Written agreement that clinic is responsible.

**Safeguards we built in:**
- Only vets can approve recommendations (staff cannot bypass)
- Logging shows who approved what and when
- Confidence scores flag uncertainty (requiring more investigation)
- Clear disclaimer: "AI is tool, vet is decision-maker"

**Safeguards you should add:**
- Regular audits (monthly reviews of AI recommendations + outcomes)
- Outcome tracking (did recommendation lead to good result?)
- Staff training (this is decision support, not a shortcut)

---

## What Surprised Me During Testing

**Surprise #1: Confidence ≠ Accuracy.** More similar cases means more confidence—but what if all three cases were misdiagnosed? The system can confidently amplify errors. I realized confidence measures *data richness*, not *correctness*. This is why vet review is critical.

**Surprise #2: Error handling was obvious.** When data was incomplete, the system gracefully lowered confidence instead of pretending to know. I expected complex workarounds—turned out simplicity (admit uncertainty) was smarter.

**Surprise #3: Data validation matters more than algorithms.** Spent more time thinking about "what if data is weird" than "how to make better recommendations." Garbage in = garbage out, even with sophisticated AI. A clean database matters more than clever code.

**Surprise #4: Tests can verify code works, not that it's useful.** Automated tests pass but miss real-world edge cases. A test catches "allergy detection works" but not "cross-reactivity between drugs." Real scenarios are messier than test cases.

**Surprise #5: Confidence is psychological.** HIGH confidence makes people trust more (even if not appropriate). LOW confidence makes people doubt (even if reasoning was sound). The confidence number anchors how people think, not just what they know.

---

## AI Helping Me Build AI: Helpful & Harmful Suggestions

**Helpful: RAG Architecture Suggestion**

When I asked how to ground AI recommendations in patient data, Claude suggested Retrieval-Augmented Generation: retrieve patient history + similar cases, then prompt the model with that context. Instead of fine-tuning (expensive) or sending entire databases (slow), RAG elegantly solved the grounding problem. This became the core architecture—it honestly works because the patient context prevents generic recommendations.

**Harmful: "Use Claude's Self-Reported Confidence"**

Early on, Claude suggested asking it for confidence ratings on a 1-10 scale. Sounded reasonable—but this was wrong. Claude is trained to sound confident even when uncertain. "89% confident" implies mathematical rigor it doesn't have. Plus, Claude can't know what it doesn't know (the foundational AI limitation).

I replaced it with data-driven confidence: HIGH if 3+ similar cases exist, MEDIUM if 1-2, LOW if 0. This is transparent about what enables the recommendation, not falsely precise about accuracy.

**The insight:** AI is great at recognizing patterns (RAG is brilliant). AI is bad at assessing itself (confidence ratings are rhetoric, not ground truth). I had to verify claims through testing rather than trusting explanations.

**Best approach:** Use AI for high-level architecture guidance, but empirically verify the details.

---

## Summary: How We Built This Responsibly

**Transparency:** System shows confidence levels. Logging explains how recommendations were generated. This document details what can't be done.

**Safety:** Vet review required (can't auto-execute). Allergy checking before drug recommendation. Clear liability: vet makes final decision.

**Honest about limits:** Only works with documented cases. Biased toward your clinic's patterns. Confidence means "data richness," not "accuracy."

**Continuous improvement:** Logging enables learning from outcomes. Staff feedback guides refinement. Willing to admit when wrong.

**Human-centered:** Augments vet judgment, doesn't replace it. Frees up time for more thoughtful care. Vet maintains responsibility.

---

## Final Thought

**What I learned building this:**

1. Limitations are features, not bugs. A system that admits uncertainty is more trustworthy than one claiming false precision.

2. AI reliability comes from data quality + honest confidence + human oversight. Not from clever algorithms alone.

3. Building AI systems WITH AI taught me to verify claims empirically rather than trust explanations.

4. The best safeguard for responsible AI is remaining skeptical—about the AI, about your data, about your assumptions.

5. This system's honesty about what it can't do is its greatest strength.
