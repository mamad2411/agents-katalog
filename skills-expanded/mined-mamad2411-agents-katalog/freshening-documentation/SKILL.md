---
name: freshening-documentation
description: Trim and freshen technical documents, READMEs, design notes, PR descriptions, internal messages, and source-code comments or docstrings. Uses independent fresh-reader reviews to expose author-context bias, then deletes repetition, defensive caveats, filler, decorative structure, and code restatements while preserving facts, decisions, actions, constraints, and necessary rationale. Use when text is overexplained, repetitive, hard to scan, written while thinking, or when comments restate code or have drifted out of sync with it.
---

# Freshening Documentation

Edit from the reader's side, not the author's. A sentence — prose or code comment — is not valuable merely because it is true or took effort to write. Keep it only when it helps the intended reader understand, decide, act, verify, or avoid a likely mistake. A comment's reader is looking at the code it annotates, so it is worth keeping only for the understanding that code cannot supply on its own.

Deletion is the default operation. Rewrite only when deletion leaves a gap or a shorter sentence can carry the same meaning.

## When to use

Use this skill when a document or code comment:

- Feels longer than the reader's task requires.
- Repeats its conclusion, rationale, caveats, or examples.
- Was produced by an author or agent that has been immersed in the topic and may be relying on unstated context.
- Was written while thinking and now needs structural revision.
- Looks organized but remains difficult to scan or act on.
- Contains comments that restate nearby code, carry a vague TODO, or may have drifted out of sync with the code.
- Is about to be published, reviewed, merged, or sent.

Do not use it as a substitute for subject-matter review. Apply it cautiously when exact wording is legally, contractually, or operationally required, and leave machine-read comments alone — linter and compiler directives, suppression pragmas, generated-file markers, doctest syntax, and framework annotations.

## Instructions

### 1. Define the reader contract

Before editing, write a private one-line contract:

`For [reader], this document should enable [decision, action, or understanding] because [reason].`

For a comment, the reader is looking at the code, so the contract covers only what the code cannot state on its own. A public API docstring is the exception: its reader is a caller who may never open the implementation, so its contract is the full calling contract.

Identify the core message, why the reader needs it, the expected action or outcome, required evidence or constraints, and the reader's assumed prior knowledge. If these cannot be stated coherently, ask one focused question or flag the ambiguity. Do not compensate for an unclear purpose by adding prose.

### 2. Run isolated fresh-reader reviews

Treat the author's current context as contaminated by familiarity. When subagents are available, launch three independent reviewers by default and five for long or high-impact documents.

Give each reviewer only the material and a brief audience profile, matching the context to what its real reader sees: the document alone for prose, the local code for an inline or block comment, the signature for a public API docstring. Never add the author's private rationale — a comment that only makes sense with it is exhibiting the bias this skill exists to remove. Do not reveal the reader contract: the first test is whether the material itself communicates its purpose and requested action.

Do not provide the conversation history, the author's private rationale, suspected problems, previous reviews, or another reviewer's output. Sample plausible reader states rather than writing styles: the intended reader, a hurried decision-maker, and an adjacent expert with little local context. Prefer diverse sampling when the runtime supports it.

Use this review prompt:

```text
Read this as a fresh member of the stated audience. Do not rewrite it.
Return only:
1. The purpose or requested action in one sentence.
2. Content you skipped, reread, or could not place.
3. Paragraphs, examples, caveats, or sections that can be deleted without changing your decision or action.
4. Missing information that would change your decision or action.
5. Misleading headings, lists, or tables.
```

If subagents are unavailable, perform three separate cold-read passes using the same reader states. Record each judgment before editing.

### 3. Build a deletion map

Classify every section, paragraph, list, and table as one of the following:

- **Keep:** It changes a decision or action, defines a requirement or invariant, records the rationale behind a non-obvious choice, supplies necessary evidence, prevents a likely error, or is required to interpret what follows.
- **Move or condense:** It is useful but secondary, such as implementation detail, an edge case, one representative example, or troubleshooting material.
- **Delete:** It is repetition, generic scene-setting, irrelevant history, self-justification, ritual politeness, verbal hedging, an obvious transition, commentary about the writing process, an exhaustive example set, a caveat that does not change behavior, a restatement of the adjacent code, commented-out code, or a vague TODO with no actionable next step.

Delete a unit when most fresh readers mark it expendable and no keep criterion protects it. When reviewers disagree, retain it only if you can name a concrete misunderstanding, wrong decision, or failure that its removal would cause.

### 4. Edit in descending order of value

Make large cuts before sentence-level polishing:

1. Remove entire sections that do not support the reader contract.
2. Remove repeated explanations, examples, caveats, and summaries.
3. Merge overlapping points.
4. Move secondary detail to an appendix, reference, or linked document when appropriate.
5. Shorten sentences, labels, and transitions.
6. Fix grammar and style last.

Apply these rules throughout:

- Lead with the conclusion, requested action, recommendation, or current status.
- Keep the core message, its rationale, and supplementary detail distinct. Do not alternate between them.
- Give each paragraph or section one concern.
- Prefer direct statements to setup, apology, and defensive wording.
- Do not compress several ideas into one dense sentence. A shorter document should also require less reader effort.
- Do not add a summary that merely repeats the body. A summary should replace detail for a broader reader, not duplicate it.
- Keep one representative example unless additional examples expose materially different behavior.
- In a comment, prefer a durable reason or invariant over narration of the current code, which goes stale as the code changes; when a comment stays true only because it describes today's structure, prefer making the code self-explanatory through naming, types, or extraction.
- Preserve technical terms, factual claims, requirements, code behavior, uncertainty, traceability, and a docstring's caller-facing contract (parameters, exceptions, side effects, ordering, thread safety) even when it is obvious from the implementation. Never shorten into inaccuracy.

### 5. Use lists and tables only for scanability

Do not convert prose to bullets merely to make it look organized. Use a list or table when the reader benefits from scanning or comparing independent items. Otherwise, use paragraphs and headings.

Every list item or table row must:

- Address one independent concern.
- Contain one item at a consistent granularity.
- Match the abstraction level of neighboring items.
- Keep related qualifications with the item they modify.
- Remain meaningful when reordered, unless the list is explicitly sequential.

If these conditions cannot be met, replace the list or table with prose. Avoid deep nesting.

### 6. Validate with new fresh readers

After editing, give only the revised document and audience profile to two new reviewers, or perform two new cold-read passes. Do not reveal the reader contract. Ask them:

```text
1. What should the reader know or do?
2. What required context or constraint is missing?
3. Which sentence or section can still be removed?
4. Where would a reader stop, hesitate, or misread?
```

Accept the revision when the reviewers agree on the purpose and action, no required fact or constraint has been lost, every section supports the reader contract, and further deletion would increase the risk of error more than it reduces reader effort.

When validation exposes a gap, restore only the minimum missing information. Do not restore the original paragraph wholesale.

### 7. Deliver without a defense of the draft

Edit the target in place when possible. Return the revised document and a compact report containing:

- The before-and-after word or comment-line count.
- The largest categories of removed content.
- Any unresolved factual or audience questions.

Do not provide a paragraph-by-paragraph justification unless requested. Do not add a change log inside the document unless the document requires one.

## Notes

Fresh readers are used to sample plausible reader states, not to vote on personal style. Their main value is detecting assumptions that became invisible to the author.

Writing while thinking is acceptable, but the resulting draft must be redesigned afterward. Large deletions and structural rewrites are normal.

Deletion is not the goal by itself. Optimize for low reader effort and reliable action. Keep a long explanation when its absence would plausibly cause a wrong decision, unsafe action, or failed implementation.

Do not silently resolve ambiguous meaning. Flag it for the author or domain owner. When a comment contradicts the code, report the conflict rather than deciding which is authoritative. For security, legal, safety, compliance, or operational runbooks — and for comments asserting such behavior — require domain-owner review after freshening.
