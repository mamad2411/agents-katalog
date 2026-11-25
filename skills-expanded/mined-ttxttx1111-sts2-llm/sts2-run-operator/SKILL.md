---
name: sts2-run-operator
description: Operate the Slay the Spire 2 workspace by probing game state, issuing actions, and persisting lessons for future runs
compatibility: opencode
---

## What This Skill Does

This skill standardizes how to operate this repository as a long-running Slay the Spire 2 agent workspace.

It is for sessions where the goal is not just to inspect the game once, but to keep building a reliable run loop with durable memory.

## When To Use It

Use this skill when you need to:

1. connect to the local `STS2MCP` API;
2. inspect the current game state;
3. issue a single documented game action;
4. save state snapshots or action responses into the active run folder;
5. update persistent lessons and known issues after discoveries or failures.

## Source Of Truth

Read these files first:

1. `README.md`
2. `docs/architecture.md`
3. `docs/operations.md`
4. `memory/lessons.md`
5. `memory/issues.md`
6. `prompts/developer_agent.md`
7. `prompts/player_agent.md`

Implementation entrypoints:

1. `src/sts2_agent/main.py`
2. `src/sts2_agent/api.py`
3. `src/sts2_agent/journal.py`

## Working Rules

1. Prefer the smallest correct next step.
2. Do not assume undocumented endpoints or payloads when the live API can be queried.
3. Save evidence of failures instead of paraphrasing them from memory.
4. After every meaningful discovery, update either `memory/lessons.md` or `memory/issues.md`.
5. Treat menu automation and in-run automation as separate problems unless the live API proves otherwise.
6. Respect the role split: developer agent handles lifecycle; player agent handles active gameplay.

## Standard Workflow

### 1. Ensure A Run Record Exists

Create a run record if there is no active run folder for the current session:

```bash
python -m src.sts2_agent.main init-run
```

### 2. Probe The API

Use this first when the game may not be running or when the API shape needs confirmation:

```bash
python -m src.sts2_agent.main probe-api
```

Expected confirmed singleplayer entrypoint:

- `GET /api/v1/singleplayer`
- `POST /api/v1/singleplayer`

### 3. Read Live State

Use JSON for programmatic work:

```bash
python -m src.sts2_agent.main read-state --save
```

Use markdown for quick human-readable inspection:

```bash
python -m src.sts2_agent.main read-state --format markdown
```

### 4. Issue One Action At A Time

Examples:

```bash
python -m src.sts2_agent.main act end_turn --save
python -m src.sts2_agent.main act choose_map_node --params '{"index":0}' --save
python -m src.sts2_agent.main act choose_event_option --params '{"index":1}' --save
python -m src.sts2_agent.main act play_card --params '{"card_index":2,"target":"JAW_WORM_0"}' --save
```

After actions that can change indices or state shape, read state again before the next action.

### 5. Persist Learnings

Update:

1. `memory/lessons.md` for reusable heuristics or integration truths;
2. `memory/issues.md` for recurring blockers, bugs, and mitigations;
3. `memory/run_history.jsonl` via the existing run tooling and saved run artifacts.

## Current Known Limitation

The current documented workflow confirms the API can report `state_type: menu`, but this workspace does not yet have a documented automated path for starting a fresh run from the main menu.

For now:

1. if the game is at `menu`, ask for manual run start or build menu automation as a separate feature;
2. once inside a run, use the documented `/api/v1/singleplayer` state and action flow.

## Success Criteria For A Good Session

At the end of a useful session, the repository should contain:

1. saved state or action artifacts under `runs/<run_id>/`;
2. any code changes needed for the next iteration;
3. at least one durable memory update if something new was learned.
