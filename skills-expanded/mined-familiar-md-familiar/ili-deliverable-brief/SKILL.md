---
name: ili-deliverable-brief
description: Scope a deliverable before drafting it, iterate on its message, audience and outline, then lock the brief for /draft-document.
disable-model-invocation: true
---

# familiar — Deliverable Brief

The user wants to settle what a deliverable says before anyone drafts it. The brief is where the
iteration happens: a sentence or a headline is cheap to change, a drafted section is not. Work moves
from the core idea, to the argument, to a headline outline, and then the user locks it.
`/draft-document` builds from the locked brief. Changes after the lock are recorded as amendments, so
an idea that arrives mid-draft goes into the brief on purpose and does not slip into the draft.

## Context contract

- **Required context:** `.familiar/core/voice.md`, `.familiar/core/plain-language.md`, `.familiar/core/file-handling.md`, project configuration, this skill's `references/brief-template.md` and `references/profile-format.md`, and `2-Drafts/_draft-index.md`.
- **Conditional context:** the deliverable's `2-Drafts/<slug>/_brief.md` only when it already exists (resume, lock, or amend); the profile files under `~/.familiar/brief-profiles/` and `.familiar/extensions/*/package/brief-profiles/` only when choosing a profile; a profile's `authority` file only when that profile is in use; example files the user names only when building a profile or using an example as a model; `5-System/project-context.md`, `5-System/Memory/status-snapshot.md`, `5-System/Decisions/` and `3-Knowledge/_knowledge-index.md` only during the harvest; a named knowledge page or source only when the harvest or a key point needs it; `.familiar/core/retrieval-fallback.md` only when the harvest cannot dispatch `lookup`; the deliverable's current draft only when briefing a deliverable that already has one; the brief or current file named on the `Builds on` line only when it is set.
- **Excluded context:** Other projects, `4-Trackers/`, `5-System/Memory/status-log.md`, other deliverables' drafts and briefs (except one named on `Builds on`), every other file under `~/.familiar/`, and undeclared extension content.
- **Updates:** `2-Drafts/<slug>/_brief.md`, creating the `2-Drafts/<slug>/` folder when the deliverable is new; and, only on the user's explicit yes, one profile at `~/.familiar/brief-profiles/<id>.md`. That profile write is this skill's declared exception to `CORE-WORKSPACE-SILO`.
- **Capabilities:** file-read, file-write; named-subagents optional for the harvest, degrading to `retrieval-fallback.md`. Where a host cannot read or write outside the project folder, say so: profiles are then unavailable and the brief runs without one.
- **Completion:** The brief is saved with its stage, status, revision, profile, open questions and evidence gaps stated, and the user knows the next step; or it is locked with the user's explicit approval and a passed headline test recorded in the file.

## The brief

`references/brief-template.md` is the file's shape. The brief is a living file with a stable name:
before replacing it, reread its `Revision` and apply `CORE-STALE-WRITE`. Every save increments
`Revision` by one. The slug is the deliverable's slug from `file-handling.md` → Saving under
`2-Drafts/`; the first draft version then lands in the same folder.

Mark every field as `agreed` or `proposed`. The user stated or accepted an `agreed` value. A
`proposed` value is familiar's suggestion and carries a one-line reason or a source locator. Never
change a `proposed` value to `agreed` without the user's yes. These marks are the boundary between
your suggestions and the user's decisions, so they stay visible in the file.

## Start: profile, then harvest

### Choose a profile

`references/profile-format.md` defines profiles and where they live. List the profiles whose
`organization` is `any` or matches the project configuration's Organization, ignoring case. Then
compare the request with each one's `name` and `select_when`.

- **One fits:** name it and its source (global or extension), and ask the user to confirm it.
- **More than one fits:** ask which one.
- **None fits:** run the generic brief. If the user has an example of this kind of deliverable, offer
  to build a profile from it (below).

Record the profile as `Profile: <id> rev <N> (<source>)` in the brief header, and copy its
`standards` paths to the brief's `Standards` line. A profile with a
different `organization` is never used. If its name fits the request, say that it exists and why it
was not offered.

With a profile in use, add its extra fields to their stages and start the Outline from its skeleton.
If its `basis` is `template`, read its `authority` file: the form's own instructions win over the
profile and over the generic brief. A conflict between the form and the user goes to Open questions,
never resolved silently.

### Build a profile from an example

The user names one or more example files: a past deliverable in `1-Inputs/Examples/`, or a file
they point to. Read them and propose a profile in the shape of `references/profile-format.md`:

- The examples' shared section structure becomes the outline skeleton.
- Elements that recur in every section become extra fields or harvest questions.
- Length, level of detail and recurring devices become Style.
- Differences between examples become Variations.

Take structure only. Client, product and person names, data, findings and copied passages from an
example never go into the profile, the brief or the draft. Set `organization` to the project's
Organization unless the user says `any`.

Show the whole proposed profile. On the user's yes, write it to `~/.familiar/brief-profiles/<id>.md`.
If that file exists, reread its `revision`, show what changes, and write only on a second yes.
If the user does not want to save a profile, use the example as a model for this brief only and
record it as `Model example: <path>`.

### Harvest

Pre-fill the brief from what the project already knows. Read `5-System/project-context.md`, the status
snapshot, `5-System/Decisions/`, and the knowledge index. Look for the profile's "Harvest looks
for" list, or for the Core and Argument fields when there is no profile. Open only the knowledge
pages the index matches. If more than a few pages match, dispatch the `lookup` agent with the list
and use its quotes. The harvest is read-only. Its only output is `proposed` fields in the brief,
each with a locator.

Report what the harvest looked for and did not find, item by item. A missing element is an Open
question, never a guess.

## Stages

The stages are an order of fidelity, not a fixed itinerary. The user can go back to any stage. A
later stage can start while an earlier field is still `proposed`, but the lock cannot.

1. **Core.** Governing thought (the one sentence the audience must accept or act on), audience (who
   they are, what they know and believe now, and whether the deliverable leaves the project, per
   `voice.md` → Audience), objective (the decision or action wanted from them), format, deadline,
   out of scope, and mandatories.
   Test: the user can say the governing thought, audience and objective back in one breath.
2. **Argument.** Situation, complication and resolution, then three to five key points that together
   support the governing thought, with no overlap between them. Give each key point its sources as
   project paths and an evidence status: `supported`, `partial`, or `gap`.
   **When the deliverable argues a position** to a decision-maker (the profile says `argues: yes`, or
   the user says so), also give each key point the verbatim quote that carries it, with its locator,
   and the strongest counter-argument the decision-maker could raise, with the answer. A key point
   whose quote cannot be found is a `gap`, never a paraphrase. If an earlier deliverable already made
   this argument (a filed request that a later section must agree with), name it on the `Builds on`
   line and carry its key points over as `proposed`.
   Test: every key point has a source or an explicit `gap`; for an argued deliverable, every key point
   has a quote and an answered counter.
3. **Outline.** One headline per section, or per slide for a deck, written as a full sentence that
   states the point. Map each headline to a key point. Draft a short executive summary. If the
   profile's `outline` is `fixed`, keep the form's sections and write the headlines inside them.
   Test: read only the headlines, in order. They state the governing thought and every key point. If
   one does not, name the weak headline.

Ask one stage's questions at a time. For a quick deliverable, the user can fill all three stages in
one pass.

## Confidence

- **High** — the user stated it, or a project source states it plainly. Write it as `agreed` when
  the user stated it. Write a source-stated value as `proposed` with its locator, and ask.
- **Medium** — your inference from the project, a profile, or an example. Write it as `proposed`,
  with the reason, and ask.
- **Low** — no basis. Leave the field empty and add it to Open questions. Never fill it to make the
  brief look complete (`CORE-NO-FABRICATION`).

## Sources

A key point's source is a `3-Knowledge/` page or a file under `1-Inputs/`, by path. If a source is in
`1-Inputs/` but not yet ingested, record the key point as `partial` and tell the user that `/ingest`
will make it citable. Retrieval belongs to `/ingest` and `/online-research`. This skill records gaps
and does not close them.

## Lock

Lock only when the user says to. Before locking, report each of these and get the user's yes:

- Core and Argument fields that are still `proposed` or empty.
- Key points with evidence status `gap`. The user can lock with a known gap. The gap then stays in
  the file as an accepted gap, so the draft marks those claims `[verify]` (`voice.md` → Uncertainty
  marker).
- Required profile sections with no headline.
- The headline test result.

To lock, set `Status: locked`, record the date and revision in `Locked`, and add a Decisions row.
Then tell the user to run `/draft-document` when they are ready. Do not start it yourself.

## Amend after the lock

If the user changes a locked brief, keep `Status: locked`. Make the change and add an Amendments row
with the revision, date, what changed, why, and its impact on the draft. Name the draft sections or
slides to rework, or write `none yet` when there is no draft. If the change alters the governing
thought or the audience, say in one line that the whole outline needs a fresh headline test, and run
it.

## Briefing a deliverable that already has a draft

Read the current draft and write down the argument it actually makes, as `proposed` fields. Show
the user where the draft is unclear, such as two candidate governing thoughts or headlines that state
no point. Do not edit the draft. Rework goes through `/draft-document`.

## Guardrails

- Write nothing except `_brief.md` and, on a yes, one global profile. A brief is not a draft, so
  `draft_save.py` and `_draft-index.md` are not part of this skill. The draft index gets the
  deliverable's row when its first draft is saved.
- The brief is internal working material. Write it in plain project language. The audience rules
  apply to the deliverable that the brief describes, not to the brief.
- One deliverable per brief. If the user describes two deliverables, ask which one to brief first.
