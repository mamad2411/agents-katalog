---
name: outreach-batch
description: Batch cold outreach for a company — finds and ranks contacts (contact_finder + evidence gate), writes an Outreach Brief for each of the top N to one review queue file, stops for Nick's spine, then drafts a Nick-voice cold email from each stated spine with provenance tags. No auto-send; you approve/edit/send each one.
argument-hint: <company-name> [count] [draft:N]
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Grep(data/*), Write(output/**), Write(data/networking.md), Bash(*), mcp__exa__web_search_exa, mcp__exa__web_fetch_exa, WebSearch, WebFetch
---

# Outreach Batch — Contact Finder → Ranked Briefs → Nick's Spine → Drafts → Review Queue

Wire the acquisition engine (`tools/contact_finder.py`) through the ranking gate
(from `/scan-contacts`) into batch cold-email drafting (from `/cold-outreach`),
landing everything in ONE review queue file. Nick reviews, edits, and sends each
draft on his own — **nothing is auto-sent**.

This skill is orchestration only. It does NOT reimplement the evidence gate, the
ranking, or the voice logic — it composes the canonical sources:
- Acquisition + gate + ranking → `.claude/skills/scan-contacts/SKILL.md` (Steps 2–5)
- Per-draft voice, provenance, quality → `.claude/skills/cold-outreach/SKILL.md` (Steps 4–7)

Origin: Loop-2 pipeline build, 2026-07-16. Per [[feedback_cold_outreach_flow_gaps]]
(the drafting FLOW is the bottleneck, so batch drafting MUST run the same flow-gap
guardrails) and [[feedback_recruiter_channel_resume_is_general]] (a general CV is the
attachable asset, but default is no-attach on first contact).

## Arguments

- `$ARGUMENTS`:
  - **Company** (required): company name (quoted if multi-word).
  - **count** (optional integer): how many contacts `contact_finder` fetches (default 20).
  - **draft:N** (optional): how many top-ranked survivors to actually draft (default 3, max 6 — batch drafting is real per-contact research, keep N small).

Examples:
- `/outreach-batch "Acme AI"` — fetch ~20, draft the top 3
- `/outreach-batch "Acme AI" 30 draft:5` — fetch ~30, draft the top 5

If no arguments, show this usage block and stop.

## Instructions

### Step 1: Profile guard

Confirm `data/profile.md` and `data/goals.md` exist with real content (not TODOs).
If either is missing/placeholder, stop and tell Nick to run `/import-cv` or fill
`data/goals.md`. (Same guard as `/scan-contacts` and `/cold-outreach`.)

### Step 2: Acquire + gate + rank (delegate to /scan-contacts logic)

Run the `/scan-contacts` pipeline for the company, Steps 2–5:
1. `PYTHONIOENCODING=utf-8 python3 tools/contact_finder.py --company "<company>" --num <count>` — deterministic acquisition.
2. **Evidence-span employment gate (MANDATORY):** quote-or-drop every candidate on provable CURRENT employment at THIS company. This is the fabrication guard — these are strangers Nick cannot sanity-check from memory. Drop anyone without a citable current-employment quote. (scan-contacts Step 3.)
3. Rank survivors on role_proximity / warm_tie / reachability / personalization_surface (scan-contacts Step 4).

Report honest-signal handling exactly as `/scan-contacts` does (an `exa_error` or `all_filtered` is a tooling miss, NOT "nobody works here").

### Step 3: Select the draft set

Take the top **N** ranked survivors (N = `draft:N` arg, default 3). Skip anyone
whose `personalization_surface` is so thin that no citable hook is plausible — a
generic-coded email fails worse than one fewer draft. Note who you dropped and why.

### Step 4: Brief each one, then STOP for the spine (delegate to /cold-outreach Steps 4 and 5b)

**Batch does not exempt the `/cold-outreach` default (changed 2026-10-01): no draft is written
before Nick states the spine.** This step previously went straight from research to drafting; that
contradicted `/cold-outreach` Step 5b and is closed as of 2026-10-06.

For EACH selected contact:

- **Research-personalization gate** (`/cold-outreach` Step 4, item 1 below).
- **Outreach Brief** (`/cold-outreach` Step 5b): why-now, verified recipient facts, sourced proofs,
  positioning, the hook, hard don'ts. Write every Brief to the queue file (Step 5) with status
  `AWAITING-SPINE`.

Then **stop and ask Nick for the spine**: the organizing claim, the hook, the proofs, the ask. He
may give one spine that covers several contacts or one per contact. A contact with no stated spine
stays `AWAITING-SPINE` and gets no draft.

### Step 4b: Draft from the spine (delegate to /cold-outreach Steps 6-7)

For each contact whose spine Nick has stated, run the `/cold-outreach` drafting flow — do not
shortcut it, and do not batch-generate templated variants. Items 2-4 below run only here:

1. **Step 4 (research-personalization gate):** a real Exa pass on the company + this
   person; find a cited, specific hook (company's own words / a named project / a
   post). If no citable hook surfaces for a contact, mark that contact
   `NEEDS-RESEARCH` in the queue and move on — do NOT draft on the headline alone.
2. **Step 6 (draft from the matched `voice-reference.md` exemplar)** + the flow-gap
   guardrails (warm opener, no thesis-jargon recital, one resonance beat, tight length).
3. **Step 6b (substance-provenance audit):** per `framework/writing-discipline.md`
   (canonical for the `N`/`C`/`I`/`G` labels) plus the `/cold-outreach` slot table.
   A `G` in any blocked slot (identity / credibility / personalization / bridge / ask)
   means STOP for that contact — mark the slot `NEEDS-SPINE` in the queue, don't invent.
   **Batch amplifies this risk:** N drafts are audited in one pass with no per-contact
   dictation, so the temptation to let a `G` slide is highest here and the blast radius
   is N contacts, not one. `NEEDS-SPINE` is the correct outcome, not a failed run.
4. **Step 7 (quality gate + tonal self-check + Content-Rules Pass):** the four-question
   extraction gate (Why you / Why now / Why me / Why this class of role, each quoting the draft), the ex-colleague readability bar, AND the `/cold-outreach` Content-Rules Pass —
   rule-gate `framework/content-rules.md` to the cold-draft rules (`L2`/`L3`/`I1`/`A3`/`C1`/`C3`,
   plus `G2`/`G3`/`H6` as they apply) per contact. Record the content-rules verdict in each
   contact's queue row; don't drop it just because this is a batch.

**Attachment default: none.** Per `/cold-outreach` Step 8 — do not attach a CV on
first contact. If a general deployment CV exists (`output/deployment-strategist/…magnuson.pdf`),
note it as "ready to send on reply," don't attach it.

### Step 5: Write the review queue file

Write all Briefs, and later the drafts, to `output/outreach-queue/MMDDYY-<company-slug>.md` (create the
`output/outreach-queue/` directory if needed). Format:

```markdown
# Outreach Queue: <Company> — <YYYY-MM-DD>

**Source:** contact_finder.py → evidence gate → rank → brief → spine → draft (/outreach-batch)
**Status:** REVIEW — none sent. Approve/edit/send each below individually.
**CV:** <path to general deployment CV, or "none"> — ready to send on reply, NOT attached.

---

## 1. <Name> — <Role> (rank <Total>/40)
**LinkedIn:** <url> · **Evidence:** "<current-employment quote>"
**Status:** AWAITING-SPINE | DRAFTED | NEEDS-RESEARCH | NEEDS-SPINE

**Outreach Brief:** <why-now · verified recipient facts · sourced proofs · positioning · hook · hard don'ts>

**Spine (Nick's, verbatim):** <organizing claim · hook · proofs · ask, or blank while AWAITING-SPINE>

**Subject:** <subject, after the spine>

<full draft body, after the spine>

**Provenance audit:** identity → C · credibility → C · personalization → I (<source URL>) · ask → N/C
**Quality gate:** Why you? "<quoted sentence>" · Why now? "<…>" · Why me? "<…>" · Why this class of role? "<…>"
**To send:** write this subject+body to `tools/.pending-draft.txt` (TO blank), write
`tools/.pending-draft.source` (`outreach-batch` + timestamp), run `python3 tools/open_draft.py`.

---

## 2. <Name> — …
```

Contacts that hit a `NEEDS-RESEARCH` or `NEEDS-SPINE` stop appear in the queue with
that flag and no body, so Nick can decide whether to source the missing piece.

### Step 6: Present summary + send instructions

Show a compact table (rank, name, role, status, subject once drafted) and point Nick to the queue
file. After Step 4 the table shows Briefs awaiting his spine; after Step 4b it shows drafts. Remind him: review/edit in the file, then to send any one, either invoke
`/cold-outreach "<Name>" "<Company>"` (which reopens the full single flow) or use
the per-contact "To send" stub. **This skill never opens Gmail or sends.**

### Step 7: Logging

Do NOT auto-log to `data/networking.md` / `data/outreach-log.md` at batch time —
these are drafts, not sends. Logging happens per-contact when Nick actually sends
(handled by `/cold-outreach` Step 9, or log manually on send). You MAY add gated
contacts to `data/networking.md` as `Source: exa-scan` rows (as `/scan-contacts`
Step 6 does) if Nick asks — otherwise leave the roster untouched.

## Notes

- **No auto-send is a hard invariant of this skill.** The whole point of a review
  queue is a human gate between batch generation and Nick's outbox.
- Public-repo PII gate: examples here are placeholders; real names appear only at
  runtime in `output/outreach-queue/` (gitignored output). Run `/audit-pii` before
  committing any change to this skill.
- Keep N small (≤6). Batch drafting runs a genuine per-contact research pass; it is
  not a mail-merge. Quality per draft > volume.
