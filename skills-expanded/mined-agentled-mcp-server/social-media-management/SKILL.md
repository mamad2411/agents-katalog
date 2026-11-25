---
name: Social Media Management
version: 0.4.1
description: Draft, approve, and prove bounded social media work through existing AgentLed services.
category: social-media
allowedApps: browser-use, openai, instagram, linkedin
allowedActions: browser-use.extract-data, openai.generate-image, instagram.create-media-post, instagram.list-recent-media, instagram.get-media-insights, linkedin.create-post-organization, linkedin.get-post-metrics
relevanceKeywords: social media, instagram, linkedin, organization post, page post, content, caption, alt text, approval, permalink
---

# Social Media Management

Use this skill as a Markdown router for named social-media Jobs. It provides operating guidance only: listing or recommending an app or action grants no permission or authority. Invoking `openai.generate-image` can spend credits. Invoking `instagram.create-media-post` or `linkedin.create-post-organization` can publish. Those actions remain governed by existing AgentLed credit/spend and approval policies. If an active action, schema, or durable receipt capability is unavailable or incompatible, return a partial result, identify the missing runtime evidence, and stop.

Host integration is separate from the Job: the AgentLed adapter assigns the Workspace Skill; Hermes installs and loads the portable skill and uses AgentLed authority. Neither host path grants permission, credentials, account connection, approval, billing, publication, or routine activation. Verify that only the capabilities required by the selected Job are available before it proceeds.

The first Job requires an exact public 1080x1350 JPEG and a strict normalized `instagram.create-media-post` input containing `accountId`, `mediaUrl`, `caption`, `altText`, `imageProfile=instagram_post_portrait`, `mediaType=IMAGE`, and any connection selector present. Before connection, make exactly one `openai.generate-image` attempt; do not retry automatically, and another generation attempt requires explicit user authorization. Durable receipt states record the attempt; any input or destination change invalidates approval, and an ambiguous result must never invite an automatic retry. After connection, use one bounded recent-media page and an explicit sample of at most three returned media IDs or permalinks for media-product insights. Revise the candidate only when that evidence changes the recommendation. If `instagram_manage_insights` or analytics evidence is unavailable, preserve the grounded draft, report the gap, and do not block the first approved static post or request comments/moderation scope solely for analytics.

The LinkedIn organization Job prepares a useful approval packet before connection or public write access. It starts from a verified source or product insight, revalidates drift-prone claims, and requires an exact organization actor, organization ID, Page URL, current human administrator identity, proposed publication time and timezone, and brand input. Its executable write uses the active strict `linkedin.create-post-organization` input with `organizationId`, `text`, `mediaUrl`, and any active connection selector. A separate alt text companion draft remains part of the reviewed packet, but the current organization-post action does not accept or transmit the companion alt text draft; never claim that it did. Proof requires `postUrl`, `postId`, `actorUrn`, and matching organization identity from one unambiguous result.

For the first-session LinkedIn path, research a verified company or product source and produce the organization-post draft in chat before requesting any connection. Only after the user explicitly chooses to publish, create or reuse one small manual workflow with exact post text, organization actor, and optional media as run inputs; asking for a draft or revision alone must not create workspace state. The only reusable external action is `linkedin.create-post-organization`, and it must retain exact-payload approval for the actor, destination, text, and media. Do not publish during setup or testing. Do not create a cross-channel package, routine, schedule, or automatic run.

## Jobs

- **Create an Instagram post** — implemented in v0.2. Read `references/jobs/create-instagram-post.md`.
- **Prepare a LinkedIn organization post** — implemented in v0.3. Read `references/jobs/prepare-linkedin-organization-post.md`.
- **Review Instagram comments** — named follow-up Job; not implemented in v0.
- **Refresh a social content calendar** — named follow-up Job; not implemented in v0.

For an implemented Job, read its channel reference and the proof/approval reference before taking any action. Keep customer context, permissions, connections, approvals, receipts, billing, and recurrence in the existing AgentLed services. **Make this weekly** is offered for Instagram only after one unambiguous public result has both a public permalink and external media ID. **Make this twice weekly** is offered for a LinkedIn organization only after one unambiguous result has a public permalink and matching organization identity. Claim **Paused recurrence** only from an authoritative existing paused routine record; this skill does not automatically configure or activate a routine.
