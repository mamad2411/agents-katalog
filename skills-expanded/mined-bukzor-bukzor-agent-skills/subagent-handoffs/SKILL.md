---
name: subagent-handoffs
description: Coordinate a multi-part implementation by delegating each small component to a sub-agent, with every handoff (brief and report) a reviewable file on disk. Load when the user asks to "use sub-agents" for a plan, to coordinate rather than implement, or when a plan's steps split into independent, file-scoped units.
---

# Sub-agent handoffs

The main session coordinates; sub-agents implement. The coordinator's context
is the scarce resource, so it writes briefs, reviews reports, and keeps the
plan current, but never does the components itself.

Every handoff, in both directions, is a file that can be reviewed, revised and
reused. A prompt or reply that exists only in chat is lost; back-filling it
later is too late, because the record should be what the agent actually worked
from.

Why the method is shaped this way -- the goals it balances, and the options
it declined -- is in [`claims.kb/design.md`](claims.kb/design.md). Read it
before changing the method, or when a case the procedure doesn't cover needs
a judgment call.

## One home per fact

A fact copied into two files drifts in one of them, and an agent that reads
the stale copy works from it. So every fact has one home, and every other
file links to it. A handoff file holds only what has no other home.

| fact | its home | the handoff file holds |
|---|---|---|
| design: what is built, and why | the project's design docs, or the plan if there are none | links to the sections that govern the unit |
| an interface a unit produces | the artifact itself: code, schema, file format | the paths that define it, and any deviation from the brief |
| a finding: a measurement, a quirk, evidence | the doc it belongs in, written by the unit that found it | a pointer to where it went |
| a rule every agent follows | the collection's `CLAUDE.md` | nothing |
| what was changed, line by line | git | nothing |
| what this unit was asked, chose, and still doubts | the handoff file | brief, Decisions, Open Questions |
| how far this unit got | the handoff file | Steps |

When no permanent home exists for a finding, the report is its home, and
nothing else copies it.

## Layout

The units elaborate a parent plan, so they nest under it (`Skill(llm-kb)`,
"Where an Elaboration Goes"):

```
{{plan}}.md                  the plan; its step list links each handoff file
{{plan}}.jsonschema.yaml     handoff frontmatter schema (todo schema `$ref`)
{{plan}}.kb/
  CLAUDE.md                  protocol + everything every agent shares
  YYYY-MM-DD-NNN-slug.md     one per unit: brief, then the agent's record
```

Claude Code loads a directory's `CLAUDE.md` when an agent reads a file in
it, so commonalities go there once instead of into every brief. Start it
from `templates/CLAUDE.md`, and start each brief from `templates/brief.md`.

## Tense

- An **open** handoff file states the current truth. An amendment is an
  in-place edit; a mistake is deleted, not documented.
- A **done** handoff file is a frozen record of what that agent did. It is
  never updated. A later correction is a new unit, or an edit to the
  fact's home. It is kept only for review: once the user is fully
  satisfied, cleanup `git rm`s it (Procedure, Close).

## Procedure

1. **Start clean.** Commit or set aside uncommitted work inside any unit's
   scope before the first launch, so each unit's commits hold that unit
   alone.
2. **Decompose** the plan step into units: ≤60 min each, scoped to a disjoint
   file list. A file several units would touch (a manifest, a package
   `__init__`) belongs to exactly one of them. A doc that receives a unit's
   findings is in that unit's file list.
3. **Order into waves** by interface dependency. Units in a wave run in
   parallel; a wave starts when the interfaces it consumes exist. Record the
   waves in the plan as checkboxes, each linking its handoff file.
4. **Brief** each unit as a file before launch. Its `required-reading:` names
   homes: the `CLAUDE.md`, the governing doc sections, the interfaces it
   consumes by path. An upstream handoff file is named only for what has no
   other home, such as its deviations or open questions. Commit the brief,
   then launch with one line: "Do the task in {{path}}; read its CLAUDE.md
   and required-reading first."
5. **Receive:** the agent replies with the path, its unit committed. Read
   its Final report and its commits, and tick the plan's checkbox. Treat the
   commits as a collaborator's: keep them, reset them, `--fixup` them, or
   ask the agent for more. Then route what came back:
   - a rule every agent needs (an environment workaround) goes into
     `CLAUDE.md`;
   - a constraint on later units goes into their briefs, or into the doc
     their briefs already name;
   - a decision that belongs to the user goes to the user, briefly.
6. **Amend** in the fact's home, never in chat, and commit it. Then
   `grep -l {{home}} {{plan}}.kb/*.md` finds the briefs that read it: message
   each open one "reread {{path}}". A done unit that the change invalidates
   gets a new unit.
7. **Resume** after an interruption: the open handoff files are the
   in-flight units, each one's Steps say how far it got, and on its scope
   the index holds its finished edits and the working tree its edit in
   flight. Relaunch each with "Resume the task in {{path}}".
8. **Close:** when the plan's success criteria pass and the user is fully
   satisfied on review, record the plan's commit range in the plan, then
   `git rm -r {{plan}}.kb/ {{plan}}.jsonschema.yaml`. Its record stays in
   git (`git log -- {{plan}}.kb/`).

## Pitfalls

- The coordinator's own failure mode is "it's only two lines, I'll just fix
  it". Anything beyond reviewing reports and commits, routing, and plan
  upkeep is a unit, including a tooling bug found along the way.
- Restating an upstream interface in a brief, "for convenience", is the
  drift this method exists to prevent. Name the path; the agent reads it.
- Work owned by another repo gets its brief in that repo's `todo.kb/`,
  standalone: no `CLAUDE.md` covers it there, so inline the protocol.
- Never move or rename a handoff file while its agent is still running:
  `status: done` in the file comes before the agent's reply arrives.
- Concurrent agents share one index: every `git add` and commit names its
  paths, so no party commits another's staged work. An `index.lock`
  collision is a sibling mid-operation: retry. The coordinator owns the
  plan.
- In auto mode, a hook that rewrites Bash calls voids the review of any other
  call sent with it in the same response: write the brief (or amendment) in
  one response and launch or message in the next.
- A brief that names an interface must say which unit owns it; when two
  parallel units need a shared type (an exception class), assign it to one
  and tell the other to wait or to stub it.
