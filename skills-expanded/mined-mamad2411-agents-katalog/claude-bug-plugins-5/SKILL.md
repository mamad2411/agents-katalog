---
name: claude-bug-plugins-5
description: The "Top 5 Claude Code plugins that catch bugs for you" carousel from @awayfromlovable - Superpowers, Context7, Security Guidance, Sentry, Code Review - with what each does, where it lives (checked against the claude-plugins-official marketplace file), its licence, what it needs and which claims on the slides could not be verified (stars, installs). Use when choosing bug-catching plugins for Claude Code or checking the install command.
---

# Five bug-catching Claude Code plugins

Source: @awayfromlovable, 7 slides. Numbers on the slides (stars, installs) are the creator's and are **unverified**: the GitHub API was blocked in this environment.

Checked on 5 October 2026 by cloning `anthropics/claude-plugins-official` and the plugin repos and reading their files.

| # | Plugin | What the slide says | What the files show | Licence | Needs |
|---|---|---|---|---|---|
| 1 | Superpowers (obra/superpowers) | brainstorming, debugging, TDD; `/plugin install superpowers@claude-plugins-official` | Listed in the official marketplace file; description matches (brainstorming, subagent development with review, debugging, red/green TDD, authoring skills) [Certain] | MIT | Nothing |
| 2 | Context7 (upstash/context7) | current docs in context | Listed; connects to Context7's hosted MCP server (`https://mcp.context7.com/mcp`), works anonymously, `CONTEXT7_API_KEY` for higher limits [Certain] | MIT | Network; sends your queries to Upstash |
| 3 | Security Guidance | warns before unsafe edits; "241,800 installs" | Listed under `plugins/security-guidance` (v2.0.9): pattern warnings on edits, diff review on Stop, a commit reviewer for injection, XSS, SSRF, secrets [Certain] | Apache-2.0 repo | Nothing. Install count unverified |
| 4 | Sentry (getsentry/sentry-mcp) | catches production errors | Listed; description: error reports, stack traces, issue search [Certain] | **FSL-1.1-Apache-2.0** (source-available; converts to Apache-2.0 later, not OSI open source now) | A Sentry account and authorisation |
| 5 | Code Review | `/code-review` flags only 80%+ confident issues; "438,525 installs" | Listed under `plugins/code-review`: multiple agents with confidence-based scoring to filter false positives [Certain]. The 80% threshold was not checked in the code | Apache-2.0 repo | Nothing. Install count unverified |

The slide attributes plugins 3 and 5 to `anthropics/claude-code`; in this check both appear in `claude-plugins-official/plugins`. Which repo is canonical was not resolved. [Guessing]

## Install (run yourself, inside Claude Code)

```
/plugin install superpowers@claude-plugins-official
/plugin install context7@claude-plugins-official
/plugin install security-guidance@claude-plugins-official
/plugin install sentry@claude-plugins-official
/plugin install code-review@claude-plugins-official
```

The `@claude-plugins-official` suffix works only if that marketplace is added; check `/plugin marketplace list` first. This repo's `.mcp.json` already has `context7` and `sentry`, so plugins 2 and 4 would duplicate them; install one route, not both.

## Honest limits

Plugins that "catch bugs" produce warnings, not guarantees. Each plugin adds prompts and hooks that run on every session: read what a plugin does before enabling it, and enable security tools on a repo you can afford to experiment on. Use `/bug-plugin-pick`.
