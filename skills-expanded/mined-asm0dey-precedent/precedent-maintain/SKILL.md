---
name: precedent-maintain
description: Check the decision graph for contradictions, tag drift and dead projects. Use when the user asks about the health of the graph, suspects duplicate tags, or wants to clean up recorded decisions.
---

# Check the graph for problems

```bash
uv run <cli> maintain
```

`<cli>` is this package's `precedent.py`; the `precedent` skill says how to
locate it.

Report what it finds. Contradictions (one project, one topic, two live answers)
are for the user to resolve — record a new decision with `--supersedes <id>`
rather than editing history. Suspected duplicate tags are repaired with
`tag --merge <old> --into <new>`.

Projects with no portable identity are reported too. A `split across two nodes`
line means one repo has two Project nodes holding two separate decision
histories — surface it. `maintain` prints a `merge-project --from <id> --into <id>`
line for each. Show the user both sides' decisions and let them decide; run it
only on a yes. The same line appears under "projects whose path no longer
exists" when a live project shares the ghost's name, and under "one checkout,
two remotes" when a checkout's remote changed (a rename, a move to another
host) and the same directory now keys a second node. There the hint merges
into the remote the checkout reports now — but a fork and its upstream are
two projects, so the same rule applies: both sides first, then a yes.

Run `maintain --apply` only to delete orphan nodes; everything else is a
proposal that needs the user's judgment.
