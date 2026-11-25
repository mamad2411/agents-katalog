---
name: llm-sessions
description: "Session log kept as files. Agent MUST load when reading or maintaining a sessions.kb/ directory, or when asked to record, find, or reconcile claude-code sessions."
---

# LLM Sessions

A `sessions.kb/` collection tracks lines of work that span claude-code
sessions -- in flight, planned, or recently relevant -- so many parallel
lines stay findable from any cwd. Each entry carries the uuids of the
sessions that worked it (also their transcript names under
`~/.claude/projects/`), when it started, and what it is for.

## What belongs

- A planned line of work not yet started (empty `session.uuid`)
- An in-flight one worth finding from other contexts
- A recently finished one whose follow-ups are still live

Not here: per-task todos (the project's `.claude/todo.kb/`,
Skill(llm-subtask)), per-session devlogs (the project, Skill(llm-collab)),
concept definitions or principles (their skill's kb).

## Entry shape

- `$slug.md` -- frontmatter from `template.md` beside this file, `$(...)`
  placeholders substituted. The body is live status (plan, blocked,
  decisions): edited in place, never appended.
- `$slug.kb/` -- one file per pickup write-up, reading like a devlog
  entry, named per Skill(llm-kb)'s `references/dated-slug-filename.md`.
  Start it once a pickup's write-up outgrows a one-line status update;
  close `$slug.md` with an `## Addenda` section pointing at it.
- Slug: kebab-case, purpose guessable from the name, unnumbered. When a
  taskfile exists, match its slug exactly (strip `CLAUDE.`/`.Task.`/`.md`).
- Open work is `- [ ]`. Bare `-` bullets are invisible to
  `claude-open-tasks-list` and silently lost (Skill(llm-subtask)).

## Start of session

Find the entry this session continues -- `grep -Rls` the collection for
the brief's basename if there is one, else for `^cwd: $PWD` (`-s`: other
hosts' symlinked entries dangle here). One match: read it and append
`$CLAUDE_CODE_SESSION_ID` to `session.uuid`.
None: create one if the work warrants it (below). Several: ask.

## Mid-session

Create an entry the moment a separate line of work is identified: a
tangent recognized as its own scope, follow-ups surfaced, the user
saying "that's another session". It earns one when the work is complex,
will take more than a couple of hours, has already spanned a day, or the
context is past ~100k tokens.

## End of session

1. Find this session's entry: `grep -Rl "$CLAUDE_CODE_SESSION_ID"`, else
   by `cwd:`.
2. Update `$slug.md`'s status in place; file this pickup's findings per
   [Entry shape](#entry-shape).
3. Propose one new entry per distinct line of follow-up work surfaced.
4. Delete entries whose follow-ups are absorbed elsewhere or no longer
   worth keeping at hand. Set `ended:` only when no further session is
   expected, never because this conversation ended.
5. Commit as the collection's own `CLAUDE.md` directs.

## Schema

`jsonschema/sessions.jsonschema.yaml` is the canonical. A collection binds
it positionally: `sessions.kb/*.md` validates against a sibling
`sessions.jsonschema.yaml`, which should be a one-line stub:

```yaml
# yaml-language-server: $schema=https://json-schema.org/draft-07/schema
$ref: "skill://llm-sessions/jsonschema/sessions.jsonschema.yaml"
```

Per-host sub-collections do the same, file-relative
(`$ref: "../sessions.jsonschema.yaml"`), so one edit to the canonical
reaches every host.

The schema declares the llm-kb dialect for its `instant`/`date` types, and
`$ref`s `cost-benefit-sweh` across to Skill(llm-subtask) rather than
restating it -- a session and a task rate their cost the same way.

## Local bindings

Rewrite this section, rather than dropping it, when porting.

- The collection is `~/.claude/sessions.kb/`, entries under
  `<hostname>.kb/`. Its `CLAUDE.md` covers that repo's host layout and
  commit cadence.
- Optionally, an entry tightly coupled to one project's artifacts may live
  at `<project>/.claude/sessions.kb/<slug>.md`, symlinked from the host
  directory. Prefer the default.
