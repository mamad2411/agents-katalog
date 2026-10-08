---
name: start
description: Start the SEA Street Guess local browser app end to end. Use when the user invokes /start, $start, asks to run the game, boot the repo, open the local app, or verify the app is serving from this repository.
---

# Start

## Overview

Start the static SEA Street Guess app from this repository with the expected local config, port, and URL.

## Workflow

1. Work from the repository root.
2. Run `scripts/start.sh`.
3. Open or hand off the printed URL, usually `http://localhost:5177/?v=game-v7`.

```bash
.codex/skills/start/scripts/start.sh
```

## Behavior

- Reuse an existing server on `PORT` when one is already listening.
- Default `PORT` to `5177`.
- Read the GrabMaps key from local-only `config.local.js`.
- If `config.local.js` is missing and `GRABMAPS_API_KEY` is set in the environment, create `config.local.js` from that value.
- If no local key is available, stop and explain that the app cannot fully initialize until `config.local.js` is created.
- Keep `config.local.js` uncommitted.

## After Starting

If the Browser plugin is available and the user wants the app opened, navigate the in-app browser to the printed URL. Otherwise, report the URL and server status.
