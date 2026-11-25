---
name: ai-agent-ux
description: 'Design user experiences for autonomous AI agents that act on behalf of users - control panels, consent flows, action previews, audit trails, and undo mechanisms. Use when: agentic AI, autonomous agents, AI autonomy controls, agent UX, AI actions, computer use, agent consent, agent audit trail.'
---

# AI Agent UX

Design experiences for AI that doesn't just suggest - it acts. Booking flights, sending emails, executing code, making purchases. The AUTONOMY framework ensures users stay in control while AI operates at machine speed.

## Core Principle

Agentic AI inverts the traditional UX model. In classical UX, users take actions and the system responds. In agentic UX, the **system takes actions and users supervise.** This requires an entirely new design vocabulary: previews instead of forms, audit trails instead of history, interrupts instead of navigation.

---

## The AUTONOMY Framework

| Letter | Principle | Design Question |
|---|---|---|
| **A** | Action Preview | Can the user see exactly what the agent will do before it does it? |
| **U** | User Override | Can the user stop, modify, or redirect the agent at any point during execution? |
| **T** | Tiered Authority | Does the agent's freedom scale appropriately with risk level? |
| **O** | Observable State | Can the user see what the agent is doing right now, in real time? |
| **N** | Narrated Reasoning | Does the agent explain why it chose this action over alternatives? |
| **O** | Outcome Verification | Can the user verify that the action completed correctly? |
| **M** | Memory of Actions | Is there a complete, searchable log of everything the agent did? |
| **Y** | Yield to Humans | Does the agent know when to stop and ask for help? |

---

## The Autonomy Dial

Not all actions require the same level of human oversight. Design a graduated control system:

| Level | Name | Agent Behavior | User Involvement | Example |
|---|---|---|---|---|
| 1 | **Suggest** | Recommends action, takes none | User must initiate | "I recommend replying with: [draft]. Send?" |
| 2 | **Draft & Wait** | Prepares the action, pauses for approval | User reviews and approves | Agent drafts email, shows preview, waits for "Send" |
| 3 | **Act & Notify** | Executes immediately, sends notification | User reviews after the fact | Agent files expense report, sends summary |
| 4 | **Act Silently** | Executes without notification | User can check audit log | Agent auto-categorizes emails |
| 5 | **Full Autonomy** | Executes complex multi-step tasks independently | User sets goals, agent reports outcomes | Agent manages a full sales outreach sequence |

### Setting the Default Level

| Risk Factor | Default Autonomy Level |
|---|---|
| Action is reversible + low cost | Level 3-4 (Act & Notify or Silent) |
| Action is irreversible OR high cost | Level 1-2 (Suggest or Draft & Wait) |
| Action involves external parties (sends emails, makes payments) | Level 2 maximum until trust is established |
| Action involves sensitive data | Level 1-2 with audit logging |
| User has explicitly granted higher autonomy | Respect the setting, but cap at the risk level |

**Design rule:** The Autonomy Dial should be a user-facing control, not a hidden system setting. Let users tune their own comfort level.

---

## Pre-Action Design

Before the agent acts, users need to understand what's about to happen.

### The Action Preview Card

Every consequential agent action should display a preview card with:

| Element | Content | Required? |
|---|---|---|
| **Action summary** | One sentence: what the agent will do | Always |
| **Targets affected** | Who or what is impacted (people, systems, data) | Always for external actions |
| **Estimated impact** | What changes as a result | For non-trivial actions |
| **Alternatives considered** | What else the agent could have done | When multiple valid options exist |
| **Reversibility indicator** | Can this be undone? How? | Always |
| **Confidence level** | How sure is the agent this is the right action? | When confidence varies |

---

## During-Action Design

While the agent is executing, users need visibility and control.

### The Agent Activity Feed

A real-time, scrollable feed showing:

| Component | Purpose | Update Frequency |
|---|---|---|
| **Current step indicator** | "Step 3 of 7: Sending confirmation email" | Per step |
| **Progress visualization** | Linear or branching progress bar | Continuous |
| **Decision log** | "Chose option A because [reason]" | Per decision point |
| **Pause/stop controls** | Always visible, always responsive | Permanent |
| **Skip/redirect** | "Skip this step" or "Do X instead" | Per step |

**Critical rule:** The stop button must work instantly. If the agent can't be stopped mid-action, the UI must make this clear BEFORE the action begins.

---

## Post-Action Design

### The Action Receipt

After every consequential action, provide an action receipt:

| Element | Content |
|---|---|
| **What was done** | Plain-language summary of completed actions |
| **What changed** | Before/after diff of affected data |
| **Undo option** | One-click reversal if action is reversible |
| **Time-limited undo** | For partially reversible actions: "You have 30 seconds to undo the email send" |
| **Audit link** | "View full activity log" |

### The Undo Architecture

| Action Type | Undo Pattern | Time Window |
|---|---|---|
| Data modification | Full revert to previous state | Unlimited |
| Message sent | Recall + replacement option | 30 seconds to 5 minutes |
| File deletion | Soft delete → permanent after 30 days | 30 days |
| Purchase/payment | Cancellation request + refund flow | Varies by provider |
| Multi-step sequence | Step-by-step rollback with checkpoint selection | Per step |
| Irreversible action | Prevention-only (no undo, must block before execution) | N/A |

---

## Trust Ramp: Progressive Autonomy

New agents should not start at Level 5. Build trust incrementally.

### The Trust Ramp Pattern

| Phase | Duration | Autonomy Level | Unlock Condition |
|---|---|---|---|
| **Onboarding** | First 5 interactions | Level 1 (Suggest only) | User completes first review cycle |
| **Building** | Next 20 interactions | Level 2 (Draft & Wait) | >80% approval rate on previews |
| **Established** | Ongoing | Level 3 (Act & Notify) | User explicitly opts in |
| **Trusted** | After sustained use | Level 4 (Act Silently) | User configures specific action types |
| **Delegated** | Expert users only | Level 5 (Full Autonomy) | User sets goals + boundary conditions |

**The cardinal rule:** Users can always dial DOWN autonomy instantly. Dialing UP requires confirmation.

---

## Multi-Agent Coordination UX

When multiple agents work together:

| Challenge | Design Solution |
|---|---|
| Which agent did what? | Color-coded agent identity in the activity feed |
| Agents disagree on approach | Surface the disagreement to the user with each agent's reasoning |
| Agent A's output feeds Agent B | Show the handoff explicitly: "Research Agent found 5 candidates → Outreach Agent will draft emails for your review" |
| Cascading failures | If Agent A fails, halt Agent B and notify user before damage propagates |

---

## Anti-Patterns

| Pattern | Why It Fails |
|---|---|
| "The AI will handle everything" messaging | Sets unrealistic expectations; users feel betrayed at first failure |
| Burying the stop button | Users feel trapped. Panic → permanent distrust |
| Asking permission for every micro-action | Decision fatigue. Users disable the agent entirely |
| No audit trail | "What did it do while I was asleep?" Users can't trust what they can't verify |
| Irreversible actions without explicit consent | One wrong autonomous action and the user never delegates again |
| Showing agent "thinking" animation without substance | A spinner is not transparency. Show what the agent is actually evaluating |

---

## Quick Reference

| Task | Framework Element | Key Deliverable |
|---|---|---|
| Design a new AI agent product | Full AUTONOMY framework | Autonomy Dial settings + Pre/During/Post action flows |
| Add agent capabilities to existing product | Trust Ramp Pattern | Phased rollout plan with unlock conditions |
| Audit agent UX for safety | Undo Architecture + Action Receipt | Gap analysis: which actions lack undo, preview, or audit? |
| Design multi-agent coordination | Multi-Agent Coordination table | Agent identity system + handoff visualization |
| Set autonomy defaults | Setting the Default Level table | Risk-matched autonomy levels per action type |

## Integration

Works with: `ai-trust-transparency` (explaining agent decisions), `ai-error-resilience` (agent failure recovery), `ai-safety-guardrails` (agent action boundaries), `ai-feedback-loops` (rating agent performance), `ai-ux-eval` (scores the predictability dimension).
