---
name: chat-n-build
description: Use this skill when the user wants a live local dashboard that they drive by talking to you, for a process or workflow they run — "fire up a dashboard for my article pipeline", "show this on the dashboard", "add a kanban for my leads", "put the review findings on the board", "advance the pipeline", "what's on the dashboard", "turn this process into a skill" (skillify) — or any turn in a project that has a dashboards/ folder with pending button clicks. You are the backend; the page renders state you change with the bundled dash CLI. Not for writing dashboard code in a web framework (React, Streamlit), charting a data file, or opening hosted tools like Grafana or Looker.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/chat-n-build/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
