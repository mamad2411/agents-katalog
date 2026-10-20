---
name: skilldrop-ai-customer-support
description: 8-step guide to building a Claude AI employee for customer support — give it one job, load your return policy, teach it your tone, set guardrails (draft-only, never promise dates), and run real ticket examples. Use when onboarding a team to AI-assisted support or building a customer service automation workflow. Source: @skilldropai carousel.
---

# Build Your First Claude AI Employee for Customer Support

An 8-step framework for creating a scoped, policy-grounded Claude assistant that drafts support replies for human review.

## Core principle

Give it ONE job. Keep the scope narrow enough that the assistant can be genuinely useful without going off-rails.

---

## Step 1 — Define the single job

Open a new Claude chat. Paste this system prompt:

```
You are my returns support assistant.
Draft customer replies using only the rules I provide.
Ask about missing facts.
Keep every reply for my review.
```

Keep all following steps in the same chat session — context builds on itself.

---

## Step 2 — Give it your rules

Paste your return policy verbatim. Example:
```
Returns accepted within 30 days of purchase.
Item must be unused and in original packaging.
Refunds processed within 5 business days.
Exchange or store credit available for items over $100.
```

---

## Step 3 — Teach it your voice

Add two approved reply examples so it learns tone:

> "Thanks for reaching out. Could you share your order number so we can check?"

> "Happy to help. Please confirm whether the item is unused."

**WARM. BRIEF. CLEAR.** Match the tone. Never copy unrelated facts.

---

## Step 4 — Set its boundaries

Explicit constraints to paste in:

```
Never invent a policy or order detail.
Never approve a refund or promise a delivery date.
Flag exceptions for a human decision.
DRAFTS ONLY — I review and send.
```

---

## Step 5 — Give it a real task

Paste an actual customer message and say: "Draft a reply to this."

---

## Step 6 — Make it check the gaps

After the draft, ask: "What information from our policy did you use? What facts were you missing?"

This surfaces uncertainty before the reply goes out.

---

## Step 7 — Get a reply to review

Review for: accuracy against policy, tone match, missing caveats. Edit and send. Log what needed fixing — use that to improve Step 2 over time.

---

## Step 8 — Scale to other jobs

Once returns support is dialled in, repeat the process for a new job:
- **Support**: refunds, exchanges, order status
- **Content**: social captions, product descriptions
- **Research**: competitor monitoring, trend summaries

Each assistant gets its own chat with its own single scope.

---

## What makes this work

- **One job at a time** prevents policy bleed between domains
- **Drafts only** keeps humans in the loop — the assistant earns trust before autonomy expands
- **Policy-grounded** means hallucinated promises don't reach customers

Source: @skilldropai (skilldropai.com)
