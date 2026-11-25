---
name: poll-schema-designer
description: "Designs Firestore collections, security rules, and composite indexes for polling, voting, and feedback applications under Firebase Anonymous Auth. Triggers on requests like: design poll schema, firestore rules for polls, vote collection, feedback data model, anonymous auth, workshop polls, polling app schema, voting database, survey schema."
---

# Poll Schema Designer

You produce three artefacts in a single response:

1. `backend/firestore.schema.md` — collection tree with field types and required fields.
2. `backend/firestore.rules` — security rules tuned for **Firebase Anonymous Auth**.
3. `backend/firestore.indexes.json` — composite indexes for common queries.

## Canonical collections

```
workshops/{workshopId}
  name: string
  date: timestamp
  createdBy: string (uid)        # workshop admin
  createdAt: timestamp
  /polls/{pollId}
    title: string
    type: "single" | "multi" | "open"
    options: array<string>       # empty for "open"
    order: number
    createdAt: timestamp
    /votes/{voteId}              # voteId === request.auth.uid (uniqueness)
      userId: string (uid)
      value: string | array<string>
      openText: string?
      createdAt: timestamp
```

**No `users/` collection in the default flow.** Anonymous uids do not need a
profile doc. If a Google SSO upgrade is later added (homework), it is
backwards-compatible — Google-signed users are still `request.auth != null`.

## Auth model

The app uses **Firebase Anonymous Auth** by default:
- Every visitor is `signInAnonymously()` on app load.
- An admin = the user who created the workshop (`createdBy == request.auth.uid`).
- No custom claims, no role lookups.

## Security rules baseline

Reads:
- `workshops/{w}`: any signed-in user.
- `polls/{p}`: any signed-in user.
- `votes/{v}`: workshop owner reads all; voter reads only their own.

Writes:
- `workshops` create: any signed-in user; must set `createdBy == request.auth.uid`.
- `workshops` update/delete: only `createdBy == request.auth.uid`.
- `polls` create/update/delete: only the parent workshop's `createdBy`.
- `votes` create: any signed-in user; **enforce `voteId == request.auth.uid`**
  for one-vote-per-user (cheaper than `exists()`).
- `votes` update/delete: never.

## Indexes (mandatory)

- `votes` collection group: `(pollId asc, createdAt asc)` — stats queries.
- `polls`: `(workshopId asc, order asc)` — ordered render.

## Output format

Always return the three files in fenced code blocks with explicit paths, in the
order: schema → rules → indexes. Never produce code outside these three artefacts
when this skill is active.

## See also

- `references/rules-snippets.md` — copy-pasteable rule fragments (already
  anonymous-auth-friendly; uses `voteId == request.auth.uid` trick).
- `scripts/validate_rules.sh` — quick lint via `firebase emulators`.
