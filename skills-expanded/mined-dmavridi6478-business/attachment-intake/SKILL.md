---
name: attachment-intake
description: Use this skill whenever an uploaded attachment (zip, photo batch, document, export, etc.) arrives with no accompanying instruction, or with an instruction that doesn't clearly relate to what the file actually contains. Covers how to inspect the file, ask a grounded clarifying question instead of guessing at intent, and handle mismatched or off-topic answers without force-fitting them.
---

## When to use this skill

- A file is uploaded with no message, or a one-line reference and nothing else.
- The accompanying message doesn't logically connect to the file's contents
  (e.g. a photo zip paired with an unrelated instruction like "set up
  skills").
- A batch of personal photos, exports, or other files arrives and it's
  unclear whether they should be committed, analyzed, or just described.

## How to use this skill

Follow `docs/procedures/attachment-intake.md` in this repo (or the
equivalent procedure if this skill has been copied elsewhere):

1. Inspect the file's actual contents first (list a zip, check type/size) —
   don't extract, commit, or deeply process anything yet.
2. Ask one structured clarifying question with 2-4 options grounded in what
   the file actually contains, not generic ones. Recommend a default when
   reasonable.
3. If the user's answer doesn't connect to the file, ask a second targeted
   question naming the mismatch explicitly — don't silently reinterpret or
   force-fit an unrelated answer onto the file.
4. Once intent is confirmed, act minimally — only the approved action,
   nothing extra.
5. Default to *not* committing raw personal photos/media into git history
   without explicit confirmation; prefer in-session use or non-versioned
   storage.
6. If the user has already set a standing preference for this kind of
   attachment in the current session, apply it without re-asking.

## Keywords
attachment, upload, zip, photo batch, iCloud Photos, unclear intent, ambiguous request, clarifying question
