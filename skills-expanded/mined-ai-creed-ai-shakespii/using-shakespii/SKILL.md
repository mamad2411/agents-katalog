---
name: using-shakespii
description: "Use when the user asks to lint, audit, test, benchmark, validate, or fix an agent skill — from a single SKILL.md frontmatter check to trigger-accuracy measurement or a corpus-wide audit of installed skills for duplication — driving the shakespii CLI (init, lint --json, test --run, bench) to resolve findings until clean."
version: 0.8.0
---

# using-shakespii

## Intent

Teach an agent to drive the shakespii CLI — the deterministic lint and scaffold
substrate for Agent Skills — so skills get created and repaired against the anatomy
contract instead of by taste. The CLI decides; this skill teaches the loop around it.

## Inputs

- Audit: the path to an existing skill directory (one containing `SKILL.md`), or a
  corpus root — a directory of skill directories — audited in one run with `--corpus`.
- Authoring: the new skill's kebab-case name, its purpose, and the situations that
  should trigger it — all three confirmed with the human before scaffolding.
- Optional: a specific finding or rule ID the human wants addressed first.

## Preconditions

- Bun is installed and on PATH (`bun --version` succeeds).
- The shakespii CLI resolves: either installed globally (`bun add -g shakespii`;
  the binary lands in `~/.bun/bin`), or the repo cloned and linked
  (`bun install && bun link` inside it); `shakespii --version` then succeeds.
- Audit: the target skill directory is readable.
- Authoring: the parent directory for the new skill is writable.

## Procedure

Shared core, both branches:

1. Run `shakespii lint <dir> --json` and parse stdout (schema `version: 1`). Each
   finding carries `ruleId`, `severity`, `file`, `line`, `message`.
2. Exit codes: `0` means no errors — proceed. `1` means errors — enter the fix loop.
   `2` means lint itself could not run — report the stderr message verbatim and stop;
   never guess around a broken run.
3. For each finding, look up its `ruleId` in
   [references/rule-remediations.md](references/rule-remediations.md) and apply the
   minimal fix. A finding whose rule has no entry there is fixed from its own
   `message` — messages are written to be actionable.
4. Re-lint. Loop until exit 0, then handle warnings: fix each one, or surface it to
   the human explicitly with a reason. Never silently ignore a warning.

Audit branch — fix an existing skill:

5. Lint the directory the human named and work the fix loop above. For a corpus
   root, run `shakespii lint <root> --corpus --json`: work each skill's findings
   with the same loop, and treat `corpusFindings` (XS rules, whose `sites` name
   every involved skill) as refactor suggestions spanning skills.
6. Preserve the skill's voice and intent: reword a description to lead with its
   trigger; do not rewrite what the skill is for.
7. Report before/after finding counts, what changed per rule, and any warnings left
   standing with reasons.

### Testing a skill's evals

After a skill lints clean, verify its eval suite with the harness:

```bash
shakespii test <skill-dir> --json
```

Exit codes: 0 = no error findings (warnings allowed), 1 = error findings to
fix, 2 = the run itself failed (bad path, no SKILL.md, claude CLI missing).
The deterministic stage checks that `evals/evals.json` exists, parses,
follows the skill-creator schema (`skill_name` equal to the frontmatter
name, unique integer ids, non-empty prompts and expectations, at least
three cases), and references only files that exist inside the skill
directory. Without `--run` the `scenario` and `grading` stages report
`skipped` — the command is free and safe to loop on.

To actually execute the evals — a headless agent runs each case, then an
LLM grader scores every expectation with cited evidence — add `--run`:

```bash
shakespii test <skill-dir> --run --json
```

`--run` spends real tokens (one executor and one grader session per eval
case), so confirm with the human before the first run on a suite (when a
human is present to answer; in a non-interactive run, an explicit approval
already given in the task prompt satisfies this). Results
are cached per (skill content, eval, model): re-running after no changes
replays instantly from cache; editing the skill or its evals re-runs only
because the content hash changed. `--fresh` forces re-execution despite the
cache; `--model <name>` overrides the default executor/grader model
(sonnet). Fix loop: deterministic findings name the JSON path of the defect
in `evals/evals.json`; `scenario` findings mean the executor run itself
failed (timeout, crash); `grading` findings quote the failed expectation
and the grader's evidence — fix the skill (or a genuinely wrong
expectation, with the human's approval) and re-run until exit 0.

### Benchmarking a skill

Once the evals pass, measure the skill's actual capability impact:

```bash
shakespii bench <skill-dir> --json
```

`bench` runs every eval in `evals/evals.json` with the skill mounted and
again without it, `--runs <n>` times per configuration (default 3), and
writes `benchmark.json`. Read `run_summary.delta` for the with-vs-without
capability delta on pass rate, time, and tokens — that delta is the signal,
not the exit code: exit 0 means the matrix was measured and written, full
stop, whether the skill helped, hurt, or made no difference; `bench` never
gates on the delta. Exit 1 means a run failed after its retry and nothing
was written; exit 2 means the eval suite has deterministic findings (fix
those first, same gate as `test`) or the `claude` CLI is unavailable.
`--model <name>` overrides the default executor model (sonnet); `--fresh`
bypasses the cache to force a fresh measurement. Like `--run`, `bench`
spends real tokens per run — confirm with the human before the first run
on a suite (or accept an approval the task prompt already grants), and
never point it at an untrusted third-party skill: both
`--run` and `bench` execute with `--dangerously-skip-permissions`.

### Measuring trigger accuracy

A skill only helps if it fires at the right moments, so measure that
directly rather than trusting the description by eye. Author
`evals/triggers.json`: at least 16 labeled queries mixing prompts that
should trigger the skill with near-miss negatives that should not — TR02
lints this set statically on every `lint` run (missing file, schema
errors, too few queries, no negatives). Then run it for real:

```bash
shakespii test <skill-dir> --run --triggers --json
```

The trigger stage mounts the skill and issues each query 3 times against a
real session, scores a query as triggered when a majority of its reps
fire, and reports overall accuracy across the set. That stage fails (an
error finding) below 0.8 accuracy. Treat description edits as a
deliberate loop, not a guess: adjust the wording, re-run with `--fresh` to
bypass the cache and force fresh measurement, and stop once accuracy holds
at 0.8 or above without regressing queries that already passed.

### Installing a skill

Once a skill lints clean and its evals pass, land it in an agent's live
skills directory through the gate rather than by hand-copying:

```bash
shakespii install <skill-dir-or-bundled-name> --json
```

`install` re-lints the source, runs the deterministic eval checks when
`evals/evals.json` exists, and only then copies the skill into the target.
Lint errors or deterministic failures block the install (exit 1); warnings
never block — surface them to the human instead. The default target is
Claude (`~/.claude/skills`); `--provider <name>` selects others (claude,
codex, cursor, antigravity, gemini, agents, ezio — repeat the flag for
several, or `--provider all` for every provider detected on the machine),
and `--target <dir>` installs into an arbitrary directory. An occupied
destination — an existing directory or symlink — is refused unless the
human approves replacing it; with that approval, add `--force`. The
`--json` report (`version: 1`) carries the gate verdict in `gate.lint` and
`gate.test` plus one entry per target in `targets[]` (`installed`,
`forced`, `reason`); `targets[].advisory` lists cross-skill duplication
findings (XS rules) against the skills already installed at that target —
advisory only, never a block, but report them to the human. Exit codes:
0 = gate passed and every target installed; 1 = gate blocked or a target
refused; 2 = usage error (unknown provider, unresolvable skill).

Authoring branch — create a new skill:

5. Confirm name, purpose, and trigger situations with the human (or adopt
   them from the task prompt when it already supplies and approves them), then run
   `shakespii init <name>` in the agreed parent directory.
6. Fill every section of the scaffold, replacing each placeholder token (the scaffold
   marks them with `TODO(shakespii)` plus a trailing colon) with real content.
7. Write at least one concrete worked example in Examples — real input, real output.
8. Fill `evals/evals.json` with at least three cases, each an in-skill
   behavior branch (happy path, refusal or error branches, variants).
   Scope negatives do not belong here — put near-miss queries in
   `evals/triggers.json`, where the trigger stage measures them.
9. Work the fix loop until lint is clean, then present the skill, its lint output,
   and its evals to the human. Install only with explicit approval and never with
   findings outstanding — and when approved, install through `shakespii install`
   (see "Installing a skill"), not by hand-copying.

## Output

- Audit: the skill's files fixed in place, plus a report of before/after finding
  counts and per-rule changes.
- Authoring: a new skill directory (`SKILL.md`, `README.md`, `evals/evals.json`) that
  lints clean, presented to the human for approval — not installed.

## Examples

Audit, end to end. The user says: "Lint my skill at `~/.claude/skills/summarize-notes`
and fix what it finds."

Input: `shakespii lint ~/.claude/skills/summarize-notes --json` exits 1 with one
finding — `ruleId` FM04, severity error, file `SKILL.md`, line 3, message
"description must begin with a trigger phrase (one of: use when, use for, use if,
use this, invoke when, when the user)".

The agent opens the FM04 entry in the remediation reference and rewrites the
description from "Compresses long chat threads into short bullet summaries" to "Use
when the user asks to summarize a long chat thread into short bullets", changing
nothing else.

Output: the re-lint exits 0 with zero findings, and the agent reports "1 error → 0
findings; FM04 fixed by rewording the description trigger-first", listing no
remaining warnings.

## Anti-patterns

- Editing skill files by taste without running lint first — the CLI is the arbiter.
- Weakening content to appease a rule: deleting a section to silence a finding, or
  gutting a description. Fix the defect, keep the substance.
- Pointing `--corpus` at a single skill directory — corpus mode takes the *parent*
  directory; lint a single skill without the flag.
- Installing a freshly authored skill without human approval, or with findings open.
- Looping on a run that exited `2` — that exit means lint itself could not run;
  report it instead of retrying.
- Hand-copying a skill into a live skills directory when `shakespii install`
  exists — the gate is the point of the install step.
