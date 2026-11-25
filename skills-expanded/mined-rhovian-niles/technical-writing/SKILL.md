---
name: technical-writing
description: Use when writing, drafting, or reviewing technical prose such as docs, READMEs, tutorials, how-tos, reference pages, or engineering blog posts under the author's name. Interviews the author, sources every claim, lints, and tests the result on a fresh reader.
---
# Technical writing

Technical readers abandon text that reads as generated, and LLM drafts rarely carry the author's actual ideas. So split the content by who can supply it:

- Experience, decisions, opinions, surprises, and voice come only from the author. Never invent them.
- Technical facts can come from the author or from primary sources you find (code, specs, docs, on-chain data, measurements). Record a source for every one.

The author must be able to explain every technical claim in their own words before it ships under their name.

## Process

Scale to the job. A README section needs steps 1, 2, 6, 7, and 8. A review of an existing draft needs step 1 (the reader, the job, and a length budget) and then steps 7-10, and it reports its findings as a list, not as edits. Lead the findings with length: the word count against the budget, the longest paragraphs, and what the reader could skip. End with the target shape in 2-3 lines. If the author wants a fast draft without the interview, draft from sources only and mark every author-owned gap `[TK]`. Keep working notes in one `notes.md` (format under Reference).

1. Write a brief: the reader, the job in one sentence ("after reading, the reader can …"), the type, and a length budget. For a rewrite, set the budget below the current length. Infer what's obvious and ask only for the rest. For docs, use Diátaxis and keep one type per page. For posts, pick a pattern (both are listed under Reference). For pieces under the author's name, ask for 1-3 samples of their writing so you can match their rhythm and vocabulary.

2. Research before asking. Read the code, PRs, logs, specs, and data. Record each finding with its source, marked established or inferred. Don't ask the author anything the sources answer.

3. If the author is still learning the subject (reverse engineering, learning in public), teach it from first principles, Socratically, one question at a time. Have them explain each mechanism back in their own words, and correct them by pointing at evidence rather than lecturing. Capture their reactions. Those are often the strongest lines in the piece.

4. Interview one question at a time. Bring your findings ("the code retries with no backoff; does that match what you saw in prod?") and ask for what only the author has: what happened, what failed, the numbers, what surprised them, what they'd change, what they believe. Push vague answers toward specifics. Log answers verbatim, because their phrasing is the draft's raw material. If they don't know a fact, research it (step 2) or teach it (step 3) instead of pressing.

5. Outline. Each heading answers a question the reader has and is backed by notes, or else marked `[GAP]`. Open with the problem or the result, not background. Cut filler sections ("why this matters", challenges, the future, a conclusion that restates). Get the author's approval before anyone drafts.

6. Draft one section at a time, the most uncertain first and the intro last. Use the author's words. Write `[TK: what's needed]` instead of filling a gap. Stay within the budget; a sentence that doesn't serve the job is cut, even if it's true. Edit surgically. Never reprint the whole document or revert the author's edits. For opinion pieces under their name, prefer that they draft and you edit.

7. Verify. List every factual claim with its origin (author, research, or inferred) and its source. Check APIs, flags, and defaults against the code at the documented version. Run commands and samples only in a scratch environment (a throwaway directory, devnet or testnet). Never run anything that spends money, touches production or mainnet, or deletes data. Mark those claims unverified instead. Resolve every link. Inferences must read as inferences in the text. Ask about, narrow, or cut anything unverified.

8. Lint with tools, not judgment. Use the project's Vale config if it has one. Otherwise, write the config under Reference into a scratch directory and run `vale --config=<dir>/.vale.ini sync`, then `vale --config=<dir>/.vale.ini <files>`, so nothing is added to the author's repo unless they ask. Also run `markdownlint-cli2 "<dir>/**/*.md"` and `lychee --no-progress --offline --include-fragments <dir>` (tested with markdownlint-cli2 0.23 and lychee 0.24). Drop `--offline` to check external URLs, but treat timeouts, 403, and 429 as unverified rather than broken. Linters over-flag, so fix the real problems, ignore the false positives, and send stock-phrase hits to step 10. If the tools can't run, say so.

9. Test on a fresh reader. Give a subagent with no conversation context only the document, the reader persona, 5-10 questions that reader would bring (ask the author for theirs too), and the prompt under Reference. For tutorials, also run the steps in a scratch environment if you can. Fix the gaps by replacing or cutting text rather than adding to it, keep the budget, and retest until the main point matches the job, which usually takes one or two rounds. Without subagents, give the prompt to the author to run in a fresh chat.

10. Audit for AI tells: inflated significance, vague attribution ("experts say"), `serves as` where "is" works, "not just X but Y", reflexive groups of three, synonym cycling, stacked hedges, bold-label bullets, and a closing summary that restates the intro, plus the stock phrases in the Vale rule's `tokens` list. In the author's prose, flag tells and don't rewrite, because a rewrite erases the voice and adds new tells. In prose you drafted, fix them by adding the specific detail, not by swapping synonyms. A tell usually marks missing substance, so get that detail from the author. Never polish text just to evade detection. The author's house style overrides this list.

## Reference

Diátaxis (one type per page):
- Tutorial: a guided lesson for a newcomer. One path, every step works, expected output shown.
- How-to: steps to a real goal for someone competent. Title it with the goal and list prerequisites first.
- Reference: complete, austere facts structured like the code. Describe, don't explain.
- Explanation: the why, meaning context, design decisions, and tradeoffs. No steps.

Post patterns (from *Writing for Developers*, by Sarna and Dunlop):
- Bug hunt: symptom, false leads, root cause, fix, lesson.
- Rewrote it in X: the pain in numbers, why X, surprises, an honest before and after.
- How we built it: constraints, architecture, non-obvious tradeoffs.
- Lessons learned: one real story per lesson.
- Thoughts on trends: an arguable thesis, evidence, the best counterargument.
- Product perspective: limitations, and who it's not for.
- Benchmarks: exact setup, method, raw numbers, caveats, how to reproduce.

`notes.md`:
```
## Brief      reader / job / type / voice samples
## Findings   finding | source | established or inferred
## Interview  verbatim Q&A
## Claims     claim | origin | source | verified?
## Open       [TK] and [GAP] items
```

Reader-test prompt:
```
You are [persona]. You have only the document below. If it doesn't say, say so.
1. Answer each question from the document alone, quoting what you relied on.
2. State the main point in one sentence.
3. List where you got confused, where you'd stop reading, terms used before they're defined, unstated assumptions, and unsupported claims.
4. For a tutorial or how-to: follow the steps literally. Where do you get stuck?
```

Vale (v3), tested:
```ini
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = warning
Packages = Google, proselint
Vocab = Project

[*.{md,mdx}]
BasedOnStyles = Vale, Google, proselint, House
Google.We = NO   # for first-person posts
```
```yaml
# .vale/styles/House/AITells.yml
extends: existence
message: "AI tell: '%s'"
level: warning
ignorecase: true
tokens: [delve, tapestry, testament to, landscape, leverage, robust, seamless, unlock the, harness the, navigate the, "it's worth noting", in conclusion, serves as, plays a crucial role, "let's dive in"]
```
StylesPath is resolved relative to the config file. Always create `.vale/styles/config/vocabularies/Project/accept.txt` next to it, with one project term per line. Vale errors if the file is missing, so create it even if it's empty.

## Handoff

Deliver the document, the claim list, any open `[TK]` or `[GAP]` items, and a two-line summary of the reader test if you ran one. If you drafted much of the prose, mention once that disclosing AI involvement is the author's call.
