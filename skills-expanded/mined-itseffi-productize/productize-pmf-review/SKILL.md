---
name: productize-pmf-review
description: >-
  Product-market fit gate between the 0-1 build loop and the grow playbook. Use to decide
  whether evidence supports PMF, signal-but-not-PMF, or no-PMF, and to route to grow, iterate,
  or pivot/kill.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# PMF Review

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

- **Skill**: `pmf-review`
- **Lifecycle**: Measure
- **Category**: Strategy
- **Primary artifact**: PMF review with cohort, evidence map, mode, super-user definition, counter-evidence, decision, and next gate

Use this gate at the handoff from `$0-1` Move 7 (Ship + Learn) to `$grow`. It
decides whether the evidence supports product-market fit, only a partial signal,
or no fit at all, and routes the next playbook move accordingly.

This is not a metrics dashboard. It is a forced decision: **PMF**,
**signal-but-not-PMF**, or **no-PMF** — followed by an explicit route to grow,
another 0-1 lap, or pivot/kill.

## Pre-Review Audit

Before judging fit:

1. Read shipped behavior, prior 0-1 artifacts, eval results, retention data,
   user interviews, support tickets, NPS, and any churn diagnostics.
2. Identify the cohort being judged. PMF is segment-specific; do not aggregate
   the beachhead with tourist cohorts.
3. Separate **demand-side evidence** (pull, retention, word-of-mouth) from
   **supply-side activity** (signups, demos, content reach).
4. Flag stale artifacts: any retention curve, survey, or cohort that predates
   the last material product change is stale.
5. Name the blocked decision in one sentence: "Should we move to `$grow`, run
   another 0-1 lap, or pivot/kill?"

## Mode Selection

Choose one mode and state why:

- **PMF**: super-user cohort, flat retention curve, organic pull, and survey
  signal all align. Route to `$grow`.
- **Signal-But-Not-PMF**: a real user pocket loves it, but retention bends or
  super-user cohort is too narrow to grow on. Route to another `$0-1` lap with
  a sharpened wedge.
- **No-PMF**: retention decays, no super-users, no organic pull. Route to
  `$thesis-review` for pivot/kill decision.
- **Too-Early**: insufficient evidence to call any of the above; specify the
  minimum data the next lap must produce.

## Review Passes

### 1. Sean Ellis Super-User Test

- Of users who experienced the core capability ≥2 times in the last 2 weeks,
  what percent would be "very disappointed" if they could no longer use it?
- If ≥40% → strong PMF signal; if 25-40% → signal-but-not-PMF; if <25% → no-PMF.
- If survey data is missing, identify the cheapest path to collect it before
  ruling.

### 2. Retention Curve

- Does the retention curve **flatten** at a non-trivial baseline, or does it
  **decay** to zero?
- Compare super-user cohort retention to overall cohort retention. PMF lives
  in the super-user curve, not the average.
- Flag if the retention window is too short to call shape (e.g., 2 weeks for
  a monthly-use product).

### 3. Super-User Cohort

- Who are the super-users? Name the segment, job, and trigger.
- Does the super-user segment match the original beachhead, or has the wedge
  moved?
- Is the super-user pocket large enough to grow on, or is it a niche that caps
  the bet?

### 4. Organic Pull

- Word-of-mouth signal: do users invite, recommend, or refer without prompting?
- Inbound demand: are leads asking for the product without acquisition spend?
- Switching pressure: do super-users describe a "before/after" change in
  workflow?

### 5. Friction And Churn

- What stops non-super-users from becoming super-users? Onboarding, value
  clarity, missing capability, or segment mismatch?
- What causes super-users to churn when they do?
- Distinguish **wrong-fit churn** (segment mismatch) from **product churn**
  (fixable in the next lap).

### 6. Counter-Evidence

- What would change a PMF call to no-PMF? List the disconfirming signals.
- What would change a no-PMF call to PMF? List the missing evidence.
- If both lists are short, the data is too thin to call; mark Too-Early.

## Decision Protocol

For each substantive signal:

- State the signal and its source (cohort, survey, retention window, interview).
- Name the cohort it applies to. Do not generalize across segments.
- Offer the smallest decision the signal supports.
- If the signal is mixed, hold the call and specify the next test.

Never declare PMF on activity metrics alone (signups, demos, reach). PMF
requires demand-side pull.

## Route Internally

- `$product-market-fit-cycle`
- `$aarrr-growth-diagnostics`
- `$cohort-analysis`
- `$churn-reduction-from-customer-data-and-exit-survey-analysis`
- `$ideal-customer-profile-icp-representative-for-x-product`
- `$beachhead-segment`
- `$post-launch-feedback-loop`
- `$metric-drops-diagnosis-with-rigorous-stepwise-decomposition`

## Required Output

Return:

1. **Cohort Under Review**: segment, size, time window, and product version.
2. **Evidence Map**: super-user survey result, retention curve shape, organic
   pull signals, churn pattern. Mark stale and missing data.
3. **Mode**: PMF, Signal-But-Not-PMF, No-PMF, or Too-Early. State why.
4. **Super-User Definition**: who, what trigger, what value, segment match to
   original beachhead.
5. **Counter-Evidence**: signals that would flip the call.
6. **Decision**: route to `$grow`, another `$0-1` lap (with sharpened wedge),
   or `$thesis-review` for pivot/kill.
7. **Next Gate**: which reviewer fires next; what data the next lap must
   produce if the call is Too-Early.
8. **Completion Summary**: status, confidence, unresolved decisions, and what
   would change your mind.
