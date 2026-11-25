---
name: sec-fetch
description: >
  This skill should be used when any other skill or agent needs to fetch data from
  SEC EDGAR domains (www.sec.gov, data.sec.gov, efts.sec.gov). It handles the
  required User-Agent header with the user's name and email, reading from config.json
  if available or prompting the user and saving credentials for future use.
---

# SEC EDGAR Fetch

Utility skill for fetching data from SEC EDGAR endpoints. SEC requires a `User-Agent` header containing a name and email address for all programmatic access — requests without it are blocked with HTTP 403.

## Process

### Step 1: Resolve SEC Credentials

Check if credentials already exist in the plugin config:

```bash
cat ${CLAUDE_PLUGIN_ROOT}/config.json 2>/dev/null
```

- **If `config.json` exists** and contains `sec.user` and `sec.email`, use those values.
- **If `config.json` does not exist or is missing SEC fields**, use the AskUserQuestion tool to ask:

> SEC EDGAR requires all API users to identify themselves (regulatory requirement).
> Please provide:
> 1. Your full name
> 2. Your email address

Then save the credentials by writing/updating `${CLAUDE_PLUGIN_ROOT}/config.json`:

```json
{
  "sec": {
    "user": "<provided name>",
    "email": "<provided email>"
  }
}
```

If `config.json` already exists with other fields, merge the `sec` section — do not overwrite existing fields.

### Step 2: Fetch the URL

Run the `sec-fetch.sh` script with the resolved credentials:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/sec-fetch/scripts/sec-fetch.sh "<url>" "<sec.user>" "<sec.email>"
```

Return the output to the calling skill/agent.

### Step 3: Error Handling

- **HTTP 403**: Credentials may be malformed. Re-prompt the user and update `config.json`.
- **HTTP 429 (rate limit)**: SEC enforces 10 req/s. Wait 2 seconds and retry (max 3 retries).
- **Timeout/network error**: Report the failure so the calling skill can fall back to secondary sources.
