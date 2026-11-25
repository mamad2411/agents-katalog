---
name: skill-benchmarking
description: "Run skill benchmarks with discriminating-only assertions against evals.json for any model and any AI agent. Use when benchmarking a skill against a model not yet tested, running with_skill/without_skill eval pairs, producing benchmark-<model>.json, re-grading an existing run, adding Phase 2 model comparison results, reviewing results in the eval viewer, updating README benchmark tables, or cleaning non-discriminating assertions from evals.json. Enforces strict grader isolation (the context that generates responses never grades them) and evidence-only passing (assertions pass only on explicit content, never on implication or charity). Works with Claude Code, Gemini CLI, GitHub Copilot, Cursor, and any other AI coding assistant."
---

# Skill Benchmarking

Strict, agent-agnostic benchmark runner for `evals.json` skill evaluation. Produces `benchmark-<model>.json` with pass rates and a discriminating assertion list. Only assertions that actually discriminate between with-skill and without-skill responses are kept; non-discriminating noise is removed via the assertion hygiene process.

This skill works with **any AI coding assistant** -- Claude Code, Gemini CLI, GitHub Copilot, Cursor, Windsurf, or any agent that can read files and run shell commands.

---

## Quick Start for Non-Claude Agents

If you are using **Gemini CLI**, **GitHub Copilot**, **Cursor**, or another AI coding assistant:

1. **Read this file** (`scripts/benchmarking/SKILL.md`) -- it is the complete workflow guide
2. **Follow the phases below** in order. Each phase tells you exactly what to do
3. **Run Python scripts** via your terminal or shell tool. All scripts use only the Python standard library (no pip installs needed)
4. **For grading** (Phase 3), you MUST use a separate/fresh context that has NOT read the skill being tested. If your agent supports subagents or separate chat sessions, use that. If not, start a new chat session for grading
5. **File paths** in this guide are relative to the repository root. Adjust if your working directory differs

### Key differences from Claude Code usage

| Claude Code feature | Equivalent for other agents |
|---|---|
| `Explore` subagent | Start a fresh chat session, or use your agent's subprocess/tool-use feature |
| `Read` / `Write` tools | Use your agent's file read/write commands, or `cat` / shell redirects |
| `Bash` tool | Use your agent's terminal/shell execution capability |

All Python scripts are standalone and require only Python 3.10+. No external dependencies.

---

## Non-Negotiable Invariants

1. **Grader isolation** -- the context/session that generated responses does NOT grade them
2. **Evidence-only** -- assertions pass only when the required content is EXPLICITLY stated in the response; implication, adjacency, and partial coverage all fail
3. **Blind grading** -- the grader does not know whether it is grading a with_skill or without_skill response
4. **Model-agnostic** -- model slug is always supplied by the caller; never infer or hardcode it

Violating any of these means the benchmark is invalid. Start over.

---

## Scripts vs AI -- Task Assignment

| Task | Tool | Why |
|------|------|-----|
| Create workspace dirs + `eval_metadata.json` | `scaffold.py` | Deterministic file layout |
| Write `response.md` from a pre-existing batch outputs JSON | `unpack-outputs.py` | Deterministic file layout |
| Grade responses against assertions | **AI (separate session)** | Requires language understanding |
| Write `grading.json` files from batch AI grading output | `ingest-grades.py` | Deterministic file layout |
| Produce `benchmark-<model>.json` | `aggregate.py` | Pure arithmetic |
| Review results visually | `eval-viewer/generate_review.py` | Interactive HTML viewer |
| Analyze benchmark patterns | **AI with `references/analyzer-prompt.md`** | Pattern recognition |
| Blind comparison of outputs | **AI with `references/comparator-prompt.md`** | Quality judgment |
| Update README benchmark tables | **AI (main context)** | README structure is flexible, not strict |
| Improve skill based on failed assertions | **AI (main context)** | Requires judgment about what to generalise |

All scripts live in `scripts/benchmarking/` relative to the repository root.

---

## Workflow (7 Phases)

```
Phase 1:  Scaffold    -> create iteration dir + eval_metadata.json          [script]
Phase 2:  Generate    -> produce with_skill and without_skill responses      [AI or unpack-outputs]
Phase 3:  Grade       -> isolated session grades responses                   [AI, separate context]
Phase 4:  Aggregate   -> produce benchmark-<model>.json                     [script]
Phase 4a: View        -> review results in interactive HTML viewer          [script, optional]
Phase 4b: Cleanup     -> remove non-discriminating assertions, re-grade     [AI + script]
Phase 5:  README      -> update skill README with new benchmark results     [AI]
Phase 6:  Improve     -> add missing content to skill files                 [AI]
```

For a **new benchmark**: run all phases.
For a **re-grade only**: run Phases 3-4.
For **adding a new model to an existing iteration**: run Phases 2-4 (scaffold already done, metadata exists).
For **README + skill update only**: run Phases 5-6 after a completed benchmark.

---

## Phase 1: Scaffold

```bash
python scripts/benchmarking/scaffold.py \
  skills/<platform>/<skill-name> \
  workspaces/<platform>/<skill-name>/iteration-N \
  <model-slug>
```

Auto-detect next iteration N by listing existing `iteration-*` dirs and incrementing.
Creates `eval-<name>/eval_metadata.json` and empty output dirs for `<model-slug>-with` and `<model-slug>-without`, with **3 run slots** (`run-1/`, `run-2/`, `run-3/`) per variant by default. Use `--runs 1` to scaffold only one run.

---

## Phase 2: Generate Responses

### Option A -- AI generates live (model accessible in this session)

For **each** eval in `evals.json`, produce two responses in the **same model, same settings**.
Never use a stronger/different model for `with_skill` vs `without_skill`.

**with_skill prompt:**
```
Read the following skill file and every reference file it mentions:
  skills/<platform>/<skill-name>/SKILL.md

Then answer this question. Save your complete response (no preamble) to:
  workspaces/<platform>/<skill-name>/iteration-N/eval-<name>/<model-slug>-with/run-1/outputs/response.md

Question: <eval.prompt>
```

**without_skill prompt:**
```
Answer this question. Do NOT read any skill or reference files.
Save your complete response (no preamble) to:
  workspaces/<platform>/<skill-name>/iteration-N/eval-<name>/<model-slug>-without/run-1/outputs/response.md

Question: <eval.prompt>
```

### Option B -- Unpack a pre-existing batch outputs JSON

If responses were already generated and stored in a standard batch file:
```json
{
  "model": "<model-slug>",
  "skill": "<skill-name>",
  "outputs": [
    {
      "eval_name": "queue-creation-simple",
      "response_with_skill": "...",
      "response_without_skill": "..."
    }
  ]
}
```

```bash
python scripts/benchmarking/unpack-outputs.py \
  evals/<platform>/<skill-name>/<model-slug>-outputs.json \
  workspaces/<platform>/<skill-name>/iteration-N
```

---

## Phase 3: Grade (MUST BE ISOLATED)

Grade in a **separate context** that has NOT read the skill being tested.

- **Claude Code**: use an `Explore` subagent
- **Gemini CLI**: start a new session (`gemini` in a new terminal)
- **GitHub Copilot**: open a new chat thread
- **Cursor / Windsurf**: open a new composer or chat
- **Any agent**: use whatever mechanism creates a fresh context with no prior conversation

Pass ONLY:
- All `response.md` contents for one variant (with OR without -- not both)
- Assertions from each `eval_metadata.json`
- Full text of `references/grading-rules.md`

Do NOT pass: SKILL.md, any skill reference files, or any description of what the skill teaches.
Grade with and without variants in **separate grading sessions**.

### Grading prompt (batch -- all evals for one variant)

Copy this prompt into the fresh grading session:

```
You are a strict evaluator. Your only job is to grade responses against assertions.

## Grading Rules
<full contents of scripts/benchmarking/references/grading-rules.md>

## Your Task
Grade each response below. Evidence-only. No charity. No benefit of the doubt.
- PASS: include a short direct quote from the response.
- FAIL: state exactly what was missing.

Return a single JSON array, no preamble, no explanation:
[
  {
    "eval_id": <number>,
    "variant": "SET_A",
    "eval_name": "<name>",
    "assertions": [{"id": "X1.1", "passed": true|false, "notes": "..."}],
    "summary": {"passed": N, "failed": N, "total": N, "pass_rate": 0.XX}
  }
]

## Evals to Grade
### Eval <id>: <eval_name>
**Assertions:** [...]
**Response:**
<response content>
---
<repeat for each eval>
```

After receiving the JSON array, save it to `/tmp/grades_SET_A_run1.json` and ingest:
```bash
python scripts/benchmarking/ingest-grades.py \
  /tmp/grades_SET_A_run1.json \
  workspaces/<platform>/<skill-name>/iteration-N \
  <model-slug> \
  --run 1
```
Repeat the grade+ingest cycle for `--run 2` and `--run 3` (each run gets an independent response and grading). Repeat for the other variant (SET_B = without_skill).

`aggregate.py` auto-detects all `run-*` dirs and averages pass_rates across runs.

---

## Phase 4: Aggregate

```bash
python scripts/benchmarking/aggregate.py \
  workspaces/<platform>/<skill-name>/iteration-N \
  <model-slug>
```

Reads all `eval-*/eval_metadata.json` and `<model-slug>-{with,without}/run-1/grading.json`.
Writes `benchmark-<model-slug>.json` to `iteration-N/`.

If the script reports missing grading files, grade the missing evals first.

---

## Phase 4a: Eval Viewer (optional, recommended)

After aggregation, launch an interactive HTML viewer to review all responses, grading results, and benchmark data side-by-side.

```bash
python scripts/benchmarking/eval-viewer/generate_review.py \
  workspaces/<platform>/<skill-name>/iteration-N \
  --skill-name <skill-name>
```

This starts a local web server (default port 3117) and opens the viewer in your browser. The viewer:
- Shows each eval's prompt, response, and grading results
- Highlights pass/fail assertions with evidence
- Allows you to leave feedback notes per eval
- Auto-saves feedback to `feedback.json` in the workspace

### Additional viewer options

```bash
# Compare with a previous iteration
python scripts/benchmarking/eval-viewer/generate_review.py \
  workspaces/<platform>/<skill-name>/iteration-2 \
  --previous-workspace workspaces/<platform>/<skill-name>/iteration-1

# Include benchmark data in the viewer
python scripts/benchmarking/eval-viewer/generate_review.py \
  workspaces/<platform>/<skill-name>/iteration-N \
  --benchmark workspaces/<platform>/<skill-name>/iteration-N/benchmark-<model-slug>.json

# Generate a static HTML file instead of starting a server
python scripts/benchmarking/eval-viewer/generate_review.py \
  workspaces/<platform>/<skill-name>/iteration-N \
  --static /tmp/review.html
```

---

## Phase 4b: Assertion Cleanup

After benchmarking, review assertions for hygiene. The goal is to keep only assertions that genuinely discriminate between skill-guided and unguided responses.

1. **Remove non-discriminating assertions** -- any assertion passing 100% across all models (both with-skill and without-skill) is noise, not signal. Remove it from `evals.json`.
2. **Soften taxonomy assertions** -- assertions that test for specific category labels or classification terms should be rewritten to test behavior or concepts instead. Test what the code does, not what it is called.
3. **Remove library name-dropping assertions** -- assertions that pass simply because a response mentions a library or framework name add no value. Remove them.
4. **Re-grade with the cleaned set** -- after modifying `evals.json`, re-run Phases 3-4 with the updated assertions. This makes the reported delta honest and closer to truth.

This step is critical for iteration-over-iteration comparisons. Without it, inflated pass rates from non-discriminating assertions mask real skill gaps.

---

## Phase 5: README Update (AI)

Read `skills/<platform>/<skill-name>/README.md` and the new `benchmark-<model-slug>.json`.
Add to the README:
1. A new row in the Results Summary table (include A/B Quality column if Phase 5a has been run)
2. A `#### Results (<Display Name>)` section matching the format of existing rows
3. A `#### Key Discriminating Assertions (<Display Name>)` section listing top misses

Do not reformat or rewrite existing content -- only add new content in the established structure.

---

## Phase 5a: Blind A/B Quality Comparison (optional, recommended)

Binary pass/fail benchmarks cannot distinguish a response that barely mentions a concept from one that provides structured explanation with code and rationale. Run a blind A/B comparison to capture quality differences.

For the full blind comparator methodology and output format, see `references/comparator-prompt.md`.

### What it measures

A blind judge reads both responses (labelled A and B), scores each 0-10, and declares a winner -- without knowing which response used the skill. This captures structure, code examples, precision, completeness, and actionability differences invisible to binary assertions.

### A/B randomization

Alternate `a_is` assignment across evals to prevent position bias:
- Odd-numbered evals: `a_is = "with"`
- Even-numbered evals: `a_is = "without"`

### A/B agent prompt template

```
You are a blind quality judge for technical responses. Compare pairs of responses (A and B).

For each eval:
1. Read BOTH response files
2. Score each 0-10 (half-point ok). Criteria: structure, code examples, precision, completeness, actionability.
3. Declare winner: "A", "B", or "tie" (tie only if scores differ by <= 0.5)
4. Write a JSON result file to the output path

**IMPORTANT: You do NOT know which response used the skill. Stay objective.**

## Eval List

Base path: <iteration-dir>
Model: <model-slug>

| # | eval_name | a_is | A-response path | B-response path | output path |
|---|-----------|------|-----------------|-----------------|-------------|
| 1 | <name> | with | eval-<name>/<model>-with/run-1/outputs/response.md | eval-<name>/<model>-without/run-1/outputs/response.md | eval-<name>/ab-<model>.json |
| 2 | <name> | without | eval-<name>/<model>-without/run-1/outputs/response.md | eval-<name>/<model>-with/run-1/outputs/response.md | eval-<name>/ab-<model>.json |
...

## Output JSON Format (per eval)

{
  "eval_name": "<name>",
  "a_is": "with|without",
  "winner": "A|B|tie",
  "with_skill_won": true|false|null,
  "scores": {"A": 8.5, "B": 7.0},
  "reasoning": "one sentence distinguishing the responses"
}

with_skill_won rules:
- a_is=with & winner=A -> true
- a_is=with & winner=B -> false
- a_is=without & winner=B -> true
- a_is=without & winner=A -> false
- tie -> null

Final Report: Table + totals: with_skill wins: X/N, avg with_skill score: Y.Y, avg without_skill score: Z.Z
```

### Batch size

Run in batches of 8-12 evals per session to keep context manageable. For 24 evals, use 2-3 batches.

### Aggregating results

```python
import json, glob

files = glob.glob("workspaces/<platform>/<skill>/iteration-N/eval-*/ab-<model>.json")
results = [json.load(open(f)) for f in files]
wins = sum(1 for r in results if r["with_skill_won"] is True)
ties = sum(1 for r in results if r["with_skill_won"] is None)
losses = sum(1 for r in results if r["with_skill_won"] is False)
avg_with = sum(r["scores"]["A"] if r["a_is"]=="with" else r["scores"]["B"] for r in results) / len(results)
avg_without = sum(r["scores"]["B"] if r["a_is"]=="with" else r["scores"]["A"] for r in results) / len(results)
print(f"{wins}/{len(results)} wins, {ties} ties, {losses} losses | avg {avg_with:.1f} vs {avg_without:.1f}")
```

### Adding A/B to README

In the Results Summary table, add an **A/B Quality** column:

```markdown
| Model     | With Skill | Without Skill | Delta     | A/B Quality                              |
|-----------|-----------|---------------|-----------|------------------------------------------|
| GPT-5.4   | 100%      | 82.2%         | **+17.8%**| **20/24 wins**, 4 ties (avg 8.5 vs 7.4) |
```

In the root README skills table, append to each model delta cell:
`**+17.8%** . 20/24 A/B (8.5 vs 7.4)`

Add this note below the root README table:
> A/B column format: `wins/total A/B (avg with vs avg without)` -- a blind judge scores both responses 0-10 and picks the better one without knowing which used the skill; position is randomized each eval.

---

## Phase 5b: Post-hoc Analysis (optional)

After A/B comparison, run the analyzer to understand WHY the winner won and generate improvement suggestions.

Use the prompt template in `references/analyzer-prompt.md`. The analyzer:
- Reads the blind comparator's output
- Reads both skills and transcripts
- Identifies winner strengths and loser weaknesses
- Generates prioritized improvement suggestions

This is most useful when comparing two versions of the same skill across iterations.

---

## Phase 6: Skill Improvement (AI)

If discriminating assertions fail with the skill, the skill under-specifies that concept.

1. Read `discriminating_assertions_failed_by_baseline` from the benchmark JSON
2. For each gap, identify which reference file should cover it
3. Add content generalised as a reusable rule or pattern -- never write content shaped only to pass a specific assertion wording
4. Re-run Phases 1-4 into `iteration-N+1` to confirm improvement

---

## Fallback: No Subagent or Separate Session Available

If you cannot create a separate context for grading:

1. Start a **fresh chat** with no prior context about the skill being tested
2. Paste the grading prompt template from Phase 3 directly into the new chat
3. Copy-paste each response's content into the prompt
4. Save the JSON array output to a file
5. Run `ingest-grades.py` to write the individual grading files

**Critical**: Never grade in the same context where you read the skill's SKILL.md or references. This contaminates the grading and invalidates results.

For agents that support it, you can also:
- Use the `grade_responses.py` script for basic keyword/pattern-based grading (flags semantic assertions for manual review)
- Use the `grader-prompt.md` template for a structured grading session

---

## References

| File | Purpose |
|------|---------|
| `scaffold.py` | Create iteration workspace from `evals.json` |
| `unpack-outputs.py` | Write `response.md` files from a pre-existing batch outputs JSON |
| `ingest-grades.py` | Write `grading.json` files from a batch AI grading response |
| `aggregate.py` | Aggregate grading artifacts into `benchmark-<model>.json` |
| `aggregate_benchmark.py` | Alternative aggregator with stddev/min/max statistics |
| `grade_responses.py` | Programmatic keyword/pattern grading (flags semantic checks for AI review) |
| `references/grading-rules.md` | Strict pass/fail contract for graders |
| `references/grader-prompt.md` | Structured grading prompt template for any AI agent |
| `references/analyzer-prompt.md` | Post-hoc analysis prompt for understanding A/B comparison results |
| `references/comparator-prompt.md` | Blind comparator prompt for A/B quality judgment |
| `eval-viewer/generate_review.py` | Generate and serve interactive HTML eval reviewer |
| `eval-viewer/viewer.html` | HTML template for the eval viewer |
