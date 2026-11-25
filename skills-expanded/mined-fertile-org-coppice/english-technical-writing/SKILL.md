---
name: english-technical-writing
description: Use when drafting, reviewing, or rewriting English prose in this Coppice repository — root READMEs, the marketing site, contributor docs, user docs, or UI copy. On a style pass, leave commands, keys, URLs, permissions, and locked positioning unchanged. Not for other languages, product behavior, or end-user agent skills.
---

# English technical writing

Accepted for Coppice repository authoring. The criterion used here is original publication more than six years before the research date: each source's first publication is strictly before 2020-11-07. That criterion does not require an immutable archived snapshot of every sentence.

The researcher and an independent reviewer each read all 30 current original textual bodies in full. The articles are originally authored English, not translations. This is a cross-author editing guide for Coppice prose. It is not a set of native-speaker biographies, and it is not 30 verified untouched pre-generative-AI texts. Later revisions mean some current wording is not proven to predate 2020. EN17 and EN24 are excluded from rule support because their version risk is unresolved. A source supports a writing choice. It does not validate that source's commands, security steps, or product claims for Coppice today.

Provenance sits beside this skill: [corpus-manifest.md](corpus-manifest.md) and [review-evidence.md](review-evidence.md). Full source articles are not in the repository.

## Where this applies

Use this skill for English in this repository:

- Root [README.md](../../../README.md)
- English pages under [website/](../../../website/)
- Contributor docs under [docs/](../../../docs/)
- English UI strings under [web/](../../../web/)

It lives in `.agents/skills/english-technical-writing/`, and `.claude/skills` links to the same folder, so any agent working in this checkout can load it. Do not copy it into a root `skills/` directory, `server/builtin-plugins/`, or `server/marketplace/`. Those paths are Coppice runtime skill layouts. This skill must not be injected into end-user agents.

Do not apply these English habits to Vietnamese, Simplified Chinese, Taiwan Traditional Chinese, Hong Kong Traditional Chinese, Japanese, or French pages. Those languages have their own skills: [vietnamese-technical-writing](../vietnamese-technical-writing/SKILL.md), [zh-cn-technical-writing](../zh-cn-technical-writing/SKILL.md), [zh-tw-technical-writing](../zh-tw-technical-writing/SKILL.md), [zh-hk-technical-writing](../zh-hk-technical-writing/SKILL.md), [ja-technical-writing](../ja-technical-writing/SKILL.md), and [fr-technical-writing](../fr-technical-writing/SKILL.md). A translation edit still preserves literals, but the prose rules below are English-only. Other languages still need their own reviewed skills. Do not draft those from this file.

On a style pass, do not change product behavior. Preserve the locked positioning and design line recorded in [docs/milestones/M12-beta-release.md](../../../docs/milestones/M12-beta-release.md) and [docs/web/DESIGN.md](../../../docs/web/DESIGN.md). Leave Beta labels and the human-gate names **Plan Review** and **Wait for Human Review** as written unless a separate product change asks for them.

## 1. Establish the writing contract

Before editing, identify:

- **Reader:** what they already know and what they need next. For Coppice, say whether the page serves someone installing the desktop app, following user docs, or changing this repository.
- **Job:** deciding whether to use a tool, completing a task, understanding a mechanism, looking up exact behavior, or recovering from a failure.
- **Outcome:** what the reader should be able to do or understand.
- **Facts and limits:** supported platforms/versions, prerequisites, defaults, permissions, side effects, failure behavior and uncertainty.

If the request is just a style rewrite, do not treat it as permission to change the technical contract. Resolve factual ambiguity rather than making a sentence confidently wrong. [R01, R16]

## 2. Protect the factual and executable material

### R16: Preserve the technical contract, not just the topic

Before rewriting, inventory commands, code, API/type names, flags, configuration keys, paths, URLs, outputs, units, version numbers, normative terms, placeholders, warnings, links and relevant anchors. Keep these literals unchanged in a style-only pass. On a Coppice style pass, that inventory includes `make` targets, ports, configuration keys, keybindings, permission flags, and doc or download URLs. Preserve qualifications about timing, ownership, permissions, concurrency, defaults and failures. If an original literal seems broken or contradicts the prose, flag it separately; copying or silently repairing it is not validation. Preserve functional alt text and link targets when changing surrounding prose.

Do not invent an output, benchmark, successful test, capability, customer result, personal experience or diagnosis. Never add mistakes or typos to make prose "human." Never silently modernize old technical instructions during a style-only edit. Flag technical corrections separately; get a technical check when meaning changes. This safeguard outranks brevity and tone. [R09, R10, R16]

## 3. Choose a structure for the reader's job

### R15: Adapt the structure to the reader's job

Use these as adaptable patterns, not identical templates. The outline is an editorial aid, not an observed universal sequence:

- **Tutorial/task guide:** goal and prerequisites → small working case → expected result and how to check it → explanation → next useful step. Warn about risks before the risky action. Separate optional extensions.
- **Explanation:** concrete phenomenon/problem → useful model → worked example or contrast → consequences and limits. Add history only when it explains a present constraint.
- **Reference:** define the item and exact behavior; organize comparable entries consistently. Keep names, types, defaults, returns, errors, conditions and examples easy to find. Do not force a narrative before every lookup.
- **README:** explain the tool and intended use in ordinary terms, then a credible path to trying it, prerequisites, limits and deeper docs. Do not put a long origin story in front of the first useful action.
- **Website:** state a concrete outcome and enough mechanism/constraint to make it credible; give a specific next action. A slogan can stay, but it should not be the only explanation.
- **UI:** name the action and object. An error should identify what failed and a supported recovery action; state a consequence where it matters. Do not invent a cause the application has not diagnosed or bury a procedure inside a button label.

Tutorial/explanation patterns have direct corpus support. Formal reference, README, website and UI applications are editorial transfers from those patterns, not findings from a balanced corpus of each genre. For Coppice, validate the pattern against the README, site page, contributor doc, or UI string actually being edited. Do not paste a genre template over a locked positioning line. [R07, R13, R15]

## 4. Write English sentences that expose the mechanism

### R01: Put a concrete contract within reach

Give the reader a recognizable object, action and result early enough for their task. "This command exports the selected rows" is more informative than "A comprehensive solution for data management." A long essay can take a different route; a setup page should not make readers search for its purpose.

### R02: Make the actor and action clear

Prefer an ordinary finite verb over a stack of abstract nouns: "The worker retries the request," not "Retry execution is performed by the worker." Put the subject near its main verb. Expand English noun stacks when their relationships are hard to parse: "Configure unique cache keys" rather than "cache key uniqueness configuration implementation."

Use passive voice when the affected object is the useful topic or the actor does not matter (for example, a definition of how an object is used). Keep deliberate parallel phrasing when it makes a procedure easier to follow. Do not mechanically turn every passive into an awkward active sentence.

### R03: Repeat the right noun

Use one term for one concept. Introduce synonyms explicitly if they are needed; do not rotate through "job," "task," "process" and "run" merely for variety. Check what "it," "this," "that" and "they" refer to. Use "this retry" or "the original list" if a bare pronoun could point to several things.

As an English editing check, distinguish introducing a countable object ("a database") from referring to an identifiable one ("the database"). Definiteness depends on context, not just whether a noun has appeared before. This is a grammatical application, not a frequency finding from the corpus. Do not impose prose articles on literal identifiers or headings.

### R04: Vary rhythm with the work the sentence does

Let information load, not a manufactured cadence, determine sentence length. A short sentence can mark a result after a longer explanation. A longer sentence is useful when its condition and consequence belong together. Split independent actions, competing conditions or nested asides when they overload the reader. Keep the condition that makes a claim true.

There is no fixed sentence-length ceiling, paragraph quota or readability-score target. Fragments are optional rhetorical tools, not required signs of human authorship.

### R05: Move from known information to new information

Carry the current object or result into the next sentence, then add what changes. In a walkthrough, reuse a dataset or example while introducing a new operation. End a paragraph at a meaningful result or question when that suits the explanation; let the next paragraph build on it. A classification or lookup entry need not build a narrative between every item.

### R06: State the actual relationship

When expressing these relationships in English, use **because** for a reason, **so** for a consequence, **but/however** for contrast, **when** for an event or trigger, and **if** for a condition. Do not change "if" to "when" if that would turn a possibility into an expected event. Use a transition only when that relationship is real. "This fails when the connection closes" often does more work than "Furthermore, there is another consideration." Paragraphs can connect without an explicit transition word when the relationship is already clear.

## 5. Explain enough, in the right order

### R07: Build one mental step at a time

Start from something observable or already understood. Establish the simple case before adding the complication. Distinguish a misconception from the correct explanation immediately enough that readers will not act on the wrong model.

Do not copy the essay trick of promising too much and retracting it later into instructions, guarantees or security explanations. Put essential limitations beside the claims they limit.

### R08: Use examples as evidence, not decoration

Introduce what the example demonstrates. Keep setup and inputs sufficient for the example's stated purpose. Say whether a block is runnable, a fragment or pseudocode; an explanatory fragment need not become a full application. Show expected output only when verified or explicitly hypothetical, then explain what to inspect. A small example can precede a complete one. A before/after comparison should hold irrelevant details steady. If two expressions look alike but behave differently, show the distinguishing operation and its consequence rather than smoothing away the contrast. When a task can appear successful without producing its intended result, include a supported check of that result, not just "the command finished."

Mark omissions and pseudocode. Never claim an example was run if it was not. Do not adopt historical source commands as current product guidance without checking them.

### R09: Preserve the force of modal verbs

Preserve the intended force of **must**, **should**, **may**, **can** and **will**, including negation and conditions. The following are editing prompts, not a rule for reinterpreting all ordinary English or replacing a standard's definitions:

- **Must**: often a requirement or invariant in instructions, but it can also express an inference. Preserve the intended sense; do not create a new obligation.
- **Should**: often a recommendation, but sometimes an expectation or a term defined by a governing specification. Determine which before editing.
- **May**: possibility or permission—make which one clear.
- **Can**: capability or possibility—do not imply a guarantee.
- **Will**: often expected/asserted behavior under the stated conditions. Do not strengthen a possibility into a promise.

Keep the relevant platform, version, default and failure cases attached. A specification's defined normative vocabulary takes priority.

### R10: Be candid where the evidence ends

Distinguish observed behavior, measured results, inference, advice and open questions. Hedge the uncertain part precisely. Remove empty doubled hedges, not real uncertainty. Do not turn "worked in this example" into "always works." Use "I" for a real author's experience, never a manufactured one. A personal blog's self-deprecation is not an appropriate default for supported documentation.

### R11: Explain jargon where the reader crosses into it

Keep canonical technical terms and identifiers. When a term is new to the intended reader, give a plain description tied to the current task and, if helpful, a concrete example. Define an umbrella concept before its categories. Link optional depth rather than interrupting the core task. Do not explain every familiar acronym to an expert audience, or replace precise terms with vague synonyms.

## 6. Keep the tone ordinary and respectful

### R12: Conversational is not theatrical

Use ordinary contractions where natural and unambiguous. Use **you** for the reader's action and imperatives for instructions: "Run …", "Choose …", "Check …". Use **we** for an actual shared walkthrough or team position; do not blur who must act. Do not manufacture a narrator, an experience or a collective opinion merely to avoid passive voice.

Ask a question when it anticipates a real uncertainty or decision, not to simulate engagement. Avoid condescension, compulsory jokes, repeated celebration, fake anecdotes and grand claims that add no information. Do not mimic a living author's catchphrases, sarcasm, lowercase headings or punctuation habits. Human prose can be restrained.

### R13: Make the shape match the relationships

As an editorial default, use numbered steps when order matters and bullets for peers; numbering can also identify items for later reference. Choose deliberately rather than pretending the corpus uses only one convention. Keep genuinely comparable list items grammatically parallel, but do not flatten a definition, condition or exception just to make its first word match. Use headings that identify the task or concept; avoid vague headings that could fit any page. Prefer a table when shared fields make comparison easier; this is an editorial transfer, not a measured corpus result. Do not convert all prose into bullets or repeat an identical heading pattern on unrelated pages.

### R14: Prefer verifiable effects over inflated wording

Replace a vague promise with an action, mechanism or consequence the facts support. "Run checks before merging" conveys more than "Unlock a seamless workflow." Do not replace an unsupported benefit with a more specific invented benefit. Keep useful product language or a deliberate slogan, but pair it with an explanation readers can verify. In Coppice, a locked slogan or positioning line stays; a style pass does not replace it. The corpus includes genuine enthusiasm and promotional adjectives; restrained wording is a reusable editorial default, not proof that enthusiasm is inhuman.

## Additional source-backed checks

- **Put the right next step after the right condition.** Distinguish a suspected implementation bug from a request to change intended behavior; route readers accordingly. Do not turn a failed approach into a universal diagnosis. (EN26 issue-routing paragraphs; EN01 alternative capture methods.)
- **Read the qualifications outside the main flow.** Footnotes and asides can contain the condition that makes an example safe or true. Move an essential qualification beside the claim or action when readers might otherwise miss it. Do not delete "at least once" to obtain a cleaner sentence. (EN30 job-delivery footnote; EN21 coverage verification and secret-token notes.)
- **Keep attribution separate from assertion.** Identify a cited authority, an observation and the writer's recommendation distinctly. A quotation is not evidence of the surrounding author's sentence habits; a cited claim is not automatically verified. (EN05 concept attribution; EN14 tests versus specification; EN28 maintainer quotation.)

These are applications of R07–R11/R16, not a mandate to add new sections to every page. EN21's historical credential guidance is not adopted.

## 7. Review the draft in separate passes

1. **Meaning:** compare propositions, not just keywords: who acts, on what, under which condition, with what result and exception? Check the literal inventory, units, modals, negation, warnings and factual qualifications.
2. **Reader path:** can this audience find the next action, result, explanation or lookup answer? Are prerequisites and essential limits in time?
3. **English:** check actor/verb distance, pronoun references, noun stacks, a/the references, causal links, list parallelism and sentence rhythm.
4. **Evidence and tone:** remove invented certainty/experience, decorative transitions, empty claims and forced personality. Keep necessary repetition and caveats.
5. **Report:** distinguish style edits from factual questions and technical corrections. Do not claim testing, improved SEO or user outcomes without evidence.

## Original miniature examples

Illustrative only; not product facts, source quotations or executed instructions. Each rewrite assumes the stated meaning is established. If it is not, ask or flag the ambiguity rather than inventing a clearer-sounding claim.

- **Agency.** Given: a worker retries a request. Wordy: "Retry execution is performed by the worker." Rewrite: "The worker retries the request." Do not delete a meaningful initiation phase from a real two-phase system merely because it resembles this example.
- **Antecedent.** Ambiguous: "The worker sends the request to the server after it starts." If worker startup is intended: "After the worker starts, it sends the request to the server." If server startup is intended, name the server instead.
- **Conditional capability.** Given: support for CSV is verified; JSON is the default. Wordy: "The default output format used by the command is JSON, and CSV output is also available." Rewrite: "The command returns JSON by default. It can also return CSV." No invented flag, spreadsheet compatibility claim or new guarantee.
- **Calibrated effect.** Given: a cache hit avoids another network request; total response time is unmeasured. Rewrite: "A cache hit avoids another network request. We haven't measured its effect on total response time." This is not an equivalent rewrite of an unsupported "always faster" claim; it is usable only with that factual brief.
- **Undiagnosed error (editorial UI transfer).** Given only that saving failed: "Couldn't save the file." Add a recovery action only when it is supported by the actual error state; do not prescribe a writable folder, retry or sign-in without that basis.
- **A qualification worth keeping.** Given: a queue delivers at least once and therefore requires idempotent jobs. Wordy: "Because the queue provides at-least-once delivery rather than exactly-once delivery, it is necessary for the jobs to be idempotent." Rewrite: "The queue delivers jobs at least once, not exactly once. Jobs must therefore be idempotent." Keep both the delivery limit and the requirement; do not substitute "retries are safe."

## Evidence note

Research scope: 30 distinct originally authored English technical articles, 15 authors, with initial publication dates from 2002-11-11 through 2020-04-06, all strictly before 2020-11-07. Both passes read the complete current-page textual bodies, including available notes. One complete pre-cutoff archived body (EN25) was additionally read. The other 29 lack that full historical-text comparison. This does not establish that every analyzed sentence predates generative AI.

EN17 and EN24 were read and then excluded from rule support. Do not cite them as grounding. Do not describe this corpus as 30 verified untouched pre-generative-AI texts, and do not describe it as native-speaker biographies. Original English here means the article was composed in English, not that a biography of the author's first language was verified.

Compact anchors, all outside the excluded pair: [Evans: Linux groups](https://jvns.ca/blog/2017/11/20/groups/) (R01–03, R07–08); [Fowler: Test Double](https://martinfowler.com/bliki/TestDouble.html) (R03, R11, R13); [Willison: sqlite-utils](https://simonwillison.net/2019/Feb/25/sqlite-utils/) (R05, R08, R14); [Batchelder: names and values](https://nedbatchelder.com/text/names) (R03–04, R07, R16); [Archibald: tasks and microtasks](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/) (R04, R09–10); [Bendersky: threaded servers](https://eli.thegreenplace.net/2017/concurrent-servers-part-2-threads/) (R06–08); [Andrew: grid accessibility](https://rachelandrew.co.uk/archives/2019/06/04/grid-content-re-ordering-and-accessibility/) (R06, R10, R14); [Brandur: HTTP transactions](https://www.brandur.org/http-transactions) (R05, R09, R16).

R02's noun-stack repair, R03's article check, R13's list/table conventions, R14's restrained default, R15's genre transfers and R16's operational rewrite safeguards are editorial recommendations grounded in or applied to the examples, not all explicit author rules. Source evidence does not establish SEO gains, a mandatory sentence length or a universal "human" voice. The bibliographic record and the rule-by-rule bounds are in [corpus-manifest.md](corpus-manifest.md) and [review-evidence.md](review-evidence.md).
