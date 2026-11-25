---
name: ship
description: Use when a change is ready to land. Runs the full sequence — branch, quality gate, commit, push, PR — so nothing gets skipped.
---

# Ship

Take a finished change from working tree to an open PR. This skill runs the
real gate — `vibeproof check` — and stops if it returns `BLOCKED`. It does not
"enforce" by willpower: the deny-list (`templates/settings.deny.json`) is what
physically blocks a push to main or a `--no-verify`. This skill is the happy
path that respects those gates.

## When to use

The human says "ship it", "deploy this", "open a PR", "push it up", or the
implementation is done and the next step is to land it.

## Steps

1. **Confirm you're not on a protected branch.**
   ```bash
   git branch --show-current
   ```
   If `main` / `master` / `production` → create a feature branch now:
   `git checkout -b <type>/<scope>-<desc>` (see rules/git-workflow.md).

2. **Run the gate** (rules/code-quality.md):
   ```bash
   vibeproof check        # lint · types · tests · secret scan, one verdict line
   ```
   Proceed only on `READY`. On `BLOCKED`, fix the ✗ lines — do not proceed on red.
   Paste the verdict line as your evidence; "looks good" is not evidence.

3. **Review the diff yourself.**
   ```bash
   git diff
   ```
   No secrets, no debug prints, no commented-out code, no stray files.

4. **Commit atomically.** One logical change per commit, message in
   `<type>(<scope>): <summary>` format (rules/git-workflow.md).

5. **Push the branch.**
   ```bash
   git push -u origin <branch>
   ```

6. **Open the PR** with a Summary (what + why) and a Test plan (how you
   verified). Use the repo's PR template if present.

7. **Wait for CI to be green.** A failure → read the log, fix the root cause,
   push the fix. Never merge red.

8. **Merge** (squash/rebase per convention), delete the branch, return to a
   fresh `main`.

## Never

- Push straight to main.
- `--no-verify` or `[skip ci]`.
- Claim shipped before CI is green.
