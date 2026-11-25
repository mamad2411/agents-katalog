---
name: consent
description: Guardian sign-off for CHILD/TEEN users — SAFE protocol session authorization
---

@markdownai v1.0

# /consent — Guardian Sign-Off

Use when USER says "approve [name] for today" or "sign off on [name]'s session".

## Sequence

1. **Identify user** — extract name from USER's message. Look up in `willow/users/` via `soil_search`.
2. **Check role** — load user profile. If role is `adult`, no guardian authorization needed — inform USER.
3. **For CHILD/TEEN users — present authorization checklist**:
   ```
   Guardian sign-off for: <name> (<role>)
   Session date: <today>

   Authorize (yes/no):
   [ ] Relationships stream
   [ ] Images stream
   [ ] Bookmarks stream

   Training data consent: no (default — cannot be changed for CHILD users)

   Type "approved" to confirm, or specify which streams.
   ```
4. **On confirmation** — write to store via `soil_put`:
   ```json
   {
     "collection": "willow/guardian_approvals",
     "record": {
       "id": "approval-<name>-<YYYYMMDD>",
       "user_id": "<id>",
       "guardian_id": "sean",
       "date": "<today>",
       "streams_authorized": ["relationships", "images"],
       "training_consent": false,
       "expires": "session"
     }
   }
   ```
5. **Confirm** — "Session authorized for <name>. Expires at session close."

## Rules

- Identity is never inferred from behavior. If the user isn't in `willow/users/`, stop and ask USER to create a profile first.
- Training consent for CHILD users is always false regardless of what USER says. Platform hard stop HS-001.
- Authorizations expire when the Stop hook fires. Never carry them across sessions.
