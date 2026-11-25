---
name: evidence-pack
description: Assemble an answer together with everything needed to audit how it was produced.
version: 1
tools: [document_reader]
pins: local
---

# The answer, and how it was reached

For work that will be defended — to a client, a regulator, a counterparty — the
answer is half the deliverable.

## Method

1. **State the answer** first, plainly, in one paragraph.
2. **List every source** used: file, and the part of it that matters. A source
   you read and did not use is worth listing as read-and-not-used.
3. **List the steps**, in the order they happened: what was read, what was
   derived, what was assumed.
4. **State the assumptions** separately from the findings. An assumption that
   turns out to be wrong should invalidate a conclusion visibly, not silently.
5. **Name what would change the answer.**

## Output

```
ANSWER      <one paragraph>
SOURCES
  - <file> · <what it contributed>
STEPS
  1. <what was done>
ASSUMPTIONS
  - <assumption> · <what happens to the answer if it is false>
WOULD CHANGE THIS
  - <fact or document that would alter the conclusion>
```

## Rules

- Never cite a document you did not read in this run.
- Distinguish "the document says" from "it follows that". The first is a quote,
  the second is your reasoning and belongs in STEPS.
- The runtime keeps its own record of where each step ran and what crossed;
  `annona audit` prints it. This skill covers the reasoning, not the placement.
