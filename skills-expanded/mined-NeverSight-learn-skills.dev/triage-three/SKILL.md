---
name: triage-three
description: "This skill should be used when the user asks for adversarial code review, security audit, bug triage, architecture review, or any deep analysis that benefits from multiple perspectives challenging each other. Trigger phrases include: 'triage this', 'find bugs in', 'security audit', 'review this code', 'adversarial review', 'find vulnerabilities', 'audit this for', 'review this PR for correctness'. Uses three adversarial roles (Pusher finds, Challenger questions, Arbiter decides) with style presets (measured, wide-funnel, paranoid, baseline, max-tension)."
---

Adversarial triage with three roles. Argument: $ARGUMENTS

## Overview

Triage-three orchestrates adversarial subagents — Pushers propose, Challengers question, Arbiters decide — to produce high-confidence results through tension.

The core unit is the **Pusher–Challenger pair**: a thesis and its Socratic interrogation. Multiple pairs explore different angles of the same problem. The Arbiter synthesizes across all pairs into verified truth.

For multi-run triage, the **Investor** sits between runs — a fund manager operating under the user's goal as its charter. It analyzes ROI, reallocates effort, and issues a directed investment thesis. Every allocation must trace back to the charter. Runs are controlled capital deployment, not open-ended repetition.

Everything works in threes: three roles, up to three angles, up to three runs.

## Scoring System

Each finding follows a lifecycle: **Proposed → Questioned → Decided**. Every agent has a point ledger that makes trade-offs explicit. State the relevant scoring table in each agent's prompt.

For complete scoring tables (Pusher, Challenger, Arbiter, Investor ledgers, escalation multipliers), consult **`references/scoring.md`**.

## Step 1: Understand & Calibrate

Parse the goal from `$ARGUMENTS`. If empty or unclear, ask using AskUserQuestion.

### Infer Roles Silently

From the goal, determine what the three roles do. Do NOT ask the user to name or confirm them — just proceed.

- [I] Pusher: what to pursue (e.g., "find bugs", "spot security issues", "identify refactoring opportunities")
- [II] Challenger: what to question (e.g., "verify these are real bugs", "challenge severity claims")
- [III] Arbiter: what to decide (e.g., "emit only confirmed issues", "rank by actual impact")

### Calibrate Effort from the Query

Read the goal and reason about the right effort level. Consider:

- **Scope**: A single file → light. A module → standard. A whole system → deep.
- **Stakes**: Quick check → light. Production audit → deep. Security review → deep.
- **Specificity**: "Are there bugs in this function?" → 1 angle. "Review this codebase" → 3 angles.

Derive effort:

| Effort | Angles | Depth | When |
|--------|--------|-------|------|
| **Light** | 1 | surface | Focused question, small scope, low stakes |
| **Standard** | 3 | thorough | Most tasks. Broad enough to catch what matters. |
| **Deep** | 3 | exhaustive | Critical systems, security audits, complex problems |

**Briefly tell the user** the reasoning and chosen effort level before proceeding:

> "This looks like a [light/standard/deep] triage. I'll explore [N] angle(s): [list]. Here's why: [1-sentence rationale]."

If the user pushes back, adjust. Otherwise, proceed. Do NOT present parameter tables or ask the user to pick from systematic options.

### Plan Angles (for Standard/Deep)

When using multiple pairs, identify distinct angles — genuinely different perspectives, not overlapping.

- **Prioritize**: primary angle gets full depth, others get depth−1 (minimum surface).
- Examples: correctness + security + performance, feasibility + impact + risk, logic + edge-cases + API contract.

## Step 2: Determine Scope

Identify what agents will operate on:

- **Code**: Target files/directories. Read them to build context.
- **Documents**: Target docs, specs, PRs.
- **Architecture**: Code + configs + docs together.

Gather context so agents work on concrete material. Do NOT run agents on vague input.

## Step 3: Execute Triage

### Phase [I]–[II]: Pusher–Challenger Pairs

Execution order:
1. Spawn all Pusher agents in parallel (one per angle). Wait for all to complete.
2. Spawn all Challenger agents in parallel, each receiving its paired Pusher's output. Wait for all to complete.
3. Spawn the Arbiter with all Pusher + Challenger outputs.

For complete prompt templates for each role (Pusher, Challenger, Arbiter), consult **`references/prompts.md`**.

#### [I] The Pusher

Select mandate from `style` (default: `measured`):

| Style | Mandate |
|-------|---------|
| `measured` | "Find real issues. Accuracy over quantity. Evidence for each claim." |
| `wide-funnel` / `baseline` | "Find as much as possible. Quantity and depth. Don't self-censor." |
| `paranoid` / `max-tension` | "Assume everything is broken. Find what others would miss." |

Include scoring from `references/scoring.md` (Pusher's Ledger section) in the prompt. Output: numbered findings, each with statement + evidence/location + severity.

#### [II] The Challenger (Socratic)

The Challenger uses **Socratic questioning** — not assertion — to stress-test findings. The Challenger genuinely investigates each question against the source material before reaching a verdict.

Select intensity from `style`:

| Style | Intensity |
|-------|-----------|
| `measured` / `wide-funnel` | Genuine inquiry. Verify together. Benefit of the doubt when evidence is ambiguous. |
| `baseline` | Skeptical cross-examination. Prove it or it's out. |
| `paranoid` / `max-tension` | Hostile interrogation. Wrong until proven right. |

Five Socratic questions per finding:
1. "What specific evidence proves this?"
2. "What would need to be true for this NOT to be an issue?"
3. "Is this the root cause or a symptom?"
4. "What's the alternative explanation?"
5. "Under what real conditions does this matter?"

Verdicts: CONFIRMED, REJECTED, or DISPUTED. Include scoring from `references/scoring.md` (Challenger's Ledger).

### Phase [III]: The Arbiter

After ALL pairs complete, the Arbiter synthesizes across every angle.

Select mandate from `style`:

| Style | Mandate |
|-------|---------|
| `measured` / `baseline` / `max-tension` | "Only verified truth. False positive = heavy penalty. Missing true finding = mild penalty." |
| `wide-funnel` | "Most complete truth. Missing real finding = HEAVY penalty. Borderline inclusion = mild penalty." |
| `paranoid` | "Only PROVABLY TRUE. Any doubt → exclude." |

Rules:
- CONFIRMED by [II]: Include, refine for clarity
- REJECTED by [II]: Exclude UNLESS [II]'s reasoning is itself flawed (verify independently)
- DISPUTED by [II]: Independent judgment against source material
- Cross-angle convergence: If multiple angles flag the same area → higher priority
- Cross-angle conflict: If angles disagree, investigate the discrepancy

Output: verified findings grouped by priority, each with evidence, severity, recommendation. Stats: total → confirmed → rejected → disputed → final.

### Iteration (Investor-directed loop)

If effort is Deep or the user requested multiple runs:

1. **Compute scorecard** — calculate point totals for this run (using the current multiplier). Calculate confirmation rate per angle.
2. **Spawn the Investor** — give it the full scorecard, per-angle ROI breakdown, and verified findings. See `references/prompts.md` for the Investor prompt template.
3. **If Investor says stop** → present final results.
4. **If Investor says continue** → the directive reshapes the next run (new/killed/refocused angles, depth adjustments).
5. **Next run** uses multiplier N+1 (run 2 = 2×, run 3 = 3×). All point values scale.
6. **Feed forward**: Each agent receives the Investor's thesis and their angle's specific focus.

For Investor scoring, charter drift detection, and the complete Investor prompt, consult **`references/scoring.md`** and **`references/prompts.md`**.

## Step 4: Present Results

1. **Verified findings** — the Arbiter's final output
2. **Triage flow** — findings generated → questioned → verified (per angle + total)
3. **Scorecard** — each agent's point total from the scoring system (see `references/scoring.md` for ledger format)
4. **Investment trail** (multi-run only) — Investor's directive after each run
5. **Cross-angle patterns** — what multiple lenses revealed together (if applicable)
6. **Evolution** — if multiple runs, how findings and angles shifted across runs

## Notes

- Each subagent is a fresh Agent tool invocation (general-purpose)
- Launch [I]–[II] pairs in parallel across angles
- Read scoped context ONCE and reuse across all agents
- If a pair produces zero findings, skip it in arbitration
- If a run produces zero findings total, stop early
- Style: pass as `style=X` in arguments; defaults to `measured`
- Available styles: `measured`, `wide-funnel`, `baseline`, `paranoid`, `max-tension`

## Additional Resources

### Reference Files

For detailed scoring and prompt templates, consult:
- **`references/scoring.md`** — Complete scoring tables for all roles, escalation multipliers, Investor ledger, charter drift detection
- **`references/prompts.md`** — Full prompt templates for Pusher, Challenger, Arbiter, and Investor subagents
