---
name: goat-dev
description: Develop, fix, refactor, or review code in the GOAT repository. Classifies the change, sets its verification floor, and carries it from plan to a merged pull request within the task's authority. Use for any code change here; use test-goat-app or test-goat-mobile for the real-client pass.
---

# Develop in GOAT

[AGENTS.md](../../../AGENTS.md) and [Development discipline](../../../docs/operations/discipline.md)
hold the rules. This skill puts them in order.

1. Classify the change from C0 to C5 and check the C4 escalation list. Reclassify when it grows.
2. From C2 up, read the code you will change and its direct callers, then write a short plan: the
   files, the surfaces from [Hit every surface](../../../AGENTS.md#hit-every-surface) that apply, and
   the commands that will prove it. Run each command once to confirm it exists and reads the change.
3. When the problem is unfamiliar, research current practice (GOAT's browser (`goat_preview_read`) or web
   search) and cite the sources in the plan or pull request.
4. Implement in small working steps and commit each locally. A logic, data, state, or protocol bug
   gets a failing test first, then the fix.
   Native Rust, C or C++ builds run through kache after `kache doctor` passes
   ([Build cache](../../../docs/operations/development.md#build-cache)); remove the `target/`
   folders and other large outputs you created before finishing.
5. Verify at the class floor. C0 needs a read-back; C1 one focused check. From C2 up, run
   `vp test run <files>` for the changed behavior, then `vp run check:changed`. A visible change
   gets one pass in a real client through [test-goat-app](../test-goat-app/SKILL.md) or
   [test-goat-mobile](../test-goat-mobile/SKILL.md), and a purely visual fix is proven with
   before/after captures instead of a test. C4 gets an independent review lane before merging, and
   C3 gets one when the risk warrants.
6. Deliver only as far as the user approved in this session. Push and open a pull request to `dev`
   under [Pull requests](../../../AGENTS.md#pull-requests), link it to the thread with
   `goat_call {path:"pull_request.link"}`, and merge under [merging](../../../docs/operations/merging.md) only when you
   hold merge authority. A goatclaw supervisor stays read-only; domain managers and issue sweepers
   hand merging to a merge manager.
7. Report each claim with its command and result, full commit SHAs, pull request URLs, and a
   `NOT RUN:` line. A codexclaw loop records the merged or green pull request with
   `cxc loop pr-record --session <id> --pr <url>`.
