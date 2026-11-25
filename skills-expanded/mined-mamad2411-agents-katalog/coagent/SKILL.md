---
name: coagent
description: Set up CoAgent feedback collection on any project. Opens a browser for authentication, creates a project, installs Agentation, and wires up the webhook.
disable-model-invocation: true
argument-hint: [project-name]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# CoAgent Setup Skill

Set up CoAgent design feedback collection on the current project.

The user may pass a project name as `$ARGUMENTS`. If not provided, use the current directory name.

**Dashboard URL:** `https://resilient-froyo-83213f.netlify.app`

## Step 1: Authentication

**Supabase URL:** `https://mfxefozwtekirymjzqty.supabase.co`
**Publishable Key:** `sb_publishable_Yktttq_uYUdnj5y6ydTjPQ__FHrUf76`

First, check if cached credentials exist at `~/.coagent/auth.json`. If the file exists, read `access_token`, `user_id`, `supabase_url`, and `publishable_key` from it.

Verify the cached token is still valid:
```bash
curl -s "https://mfxefozwtekirymjzqty.supabase.co/auth/v1/user" \
  -H "apikey: sb_publishable_Yktttq_uYUdnj5y6ydTjPQ__FHrUf76" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

If this returns a user object (has `"id"`), the token is valid — skip to Step 2.

If there are no cached credentials or the token is expired, do the browser auth flow:

1. Generate a random session ID:
```bash
SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
```

2. Open the browser:
```bash
open "https://resilient-froyo-83213f.netlify.app/cli-auth?session=$SESSION_ID"
```
(Use `xdg-open` on Linux instead of `open`.)

Tell the user: "Opening your browser to authenticate with CoAgent. Please sign in and click Authorize."

3. Poll Supabase for the auth result (check every 2 seconds, timeout after 2 minutes):
```bash
for i in $(seq 1 60); do
  RESULT=$(curl -s "https://mfxefozwtekirymjzqty.supabase.co/rest/v1/cli_auth_sessions?id=eq.$SESSION_ID&select=*" \
    -H "apikey: sb_publishable_Yktttq_uYUdnj5y6ydTjPQ__FHrUf76")
  if echo "$RESULT" | grep -q "access_token"; then
    echo "$RESULT"
    break
  fi
  sleep 2
done
```

4. Parse the JSON response (it's an array with one object). Extract `access_token`, `user_id`, `supabase_url`, and `publishable_key`.

5. Save credentials to `~/.coagent/auth.json` for future runs:
```bash
mkdir -p ~/.coagent
cat > ~/.coagent/auth.json << EOF
{
  "access_token": "$ACCESS_TOKEN",
  "user_id": "$USER_ID",
  "supabase_url": "$SUPABASE_URL",
  "publishable_key": "$PUBLISHABLE_KEY"
}
EOF
```

If polling times out with no result, tell the user and suggest retrying.

## Step 2: Create a project

Use the auth token to create a new project via the Supabase REST API:

```bash
curl -s -X POST "$SUPABASE_URL/rest/v1/projects" \
  -H "apikey: $PUBLISHABLE_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "PROJECT_NAME", "owner_id": "USER_ID"}'
```

Extract `id` and `webhook_secret` from the response.

## Step 3: Build the webhook URL

```
$SUPABASE_URL/functions/v1/webhook-receiver?project_id=$PROJECT_ID&secret=$WEBHOOK_SECRET
```

## Step 4: Set up Agentation

Check if Agentation is already installed and set up in the project:

- If an `<Agentation` component already exists in the codebase, just add or update the `webhookUrl` prop on it with the URL from Step 3. Done.
- If Agentation is not set up yet:
  1. Detect the package manager (`yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `bun.lockb` → bun, otherwise npm). Install `agentation` as a dev dependency.
  2. Find the root component (`src/App.tsx`, `src/app/layout.tsx`, `app/layout.tsx`, `src/pages/_app.tsx`, etc.)
  3. Add `import { Agentation } from "agentation"` at the top
  4. Add `<Agentation webhookUrl="WEBHOOK_URL" />` as the last child inside the returned JSX, replacing `WEBHOOK_URL` with the actual URL from Step 3.
  5. If the root component can't be found, ask the user which file to modify.

## Step 5: Report success

Print a summary:
- Project name created in CoAgent
- Which file was modified
- Remind the user to start their dev server to see the Agentation toolbar
- Link to view feedback: `https://resilient-froyo-83213f.netlify.app/projects/$PROJECT_ID`

## Error Handling

- If the auth server times out (2 min): Tell the user and suggest retrying
- If project creation fails: Show the error from Supabase
- If Agentation is already fully configured with a webhookUrl: Just report the dashboard link, no changes needed
