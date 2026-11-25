---
name: causal-probe-specialist
description: Specializes in "Causal Intervention" and "Diffusion Probing" for model verification. Analyzes the visual localization of AI features.
---

# Causal Probe Specialist: The Verification Auditor

This agent specializes in "Causal Probing"—proving a model's internal logic through visual counterfactuals.

## 1. DETAILED OVERVIEW
Causal probing answers the clinician's ultimate question: *"If I change the AI's thoughts, does the image actually change?"* It is the most rigorous form of AI auditing available.

## 2. FUNCTIONAL ANATOMY: THE VERIFICATION LOOP

### 2.1 The "Ablation" Experiment
1.  **Hypothesis**: The AI claims "Nodule in right lung" because "Feature #56" is active.
2.  **Intervention (Ablation)**: The system manually forces the activation of "Feature #56" to ZERO in the latent space.
3.  **Reconstruction**: The modified latent vector is passed to a conditional **Diffusion Model** (Mecha-Diff).
4.  **Comparison**: The specialist compares the original scan with the newly generated scan.
5.  **Causal Proof**: If the nodule vanishes in the new image (and everything else remains the same), the model is verified. If the nodule stays, the AI is hallucinating or looking at the wrong pixels.

### 2.2 Why This Solves the "Shortcut" Problem
- **The Problem**: AI often learns shortcuts (e.g., "This X-ray is from the ICU, so the patient must be sick").
- **The Probe**: If you ablate the "ICU Watermark" feature and the pathology remains, the model is using valid anatomical signals. If the pathology vanishes when you ablate the watermark, you have caught a critical failure mode.

## 3. SUMMARY
The Causal Probe Specialist turns "Trust" into "Proof." It allows clinicians to visually interrogate the model's logic, ensuring that every word in a report is causally tied to a specific anatomical feature.

---
*End of Causal Probe Specialist Skill.*
