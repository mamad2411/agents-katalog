---
name: echolot-setup
description: Build echolot.yml for an Android project — a repository scan, a probe trace, and a few questions only the human can answer. The echolot skill routes here when the project has no config.
---

# Setup

Run `echolot guide setup` and follow it. The installed echolot prints it, so
it matches the commands you are about to run.

What it rests on: **the human does not open the config.** Take everything
the repository and a probe trace can give — `echolot scan`, a probe capture,
`echolot probe`, `echolot names`, `echolot domains --root .` — and ask only
what exists in neither.

Ask one question at a time. Each is a choice among options taken from the
trace, with a default, and you wait for the answer before the next. You
present candidates and the human decides; a value nobody could find is
written as `null` and said out loud, never invented.

Before calling the config done, `echolot analyze` the probe trace and read
the window, not the findings: `start_anchor.matches` and
`end_anchor.matches` above zero, a window
that looks like the scenario, and not every detector firing at once. A
scenario with `window: launch` has no anchors to pick or to check: the trace
says where the launch ends, and `window.defined_by` reports it. Then
`echolot` should say `next: hunt`.

A project with a config that wants another journey measured needs no new
setup: the end of `echolot guide setup` says how to add a scenario.
