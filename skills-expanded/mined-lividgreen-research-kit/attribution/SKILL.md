---
name: attribution
description: An attribution check — every sentence crediting the project with proving, settling, bypassing, re-deriving or being first at a named external result, held to that result's primary source on four axes (the resource measured, the quantifiers, the scope and the author's own caveats), each verdict recorded on the work's card as an extract; a table of verdicts, the documents edited by nothing, after which each overclaim is corrected. Use as `/research:attribution`, optionally with documents (`/research:attribution the survey`), before a document goes out, and after an edit that adds or rewords a claim about an external work. Runs the `library` skill's commands; the project's instructions file names its documents and its claim words. When the person says 'attribution', 'check the attributions' or 'attrcheck', they mean this skill — call it every time, even if it ran earlier in the session, and take every step.
license: Apache-2.0
compatibility: The `library` skill beside this one, whose script it runs; a kept or fetchable copy of each primary source.
metadata:
  version: "0.12.1"
  requires: library
---

# An attribution check

Crediting the work with settling a named external result requires reading that result's primary source first: its quantifiers, its resources and its author's own caveats; a partial match names the special case proved and the gap.
`library check` confirms that a cited work exists and is tied to its entry; this check confirms that what a sentence says of the work is what the work states.
`library …` below is the `library` skill's `scripts/library.py`, run by its path from the project root as that skill says.

## The project's part

The claim shapes `library claims` matches are `[claims] shapes` in `library.toml`, where a project with a prover adds its own words.
The setup (`/research:research-init`) forms with the person the documents a reader sees beyond those `library.toml` binds (a blog, a front page), and which documents a review may correct in the session and which it reports and asks the person about first, and writes them under a `### Reviews` heading of the instructions file, inside its `## Records and method` section; the check reads them there.
Where the instructions file has no such part, or it does not say what this review needs, the review says so and advises `/research:research-init`, which forms it with the person in a project set up before as well; where only this review's part is missing and a full setup is not needed, it asks the person for that part in place and, on their word, writes it where the setup would.
The documents of a run are what the person gives with the command, and otherwise the bound ones with those the instructions add; the report says which it took.

## The steps

1. **The worklist.**
   `library claims` lists every claim-shaped sentence of the bound documents that names a carded work, with the extracts the card carries, and `library claims --uncovered` those whose card carries none, which are unverifiable from the library until the work is read and an extract written.
   The list is a net, not the end of the worklist: it reads the bound documents only, and sees a work only where the sentence carries the first author's surname and the year, so the documents are also read for these shapes; a document `library.toml` does not bind lists nothing under `library claims`, and is read for them by hand:
   - a verb of settling on a named result — proves, resolves, settles, establishes, closes, answers, bypasses, refutes — a named conjecture, theorem, problem, bound or impossibility;
   - a change of resource, proving in one measure what the author stated in another (time for space, a size for a count), where an overclaim most often hides;
   - an identification, "the external result is our Theorem N";
   - a first or a novelty, "the first proof of X", "to our knowledge none precedes";
   - a re-derivation, where the direction is checked: a necessary condition used as a sufficient one is the usual sibling flaw.

   The document's references name the primary source of each; the worklist is the sentence, its file and line, the external result, and its source.
2. **Each claim against the primary source, not a paraphrase.**
   `library show KEY` first: an extract on the card says what the work states at a place, its author's caveat, the rule on what may be claimed, and the date and edition it was checked in; where one covers the sentence, the sentence is compared with it.
   Where none does, the result's own statement is read — `library fetch KEY` keeps a copy, `library page KEY N` and `library find --text WORDS` read it — and the extract is written in the same pass (`library extract KEY ID --at "Theorem 4" --quote "…" --caveat "…" --rule "…" --edition "…"`); where this reading goes further than the grade the card records, it is recorded (`library read KEY --grade parts --what "…"`), never a grade below the card's.
   A report or a summary that quotes the result is a lead, never the source; where the primary source cannot be obtained, the verdict is UNVERIFIABLE and is never passed as faithful.
   Then the four axes:
   1. **The resource.** The quantity the sentence measures is the one the source measures; a change of currency is an overclaim unless the sentence says so and names the gap.
   2. **The quantifiers.** The logical form matches: for-all-exists against exists, an upper bound against a lower one, necessary, sufficient or both, generic against universal.
   3. **The scope.** The domain, the hypothesis class and the exceptions to a generic claim are the source's, and the sentence says where it covers less.
   4. **The author's caveats.** A vacuity, a scope limit or a condition the source states and the sentence omits is an overclaim.

   Only where the works are many, each verification, being independent, may go to one fresh subagent per work reading its own primary source; its verdict comes back with the place and the quotation, which the session sees in the kept copy before the extract is written, since a subagent's report is a candidate and never a read.
3. **The report, the documents edited by nothing.**
   A table: the sentence with its file and line, the external result and its source, the axis of the mismatch, the verdict, and a reframe.
   The verdicts are faithful, OVERCLAIM (naming the axis and what the source does state) and UNVERIFIABLE.
   An overclaim's reframe claims what was established — the premise, the special case, the one direction — names the gap, and never claims the whole named result.
4. **Every verdict on the work's card.**
   A verdict of faithful or OVERCLAIM is the extract step 2 compared or wrote, never a second one beside it: the place read, the work's words quoted or restated, its author's caveats, and under `Rule:` the verdict with what may be claimed; on a re-check the extract is replaced (`--replace`) and a dated note says what changed (`library note KEY --note "…"`).
   An UNVERIFIABLE verdict has no place read, so it is a dated note on the card saying what could not be obtained, never an extract.
   The cards carry the verdicts between sessions; `library claims --uncovered` lists only the works whose card carries no extract at all, so a sentence at a work that has one is still compared with it, sentence by sentence.
5. **Then the corrections.**
   After the report, each overclaim is corrected in this session at its own size, the reframe written where the sentence stood and at every summary site that restates it; a document the project's part names as one a review reports and asks about first gets the sentence, its evidence and the reframe put to the person instead.
   This check runs again over the corrected sentences and `library check` with the project's gates after the edits, and the `audit` skill too where the reframe changed a statement other documents cite.

## Traps

- A cited theorem or equation number is checked to exist in the edition cited, not only the work: editions number differently, and an extract records its edition.
- A quotation typed from a rendering may not be the source's words; a failing anchor is read at the kept text before the extract is blamed.
- A claim that a result is absent from an upstream library, or present in it, is checked at the upstream's committed state (`git show HEAD:<path>`, or the tag the document cites) or at the live upstream, never at a working tree, which may carry the project's own uncommitted patch and read the claim's negation.

**Output.** The documents taken, the table of verdicts, the extracts written or replaced, the corrections made, and what was asked or captured.
