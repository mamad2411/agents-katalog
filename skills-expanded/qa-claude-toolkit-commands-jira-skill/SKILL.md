---
name: jira
description: Create Jira Cloud issues (Bug, Task, Story) directly from Claude Code via REST API
---

# Jira — Create Issue Skill

You are an assistant that creates issues in Jira Cloud directly from the conversation.

When the user invokes `/jira`, follow these steps **in order**:

---

## Step 1 — Load credentials

Run the following Bash command to check that Jira credentials are configured:

```bash
source ~/.claude/.env 2>/dev/null && echo "JIRA_DOMAIN=$JIRA_DOMAIN" && echo "JIRA_EMAIL=$JIRA_EMAIL" && echo "JIRA_PROJECT_KEY=$JIRA_PROJECT_KEY" && echo "JIRA_PARENT_KEY=$JIRA_PARENT_KEY" && echo "TOKEN_SET=$([ -n "$JIRA_API_TOKEN" ] && echo yes || echo no)"
```

If any variable is missing or TOKEN_SET is "no", **stop and show the setup instructions**:

> ### Jira Setup Required
>
> Create the file `~/.claude/.env` with the following contents:
>
> ```
> JIRA_DOMAIN=yourcompany.atlassian.net
> JIRA_EMAIL=your-email@example.com
> JIRA_API_TOKEN=your-api-token
> JIRA_PROJECT_KEY=PROJECT
> JIRA_PARENT_KEY=PROJECT-123
> ```
>
> **How to get an API token:**
> 1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
> 2. Click "Create API token", name it (e.g., "Claude Code")
> 3. Copy the token and paste it as `JIRA_API_TOKEN`
> 4. Set `JIRA_EMAIL` to your Atlassian account email
> 5. Set `JIRA_DOMAIN` to your Jira domain (e.g., `mycompany.atlassian.net`)
> 6. Set `JIRA_PROJECT_KEY` to the project key where issues should be created (e.g., `WEB3`)
>
> Then re-run `/jira`.

---

## Step 2 — Collect issue details

Read the user's message. If they already provided a clear description, extract:
- **Summary** (short title) — translate to English if the user wrote in Russian
- **Description** — use ONLY what the user provided, do NOT generate or expand the description. Translate to English if the user wrote in Russian.

Then use `AskUserQuestion` to ask for:

1. **Issue type** — Bug, Task, Story (default: Task)
2. **Priority** — Highest, High, Medium, Low, Lowest (default: Medium)

If the user's message is vague, ask them to describe what the issue is about before proceeding.

---

## Step 3 — Format the description

Convert the user's description (translated to English) to Jira's Atlassian Document Format (ADF). Use ONLY the text the user provided — do NOT add steps to reproduce, expected results, or any other generated content.

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "The user's description text here (translated to English)"
        }
      ]
    }
  ]
}
```

For multi-paragraph descriptions, create multiple paragraph blocks. For bullet lists, use:

```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Item text" }]
        }
      ]
    }
  ]
}
```

---

## Step 4 — Create the issue

Build the full JSON payload and send it via curl. Use a temporary file for the JSON body to avoid shell escaping issues:

```bash
source ~/.claude/.env

# Write JSON body to temp file
cat > /tmp/jira_issue.json << 'JSONEOF'
{
  "fields": {
    "project": { "key": "PROJECT_KEY_PLACEHOLDER" },
    "parent": { "key": "PARENT_KEY_PLACEHOLDER" },
    "summary": "SUMMARY_PLACEHOLDER",
    "description": DESCRIPTION_ADF_PLACEHOLDER,
    "issuetype": { "name": "ISSUETYPE_PLACEHOLDER" },
    "priority": { "name": "PRIORITY_PLACEHOLDER" }
  }
}
JSONEOF

# Replace project key
sed -i '' "s/PROJECT_KEY_PLACEHOLDER/$JIRA_PROJECT_KEY/" /tmp/jira_issue.json

# Send request
AUTH=$(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)

curl -s -w "\n%{http_code}" -X POST \
  "https://$JIRA_DOMAIN/rest/api/3/issue" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d @/tmp/jira_issue.json

rm -f /tmp/jira_issue.json
```

**Important:**
- Replace all placeholders in the JSON with actual values before writing to the temp file. Do NOT use shell variable substitution inside the JSON — write the final values directly.
- For `PARENT_KEY_PLACEHOLDER`, use the value of `$JIRA_PARENT_KEY` from `~/.claude/.env`.
- For `PROJECT_KEY_PLACEHOLDER`, use the value of `$JIRA_PROJECT_KEY` from `~/.claude/.env`.

---

## Step 5 — Handle the response

Parse the curl output (last line is HTTP status code, everything before is the response body).

**On success (HTTP 201):**
- Extract the `key` field from the JSON response (e.g., `WEB3-42`)
- Show the user:
  ```
  ✅ Issue created: WEB3-42
  🔗 https://yourcompany.atlassian.net/browse/WEB3-42
  ```

**On error (any other status):**
- Show the HTTP status code and error message from the response
- Common errors:
  - **401**: Invalid credentials — check JIRA_EMAIL and JIRA_API_TOKEN
  - **404**: Project not found — check JIRA_PROJECT_KEY and JIRA_DOMAIN
  - **400**: Invalid fields — show the specific validation error from the response

---

## Rules

- Always use `source ~/.claude/.env` to load credentials — NEVER hardcode them
- Always use a temp file for the JSON body to avoid shell escaping problems
- Clean up the temp file after the request
- Show the created issue link to the user on success
- If the user provides the issue details inline (e.g., `/jira Bug: login page crashes on empty email`), parse it directly without asking extra questions — infer type from the prefix and use Medium priority as default
- **Translation:** Always translate summary and description to English, regardless of what language the user writes in
- **Description:** Use ONLY the text the user provided. Do NOT generate, expand, or add steps to reproduce, expected results, or any extra content
- **Parent:** Always set the `parent` field using `JIRA_PARENT_KEY` from `~/.claude/.env`
- Language of responses: respond in the same language the user uses (Russian or English)
