---
name: fetching-circleci-logs
description: "Fetches CircleCI job logs via the v1.1 API and displays step-level output. Focuses on failed steps. Use when: CI checks fail on a PR, user shares a CircleCI job URL, user asks to check build logs, 'circleci', 'build failed', 'CI failed', 'check the logs'."
---

# Fetching CircleCI Logs

Fetch step-level build logs from CircleCI jobs using the v1.1 API.

## When to use

- PR checks failed and you need to see why
- User shares a CircleCI URL (e.g. `https://circleci.com/gh/org/repo/169955`)
- User asks to investigate a CI failure

## Extract job details from URL

CircleCI URLs follow this pattern:

```
https://circleci.com/gh/{org}/{repo}/{job_number}
```

Extract `org`, `repo`, and `job_number` from the URL. If the user provides only a job number, ask for the org/repo or check the current git remote:

```bash
git remote get-url origin | sed -E 's|.*github\.com[:/]([^/]+)/([^/.]+).*|\1/\2|'
```

## Fetch logs

### Step 1: Get the CircleCI token

```bash
grep 'token' ~/.circleci/cli.yml | awk '{print $2}'
```

If the file doesn't exist or has no token, tell the user to run `circleci setup` or set the token manually.

### Step 2: Fetch job data and display step output

Run this as a single command, substituting `{org}`, `{repo}`, and `{job_number}`:

```bash
TOKEN=$(grep 'token' ~/.circleci/cli.yml | awk '{print $2}') && \
curl -s -H "Circle-Token: $TOKEN" \
  "https://circleci.com/api/v1.1/project/gh/{org}/{repo}/{job_number}" | \
python3 -c "
import sys, json, urllib.request
data = json.load(sys.stdin)
for step in data.get('steps', []):
    for action in step.get('actions', []):
        status = action.get('status', '')
        name = action.get('name', '')
        exit_code = action.get('exit_code')
        failed = action.get('failed', False)
        print(f'STEP: {name} | status: {status} | exit: {exit_code}')
        if failed and action.get('output_url'):
            with urllib.request.urlopen(action['output_url']) as r:
                for msg in json.load(r):
                    print(msg.get('message', '')[:2000])
"
```

### Step 3: Analyze the output

After fetching, summarize:
1. Which steps failed and why
2. The relevant error messages (not the full log)
3. Suggested fix if the cause is clear

## Important notes

- **Use API v1.1** — v2 does not return step-level output with log URLs.
- The `output_url` is a pre-signed S3 URL — no additional auth needed to fetch it.
- Truncate log messages to 2000 chars per action to avoid context window bloat.
- If the API returns 404, the job number is likely wrong or the token lacks access to that project.

## Mandatory Checklist

When fetching CircleCI logs, complete this checklist:

1. [ ] Verify the CircleCI token exists in `~/.circleci/cli.yml`
2. [ ] Verify org, repo, and job number are correctly extracted from the URL or git remote
3. [ ] Verify you are using the v1.1 API (not v2)
4. [ ] Verify you summarized the failure cause, not just dumped raw logs

Do not proceed to suggest fixes until all checks pass.
