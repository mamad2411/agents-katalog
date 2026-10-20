---
name: ssagent-profile
description: Configures SSAgent preferences interactively and writes them to ~/.ssagent/profile.yml. Sets note format, storage location, ASQ root, DAB creation, closure reports, and custom instructions used by all ssagent skills. Runs incrementally — only asks about missing or new settings, confirms existing ones.
user-invocable: true
model: haiku
---

# SSAgent Profile Setup

Interactive setup for SSAgent preferences. Writes `~/.ssagent/profile.yml`.

**Usage:** `/ssagent-profile`

---

## Incremental Mode

Before asking any questions, check for an existing profile:
```bash
cat ~/.ssagent/profile.yml 2>/dev/null
```

**If a profile exists:**
1. Parse it into a key-value map.
2. Compare its keys against the **full key list** (see Step 4 YAML template below).
3. Identify **missing keys** — these are new settings added since the profile was created.
4. For missing keys: ask the user the corresponding question (from Steps 1–3 below), clearly noting these are new settings.
5. For existing keys: show all current values in a summary and ask: "These existing settings look correct?" with options: "Yes, keep all" (Recommended), "Change one or more". If the user wants to change, ask which key(s) and re-prompt only those questions.
6. Skip Step 0 (Salesforce Identity) if `sf_org`, `sf_user_id`, and `initials` are already set — unless the user explicitly wants to re-authenticate.

**If no profile exists:** run all steps from scratch (full setup).

---

## Step 0 — Salesforce Identity

Invoke `fe-salesforce-tools:salesforce-authentication` and note the authenticated username.

Then fetch the user's Salesforce ID and initials:
```bash
sf data query --query "SELECT Id, FirstName, LastName FROM User WHERE Username = '<SF_ORG_USERNAME>'" --target-org <SF_ORG_USERNAME> --json 2>/dev/null | python3 -c "
import sys, json
u = json.load(sys.stdin)['result']['records'][0]
print('sf_org:', '<SF_ORG_USERNAME>')
print('sf_user_id:', u['Id'])
print('initials:', u['FirstName'][0] + u['LastName'][0])
"
```

Store `sf_org`, `sf_user_id`, and `initials` — they will be written to the profile at the end.

---

## Step 1b — Update Channel Preference

Use `AskUserQuestion`:

**Q0b** "Where should SSAgent post your status updates?"
- "Both (dual-write)" (Recommended) — write to `Request_Status_Notes__c` and post to Chatter sidebar
- "Notes field only" — write to `Request_Status_Notes__c` only
- "Chatter only" — post to Chatter feed only

Map to `sf_update_channel`: `dual`, `notes`, or `chatter`.

**Optional context — Logfood detection:** Before presenting the question, attempt to fetch historical usage stats to help inform the user's choice. This is best-effort — skip silently on any failure.

Resolve the detection script path:
```bash
DETECT_CHANNEL=$(ls ~/.claude/plugins/cache/fe-vibe/fe-ssagent/*/skills/ssagent-sfdc/scripts/detect_sf_update_channel.py 2>/dev/null | sort -V | tail -1)
```

If found, run it with the user's `sf_user_id`:
```bash
python3 "$DETECT_CHANNEL" --sf-user-id "<SF_USER_ID>" --profile logfood
```

If the script succeeds, show the stats as context before the question:
```
For reference — your last 12 months of ASQ activity:
  - X% of your ASQs have Chatter posts
  - Y% have Request_Status_Notes__c populated
```

If detection fails or the script is not found, skip the context and ask the question without it.

---

## Step 1 — Note Format

Use `AskUserQuestion` with these two questions:

**Q1** "How should note prefixes be formatted?"
- `<INITIALS> YYYY-MM-DD` (Recommended) — e.g. "TR 2026-02-20"
- `<FULL_NAME> YYYY-MM-DD` — e.g. "Timo Roest 2026-02-20"
- `YYYY-MM-DD only` — e.g. "2026-02-20"

**Q2** "What template should notes follow?"
- `<prefix>: <summary>. Next: <next steps>.` (Recommended)
- `<prefix>: <summary>.`
- `<prefix>: <freeform>`

**Q2b** "How should notes be separated when prepending?"
- `Single newline` (Recommended) — notes are separated by one line break
- `Double newline` — notes are separated by a blank line for readability

Map answers to `note_format.prefix`, `note_format.template`, and `note_format.separator` (`single` or `double`).

---

## Step 2 — Storage & Workspace

Use `AskUserQuestion` with these two questions:

**Q3** "Where do you keep engagement notes?"
- `Salesforce only` (Recommended) — notes stay in Request_Status_Notes__c
- `Google Docs` — also create a Google Doc per engagement
- `Markdown in repo` — write notes to the engagement repo

Map to `note_location`: `local-only`, `google-docs`, or `markdown-in-repo`.

**Q4** "Should new ASQs auto-create a Databricks Asset Bundle?"
- `Yes` (Recommended)
- `No — folder only`

Map to `auto_create_dab`: `true` or `false`.

**Q4b** "Create a Google Doc closure report when closing ASQs?"
- `Always` (Recommended) — automatically create a branded closure report in the shared Drive folder
- `Ask each time` — prompt before creating
- `Never` — skip closure reports

Map to `closure_doc`: `always`, `ask`, or `never`.

---

## Step 3 — Custom Instructions

Use `AskUserQuestion`:

**Q5** "Any custom instructions for note drafts?"
- `None`
- `Always mention stakeholder names`
- `Keep notes concise (one line max)`

The user can also select "Other" to enter freeform text (e.g. "Keep notes in Dutch").

Map to `custom_instructions`.

---

## Step 4 — Write Profile

Show a summary of all values (merged: existing + newly set):

```
SSAgent Profile Summary:

  SF org:          timo.roest@databricks.com
  SF user ID:      0053f000000WSlUAAW
  Initials:        TR
  Update channel:  dual
  Note prefix:     <INITIALS> YYYY-MM-DD
  Note template:   <prefix>: <summary>. Next: <next steps>.
  Note separator:  single
  Note location:   local-only
  ASQ root:        ~/ASQ
  Auto-create DAB: true
  Default catalog: users
  Calendar past:   7 days
  Calendar future: 14 days
  Email lookback:  14 days
  Closure doc:     ask
  Closure folder:  14c9jL-k4GusjRr6kwqdUCtpXGennm-70
  Custom:          (none)
```

Then use `AskUserQuestion` to confirm:
- "Write this profile?" — `Yes, write it` (Recommended), `Edit a value`

On approval, create the directory and write the file:

```bash
mkdir -p ~/.ssagent
```

Write `~/.ssagent/profile.yml`:

```yaml
# SSAgent Profile — generated by /ssagent-profile
version: 1
sf_org: "<SF_ORG_USERNAME>"
sf_user_id: "<SF_USER_ID>"
initials: "<INITIALS>"
sf_update_channel: "<chatter|notes|dual>"
note_format:
  prefix: "<CHOSEN_PREFIX>"
  template: "<CHOSEN_TEMPLATE>"
  separator: "<single|double>"
note_location: <CHOSEN_LOCATION>
asq_root: ~/ASQ
auto_create_dab: <true|false>
default_catalog: users
lookback:
  calendar_past_days: 7
  calendar_future_days: 14
  email_days: 14
closure_doc: "<always|ask|never>"
closure_folder_id: "14c9jL-k4GusjRr6kwqdUCtpXGennm-70"
custom_instructions: "<CHOSEN_CUSTOM>"
```

Confirm to the user:

```
Profile written to ~/.ssagent/profile.yml
All ssagent skills will use these preferences. Re-run /ssagent-profile to change them.
```
