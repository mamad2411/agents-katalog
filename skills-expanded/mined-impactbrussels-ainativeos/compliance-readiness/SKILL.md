---
name: compliance-readiness
description: Use when an AI or agent workload is heading into a security review, an enterprise buyer's questionnaire, or an audit and you do not yet know which frameworks you touch. Reach for this when you say "the customer's security team is asking", "do we need SOC 2", "is this HIPAA", "GDPR applies to us right?", "the EU AI Act, are we in scope", "what evidence will the auditor want", "I do not know what we are on the hook for", or before signing an enterprise deal that demands a compliance posture. This is SCOPING, not legal advice: it maps which frameworks apply and what evidence each one commonly demands so you walk in knowing the gaps, then verify with qualified counsel. Produces a framework-scope map, an evidence checklist per framework, and a ranked gap list. Invoke after eval-and-safety-harness, alongside red-team-the-agent.
stage: trust
function: safety
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Compliance Readiness

A security questionnaire lands the week you are trying to close the deal, and you discover what you should have known six months ago. Compliance in an AI workload is not a single gate; it is a map of overlapping frameworks, each demanding its own evidence, and the agent-shaped wrinkles (audit logging, data residency, model-provider subprocessors) are exactly the ones founders miss until an auditor asks. This skill maps the scope so you find the gaps before a reviewer does. It does not replace a qualified compliance professional or a lawyer, and you must verify current requirements with counsel before you act on any of it.

## The method

Map which frameworks the workload touches, list the evidence each demands, then rank the gaps. Full framework: [`references/compliance-scoping.md`](references/compliance-scoping.md). This pairs with `eval-and-safety-harness`: the six pillars (versioned data, audit trail, fallbacks) are the controls compliance asks you to evidence.

### Step 1: Map which frameworks apply

Walk each framework against your workload. "We are probably out of scope" is a guess, not a finding; check the trigger.

| Framework | Commonly applies when (verify) | The agent-specific wrinkle |
|---|---|---|
| SOC 2 | An enterprise buyer requires it before they trust you with their data | Every agent action must land in an audit trail you can produce |
| HIPAA | You touch US protected health information | A model provider handling PHI may need a Business Associate Agreement |
| ISO 27001 | A buyer or region expects a certified ISMS | Information-security controls must cover the AI tooling, not just the app |
| GDPR | You process EU residents' personal data | Data residency, a lawful basis, and subprocessor disclosure for model providers |
| EU AI Act | Your AI system falls in a regulated risk tier | Risk classification and obligations scale with the use case; verify the tier |

Mark each: in scope, out of scope, or unsure. Unsure goes to counsel, not to a guess.

### Step 2: List the evidence each in-scope framework demands

For each in-scope framework, the auditor wants artefacts, not assurances. The per-framework evidence checklists are in the reference. The recurring AI-specific items: an immutable audit log of agent actions; data-residency proof; the list of model-provider subprocessors and their attestations; the human-on-the-loop boundary for consequential decisions; and confirmation that each AI tool is in audit-log scope.

### Step 3: Rank the gaps

Not all gaps block the same door. Rank by what stops a deal or fails an audit first.

| Gap rank | What it is | Action |
|---|---|---|
| Blocker | Stops the deal or fails the audit on day one (no audit trail, no BAA) | Fix before the review |
| Material | Auditor will flag it; deal slips | Fix on the readiness plan |
| Minor | Tidy-up, not blocking | Backlog |

## Output

- A **framework-scope map**: each framework marked in scope / out / unsure, with the trigger noted.
- An **evidence checklist per in-scope framework**: the artefacts an auditor will ask for.
- A **ranked gap list**: blockers, material, minor, each with an owner.
- A written note routing every "unsure" and every requirement to qualified counsel for verification.
- Next: run `red-team-the-agent` to prove the controls hold, and `eval-and-safety-harness` to build the missing pillars.

## Constraints

- This is scoping, not legal advice. It maps what to check; it does not tell you that you comply. Verify every requirement and every scope call with a qualified compliance professional or lawyer before acting.
- Research before asserting: never state a regulatory requirement as settled fact. Frame each as "commonly required, verify current rules", because regulations change and a model's knowledge of them is stale by definition.
- A model provider's compliance is not your compliance. Their certification covers their service, not your use of it; you still own your controls.
- Do not leave logging until an incident. The audit trail is a day-one control, with a human on the loop owning the scope confirmation. No confirmation, no regulated data.
- Stay theme-agnostic; the founder supplies the domain, you supply the map.

## Dictionary

[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl) ·
[audit trail](../../dictionary/06-evaluation-and-safety.md#audit-trail) ·
[verification deficit](../../dictionary/05-failure-modes.md#verification-deficit) ·
[versioned data](../../dictionary/06-evaluation-and-safety.md#versioned-data) ·
[the six-pillar trust substrate](../../dictionary/06-evaluation-and-safety.md#the-six-pillar-trust-substrate)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0). Tag: chat for the scoping map, build for wiring the audit log.

```
Act as a compliance-readiness scout, NOT my lawyer. Map my exposure so I know the gaps before an
auditor or a buyer's security team does. State clearly at the top and the bottom that this is scoping
only, that I must verify every point with a qualified compliance professional or lawyer, and that you
will frame requirements as "commonly required, verify" rather than settled fact.
My product: [ONE_LINER]. Domain: [DOMAIN]. Data it touches: [PROBLEM/data types]. Customers: [ICP].
Model providers and AI tools I use: [list].
1. For SOC 2, HIPAA, ISO 27001, GDPR, and the EU AI Act, tell me for each: likely in scope, out of
   scope, or unsure, and the trigger that decides it. Send every "unsure" to counsel.
2. For each likely-in-scope framework, list the evidence an auditor will ask for, calling out the
   AI-specific ones: an immutable audit log of agent actions, data residency, model-provider
   subprocessors and their attestations, and the human-on-the-loop boundary.
3. Rank my gaps: blocker (fails the audit or kills the deal), material, minor.
Do not reassure me that I am fine. End with the single most likely blocker and the one question I
should take to a qualified professional this week.
```
