---
name: qa
description: >-
  Exercise a change end-to-end like a user before declaring it done. Trigger
  on "test this", "qa this", or after implementing any user-visible change.
  Drives the real flow (API calls, running app, UI), not just unit tests.
---

# QA

Tests passing is not QA. QA = the real flow behaves correctly.

## Steps

1. From the task's acceptance criteria (or infer them), list the flows to
   exercise: happy path, the main edge cases, and both access tiers where the
   app gates features (anonymous/free vs paid).
2. **Backend**: curl the real endpoints with realistic params; check the JSON
   shape and values, not just 200. Verify error paths return sane errors.
3. **Web**: run the dev server, drive the page (Playwright if available),
   check mobile viewport too (the apps are responsive by policy). Check the
   browser console for errors.
4. **iOS**: build the scheme; run in the simulator when the change is
   UI-visible.
5. **Analytics**: drive the flow and confirm the behaviour events actually
   arrived with the right properties (the events table, the debug log, or the
   tracking service's output). An event that exists in the code but never lands
   is the same as no event.
6. **Localization**: if user-facing strings changed, confirm they went
   through the i18n layer (en/uk/es), not hardcoded English.
7. Record what was actually exercised and what was observed: "verified" means
   you saw it work, with output/screenshot to show.
