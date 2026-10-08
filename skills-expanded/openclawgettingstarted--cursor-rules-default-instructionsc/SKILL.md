---
description: Default instructions for OpenClawGettingStarted - publish, run locally, and common commands
alwaysApply: true
---

# OpenClawGettingStarted - Default Instructions

This is an MkDocs Material blog. Use these commands when the user asks to publish, run locally, or build.

## Publish the site

When the user says "publish", "deploy", or "publish the site":

```powershell
cd c:\Users\FinnPedersen\GitHub\OpenClawGettingStarted; python -m mkdocs gh-deploy
```

The site is published to: https://finnpedersenkazes.github.io/OpenClawGettingStarted/

## Run the site locally

```powershell
cd c:\Users\FinnPedersen\GitHub\OpenClawGettingStarted
python -m mkdocs serve --livereload
```

Site is available at http://127.0.0.1:8000

## Other commands

| Command                          | Description            |
| -------------------------------- | ---------------------- |
| `python -m mkdocs build`         | Build static site      |
| `python -m mkdocs build --clean` | Build with clean cache |
