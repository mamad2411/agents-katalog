---
name: submit-project
description: Submit or update a project on the Skillathon showcase site via the API. Use when the user wants to submit their Claude skill demo to Skillathon, or update an existing submission.
license: MIT
metadata:
  author: skillathon
  version: "1.1"
---

# Submit / Update Skillathon Project

This skill helps users submit a new Claude skill project to Skillathon, or update an existing submission.

## When invoked

### Step 1 — Check for API key

Look for `SKILLATHON_API_KEY` in the environment. If not set, tell the user:
> "You need a Skillathon API key to submit. Please:
> 1. Go to https://hackbarna-skillathon.netlify.app/account (sign in first if needed)
> 2. Generate a new API key
> 3. Copy it and set it: `export SKILLATHON_API_KEY=sk_...`
> Then run `/submit-project` again."

Stop here until they have the key.

### Step 2 — New submission or update?

Ask the user: **"Are you submitting a new project, or updating an existing one?"**

---

## Flow A: Submit new project

Gather project info interactively (you can ask for multiple fields at once):

| Field | Required | Notes |
|-------|----------|-------|
| `title` | ✅ | The skill's display name |
| `description` | ✅ | What it does and what problems it solves |
| `authorName` | ✅ | Their display name |
| `installCommand` | optional | The `owner/repo` part of `npx skills add owner/repo` — skip if not published yet |
| `teamMembers` | optional | Comma-separated collaborator names |
| `tags` | optional | Pick from: Productivity, Developer Tools, AI/ML, Data, Design, Communication, Education, Fun, Utilities, Integration |
| `githubUrl` | optional | Link to GitHub repo or Gist |
| `mediaType` + `mediaUrl` | optional | YouTube/Vimeo video URL or image URL for demo |

Show a summary and ask to confirm, then submit:

```
POST $SKILLATHON_API_URL/api/submit
Authorization: Bearer $SKILLATHON_API_KEY
Content-Type: application/json
```

where `SKILLATHON_API_URL` defaults to `https://hackbarna-skillathon.netlify.app` if not set.

On success, show the returned `id` and tell the user to **save it** — they'll need it to update the project later.

---

## Flow B: Update existing project

Ask for the **project ID** (the `id` returned when they originally submitted). If they don't have it, they can find it in the URL on the project page: `https://hackbarna-skillathon.netlify.app/projects/<id>`.

Ask which fields they want to update — only changed fields need to be sent. Show current values if known.

Send the update:

```
PATCH $SKILLATHON_API_URL/api/update
Authorization: Bearer $SKILLATHON_API_KEY
Content-Type: application/json

{
  "id": "<project id>",
  // only the fields to change:
  "description": "...",
  "installCommand": "owner/repo",
  "mediaType": "youtube",
  "mediaUrl": "https://youtube.com/watch?v=..."
}
```

On success, confirm the project has been updated and link to it on the site.

---

## Error handling

| Status | Action |
|--------|--------|
| 401 | API key invalid — direct to `/account` to regenerate |
| 403 | Not the original author — they can only update their own projects |
| 404 | Project ID not found — ask them to double-check |
| 400 | Missing fields — ask for the missing ones |
| 5xx | Show error message, offer to retry |

## Notes
- `installCommand` should be just `owner/repo` — it becomes `npx skills add owner/repo` on the site
- This skill itself is hosted at https://github.com/hackbarna/skillathon and installed via `npx skills add hackbarna/skillathon`
- If the user is in a skill project directory, offer to infer `installCommand` from the git remote URL
- Keep the conversation friendly and brief — don't overwhelm with all questions at once
- The same API key works for both submit and update (as long as they're the project author)
