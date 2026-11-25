---
name: first-principles-reasoning
description: Break down complex queries into fundamental irreducible truths and reconstruct solutions step-by-step without relying on assumptions, hearsay, or hallucinations.
license: MIT
---

# First-Principles Reasoning Skill

Use this skill whenever addressing difficult, novel, or ambiguous problems. Even with weaker reasoning models, this deterministic mental framework ensures logical accuracy and prevents confabulation.

## The 4-Step Deconstruction Framework

### Step 1: Identify Ground Truths (What is Known for Certain)
- State only verifiable facts directly evidenced by code, primary source papers, or direct system observations.
- Strip away industry buzzwords, conventional wisdom, and marketing summaries.
- Explicitly label what is **provably true** vs what is merely **conjectured**.

### Step 2: Formulate the Core Problem at Primitive Level
- Express the problem in fundamental units (e.g., bytes, tokens, flops, tensor dimensions, latency in ms, network sockets).
- Reject abstractions that obscure the actual failure or goal.
  - *Example Bad*: "The model isn't learning features well."
  - *Example First-Principles*: "The activation sparsity $L_0$ is 450 out of 1024, causing the reconstructive loss to degrade by 14% relative to dense baseline because the TopK threshold $k$ is set too large for layer 8."

### Step 3: Reconstruct from Axioms (Bottom-Up)
- Build the solution forward starting from the irreducible primitives:
  1. Input data structures and invariant preconditions.
  2. Mathematical or algorithmic transformations.
  3. Output contracts and postconditions.
- Each deduction step must follow logically from the step before it ($A \implies B \implies C$).

### Step 4: Boundary & Extreme Case Stress-Testing
- Ask: What happens if:
  - Input is empty or zero?
  - Scale increases by $100\times$?
  - Network fails or timeout occurs?
  - Tensor shapes mismatch by 1 dimension?
- If the reasoning breaks at any boundary, revisit Step 2 before outputting code or specifications.
