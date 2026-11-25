---
name: omt
description: oh-my-t3 router. Lists the omt workflows for T3 Code and when to use each.
disable-model-invocation: true
---

# oh-my-t3

omt runs workflows in this T3 thread: the main thread explores, plans, and builds, and role-routed children started with the T3 `delegate_task` tool review and test the work. Pick the workflow that matches the request, then load that skill.

On git actions, reply style, tests, and model choice, the user's own instructions win over omt defaults. Their message comes first, then their `AGENTS.md` or `CLAUDE.md`. omt owns the workflow steps ([User instructions win](references/delegation.md#user-instructions-win)).

## Workflows

| Skill | Use it when |
| --- | --- |
| `omt-ulw` | The user wants something built or fixed end to end. The main thread explores, asks, plans, and builds; one review child and one QA child check the work. The default. |
| `omt-plan` | The user wants a reviewed plan before code changes, or a stress test of a vague goal, or `omt-ulw` needs a plan for a HEAVY task. |
| `omt-design` | The user wants designs, mockups, screens, or a design pass. |
| `omt-code-review` | The user wants a review of uncommitted changes, a branch, a commit, or a PR (`omt-code-review <number>`). |
| `omt-research` | The user wants a cited answer from this repository, docs, or the web, with no code changes. |
| `omt-setup` | The user wants help with omt, or wants it set up, configured, or updated. It asks before each write. |

`omt-swarm` builds a plan as separate worktree threads. It installs only with `omt install --with omt-swarm`.

Each skill name works as a composer mention: `$omt-ulw` becomes `/omt-ulw` in Claude and Cursor, `/skill:omt-ulw` in Pi, and stays `$omt-ulw` in Codex.

For the CLI, run `omt help` and `omt help <command>`. The shared T3 rules are in [delegation.md](references/delegation.md), the roles in [roles.md](references/roles.md), and the result blocks in [results.md](references/results.md).
