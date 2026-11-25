---
name: realitygate-audit
description: Audit a codebase for fake, unfinished or unsafe AI-generated code and give it a Reality Score from 0 to 100. Use when the user asks whether their app is production ready, real, finished or safe to launch; asks to audit, review or health-check AI-generated or vibe-coded code; or mentions stubs, TODOs, placeholder or mock data, hallucinated or invented npm packages, leaked API keys, or a Reality Score.
---

# RealityGate audit

Score the project and explain the result in plain language.

1. Run the audit from the project root:

   ```bash
   npx --yes realitygate audit . --md=REALITY-AUDIT.md
   ```

2. Read the terminal summary and `REALITY-AUDIT.md`. Report to the user, in this order:
   - the score and grade in one line, saying it comes from reading the code, not running it;
   - what the "Executed" section shows: which checks actually ran and passed or failed, and
     which are NOT RUN. Never describe a NOT RUN check as passing. If tests or the clean-install
     boot weren't run, offer `audit . --exec`. It runs the project's own commands, so ask first;
   - anything **urgent** first: exposed secrets (R-011, R-012, committed `.env`) mean the user
     must rotate those credentials. Say so plainly and never print secret values;
   - the 3–5 most important findings, each in one sentence a non-programmer understands,
     with `file:line`;
   - the fix plan from the report.

3. Offer to fix the findings, highest risk first, using the `realitygate-fix` skill. Do not start fixing
   without the user's go-ahead.

Rules:
- The score is heuristic. Say "found" rather than "proven broken". A high score means none of
  these patterns were found; it doesn't mean the product is correct.
- Never read `.env` files. The audit detects them by name only.
- If the command exits with "no source files found", tell the user which directory you
  scanned and ask where the code lives. Don't report a score.
