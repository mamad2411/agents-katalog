---
name: review
description: "Runs the full code-review-core pipeline on a git diff. Linters scan the changed lines, gated review agents judge what linters cannot, and a deterministic finalize step writes the verdict to .code-review/VALIDATED.json. Use when a branch needs a complete review with a verdict a script or a transport can read. Not for a quick conversational review (use /code-review); not for the linter pass alone (use review-scan). Claude Code only: needs a git checkout and a shell."
argument-hint: "[base-ref] [--effort low|medium|high]"
disable-model-invocation: true
allowed-tools: Bash(bash "${CLAUDE_PLUGIN_ROOT}/pipeline/prepare-context.sh" *), Bash(bash "${CLAUDE_PLUGIN_ROOT}/pipeline/review-scan.sh" *), Bash(python3 "${CLAUDE_PLUGIN_ROOT}/pipeline/contract.py" finalize *), Bash(python3 -m json.tool */.code-review/VALIDATED.json), Bash(git symbolic-ref *), Bash(git rev-parse *), Read, Grep, Glob
license: MIT
---

# review

Arguments: `$ARGUMENTS`

Run the stages below in order, in this conversation. Each stage talks to the next only through files
in `<root>/.code-review/`. Your job is to run the scripts and agents and report what they wrote.
Leave agent artifacts and `VALIDATED.json` to their owners, because a hand-written verdict is one
nobody re-read.

Shell variables do not survive between Bash calls, so write resolved values literally into every
command and prompt below. `<root>` stands for the repository root and `<base>` for the base ref.

## 1. Resolve the root and the base ref

Run `git rev-parse --show-toplevel` and use its output as `<root>`. The scripts always write to
`<root>/.code-review/`, whatever directory this session started in, so every path below is absolute.
If the command fails, there is no repository: see **Without a checkout**.

Take the first argument that does not start with `--` as the base ref. Keep `--effort <level>` if
given, and pass it to `prepare-context.sh` only.

With no base argument, try these in order and use the first that resolves:

1. `git symbolic-ref --short refs/remotes/origin/HEAD` (prints e.g. `origin/main`)
2. `git rev-parse --verify --quiet origin/main`
3. `git rev-parse --verify --quiet origin/master`

If none resolves, stop and ask the user for a base ref. Nothing has run yet, so there is no verdict
to report.

## 2. Build the context

```bash
bash "${CLAUDE_PLUGIN_ROOT}/pipeline/prepare-context.sh" --base <base> [--effort <level>]
```

It clears the previous run's agent artifacts, runs the detection scan, caps the diff into
`DIFF.md`, and records the agent gates in `CONTEXT.json`.

- **Exit 2** means the context could not be built (bad ref, not a git repo, missing `git` or
  `python3`). Stop here and report `INCOMPLETE — prepare-context failed: <its stderr line>`. Run no
  agents: without `CONTEXT.json` and `DIFF.md` they have nothing bounded to read.
- A `WARN` saying the working tree is not at the reviewed ref goes into the final report verbatim.
  Findings may be anchored on the wrong lines.

## 3. Make sure the scan exists

`prepare-context.sh` runs the scan itself. If `<root>/.code-review/SCAN.json` is missing afterwards
(it warns "continuing without SCAN.json"), run the scan standalone once:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/pipeline/review-scan.sh" --base <base>
```

If it is still missing, continue. `CONTEXT.json.scan.present` is `false`, and finalize reports the
missing scan as `INCOMPLETE`.

## 4. Run the judgement agents in parallel

Read `<root>/.code-review/CONTEXT.json` and note its `reviewed_sha`. Launch these agents in **one
message** so they run in parallel:

| Agent | Runs when | Writes |
| --- | --- | --- |
| `code-review-core:review-semantic` | always | `SEMANTIC.json`, `SEMANTIC.md` |
| `code-review-core:review-testing` | `testing.spawn` is `true` | `TESTING.json`, `TESTING.md` |
| `code-review-core:review-architect` | `architect.spawn` is `true` | `ARCHITECTURE.json`, `ARCHITECTURE.md` |
| `code-review-core:review-authoring-conformance` | `claude_config.spawn` is `true` | `CLAUDE_CONFIG.json`, `CLAUDE_CONFIG.md` |

The gates are the script's decision, not yours. A gated agent whose `spawn` is `false` does not run.
Report its `reason`. Give each agent the same short prompt, with `<root>` written out: "The review
workspace is `<root>/.code-review/`. Review the change described by its `CONTEXT.json`, `DIFF.md` and
`SCAN.json`, and write your artifacts there."

When they return, check each launched agent. It **failed** when any of these holds:

| Check | Failed when |
| --- | --- |
| Trailer | its final message has no `REVIEW-TRAILER v1` block, or the last one says `STATUS: BLOCKED` |
| Artifact | `<root>/.code-review/<CATEGORY>.json` is missing or does not parse (read it with `Read`) |
| Freshness | the artifact's `reviewed_sha` differs from `CONTEXT.json.reviewed_sha` |
| Counts | the trailer's `FINDINGS` or `SEVERITIES` differ from the artifact's `findings` |

Note each failure as `<agent>: <which check, and what you saw>`. Do not re-run the agent or write
the file for it.

- **Every failed agent left no artifact**: continue. Finalize turns each missing input into an
  `INCOMPLETE` verdict that names it.
- **A failed agent's artifact is still on disk** (stale, unconfirmed or miscounted): stop here. Skip
  steps 5 and 6, so that no `VALIDATED.json` is written from a file nobody can vouch for, and report
  `INCOMPLETE — <agent>: <failure>`. Say that the transports will refuse to post, and that a re-run
  starts clean.

## 5. Validate

Launch `code-review-core:review-validator` alone, after every step 4 agent has returned, with the
same `<root>/.code-review/` workspace line in its prompt. It re-reads each cited line and writes only
`<root>/.code-review/VALIDATOR-DECISIONS.json`. If it fails or that file is missing, note it and
continue to step 6; finalize reports the missing decisions as `INCOMPLETE`.

## 6. Finalize

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/pipeline/contract.py" finalize --dir <root>/.code-review
```

This deterministic step merges the agent artifacts and the validator's decisions. It writes
`VALIDATED.json`, `VALIDATED.md`, and `CONTRACT-DEFECTS.md` when there are defects. The blocking floor
comes from `CODE_REVIEW_BLOCKING_FLOOR` (default `MINOR`) and is recorded in the output.

- **Exit 0**: written.
- **Exit 2**: an input was missing or unparseable. It still writes an `INCOMPLETE` `VALIDATED.json`
  naming the input. Report `INCOMPLETE — <that input>`.
- **Any other exit, or no `VALIDATED.json`**: report `INCOMPLETE — finalize failed: <stderr>`.

## 7. Verify and report

```bash
python3 -m json.tool <root>/.code-review/VALIDATED.json
```

If this fails, the review did not finish. Report `INCOMPLETE` and say that the transports will
refuse to post it. Otherwise, reply with this shape:

```markdown
**Verdict:** APPROVE | REQUEST_CHANGES | INCOMPLETE — <reason when INCOMPLETE>
**Findings:** <n> total · BLOCKER <n> · MAJOR <n> · MINOR <n> · NIT <n> · <n> outside the diff
**Agents:** semantic <ran|failed: what> · testing <ran|skipped: reason|failed: what> · architect <…> · authoring <…> · validator <…>
**Scan:** <k> tools ran, <m> skipped (<names>)
**Notes:** <worktree warning, agent failures, CONTRACT-DEFECTS.md if present>
Full report: <root>/.code-review/VALIDATED.md
```

Take the verdict and counts from `VALIDATED.json`, never from your own reading of the findings.

Then point to the next step. To publish, use `github-workflow:review-transport` for a GitHub PR or
`gitlab-workflow:review-transport` for a GitLab MR. For a quick conversational pass instead of this
pipeline, use `/code-review`.

## Without a checkout

This pipeline needs a git checkout, a shell, and subagents. If there is no repository here, say so
and suggest `/code-review` on a pasted diff instead. Do not simulate the pipeline's output.
