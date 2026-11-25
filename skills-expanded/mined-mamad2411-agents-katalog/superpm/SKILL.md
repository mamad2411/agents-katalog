---
name: superpm
description: Produce product planning, strategy, research, analytics, and launch artifacts with independent critique. Includes PRDs, roadmaps, user flows, screen specs, implementation handoffs, and resume or policy-document review.
---

# /superpm - one PM request, a verified artifact

One PM ask -> capture intent -> diverge by domain -> the smallest useful artifact -> an
independent critic checks it against the framework and the real decision -> stop.

68 PM frameworks live in `reference/`; this file routes the ask and names the loop. For a
one-paragraph note you could write directly, skip the skill.

## Principles

- **Serve the real decision.** Name the decision the artifact drives before drafting; a
  framework filled in for its own sake is waste.
- **Smallest useful artifact.** Only the frameworks the decision needs - no bolted-on
  SWOT/persona/roadmap when the ask was one pricing call.
- **Ground claims in evidence.** Numbers, quotes, segments come from the user's data, docs, or
  named assumptions - never invented.
- **Surface hidden assumptions.** The critic names unstated assumptions and missing pieces as
  risks - never present an assumption as fact.
- **Ask only when genuinely ambiguous.** Read the repo/docs/data first; interview only
  load-bearing, user-only choices (`reference/intent.md`).
- **Hard stops.** Irreversible or outward-facing actions (publish, send, post, share
  externally) need explicit consent.
- **Trace the chain.** EXECUTE -> FLOW -> STORYBOARD -> PACKAGE share the 기능명세 (SPEC) as one
  source of truth (`reference/model.md`); a flow node or screen callout with no SPEC is never
  invented. Derived artifacts come from the spec, not beside it.

## Intent capture - signal to domain

Read the request and route to one domain (the artifact named usually decides it). When the ask
spans domains, pick the primary deliverable and pull supporting frameworks from the others. When
the ask is to **plan a buildable thing end-to-end** (기획하자 / 개발하고 싶어, no single artifact
named), route to **PLAN** - a stepped session over the chain, not one artifact (`reference/plan.md`).

| Signal in the request | Domain | Reference |
|---|---|---|
| 기획하자 / 이거 개발하고 싶어 / 기획 도와줘 / plan this feature end-to-end / PRD부터 화면까지 | **PLAN** (session) | `reference/plan.md` |
| brainstorm ideas / risky assumptions / opportunity tree / prioritize features / customer interview / metrics | **DISCOVER** | `reference/discover.md` |
| product strategy / vision / value proposition / lean or business model / monetization / pricing / SWOT / PESTLE / Porter / Ansoff | **STRATEGY** | `reference/strategy.md` |
| PRD / OKRs / roadmap / sprint plan / retro / pre-mortem / user or job stories / stakeholder map / prioritization framework / red-team a plan | **EXECUTE** | `reference/execute.md` |
| user flow / 유저플로우 / flowchart / screen-to-screen flow / 화면 흐름 / 분기·상태 전이 | **FLOW** | `reference/flow.md` |
| 화면설계서 / 기능명세 / 스토리보드 / screen design doc / screen spec / wireframe / UI spec | **STORYBOARD** | `reference/storyboard.md` |
| implementation package / 구현 패키지 / 통합 산출물 번들 / export bundle / hand off to devs | **PACKAGE** | `reference/package.md` |
| personas / segments / customer journey / market sizing (TAM/SAM/SOM) / competitor analysis / sentiment | **RESEARCH** | `reference/research.md` |
| SQL from a question / cohort analysis / A/B test read-out | **ANALYTICS** | `reference/analytics.md` |
| go-to-market / beachhead / ICP / growth loops / GTM motion / battlecard | **GTM** | `reference/gtm.md` |
| marketing ideas / positioning / value-prop statements / product name / North Star metric | **GROWTH** | `reference/growth.md` |
| review or tailor a resume / draft an NDA or privacy policy / proofread | **TOOLKIT** | `reference/toolkit.md` |
| document an AI-built app / shipping artifacts / intended-vs-implemented gap | **AI-SHIP** | `reference/ai-ship.md` |

The domain decides which reference loads; the loop is the same for all. Cross-cutting: asks
about *what the market/customers want* (demand, trends, voice of customer) ground the artifact
in `reference/signal.md` first.

## The loop - Capture, Frame, Draft, Critic, Deliver

1. **Capture.** Classify and record one line - `Domain: <X> | Artifact: <Y> | Decision it
   serves: <Z>` - even when nothing is ambiguous. If genuinely underspecified, run the
   `reference/intent.md` gate (<=5 questions, one batched round, a recommended answer per
   question). Resolve doc/data-answerable questions by reading, not asking.

2. **Frame.** Extend that line into the artifact's `## Intent` block: classification, the real
   decision, and the completion bar (what "done and trustworthy" looks like for this
   framework). This block is the contract the critic checks against.

3. **Draft.** Load `reference/<domain>.md` and apply the named framework. Use the user's real
   inputs; mark gaps as explicit assumptions. Smallest useful artifact - no filler frameworks.

4. **Critic (independent).** Run `reference/critic.md`. Independence is mechanical: if the
   harness supports subagents, hand a fresh one only the `## Intent` block + the draft;
   otherwise switch stance and read cold. Red-team all four checks: missing framework sections,
   unsupported claims, dodged decisions, unvalidated assumptions - each emitted as a risk. Do not
   self-congratulate a draft to green.

5. **Deliver.** Fold blockers and gaps back in; leave user-owned risks in a `## Critic` block.
   Response shape: artifact -> remaining risks -> one line on what was checked against what ->
   the one natural next artifact in the chain (DISCOVER -> STRATEGY -> EXECUTE -> FLOW ->
   STORYBOARD -> PACKAGE; GTM/GROWTH for launch; ANALYTICS measures any) - offer it, don't start
   it. Inline by default; write
   files when multi-page or multi-file (STORYBOARD/PACKAGE: always files, default
   `templates/workspace.html` - the interactive SSOT canvas) and report paths.
   Outward/irreversible steps wait for explicit consent.

For a **PLAN session** (`reference/plan.md`), run this loop once per stage
(EXECUTE -> FLOW -> STORYBOARD -> PACKAGE), gating for the user after each and carrying the running
SSOT JSON forward; the whole chain is the deliverable, ending in `workspace.html` + a PACKAGE.

## Follow-up turns

The loop is per-artifact, not per-message. On iteration:

- Substantive change (new claim, section, or decision) -> re-Draft, re-run the critic on the
  delta only.
- Tone / format / length-only edits -> no critic re-run.
- New artifact or new domain -> new loop from Capture. "Another idea / different one" in
  DISCOVER follows the idea-proposal batch rule (`reference/discover.md`).
- Keep the loaded domain reference; do not re-read it each turn.

## Shared references

The domain table above routes domain-specific reading. Load these only when needed:

| Read | When |
|---|---|
| `reference/intent.md` | Capture: unresolved choices that only the user can answer |
| `reference/critic.md` | Independent review against the artifact's intent |
| `reference/signal.md` | Current market/customer evidence; uses `last30days` if installed |
| `reference/model.md` | Shared SPEC identifiers, entities, sync rules R1-R6, and validation codes for FLOW/STORYBOARD/PACKAGE |
| `templates/` | Artifact scaffolds, including the shared `templates/workspace.html` canvas |

## Output language

Write the artifact in the user's language. Keep framework names, metric names, and
machine-checked anchors (SQL, identifiers, file paths) in their canonical form.
