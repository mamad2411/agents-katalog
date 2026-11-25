---
name: customer-voice
description: Use when writing, reviewing or checking any text a customer or reader will see on a CBEG property (product results, pages, forms, emails, newsletters, offers, error and status messages, assistant-facing tool text). Makes the text read as a person wrote it for one reader.
---

# Customer voice

Anything a customer reads should sound like a knowledgeable person explaining it to them across a desk. Readers spot machine-written text in a sentence or two, and once they do they trust the content less. Natural text is also simply easier to read.

The master copy of this file is `.claude/skills/customer-voice/SKILL.md` on Crindo2/vault main. Other copies are taken from it unchanged.

## The test

Read it aloud to one imagined reader who has the problem the text is about. If you would not say a sentence that way to their face, rewrite it. If the text only passes because every rule was satisfied, it has not passed.

## How to write it

1. Write for one reader in one situation. Start from the thing they most want to know and say it first.
2. Compose the whole passage, then check it. Do not assemble it from separately written fragments.
3. Use their facts: the insurer's name, their dates, their city. "Cigna confirmed yours complete on September 24" beats "the insurance company confirmed application complete".
4. Join the reasoning. Words like because, so, which means and until carry the logic from one sentence into the next. A run of short declaratives with no connection between them is the clearest machine tell there is.
5. Let sentences vary in length the way speech does. Contractions are fine.
6. Say numbers and dates the way a person would: "five days past the deadline", "September 24".
7. End on what to do next, once, in plain words.
8. Keep every fact exact. Voice changes never change a number, a date, a source, a price or a legal reference.

## What stays true from earlier rules

- Say what we know and what follows from it, plainly. No caveat stacks, no hedging words, no method notes.
- Name the source when a result rests on one (the statute, the insurer's own figure).
- Each property's own rules still apply: identity separation, the helpline and no medical claims on health content, no refund sentence, approved offer wording that is marked as fixed.

## Tells to remove

- Fragment chains: "Yours is at day 50. It is 5 calendar days overdue."
- A stock instruction repeated everywhere, such as "ask for it in writing". Use it only where a written answer is the real next step.
- Institutional noun piles: "the insurance company's published provider onboarding contact".
- Label and colon lines used in place of a sentence ("First step: ...", "You have an answer when: ...") where a sentence would do.
- Repeating the full noun every time when "they" or "it" is clear.
- Groups of three for rhythm, "not X but Y" constructions, rhetorical questions, and summary lines that restate what was just said.
- Openers and closers that say nothing ("Here is", "In summary", "We hope this helps").
- Em dashes and en dashes.
- Words chosen to sound thorough: comprehensive, robust, seamless, leverage, ensure, navigate, tailored.

## Text built from templates

Much product text is selected by code from a fixed set of outcomes. For that text:

1. Write one whole paragraph per outcome, with the variables inside the sentences. Do not write clauses for code to join.
2. Fill each paragraph with three real sets of values, including the awkward ones (one day, zero days, a long insurer name), and read each aloud.
3. A ruling or spec says what must be true. It is never the wording. Do not copy a ruling's sentences into customer text.
4. The builder wires approved wording in word for word and reports any place the code cannot hold it.

## Text generated fresh each time

Articles, newsletter items and replies have no finite set. The writer applies this file while writing, and the text then gets the editor's read below before it ships.

## The editor's read

Done by a reader who did not write the text, as part of the ordinary non-author check whenever a change touches customer-facing words.

1. Read it once as the customer, start to finish, before looking at any rule or diff.
2. Mark every sentence you would not say aloud to that customer.
3. Rewrite the marked sentences, keeping every fact exactly as it was.
4. Run the construction check used for articles (`scripts/verify_article_quality.py` on getpracticehelp) over the text where the repository has it.
5. Report the before and after of each rewritten sentence. A change with unreadable customer text does not pass, whatever its tests say.

## Before and after

Before: "Kentucky law gives the insurer 45 calendar days from a complete application. Yours is at day 50. It is 5 calendar days overdue. Call provider relations, cite KRS 304.17A-576(1)-(4), and ask for the decision date in writing."

After: "Kentucky gives an insurer 45 days to decide once your application is complete. Cigna confirmed yours complete on September 24, so today is day 50 and they are five days past the deadline. When you call provider relations, tell them that, mention KRS 304.17A-576, and ask what date you will have a decision."

Before: "Kentucky's 45 days start when the application is complete. The insurer has asked for more, so the clock has not started. Send what it asked for and get the completion date in writing."

After: "Cigna has asked you for more information, and until they have it your application isn't counted as complete. That matters because Kentucky's 45-day deadline only starts on the day it is. You submitted on September 14, so you are 60 days in and none of them count yet. Send what they asked for and ask them to confirm the date they mark it complete. From that date they have 45 days."
