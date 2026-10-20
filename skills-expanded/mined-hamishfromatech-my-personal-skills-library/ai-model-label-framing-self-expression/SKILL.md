---
name: ai-model-label-framing-self-expression
description: Applies research on how AI-generated model labels function as emphasis-framing cues that reduce consumer self-expression through eeriness and perceived risk. Use when designing AI disclosure labels for product displays, deciding whether to label AI-generated models, or evaluating how AI transparency requirements impact symbolic vs functional product categories.
---

# AI Model Label Framing Effect on Consumer Self-Expression

## Overview
This skill applies the first systematic study of how labeling a product display model as "AI-generated" functions as an emphasis-framing cue that triggers eeriness, elevates perceived psychological and performance risk, and reduces consumer self-expression — but only for symbolic products, not functional ones.

## When to Use
- Designing AI disclosure labels for product displays (regulatory compliance: EU AI Act, California AI Transparency Act, China AI labeling measures)
- Deciding whether to use AI-generated models vs human models for product imagery
- Evaluating how AI transparency requirements will impact different product categories
- Building adaptive labeling strategies that minimize negative consumer responses
- NOT for: low-stakes factual content where AI labels have no measurable effect (see ai-generated-ad-pretesting-effectiveness)

## Core Process / Workflow

### 1. Assess Product Type (Symbolic vs Functional)

Determine whether the product is primarily **symbolic** (luxury, fashion, identity-expressive — e.g., a dress) or **functional** (utilitarian, practical — e.g., a T-shirt).

**Decision rule:**
- Symbolic products → AI label effects are LARGE and negative (self-expression drops significantly)
- Functional products → AI label effects DISAPPEAR (no significant difference between AI and human labels)

### 2. Understand the Mediation Chain

The AI model label operates through a serial mediation pathway:

```
AI Label → Eeriness → Perceived Psychological Risk → Reduced Self-Expression
AI Label → Eeriness → Perceived Performance Risk → Reduced Self-Expression
```

**Key mechanism:** The AI label is an **emphasis-framing cue** that brings the model's nonhuman source to the foreground, making consumers unable to project themselves into the wearing context.

### 3. Apply the Product Type Boundary Condition

The entire negative effect is **moderated by product type**:

| Product Type | Eeriness | Psych Risk | Perf Risk | Self-Expression |
|---|---|---|---|---|
| Symbolic (dress) | AI >> Human (p<.001) | AI >> Human (p<.001) | AI >> Human (p<.001) | AI << Human (p<.001) |
| Functional (T-shirt) | No difference (p=.169) | No difference (p=.354) | No difference (p=.149) | No difference (p=.137) |

### 4. Design Adaptive AI Labeling Strategy

**For symbolic products:**
- Exercise extreme caution with AI-generated models
- Prioritize human models for identity-expressive categories
- If AI models are used, consider assigning names and backstories to enhance perceived social presence
- Provide body measurements alongside images to aid self-projection
- Position AI-generated models as brand-affiliated representatives

**For functional products:**
- AI-generated models can be adopted proactively for cost efficiency
- AI labels have no measurable negative effect on self-expression
- Focus on functional attributes (specs, quality, price) in messaging

### 5. Implement Risk Mitigation

When AI labels are required (regulatory compliance):
- Provide detailed product material descriptions and close-up displays
- Strengthen brand trust signals (endorsements, quality guarantees, after-sales)
- Reduce perceived uncertainty through informational support
- Design label wording, placement, and contextual explanation carefully

## Key Evidence

**Source:** Cheng & Nam, Chung-Ang University, Frontiers in Psychology, July 2026
- 2×2 between-subjects experiment (AI vs Human label × Symbolic vs Functional product)
- N=200 US participants via MTurk
- Serial mediation via PROCESS Model 81
- Self-expression (α=.969) as focal outcome (not purchase intention or attitude)
- All CIs exclude zero for indirect effects

**Effect sizes (symbolic products):**
- Self-expression: AI=1.97 vs Human=4.37 (p<.001)
- Eeriness: AI=5.91 vs Human=3.97 (p<.001)
- Perceived psychological risk: AI=5.99 vs Human=3.67 (p<.001)
- Perceived performance risk: AI=6.01 vs Human=4.13 (p<.001)

## A-Tech Alignment

- **Open-source:** Applies to AI-generated marketing for OSS products (open-weight image models can generate models)
- **Data privacy:** Behavioral proxies (self-report) over biometric surveillance
- **Financial freedom:** Reduces cost of product imagery for SMEs (AI models cheaper than human photoshoots)
- **Practical implementation:** Clear decision framework based on product type

## References
- See [references/evidence-base.md](references/evidence-base.md) for full experimental details, mediation analysis, and theoretical context.