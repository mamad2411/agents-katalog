---
name: plan-tdd
description: >
  Implement one TASK with evidence-backed red, green, and refactor cycles.
  Use before changing behavior during apply or load-and-build, for a TDD
  request, or when an implementer needs tests for written AC. Also use for
  /ultimate-sdd:tdd. Records explicit applicability exceptions for docs,
  configuration, and projects without a test harness.
license: MIT
metadata:
  author: andrewr303
  version: "1.0.0"
---

Build one behavior at a time, with observable evidence rather than a claimed pass.

**Read:** `references/tdd.md` for the loop and exceptions; `references/execution.md` for command authorization, evidence, and independent review. Keep the parent TASK's file scope and AC unchanged.

1. Read project conventions, TASK/REQ AC, validated `tdd` policy, and approved test argv. If context or commands are missing, name the blocker; do not guess tooling.
2. Map each owned AC/scenario to proof. Default `tdd=required`: observe the expected RED failure, write minimum GREEN code, then record a REFACTOR assessment and recheck. Finish one behavior before beginning the next.
3. Record exact commands, cwd, exit/output, test names, and per-behavior refactor results. Record docs/config/no-test-harness applicability explicitly using `references/tdd.md`; never invent a red run.
4. Run affected regression and project-required checks. Do not impose a non-project coverage percentage, weaken assertions, skip failing tests, or mutate configuration to bypass a failure.
5. Return evidence and unresolved checks to the coordinator. TDD is implementation discipline, not permission to mark TASK `done`: fresh independent spec review comes first, quality review only after its pass, then the complete gate.

If the project has `tdd=off`, report that policy and still collect test/AC evidence. If there is no usable harness and no authorized alternative proof, leave required verification blocked. No automatic git commit/reset/revert or destructive restart.
