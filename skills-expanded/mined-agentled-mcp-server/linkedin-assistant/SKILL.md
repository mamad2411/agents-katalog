---
name: linkedin-assistant
version: 0.1.1
description: Use when tracking LinkedIn activity, connection quotas, replies, meetings, follow-ups, or approval-ready LinkedIn actions in AgentLed.
category: outreach
relevanceKeywords: linkedin,connections,follow-up,reply,meeting,quota,approval,outreach
---

# LinkedIn Assistant

## Purpose

Use this skill to maintain a LinkedIn operating ledger in AgentLed and to prepare actions that a human or approved executor can run later. The skill is for tracking, classification, drafting, quota control, and approval preparation. It is not permission to send LinkedIn messages, connection requests, InMail, email, WhatsApp, provider campaigns, CRM writes, or public posts.

## Source Of Truth

Resolve the target workspace, use case, and operating workflow before reading or changing LinkedIn state:

```bash
agentled --workspace <workspace> workflows get <workflow-id> --format json
agentled --workspace <workspace> use-cases get <use-case-key> --format json
```

Read every operating guide listed in `useCaseContext.useCase.operatingGuides` before making state changes.

Identify the workspace's lists for active people, follow-up actions, activity events, daily quota, archived contacts, and campaign-session deduplication from those guides. Do not assume personal workspace aliases, UUIDs, or list keys.

## Timestamp Contract

Do not let timestamp fields drift into vague "Date" semantics.

- Row `createdAt` and `updatedAt` are AgentLed storage metadata. They mean when the KG row was inserted or changed.
- `rowData.occurredAt` is the timestamp used for activity chronology. It must describe the LinkedIn lifecycle event time when that time is visible or explicitly confirmed.
- If the exact LinkedIn event time is not known and the event was only observed or flagged by the user, `occurredAt` may be the observed/flagged time, but the row must also include `timestampType: "observed_at"` and a short `timestampNote`.
- If only a calendar date is known, use local midnight for that date and include `timestampPrecision: "date"` plus a note.
- Person fields such as `connectionSentAt`, `connectedAt`, `messageSentAt`, `replyReceivedAt`, `meetingScheduledAt`, and `meetingDoneAt` are lifecycle timestamps. Leave them blank unless there is visible LinkedIn evidence or explicit user confirmation.
- `lastSentAt` is the latest outbound LinkedIn touch for the person, including connection requests, first messages, and follow-ups. Store `lastSentType`, `lastSentAtType`, and a short `lastSentAtNote` when the timestamp is observed/imported rather than verified from LinkedIn.
- `lastReplyAt` is the latest inbound LinkedIn reply from the person. Store `lastReplyAtType` and a short `lastReplyAtNote` when the exact LinkedIn receive timestamp is not visible.
- `messageSentAt` and `replyReceivedAt` can keep a specific lifecycle milestone, but reports and follow-up decisions should use `lastSentAt` and `lastReplyAt` once those fields exist.
- `lastActivityAt` may point to the latest verified or observed activity, but do not use it as a replacement for `lastSentAt` or `lastReplyAt`. Add `lastActivityAtType` when it is not a verified LinkedIn event timestamp.
- `capturedAt` or row `createdAt` can be used to explain when AgentLed learned about the event.

Example: if an activity row has an `occurredAt` later than its row `createdAt`, the report date is the observed or flagged activity time. It is not the KG insertion time and is not automatically a verified LinkedIn message receive timestamp.

## State Machine

Use one current person state unless the contact is archived:

- `prospect`: not contacted yet.
- `connection_sent`: request or note sent, waiting for acceptance.
- `connection_accepted`: accepted/connected, first post-acceptance note due.
- `first_message_sent`: first message sent, waiting for reply.
- `follow_up_due`: follow-up action is due.
- `reply_received`: contact replied; classify topic and decide response/meeting/archive.
- `meeting_scheduled`: call or meeting scheduled.
- `meeting_done`: meeting happened; classify interest and next step.
- `task_required`: non-message work is needed before messaging.
- `archived` or `closed`: no active follow-up.

## Action Queue Contract

Every open item in the discovered follow-up queue should be actionable without guessing:

- `fullName`
- `linkedinUrl`
- `personKey`
- `campaignKey`
- `sourceThreadId`
- `actionType`
- `reason`
- `priority`
- `dueAt`
- `lastSentAt` and `lastReplyAt` when known
- `approvalRequired`
- `draftMessage` when a draft exists
- `timestampEvidence` or timestamp note when dates are ambiguous

Expected `actionType` handling:

- `profile_review`: open the profile and classify fit; do not send.
- `check_acceptance`: verify whether LinkedIn shows accepted/connected; update state only with evidence or user confirmation.
- `send_first_note`: draft or prepare a post-acceptance message approval; do not send.
- `draft_follow_up`: draft a follow-up approval; do not send.
- `reply_needed`: classify reply topic and draft/prepare a response or meeting action; do not send.
- `schedule_meeting`: prepare scheduling text or a calendar task; do not book without approval.
- `prepare_asset`: build the requested asset/report before any message.
- `manual_review`: inspect and propose the next safe state.
- `archive`: move closed/dead/no-fit contacts out of the active queue.

Approval execution cards should preserve the LinkedIn URL and expose an `Open profile` action when a URL is available.

## Quota And Evidence Rules

- Read the discovered daily-quota list before preparing new connection or message actions for the current day.
- Historical sync rows are audit evidence only; they do not reserve today's quota.
- Only count a send after the send is visible in LinkedIn or explicitly confirmed by the user.
- Do not mark `connection_requested`, `first_message_sent`, `follow_up_sent`, `reply_received`, `meeting_scheduled`, or `meeting_done` from a draft alone.
- Keep all source thread IDs and campaign keys so GTM, VC, event, and personal networking sessions dedupe against the same personal ledger.

## Safe Automation Boundary

Allowed without additional approval:

- Read LinkedIn-related KG rows.
- Read operating guides and use-case context.
- Classify contacts, topics, replies, and state.
- Draft messages.
- Update AgentLed KG rows to reflect observed/user-confirmed state.
- Create approval-ready action objects.
- Archive dead/no-fit contacts when the user asked to close them.

Requires explicit recipient/action approval:

- Sending a LinkedIn connection request, DM, follow-up, or InMail.
- Marking a drafted message as sent.
- Booking or confirming a meeting.
- Triggering an external provider or enrichment that spends credits.
- Publishing content.

## Common Mistakes

- Treating the report column `Date` as KG `createdAt`.
- Treating an observed/flagged chat time as the exact LinkedIn reply receive time.
- Collapsing outbound sends and inbound replies into `lastActivityAt` instead of maintaining `lastSentAt` and `lastReplyAt`.
- Updating quota when a draft is approved but not actually sent.
- Leaving dead/no-fit contacts active instead of archiving.
- Dropping LinkedIn profile URLs from approval cards.
- Updating one campaign workspace without mirroring connection-sent-or-later lifecycle state into the personal ledger.
