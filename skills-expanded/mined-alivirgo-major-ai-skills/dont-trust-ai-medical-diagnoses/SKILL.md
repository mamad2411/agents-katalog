---
name: dont-trust-ai-medical-diagnoses
description: "Use AI for medical vocabulary and appointment preparation while directing diagnosis and treatment questions to qualified clinicians."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["medical-literacy", "health-safety", "lab-results", "doctor-prep", "safety-guidelines", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Don't Trust AI Medical Diagnoses (Health Literacy Framework) (AI Skill)

## Overview
Searching symptoms or pasting medical reports into an AI assistant often triggers extreme responses: either catastrophic worst-case diagnoses (e.g. rare autoimmune conditions or oncology) or false reassurance that causes patients to delay critical in-person care.

The **Health Literacy & Doctor-Prep Protocol** establishes strict boundaries: never use AI to diagnose illnesses or prescribe dosages, but leverage its strength to **translate complex clinical jargon, explain anatomical mechanisms, and generate organized questions for your physician**.

---

## The Medical AI Safety Boundary

```
┌─────────────────────────────────────────────────────────────┐
│                 Safe vs. Dangerous Medical AI               │
│                                                             │
│  ❌ DANGEROUS USE CASES (Do Not Outsource to AI):           │
│  • Diagnosing chest pain, acute abdominal pain, or rashes   │
│  • Adjusting prescription medication dosages                │
│  • Deciding whether to skip emergency medical care          │
│                                                             │
│  ✅ SAFE, HIGH-LEVERAGE USE CASES (Literacy & Prep):        │
│  • Translating lab report acronyms (e.g. eGFR, ALT, MCV)    │
│  • Understanding standard anatomical terminology            │
│  • Generating a prioritized list of questions for your doctor│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Health Literacy Prompt Templates

### Pattern 1: The Lab Report Jargon Translator
Use to demystify complex lab results before your doctor appointment:

```markdown
Here is a line from my lab report:
"[PASTE SPECIFIC LAB TEST NAME & REFERENCE RANGE]"

Task:
1. Explain what [TEST NAME] measures in plain English using a simple biological analogy.
2. What is the standard purpose of this test in routine checkups?
3. Generate 2 clear, informed questions I can ask my physician during my follow-up appointment.

Do NOT attempt to diagnose my health or tell me if I have a disease.
```

---

### Pattern 2: The Doctor Appointment Preparation Guide
Use when preparing for an upcoming consultation with a specialist:

```markdown
I have an appointment with a [SPECIALIST TYPE: e.g. Gastroenterologist / Cardiologist] regarding [GENERAL SYMPTOM / TOPIC].

Help me organize my thoughts before the visit:
1. What specific timeline and symptom details should I write down to help the doctor?
2. What are 4 high-value questions I should ask about treatment options, lifestyle modifications, and next diagnostic steps?
```

---

## Real-World Case Study

### Scenario: Interpreting a Routine Blood Work Panel

#### Unsafe Prompting (Anxiety & Misinformation)
> **User**: *"My ferritin is 450 ng/mL and my AST is 52 U/L. What disease do I have?"*
>
> ❌ *Risky AI Output: "You may have hereditary hemochromatosis, non-alcoholic steatohepatitis (NASH), or hepatocellular carcinoma..." (Triggers severe health anxiety).*

#### Safe Health Literacy Output
> **Prompt**: *"Explain the biological function of Ferritin and AST in plain English, and what questions I should ask my doctor."*

**AI Response**:
> - **Ferritin**: Acts like the body's iron storage warehouse. High levels can indicate increased iron stores, but ferritin is also an "acute-phase reactant" - meaning it temporarily rises in response to everyday inflammation, infection, or exercise.
> - **AST (Aspartate Aminotransferase)**: An enzyme found primarily in liver and muscle cells. When cells are stressed, AST can leak into the bloodstream.
>
> **Questions to Ask Your Doctor**:
> 1. *"Could my elevated ferritin and AST be related to recent workouts, supplements, or a recent virus?"*
> 2. *"Would you recommend repeating this panel fasting in 4-6 weeks, or checking fasting iron saturation?"*

---

## Red-Flag Emergency Directives
If you or anyone around you experiences:
- Sudden severe chest pain or pressure
- Difficulty breathing or shortness of breath
- Sudden numbness, weakness, or facial drooping (signs of stroke)
- Uncontrolled bleeding or severe head trauma

**Close the AI chat immediately and call emergency services (e.g. 911 / 112 / 999) or proceed to the nearest emergency department.**
