---
name: lantern-no-comments
description: Use whenever writing, editing, or reviewing code and tempted to add a comment. Default to self-explanatory code — no comments that describe what a function/module/line does, no doc-blocks, no commented-out code. Comment ONLY for the non-obvious WHY: workarounds, gotchas, warnings, and required tooling pragmas.
user-invocable: false
---

# No Comments — the code explains itself

**Default to writing code that needs no comment.** Clear names and small functions explain
*what* the code does; a comment is only worth its weight when it explains a *why* the code
**cannot**. If you're tempted to write a comment that restates the code, fix the code instead.

## Don't write these

- **Doc-blocks describing a function/method/class/module** — the name + signature already say
  it. No "`// formats the user's name`" above `formatUserName`.
- **Comments that paraphrase the next line** — `// loop over users`, `// increment counter`,
  `// return the result`.
- **JSDoc/param/return descriptions** added just for ceremony (`@param id the id`).
- **Section banners / dividers** (`// ===== HELPERS =====`) and `// end of function`.
- **Commented-out code** — delete it; git remembers.
- A comment that exists because the code is unclear — **rename or extract** instead.

## Comment only for the non-obvious *why*

Keep a comment when it carries information the code genuinely can't:

- **Why** — a non-obvious decision, tradeoff, or constraint (*"sequential, not `Promise.all`
  — the API rate-limits to 1 req/s"*).
- **Workaround / gotcha** — *"Safari needs the timeout; remove when bug #1234 ships"* — with a
  link/issue, so it can be cleaned up later.
- **Warning / footgun** — ordering requirements, side effects, "don't reorder these", a
  surprising consequence.
- **Required pragmas** — `eslint-disable-next-line <rule>` (with the reason), a `TODO` that
  references a ticket, a type assertion that needs justification.
- **Published-API docs** — for a library others consume, document the *contract/usage* (not
  the internals).

Keep these short and current — a stale comment is worse than none.

## Prefer code over comments

- Extract a **well-named** function or intermediate variable instead of a comment.
- Use intention-revealing names (`is/has/should` booleans, verb-first functions).
- Encode invariants in **types**, not prose.

Before writing any comment, ask: *"Can I make the code say this?"* If yes, do that. If the
comment explains a non-obvious **why**, keep it — one tight line.
