---
name: oxygen-publishing
description: Use OXYGEN Posts and Publishing to save drafts, queue, approve, schedule and read back LinkedIn, X and other channel posts, keep approval separate from status, handle uncertain publishes, and read post performance.
---

# Publish with approval

Read [the runtime contract](../../../docs/runtime-contract.md). Posts hold broadcast artifacts and what happened to them; Publishing schedules, approves, dispatches and retries them. A post is a public write in someone's name, so a post the user has not seen stays unapproved. For writing the copy, use [oxygen-linkedin-content](../oxygen-linkedin-content/SKILL.md).

## Save a draft

A post the user asked for but has not approved is saved, not left in chat: `oxygen publishing posts create --draft --publish-at <iso> --text-file post.txt --json`. A draft needs no sender and publishes nothing. Return its link.

## Queue a post

1. Check the sender is active: `oxygen senders list --json`.
2. Write from stored context (`oxygen knowledge resolve --purpose outbound_copy --json`); mark any offer detail the context does not state as `[confirm]`.
3. Create without approval with `--sender`, `--publish-at` and `--timezone`. It lands scheduled and needs approval; nothing sends.
4. Show each post exactly as queued, edit while unapproved, then approve only the posts the user approved: `oxygen publishing posts approve <post_id> --json`.
5. Read back status, attempts and the provider post id.

Status (where the post sits) and approval status (review state) are separate. Editing an approved post revokes its approval. One post can span several channels with `--group-with`.

## Locks

- `publishing_effect_outcome_uncertain`: the channel never confirmed the post. Ask the user to check the profile; only if it is absent, retry with `--confirm-not-published`.
- A rate-limited post is deferred, not failed.
- Team amplification makes teammates' accounts react and comment in public; it needs approval, a ceiling and a stated account-safety risk.
