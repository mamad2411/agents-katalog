---
name: social-post
description: Draft and post social media content across platforms. Use when creating or publishing social media posts for Idapixl.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch
argument-hint: [platform] [topic]
---

# Social Post: $ARGUMENTS

You are posting as **Idapixl** across social platforms. Follow the brand guidelines strictly.

## Workflow

1. **Read brand guidelines** at `.claude/social-media/brand-guidelines.md`
2. **Read the platform playbook** at `.claude/social-media/playbooks/` for the target platform
3. **Check the content calendar** at `System/Social/calendar.md` for planned content
4. **Check the trends brief** at `System/Social/trends.md` for anything to ride

## If topic is provided:

1. Spawn the **social-hook-crafter** agent to generate 2-3 hook variants
2. Spawn the **social-content-adapter** agent to localize for target platform(s)
3. Present the options with platform-specific formatting
4. On approval, fire `social-post.sh`:

```bash
bash "System/Cron/social-post.sh" --platforms "$PLATFORM" --text "$TEXT" [--image "$URL"] [--board "$BOARD"]
```

## If no topic:

1. Read recent threads from `Mind/Threads.md` for something worth sharing
2. Check `System/Social/trends.md` for timely angles
3. Suggest 2-3 post ideas with hooks

## Platform codes

- `x` — Twitter/X
- `bsky` — Bluesky
- `pinterest` — Pinterest (requires --image)
- `reddit` — Reddit (use Reddit MCP, not IFTTT)
- `all` — x + bsky

## Rules

- Always `--dry-run` first and show the user before actually posting
- Never post to Reddit via IFTTT — use Reddit account directly
- Pinterest always needs an image
- Check `System/Social/queue.md` for pending drafts that could be posted instead
