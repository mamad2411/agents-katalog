---
name: slop-scrub
description: Edit drafts before they leave the agent. Also triggers on "slop scrub", "check for AI-isms", "scrub this", "check this copy", "review this writing", or "run slop scrub on this". Check claims and preserve the author's voice while removing banned wording and repetitive prose.
---

# Slop Scrub

Read the draft as its copy editor and apply the checklist. Run it again after you've made the edits.

This skill runs on any text before it leaves the agent. No channel is exempt. No context makes AI-isms acceptable. Even internal notes get scrubbed if they might be forwarded.

> **Not using Claude Code?** This file works as a standalone checklist too — see the [README](../../README.md) for how to run it as a plain prompt, a git hook, or a CI check with any LLM.

## Input

The text to scrub is one of:

- Pasted directly after the `/slop-scrub` command
- The most recent draft the agent just produced (scrub it before showing the user)
- A specific file or message the user references ("scrub the LinkedIn draft I just wrote")

If no text is provided and no draft is in scope, ask the user what to scrub. Don't guess.

## The 14-item checklist

Run every item. For EACH item, report what you found. "Clean" is acceptable only if you actually checked. Do not skip items. Do not batch them. The whole point is to catch the thing you'd skip.

### 1. Word scan

Search the text for every word in this banned list. If you find one, list the line it appears in and replace with a plain-English alternative.

**Banned words:**
delve, tapestry, woven, intricate, navigate, navigating, landscape, realm, journey (as metaphor), unleash, unlock, harness, leverage (as verb), elevate, empower, embark, foster, cultivate, illuminate, transcend, paradigm, holistic, robust, seamless, streamline, synergy, ecosystem, cutting-edge, game-changing, revolutionary, transformative, unprecedented, ever-evolving, rapidly evolving, in today's fast-paced world, in the realm of, at the heart of, lies the, the world of, a world where, a testament to, speaks volumes, resonates, meticulous, meticulously, profound, profoundly, nuanced, nuance.

This list is a starting point, not a ceiling. If a word feels like AI reaching for grandeur, flag it.

### 2. Construction scan

Search for these banned sentence shapes:

- **"It's not X, it's Y"** and any variant ("This isn't X. It's Y." / "Not just X — Y.")
- **"Not only X, but also Y"** and variants such as "not just X, but Y"
- **"No X. No Y. Just Z."** triplets used for emphasis
- **Automatic groups of three** in parallel clauses, adjectives, or nouns. Keep the entries that each give the reader something they need.
- **Mid-sentence self-questions** — "And what does that mean? It means..."
- **"An X with Y and Z" catty dismissals** — "An app with a logo and a landing page"
- **Pre-loaded transitions** — "Here's the thing:", "But here's the kicker:", "What's interesting is:"
- **Dressed-up verbs** such as `serves as`, `stands as`, `acts as`, `functions as`, `boasts`, `features`, and `represents` where `is`, `are`, or `has` would mean the same thing

Rewrite any found. Replace with plain declarative sentences.

### 3. Drumroll scan

Search for pre-announcements that promise something is coming instead of just saying it:

- "Here's the wildest part:"
- "What most people don't realize:"
- "The best thing about this:"
- "But here's the kicker:"
- "Here's why this matters:"
- "The crazy thing is:"

Delete the drumroll. Keep the point. The reader doesn't need a pep band warming them up for a sentence.

### 4. Metaphor check

Is every metaphor earned (rooted in real observation) or is it concept-stacking (piling abstract nouns on top of each other to sound profound)? Cut any stacking. "The architecture of trust" is concept-stacking. "Trust is the load-bearing wall — pull it and the whole house comes down" is earned.

### 5. Sensory check

Is sensory language attached to something you can actually sense?

- "The texture of embarrassment" — cut. Embarrassment has no texture.
- "The weight of a $9,400 invoice" — fine. An invoice has weight, literally and figuratively, and the number grounds it.

If you can't physically perceive the thing the sensory word is attached to, cut it.

### 6. Quietness check

Are things described as quiet, humming, whispering, spectral, or ghostly that literally aren't? AI loves making everything quietly happen. Cut those. "The bug quietly corrupts your data" — does it actually do this without noise? If yes, fine. If you just liked the cadence, cut.

### 7. Profundity check

Read the whole piece for claims of importance without a stated consequence. If the prose calls an ordinary event a pivotal milestone or a turning point, or says it leaves a legacy, use the author's facts to say what changed and how much. Cut commentary that says a fact "highlights," "underscores," "reflects," or "shows" something when it adds no information. Keep a verb like "shows" when the sentence explains what the evidence establishes.

- "And maybe that's exactly the point." — cut.
- "Sometimes the answer was in front of us all along." — cut.
- "The real question isn't X. It's Y." — cut.

State the consequence when the author has supplied one. End on the point the reader came for.

### 8. Bartender test

Would a smart bartender — not a customer at the bar, the bartender — understand every sentence after one read? Technical terms are fine if the audience is technical. Abstract jargon stacking is never fine. If you can't pass this test, simplify until you can.

### 9. Specificity and swap test

Check every paragraph for at least one detail only the author could provide. Look for a number, name, date, place, or action in the draft, supplied notes, or approved `VOICE.md` samples. For copy about a company or product, try swapping in a competitor's name. Flag interchangeable passages.

Use supplied facts that apply to this piece. For a paragraph without a qualifying detail, flag it as `needs a real detail from the author`. Never invent a detail.

### 10. Em dash check

Zero tolerance. Search for `—` (em dash) and `–` (en dash). Replace every one with a period, comma, line break, or set of parentheses. AI uses em dashes as a tell. Humans rarely do, especially not three per paragraph.

Exception: this rule applies to OUTPUT text (content meant for human readers). It does not apply to internal instruction docs, code comments, or project-level agent instruction files.

### 11. Source check

Does every factual claim have a source, or is it clearly framed as illustrative?

- "73% of AI companies struggle with margins" — needs a source or it's fabricated.
- "Consider two customers on the same plan" — clearly hypothetical, fine.

Flag every unsourced claim. Replace vague attributions such as "experts say," "studies show," "research suggests," or "many believe" with a named source that supports the claim. Flag runs of outlet, brand, or institution names that borrow prestige without adding evidence. Cite one source for a point, and add another only if it supplies different evidence the reader needs. Cut unsupported claims or frame genuinely hypothetical examples as illustrative.

### 12. Contraction check

Check for stiff, over-expanded prose, but do not force contractions into every sentence. AI often avoids contractions even when the surrounding voice uses them. Where a contraction sounds natural for this writer and reader, use it; where the expanded form adds emphasis, fits a formal passage, or matches the author's samples, keep it. Preserve contractions already present when they fit.

Examples of common contractions include `do not` / `don't`, `cannot` / `can't`, `will not` / `won't`, `it is` / `it's`, `we are` / `we're`, and `I have` / `I've`. Check meaning and grammar before changing a form. In particular, `let us know` and `let us help you` mean _allow us_, so do not change them to `let's`.

Flag repeated uncontracted forms when they make conversational copy sound formal or unlike its author. Do not treat an isolated expanded form as an error by itself.

### 13. Staccato check

Look for adjacent runs of two or more sentences where every sentence is short (about 12 words or fewer), declarative, a complete claim on its own, parallel in shape, and unconnected to the next sentence by a word or phrase such as `because`, `so`, `which`, `when`, `but`, or `and`. The run reads like a list of verdicts.

Example to rewrite: "The same request produces a different plan tomorrow. A passing test does not carry forward." Join the claims: "The same request produces a different plan tomorrow, so a passing test doesn't carry forward."

- Three or more qualifying sentences in a row: rewrite the run.
- Two qualifying sentences in a row: flag the run for review. Rewrite it when both sentences also avoid contractions.

Join the claims with a connective that states their relationship, vary sentence length on purpose, or add a concrete example that supports the claim. One short sentence after a longer one can work when the contrast is the point.

Also flag three or more consecutive sentences of nearly equal length, including long sentences. Read the run aloud and vary the pacing if the sentences repeat the same beat.

Exempt headlines, bullets, calls to action, captions, table cells, and quoted speech from a named person.

### 14. Sales pitch, caveats, and assistant residue

- In prose outside an ad, check for sales language such as `nestled`, `vibrant`, `boasts`, `must-see`, and `world-class`. Describe the fact a reader can verify.
- Cut needless caveats such as `important to note`, `worth mentioning`, or `results may vary`. Keep qualifications that tell the reader a specific limit or condition.
- Remove assistant residue on sight. Look for `as an AI`, `I hope this helps`, `great question`, `certainly` as an opening acknowledgment, `let me know if you would like`, and `here is a revised version`.

## Writing in the author's voice

The checklist above cleans a draft. The five sections below are for a piece that has to sound like its author. Pick by what the author gave you:

| The author gave you | Use |
|---|---|
| Rough words of their own on this subject, to be tightened | Own-words mode |
| Rough words of their own on this subject, for a finished piece | Anchor mode |
| Finished pieces of their own, for a new version of a piece they have already written | Sentence-bank mode |
| Finished pieces of their own, for a different kind of piece | Carried-voice mode |
| Nothing of their own | No sample yet |

An author's words serve that author only. Never carry one author's samples, sentences or habits into another author's piece, and never fall back on a stock voice.

## Own-words mode

Use this mode when the author hands you their own rough words: a voice memo transcript, a brain dump, messages typed fast, or notes. Give the author's words back, tightened. In this mode you edit with scissors and you write nothing.

You may:

- Cut words and whole sentences.
- Put the author's sentences in a better order.
- Split one of the author's sentences, or join two of them, at a natural break.
- Fix spelling and punctuation.
- Spell out shorthand the author typed.

You may not:

- Write a new sentence, a bridge, a summary line or an ending.
- Swap the author's word for a different word.
- Smooth a rough sentence into a polished one.
- Cut a "not", a "never" or a "no" out of a sentence you keep, or change a number.

When two parts need a bridge, leave the gap open and tell the author which one it is.

At most 5 of every 100 words in the piece may be words the author did not type. The script beside this file counts them. It also fails a piece that holds a sentence the author did not write or that drops a negation from inside a sentence, and it lists each spelling you changed. Run it and fix the piece until it passes:

```
python3 own_words_check.py RAW_FILE EDITED_FILE --cap 5
```

Items 10 and 11 of the checklist still apply as written in this mode. Every other item becomes a flag for the author, so report what you found and change nothing.

Report the piece, the checker's output, each word you added, and each gap you left.

## Anchor mode

Use this mode when the author gives you their own words and wants a finished piece back: a rant typed into the request, a voice memo transcript, rough notes, or a piece they already wrote that needs a new cut for a new reader. Their words are the body of the piece and you build around them.

A piece that is mostly the author's own sentences reads as the author. A piece where you write the sentences does not, however you word it. In tests run in November 2026 against a commercial AI-writing detector, pieces that kept the author's words at 75 or more in every 100 read as human-written each time, pieces a model wrote in full never did, and pieces in between went either way. Treat that as evidence about how the text reads and never as a promise about any detector.

1. **The author's sentences make up at least 75 of every 100 words.** Handle them as own-words mode does: cut, reorder, split, join, fix spelling and punctuation, spell out shorthand. Do not swap their word for yours or smooth a rough sentence.
2. **What you add is plain and concrete.** A supplied fact, a number, a name, a step, or a short link between two of the author's points. Short sentences in everyday words.
3. **Add no commentary.** No sentence that states the author's purpose, sums up, reflects or looks ahead. In the tests one such paragraph changed how a whole piece read, wherever it sat.
4. **Keep the author's sentences together.** Leave their paragraphs whole. Put what you add in its own short paragraph, or as one short sentence at the end of one of theirs. Do not alternate one of theirs with one of yours.
5. **Join with a word or a fact.** If two of the author's parts need a bridge, use `so`, `because`, `and`, or the fact that connects them. Never a pointing phrase such as "Here's why that matters".
6. **Open and close on the author's sentences** whenever their words allow it.
7. **Use only supplied facts.** If the piece needs a fact you do not have, leave it out and ask the author for it.
8. **Never pad.** If the author's words cannot fill 75 of every 100, make the piece shorter or ask the author for more of their own words.

The script beside this file counts the share. Run it and fix the piece until it passes:

```
python3 anchor_check.py RAW_FILE PIECE_FILE --cap 25
```

Items 10 and 11 of the checklist apply as written in this mode. Every other item becomes a flag for the author on their own sentences, so report what you found there and change nothing.

Report the piece, the counter's last line, each sentence you added, and each question for the author.

## Sentence-bank mode

Use this mode when the author asks for a new piece and has given you finished pieces of their own: the samples in `VOICE.md`, or posts and emails they wrote. Treat those pieces as a bank of sentences. The new piece gets its own plan, and its sentences come from the bank.

**This mode has a short reach, and you tell the author when you hit the end of it.** It works when the new piece is the same kind of piece as one in the bank and makes the same kind of points: one pitch reworked for a second product, last year's announcement reworked for this year's. What comes back is a new version of something they have written, and a reader who knows the original will hear it. In the same November 2026 tests, pieces that kept long runs of the author's own wording read as their author, in any sentence order. When the request moved further off (a calm how-to from a bank of rants, a moving notice from a bank of thank-you posts, even a report on a burst pipe from a post about a storm), careful editors could not reach the floor below without padding or dropping facts the reader needed, and every piece that fell short read as machine-written. Treat that as evidence about how the text reads and never as a promise about any detector.

1. **Plan the new piece first, for its own subject and reader.** Decide what it opens on, what the middle says and where it stops. Do not start at the top of one of the author's pieces and walk down it.
2. **For each thing the plan needs said, find a sentence of the author's that does that job:** a verdict, a price comparison, a thank-you, an aside to a second reader. Rework that sentence for the new subject.
3. **Change the fewest words that make the sentence true of the new subject.** Swap the subject, the names, the numbers and the examples. Leave how the sentence opens, how it joins and how it ends.
4. **Keep each of their sentences whole.** One sentence of theirs makes one sentence of yours. Do not join the front of one of their sentences to the back of another, and do not write a clause of your own into one of theirs. In the tests one piece read as machine-written with the editor's words written into the author's sentences, and as the author's once those words were moved into sentences of their own.
5. **New facts come only from the author's notes for the new piece.** A fact that will not fit by swapping a word, a name or a number goes in a short plain sentence of its own. If the new subject cannot support a sentence, leave that sentence in the bank. Never bend a fact to fit a sentence.
6. **When the bank has no sentence for something the piece must say, write it short and plain,** and keep such sentences few.
7. **Leave the author's best-known lines in the bank.** A joke, a catchphrase, a dare, a sign-off, a story: any line a regular reader would recognize on seeing it twice. Build from their working sentences, the ones that state, explain, list, thank or connect. In the tests a piece that read as its author still did with its two best-known lines taken out.
8. **Spread the borrowing when the bank allows it.** If several of the author's pieces can do the job, draw on several. If only one can, tell the author the new piece will read as a version of that one, and ask whether they have more writing of that kind.
9. **At least 60 of every 100 words sit inside runs of three or more words taken from the bank.**
10. **When the bank cannot carry the piece, stop and say so.** Read the bank before you plan. If it plainly holds no sentences for this kind of piece or this tone, stop there. If you cannot tell, build the piece once, honestly, and count. If the floor cannot be met without padding, bending a fact, or forcing in a sentence whose tone does not fit, do not force it and do not game the counter. Tell the author what their writing lacks for this piece (no sentences for instructions, nothing warm, nothing that announces news). Then offer the ways on: they add a piece of their own of that kind to the bank, or they say this piece to you in their own words and you use anchor mode (see No sample yet), or they give you three to five things that happened and you use carried-voice mode. A draft that stopped here is your evidence and is not sent as the piece.
11. **The counter measures borrowed wording and never tone.** If the author asked for a tone and the sentences that carry it are yours, tell them which ones.
12. **Tell the author which pieces and which lines you drew on,** so two pieces built from the same sentences do not go out close together.

The script beside this file measures the share, sentence by sentence and for the whole piece. It also lists the lines carried over nearly whole, the sentences that are part the author's and part yours, and how much came from each bank file. Run it and revise until it passes, or until rule 10 applies:

```
python3 bank_check.py PIECE_FILE BANK_FILE [BANK_FILE ...]
python3 bank_check.py PIECE_FILE BANK_FILE [BANK_FILE ...] --most-from-one 40
```

Items 10 and 11 of the checklist apply as written in this mode. Every other item becomes a flag for the author on wording that came from their bank, so report what you found there and change nothing. Run every item in full on sentences you wrote.

Report the piece, the counter's last line, your plan in three lines, which of the author's sentences you used, what the bank could not cover, and each question for the author.

## Carried-voice mode

Use this mode when the author has given you finished pieces of their own and asks for a different kind of piece: a how-to from someone whose samples are rants, a notice from someone whose samples are thank-you posts. Their sentences will not fit the new piece. Their voice still can.

**What the tests showed.** A model writing a whole piece "in the author's voice" from samples read as machine-written every time it was tried. The same voice laid on in layers, over a plain piece built on true things that happened, did not. In the last test twenty-four fresh writers each got this skill, one author's samples and three things that happened, for two authors and three kinds of piece. All twenty-four pieces read as a person's writing, and blind readers gave all twenty-four to the right author. They called nineteen natural and five an impression, and four of those five came from the author who had given one sample. With one sample there is little to carry, so ask for two or three. That was one week, two authors and one checker. Treat it as evidence about how the text reads and never as a promise about any detector.

1. **Get three to five things that happened,** as in No sample yet, step 4. The author's samples do not replace them.
2. **Write the plain piece first,** by every rule in that step: the first line that says what the piece is, the things that happened, the ration of always-true words, the same name every time, the stop on a thing that happened. In this mode keep that first line to one sentence of about 30 words at most, and move no fact into it later to make room for voice.
3. **Study the samples before you touch the piece.** Ten lines or fewer, each with a quoted example of ten words or fewer: what they call things, how they join sentences, whether they contract, what they do with numbers, how they speak to the reader, how they open, what they are sure of, what annoys them.
4. **Lay the voice on in this order, and use every layer the samples support:**
   - their words for things, swapped into the sentences you already have;
   - their joins and their contractions, inside those sentences;
   - their way of opening, on the first line, as long as that line still says what the piece is;
   - the shape of their sentences, on the always-true sentences.
5. **Carry their marks, three in all.** From your study pick the habits a reader would know them by: a one-word verdict, a sentence that opens on "And,", a question they ask and then answer, an exclamation mark, a bracketed aside, shorthand for money, a stock phrase of theirs. A piece of 250 words or fewer gets three of these in all, and the carried sentence of step 7 and the stance of step 8 each count as one of the three. A longer piece may carry one more for each further 100 words. Each appears once, never two in one sentence, with at least one full sentence between any two, and none bigger than it is in the samples: if their lists run to three items, so do yours. Use each mark where they would. Look at what it does in the samples: if their exclamation marks sit on warm details and their one-word verdict follows a number that surprises, yours do the same. Their words for things, their contractions and their way of opening are not counted, with one exception: a phrase of theirs that a reader would recognize, such as "right here", is a mark wherever it sits, the first line included. Three is the floor as well as the ceiling. In the tests blind readers gave the pieces that carried these marks to the right author every time and called the pieces without them nobody's. The pieces they called an impression stacked four or more marks into a short piece, or set a mark where the author would not have. A mark stays even where a checklist item would flag it, and you name the item in your report.
6. **Leave the facts alone.** Voice changes wording. It never adds a fact, a number or an event, and it never makes a happening bigger than the author told it.
7. **At most one sentence carried whole from the samples, and only a short verdict of theirs:** five words or fewer, with not a word changed, set where they would set it. "Seriously." after a number that is hard to believe travels. A longer sentence of theirs belongs to the piece it came from. In the tests both pieces that carried a 13-word sentence of the author's were called an impression by every reader, because it did not follow from the sentence before it. A carried sentence counts in the ration as an always-true sentence.
8. **One sentence of stance, only where the samples give you one:** something the samples show this author is sure of, grateful for or annoyed by, pointed at this subject. A stance is the author's opinion, so never make one up. If nothing in the samples reaches this subject honestly, carry no stance, make up the three with another mark, and say so in your report. Twelve words or fewer, with no fact and no number in it, and never last. Write it fresh: a sentence of theirs with a few words swapped is a carried sentence, and readers hear the original through it. It has to follow from the happening it sits after: if the same line could be dropped into any piece, it does not belong in this one. It counts as always-true for the ration: where the plain piece has an always-true sentence to give up, the stance takes its place. In the tests a long closing line with three facts and a dare in it read as machine-written, and so did a short opinion added to a short piece with nothing taken out. Blind readers called a piece an impression when its stance was a feeling the writer had supplied, such as gratitude for an evening the author had only described.
9. **Seat every sentence of voice after a whole happening.** That covers the carried sentence, the stance and any other mark that is a sentence of its own, such as a question they ask and answer. Tell the first thing that happened to its end before one appears: nothing sits between the first line and the first happening, and nothing splits a happening in two. Between two happenings there is room for one of them, or for one always-true sentence, and never for two. Leave one gap between happenings empty: a piece with three happenings takes one such sentence in all, and a piece with four takes two. Choose which, leave out a fact that is left over, and let your other marks be ones that live inside a sentence: an aside, an opening word, a punctuation habit. Never cut a happening into two sentences to make room for a mark. In the tests a piece that read as machine-written read as a person's once its stance moved from the middle of the first happening to the end of it, with nothing else changed. Another did once its first line, grown to 41 words to hold the facts that voice had pushed out, was cut to 18. Two three-happening pieces that carried both a stance and an always-true sentence read as machine-written, and each read as a person's with either one taken out.
10. **The piece still stops on a thing that happened.**
11. **Their voice, never their sentences.** Run the counter against the samples. In this mode the number has to come out low: at most 15 of every 100 words inside runs taken from the samples. A higher number means you have drifted into reusing their piece.
12. **Test it before you send it.** Put the piece beside the plain version you started from. If a reader who knows the author could not say which of the two is theirs, you have not carried enough: strengthen the layers of step 4, or trade a mark for one a reader would know them by sooner. Never go past three marks to pass this test.
13. **Only the author can say it sounds like them.** Tell them which habits you carried and which you left out, and ask them to read it.

```
python3 bank_check.py PIECE_FILE SAMPLE_FILE [SAMPLE_FILE ...] --at-most 15
```

Run the checklist on the piece. A habit of the author's that breaks a checklist item stays, and you name the item in your report. Never add an error of your own.

Report the piece, the counter's last line, your study of the samples, what you carried (words, joins, the whole sentence, the stance), the facts you left out, and each question for the author.

## No sample yet

Use this when the author wants a piece in their voice and you hold nothing they wrote. If you hold finished pieces of theirs of another kind, use carried-voice mode.

A model cannot supply a voice. In the same tests, pieces a model wrote from a list of facts did not read as a person's writing: none in twelve different styles from two models, and none from two sets of written rules. What read as the author, every time, was the author's own wording. So get some before you write. Failing that, get three to five things that happened (step 4).

1. **Ask the author to say the piece to you in their own words.** Two or three minutes typed fast or dictated, about 200 words or more, unedited. For a longer piece, ask for about three quarters of the length they want. Rough is good, and extra gives you room to cut. If it helps, give them three plain questions fitted to the piece: what this is or what happened, why it matters to them, and what they want the reader to do. Ask above all for things that happened: who did what, with the numbers.
2. **Count what they have already typed.** Their request, their notes and their earlier messages to you are their words. Ask before you use them, and leave out anything they would not want printed. If those already come to about 200 words on this subject, you can skip the ask.
3. **Then use anchor mode** on what they gave you.
4. **If they would rather not say it themselves, ask for three to five things that happened and write a plain piece around them.** A sentence each is enough: who did what, with the numbers. More is better, because the piece can only be as long as its happenings allow. In the tests a post built on a list of features did not read as a person's writing however it was worded. The same post cut down to its first line and three true things that happened did, every time, and each always-true sentence put back pulled it away again. That was a few dozen pieces in one week, so promise the author nothing. The rules:
   - The first line says what the piece is, in plain words: an offer, a notice, a request, a thank-you, an apology. "This is a notice about the tool library's move." "I'm asking you to come and volunteer at the archive." It may name the thing and say what it is. It is not a drumroll under item 3, because it carries the piece's job and the thing's name in one sentence.
   - The things that happened come straight after it, as plain past-tense sentences with their numbers.
   - **Ration the always-true facts, by weight.** A fact is always-true when it would be true on any day: what a thing costs, what it does, how many parts it has, where to get it. After the first line, the always-true sentences together may take at most one word in five of the whole piece. Count it: add up the words in those sentences and divide by the words in the piece. Two facts packed into one long sentence weigh the same as two sentences, so packing buys nothing. Put each always-true sentence beside the happening it belongs with, and never set two of them back to back. A fact that belongs with no happening, such as where to get the thing, goes in the first line. A dated count ("this year 295 volunteers gave 42,284 hours") is a thing that happened, whatever heading the author filed it under. Leave the other facts out. Tell the author which ones you left out, and that one more thing that happened makes room for more. Never pad to a length with facts: a short piece stays short.
   - **In a how-to,** the list of what is needed and the steps are what the reader came for. Keep them together in the middle, with any caution that belongs to a step beside that step, and leave all of it out of both sides of the ration count. They never come last, so the things that happened split around them: some before, one after.
   - **Call each thing by the same name every time.** If the thing has a name, use the name again: "slop-scrub" each time, never "the checklist" or "the tool" the second time. "It" is fine, and a lower-case name may start a sentence. In the tests one piece changed how it read on those two swaps alone.
   - Nobody performs: no jokes, asides, hooks or feelings the author did not supply.
   - Stop when the things that happened are told, on one of them. No lesson, no summing-up and no closing instruction to the reader.
   - **Facts and happenings come only from the author. Never make one up and never dress one up.** In the tests, made-up happenings did not read as a person's writing even standing alone. If the author has none to give, write it plainly from the facts and say what is missing.

   Run the checklist, and tell the author the piece is in no one's voice. Do not dress it up to sound like a person you invented, and do not borrow anyone else's samples.
5. **If they cannot answer right now,** send the ask anyway. If they need something in the meantime, send a plain draft from their facts with it, labeled as in no one's voice.
6. **Offer to keep what they said** in a file of their own words, once they have looked it over, so the next piece can start from it.

When the job ends in a question to the author, your report is that message: what you need from them, why, and the ways on. Run the checklist on it like any other text that leaves you.

## Output Format

```
SLOP SCRUB REPORT
=================

VOICE: [USED: project-root VOICE.md | NOT FOUND: offer to build one from two author-selected pieces]

1. Word scan: [CLEAN | FOUND: list with line numbers]
2. Construction scan: [CLEAN | FOUND: shapes and verbs]
3. Drumroll scan: [CLEAN | FOUND: list]
4. Metaphor check: [CLEAN | FOUND: list]
5. Sensory check: [CLEAN | FOUND: list]
6. Quietness check: [CLEAN | FOUND: list]
7. Profundity check: [CLEAN | FOUND: inflated claims, empty commentary, or endings]
8. Bartender test: [PASS | FLAGGED: list]
9. Specificity and swap test: [PASS | FLAGGED: paragraph and missing detail]
10. Em dash check: [CLEAN | FOUND: count]
11. Source check: [PASS | FLAGGED: claims and attributions]
12. Contraction check: [CLEAN | FOUND: list]
13. Staccato and repeated length: [CLEAN | FLAGGED: runs]
14. Sales pitch, caveats, and assistant residue: [CLEAN | FOUND: list]

CHANGES MADE:
- [original phrase] → [replacement phrase]
- [original phrase] → [replacement phrase]

CLEANED TEXT:
[full text with all fixes applied]
```

Check and report all 14 items, even when each one is clean.

## Severity (when prioritizing fixes)

**Instant kill (rewrite immediately)**

- Any banned word
- Any em or en dash in output text
- "It's not X, it's Y" and "not only X, but also Y" constructions
- Assistant residue
- Fabricated stats without source notes
- Engagement-bait questions at the end of posts ("What do you think?")

**Strong rewrite recommended**

- Unnecessary groups of three and dressed-up verbs
- Drumrolls and pre-loaded transitions
- Staccato runs of three or more qualifying sentences, and two qualifying sentences when both are uncontracted
- Repeated rhythm across three or more sentences of similar length
- Mid-sentence self-questions
- Sensory language on abstracts
- Endings that hint at significance and unsupported claims of importance elsewhere
- Concept-stacking
- Mixed metaphors
- Sales wording in non-ad prose and vague caveats

**Flag for review**

- Forced quietness or ghostly imagery (sometimes context justifies it)
- Interchangeable passages and missing facts the reader needs
- Unnamed sources and multiple citations that serve the same purpose
- Wording the intended reader would need to read twice
- Contractions or expanded forms that sound wrong for this author
- Two short verdict-like sentences when the rewrite threshold is unmet

## Rules

- Read any project voice guide before editing. Read a project-root `VOICE.md` in full on every run and honor any words and phrases the author avoids. Use the samples to match the author's range of sentence lengths, use of contractions, choice of `I` or `we`, and punctuation within the checklist rules. Preserve their directness and vocabulary. Compare the edited copy with the full range of the approved samples.
- Keep approved samples verbatim. When `VOICE.md` is absent, edit from the supplied material, state the file's absence in the report, and offer to build one from two short pieces the author selects. Never invent a voice, details, or samples for the author.
- When a paragraph needs rebuilding, use the author's supplied facts in the order the author would tell them. A swap of synonyms leaves the paragraph's structure and claims in place.
- Use the full checklist even if the local linter reports zero findings. The editor still decides whether each sentence serves the reader.
- The strongest basis for the edit is the author's own wording, supported by their facts and approved samples. A scrub cannot guarantee a detector verdict. Never add typos, odd punctuation, invisible characters, look-alike characters, or grammar errors to change a score.
- Sweep the draft for em and en dashes again when the edits are complete.
- If the user asks you to scrub a draft and you can't find one to scrub, ask. Don't invent text to scrub.
- Never apologize for finding slop. Finding it is the job. Reporting "clean" when you didn't actually check is the failure.
