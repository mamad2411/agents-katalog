---
name: hermes-profile-evolution
description: Route proposed Team Mimir profile behavior changes to target-owned Hermes dialogue.
---

# Hermes Profile Evolution

## Overview

This skill sends influence, not authority. The named Hermes profile alone can create Kanban work or mutate its behavior.

## Usage

Classify paths first. For profile-owned, unknown, mixed, or prohibited custody, submit a target-addressed proposal instead of editing files.

## Prerequisites

The administrative Hermes host must expose a compatible `hermes profile-request` command. Its route registry and credentials remain external custody.

## Examples

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/profile_request.py" suggest brokkr \
  "Consider a change to your stated review preference"
```

## Safety boundary

Use JSON standard input only. Do not pass credentials, hosts, API keys, model/provider overrides, system prompts, tool overrides, or shell fragments. The Claude Code hook blocks recognizable direct file-tool edits only; it does not claim to intercept Bash or external editors.
