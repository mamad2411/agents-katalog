---
name: verify-gate
description: Evidence-only verification gate that runs the project's real test suite, coverage, linter, type checker and security scan, reports each command with its exit code, and returns VERIFY PASS only when every check exits 0. Use before saying a task is done, before committing or opening a pull request, after an agent claims "all tests pass", or whenever you need proof that the code works rather than an assertion that it does.
---

# Verify gate: measure substance, not claims

Trust no completion claim, including your own. A check counts only if you ran it in this session
and saw its exit code.

## Procedure

1. **Find the project's own checks first.** The CI definition is the source of truth: read
   `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Makefile`, `package.json` scripts, `tox.ini`,
   `noxfile.py` or the equivalent and mirror those commands exactly. Fall back to the per-stack
   defaults in `references/stack-commands.md` only for checks the project does not define.
2. **Pick the five check families:** tests, coverage, lint, types, security (static analysis plus
   a secret scan). Not every stack has all five; record a missing family as `N/A (no tool for this
   stack)`, never as PASS.
3. **Run each check as its own command** and capture its exit code. Do not chain with `&&`: one
   failure would hide the others.
4. **Never install packages, edit configuration, lower thresholds or add ignore rules** to make a
   check pass. A tool that is not installed is `SKIPPED (not installed)`; tell the user the exact
   install command and let them decide.
5. **Coverage:** use the project's configured threshold. If none is configured, report the number
   and do not invent a threshold.
6. **Secret scan:** if `gitleaks` or `trufflehog` is installed, run it. Otherwise search tracked
   files for credential shapes (private key blocks, cloud access key ids, tokens or passwords
   assigned to literals) and report matches as `file:line` without echoing the secret itself.
7. **Do not fix anything during verification.** Verifying and repairing are separate steps. If the
   user asks for fixes, make them, then re-run the whole gate from step 3.
8. **Write the report** with `assets/VERIFY-template.md`: one row per check (command, exit code,
   result) and the last ~20 lines of real output for every failure.

## Verdict

- `VERIFY: PASS`: every applicable check ran and exited 0.
- `VERIFY: FAIL`: at least one check exited non-zero. List them.
- `VERIFY: INCOMPLETE`: nothing failed, but at least one check was skipped. This is not a pass.

Quote command output verbatim. Never summarise a check you did not run, and never report a
verdict from memory of an earlier run after the code changed.
