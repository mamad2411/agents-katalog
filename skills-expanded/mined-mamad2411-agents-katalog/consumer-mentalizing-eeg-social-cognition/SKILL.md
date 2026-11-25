---
name: consumer-mentalizing-eeg-social-cognition
description: Applies the emerging research on consumer mentalizing — the social-cognitive process of inferring others' mental states during consumption contexts — measured via EEG. Use when designing advertising, influencer content, testimonial narratives, or any marketing that involves social cues where consumers infer characters' emotions, intentions, and goals. Bridges social cognition neuroscience with consumer behavior research.
---

# Consumer Mentalizing: EEG-Based Social Cognition in Consumer Behavior

## Overview

Mentalizing — the ability to infer one's own and others' internal states, beliefs, intentions, and emotions — is a core social cognition process that has been largely overlooked in consumer neuroscience research. While neuromarketing has traditionally focused on basic processes like emotion, attention, and memory, mentalizing represents a higher-order social-cognitive layer that explains how consumers interpret social cues in advertising, influencer content, and testimonial narratives.

## Key Research Findings

### The Mentalizing Framework for Consumer Behavior

**Source:** Casiraghi, Zito & Russo (IULM University, Frontiers in Psychology, April 2026) + Bilucaglia, Casiraghi, Russo & Zito (Frontiers in Behavioral Neuroscience, July 2026)

Mentalizing is positioned as a **mediating process** between marketing stimuli containing social cues (human interactions, brand personifications, testimonials, influencer communication) and consumer responses. This extends the Elaboration Likelihood Model and Narrative Transportation Theory by adding a social-cognitive layer.

**Key distinctions:**
- Mentalizing ≠ Empathy (empathy involves emotional resonance and affective sharing; mentalizing is the inferential process)
- Mentalizing ≠ Theory of Mind (ToM uses societal heuristics; mentalizing is the more fundamental attribution process)
- Mentalizing ≠ Perspective-taking (cognitive adoption of another's viewpoint)

### EEG Correlates of Consumer Mentalizing

**Perspective-taking in video advertising (Bilucaglia et al., 2026):**
- N=20 participants, EEG recorded during food/beverage ad viewing with testimonial-style product interactions
- **Cognitive perspective-taking** correlated negatively with frontal θ power (F7, F4 electrodes) — suggesting more fluent, automatic processing when mentalizing is engaged
- **Cognitive perspective-taking** correlated positively with α clustering coefficient — indicating information integration and working memory involvement
- **Perceived ad effectiveness** correlated with α clustering coefficient, α kappa divergence (MST), α path length, and δ average degree/path length
- Partial overlap between cognitive perspective-taking and ad effectiveness EEG correlates (α clustering coefficient) — consistent with Narrative Transportation Theory
- Effects were stimulus-specific (not consistent across all ads), influenced by product type, testimonial gender, and interaction type

### Why EEG Over Other Methods

- **fMRI**: Good spatial resolution but poor temporal resolution; immobile setup unsuitable for interactive consumer experiences
- **Eye-tracking**: Most used in practice but cannot access complex social-cognitive processes like mentalizing
- **fNIRS**: Portable but shallow spatial resolution
- **Autonomic measures (GSR, HR)**: Track affective responses but cannot isolate cognitive/inferential features
- **EEG**: Millisecond temporal resolution, portable, cost-effective, adaptable to diverse scenarios (video ads, purchase interactions, social media dynamics), adopted in applied market research

## Practical Framework

### When Mentalizing Matters in Consumer Contexts

1. **Testimonial advertising**: Characters physically interacting with products (eating, drinking) trigger perspective-taking and embodied simulation
2. **Influencer marketing**: Consumers mentalize with influencers even without physical copresence
3. **Social proof and conformity**: Observational learning, social comparison, and social proof all rely on mentalizing
4. **Narrative transportation**: Character identification requires mentalizing as a precursor
5. **Brand personification**: Anthropomorphized brands trigger mental state attribution

### Design Implications

**To enhance mentalizing in marketing content:**
- Include human characters with clear emotional expressions and intentional actions
- Show product interactions that trigger embodied simulation (characters using/experiencing products)
- Create narrative structures that require viewers to infer character motivations
- Match testimonial characteristics (gender, demographics) to target audience for stronger identification
- Design social media content that invites inference about the creator's mental state

**To measure mentalizing via EEG:**
- Use high-density systems (50-60 electrodes) for sufficient spatial resolution
- Combine spectral analysis (θ, α, β, γ bands) with connectivity measures (MST-based)
- Pair EEG with behavioral and self-report measures for data triangulation
- Validate with established mentalizing paradigms adapted to consumer stimuli
- Consider hyperscanning approaches for interactive/conversational contexts

### Ethical Considerations

- Measuring mentalizing raises **psychological privacy** concerns (capturing how individuals infer others' intentions)
- Potential for manipulation if used to design persuasive strategies without transparency
- Requires informed consent, transparency, and data protection
- Must adhere to ethical guidelines in both neuroscience and consumer research

## A-Tech Alignment

- **Open-source**: EEG analysis tools (EEGLab, Brain Connectivity Toolbox) are open-source; methodology is reproducible
- **Data privacy**: EEG-based mentalizing measurement avoids centralized biometric data collection when combined with on-device processing
- **Financial freedom**: Understanding social cognition in consumer behavior enables more effective open-source product marketing
- **Practical implementation**: Framework provides concrete EEG correlates and measurement protocols

## Cross-References

- `cognitive-science-and-ux/neuroadaptive-attention-engineering` — complementary neural measurement approach
- `marketing-and-content/narrative-transportation-developer-trust` — narrative transportation relies on mentalizing
- `marketing-and-content/marketing-digital-human-dual-trust-neural` — digital humans trigger mentalizing
- `privacy-and-trust/authenticity-by-design-cognitive-autonomy` — mentalizing measurement and cognitive autonomy

## Limitations and Future Directions

- Current EEG evidence on mentalizing is limited and fragmented
- Theta and alpha band findings are inconsistent across studies
- Scalp-level analysis has limitations vs. source-level analysis (needs 64+ electrodes for cortical connectivity)
- Short stimulus segments (~3s) may limit reliability of connectivity estimates
- Need larger samples (40+ participants) and more controlled stimulus sets
- Future: HD-EEG, source localization, longer epochs, multimethod approaches (EEG + eye-tracking + behavioral)