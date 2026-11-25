---
name: vault-update
description: Automate daily updates for the vault, including the Daily Brief and Daily News. Executes instructions stored in "01 Updates/📌 Daily Brief.md" and "01 Updates/📰 Daily News.md".
---

# Vault Update Skill

## Table of Contents
- [Workflow](#workflow)
- [Updating Daily Brief](#updating-daily-brief)
- [Updating Daily News](#updating-daily-news)
- [General Rules](#general-rules)

## Workflow

1.  **Identify Target**: Determine if the user wants to update the Daily Brief, the Daily News, or both.
2.  **Read Instructions**: Read the `> [!prompt]` callout in the corresponding file:
    *   **Daily Brief**: `01 Updates/📌 Daily Brief.md`
    *   **Daily News**: `01 Updates/📰 Daily News.md`
3.  **Gather Data**: Use available tools (Search, Gmail, Calendar, local scripts) to gather the required information.
4.  **Format and Insert**: Follow the formatting rules in the instructions, handling the collapsing of previous days.
5.  **Finalize**: Update frontmatter (`updated:`, `unread: true`) and report completion to the user.

## Updating Daily Brief

**Instructions path**: `01 Updates/📌 Daily Brief.md`

**Data sources**:
- **Weather**: Run `python3 weather.py` if available, or search for current weather in São Paulo.
- **Calendar**: Use `gcal__get_calendar_events` for today.
- **Email**: Use `gmail__search_email` with queries like `is:unread` or `newer_than:1d`. Ignore "closed won" opportunities.
- **Messages**: Check for unreplied DMs (if messenger tools are available, otherwise skip).
- **Tasks**: Check `05 Projects/` logs or current daily notes for pending items.

**Formatting**:
- Day heading: `### [[DD-MM-YYYY Day]]`
- Callouts for each section (Weather, Calendar, Email, Messages, Tasks).
- Collapse previous day into `> [!note]- [[date]]`.

## Updating Daily News

**Instructions path**: `01 Updates/📰 Daily News.md`

**Data sources**:
- **Topics**: AI, Tech, Macro, World, São Paulo/Brasil, Games.
- **Sources**: Reddit (r/technology, r/technews, r/brdev), Hacker News, CNN, G1, IGN.
- **Selection**: Pick exactly ONE most important story per topic.

**Formatting**:
- Each story in a collapsed callout (`> [!note]- Topic: Headline (Source)`).
- Body: 2–4 sentences + `[Source](url)`.
- Group days under `## MM-YYYY` month headers.
- Newest day at the top.

## General Rules

- **No `# Title` headings**: Filename is the title.
- **Set `unread: true`**: In frontmatter for every update.
- **Update `updated` date**: In frontmatter.
- **Maintain Month Headers**: Ensure entries are grouped correctly by `## MM-YYYY`.
- **Iterative Improvement**: If a topic or section is missing data, use placeholders and notify the user.
