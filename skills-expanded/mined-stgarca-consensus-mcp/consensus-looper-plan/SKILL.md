---
name: consensus-looper-plan
description: >
  Design-coach front-door for Consensus Build (workflow D). Use when the
  operator chooses to launch Build WITH a Looper plan - i.e. coach a sharp goal,
  typed verification, and termination caps BEFORE the architect writes a spec,
  then SEED the Build goal from the coached plan. This is the DESIGN layer;
  Consensus Build is the EXECUTOR. It does NOT run the loop - it writes
  problem.md + suggestions into the goal dir and hands off to
  `consensus-mcp-architect step`. (Built on a vendored MIT-licensed loop-design
  slice; attribution in consensus_mcp/looper_plan/NOTICE.)
disable-model-invocation: true
argument-hint: "<goal-id>"
allowed-tools: Read, Write, Bash(python3 *), Bash(python *)
---

# Consensus Looper Plan (design coach -> seed Build)

Looper here is the **design coach** for Consensus Build, NOT a second executor.
You coach the operator to a good goal + typed verification + caps, compile it,
and seed the Build goal. Build then executes it UNTOUCHED. Never run the loop
from this skill; never edit the Build supervisor.

The vendored slice lives in the installed package at
`consensus_mcp/looper_plan/` (rubrics under `rubrics/`, helpers `compile.py` /
`seed.py`). Resolve its path once:

```bash
python3 -c "import consensus_mcp.looper_plan as L, os; print(os.path.dirname(L.__file__))"
```

Call it `LP_DIR`. Use `LP_DIR/rubrics/<stage>-rubric.md` for coaching.

## Workflow

1. **Resolve + VALIDATE the goal dir BEFORE any mkdir/write.** Do not build the
   path from the raw `<goal-id>` string - validate it through Build's own rule:

   ```bash
   python3 -c "from consensus_mcp.looper_plan import seed; print(seed.resolve_goal_dir('.', '<goal-id>'))"
   ```

   This reuses `_architect_paths.goal_dir`, returns the path under
   `.consensus/architect/`, and raises `ArchitectPathError` on a malformed id
   (path separators, traversal, Windows-reserved name, leading/trailing dot). If
   it raises, STOP and tell the operator the goal id is invalid. Use the RETURNED
   path for every subsequent read/write; create it if absent.

2. **Refuse if Build has already begun (write-once guard).** Before any
   coaching, run:

   ```bash
   python3 -c "from consensus_mcp.looper_plan import seed; seed.assert_safe_to_coach('.consensus/architect/<goal-id>')"
   ```

   If it raises `ReCoachRefused`, STOP and tell the operator: the goal already
   has a sealed spec/approval/cycle, so re-coaching would mutate baseline-covered
   inputs and block delivery - start a NEW goal id instead. Do not proceed.

3. **Read Build's roles (authoritative; re-read fresh).** Read
   `.consensus/config.yaml` `roles:` (architect / builder / reviewer)
   immediately before compiling. The Looper host/council are PRE-SEEDED from
   these (builder = looper host, reviewer = judge, architect = spec author). The
   operator may NOT re-litigate model choice here - state the mapping and move
   on.

4. **Interview in stages, coaching against the rubric (progressive disclosure).**
   The rubrics live in the installed package's rubrics directory - `LP_DIR` +
   `/rubrics/` (NOT in this skill dir). Read only the relevant one per stage:
   - Goal stage - read the goal rubric (`goal-rubric.md`): push toward a concrete
     outcome, definition-of-done, scope boundaries, context sources.
   - Verification stage - read the verification rubric (`verification-rubric.md`,
     the highest-leverage one): force typed criteria (`programmatic` / `judge` /
     `human`); push hard toward programmatic; warn if everything is vibe.
   - Gates/control stage - read the control rubric (`control-rubric.md`): require
     termination guards: `max_iterations` (-> Build `max_cycles`), a wall-clock or
     budget cap (-> `max_wall_clock_minutes`). The council rubric
     (`council-rubric.md`) is context only - Build's cross-AI panel supersedes
     Looper's single judge.

5. **Build the coached dict and stub-synthesize the unused schema fields.**
   Assemble `{version: 1, meta, goal: {statement, definition_of_done,
   verification: [...]}, loop_control: {...}}`, then call
   `synthesize_stub_fields(coached, roles)` to fill host/council/gates/
   workspace/execution (so it validates - these stubs are NEVER executed; Build
   is the runner). Write the result to
   `.consensus/architect/<goal-id>/looper-plan/loop.yaml`.

6. **Compile + preview.** Run the compile helper to validate and render:

   ```bash
   python3 - <<'PY'
   from consensus_mcp.looper_plan import compile as c
   import json, pathlib
   g = pathlib.Path(".consensus/architect/<goal-id>/looper-plan")
   resolved, md = c.compile_plan(g / "loop.yaml")
   (g / "loop.resolved.json").write_text(json.dumps(resolved, indent=2, sort_keys=True) + "\n", encoding="utf-8")
   (g / "LOOP.md").write_text(md, encoding="utf-8")
   print("compiled")
   PY
   ```

   Show the operator the ASCII flow preview from `LOOP.md`, labeled clearly:
   **"design preview - NOT the Build supervisor loop."** Confirm before seeding.

7. **Seed the Build goal.** Run:

   ```bash
   python3 -c "
   import json; from consensus_mcp.looper_plan import seed
   r = json.load(open('.consensus/architect/<goal-id>/looper-plan/loop.resolved.json'))
   print(seed.seed_build_inputs(r, '.consensus/architect/<goal-id>'))"
   ```

   This writes `problem.md` (the architect's context), `looper-suggestions.yaml`,
   and `looper-plan-manifest.yaml`.

8. **apply-looper-suggestions (two-tier confirm; NEVER silent).** Read
   `looper-suggestions.yaml` and present a VISIBLE DIFF against the current
   `.consensus/config.yaml` `architect_loop:`. Use AskUserQuestion:
   - Tier 1 - EXECUTION CONTRACT (`frozen_verification` + `acceptance_gates`):
     requires explicit per-field or batch confirmation. Flag any acceptance gate
     with `needs_operator_edit: true` (non-`exit_zero` expect) for the operator
     to define - never apply it as-is.
   - Tier 2 - TERMINATION CAPS (`max_cycles`, `max_wall_clock_minutes`):
     pre-filled, but still require one confirm action.
   - Offer "accept all suggestions" as a single action. On confirm, write the
     chosen values into `.consensus/config.yaml` `architect_loop:`. If the
     operator declines, leave config untouched and proceed with Build's defaults.

9. **Hand off to Build (do NOT run the loop).** Tell the operator:
   "Looper plan seeded. Run `consensus-mcp-architect step --goal-dir
   .consensus/architect/<goal-id>`. The architect will read the coached
   `problem.md` + `looper-plan/` as context when authoring the spec; the human
   spec-approval and delivery gates are unchanged."

## File Rules

- Write argv arrays, never shell command strings, in `loop.yaml`.
- Never write `.consensus/config.yaml` without the explicit operator confirm
  (step 8).
- Never re-litigate model choice - Build `roles:` are authoritative.
- Never edit any Build supervisor module (`_architect_lane.py`, the
  `architect.loop_step` handler, etc.). This skill only writes goal-dir inputs.
- Never run `consensus-mcp-architect step` yourself - hand off to the operator.
