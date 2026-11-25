---
name: redact-and-ask
description: Restate a question so it can be answered without the identifiers, then apply the answer to the real case.
version: 1
pins: none
---

# Ask without giving away the case

Some questions are general even when the material is not. "Can this deadline be
extended?" does not need a name to be answered.

## Method

1. **Separate the question from the case.** Write the question as it would
   appear in a textbook: roles instead of names, durations instead of dates,
   categories instead of identifiers.
2. **Check what remains.** Read your restatement as a stranger. If it still
   identifies a person, an organisation or a matter — directly or by
   combination — restate it again. A rare condition plus a small town is an
   identifier.
3. **Answer the general question**, or let it be answered elsewhere.
4. **Apply the answer to the actual case yourself**, here, with the real values.

## Output

```
GENERAL     <the question, with nothing identifying>
WHY IT IS SAFE  <one line: what you removed and why what is left cannot identify>
ANSWER      <the general answer>
APPLIED     <the answer as it applies to this specific matter>
```

## Rules

- Never restate a question by shortening it. Removing context is not
  de-identification; replacing specifics is.
- If the question cannot be asked generally — because the answer depends on the
  identity — say so and stop. That is a correct outcome, not a failure.
- The runtime may also redact mechanically before anything crosses. This skill
  is the reasoning half; neither replaces the other.
