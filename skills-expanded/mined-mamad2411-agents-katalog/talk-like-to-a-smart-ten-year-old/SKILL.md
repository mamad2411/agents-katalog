---
name: talk-like-to-a-smart-ten-year-old
description: "Explain complex ideas in clear everyday language with concrete examples and without condescension."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["eli10", "mental-models", "analogies", "learning", "simplification", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Explain Like I Am a Smart 10-Year-Old (The ELI10 Analogy Protocol) (AI Skill)

## Overview
When users ask for simple explanations using *"Explain like I am 5 (ELI5)"*, models often generate babyish, patronizing metaphors (*"Imagine a magical fairy giving cookies..."*). Conversely, standard technical explanations are dense with acronyms and math.

The **ELI10 Analogy Protocol** (*"Explain like I am a smart, curious 10-year-old"*) hits the sweet spot of conceptual clarity: it replaces abstract math with **tangible physical mechanical analogies**, preserving scientific truth while eliminating cognitive friction.

---

## The 3-Step ELI10 Mental Model Framework

```
┌─────────────────────────────────────────────────────────────┐
│                 The 3-Step ELI10 Framework                  │
│                                                             │
│  1. THE PHYSICAL ANALOGY ──► Ground in a physical object    │
│                              (Lockboxes, post offices, dams)│
│  2. THE CORE MECHANISM   ──► How the moving parts interact  │
│  3. WHY IT MATTERS       ──► The real-world consequence     │
└─────────────────────────────────────────────────────────────┘
```

---

## Master ELI10 Prompt Templates

### Pattern 1: The Physical Analogy Deconstructor
Use for complex software, cryptography, finance, or physics:

```markdown
Explain [COMPLEX CONCEPT: e.g. Public Key Cryptography / Vector Databases] to me like I am a smart, curious 10-year-old.

Rules:
1. **The Physical Analogy**: Use a physical, real-world metaphor (e.g. locks, mailboxes, library shelves, recipes).
2. **The Mechanism**: Explain the step-by-step process without using technical jargon or acronyms.
3. **The 'Aha!' Takeaway**: Conclude with 1 sentence explaining why this was a breakthrough for humanity.
4. Keep the total response under 150 words.
```

---

### Pattern 2: The Jargon-Free Mechanism Test
Use to prepare client-friendly explanations:

```markdown
I need to explain [OUR TECHNICAL FEATURE] to a non-technical customer.
- Translate the technical architecture into a plain-English physical analogy.
- Zero buzzwords (no "scalable", "AI-driven", "synergistic", "paradigm").
```

---

## Real-World Case Study

### Scenario: Explaining Public Key Cryptography (Asymmetric Encryption)

#### Standard Textbook Explanation (Jargon-Heavy)
> *"Asymmetric encryption utilizes pairs of mathematically related keys: a public key for encryption generated via elliptic curve or RSA factorization algorithms, and a private key for decryption based on modular arithmetic trapdoor functions..."*
> ❌ *(Completely opaque to anyone without a computer science degree).*

#### ELI10 Protocol Output (Crystal Clear)
> Imagine you have a special **Open Padlock** and a **Secret Key**.
> 
> 1. **The Public Lock**: You make 1,000 copies of your open padlock and hand them out to all your friends. Anyone can take your lock, put a secret letter in a box, and snap the lock shut.
> 2. **The Secret Key**: Once the padlock snaps shut, **only you hold the key** that can unlock it. Even the person who locked the box cannot open it back up.
> 
> This means anyone in the world can safely send you private messages across the internet, without you ever having to mail them your secret key!

---

## Summary Best Practices
- **Ask for a "Physical Analogy"**: Forces the model to anchor in real-world mechanics (water flow, train switches, post offices) rather than abstract math.
- **Use "Smart 10-Year-Old" over "5-Year-Old"**: Avoids silly cartoonish stories while demanding total clarity.
