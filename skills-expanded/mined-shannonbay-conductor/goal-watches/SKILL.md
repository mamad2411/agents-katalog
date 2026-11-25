---
name: goal-watches
description: Use when a Quarterdeck goal should start a run because something happened (a new GitHub issue or pull request, a new feed entry, a new file, a changed web page, a new email) and not only on a timer. Explains what a watch is, how to write and test its command, recipes for common sources, and when a schedule or a webhook fits better.
---

# Watches for Quarterdeck goals

A goal runs on a schedule. A **watch** also starts a run when something new appears. You set one with `update_goal` (`watches`); the person sees the whole command and confirms it.

A goal run cannot set a watch itself. When it knows what should start its next run ("tell me when a buyer replies"), it calls `propose_watch` (same fields as a watch spec, plus a short `reason`) instead of asking how to watch for it: the request waits under Needs you with the exact command, and nothing runs until the person approves.

## How a watch works

- A watch is a shell command (or, for a connector, a tool: see below), run every few minutes (`every_minutes`, default 5, at least 1) in the goal's working directory.
- The command prints **one line per current item**: an issue number, a feed entry's id, a file name. It exits 0.
- A line it has not printed before is new. New lines queue a run, and that run's brief lists them under `watch_events`.
- The first check only records what is there. It starts nothing.
- A check that fails (non-zero exit or longer than 30 seconds) changes nothing and starts nothing. After three failures in a row the Goals pane shows the watch as failing.
- Several new lines, or lines that arrive while a run is going, make one run, not one each.
- Each run is a full model run: see "Fewer quiet runs" for choosing `every_minutes`, filtering with `match` / `ignore`, and spacing watch runs out.
- With `fires: "change"` (default `"new"`), the watch compares each check only with the one before: see "Watching a state" below.

So print **stable identifiers**, not text that changes. A line with a comment count or a "2 hours ago" in it looks new at every check.

## Writing the command

1. Run the command yourself first, in the goal's directory, and read what it prints.
2. Check it prints nothing but item lines on stdout. Stderr is ignored, except to explain a failure.
3. Check it exits non-zero when the source can't be reached. Otherwise an outage reads as "no items", which is harmless, but a half-printed list is not.
4. Keep it to at most 200 lines of at most 300 characters. More are ignored.
5. Commands run under `cmd.exe` on Windows and `sh` elsewhere. Quote with double quotes, and avoid `$( )`, pipes into `grep`/`awk`, and single quotes around arguments. When it needs more than one program, write it as `node -e "..."` (Node is always there) or put a script file in the goal's directory and run that.
6. The command runs unattended with the person's own access. Keep it read-only.

After `update_goal`, the answer says how the first check went: how many items it found, or the error.

## Recipes

Open issues in a GitHub repository (needs `gh`, signed in):

```
gh issue list --repo OWNER/REPO --state open --limit 100 --json number --jq ".[].number"
```

Open pull requests:

```
gh pr list --repo OWNER/REPO --state open --limit 100 --json number --jq ".[].number"
```

Releases:

```
gh release list --repo OWNER/REPO --limit 20 --json tagName --jq ".[].tagName"
```

An RSS or Atom feed (prints each entry's link or id):

```
node -e "fetch(process.argv[1]).then(r=>{if(!r.ok)process.exit(1);return r.text()}).then(t=>{for(const m of t.matchAll(/<(?:guid|id)[^>]*>([^<]+)</g))console.log(m[1].trim())}).catch(()=>process.exit(1))" https://example.com/feed.xml
```

Files in a folder (a new file is a new line):

```
node -e "for(const f of require('fs').readdirSync(process.argv[1]))console.log(f)" inbox
```

A web page or file that changes (one line: a hash of its content, so any change is new):

```
node -e "fetch(process.argv[1]).then(r=>{if(!r.ok)process.exit(1);return r.text()}).then(t=>console.log(require('crypto').createHash('sha256').update(t).digest('hex'))).catch(()=>process.exit(1))" https://example.com/status
```

## Watching a state: `fires: "change"`

A normal watch fires once per line it has never printed, so a state that flips back and forth (a working tree clean, then dirty, then clean again; a health check up, then down) fires only the first time. For a state, set `fires: "change"`:

- A check whose lines differ from the last check's (the same lines in another order are no change) is an event; each line that wasn't in the last check is listed in `watch_events`.
- Output that becomes empty is one `(none)` event.
- Only the last check is remembered. Changing a watch's `fires` starts it over, like changing its command.

A repository's working tree (one line: the commit, with `-dirty` while there are uncommitted changes):

```
git describe --always --dirty
```

Whether a service answers (one line: its status code, or `down`):

```
node -e "fetch(process.argv[1]).then(r=>console.log(r.status)).catch(()=>console.log('down'))" https://example.com/health
```

```
watches: { "working tree": { command: "git describe --always --dirty", fires: "change" } }
```

## A watch that sets the status, with no run

When a goal only reports a state (is the tree clean, is the service up), a run that reads the check and calls `end_run` costs a model turn for every change. Give the watch `status` rules instead and it sets the goal's status and tone itself:

```
watches: { "working tree": { command: "git status --porcelain", fires: "change", status: {
  rules: [{ match: "^ ?M ", status: "uncommitted changes", tone: "attention" }],
  default: { status: "clean", tone: "ok" } } } }
```

- At each check the first rule with `run: true` whose `match` (a regular expression) matches any line wins, so a line that should start a run is never hidden by an earlier rule; then the first rule that matches any line; with none, `default`. The status is set from the first check on.
- The status text is only ever the rule's, never the command's output, at most 40 characters. Tones are `ok`, `attention` and `problem`.
- No run starts unless the winning rule (or the default) says `run: true`; then its new lines are events, as usual. On a `fires: "new"` watch, a check that starts no run marks nothing seen, and when a run rule wins a line only a quiet rule matches is never an event or marked seen, so a run rule or default added later can still fire on those lines. A `fires: "change"` watch compares the whole output, so a quiet line is an event whenever a run rule wins and the output changed, and adding a run rule for a line that is already there starts no run.
- The status is written only when it changes. It replaces a run's status and any status check attached to it; a later run's `end_run` status replaces it in turn. The pane says "set by watch <name>".
- Editing a watch's rules keeps what it has seen. Adding rules to a watch, or removing them all, starts it over, like changing its command.

## Tool watches: what only a connector reaches

Mail, calendars and cloud files have no command to run: only a Claude Code session can reach their connectors. For those a watch names a **tool** instead of a command. The session that runs goals calls it every few minutes, with no model turn and nobody asked, and Quarterdeck reads the items out of its answer.

- `tool`: the tool's full name, as your tool list has it (`mcp__claude_ai_Gmail__search_threads`). It must be a connector or MCP tool that only reads. Quarterdeck's own tools are refused, and so is a tool the goal's rules put in a category that is `propose` or `off`.
- `input`: the tool's arguments. Ask for ids only and for few results: the answer is read, not kept.
- `match` (optional): a regular expression over the answer's text; each match's first group is one item. Left out, every `"id": "…"` in a JSON answer is an item, which suits most searches. Each match must differ per item: a fixed pattern with no group, such as `[Dd]ryer`, turns every item into the same line, so capture what differs, e.g. `(\w[^·\n]*) · <listing title>`. Setting such a watch answers with a warning.
- Call the tool yourself first with the same input and look at the answer: check the ids are there and are stable.
- The first call is made within a minute by the session running goals. `goal_detail` shows the watch as failing, with the reason, if the connector isn't signed in there or the call is refused.
- A call that takes over 30 seconds, is refused by a permission rule, or answers an error is a failed check: nothing starts.

New mail in the inbox (Gmail connector):

```json
{ "goal": "Inbox", "watches": { "new mail": { "tool": "mcp__claude_ai_Gmail__search_threads", "input": { "query": "in:inbox newer_than:2d", "pageSize": 25, "view": "THREAD_VIEW_IDS_ONLY" }, "every_minutes": 5 } } }
```

Keep the search narrow and recent (`newer_than:2d`, a sender, a label), so a thread that scrolls off the first page and comes back isn't taken for new. The run is told thread ids; say in the goal's instructions to read each with the connector's `get_thread`.

## A tool watch with steps (reading a page in the browser)

Some sources need two calls, and the second needs a value from the first (Claude in Chrome: `tabs_create_mcp` opens a tab, `get_page_text` reads it by tab id). Give `steps` (up to 4) instead of `tool`, and `finally` for a clean-up call that always runs:

```json
{ "steps": [
    { "tool": "mcp__claude-in-chrome__tabs_context_mcp", "input": { "createIfEmpty": true } },
    { "tool": "mcp__claude-in-chrome__tabs_create_mcp", "pick": { "tabId": { "regex": "Tab ID: ([0-9]+)" } } },
    { "tool": "mcp__claude-in-chrome__navigate", "input": { "tabId": "{{tabId}}", "url": "https://example.com/inbox" } },
    { "tool": "mcp__claude-in-chrome__get_page_text", "input": { "tabId": "{{tabId}}" }, "expect": "Dryer", "retry": 3 } ],
  "finally": { "tool": "mcp__claude-in-chrome__tabs_close_mcp", "input": { "tabId": "{{tabId}}" } },
  "match": "(.+)", "every_minutes": 15 }
```

- Try the calls yourself first and read the answers: the pick's regex needs exactly one group (or use `json`: `a.b[0]`).
- Page text changes (timestamps such as "2 m", "5 m"): make `match` pick only stable parts (a name, a message's first words), or `fires: new` will start runs that find nothing new. Test `match` against two reads a few minutes apart.
- Reading can change what the site does: opening an inbox may mark messages seen and stop the site's own emails or pushes.
- The extension not connected, or a site-permission prompt nobody can answer, is a failed check, never "nothing new". A browser problem the tool answers as ordinary text (a lost tab group, a login page, "content not available") is not marked as an error, so it looks like "nothing new" unless the reading step gives `expect`, a regex its answer must match. Name something only the loaded content has, such as a listing title or a row label you know is there ("Dryer"), never a word in the URL, the title or the navigation ("Inbox", "Marketplace"): those are there on a blank or signed-out page too. Claude in Chrome's reading tools (`get_page_text`, `read_page`, `find`) start their answer with a `Title:` / `URL:` / `Source element:` header ended by `---`; the runner strips it, so `expect`, picks and `match` see only the page content. an answer that doesn't match is a failed check naming the step and the pattern (the page text is left out of the error, since it is outside text). An empty result that matches `expect` is still a good check.
- A picked number reaches the tool as a number when the input is exactly `"{{name}}"`.
- Facebook Marketplace inbox: read it with `read_page`, not `get_page_text`, which gives only the frame (`Inbox / More / Selling / Buying`). `read_page` lists one row per conversation, such as `generic "<buyer name><listing title>"`: give `match` one capture group per buyer row on the listing title, and `expect` a listing title you sell (content only, never "Inbox" or "Marketplace"). Offers made with the offer button may show only in the docked Messenger chat, not in the inbox list, so a page watch can miss them: the reliable path is a Gmail watch on Facebook's Marketplace message emails (the person turns those emails on in Facebook's notification settings).
- The first step makes sure the session has a tab group: without one, `tabs_create_mcp` fails with `This session has no tab group of its own`, and a lost group does the same. When there is none, that call can open a Chrome window.
- `navigate` returns before the page has loaded, so the step that reads it can fail on a blank tab or read the previous page. Give that step `retry` (tries in all, 1 to 5, such as 3) with an `expect`: when the call errors or can't run (Claude in Chrome's "Navigate to a web page first" comes back this way), misses `expect` or misses a pick, it waits about 2 s and calls the same step again with the same picks. Only that step repeats, so a retry never opens a second tab; the last failure is reported with the number of tries, e.g. `(step 4, …, after 3 tries)`. The time limit (30 s) covers the whole sequence, retries and their waits included, not each step.
- Create the tab yourself: `navigate` without a `tabId` reuses the first tab in the session's group, which `finally` would then close.
- Each check opens a tab in the person's real browser: always give a `finally` that closes it.

## Fewer quiet runs

Every run a watch starts is a full model run, so a run that finds nothing worth doing costs as much as one that does. Cut them at the source:

- **Check as seldom as the source allows.** Keep `every_minutes: 5` only where minutes matter (a free item that goes within the hour, a failing build someone is waiting on). New issues, feeds, replies and most mail are fine at 30 to 60 minutes, or more.
- **Print only lines that need a run.** Filter in the command (`--label`, `--search`, jq's `select`), or give `match` and `ignore`:
  - `match`: for a command, only output lines this regular expression matches count; for a tool, it picks the items out of the answer (see below). Filtered before the 200-line cap.
  - `ignore` (either kind): lines this regular expression matches are left out: never a run, never marked seen, not read by status rules. Example: `"ignore": "dependabot|renovate"` on a pull request watch. Removing `ignore` later lets those lines fire, since they were never seen.
- **Gate runs on the lines.** Status rules with `run: true` (below) start a run only when a line matches a rule that says so; the rest only set the status.
- **Space out watch runs.** A goal with several watches starts a run for each one that fires. Set the goal's `min_watch_gap_minutes` with `update_goal` (20 to 30 suits most goals with several watches): after a watch-started run, news that arrives within the gap waits and shares the first run after it. Give a watch `"urgent": true` when its news can't wait (free items): it starts a run at once, which also carries whatever else is waiting. Scheduled runs and Run now are not held by the gap, and they pick up waiting news too.

```json
{ "goal": "Listings", "min_watch_gap_minutes": 30, "watches": { "free items": { "command": "node free.js", "every_minutes": 5, "urgent": true }, "new listings": { "command": "node listings.js", "every_minutes": 30, "ignore": "^sold " } } }
```

## When not to use a watch

- **The source can call out** (a service with webhooks, a CI job): use the goal's webhook, `/api/goals/<id>/trigger` on the Quarterdeck web app. It needs the web app running and reachable from the sender.
- **The work is periodic anyway** ("every morning, summarise…"): a schedule alone is enough.
- **The connector has no tool that lists items by id**: give the goal a short schedule, and have its instructions say to check for what is new and to `remember` the last thing it handled.

A goal can have both a schedule and watches. The watch brings the run forward; the schedule still catches whatever the watch can't see.

## Setting, changing and removing

```json
{ "goal": "Triage issues", "watches": { "new issues": { "command": "gh issue list --repo OWNER/REPO --state open --limit 100 --json number --jq \".[].number\"", "every_minutes": 5 } } }
```

- Giving an existing name changes that watch. A new command starts over with a new first check.
- `null` removes a watch: `{ "watches": { "new issues": null } }`.
- `goal_detail` lists a goal's watches and says when one is failing and why.
- Tell the goal what to do with the news: add a line to its instructions such as "watch_events lists new issue numbers: read each with `gh issue view` and propose a label".
