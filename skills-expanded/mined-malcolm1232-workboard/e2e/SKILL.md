---
name: e2e
description: Run (and extend) the reusable end-to-end test harness for board-steward. Use when the user wants to verify a board-steward overhaul end-to-end — multi-board routing/isolation, reconciliation (gating + real-Haiku moves), or a future feature — WITHOUT polluting their live board. Triggers: "run e2e", "/e2e", "test multi-board", "test recon end to end", "verify the overhaul", "regression test the board", "does routing/recon still work". The harness isolates all state, uses throwaway boards, and asserts the live board is untouched.
---

# e2e — board-steward end-to-end test harness

A reusable harness that codifies the verification patterns proven during **ARCH REDESIGN v2** (multi-board routing + reconciliation). Run it to regression-test those overhauls — or extend it for the next one — instead of hand-writing throwaway test scripts each time.

Source of the redesign it tests: `~/Desktop/WorkBoard/docs/ARCH_REDESIGN_V2.md`.

## The cardinal rule (why this exists)

**A test must NEVER pollute the user's live board or global state.** The harness enforces this structurally:

- **Isolated state** — `BOARD_REGISTRY` / `BOARD_ASSIGNMENTS` / `BOARD_ACTIVE` are pointed at temp files; `BOARD_NO_SERVER=1` forces direct file writes for tests that don't need a server. The real `~/.board-steward/` is never touched.
- **Throwaway boards** — every board under test is a temp dir, seeded in-memory or from `templates/board.json`.
- **Live-board guard** — the live board's (`:7891`) card count is captured before the run and asserted **unchanged** after. If a test touches it, the suite fails.
- **Cleanup** — all temp dirs are removed at the end.

## How to run

```bash
python3 ~/.claude/skills/e2e/e2e_workboard.py multiboard    # routing + $HOME disambiguation (no LLM, free)
python3 ~/.claude/skills/e2e/e2e_workboard.py recon         # only_discovered flag + gating + CLAUDECODE path (free)
python3 ~/.claude/skills/e2e/e2e_workboard.py recon-haiku   # real Haiku: IP→done / IP→backlog (~1 Haiku call)
python3 ~/.claude/skills/e2e/e2e_workboard.py all           # multiboard + recon (free tier)
python3 ~/.claude/skills/e2e/e2e_workboard.py all --haiku   # everything, including the Haiku E2E
```

Override the repo with `BOARD_REPO=/path/to/WorkBoard` (default `~/Desktop/WorkBoard`).
Exit code `0` = all passed, `1` = a failure (printed at the bottom), `2` = bad args / repo not found.

## Test catalog (what each group proves)

**multiboard** — the v2 multi-board work
- `routing_isolation` — a card added from inside project A lands on A, never B; `last-active` tracks the last-mutated board.
- `disambiguation` — at `$HOME`, the **last-active** board wins over a newer-mtime board; mtime is only the fallback (the wrong-board bug that started v2).

**recon** (free) — the v2 reconciliation work
- `only_discovered_flag` — `reconcile_sweep(only_discovered=True)` scopes to bootstrap-mined cards; `False` reconciles every non-done card (so SessionStart catches live cards).
- `gates_short_circuit` — `--reconcile-only` makes **no Haiku call** when there are no non-done cards (Gate A) or no recorded project activity (Gate B).
- `claudecode_path` — `CLAUDECODE=1` writes a prose `recon_pending.json` (no Haiku); proves the spawn's `env -u CLAUDECODE` is load-bearing for the autonomous Haiku path.

**recon-haiku** (costs ~1 Haiku call) — the real end-to-end
- `haiku_e2e` — a real `claude -p --model haiku` pass moves a *shipped* In-Progress card → **done** and a *"nvm/skip"* card → **backlog**.

## Extending for the NEXT overhaul

Add a function `test_<group>_<name>(ctx)` in `e2e_workboard.py` and register it in `GROUPS`. Use the context helpers — they keep the cardinal rule automatic:

- `ctx.board(cards=[...])` → a throwaway project board.json (pass `from_template=True` for the real seed).
- `ctx.card(num, column, title, tags=[...])` → a minimally-valid card dict (real cards always carry an `id`).
- `ctx.assert_eq(name, got, want)` / `ctx.assert_true(name, cond, detail)` → record pass/fail.
- State is already isolated in `Ctx.__init__`; the live-board guard runs automatically.

**Always**: isolate state, use throwaway boards, and never assume the live server's state. If a feature needs a running server, start it on an explicit free port (e.g. 7950) and verify `:7891`'s count is unchanged.
