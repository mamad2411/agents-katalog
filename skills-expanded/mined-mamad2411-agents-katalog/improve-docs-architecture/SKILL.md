---
name: improve-docs-architecture
description: Strict architecture review for markdown/docs corpora. Survey, deletion test, candidate cards, grilling. Review-only until apply.
disable-model-invocation: true
---

# Improve Docs Architecture

Strict structural review for a body of markdown. Combination of
`/thermo-nuclear-code-quality-review` (standards, ambition, tone) and
aihero.dev's `/improve-codebase-architecture` (survey → deletion test →
candidate cards → grilling). Docs rot like code: facts get two homes and
drift, stories bury rules, indexes restate content, and always-loaded files
tax every session. Do not collect nits. Hunt for "doc judo" moves: restructurings
that keep every load-bearing fact while making the corpus dramatically
smaller, flatter, and harder to contradict.

## Scope and modes

- **Survey mode (default):** the whole corpus the user names: a `.claude/`
  config tree, a `docs/` dir, a repo's markdown, a skill fleet.
- **Diff mode:** when the user names a branch, PR, or file, review only that
  change against the standards below, thermo-nuclear style.
- **Activity bias:** read git history (file mtimes when there is no repo) and
  weight actively-edited files. Weight **always-loaded files highest**: anything
  injected into context every session (CLAUDE.md, rules/, memory indexes) pays
  its cost on every turn. A cleanup in a doc nobody reads is a refactor you
  will never cash in.
- **Measure first.** Before judging, compute the numbers the review will rest
  on: lines and bytes per file, and the total always-loaded payload. Report
  them. No adjective without the yardstick.

## Deep vs shallow, for markdown

A **deep** doc hides detail behind a small stable surface: a rule you can obey
without opening three other files; an index that is only pointers; a story
that lives in an archive nobody loads. A **shallow** doc has a surface as wide
as its content. The three shallowness forms to hunt:

1. **Split meaning:** one policy smeared across files so the real rule lives
   in the orchestration ("read A, unless B, see priority order in C").
2. **Boundary leaks:** machine-specific facts in a shared doc, project facts
   in a global doc, incident history in a rulebook, content in an index.
3. **Five-file concepts:** a thing you cannot understand without opening five
   files that point at each other.

## The deletion test

Every candidate must pass: **if this file or section were deleted or merged,
would its job concentrate into one existing home, or would readers lose
something no other file provides?** Only "concentrates" qualifies. This kills
generic cleanup advice before it reaches the report.

## Non-negotiable standards

0. **Be ambitious.** Prefer the move that makes whole sections, files, or
   meta-rules disappear. If a precedence table exists to referee overlapping
   rules, the judo move is merging the rules, not polishing the table.
1. **One home per fact.** The same rule, path, count, or convention stated in
   two files is a drift bomb; one copy will rot silently. Flag every
   duplicate; name the surviving home.
2. **Size gates.** A doc drifting past ~300-400 lines is a decompose-or-cut
   candidate. An always-loaded corpus has a token budget; state the current
   total and the target. An index entry is one line; an index holding
   paragraphs has become a second copy of the content.
3. **No stories in source.** Dates, incident history, benchmark numbers, and
   "we tried X first" belong in an archive file (`docs/incidents.md`,
   ADRs), never in an always-loaded rule. Keep the one-line rule, move
   the story. (Same law as the Comments rule in coding-standards.)
4. **Contradictions are severity-one.** Two docs disagreeing on a fact is
   worse than either being missing; the reader cannot tell which is live.
   Stale dated claims ("as of", versions, model names, counts) are
   contradictions in waiting: verify or delete them.
5. **Verifier over prose.** Where a hook, lint, or CI check enforces a rule,
   shrink the prose to one line naming the verifier. Prose is taxed every
   load; the hook is free.
6. **No wrapper docs.** Files that only point at other files, headers over a
   single bullet, meta-sections about how to read the sections: indirection
   must buy clarity or die.
7. **Scoped exceptions, not scattered ones.** "Does NOT fire on" patches,
   per-file carve-outs, and special-case notes bolted on after the fact are
   spaghetti growth. Reframe the rule so the exceptions disappear.

## Standards, symptoms, and moves

| Standard | Symptom to flag | Preferred move |
|---|---|---|
| 0. Be ambitious | A rulebook needed an internal priority system to referee its own overlapping sections; a merge shuffled text without reducing how many places a reader must look | Merge overlapping sections into one and delete the referee |
| 1. One home per fact | A fact, rule, or path with two or more homes, especially across always-loaded files; a shared doc carrying machine- or project-specific facts | Relocate the fact to its owning layer (machine to local file, project to project CLAUDE.md, shared to the shared repo file) |
| 2. Size gates | Indexes whose entries have grown into paragraphs | Collapse an index entry to one line; the detail already lives in the file it points to |
| 3. No stories in source | Incident narratives inside rules that fire every session | Move the story to the archive; keep the sentence |
| 4. Contradictions are severity-one | Dated claims that no longer match the system they describe | Fix or delete every stale dated claim in the same pass |
| 5. Verifier over prose | Docs whose job a deterministic check already does | Replace enforced prose with one line naming the hook |
| 6. No wrapper docs | A concept that takes five files to understand | Delete the wrapper file; point the one reference at the real home |
| 7. Scoped exceptions, not scattered ones | "Does NOT fire on" patches and per-file carve-outs bolted on after the fact | Reframe the rule so the exceptions disappear |

## Report

Produce a single self-contained HTML report (inline CSS, no framework) in the
scratchpad or OS temp dir: `docs-architecture-review-<timestamp>.html`. Open
it when done. Lead with the measured numbers (per-file sizes, always-loaded
total, duplicate-fact count). Then one card per candidate:

- files and sections involved
- the friction, in plain English
- the move, in plain English
- payoff: tokens saved per load × drift surfaces removed
- before/after outline (headings only)
- strength badge

| Badge | Meaning |
|---|---|
| **Strong** | Deletion test passes clearly; the friction is real today |
| **Worth exploring** | Plausible; payoff depends on where the corpus is heading |
| **Speculative** | Surfaced for completeness; safe to ignore |

End with one top recommendation. Then **pick the top candidate, say why in
one line, and continue**. One candidate per session; a full-corpus rewrite in one pass is
how load-bearing lines get lost.

## Grilling session

For the chosen candidate, pressure-test before any edit is proposed:

- **References:** grep for every link, anchor, skill name, and path that
  points at the text being moved or deleted. List what must be updated.
- **Survival:** name each load-bearing fact in the affected text and its
  destination. A fact with no destination blocks the move.
- **Hidden coupling:** who else loads this file (hooks, tools, other boxes,
  CI)? A shared repo file changes on every machine that pulls it.
- **Deepened shape:** write the after-outline: headings and one-liners only.

The output of the grilling is a decision, not an edit.

## Apply gate

**This skill never changes a file without an explicit "apply" from the user.**
Both parents are review-only; this one adds a single gated exception. On
"apply": honor the Hand-Maintained Files rule (show full rewrites and wait;
targeted edits proceed), save backups, make the reference updates found in the
grilling in the same pass, and re-run the measurement so the report's numbers
have an after-column. If the corpus is a git repo, leave the change
uncommitted unless asked.

## Tone and output bar

Direct, serious, demanding, never rude. Do not soften a structural problem
into a mild suggestion. Prioritize: contradictions and duplicate homes, then
missed judo moves, then boundary leaks, then size, then style. A small number
of high-conviction candidates beats a long list of cosmetic notes. Do not
approve a docs change merely because the words are accurate: no new second
home for an existing fact, no new story in an always-loaded file, no new
wrapper, no size gate crossed without a stated reason; treat these as
presumptive blockers unless justified.
