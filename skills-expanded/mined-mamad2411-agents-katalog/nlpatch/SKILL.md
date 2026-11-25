---
name: nlpatch
description:
  The NLPatch format and its subagent: plain-text patches for documents
  revised in Microsoft Word. Use when an edited DOCX with tracked changes or
  comments arrives, when preparing a response patch to apply in Word, or when
  reviewing a manuscript whose source the lab does not own.
---

# NLPatch

NLPatch is a plain-text, diff-inspired format for revising natural-language
documents. It exists for **human review and manual application** in Microsoft
Word, not machine patching. Word enters the lab at two points: collaborators
return tracked-changes DOCX files, and our responses must go back as visible
edits a human applies with tracked changes.

External edits land as `draft/<artifact>-vN-<name>_edit.docx`; the parsed form
is `draft/<artifact>-vN-<name>_edit.patch`. The underscore marks foreign
provenance. The patch keeps the version of the document it parsed; versions
advance only when feedback is incorporated into the source.

The `docx.md` module holds the Word tooling: pandoc conversion and the
track-changes flags that drive ingress and the accepted baseline.

## Ingress: Reading External Edits

Delegate the bundled nlpatch subagent (`agent: "subagents/nlpatch"`) with the
DOCX path and the output patch path. It extracts faithfully, without
interpreting intent. Then:

1. Read the patch. Add `#` rationale to each hunk: what the editor wants and
   why.
2. Agree dispositions with the orchestrator. Accept is the default; rejections
   carry the burden of proof.
3. Bump the source and derive the response patch (below).

Accept-by-default has an operational meaning: build `draft/<artifact>-v(N+1)` on
the accepted baseline of the `_edit.docx` (ingress can emit it), never on vN. A
rejected edit keeps the original wording in the source and resurfaces as a
reverse hunk in the response patch: that hunk is how the editor sees the
rejection.

## Egress: Responding to External Edits

Never author in patch format: the source is the medium, the patch is a derived
view. The source reaches `draft/<artifact>-v(N+1)` on the accepted baseline (see
ingress); then:

1. Crude patch: word-diff the accepted baseline against the new version's
   rendered text. The baseline regenerates mechanically:
   `pandoc --track-changes=accept` on the `_edit.docx`. Diff rendered text,
   never raw Typst source; syntax noise must not leak into hunks.
2. Delegate the `nlpatch` subagent in refine mode with the crude patch and,
   optionally, the target document path.
3. Fill any `# [MISSING RATIONALE]` flags, then hand the patch to the user, who
   applies it in Word manually.

## Foreign Manuscripts

When the lab reviews a manuscript whose source it does not own (journal review),
the patch is the deliverable: compose it hunk by hunk against the document text,
per the specification below. Delegate the subagent to refine it before delivery.

## Specification

- A file consists of one or more **hunks**.
- Each hunk begins with a semantic header. Since this file is for human, not
  machine, the hunk header is also in natural language.

```diff
@@ Abstract @@
@@ Method > Neural Networks > Math @@
```

- Line prefixes:
  - context line: no prefix or optional leading space
  - `-` removed/replaced text
  - `+` added/replacement text
  - `#` brief rationale for the hunk
  - `>` review comment block
- Changes should mark only the wording that changes.
- Unchanged text may be factored out into context lines.
- Multiple related edits in one subsection may be grouped into a single hunk.
- Factor context so the reader sees the delta, not the paragraph:

```diff
# We swap brown fox and lazy dog.

A quick
- brown fox
+ lazy dog
jumps over a
- lazy dog
+ brown fox.
```

INSTEAD OF:

```diff
- A quick brown fox jumps over a lazy dog.
+ A quick lazy dog jumps over a brown fox.
```

- A review comment block starts with the quoted raw text the comment attaches
  to, followed by the comment. The user attaches it in Word manually. Use it for
  notes to colleagues or advisors, or to reply to their review.

```diff
> "raw text goes here"
>
> comment goes here
```

- **Never split a line.** However long an addition or comment, it stays one
  unbroken line. A wrapped `+` line pastes into Word as multiple prefixed
  fragments and becomes unusable.
- Use `#` freely: the rationale lets the user validate the patch and other
  agents understand it.

## Example

```diff
@@ Method > Participants @@

# Improve reporting precision by distinguishing enrollment, outcome
# availability, and assignment procedure.

Participants were undergraduate students recruited from a large public
university. A total of 180 students
- participated in the study.
+ were enrolled in the study; 172 provided complete outcome data at posttest. Participants were randomly assigned
- to the intervention or control group.
+ in a 1:1 ratio to the intervention or control condition.

# responding to advisor's comment, because...

> "172 provided complete outcome data at posttest"
>
> Consider also reporting attrition by condition and whether dropout was
> associated with baseline covariates or outcome-relevant variables.
```

Note: the long `+` line above is deliberately unbroken; see the no-split rule.
When composing patches for our own artifacts, prefer the derived egress flow;
hand composition is for foreign manuscripts.

## Synchronization

The operative spec is mirrored, condensed, in
`config/agents/subagents/nlpatch.md` so the blind subagent is self-contained.
Keep the two in sync.
