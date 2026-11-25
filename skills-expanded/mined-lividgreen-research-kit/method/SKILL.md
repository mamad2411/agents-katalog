---
name: method
description: Method rules for a project that writes documents and makes claims — how to answer a review, what to call things, what a document holds and when a result enters one, what counts as evidence, what to check before pricing a piece of work, how to change a target honestly when a wall is hit, how to work with the project's owner, and, where the project keeps a machine-checked library, how a formal target is picked and scoped and what a wall is. Use before a design round, a list refresh, a review pass, a registration or the pricing of a formal target. The rules come from one research programme, and the incidents that earned them are not part of the kit.
license: Apache-2.0
compatibility: No tooling; read before design, review and target changes.
metadata:
  version: "0.12.1"
---

# Research method

These are one project's rules, earned over a research programme that pairs written documents with a machine-checked library; each is contestable, a project adopts them by installing this skill and keeps what fits, and the incidents behind them stay in that programme's log, which is not public.

## Review

- A structural pass and a correctness pass find disjoint defect classes; a section is reviewed only after both.
- The citation discipline applies inward: open the exporting statement before citing it, even when it sits three paragraphs up in the same file.
- A correction reaches every summary site — the headline, the abstract, the registry, the companion prose, a library docstring that summarizes the result — not only the detailed site where it was found; the project binds the list.
- A scope qualifier sits on the claim, not on the sentence's conclusion.
- A negative-coverage sentence ("nothing in this work does X") is a claim about every document at once; its counterexample is usually a companion's own headline result under a hypothesis — and every landing re-reads such sentences for the landed result's kind, since no gate does.
- A sentence found false of the artifact is corrected by the session that finds it, at its exact size, in that session; it is never put to the project's owner as a choice. The owner decides scope and significance; whether a false sentence stands is not a decision. A project whose instructions file says the owner is asked before any correction has opted out, and the session then puts the sentence, its evidence and the correction to them instead.
- Crediting the work with settling a NAMED external result requires reading that result's primary source first — its quantifiers, its resources and the author's own caveats; a partial match names the special case proved and the gap; the `attribution` skill runs the check.
- A consistency audit across documents is the `audit` skill, and argument-level scrutiny the `scrutinize` skill; answering a review, triaging a review of a public artifact and an outsider pass follow [`references/reviews.md`](references/reviews.md).

## Terminology

- An object the literature names is called by that name, verified at a primary source before it is written; a term of the project's own stands only where no established one exists, defined once where it is introduced.
- One invented term is never replaced by another invented term.
- The rule reaches names in code: a declaration, a file or a namespace carrying a term the literature names otherwise is renamed to the literature's.
- A dependency graph has sources (what depends on nothing) and sinks (what nothing depends on); a directory or module tree has roots and leaves; the two vocabularies are not mixed, and "leaf" never means light or small.

## Documents

- Where the documents form a dependency graph, a core document never cites the sink: a citation of the capstone that imports the others runs against the direction; if the citing sentence is load-bearing, the documents are reorganized — the content moves to the capstone or the dependency is cut — and that is put to the owner; if it is not, the citation goes.
- One document holds a class and its generalization, never two siblings; when two documents fit a result, the later one in the graph takes it and cites the earlier, or the statement is split so each part lands where it is owned.
- Where the project has no rule of its own, a landed result enters a document when it:
  - changes a sentence the document already has — settles or narrows a stated open, falsifies a negative-coverage sentence, closes a gap a boundary names;
  - is a step on an open the document names, registered as a step with one sentence saying how it falls short;
  - is a statement over a class a reader recognizes that continues a section's own story;
  - is interesting on its own, registered as a labelled side story.

  Otherwise it is library content, described where the artifact is described and registered in no document.
  The form is a specific numbered result with its rows and boundary, never a thesis rewrite, and the headline gets one sentence at most.
  The landing names the clause that fired, or why none did, so that reversing it costs the owner one word; the owner is asked first only when the result needs a new section or document, changes an abstract or a headline, or meets a clause while a clear reason keeps it in the library.
- A published document points only at what its reader can open: no path into the development repository, no record id, no note that scripts are kept there; the development's computation may be stated as provenance, which asks the reader to open nothing.
- A document for an outside reader posts fresh, with no "updated since" note and no version diary; the development dates in an artifact's rows are provenance and stay.
- A class claim is kept apart from an instance claim, and each sentence says which it makes.
- A document reviewed whole is iterated by draft, rigorous review and full rewrite, not by incremental patches.
- No file names a version or a version DOI except where the version is its subject — release notes, a changelog, a comparison, a dated record — and the rest point at the releases page and the concept DOI, since a version DOI exists only after its tag and is always one behind.
- A release's title and notes say what the release changes and nothing the front page already promises, and a commit names the version only when it is the bump.

## Evidence

- Where the work needs something found out that the records do not hold, a question is minted first, before the act that finds it out (a probe of the machine, a read, a search), and then goes the usual way, drawn and answered by a finding with its evidence; the question "what are the parameters of this computer?" comes before the probe of the machine, and the figures are the finding's, never prose in another record's body.
- A probe is owed by a claim's shape, not by a clock: a committed self-asserting check is owed where a claim is load-bearing (a statement, a row, a decision or a design resolution rests on it), is established only numerically and is not re-derivable in a line, and always for a sentence characterizing what remains open; none is owed to re-confirm a machine-checked statement, for a sanity check no record cites, or for arithmetic a reader redoes in their head.
- A counting or closed-form claim gets its planted-defect probe in the same round it is made.
- A check asserts both that it bites where it should (a planted defect fails it) and that it passes where it should; an instrument that cannot fail tests nothing.
- A refutation is a counterexample, and a counterexample outlives the statement it killed: it is kept at the parameters that break it, a standing candidate for a checked guard beside the reformulated statement.
- Code in any language is the search stage and the checked artifact is the result: the script located the witness, and the checked statement is the witness.
- Unverified code is not evidence; a numerical check a reader would need is an argument for checking it mechanically, not for shipping the script.
- A probe that ports a machine-checked statement is checked against the prover, never the other way round: where the two disagree, the port is what broke.
- Suspect the bound, not the witness: a residue that keeps coming out wrong is a fact about the bound until the bound has been pushed.
- A row or a remark about a checked artifact is written from the landed artifact, never from the design record that commissioned it.
- A record paraphrase can name the wrong referent; agreement between two citations is not verification — open what they point at.
- A whole-tree count (declarations, guards, modules) is a tree-derived figure with two homes, where a check recomputes it: the artifact's own falsifiable claim with its recount method, and the front page its consumers read; everywhere else states it without numerals and points there, and no memory holds it.
- A report's count is recounted at the tree before it enters a row; a handback's "cannot be done because Y" is verified like its landed claims; a fetched summary of a PDF is a small model's reading, not the source.
- A defect that recurs after it was written down gets a mechanical check, which is when a lesson stops being prose.
- A declaration name in a document is a claim that the declaration exists with that statement; a document never names a declaration in order to say it does NOT exist, since the check that resolves names cannot tell assertion from denial.

## Before pricing a target

- Check what structure the target already carries before pricing a replacement into it.
- A label or category tag is a filing address, not a statement.
- An item's own pointer can be the stale thing, or born wrong.
- Existence is the cheap half: check what CONSUMES the object before pricing its existence.
- Checking a target's inputs is not checking what the project already derives from them.
- An equivalence proved about a hypothesis does not discharge it.
- When a bill misbehaves, ask of each term who holds it and whether it is a count or a clock.
- A parking reason can be priced against the wrong object; the cheapest check is the document's own definition.

## Changing the target honestly

The freedom is of route: on a wall, change the statement, the definition, the object or the currency to reach the goal.
These invariants keep that honest.

1. **The original question stays on record.** Beside the result, write the statement before, the statement after, why, and whether the original is now settled, still open or refuted. An original open is never deleted by a change; it is answered, re-parked with the new reason, or marked refuted.
2. **A change is not a settle.** A result proved after a change is registered as a result about the changed statement; its status label, its verification row and every summary site name that statement, and no sentence claims the original was settled unless the change is shown equivalent or stronger.
3. **Weakening is disclosed where a reader looks first.** A change that adds a hypothesis, narrows a class or swaps a currency is carried at the headline, the abstract, the status label and the contributions, not only in an appendix row.
4. **Every consumer is swept in the same session.** A changed definition or statement reaches every document, registry entry and docstring that cites it before the commit; the `audit` skill checks this, over the corpus the project names.
5. **Evaluation is fixed before the result.** Probes, sweep sets, kill criteria and named hypotheses fixed for a round are not altered after seeing its result; changing them opens a new round with its own record. A probe that now passes because the statement moved is re-derived against the moved statement and says so.
6. **A change that drops the interesting property is a finding, not a route.** When the provable form loses what made the question worth asking, record "the natural statement is unreachable or false; the provable form is X" and keep the natural statement open.
7. **No change to please a check.** A statement is never weakened because a cited result lacks a mechanical proof, and never strengthened in prose beyond what the artifact proves; a named hypothesis with a citation is the honest form.

## Working with the owner

- A choice among options goes to the owner through the agent's question tool where it has one, with its options and one recommendation first, never as a prose list; an item the owner owns, and a call the agent is still unsure of after the test below, is asked before the agent decides alone, in the turn the agent meets the decision.
- A question carries what the decision rests on, since the question tool's dialog covers what the turn wrote before it: the facts, the options with what each leads to, and the recommendation are in the question itself.
- A review of content, a text to read or a design to change, is asked in prose and answered in the person's own words; the question tool is kept for a choice among options.
- A decision still open at the turn's end becomes a task in the owner's deck whose title names the decision, and the card that waits on it is blocked on that task; the log's State paragraph names the task, and the decision is never left as prose alone in a record's body or the log.
- The owner's items are what only they can do (a send, a registration) and what only they should decide; the rest is the agent's.
- Before a question is put to the owner, or a piece of work handed to them as their decision (in the flow, a task in their deck), the agent asks whether a test settles it: what each option does for the goal, or whether the object meets the criterion as written.
  Where there is such a test the agent runs it, decides, and records the decision with the test; what is correct is never the owner's choice.
  A check that stops at a term the criterion leaves open makes a question of that term.
  What goes to the owner is the goal and the directions, an outward act, and options a test leaves apart that lead to different programmes, each put with what it leads to.
- A design answer is a recommendation, its consequences and the alternatives, briefly, with the evidence after.
- A question the owner cannot answer but may postpone, the answer being the research's and the working value the owner's, is neither closed nor answered by that value; it takes the `flow` skill's four steps, in "Questions in practice":
  the owner's decision is written where the project keeps its own word;
  a finding says what is true, the working value and whose decision of which day it is, with `stated:FILE#anchor` as its evidence and the question in `--ref`, no `--answers`;
  the question is parked, its reason naming the finding and its revival what reopens the search;
  when the answer lands, its finding answers the question and the working-value finding is removed.
- A ruled decision is not put to the owner again: executing a ruling is the agent's.
- Reversible options are paths, not forks: take the one of highest benefit and go; a wall is a pivot, not a question.
- The owner's test is applied literally: a binary test as given, with the borderline cases listed, never widened into a category of the agent's own.
- The owner's statements are captured as they are made — an idea in their words with its date and source, a ruling where the project's rules live, a preference in the agent's memory — and a task is minted when its shape is already there.
- A record is written for a reader with no other record open: its title says what the card is and its summary explains it, by the `flow` skill's part "Writing a title and a summary".
- The owner's own ideas get the citation discipline: checked against the exporting statements before they are agreed with.
- Publication is the owner's alone: no session schedules, proposes or sequences it, and nothing is sent anywhere without the owner's word for that item.
- Messages are terse and deliver results: no line counts or statistics in a message, a commit message or release notes, and the framing of a result's significance is the owner's.
- Saving tokens means fewer subagents, not less work; a cold read goes to one fresh subagent, never a fork of the session, since the cold reading is the point.
- A pause means starting nothing new and reporting what runs; an unpause resumes from the records.
- A failing prose linter means the prose is wrong until shown otherwise: the prose is fixed, unless extending the linter's vocabulary is the right call.

## With a prover

Where the project pairs its documents with a machine-checked library, these rules decide which statement is proved next and when a target changes; the prover session's own mechanics — the handoff, the landing, the sweeps — are the `formal` plugin's.

- Statement-first: the statement is designed from the document's actual text, opened, never from memory.
- Ties among formal targets are ordered by: what a document needs; statement readiness; the kind of effect on the document; elaboration risk; then how many rows move and how big the piece is.
- Check computability of what a construction reads before commissioning it; a search over an infinite object is a wall, not a target.
- A generic piece and a specific piece of one bundle carry the same quantification; a bundle lands sink-first — the composite statement nothing in the bundle depends on, with its predecessors' statements as hypotheses, read back before any predecessor is proved — and each predecessor is computed at its edge parameters before dispatch.
- A refute-first computation at the smallest parameters precedes every handoff; a theorem with two or more hypotheses is commissioned with a non-vacuity witness beside it.
- A wall names its kind: expressivity (the statement cannot be expressed), elaboration (the prover cannot handle the term), missing-upstream (a needed library result is absent), misstated (the statement was wrong); a wall fitting none is a new kind, recorded.
- On a wall, change the target under the invariants above; another attempt that restates the object is tried before the wall is recorded as such.
- A repair loop against a failing build is bounded: three attempts, then stop and report the wall honestly with its error blocks trimmed to what matters.
