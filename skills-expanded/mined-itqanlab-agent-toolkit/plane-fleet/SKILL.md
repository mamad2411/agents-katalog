---
name: plane-fleet
description: "Run work from a Plane board with teams of agent roles, one section per kind of work. Triggers: 'plane fleet', 'fleet run', 'run the board', 'work the tickets', 'work PROJ-12', 'test PR 212', 'plan this', 'write a ticket for this', 'ship the queue on my own'. Engineering: a PM claims tickets oldest first, engineers each take one ticket into their own git worktree and environment slot and open a PR, testers check every PR blind in the browser and add tests, and the PM merges approved PRs in groups, confirms CI and deploy, and moves tickets to Done. Core: a planner turns requests into right-sized tickets, a board specialist files and reshapes them, a scanner does read-only counting. Roles can run on other coding CLIs too, picked per spawn by task kind and remaining budget, with real cost and time measured per ticket. Needs a Plane MCP server and the GitHub CLI."
license: MIT
compatibility: "Needs git, the GitHub CLI (gh) signed in, python3 and node 18 or newer, and a Plane MCP server named plane (see README.md). Optional: other coding CLIs for non-default executors. Network access to Plane and GitHub."
metadata:
  author: itqanlab
  version: 3.0.0
  category: devops
  short: "Run a Plane board with sections of agent roles"
  starter: "fleet run: work the board until the queue is empty"
---

# plane-fleet

Teams of agent roles that work a Plane board the way small teams do, one section per kind of
work. Nobody waits for anybody: an engineer opens a PR and moves on, a tester picks up any open
PR at once, the PM lands what is approved and green.

All paths below are relative to this folder, the one that holds this file.

## Sections

| Section | What it does | Folder |
| --- | --- | --- |
| core | runs the fleet: the PM, the planner, the board specialist, the scanner, solo mode, the `fleet` command, the shared references | `core/` |
| engineering | ships code: an engineer per ticket, a tester per PR, the merge queue | `engineering/` |
| social | posters, carousels and reels (planned: its roles are built and tested before they run) | `social/` |

Each section's `README.md` says what it holds. Each role is a folder with the same parts:
`role.md` (who it is, its limits, its report, and an index of its skills) and `skills/` (one file
per thing it does, read only when that step comes).

## Pick the role, then read its file

| The user asks | Role | File |
| --- | --- | --- |
| fleet run, run the board, work the tickets, keep the fleet going | PM | `core/pm/role.md` |
| plan this, break this down, size or regroup tickets | planner | `core/planner/role.md` |
| write a ticket for this, turn notes into tickets | planner, writing | `core/planner/skills/write-ticket.md` |
| file this plan, merge these tickets, board report | board specialist | `core/board/role.md` |
| count, triage, read these logs | scanner | `core/scanner/role.md` |
| work one ticket to a PR | engineer | `engineering/engineer/role.md` |
| test one open PR | tester | `engineering/tester/role.md` |
| ship the queue alone, one ticket at a time, no team | solo | `core/solo/role.md` |

Read the role file and follow it exactly. It names its skill files and when to read each.

## Agents

The plugin's `agents/` folder holds one short card per role, grouped by section, each carrying
only the tools its role uses: `core/` holds `fleet-planner`, `fleet-board` and `fleet-scanner`;
`engineering/` holds `fleet-engineer` and `fleet-tester`. A card points its agent at the role
file. The PM spawns them as sub-sessions, one per ticket or PR. With no sub-sessions, run solo
mode, or one engineer or tester role by hand. Install notes are in `README.md`.

## Shared references

In the `core` section's references folder:

- `config-schema.md` — the project config and the private per-user override
- `plane-api.md` — the Plane MCP calls and what a board read costs
- `usage-budget.md` — spending a usage window on purpose and stopping safely
- `executors.md` and `executors.json` — which program runs which role, and prices
- `non-claude-adapter.md` — what a role running on another coding CLI must know

In the `engineering` section's references folder:

- `standing-brief.md` — the boundaries every engineer and tester keeps
- `ticket-rules.md` — when to file a ticket, and how big one may be
- `brief-checklist.md` — defect classes that caused repeat rework; the PM copies the ones that apply into each brief
- `notify.md` — telling the client, with a screenshot

## The fleet command

`scripts/fleet` runs lanes on other coding CLIs and holds the shared tools:

```bash
scripts/fleet config --cwd <repo>          # the project config, merged
scripts/fleet status                       # machine gate, budget, slots, lanes, held work, open PRs, trunk CI
scripts/fleet held set PROJ-12 --blocked-by PROJ-11   # a ticket skipped for its blockers; status says when to stack it
scripts/fleet resources                    # memory, swap, CPU and disk on any OS, the biggest processes, the fixes
scripts/fleet cache-server env --cwd <repo> # one Nx cache for every worktree (eval its output)
scripts/fleet slot-template clone A --cwd <repo>   # slot A's DB from the migrated, seeded template; exit 3 = run the recipe
scripts/fleet gate-stamp check --pr 212    # a group PR may merge on the local gate stamp
scripts/fleet watch PROJ-12-ci -- gh run watch 123   # one background watcher per name; a second start is refused
scripts/fleet pick --role engineer --kind api --cwd <repo>
scripts/fleet cost --since 2026-10-01      # real spend and time per merged ticket
scripts/fleet cost --ticket PROJ-12        # one ticket's sessions in order
scripts/fleet retro --since <run start> --cwd <repo>   # numbered findings on the run: cause, fix, owner; exit 3 on an alert
scripts/fleet review --cwd <repo> --md <file>          # every run measured the same way, kept, compared with the runs before
scripts/fleet findings /tmp/PROJ-12-review.md          # only the findings of a review transcript, deduplicated
scripts/fleet watch --stop-prefix PROJ-12-  # stop every watcher of one ticket, before the report
scripts/fleet free-models refresh          # today's free models, for read-only scans
scripts/fleet stats --role engineer        # the executor scoreboard
```

The token counts the log keeps for a sub-session are the size of its last call, not its spend;
`cost` reads the spend from the session files. Engineering's own tools (board drift, pre-pick
triage, git tidy, the leftover sweep) are in its scripts folder.

## Project config

Each repo carries `.plane/config.json` (Plane project, trunk, quality gate, CI, deploy, slots).
Private values (client contact, server names, timezone) go in a per-user override outside the
repo. When a repo has no config yet, the PM and solo roles build it from the board and the repo.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
