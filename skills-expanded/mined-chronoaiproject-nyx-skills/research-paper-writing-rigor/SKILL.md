---
name: research-paper-writing-rigor
version: "2.0"
description: Draft, revise, or review focused research manuscripts with complete arguments, verified literature, and direct prose. Remove defensive wording and repeated summaries while preserving exact claims, attribution, authors' voice, and reproducibility. Especially useful for mathematical, theoretical-CS, and computer-assisted papers, short notes, and coauthor revisions; adaptable to empirical papers. Use for manuscript work, not outreach campaigns or standalone theorem proving.
metadata:
  category: tool-based
  tool-list: [filesystem, shell, web-search]
  tag: [research-writing, mathematics, scientific-writing, reproducibility, peer-review]
  depends-on: []
---

# Research Paper Writing with Rigor

Write a paper that lets a knowledgeable reader see the result, understand why
it follows, identify what is new, and obtain the evidence needed to check it.
Use direct language for established facts and precise uncertainty for open
questions. A short note earns its concision through a focused question, removal
of repetition, and clear organization. Every core conclusion it retains needs
a complete argument.

## Primary principle: make the completed contribution visible

The paper's main job is to explain what the authors accomplished, how they
accomplished it, and why it matters. Organize the abstract, introduction, result
summaries, and conclusion around those completed contributions. Give supported
results their full strength: "we prove", "we construct", "we establish", and
"we formalize" are appropriate when the evidence warrants them.

Excessive modesty can misrepresent the work as surely as exaggeration. Remove
"merely", "only a modest step", "we attempt to", or "may suggest" when they
weaken an established result without a scientific reason. Preserve qualifiers
that express actual uncertainty, statistical evidence, or mathematical scope.
Neither routine attribution nor an unresolved extension requires an apology
for the present result.

Evaluate a proposed caveat by the reader's needs: would omitting it materially
change the claim's meaning, evidence level, applicability, or attribution? If
yes, state it precisely at the relevant point. If no, remove it or move useful
operational detail to the supporting documentation. Do not invent hypothetical
claims a reader might make merely to deny them. Avoid opening or closing a
contribution paragraph with a catalogue of things the paper does not do.

Use evidence checks to earn confident writing. A review finding should lead
to the strongest accurate statement supported by the work; default hedging is
not the goal. The final reader should remember the result and its mechanism.

For a new draft or substantial revision, apply these checks in order:

1. State the question and main result in the first paragraph of the introduction;
   do the same within the abstract if there is one. Give the actual scope, using
   a faithful plain-language version when formal notation must come later.
2. Keep material that answers the question, proves the result, explains its
   mechanism, or places it in the literature. Cut unrelated claims and repeated
   narrative across the abstract, introduction, body, and conclusion.
3. Give every retained mathematical conclusion a complete proof or a precise,
   checked reference with its hypotheses matched here. Remove an unsupported
   conclusion from the results; hedging cannot supply its missing argument.
4. Replace routine defensive phrases with the supported statement, attribution,
   or one relevant open question. State mixed verification scope once in a
   status sentence or table; preserve the hypotheses and finite premises in
   the statements that need them.
5. Cover the literature systematically. For a short paper, plan 12–20 or more
   relevant, verified references; follow the coverage and verification checks in
   [literature-and-citations.md](references/literature-and-citations.md).
6. Finish with a read-aloud pass for rhythm, then recheck mathematical meaning
   after any sentence changed for fluency.

Read [focus-and-structure.md](references/focus-and-structure.md) for the scope
test, repetition audit, 2–4 page note and short-paper templates, and final
acceptance checklist. Apply these to the requested passage for a local edit;
do not turn it into an unsolicited full-paper audit.

## Choose the requested work

- For a sentence or paragraph, give the concrete revision and only material
  explanations. Do not create a manuscript-wide audit or release workflow.
- For drafting or substantial revision, read the current source, relevant
  results, and coauthor comments before editing. Work from the actual latest
  version, not a remembered draft or stale line numbers.
- For review only, lead with findings and locations; do not silently rewrite
  files. Distinguish a demonstrated error from an unresolved concern.
- For a submission package, read [release-and-reproduction.md](references/release-and-reproduction.md).
  Editing prose alone does not authorize repository publication, journal or
  arXiv submission, messages to others, or shared CI changes.

Adapt the structure to the discipline, venue, and requested length. A short
mathematical note need not have IMRaD sections, ablations, a teaser figure,
or an experimental-performance narrative. Follow explicit user instructions
and applicable venue requirements over these defaults.

## Learn the discipline's written language

Treat academic style as a set of field-specific explanatory choices: which
objects are named, what can be assumed, where an argument needs a calculation,
and how results are related to earlier work. Formal-sounding vocabulary alone
does not supply these choices. For substantial drafting or complaints about
generic or machine-like prose, read
[discipline-and-voice.md](references/discipline-and-voice.md).

Before writing technical content, search recent relevant papers in the field
and, when applicable, the correspondent's own papers. Read the relevant passages
and adopt their standard terms and notation; when writing to an author about
their paper, use that paper's notation. For small edits, reuse already checked
sources when sufficient. Learn the field's organization and level of explanation
while preserving the argument and authors' voice. Do not imitate an author's
identity or copy distinctive phrases.

Use established field terms; do not coin a name when a standard term exists.
If a new term is unavoidable, define it in one sentence at first use and relate
it to the standard term or object. Prefer direct theorem statements; add an
optional theorem label only if readers will use it. Avoid naming every
observation or importing internal research labels. A proof paragraph should
expose the inference that makes the conclusion follow; editing words cannot
replace a missing inference.

Judge the revision by its usefulness to a specialist, mathematical fidelity
and fit with the authors' prose. Do not optimize for detector scores, invent
human drafting history, introduce errors or slang to seem human, or promise
that the text's origin will be undetectable.

## Establish the argument before polishing

Identify the question, main result, key obstacle, proof or method mechanism,
closest prior result, and remaining uncertainty. For long work, use a short
private outline or claim-source map if it helps; reuse existing records.
Do not insert drafting labels or audit tables into the manuscript by default.

For substantial mathematical-note drafting, coauthor revisions, or feedback
that proofs are too compressed, read
[proof-completeness.md](references/proof-completeness.md). Check the actual
inference chain before shortening it: changes of representation, normalization,
dimension, summation order, and boundary cases need their mathematical reasons.
Keep the main argument readable and place longer necessary derivations in
precisely referenced appendices. Length is a constraint on scope and exposition,
not evidence that a proof is complete.

For substantial revision, check which auxiliary results and appendices the
main argument actually uses. Keep an independent proof or example when it
provides a distinct result, method, obstruction, or explanatory benefit
worth its length. A consequence already supplied by the main theorem may
need only its deduction. Before removing material, preserve every dependency
and update the abstract, introduction, cross-references, and bibliography.

For each central claim, know its scope and supporting evidence. Preserve
quantifiers, initial indices, exceptional cases, hypotheses, and constants.
Separate new mathematics from a new proof, a formalization, an implementation,
and an empirical observation. Do not equate an agent's agreement or a finite
prefix match with an all-input proof. Read
[argument-and-evidence.md](references/argument-and-evidence.md) for proofs,
computer-assisted results, literature placement and application, or mixed
verification. Its literature review includes a dedicated independent referee
pass and a hard documented search gate before calling a manuscript or short note
ready.

Call something a "counterexample" only when it falsifies a precisely quoted
statement: quote that statement, check its hypotheses, and identify the failed
conclusion. Otherwise call it an example or illustration and say what it shows.

If support is missing, complete the argument, prove a narrower statement, or
remove the claim and its dependent assertions. Keep a conjecture or open question
only when it serves the paper, clearly separated from established results.
Do not retain an unsupported conclusion by adding "may", "appears", or a
disclaimer. Do not invent proof steps, references, numbers, author actions,
model identities, successful checks, or public artifact links. A blocked claim
need not stop independent writing work on supported results.

## Write as a research paper

1. Lead with the mathematical or scientific content: what is established and
   the mechanism that establishes it. State the contribution specifically and
   at its full supported strength; keep it as the paragraph's main message.
2. In the introduction, say why the question matters before the proof: the
   difficulty it resolves and the consequences the result makes available.
   Give each paragraph a clear job. Check the sequence of paragraph messages
   before polishing sentences. Connect definitions, arguments, evidence, and
   consequences in the order a reader needs them.
3. Use precise verbs and stable terminology. Prefer an identifiable object,
   such as "the correction automaton E", to "the supplied correction".
   Avoid internal project language and chronology unless they matter to the
   result. Repeating a defined term is preferable to a misleading synonym.
   Check what each symbol denotes, its domain, and its normalization. Make
   the map and measure clear when moving between representations or writing
   integrals. Define a local use of a term that also names a different
   standard quantity in the field.
4. Place the contribution in the wider literature and credit the specific method
   or theorem where it is used. Replace repeated novelty denials with positive
   attribution and a clear statement of this paper's extension. A citation must
   support the exact attached claim.
5. Separate indispensable limitations from defensive repetition. Keep a
   qualification beside a claim if omitting it would change its interpretation;
   consolidate verification status in one sentence or table. Use a limitations
   section when it has substantive content, not as a ritual closing paragraph.
6. State open problems as open problems. Distinguish an unproved identity,
   minimality, attainment, asymptotic behavior, and a dynamical interpretation.
   Do not replace "not established" with "false" or "unnecessary".
7. Put operational details where readers need them: essential proof evidence
   in the paper or a precise accessible reference, reproduction commands and
   detailed environment records in the supporting package. The main text
   should not become an account of internal orchestration or mail handling.

Read [editing-patterns.md](references/editing-patterns.md) when tightening prose
or applying coauthor comments. Its examples are decision patterns, not mandatory
sentences to paste into every manuscript. Do not mechanically ban passive voice,
hedging, repeated terms, or punctuation that serves the argument.

## Apply comments with judgment

Classify material comments as correctness, attribution, scope, reproducibility,
or presentation. Check technical replacements against their surrounding proof;
do not infer validity from the reviewer's authority alone. A shorter sentence
must retain the witness bounds or hypotheses that make it true. Verify removal
of an algebraic assumption with exact reasoning where feasible.

A precise citation can replace a proof of a standard tool. Read the cited
statement and match its domain, topology, boundedness or integrability,
and normalization requirements to this application. Keep the instantiation
and the conclusion used here explicit. When shortening local reasoning,
retain the bound or hypothesis that licenses the next inference.
When a known existence theorem supplies an exact optimizer, a proof can
often use that optimizer instead of an approximate one with a split error
budget; verify the theorem's hypotheses first.

Implement supported changes when revision is requested. Explain disagreements
with evidence and propose a precise alternative. When a coauthor's supervisor
comments, address every point concretely in a change log: comment, manuscript
location, change or reasoned response, and verification or unresolved issue.
For other reviews, keep a compact disposition record when the number or
importance of comments warrants one. Keep this log outside the manuscript;
do not require a separate approval checkpoint for every reversible edit.

When following several revisions, distinguish the received draft, the
corrected draft, and any later published version. Track important passages
by their mathematical content as numbering and notation change. Recheck
that previously accepted corrections remain effective; an equivalent
reformulation may preserve a correction without preserving its wording.

For feedback about formulaic prose or excessive theorem labels, read the
comment and affected passage together. Identify the concrete defect, revise
the passage, and extract a reusable lesson only if it applies beyond that
example. Recheck the rendered statement and its proof dependencies; changing
a heading alone does not address missing explanation. Use the focused review
in [discipline-and-voice.md](references/discipline-and-voice.md).

## Short result notes for a correspondent

A short note answers one reader's question first: the author
whose open problem, conjecture or request it addresses. Read their exact
statement (paper version, section, equation) and answer that; move anything
else to one closing remark or cut it.

Follow the requested or venue length rather than imposing a fixed page range.
Write the complete argument for the retained claims before compressing its
presentation. Under a tight page limit, remove secondary claims or use allowed
appendices before deleting a necessary inference. Standard tools can be cited
with their applicable hypotheses; a central new step needs a written proof.

- Before writing, list each claim with its status: proved here, known (exact
  source), known in a special case (state precisely what is new), computed
  (finite range and method), or open. Only proved claims become theorems.
- Title states the mathematics, never "Response to X". Use the byline and
  affiliations the task supplies. Abstract gives the main statement exactly
  and its scope in three to six sentences.
- Introduction: the question as the source states it, the answer, its
  relation to known results. Then setting in the source's notation and results
  with complete proofs. Include examples, certificates, or open problems when
  they add information; finish with references. Use the templates in
  [focus-and-structure.md](references/focus-and-structure.md) at the requested length.
- Keep an attribution ledger for a correspondent-facing note: identify which
  results are proved by the present authors, which are independent checks of
  another author's result, and which are direct consequences of cited theorems.
  Describe the latter two as verification or consequences, never as advances.
- Computation supports but never replaces a proof of an all-parameter
  statement; give finite ranges explicitly. Never cite your own unpublished
  drafts; fold what is needed into the note. Credit the correspondent's
  question, examples, corrections and counterexamples plainly in ordinary
  prose, for example “in correspondence, 19 October 2026”; do not create an
  email bibliography entry. Never cite or mention "private communication",
  including hyphenated variants and self-certifying sentences such as
  "no private-communication references".
- Keep process and evidence logistics in a repository README, not the note.
  No local paths, no tool or pipeline narrative, no long hash strings.
- Compile, inspect every page, recheck every number against its computation,
  and record what is proved, computed and open, plus any citation that could
  not be verified.

For delivery of a research note by email, package one merged PDF named
note_YYYYMMDD.pdf and one dated source ZIP (for example
verification_YYYYMMDD.zip), with total attachments <= 5 MB (5,000,000 bytes).
Fold every meaningful result into that manuscript or note. The coauthor package
has one deliverable: the manuscript PDF and at most one source archive. Put
verification material in the public repository at a pinned link instead of
adding separate result notes or extra archives.
The ZIP contains text/source and concise readable outputs only; exclude binary
files (.bin, .dat, .npz, .gz, .pkl), third-party copyrighted PDFs, and internal
RESULTS-r*, REVIEW-r* and NOTES files, including nested copies. The merged note
PDF is the document-format exception. Omit regenerable generator output even
when it is text: give the exact command and output SHA256 in the package README.
Large data belongs in the authors' designated public data repository;
use a verified commit-pinned link and do not invent or publish artifacts without authority.
Check final PDF text, source and archive members for long digit runs, including
space/hyphen-separated digits, that pass Luhn and trigger institutional DLP.
Use exact symbolic forms, concise scientific notation or pinned public data
links to keep those runs out of delivered material.

When asked to review such a note adversarially, recompute independently,
read each proof line by line, verify every citation against the primary
source, look for scope overreach and missing hypotheses, deliver a corrected
version and a verdict: correct, fixable gaps (listed), or wrong at a named step.

## Verification, authorship, and AI use

Report the actual verification scope: which statements were proved, which were
kernel checked, which computations ran, and which results are merely reported
by another author. A successful build is evidence about a specific source
version; it is not validation of all prose or a fresh independent review.

When the authors have a prescribed AI-use sentence, use it verbatim; do not
substitute another sentence or add a process narrative. Do not attribute that
use to other collaborators. Keep detailed provenance and
actual verification scope in internal research records. Do not claim every
proof was kernel checked when only a subset was formalized, or imply every
coauthor reran the tools or approved a pending draft. Answer direct process
questions truthfully. If a venue requires additional disclosures, flag the
specific requirement separately rather than silently changing this sentence.
Do not insert these authors into unrelated manuscripts; establish their actual
authors and applicable disclosure requirements from the task.
Keep data/code availability in a separate statement; see
[release-and-reproduction.md](references/release-and-reproduction.md).

Distinguish permission to use AI in research from permission to use AI-written
submission prose. If the selected venue requires the actual wording to be
human-authored, supply mathematical derivations, source checks, an outline and
comments on the humans' text in the permitted roles. Keep model-written
examples as working material; they do not become human-authored by paraphrasing,
translation or a final approval pass. Apply this boundary to that venue rather
than prohibiting manuscript drafting for every other venue.

## Finish proportionately

Before sending or submitting a draft, complete the independent terminology and
readability referee pass in
[discipline-and-voice.md](references/discipline-and-voice.md#check-the-result).

Check that the abstract, introduction, theorem statements, tables, conclusion,
and verification description agree on the central claims. Read the abstract
and conclusion once just for emphasis: do they make the completed result and
its significance clear, or does a list of exclusions obscure them? Correct
unnecessary hedging as well as overstatement. Run the cross-section repetition
audit and final read-aloud pass in
[focus-and-structure.md](references/focus-and-structure.md#final-read-aloud-and-acceptance-pass).
For changed LaTeX,
compile the affected deliverable when available and inspect relevant rendered
pages; report unavailable validation honestly. Do not rerun expensive formal
jobs solely for prose changes unless changed claims or project rules require it.
Respect the configured validation machine and existing repository gates.

When assessing concision, compare like scopes: report whether the reduction
comes from removed auxiliary material or from a shorter treatment of the
retained argument. State the counting convention when lengths matter, and
check any reported page count against the actual rendered artifact.

Deliver the requested prose or artifact first, then a short account of material
changes, completed checks, and remaining decisions. Keep internal checklists out
of the publication text. Do not promise acceptance, universal novelty, or that
all possible objections have been eliminated.

For provenance and deliberate departures from upstream writing skills, read
[sources.md](references/sources.md). This skill contains paraphrased lessons
from a private mathematical coauthor review, not the correspondence itself.

## CHANGELOG

- 2026-10-29 — 2.0: make focus, cross-section deduplication, complete support
  for retained conclusions, and removal of defensive boilerplate explicit
  acceptance checks. Add note/paper templates, systematic literature coverage
  with a 12–20-reference short-paper target and index verification, and a final
  read-aloud pass. Synthesize nine public writing skills and guides with pinned
  source attribution; retain the proof, authorship, and reproduction guidance.
- 2026-10-29 — 1.10: make proof completeness operational for compact notes:
  explicit transformation and coefficient checks, domain and dimension tracking,
  justified boundary limits, equality arguments, and precise appendix links.
  Preserve coauthor scope and remove the fixed short-note page range.
- 2026-10-29 — 1.9: add a hard, documented literature gate covering recent
  searches and overlap checks; require minimal manuscript packages with a
  pinned public verification link; and separate our results from independent
  checks and cited consequences in correspondent-facing notes.
- 2026-10-19 — 1.8: use the authors' prescribed AI sentence verbatim, prohibit correspondence citations and self-certifying mentions, and require small dated note/source packages with reproducible public data links, no internal process files or binary data, and DLP digit checks.
