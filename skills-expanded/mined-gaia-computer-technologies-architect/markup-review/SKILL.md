---
name: markup-review
description: Collate comments from marked-up drawings into a numbered comment-response schedule, grouped by sheet and discipline, with a status and a draft response for each. Reads PDF annotations directly (bundled PyMuPDF script), a Bluebeam Markups List CSV export, or Bluebeam Revu through its MCP if connected. Use when the architect wants to "collate the markups", "go through the client's comments", "make a comments schedule", "respond to the consultant's markups", "what did they mark up on the drawings", or "track design review comments". Hands to rfi for queries that need a formal RFI, drawing-register-qa for issue-sheet checks, and project-email to send the responses.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Markup review

Turn a pile of red-pen PDFs into one schedule the team can work through: every comment numbered, located, owned, and answered or open. Nothing dropped, nothing invented.

## When to use

- A client, consultant, planner, or checker has returned marked-up drawings.
- Internal design review or QA markups need collating before the next issue.
- The team needs a comment-response schedule to send back with a revision.

## Input

Any of:
- **Marked-up PDFs.** Run [scripts/extract_annotations.py](scripts/extract_annotations.py) to pull every annotation into a CSV.
- **Bluebeam Markups List export** (CSV or XML from Revu's Markups List). Column names vary with the user's list setup. Map them to the schedule fields and say which column you used for each.
- **Bluebeam Revu MCP** (Revu 21.9+, Max plan), if connected: read markups through it.
- **Screenshots or scans** with handwritten marks: read them visually and mark every item "transcribed from image, verify".
- Optional: the drawing register (to name sheets), and who owns which discipline.

## Process

1. **Extract everything.** With PDFs: `uv run scripts/extract_annotations.py comments.csv --dir ./markups` (or list files). The script reports counts by markup type, graphic-only markups with no text, and pages with no text layer. Report those counts to the architect before going further.
2. **Clean, don't rewrite.** Keep each reviewer's words verbatim in the "Comment" column. Fix nothing except whitespace. Graphic-only markups (clouds, highlights, arrows with no text) get "graphic markup, see sheet" plus the text underneath, if the script captured it.
3. **De-duplicate carefully.** A highlight sitting under a text comment is often one comment, not two. Merge only when they overlap on the same sheet and the same author. Keep both IDs ("3, 4") so nothing disappears.
4. **Group** by sheet, then by discipline or topic (architecture, structure, MEP, landscape, client brief, planning). Ask who owns what if it isn't obvious.
5. **Classify** each comment:
   - **Action**: change the drawing.
   - **Query**: needs an answer, not a change. Escalate to `rfi` if it's a contractual query.
   - **Noted**: no action, acknowledge.
   - **Disagree**: the design team proposes not to act. A reason is required.
   - **Out of scope / other party**: belongs to another consultant.
6. **Draft responses** only where the answer is evident from what you have. Otherwise leave the response "[to answer]" and name the owner. Never invent a design decision.
7. **Check coverage.** The schedule's row count must equal the extracted count minus documented merges. State both numbers.

## Domain knowledge

- **PDF annotation types:** Text (sticky note), FreeText (typed on the sheet), Square/Circle/Polygon (clouds are usually Polygon or Square with a cloud border), Line/PolyLine (arrows, dimensions), Highlight/StrikeOut/Underline (text markups), Ink (freehand), Stamp. Measurement markups in Bluebeam carry a value in the comment or a separate column.
- **Author field** is whatever the reviewer's software had set. It may be a person, a company, or "Guest". Report it as given.
- **Flattened markups** (burned into the page) are not annotations. The script won't find them. If a sheet visibly has red marks but zero extracted markups, say it's probably flattened and needs a visual read.
- **Revision discipline:** responses go back with the revision letter they relate to. Record the revision of the marked-up sheet if known.

## Output format

```
## Comment-response schedule: [project] · [review name / date]

**Source:** [files / Bluebeam export / MCP] · extracted [n] markups · merged [m] · listed [n - m]
**Not readable:** [pages with no text layer, likely flattened sheets]

| # | Sheet | Rev | Discipline | Reviewer | Comment (verbatim) | Type | Response | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A-101 | P2 | MEP | MEP Eng | Check door swing clashes with WC | Action | [to answer] | Arch | Open |

**Summary:** [x] actions · [y] queries · [z] disagreements needing a reason · [n] open
**Needs a decision:** [comments where the team must choose before responding]
```

Offer the schedule as CSV or XLSX if the team tracks comments in a spreadsheet.

## What you don't do

- Don't paraphrase reviewer comments in the Comment column. Verbatim, always.
- Don't drop a markup because it seems trivial. Every extracted item is listed or explicitly merged.
- Don't write responses that commit the design team to a change nobody decided. Use "[to answer]".
- Don't answer structural, fire, accessibility, or code comments on the merits. Route them to the responsible consultant, marked "requires verification by a qualified professional."
