---
title: "plugin skill installing-enforcement — the soft-vs-hard boundary (I6)"
description: "The plugin skill that owns the soft-vs-hard boundary explanation: the plugin can never silently wire a consumer's git/CI, so the hard layer is an explicit /getff:install-enforcement opt-in with consent — and the SKILL, not any site prose, is where that boundary is authored."
---

<!-- provenance: framework @ aa87d0a47a6d8502f983cc9fe7284bd5dcb3d650 2026-09-12 · raw draft (beta-docs-encyclopedia) —
     polish pass pending; re-derive from the anchors below, do not hand-edit prose -->

# plugin skill installing-enforcement — the soft-vs-hard boundary (I6)

**Status:** shipped-beta · **Ships to:** plugin (marketplace install of `getff@getff`) · **Fires at:** when the user asks to actually WIRE the hard layer (git pre-commit/pre-push hooks + CI) or to make rules build-failing — the SKILL description's own trigger list

## What it is

A 52-line SKILL.md that explains WHERE THE LINE IS between what a plugin install does and what it deliberately never does: the plugin delivers the SOFT layer (skills, agents, session hooks — advice and session-time discipline); the HARD layer (git hooks that block commits/pushes and CI gates) is wired only by an explicit, consent-gated command this skill points at. Attribution note (census T-ENC-A): the soft-vs-hard boundary prose the site carries is authored in THIS SKILL artifact — the SKILL is its source, and this page credits it there rather than to any earlier site page.

## How it works

- The boundary is stated as a structural property, not a preference: "A plugin can **never** silently wire a consumer's git/CI — so the hard layer is deliberately" gated behind the command.
- It scopes WHEN to wire: wire the hard layer when the user wants rules to actually fail the build; do NOT wire it when the user only wants the methodology/advice — the soft layer already covers that.
- The wiring flow it describes is consent-shaped: the command runs a dry-run first, asks for explicit `[y/N]` consent, and only then applies — the mechanical half of that flow is `fetch-and-wire.sh` (I9).
- Its "Honest boundary (T16)" section instructs the agent's own speech: never tell the user the PLUGIN installed the git hooks/CI — the plugin delivered the soft layer, and THEY opted into the hard layer via the command, which ran the official installer.
- Lane honesty: plugin-path only. The clone/npm installer path reaches the same hard layer directly (install.sh IS the hard layer); this skill exists for the plugin audience who got the soft layer first.

## Satellites & companions

The prose counterpart of `/getff:install-enforcement` (I3) — it EXPLAINS, the command INVOKES, `fetch-and-wire.sh` (I9) EXECUTES. Routed to from the orientation skill (I5). The honesty section implements the same posture as the installer-side never-prompt and decline-as-success patterns (A23).

## Anchors

At framework pin `aa87d0a47a6d8502f983cc9fe7284bd5dcb3d650`:

- `plugin/skills/installing-enforcement/SKILL.md:2` — «name: installing-enforcement»
- `plugin/skills/installing-enforcement/SKILL.md:3` — «description: Use when the user wants to actually WIRE the hard enforcement layer (git pre-commit/pre-push hooks + CI) into their repo… Explains the soft-vs-hard boundary and points at the /getff:install-enforcement command.»
- `plugin/skills/installing-enforcement/SKILL.md:8` — «> **Authoritative for:** when and how to wire the plugin's hard enforcement layer (git hooks + CI) — the soft-vs-hard split and the `/getff:install-enforcement` flow.»
- `plugin/skills/installing-enforcement/SKILL.md:21` — «A plugin can **never** silently wire a consumer's git/CI — so the hard layer is deliberately»
- `plugin/skills/installing-enforcement/SKILL.md:41` — «3. asks for explicit `[y/N]` consent,»
- `plugin/skills/installing-enforcement/SKILL.md:48-51` — «## Honest boundary (T16)» «Never tell the user the *plugin* installed the git hooks/CI. The plugin delivered the soft layer;» «**they** opted into the hard layer via this command, which ran the official installer in their»
