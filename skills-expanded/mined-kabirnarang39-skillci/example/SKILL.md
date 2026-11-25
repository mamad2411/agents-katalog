---
name: example-skill
description: Writes a single changelog entry summarizing a code change, given a short description of what changed.
---

Given a short description of a code change, write one changelog entry
in the "type: summary" format (e.g. "fix: correct off-by-one in
pagination"). Pick the type from feat, fix, docs, refactor, test, or
chore based on what the change actually does. Keep the summary under
twelve words, written in the imperative mood, and never end it with a
period.

If the description doesn't describe an actual code change — a
question, a status update, unrelated small talk — say so plainly
instead of inventing a changelog entry.
