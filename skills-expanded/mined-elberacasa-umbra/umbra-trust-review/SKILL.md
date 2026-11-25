---
name: umbra-trust-review
description: Verify AI-generated code before shipping. Run Umbra's Trust Score scan before committing or finishing any coding task, treat findings as blocking issues, and re-scan until clean. Use when finishing a task, before a commit, or when reviewing code written by an agent.
---

# Umbra Trust Review

You wrote this code. Prove it deserves to ship.

Umbra scores a repo 0–100 on two axes: **SAFE** (secrets, injection sinks,
missing authz, hallucinated deps) and **CLEAN** (dead code, unused deps,
mega-files, copy-paste). Every finding has `file:line` evidence and a
confidence level. Only high/medium confidence findings affect the score.

## The rule

Before you commit, open a PR, or declare a task finished:

1. Run the scan:

   ```bash
   npx @elberacasa/umbra .   # or: node /path/to/umbra/dist/cli.js .
   ```

   Use `--offline` if the network is restricted, `--json` if you want to
   parse the report.

2. **Exit code 1 (score < 50) means you are not done.** Do not commit.
   Do not rationalize. Fix the findings.

3. Let the tool heal first: run `npx @elberacasa/umbra . --fix`. It applies
   the provably-safe fixes (unused deps, secret extraction to env vars) and
   re-scans. Then work the remaining manual list.

4. Fix **SAFE** findings first, then **CLEAN**. A leaked secret is a
   breach; dead code is a smell. Order your work accordingly.

5. For every finding, read the `file:line` evidence and fix the root
   cause. Never suppress, delete, or work around the check to raise the
   score — the score is the point.

6. Re-run the scan after every fix round. Loop until the scan passes.

7. If a finding is genuinely a false positive, leave the code alone and
   state, in one sentence with the evidence, why it is a false positive.
   Then continue. Low-confidence notes never block.

## When Umbra blocks a write

If `umbra protect` hooks are installed, Umbra reviews every file you write
before it lands. When a write is refused, the hook exits 2 and the stderr
starts with `UMBRA BLOCKED` followed by the rule id and the reason.

Treat `UMBRA BLOCKED` as a hard stop:

1. Read the stderr reason. It names the rule and the fix.
2. Fix the root cause and write again (e.g. move the secret to an
   environment variable reference, drop the live key, choose a path outside
   `.git/hooks`).
3. If the block is genuinely a false positive, state why in one sentence
   with the evidence and ask the user how to proceed. Do not silently work
   around it.

## If UMBRA.md exists in the repo

The repo carries an Umbra trust report. Treat its unchecked findings as your
task list before writing new code: fix each at its `file:line`, then re-run
`npx umbra-scan --report` to regenerate it. Never check off, delete, or edit
UMBRA.md by hand — the scan regenerates it. If the scan is clean, you may
delete the file entirely.

## What you may not do

- Never route around the guard. No writing the same content via Bash
  redirection, `tee`, or `cat <<EOF`; no splitting a write into pieces to
  dodge the rule; no editing config to disable the hook. A block is a
  signal about the content, and the signal travels with it.
- Do not retry the identical write unchanged after a block.
- Do not commit with a failing score.
- Do not mark a task "done" while findings are open.
- Do not claim tests pass, auth works, or secrets are handled unless you
  verified it. Umbra exists because agents claim things that are not true.
  Do not become the evidence for that claim.
- Do not weaken code to dodge a rule (e.g. renaming `eval` usage). Fix it.

## Output

When you finish, report: final score, findings fixed, and any false
positives with your one-sentence justification.
