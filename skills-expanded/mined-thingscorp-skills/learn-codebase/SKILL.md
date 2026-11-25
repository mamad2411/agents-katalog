---
name: learn-codebase
description: >-
  use this when getting up to speed in an unfamiliar codebase — sibling
  workspace, MISSION structure, prove-it checks, not a map-only prompt
license: MIT
metadata:
  portability: portable
---
# learn-codebase

Get productive in an unfamiliar codebase with a structured, disk-backed workflow — not a one-off "draw me a map" prompt. Orientation only: for an honest feature inventory and test pass on a shipped product, use quality-loop.

## Setup
1. Leave the app repo; create a **sibling workspace** for learning notes. If you're already inside the app repo with a map-only prompt, stop — relocate. A directory map is not understanding.
2. Declare an **honest experience level** at the top of MISSION.md — newcomer, practitioner, or expert. Under/overclaiming breaks the depth calibration below.
3. Work the repo in leveled passes; advance a level only when you can **predict behavior** (see prove-it):
   - **Newcomer:** entry points, README, one end-to-end trace (request → data → UI).
   - **Practitioner:** data flow, test suite, team conventions.
   - **Expert:** edge cases, failure modes, the why-nots in the design.
4. Keep state on disk (so **clearing the session is safe**):
   - **MISSION.md** — learning goal + success criteria (re-read when lost)
   - **NOTES.md** — what you know / don't
   - **RESOURCES.md** — primary sources (official docs, links) found so far
   - **lessons/** — leveled lessons + shared exercise assets
   - **reference/glossary.html** — return doc
   - **learning-records/** — progress state across clears
5. Do the leveled passes above. Then **prove it** (reading ≠ learning): edit, run, and predict outcomes — e.g. add a `console.log("LOADER RAN")` in a loader and `console.log("COMPONENT RAN")` in a component; predict terminal vs browser; run and notice surprises. Do the edit when the pass calls for it.

## Exploration tactics
- Compare subagent exploration vs solo skim; note token cost of surface vs deep dive.
- Demand real file paths for round-trips (entry → data → UI → tests).
- Re-ask or verify with file reads when answers disagree.
- If a shape sketch helps: C4 **Context** then **Container** (a running app or store, not Docker). Stop there. A repo tree is not C4. Do not hand-draw Code diagrams.

## Done when
Real files identified, disk-backed MISSION/NOTES/RESOURCES/lessons/records in place, and at least one prove-it check run — not a chat-only architecture sketch.

## Anti-patterns
- Running a map-only prompt inside the app repo instead of relocating to a sibling workspace.
- Overclaiming experience — breaks depth calibration; underclaiming wastes a level.
- Calling a directory map or repo tree "understanding"; they are not C4 Context/Container.
- Hand-drawing Code diagrams.
- A chat-only architecture sketch with no prove-it check.

## Related
quality-loop (owns the inventory/test pass on shipped products) ·
session-hygiene · compact
