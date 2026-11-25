---
name: discourse-post
description: Post a project description or phase status update to the project's Discourse forum topic. Compiles content from docs/roadmap.md, log.md, and docs/findings.md.
argument-hint: "description|status [<topic-url>]"
allowed-tools: Read, Edit, Bash
---

# Discourse Post Skill

Compile and post a message to the project's Discourse forum topic. Two modes: `description` (project intro) and `status` (phase progress update). Uses the Discourse REST API via `curl`.

## Input

- **$0** (required): Mode — `description` or `status`
- **`<topic-url>`** (optional): Post to a different topic URL for this invocation. If provided and different from the stored URL, ask whether to also save it as the new default.

## Environment

Required (in shell env or `.env` file at repo root):
- `DISCOURSE_API_KEY` — API key from forum profile
- `DISCOURSE_API_USERNAME` — forum username

---

## Workflow

### Step 1: Load Environment

```bash
[ -f .env ] && export $(grep -v '^#' .env | xargs)
```

Check that both `DISCOURSE_API_KEY` and `DISCOURSE_API_USERNAME` are set. If either is missing, stop:
```
❌ Missing credentials. Set in shell or .env:
   DISCOURSE_API_KEY=...
   DISCOURSE_API_USERNAME=...

To generate an API key: <base_url>/u/<username>/preferences/api
```

Validate mode is `description` or `status`. If missing or invalid:
```
Usage: /discourse-post description|status [<topic-url>]
```

---

### Step 2: Bootstrap — Resolve Topic URL

1. If a `<topic-url>` argument was provided:
   - Parse it to extract `base_url`, `topic_id`, `topic_slug`
   - If it differs from the stored URL, ask:
     ```
     Save this as the new default topic URL? [Y/n]
     ```
   - If yes, update `CLAUDE.md`. If no, use it for this run only.
2. Otherwise read `CLAUDE.md` `## Discourse` section for `base_url` and `topic_id`.
3. If no `## Discourse` section exists, prompt for URL (same as `/discourse-read` bootstrap), parse, and save to `CLAUDE.md`:
   ```markdown
   ## Discourse

   - **Topic URL**: <full url>
   - **Base URL**: <base_url>
   - **Topic ID**: <topic_id>
   - **Last read post**: 0
   ```

---

### Step 3: Compile Post Content

#### Mode: `description`

Read the following files:
- `docs/roadmap.md` — extract: research question, hypothesis, phase list with statuses
- `docs/findings.md` — extract: all current findings (brief)

Compile into a Discourse-formatted post:

```markdown
## Project Overview

**Research question:** <from roadmap>

**Hypothesis:** <from roadmap>

## Validation Roadmap

<Phase tree as a numbered list with status indicators: ✅ complete | 🔄 in-progress | ⏳ pending>

## Key Findings So Far

<Numbered list of findings from docs/findings.md, one sentence each>

## Next Steps

<Pending phases from roadmap>

---
*Posted via Claude Code · [GUIDELINES.md](./GUIDELINES.md)*
```

#### Mode: `status`

Read the following files:
- `log.md` — extract the most recent entry (top of file)
- `docs/findings.md` — extract findings added since the last Discourse post date (stored in CLAUDE.md as `last_posted`)
- `docs/roadmap.md` — extract next pending phase

Compile into a Discourse-formatted post:

```markdown
## Status Update — <date>

### Phase Completed: <phase name and number>

**What was done:** <from log What field>
**Why:** <from log Why field>
**How:** <from log How field>

### Key Finding

<Most recent finding from docs/findings.md>

### Next Step

**Phase <N>: <name>** — <goal from roadmap>

---
*Posted via Claude Code · <topic_url>*
```

---

### Step 4: Preview and Confirm

Display the compiled post in full, then ask:
```
Post this to <topic_url>? [Y/n/edit]
```

- **Y**: proceed to post
- **n**: abort, nothing posted
- **edit**: accept freeform edits from user, apply them, re-display, confirm once more

---

### Step 5: Post via Discourse API

```bash
curl -s -X POST "${base_url}/posts.json" \
  -H "Api-Key: ${DISCOURSE_API_KEY}" \
  -H "Api-Username: ${DISCOURSE_API_USERNAME}" \
  -H "Content-Type: application/json" \
  -d "{\"topic_id\": ${topic_id}, \"raw\": $(echo "$content" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}"
```

Parse the response JSON:
- On success: extract `post_number` and `id` from response
- On failure: extract `errors` array and display them

---

### Step 6: Update CLAUDE.md and log.md

On successful post, do two things:

**Update `CLAUDE.md`** — record the last post date:
Replace or add under `## Discourse`:
```
- **Last posted**: <YYYY-MM-DD> (<mode>)
```

**Append to `log.md`** — record the forum activity:
```markdown
## [YYYY-MM-DD] Discourse: posted <mode>

**What:** Posted <mode> update to Discourse topic #<topic_id>  
**Why:** Community communication / project visibility  
**How:** /discourse-post <mode> via Discourse REST API  
**Findings:** Post #<post_number> published at <topic_url>/<post_number>  
```

---

### Step 7: Output Summary

```
✅ Posted to Discourse!

Topic  : <topic_url>
Post # : <post_number>
Mode   : <description|status>
URL    : <base_url>/t/<slug>/<topic_id>/<post_number>

CLAUDE.md updated (last_posted)
log.md updated
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing credentials | Stop with setup instructions including API key generation URL |
| Invalid mode | Print usage and stop |
| 401 Unauthorized | Stop: "Check DISCOURSE_API_KEY and DISCOURSE_API_USERNAME" |
| 403 Forbidden | Stop: "API key may lack post permissions. Check forum profile settings." |
| 404 Topic not found | Stop: "Verify topic URL in CLAUDE.md" |
| 422 Unprocessable | Display `errors` from response body |
| `docs/roadmap.md` missing | Stop: "Run /setup-repo first to scaffold the project structure" |
| `log.md` empty (status mode) | Warn: "No log entries found. Post will note no phases completed yet." |
| User aborts at preview | Exit cleanly, nothing written |
