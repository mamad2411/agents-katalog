---
name: promotional-preventive-framing-erp-neuromarketing
description: Applies the first ERP study of promotional vs. preventive framing in AI-generated content (Wang, Alves, Hu & Chen, Zhejiang University, Scientific Reports, July 2026) to optimize AIGC recommendation messaging. Use when designing AI-generated marketing content, testing message framing strategies for AI recommendations, or evaluating consumer trust in AI-mediated communication.
---

# Promotional-Preventive Framing in AIGC Neuromarketing

## Overview
This skill applies the first ERP (Event-Related Potentials) study examining how promotional and preventive message framing in AI-generated content (AIGC) influences consumer trust and neural responses, with implications for designing more effective AI-mediated marketing communication.

## When to Use
- Designing AI-generated marketing messages for products or services
- Testing message framing strategies for AI recommendation systems
- Evaluating consumer trust responses to AI-generated content
- Optimizing AIGC for hedonic vs. utilitarian products
- NOT for human-authored content (study is specific to AIGC context)
- NOT for direct behavioral purchase prediction (study uses passive viewing paradigm)

## Core Process / Workflow

### 1. Study Design
- **Source:** Wang, Alves, Hu & Chen, Zhejiang University Neuromanagement Lab, Scientific Reports 16, 23547 (July 2026)
- **Design:** 2 (message framing: promotion vs. prevention) × 2 (product type: hedonic vs. utilitarian) within-subject
- **Participants:** 28 right-handed students (19 male, mean age 21.91, SD 2.63)
- **Stimuli:** 20 AIGC images + 40 framed recommendation messages (20 promotional, 20 preventive)
- **Method:** 64-electrode EEG, E-Prime 3.0, Neuroscan Synamp 2

### 2. Key Findings

**Behavioral Results:**
- Promotional messages elicited **higher trust ratings** than preventive messages across both product types (p = .007, η²p = 0.242)
- Promotional messages elicited **faster reaction times** (p = .005, η²p = 0.259)
- No significant interaction between framing and product type on behavioral measures

**Neural Results (ERP Components):**

| Component | Time Window | Key Finding | Significance |
|-----------|-------------|-------------|--------------|
| **P300** | 300-400ms | Promotion + hedonic → larger P3 (greater attentional engagement) | F(1,27)=10.03, p=.004, η²p=0.271 |
| **N400** | 400-500ms | Prevention + hedonic → larger N4 (more semantic processing difficulty) | F(1,27)=9.04, p=.006, η²p=0.251 |
| **LPP** | 600-800ms | Interaction significant, but no reliable simple-framing differences | F(1,27)=7.74, p=.010, η²p=0.223 |

**Core Insight:** For hedonic products, promotion-framed AIGC recommendations enhance attentional engagement (P3) and reduce semantic processing difficulty (N4). For utilitarian products, framing strategy matters less because consumers already perceive AI as competent for functional recommendations.

### 3. Regulatory Focus Theory in AIGC Context

The study extends Regulatory Focus Theory to AI-generated content:
- **Promotion focus:** Emphasizes gains, aspirations, positive outcomes
- **Prevention focus:** Emphasizes risk reduction, safety, avoiding negative outcomes
- **Hedonic products:** Pleasure, enjoyment, experiential value (aligns with promotion)
- **Utilitarian products:** Practicality, functionality, problem-solving (aligns with prevention)

**Key difference from human-authored content:** The "word-of-machine effect" (Longoni & Cian, 2020) suggests consumers perceive AI as more competent for utilitarian than hedonic recommendations. This makes framing less critical for utilitarian products but essential for hedonic ones.

### 4. Practical Framework for AIGC Message Design

```
Message Design Decision Tree:

1. Identify product type:
   - Hedonic (gaming, fragrance, entertainment, luxury)
   - Utilitarian (tools, appliances, software, data storage)

2. Select framing strategy:
   IF hedonic:
     → Use PROMOTIONAL framing ("Ignite every thrilling moment")
     → Emphasize enjoyment, aspiration, positive experiences
     → Expected neural response: enhanced P3, reduced N4
   IF utilitarian:
     → Framing less critical (AI already perceived as competent)
     → Either framing acceptable; promotion slightly better overall
     → Focus on functional benefits and reliability

3. For AI-generated recommendations specifically:
   → Promotional framing mitigates AI skepticism for hedonic products
   → Prevention framing for hedonic products creates cognitive dissonance (larger N4)
   → AI competence perception already favors utilitarian recommendations
```

### 5. A-Tech Application Framework

**For Open-Source AI Products:**
- When generating marketing content with AI models, default to promotional framing for experiential/developer experience features
- For compliance/security features (utilitarian), framing matters less but promotional still slightly preferred
- Use this framework to design AI-generated content that builds trust without manipulating

**Privacy-First Adaptation:**
- ERP signals are indirect indicators of attention and processing, not direct trust measures
- Behavioral trust ratings should complement neural insights
- All AIGC should disclose AI authorship (the study context assumes AIGC labeling)

**Ethical Guardrails:**
- The study explicitly notes ERP signals are "indirect indicators that may support but do not confirm trust-related evaluations"
- Avoid reverse inference: P3 amplitude ≠ trust; it indicates attentional engagement
- Promotional framing effectiveness should not be used to exploit consumer vulnerability

## References
- See [references/evidence-base.md](references/evidence-base.md) for full methodology, statistical results, and comparison with prior framing research.