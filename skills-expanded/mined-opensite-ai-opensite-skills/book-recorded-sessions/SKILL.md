---
name: book-recorded-sessions
description: "Plan, record, and merge recorded sessions into book chapters: solo lessons, interviews with a proxy reader, multi-guest panels, or hybrid lesson-plus-conversation episodes that also serve video and short-form clips. Covers contract-driven run-of-show, contributor releases and employer clearance, per-speaker capture and transcripts, speaker-attributed atoms, merging many sessions into a traceable chapter, and clip hand-off flags. Use when chapters are built from spoken recordings or podcasts. Not for narrating the finished audiobook or editing clips."
compatibility: "Python 3.9+ with PyYAML. Any multitrack recorder and any transcription tool that exports VTT or SRT."
metadata:
  version: "2.1"
  suite: book-publishing-system
---

# Recorded sessions to chapters

A good conversation is not a chapter. Design each recording from the chapter contract, capture
every speaker on their own track, and merge by tracing every paragraph back to someone's
recorded words. The author teaches; guests contribute cases, and their words are credited.

## Procedure

1. **Pick the format per chapter** using `references/session-formats.md`: solo, interview (author
   plus a proxy reader), panel, or hybrid (part A lesson with a proxy reader, part B conversation
   with practitioners). Default for a teaching book with guests: hybrid.
2. **Contributors and rights first.** List everyone in `01-evidence/CONTRIBUTORS.csv` (role,
   attribution, speaker labels, rights_id). Before recording, each guest signs a release and the
   employer clears the session when recorded on company time or premises or about company work:
   `references/contributor-release.md`. Track each release as a `RIGHTS_LEDGER.csv` row.
3. **Plan.** Register the session in `01-evidence/SESSIONS.csv`, then
   `python scripts/session_plan.py <root> --chapter ch01 --format hybrid --session-id S01 --out 01-evidence/raw/sessions/S01/RUN_OF_SHOW.md`.
   It fails if the chapter contract is incomplete or a needed role is missing.
4. **Record** to the capture spec in `references/session-formats.md`: one microphone per speaker
   on its own track, slate, room tone, and segment markers dropped by the producer.
5. **Ingest.** Put one transcript per track (`<label>.vtt` or `.srt`) and `markers.csv`
   (segment_id,start) in the session folder, then
   `python scripts/session_ingest.py <root> --session S01 --watchlist <confidential terms> --json 06-production/reports/session_S01.json`.
   It writes `timeline.csv` and `segments.csv` (clip candidates flagged for claim checks and
   clearance) and reports talk share per speaker.
6. **Atomize** into `01-evidence/ATOMS.csv` with `speaker` (contributor_id) and `session_id`; run
   `book-author-source-capture/scripts/atom_coverage.py`. Record short solo pickups for gaps.
7. **Merge** chapters with `references/merge-rules.md`: the author's lesson is the spine; guests'
   cases appear as credited quotes or credited paraphrase. End every paragraph with
   `<!-- src:A-0012 -->` (same paragraph, comma-separated for several atoms). Composed
   connective text goes in `{{ai}}...{{/ai}}` for the author to rewrite (mode T).
8. **Trace.** `python scripts/chapter_trace.py <root> --json 06-production/reports/chapter_trace.json`
   before G4; with `--lock --json 06-production/reports/chapter_trace_lock.json` before G6.
9. **Clips hand-off.** Give `segments.csv` to the clipping workflow. Do not publish a segment
   flagged `needs_claim_check` until its claims pass `book-evidence-factcheck`, or one flagged
   `needs_clearance` until the owner clears it.

## Acceptance evidence (external)

- Signed releases and employer clearance on file before any guest's words are used.
- `atom_coverage.json` passes from session atoms; `chapter_trace` passes (draft at G4, lock at G6).
- The contributors approve their credited quotes in writing; independent readers judge the
  chapters in beta rounds. Colleagues on the show are not validators.

## Never

- Put a guest's experience in the author's mouth, or build composite quotes or people.
- Record or use a guest's words without a signed release; publish client names, deal terms, or
  internal numbers without written clearance.
- Treat a transcript cleanup as a chapter: no merge without the contract, trace, and fact-check.

## Files

- `scripts/session_plan.py` — chapter contract to run-of-show; checks roles, releases, coverage.
- `scripts/session_ingest.py` — per-speaker transcripts to timeline, talk share, segment flags.
- `scripts/chapter_trace.py` — paragraph-level trace, guest release and credit checks, author share.
- `assets/segment_types.yaml` — segment library and format timings used by session_plan.py.
- `references/session-formats.md` — formats, roles, capture spec, time budget. Read at step 1.
- `references/merge-rules.md` — how to merge sessions into a chapter. Read at step 7.
- `references/contributor-release.md` — release and clearance checklist. Read at step 2.
