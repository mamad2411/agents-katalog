---
name: credential-incident
description: >-
  Use the moment a live credential is in front of you — in a log, a body, a
  transcript, a screenshot — or one has been posted to GitHub.
metadata:
  author: Spool maintainers
---

# /credential-incident — a live credential in front of you

*Moved verbatim from `docs/CONVENTIONS.md` (#470), which keeps the one-line rule
and points here. The rule binds whether or not this skill is loaded.*

**A live credential in front of you is an incident.** Stop; do not copy it
anywhere; redact it where you can still reach it; tell the operator privately.
The value and the steps that reproduce it never go in the group — that an
exposure happened does, because everyone's evidence may carry it. The operator
rotates. Whoever found it files the code issue with the value redacted — the fix
is public work, the exposure is not.

**An issue or comment body is redacted, not rejected**: text posted to GitHub
is published before anything can run, so the redaction guard in the `issue-guards` workflow edits
the value out and posts what the edit does not fix — the revision history
still holds the original, and rotation is not optional. Who deletes the
revision depends on who pasted it: a person does it themselves, from the
`edited` menu; a loop cannot, because edit history is read-only in both
APIs, so it reports the exposure privately to the operator — what and
where, never the value — and the operator deletes it (#206). Both guards
read their shapes from `scripts/secret-rules.awk`; two of those shapes —
a loop's bot handle and the group's chat id — apply to bodies only, since
in the tree they are configuration and fixture data rather than a quote of
the group (#249).
