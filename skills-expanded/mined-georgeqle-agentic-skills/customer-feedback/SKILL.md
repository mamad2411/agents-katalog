---
name: customer-feedback
description: Ingest and synthesize customer feedback — categorize findings against ICP and journey map, maintain a running log
type: research
version: v0.8
argument-hint: "[file path, pasted text, or empty to be prompted]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Customer Feedback — Ingest & Synthesize

Invoke as `$customer-feedback`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Soft Prerequisites

- Read `research/icp.md` (or `research/{slug}/icp.md` in product-path mode) if it exists — grounds categorization in ICP segments and pain points.
- Read `research/journey-map.md` (or `research/{slug}/journey-map.md` in product-path mode) if it exists — tags findings to journey stages.

These are not required. The skill works without them but categorization will be less precise.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Context

- Read `research/icp.md` (or `research/{slug}/icp.md`) if it exists — extract ICP segments, user profiles, pain points, value props
- Read `research/journey-map.md` (or `research/{slug}/journey-map.md`) if it exists — extract journey stages, use cases, critical moments
- Read `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) if it exists — load all previous sessions for synthesis context

### 2. Ingest Feedback

Check `$ARGUMENTS`:
- **File path provided**: Read the file and use its contents as the feedback input
- **Text provided**: Use the argument text directly as feedback
- **Empty**: Ask the user to paste or describe the feedback. If the session is already in Plan mode and there are 2-3 concrete input-source choices, prefer `request_user_input`; otherwise ask in plain text.

Accept any format: interview notes, support tickets, survey responses, NPS comments, user testing observations, sales call notes, social media mentions, app store reviews.

### 3. Categorize Findings

For each distinct finding in the feedback:

1. **Classification**: One of:
   - **Confirmed** — validates an existing ICP assumption, pain point, or journey step
   - **Wrong** — contradicts an ICP assumption, pain point, or mapped journey
   - **New** — reveals something not captured in ICP or journey map

2. **ICP Tag** (when `research/icp.md` exists): Which ICP section does this relate to? (pain point, value prop, user profile, trigger event, etc.)

3. **Journey Stage** (when `research/journey-map.md` exists): Which journey stage does this touch? (discovery, evaluation, onboarding, aha moment, retention, etc.)

4. **Severity**: High / Medium / Low — based on how many users it affects and how strongly

5. **Quote or Evidence**: The specific words or behavior that support this finding

### 4. Present & Validate

Present the categorized findings to the user. If the session is already in Plan mode and there are 2-3 concrete validation choices, prefer `request_user_input`; otherwise ask in plain text:

- Show each finding with its classification, tags, and evidence
- Ask: "Does this categorization look right? Any findings I've miscategorized or missed?"
- If the user corrects anything, update before writing

### 5. Check Staleness Triggers

Count the number of **Wrong** and **New** findings across ALL sessions (including previous ones):

- If 3+ **Wrong** findings relate to ICP assumptions: recommend re-running `$customer-discovery`
- If 3+ **Wrong** findings relate to journey stages: recommend re-running `$journey-map`
- If 3+ **New** findings suggest an unserved segment: recommend re-running `$customer-discovery`

Display these recommendations after the categorized findings.

### 6. Populate Next Steps

Before writing, check which files exist and synthesis results to populate the `## Next Steps` section contextually. Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2–4 alternatives). Use this format in the output:

### Next Steps

**Recommended:** [recommended skill] — [one-line reason why this is the highest-impact next action given current state]

Other options:
- `$skill` — [description]
- ...

**Recommendation priority** (first applicable becomes the recommendation):
1. IF downstream impact is **Major**: recommend `$reconcile-research` — [N] conflicts found in downstream docs need resolution before other work
2. IF staleness alert for ICP: recommend `$customer-discovery` — feedback has invalidated key ICP assumptions that other research depends on
3. IF staleness alert for journey map: recommend `$journey-map` — real user behavior differs from mapped experience
4. IF 3+ New findings: recommend `$brainstorm` — newly revealed customer needs deserve solution exploration
5. IF no staleness alerts and no major findings: recommend `$research-roadmap` — check overall project status for the next priority

**Other options** (include all applicable items not chosen as recommended):
- IF staleness alert for ICP: `$customer-discovery` — Re-run discovery — feedback has invalidated key assumptions
- IF staleness alert for journey map: `$journey-map` — Re-map journeys — real behavior differs from mapped experience
- IF 3+ New findings: `$brainstorm` — Generate ideas for newly revealed customer needs
- IF New findings relate to a gap: `$ux-variations [topic]` — Explore UX solutions for the most impactful finding
- IF no staleness alerts: `$research-roadmap` — Check overall project status
- IF feedback came from experiment results: `$assumption-tracker` — Update assumption validation status with experiment findings
- IF 3+ research docs exist and no `research/assumption-tracker.md`: `$assumption-tracker` — Build the assumptions register to track what feedback is validating

**Impact-aware adjustments:**
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"
- If downstream impact has not been classified yet, run the downstream impact check against the proposed output before selecting the final recommendation. Do not emit a Minor/Major impact recommendation speculatively.

### 7. Write Output

Only after the user validates, write to `research/customer-feedback.md`:

**If the file doesn't exist**: Create it with the structure below.
**If the file exists**: Append the new session section, then regenerate the `## Synthesis` section at the top.

### 8. Downstream Impact Check

After writing, check for downstream research documents that may be affected by what was just decided. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/gtm.md`
- `research/monetization.md`

For each existing downstream document:
1. Read it — focus on `> Based on:` header, `## Summary`, and sections that reference concepts this skill just defined or changed
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - Customer language or pain point framing in GTM messaging that feedback has invalidated
   - Pricing assumptions in monetization anchored to customer willingness-to-pay signals that have shifted
   - Channel strategy built on customer behavior patterns that new feedback contradicts
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed — e.g., primary pain point invalidated, willingness-to-pay signals contradicted, key customer behavior pattern disproved): Display conflicts and strongly recommend `$reconcile-research`.

Display to the user after showing the written file confirmation. This should be quick — one read per downstream doc, scan for conflicts against key decisions. Not a deep reconciliation.

## Output

### `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`)

```markdown
# Customer Feedback

> Last updated: [current date]
> Sessions: [total count]

## Synthesis

[Regenerated each run. Summarizes patterns across ALL sessions:]

### Confirmed Assumptions
[ICP and journey assumptions that feedback consistently validates]

### Invalidated Assumptions
[ICP and journey assumptions that feedback contradicts — with evidence count]

### New Discoveries
[Findings not captured in any existing research — potential ICP updates or new journey stages]

### Staleness Alerts
[If 3+ Wrong/New findings accumulated, list which research docs should be re-run and why]

<!-- Only include the Downstream Impact section when impact is Minor or Major. Omit entirely for None. -->
### Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

#### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote from downstream doc]"
   - **Now**: [what this skill's output says instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

### Next Steps

**Recommended:** `$skill` — [one-line reason]

Other options:
- [conditional items from step 6 — only include items whose conditions are met]

---

## Feedback Session: [date]

> Source: [file path, "pasted text", or "interview"]
> ICP context: [yes/no — whether research/icp.md was loaded]
> Journey context: [yes/no — whether research/journey-map.md was loaded]

### Findings

| # | Finding | Classification | ICP Tag | Journey Stage | Severity |
|---|---------|---------------|---------|---------------|----------|
| 1 | [finding] | Confirmed/Wrong/New | [tag] | [stage] | H/M/L |

### Details

#### Finding 1: [title]
**Classification**: [Confirmed/Wrong/New]
**Evidence**: "[quote or observation]"
**ICP Tag**: [which ICP section]
**Journey Stage**: [which stage]
**Severity**: [High/Medium/Low]
**Implication**: [what this means for the product]

[Repeat for each finding]

---

[Previous sessions remain below, newest first]
```

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Append-only.** Never delete or overwrite previous sessions in `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`). Only the `## Synthesis` section at the top is regenerated.
- **Present before writing.** Never write until the user validates the categorization.
- **Tag to existing research.** When ICP and journey map exist, every finding must be tagged. When they don't exist, skip tagging but note "no ICP/journey context" in the session header.
- **Count across sessions.** Staleness triggers are based on cumulative findings, not just the current session.
- **Accept any format.** The skill should handle messy, unstructured input gracefully.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/customer-feedback-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
