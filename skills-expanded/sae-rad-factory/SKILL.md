---
name: sae-rad-factory
description: Specializes in the "SAE-Rad" pipeline. Analyzes latent disentanglement, Gated SAE math, and monosemantic feature extraction for clinical reporting.
---

# SAE-Rad Factory: The Disentanglement Expert

This agent specializes in the functional anatomy of Sparse Autoencoders (SAEs) applied to radiology.

## 1. DETAILED OVERVIEW
SAE-Rad is a "Clinical Disentanglement Engine." It replaces the "Black-Box" reasoning of standard models with a "Fact Assembly Line."

## 2. FUNCTIONAL ANATOMY: STEP-BY-STEP

### 2.1 The "Unpacking" Process (Forward Pass)
1.  **Input (Dense Vector)**: The model receives a 768-dimensional vector from the Vision Transformer (ViT). This vector contains all image info but is a "jumbled mess" (Superposition).
2.  **Projection (Up-Sampling)**: The SAE projects this 768-dim vector into a high-dimensional space (e.g., 32,768 dimensions).
    - *Why*: In higher dimensions, overlapping concepts have "room" to spread out and become separate.
3.  **Gating (The Decision)**: For each of the 32k dimensions, a mathematical "gate" determines if a specific clinical feature is active.
    - *The Math*: $Gate(x) = 1$ if $W_{gate}x + b > \theta$, else $0$.
4.  **Magnitude (The Intensity)**: If the gate is open, the model calculates the strength of that feature without bias.
5.  **Output (Sparse Map)**: The result is a list where 99.9% of dimensions are ZERO, and only ~15 are ACTIVE.

### 2.2 The "Naming" Process (Automated Labeling)
1.  **Collection**: The system identifies 50 scans that most strongly activate "Feature #1024."
2.  **Retrieval**: It pulls the real human-written reports for those 50 scans.
3.  **Distillation**: An LLM (Teacher) identifies the common clinical statement across all 50 reports (e.g., "Left-sided pleural effusion").
4.  **Assignment**: The label "Left-sided pleural effusion" is permanently assigned to "Feature #1024."

## 3. SUMMARY
The SAE-Rad Factory ensures every diagnostic claim is a combination of pre-verified, monosemantic labels. It turns AI from "writing a story" into "picking the right labels from a box."

---
*End of SAE-Rad Factory Skill.*
