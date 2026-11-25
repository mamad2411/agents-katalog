---
name: discovery
description: >
  The vocabulary and format rules for discovery artefacts — brief files, decision maps, evidence
  tags, and the Definition of Ready. Use when writing or reading a brief, tagging a claim as
  evidence or assumption, deciding whether a ticket is ready to spec, charting or resolving a
  decision map (destination, fog, frontier), or running any discovery command (/sdlc:brainstorm,
  /sdlc:discover, /sdlc:synthetic-users, /sdlc:backlog, /sdlc:ux-shape, /sdlc:chart).
---

# Discovery

Pre-spec artefacts live in `specs/briefs/` (C1 `Briefs live in:` key). A brief captures
claims at varying confidence levels. The evidence-tag system tells `/sdlc:backlog` and
`/sdlc:spec` which claims are ready to act on.

## Evidence tags

Every factual sentence in a brief ends with exactly one tag:

| Tag | Meaning |
|-----|---------|
| `[EVIDENCE: <source>]` | A human produced it; source named |
| `[ASSUMPTION]` | No human source; inferred or guessed |
| `[SYNTHETIC]` | Output of a synthetic-users run |
| `[SOURCE: <url>]` | A verifiable artefact outside the working directory that an agent read; the URL or exact path is named |

**A tag never upgrades.** `[SYNTHETIC]` stays `[SYNTHETIC]`. `[ASSUMPTION]` stays until a
human provides a source — then rewrite the sentence with `[EVIDENCE: <source>]`. The tag on
a sentence is the lowest confidence it has ever had.

`[SOURCE]` may replace `[ASSUMPTION]` when the sentence is rewritten against a named external
artefact. `[SOURCE]` never becomes `[EVIDENCE]`: only a human source does that. Files inside this
repository stay `[EVIDENCE: <path>]`, which is what `/sdlc:discover` already writes.

`/sdlc:backlog` refuses when the Problem section contains any `[ASSUMPTION]` (UC-6).

## Brief formats

`specs/briefs/<slug>.md` — ≤ 80 lines. Blank: `references/brief-template.md`.

Sections in order: **Problem** · **Expected outcome** · **Alternatives considered**
(always includes "do nothing") · **Non-goals** · **Decisions** (owner each) · **Open questions**

`specs/briefs/product-brief.md` — ≤ 200 lines.

Sections in order: Problem · Who · Stakeholders · Rules · Flows · Benchmark · Success criteria ·
Scope (now / later / not) · Non-goals · Decisions (owner each) · Riskiest assumptions (test each) ·
Open questions

`specs/briefs/ux-<slug>.md` — ≤ 60 lines. Produced by `/sdlc:ux-shape`.

Sections: Direction · Scope · States (empty, loading, error, denied, success) ·
Riskiest assumption + test

## Decision maps

`specs/briefs/map-<slug>.md` — ≤ 120 lines. Blank: `references/map-template.md`. Produced by
`/sdlc:chart` for an effort whose route needs several sessions.

Frontmatter: `slug`, `map` (tracker ref or `none`), `status` (`charting|open|cleared|abandoned`).
Sections in this order and no others: **Destination** · **Decisions so far** · **Open tickets** ·
**Not yet specified** · **Out of scope**.

- The map is an index, not a store: a decision's detail lives on its ticket; the map holds one line
  and a link. There is no `Notes` section — the planning constraint is enforced by
  `guard pre-write`, not by text this agent can edit.
- A decision appears in exactly one section. Fog that graduates into a ticket leaves
  **Not yet specified** in the same edit.
- Decision ids are `D-1`, `D-2`, … and are never renumbered, for the same reason `UC-` ids are not.
- Caps: at most **7** rows in **Open tickets** and **10** bullets in **Not yet specified**. Over
  either cap, the destination is too wide — narrow it instead of charting more.

|Type|Label|Mode|Reach for it when|Resolved by|
|---|---|---|---|---|
|grilling|`decision:grilling`|HITL|the default: talking it through settles it|`/sdlc:brainstorm` in a fresh session|
|prototype|`decision:prototype`|HITL|"how should this look or behave" — talk cannot settle it|a one-file prototype, built to `mockup.md` Phase 2 rules|
|research|`decision:research`|AFK|a fact outside the working directory blocks the decision|a subagent writing `[SOURCE: <url>]`-tagged notes|
|task|`decision:task`|either|nothing to decide, but manual work blocks a decision|the agent where it can, else a checklist for the human|

`task` is the only type that does rather than decides, and it belongs on a map only because it
unblocks a decision. A `task` ticket that delivers part of the destination is mis-typed.

**HITL resolution rule.** A `grilling` or `prototype` ticket resolves only through a human's own
words typed in this session; `Decision:` restates that reply and `Answered by: @<login>` names the
human. No reply — an unattended run (`AISDLC_HEADLESS=1`), or a proposal the human did not confirm
in their own words — leaves the ticket open: there `Answered by:` could only be the automation
identity (**current-user** of an unattended run), and the agent cannot answer its own grilling.

**Question discipline.** Ask exactly one question per message; keep each question under 40 words;
end it with the decision id it unblocks, `(unblocks D-<n>)`.

## Definition of Ready

A brief is ready to pass to `/sdlc:spec` when all three hold:

1. Problem and who has it stated with `[EVIDENCE: …]` (not `[ASSUMPTION]`)
   `[SOURCE]` does not satisfy this line; a human must name the source.
2. Expected outcome is observable and written down
3. No blocking open question remains

`/sdlc:init --discovery` writes this block into `.claude/sdlc.md`.

## Sizing

| Artefact | Limit | Why |
|----------|-------|-----|
| `specs/briefs/<slug>.md` | ≤ 80 lines | Loads beside the router and a playbook |
| `specs/briefs/product-brief.md` | ≤ 200 lines | Loads beside the router and a spec |
| `specs/briefs/ux-<slug>.md` | ≤ 60 lines | Loaded in `/sdlc:mockup` Phase 1 |
| `specs/briefs/map-<slug>.md` | ≤ 120 lines | the index loads at the start of every map session |

## Anti-patterns

| Pattern | Consequence |
|---------|-------------|
| Factual sentence with no tag | `discover` quality gate rejects; brief is blocked |
| `[SYNTHETIC]` treated as `[EVIDENCE]` | Invalidates the `backlog` readiness gate |
| Problem entirely `[ASSUMPTION]` | `backlog` refuses until research fills it |
| Numeric claims in synthetic output | Anchors the team to invented figures |
| `[SOURCE]` treated as `[EVIDENCE]` | Invalidates the `backlog` readiness gate |
| Ticket that reads "build the X" | An implementation ticket on a decision map; belongs downstream of `/sdlc:spec` |
| Brief over its size limit | Cannot load beside a spec context |

## Review checklist

- [ ] Every factual sentence ends with exactly one evidence tag
- [ ] No `[ASSUMPTION]` in Problem (if passing to `backlog`)
- [ ] "Do nothing" appears in Alternatives considered
- [ ] Each Decision has an owner
- [ ] Open questions are genuine questions, not deferred tasks
- [ ] Sizes within limits above
- [ ] Every open ticket reads as a question
- [ ] Nothing appears in both Decisions so far and Not yet specified
