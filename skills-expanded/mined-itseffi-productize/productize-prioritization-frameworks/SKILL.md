---
name: productize-prioritization-frameworks
description: >-
  Prioritization Frameworks. Use when selecting or comparing prioritization frameworks such as
  RICE, ICE, Kano, MoSCoW, Opportunity Score, cost of delay, or impact-effort.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Prioritization Frameworks

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `prioritization-frameworks`
- **Lifecycle**: Plan
- **Category**: Delivery
- **Primary artifact**: Prioritization framework recommendation with scoring template and decision rationale

Use when selecting or comparing prioritization frameworks such as RICE, ICE, Kano, MoSCoW, Opportunity Score, cost of delay, or impact-effort.

## Productize Contract

- **Primary lifecycle**: Plan
- **Supporting lifecycle**: none
- **Primary artifact**: Prioritization framework recommendation with scoring template and decision rationale
- **Source method**: pm-skills-main/pm-execution/skills/prioritization-frameworks/SKILL.md

## Method

## Prioritization Frameworks Reference

A reference guide to help you select and apply the right prioritization framework for your context.

### Core Principle

Never allow customers to design solutions. Prioritize **problems (opportunities)**, not features.

### Opportunity Score (Dan Olsen, *The Lean Product Playbook*)

The recommended framework for prioritizing customer problems.

Survey customers on **Importance** and **Satisfaction** for each need (normalize to 0-1 scale).

Three related formulas:
- **Current value** = Importance x Satisfaction
- **Opportunity Score** = Importance x (1  Satisfaction)
- **Customer value created** = Importance x (S2  S1), where S1 = satisfaction before, S2 = satisfaction after

High Importance + low Satisfaction = highest Opportunity Score = best opportunities. Plot on an Importance vs Satisfaction chart -- upper-left quadrant is the sweet spot. Prioritizes customer problems, not solutions.

### ICE Framework

Useful for prioritizing initiatives and ideas. Considers not only value but also risk and economic factors.

- **I** (Impact) = Opportunity Score x Number of Customers affected
- **C** (Confidence) = How confident are we? (1-10). Accounts for risk.
- **E** (Ease) = How easy is it to implement? (1-10). Accounts for economic factors.

**Score** = I x C x E. Higher = prioritize first.

### RICE Framework

Splits ICE's Impact into two separate factors. Useful for larger teams that need more granularity.

- **R** (Reach) = Number of customers affected
- **I** (Impact) = Opportunity Score (value per customer)
- **C** (Confidence) = How confident are we? (0-100%)
- **E** (Effort) = How much effort to implement? (person-months)

**Score** = (R x I x C) / E

### 9 Frameworks Overview

| Framework | Best For | Key Insight |
|-----------|----------|-------------|
| Eisenhower Matrix | Personal tasks | Urgent vs Important -- for individual PM task management |
| Impact vs Effort | Tasks/initiatives | Simple 2x2 -- quick triage, not rigorous for strategic decisions |
| Risk vs Reward | Initiatives | Like Impact vs Effort but accounts for uncertainty |
| **Opportunity Score** | Customer problems | **Recommended.** Importance x (1  Satisfaction). Normalize to 0-1. |
| Kano Model | Understanding expectations | Must-be, Performance, Attractive, Indifferent, Reverse. For understanding, not prioritizing. |
| Weighted Decision Matrix | Multi-factor decisions | Assign weights to criteria, score each option. Useful for stakeholder buy-in. |
| **ICE** | Ideas/initiatives | Impact x Confidence x Ease. Recommended for quick prioritization. |
| **RICE** | Ideas at scale | (Reach x Impact x Confidence) / Effort. Adds Reach to ICE. |
| MoSCoW | Requirements | Must/Should/Could/Won't. Caution: project management origin. |

### Templates

- [Opportunity Score intro (PDF)](https://drive.google.com/file/d/1ENbYPmk1i1AKO7UnfyTuULL5GucTVufW/view)
- [Importance vs Satisfaction Template -- Dan Olsen (Google Slides)](https://docs.google.com/presentation/d/1jg-LuF_3QHsf6f1nE1f98i4C0aulnRNMOO1jftgti8M/edit#slide=id.g796641d975_0_3)
- [ICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1LUfnsPolhZgm7X2oij-7EUe0CJT-Dwr-/edit?usp=share_link&ouid=111307342557889008106&rtpof=true&sd=true)
- [RICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1S-6QpyOz5MCrV7B67LUWdZkAzn38Eahv/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### Further Reading

- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)

## Productize Output Rules

- Produce the artifact named in the Productize contract, not a generic framework summary.
- Separate known facts, assumptions, missing evidence, and risky leaps before recommending.
- Convert uncertain claims into validation steps, metrics, owner decisions, or launch/readout checks.
- If this reference method conflicts with Productize evidence standards, keep the Productize standard.
