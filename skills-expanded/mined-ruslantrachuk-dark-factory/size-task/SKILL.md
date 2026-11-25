---
name: size-task
description: >
  Use when a request starts new work in a repository — "add", "build", "fix", "make", "change",
  "implement", "where do we start", a new ask from the owner or a customer — before any code, spec or
  branch, even when the answer seems obvious. Sizes the work (trivial / small / large) for the owner's ok
  and names the branch type, slug, tracker ID and end-to-end phases.
---

# Skill `size-task` — how big is this, and how do we name it

> Part of the dark-factory plugin. Needs no configuration.

> **Seam:** the tracker ID. It is recognised in a branch name by the project's `TRACKER_ID_RE` in
> `scripts/merge-feature.sh` — read the pattern from there (`grep -m1 '^TRACKER_ID_RE=' scripts/merge-feature.sh`);
> without that script, the default `[A-Z][A-Z0-9]+-[0-9]+` (Linear/Jira style `DMP-123`). **To swap the tracker, change
> that one line in the project.** With GitHub Issues the project sets `[0-9]+` (`feat/123-voice-input`); it is not the
> default because it would read `fix/404-page` as issue 404.

You are the tech lead. Before any code, size the work and agree it with the owner in one line. No code,
no branch, no spec until the owner says ok.

## Steps

1. **Read** the request (and the tracker card, if there is one) and the code it touches: entry points,
   tests, open PRs, `openspec/changes/` and the queue for overlap. Surfaces of a user-visible
   feature are asked first (`AGENTS.md` rule 7).
2. **Verdict**, one line, with the reason:

   | Verdict | When | What exists |
   |---|---|---|
   | `trivial` | one clear spot, no contract change, nothing to decide: a typo, a string, a one-line fix, a config value | no spec: a branch and a PR |
   | `small` | one behaviour or a few, within the existing model and API | `openspec/changes/<slug>/` with a short `proposal.md` (including WHEN/THEN acceptance scenarios) and `tasks.md` |
   | `large` | the data model, an API contract or a user flow changes | the same plus `design.md`: the delta and the transition tree |

3. **Propose**, in the same message:
   - **type**: `feat | fix | ui | refactor | chore | docs`;
   - **slug**: lowercase words with hyphens, unique — taken if `openspec/changes/<slug>/` exists (check it);
   - **tracker ID**, if the work has a card (`DMP-123`; GitHub Issues: the number, and `Fixes #123` goes in the PR);
   - **branch**: `<type>/<ID>-<slug>` with a tracker, `<type>/<slug>` without (`feat/DMP-123-voice-input`);
     the PR title carries the ID so the tracker links the PR and moves the card;
   - **phases** for `small` and `large` when there is more than one: each phase works **end to end**,
     from the entry point (webhook, route, command) to the result, and has an entry-level test. Never
     slice by layers ("data", then "API", then "UI"). Each phase is its own branch and PR: its own
     sub-card with its own ID (preferred), or `-p<K>` after the slug when there is no tracker.
   - **path and build mode** of a phase that will go through the feature pipeline: path `lite` when it touches
     about five files or fewer (tests included), with no migration or contract change, and does not split into
     parallel tasks — otherwise `full`; build mode `session` (one builder, slices in order) unless the slices are
     independent and wide enough that parallel wall time matters — then `pipeline` (the path matters only there:
     `session` builds any size with one builder). The owner's ok fixes both: the
     run does not size the work again;
4. **Wait for the owner's ok.** A change of verdict, name or phases is cheap now and expensive after the
   first commit.
5. After the ok: `trivial` — branch and PR. `small`/`large` — write `openspec/changes/<slug>/` with the
   `openspec` skill (superpowers skills such as brainstorming and writing-plans may help, but they write
   into that folder), then `openspec-to-beads` for the queue when the project has bd. Building a phase in the session: the `plan`,
   `build-tdd`, `integrate` and `wrap` skills.

## Output shape

```
Verdict: small — one behaviour in the existing bot flow, no model change.
Name: feat/DMP-123-voice-input (slug voice-input, tracker DMP-123)
Phases: 1) voice message → transcript reply, 2) length limit and error reply (sub-cards DMP-124, DMP-125)
Ok?
```

## Don'ts

- Don't start code, a branch or a folder before the ok.
- Don't inflate: a typo is `trivial`; a spec for it is waste.
- Don't deflate: a changed contract is `large` even if the diff is small.
- Don't reuse a taken slug or the name of an older change folder.
