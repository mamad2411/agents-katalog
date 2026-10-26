---
name: using-ai-skills
description: Bootstrap for the ai-skills collection - says to check for a matching skill before acting (including before clarifying questions or exploring the code), which skill covers which stage of development work, and the order to chain them in. Use at the start of a conversation and whenever unsure which skill applies. Ignore it inside a subagent spawned for one specific task.
---

# Using ai-skills

If you were spawned as a subagent for one specific task, ignore this skill and do the
task.

## The rule

Before responding or acting, including before a clarifying question or a look at the code,
check whether a skill covers the task. If one plausibly does, open its `SKILL.md` and
follow it; drop it if it turns out not to fit. Reading a skill costs a few hundred tokens,
while skipping one usually costs a redo: the skills hold the steps that are easy to skip
under pressure (the failing test first, the root cause before the fix, fresh evidence
before "done").

The user can also name a skill directly with `$<name>`. Say in one line which skill you are
using and why.

## Which skill when

| Situation | Skill |
| --- | --- |
| "Let's build / add / change X", anything new | `brainstorming` |
| An approved design or spec that needs implementing | `writing-plans` |
| Feature work that should not touch the current checkout | `using-git-worktrees` |
| Executing a plan with subagents (default when `multi_agent` is on) | `subagent-driven-development` |
| Executing a plan yourself, in this session | `executing-plans` |
| Writing any production code with observable behavior | `test-driven-development` |
| A bug, failing test, flaky test or unexpected behavior | `systematic-debugging` |
| Delegating anything: which subagent, model and effort | `agent-router` |
| Two or more independent problems at once | `dispatching-parallel-agents` |
| A task or feature is done, or before a merge | `requesting-code-review` |
| Review feedback arrived (PR comments, a reviewer report) | `receiving-code-review` |
| About to say "done", "fixed", "passing" or to commit | `verification-before-completion` |
| Work is verified and needs merging, a PR or cleanup | `finishing-a-development-branch` |
| "What did we decide", "did we hit this before" | `cortex-memory` |
| Creating or editing a skill | `writing-skills` |
| A diagram that explains a concept | `excalidraw-diagram` |
| A Rust security audit, only when the user asks for it by name | `rust-review` |

The usual chain for new work: `brainstorming` -> `writing-plans` -> `using-git-worktrees`
-> `subagent-driven-development` (each task through `test-driven-development` and
`requesting-code-review`) -> `verification-before-completion` ->
`finishing-a-development-branch`. A bug enters at `systematic-debugging` instead.

Skills from other sources (plugins, `~/.agents/skills`, `~/.codex/skills`, project skills)
follow the same rule.

## Priority

Process skills come first because they decide how to approach the task; domain skills
then carry it out. "Build X" starts with `brainstorming`; "fix this bug" starts with
`systematic-debugging`.

Instructions from the user and AGENTS.md override skills, and skills override default
behavior. Skip a skill's workflow only when the user says so.

## Thoughts that mean you are about to skip a skill

| Thought | Why it is wrong |
| --- | --- |
| "It is just a quick question" | Questions are tasks; the check takes seconds. |
| "Let me look at the code first" | Skills say how to explore; check before exploring. |
| "I remember what that skill says" | Skills change; read the current version. |
| "The skill is overkill here" | Small tasks are where skipped steps go unnoticed. |
| "I'll do this one thing first" | The first action is the one the skill shapes. |

## Codex notes

- Skills that spawn subagents need `multi_agent = true` under `[features]` in
  `~/.codex/config.toml`. Without it, run the plan with `executing-plans` and do reviews
  as a separate fresh pass yourself.
- Spawn with `fork_turns: "none"` so the subagent gets a clean context, and set `model`
  and `reasoning_effort` explicitly on every spawn (`agent-router` says which); setting
  only `model` resets effort to that model's default.
- The role files `scout`, `builder`, `architect`, `reviewer` and `test-runner` are copied
  into `.codex/agents/` by `install.sh --agents` and selected with `agent_type`.
- Track a skill's checklist with `update_plan`, one item per step.
