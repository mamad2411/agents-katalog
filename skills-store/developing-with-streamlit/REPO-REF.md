# Repo Referensi: streamlit/agent-skills

Repo: https://github.com/streamlit/agent-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/streamlit_agent-skills
API: curl "localhost:27126/repos/readme?name=streamlit_agent-skills"
Dibuat: 2026-09-16

## Cuplikan README
# streamlit/agent-skills

Source: https://github.com/streamlit/agent-skills
Fetched: 2026-09-16

## README
# Agent Skills for Streamlit Development

> [!WARNING]
> **This repository is deprecated and is being archived.**
>
> The `developing-with-streamlit` **meta-skill now lives in and ships with Streamlit itself** — [**`streamlit/streamlit`**](https://github.com/streamlit/streamlit) is the canonical source of truth. As of Streamlit **1.60+** the meta-skill is bundled in the pip package at [`lib/streamlit/.agents/meta-skill/developing-with-streamlit`](https://github.com/streamlit/streamlit/tree/develop/lib/streamlit/.agents/meta-skill/developing-with-streamlit), and `streamlit skills` installs it from your local install — no download from this repo.
>
> - **Recommended:** `pip install --upgrade streamlit` (1.60+), then `streamlit skills`.
> - **Existing installs keep working.** This repo stays public and its `v1` tag is preserved, so `npx skills` / `gh skill` / `git clone` installs continue to resolve; `discover.py` runs entirely locally, so archiving does not affect it.
> - **New development and fixes to the meta-skill happen in [`streamlit/streamlit`](https://github.com/streamlit/streamlit), not here.**

A lightweight **meta-skill** that teaches AI coding assistants (Claude Code, Cursor, and others) how to discover and load the Streamlit development skills bundled inside the Streamlit pip package (1.57+).

## What are Agent Skills?

Agent Skills are specialized instruction sets that enhance AI coding assistants' capabilities for specific tasks. Each skill contains instructions, scripts, and resources that the AI loads dynamically to improve performance on Streamlit development workflows.

The actual skill content (dashboards, themes, layouts, session state, custom components, etc.) ships with Streamlit itself — this repo only contains the entry point that bootstraps discovery.

## How it works

Starting with Streamlit 1.57, the full set of Streamlit development skills ships **inside the Streamlit pip package** itself. This repository provides a lightweight **meta-skill** that teaches agents how to discover and load those bundled skills.

The meta-skill ([`developing-with-streamlit/SKILL.md`](developing-with-streamlit/SKILL.md)):

1. Detects the active Python interpreter (virtualenv, conda, pipenv, poetry, pdm, uv, or system)
2. Locates the installed Streamlit package path
3. Points the agent to the bundled skills at `<streamlit_path>/.agents/skills/`
4. 
