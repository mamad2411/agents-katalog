---
name: draft-post-batch
description: >
  Draft and publish a batch of social media posts directly into Planable as drafts.
  Use this skill whenever the user wants to generate multiple posts for a client,
  create content for a workspace, write a week's worth of posts, batch-create drafts,
  or says things like "draft posts for [client]", "create 5 posts about [topic]",
  "fill the calendar for [client]", or "write posts and add them to Planable".
  Always activate this skill when post creation + Planable is involved.
---

# Draft a post batch for a client

Generate a set of on-brand social media post drafts and create them directly in Planable.

## How this skill works

1. Gather inputs (client/workspace, platform, topic, number of posts, tone/angle)
2. Identify the right workspace and page(s) in Planable
3. Generate the post copy
4. Create each draft directly in Planable via the connector

---

## Step 1: Gather inputs

Before writing anything, confirm:

- **Workspace / client name** — which Planable workspace to post into
- **Platform(s)** — LinkedIn, Instagram, Facebook, X/Twitter, TikTok, etc.
- **Topic or brief** — what the posts should be about
- **Number of posts** — how many drafts to create (default: 5 if not specified)
- **Tone or angle** — optional; if not provided, use the platform's natural register
- **Proposed schedule** — optional; if provided, space posts evenly across the range
- **Labels** — optional; ask only if the user mentions them
- **Team-only / internal note** — optional; default is false (visible to all workspace members)

If the workspace name is ambiguous or not provided, call `list_workspaces` and show the options. Do not guess.

---

## Step 2: Navigate to the right workspace and page

```
list_workspaces → find matching workspace → get workspaceId
list_pages(workspaceId) → find matching page(s) for the requested platform(s)
```

- Match workspace by name (case-insensitive)
- Match page by platform type (`facebook`, `instagram`, `linkedin`, `twitter`, `tiktok`, `youtube`, `pinterest`, `threads`, `universal`)
- If multiple pages exist for the same platform, ask the user which one to use
- If labels are requested, call `list_labels(workspaceId)` to get UUIDs

---

## Step 3: Write the posts

Generate all drafts before creating any of them in Planable.

**Platform character/format guidelines:**
| Platform | Max length | Notes |
|---|---|---|
| LinkedIn | ~3,000 chars | Professional tone, can be longer-form, use line breaks |
| Instagram | ~2,200 chars | Visual-first captions, hashtags at end or first comment |
| Facebook | ~63,206 chars | Conversational, shorter tends to perform better |
| X/Twitter | 280 chars | Punchy, no filler |
| TikTok | ~2,200 chars | Casual, trend-aware |
| YouTube | ~5,000 chars (description) | Informational, include keywords naturally |

**Writing guidelines:**
- Match the client's industry and voice if context is available
- Vary the hook and format across the batch — don't repeat the same structure
- No banned words: seamless, streamline, effortlessly, optimize, enhance, all-in-one, unleash, eliminate, etc.
- Active voice, contractions, short sentences
- If posts are for Planable's own channels, apply Planable brand voice (see brand guidelines in project)

Show the user all drafts in a clear preview **before** creating them in Planable, unless they've explicitly said "just create them."

---

## Step 4: Create the drafts in Planable

After showing the preview and getting confirmation (or if the user said to go ahead directly):

**Single platform:**
```
create_post(
  workspaceId,
  pageId,
  text,
  scheduledAt (if provided),
  labels (if provided),
  teamOnly (default: false)
)
```

**Multiple platforms with same content:**
```
create_grouped_post(
  workspaceId,
  pageIds[],
  text,
  scheduledAt (if provided),
  labels (if provided)
)
```

**Multiple platforms with adapted content:**
Call `create_post` once per platform with the platform-specific version of the copy.

---

## Step 5: Confirm and summarize

After all posts are created, report back:
- How many drafts were created
- Which workspace and page(s) they're in
- Proposed schedule times (if any)
- Any `validationErrors` returned (e.g., Instagram requires media — flag this clearly)
- A direct note that posts are drafts only and will not publish until approved/scheduled in Planable

---

## Edge cases

- **Media**: This skill creates text-only drafts by default. If the user provides a public image URL, pass it as `mediaUrl`. If they reference a file from their computer, explain that Planable requires a public URL and suggest uploading to Google Drive or similar first.
- **Update coming**: Post editing is not yet available via the connector. If the user asks to revise an existing post, note this and suggest editing directly in Planable.
- **Stories / Reels**: Supported via `classification` parameter. Ask the user if they want post, story, or reels format if the platform supports multiple (Instagram, TikTok, YouTube).
- **Rate**: Create posts one at a time (not in bulk API calls) to surface any per-post validation errors clearly.
