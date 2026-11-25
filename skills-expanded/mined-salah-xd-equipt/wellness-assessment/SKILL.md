---
name: wellness-assessment
description: "Builds wellness intake assessments with health history, goal setting, and lifestyle evaluation questionnaires."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Wellness Assessment

## When to Use This Skill

Use this skill when you need to:
- Create a wellness intake assessment for new coaching or training clients
- Build health history questionnaires that inform program design
- Design goal-setting frameworks for wellness engagements
- Evaluate lifestyle factors that affect client outcomes

**DO NOT** use this skill for medical intake forms, clinical assessments, or diagnostic questionnaires. This is for wellness coaches, personal trainers, and health coaches operating within their scope of practice.

---

## Core Principle

A WELLNESS ASSESSMENT IS NOT A MEDICAL EXAM — IT IS A TOOL TO UNDERSTAND WHERE YOUR CLIENT IS, WHERE THEY WANT TO GO, AND WHAT LIFESTYLE FACTORS WILL HELP OR HINDER THEIR PROGRESS.

---

## Phase 1: Assessment Scope

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Service type** | "What service will you provide — personal training, health coaching, nutrition coaching?" | Health coaching |
| **Client population** | "Who are your typical clients?" | Adults 30-55, general wellness |
| **Scope of practice** | "What are your credentials and what are you qualified to assess?" | No default — must be provided |
| **Assessment depth** | "How detailed — quick screening or comprehensive intake?" | Comprehensive intake |
| **Follow-up assessments** | "Will you reassess periodically?" | Yes — every 8-12 weeks |

**GATE: Confirm scope of practice before designing the assessment. Only include sections you are qualified to evaluate.**

---

## Phase 2: Assessment Sections

### Section 1: Personal Information

```
## Client Information

Name: _______________
Date: _______________
Date of birth: _______________
Email: _______________
Phone: _______________
Emergency contact: _______________
Emergency phone: _______________
```

### Section 2: Health History

```
## Health History

**Current medical conditions (check all that apply):**
[ ] Heart disease or cardiovascular condition
[ ] High blood pressure
[ ] Diabetes (Type 1 / Type 2)
[ ] Asthma or respiratory condition
[ ] Joint or bone issues (arthritis, osteoporosis)
[ ] Back pain or spinal conditions
[ ] Thyroid condition
[ ] Anxiety or depression
[ ] Autoimmune condition
[ ] None of the above
[ ] Other: _______________

**Current medications:**
_______________

**Allergies (food, medication, environmental):**
_______________

**Past surgeries or injuries:**
_______________

**Are you currently under a doctor's care for any condition?** Yes / No
If yes, has your doctor cleared you for [exercise / dietary changes]? Yes / No / Not yet

**For women: Are you pregnant or planning to become pregnant?** Yes / No / N/A

**Do you have any physical limitations that affect movement or exercise?**
_______________
```

### Section 3: Lifestyle Evaluation

```
## Current Lifestyle

**Sleep:**
- Average hours per night: ___
- Sleep quality (1-5, 5 = excellent): ___
- Do you have trouble falling or staying asleep? Yes / No

**Stress:**
- Current stress level (1-10, 10 = extremely stressed): ___
- Top 3 sources of stress: _______________
- How do you currently manage stress? _______________

**Nutrition (typical day):**
- Breakfast: _______________
- Lunch: _______________
- Dinner: _______________
- Snacks: _______________
- Water intake (glasses per day): ___
- Alcohol (drinks per week): ___
- Caffeine (cups per day): ___

**Physical Activity:**
- Current exercise frequency: ___ days/week
- Types of exercise: _______________
- Activity level at work: Sedentary / Lightly active / Active / Very active

**Habits:**
- Do you smoke? Yes / No / Former
- Screen time (hours per day outside of work): ___
```

### Section 4: Goals & Motivation

```
## Your Goals

**Primary goal:**
_______________

**Why is this goal important to you right now?**
_______________

**What have you tried before to achieve this goal?**
_______________

**What worked? What didn't?**
_______________

**On a scale of 1-10, how ready are you to make changes?** ___

**On a scale of 1-10, how confident are you that you can succeed?** ___

**What is the biggest obstacle you anticipate?**
_______________

**How will you know you have succeeded? What does success look and feel like?**
_______________

**Timeline: When do you want to achieve this goal?**
_______________
```

---

## Phase 3: Evaluation & Summary

### Assessment Summary Template

```
## Wellness Assessment Summary — [Client Name]

**Date:** [Date]
**Assessed by:** [Your name]

### Key Findings

**Health considerations:**
- [Any conditions or medications that affect programming]
- [Referral needed? Yes/No — to whom]

**Lifestyle strengths:**
- [What they are already doing well]

**Lifestyle areas for improvement:**
- [Sleep, stress, nutrition, or activity gaps]

**Goal alignment:**
- Primary goal: [Goal]
- Readiness level: [X/10]
- Confidence level: [X/10]
- Timeline: [Stated timeline — realistic? Yes/No]

### Recommended Focus Areas (Priority Order)

1. [Focus area 1] — [Why and initial action step]
2. [Focus area 2] — [Why and initial action step]
3. [Focus area 3] — [Why and initial action step]

### Referrals Needed
- [ ] Medical clearance from physician
- [ ] Registered dietitian for [specific concern]
- [ ] Mental health professional for [specific concern]
- [ ] Physical therapist for [specific concern]
- [X] None needed at this time
```

### Reassessment Plan

Schedule reassessments at regular intervals:
- **4-week check-in:** Quick progress review, habit adherence, adjust as needed
- **8-12 week reassessment:** Full assessment comparison, measure progress toward goals
- **Ongoing:** Brief monthly check-ins between full assessments

---

## Phase 4: Implementation

### Delivery Options

| Format | Best For |
|--------|----------|
| Paper form | In-person consultations |
| Google Form | Remote clients, automated collection |
| PDF fillable form | Email-based intake |
| Practice management software | Integrated client management (Practice Better, TrueCoach) |

### Assessment Checklist

- [ ] All sections are appropriate for your scope of practice
- [ ] Health history section covers conditions relevant to your service
- [ ] Consent and disclaimer are included (see health-disclaimer skill)
- [ ] Referral triggers are identified (when to refer to a medical professional)
- [ ] Assessment is stored securely and confidentially
- [ ] Reassessment schedule is communicated to the client
- [ ] Summary is reviewed with the client, not just filed away

---

## Anti-Patterns

- **Asking medical questions beyond your scope** — if you are not a doctor, do not diagnose. Collect history and refer when appropriate.
- **Collecting data and never using it** — every question should inform your programming. Remove questions that do not change what you do.
- **Skipping the health history** — starting a fitness or nutrition program without knowing medical conditions is reckless.
- **Not following up on red flags** — if a client reports chest pain during exercise or an unmanaged condition, refer them to a physician before continuing.
- **One assessment and done** — progress tracking requires reassessment. Build it into your process.

---

## Recovery

- **Client does not disclose a condition:** Include a clause that the client is responsible for disclosing all relevant health information and updating you if their status changes.
- **Red flag in health history:** Pause programming and require medical clearance. Do not design programs around conditions you are not qualified to manage.
- **Client is resistant to the assessment:** Explain that the assessment ensures their safety and helps you design the most effective program for them.
- **Assessment is too long:** Trim to essential sections only. A 30-minute assessment that gets completed beats a 60-minute one that gets abandoned.
- **Client goals are unrealistic:** Have an honest conversation. Adjust the timeline or reframe the goal to be achievable and measurable.
