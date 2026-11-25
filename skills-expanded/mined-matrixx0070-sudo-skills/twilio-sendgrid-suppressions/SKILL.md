---
name: twilio-sendgrid-suppressions
version: 1.0.0
description: Manage SendGrid suppressions — global unsubscribes, bounces, blocks, spam reports, invalid emails, and unsubscribe groups — to protect reputation and honor opt-outs.
author: matrixx0070
tags: [sendgrid, suppressions, unsubscribe-groups, bounces, blocks, spam-reports, list-hygiene]
capabilities: []
---

## When to use

Use this when you need to see or change who SendGrid will not send to — reviewing bounces/blocks, honoring unsubscribes, cleaning a list, or wiring unsubscribe groups (subscription preferences) into your mail.

**Not for:** account-wide tracking/footer behavior (see `twilio-sendgrid-email-settings`) or reacting to the events that create suppressions (see `twilio-sendgrid-webhooks`).

## Method

1. Know the suppression types and which are yours to clear. Global unsubscribes and spam reports are recipient choices — respect them, do not silently re-add. Bounces, blocks, and invalid emails are deliverability signals you may clean after investigation.
2. Read before you write: `GET /v3/suppression/{bounces,blocks,spam_reports,invalid_emails}` and `GET /v3/asm/suppressions/global`. Understand why an address is suppressed (the `reason`/`status` field) before removing it.
3. Remove only with cause. Delete a bounce/block suppression only after the underlying issue is fixed (e.g. a full mailbox cleared, a typo'd domain corrected). Deleting a hard bounce so you can re-send to a dead address damages reputation.
4. Use unsubscribe groups (ASM) for preference management. Create groups via `/v3/asm/groups`, then set `asm.group_id` and `asm.groups_to_display` in the send payload so recipients unsubscribe from a category, not everything.
5. Honor group and global unsubscribes automatically — SendGrid drops sends to suppressed addresses; do not fight this by scrubbing suppressions.
6. Never delete global unsubscribes or spam reports to re-engage. That is both a reputation and a compliance failure.
7. Reconcile with your own database from webhook events so your app-side state matches SendGrid's.

## Example

Inspect a bounce and remove it only after confirming a transient cause:

```bash
# Why is this address bouncing?
curl -sS "https://api.sendgrid.com/v3/suppression/bounces/user@example.com" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
# -> {"reason":"550 mailbox full","status":"4.2.2"} => transient

# Mailbox since cleared: remove the suppression
curl -sS -X DELETE "https://api.sendgrid.com/v3/suppression/bounces/user@example.com" \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

## Pitfalls

- **Clearing hard bounces to re-send.** A `5.1.1 no such user` is permanent. Removing it and resending spikes bounce rate and can get you throttled or blocked.
- **Deleting global unsubscribes/spam reports.** These are opt-outs; removing them to re-contact is a compliance violation and a fast track to blocklisting.
- **No unsubscribe groups.** A single global unsubscribe loses the whole recipient; groups let them mute one category and keep the rest.
- **Suppression state drift.** If your DB does not track suppressions, you keep queuing mail that SendGrid silently drops. Sync from webhook events.
- **Bulk-deleting without reading reasons.** The `reason`/`status` tells you transient vs permanent; deleting blind reintroduces bad addresses.

## Output format

```
# Suppressions: <account/list>
TYPES REVIEWED: bounces=<n> blocks=<n> spam_reports=<n> invalid=<n> global_unsub=<n>
ASM GROUPS: [<id: name>] applied via asm.group_id
ACTIONS: removed=[<addr: transient reason>] kept=[<permanent/opt-out>]
COMPLIANCE: global_unsub & spam_reports untouched
SYNC: app DB reconciled from events
```

## Reference

- Suppression endpoints: `/v3/suppression/bounces`, `/v3/suppression/blocks`, `/v3/suppression/spam_reports`, `/v3/suppression/invalid_emails` (GET/DELETE per address).
- Global unsubscribes: `/v3/asm/suppressions/global`. Unsubscribe groups: `/v3/asm/groups` and `/v3/asm/groups/{id}/suppressions`.
- Send integration: `asm: { group_id, groups_to_display }` in the Mail Send payload wires preference-based unsubscribe.
- Deliverability: suppression hygiene is core to sender reputation — honoring opt-outs and pruning hard bounces keeps complaint and bounce rates low, which is what receivers score.
