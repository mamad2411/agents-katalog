---
name: assemble-team
description: Assemble the RIGHT agent team for a project of ANY stack — select the core agents that fit, forge new senior specialists for gaps (mobile, game, data/ML, embedded, blockchain, …), prune the rest, and write the team roster. Runs at kickoff after /refine-idea (greenfield) or /adopt (brownfield). Trigger words — assemble team, staff the project, build the team, what agents do I need, team for my stack, mobile/game/data project.
---
# /assemble-team — put the right senior team on any project

**Use when:** a project is scoped (`/refine-idea` or `/adopt` done) and you need the team that fits its stack —
web, mobile, game, data/ML, embedded, blockchain, desktop, anything. **Owner:** `agent-architect`.

## Procedure
1. **Read the need** — `docs/planning/project-brief.md` and/or `CLAUDE.md` / the `/adopt` codebase-map: platform,
   language(s), domain, integrations.
2. **Select** the core agents that fit (roles are stack-adaptive; assign only what's needed).
3. **Spot gaps** — domains the core doesn't cover (e.g. Flutter, Unity, SwiftUI, Solidity, ML, firmware).
4. **Forge** a senior specialist for each gap via `/forge-agent` (agent + any stack-specific skills), to the house
   quality bar.
5. **Prune** — drop/inactive the agents this project won't use.
6. **Roster** — write `docs/planning/team.md` (who, role, core-vs-forged, why) from `docs/_templates/team.md`.

## Guardrails
Assign only what the project needs — no idle agents. Every forged agent meets the full quality bar (senior,
trigger-rich description, wired to skills) — never a thin stub. Prefer adapting a core role over forging a
near-duplicate. Record why each agent is on (or off) the team.

## The selection rule
Selection is not taste. Each row is a predicate over things that already exist — the brief, `vantry.yml`, the
files on disk — so two runs over the same project produce the same team, and a wrong team is falsifiable.

| Role | Selected when |
|---|---|
| `tech-lead-orchestrator`, `qa-test-engineer`, `security-engineer` | **always** — the non-prunable core |
| `debugger` | **always** — it receives every `FAILED` verdict; without it a failure has no owner |
| `backend-engineer` | the project has a server entry point, an API, or a job |
| `frontend-engineer`, `ui-ux-designer` | `project_type` is `web` or `mobile` |
| `ui-ux-designer` alone | `project_type` is `game` or `desktop` — a player-facing surface, but no web frontend |
| *(no frontend role)* | `project_type` is `cli`, `library`, `service`, `data`, `embedded` or `contract` — a React persona on a firmware project is a wrong answer, not a spare hand |
| `database-architect` | a migrations directory or an ORM schema exists |
| `payments-engineer` | the brief names money, subscriptions or refunds, **or** `sensitive_paths` matches `**/payment*/**` or `**/billing/**` |
| `ai-integration-engineer` | the brief or the dependencies name an LLM or model provider |
| `devops-engineer` | a deploy target, a container file, or `.github/workflows/` exists |
| `product-strategist` | a brief exists (always, on greenfield) |
| `sprint-planner` | a backlog will be produced — i.e. `/bootstrap` or `/adopt` is running |
| `content-marketer`, `growth-strategist` | the project has an audience to reach; skip for internal tooling |
| `agent-architect` | **always** — it is what forges the gaps below |

**The six project types with no engineering role above are the interesting ones**, and this was left to taste —
so two runs staffed a Unity project differently, and one typed `mobile` received a Next.js persona. They are
gaps **by definition**:

| `project_type` | the lead engineering role is **always forged** | what it must own |
|---|---|---|
| `game` | e.g. `unity-gameplay-engineer`, `godot-engineer` | the loop, frame budget, input, scene lifecycle, build pipeline |
| `embedded` | e.g. `firmware-engineer` | memory and interrupt discipline, the HAL, flashing, on-device test |
| `contract` | e.g. `solidity-engineer`, `anchor-engineer` | reentrancy, gas, upgradeability, the local-chain suite |
| `data` | e.g. `data-pipeline-engineer` | schema contracts, idempotent backfills, late and duplicate records |
| `desktop` | e.g. `tauri-engineer`, `electron-engineer` | packaging, auto-update, OS integration, code signing |
| `library` | e.g. a specialist for the target ecosystem | the public API surface, semver, the consumer smoke |

Anything else the table does not cover and the project needs is a **gap** too: forge it with `/forge-agent`,
never stretch a generalist over it. A Flutter, Unity, Rust, Solidity or ML project has at least one.

## What reads the roster
`docs/planning/team.md` is not a memo. `scripts/kanban/lint-kanban.sh` fails any issue whose `agent` column
names a persona that does not exist in `agents/`, and `scripts/validate-agents.sh` fails any persona missing
from `agents/README.md`. So the team you write here is the team `/next` can actually dispatch to — and a role
you selected but never created will stop the board, loudly, at the first issue that names it.

## Done when
`docs/planning/team.md` lists a complete, senior team matched to the project's actual stack — and the forged
agents exist in `agents/`.
