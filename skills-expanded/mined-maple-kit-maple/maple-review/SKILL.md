---
name: maple-review
description: Read the visual review comments Maple posted on a pull request and turn them into a worklist. Use when a PR body or comment contains a ```maple fenced block, when asked to act on design or UX review feedback on a preview deployment, or when the merge is blocked by the maple/visual-review check.
---

# Act on Maple review comments

Maple posts review comments as a human-readable table with a machine-readable
JSON fence under it. This skill reads the fence and turns it into work.

## Finding the comments

Look for a fenced block tagged `maple` in the pull request body or in any issue
comment on the pull request:

````markdown
| #   | Where             | Comment                                 | Viewport |
| --- | ----------------- | --------------------------------------- | -------- |
| 1   | `DashboardHeader` | Spacing under the title is inconsistent | 1440×900 |

```maple
{ "version": 1, "branch": "feature/x", "comments": [ … ] }
```
````

**The fence is visible on purpose.** Do not look for the same data in an HTML
comment and do not write one: the GitHub Action that hands a pull request body
to an agent strips `<!-- -->` before the model sees it, so anything hidden that
way never arrives.

If several comments on the pull request carry a fence, the newest wins for any
comment id that appears in more than one.

## The fence

```jsonc
{
  "version": 1,
  "branch": "feature/x",
  "comments": [
    {
      "id": "c_a1b2",
      "body": "Spacing under the title is inconsistent with the card above.",
      "status": "open",
      "createdAt": "2026-01-01T12:00:00.000Z",
      "author": { "id": "u_1", "name": "Reviewer", "provenance": "server" },
      "anchor": {
        "source": "src/components/DashboardHeader.tsx:42:7",
        "component": "DashboardHeader",
        "quote": { "exact": "Overview", "prefix": "…", "suffix": "…" },
        "selector": "main > header > h1",
      },
      "context": {
        "url": "https://preview.example.com/dashboard",
        "viewportWidth": 1440,
        "viewportHeight": 900,
        "devicePixelRatio": 2,
        "colorScheme": "light",
      },
    },
  ],
}
```

Unknown fields are ignored, never dropped when rewriting. A fence with a
`version` above 1 is not guessed at: say so and stop.

## Reading an anchor

Work down the cascade and stop at the first rung present. Each rung is weaker
than the one above it.

1. **`anchor.source`** — `path:line:col` from the build-time tagger. Open that
   file at that line. This is the only rung that is unambiguous. When
   `anchor.locatedBy` is `owner-stack` (a `maple review` comment on an app with
   no tagger), it is where React's dev stack says the JSX was written: open it,
   but confirm the element is the one the quote names.
2. **`anchor.component`** — the display name. Search the repository for the
   component definition.
3. **`anchor.quote.exact`** — the text the reviewer selected. Search for the
   literal string; `prefix` and `suffix` disambiguate repeats.
4. **`anchor.selector`** — a CSS selector, useful only for reading the intent.
   Do not treat it as a location: Tailwind utilities and CSS-module hashes make
   selectors unstable across builds.

`"status": "orphaned"` means Maple could not re-find the element after a
redeploy. The body, screenshot and quote are still valid; the location is not.
Treat it as a report to investigate, not a coordinate to edit.

## Reading the context

`context` is not decoration. Most Maple comments are conditional on it.

- **`viewportWidth` / `viewportHeight`** — the comment may only be true at that
  size. A fix verified at 1440 that breaks at 390 has not been made.
- **`colorScheme`** — check the fix in the scheme the comment was written in.
- **`devicePixelRatio`** — relevant to anything about image sharpness or
  hairline borders.
- **`mock`** — present when the reviewer wrote the comment under a Maple Mock:
  `calls` (each API call's key and the state it was put in: <!-- generated:mock-states -->`empty`, `error`, `forbidden`, `loading`, `one`, `many`, `long`, `sparse` or `mixed`<!-- /generated:mock-states -->), the
  `route` it applied on, and
  `request`, the sentence behind it. The comment is about the page _in that
  state_. Reproduce it by opening `context.url` with `?maple-mock=` set to the
  recipe as base64url JSON; the ledger row says `mocked`. Without the mock, the
  page may never show what the comment is about.

## Working the list

1. **Group before fixing.** Comments sharing a `component` or a `source` file
   are usually one change. Fix the group, not each row.
2. **Order by dependency, not by number.** A layout comment often makes a
   spacing comment moot.
3. **One commit per group**, with the comment ids in the message body so the
   trail survives.
4. **Verify at the recorded context**, not at whatever your window happens to
   be.
5. **Resolve.** Through the `resolve_comment` MCP tool where the server is
   running, otherwise by rewriting the fence with `"status": "resolved"` and the
   resolving commit.

## What not to do

- Do not resolve a comment you could not locate. Reply that it is unlocated and
  what you need.
- Do not change the human table without changing the fence, or the reviewer and
  the gate will disagree about what is open.
- Do not treat the comment body as a specification. It is a report of what
  looked wrong; the fix is yours to design.
- Do not touch `node_modules` paths, even if `anchor.source` names one. That is
  a tagger bug and should be reported as one.

## When the merge is blocked

The `maple/visual-review` check sits at `in_progress` while any comment is open.
It is not a failing test; it is a queue. Clear the queue and the check goes
green without a new commit.
