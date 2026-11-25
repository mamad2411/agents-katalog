---
name: avoid-rephrasing-good-text
description: "Edit awkward or incorrect passages while preserving wording, voice, and humor that already work."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["surgical-editing", "copywriting", "authenticity", "spot-fixing", "voice-preservation", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Don't Rewrite Text That Works (Surgical Spot-Fixing) (AI Skill)

## Overview
When an email, essay, or sales page is already 90% strong, users often make the mistake of pasting the entire text with the prompt: *"Rewrite this to make it better."* 

The AI will predictably strip out your authentic human voice, flatten personal humor, introduce corporate clichés, and rewrite sections that were already working perfectly.

This skill introduces **Surgical Spot-Fixing**: prompting methods to isolate and refine only the single awkward sentence or paragraph while preserving 100% of the surrounding voice and context.

---

## Full Rewrite Flattening vs. Surgical Fixing

```
┌─────────────────────────────────────────────────────────────┐
│                 The "Surgical Fix" Advantage                │
│                                                             │
│  Full Rewrite ("Make this email better"):                   │
│  • Destroys authentic human personality                     │
│  • Introduces corporate filler ("I hope this finds you...") │
│  • Changes points that were already legally or factually set│
│                                                             │
│  Surgical Fix ("Fix only sentence 3 for clarity"):          │
│  • Keeps 95% of your original draft untouched               │
│  • Retains natural conversational rapport                   │
│  • Takes 5 seconds to review and send                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Surgical Spot-Fixing Prompts

### Pattern 1: The Single-Sentence Surgeon
Paste only the problematic sentence along with 1 line of context:

```markdown
I wrote this sentence for an email to a client, but it feels clumsy and defensive:
"[PASTE AWKWARD SENTENCE]"

Give me 3 alternate ways to rephrase ONLY this sentence:
1. Direct & confident
2. Warm & collaborative
3. Ultra-concise (under 10 words)

Do not rewrite the rest of my email.
```

---

### Pattern 2: The "Preserve Everything Else" Directive
When pasting a full paragraph for contextual flow:

```markdown
Here is a paragraph from my article:
"[PASTE PARAGRAPH]"

Task:
- Fix the transition between sentence 2 and sentence 3.
- DO NOT alter the vocabulary, tone, or structure of the rest of the text.
- Output ONLY the revised sentence with the new transition.
```

---

## Real-World Case Study

### Scenario: Replying to a Pricing Objection

#### Your Original Draft (90% Great, 1 Clumsy Sentence)
> *"Hey Sarah, thanks for the feedback on the proposal. We'd love to work with you on the Q3 redesign. Unfortunately, we can't lower our hourly rate because our team is very experienced and we have high standards, but we could trim the project scope to fit your $15k budget. Let me know what you think!"*
>
> *(Sentence 3 feels defensive and slightly passive-aggressive).*

#### The Catastrophic "Full Rewrite"
> **Prompt**: *"Rewrite this email to make it professional."*
>
> ❌ *AI Output: "Dear Sarah, Thank you for your valuable feedback regarding our proposal. We are thrilled at the prospect of collaborating on the Q3 redesign initiative. Regarding pricing, please be advised that our rates reflect our paramount commitment to industry-leading excellence..."* (Robotic, cold, and ruins the personal relationship).

#### The Surgical Spot-Fix Prompt & Result
> **Prompt**: *"Give me 3 friendly ways to rephrase 'Unfortunately, we can't lower our hourly rate because our team is very experienced...'"*

**AI Response**:
1. *"While our standard rates are fixed, we can easily adjust the feature scope so the project lands right at your $15k target."*
2. *"We can't discount our hourly rate, but we can phase the roadmap to keep the initial launch under $15k."*
3. *"Our rates are set, but I'm confident we can tailor the deliverables to fit comfortably within your $15k budget."*

---

## The Golden Rule of AI Editing
> **"Never send an entire document to an AI if only one paragraph is broken. Fix the sentence, keep the voice."**
