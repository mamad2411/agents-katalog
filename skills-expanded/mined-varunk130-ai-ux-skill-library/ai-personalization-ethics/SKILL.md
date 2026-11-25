---
name: ai-personalization-ethics
description: 'Design AI-driven personalization that adapts interfaces to users while respecting privacy, avoiding filter bubbles, and maintaining user agency. Use when: adaptive UI, AI personalization, recommendation UX, filter bubble prevention, privacy personalization balance, algorithmic fairness UX, user preference learning.'
---

# AI Personalization & Ethics

Design adaptive interfaces that learn from users and improve over time - without crossing into surveillance, manipulation, or exclusion. The ADAPT framework ensures personalization serves the user's interests, not just engagement metrics.

## Core Principle

Personalization is not a feature - it is a **power dynamic.** The system knows things about the user that the user may not know about themselves. With that knowledge comes responsibility: personalization must be transparent, controllable, and in service of the user's actual goals, not the platform's engagement targets.

---

## The ADAPT Framework

| Letter | Principle | Design Question |
|---|---|---|
| **A** | Agency Preserved | Can the user see, understand, and override every personalization decision? |
| **D** | Data Minimized | Are you collecting only what's necessary, and being transparent about it? |
| **A** | Alternatives Accessible | Can the user easily access non-personalized or differently-personalized views? |
| **P** | Patterns Not Profiles | Are you personalizing based on behavior patterns, not invasive profiling? |
| **T** | Tested for Fairness | Have you verified that personalization doesn't discriminate across user groups? |

---

## The Personalization Ladder

Not all personalization is created equal. Higher rungs are more valuable but more ethically complex.

| Rung | Personalization Type | Data Needed | Value to User | Ethical Risk |
|---|---|---|---|---|
| 1 | **Segment-based** | Demographics, role, industry | Low-medium (generic) | Low - broad groupings |
| 2 | **Preference-based** | Explicit user settings | Medium (user-controlled) | Very low - user chose this |
| 3 | **Behavior-based** | Usage patterns, interaction history | High (relevant) | Medium - user may not realize they're being tracked |
| 4 | **Predictive** | ML models inferring future needs | Very high (proactive) | High - AI "knows" things about the user |
| 5 | **Contextual** | Location, time, device, ambient signals | Highest (seamless) | Highest - feels invasive if done without consent |

**Design rule:** Start at Rung 2 (explicit preferences). Only climb higher with user consent, transparency, and a clear user benefit that justifies the data collection.

---

## The Personalization Transparency Card

Every personalized AI experience should have an accessible transparency card explaining:

| Element | Content | Example |
|---|---|---|
| **What is personalized** | Which elements of the experience adapt to the user | "Your dashboard layout, content recommendations, and notification timing are personalized." |
| **What data drives it** | Which user data informs personalization decisions | "Based on: your interaction history, stated preferences, and team role." |
| **How to control it** | User controls for adjusting or disabling personalization | Toggle: "Use personalized experience" / "Use default experience" |
| **How to reset** | Ability to clear learned preferences and start fresh | "Reset my preferences" button with confirmation |
| **What you don't track** | Explicit statement of data not collected | "We do not track: browsing outside this app, personal demographics, or individual keystrokes." |

---

## The Filter Bubble Audit

AI personalization can trap users in echo chambers. Design deliberate escape hatches.

### Filter Bubble Risk Indicators

| Signal | Risk Level | Intervention |
|---|---|---|
| User only sees content matching past preferences | High | Inject "Outside your usual" section with diverse recommendations |
| Recommendation diversity score drops below 30% | High | Algorithmic diversity floor: ensure minimum variety |
| User hasn't discovered a major feature after 30 days | Medium | Proactive feature surfacing outside the personalization model |
| Same 5 content sources repeatedly recommended | Medium | Source diversity requirement in recommendation algorithm |
| User clicks "not interested" on novel content | Low (but watch) | Distinguish "not now" from "never" - don't over-learn from single signals |

### Escape Hatch Patterns

| Pattern | How It Works | When to Use |
|---|---|---|
| **"Explore" mode** | Temporarily disables personalization, shows popular/trending/random | Always available as a toggle |
| **"Show me something different"** | Single-click to get recommendation outside the model | On any recommendation surface |
| **Diversity slider** | User controls the balance between "familiar" and "surprising" | Products with content feeds or recommendation engines |
| **Serendipity injection** | System randomly introduces 10-15% non-personalized content | Always (invisible to user, but prevents extreme narrowing) |

---

## Privacy-Personalization Spectrum

| Privacy Level | What's Allowed | User Experience | When Appropriate |
|---|---|---|---|
| **Maximum privacy** | No tracking, no personalization, anonymous use | Generic experience, same for everyone | Privacy-critical contexts (health, finance) |
| **Declared preferences** | Only explicit user-stated preferences | Good personalization from settings, no behavioral tracking | Default for most products |
| **Behavioral learning** | Track in-product behavior to improve experience | Strong personalization, requires transparency about data use | After explicit consent |
| **Cross-session profiling** | Build persistent user model across sessions | Highly tailored experience, requires strong privacy controls | Power users who opt in |
| **Cross-platform** | Combine data from multiple services | Maximum personalization but maximum privacy risk | Only with granular consent per data source |

---

## Fairness Checkpoints

AI personalization can silently discriminate. Build fairness checks into the design process.

### The Fairness Audit Checklist

| Checkpoint | Question to Ask | Red Flag |
|---|---|---|
| **Access equity** | Does personalization give different quality of service to different user groups? | Premium features shown only to "high-value" users |
| **Price discrimination** | Are prices or offers different based on inferred user characteristics? | Higher prices shown to users with expensive devices |
| **Information equity** | Do all users have access to the same critical information? | Safety warnings personalized away from some groups |
| **Representation** | Do recommendations reflect the diversity of available content? | Only recommending content from dominant cultural perspectives |
| **Recovery equity** | Can all users equally recover from bad personalization? | Reset/override options harder to find for less technical users |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| Personalizing without telling the user | Users discover they're in a filter bubble and feel manipulated |
| "Based on your activity" with no detail | Which activity? When? How does it affect what I see? Vagueness breeds distrust |
| Making it hard to disable personalization | Buried in Settings > Privacy > Advanced > Personalization = hostile design |
| Learning too fast from single interactions | One click on a topic ≠ lifelong interest. Build in decay and forgetting |
| Personalizing critical safety information | Warnings, terms, security alerts must be universal - never filter these |
| A/B testing personalization without consent | Users in different test groups get materially different experiences without knowing |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Add personalization to AI product | Personalization Ladder + ADAPT framework | Rung selection + transparency card design |
| Audit for filter bubbles | Filter Bubble Audit | Risk assessment + escape hatch implementation plan |
| Balance privacy and personalization | Privacy-Personalization Spectrum | Privacy tier selection + consent flow design |
| Check for discrimination | Fairness Audit Checklist | Fairness report with access, pricing, information, and representation checks |
| Design personalization controls | Transparency Card elements | User-facing control panel specification |

## Integration

Works with: `ai-safety-guardrails` (preventing personalization-driven harm), `ai-trust-transparency` (transparency about what's personalized), `ai-onboarding-calibration` (personalizing the onboarding experience), `ai-prompt-ux` (personalized prompt suggestions).
