---
name: write-ticket
description: >-
  Create or refine one Feature, Tweak, Bug, or Refactor ticket in Linear or GitHub.
  Grills intent, analyzes the codebase, drafts an approved body and metadata,
  then writes it. Use for tracker tickets, never inside /goal.
disable-model-invocation: true
---

# Write Ticket

**Variants:** [../pack-shared/variants.md](../pack-shared/variants.md) — standalone-only. If flow is requested, use the no-flow message.

**Read:** [doctrine.md](doctrine.md) · [reference.md](reference.md) · **Ask style:** [../pack-shared/asking.md](../pack-shared/asking.md)

**Standalone only.** This skill writes a tracker ticket; `/trackers` reads and `/analyze` researches. Open ticket grills use the documented freeform exception in the doctrine.

## Process

1. Load an existing ticket or seed a new one.
2. Lock Feature, Tweak, Bug, or Refactor.
3. Run the type-specific open grill.
4. Run `/analyze` on the grilled brief.
5. Announce the principle-level solution when applicable.
6. Show the complete draft, lock metadata, and write only after approval.

Question suites, body templates, tracker fields, and failure handling live in the reference and doctrine.
