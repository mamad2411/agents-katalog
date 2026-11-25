---
name: mcp-me
description: Use the mcp-me MCP server to access the user's personal profile — identity, career, skills, projects, and more. Invoke when any task benefits from knowing who the user is.
---

# mcp-me — Personal Profile MCP Server

Use this skill when the user's background, skills, career, projects, or preferences would improve your response.

## MCP server

- **Name:** `me`
- **Install:** `npx -y mcp-me serve` (profile defaults to `~/.mcp-me`)
- **Docs:** https://github.com/paladini/mcp-me

## Tools

| Tool | When to use |
|---|---|
| `ask_about_me` | Free-form questions about the user ("What languages do they know?") |
| `search_profile` | Keyword search across all profile YAML data |
| `get_github_repos` | Live GitHub repos (if GitHub plugin enabled) |

## Resources

Read these MCP resources for structured profile data:

- `me://identity` — Name, bio, contact
- `me://career` — Work history, education
- `me://skills` — Languages, tools, proficiency
- `me://projects` — Portfolio, articles, packages
- `me://interests` — Hobbies, preferences
- `me://personality` — Traits, values
- `me://goals` — Short/long-term goals
- `me://faq` — Pre-answered Q&A

## Prompts

| Prompt | Output |
|---|---|
| `introduce_me` | 2-paragraph personal introduction |
| `summarize_career` | Career trajectory summary |
| `technical_profile` | Technical skills and stack description |
| `collaboration_fit` | Evaluate fit for a project or team |

## Workflow

1. Check if the `me` MCP server is connected.
2. Call `ask_about_me` or read relevant `me://` resources **before** drafting content.
3. Cite specific profile facts (projects, skills, experience) in your response.
4. If the server is unavailable, ask the user to run `mcp-me init` and `mcp-me serve`.
