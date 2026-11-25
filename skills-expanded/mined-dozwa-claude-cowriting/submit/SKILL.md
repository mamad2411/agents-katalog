---
name: submit
description: Pre-submission run of the whole paper, as one checklist. The Integrity Guardian's check, the consistency report, open markers and unverified references, the AI log's open turns and whether the disclosure is current. Use when a draft is about to leave the house (supervisor, co-authors, journal, examination office).
argument-hint: "[target: journal, thesis, …]"
---

# Pre-submission run

The author is about to hand the paper on. Gather what is still open, in one checklist with locations. Change nothing, write no text for the paper, fix nothing yourself: every item names what the author does next.

Target, if given: `$ARGUMENTS` (a journal, "thesis", "examination office", a funder). Ask for it only if nothing is given and a check below needs it.

The paper folder is the active paper (`paper.json`; `/cowrite:paper` if there is none). Run the parts that are independent at the same time:

1. **Integrity.** Start the `cowrite:integrity-guardian` agent on the whole manuscript (one Agent call, the task naming the paper folder and the target). Keep its top issues as they are.
2. **Consistency.** Invoke the `cowrite:consistency` skill (terms, abbreviations, cross-references, citekeys, figures and tables) and keep its findings.
3. **Open markers.** Grep `manuscript/` for `TODO`, `FIXME`, `XXX`, `??`, `UNVERIFIED`, `[AI-TEXT]`, `citation needed`, `\todo{` and `\xxx{`. List each with `file:line`. An `[AI-TEXT]` passage must be disclosed; `UNVERIFIED` references must be checked or removed.
4. **References.** If `literature/` holds a bibliography (`.bib`, CSL `.json`, `.ris`, `.nbib`), run `python3 "${CLAUDE_PLUGIN_ROOT}/tools/verify_refs.py"` and list every entry that is not `OK`: `MISMATCH`, `NOT FOUND`, `NO DOI` (with the DOI Crossref suggests, where it does), `ERROR`. Point to `/cowrite:sources` for the fixes.
5. **AI log and disclosure.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" stats`. Report unannotated turns (`/cowrite:annotate`), changes to the author's files that happened during AI tool calls (the author checks the git history and says what remained), and whether `disclosure/ai-register.*` exists and is younger than the newest log entry (`/cowrite:disclosure` if not, and if the target asks for the prompts, the prompts appendix too).
6. **Target rules**, if the target is known: name the rules you know apply (word or page limits, reporting guideline, reference style, AI policy, authorship statement) and look up the current policy when the target is a journal or a named institution, citing where you found it. Mark what you could not verify `UNVERIFIED`.

Then give one checklist, grouped in that order, each item either ✓ (nothing open) or ☐ with the location and the author's next step. Close with the count of open items and the three the author should take first. Everything in it is a finding for the author to act on; nothing here is a judgement of readiness, which is theirs and their supervisor's.
