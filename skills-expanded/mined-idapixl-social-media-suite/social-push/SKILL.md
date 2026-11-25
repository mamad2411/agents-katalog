---
name: social-push
description: Push approved content from the queue to platforms. Batch-fire posts that are ready to go.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [all|platform]
---

# Social Push: $ARGUMENTS

Push approved content from the queue to platforms.

## Workflow

1. **Read the queue** at `System/Social/queue.md`
2. **Filter for approved/ready drafts** (status: approved or ready)
3. **If platform argument provided**, filter to that platform only
4. **For each approved post:**

   a. Show the post content and target platform
   b. Run `social-post.sh --dry-run` first:
   ```bash
   bash "System/Cron/social-post.sh" --platforms "$PLATFORM" --text "$TEXT" --dry-run [--image "$URL"] [--board "$BOARD"]
   ```

   c. Confirm with user before firing

   d. On confirmation, post for real:
   ```bash
   bash "System/Cron/social-post.sh" --platforms "$PLATFORM" --text "$TEXT" [--image "$URL"] [--board "$BOARD"]
   ```

   e. Update queue entry status to "posted"
   f. Post logger hook will auto-log to `System/Social/post-log.md`

5. **Summary** — report how many posts pushed, any failures

## Safety

- ALWAYS dry-run first
- ALWAYS show the user what will be posted before firing
- Never batch-fire more than 5 posts without pausing for confirmation
- Pinterest posts must have --image
- Reddit posts go through Reddit directly, not IFTTT

## Queue Status Values

| Status | Meaning |
|--------|---------|
| draft | Not yet reviewed |
| pending | Awaiting review |
| approved | Reviewed and ready to post |
| posted | Successfully published |
| rejected | Reviewed and declined |
