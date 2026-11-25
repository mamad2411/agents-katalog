---
name: intent
description: Turns a request (message, note, idea) into an issue an agent can work from (user story, error behaviours, definition of done, testable acceptance criteria, axis labels), following the Belayline harness. Use before any work that does not yet have a clear issue.
argument-hint: "<request in one sentence>"
---

# Define the intent

Request: $ARGUMENTS. Reference: `.harness/docs/METHODOLOGY.md` §2 (otherwise `${CLAUDE_PLUGIN_ROOT}/docs/METHODOLOGY.md`).

1. **Duplicates** first: issues and PRs, open and closed. One exists → complete it rather than create another.
2. Write, in the project's language:
   - `### Summary`: "As <who>, I want <X> to do <Y>, so that <benefit>";
   - `### Error behaviours`: each invalid input, external failure, limit, with the expected result (message, code,
     state kept); "none" must be justified;
   - `### Acceptance criteria`: Given / When / Then, each verifiable by a test;
   - `### Definition of done`: tests (written first, seen red), docs updated, review by another model, compliance if
     the scope requires it, what will be validated on the device;
   - `### Out of scope` and `### Sources` (nothing guessed).
3. Labels: type, priority, status, and difficulty if the project has that axis (prefixes: `.harness/config.json` →
   `labels`, METHODOLOGY §4); `status: needs-decision` + the exact question if a product decision is missing.
4. **Show the text to the operator before creating the issue**; after approval, create it and give the link.
