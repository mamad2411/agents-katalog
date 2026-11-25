---
name: research-proposal
type: instruction
description: Defines the structure and requirements for a research proposal.
---

# Research Proposal

A research proposal is a structured 2-page document. Every section must be present. Be concrete — vague claims are not acceptable.

---

## Sections

### 1. Problem Statement and Task Definition
What does the system do? What is its input and output? What real-world problem does it solve? Scope must be neither too narrow nor too broad.

### 2. Input / Output Behavior
Concrete examples of inputs and outputs. Describe what the input and output variables look like and how they interact. Reference the actual data being used — do not describe hypothetical data.

### 3. Evaluation Metric
How will success be measured? Why is this metric the right one for this problem? A reasonably sized dataset of example input-output pairs must be identified — either from an existing source or collected from scratch.

### 4. Related Works
What existing research and projects are relevant? How does the proposed work differ? Reference specific papers and systems, not general fields.

### 5. Baseline and Oracle
- **Baseline**: a simple, easy-to-implement approach that gives a lower bound on expected performance
- **Oracle**: an upper bound — what would near-perfect performance look like?
- Neither needs to be implemented for the proposal, but both must be clearly described. If the gap between baseline and oracle is too small, the task is probably not well-chosen.

### 6. Methodology and Challenges
How will the problem be approached? Why does this method fit? What are the key challenges? What algorithms or models are appropriate, and what are the tradeoffs between accuracy and efficiency?

---

## Requirements

- 2 pages maximum
- Every section must be present — do not skip or merge sections
- Concrete over vague in every section
- Related works must cite specific papers, not just name fields
