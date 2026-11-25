---
name: regression-proof
description: Prove a change before claiming it is done - judge lint, typecheck, tests and git push by their exit codes rather than by reading output, and show that a bug fix's regression test fails without the fix. Use before saying "tests pass", "lint is clean", "pushed" or "fixed in <sha>"; before opening or updating a pull request; whenever a command is piped into grep, tail or head; and whenever a bug fix or false-positive fix ships with a new test. For whether a measured number (a score, a timing, an eval result) can be credited to a change, use `explain-the-number`.
---

# Regression proof

Two habits that each cost a CI round, or a reviewer's trust, every time they were skipped:

1. **A gate passed only if its exit code was 0.** Not if the output "looked clean".
2. **A regression test counts only if it fails without the fix.** A test that passes both
   ways would not have caught the bug.

## Part 1: exit codes, never output

A pipe replaces a command's exit code with the last command's. Each of these really
happened:

| What ran | What it reported | What was true |
| --- | --- | --- |
| `npm run lint \| grep -E "error\|warning"` | clean | prettier printed `[warn] file.ts` and CI failed on formatting |
| `npm test \| grep …; git commit; git push` | pushed | a test was failing; the grep succeeded, so the chain went on |
| `git push -q 2>&1 \| tail -1; echo $?` | `0` | the push had failed; `0` was `tail`'s exit code. Replies then cited a sha that was not on the remote |

Rules:

- Run each gate as its own step, with no pipe, and capture the code:
  `npm run lint > /tmp/lint.txt 2>&1; echo "lint=$?"`. Read the file only to explain a
  non-zero code.
- Run every gate even after one fails, so one report covers all of them. If the project has a
  single command that runs every CI gate and summarizes by exit code, use it.
- Never chain a commit or push after a gate with `;`. Push in a separate step, after every
  gate reported 0.
- After a push, confirm the remote: `git ls-remote origin refs/heads/<branch>` must equal
  `git rev-parse HEAD`. Only then write "fixed in <sha>" anywhere.
- In a worktree you did not create, check `git rev-parse --abbrev-ref @{upstream}` first; a
  branch tracking `origin/main` pushes somewhere you did not intend, or not at all.
- Report codes, not adjectives: `typecheck=0 lint=0 test=0`, not "all green".

## Part 2: the test must fail without the fix

Use this for any bug fix or false-positive fix that adds or changes a test.

1. Commit the work locally (it does not need to be pushed).
2. Make a scratch worktree at the merge base, outside the checkout:
   ```bash
   base=$(git merge-base origin/main HEAD)
   head=$(git rev-parse HEAD)
   git worktree add --detach /tmp/proof "$base"
   ```
3. Copy the branch's **tests only** into it: test files, fixtures and test helpers, nothing
   from the source tree. List what changed under the test directory, then check those paths
   out from the branch:
   ```bash
   git diff --name-only --diff-filter=AM "$base" "$head" -- tests/
   git -C /tmp/proof checkout "$head" -- <the test paths listed>
   ```
   Reuse the checkout's dependencies (a symlinked `node_modules`, the same virtualenv) unless
   the fix changed them.
4. Run only the new test there. Then run it on the branch.
5. Read the verdict:

| Without fix | With fix | Verdict |
| --- | --- | --- |
| fails on an assertion | passes | **proves**: keep it |
| passes | passes | **does not prove**: rewrite it so it fails against the base |
| fails to load, or fails because a name the fix added does not exist | passes | **no verdict**: the test only calls new code. Keep it, and if the fix changed existing behavior, add or point at a test of that behavior and prove that one |
| fails | fails | the test is broken; fix it before anything else |

6. Remove the worktree: `git worktree remove --force /tmp/proof` (`--force` because the
   copied tests are uncommitted changes there).

Put the verdict in the PR's test plan, with the command and both exit codes. Only **proves**
is evidence that the test guards the bug.

## Output

When reporting a change as done, give one line per gate with its exit code, the push check
(`remote head = <sha>`), and for a fix, the proof verdict for each new test.
