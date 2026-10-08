---
name: notification-design
description: "Communicate without annoying. Patterns for in-app alerts, email triggers, push notification copy, and frequency capping. Use when designing notification systems or any touchpoint that competes for attention."
---

# Notification Design

Communicate without annoying.

## How to use

- `/notification-design` Apply notification constraints to this conversation.

## Constraints

### Hierarchy of Interruption (least to most disruptive)
1. Badge/dot (unread indicator)
2. In-app notification center
3. Toast/banner within the app
4. Email digest
5. Individual email
6. Push notification
7. SMS

### Rules
- MUST match urgency level to interruption level. Not everything is push-worthy.
- MUST let users control notification preferences at a granular level
- MUST include an unsubscribe/mute option in every notification channel
- NEVER send the same notification through multiple channels simultaneously
- SHOULD batch low-urgency updates into digests instead of individual messages

### Copy
- MUST be actionable. Tell them what happened AND what to do next.
- Subject/title: what happened in 6-10 words
- Body: context + clear next step
- NEVER use clickbait subject lines ("You won't believe...")
- MUST preview well in notification trays (front-load the important info)

### Timing
- SHOULD respect the user's timezone
- NEVER send non-urgent notifications between 9pm and 8am local time
- MUST implement frequency caps (max notifications per day per user)
- First notification within 24 hours of signup should deliver value, not ask for something

### Anti-Patterns
- Re-engagement emails that say "We miss you" (users don't miss you back)
- Push notifications for marketing content disguised as product updates
- Notification counts that include items the user can't act on
- Sending a notification about a notification preference change
