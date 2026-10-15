---
name: shortcut-updates
description: Gets concise Shortcut story updates grouped for review. Use when user asks for Shortcut updates, unfinished stories, owned stories, story status summaries, or last updates/activity on Shortcut tickets.
---

# Shortcut Updates

## Quick start

Use Shortcut MCP.

Default ask: unfinished stories owned by user.

Search:
```json
{"owner":"me","isDone":false,"isArchived":false}
```

Then for each story get history:
```json
{"storyPublicId":12345}
```

## Output shape

Group like:

```md
## <Workflow Name>

### <Epic Name or No Epic>

#### [<id>](<url>) — <story name>
State: <state name>
- <actor> — <short update>. — <YYYY-MM-DD HH:mm>
- <actor> — <short update>. — <YYYY-MM-DD HH:mm>
- <actor> — <short update>. — <YYYY-MM-DD HH:mm>
```

Rules:
- Workflow first, epic second, stories third.
- Put `No Epic` for null epic.
- Show state as plain text. No underline.
- Last 3 history entries only, newest first.
- Put date at end of each update.
- Keep grammar loose. Short > polished.
- If only 1-2 updates exist, show only those.
- Prefer state names from `relatedEntities.workflows[*].states`.
- Prefer workflow + epic names from `relatedEntities`.
- If search paginates, keep fetching `nextPageToken` until done.

## Update wording

Translate history actions to plain notes:
- create → `Created story. <key detail if obvious>`
- workflow_state_id change → `Moved <old> → <new>.`
- completed true/false → `marked complete/incomplete`
- owner_ids add/remove → `Added/removed <person> as owner.`
- follower_ids add/remove → `Added/removed <person> as follower.`
- name change → `Renamed story.`
- description change → `Updated description; <short visible detail if useful>.`
- branch push → `Pushed branch <name>.`
- comment create → `Commented.`

Do not dump raw JSON. Do not include screenshots/long links unless needed.
