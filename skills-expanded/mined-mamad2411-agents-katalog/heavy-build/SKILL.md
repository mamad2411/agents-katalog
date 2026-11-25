---
name: heavy-build
description: Author a new heavy prompt for your heavy/library/. Interviews you for the goal and shape, decomposes it into phases → idempotent steps with anchored output sections, encodes defaults so the run never needs to ask, assigns the next ID, writes the file, and updates the library INDEX. Run /heavy-review after.
---

# Heavy-prompt builder

Authoring tool. Runs **with you present**, so asking questions here is fine — the goal is to produce
a heavy prompt that is then **launched-and-left** with zero questions. Work in your project repo
(current working directory). Paths below are relative to its root (the library lives under `heavy/`).

## Step 1 — Load the conventions
Read these so the new prompt matches exactly:
- `heavy/library/_TEMPLATE.md` — the structure every prompt must follow (frontmatter + 7 sections).
- `heavy/README.md` — conventions (anchors, append-only, shared vocab, no-AskUserQuestion-mid-run, subagents off).
- `heavy/library/INDEX.md` — to find the **next ID** (highest existing NN + 1, zero-padded).

## Step 2 — Interview the user
Use `AskUserQuestion` (or plain prose Q&A) to settle, in this order — batch related questions:
1. **Goal** — the one outcome the run must produce (if `$ARGUMENTS` was given, start from that).
2. **Context** — what problem it serves; which repo files/areas it touches.
3. **Shape** — roughly what phases/stages the work has (you'll refine into steps).
4. **Subagents** — almost always `false` (default; keeps the whole run in one session). Only `true`
   if the user explicitly wants subagents and accepts that spawned agents add complexity and may
   bill differently from the interactive session.
5. **WebSearch** — does it need the web? set a sane `websearch_max` (0 if not).
6. **Cost** — rough `est_cost` (low/medium/high) from the scope.

If the user is vague, propose a concrete decomposition and confirm it — don't leave it open.

## Step 3 — Decompose into phases → steps
- Break the job into ordered **phases**; each phase = a list of **idempotent steps**.
- Give every step an id `<phase>.<step>` and a single defined **output** (a file + an anchored
  section `<!-- SEC:id -->`). Use the shared vocabulary where it fits: `summary`, `findings.*`,
  `decisions`, `actions`, `assumptions`, `sources`.
- The last phase is always `synthesize` (write/finish `00-summary.md`, regenerate `MAP.md`, update
  `heavy/output/INDEX.md`).

## Step 4 — Encode defaults for EVERY decision
This is the most important step. The run is unattended, so for any choice the prompt would otherwise
ask about, **write the default into the prompt** plus the rule "when uncertain, take the default and
record it under `<!-- SEC:assumptions -->`." A heavy prompt that needs a human mid-run is broken.

## Step 5 — Write the prompt file
Copy `_TEMPLATE.md` structure into `heavy/library/NN-slug.md` (slug = short kebab-case of the goal),
filled in: frontmatter (`id`, `title`, `goal`, `output_dir: heavy/output/NN-slug/`, `phases`,
`subagents`, `websearch_max`, `est_cost`) + GOAL, CONTEXT, PHASES, OUTPUT SPEC (anchored, append-only),
GUARDRAILS, RESUME (read STATUS.json), DONE (checkable criteria). Be fully self-contained — every path,
every default, every output file named.

## Step 6 — Register it
Add a row to `heavy/library/INDEX.md` (ID, Title, Goal, Cost, Subagents, Output dir).

## Step 7 — Hand off to review
Tell the user the prompt is drafted and recommend `/heavy-review NN` to catch logical gaps before a
real run. Offer to run the review now. Do NOT launch the heavy prompt itself from here — that's `/heavy NN`.

Do not commit unless the user asks (or follow the repo's normal commit discipline if they do).
