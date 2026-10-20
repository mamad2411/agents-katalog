---
name: kb-notifications
description: Portable notification-system patterns for Next.js apps — modeling categories × channels (in-app / push / email), toast UX rules (when to toast vs persist vs both), the SSE vs polling vs WebSocket decision tree for real-time updates, and user-preference storage shape. Use when designing a notification system from scratch or deciding delivery strategy. For kit-shipped infra (`notify()`, SSE route, UI components) → `sk-notifications`.
last-verified: 2026-04-23
---

# kb-notifications — Portable Notification Patterns

> Portable notification system patterns. Pair: [`sk-notifications`](../sk-notifications/SKILL.md)
>
> Stack-anchored to Next.js (App Router, RSC, Server Actions) but **agnostic to any kit helper**. These patterns apply to any Next.js app; kit-shipped infrastructure (concrete APIs, SSE routes, provider components, Sonner wiring) lives in the paired `sk-notifications`.

---

## 1. Categories × Channels — the core model

A notification system is a matrix of **categories** (what kind of event) × **channels** (how the user receives it). Modeling this explicitly prevents the common drift where every new feature invents its own delivery logic.

| Category (example) | in-app | push | email | Default state                   |
| ------------------ | :----: | :--: | :---: | ------------------------------- |
| `system`           |   on   |  on  |  on   | **forced-on** (cannot disable)  |
| `transactional`    |   on   |  on  |  on   | on by default, user-disableable |
| `behavioral`       |   on   |  on  |  off  | on, email opt-in                |
| `marketing`        |   on   | off  |  off  | opt-in per channel              |

Rules:

- Each `(category, channel)` is a first-class preference.
- `system` (security alerts, password resets, critical account events) is **non-dismissable** by policy — never honor a preference check for it.
- `marketing` must be **opt-in per channel** to stay compliant (CAN-SPAM, GDPR).
- Channel availability is also per-user: a user without a push subscription cannot receive `push` regardless of preference.

---

## 2. Toast UX — when to toast, persist, or both

A common failure mode: teams use toasts as the notification system. Toasts are **ephemeral feedback**, not a history. Separate the two concerns.

| Scenario                                    | Toast? | Persist? | Reason                                          |
| ------------------------------------------- | :----: | :------: | ----------------------------------------------- |
| User clicks "Save" → success                |   ✅   |    ❌    | Immediate feedback for a foreground action      |
| User clicks "Save" → validation error       |   ✅   |    ❌    | Same — inline feedback                          |
| Background job finishes (report, import)    |   ✅   |    ✅    | User may have navigated away; history is useful |
| Another user invites you                    |   ❌   |    ✅    | Not caused by your action — persist only        |
| Critical success (payment captured)         |   ✅   |    ✅    | Both — feedback **and** auditable history       |
| Destructive action confirmation (Undo sent) |   ✅   |    ❌    | Transient, action-bound                         |

Heuristic: **if the user didn't cause it right now, don't toast — persist it.** Toasts interrupt; persisted notifications wait.

---

## 3. Real-time delivery — decision tree

Pick the transport based on the update shape, not developer preference.

```
Is the update user-triggered and local? ─── yes ─► no transport needed (optimistic UI)
             │
             no
             ▼
Is it unidirectional (server → client)?
      │
      ├── yes → frequency?
      │          ├── low (minutes), tolerable delay       → polling (simple, cacheable)
      │          └── medium-high (seconds), low-latency   → SSE (HTTP/1.1, reconnects, trivial)
      │
      └── no (bidirectional, chat/cursors/presence)       → WebSocket
```

Guidelines:

- **Prefer SSE** for notification streams in Next.js — works over standard HTTP, survives proxies, auto-reconnects, and fits the "server pushes events" shape perfectly.
- **Polling is not a failure mode.** For low-frequency updates (unread count refreshed every 60s), polling is simpler, cacheable, and degrades gracefully.
- **WebSockets only when you need the upstream channel** (typing indicators, live collaboration). Otherwise the extra infra cost is waste.

---

## 4. Backpressure & ordering

Notifications fan out. A single domain event can produce N in-app rows + M push deliveries + K emails. Three rules keep this sane:

1. **Server-side timestamps, monotonic.** Never trust client clocks for ordering. Order by `createdAt` (DB-generated) on render.
2. **Dedup key per logical event.** Two identical notifications within a short window collapse to one. Pattern: hash `(userId, type, subjectId)` + debounce window (e.g. 60s). Prevents the "10 toasts for 10 likes in 10 seconds" trap.
3. **Queue, don't fan out in the request path.** Email/push delivery happens out-of-band (job queue, background worker, or at minimum a `setImmediate`/`after()` handoff). Never block a user's Server Action on a 3rd-party email API.

Failure-mode defaults:

- Email/push delivery retries with exponential backoff, max 3–5 attempts, dead-letter after that.
- In-app delivery is **authoritative**: if the row exists in the DB, the user got the notification, regardless of push/email delivery status.

---

## 5. User preference storage — flat wins

Two shapes appear in practice:

**Flat (recommended):**

```
user_notification_preferences
┌─────────┬────────────┬─────────┬─────────┐
│ user_id │ category   │ channel │ enabled │
├─────────┼────────────┼─────────┼─────────┤
│ u1      │ behavioral │ email   │ false   │
│ u1      │ marketing  │ push    │ true    │
└─────────┴────────────┴─────────┴─────────┘
```

**Nested (JSON blob):**

```json
{ "behavioral": { "email": false }, "marketing": { "push": true } }
```

| Dimension                  | Flat                              | Nested JSON                      |
| -------------------------- | --------------------------------- | -------------------------------- |
| Query "who wants email X?" | Indexed scan, fast                | Requires JSON extraction per row |
| Migrate new category       | `INSERT` rows on deploy           | `UPDATE` every user row          |
| Audit trail per preference | Row-level `updated_at` natural    | Needs diff tracking              |
| Bulk ops                   | Trivial (`DELETE WHERE category`) | JSON surgery                     |

Default to **flat**. Reach for JSON only if preferences are deeply hierarchical (per-project, per-channel, per-type) and flat would balloon the row count.

---

## 6. Notification type taxonomy

Give every notification a `type` string with a stable taxonomy. This is what lets the UI render icons, group items, and link to the right surface.

| Bucket          | Examples                                                | Lifecycle   |
| --------------- | ------------------------------------------------------- | ----------- |
| `system`        | `security.login_new_device`, `account.password_changed` | Forced-on   |
| `transactional` | `order.confirmed`, `invoice.paid`, `invite.accepted`    | User-toggle |
| `behavioral`    | `comment.mentioned`, `thread.replied`, `task.assigned`  | User-toggle |
| `marketing`     | `newsletter.weekly`, `product.new_feature`              | Opt-in      |

Naming convention: `<domain>.<event>` in snake_case — stable across code, DB, and analytics. Never couple types to a specific UI component (`type: "red_toast"` is an anti-pattern).

---

## 7. Anti-patterns

```
❌ Calling toast() directly from a deep component
   → Every component now owns toast policy. Use the notification service
     (one entry point) so you can add dedup, logging, or routing later.

❌ Toasting from server code (Server Action / Route Handler)
   → Server code cannot trigger client UI synchronously. Return a result
     shape; the caller decides whether to toast.

❌ Fire-and-forget external delivery inside the request path
   → await resend.send() on a Server Action blocks the user on a 3rd-party
     API. Queue it; return fast.

❌ Bypassing the preference check
   → "Just this one email is important" — no. If it's truly critical it belongs
     to the `system` category (forced-on by policy), not a preference bypass.

❌ Using toast history as notification history
   → Toasts disappear. If the user needs to see it later, it must be persisted.

❌ Per-feature notification tables
   → `comment_notifications`, `invite_notifications`, `order_notifications` —
     one unified `notifications` table with a `type` discriminator. Features
     change; the delivery layer shouldn't.

❌ Client-generated notification IDs or timestamps
   → Ordering breaks under clock skew. Server is the source of truth.

❌ Sending push/email synchronously on every DB write
   → Use a single service entry point that reads preferences, applies dedup,
     and fans out to channels. Don't scatter resend.send() across the codebase.
```

---

Cross-reference: [`sk-notifications`](../sk-notifications/SKILL.md) — kit-shipped infra. [`sk-features-index`](../sk-features-index/SKILL.md) — feature catalog.
