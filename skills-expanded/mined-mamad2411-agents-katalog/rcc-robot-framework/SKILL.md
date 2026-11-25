---
name: rcc-robot-framework
description: Use when authoring, reviewing, running, or debugging Robot Framework .robot suites, resources, custom Python libraries, Robot CLI or Rebot results, or RCC's robot_tests acceptance harness.
---

# RCC Robot Framework

## First Inspection

1. Inspect the repository configuration and source before editing: read the root suite/resource files, the target `.robot` suite, its Python libraries, fixtures, and the relevant RCC command implementation.
2. For `joshyorko/rcc`, inspect `robot_tests/resources.robot`, `robot_tests/supporting.py`, and the nearest suite before choosing a helper or assertion. Confirm the checked-out source revision when behavior is version-specific.
3. Establish a focused command and isolated output/state roots before running a suite. Do not use host `pip install` as the default for an RCC-contained project.

## Operating Rules

- Treat exit status, stdout, and stderr as three separate contracts. Capture all three; assert the exact expected nonzero code, select the stream deliberately, and keep JSON stdout free of diagnostic text.
- Parse JSON structurally with the suite helper or Python library; do not validate JSON by substring matching. Assert object/list shape and the relevant fields.
- Isolate mutable RCC state. Acceptance tests may mutate `ROBOCORP_HOME`, holotree spaces, and `tmp/`. The current RCC acceptance suite must run serially. Use Pabot only after the suite derives each worker's home, temporary roots, and fixtures from a worker identity, or after CI provisions truly isolated copies with concrete, defined commands. PabotLib locks do not make shared RCC state safe.
- Use `Step` for commands that need an expected result and stream assertions. `Fire And Forget` captures/logs streams but does not assert an exit code, so limit it to intentional best-effort cleanup/setup.
- Review golden-file diffs rather than blindly accepting them. Normalize CRLF/LF before comparison and make adversarial fixtures through Python helpers when shell quoting would hide the case being tested.
- Use `robot --dryrun` for syntax/control-flow checking and focused suite/test/tag selection before a full run. Keep `--outputdir` outside committed fixtures.
- In an implementation/review answer, name the exact source files and source revision used, the focused command, the exit-code/stdout/stderr and structural-JSON contracts, and the state-isolation/parallel-safety decision—even when the focused run is serial or JSON is not the immediate change.
- Give runnable commands only for prerequisites that exist. If parallel isolation is absent, give the exact serial initial/rerun/merge commands and list Pabot enablement as future work; do not invent a listener, hook, wrapper, or executable helper.
- Route RCC CLI, holotree, cache, endpoint, or source failures to `$rcc-core`; route `robot.yaml`, `conda.yaml`, environment, package, and runtime project failures to `$rcc-robots`.

## Boundary With Other RCC Skills

This skill owns Robot Framework suite design, result processing, and RCC's `robot_tests` acceptance harness. `$rcc-core` owns RCC source and CLI/holotree behavior. `$rcc-robots` owns RCC automation-project configuration and runtime environments. Use those skills after this skill identifies the failure boundary.

## References

- Read `references/authoring-and-execution.md` when creating or changing Robot suites, resources, libraries, syntax, selection, or local execution.
- Read `references/rcc-acceptance-tests.md` when working in `joshyorko/rcc/robot_tests`, including fixtures, command assertions, `ht hash`, and golden output.
- Read `references/results-and-ci.md` when processing Robot results, rerunning failures, configuring CI, artifacts, or Pabot.
