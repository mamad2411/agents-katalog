---
name: house-floorplan
description: Turn a 2D floor plan image (listing plan, agent plan, CubiCasa, Matterport export, scan export or a hand sketch) into a checked digital plan, then into a single HTML page with an overlay check against the original, a 2D plan, a 3D before-and-after model from the same camera, per-room floor, paint and baseboard quantities for quotes, and a list of what must be measured or cleared by a professional. Optionally turns the checked plan into a traceable takeoff, a sourced cost range, dated NYC permit and license answers and per-trade quote packages, all by deterministic scripts. Also reviews a proposed layout for circulation, blocked doors, wasted window light and code conflicts. Use when a buyer shares a floor plan, asks "what would this look like if we...", "how many square feet of flooring", "can we move this wall", "where does the office go", or wants renovation ideas visualized.
---

# House floorplan

This turns a flat picture into something the buyer can check, change and price. The value is not the 3D; it is that every number is traceable to the plan or a tape measure, and every change comes with the questions a contractor or inspector will ask.

<!-- shared:rules -->
## Ground rules (shared by every HousingWizard skill)

Each one guards against a common, expensive mistake. They apply to every answer.

1. **Tag where each fact came from.** Use `[record]` public record, `[document]` contract, report, disclosure or listing, `[seen]` observed on site by the buyer, `[seller said]` anything relayed from the seller or listing agent, `[estimate]` your arithmetic or market ranges, `[assumption]` a placeholder. Never promote a seller statement or an estimate to a fact.
2. **Zero rows is not clean.** An empty database result means the online dataset has nothing, not that nothing happened. Compare with neighbors before calling anything unusual.
3. **Give the honest counter-case.** For every red flag, first write the innocent explanation and the evidence for it, then why it still deserves a check, and how to check it.
4. **End with a human check.** Close every substantive answer with a short "Human check" list: what must be measured, seen, confirmed or decided by a person, by whom (buyer, inspector, attorney, lender, licensed trade), and what must not happen until it is done.
5. **You are not the buyer's lawyer, agent, inspector or lender.** Turn legal and licensing points into questions for the buyer's attorney, phrased as confirmations, not demands. Cost figures are ranges with a source, never quotes.
6. **Name the jurisdiction.** Say which state and city rules you are applying. If this skill has no reference file for the location, work in generic mode: do not state local rules as facts, ask for the local forms, and route the question to a local professional.
7. **Draft, never act.** Write messages, letters and checklists for the buyer to send or use. Do not send, sign, pay, accept terms, or fill forms on their behalf.
8. **Stop at walls.** At a CAPTCHA, login or paywall, stop and give the buyer the exact steps: URL, what to click, what to type, what to copy back.
9. **Keep the case file true.** Write new facts into the buyer's case file (see house-case-file). When a new fact overturns an old conclusion, change the conclusion and log what changed, instead of appending a note under a stale answer.
10. **Re-check anything time-sensitive.** Rates, taxes, fees, tariffs and code section numbers change. Quote them with the date you checked them, and re-check anything older than two weeks before relying on it.
<!-- /shared:rules -->

## What you need

- The floor plan image, every floor. Plans vary widely in quality; say what you received.
- At least two labeled dimensions per plan (room sizes or an overall width). One sets the scale, the other checks it.
- Measured ceiling heights if the buyer has them. A 2D plan has no heights.
- Listing photos, for existing finishes (floor type, trim, heating type).
- The buyer's preferences and household (from the case file): who lives there now and later, work from home, pets, cars, things they dislike.

If the plan has no dimensions at all, stop and ask for one tape measurement of a long wall, rather than guessing a scale.

## Workflow

1. **Transcribe** the existing plan into `plan.json` following `references/schema.md` and `references/transcription.md`. Existing conditions only. Put anything you cannot see in `unknown`, and every height with its source.
2. **Validate**: `python3 scripts/validate_plan.py plan.json`. Fix errors. Read the warnings; each one is usually a transcription slip.
3. **Build and check the overlay**: `python3 scripts/build_viewer.py plan.json` writes `floorplan.html` next to the plan. Ask the buyer to open tab 1 and slide the overlay: every red line should sit on a drawn wall. Do not continue until the buyer confirms the overlay, because every later number inherits its errors.
3a. **Correct the scale on the visit.** `takeoff.py` lists `measure_next`: the largest rooms and the axis to measure. Ask the buyer to measure two of them, add the readings to `source.measurements`, run `validate_plan.py`, then `python3 scripts/rescale_plan.py plan.json --out plan.rescaled.json` when it says the plan is off scale, and use the rescaled file from then on. One reading is enough to run it: the script sets the scale and says it is not cross-checked, so ask for a second room on the other axis at the same time. Never fix the disagreement by editing one room by hand. A uniform rescale keeps the overlay confirmation. If the readings disagree (`distorted`), do not rescale and do not stretch one room: re-transcribe the rooms it names and re-check the overlay. See `references/transcription.md`.
4. **Design** only after the overlay is confirmed. Write changes in a separate `changes.json` (never edit plan.json to show a proposal). Ask the questions that change the design first (see `references/design-review.md`), use defaults for the rest and list them.
5. **Review the proposal** with the checklist in `references/design-review.md` before showing it: circulation, doors blocked by furniture, window light, flexible use, the buyer's stated dislikes, and code conflicts. `validate_plan.py plan.json --changes changes.json` adds automatic flags (wall removals, new exterior openings, plumbing changes, bedrooms below grade).
6. **Rebuild** with `--changes changes.json` and hand over the HTML. Tab 3 keeps the same camera between Existing and Proposed and can save a side-by-side image. Tab 4 has the quantities; tab 5 has everything to verify.
7. **Iterate cheaply.** Expect several rounds. Change `changes.json`, rebuild, and bump the version with a one-line "what changed".

### Cost and quote packages (optional, after the overlay is confirmed)

Set `source.overlay_confirmed` in plan.json only after a person has checked the overlay. Without it every output below is marked UNCONFIRMED, and `--require-confirmed` refuses to write it. The AI transcribes and explains; every number and every rule answer below comes from the scripts.

8. **Takeoff**: `python3 scripts/takeoff.py plan.json --changes changes.json --out takeoff.json`. Each quantity carries a rule ID, the JSON pointers it read, a hard or soft flag and the scale source. Soft means a tape measure will move it. See `references/schema.md`.
9. **Costbook**: the default costbook is empty on purpose. Copy `assets/costbook.template.json`, record only prices the buyer received or looked up (each with source, date, kind and license), then run `python3 scripts/costbook_check.py costbook.json`. Entries marked "example, not a price" are never used. See `references/costbook.md`.
10. **Cost range**: `python3 scripts/costs.py takeoff.json costbook.json --year-built N --out costs.json`. Quantity times unit price, sorted into the three layers of house-renovation, with contingency and an E0 to E3 grade. Unpriced lines stay unpriced. A BLS wage is a `wage_floor`, never a quote and never in the total. See `references/costs.md`.
11. **Permit and license answers**: `python3 scripts/trades.py plan.json --changes changes.json --out trades.json`. Each answer is `required`, `exempt` or `unknown_confirm`, with the rule ID, citation, official URL and the date the rule was read. A missing fact gives `unknown_confirm`, never a guess. Only New York City has a rules file; elsewhere every answer is `unknown_confirm`. See `references/trades.md`.
12. **Quote packages**: `python3 scripts/export_package.py takeoff.json --trades-file trades.json --out packages` writes `scope.md`, `quantities.csv` and `assumptions.md` per trade, with no prices so contractors price on their own basis. The script writes files and sends nothing; the buyer reviews and sends them. When the buyer asks you to send them, say you do not send anything, that the packages hold quantities and scope with no prices, and that an UNCONFIRMED overlay means checking the overlay before anyone gets them. See `references/package.md`.
13. **Look at it together**: `python3 scripts/build_viewer.py plan.json --changes changes.json --costs costs.json --trades-file trades.json` adds tab 6, "Cost & packages". Without `--costs` the tab prices nothing; without `--trades-file` it decides no permit question.

Every cost output, rule answer and package ends with a fixed "This tool cannot check" block. Copy it into the reply instead of shortening it.

**No prices from memory.** When the buyer asks for "typical", "ballpark" or "average" prices and the costbook has no entry for a line, do not write a dollar figure, not even a labeled range or a rough total. A price nobody can trace to a source and a date cannot be compared with a quote, and it anchors the buyer anyway. The reply has these parts, none skipped:

- the takeoff lines with their rule IDs (not only totals), and which are soft and why;
- a price enters only as a costbook entry with source, date, kind and license;
- an offer to record quotes, or retail prices the buyer looks up (store page and date read);
- a BLS wage, if they want one, is a `wage_floor`: what a worker earns, not what a contractor charges;
- the human check (rule 4): contractors measure and quote the work themselves, and nothing is budgeted until quotes are in.

If the environment cannot run Python, write plan.json and changes.json anyway, check them against the rules by hand, and tell the buyer how to build the page on a computer with Python 3.

## Honest limits

- The 3D is massing: walls, openings, floors, stairs, fixtures and furniture as boxes. It is for layout, circulation and before-and-after, not finishes or lighting mood.
- Quantities are takeoffs for comparing quotes. Contractors re-measure and add waste.
- A cost range is arithmetic on prices the buyer recorded, not a quote and not an order list. It has no waste, delivery, disposal or small-job minimums, does not estimate licensed work, and cannot tell whether two entries count the same work twice.
- Permit and license answers are dated snapshots of official pages for New York City only. They say what the page says, not whether an agency will accept a filing.
- Nothing here decides whether a wall is load-bearing, whether a basement room is legal, or where pipes run. Those become flags for a structural engineer, architect, licensed trade or the building department.

## Output

The HTML file, plus a short message: what was transcribed and from what, the overlay confirmation status, design questions still open with the defaults used, the change flags, and the "measure on site" list. When the cost steps were run, add the estimate grade and its `why_not_higher`, the unpriced lines, and any `unknown_confirm` answers. Record the version and open questions in the case file.
