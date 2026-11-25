---
name: vidiq-publishing
description: Prepare and adapt supplied content for YouTube, Instagram, TikTok, X, Facebook Pages, and Bluesky; save drafts, publish or schedule approved versions, and track each destination. Use when asked 'post this everywhere', 'publish a Reel', 'upload to YouTube', 'tweet this', 'schedule these posts', 'change my draft', 'what is scheduled', or 'did my post go out'. For changes to a video already on YouTube, use vidiq-video-metadata.
---

# vidIQ Publishing

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

## Enter at the requested stage

| Request | Start here |
| --- | --- |
| Write captions or propose versions only | Adapt the supplied content; no account lookup or saved draft is needed. |
| Save a draft, post, cross-post, upload to a platform, or schedule | Resolve destinations and media, then prepare one saved post. |
| Change or resume an existing draft | Read [Edit or resume a draft](references/delivery-and-recovery.md#edit-or-resume-a-draft); keep the existing post. |
| Check delivery, find posts, or resolve a failure | Read [Delivery and recovery](references/delivery-and-recovery.md); use status or history without creating a draft. |

Use live tool schemas. If a tool is missing, complete supported preparation and name the gap.
Use `vidiq-video-metadata` for existing YouTube video changes, and `vidiq-video-ideas` or
`vidiq-shorts-inspiration` for discovery when available. Research and new media require that scope.

## Resolve the publication brief

1. Reuse supplied content, tone, destinations, timing, and earlier choices. Resolve missing details
   together. Interpret "everywhere" against connected accounts and show the proposed selection;
   it does not authorize every account.
2. For saved drafts or publication, call `vidiq_social_account_list`. Use exact `platformAccountId`
   values and `canPublish`; resolve multiple accounts before selecting one. A platform in `partial`
   has unknown connection state.
3. For a requested connection, use `vidiq_social_account_connect`, or
   `vidiq_connect_youtube_channel` for YouTube. Show authorization, wait, then re-list accounts.
   Offer reconnection when needed; connecting does not authorize publication.
4. Resolve scheduled dates, local times, and timezone; retain timestamps with offsets. Ask about
   ambiguity rather than inventing a time. A series needs explicit occurrences, not assumed recurrence.
5. Read [Platforms and media](references/platforms-and-media.md) for the selected destinations and
   imports. Retain supplied privacy and platform settings; ask for missing choices.
6. For several posts to one account in a day, especially several YouTube videos, read
   [Pacing and platform limits](references/platform-limits.md) before preparing them.

Keep a working brief with source/library IDs, content, settings and times per account, `postId`,
`publicationId`s, current `revision`, exclusions, and approval. Update it after edits and results:
readback omits some settings and shows media counts, so it cannot reconstruct the full brief.

## Adapt and prepare

Preserve the creator's meaning, voice, and requested exact wording. Adapt to each destination and
the actual asset when requested, using supplied or inspected evidence; explain material changes.

1. Import media once and reuse library IDs, not source URLs, in drafts.
2. Use `vidiq_social_post_draft_create` for one creative post with all its regular destinations:
   common text, media, and timing with destination overrides. Distinct posts need distinct drafts.
3. Inspect every destination's issue, saved state, and `pacing`; `ready` is validation, not
   guaranteed delivery, and `pacing` is advice covered in [Pacing and platform limits](references/platform-limits.md).
   Before any `vidiq_social_post_draft_update`, read [Edit or resume a draft](references/delivery-and-recovery.md#edit-or-resume-a-draft).
   Correct supported issues on the same post. Stop when resolution needs a creator choice or
   external change; explain remaining refusals before proposing fewer destinations.

## Show the exact version for approval

Show each account's final text, identifiable media and order, settings, exact timing and timezone,
quoted cost, and the total. Include unresolved issues and excluded destinations. A quote is not a charge.

Distinguish settings retained in the brief from server-confirmed fields; resolve discrepancies.
A dated draft is only planned. Before scheduling, explain that a scheduled destination can later be
changed or cancelled only by replacing it, as described in [Edit or resume a draft](references/delivery-and-recovery.md#edit-or-resume-a-draft),
and that a published one cannot be changed.

Publish only the saved version the creator has seen and explicitly approved, including destinations,
settings, times, and cost. An initial posting request or status question does not approve a later
draft. Existing approval remains valid for that exact version; "publish these only" narrows it.
Changes to content, settings, time, or cost need renewed review and approval. Prepare before asking.

## Publish and report delivery

Call `vidiq_social_post_publish` with the approved `postId`, `revision`, and explicit `publicationIds`.
Retain exclusions; publish sequentially for the same post. A stale revision requires reading and
reviewing the changed draft, not substituting a fresh token. On `verification_required`, show the
returned step, wait for completion, and resume the same approved call without another content approval.

Read [Delivery and recovery](references/delivery-and-recovery.md) before status checks or retries,
and [Pacing and platform limits](references/platform-limits.md) for any limit failure, including a
YouTube failure that mentions `uploadLimitExceeded`.
Report each destination's actual state, link, and next action. Preserve successful destinations;
distinguish saved drafts, accepted requests, scheduled posts, and confirmed live posts.
