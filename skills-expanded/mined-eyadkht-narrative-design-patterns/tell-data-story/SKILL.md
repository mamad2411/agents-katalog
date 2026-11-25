---
name: tell-data-story
description: Picks 2-3 narrative design patterns suited to the user's data and goal, then generates a standalone HTML page demonstrating them on that data. Use when the user shares a dataset (CSV, PDF, table, JSON, text), screenshot of numbers, or describes data and asks how to present it, communicate it, make it memorable, persuasive, or emotionally resonant. Pass a pattern name or number as the argument to apply a specific pattern directly instead of auto-picking.
argument-hint: "[pattern-name-or-number]"
allowed-tools: Read Write Bash(python3 *) Bash(head *) Bash(wc *) Bash(file *)
---

# Tell Data Story

Turn raw data plus a goal into a one-page interactive story built from 2-3 narrative design patterns. The output is a single self-contained HTML file the user can open in a browser, send to a colleague, or paste into a CMS.

## Inputs

The user provides:
1. **Data** — file path to CSV/PDF/JSON/Markdown table, a pasted table, or a verbal description of numbers.
2. **Goal and audience** — what they want the reader to take away, and who that reader is. If missing, ask in Step 2.

Optional `$ARGUMENTS`: a pattern name (`compare`, `concretise`) or pattern number (`13`, `08`). Empty argument means auto-pick mode.

## Workflow

Copy this checklist into your response and tick boxes as you go:

```
- [ ] Step 1: Read the data and note its shape
- [ ] Step 2: Clarify takeaway, audience, format (skip questions already answered)
- [ ] Step 3: Confirm the goal back to the user before going further
- [ ] Step 4: Propose patterns (direct from $ARGUMENTS, or auto-pick 2-3) and get sign-off
- [ ] Step 5: Generate narrative-output.html from template.html
- [ ] Step 6: Report picks, rationale, and output path
```

### Step 1 — Read the data

- **CSV, JSON, Markdown, plain text**: read directly with the Read tool. Note row count, column names, key dimension (time, category, geography), magnitude range, and any obvious outliers.
- **PDF**: try `python3 -c "import pdfplumber, sys; print(pdfplumber.open(sys.argv[1]).pages[0].extract_text())" <path>`. If pdfplumber is not installed or extraction fails, ask the user to paste the key rows.
- **Pasted table or verbal description**: work from what they gave you; ask for a sample if it is too abstract to choose patterns from.

State the shape back in one sentence so the user can correct you before pattern selection.

### Step 2 — Clarify intent

If the user has not already said, ask up to three questions in a single message. Do not ask more than three. Skip any that are already answered:

1. **Takeaway** — In one sentence, what should the reader walk away thinking?
2. **Audience** — General public, technical/expert, internal decision-makers, or something else?
3. **Format** — Where does this live? Slide, blog post, social share, internal report, exhibit panel?

### Step 3 — Confirm the goal

Before picking patterns, mirror the brief back to the user in 2 to 4 short lines, then stop and wait for confirmation. Do not move on until they reply.

Use this shape:

> **Data:** one line restating the shape (rows, dimension, range).
> **Takeaway:** the one-sentence message you'll build the story around.
> **Audience and format:** who it's for, where it lives.
>
> Sound right, or want to adjust before I pick patterns?

If the user corrects anything, update your understanding and re-confirm only if the change is material (different takeaway, different audience). Small wording tweaks do not need a second round.

### Step 4 — Propose patterns and get sign-off

**If `$ARGUMENTS` is non-empty** (direct mode):

- Match against the list in **Available patterns** below. Accept the id (`13-compare`), the short name (`compare`), or the number (`13`).
- If no match, stop and list the 18 valid names so the user can retry.
- Apply that single pattern. Skip auto-pick heuristics. Still walk the user through it (one or two sentences on why it fits their data) and ask for the green light before generating.

**Otherwise** (auto-pick mode), choose **2 to 3** patterns. Use these heuristics, then read [patterns.md](patterns.md) for the candidates' full `why` and `how` before finalising:

- **Persuade / argue a point** → Argumentation: `01-repetition`, `02-silent-data`, `13-compare`
- **Make scale or magnitude land** → Emotion: `08-concretise`, `05-humans-behind-the-dots`
- **Pull the reader in, let them play** → Engagement: `03-exploration`, `04-users-find-themselves`, `16-make-a-guess`
- **Sequence complex material** → Flow: `06-gradual-reveal`, `07-speed-up-slow-down`
- **Shift perspective, reframe** → Framing: `09-familiarisation`, `15-defamiliarisation`, `14-convention-breaking`, `17-physical-metaphor`
- **Move the reader to act** → Engagement: `18-call-to-action`
- **Empathy / personal stake** → Emotion + Framing: `11-breaking-the-4th-wall`, `12-addressing-the-audience`

Selection rules:
- Prefer patterns whose `categories` (in [patterns.md](patterns.md)) align with the stated goal.
- Diversify: when two patterns serve the same purpose, prefer the pair that covers different categories so the story has both head and heart.
- Match data shape: small-multiples-able data favours `01-repetition`; two-entity comparisons favour `13-compare`; sequential or time-series data favours `06-gradual-reveal`; large counts of people or events favour `05-humans-behind-the-dots` or `08-concretise`.

For each pick, write **one sentence of rationale that names the user's specific data and goal**, not a generic restatement of the pattern. Bad: "Use Compare to show the difference." Good: "Use Compare so the 3 % marketing spend sits next to the 47 % salary line at the same scale, and the gap becomes the chart."

Then present the proposal to the user as a short bulleted list (pattern name, one-sentence rationale each) and ask:

> Happy with these, or want to swap one out? I'll generate the page once you say go.

Wait for a green light before Step 5. If they swap a pattern, update the list and re-confirm. If they say go, proceed.

### Step 5 — Generate output

1. Read [template.html](template.html).
2. Fill placeholders:
   - `{{TITLE}}` — short headline derived from the user's takeaway.
   - `{{TAKEAWAY}}` — the takeaway sentence verbatim.
   - `{{PATTERN_BLOCKS}}` — one `<section class="pattern-demo">` per selected pattern, in the order the story should be read. Each block contains:
     - Category pill (use the primary category from [patterns.md](patterns.md))
     - Pattern title and number
     - **Why this pattern** — one or two sentences pulled and tightened from the pattern's `why`
     - **Applied here** — one or two sentences naming the user's data and the specific move
     - A **working demo** built from the user's actual data: inline SVG, HTML, and JS. No frameworks, no external CSS, no build step. Match the visual language defined in [design-system.html](design-system.html): Fraunces headings, monospace labels for axes/captions, the paper/ink/category tokens already inlined in `template.html`, yellow `.hl` only as a background behind text, soft `.demo-frame` panels for chart areas.
3. Write the filled-in file to `narrative-output.html` in the current working directory. Overwrite if it exists.

Critical: the demo must use the user's numbers, not the example data from the pattern's catalog entry. The catalog's `example` field is a reference to existing work, not data to copy.

### Step 6 — Report

In your final response, give the user:
- A bulleted list of the 1-3 patterns picked, each with the one-sentence rationale from Step 3.
- The output path (`./narrative-output.html`).
- One line telling them to open it in a browser.

Keep the report short. The HTML is the deliverable.

## Available patterns

Use these ids (or the bare number / short name) for `$ARGUMENTS` matching. Full `why` and `how` for each in [patterns.md](patterns.md).

- `01-repetition` — Repeat one motif across small multiples until the pattern feels inescapable.
- `02-silent-data` — Ghost a data point, then reveal it for shock.
- `03-exploration` — Let the reader filter and drill in.
- `04-users-find-themselves` — Reader locates their own dot in the population.
- `05-humans-behind-the-dots` — Hover a dot, meet the person.
- `06-gradual-reveal` — Layer complexity one beat at a time.
- `07-speed-up-slow-down` — Control playback tempo to spotlight dense moments.
- `08-concretise` — Translate abstract magnitude into a familiar physical equivalent.
- `09-familiarisation` — Re-label the chart around the reader's own reference point.
- `10-rhetorical-question` — Open with a question, deliver the answer in the chart.
- `11-breaking-the-4th-wall` — A subject inside the chart turns and addresses the reader.
- `12-addressing-the-audience` — Rewrite copy in the second person.
- `13-compare` — Two things at the same scale; the disparity is the chart.
- `14-convention-breaking` — Set up a chart convention, then break it.
- `15-defamiliarisation` — Re-draw something familiar strangely.
- `16-make-a-guess` — Reader draws their prediction; reveal the truth over it.
- `17-physical-metaphor` — Direction carries feeling: up is good, down is bad.
- `18-call-to-action` — End with one specific, low-friction next step.

## References

- Full pattern catalog with `why`, `how`, and a real-world example for each: [patterns.md](patterns.md)
- Output scaffold with the design tokens inlined: [template.html](template.html)
- Visual language reference (colors, type, components, motion). Edit this file to retheme the skill; keep token names stable so `template.html` stays in sync: [design-system.html](design-system.html)
