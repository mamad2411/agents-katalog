---
name: client-journey
description: Generate a multi-year synthetic financial-advice client journey as full-length meeting transcripts. Produces a thin seed file of basic client details as copy-pasteable key-value lines, then one long adviser-to-client conversation per meeting, an onboarding followed by annual reviews, each carrying every fact for that year in the dialogue itself. Use for realistic fact-find test data, demo client histories, or ground truth for document extraction pipelines.
---

# Client Journey Generator

Invents a household and writes their financial life as **meeting transcripts**.

The transcript is the product. Everything the pipeline is meant to extract must
be spoken aloud in the conversation, because the conversation is the only thing
that gets uploaded.

## Output, and nothing else

```
<output_dir>/client-journey-<surname>-<YYYYMMDD-HHMM>/
├─ seed.md                              basic client details, one per line
├─ 01-onboarding-<YYYY-MM-DD>.docx
├─ 02-annual-review-<YYYY-MM-DD>.docx
└─ ...
```

One seed file. One file per meeting. That is the whole output.

Do **not** produce meeting notes, a JSON ledger, a summary document, or markdown
copies alongside the `.docx` files. Write each transcript's markdown to a
temporary path, render it, and delete the markdown. The user gets the docx.

`.docx` is used because document upload paths accept `.docx` or `.pdf` only.

## Inputs

Parse the user's free text. Every input has a default, so `/client-journey` with
no arguments is valid. State which defaults you used, in one line, at the end.

| Input | Default | Notes |
|---|---|---|
| `people` | **1** | Number of **clients**, excluding the adviser. Default is 1, giving a two-person adviser-and-client conversation. 2 is a couple. 3+ adds an adult child, parent or business partner. Only use more than 1 if the user asks for it |
| `meetings` | 5 | First is onboarding, the rest annual reviews |
| `start_year` | today minus (`meetings` - 1) years | So the final meeting lands near today |
| `output_dir` | `~/Downloads` | A new timestamped directory is created inside it |
| `region` | UK | Currency, tax wrappers, product names |
| `wealth` | mass affluent | `emerging`, `mass affluent`, `high net worth` |

## Procedure

### Step 1. Write seed.md

`seed.md` is **basic details only**, so it can be copied straight into a CRM.
One fact per line, `Key: value`, no tables, no prose, no plan. Open with a
journey line of one or two sentences and nothing more.

All dates are **DD/MM/YYYY**.

```markdown
# <Full name>

Journey: <one or two sentences. Who they are and what happens across the years.>

Full name: Nadia Claire Farrow
Known as: Nadia
Date of birth: 14/03/1985
Gender: Female
Marital status: Divorced
Nationality: British
Country of residence: United Kingdom
Email: nadia.farrow@outlook.com
Mobile: 07793 441602
Address line 1: 27 Bellingham Road
Address line 2: Redland
City: Bristol
Postcode: BS6 6QN
National Insurance number: NR 82 44 17 C
Occupation: Senior Radiographer
Employer: University Hospitals Bristol NHS Foundation Trust
Client since: 14/09/2022

Dependant 1 name: Isla Grace Farrow
Dependant 1 date of birth: 02/05/2016
Dependant 1 relationship: Daughter

Adviser: Gareth Hollis
```

Add a line only if a CRM would hold it. Financial detail belongs in the
transcripts, not here: meeting one is what fleshes the record out. Keep the
whole file under about forty lines.

### Step 1b. Plot the arc in a scratch file

Plot the entire arc **before writing any transcript**. Plotting first is the
only thing that stops meeting four contradicting meeting two.

Write it to a scratch path outside the output directory, for example
`/tmp/<surname>-arc.md`: one line per meeting giving date, type and that year's
beat, then a table of every figure that moves across the years so the meetings
have something to agree on.

Read `references/fact-domain.md` for what a fact-find holds, and
`references/life-events.md` for beats. Choose beats that interact: a promotion in
year two makes an allowance problem in year four, an inheritance in year three
creates the estate conversation in year five.

Check the arc against the coverage table in `references/continuity-rules.md`
before writing anything.

**Delete the scratch file at the end of the run.** It is working material, not a
deliverable. The user asked for a seed and some transcripts.

### Step 2. Write each meeting in sequence

**Never generate meetings in parallel.** Parallel generation produces
transcripts that are individually plausible and collectively contradictory,
which is the exact failure this exists to prevent.

For each meeting in order:

1. Read `seed.md`, the arc scratch file, and every transcript already written.
   Those are the state.
2. Write the full conversation, following `references/transcript-anatomy.md`
3. Render to `.docx` with `scripts/write_docx.py` and delete the markdown

### Step 3. Validate and report

Run the checks in `references/continuity-rules.md`. Fix what fails. Then tell
the user the directory, the meeting list, and the defaults applied. Nothing more.

## Write the whole conversation

This is the point of the skill and the thing most likely to go wrong.

A real first meeting runs an hour and a half. **Onboarding must be 6,000 to
9,000 words. Annual reviews 3,500 to 5,000.** That is long, and it is meant to
be. A short transcript is a summary wearing a transcript's clothes, and it
carries none of the difficulty a real one does.

Absolutely forbidden in the output:

- `[conversation continues]`, `...and so on`, `[remainder of discussion]`
- Any bracketed stage direction standing in for dialogue that should be written
- Skipping the middle of a meeting to reach the actions
- Summarising a topic instead of having the two people talk through it

If the transcript feels long while writing it, it is approaching correct. Write
every turn. Do not stop early, and do not compress to save effort.

## Hard rules

**Everything is spoken.** If a fact is not said out loud by someone in the room,
it does not exist. There is no notes document to fall back on.

**Money carries forward.** A figure stated in one meeting stays that figure in
the next unless someone says it changed.

**Ages follow dates of birth.** Compute at each meeting date. Never restate an
age from an earlier transcript.

**Nothing disappears.** Policies, jobs and accounts get ceased, transferred or
surrendered, with a date and a reason.

**No tables in a transcript.** People do not speak in tables, and some `.docx`
extractors drop table content entirely.

**Vary the openings.** If every meeting starts the same way the corpus is
useless for testing.

## Rendering

```bash
python3 scripts/write_docx.py meeting.md meeting.docx
python3 scripts/write_docx.py --selftest
```

No dependencies. Supports headings, paragraphs, bullets and `**bold**`, which is
all a transcript needs.
