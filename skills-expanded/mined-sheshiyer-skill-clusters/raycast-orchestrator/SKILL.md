---
name: raycast-orchestrator
description: "Route a Raycast task to the right spoke — build an extension/command, build an AI extension (tools the Raycast AI calls), publish to the Store, or design a Raycast-aesthetic UI in your own app. USE WHEN a user wants to work with Raycast but the specific concern isn't named."
cluster: raycast
version: 1.0.0
---

# Raycast Orchestrator

Entry skill for Raycast work. It separates the four distinct jobs people mean by "Raycast" and
routes accordingly. The extension model (command types, manifest, `@raycast/api`, data, build)
lives in `raycast-core`.

## Cluster map (routing targets)

- `raycast-core` — command types, the `package.json` manifest, UI/navigation, preferences, data/storage hooks, build/develop/publish.
- `raycast-extension` — build an extension/command with React + TypeScript (the hands-on building spoke).
- `raycast-ai-extensions` — AI extensions: declare `tools[]` the Raycast AI can call, with instructions, confirmations, and evals.
- `raycast-store-publishing` — package and submit to the Raycast Store (metadata, icon, screenshots, PR + review).
- `raycast-ui-skills` — design your *own* app to look like Raycast (light mode, Inter, 4px grid). **Not** the extension API.

## Routing Rules by Intent

- **"Build a Raycast extension / command"** → `raycast-extension` (+ `raycast-core` for the model).
- **"Make it AI-callable / build an AI extension / add tools"** → `raycast-ai-extensions`.
- **"Publish / submit to the Store"** → `raycast-store-publishing`.
- **"Make my app/site look like Raycast"** → `raycast-ui-skills` (aesthetic only).

## Standard Operating Flow

1. Disambiguate the job: build extension vs AI extension vs publish vs Raycast-look UI.
2. For building, ground in `raycast-core` (command `mode`, manifest entries, the right `@raycast/api` container).
3. Delegate; for "ship it", run build → `raycast-store-publishing`.
4. Return: command type(s), manifest changes implied, and the next action.

## Guardrails

See `raycast-core`. Keep the `package.json` manifest in sync with code; confirm destructive
actions; never expose secrets from preferences; for AI tools, gate side-effecting tools behind
confirmation. Defer changing API specifics to developers.raycast.com.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
