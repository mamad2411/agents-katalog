---
name: conduct-plan
description: "Controller plans a feature into small delegable tasks (writes docs/plan/<slug>.md)"
argument-hint: "<what to build>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(conductor-ai run ask:*), Bash(conductor-ai status:*), Bash(conductor-ai plan check:*), Bash(git status:*), Bash(git switch -c:*), Bash(git branch:*)"
---

You are the controller (see `.conductor-ai/ORCHESTRATOR.md`). Plan: **the arguments the user gave**

Use as few of your own tokens as possible:
1. Read `HANDOFF.md` and `docs/architecture.md`. If architecture.md is empty, don't explore the repo yourself. Run this in the background and read the result:
   `conductor-ai run ask "Map this codebase for other engineers: purpose, folder layout, data flow, key modules and public functions, how to run and test. Max 150 lines." --save docs/architecture.md`
2. For specific facts, use `conductor-ai run ask "<question>"` instead of reading many files. Open individual files only for the decisions that need them.
3. **Clarity first.** Before designing, list what is still ambiguous: behaviour the request doesn't pin down, choices with real trade-offs, missing facts about the code. Settle what you can from the code (via `conductor-ai run ask`). Ask the user the rest in one short batch of questions and wait for the answers. Record every item under `## Open questions` as `- [x] question → answer`. conductor-ai refuses to hand out write tasks while any item is still `- [ ]`. If nothing was ambiguous, write `- [x] none`.
4. Copy `docs/plan/_TEMPLATE.md` to `docs/plan/<slug>.md` and fill it in: concrete Design notes (names, types, signatures, file locations), then tasks T1…Tn, each about 1–3 files and under ~200 lines, with role (build/fix/test/docs/controller), `depends on`, files, steps, acceptance criteria and verify. Avoid giving two independent tasks the same file, so they can run in parallel. Give tests and docs their own tasks (roles `test`/`docs`, which go to free models).
5. Run `conductor-ai plan check docs/plan/<slug>.md` and fix every ✗ it reports. conductor-ai refuses to hand out a task that fails it. Also fix every `!` warning: two rules in the plan that contradict each other (e.g. "wrong type → TypeError" and "qty must be an integer, else RangeError"), so a worker can follow either one and still be "right". Say which rule wins, and add an acceptance check for that case. Each write task needs: `files:`, acceptance criteria a check can confirm (a return value, an HTTP status, a command that passes; never "works" or "done"), a verify command, and at most 4 files besides tests. Workers repeat the criteria back with evidence, so write them precisely. Put code in backticks with its exact name, e.g. `` `toQuery({ a: 1 })` returns `'a=1'` ``: conductor-ai rejects work that doesn't define a function or class the task names, and runs every line written as `` `expr` returns `value` `` or `` `expr` throws ErrorType `` as a real check (JavaScript), so prefer that form. Write such a check for every edge case and exact value the Design notes give for the task (empty input, an empty field, a boundary, an exact error message), not only the happy path: workers miss the rules that no check covers (B2: a `,` row read as one field instead of two; `invalid price: 9.999` where the notes said `invalid price`). If a general rule says messages *contain* a text but a value is compared exactly (a `message` field in returned data), say "exactly". For a `fix` task, add `- **repro:** \`<command>\`` when you can: a command that fails now because of the bug (conductor-ai runs it before and after). Without one, the worker must write a regression test that fails on the original code, and conductor-ai checks that it does.
6. If on main/master, create the branch named in the plan.
7. Update `HANDOFF.md`.

Show the user the task table (id, title, role, depends on), which tasks can run in parallel, and offer `/conduct-run docs/plan/<slug>.md`.
