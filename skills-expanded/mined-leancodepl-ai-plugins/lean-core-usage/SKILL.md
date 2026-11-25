---
name: lean-core-usage
description: Explain what the LeanCode AI plugins marketplace covers, which plugins are available, and how to install them. Use when the user invokes `/lean-core-usage`, asks what this marketplace is, asks which plugins exist, or asks where to begin. Manual-only entry point — does not auto-fire.
disable-model-invocation: true
---

# LeanCode Core Usage

## How to respond

1. **Read the sources of truth first** — do not rely on memory or hardcoded lists:
   - `.claude-plugin/marketplace.json` at the repo root for the canonical plugin list (`name` + `description` per plugin).
   - The root `README.md` "Supported clients" section for the list of supported clients. Always read it — do not enumerate clients from memory, do not invent client names.
   - If the working directory is not the repo, point the user at https://github.com/leancodepl/ai-plugins and read from the GitHub-hosted versions of those files.
2. Summarize what the marketplace covers in one paragraph, using the descriptions read from the JSON.
3. Print one bullet per plugin: name + the description from `marketplace.json`. Do not invent or restate descriptions.
4. List the supported clients from the root README, in the order they appear there.
5. Route domain questions to the matching `/<plugin>-usage` skill rather than answering them here.
6. When the user wants to contribute, point at `/lean-contribute`.
7. Do not reply with filler like "skill loaded" or "ready for the task" before explaining the marketplace.

## What the marketplace is

`leancodepl/ai-plugins` is LeanCode's shared marketplace of AI plugins for Claude Code, focused on Flutter development. Each plugin is small, focused, and independently installable.

`lean-core` is the meta plugin: an entry point that explains the marketplace (`/lean-core-usage`) and a contribution helper (`/lean-contribute`). Nothing else lives in `lean-core` — every domain capability is its own plugin.

## Picking plugins

Install only what the project actually uses. If unsure, install `lean-core` first, run `/lean-core-usage`, and pick from the read-from-JSON list.

## Installing the marketplace

Each plugin stored in this repository has its own `/<plugin>-usage` skill (for example `/flutter-bloc-usage`); the externally sourced `flutter-forms` and `flutter-patrol` ship their own skills instead. Reach for it once the plugin is installed.

Step-by-step install lives in the root `README.md` under "Install". Walk the user through it. The supported clients are listed in the root README's "Supported clients" section — read it; do not invent client names.

## Contributing

When you want to propose a tweak or a new plugin, run `/lean-contribute`. It walks through the repo structure, the CI checks, and the PR steps.

## What this plugin is NOT about

- Any domain guidance. Route to the matching `/<plugin>-usage`.
- Running commands or rewriting files for you. This skill only explains.
- Restating the plugin or client list from memory. Always read the source of truth.
