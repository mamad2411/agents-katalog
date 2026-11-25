---
name: precedent-tag
description: Show or set this project's tags, which is how precedent finds comparable work. Use when a project is untagged, when its brief reports no matches, or when the user asks what kind of project the graph thinks this is.
---

# Show or set this project's tags

With nothing to add, show the vocabulary and this project's current tags:

```bash
uv run <cli> tag --project .
```

To add tags:

```bash
uv run <cli> tag --project . --add "<comma-separated tags>"
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it.

Always look at the vocabulary before coining anything. Matching is exact, so a
near-duplicate hides half the history from the other half; the command refuses
obvious collisions but cannot know whether you meant something genuinely
different. Prefer several small orthogonal tags (`backend`, `java`,
`distributed`) over one compound name — each part is reused by other projects,
which is what makes overlap meaningful.

In a monorepo, tag each module separately and tag the root with what is true of
the whole repository.
