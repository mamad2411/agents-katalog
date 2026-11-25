---
name: timon-export
description: Export your agents (Hermes profiles, Grok Bot Bots and groups, or yourself) into one zip that Timon imports. Use when the user asks to export their agents for Timon, to move their agents to Timon, or to make a Timon agent archive.
---

# Export agents for Timon

You are about to pack the user's agents into **one `.zip` file** that Timon
reads in **Import agents › Grok Bot, Hermes or another agent**. The archive
holds a single JSON file, `timon-agent-import.json`, in the exact format
described below. Timon shows the user a preview of everything before it
writes anything.

## Rules that never bend

- **No secret value, ever.** API keys, tokens, passwords, cookies, session
  ids, private URLs with credentials: never copy their value anywhere in the
  archive, not even in a warning. A secret travels by its **name** only
  (`OPENAI_API_KEY`, `Authorization`), in a `secretNames` list.
- **Read, do not change.** You only read the user's agents. Do not edit,
  move or delete anything of theirs, and do not run their scripts.
- **Ask before you pack.** List what you found and let the user choose.
- **The format is strict.** Every object accepts only the fields listed here.
  An unknown field, a wrong type or a value past its limit makes Timon refuse
  the whole archive. Leave a field out rather than guess.

## Step 1 — Find the agents

### In Hermes

1. Find the **standard folder**: `~/.hermes` on Linux and macOS,
   `%LOCALAPPDATA%\hermes` on Windows (then `%USERPROFILE%\.hermes` if that
   one does not exist).
2. Find the **active folder**, the profile you run in: the folder named by
   the `HERMES_HOME` environment variable when it is set, otherwise the
   standard folder. Hermes started on a named profile (`hermes -p work`) sets
   `HERMES_HOME` to that profile's folder, not to the root.
3. Find the **root**, the folder that holds every profile, as Hermes does:
   - no `HERMES_HOME`, or a `HERMES_HOME` inside the standard folder
     (`~/.hermes/profiles/work`): the standard folder;
   - otherwise, a `HERMES_HOME` of the form `<folder>/profiles/<name>`:
     `<folder>`;
   - otherwise: `HERMES_HOME` itself.
4. Each profile is one agent. The root itself is the profile `default`; each
   folder `<root>/profiles/<name>` is the profile `<name>`. Skip the names
   found in `<root>/profiles/.deleted`. Name a profile by **its folder**,
   never by the folder you run in: when the active folder is
   `<root>/profiles/work`, you are `work`, not `default`. List every profile
   of the root, and say which one is active.
5. Per profile, read only these files (paths relative to the profile folder):
   - `SOUL.md`: the identity. Drop its HTML comments (`<!-- … -->`); if only
     headings are left, it is empty.
   - `memories/USER.md` and `memories/MEMORY.md`: entries separated by `§`.
     Each non-empty entry is one memory: `preference` for `USER.md`,
     `decision` for `MEMORY.md`.
   - `skills/<name>/SKILL.md` and `skills/<category>/<name>/SKILL.md`: one
     skill each. Skip hidden folders and the skills named in
     `skills/.bundled_manifest` (one `name:hash` per line, shipped with Hermes).
   - `cron/jobs.json`: the scheduled jobs (a list, or `{ "jobs": [...] }`).
   - `config.yaml`: `model` (a string, or `{ provider, default }` →
     `provider/default`), `timezone`, and `mcp_servers`.
   - `.env`: the variable **names** only, never the values.
   - Whether `state.db` or `sessions/` exists: that is a history, which Timon
     does not import (`hints.hasHistory: true`).

### In Grok Bot

1. List the Bots and the groups you can see: for each Bot its name, title,
   description (its job), its instructions, the skills it uses, its routines
   (instruction, when to run, time zone, paused or active), what it remembers,
   and its picture if you can read it. For each group: its name and members.
2. If you can only see yourself, export yourself, and tell the user to ask
   each other Bot the same thing. Timon imports several archives one after
   the other.
3. A routine started by an event (Slack, email, GitHub, a webhook…) cannot be
   carried: name it in `warnings`.

### In any other agent tool

Export yourself: your name, your role or title, your identity and
instructions, what you remember about the user, your text skills, your
scheduled tasks and your MCP servers.

## Step 2 — Ask which agents to export

Show the user the list (name and one line each) and ask which ones to export:
all of them, or some. Export only what they chose.

## Step 3 — Write the manifest

One JSON object, UTF-8, at most **10 MiB**. Its top level:

| Field | Value |
|---|---|
| `format` | always `"timon-agent-import"` |
| `version` | always `1` |
| `source` | `{ "app": "<app>", "exportedAt": "<now, ISO 8601 with offset>" }`. `app` is `"hermes"` for Hermes, `"grok-bot"` for Grok Bot, otherwise a short lowercase name of your tool (`a-z`, `0-9`, `-`). Timon names the agents `<app>.<key>`. |
| `agents` | 1 to 100 agents (below). |
| `groups` | optional, up to 100 groups (below). |
| `warnings` | optional, up to 200 sentences of at most 500 characters: what you could not carry, in plain words. |

### An agent

| Field | Required | Value |
|---|---|---|
| `key` | yes | lowercase `a-z`, `0-9` and `-`, 1 to 64 characters, starting and ending with a letter or digit. Unique in the manifest. |
| `displayName` | yes | 1 to 100 characters. |
| `sourceRef` | yes | the agent's stable id at the source, unique, at most 300 characters. Always the same for the same agent: Timon updates the agent it already imported instead of creating a copy. |
| `title` | no | at most 120 characters. |
| `soul` | no | who the agent is (becomes its `SOUL.md`), at most 200,000 characters. |
| `instructions` | no | its working instructions (its system prompt), at most 200,000 characters. |
| `directives` | no | extra directives, at most 20,000 characters. |
| `docs` | no | up to 32 documents `{ "name", "content" }`: `name` ends in `.md` (letters, digits, `_`, `.`, `-`, at most 99 characters, not `system-prompt.md`), `content` 1 to 200,000 characters. Names are unique. |
| `memories` | no | up to 256 `{ "text", "kind" }`: `text` 1 to 4,000 characters, `kind` one of `preference`, `decision`, `pitfall`. |
| `skills` | no | up to 200 `{ "id", "content" }` (below). |
| `routines` | no | up to 64 routines (below). |
| `mcpServers` | no | up to 64 servers (below). |
| `avatar` | no | `{ "mime", "dataBase64" }`: `mime` one of `image/png`, `image/jpeg`, `image/webp`, `image/gif`; the picture in standard base64 (no `data:` prefix, no line breaks), at most 2 MiB once decoded. |
| `hints` | no | `{ "model", "deliveries", "secretNames", "hasHistory" }`, all optional: `model` at most 200 characters; `deliveries` up to 32 platform names (`telegram`, `discord`…); `secretNames` up to 64 names of the secrets the agent used; `hasHistory` `true` when there is a conversation history. |

A **skill** is `{ "id", "content" }` and, when the skill folder holds more
than its `SKILL.md`, `"companionFiles"` (their relative paths, up to 200) and
`"hasCode": true` when one of them is a script. `id` is lowercase `a-z`,
`0-9`, `.`, `_`, `-`, 1 to 100 characters (the folder name, lowercased);
`content` is the whole `SKILL.md` text, at most 1 MiB. Timon imports
text-only skills and lists the others.

A **routine** is `{ "name", "instruction", "schedule", "timezone",
"enabledInSource" }`: `name` 1 to 80 characters, `instruction` (what the agent
is asked to do) 1 to 100,000 characters, `timezone` an IANA zone such as
`Europe/Paris` or `null`, `enabledInSource` `true` when it is active at the
source. Leave out a job that runs a script instead of asking the agent. The
`schedule` is exactly one of:

| `schedule` | Meaning |
|---|---|
| `{ "kind": "cron", "expression": "0 9 * * 1-5" }` | a 5-field cron expression |
| `{ "kind": "interval", "minutes": 120 }` | every N minutes, 1 to 527,040 |
| `{ "kind": "hourly", "minute": 15 }` | every hour at that minute (`minute` optional, 0–59) |
| `{ "kind": "daily", "time": "08:00" }` | every day, `HH:MM` 24-hour |
| `{ "kind": "weekdays", "time": "08:00" }` | Monday to Friday |
| `{ "kind": "weekly", "days": ["mon", "thu"], "time": "18:30" }` | 1 to 7 days: `sun`…`sat`, full names, or 0–7 (0 and 7 are Sunday) |
| `{ "kind": "monthly", "day": 1, "time": "09:00" }` | day 1 to 31 of each month |
| `{ "kind": "once", "at": "2026-12-24T18:00:00+01:00" }` | one run, ISO 8601 with offset (shown, not scheduled) |

An **MCP server** is `{ "name", "transport", … }`: `name` 1 to 100
characters, `transport` `"http"` or `"stdio"`. An `http` server has `url`
(at most 2,048 characters) **without** user name, password, or any query
parameter or path segment that holds a secret. A `stdio` server has
`command` and `args` with every secret value replaced by `<redacted>`. In
both, `secretNames` lists the names of the headers and environment variables
it needs. Leave out a server that is turned off.

### A group

`{ "key", "name", "members", "color" }`: `key` like an agent key, `name` 1 to
160 characters, `members` the `key`s of agents **in this manifest** (up to
100), `color` optional. Timon makes each group a team. A group's lead, own
instructions, routines and memories have no place there: say so in
`warnings`.

### How each source fills it

| | Hermes | Grok Bot |
|---|---|---|
| `source.app` | `hermes` | `grok-bot` |
| `key` | the profile name, lowercased, every run of other characters turned into `-` (`default` stays `default`) | the Bot's name, the same way |
| `displayName` | `Hermes` for `default`, the profile name otherwise | the Bot's name |
| `sourceRef` | `profile:<profile name>`, the name its folder gives it in step 1 (`default` only for the root) | `grok-bot:<the Bot's id, or its key>` |
| `soul` | `SOUL.md` without comments | name, title and description |
| `memories` | `USER.md` → `preference`, `MEMORY.md` → `decision` | what it remembers → `preference` |
| `routines` | `cron/jobs.json`: `prompt` → `instruction`; `schedule` `{kind: cron, expr}` → `cron`, `{kind: interval, minutes}` → `interval`; `enabled` and `state` → `enabledInSource`; the `timezone` of `config.yaml` | its routines, their time zone, active or paused |
| `mcpServers` | `mcp_servers` of `config.yaml` | the apps it uses, when they are MCP servers |
| `hints.secretNames` | the names in `.env` | the names of the secrets it uses |

## Step 4 — Check it

Before you pack, check every rule above: no unknown field, every required
field present, the limits respected, keys and `sourceRef`s unique, every
group member a key of the manifest. Search the whole JSON one last time for a
secret value: there must be none. If the file is over 10 MiB, drop the
pictures first.

## Step 5 — Make the zip

Name it `timon-agents-<app>-<YYYY-MM-DD>.zip` (`timon-agents-hermes-2026-11-03.zip`),
with `-2`, `-3`… when that name is taken. `timon-agent-import.json` sits at
the **root** of the zip, not in a folder.

Put it in the user's Downloads folder: `~/Downloads` on macOS, Windows
(`%USERPROFILE%\Downloads`) and Linux (or the folder `xdg-user-dir DOWNLOAD`
prints). Write it as `<name>.zip.part` first, then rename it to `<name>.zip`,
so that Timon never sees a half-written file. With Python:

```python
import os, zipfile
target = os.path.join(downloads, name)   # downloads and name chosen above
with zipfile.ZipFile(target + ".part", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("timon-agent-import.json", manifest_json)   # the text, UTF-8
os.replace(target + ".part", target)
```

**You work on a computer that is not the user's** (Grok Bot's cloud computer,
a remote server): make the zip there, then attach it to the conversation so
the user downloads it.

## Step 6 — Tell the user

Say where the zip is, how many agents it holds, and what you left out. Then:
in Timon, **Import agents**, the card **Grok Bot, Hermes or another agent**,
pick the zip, check the preview, then import. From a terminal:
`timon agent import <the zip>`. The secrets have to be entered again in Timon:
list their names.

## Example manifest

A complete, valid manifest (a Grok Bot export of two Bots and their group):

<!-- timon-export:example -->
```json
{
  "format": "timon-agent-import",
  "version": 1,
  "source": { "app": "grok-bot", "exportedAt": "2026-11-03T18:30:00+01:00" },
  "agents": [
    {
      "key": "ada",
      "displayName": "Ada",
      "title": "Daily tech scout",
      "sourceRef": "grok-bot:ada",
      "soul": "Ada scouts new developer tools and explains them in plain words.",
      "instructions": "Each weekday, read the bookmarks, pick one tool worth a demo and draft a short note about it. Ask before sending anything.",
      "docs": [{ "name": "STYLE.md", "content": "Short sentences. One example per idea." }],
      "memories": [
        { "text": "The user reads the morning note on the phone.", "kind": "preference" },
        { "text": "Notes go to the #tech channel, never to customers.", "kind": "decision" }
      ],
      "skills": [
        {
          "id": "weekly-digest",
          "content": "---\nname: weekly-digest\ndescription: Sum up the week's notes in five lines.\n---\n\nRead this week's notes and write five lines, one per day.\n"
        }
      ],
      "routines": [
        {
          "name": "Morning note",
          "instruction": "Pick one tool from the bookmarks and draft the morning note.",
          "schedule": { "kind": "weekdays", "time": "08:00" },
          "timezone": "Europe/Paris",
          "enabledInSource": true
        },
        {
          "name": "Inbox sweep",
          "instruction": "List the unread mentions and suggest a reply for each.",
          "schedule": { "kind": "interval", "minutes": 120 },
          "timezone": null,
          "enabledInSource": false
        }
      ],
      "mcpServers": [
        { "name": "notes", "transport": "http", "url": "https://mcp.example.com/notes", "secretNames": ["Authorization"] }
      ],
      "avatar": {
        "mime": "image/png",
        "dataBase64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
      },
      "hints": { "model": "grok-4", "deliveries": ["slack"], "secretNames": ["GITHUB_TOKEN"] }
    },
    {
      "key": "max",
      "displayName": "Max",
      "sourceRef": "grok-bot:max",
      "soul": "Max reviews the drafts before they go out.",
      "routines": [
        {
          "name": "Friday review",
          "instruction": "Review the drafts of the week and list what to fix.",
          "schedule": { "kind": "weekly", "days": ["fri"], "time": "16:00" },
          "timezone": "Europe/Paris",
          "enabledInSource": true
        }
      ]
    }
  ],
  "groups": [{ "key": "newsroom", "name": "Newsroom", "members": ["ada", "max"] }],
  "warnings": ["Max: the routine \"New mention\" starts on a Slack message and was not exported."]
}
```
