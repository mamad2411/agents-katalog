---
name: evals-code-run
description: Evaluate the unpushed commits on the current branch across four quality dimensions — code duplication (checked against the rest of the repo), code bloat, inefficient code, and security issues — and record the results as an eval log. Use when the user wants to evaluate, score, audit, or quality-check recent unpushed changes, "run code evals", or measure duplication/bloat/inefficiency/security of work just committed — typically after /feature-implement or /bug-fix has landed commits that have not been pushed yet. Each dimension gets a 0–100% score (the percentage of the change affected — higher is worse) and, when issues are found, a ≤100-word recommendation for improving the feature-implement skill; one JSON entry per dimension is appended to ~/.claude/evals/code.json. Read-only with respect to the repo — never modifies project files, never commits, never pushes; its only write is the eval log. Step 0 confirms with the user via AskUserQuestion before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /evals-code-run.
user-invocable: true
disable-model-invocation: false
argument-hint: <optional base ref to diff against when the branch has no upstream, or omit to use @{u}>
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, Agent, Bash(git *), Bash(ls *), Bash(find *), Bash(date *), Bash(pwd), Bash(test *), Bash(mkdir *), Bash(basename *), Bash(mv *), Bash(cat *), Bash(wc *), Bash(jq *), Bash(python3 *)
---

# evals-code-run — Score unpushed changes across four quality dimensions

You are running the `evals-code-run` skill. The user may have arrived here by typing `/evals-code-run` (with an optional base ref in `$ARGUMENTS`) or because the model proactively invoked the skill. Your job is to evaluate everything committed on the current branch but **not yet pushed**, score it against four quality dimensions — **duplication**, **bloat**, **inefficiency**, **security** — and append one JSON entry per dimension to `~/.claude/evals/code.json`.

The scores exist to build a longitudinal record of code quality produced by the `feature-implement` workflow, so honest, evidence-based scoring matters more than flattering numbers. A score of 0 with no findings is the common, correct outcome for clean changes — never invent findings to make an eval look thorough.

This skill is **read-only with respect to the repo**: it never modifies project files, never stages, commits, checks out, or pushes anything. Its only write is the eval log under `~/.claude/evals/` (plus a sibling backup if that log turns out to be corrupt).

This skill has six steps (Steps 0–5). Execute them in order.

## Step 0 — Proactive-invocation confirmation

Check the current conversation turn for the literal tag `<command-name>/evals-code-run</command-name>` (or the plugin-qualified form). If present, the user explicitly invoked the skill — skip to Step 1.

Otherwise you are being invoked proactively. Ask once via `AskUserQuestion`:

- Question: "Run code evals on the unpushed changes (duplication, bloat, inefficiency, security), appending scores to ~/.claude/evals/code.json?"
- Options: **"Yes, run the evals"** (Recommended — read-only analysis, one log append) / **"No, skip"**.

If the user declines, stop. If you are running in a context with no user channel (e.g. inside a subagent), proceed only when the calling agent's brief explicitly told you to execute this skill; otherwise stop.

## Step 1 — Resolve the unpushed change set

1. Confirm you are inside a git repository (`git rev-parse --show-toplevel`). If not, tell the user and stop.
2. Determine the **base** the evaluation diffs against:
   - If `$ARGUMENTS` contains a ref, verify it resolves (`git rev-parse --verify <ref>`) and use it. If it doesn't resolve, tell the user and stop.
   - Otherwise use the branch upstream: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`.
   - If there is no upstream but `origin/HEAD` resolves, use it and say so in the final summary.
   - If neither exists (no remote), "not pushed" is undefined — tell the user and suggest re-running with an explicit base ref in `$ARGUMENTS`. Stop.
3. Collect the change set. Use the **three-dot** diff (`<base>...HEAD`) so commits that only exist on the remote side never pollute the evaluation:
   - Commits under evaluation: `git log --oneline <base>..HEAD`. If this is empty, there is nothing unpushed — tell the user and stop **without writing anything** to the eval log. A run that evaluates nothing must not produce entries.
   - The diff: `git diff <base>...HEAD` and `git diff --numstat <base>...HEAD`.
4. Compute the **denominator**: sum the added-lines column of `git diff --numstat <base>...HEAD` over the non-excluded files (numstat counts added blank lines too, which a naive grep for `^+` misses; binary files show `-` and drop out naturally). Exclude generated/vendored artifacts (lockfiles such as `package-lock.json` / `uv.lock` / `Cargo.lock`, minified bundles, `dist/`-style build output, files with an explicit "generated" marker). Machine-written lines say nothing about the quality of the authored change, and they'd dilute every score toward 0. Record what you excluded.
   - If the denominator is 0 (pure deletions/renames), all four scores are 0 with empty recommendations — skip Step 2, note the reason, and continue from Step 4.
5. Note (for the final summary only) whether the working tree is dirty. Uncommitted changes are deliberately **not** evaluated — the expected flow is that `feature-implement` commits each stage before evals run.

## Step 2 — Run the four evals

Launch **four parallel subagents** (general-purpose, read-only intent), one per dimension, in a single message; each inherits the session model and effort. Parallelism matters: the duplication eval is search-heavy and the four analyses are fully independent. If the Agent tool is unavailable in your context, run the same four analyses yourself, sequentially, applying the briefs below verbatim.

Each subagent knows nothing about this conversation, so its brief must be self-contained. Include:

- The repo root and the exact base ref, plus the commands to reproduce the change set (`git diff <base>...HEAD`, per-file `git diff <base>...HEAD -- <file>`).
- The list of changed files with per-file added-line counts, the denominator from Step 1, and the exclusion list.
- Its dimension definition and the shared counting rules (copy the relevant blocks below verbatim).
- The output contract (below), and an instruction that its final message must be exactly one output block and nothing else.
- A hard constraint: read-only — it must not modify, stage, commit, or push anything.

### The four dimensions

**duplication** — Of the added lines, how many substantially duplicate code that already exists **elsewhere in the repo** (outside this change) or is repeated **within the change itself**? Hunt actively: pick distinctive identifiers, string literals, and logic shapes from the added code and `Grep` the rest of the repo for them; compare candidate matches by reading both sides. Count: copied or near-copied blocks (roughly ≥4 contiguous lines of matching logic), reimplementations of an existing helper/utility the change should have called, and repeated blocks pasted between the new files themselves. Do **not** count unavoidable boilerplate: imports, interface/framework-mandated signatures, config keys that must be restated.

**bloat** — Only within the change: added code that the change does not need. Count: dead or unreachable code, unused imports/variables/parameters introduced by the change, abstractions with a single caller that a direct call would serve, speculative generality (options, flags, hooks nothing uses), comments that merely restate the adjacent code, and verbose constructs where the language or its standard library offers a direct idiom. Judge against what the change actually needed to accomplish, not against personal style.

**inefficiency** — Only within the change: added code that does its job wastefully. Count: nested scans where a keyed lookup fits, work recomputed inside loops that is invariant, N+1 patterns for I/O or queries, loading an entire file/collection where streaming or a bounded read applies, unnecessary copies or allocations on hot paths, and missing early exits on the common case. Only count what is plausibly consequential — a linear scan over a five-element constant list is not a finding.

**security** — Only within the change: added code with a security defect. Count: injection risks (command, SQL, path traversal) from unsanitized input, hardcoded secrets or credentials, unsafe deserialization of untrusted data, missing validation at a trust boundary, insecure temp-file or permission handling, weak randomness or crypto used for a security purpose, and sensitive data written to logs. Score the lines belonging to each insecure code path.

### Shared counting rules

- **Denominator** = the total added-line count from Step 1 (passed in the brief). Use it as-is.
- **Numerator** = the number of distinct added lines exhibiting the issue for *this* dimension. Count each line at most once within a dimension (the same line may legitimately count in several dimensions).
- **score** = `round(100 × numerator / denominator)`, clamped to 0–100.
- Every finding must cite evidence: `file:line(s)` plus, for duplication, the pre-existing location it duplicates. A finding you cannot point at is not a finding.
- Stay language-agnostic in judgement — apply the dimension definitions to whatever languages the diff contains; do not penalize idioms merely for being unfamiliar.

### Recommendation rules

The recommendation is **not** a project-specific fix — it is process feedback for `skills/feature-implement/SKILL.md`, the skill that (in the expected flow) produced these commits. Phrase it as a generic, language-agnostic improvement to how that skill works (e.g. a sharper self-review lens in its per-stage review, a check to search for existing helpers before writing new ones), such that the issues found this run would have been caught or prevented.

- Maximum 100 words. One recommendation per dimension per run.
- If the dimension found **no** issues (score 0), the recommendation is the empty string `""` — do not manufacture advice.

### Subagent output contract

The subagent's final message must be exactly this block:

```
EVAL_RESULT
eval_type: <duplication|bloat|inefficiency|security>
denominator_lines: <N>
affected_lines: <N>
score: <0-100 integer>
findings:
- <file>:<lines> — <one-line description[; duplicates <file>:<lines>]>
recommendation: <one paragraph, ≤100 words, or empty>
END_EVAL_RESULT
```

(`findings:` may be followed by `- none`.)

## Step 3 — Validate the results

For each of the four result blocks:

- Recompute `round(100 × affected_lines / denominator_lines)` and use that as the score if the subagent's arithmetic disagrees; clamp to 0–100.
- Verify the score and findings are consistent: a nonzero score with no cited findings, or findings with a zero numerator, means the block is unreliable — re-run that one eval (once) with the same brief before accepting it.
- Trim any recommendation over 100 words down to its core; force the recommendation to `""` whenever the score is 0.

If a subagent failed or returned garbage twice, run that dimension's analysis yourself using the same brief rather than shipping a hole in the record.

## Step 4 — Append to ~/.claude/evals/code.json

The log is a **single JSON array**; each run appends exactly four entry objects (one per dimension) with **exactly these five fields** — no extras, no omissions:

```json
{
  "repo_name": "<repo name>",
  "timestamp": "<UTC ISO-8601, e.g. 2026-07-04T10:12:00Z>",
  "eval-type": "duplication",
  "score": 9,
  "recommendation": "…or the empty string"
}
```

- `repo_name`: basename of `git remote get-url origin` with any `.git` suffix stripped; if there is no `origin`, the basename of `git rev-parse --show-toplevel`.
- `timestamp`: one `date -u +%Y-%m-%dT%H:%M:%SZ` value shared by all four entries of the run, so a run is identifiable in the log.
- `eval-type`: exactly `duplication`, `bloat`, `inefficiency`, or `security`. All four entries are always written, including score-0 ones — a clean run is signal too.

Append with a read-modify-write that cannot half-destroy the log. Preferred: a `python3` heredoc that loads the file (missing or empty file → `[]`), extends the array, and writes atomically via a temp file + `os.replace` in the same directory:

```bash
mkdir -p ~/.claude/evals
python3 - <<'EOF'
import json, os, tempfile
path = os.path.expanduser('~/.claude/evals/code.json')
new_entries = [
    # the four entry objects, filled in literally for this run
]
data = []
if os.path.exists(path) and os.path.getsize(path) > 0:
    with open(path) as f:
        data = json.load(f)
data.extend(new_entries)
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
with os.fdopen(fd, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
os.replace(tmp, path)
print(f'{len(new_entries)} entries appended; log now has {len(data)}.')
EOF
```

If `python3` is unavailable, do the same with the Read and Write tools and then verify the result parses (`jq . ~/.claude/evals/code.json`).

If the existing file **fails to parse**: do not silently discard it. Move it aside to `~/.claude/evals/code.json.corrupt-<UTC timestamp>`, start a fresh array containing this run's four entries, and tell the user about the backup in the final summary.

## Step 5 — Present the summary

Report in chat, in this order:

1. What was evaluated: the base ref, the commit count (`git log --oneline <base>..HEAD | wc -l`) , the denominator (added lines) and any exclusions; a note if the working tree had uncommitted changes that were not evaluated.
2. A compact score table:

   | Eval | Score | Affected / total lines |
   |---|---|---|
   | duplication | 9% | 37 / 412 |

3. For each nonzero dimension: the top findings (with `file:line` evidence) and the recommendation.
4. Confirmation of the log write: "4 entries appended to `~/.claude/evals/code.json` (log now has N entries)." — plus the corrupt-backup note if Step 4 needed one.

This skill does **not** call `lessons-capture` — like `bug-submit`, it is a filing/recording skill, and its recommendations already have a home (the JSON log).

## Constraints (non-negotiable)

- **Read-only with respect to the repo.** Never modify, create, stage, commit, checkout, or push anything in the project. Subagent briefs must carry the same constraint.
- **The only write is `~/.claude/evals/code.json`** (and its `.corrupt-<ts>` backup when needed). Never write under the project's `features/`, `bugs/`, or `docs/`.
- **Exactly five fields per entry, four entries per run, one shared timestamp.** Consumers of the log depend on the shape staying stable.
- **Nothing evaluated → nothing written.** No commits ahead of the base means stop without touching the log.
- **Evidence or it didn't happen.** Every nonzero score traces to cited findings; every score-0 dimension carries an empty recommendation. Do not pad.
- **Committed-but-unpushed only.** Uncommitted working-tree changes are out of scope by design; mention them, don't evaluate them.
- **No symlinks**, per plugin-wide convention.
