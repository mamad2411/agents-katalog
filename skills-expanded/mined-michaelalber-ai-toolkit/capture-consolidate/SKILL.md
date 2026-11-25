---
name: capture-consolidate
audience: team
description: Merges multiple capture documents from transcript-capture and email-capture into a unified intake bundle. Assigns canonical per-project REQ-XXX IDs, deduplicates overlapping requirements, surfaces cross-document contradictions for PM resolution, and produces a final capture bundle ready for spec generation. Use when two or more capture documents from transcript-capture or email-capture need to be merged into a single intake bundle for spec generation.
---

# Capture Consolidate

> "The requirements you want are in five different documents.
> The requirements you need are the ones that appear in all five and don't contradict."

> "A requirement stated twice is not two requirements.
> A requirement stated twice differently is a problem."

## Core Philosophy

Individual capture sessions — whether from transcripts or email threads — produce fragmented snapshots. The same requirement may appear in different phrasing across documents. One document may say "users must log in with SSO" while another says "SAML authentication required." A stakeholder may have clarified in a follow-up email what they requested ambiguously in the meeting. And the same `DRAFT-001` ID from two separate capture sessions refers to two completely different items.

Consolidation makes the capture bundle coherent enough for spec generation. It does three things: assigns canonical per-project REQ numbering, deduplicates semantically equivalent requirements, and surfaces contradictions between documents so the PM can resolve them before they become conflicting specs.

This is a PM-supervised process. The skill makes proposals; the PM decides. No requirement is dropped, merged, or renumbered without PM awareness.

**What this skill does:** Reads all `DRAFT-NNN` capture documents, identifies duplicates and near-duplicates, surfaces contradictions, assigns canonical `REQ-XXX` IDs, produces a unified capture bundle.

**What this skill does NOT do:** Write specs, resolve contradictions autonomously, drop requirements without PM approval, or push to Confluence without explicit PM instruction.

**Non-Negotiable Constraints:**
1. **The skill proposes; the PM decides** — no requirement is dropped, merged, or renumbered without PM awareness
2. **Contradictions are surfaced, never resolved** — conflicting statements across documents go to the PM with both sources
3. **IDs are canonical per project** — every accepted item gets a `REQ-XXX` ID; `DRAFT-NNN` IDs from different sessions are never assumed to match
4. **Every requirement keeps its sources** — a merged item lists each capture document it came from
5. **No Confluence push without explicit PM instruction**

## Workflow

### Phase 1: LOAD

Ask the PM which project this consolidation covers. Read the `captures/` directory and list all capture documents. Read the existing `req-registry.md` if one exists (incremental run). Extract all `DRAFT-NNN` items into a flat working list. Report before proceeding: project name, documents found, whether registry exists and its last REQ number, and counts of DRAFT items by type (requirements, decisions, commitments, open questions, within-document contradictions).

### Phase 2: DEDUPLICATE

Call `search_knowledge("requirements deduplication equivalence semantic matching")` to calibrate. For each DRAFT requirement, compare it against all others for:

| Class | Description | PM Decision Required |
|-------|-------------|---------------------|
| `exact` | Same requirement, same phrasing. One document likely echoes the other. | Confirm merge |
| `semantic` | Same requirement, different phrasing. ("SSO" vs "SAML authentication") | Confirm equivalence and choose canonical phrasing |
| `subset` | One is a specific case of the other. ("Login with SSO" ⊆ "Authentication system") | Decide: keep both, or roll sub into parent |
| `conflict` | Same topic, different positions. Cannot merge — must resolve first. | Resolve contradiction before REQ assignment |
| `distinct` | Similar topic, different requirements. Appears related but is actually independent. | Confirm as two separate REQs |

Present each candidate merge set to the PM:

```markdown
### Candidate Merge Set M-[NNN]

**Similarity class**: [exact | semantic | subset | conflict | distinct]

| DRAFT ID | Source Document | Statement | Uncertainty Tags |
|----------|----------------|-----------|-----------------|
| DRAFT-002 | 2026-01-10-kickoff.md | "Users must authenticate with SSO" | — |
| DRAFT-014 | 2026-01-15-email.md | "SAML-based authentication required" | — |

**Assessment**: These appear to be the same requirement in different terms.
**Proposed canonical phrasing**: "System must support SSO/SAML authentication"

PM decision: merge / merge with revised phrasing / keep separate / conflict
```

After all merge sets are reviewed, report: merge sets reviewed, count merged vs. kept separate vs. flagged as conflicts.

### Phase 3: RESOLVE

For each flagged conflict, present both positions and ask the PM to resolve:

```markdown
### Conflict C-[NNN] — Resolution Required

**Topic**: [What this conflict is about]

| Position | Statement | Source Document | Date | Speaker / Sender |
|----------|-----------|----------------|------|-----------------|
| A | "[statement A]" | [filename] | [date] | [speaker/sender] |
| B | "[statement B]" | [filename] | [date] | [speaker/sender] |

**Why this matters**: Implementing A and B together would [describe the conflict].

PM resolution: Position A is current / Position B is current / Both are valid (PM explains) / Neither is final (becomes open question)
```

Conflicts block REQ assignment. If the PM defers a conflict, it is logged as an open question in the consolidated output — not assigned a REQ ID.

### Phase 4: RENUMBER

Load `req-registry.md` to find the last-used REQ number (or start at `REQ-001`). For each accepted requirement, assign the next sequential `REQ-XXX`. Record the mapping: `REQ-XXX ← DRAFT-NNN (source doc) + DRAFT-NNN (source doc)`. Record superseded DRAFTs in the Retired section. Update `req-registry.md`.

**REQ IDs are sequential, never recycled.** A retired REQ ID stays in the Retired section permanently.

After RENUMBER, report: REQs assigned this session (starting and ending number), DRAFTs retired, open questions retained without REQ.

### Phase 5: OUTPUT

Produce two files:
1. **`captures/consolidated-[YYYY-MM-DD].md`** — The unified capture document for this run
2. **`captures/req-registry.md`** — The running REQ registry (create or update)

If Confluence output is requested: ask for target space and parent page before publishing. Default to local files.

AI discipline rules (propose-don't-execute, contradictions block progress, provenance travels with every REQ, semantic similarity is a proposal, never recycle IDs), the full anti-pattern catalog, and error-recovery procedures (no documents found, corrupted registry, >100-item sets, post-consolidation splits) live in `references/discipline-and-recovery.md`.

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase).

## State Block

```
<capture-consolidate-state>
phase: load | deduplicate | resolve | renumber | output
project: [project name]
capture_docs: [list of filenames]
draft_items_total: N
merge_sets_total: N
merge_sets_reviewed: N
merged: N
kept_separate: N
conflicts_total: N
conflicts_resolved: N
conflicts_pending: N
last_req_before: REQ-[NNN] | none
last_req_after: REQ-[NNN] | pending
output_path_consolidated: [path or pending]
output_path_registry: [path or pending]
last_action: [what was just done]
next_action: [what should happen next]
</capture-consolidate-state>
```

## Output Template

**Consolidated capture bundle header:** `# Consolidated Capture Bundle — [Project] — [Date] | Sources: [filenames] | REQ range: REQ-NNN – REQ-NNN`

**Requirements table:** `| REQ ID | Statement | Source Documents | Uncertainty | Status |` with statuses Active/Retired.

**Provenance map:** `| REQ ID | Merged From (DRAFT IDs) | Source Documents |` — traces every REQ back to its original capture session.

**REQ registry tables:** Active Requirements `| REQ ID | Statement (short) | Source Documents | Assigned Date | Status |` and Retired Requirements `| REQ/DRAFT ID | Statement | Reason Retired | Superseded By | Retired Date |`

**Session opening:** Explain the 5-phase process, ask PM for project name and capture document location, emit initial `<capture-consolidate-state>` block with `phase: load`.

Full REQ registry handling (Active/Retired tables, ID assignment across sessions): `references/req-registry-guide.md`

## Integration with Other Skills

- **`transcript-capture`** — Produces `DRAFT-NNN` capture documents from meeting transcripts. This skill is the downstream consumer.
- **`email-capture`** — Produces `DRAFT-NNN` capture documents from email threads and documents. This skill is the downstream consumer.
- **`task-decomposition`** — After consolidation produces `REQ-XXX` requirements, use this skill to decompose them into Jira-sized tickets.
- **`confluence-guide-writer`** — If the consolidated capture bundle should be published to Confluence, use this skill after PM approval.
