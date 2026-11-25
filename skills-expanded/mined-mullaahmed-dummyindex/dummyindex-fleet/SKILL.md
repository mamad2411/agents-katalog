---
name: dummyindex-fleet
description: "Babysit a checkpointed fleet run: sweep a host-side tracker into intake JSON, group tickets into file-disjoint proposal-sized units, and drive them in parallel through the deterministic `context fleet` CLI — worktree-isolated orchestrators, spend metering under a budget circuit-breaker, gate-and-skip anti-stall rules, dormant-agent probes, and resume-from-state recovery. All run state lives in committed CLI artifacts (RUN-MANIFEST.md + state.json), never transcripts. The merge/landing phase is opt-in. Use for /dummyindex-fleet, $dummyindex-fleet, run the fleet, overnight run, multi-proposal sweep, or resume a fleet run."
---

# /dummyindex-fleet / $dummyindex-fleet — fleet-run babysitter

> **Installed from dummyindex `__VERSION__`.** Run `dummyindex --version` to confirm the CLI matches. If they diverge, diagnose with `dummyindex context check --versions` (it reports which layer is stale), then run `/dummyindex-update` on Claude or `$dummyindex-update` on Codex to bring the CLI, skills, and this repo's wiring back into sync.

You are the fleet conductor. You never touch run state by hand: **every** read
or write goes through the `dummyindex context fleet` verbs (`init | next |
checkpoint | spend | merge-order | status`). The CLI owns ordering,
file-disjointness, gating, and the budget breaker over the committed artifacts
under `.context/fleet/run-<id>/` (`RUN-MANIFEST.md` written first,
`state.json` last). Your judgment lives in four places: what becomes a unit,
who runs it, whether an agent is alive, and when to merge. No LLM runs inside
the CLI.

Resolve the active host first. On Claude Code this workflow uses native Task
delegation vocabulary. On any other host, take the **portable host path**:
invoke this skill through your own skill mechanism, delegate each orchestrator
to your host's named or generic subagents, and inline the ground-rules block
(section 5) into the delegated prompt instead of looking for a named Claude
subagent type.

## 1. Intake (host-side) — produce `intake.json`

Tracker access (MCP connectors, REST, whatever the host has) stays **outside**
the CLI. Produce a file:

```json
{"units": [
  {"ticket": "<id>", "title": "<one line>", "paths": ["src/a.py", "src/a_test.py"]}
]}
```

- `paths` = repo-relative files the unit may ever touch. This freezes
  file-disjointness for the whole run — be deliberate.
- Extra keys (`repo_hint`, `size`, ...) are allowed; the CLI ignores them.

## 2. Grouping rules

- **Small + disjoint** tickets may share one unit; keep every unit
  proposal-sized (a spec + plan + checklist can describe it — scaffold with
  `context propose` when using `--plans` mode).
- **Big or risky** tickets run solo.
- **Subset-dedupe:** if ticket A's path set is contained in ticket B's, do not
  create both — fold A into B, or accept they serialize (an intersection never
  co-dispatches).
- Duplicate slugs and zero-unit batches are refused at `init`; fix intake
  instead of arguing with the CLI.

## 3. Init

```bash
dummyindex context fleet init --intake intake.json \
  --budget-usd <cap> --max-parallel <n> \
  [--branch-template "{run}/{id}-{slug}"] [--ruling key=value]...
```

Pass the branch template the host repo actually wants (the default
`{run}/{id}-{slug}` is deliberately neutral). Then **commit the run dir**
(`.context/fleet/run-<id>/`) — these artifacts are the run's memory. Read the
printed warnings: a unit without known paths schedules conservatively serially.

## 4. Dispatch loop

```bash
dummyindex context fleet next [--run DIR] --json
```

For each returned unit: create an isolated worktree on the unit's branch,
spawn an orchestrator there, hand it its ground-rules block (section 5) and
its proposal path. Record the wave with
`fleet checkpoint --unit <id> --status building --wave N`.

The envelope is always valid and exits 0:

- `skipped: gated` — a parked question exists. Do **not** stall the fleet:
  surface the question out-of-band, then answer it with
  `fleet checkpoint --unit <id> --status planning --note "<the answer>"`.
- An **empty-but-valid** envelope with nothing left = every lane done/blocked
  — proceed to section 7. A fleet never waits on a question.
- `BUDGET-HALT` (`"halt": true`) — stop dispatching. Correct the meter only
  via the printed resume path (`fleet spend --est-usd -X --adjust` against the
  unit that ran over), then re-run `next`. Never resume silently.

## 5. Orchestrator ground rules (paste verbatim into every dispatch)

```text
You are ONE fleet unit's orchestrator, isolated in your own worktree.
1. Invoke the /dummyindex-build (or $dummyindex-build) procedure on the
   proposal you were assigned; drive its checklist wave-by-wave.
2. Commit policy — conventional types only (feat/fix/test/docs/refactor/chore).
3. Stage ONLY files in your assigned paths[] — a file another unit owns is
   never yours to stage, even if your edit touched it incidentally.
4. Verify in the FOREGROUND before reporting: run the repo's own test/lint
   commands and paste real output. Never report unverified success.
5. Your FINAL message is the report the conductor will checkpoint. End it
   with exactly one magic word:
   DONE    - complete, verified in the foreground, ready to merge
   BLOCKED - cannot proceed; say why and what you tried
   GATED   - parked on an open question; state the question precisely
6. Estimate tokens/dollars honestly when asked for a spend figure.
```

## 6. Metering, liveness, resume

- After each orchestrator report: `fleet checkpoint` its status/wave/note,
  then `fleet spend --unit <id> --est-usd <estimate>` so the breaker tracks
  reality. A unit that crosses the cap trips `BUDGET-HALT` for everyone —
  that is the point.
- **Dormant-agent probe:** if an orchestrator has not reported within the
  probe interval, probe it once. No response → checkpoint it `blocked` with a
  note and let the fleet advance; a stalled lane must never stall the run.
- **Resume-from-state only.** A fresh session resumes by reading
  `RUN-MANIFEST.md` + running `fleet status` and `fleet next`. Never resume
  from transcripts or chat history — they are not the run. If `state.json`
  is missing/corrupt, the CLI fails loud with printed repair/re-init
  instructions; follow them exactly instead of hand-editing around them.

## 7. Merge phase (opt-in)

Never merge without the user's explicit go-ahead for the phase. When given:

```bash
dummyindex context fleet merge-order [--run DIR]
```

Land branches top-down in the printed order — each row already cites the
earlier unit it must land after (shared member paths) or marks itself
parallel-safe. Checkpoint each unit `merging`, then `done`, as it lands;
commit the updated run dir with the landing commits.

## Non-negotiables

- All state through the CLI verbs; never hand-edit `state.json`.
- Deterministic CLI, judgment in this skill — no LLM calls inside the tool.
- Committed artifacts over memory: init dir committed, landing commits
  committed, resume from files only.

