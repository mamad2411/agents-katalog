---
name: systematic-debugging
description: Debugs by evidence instead of guessing. Use whenever a test fails, behavior regressed, a bug is intermittent or environment-specific, or the user needs to find which commit introduced a defect, even if they only say "this is broken" or "why does this fail". Reproduces, isolates and proves the root cause, then locks the fix with a regression test. Uses git bisect, blame and reflog.
---

# systematic-debugging

Debug by evidence, not by guessing. Each step narrows the search space until the root cause is proven and a regression test locks the fix.

```
systematic-debugging/
├── SKILL.md
├── scripts/
│   ├── bisect_helper.sh     safe `git bisect run` wrapper with sanity checks and automatic reset
│   └── flaky_runner.sh      run a command N times, report failure rate, save first failure log
├── references/
│   ├── bisect-playbook.md   preconditions, exit codes, merge commits, skipping, after the hit
│   └── flaky-and-env.md     flaky test causes, "works on my machine" checklist, delta debugging
└── templates/
    └── bug-report.md        report with evidence, root cause, regression test, verification
```

## When to use

- A test fails or behavior regressed
- A bug is intermittent or environment-specific
- You need the exact commit that introduced a defect

## Method

1. **Reproduce**: build the smallest reliable failing case. If it is intermittent, measure the rate with `scripts/flaky_runner.sh`.
2. **Observe**: collect logs, stack traces, inputs and versions.
3. **Hypothesize**: write 2 to 3 candidate causes, ranked by likelihood, each with a test that would disprove it.
4. **Isolate**: bisect history with `scripts/bisect_helper.sh`, or shrink the input by halves.
5. **Prove**: confirm the root cause with a failing test or a printed fact. A theory without evidence is still a guess.
6. **Fix**: change the minimum necessary.
7. **Guard**: add a regression test that fails before and passes after the fix, then run the full suite.
8. **Record**: put cause and fix in the commit message and fill `templates/bug-report.md` for non-trivial bugs.

## Choosing the isolation tool

| Situation | Tool |
|-----------|------|
| It worked before, you know a good commit | `bash scripts/bisect_helper.sh <good> HEAD -- <test>` |
| Which change touched this line | `git blame -L 40,60 file` then `git log -p -- file` |
| When did this string appear or vanish | `git log -S "name" --oneline` |
| Fails sometimes | `bash scripts/flaky_runner.sh 50 -- <test>` then `references/flaky-and-env.md` |
| Works here, fails there | env and dependency diff, clean `git worktree` |
| Lost work or odd HEAD | `git reflog`, `git stash list` |
| Large input triggers it | halve the input until minimal |

Details and edge cases: `references/bisect-playbook.md`.

## Git-powered commands

```bash
git bisect start && git bisect bad HEAD && git bisect good v1.2.0
git bisect run /tmp/run_test.sh     # keep the script outside the repo
git bisect reset

git blame -L 40,60 path/to/file
git log -S "functionName" --oneline
git reflog
git stash push -m "wip debugging"
git worktree add ../repro <commit>
```

## Instrumentation tips

```bash
# Shell scripts
set -euxo pipefail
```

```python
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(threadName)s %(message)s")
# breakpoint()  # drop into pdb at the suspicious line
```

## Rules of thumb

- Change one variable at a time
- If you cannot reproduce it, you cannot claim to have fixed it
- One green run does not prove an intermittent bug is fixed; repeat it
- Verify that the code you edit is the code that actually runs
- Keep the bisect test script outside the repository, or old commits will not contain it
- After 30 minutes without progress, explain the problem in writing (rubber duck)
- Never commit a fix without a test or a documented manual proof

## What to report back

| Field | Content |
|-------|---------|
| Root cause | one paragraph with the evidence that proves it |
| First bad commit | sha and subject, if bisected |
| Fix | files changed and why it is minimal |
| Regression test | file and name, shown failing before the fix |
| Residual risk | similar code paths checked or not |

## Related skills

- `commitsmith`: write the commit message for the fix, naming the root cause
- `pdf-processing`: an example pipeline that benefits from verification-first debugging
- `multi-agent-orchestration`: trace handoff logs to find which agent produced a wrong result
