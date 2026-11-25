---
name: ai-character-fnirs-eye-tracking-design
description: Applies the first integrated fNIRS + eye-tracking study of how AI-generated character design variables (age and image type: real/2D/3D) affect visual attention and prefrontal cognitive engagement. Use when designing AI-generated characters for marketing, customer service, or brand representation; selecting character age and visual style; or evaluating user engagement with virtual characters.
---

# AI-Generated Character Design: fNIRS + Eye-Tracking Integration

## Overview
This skill applies the first study combining functional near-infrared spectroscopy (fNIRS) and eye-tracking to measure how AI-generated character design choices — age (infant to elderly) and image type (real, 2D cartoon, 3D character) — affect both visual attention (pupil dilation, fixation patterns) and prefrontal cognitive engagement (DLPFC oxygenated hemoglobin), providing evidence-based guidance for character design.

## When to Use
- Designing AI-generated characters for advertising, brand marketing, social media, or customer service
- Selecting character age representation for target audiences
- Choosing between real, 2D cartoon, or 3D character visual styles
- Evaluating emotional rapport and cognitive engagement with virtual characters
- NOT for: character design decisions based solely on aesthetic preference without engagement measurement

## Core Process / Workflow

### 1. Map Design Variables to User Response

Two design variables systematically affect user engagement:

**Age conditions (6 levels):** infant, child, adolescent, adult, middle-aged, elderly
**Image type conditions (3 levels):** real photograph, 2D cartoon, 3D character

### 2. Use the Dual-Metric Assessment Framework

| Metric | What It Measures | Tool | Key Finding |
|---|---|---|---|
| **Average pupil diameter** | Emotional arousal, liking, engagement | Eye-tracker (Tobii Pro Spectrum, 1200 Hz) | Middle-aged + 3D = highest arousal |
| **Number of fixations** | Visual exploration strategy, cognitive processing | Eye-tracker | Real images = lower for adult condition |
| **DLPFC HbO concentration** | Higher-order cognitive engagement, evaluation, decision-making | fNIRS (NIRSIT, 48 channels) | Child condition = highest right DLPFC; AI-generated (2D/3D) = higher left DLPFC |

### 3. Apply the Age × Image Type Interaction

**Pupil diameter (emotional arousal):**
- **Middle-aged + 3D** produces the largest pupil dilation (highest arousal/engagement)
- Within 3D condition: middle-aged > all other age groups (p=.003, η²=.230)
- Within middle-aged: 3D > real and 2D (p=.022, η²=.275)

**DLPFC cognitive engagement (HbO):**
- **Child condition** triggers highest right DLPFC activation (Channel 5, p=.003, η²=.146) and left DLPFC (Channel 19, p=.038, η²=.100)
- **AI-generated characters (2D and 3D)** produce higher left DLPFC activation than real images (Channel 35, p=.006, η²=.190)

### 4. Interpret the Complementary Pupil-HbO Pattern

The two metrics reveal **distinct cognitive states**:

| Pattern | Pupil Dilation | DLPFC HbO | Interpretation |
|---|---|---|---|
| **High pupil + Low DLPFC** | High | Low | Bottom-up attentional capture; insufficient top-down cognitive control; strong affective pull with limited deliberate evaluation |
| **Low pupil + High DLPFC** | Low | High | Top-down cognitive control; stable arousal; deliberate evaluation; well-learned or predictable stimuli |

### 5. Design Strategy by Use Case

**For rapid attention capture (advertising, social media scrolling):**
- Use **middle-aged 3D characters** → largest pupil dilation → strongest initial attention pull
- Apply to contexts where quick engagement matters more than deep evaluation

**For deeper cognitive engagement (customer service, educational content):**
- Use **child-age characters** → highest DLPFC activation → greater evaluative processing
- Apply to contexts where users need to process and evaluate information

**For AI character vs real photograph choice:**
- **AI-generated characters (2D/3D)** produce higher left DLPFC engagement than real images
- This suggests AI characters trigger more active cognitive evaluation
- Use AI characters when you want users to actively process character-related information

### 6. Apply the Integrated Design Framework

```
Design Decision Tree:
├── Goal: Rapid attention capture
│   └── Choose: Middle-aged + 3D character
│   └── Expected: High pupil dilation, moderate DLPFC
├── Goal: Deep cognitive engagement
│   └── Choose: Child-age character (any image type)
│   └── Expected: High DLPFC HbO, moderate pupil
├── Goal: Active evaluation of AI character
│   └── Choose: AI-generated (2D or 3D) over real photograph
│   └── Expected: Higher left DLPFC activation
└── Goal: Balanced engagement
    └── Choose: Adult + 2D cartoon
    └── Expected: Moderate on both metrics
```

## Key Evidence

**Source:** Cha, Lee & Kim, Sejong/Hongik University, Frontiers in Human Neuroscience, April 2026
- 24 participants (21-26 years, 11 male/13 female, all right-handed)
- 18 stimuli: 6 age conditions × 3 image types
- Eye-tracker: Tobii Pro Spectrum, 1200 Hz; 4 metrics (total fixation duration, average fixation duration, number of fixations, average pupil diameter)
- fNIRS: NIRSIT (OBELAB), 48 channels, 780/850 nm, prefrontal cortex mapping
- Repeated-measures ANOVA with Greenhouse-Geisser correction, Bonferroni post-hoc, FDR correction
- IRB approved (Hongik University IRB no. 7002340-202409-HR-023)

**Key statistical results:**
- Pupil diameter: Age×Type interaction F=3.88, p=.003, η²=.230 (3D condition, middle-aged highest)
- Pupil diameter: Within middle-aged, 3D > real and 2D, F=4.17, p=.022, η²=.275
- Number of fixations: Within adult, real < 2D and 3D, F=3.76, p=.030, η²=.190
- Right DLPFC (Ch 5): Age effect F=3.94, p=.003, η²=.146 (child highest)
- Left DLPFC (Ch 19): Age effect F=2.57, p=.038, η²=.100 (child highest)
- Left DLPFC (Ch 35): Type effect F=5.39, p=.006, η²=.190 (2D and 3D > real)

## A-Tech Alignment

- **Open-source:** fNIRS and eye-tracking analysis can use open-source tools (NIRSIT Quest, standard neuroimaging libraries)
- **Data privacy:** Physiological measurement in controlled settings; no biometric surveillance in the wild
- **Financial freedom:** Enables SMEs to make evidence-based character design decisions without expensive A/B testing at scale
- **Practical implementation:** Concrete design decision tree based on physiological evidence

## References
- See [references/evidence-base.md](references/evidence-base.md) for full methodology, statistical tables, and theoretical interpretation.