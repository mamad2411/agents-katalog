---
name: write-sunset-notice
description: Author a deprecation / sunset notice — two dates (warn, remove), concrete migration with before/after code, exception path, FAQ.
---

# write-sunset-notice

> A sunset notice is two dates and a migration. Anything else is decoration. The reader needs to know what to do and by when.

## When to use

- A capability (API endpoint, feature, integration) is being deprecated.
- A library version is going end-of-life.
- A workflow's sunset step needs structured user-facing content.

## Inputs

- The capability being sunset (required).
- Sunset date (when warnings appear / new usage blocked).
- Removal date (when the capability stops working).
- The replacement (required — sunset without a replacement is just removal, write that differently).

## Procedure

1. Read [`Sunset-notice.md`](../../templates/Sunset-notice.md).
2. Compute slug from the capability name.
3. Draft `docs/sunsets/<slug>.md`:
   - **What's being sunset**: one sentence in the user's vocabulary.
   - **When**: today's deprecation warning + sunset date + removal date. All three.
   - **Why**: one paragraph, honest. "We're refocusing" beats "tech debt".
   - **What you should do**: before/after code example. The only section that matters for most readers.
   - **What replaces it**: the supported alternative + one-line comparison.
   - **Out of scope**: what's *not* changing (calms the readers who feared more).
   - **Exception / extension path**: how to request more time.
   - **FAQ**: the 3 hardest questions, answered.
4. Surface this with at least the standard sunset window (60–90 days for most capabilities; 6+ months for paid integrations).

## Quality bar

- Two dates: sunset (warning) and removal (stop working). Both must exist.
- Before/after code or config example present.
- A replacement is named. If there's no replacement, the doc is a removal-notice, not a sunset-notice — rewrite accordingly.
- Exception path documented.

## Output

- File: `docs/sunsets/<slug>.md`.
- Summary: capability + sunset date + removal date + replacement.

## Anti-patterns to avoid

- "We're sunsetting X" without a removal date. Open-ended deprecations rot.
- Sunset notice without a replacement. That's a removal, not a sunset.
- "Why" section that's "tech debt cleanup". Customers don't care about your debt; explain the user-impacting reason.
- No FAQ. Readers will have questions; better to answer the ones you anticipate.
