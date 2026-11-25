---
name: plan-feature
description: "Plans a feature before any code is written: files to touch, ordered steps, risks and the exact checks that prove it works."
disable-model-invocation: true
---

Plan this feature without writing code: $ARGUMENTS

1. Restate the goal in two sentences and list what is out of scope. If the request is ambiguous, ask up to three questions first and wait.
2. Explore: find the closest existing feature, read its entry points, data model, tests and routes. Note naming and layering conventions.
3. Produce the plan:
   - **Files**: each file to create or change, with one line on why.
   - **Steps**: ordered, each small enough for one commit, each leaving the build green.
   - **Data and API changes**: schema, migrations, contracts, feature flags.
   - **Risks**: what could break, who depends on it, what is irreversible.
   - **Verification**: tests to add, commands to run, and a manual check.
4. Name one simpler alternative and why you did not pick it.

Keep the plan under one page. End with "Approve this plan, or what should change?" Do not edit any file or run migrations before approval.
