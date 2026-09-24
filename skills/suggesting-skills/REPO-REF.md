# Repo Referensi: spencerpauly/awesome-cursor-skills

Repo: https://github.com/spencerpauly/awesome-cursor-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/spencerpauly_awesome-cursor-skills
API: curl "localhost:27126/repos/readme?name=spencerpauly_awesome-cursor-skills"
Dibuat: 2026-09-16

## Cuplikan README
# spencerpauly/awesome-cursor-skills

Source: https://github.com/spencerpauly/awesome-cursor-skills
Fetched: 2026-09-16

## README
# Awesome Cursor Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome [skills](https://docs.cursor.com/agent/skills) for [Cursor](https://cursor.com), the AI code editor.

Skills are reusable `SKILL.md` instruction files that teach the AI agent how to perform specific tasks — from setting up analytics to scaffolding entire projects. In cursor, they live in `.cursor/skills/` (personal) or project directories and are automatically discovered by the agent.

## Contents

- [Skills](#skills)
- [Plugins](#plugins)
- [Cursor Resources](#cursor-resources)
- [Contributing](#contributing)

---

## Skills

Ready-to-use `SKILL.md` files you can copy into your `.cursor/skills/` directory. Each one teaches the agent a specific engineering workflow.

### Cursor-Native

Skills that harness Cursor's unique agent capabilities — things only an AI inside Cursor can do.

- [`suggesting-cursor-rules`](resources/suggesting-cursor-rules/SKILL.md) - If you keep correcting the agent on the same convention, it suggests a `.cursor/rules/` file to encode it permanently.
- [`suggesting-cursor-hooks`](resources/suggesting-cursor-hooks/SKILL.md) - If you keep asking the agent to run the same check (lint, types, tests), it suggests a `.cursor/hooks.json` hook to automate it.
- [`switching-projects`](resources/switching-projects/SKILL.md) - Switch the active workspace to a different project using the `cursor-app-control` MCP, without opening a new window.
- [`saving-workspace-context`](resources/saving-workspace-context/SKILL.md) - Automatically persist research, decisions, and learnings to workspace files so knowledge survives across conversations.
- [`visual-qa-testing`](resources/visual-qa-testing/SKILL.md) - Open the app in Cursor's built-in browser, take screenshots, check console errors, and audit network requests after making changes.
- [`verifying-in-browser`](resources/verifying-in-browser/SKILL.md) - Start the dev server, open the app side-by-side with your code, and verify rendering, console, and network health.
- [`profiling-performance`](resources/profiling-performance/SKILL.md) - Profile CPU performance of a running app using Cursor's browser profiler to capture call stacks and identify slow functions.
- [`screenshotting-changelog`](resources/screenshotting-changelog/SKILL.md) - Generate visual before/
