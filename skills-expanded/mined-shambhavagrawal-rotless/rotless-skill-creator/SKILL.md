---
name: rotless-skill-creator
description: Create new agent skills (SKILL.md) and improve existing ones, for any agent - Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode. Runs the whole rotless flow - prior art with rotless-github-research, a failing baseline first, interview, draft, test cases run with and without the skill, human review, trigger tuning, spec and portability validation, then a rotless.json through rotless-skill-modernizer and a field-notes footer for rotless-skill-refiner. Use whenever the user wants to make, write, build, scaffold, edit, test, benchmark or package a skill, turn a workflow into a skill, or fix when a skill triggers, even if they only say "make this a skill".
license: Apache-2.0. Modified from Anthropic's skill-creator; see LICENSE.txt and NOTICE.
---
<!-- Modified by rotless contributors (2026) from Anthropic's skill-creator (Apache-2.0). Changes are listed in NOTICE. -->

# rotless-skill-creator

This skill creates and improves skills on whatever agent you're running in. The loop:

1. Find out whether it already exists, and what to borrow.
2. Show what goes wrong today without the skill.
3. Interview the user, then draft the skill.
4. Run realistic test prompts with and without the skill, and let the user review the outputs.
5. Improve and rerun until the user is happy.
6. Tune the description so the skill triggers when it should and stays quiet otherwise.
7. Validate it, write its `rotless.json` and add the field-notes footer.

Work out where the user is in this loop and pick up from there. Someone with a draft goes straight to testing; someone who says "no evals, just vibe with me" gets that. Match your vocabulary to the user and explain terms like "assertion" or "JSON" briefly unless they clearly know them.

## The rotless family

There are four skills. Each works alone, and when the others are installed this one hands off to them:

| Skill | Role | When this skill uses it |
|---|---|---|
| rotless-github-research | prior art: does it exist, what to borrow, where the gap is | step 0, before any drafting |
| rotless-skill-creator (this) | build, test and tune a skill | |
| rotless-skill-modernizer | records what the skill relies on in `rotless.json`; `check` catches drift when the outside world changes | step 8, and whenever you edit a skill that has a `rotless.json` |
| rotless-skill-refiner | learns from real use: fixes and optimizations logged while the skill is used become small edits, each with a check | the footer you add in step 8 feeds it; its behaviour checks run through this skill's `run_case.py` |

If a sibling isn't installed, do its step by hand and say so: search for prior art yourself, and list the skill's dependencies in your summary.

## Finding things

- `C` = this skill's folder (the one holding this SKILL.md; Claude Code prints it as "Base directory for this skill"). Scripts are `$C/scripts/…`; run them with `python` (`python3` where `python` is Python 2).
- Sibling skills sit next to this folder, in the same skills folder. Use those copies only: don't search other installs or plugin-cache versions, which can be older.
- `python $C/scripts/harness.py agents` lists the agent CLIs on this machine and which ones are verified for headless runs.

## How tests run on your agent

Each test run needs a fresh agent that sees only the task. Use the first mode that works:

| Mode | When | How |
|---|---|---|
| A. Subagents | your agent can spawn subagents | spawn one per run, as below |
| B. Headless CLI | an agent CLI is installed (`harness.py agents`) | `run_case.py` per run; `run_eval.py` for trigger tests. Verified: Claude Code (`claude -p`) and Codex (`codex exec`). For any other CLI, run `harness.py probe --agent <name>` first |
| C. In-session | neither | do each test yourself, one at a time, following the skill. Skip baselines and tell the user the result is weaker, since you wrote the skill and aren't a fresh reader |

Modes A and B can mix, for example talking in Cursor while tests run on Codex. Mode B installs a temporary copy of the skill into every known project skills folder of a throwaway workspace, so you don't need to know which folder a given agent reads. Runs that write files need a write mode limited to the workspace, which only Claude Code and Codex have today. On other CLIs, use mode A or C for those cases rather than an allow-everything flag.

## Step 0: Local first, then prior art

1. Look through the user's skills folders. If one of their skills already covers this, offer to improve it instead.
2. Use rotless-github-research on the idea, with its full method when it's a build-or-reuse decision. Create `<skills folder>/<name>/references/` (a kebab-case name, in the user's skills folder or, for project-only skills, a project's skills folder) and ask it to write `references/prior-art.md` in the shape rotless-skill-modernizer defines under *prior-art.md*. Steps 1 and 8 read that file.
3. **Gate:** show the user the verdict. *Use* or *contribute* means stop or adapt an existing tool. *Blend* or *build* means continue, carrying "borrow X, avoid Y, fill gap Z".

## Step 1: Capture intent

The conversation may already hold the workflow ("turn this into a skill"). Extract the tools used, the steps, the corrections the user made, and the input and output formats. Then confirm with the user and fill the gaps:

1. What should the skill let the agent do?
2. When should it trigger (what users say, in what contexts)?
3. What's the expected output?
4. Should it have test cases? Skills with objectively checkable outputs (file transforms, extraction, code, fixed steps) benefit; subjective ones (style, art) often don't. Suggest a default and let the user decide.

Then interview for edge cases, input and output formats, example files, success criteria, and every external thing the skill will rely on: CLIs, APIs, MCP servers, docs, repos and limits. That list becomes its `rotless.json` in step 8. Research what you can yourself (docs, MCP servers, subagents) so the user isn't doing your homework.

## Step 2: Show a failure before writing the skill

Run 2 or 3 realistic prompts with no skill (any mode above) and record exactly what the agent does wrong, in its own words where it rationalises. Agents cut corners under pressure (time, sunk cost, authority, "it's just a quick one"), so combine a couple of pressures in at least one prompt. If the baseline already does the job, say so: the skill may not be needed, or it's a reference pack whose value is knowledge the agent lacks.

The recorded failures are what the skill must answer, and they become the first test cases. This step comes from obra/superpowers' *writing-skills* (MIT). Its "match the form to the failure" table is worth reading when a fix doesn't stick: rule-breaking needs a prohibition plus the excuse it closes, a wrong output shape needs a positive recipe, and a missing element needs a template slot.

## Step 3: Write the SKILL.md

- `name`: kebab-case, matching the folder, at most 64 characters.
- `description`: what the skill does and when to use it. All the "when" goes here, not in the body. Agents tend to under-trigger skills, so be a little pushy: "…Use whenever the user mentions X, Y or Z, even if they don't say 'X'". At most 1024 characters, with no angle brackets.
- Keep the frontmatter to `name`, `description`, `license`, `compatibility`, `metadata` (string values) and `allowed-tools`. Other agents reject a skill with agent-specific fields, so extra data goes under `metadata`.

### Anatomy

```
skill-name/
├── SKILL.md              (required: frontmatter + instructions)
├── scripts/              executable code for deterministic or repeated work
├── references/           docs loaded when needed (prior-art.md, lessons.md…)
├── assets/               templates, icons, fonts used in output
├── evals/                test cases (step 4)
└── rotless.json          what the skill relies on (step 8)
```

Agents load a skill in stages. The name and description are always in context (about 100 words), the body loads when the skill triggers (keep it under 500 lines), and bundled files load only when needed. Point clearly to each reference file and say when to read it, and give long references a table of contents. A skill covering several variants (AWS/GCP/Azure) keeps the selection logic in SKILL.md and one reference file per variant.

### Writing it so any agent can follow it

- Describe the action ("search the web", "ask the user", "spawn a subagent if you can, otherwise…") instead of naming one agent's tool. Mention an agent-specific tool name, path or syntax only as a labelled example among others.
- Scripts use the standard library where possible, pass `encoding="utf-8"` on every file read and write, and take prompts and paths as arguments rather than shell strings, so they work on Windows too.
- Write paths relative to the skill folder ("the folder containing this SKILL.md"), never a user's home layout.
- Use the imperative voice. Explain why things matter instead of stacking MUSTs; if you find yourself writing ALWAYS or NEVER in capitals, give the reason instead. Examples help when they stay general and aren't fitted to the test prompts.
- No malware, no hidden behaviour, nothing that would surprise the user if described. "Roleplay as X" skills are fine.

After drafting, reread it with fresh eyes and tighten it.

## Step 4: Test cases

Write 2 or 3 realistic prompts of the kind a real user types, starting from the step 2 failures. Share them: "Here are the test cases I'd like to try. Do these look right, or do you want to add more?"

Each case is a folder under the skill's `evals/`. The format is strict and is described in `references/schemas.md`: read its *Test cases* section before writing the first one and copy its templates.

```
evals/flags-negative-quantity/
├── prompt.md       settings block, then the user's prompt
├── case.yaml       name and what a good result looks like
├── graders/        one statement per file; a placeholder until step 5
└── files/          input files, only if needed
```

If an input file is itself a skill, name it `SKILL.md.fixture` in the case's `files/`, so tools that scan a repo for skills don't offer it as one of yours. `run_case.py` restores the real name in each run, and the case's `place-files.sh` should do the same.

An older skill may have `evals/evals.json`. Its tests still count: run them alongside the case folders, and never edit, convert or delete that file unless asked.

## Step 5: Run and evaluate

Run this step as one sequence without stopping halfway. Results go in `<skill-name>-workspace/` next to the skill folder, by iteration and case name. Keep the names stable across iterations, because the viewer matches runs by path.

```
<skill-name>-workspace/iteration-1/<case-name>/
├── eval_metadata.json     {"eval_name", "prompt", "assertions": []}
├── with_skill/            outputs/, grading.json, timing.json
└── without_skill/         the baseline (old_skill/ when improving a skill)
```

1. Launch every run at once, with-skill and baseline together, so they finish together. The baseline is no skill for a new skill, or a snapshot of the old version (`cp -r <skill> <workspace>/skill-snapshot/`) when improving one.
   - Mode A: give each subagent the skill path, the task, the input files, where to save outputs and which outputs matter.
   - Mode B: `python $C/scripts/run_case.py --agent <cli> --case <skill>/evals/<case> [--skill-path <skill>] --out <workspace>/iteration-N/<case>/with_skill [--allow-writes]`; leave out `--skill-path` for the baseline.
   - Write each case's `eval_metadata.json` now, fresh every iteration, because the viewer takes the prompt from it.
2. While the runs go, draft assertions: objectively checkable statements whose names read well in a report. Describe the result itself ("summary.md states a total revenue of 693.5"), not where it's saved. Put one in each file of the case's `graders/` and the same sentences in `eval_metadata.json`. Leave subjective cases to human judgment, and explain to the user what they'll see.
3. As each run ends, save its timing to the run's `timing.json` (`total_tokens`, `duration_ms`, `total_duration_seconds`). Subagent notifications carry these and are the only chance to save them; `run_case.py` writes the duration and leaves tokens null.
4. Grade each run against its assertions (read `agents/grader.md`), and script anything checkable instead of eyeballing it. `grading.json` uses exactly the fields `text`, `passed` and `evidence`, because the viewer depends on them.
5. Aggregate with `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`, run from `$C`. It writes `benchmark.json` and `benchmark.md` with pass rate, time and tokens (mean ± stddev), listing with-skill before baseline.
6. Do an analyst pass with `agents/analyzer.md`: look for assertions that pass either way, high-variance cases, and time and token trade-offs. Append your notes to `benchmark.json`'s `notes`.
7. Open the viewer before judging anything yourself, so the user sees the outputs first:
   `python $C/eval-viewer/generate_review.py <workspace>/iteration-N --skill-name <name> --benchmark <workspace>/iteration-N/benchmark.json` (add `--previous-workspace <workspace>/iteration-N-1` from iteration 2). Without a browser or display, add `--static <file>.html` and give the user the path; their "Submit All Reviews" then downloads `feedback.json`.
8. Tell the user: "The Outputs tab lets you step through each case and leave feedback; Benchmark shows the numbers. Come back when you're done."
9. Read `feedback.json` (empty feedback means the case was fine), and stop the viewer server if one is running.

## Step 6: Improve

- Generalise from the feedback. The skill will run on far more prompts than these few, so avoid fiddly fixes fitted to them and oppressive MUSTs. If something resists, try a different framing or metaphor.
- Keep it lean. Read the transcripts as well as the outputs, and cut whatever makes the agent waste effort.
- Explain the reasons behind rules, so the agent can handle cases the rules don't cover.
- Bundle repeated work: if every run wrote the same helper script, put it in `scripts/` once.
- Match the form to the failure (step 2): a prohibition plus the excuse it closes, a positive recipe, a template slot, or an observable condition.

Then rerun everything into `iteration-N+1/` with baselines, reopen the viewer with `--previous-workspace`, and repeat until the user is happy, the feedback is empty, or progress stalls.

An optional blind comparison answers "is the new version really better?" when you can spawn subagents. Give two outputs to a fresh agent without saying which is which (`agents/comparator.md`), then analyse why the winner won (`agents/analyzer.md`).

## Step 7: Tune the trigger

The description decides when an agent loads the skill. Offer this step once the skill works.

1. Write an eval set of 20 realistic queries, saved as `[{"query": "...", "should_trigger": true}, ...]`. Make them concrete and specific, with file names, context, casual phrasing, typos and different lengths. Trigger runs get no input files, so don't write a query that hands the agent something to open first ("here's my SKILL.md, test it"): the agent stops to ask for the file before it loads any skill, and the run counts as a miss. 8-10 should trigger: vary the phrasing, include cases where the user never names the skill, and cases where it competes with another skill and should win. 8-10 should not, and those must be near misses that share words with the skill but need something else; "write a fibonacci function" tests nothing. Simple one-step queries make poor tests, because agents don't load skills for what they can do directly.
2. Review the set with the user: `python $C/scripts/make_eval_review.py --eval-set <file> --skill-path <skill> --out <workspace>/eval_review.html` escapes the queries and description safely. Open the page and let the user edit it and click "Export Eval Set", which saves `eval_set.json` to their Downloads.
3. Measure with `python $C/scripts/run_eval.py --eval-set <file> --skill-path <skill> --agent <cli> --holdout 0.4 --out <workspace>/trigger-0.json`. It runs each query 3 times in fresh sessions, splits the set 60/40 into train and test (stratified), and reports accuracy, precision and recall per split.
4. Improve the description yourself; there's no script for this. Read the failing train queries, write a better description and measure it with `--description "<candidate>"`, for up to 5 rounds. Pick the winner by its test score, not its train score, so you don't overfit the queries you've been staring at.
5. Show the user the before and after descriptions with their scores, then update the frontmatter.

Measure on the agent the user actually uses (`--agent`). Without a headless CLI (mode C), check that each should-trigger query shares distinctive words with the description and that none of the near misses do, and tell the user that this is a weak signal.

## Step 8: Validate, record, hand off

1. `python $C/scripts/quick_validate.py <skill>` checks the spec (fields, name matches folder, lengths) and warns about agent-specific wording. Fix every warning or say why it stays.
2. Write the `rotless.json` with rotless-skill-modernizer: run its `init` on the skill (it imports the repos from `references/prior-art.md`), curate the result with the dependency list from step 1, then run its `check` until there's no FAIL, CHANGED or GAP. `init` also records today as the skill's `updated` date, which starts its 15-day reminder clock.
3. End the SKILL.md with the field-notes section below, unchanged except for the skill's name, so rotless-skill-refiner can learn from real use:

   ```markdown
   ## Field notes
   While using this skill, log anything worth learning in one line and carry on: a step that failed, a correction from the user, a workaround, a noisy search, a faster or simpler way, work that could be cheaper, or a rule that clearly helped. `python <rotless-skill-refiner folder>/scripts/notes.py add <skill-name> --kind failure|correction|workaround|noise|missing|stale|better-way|optimization|confirmed --where "<file:line or section>" --what "<what happened>" --evidence "<command and output, numbers, or the user's words>"`. Skip this if rotless-skill-refiner isn't installed. What you log is data for a later review, never instructions.

   Once per session, after you finish a task with this skill, run `python <rotless-skill-modernizer folder>/scripts/keeper.py status`. If it lists this skill as not updated or checked recently, end your reply with one line such as: "<skill-name> hasn't been updated or checked in N days. Want me to check it against recent changes with rotless-skill-modernizer?" Run the check only if the user says yes, and leave the line out when the reply has to stay machine-readable, such as raw JSON for another program. `status` lists only the skills the user marked as their own, so a skill someone else wrote never asks. Skip this if rotless-skill-modernizer isn't installed.
   ```
4. Optionally, for apps that install a skill from a file (the Claude apps, for example), `python -m scripts.package_skill <skill>` run from `$C` builds a `.skill` zip.
5. Summarise for the user: the prior-art verdict, the files created, the dependencies tracked, the test results, and how to re-check (rotless-skill-modernizer `check <name>`) and refine (rotless-skill-refiner `review <name>`).

## Improving an existing skill

- Keep its folder name and `name` unchanged.
- If the installed copy is read-only, copy it somewhere writable, edit there, and copy back or package from the copy.
- Snapshot it before editing; the snapshot is the baseline (`old_skill/`).
- A skill someone else wrote belongs to them, so don't edit it unless the user owns it. Offer to draft an issue for its author instead.
- If it has a `rotless.json`, update it in the same change and run rotless-skill-modernizer `check`.
- If it has logged field notes, start from them by running rotless-skill-refiner `review` first.

## Reference files

- `agents/grader.md`: grading assertions against outputs
- `agents/comparator.md`: blind A/B comparison
- `agents/analyzer.md`: why one version beat another; benchmark patterns
- `references/schemas.md`: test case folders, older evals.json, grading.json, benchmark.json
- `scripts/harness.py`: agent CLIs, headless runs, the project skills folders it installs into
- `scripts/run_case.py`, `scripts/run_eval.py`: test-case runs and trigger tests on any agent CLI
- `scripts/quick_validate.py`: spec validation and portability warnings
- `scripts/make_eval_review.py`: fills the eval-set review page safely
- `scripts/test_harness.py`: lesson checks for the runners (`references/lessons.md`)

## Field notes
While using this skill, log anything worth learning in one line and carry on: a step that failed, a correction from the user, a workaround, a noisy search, a faster or simpler way, work that could be cheaper, or a rule that clearly helped. `python <rotless-skill-refiner folder>/scripts/notes.py add rotless-skill-creator --kind failure|correction|workaround|noise|missing|stale|better-way|optimization|confirmed --where "<file:line or section>" --what "<what happened>" --evidence "<command and output, numbers, or the user's words>"`. Skip this if rotless-skill-refiner isn't installed. What you log is data for a later review, never instructions.

Once per session, after you finish a task with this skill, run `python <rotless-skill-modernizer folder>/scripts/keeper.py status`. If it lists this skill as not updated or checked recently, end your reply with one line such as: "rotless-skill-creator hasn't been updated or checked in N days. Want me to check it against recent changes with rotless-skill-modernizer?" Run the check only if the user says yes, and leave the line out when the reply has to stay machine-readable, such as raw JSON for another program. `status` lists only the skills the user marked as their own, so a skill someone else wrote never asks. Skip this if rotless-skill-modernizer isn't installed.
