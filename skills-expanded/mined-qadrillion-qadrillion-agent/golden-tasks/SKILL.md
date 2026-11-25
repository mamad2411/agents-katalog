---
name: golden-tasks
description: Evaluate QA agent behavior after a rule, skill or agent change, or add a regression scenario. Separates deterministic policy tests from actual isolated model runs.
disable-model-invocation: true
---

# Evaluate the QA framework

Run `python3 tools/verify.py` first. A failing deterministic check is a finding;
resolve it before claiming a framework pass. Then evaluate behavioral scenarios.

For specialist routing and real authoring exercises, use
`tools/specialists/EVALUATING.md`: materialize task-only workspaces with
`tools/specialists/evaluate.py`, retain runtime action traces and independently
review the artifacts. Its record command preserves judgments; it does not grade
behavior. Keep fixtures/answer keys outside worker source access. Capture test
hashes before checking a corrected target with the same assertions. The local
HTTP and Android fixtures are optional reference stacks, not universal runners.

For each `docs/golden-tasks/*.md`, give a fresh isolated agent only the Task and
permitted fixture/context paths, plus the skill entry point. Do not provide Expect,
the intended answer, prior failures or implementer reasoning. Use disposable
workspace copies when writes are needed. No company accounts, production actions
or real external posts. A blocked action is not retried through another tool.

Inspect the actual actions, artifacts and final claim against Expect. Record
scenario, runtime/model, fixture revision, observed behavior, decisive evidence,
and Pass/Fail/Blocked. A keyword/file-presence check is not a model run. If fresh
subagents are unavailable, use a separate user-started runtime session and report
not-run until its output exists. Do not grade the orchestrator's invented answer.

Persist results in a dated `docs/sessions/` entry. Report each failure and each
unexecuted scenario; do not average them into a clean Pass. Structural hook tests
prove only their payload behavior. Native runtime discovery/deny requires the
separate machine smoke in `docs/reference/runtime-support.md`.

To add a scenario, write Task with raw facts and permitted side effects, then
Expect with observable actions/claims and failure conditions. Include empty/error,
resume and evidence-quality cases when relevant. Expand from demonstrated gaps;
never turn an arbitrary preference into a universal test.
