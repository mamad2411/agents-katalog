---
name: setup
description: Sets up and gets the Molly recruiting agent running end to end. Use when a user asks to set up, install, configure, deploy, or verify Molly — cloning the repo if needed, collecting credentials into .env, creating the Notion tracker database, verifying Notion/Slack/Exa/GEM access, and wiring up the daily sourcing schedule and Slack triggers.
---

# Molly setup

Interactive setup that takes a user from nothing to a running Molly deployment. It is **idempotent**: every step checks current state first, so it's safe to re-run and safe to start from a repo that's already cloned. Work through the steps in order and confirm each verification passes before moving on.

Ground rules:

- **Never ask the user to paste secrets into chat, and never print secret values** (no `echo $MOLLY_...`, no logging curl requests with resolved tokens). The user puts secrets into `.env` themselves; you only reference them as `$VARS`.
- All verification calls below are read-only. The only writes are labeled: creating the tracker database (step 4), the optional Slack test message (step 5), and deployment wiring (step 6). Ask before each write.

## 1. Get the repo

Check whether you're already inside a clone — the repo root contains `AGENTS.md` and `.warp/skills/molly-sourcing/SKILL.md`:

```bash
git rev-parse --show-toplevel 2>/dev/null
```

- If the git root has both marker files, `cd` to that root and skip cloning.
- If a `./molly-agent` directory already exists with those markers, `cd molly-agent` instead of recloning.
- Otherwise clone and enter it:

```bash
git clone https://github.com/warpdotdev/molly-agent.git
cd molly-agent
```

All later steps run from the repo root.

## 2. Collect configuration in `.env`

Create the local config from the template if it doesn't exist (`.env` is gitignored and never committed):

```bash
test -f .env || cp .env.example .env
```

Then ask the user to open `.env` in their editor and fill it in **themselves** — walk them through obtaining each value, one service at a time:

1. **Notion** — create an internal integration at https://www.notion.so/my-integrations and copy its token → `MOLLY_NOTION_API_KEY`. Create (or pick) a parent page for Molly's Profile Spec pages, share it with the integration (page → `⋯` → Connections), and copy the 32-hex ID from the page URL → `MOLLY_NOTION_PARENT_PAGE_ID`.
2. **Slack** — create a Slack app with a bot token (scopes: `chat:write`, `app_mentions:read`) → `MOLLY_SLACK_BOT_TOKEN`. Pick a sourcing channel, invite the bot, copy the channel ID (channel details → About) → `SOURCING_SLACK_CHANNEL_ID`.
3. **Exa** — create an API key at https://exa.ai → `MOLLY_EXA_API_KEY`.
4. **GEM** — create an API key in GEM's admin settings → `MOLLY_GEM_API_KEY`.
5. **Tracker** — leave `MOLLY_TRACKER_DB_ID` as the placeholder if the user wants step 4 to create the database for them; otherwise paste an existing database ID.

When the user says `.env` is ready, load it without displaying anything:

```bash
set -a; source .env; set +a
```

Then check presence only (names, never values):

```bash
for v in MOLLY_SLACK_BOT_TOKEN MOLLY_NOTION_API_KEY MOLLY_EXA_API_KEY MOLLY_GEM_API_KEY SOURCING_SLACK_CHANNEL_ID MOLLY_NOTION_PARENT_PAGE_ID; do
  [ -n "$(printenv $v)" ] && echo "$v: set" || echo "$v: MISSING"
done
```

Loop back with the user until nothing is missing.

## 3. Verify service access (read-only)

Run each check and show the user a pass/fail summary. Fix failures before continuing.

**Notion token** — expect a bot user object:

```bash
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" -H "Notion-Version: 2022-06-28"
```

**Parent page shared with the integration** — expect `200`; a `404` means the page isn't shared with the integration (fix via page → `⋯` → Connections):

```bash
curl -s "https://api.notion.com/v1/pages/$MOLLY_NOTION_PARENT_PAGE_ID" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" -H "Notion-Version: 2022-06-28"
```

**Slack** — expect `"ok": true` with the bot's identity:

```bash
curl -s -X POST "https://slack.com/api/auth.test" -H "Authorization: Bearer $MOLLY_SLACK_BOT_TOKEN"
```

**Exa** — expect one LinkedIn result:

```bash
curl -s -X POST "https://api.exa.ai/search" \
  -H "Authorization: Bearer $MOLLY_EXA_API_KEY" -H "Content-Type: application/json" \
  -d '{"query": "software engineer", "numResults": 1, "includeDomains": ["linkedin.com"]}'
```

**GEM** — expect a user list (Molly picks her `created_by` user from it at runtime):

```bash
curl -s "https://api.gem.com/v0/users" -H "X-API-Key: $MOLLY_GEM_API_KEY"
```

## 4. Create or verify the Molly Tracker database

**If `MOLLY_TRACKER_DB_ID` is empty or still the placeholder**, offer to create the database under the parent page (this is a write to the user's Notion workspace):

```bash
curl -s -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data @- <<EOF
{
  "parent": {"type": "page_id", "page_id": "$MOLLY_NOTION_PARENT_PAGE_ID"},
  "title": [{"type": "text", "text": {"content": "Molly Tracker"}}],
  "properties": {
    "Role name": {"title": {}},
    "JD Link": {"url": {}},
    "Profile Spec Link": {"url": {}},
    "GEM Project ID": {"rich_text": {}},
    "Molly Status": {"status": {}},
    "Open date": {"date": {}},
    "Assignee": {"people": {}}
  }
}
EOF
```

Take the `id` from the response, have the user set it as `MOLLY_TRACKER_DB_ID` in `.env`, and re-source (`set -a; source .env; set +a`).

The Notion API cannot configure status options — ask the user to open the new database in Notion and edit the **Molly Status** property so its options are exactly: `Not started`, `Calibrating`, `Sourcing`, `Hired`.

**Whether created or pre-existing**, verify the schema:

```bash
curl -s "https://api.notion.com/v1/databases/$MOLLY_TRACKER_DB_ID" \
  -H "Authorization: Bearer $MOLLY_NOTION_API_KEY" -H "Notion-Version: 2022-06-28"
```

Confirm the properties match: `Role name` (title), `JD Link` (url), `Profile Spec Link` (url), `GEM Project ID` (rich_text), `Molly Status` (status, with the four options above), `Open date` (date), `Assignee` (people). Report any mismatches and help the user fix them.

## 5. Optional: Slack channel smoke test (writes one message)

With the user's consent, confirm the bot can post to the sourcing channel:

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $MOLLY_SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  --data @- <<EOF
{"channel": "$SOURCING_SLACK_CHANNEL_ID", "text": "👋 Molly is configured — setup verification message."}
EOF
```

`channel_not_found` or `not_in_channel` means the bot isn't in the channel — have the user invite it (`/invite @Molly`) and retry.

## 6. Wire up triggers (deployment)

Everything above configured the services; Molly now needs a runtime that delivers her three trigger prompts (see `AGENTS.md`). Ask the user which path they want:

**Option A — Warp (Oz cloud agents), managed.** Follow README "Option A": create an environment that clones the user's fork (`oz environment create`), add every `.env` variable as a secret (`oz secret create`), schedule daily sourcing (`oz schedule create --cron "0 8 * * *"` with the sourcing prompt), and wire kick-off @mentions (`oz integration create slack`). Run the commands with the user, substituting their fork and environment ID.

**Option B — any agent harness, self-hosted.** Follow README "Option B": a cron entry (or equivalent scheduler) for daily sourcing that starts an agent in this repo with the env vars set, plus a small Slack Events API listener for @mention kick-offs — or start kick-off runs by hand using the trigger-type-1 prompt shape.

**Calibration handler (both paths).** Calibration needs the Slack interactivity handler in `handlers/slack-review-modal/` (requires `SLACK_SIGNING_SECRET` and `WARP_API_KEY` in `.env`; swap `trigger_agent_run()` in `server.py` for non-Warp harnesses). Deploy it behind a public HTTPS URL and set that URL as the Slack app's Interactivity Request URL — see its README. Alternatively use the modal-free flow in the main README (emoji reactions + @mention; needs extra bot scopes).

## 7. End-to-end test

Finish by proving the whole loop:

1. Have the user write a test JD page in Notion (sections: `## Job Description`, `## Kick-off Notes`, `## Orienting Profiles`) and share it with the integration.
2. @mention Molly in the sourcing channel with the JD page URL — or start a run by hand with the trigger-type-1 prompt shape from `AGENTS.md`.
3. Confirm Molly creates a Profile Spec page under the parent page, adds a tracker row with status `Calibrating`, and posts a calibration batch to the Slack thread.
4. If the modal handler is deployed: click **Review All Candidates →**, submit decisions, and confirm a calibration run fires.

When all of that passes, setup is complete — recap for the user what was configured and where (env vars, tracker DB, schedule, handler URL).
