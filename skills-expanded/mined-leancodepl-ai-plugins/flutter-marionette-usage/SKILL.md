---
name: flutter-marionette-usage
description: Explain what the `flutter-marionette` plugin does and route to its Marionette skills. Use when the user invokes `/flutter-marionette-usage`, asks what this plugin covers, asks how Marionette compares with Patrol, or is unsure which Marionette skill fits a task.
---

# Marionette Usage

## How to respond

- If the user invoked this skill without a concrete task, explain what Marionette is for and when it is better than writing tests, then show the example requests below.
- If the user gave a concrete task, load the skill that fits it (table below) and do the work.
- Do not reply with filler like "skill loaded", "ready for the task", or "what would you like to do?" before explaining the plugin.

## What this plugin does

- Ships the `marionette` MCP server entry, which runs `marionette_mcp`, so the agent can tap, type, scroll, take screenshots and read logs in a running debug or profile app.
- Installs `flutter-marionette-skills`: the Agent Skills that ship in the `marionette_flutter` package, read from Marionette's `main` branch.

| Task | Skill |
| --- | --- |
| Add Marionette to an app; configure a custom design system, logs or device config; fix a binding or version error | `marionette-flutter-setup` |
| Drive a running app: smoke-test a flow, reproduce or verify a bug, sweep text scale, write the session report | `marionette-flutter-drive-app` |
| Turn a verified session (`steps.md`, `report.md`, screenshots) into Patrol tests | `marionette-flutter-to-patrol` |

If those skills are missing, the dependency did not install. Tell the user to run `/plugin install flutter-marionette-skills@leancode-ai-plugins`.

## Marionette or Patrol

- Marionette: an agent drives a live app, with no test files. Gestures are best effort. Use it to explore, smoke-check and debug.
- Patrol (the `flutter-patrol` plugin): deterministic E2E tests in `patrol_test/`, in debug and release builds, for CI. `marionette-flutter-to-patrol` turns a Marionette run into such tests and builds on Patrol's skills.

## Example requests

- "Add Marionette to this app."
- "Use Marionette to smoke-test the onboarding flow."
- "Write Patrol tests from .marionette/sessions/checkout-20260922T1801."

## Reach for these assets

- `README.md`: install, the bundled MCP launcher, and the manual config for other MCP clients.
- https://marionette.leancode.co/docs/: the full Marionette documentation.
- Related plugin: `flutter-patrol`, deterministic E2E testing with Patrol.
