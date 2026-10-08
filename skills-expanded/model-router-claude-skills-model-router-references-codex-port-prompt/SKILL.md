# Prompt: port the model-router to Codex

Build me a quality-first "model router" for this Codex setup, equivalent to one I run in Claude Code. Work in this order and do not skip step 1.

## 1. Discover your own levers first (do not assume)
Check the Codex CLI docs and my current config (`~/.codex/config.toml`, any `AGENTS.md`) and report, before building:
- Can Codex set **model** and **reasoning effort** independently? Where: `model`, `model_reasoning_effort`, and `[profiles.<name>]` blocks in config.toml. List the exact allowed effort values for the models I have access to.
- Can Codex delegate part of a task to a **sub-agent pinned to a different model/effort** (any spawn/agents/collab feature, or running `codex exec --profile <name>` as a child process)? If there is no native sub-agent, the fallback is: define profiles and run `codex exec -p <profile> "<brief>"` from the main session, capturing only the compact result.
- Can Codex change its **own** session model/effort mid-task, or is `/model` user-only? State the answer plainly; the router must not pretend to do what the harness forbids.

## 2. Define four tiers as profiles in config.toml
Pick concrete models from the list I actually have access to (check, do not guess):
- `scout` — fast/cheap model, lowest effort. Read-only. Grep, locate files, summarize logs/docs, answer "where is X". Returns `path:line — fact` lists, never file dumps. If it needs deep reading it must say "can't tell without reading deeply — promote to builder".
- `builder` — strong general model, high effort. Implements an agreed plan: features, refactors, tests, docs. Follows the brief exactly, matches file conventions, smallest diff, runs the check named in the brief, never commits unless told. Stops and reports if it hits billing/auth/data-deletion/deploy.
- `verifier` — same strength as builder, high effort, read-only + can run tests. Adversarial: tries to break the change against its brief, quotes real test output, returns `PASS`/`FAIL` with `BLOCKER / SHOULD-FIX / NIT` findings. Never the same run that wrote the code.
- `architect` — your strongest reasoning model, highest effort. Plans and verdicts only, no edits. Investigates real code, gives ONE recommendation with trade-offs, and writes a plan a builder can execute alone: goal, files + changes, order, risks, definition of done, what to do if the check fails.

Write each tier's rules into a per-profile instruction file (or the `AGENTS.md` section the profile loads).

## 3. Write the router instructions into AGENTS.md
**Goal: quality first, cost second.** Never trade correctness for cost.

**Classify (no tools, 30 s).** Score 0–2 on four axes: Ambiguity (specified → approach unknown), Blast radius (reversible → billing/auth/data/deploy/public API/irreversible), Novelty (pattern exists → new architecture), Verification (tests prove it → only a human can). Sum: 0–1 scout, 2–4 builder, 5–8 architect. **Overrides:** blast radius 2 → architect always, and STOP for human review before any edit. Legal/financial/medical substance → architect. User says "just do it quickly" on a reversible task → drop one tier.

**Split before routing.** investigate+plan → architect (stop for review if blast ≥ 1) · implement → builder · find/grep/summarize → scout, in parallel · verify → verifier (never the author) · final review of blast-2 change → architect.

**Brief template** every delegated part receives: GOAL (one sentence) · CONSTRAINTS · INPUTS (exact paths) · DEFINITION OF DONE (checkable) · EFFORT (keyword or "answer directly") · RETURN (compact shape). Never forward conversation history. State the routing in one line before starting, e.g. `Routing: architect → plan (stop) · builder → implement · verifier → check`.

**Effort follows the tier**, then bump within a tier only when reasoning is the bottleneck for that part: builder on concurrency/migrations/edge-case tests → raise effort one step; architect on blast-2 or unknown-cause debugging → maximum effort; scout → never.

**Re-route at every checkpoint (mid-task switching).** Tiers belong to *parts*, not to the task. A checkpoint = plan approved, sub-run returned, verdict in, new fact, user changed the ask. Re-score the next part at each one.
- Shift UP: unknown cause / unfamiliar architecture / trade-off appears → architect. Anyone touches billing/auth/data/deploy → stop, blast 2, architect, wait for human. Scout says "can't tell" → builder. Builder fails verification once → retry builder at higher effort if it is a contained slip, otherwise straight to architect. Fails twice → architect, no exceptions. Verifier finds a BLOCKER it can't explain → architect root-causes before anyone patches.
- Shift DOWN: plan approved → builder. Part becomes lookup/rename/grep → scout. A retry passed → next part resumes its natural tier; escalation never sticks to the whole task. Verification is mechanical → verifier at default.
- Never shift down: inside a running part; below the tier of the code being debugged (a billing bug stays architect even for a one-line fix); on a part that already failed at that tier; on anything the user will ship, publish, or send to another person (always run the verifier).
- Announce every switch in one line: `Re-route: builder → architect (cause unknown after failed patch)`. Say nothing if unchanged.
- Do not suggest moving the main session to a cheaper model to save usage.

**Trivial tasks** (score 0–1, one step): skip routing and just do it. The router must never cost more than the work.

**Anti-patterns to name in the file:** architect used as a typist; effort as reassurance ("max on everything"); verifier = author; scout dumping files; silent downgrade inside a part; sticky escalation; routing the trivial.

## 4. Verify and report
Run one dry task through it (e.g. "add a unit test for function X") and one mixed task (e.g. "find where config is loaded and make the timeout configurable") and show me the routing lines and re-route lines they produced. Report: the exact files you created/edited, the model+effort pinned per tier, and anything from step 1 that Codex cannot do so I know the limits.
