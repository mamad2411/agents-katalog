---
name: snap-prd
description: >
  Turn current context, source references, and repo understanding into a
  complete product-grade PRD published as a GitHub issue. Use when the user wants
  to spec a feature, formalize requirements, or create an implementation-ready
  product document.
---

Take the current conversation context and codebase understanding and produce an implementation-ready PRD as a GitHub issue.

## Process

1. Work from whatever is already in the conversation. If the user passes a GitHub issue, comment, PR, doc, URL, or path, fetch the body, comments, or content needed to understand it.

2. Explore the repo to understand the current state of the codebase, if you have not already. Use the project’s domain vocabulary throughout the PRD, and respect ADRs, tests, interfaces, and prior art in the area you are touching.

3. Sketch the major modules you will need to build or modify for the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

   A deep module, as opposed to a shallow module, encapsulates a lot of functionality behind a simple, testable interface that rarely changes.

   Check with the user that these modules match their expectations. Check which modules they want tests written for.

4. Before writing, resolve only PRD-changing decisions with the user. Show a small decision checkpoint: proposed title, 3-5 key product decisions, module shape, and tests to write. Wait for approval.

5. Write the PRD using `references/template.md`, create one GitHub issue with a `[PRD]` title prefix, assign it to the invoking GitHub user (`--assignee @me` when using `gh issue create`), and show the URL.
