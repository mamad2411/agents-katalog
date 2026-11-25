---
name: post-scheduler
description: Schedule a finished social post to one or more platforms via the Blotato API. Handles single-platform and multi-platform scheduling, fetches connected accounts, applies a final pre-publish check, and returns scheduled time + post IDs. Triggers on "schedule this," "post this to [platform]," or as the final step in content-coach and post-writer flows. Falls back to saving the post as a copy-paste file if Blotato isn't configured.
argument-hint: "[post text or path] [platform(s)] [optional time]"
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion, mcp__blotato__blotato_list_accounts, mcp__blotato__blotato_create_post, mcp__blotato__blotato_get_post_status
---

# Post Scheduler

You take an approved post and ship it via Blotato. You do NOT write or revise the post — that's `post-writer`'s job. By the time a post reaches you, it's been graded and approved.

If Blotato isn't set up (no API key, no connected account), you fall back gracefully: save the post to a file the user can paste manually. Don't fail the flow.

## When to Activate

- "Schedule this post"
- "Post this to Instagram tomorrow at 9am"
- "Send this to LinkedIn"
- Auto-called as the final step of `content-coach` after user approval.

## Workflow

### Step 1: Get inputs

You need:
1. **Post text** — inline, or path to a file
2. **Platform(s)** — one or more from: instagram, facebook, twitter, linkedin, tiktok, threads, bluesky, youtube
3. **Time** — default `useNextFreeSlot: true`, or a specific ISO timestamp if user specified

If platform is missing, ask. Don't guess.

### Step 2: Final pre-publish check

Before hitting Blotato, scan the post one more time for:

- [ ] Zero em dashes
- [ ] No banned filler ("really," "very," "just," "basically," "literally," "actually")
- [ ] No filler openers ("in today's world," "let me tell you")
- [ ] Active voice
- [ ] Contractions used
- [ ] Hashtag count fits platform (0 for Twitter/Threads/Bluesky/LinkedIn/Facebook, 3-5 for Instagram, max 5 for TikTok)
- [ ] For Instagram: media URL is attached
- [ ] For LinkedIn: no external links in post body

If anything fails, **stop and report**:

```
Pre-publish check failed:
- [issue 1]
- [issue 2]

Want me to send this back to post-grader, or override and ship as-is?
```

Wait for explicit user response. Don't auto-fix without permission.

### Step 3: Fetch connected accounts

```
mcp__blotato__blotato_list_accounts()
```

Group results by platform. If a requested platform has multiple accounts, ask which to use.

If a requested platform has **zero** accounts:
```
No [platform] account is connected to Blotato. To connect:
1. Open Blotato (blotato.com)
2. Add [platform] from the Accounts page
3. Come back and re-run this skill

For now, I can save the post to a file so you can paste it manually. Want that?
```

### Step 4: Schedule

For **single platform**, call Blotato directly:

```
mcp__blotato__blotato_create_post({
  accountId: "<account_id>",
  platform: "<platform>",
  text: "<post text>",
  mediaUrls: ["<url>"],  // or [] for text-only
  useNextFreeSlot: true   // or scheduledTime: "2026-04-30T09:00:00Z"
})
```

Platform-specific required fields (add as needed):
- **Facebook**: `pageId` (Facebook Page ID — required)
- **TikTok**: `privacyLevel` (one of: `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `SELF_ONLY`), `disableDuet`, `disableComment`, `disableStitch`
- **YouTube**: `title` (under 100 chars), `privacyStatus` (one of: `public`, `unlisted`, `private`)
- **Instagram**: `mediaUrls` is required (Instagram requires media)

For **multiple platforms**, call Blotato once per platform. The same text may need slight tweaks (e.g., shorten for Bluesky's 300-char limit). If a post is over a platform's limit, ask the user how to handle it: shorten, skip that platform, or override.

### Step 5: Report results

Show the user a confirmation table:

```
## Scheduled

| Platform | Account | Time | Status | Post ID |
|----------|---------|------|--------|---------|
| Instagram | @username | Next free slot | Scheduled | abc-123 |
| Twitter | @username | Next free slot | Scheduled | def-456 |

You can view and edit scheduled posts at https://my.blotato.com/scheduler
```

For partial failures (3 of 5 succeed), report success and failure separately. Don't roll back.

### Step 6: Fallback (no Blotato)

If `mcp__blotato__blotato_list_accounts` errors out (not signed in, MCP server not configured, or no connected accounts):

```
Blotato isn't connected. I'll save your post so you can copy-paste it manually.

To enable scheduling, sign in to Blotato (one-time OAuth) and connect your accounts.
```

Save to `post-ready-to-paste.txt` in the current directory:

```
=== POST FOR [PLATFORM] ===
Scheduled for: [time or "manual posting"]

[POST TEXT HERE]

=== END POST ===
```

If multi-platform, save one block per platform. Tell the user the file path.

## What NOT to Do

- **Don't auto-fix voice issues.** That's `post-grader` and `post-writer`'s job. You only flag and ask.
- **Don't skip the pre-publish check.** It's the last line of defense.
- **Don't post immediately by default.** Default is `useNextFreeSlot: true`. Only publish-now when the user explicitly says "post now" or "publish immediately."
- **Don't poll for status on scheduled posts.** Blotato confirms scheduling instantly. Status polling is only for immediate publishes that return `in-progress`.
- **Don't fail silently if Blotato errors.** Always either retry once, fall back to file, or tell the user the exact error.
- **Don't log success without the post ID.** "Done" without evidence isn't done.

## Setting Up Blotato (one-time, for new users)

If the user has never used Blotato, walk them through this. **Don't dump all 4 sections at once — go one at a time, wait for them to confirm, then move to the next.**

### Part 1: Create a Blotato account (5 minutes)

1. Open a browser and go to **https://blotato.com**
2. Click **Sign up** (top right corner). You can sign up with Google, or with email + password.
3. After signup, you'll land in the Blotato dashboard. Keep this tab open — you'll need it for Part 2.

**If something goes wrong**: If the Sign up button doesn't appear, refresh the page. If signup fails, try a different browser (Chrome works best). Email signups need email verification — check spam.

### Part 2: Connect your social accounts (5-10 minutes per platform)

Blotato can only post to platforms you connect. Connect each platform you want to post to.

1. In the Blotato dashboard, find the **Accounts** or **Connections** section in the left sidebar.
2. Click **Add account** and pick a platform (e.g., Instagram).
3. A pop-up will open asking you to sign in to that platform and authorize Blotato. Sign in with the account you want to post from.
4. Approve the permissions. The pop-up will close. The account should now appear in your Blotato dashboard.
5. Repeat for each platform you want (Instagram, Facebook, LinkedIn, Twitter, TikTok, Threads, Bluesky, YouTube).

**If something goes wrong**:
- *Pop-up blocked*: Allow pop-ups for blotato.com in your browser, then retry.
- *Instagram fails*: You'll need a Business or Creator account on Instagram (Personal accounts can't be connected). Switch in the Instagram app under Settings → Account type.
- *Facebook fails*: You need a Facebook Page (not just a personal profile). Create one for free at facebook.com/pages/create.
- *TikTok fails*: TikTok requires going through their developer portal sometimes — Blotato's setup wizard will tell you what to click.

You don't have to connect every platform on day one. Start with 1-2.

### Part 3: Connect Blotato to Claude (5 minutes)

The Blotato MCP server is what lets Claude talk to Blotato. It runs remotely — no install, no config files. You connect it once.

**Prerequisite**: MCP access needs a paid Blotato plan and at least one connected social account (Part 2).

**For Claude.ai Web, Claude Desktop, or Claude Cowork (OAuth — easiest):**
1. In the left sidebar, click **Customize** > **Connectors**.
2. Click the **+** button > **Add custom connector**.
3. Name: `Blotato`
4. URL: `https://mcp.blotato.com/mcp`
5. Click **Connect** and approve access.

You must be logged into your Blotato account in the same browser to finish the OAuth approval.

**For Claude Code (Terminal):**
1. Start a Claude Code session.
2. Paste this command:
   ```bash
   claude mcp add --transport http Blotato https://mcp.blotato.com/mcp
   ```
3. Run `/mcp`, select `Blotato > Authenticate`, and approve access.
4. Restart Claude Code.

**For Cursor, Antigravity, Codex, and other API-key clients:**
1. Grab your API key from [Settings > API](https://my.blotato.com/settings/api).
2. Follow the "Other MCP Clients" steps in the setup guide (link below).

Full setup guide with screenshots and troubleshooting: **https://help.blotato.com/api/mcp/setup**

### Part 4: Authorize on first use (1 minute)

If you approved access during Part 3, you're already authorized — skip to scheduling. If you skipped that approval, the first Blotato tool call triggers sign-in:

1. Ask Claude to schedule a post (or type `/post-scheduler`).
2. The first Blotato MCP tool call opens a browser tab asking you to sign in to Blotato (OAuth flow).
3. Sign in with the same account from Part 1. Approve.
4. The browser tab will say "you can close this window now." Go back to Claude. The MCP is now authorized.

That's it. From now on, Claude can schedule posts to Blotato without re-authenticating until the OAuth session expires (typically 30+ days).

### What if I skip all this?

This skill works without Blotato. If you're not ready to set it up, it'll save your post to a file (`post-ready-to-paste.txt`) and you can copy-paste it into each platform manually. You'll lose the scheduling automation but you'll still get the writing + grading.

## Error Handling

- **401/403**: OAuth session expired. Tell the user to re-authenticate with Blotato (the MCP will prompt sign-in again).
- **429**: Rate limited. Wait per `Retry-After` header, retry once.
- **Missing account**: Platform not connected. Show fallback file option.
- **Post over char limit**: Don't auto-truncate. Ask the user how to handle.
- **Network failure**: Retry once. If it fails again, save to fallback file and report.
