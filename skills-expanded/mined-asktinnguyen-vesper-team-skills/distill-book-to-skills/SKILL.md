---
name: distill-book-to-skills
description: "Turn any book or long document (PDF, epub, or text) into a usable Hermes skill family: extract the full text, map its structure (rules/index/chapters), design a router + per-part skills + a workflow/validation skill, then verify fidelity through self-critique and multi-subagent review. Use whenever a user hands you a book (or long reference doc) and wants its knowledge captured as reusable skills, e.g. 'turn this book into skills for X'."
version: 1.0.0
author: Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [books, knowledge-distillation, skills, pdf, workflow, validation, subagents]
    related_skills: [write-clearly, write-clearly-revise, google-workspace, ocr-and-documents]
---

# Distill a Book into a Skill Family

Reusable end-to-end pipeline for converting a book (or long reference document) into a
family of Hermes skills that faithfully carry its knowledge. Proven on Abbott's *How to
Write Clearly* → the `write-clearly` family (umbrella + words + word-order + brevity +
revise), where a 4-subagent review caught real errors that were then fixed.

## When to use
- The user says "turn this book/PDF into skills for <topic>," "capture this book as a workflow," etc.
- You have a long document whose knowledge should become reusable procedural skills, not just a summary.

## Pipeline

**1. Locate & extract.**
The source may be local (a drive/path) or online. For local PDFs use PyMuPDF —
`fitz.open(path)` then `page.get_text("text")` per page, preserving `===== PAGE N =====`
breaks, and write the full dump to a working file. (pymupdf is usually already importable;
else `pip install pymupdf`.) Confirm page count and char count. For a Google Drive path,
load the `google-workspace` skill and authenticate if needed — but first check whether the
user means a *local* drive (drive letter) rather than Google Drive, as "G Drive" often means `G:\`.

**2. Read & map the structure FIRST.**
Before reading the whole body, find the book's own index/TOC (rules, chapters, sections).
It gives you the skeleton. Search for the book's heading pattern (e.g. `RULE \d+`) and read
the index, THEN read each body section. You need the exact wording of each principle, not a
paraphrase — skim is not enough for fidelity.

**3. Design the skill family.**
A good shape (used for write-clearly):
- **Umbrella/router skill** — overview, the full index of principles, a "quick routing"
  section, and a pointer to per-part skills. Attach the *full book text* as a reference file
  (`references/<book>.txt`) so it's verifiable verbatim.
- **One skill per major part/section** — each carries the exact principles for that part,
  the book's own examples, and an operational "check" for applying each.
- **A workflow/validation skill** — how to apply the family, self-critique, and validate.
Keep rule/principle numbering faithful to the source.
Create each via `skill_manage(action='create', category=..., name=..., content=...)`; add
reference files via `skill_manage(action='write_file', ...)` or copy the extracted file in.

**4. Self-critique against the source (before subagents).**
Run an automated verbatim check: pick 30–50 example fragments you quoted, normalize
(uppercase + collapse whitespace), and assert they appear in the source dump. Catch
false negatives: inline annotation markers like `(a')`, punctuation differences, and typos
in your *own* check strings will trigger spurious misses — verify each "miss" manually
before treating it as a real error.

**5. Validate with parallel subagents (do not trust single-pass).**
Spawn independent reviewers via `delegate_task` batch mode (≤3 concurrent; two batches for
4 roles), giving each: the skill file paths, the source reference path, its role, and a
rule that it must quote both sides for any discrepancy and must NOT invent problems.
Recommended roles:
- **EVIDENCE** — index numbering/titles/categories match the book's index; example
  fidelity; author/title/date framing.
- **CLARITY** (or per-topic first reviewer) — each principle is faithfully encoded, not
  mangled.
- **SECOND-PART reviewer** (e.g. brevity) — covers the remaining section(s).
- **RED-TEAM** — attempt to break the set: instructions that would *produce* bad output,
  internal contradictions, unverifiable steps; also confirm earlier fixes are actually in
  the files.
Adjudicate every finding yourself: verify the cited rule against the source before
accepting. Separate **must-fix** (real meaning/attribution errors, wrong examples) from
**cosmetic** (dropped words, punctuation, labeling). Apply the accepted fixes via
`skill_manage(action='patch', ...)`.

**6. Polishing pitfalls from practice.**
- Check the book's **own formal numbering** before labeling parts (e.g. a book might number
  only two divisions I/II while you'd be tempted to say "Part III") — staying faithful here
  matters.
- Add a clarifying note when a book's example has an archaic/rare reading that a modern
  user could misapply (rather than silently "fixing" it).
- Give every instruction a concrete, verifiable rewrite target — a rule that says "reorder
  it" without showing the target is not checkable.
- Keep each subagent's context self-contained: it shares no conversation, so pass file
  paths and the source path explicitly; tell it the output language and that it must verify
  against the actual file.

## Pitfalls
- **Do not paraphrase principles you must preserve exactly** — quote the source, then add
  your operational gloss.
- **Subagent self-reports are not proof** — re-check their citations against the source file
  before trusting or acting on them.
- **Beware "my local G drive" vs "Google Drive"** — ask/verify the location before OAuth.
- **Excessive suspense / no escaping context** — the extracted text can be 200K+ chars; read
  it in chunked pages and keep the diagram/index in your head, not all prose in context.

## Verification
A build is "done" only after: (a) skill family listed via `skills_list`/`skill_view` with the
reference file present; (b) automated verbatim fragment check passes (or every miss manually
explained); (c) all four subagent roles report clean OR their findings are adjudicated and
fixed; (d) a final red-team pass confirms the fixes are actually present.
