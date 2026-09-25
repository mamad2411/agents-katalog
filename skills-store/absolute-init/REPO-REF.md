# Repo Referensi: maddhruv/absolute

Repo: https://github.com/maddhruv/absolute
Ref lokal: /Users/chaali0324/.agents/repo-refs/maddhruv_absolute
API: curl "localhost:27126/repos/readme?name=maddhruv_absolute"
Dibuat: 2026-09-16

## Cuplikan README
# maddhruv/absolute

Source: https://github.com/maddhruv/absolute
Fetched: 2026-09-16

## README
# Absolute

**A development workflow engine for AI coding agents. Eleven separate skills — a one-time `absolute-init` (interview + stack detection → config), a build loop you run every day (`think → spec → plan → build → polish → document`), plus an engineering-health family that keeps the codebase maintained (deps, security, dead code, lint/type debt, flaky tests).**

> **Quick start:** install each skill via `npx skills add maddhruv/absolute-<name>`, then invoke it directly in your AI coding tool.

```bash
/absolute-init                                              # interview + detect stack → write config the commands read
/absolute-work "Add OAuth2 login with Google and GitHub"   # plan it, build it, verify it
/absolute-spec "Design a commenting system"                 # write a reviewed design doc, don't build yet
/absolute-ui "Design a pricing page"                        # make it look intentional, not generated
/absolute-simplify                                          # clean the diff before you commit
/absolute-docs "Write a getting-started tutorial"           # document what you shipped
/absolute-upgrade                                           # bring dependencies up to date, safely
/absolute-audit                                             # scan deps + code for vulnerabilities
/absolute-deflake                                           # fix the tests that fail randomly
```

---

## Why Absolute?

Most coding agents are great at the middle of a task and bad at the edges. They start writing code before the design is settled, ship UIs that scream "an AI made this," leave the diff messier than it needed to be, and write docs that drift from the code. You end up babysitting.

Absolute replaces that with **eleven opinionated skills** that cover the loop end to end:

- **It refuses to guess.** `absolute-work` interviews you to a shared design one question at a time, writes a reviewed spec, and decomposes the work into a dependency-graphed task board — *before* any code. Want just the design? `absolute-spec` writes a reviewed design doc and stops.
- **It builds safely.** Tasks run one wave at a time, test-first, with an independent evaluator grading each one. Blockers serialize; only provably-independent work parallelizes.
- **It has taste.** `absolute-ui` encodes concrete CSS/Tailwind values — spacing scales, color ratios, type scales, motion rules —
