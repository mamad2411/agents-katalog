---
name: lantern-jira
description: Read and update Jira Cloud tickets (Atlassian, the site in ATLASSIAN_BASE_URL) from the terminal with the account added in Lantern — get an issue, search by JQL, add a comment, list the statuses an issue can move to, move it to a named status, write its description. Use whenever the user mentions a Jira ticket or key such as PROJ-123, asks to "check the ticket", "what is in Jira", "find tickets", "comment on the issue", "move it to In Progress / Done", "update the ticket description", or hands over a task by ticket number, even without saying Jira. Needs no setup beyond adding the Jira account in Lantern (command palette, Integrations), which puts ATLASSIAN_EMAIL, GLOBAL_ATLASSIAN_TOKEN and ATLASSIAN_BASE_URL in the run's environment, or hands them to the script on request when the chat was not started by Lantern; nothing to install or configure by hand. If the user already has their own Jira skill in the project or in ~/.claude/skills, use that one instead; this is the default for projects that have none. Never deletes or bulk-edits.
---

# Jira, with the Lantern account

One script, `scripts/jira.mjs`, no dependencies (Node 18 or newer). It reads the credentials Lantern
puts in the environment and prints plain lines. It never prints the token, an Authorization header
or a URL carrying one. Run it from anywhere: `scripts/` below is this skill's folder, so from a project root the script is
`node .claude/skills/lantern-jira/scripts/jira.mjs` (or `.agents/skills/...` under Codex).

## Commands

```
node scripts/jira.mjs get PROJ-123
node scripts/jira.mjs search "project = PROJ AND status = 'In Progress' ORDER BY updated DESC" --limit 10
node scripts/jira.mjs comment PROJ-123 --body "Fixed in the latest commit."
node scripts/jira.mjs transitions PROJ-123
node scripts/jira.mjs transition PROJ-123 "In Review"
node scripts/jira.mjs describe PROJ-123 --body-file description.txt
```

- `get` and `search` take `--json` for the raw response; `search` takes `--limit` (1 to 100, default 20).
- `comment` and `describe` take the text as `--body "<text>"` or `--body-file <path>`. Plain text is
  written as Atlassian Document Format for you: blank lines split paragraphs, a single newline is a
  line break, lines starting with `- ` become a bullet list. A plain string would be rejected by Jira.
- `transition` matches the name of the transition or of the status it leads to, ignoring case. When
  nothing matches it lists what the issue can move to; run `transitions` first when unsure.
- The issue key is checked before any request. There is no delete, no bulk edit and no create.

## Conventions are the user's

This skill says how to connect to Jira and run its commands. It never says what goes in a summary, description, comment, label or transition: people and teams have their own rules, and their own skills for them.

Before the first `comment`, `describe` or `transition` of a session, run `node scripts/jira.mjs conventions` (read-only, offline; `--json` for data). It lists, with a path and one line each, the repository's own issue templates, the user's skills about tickets or issues (project and home `.claude/skills` and `.agents/skills`) and any template saved for this project. It prints names and paths only, never the contents.

- Something found: ask the user once which to follow ("I found X; use it?"), never choose silently. On yes, read that file or skill and follow it yourself.
- Nothing found: ask whether to write a ticket template for this project. On yes, draft it with the user, write it to a file they approve and keep it with `node scripts/jira.mjs template save ticket --file <path>` (it refuses to replace a saved one without `--force`); `template show ticket` prints it later, and you fill it in. On no, use the user's own wording.
- The skill supplies no default title, body, comment, label or transition text.

## Where the credentials come from

1. `ATLASSIAN_EMAIL`, `GLOBAL_ATLASSIAN_TOKEN` and `ATLASSIAN_BASE_URL` in the environment. When either
   the email or the token is set, nothing else is contacted.
2. Otherwise the running Lantern, asked over a local socket for the account of the project the script
   runs in (the working directory). The answer is used in memory for that one run: it is never
   written to a file, the environment or the output. The socket is `LANTERN_CREDENTIAL_SOCKET` when
   that is set, else `lantern.sock` in Lantern's user-data folder (`Lantern`, or `Lantern-dev` for a
   dev run).

This is what makes the skill work in a chat inside Lantern's embedded editor, which Lantern did not
start and so could not give an environment.

## When it fails

- `Missing ATLASSIAN_EMAIL, ...`: the account is not in Lantern for this run. The message ends with the
  reason Lantern gave: no Jira account added yet, or none chosen for this project (the user chooses an
  account for this project in Integrations, any account they added, whatever the remote), its store locked
  or unavailable, a folder that is not an opened project, or Lantern not running. Tell the user what it
  says; do not ask them to paste a token into the chat or a file.
- `refused (401)`: the account was not accepted; it may have expired or lack the Jira scope.
- Calls go through the Atlassian gateway first, using the site's cloud id, because a scoped API token
  is refused or told "issue does not exist" on the site URL itself; when the gateway answers 401 or
  the cloud id cannot be found, the site URL is used. Nothing to do.
- `refused (400)` on a transition usually means the workflow asks for a field on that step; say so and
  ask the user rather than guessing a value.
