---
name: feedback-capture
description: Capture one localization-feedback item (correction, gap, friction) tied to a named Polymath surface — 180d TTL, evaluated later via feedback-digest; not a general note-taker.
---

# feedback-capture

> Localization improves only if the moments where it failed are written
> down. Capture them sparingly and precisely — a noisy feedback store is
> worse than none, because nobody digests it.

## When to use

- The user explicitly corrected output that a Polymath skill/workflow
  produced ("no, our convention is X", "that went to the wrong board").
- A surface clearly lacked project knowledge it should have had
  (`conventions_docs`, `skill_overrides`, routing signals).
- Recurring friction with a localized behavior, confirmed by the user.

Not for: style preferences stated once, your own uncertainty, anything the
user hasn't confirmed as wrong, or general TODOs. When in doubt, don't
capture — conservative is the contract.

## Procedure

1. **Qualify.** Capture only if all three hold: (a) tied to a *named*
   surface (`<plugin>:<skill>`, a workflow name, or `direct`), (b) the
   user confirmed the behavior was wrong or missing, (c) a localization
   fix is conceivable (conventions doc, `skill_overrides`,
   `route-signals.project.json` — or a catalog change).
2. **Strip secrets.** The note must contain no credentials, tokens, or
   personal data — describe the behavior, not the payload.
3. **Record one item per distinct issue:**

   ```bash
   "${POLYMATH_PLUGIN_ROOT}/bin/polymath-pipeline" feedback capture \
     --surface <plugin>:<skill> --kind correction|gap|friction|praise \
     --note "<what happened, one screen max>" \
     --evidence "<artifact/run path that shows it>"
   ```

4. Tell the user it was captured (id + that `feedback-digest` evaluates
   it later). Items expire after 180 days — feedback is perishable.

## Quality bar

- Named surface, user-confirmed, fix conceivable — all three, or no capture.
- One capture per distinct issue; no duplicates of an open item (check
  `feedback digest` if unsure).
- Note readable by someone without this conversation's context.
