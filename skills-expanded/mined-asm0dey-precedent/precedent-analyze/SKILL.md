---
name: precedent-analyze
description: Read an existing project and record the decisions already visible in it. Use for a project that predates the graph, when the user wants to backfill decisions from manifests, CI config and docs rather than from conversation.
---

# Backfill the graph from an existing project

The decisions were made already — they are sitting in the manifests, the CI
config and the README, and nobody wrote them down anywhere they can be queried
from. `<cli>` below is this package's `precedent.py`; the `precedent` skill says
how to locate it.

Work in this order. Do not skip to recording.

**1. See what is already known.**

```bash
uv run <cli> brief --project <path>
```

Everything under "decided here" is already recorded; re-recording it creates a
second decision saying the same thing with a different id, and `maintain` will
report the pair as a contradiction. Note the tags too — an untagged project's
decisions surface nowhere, so tag it (the `precedent-tag` skill) before
recording anything.

**2. Read the evidence.** Not just the file listing — open them:

- build manifests and lockfiles (what was picked, and what version policy)
- CI and release workflows (where it builds, what gates a merge)
- `Dockerfile`, compose files, deployment and infra config (where it runs)
- `docs/adr/`, `decisions/`, `ARCHITECTURE.md` if they exist — these are
  decisions already written as decisions, with their rationale intact
- `README.md` and `CONTRIBUTING.md`, especially any "why" sections
- `git log --oneline | grep -iE 'switch|migrat|replac|drop|move (to|off)'` —
  a migration commit is a decision with a date and often a reason

**3. Keep only what is worth quoting back.** The test for each candidate is:
*if I started a comparable project tomorrow, would I want to be told about this?*

Record: the database, the framework where alternatives existed, auth, the
deployment target, the language, the test and lint stack, the release process,
the licence, anything the project pays a visible cost for.

Do not record: transitive dependencies nobody chose, framework defaults that came
with the template, formatting settings, or a version number. A decision with no
alternative is not a decision.

**4. Rationale comes from evidence or from the user — never from you.**

This is the step that makes the difference between a useful graph and a
poisoned one. A rationale you inferred gets replayed to the user in two years as
*their own reasoning*, and they will believe it. So:

- Evidence exists (ADR, README paragraph, commit message) → use it, and say
  where it came from: `--rationale "inferred from docs/adr/0003.md: ..."`.
- No evidence → ask the user for the why, in one batch at the end, or record
  with an empty `--rationale`. An honest gap is recoverable; a fabricated
  rationale is not.

Same rule for `--rejected`: only when the evidence names the alternative that
was turned down.

**5. Show the list and wait.** One line per candidate — scope, title, chosen
option, and where the rationale came from. Let the user strike the ones that are
noise. Then record them one at a time:

```bash
uv run <cli> record --project <path> \
  --title "..." --rationale "inferred from ..." --scope tooling \
  --topic "..." --chose "..." --rejected "..."
```

`--topic` is the question the decision answers (`persistence`,
`backend-framework`), never a project tag like `java` or `telegram-bot`,
and never a bare noun plus a qualifier (`framework,java`). Put the
qualifier inside one topic.

Ten decisions is a lot for one project; three or four good ones with real
rationale beat fifteen guesses. In a monorepo, record against the module the
decision is about and put only repo-wide decisions on the root.
