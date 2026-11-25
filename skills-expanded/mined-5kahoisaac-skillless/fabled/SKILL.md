---
name: fabled
description: Six-phase build discipline that turns one prompt into a complete, runnable deliverable with zero placeholders. Use for ANY non-trivial single-prompt build request — "build me…", "create an app/script/tool/site/game/bot/pipeline that…", "make a complete…", "write a program that…" — and whenever the user says "runnable", "production-ready", "complete project", "end-to-end", "MVP", "one-shot", or invokes the skill by name ("use Fabled", "Fabled workflow", "think like Fable"). Also applies to non-code deliverables (documents, plans, reports, analyses) by mapping the same phases — intent → scope → outline/contract → full draft → verify → deliver. When unsure whether a build request is non-trivial, use this skill.
---

# Fabled

Fabled makes the invisible working process of a frontier model explicit, so it can be followed step by step. It cannot
transfer raw intelligence — it transfers process discipline: reconstructing intent, deciding scope, designing before
building, refusing placeholders, and verifying against the original request before finishing. Most one-shot failures
come from skipping that work, not from inability to write any given function. Follow every phase in order; each rule
states its reason, and the reason is why the step is not optional.

## Hard rules — non-negotiable

1. **Complete files only.** Every file is written in full, top to bottom. (Why: a fragment that doesn't run fails the
   user completely; "mostly done" is not done.)
2. **Banned strings.** The final output must contain zero of: `TODO` used as a deferral marker (`# TODO`, `// TODO`, or
   bare uppercase `TODO`), "rest of the code", "rest of code here", "you can implement", "for brevity", "left as an
   exercise", and function bodies that are empty or contain only `pass`, `...`, or a not-implemented error. (Why: these
   are lexically checkable, so the ban is enforceable — unlike a vague "be complete".) Ordinary domain words are fine —
   a todo-list app may contain `todo` items; the ban is on the deferral marker.
3. **Never ask. Assume and record.** Where the prompt is ambiguous, pick the most reasonable default, write it under
   `## Assumptions`, and move on. (Why: in a single-prompt setting there is no second turn; a question back is a
   non-answer.)
4. **Verify before responding.** Re-check every numbered requirement from Phase 0 against the actual output, quoting
   evidence, before finishing. (Why: the most common failure is shipping something that silently ignores part of the
   request.)
5. **Fill the output template below, in order.** (Why: the structure forces the phases to actually happen.)

## Calibrate rigor — objective signals only

The process below is the correct behavior at every capability level; calibration only tunes how much *extra* discipline
to add. Two strict limits: adjustments are keyed to objective signals only, and no tier ever skips a gate or a hard
rule.

- Identify the running model from objective sources only: the model ID reported by the runtime or system context, or an
  explicit user flag such as "strict mode". **Never estimate your own capability by introspection or self-quiz** — there
  is no ground truth at runtime, and the models that most need the full process are exactly the ones most likely to talk
  themselves out of it.
- Best-effort external ranking (optional): if a command/network tool is available, you may fetch a frontier-model
  tracker, e.g. `curl -s https://www.demandsphere.com/research/demandsphere-radar/ai-frontier-model-tracker/api.json`,
  and look up the running model's relative standing. If the call fails, the response is unparseable, or the model isn't
  listed, ignore it silently and fall through to name keywords. Never block on, or retry, this call.
- Map to a tier and apply its adjustment:

| Tier                  | Objective signals (examples)                                                                  | Adjustment on top of the full process                                                                                                                                                                                                                                           |
|-----------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| S — frontier          | tracker top tier; names like "Fable"/"Mythos"-class flagships                                 | Plan narration may be terse bullets; everything else as written.                                                                                                                                                                                                                |
| A — strong            | tracker upper tier; "Opus"/"GPT-5.x"-class flagships                                          | As written; give extra care to edge boundaries when answering Phase 0 Q3. The characteristic strong-model failure is verifying thoroughly in-session but skipping the *shipped* test file and the failure fallback — do both; capability does not substitute for the artifacts. |
| B — capable / unknown | mid-size models, or no reliable signal                                                        | As written. Unknown always lands here, never higher.                                                                                                                                                                                                                            |
| C — small / cheap     | tracker lower tier; names containing "mini", "nano", "haiku", "flash", "lite", "slim", "tiny" | As written PLUS: keep each file under ~80 lines; restate the contract before *every* file; run Gate B after *every* file, not only at the end; allow at most 2 implicit features; do a second full Phase 4 pass.                                                                |

## Effort budget

Spend roughly the first 20% of the output on Phases 0–2 before writing any code or final content. (Why: under-planning
is the default failure mode; an explicit ratio corrects the allocation.)

## Mandatory output template

Fill this exact skeleton, in this order:

```markdown
## Plan

(Phase 0 output: one-sentence definition of done, the numbered
requirement checklist, the four self-interview answers)

## Assumptions

(numbered list of the defaults chosen for anything ambiguous)

## File tree & contracts

(Phase 2 output: the full tree, then data shapes / signatures / interfaces)

(…every file, complete — each preceded by its one-line contract…)

## How to run

(prerequisites → install command → run command, in that order)

## Verification

(the Phase 0 checklist re-copied verbatim, every item ticked with evidence)
```

## Route by task category

Pick the one row whose signals best match the request; it sets the deliverable form and what "run" and "verify" mean
downstream. (Why: a game and a memo fail in different ways; one untyped workflow under-serves both.)

| Category (signals)                                                 | Deliverable form                                                   | "How to run" means                       | Verification focus                                                                                                                                                                                                                     | Quality bar additions                                                                                                                                                                                                                                                                                                 |
|--------------------------------------------------------------------|--------------------------------------------------------------------|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CLI / script ("tool", "script", "tracker", "automation")           | single script or small package                                     | the exact command                        | trace input→output; first-five-minutes bad input                                                                                                                                                                                       | help text, clean error messages                                                                                                                                                                                                                                                                                       |
| Web page / app / game ("website", "web", "page", "game", "UI")     | one self-contained HTML file unless a server is genuinely required | open the file, or one serve command      | unit-test the pure logic apart from rendering **and ship the test file**; pin CDN versions; dependency-load and capability failures (CDN blocked, WebGL/API unavailable) must show a visible error message — never a silent blank page | translate "pretty/playable" via Phase 0; all UI states present; keyboard + touch input; resize handled; assume embedded previews may block storage APIs; no per-frame allocation in the render loop (pool/reuse objects); default difficulty lets a first-time player plausibly score within their first few attempts |
| Server / API ("backend", "endpoint", "service")                    | project with entry point + dependency manifest                     | install command + start command          | manifest matches actual imports; trace one full request                                                                                                                                                                                | input validation, meaningful error responses                                                                                                                                                                                                                                                                          |
| Data / analysis ("analyze", "from this CSV", "report on the data") | script plus the produced artifact                                  | the command over the input               | re-derive 2–3 output numbers independently; handle empty/malformed rows                                                                                                                                                                | state method and caveats next to results                                                                                                                                                                                                                                                                              |
| Document / plan ("write me a … plan/doc/report/spec")              | the finished document itself                                       | who reads it, when, what they do with it | every section fulfills its one-line contract; zero empty headings                                                                                                                                                                      | concrete names, times, owners — or a stated assumption standing in                                                                                                                                                                                                                                                    |

## Phase 0 — Reconstruct intent (before generating anything)

- Re-read the entire prompt twice.
- Extract every explicit requirement into a numbered checklist. This exact list is reused in Phase 4, so number it
  cleanly.
- Translate every subjective adjective — "pretty", "clean", "fast", "user-friendly", "playable" — into 3–6 objective,
  checkable items and add them to the numbered list. (Why: "looks good" can't be ticked; "cohesive 4-color palette, lit
  with shadows, all UI states present, touch + keyboard input" can.)
- Add the implicit requirements the user obviously needs but didn't say: an entry point, persistence if state must
  survive runs, basic error handling, and the runnable-ness itself.
- Write one sentence: the definition of done from the user's point of view.
- Answer this self-interview in writing — the answers go in `## Plan`. (Why: a wrong answer surfaces a misunderstanding
  early, where it is cheap to fix.)
    1. In one sentence, what is being built and for whom?
    2. What single command or action proves the result works?
    3. What are the three most likely ways this output fails or disappoints the user?
    4. What is deliberately out of scope?
- For anything ambiguous: choose a sensible default and record it in `## Assumptions`. Do not ask.

```
GATE A — All four self-interview answers written, all requirements numbered?
  PASS → Phase 1.   FAIL → re-read the user prompt and complete them. Do not write code yet.
```

## Phase 1 — Decide scope and stack

- Apply the category row chosen above; it dictates the deliverable form.
- Choose boring, mainstream technology with minimal dependencies, unless the user specified otherwise — and pin exact
  versions of anything fetched at runtime (CDN scripts, packages). (Why: exotic stacks and floating versions multiply
  the ways a one-shot answer breaks on the user's machine.)
- State explicitly what is in scope and out of scope. Guard against both under-building (a fragment that doesn't run)
  and over-building (features nobody asked for).
- Treat the answer as final: it must stand alone with zero follow-up.

## Phase 2 — Design before code

- Write the full file tree first.
- Define the contracts next: data shapes, function signatures, API routes, module interfaces. All code is then written
  *against* these contracts. (Why: shared contracts are what prevent drift between files.)
- Design for verification: keep the core logic — rules, math, state transitions — in pure functions, separated from I/O,
  UI, or rendering, so Phase 4 can exercise the exact shipped logic without its environment. If the logic lives inside a
  larger file, mark its boundaries so it can be extracted for testing.
- Also plan the state→visual binding check: pure-logic tests cannot catch a presentation layer that mis-binds state — a
  HUD that never updates, scene objects that stop tracking the entities they represent. List each state field alongside
  the visual element it drives; Phase 4 traces one full update through that mapping. (Why: a logic core can verify 100%
  while the layer that displays it is broken — the binding is its own failure surface.)
- Order the build by dependency: foundations (types / config / utils) → core logic → integration and entry point.

## Phase 3 — Build, completely

- Before writing each file, restate in one or two lines what that file must export and what it consumes. (Why: it keeps
  the local working set small — the first place errors creep in.)
- If you can write files, write each completed file to disk as soon as it is finished — never hold the whole build in
  one long response. (Why: a session or transport failure mid-build then costs one file, not the whole deliverable.)
- Write every file in full. Apply hard rules 1 and 2: no stubs, no deferrals, no pseudo-code.
- When writing file N, re-check its imports against what files 1..N−1 actually export. Fix mismatches immediately.
- Handle the obvious failure modes inline: empty input, missing file or env var, bad user input, a runtime dependency
  failing to load. Not exhaustively — just what a user would hit in the first five minutes.

```
GATE B — Search your own output for every banned string in hard rule 2. Zero hits?
  PASS → the checkpoint below, then Phase 4.   FAIL → rewrite the offending file in full.
```

If you can execute commands and the files are on disk, run `python scripts/check.py <output-dir>` from this skill
instead of scanning by eye — a mechanical check beats a vibes check.

## Checkpoint — re-copy the checklist

Immediately before Phase 4, copy the Phase 0 numbered requirement checklist again, verbatim, into `## Verification`. (
Why: early context fades over a long generation; forced repetition re-injects it exactly where it is needed.)

## Phase 4 — Verify before delivering

First pick the verification mode — this is a real branch:

```
VERIFICATION MODE — Can you execute code in this environment (run commands, tests, scripts)?
  YES → Mode B (executed checks).   NO → Mode A (static trace).
```

**Mode A — static trace** (no execution available):

- Mentally execute the happy path from the run command through to the output; trace one full run end to end.
- Cross-check mechanically: every import resolves; every referenced file exists in the tree; the dependency list matches
  actual imports; the stated run command matches the actual entry point.

**Mode B — executed checks** (strictly preferred when available):

- Write and run real checks against the exact shipped artifact: parse/syntax checks, unit tests on the pure-logic core
  from Phase 2, the banned-string scanner, and — where feasible — the actual run command.
- **Ship the checks.** The test file is part of the deliverable: it appears in the Phase 2 file tree and the user can
  re-run it with one command (`node test-logic.js`, `pytest`, …). In-session verification that leaves no runnable
  artifact behind does not count as Mode B. (Why: verification the user cannot re-run is a claim, not evidence —
  transient checks vanish with the session, shipped tests keep the artifact verifiable after delivery.)
- Evidence is pasted command output, not claims.
- When a check fails, first decide *which side is wrong* — the code or the check. The requirement checklist is the
  arbiter. "Fixing" correct code to satisfy a broken test is a real failure; fix the wrong side, then re-run everything.

Then, in both modes:

- Tick every numbered requirement against the produced output. For each item, paste the exact line(s) of your own
  output — or the test result — that satisfy it. "Yes, done" without evidence does not count. (Why: quoting turns a
  vibes check into a mechanical one.)

```
GATE C — Every numbered requirement ticked with quoted evidence?
  PASS → Phase 5.   FAIL → return to Phase 3 for each unticked item, then redo Gate B and Phase 4.
```

## Phase 5 — Deliver for a human

- The deliverable is the runnable artifact itself. A report *about* the build, however thorough, is not a build — if no
  entry file exists, the task failed. (Why: the user asked for the thing, not a description of the thing.)
- Sweep for scaffold leftovers before delivering: debug objects, placeholder description text, stray console output. (
  Why: they read as unfinished even when everything works.)
- Lead with how to run it: prerequisites, install command, run command — in that order.
- Briefly restate the Assumptions list.
- No meta-narration about effort or process. The deliverable speaks for itself.

## WRONG vs RIGHT

WRONG — this is what failure looks like:

```python
def load_expenses(path):
    # TODO: implement loading
    pass
```

RIGHT — complete, with the first-five-minutes failure modes handled:

```python
def load_expenses(path):
    """Return the list of expense dicts stored at path, or [] if none yet."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise SystemExit(f"Data file {path} is corrupted; fix or delete it.")
```

## Non-code deliverables

The same loop applies to documents, plans, reports, and analyses. Map the phases: requirements → scope → section outline
with a one-line contract per section (what question that section answers) → full draft of every section → verify each
requirement with quoted evidence → deliver. Banned equivalents: "[add details here]", "section left for the author",
empty headings, and "etc." standing in for real content. "How to run" becomes "how to use this document" (who reads it,
when, what they do with it).

## Small tasks

If the request is objectively tiny — a single short function or one-file snippet, no persistence, no multiple
components — compress Phases 0–2 into a three-line plan (definition of done, requirements, assumptions). The hard rules
and Gates B–C still apply in full. Compress only on these objective signals, never because the task "feels easy".

## Worked examples

Read `references/examples/index.md`, pick the **one** example whose category matches the task, and read only that
file. (Why: the index keeps context cost low, and one matching trace teaches the expected shape better than reading them
all.) Read an example the first time you use this skill, or whenever unsure what the output should look like.
