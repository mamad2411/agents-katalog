---
name: hook-model
type: research
version: v0.8
description: Nir Eyal engagement loop design — trigger, action, variable reward, investment
argument-hint: "[optional: specific engagement loop or user behavior to focus on]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Hook Model — Engagement Loop Design

Invoke as `$hook-model`.

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

## Prerequisites

- **Hard**: `research/journey-map.md` (or `research/{slug}/journey-map.md`) must exist. If not, tell the user to run `$journey-map` first and stop.
- **Soft**: Read these if they exist:
  - `research/icp.md` — emotional pains, motivations, user psychology
  - `research/competitive-analysis.md` — competitor engagement mechanics, retention strategies

## Process

### 0a. Product Path Manifest

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the hook model to the active product path by default.

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

- Read `research/journey-map.md` — retention stages, habit opportunities, critical moments, aha moments, drop-off points
- Read `research/icp.md` if it exists — emotional pains, motivations, trigger events, daily routines
- Read `research/competitive-analysis.md` if it exists — competitor engagement mechanics, retention strategies, habit loops
- Read CLAUDE.md, README, and key source files for product context

### 2. Applicability Check

Detect product type from context. Evaluate whether habit-loop design is appropriate:

- **Usage frequency**: Is the product used daily/weekly, or monthly/quarterly?
- **User type**: Consumer, prosumer, SMB, or enterprise?
- **Sales cycle**: Self-serve or long sales cycle with procurement?
- **Consumer-facing component**: Does the product have end-user engagement, or is it infrastructure/back-office?

IF the product is B2B/enterprise with long sales cycles, infrequent usage, or no consumer-facing component:

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "This appears to be a B2B/enterprise product where habit loops may not apply. Usage is [infrequent/transactional/procurement-driven]. Would you like to skip to `$metrics` instead, or continue with hook model design for specific engagement patterns?"

If user chooses skip, recommend `$metrics` and stop.

### 3. Research Hook Patterns

Use WebSearch with **4-6 targeted queries**:

1. **Hook model domain examples** — "hook model [domain] examples"
2. **Nir Eyal category applications** — "Nir Eyal hooked [category]"
3. **Habit-forming product design** — "habit forming [product type] design"
4. **Variable reward types** — "variable reward types [category]"
5. **Engagement loop patterns** — "engagement loops [domain]"
6. **Competitor engagement mechanics** — "[competitor] engagement mechanics"

### 4. Design Hook Loops

For each distinct user behavior that should become habitual, design the full hook:

**External Triggers** (from journey discovery/acquisition stages):
- Notifications, emails, social prompts, content, integrations
- Map to specific journey touchpoints where the trigger fires

**Internal Triggers** (from ICP emotional pains):
- Boredom, anxiety, FOMO, uncertainty, loneliness, incompleteness
- The emotional state that precedes the habitual action
- Must connect to real ICP pain data, not assumptions

**Action** (the simplest behavior in anticipation of reward):
- Must be easier than the thought — lower friction than NOT doing it
- Follows Fogg Behavior Model: Motivation + Ability + Trigger = Behavior
- Identify friction points and how to minimize them

**Variable Reward** (classify each):
- **Tribe** — social validation, acceptance, belonging, status among peers
- **Hunt** — material resources, information, deals, search for relevant content
- **Self** — mastery, completion, competence, consistency, self-improvement

**Investment** (user puts something in that loads the next trigger):
- Data, content, followers, reputation, skill, preferences, history
- Each investment should make the next cycle more valuable AND more likely

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here are the hook loops I've designed. Which triggers feel forced, which actions are too complex, and which rewards don't match your users' real motivations?"

### 5. Map Multiple Hooks

If the product has distinct engagement loops (e.g., creation loop vs. consumption loop, social loop vs. productivity loop):

1. Design each loop separately with the full 4-component structure
2. Identify reinforcement points — where one loop feeds into another
3. Map the hook interaction pattern — which loops are primary vs. supporting
4. Identify the "gateway hook" — the first loop new users enter

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Do these loops capture the core behaviors you want to be habitual? Any missing loops or interactions between them?"

### 6. Populate Next Steps

Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2-4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** `$metrics` — define engagement and retention metrics grounded in these hook loops

Other options:
- `$roadmap` — Sequence the highest-priority engagement mechanism into the roadmap
- IF no `research/monetization.md`: `$monetization` — Hook loops inform monetization timing — when to convert habitual users

### 7. Write Output

Only after the user confirms, write the output files.

Create the `research/` directory if it doesn't exist.

### 8. Downstream Impact Check

After writing, check for downstream research documents that may be affected.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/metrics.md`
- `research/monetization.md`

For each existing downstream document:
1. Read it — focus on engagement metrics, retention definitions, conversion triggers
2. Identify conflicts where metrics or monetization assumptions don't align with the designed hook loops
3. Note each conflict: file, section, stale claim, what it should now say

**Classify the impact**:
- **None**: No downstream docs exist, or no conflicts. Skip display.
- **Minor** (1-2 small conflicts): Display inline.
- **Major** (3+ conflicts OR primary hook loop changed, reward type shifted, trigger mechanism redesigned): Display and recommend `$reconcile-research`.

## Output

### `research/hook-model.md` (or `research/{slug}/hook-model.md`)

```markdown
# Hook Model — Engagement Loop Design

> Based on: research/journey-map.md[, research/icp.md, research/competitive-analysis.md]
> Date: [current date]
> Methodology: Hook Model (Nir Eyal, "Hooked")
> Applicability: [Consumer / PLG / B2B with consumer component / Limited — see assessment]

## Summary
[2-3 sentences: the engagement thesis — what behaviors should become habitual, why they matter for retention, and how the hooks reinforce each other]

## Applicability Assessment

**Product type**: [Consumer / PLG / B2B / Marketplace / etc.]
**Expected usage frequency**: [Daily / Weekly / Event-driven / etc.]
**Habit potential rating**: [High / Medium / Low]
**Rationale**: [Why this product is or isn't a strong candidate for habit-loop design]

## Hook Loop 1: [Behavior Name]

> Target behavior: [the specific action that should become habitual]
> Frequency target: [how often this should occur]

### Trigger

**External Triggers** (acquisition/re-engagement):
| Trigger Type | Channel | Journey Stage | Evidence |
|-------------|---------|---------------|----------|
| [type] | [email/push/social/etc.] | [discovery/onboarding/retention] | [source] |

**Internal Trigger** (emotional state):
- **Emotion**: [the feeling that precedes the action]
- **Context**: [when/where this emotion arises]
- **Evidence**: [from ICP data — not assumed]

### Action

**The behavior**: [simplest action in anticipation of reward]
**Motivation**: [why the user is motivated in this moment]
**Ability**: [why this is easy enough — fewer steps than the thought]
**Current friction**: [what makes this harder than it should be]
**Friction reduction**: [how to make the action effortless]

### Variable Reward

**Type**: [Tribe / Hunt / Self]
**The reward**: [what the user gets]
**Why it's variable**: [what changes each time — unpredictability]
**Evidence**: [why this reward matches real user motivations]

### Investment

**What the user stores**: [data / content / followers / reputation / skill / preferences]
**How it loads the next trigger**: [why this investment makes the next cycle more likely]
**Compounding effect**: [how the investment makes the product more valuable over time]

## Hook Loop 2: [Behavior Name]
[Same structure as Hook Loop 1]

## Hook Interaction Map

[How the loops reinforce each other — which loop feeds into which, what the gateway hook is for new users]

| Loop | Feeds Into | Mechanism |
|------|-----------|-----------|
| [loop name] | [loop name] | [how one loop's investment/reward triggers the other] |

**Gateway hook**: [the first loop new users enter]
**Reinforcement pattern**: [how loops compound — e.g., creation feeds consumption which feeds social which feeds creation]

## Engagement Risk Assessment

### Ethical Considerations
- [Risk 1: potential for manipulation or dark pattern]
- [Risk 2: potential for addictive behavior without genuine value]

### Dark Pattern Avoidance
- [Guideline 1: how to keep engagement genuine]
- [Guideline 2: how to ensure user control and transparency]

### Value Alignment
- [How each hook loop delivers genuine user value, not just engagement metrics]

## Strategic Implications

### For Product
[What to build to strengthen the hooks — feature priorities, friction reduction, reward design]

### For Metrics
[What to measure — trigger response rates, action completion, reward satisfaction, investment depth]

### For Growth
[How hooks create organic growth — virality through social triggers, investment-driven retention]

<!-- Only include when downstream impact is Minor or Major -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote]"
   - **Now**: [what hook model says instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

**Recommended:** `$metrics` — define engagement and retention metrics grounded in these hook loops

Other options:
- [conditional items from step 6]
```

### `research/hook-model-search-log.md` (or `research/{slug}/hook-model-search-log.md`)
Raw research log — queries, findings, evidence for each hook design decision.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stays in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires journey map.** Hooks without journey context are disconnected from reality.
- **Evidence-grounded.** Triggers and rewards must connect to ICP data and journey insights — not wishful thinking.
- **Ethical awareness.** Flag potential dark patterns. Design for genuine value, not manipulation.
- **Do not force habit-loop thinking on products where usage is naturally infrequent or transactional.** The applicability check exists for a reason — respect it.
- **Present before writing.** Never write output files until the hook loops have been presented and validated.
- **Do not overwrite existing `research/hook-model.md`** without asking the user first.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/hook-model-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
