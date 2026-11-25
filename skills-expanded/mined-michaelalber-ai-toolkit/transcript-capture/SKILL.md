---
name: transcript-capture
audience: team
description: Converts raw Zoom/Slack AI-generated transcripts into structured capture documents for spec-driven development. Uses per-block human review to filter small talk and off-topic content. The PM guides what is in scope; the skill structures that judgment. Use when given a raw Zoom transcript, Slack AI-generated meeting summary, or pasted meeting notes that need to be converted into a structured capture document for spec-driven development.
---

# Transcript Capture

> "Information is not knowledge. The map is not the territory.
> The transcript is not the meeting."
> -- Adapted from Alfred Korzybski

> "The problem with AI-generated meeting summaries is not that they are wrong.
> It is that they are confidently, plausibly, usefully wrong in exactly the right places."

## Core Philosophy

Zoom, Slack, and Teams AI summaries are high-noise artifacts. They contain small talk, tangential discussions, resolved disagreements, social coordination, and meeting logistics alongside genuine requirements. An AI that processes them without human guidance will extract all of it — or worse, hallucinate a synthesis that sounds like requirements but reflects the model's priors rather than the stakeholder's intent.

This skill does not replace PM judgment. It structures it. The PM provides context before filtering begins, reviews candidates block by block, and annotates ambiguous items. The skill organizes the judgment workflow so nothing is silently dropped and every accepted item is traceable to its source.

**What this skill does:** Accepts raw transcript text or a file path, segments into topical conversation blocks, scores each block for relevance, presents each to the PM for accept/reject/annotate decision, produces a structured capture markdown with `DRAFT-NNN` IDs.

**What this skill does NOT do:** Auto-accept any block, invent requirements from ambiguous phrasing, filter silently, or push to Confluence without explicit PM instruction.

**Non-Negotiable Constraints:**
1. **The PM reviews every block** — nothing is auto-accepted; each block is accepted, rejected, or annotated by the PM
2. **Nothing is filtered silently** — a rejected block is still recorded as rejected
3. **No requirements from ambiguous phrasing** — unclear statements become annotated questions, not requirements
4. **Every accepted item is traceable** — it links back to its source block in the transcript
5. **No Confluence push without explicit PM instruction**

The full domain-principle set, AI discipline rules, anti-pattern catalog, and error-recovery
procedures live in `references/discipline-and-recovery.md`. Signal-type definitions live in
`references/signal-types.md`.

## Workflow

The INTAKE–FILTER–REVIEW–OUTPUT loop. Fill-in templates for every phase are in
`references/capture-templates.md`.

### Phase 1: INTAKE — Gather PM Context

1. Ask the PM for the transcript source — paste or file path (`.txt` or `.md`)
2. Collect context using the Intake Template (`references/capture-templates.md`) — all six fields
3. Confirm understanding of in-scope and out-of-scope topics before proceeding
4. Only then → FILTER

**Do not proceed to FILTER without all six context fields.** If the PM skips a field, ask for it specifically. The `capture sensitivity` field (`standard` | `thorough`) sets how aggressively soft signals are captured — see the template reference.

### Phase 2: FILTER — Segment and Score the Transcript

1. Call `search_knowledge("requirements extraction meeting transcript interview")` to calibrate
2. Read the transcript in full — do not extract during reading
3. Segment into topical conversation blocks (natural topic breaks, not fixed line counts)
4. For each block, assign: Block ID (`B-001`, ...), Speaker(s), Timestamp / line range, Topic summary, Relevance score, Relevance reason, Signal type(s)
5. Post a brief filter summary (block counts by score, totals), then begin per-block review

**Relevance Scoring:**

| Score | Criteria |
|-------|----------|
| `HIGH` | Directly names a feature, constraint, requirement, or decision within in-scope topics. Speaker is an authoritative stakeholder. |
| `MEDIUM` | Touches an in-scope topic but with uncertainty, indirectly, or from a non-authoritative speaker. |
| `LOW` | Tangentially related. Requires PM judgment. |
| `SKIP` | Clearly out-of-scope: logistics, small talk, unrelated project discussion, repeated content. |

SKIP blocks are not presented for review — they are logged in the drop log, available on request.

### Phase 3: REVIEW — Per-Block PM Review

Present each non-SKIP block individually using the Per-Block Presentation Format
(`references/capture-templates.md`). Do not present the next block until the PM responds to the
current one. Order: HIGH → MEDIUM → LOW.

**Review Rules:** Present one block at a time and wait. If the PM requests full block context, provide 10 additional lines. If the PM requests the SKIP log, show it immediately. Allow re-review of previously decided blocks without friction. Do not editorialize on PM decisions. After all blocks are reviewed, post a brief summary (accepted / rejected / flagged / skipped counts) before OUTPUT.

### Phase 4: OUTPUT — Produce Capture Document

1. Call `search_knowledge("acceptance criteria given when then format")` to confirm output format
2. Organize accepted content by signal type: requirements, decisions, open questions, action items
3. Assign provisional `DRAFT-NNN` IDs to all extracted requirements
4. Produce the capture markdown (see Output Template below)
5. If Confluence publish is requested: ask for target space and parent page before publishing

**Load on demand — `references/discipline-and-recovery.md`:** Knowledge Base Lookups (run them before the first phase).

## State Block

```
<transcript-capture-state>
phase: intake | filter | review | output
project: [project or client name]
meeting: [meeting name and date]
capture_sensitivity: standard | thorough
blocks_total: N
blocks_high: N
blocks_medium: N
blocks_low: N
blocks_skip: N
blocks_reviewed: N
blocks_accepted: N
blocks_rejected: N
blocks_flagged: N
current_block: B-[NNN] | complete
output_path: [file path, or "pending"]
last_action: [what was just done]
next_action: [what should happen next]
</transcript-capture-state>
```

## Output Template

Default output path: `captures/[YYYY-MM-DD]-[meeting-slug].md`.

**Header:** `# [Meeting Name] — [Date] — [Project / Client]`
**Sections:** Participants | Summary (2–3 sentences) | Key Decisions (statement + source attribution) | Requirements Extracted (`DRAFT-NNN` + statement + source, with `⚠ [UNCERTAIN]` or `🔍 [NEEDS-CLARIFICATION]` tags) | Open Questions (question + owner) | Action Items (owner + due date) | Drop Log (Block / Score / Reason / PM Decision).

**Session Opening:** Explain the 4-phase process (intake → filter → review → output), state that nothing is silently dropped, ask for transcript location, meeting purpose, and project. Emit the initial `<transcript-capture-state>` with `phase: intake`.

Full document template and session-opening detail: `references/capture-templates.md`.

## Integration with Other Skills

- **`email-capture`** — Use when the intake source is an email thread instead of a meeting transcript. Both produce the same `DRAFT-NNN` format; use `capture-consolidate` to merge outputs.
- **`capture-consolidate`** — Run after one or more capture sessions to assign canonical `REQ-XXX` IDs, deduplicate overlapping requirements, and surface contradictions.
- **`confluence-guide-writer`** — If the final capture document should be published as a stakeholder-facing artifact, use this skill to format and publish it after PM approval.
