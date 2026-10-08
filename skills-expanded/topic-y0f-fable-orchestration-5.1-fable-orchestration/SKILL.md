---
name: fable-orchestration
description: Use when running Claude Fable 5.1 in Claude Code - wiring Fable as architect or advisor with Opus/Sonnet lanes, choosing advisor vs subagents vs teams vs workflows vs /goal, setting effort per model, or when Fable fell back to Opus, over-plans, stops early, or burns tokens on routine work.
---

# Fable 5.1 Orchestration

Pay Fable rate only for judgment. Everything else runs on cheaper lanes.

**Rule:** Fable decides. Opus 5 builds. Sonnet 5 grinds. Haiku 4.5 scouts. Fresh-context verifier checks. Fable earns its rate on ambiguous scope and parallel builds, not on fully specified single-builder tasks.

Facts + sources: `reference/models.md`. Configs: `reference/wiring.md`. Paste-in prompts: `reference/prompt-kit.md`. Symptom -> fix: `reference/failure-modes.md`. Drop-in `settings.json` and `CLAUDE.md` examples: `${CLAUDE_PLUGIN_ROOT}/settings/`.

## Lanes

Agents ship with this plugin as `fable-orchestration:<name>`.

| Lane | Agent | Model | Effort | Job |
|---|---|---|---|---|
| Architect | main session | `fable` ($10 / $50, cache read $0.25) | `high` | Plan, ambiguous calls, root cause, final judgment |
| Architect, one-off | `fable-architect` | `fable` | `high` | Plan-only pass from an Opus/Sonnet main. Returns text, no code |
| Builder | `opus-builder` | `opus` ($5 / $25) | `high` | Multi-file implementation, hard debugging |
| Worker | `sonnet-worker` | `sonnet` ($2 / $10) | `medium` | Boilerplate, tests, migrations, docs, research reads |
| Scout | `haiku-scout` | `haiku` ($1 / $5) | none (no effort levels) | Locate files, grep, condense logs |
| Verifier | `fresh-verifier` | `opus`, clean context | `high` | Check work vs spec. Never the builder |

Anthropic's Fable 5.1 guidance: `low` effort on Fable often exceeds prior models at `xhigh`. Cheaper lanes are for volume (many files, long test runs, research reads), not for doubt about quality.

## Pick wiring

1. **Fable steers, cheap model types** -> advisor mode (experimental, Anthropic API only). Accept Fable usage-credit consent once via `/model fable`, then `/model sonnet` or `opus`, then `/advisor fable`. Each consult re-reads the full transcript uncached: $10 x transcript MTok. Cheap when consults are few and you `/clear` often. Cost test: consults x $10 x transcript MTok vs the ~$0.10-0.20 those decisions cost as Fable-architect turns. Fable main accepts only a Fable advisor (Claude Code rule, stricter than the raw API).
2. **Fable plans, parallel agents build** -> architect + delegate. `/model fable`, `/effort high`. Fable spawns `opus-builder` / `sonnet-worker` async, keeps working, spawns `fresh-verifier` at end. Default for real builds. With one builder it is overhead; wall-time savings need several builders on independent modules.
3. **Peers need to argue** (competing hypotheses, cross-layer feature, parallel review) -> agent teams. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Fable lead, Sonnet teammates. ~7x tokens of a solo session when teammates plan. Interactive only. Use rarely.
4. **Same step across many items** (audit 200 files, migrate a tree, fix-until-green) -> workflow. Type `use a workflow to ...` or `ultracode:`. Triggers only in a prompt you type; for unattended runs save the workflow once, then invoke `/<name>`. Script holds the loop; Fable context holds only the result.
5. **Long unattended run with verifiable end state** -> `/goal <condition>` on top of any pattern. Haiku evaluator re-prompts until tests pass / queue empty / `stop after N turns`. Needs `claude --permission-mode auto` or prompts block.

Skip Fable entirely for: renames, formatting, lockfile bumps, single-file bug with clear repro, any fully specified task a cheaper lane finishes in one pass. On those, a cheaper lane solo beats orchestration on both cost and wall time; orchestrate for ambiguity and parallel builders. Measure your own task shape with `${CLAUDE_PLUGIN_ROOT}/bench/run.sh` (3 runs per arm by default; single runs are noise).

## Effort

`/effort low|medium|high|xhigh|max`. Settings keys (`effortLevel`, `modelSettings.<id>.effortLevel`) accept `low`-`xhigh` only; `max` is `/effort`-only. Subagent override: frontmatter `effort:`.

- Fable `high` default. `max` never for routine.
- Measure before raising: same task at `high` and `xhigh`, compare `/usage` cost and whether `fresh-verifier` passes both. Keep `xhigh` only if the verifier flips FAIL to PASS.
- Correct but slow -> drop one level. Wrong -> raise one level, never jump to `max`.
- Higher effort = more verification and more unrequested tidying. Pair with the no-tidying block.
- `ultracode` is a valid `/effort` value: `xhigh` plus automatic workflows for every task. Session-wide, expensive.

## Cost levers (in order)

1. **Cache.** Main session caches 1h on subscription, 5m once Fable bills to usage credits; subagents 5m by default. Set `promptCacheTtl: "1h"` and `subagentPromptCacheTtl: "1h"` for long sessions. Fable cache reads cost $0.25/MTok (2.5% of input; Opus and Sonnet stay at 10%). That makes Fable re-reading its own context cheaper than Opus reading the same context ($0.50). Delegation saves on output ($50 vs $25) and on fresh input, and costs a new cache write per spawned agent. Long-lived agents resumed with `SendMessage` beat spawn-per-task, which pays cache writes again.
2. **Async delegation.** Spawn, keep working, read results when they land. Blocking on the slowest agent wastes Fable wall-clock and context.
3. **Lane routing.** `CLAUDE_CODE_SUBAGENT_MODEL=opus` so unpinned subagents never land on Fable. Confirm with `/tasks` (model + effort per agent). After a build check `/usage`: if Fable output tokens exceed Opus output tokens, Fable did execution - move it to lanes.
4. **Context hygiene.** Verbose output (tests, logs, docs fetch) -> subagent. `/clear` between unrelated tasks. CLAUDE.md under 200 lines.
5. **Effort** last. Lower only after 1-4.

## Prompting Fable 5.1

Short instructions steer better than rule piles. Strip scaffolding written for older models - step-by-step recipes reduce Fable output quality. Anthropic reports an instruction given once holds better than on Fable 5 (unconfirmed at launch): drop per-turn repetition and re-test.

`reference/prompt-kit.md` has a per-block table of what Claude Code's own system prompt already says to a Fable main (checked in a live 2.1.266 session) versus what a subagent or raw API prompt gets (nothing). For a Fable main in Claude Code paste only: **no unrequested tidying**, **targeted edits**, the lane-routing line, the test-coverage lines, **verify with fresh eyes**. **act don't overplan**, **autonomous run**, **progress updates**, **context anxiety** are already in the system prompt there. Agent bodies and API prompts need the full set.

Hand it the hard problem first. Fable scopes, asks, executes. Don't pre-chunk into small tasks.

## Traps

Detail in `reference/failure-modes.md`.

- **Classifier fallback.** Cyber-flagged request -> Opus 4.8. Bio-flagged -> Opus 5. One transcript notice, then the session stays on the fallback. First request carries CLAUDE.md + git status, so a security-flavored repo trips it before you type. Interactive: `switchModelsOnFlag: false` pauses and asks. Unattended: keep default `true` or the run stalls; check `/usage` after.
- **Reasoning extraction.** "Show / print your reasoning" in any prompt can return a refusal. Audit CLAUDE.md, skills, hooks.
- **Early stop.** Long runs may end with "I'll now run X" and no tool call. Autonomous-run block. Interactive: `continue`.
- **Context anxiety.** Never show Fable a remaining-token count.
- **Blocking on subagents.** Spawn async. Resume named agents with `SendMessage` instead of respawning.
- **Forks run on Fable.** `subagent_type: "fork"` inherits the full transcript and the parent model, and ignores `CLAUDE_CODE_SUBAGENT_MODEL`. Fork only when the task needs the whole conversation.
- **Agent teams auto-form.** With teams enabled, any named subagent becomes a teammate. Set env to `0` for plain delegation.

## Pre-run checklist

1. `/model` shows `fable`? Claude Code >= v2.1.255? Usage-credit consent given if the plan needs it?
2. Which wiring (1-5) and why?
3. `CLAUDE_CODE_SUBAGENT_MODEL` set so unpinned agents don't inherit Fable?
4. Effort per lane set, not everything on `high`?
5. Prompt kit blocks in CLAUDE.md, no "explain your reasoning" text anywhere?
6. Verifier is fresh context, not the builder?
7. Long run: `/goal` condition has one measurable end state, a check command, and a stop clause?
