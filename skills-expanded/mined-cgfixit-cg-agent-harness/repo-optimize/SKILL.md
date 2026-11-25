---
name: repo-optimize
description: Scan this repository's default branch for code, CI, security, financial-risk, and maintainability fixes, then open a focused draft pull request only when a chunk earns its keep. Use when asked to optimize the repo, harden CI, audit risk, propose improvements, or open optimization PRs. Works on any GitHub repo. Triggers: optimize, find improvements, harden CI, audit, draft optimization PR, repo-optimize.
argument-hint: "[topic or area to scan]"
user-invocable: true
compatibility: GitHub Copilot (github.com coding agent, Copilot CLI, VS Code / Visual Studio agent mode). Requires git + gh or the GitHub MCP tools.
---

# repo-optimize

You are a modern engineer working **this** repository. Learn the stack from the
tree. Do not assume Python, FastAPI, LangGraph, or any other project's modules.

Read code for leverage: performance, security, financial risk / oversight in
assumptions, auditability, maintainability. Do not invent work to hit a quota.

## Before starting

Resolve identity from git. Never hardcode owner, repo, or default branch.

```bash
OWNER="$(git remote get-url origin | sed -E 's#.*[:/]([^/]+)/[^/]+(\.git)?$#\1#')"
REPO="$(git remote get-url origin | sed -E 's#.*[:/][^/]+/([^/]+)(\.git)?$#\1#' | sed 's/\.git$//')"
DEFAULT_BRANCH="$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || echo main)"
echo "$OWNER/$REPO default=$DEFAULT_BRANCH"
