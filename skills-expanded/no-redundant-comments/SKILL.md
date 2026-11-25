---
name: no-redundant-comments
description: >-
  Remove code comments that just restate the code, and keep the ones that explain
  why. Use this WHENEVER you write or edit code in any language. Comments like
  "// increment i", "// loop over the items", "// constructor", "// return the
  result", and a docstring that repeats the function name in English are noise
  that signals machine-generated code and rots as the code changes. Keep comments
  that explain intent, a non-obvious reason, a tradeoff, a caveat, or a link to
  context the code cannot show. Delete the narration.
---

# No redundant comments

Good code already says what it does. A comment that restates the next line in
English adds nothing, doubles the maintenance surface, and is a classic tell of
generated code, where every line gets a dutiful narration. The comments worth
keeping explain what the code cannot: why this approach, why this odd value, what
breaks if you change it.

The rule: comment the why, not the what. If the comment just translates the code
into a sentence, delete it.

## Delete these

```js
// increment the counter
counter++;

// loop over each user
for (const user of users) { ... }

// return the total
return total;

// set name to the given name
this.name = name;
```

Also delete:

- section banners that restate structure: `// Constructor`, `// Getters`,
  `// Helper functions`
- a docstring that only repeats the signature: `/** Gets the user. @param id the
  id @returns the user */` over `getUser(id)`
- commented-out old code left "just in case" (that is what version control is for)
- TODOs with no content: `// TODO: fix this`

## Keep these

```js
// Stripe rounds half-up; mirror that here so totals reconcile.
const cents = Math.round(amount * 100);

// The API caps page size at 100; larger values are silently truncated.
const pageSize = Math.min(requested, 100);

// Intentionally not awaited: fire-and-forget metrics, must not block the response.
void reportMetric(event);

// Workaround for facebook/react#1234, remove once the fix ships.
```

Keep comments that carry: intent, a non-obvious constraint or magic number, a
deliberate tradeoff, a warning about a sharp edge, or a link to an issue or spec.

## Prefer better names over comments

Often the fix is not a comment at all. If you reach for `// check if the user can
edit`, a function named `canEdit(user)` says it in the code and cannot fall out of
date. Rename and restructure first; comment only what naming cannot capture.

## Before you deliver

Read each comment you wrote and ask: does this tell the reader something the code
does not already say? If it only restates the line below it, delete it. If it is
trying to explain a why, make sure it actually states the why and is still true.

For the prose style inside docstrings and longer comments, pair with
`no-filler-phrases`, `no-em-dashes`, and `no-fancy-ascii`.
