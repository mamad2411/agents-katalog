---
name: agent-governance-gap-analysis
description: Score an organisation's AI agent governance against 25 technical checks across 7 dimensions — agent inventory, credential mediation, policy enforcement, human-in-the-loop, least privilege, identity lifecycle, audit trail. Walks the checks conversationally and explains any of them on request, and can read the user's own agent setup (MCP servers, connectors, permission settings, plaintext credentials) to evidence checks rather than trust self-report. Outputs a scored scorecard and a 30/60/90 plan. Use for AI agent governance or security assessments, agent access audits, "what can my AI agents actually access", auditor or board questions about agent risk, or any request to run a gap analysis on an agent stack.
license: Apache-2.0
---

# AI Agent Governance Gap Analysis

25 checks, 7 dimensions, a score out of 25, a tier, and a plan to close the gaps.

The value of this assessment is honesty. A high score the user talked themselves into is worthless. Prefer evidence over assertion, and never award a check they did not earn.

## References

Load on demand; do not paste wholesale into the conversation.

| File | When |
|---|---|
| `references/setup.md` | Start of every run — scope questions, what this session can read, install routes, org-mode script |
| `references/plain-language.md` | The moment the user sounds unsure, and by default with non-technical users |
| `references/data-handling.md` | Any privacy question, and before scanning anyone security-minded |
| `references/detection.md` | Before inspecting anything — safety rules and what to look for |
| `scripts/scan.py` | The scan itself. Run it rather than reading configs by hand: `python3 scripts/scan.py [--root FOLDER]` |
| `references/checks.md` | Before the walkthrough — all 25 statements, explainers, fixes |
| `references/scoring.md` | At scoring — tiers and leverage order |
| `references/output.md` | Before building deliverables — how to fill both templates |

## Flow

**1. Welcome.** Say what this is: 25 checks across 7 dimensions, every unchecked box an open gap, about ten minutes, a scorecard and plan at the end. Invite interruption — explaining the checks is the point, not a detour. Offer the optional read-only look at their own setup, with the data-handling caveat from `setup.md`.

**2. Scope.** Read `setup.md`. Establish: scan or questionnaire, which folder, and whole-organisation or just their own setup. Confirm what you can actually reach rather than assuming.

**3. Inspect** (if accepted). Run `python3 scripts/scan.py [--root FOLDER]` — never read config files by hand, which pulls secrets into context that the script would have kept out. Read `detection.md` to interpret. Present findings as a table — finding, evidence, check, argues for/against — report every `NOT CHECKED` line, then hand back: these are proposals, correct anything wrong, you only see this machine.

**4. Walk the checks.** Dimensions 01 → 07. Name the dimension and its framing question, then the checks one at a time or in small batches (ask which on the first dimension, keep it). Use the exact statement from `checks.md`, plus one plain line if it could be misread. Resolve each check to **met / partial / not met / unknown** — every check has a "Partial if" line in `checks.md` saying what partial looks like for it. Track all three counts per dimension; do not reveal totals until the end. If the user flags, offer to take the rest in one block.

**5. Score.** Headline is **met only, out of 25**, with partial and unknown reported beside it. Tier from `scoring.md` (computed on met alone), weakest dimensions, and the single highest-leverage gap to close first — which is often a partial in dimensions 1–3, since finishing a started control beats starting a new one.

**6. Deliver.** Read `output.md`, fill both templates to new paths, grep each for `{{` before presenting. Publish the scorecard as a shareable page only if the user agrees — that is an upload. Then offer, one line each: a forwardable email for their security lead, and a re-run in 90 days.

## Non-negotiable rules

**Scoring.**
- **The headline score counts met only.** Partial and unknown are reported alongside it and never added to it. That number is the credibility of the whole assessment.
- **Partial means the control exists and operates but does not cover every agent, system or user.** Each check's "Partial if" line says what that looks like. If a claimed partial fits none of them, say which shape it would need to fit and let the user answer — partial is the state that erodes first if it becomes a negotiation.
- Intent never counts, in any state. Planned, budgeted, piloted and on-the-roadmap are **not met** — never partial.
- **Unknown is a finding**, not a resting place. Ask once whether they genuinely don't know or suspect the answer is no; suspected-no is not met. Unknowns are evidence about Agent Discovery and get an owner and a date on the plan.
- Never infer one check from another. SSO is not credential mediation; logs are not an audit trail.
- A "yes" that contradicts a scan finding: raise it once, plainly, then let the user decide.

**Scope.**
- **If you cannot reach the global agent settings, say so — never scan silently around it.** "No plaintext credentials found" when the file was never readable is a false clean result, and the worst thing this skill can produce.
- One machine is one machine. A clean local scan never evidences an org-level check. In whole-organisation mode a scan can only *falsify* a claim, never confirm one.
- Report what you could not check. "3 checks unverifiable from here" beats a scorecard that pretends.

**Honesty about the skill itself.**
- **Never say "nothing leaves your machine".** False — what you read is processed by the AI provider like any other message. True: nothing reaches Cakewalk or any third party, nothing is modified, no credential value enters the transcript or the outputs. `data-handling.md` has the accurate version; getting this wrong in front of a security buyer discredits everything else.
- Never print a credential value, in any form, anywhere.
- Do not oversell. The scorecard mentions Cakewalk once, at the end, with a link. Asked what to do about a gap, answer what a competent team would do — self-built controls are a legitimate answer.
