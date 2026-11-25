---
name: model-lab
description: "Write, improve, restructure or test an agent skill (a SKILL.md with its references and scripts), or any prompt, template or checker a model has to follow. Use when the user asks to make a skill for a task, to turn a finished session into a skill, to fix a skill that agents ignore, skip steps of or loop on, to split or dedupe a bloated one, or to prove that a skill beats no skill. Use it too when a skill does not trigger, for anything a small local model (1.7B to 27B) will run, and when the user asks what a harness actually sends the model. Holds measured design rules, the Agent Skills format, and a test stand on omp, Pi and Claude Code."
compatibility: "The writing rules need nothing. The test stand is Linux-only: bash, git, rsync, python3, script (util-linux), docker and just, with omp or Pi inside the IISD sandbox (github.com/rakshazi/IISD-sandbox) and a local OpenAI-compatible model server. The Claude Code stand needs the claude CLI and its auth."
metadata:
  version: "3.2.1"
  author: rakshazi
  source: https://github.com/rakshazi/model-lab
license: "GPL-3.0-or-later (code), CC-BY-SA-4.0 (Markdown), CC0-1.0 (assets); see LICENSES/ and REUSE.toml."
---

# model-lab

A skill for writing skills. Two jobs, one body of evidence: write a skill a model can execute, then measure whether it does. The rules were measured on small local models (1.7B to 27B), where a weak instruction fails loudly; a skill that holds there holds on a larger model, minus the two crutches named below. Every rule was paid for with a run that went wrong, and its receipt sits in `references/`.

## Writing the skill

The method, in order:

1. **Target model first, a stronger one as the reference.** Write and tune against the smallest model that will run the skill: prompts carry upward fairly well and lose ground going down. Run Haiku or the 27B on the same input to see what more intelligence does with it. If it fails too, the input is the problem, so preprocess it. If only the small model fails, a rule has room. Its transcript is the review material: the steps it took that the small model skipped, and the places it had to guess, each become a clause.
2. **Checker before prompt.** Write the script that judges the output, then run it on your own example. It finds the example's defects before any model does.
3. **Move every judgment you can out of prose.** Into the sampler (grammar, `json_schema` enum, prefill, bounded reasoning), the template (the empty branch, the parse contract), or a script (counts, citations, cleanup). A sentence is the weakest place for a rule; use it for what nothing else can hold. A script also binds every model alike, so it is the part of a skill that survives a model switch.
4. **One change per variant, three runs each** (Evaluating, below).

The rules that fire on almost every skill:

- **Concise and specific.** A small model's attention is the budget. Use RFC 2119 words (`MUST`, `SHOULD`, `MAY`; `NEVER` = `MUST NOT`), and hand it world knowledge as the exact command, never as `--help` output. Concise means no prose a check could replace; for a 4B it still often means an example, a template or a script, which costs a big model tokens and rarely accuracy.
- **When a big or reasoning model runs the skill too, strip two crutches:** forced step-by-step reasoning in the body, and several long worked examples (keep a single short output example). Then run the `NOSKILL=1` baseline on that model as well.
- **Shape first for a one-shot output, shape last for an agentic one.** State what the output IS and where it ENDS before any content rule. In an agentic skill the final reply shape sits next to the step that produces it, because a model shown the handoff first replies with the handoff.
- **Stop with structure.** A grammar, a prefill, or a token bound in the sampler. "Then stop" in prose only reduces trailing text.
- **The input is DATA.** Say so, and strip any block in the input that looks like the output you want: the model copies it and believes its labels.
- **Examples are complete outputs, visibly unlike the real input.** Their verbs, values and framing leak. Show the empty branch in the template and the full branch in the example.
- **Remove the trap.** A placeholder, a fictional value, a cited ID, a generic command list: the model copies it. Delete it or make it real; a rule against copying loses to the copy.
- **No escape hatch without measuring it.** "Output NONE if nothing qualifies" or "or ask the user" becomes the default answer. A status the template ships but the rule never defines is the same hatch.
- **No rule for what a filter can do.** Excluding a class, copy-exactly identifiers, style, a mechanical suffix, a retry counter: each one gets stated and then broken. Check the output instead.
- **Long output in passes.** Ledger, then body, then summary from the finished body. Write each block while its source is open, and fix one block in, one block out, never the whole document.
- **Every mandatory tool call is a loop surface.** An identical tool answer carries no new information, so the model never leaves. Gate the finish on hard failures only, make every error one line naming the next action, refuse inputs that can only be mistakes, and give the checker the oracle the repo already has (`git check-ignore`, the runner file).
- **Guard the sides of a gate.** The model passes an output check by editing something else: the repo, the ledger, the checker's inputs. Fail on any modified tracked file.
- **Delete scaffolding in the step that proves it is done.** A step the model has to remember is a step it skips.
- **Keep a late-binding rule in the body.** The skill body is re-sent verbatim after a compaction; a reference read is a tool result and may not survive. Put the rule that must bind at hour 5 in the body or in a gate that prints it, and keep references for depth.
- **Split runbook, lookup and index.** The body carries the method and the rules that bind late; references carry tables read on demand; generated artifacts carry absolute links to the exact reference section, each with a `read when` trigger. Count the bytes the skill tells the model to read before the first action: front-loaded references bought one skill almost nothing over a short prompt.

The run behind each rule, and the rarer rules, by the failure that sends you there:

| Read | When |
|---|---|
| [Before writing a rule](references/prompts.md#before-writing-a-rule) | choosing the model to tune on; a big model will run the skill too; a branch leaves the call to someone else |
| [Output shape](references/prompts.md#output-shape) | the output trails past its end, glues words together, picks the middle label, or echoes a schema key |
| [Input](references/prompts.md#input) | the model acts on its input, quotes an old block as the request, copies a repo file, or opens every link up front |
| [Examples and templates](references/prompts.md#examples-and-templates) | example values or placeholders reach the output, an empty section gets invented content, or a shorter tool description changes the tool picked |
| [Rules that do not bind](references/prompts.md#rules-that-do-not-bind) | a rule is stated and broken in one run, or the model takes the `NONE` or `ask` exit on inputs with content |
| [Long outputs](references/prompts.md#long-outputs) | one generation cannot hold the output: miscited long writes, a fix pass that returns the document unchanged |
| [Scripts over prose](references/agentic.md#scripts-over-prose) | writing a checker; one passes wrong content, rejects valid content, or accepts a citation to the neighbouring function |
| [Gates and the loop surface](references/agentic.md#gates-and-the-loop-surface) | a run loops on one tool call, passes a gate by editing something else, fills a table with `clean`, ships a proof that cannot fail, or spends its budget on paperwork |
| [Scaffolding and environment](references/agentic.md#scaffolding-and-environment) | controls fail in bulk with no visible cause, scaffolding survives the run, or a race proof will not hold still |

## The skill as a file tree

The Agent Skills format ([agentskills.io](https://agentskills.io)) is the container: a directory with `SKILL.md`, and `scripts/`, `references/` and `assets/` beside it. What binds on every skill, whatever model runs it:

- **`name` and `description` are all an agent sees before it activates the skill.** The description says what the skill does and when to use it, in the user's words, including the asks that never name the domain. `name` equals the directory name.
- **The body loads whole on activation: under 500 lines and 5000 tokens.** It holds the procedure every run walks and the gotchas. A line stays if the agent would get it wrong without it.
- **Everything else loads on demand, and only when something says when.** Link each reference with the moment to read it, and cross-reference the references: a file that touches another file's topic names that file and section. Knowledge one file away with no pointer gets skipped.
- **Alternatives get a page each** and one table in the body (the "Agents" table below).
- **Scripts take `--help`, never prompt, and fail with one line that names the fix.** List them in the body.
- **Prove it against no skill** (Evaluating, below), and prove the description fires with twenty labelled queries.

| Read | When |
|---|---|
| [Frontmatter and layout](references/skill-format.md#frontmatter-and-layout) | creating the directory, or a client refuses to load the skill |
| [Description and triggering](references/skill-format.md#description-and-triggering) | the skill does not fire, or fires on the wrong ask |
| [Body and references](references/skill-format.md#body-and-references) | the body is over budget, or a reference never gets opened |
| [Instruction patterns](references/skill-format.md#instruction-patterns) | the agent thrashes between options, skips a step, or one skill has to serve a 4B and a frontier model |
| [Scripts](references/skill-format.md#scripts) | bundling a script, or the agent rewrites the same helper every run |
| [Evals in the spec's shape](references/skill-format.md#evals-in-the-specs-shape) | shipping evals with the skill, or mapping a lab onto the spec's workspace |

## Evaluating

A lab answers one question: what does THIS model do with THIS skill on THIS repo. Everything below exists because a run once measured something other than that.

### Agents

The lab runs the skill inside a real agent harness. Pick one and read its page before the first run: it holds the run command, the knobs, and what that harness sends the model on its own.

| Agent | Runner | Its page, and when to reopen it |
|---|---|---|
| omp, local models | `scripts/omp/run.sh`, `scripts/omp/probe.sh` | [references/agents/omp.md](references/agents/omp.md): a run shows a tool, a scanner name or an instruction the skill never gave; a rule vanishes after a rollover; before changing `SYSPROMPT`, `TOOLS` or `OMPFLAGS`; a path has to resolve inside the container; after an omp update |
| Pi, local models | `scripts/pi/run.sh` | [references/agents/pi.md](references/agents/pi.md): a run shows a tool, a persona or a context file the skill never named; a subagent fails to start or leaves no trace; two labs share variant names; output paths point into the container; the only question is which tool the model reaches for first; a Pi extension calls a model; after a Pi update |
| Claude Code, cloud models, cold A/B against the old skill or none | `scripts/claude-code/run.sh`, `scripts/claude-code/summary.py`, `scripts/claude-code/blind.py`, defaults in `assets/claude-code/` | [references/agents/claude-code.md](references/agents/claude-code.md): its own procedure replaces the one below; a run is denied a tool; a "cold" model shows house knowledge; your own session's hooks refuse the scratch repo; a score looks too good to read |

### Layout

```
$LAB/                          # /tmp/<skill>-lab
  base/                        # sealed fixture: one commit, no answer key (scripts/seal.sh)
  evals.json                   # spec-shaped eval: prompt, expected_output, assertions (scripts/assert.py)
  literals.txt                 # optional: fixed strings from the reference output, for grade.sh
  check.sh  RUN SNAP           # optional: the skill's own checker on the output (exec bit)
  grade.sh  RUN SESSDIR        # optional: copy or symlink scripts/grade.sh (exec bit)
  runs/<variant>/<n>/          # repo/, prompt.txt, session.log, result.txt, status.txt, outputs,
                               #   trace.json, timing.json, grading.json
  runs/<variant>/benchmark.json  # scripts/summary.py: mean/stddev, delta against the baseline
```

The frozen skill snapshot per variant and the session files live under the agent's own directory; its page names the paths.

### Scripts

Paths are relative to the skill root. Each one takes `--help`, exits 2 with a one-line error on bad input, and never prompts.

| Script | Use it when |
|---|---|
| `scripts/seal.sh` | starting a lab: `$LAB/base` from a source repo, minus the answer key, as one commit |
| `scripts/assert.py` | grading a run against `$LAB/evals.json` into `grading.json`: `grep`, `absent`, `regex` and `cmd` assertions run locally, plain sentences go to a judge model (`JUDGE`, default Haiku) with the `context` files as ground truth |
| `scripts/summary.py` | reading a batch: per variant exit, wall, pass rate, literals, tokens, calls, output caps, seconds after the done signal, repo edits; `benchmark.json` with the delta against the first variant |
| `scripts/grade.sh` | a lab wants the literal smoke alarm against `$LAB/literals.txt` |
| `scripts/trace.py` | one run stands out: tool counts, tokens, output-cap hits, gaps, `--after` a signal, `--json`; `--system` and `--has TEXT` on a session that records its system prompt |
| `scripts/dups.py` | a skill grew or got restructured: lists passages that share a phrase, a measured number or a literal, so each fact keeps one home; runs on any skill directory |
| `assets/evals.example.json` | writing `$LAB/evals.json` |
| `assets/check-snapshot.example.sh` | writing a `$LAB/check.sh` that runs the skill's own checker from the variant's snapshot |
| `assets/check-outside.example.sh` | the skill under test writes outside the repo: a `check.sh` that collects the output first |

The local runners call `check.sh`, `grade.sh` and `assert.py` after every run and write `trace.json` and `timing.json`.

### Procedure

1. **Fixture.** `PREP='go mod vendor' KEEP=vendor scripts/seal.sh <src-repo> $LAB AGENTS.md CLAUDE.md`. Exclude the reference output and anything that leaks it. One fresh commit, because a cloud subagent once scored 31 of 32 by running `git show HEAD~1:AGENTS.md`. The sandbox has no network, so dependencies come in through PREP.
2. **Evals and graders.** Write `$LAB/evals.json` from `assets/evals.example.json`: the user's prompt, the expected output in plain words, the `outputs` to grade, the `context` files the judge treats as truth, and five to ten assertions. Use a script assertion for anything a grep can settle (a command named, an invented target absent, no scaffolding left) and a sentence for judgment ("warns that db-reset wipes the local database"). A good assertion separates a good draft from a bad one: one that passes in every run, skill or no skill, measures nothing, so replace it. Literals in `literals.txt` stay as the smoke alarm, and the skill's own checker goes in `check.sh`.
3. **Probe** what the model receives, once per setup, before blaming any prompt. The agent's page has the command.
4. **Baselines**: three runs with `NOSKILL=1` (the bare task, same `ARGS`), which shows what the skill adds at all. Then the current skill, three runs. Then **one change per variant**, three runs each. A snapshot is taken on first use of a variant name, so the live skill can be edited while a batch runs, unless it calls its own script by installed path: that executes the live file.
5. **Run** in the background, one batch at a time, from the skill root, with the agent's runner: `bash scripts/<agent>/run.sh <variant> <n> <model>`. The model id is required and comes from your harness config.
6. **Read** the batch: `python3 -I scripts/summary.py $LAB noskill v1 v2 --signal '<done signal text>'` gives the table and the deltas. Then, per run that stands out: `status.txt` (did it edit the repo?), `check.txt`, `grading.json` (the evidence behind each FAIL), and `python3 -I scripts/trace.py <session.jsonl> --after '<signal>'` for what the model did once it was told it had finished. Read the drafts against the reference last, and read them yourself.
7. **File the lesson**: the rule, then the run that taught it, as one bullet in the reference section it belongs to. `AGENTS.md` in this directory has the filing rules.

### Reading the numbers

- **n=3 spreads 0 to 15 within one variant.** That is wider than any difference between two variants, so a literal score is a smoke alarm, never the verdict. A zero is usually a timeout or an output cap: read the trace before reading the score.
- **An output cap is a tax on the batch.** Thinking-mode sampling (temp 0.6, top-p 0.95, top-k 20, no presence penalty; Qwen recommends the penalty for instruct mode only) leaves runaway generations in. Roughly one run in five spends 11 to 13 silent minutes on one tool call that hits the 32768-token output cap (`stopReason: length`), and then times out. `trace.py` prints `OUTPUT CAP` for it, and it says nothing about the skill.
- **A pass/fail cell at five runs cannot tell 40% from 75%.** One tool description scored 1 of 5 in a batch and 15 of 20 on the cell alone. Four stray tool calls in 75 runs against zero for the baseline vanished at 60 runs per arm, where the baseline produced the only one. When one cell carries the verdict, rerun that cell at 20 and leave the batch alone.
- **Repeat before believing, one change at a time.** At temperature 0.1 a key term survived under one prompt and died under the next, with no rule touching it. A verdict needs the same input moved the same way twice. Two review suggestions applied together graded as a gain (83 to 97 facts) and hid that one of them was an example leak; split into two variants, one was kept and the other refused.
- **A fix proves itself in the trace.** The question is whether the mechanism changed (the warning gone, the loop shorter, the minutes after the done signal), and a batch average can't answer it.
- **Grade the content, never the shape.** Headers, sections and markers all appeared while the inside carried fabricated paths and dropped the final request. Grep every literal (path, identifier, test name) against the source, plus two or three literals per input that survive only if the pending request did.
- **Grade the outcome the user asked for.** Pick the outcome metric before the first variant and report proof quality as a separate axis: a skill can buy perfect citations for twice the wall time while the bugs found stay flat. The run that paid for it: [Gates and the loop surface](references/agentic.md#gates-and-the-loop-surface), read when proof work eats the budget.
- **A pass can come from an edited repo.** A gate that checks only the output gets passed by changing something else, and `status.txt` shows it.
- **A judge has a noise floor.** Grade blind, then regrade the unchanged arm with a second judge and a new seed: [Grading](references/agents/claude-code.md#grading), read before any model judges a batch.
- **Read where the time went.** A 27B never wrote the file: 45 minutes of reading, thinking blocks of 20 to 28k characters. A slow model's failure is often budget, and `trace.py` shows it.
- **Exit 0 proves nothing about existence.** Check a named target against the file that defines it.

### Pitfalls

- **Never edit a script a running batch executes.** Bash reads it as it goes, so the change lands mid-run. Wait for the batch, or edit a copy.
- **One netless session at a time** (a flock). The local runners sleep 8 s before starting so the previous container's lock has been released.
- **The local runners key snapshots and sessions by variant name, with no lab in the path.** Two labs that reuse a name share a stale snapshot and overwrite each other's sessions: give each lab its own names (`a-old`, `b-old`).
- `pgrep -f <pattern>` and `pkill -f` match their own command line, so anchor the pattern.
- Run real repositories only inside the sandbox. A host-side test of a "safe to run?" classifier ran a plugin installer and opened a browser tab.
- The skill under test is often its own git repo, and its owner commits. The lab never does.

Editing this skill: read `AGENTS.md` in this directory first.
