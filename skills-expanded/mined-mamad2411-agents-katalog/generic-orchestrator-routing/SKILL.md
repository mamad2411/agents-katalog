---
name: generic-orchestrator-routing
description: Apply when deciding whether a user request should route through the dev-team orchestrator or be answered directly. Defines the substantive vs trivial threshold and the bare-/orchestrator aliasing rule.
metadata:
  stack: [generic]
  specificity: 95
---

# Orchestrator routing

The plugin orchestrator is the entry point for **substantive engineering work**. It is overkill for trivial questions and lookups. This skill defines the threshold and the alias rules.

## The threshold

### Direct answer (no orchestrator)

Handle these inline without invoking the orchestrator:

- **Explanatory questions** — "what does X do", "where does Y live", "how does Z work", "what's the difference between A and B".
- **Single-file lookups** — read this file and tell me, find the function, grep for this symbol.
- **Status / inventory** — what's on this branch, what tests exist, list the skills, what's the current Expo SDK version.
- **Naming / typo / cosmetic edits** — rename this variable, fix this spelling, reformat this block.
- **Doc reads** — what does CLAUDE.md say about X, summarise this design doc.
- **Simple `run X` commands** — run the tests, run the lint, run the dev server.

### Orchestrator (delegate to the `dev-team:orchestrator` agent)

Invoke the orchestrator for anything that touches the 7-gate pipeline (see [`generic-gate-pipeline`](../generic-gate-pipeline/SKILL.md)):

- Features (new behaviour, even small).
- Bug fixes (anything requiring a failing test).
- Refactors that change behaviour or touch multiple files.
- Multi-stack changes (api + spa, or api + mobile-app).
- Anything requiring tests to be written.
- Anything where requirements / BDD / design might be incomplete.
- Anything where a human approval gate matters.

**When in doubt, route through the orchestrator.** The cost of going through the orchestrator on a borderline trivial task is small. The cost of skipping the orchestrator on a substantive task — and shipping un-tested, un-reviewed code — is large.

## Aliasing rules

- The local slash command `/orchestrator` is **a thin alias** that delegates to the `dev-team:orchestrator` **agent** — invoke it as a subagent, `subagent_type: dev-team:orchestrator` (it is an agent, not a slash command; see [`rules/dev-team-contract.md`](../../rules/dev-team-contract.md)). There is no local orchestrator persona.
- When the user types bare `/orchestrator`, do NOT interpret as freeform text, do NOT search the repo for it as a string — delegate to the `dev-team:orchestrator` agent immediately with whatever arguments follow.
- When a request arrives in **plain English** without any slash command, apply the threshold above. If it's substantive, invoke the orchestrator before doing anything else. If it's trivial, answer directly.
- Do NOT improvise an alternative agent lineup. Do NOT do "inline reviews" or "inline planning" — that's the orchestrator's job.

## Missing a capability? Default to the plugin

If a task needs a skill, workflow, or agent that the **local** toolbox doesn't provide, assume the `dev-team` plugin already covers it before hand-rolling a local equivalent. The plugin ships a large catalogue (dozens of `/dev-team:*` skills plus specialist agents) that this repo's `rules/delegation-map.md` only samples. When something is missing locally:

- Look it up first — `/dev-team:help` (or the plugin's `knowledge/skills-registry.md`) lists the full set.
- Prefer routing to the plugin — invoke the matching `/dev-team:*` skill, or delegate to the `dev-team:orchestrator` agent for multi-step work — over writing a new local skill/command.
- Only add a **local** entry when the gap is genuinely project-specific (paths, glossary, vendor integrations) or is a thin alias that pre-loads project context. See `rules/delegation-map.md` → "When to write a local entry vs use the plugin".

## Examples

| User input | Route |
|---|---|
| "What does dotnet-vendor-adapters say about HMAC?" | Direct answer (lookup) |
| "Where is the BFF proxy?" | Direct answer (lookup) |
| "Add a daily spending limit per card" | Orchestrator (feature) |
| "Fix the off-by-one in the SCA approval window" | Orchestrator (bug fix) |
| "Rename `IdentityNumber` to `NationalId` everywhere" | Orchestrator (multi-file refactor with behavioural impact) |
| "What tests exist for the issuance flow?" | Direct answer (inventory) |
| "Run `dotnet test`" | Direct answer (command) |
| "Add a /toolbox command that lists local skills" | Orchestrator (new feature) |
| "Update the description in nextjs-sentry/SKILL.md to mention the new project name" | Direct answer (cosmetic edit) |
| "Refactor the gate-pipeline skill to add a Gate 0 for triage" | Orchestrator (substantive — affects the process) |

## Anti-patterns

- Routing every plain-English message through the orchestrator. Lookups, status checks, and explanations don't need it.
- Skipping the orchestrator because "this is just a small fix". Small fixes still need failing tests if behaviour changes.
- Treating bare `/orchestrator` as a string to search for. It's a deterministic alias — invoke immediately.
- Inventing a "local orchestrator" persona because the request seems "less complex than what the plugin handles". The plugin is the authority; the local layer adds stack-tag filtering and project context, not a different persona.
