---
name: intake
description: Interactive Q&A capture of company knowledge into typed nodes in a company-brain vault. Sub-modes - vision (dictation-friendly six-phase flow), for-doc (document-driven interview that walks a target doc's sections), product, persona, competitor, competitor-ifu, competitor-clearance, competitor-snapshot, metric, meeting-notes, risk, clearance. Each session writes new typed markdown node files into the right folder and links them via derived_from edges to a source node. Always reads the vault's _system/PROFILE.md first to learn the active schema, never assumes it.
---

# intake

This skill turns conversation into typed nodes. The user talks; you write atomic markdown files into the vault's node folders, with frontmatter matching the schema, and edges that anchor every claim to a source.

You do not invent facts. You do not write into folders the schema does not have. You do not flip controlled-document boundaries.

## Before any sub-mode

Always do these first when the skill is invoked:

1. **Confirm the vault path.** Default: the current working directory. Resolve to absolute. Refuse politely if the path has no `_system/PROFILE.md` — that's how we recognize a vault.
2. **Load the active schema.** Run:
   ```
   cb describe-profile --path <vault>
   ```
   This returns JSON with the active profile name, the controlled-document-footer policy, and the full list of `active_node_types` (each with its folder). Use this list as the authority on what types you can create and where files go.
3. **For any node type you're about to write**, run:
   ```
   cb describe-node <type>
   ```
   to get its `extra_required_fields`. Populate them. Never skip a required field.
4. **Read the user's preferred handle** (the `verified_by` value). Ask once at session start if unset.

## Universal node-writing rules

Every node you write must have the base required frontmatter:

```yaml
---
id: <type>-<kebab-slug>
title: "Human-readable Title"
type: <one of the active types from describe-profile>
namespace: <free-form short string, e.g. "product-strategy">
summary: "One line, 100-200 chars, lets an agent decide whether to load the full body."
auto_inject: false   # true only for pillars that should govern future agent answers
applicable_when: null   # required when auto_inject is true
primary: false   # optional; see "Primary-entity marking" below
confidence: 0.85   # 0.0 to 1.0
verified_at: <ISO date today>
verified_by: <user's handle>
staleness_signal: null   # or a concrete description of what would make this node stale
tags: []
edges: []   # see edge-writing rules below
related: []
source_url: null
controlled_document: false
---
```

Plus whatever extra fields `cb describe-node <type>` lists as `extra_required_fields`.

For risk/* and entities/indications-for-use/* node types, `controlled_document: false` is **mandatory**, not just default. The validator will reject any other value.

## Edge-writing rules

When the user gives you a relationship — "this decision supports our pricing pillar" — write an edge:

```yaml
edges:
  - target: pillar-pricing-philosophy
    type: supports
    weight: 0.9
    note: "This decision is the operational expression of the pricing pillar."
```

Allowed `type` values: `related_to`, `depends_on`, `derived_from`, `contradicts`, `supports`, `part_of`, `preceded_by`, `followed_by`, `authored_by`, `tagged_with`.

`target` must be an id that already exists in the vault. If the target doesn't exist yet, either create that node first or note the link explicitly to the user so they can decide.

Every node that derives from a source should have a `derived_from` edge to that source. This is how the doc-generators trace claims.

## Primary-entity marking

The optional `primary: true` boolean on a node frontmatter tells doc-generators ("which persona leads the MRD," "which competitor the default sales-battle-card targets") which node to pick when there is more than one of the same type. Scoped per `(type, namespace)` — a primary persona in `market` and a primary persona in `partners` is a legitimate configuration.

Intake rules:

1. **First-of-type in a session auto-marks `primary: true`.** When you write the first `persona`, `product`, `competitor` (or any other type that benefits from primary marking) in a session, set `primary: true` on its frontmatter. Subsequent entities of the same type default to `primary: false`.
2. **Run `cb list-nodes --type <type> --path <vault>` before auto-marking.** If the vault already has a node of that type, do NOT auto-mark the new one — there is already a representative, and the existing primary should remain unless the user says otherwise.
3. **Honor a `--make-primary <id>` request from the user.** Anywhere in the session, if the user says something like `--make-primary persona-founder`, "make persona-founder the primary," or "promote competitor-gbrain to primary," demote the current primary in that `(type, namespace)` to `primary: false` and set the named node to `primary: true`. Echo the change back so the user sees the diff. The `--make-primary <id>` form is a recognized shorthand, not a CLI flag (intake is LLM-driven, not a `cb` subcommand).
4. **Never demote silently.** If the user marks a second node primary without naming what to demote, mention the existing primary and ask which one wins.
5. **Don't auto-mark profile-conditional types** (`indication-for-use`, `regulatory-clearance`, `risk-insight`, hazards, harms, controls, regulations, standards). These don't have a "representative" semantics.

The validator emits a `--strict` warning when more than one node of the same `(type, namespace)` carries `primary: true`. Renders still produce deterministic output (alphabetical among the primaries) with a footer note, so an over-marked vault stays useful until you tidy it.

## After writing nodes

Always run:

```
cb validate --path <vault>
```

at the end of the session. If it reports errors, fix them before declaring done. The exit code matters: 0 means clean.

You do **not** commit. The user (or their team) decides when to commit. If the vault is a git repo and the user wants you to commit after intake, do it — but ask first, with a structured commit message naming the new node ids.

## Sub-modes

### `vision` (dictation-friendly)

The flagship sub-mode. Six phases.

**Phase 1 — Open capture.**
Say to the user: "Talk freely. End with 'done' or 'process' when you're finished. You can dictate via your OS or just type." Then wait for input. Do not interrupt with structure-imposing questions.

**Phase 2 — Source node.**
The first thing you write, before any extraction, is one immutable `source` node:

```yaml
---
id: source-vision-session-<YYYY-MM-DD>
title: "Vision capture session <YYYY-MM-DD>"
type: source
namespace: vision
summary: "Founder vision capture session. Raw transcript preserved for provenance."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: <today>
verified_by: <handle>
staleness_signal: null
tags: [vision, dictation]
source_kind: founder-vision
edges: []
related: []
source_url: null
controlled_document: false
---

# Vision capture session <YYYY-MM-DD>

## Raw transcript

<the entire transcript verbatim, no edits>

## Rejected extractions

<filled in during phase 4 — leave empty initially>
```

If the same user has multiple sessions, suffix with a session number: `source-vision-session-2026-05-22-2`.

**Phase 3 — Nugget extraction.**
Scan the transcript. Identify distinct knowledge units. For each one, decide its type using these rules:

- A stated principle that should govern future answers → `pillar` (auto_inject likely true).
- A statement of "we will NOT do X" → `pillar` with negative framing (auto_inject true) OR a `decision` with strong `## What This Rules Out` section. Use pillar when it's a durable boundary; decision when it has alternatives that were considered.
- A concrete choice between alternatives → `decision`.
- A falsifiable bet → `hypothesis`.
- An observed regularity across examples → `pattern`.
- A verified atomic claim → `fact`.
- A defined term or mental model → `concept`.
- A known unknown → `question`.
- An indication for use the user described → `indication-for-use` (medical-device profile only).
- A risk observation in ISO-14971-adjacent language → `risk-insight` (medical-device profile only).

**Be conservative.** Not every sentence becomes a node. The bar: "would an agent retrieve this six months from now?" If the answer is no, leave it in the source transcript only.

Present extractions as a batched table for the user to review:

```
| # | Excerpt | Proposed type | Proposed id | Rationale |
|---|---------|---------------|-------------|-----------|
| 1 | "We never enter pediatric..." | pillar (non-goal) | pillar-no-pediatric-use | Durable boundary; should auto-inject when pediatric topics come up. |
| 2 | "Pricing is monthly..." | decision | decision-001-monthly-pricing | Concrete choice between monthly and annual. |
...
```

Default to batched-table review. If the user requests one-at-a-time, switch to that style.

**Phase 4 — Review loop.**
For each row, ask the user: accept / edit / reject / split / merge.

- **Accept**: write the node with the extraction as the source of its body.
- **Edit**: take the user's edits and re-render.
- **Reject**: append a row to the source node's "Rejected extractions" section with the excerpt and the reason. Do not write a node.
- **Split**: extract becomes two or more nodes.
- **Merge**: this extraction joins an existing extraction.

**Phase 5 — Write and link.**
For each accepted extraction, write the node file. Add a `derived_from` edge pointing at the session source node:

```yaml
edges:
  - target: source-vision-session-2026-05-22
    type: derived_from
    weight: 0.9
    note: "Captured in this vision session."
```

If the user gave you a relationship to another existing node, add that edge too.

**Phase 6 — Anti-decision sweep.**
Before declaring done, ask explicitly: "Were there any 'we are NOT doing X' statements I missed? Dictation tends to bury non-goals in positive prose." Capture anything new as a non-goal pillar or anti-decision.

Final action: run `cb validate --path <vault>` and report results.

### `for-doc` (document-driven)

A document-driven interview that walks the sections of a target planning
document (MRD, and over time other doc types) and captures what's needed to
render it. The doc's section structure becomes the script; the operator
answers section by section, often by voice dictation. Two outputs from one
session: new typed nodes in the vault, and a rendered doc at the end if the
operator wants it.

The user invokes this with phrasing like "intake for-doc mrd" or "let's do
a document-driven intake of the MRD."

**Step 1 — Load the manifest and detect gaps.**

```
cb describe-doc-questions <doc> --path <vault>
cb gaps-for-doc <doc> --path <vault>
```

Both emit JSON. The first returns the section list (already filtered for
the vault's profile — medical-device-only sections drop on saas vaults
automatically). The second classifies each section as `complete`,
`partial`, or `empty`.

If the doc has no manifest yet (`unknown doc`), tell the user — v0.7.0
ships `mrd`; other doc types add their manifests as adopter demand
surfaces.

**Step 2 — Announce the plan.**

Tell the user, before asking the first question:

- Which sections will be skipped (already complete) — name them.
- Which sections will be partial (we already have something, but need more).
- Which sections will start empty.

Example: "I have everything I need for executive-summary, market-personas,
and competitive-landscape. Vision and positioning is partial — you have 2
pillars but the section likes 3+. The remaining 4 sections are empty. We'll
walk those 5 sections. Ready?"

**Step 3 — Walk sections in order.**

For each section in the (filtered) manifest:

- **complete** — skip silently after the opening announcement. Do not
  ask its questions.
- **partial** — confirm what's there: "You already have [list ids]. The
  section asks for at least N of these; you have M. Want to add more, or
  move on?" If the user wants to add, ask the section's questions.
- **empty** — pose the section's questions one at a time, in the order they
  appear in the manifest. Use the prompt verbatim if it reads well; rephrase
  for flow if it doesn't.

**Step 4 — Extract from each answer.**

Voice dictation produces rambling, parentheticals, half-sentences, and
tangents that veer into other topics. For every answer:

1. **The on-topic part** → draft a node of the type indicated by the
   question's `captures` field. Follow the universal node-writing rules
   above (required frontmatter, derived_from edge to a session source node).
2. **Stray facts that match another section's `feeds_from`** in the current
   doc → also draft nodes, filed in the right folder. The operator will see
   them in the end-of-session review; don't interrupt to confirm.
3. **Anything else** (off-topic asides, half-formed thoughts, noise) → drop.
   You may mention them in the review for the operator to decide.

The "stray fact" scope is **narrow**: only file what would land in another
section of the doc the user is interviewing. Don't go broader. If the user
mentions something interesting that doesn't match any section's feeds_from,
note it in the review summary instead of writing a node.

**Step 5 — Re-check before each section.**

Before posing the next section's questions, re-run:

```
cb gaps-for-doc <doc> --path <vault>
```

If the previous answer accidentally satisfied (or partially satisfied) the
section coming up, surface it: "I think you mentioned earlier that [X],
which lands in this section. Anything more to add, or shall we move on?"

This is how the document-driven flow stays adaptive — the operator's
natural rambling pre-fills downstream sections, and the interview reacts.

**Step 6 — Session source node.**

Like the `vision` sub-mode, write one immutable `source` node early in the
session with `source_kind: strategic-thesis` (or `internal-data` if the
operator says it's more an accounting of current state than a vision
statement). Every node you write in this session gets a `derived_from`
edge to that source. Id pattern:
`source-for-doc-<doc>-session-<YYYY-MM-DD>`.

**Step 7 — End-of-session review.**

When every non-complete section has been walked, print a captured summary:

```
Captured this session:

Executive summary:
  - pillar-... — "Title"
  - product-... — "Title"

Vision and positioning:
  - pillar-... — "Title"
  ...

Stray-filed into other sections:
  - competitor-acme (filed into Competitive landscape from your answer to
    "What are your competitors?")
  ...
```

Then:

1. Run `cb validate --path <vault>` and report results. If there are
   errors, propose fixes (don't auto-rewrite — surface and confirm).
2. Ask: "Render the document now? [Y/n]" If yes, run
   `cb render <doc> --path <vault>` and report the output path.

**Resumability.**

Nodes are written as the session proceeds, not batched at the end. If the
operator stops halfway, the next `intake for-doc <doc>` run sees the
partially-populated vault, classifies the early sections as
complete/partial, and picks up at the first still-empty section. No state
file required — the vault is the state.

**Voice-dictation notes.**

- Expect parentheticals ("we work with hospitals, well, actually mainly
  outpatient surgery centers"). Extract the substance, not the surface
  form.
- Expect "we do X, but never Y" answers that mix positive and non-goal
  pillars. File them in the right sections.
- Expect the operator to drift into territory another section covers.
  This is the whole point of the data-driven flow — react and refile.

### `product`

Capture a `product` or `product-line` node.

Ask:
1. Is this a product or a product line? (Determines `type`.)
2. What's the name?
3. What does it do, in one line? (becomes the summary)
4. What product line does it belong to? (becomes a `part_of` edge if a product line exists)
5. What IFU applies to it, if any? (medical-device only — flags whether we need a `competitor-ifu` follow-up)

Write the node. Add edges. Run validate.

### `persona`

Capture a `persona`.

Ask:
1. Persona name (archetype, not real person — that's `customer`).
2. Who is this person? (role, context — 1-2 sentences)
3. What do they care about? (3-5 bullets)
4. What do they NOT care about?
5. Any related ICP pillar? (becomes a `supports` edge)

### `competitor`

Capture a `competitor` entity. Required fields: `legal_name`, `canonical_url`.

Ask:
1. Legal name.
2. Canonical URL (the company's primary domain). This is mandatory — it disambiguates "Acme Medical Inc" from any other "Acme."
3. Positioning, in one paragraph.
4. Strengths (per public signals).
5. Weaknesses (per your hypothesis — note these as your reading, not as fact).

### `competitor-ifu` (medical-device profile only)

Capture or update a competitor's `indication-for-use`. Required fields: `population`, `condition`, `intervention`, `setting`, `belongs_to_product`.

Ask:
1. Which competitor? (must already have a `competitor` node)
2. Which of their products? (Place the IFU as `belongs_to_product`. If competitor products aren't modeled as separate `product` nodes, use the closest internal product node as a placeholder and note this; the v1 schema requires this field to resolve.)
3. When was it cleared / what's the version label? (Drives the node id and the chain.)
4. Population, condition, intervention, setting — capture each separately.
5. Is this a successor to a prior IFU version? If yes, add a `preceded_by` edge to that prior IFU.
6. What source? (510(k) summary PDF? website snapshot? press release?) Create the source node if needed; add `derived_from`.

### `competitor-clearance` (medical-device profile only)

Capture a `regulatory-clearance`. Required fields: `clearance_number`, `clearance_type`, `clearance_date`, `applicant`, `device_name`, `product_codes`, `summary_url`.

Ask:
1. K-number (or De Novo / PMA equivalent).
2. Clearance type: 510k / de-novo / pma / breakthrough / letter-to-file.
3. Clearance date.
4. Applicant company name.
5. Device name.
6. Product codes (FDA, e.g., DRT).
7. Summary URL (or "https://example.com/..." if planning a future filing without an actual URL).
8. Predicate clearances? (Become `preceded_by` edges on this node. The predicate clearances should already exist as nodes — if not, capture them via this same sub-mode first.)

### `competitor-snapshot` (medical-device profile and others)

Capture a web-snapshot `source`. The user supplies a screenshot image path (in v1; v1.x adds chrome-devtools-mcp automation).

Ask:
1. Which competitor? (must already exist)
2. URL of the page captured.
3. Path to the screenshot file (PNG / JPG).
4. When was it captured? (default: today)
5. Capture method: manual-screenshot (v1) — leave room for chrome-devtools-mcp later.

Use Claude's vision capability to read the screenshot text, then write the `source` node with the extracted text in the body. The image moves into `<vault>/_attachments/` with a name like `<YYYY-MM-DD>-<competitor-slug>-<page-slug>.png`. Source node frontmatter includes `attachment` pointing at that path.

### `metric`

Capture a `metric` node. Required field: `volatility_class`.

Ask:
1. Metric name (e.g. "MRR", "Day-1 pad attach rate").
2. Definition — what is this measuring exactly?
3. Volatility class: `low` (changes annually), `medium` (changes quarterly), or `high` (changes monthly or faster). Drives confidence decay for snapshot facts.
4. Any related pillars or decisions? (typically a `related_to` edge)

After capturing the metric, offer to capture a first snapshot fact: a `fact` node with `metric_id` set to this metric's id.

### `meeting-notes`

Process freshly-finished meeting content into atomic nodes.

Ask:
1. Meeting date, attendees, topic.
2. Paste or describe what was discussed.

Then treat the meeting content like the vision sub-mode: extract typed nodes (decisions made, action items as questions, observations as patterns). Write one `source` node with `source_kind: customer-interview` if external, else `internal-data`. Derive new nodes from it.

### `risk` (medical-device profile only)

ISO-14971-vocabulary risk thinking. **This is planning, not a controlled risk management file.** Every node you write must have `controlled_document: false`. Remind the user explicitly.

Ask:
1. What's the hazard? (a potential source of harm) — `hazard` node.
2. Under what circumstances could it cause harm? (a hazardous situation) — `hazardous-situation` node.
3. What's the potential harm? — `harm` node.
4. Candidate mitigations? — `risk-control-idea` node(s).
5. Any planning-level observation about how this hazard behaves? — `risk-insight` node.

Link them: hazardous-situation `related_to` hazard, harm `related_to` hazardous-situation, risk-control-idea `supports` harm-prevention.

Closing reminder, every time: "This is planning. The controlled risk management file is a separate artifact created under your QMS."

### `clearance` (our own — medical-device profile only)

Same shape as `competitor-clearance` but for our own planned or actual filing. Confidence tends to be lower (e.g., 0.5) for planned filings, higher (0.95) for cleared ones.

## What this skill does NOT do

- Does not write nodes outside the active profile's `active_node_types`.
- Does not modify `_system/*.md` files.
- Does not change `controlled_document` from `false` to `true`. The validator will reject any such attempt; the controlled-document boundary is a v1 rail.
- Does not push to git remotes.
- Does not run document generation. Use the `doc-generate` skill for that.

## What to do when something goes wrong

- **Validation errors after a session**: list them, propose fixes, ask the user to confirm before re-writing nodes.
- **The user contradicts an existing node**: don't silently overwrite. Surface the contradiction and ask whether to (a) supersede the existing node (mark old one with a low confidence and write a new one), (b) preserve both with a `contradicts` edge, or (c) update in place (with a higher confidence and updated `verified_at`).
- **The user asks for a node type you can't write** (because the profile doesn't activate it): explain which profile would activate it and stop. Don't write into a folder the schema doesn't have.
