---
name: eve-compat
description: Deploy an agent built with the eve framework (eve.dev / Vercel) onto Zavu, or import it straight from GitHub with `npx zavudev import`. Use this skill when the user has an eve-layout project (agent/instructions.md, agent/tools/*.ts) and wants it answering on Zavu's messaging channels, or asks whether an eve capability works on Zavu.
---

# Deploy eve projects on Zavu

Zavu compiles an eve-layout project into a first-class Zavu agent. The user's
files are never edited: `agent/instructions.md` becomes the system prompt,
each `agent/tools/<name>.ts` becomes a tool named `<name>`, and Zod
`inputSchema` objects are converted to JSON Schema automatically.

## Commands

```sh
# Import from GitHub and deploy in one step (also works for Zavu-native repos):
npx zavudev import owner/repo --sender sndr_123
npx zavudev import owner/repo#branch --root apps/agent   # monorepo / branch
# Private repos: set GITHUB_TOKEN in the environment (sent only to GitHub).

# Deploy a local eve project (detected by agent/instructions.md):
cd my-eve-agent && npx zavudev deploy --sender sndr_123
```

The sender can come from `--sender` (inlined at compile time) or the
`SENDER_ID` function secret (`npx zavudev fn secrets set SENDER_ID sndr_123`).
Without either, the agent deploys but stays disconnected until a sender is
attached in the dashboard.

## What maps

| eve | Zavu |
|---|---|
| `agent/instructions.md` | system prompt (required) |
| `agent/agent.ts` string `model` | agent model; non-string configs (provider instances, `defineDynamic`) fall back to the default with a warning |
| `agent/tools/*.ts` (default-export `defineTool`) | tools, named by filename stem |
| Zod / JSON Schema `inputSchema` | JSON Schema `parameters` |
| `package.json` dependencies | installed server-side; the `eve` package itself is compiled away |

## What does NOT run on Zavu (always tell the user)

The deploy prints a compatibility report; these produce explicit warnings:

- `agent/channels/` — unnecessary: Zavu senders are the channels.
- `agent/schedules/` — cron is not available on Zavu Functions yet.
- `agent/skills/` — not loaded at runtime; fold content into
  `instructions.md` or a knowledge base.
- `agent/subagents/`, `agent/sandbox/`, `agent/connections/`, `evals/` — not
  supported. Agents that depend on them should run on eve's own runtime.
- Tool `approval` gates and `toModelOutput` — ignored per tool, with warnings.
- `agent.ts` options `reasoning`, `compaction`, `limits`, `modelOptions`,
  `outputSchema` — ignored, with warnings.

Tools run on every channel — plain text (SMS/WhatsApp/Telegram), voice, and
flow `tool` steps — with up to 5 tool rounds per reply. The one exception is
`agents test`: a dry run never executes tools (that would fire real webhooks)
and says so in its warnings.

## Requirements and troubleshooting

- Compiling an eve layout needs `esbuild` resolvable in the project
  (`npm install -D esbuild`). `npx zavudev import` adds and installs it
  automatically; only `--no-install` skips that.
- `inputSchema` must be an object schema — `z.object({...})` or a JSON Schema
  with `type: "object"`. Exotic Zod types fall back to a permissive schema
  with a warning in the build logs.
- After deploying: `npx zavudev agents list` for the agent id, then
  `npx zavudev agents test <agentId> --message "hi"` for a dry run that
  delivers nothing and charges nothing.
- Redeploy after edits with `npx zavudev deploy` — the reconcile summary
  (`+` / `~` / `=` / `-`) is the source of truth for what changed.
