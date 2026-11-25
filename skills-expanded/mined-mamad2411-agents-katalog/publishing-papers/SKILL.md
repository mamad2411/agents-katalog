---
name: publishing-papers
description: 'Use when a paper has to get through a journal — its source, its upload packet, or its answer to the reviewers. Covers 期刊模板, 双栏 layout, 页数超限, and an elsarticle or IEEEtran source that will not compile; 投稿 and 投稿材料 for Elsevier Editorial Manager or the IEEE Author Portal, cover letter, highlights, required statements, EDICS, and the source zip; and 修回稿, 返稿, 审稿意见, 怎么回复审稿人 — a major or minor revision decision whose reviewer comments each need 逐条回应 in a point-by-point response letter. Do not use for writing or reviewing the paper''s argument and prose, or for producing figure artifacts.'
license: MIT
compatibility: Requires Python 3 and a LaTeX runtime (latexmk with elsarticle or IEEEtran); pdfinfo (poppler-utils) for page counts, python-docx for Markdown-to-DOCX, and a full TeX Live with tcolorbox's breakable library for the response letter.
---

# Publishing a Paper to a Journal

Everything after the science is settled: the publisher's manuscript source, the files a
submission screen asks for, and the answer to a revision decision. This skill does not write or
review the paper's argument, and it does not produce figure artifacts.

Three things below hold in every phase. Read them once, then take the phase you are in.

## Establish the publisher first

The two supported vocabularies do not overlap, and mixing them produces a source that compiles
under neither class. `elsarticle` uses a `frontmatter` environment with `\ead` and `\corref`;
`IEEEtran` journal mode has no `frontmatter` and uses `\thanks`, `\markboth`, and `\IEEEPARstart`.
The upload screens diverge just as hard.

So settle the publisher before touching anything, then read **exactly one** publisher reference
per phase. If the target journal is unknown, ask — a guessed publisher costs a full rewrite of
the title block, the back matter, and the bibliography setup.

## Precedence: which instruction wins

Instructions arrive from several places and they do conflict. **The narrower the audience a source
was written for, the more it outranks:**

1. The decision or invitation letter, written about this manuscript.
2. The live submission screen for the current step: the item types it names, the limits it
   displays, the formats it refuses.
3. The journal's Guide for Authors.
4. Publisher-wide policy and support articles, which describe every journal and therefore none of
   them exactly.

Record a conflict rather than resolving it silently. A screen that contradicts the guide is a
durable fact about this journal, and it will contradict it again next round.

**Your notes about a source are not that source and hold no rank at all.** A digest of the
decision letter, a checklist someone typed up from the guide, a summary of last round — each is a
claim to re-verify against the artifact it describes, and each drifts toward the generic list its
author half-remembered. The failure to expect: a note that promotes a publisher's optional
materials into "required", sending you off to build documents the screen never asked for. Read the
letter and read the screen.

**System behaviour is not a rung on this ladder.** How the platform unpacks an archive, where it
puts figures, what it does to a filename — that is mechanism. It holds whatever any instruction
says, and no journal wording overrides it. The failure to avoid is inferring a requirement from a
mechanism: that a platform expands an archive into per-file items tells you how to tag and order
those items, and nothing at all about how many files the archive should have contained.

## The two-column PDF is the yardstick

Page limits are judged against the layout the journal publishes in, not against a reading draft.
An IEEE transaction counts pages in two-column `journal` mode; `draftclsnofoot,onecolumn` is for
reading, never for measuring. Whatever you compress, verify it in the layout that will be judged.

## Route by phase

| You are | Read |
|---|---|
| Starting or maintaining the manuscript source — class options, frontmatter, bibliography, a local build that fails | [references/manuscript-source.md](references/manuscript-source.md) |
| Building the files a submission screen asks for — statements, side materials, source archive, the final check | [references/packet.md](references/packet.md) |
| Answering a revision decision — scoping each comment, running what was asked, writing the response letter | [references/revision.md](references/revision.md) |

A revision touches all three: the comments decide what changes, the source has to absorb those
changes and still compile, and the packet has to distinguish clean from marked files. Take them in
that order — the letter is the last thing written, because it can only report work that already
exists.

Publisher references, one per phase, never both:

- Manuscript source: [elsarticle.md](references/elsarticle.md) **or** [ieeetran.md](references/ieeetran.md)
- Packet: [elsevier.md](references/elsevier.md) **or** [ieee.md](references/ieee.md)
- A journal's own limits, once extracted: [journal-profile.md](references/journal-profile.md)

## Done

Each phase reference states its own completion bar. Across all of them:

- One publisher's vocabulary is used throughout; no macro or item type from the other survives.
- Every limit that applies was read off a live source this round, not recalled from last round.
- The build exits zero with no undefined references or citations, in the layout the journal judges.
- Nothing is reported as done that a reader cannot check in the artifacts you are submitting.
