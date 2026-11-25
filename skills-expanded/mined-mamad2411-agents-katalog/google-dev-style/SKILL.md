---
name: google-dev-style
description: Write and edit prose the way the Google developer documentation style guide says to — plain, direct, second person, present tense, active voice, sentence case, no filler. Use this whenever you produce or revise text a human will read: READMEs, API and reference docs, tutorials, quickstarts, guides, release notes, changelogs, PR and commit descriptions, code comments, error messages, UI copy, help text, design docs, RFCs, postmortems, and technical explanations in chat. Also use it when someone asks you to make writing clearer, simpler, less bloated, less corporate, less "AI-sounding", or asks you to copyedit, tighten, or proofread. Reach for it by default on writing tasks rather than waiting to be asked.
---

# Google developer documentation style

The full guide is in `references/`. This file is the working subset: the rules
that change almost every paragraph. Read a reference page when you need a
detail this page doesn't settle — `references/INDEX.md` says which page covers
what.

## What this is for

Most bad technical writing fails the same handful of ways: it hides who does
what, it hedges, it pads, it announces itself before it says anything, and it
uses ten words where three would do. The rules below exist to close off those
failure modes. They aren't decoration, and following them is not the same as
writing tersely — a clear sentence is often longer than a vague one.

Apply the *voice and clarity* rules to everything you write. Apply the
*formatting* rules to documents. A one-line answer in chat doesn't need a
heading hierarchy, and forcing document conventions onto a conversational reply
is its own kind of stiffness. Match the artifact.

## The core moves

**Address the reader as "you."** Not "we," not "the user," not "one." Use "the
user" only for the person who uses the software your reader is building. Use
"we" only for the organization publishing the document, and only after you've
named it.

> Consider adding a description to your table.
> ~~Let's add a description to our table.~~

**Give instructions in the imperative.** The "you" is implied. "Click Submit,"
not "You should click Submit" and not "the Submit button should be clicked."

**Use active voice.** Make clear who performs the action. Passive voice lets
you drop the actor, and then the reader can't tell whether they, the server, or
some third party is supposed to do the thing.

> Send a query to the service. The server sends an acknowledgment.
> ~~The service is queried, and an acknowledgment is sent.~~

Passive is right when the object genuinely matters more than the actor ("The
file is saved"), when naming the actor would be accusatory ("Over 50 conflicts
were found in the file" beats "You created over 50 conflicts"), or when nobody
needs to know who acted.

**Use present tense.** Describe how the thing works, not how it will work.
Reserve "will" for something that genuinely happens later than the sentence
you're in: "The file will be archived the next time the backup runs." Avoid
hypothetical "would" entirely — rewrite as a conditional with a present-tense
result.

**Put the condition before the instruction.** The reader can then skip the
instruction when it doesn't apply to them, instead of reading it and
backtracking.

> To delete the entire document, click Delete.
> ~~Click Delete if you want to delete the entire document.~~

> For more information, see [the other doc].
> ~~See [the other doc] for more information.~~

The same ordering holds inside a procedure step: say where before you say what.
"In the Google Cloud console, go to the Monitoring page" — not the reverse.

**Say must, can, might — not should.** "Should" is genuinely ambiguous: the
reader can't tell whether they have to do the thing. Required is *must* or a
bare imperative. Optional is *can*. Possible outcome is *might* or *can*.
Recommended is *We recommend that you…*. "Should" is only safe for
near-universal advice ("You should use a strong password").

**Don't attribute human qualities to software.** A parser doesn't "see," "know,"
"want," "try," "decide," or "understand." Say what it does.

> The PC detects a new device.
> ~~The PC sees a new device.~~

**Write timelessly.** A doc has no idea when it's being read, so words that
point at "the moment of writing" go stale or were never true. Cut *currently,
now, new, newer, latest, soon, old, older, existing, at present, as of this
writing, eventually, in the future, does not yet*. "The emulator supports these
filters" — the "now" was never carrying meaning. If you truly need "new," anchor
it to a version or date.

Time words are fine in release notes, changelogs, and blog posts, which *are*
anchored to a moment.

**Don't overclaim.** Avoid superlatives — *best, simplest, fastest, never,
always* — and be careful with *ensure* and *guarantee*, which should only appear
when something really is guaranteed. The same caution covers the marketing
adjectives the guide doesn't name: *seamless, powerful, robust, blazing-fast*
assert things nobody can check. Performance and cost claims need a source the
reader can check. A security claim becomes false the day someone breaks the
product, so write "helps protect against" rather than "prevents."

**Cut the ceremony.** No "please" in instructions. No "it's easy," "simply,"
"just," "quickly," or "it's that simple" — if it turns out not to be easy, you've
told the reader the problem is them. No exclamation points outside a tutorial
milestone. No pre-announcing what the paragraph is about to do.

## Words

The guide's word list is opinionated and long. `references/avoid-words.md` holds
the 231 entries that say "don't use" or "avoid" — scan it when a word feels
shaky. `references/word-list.md` is the full 597 entries.

The ones worth knowing without a lookup:

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| commence | start, begin |
| consequently | so |
| in order to | to |
| a number of | some, many |
| allows you to | lets you |
| via | with, by, through |
| e.g. / i.e. | for example / that is |
| etc., and so on | rewrite the introduction so the list is obviously partial |
| and/or | and, or, or "X, Y, or both" |
| aka | also known as |
| above / below (in a doc) | preceding / following, or link to the section |
| abort | stop, cancel, end, exit |
| execute (of a program) | run |
| desire | want |
| agnostic | platform-independent (or whatever it actually means) |
| blacklist / whitelist | denylist, blocklist / allowlist — as nouns only, never verbs |
| master / slave | primary / replica, or the domain's own terms |
| sanity check | quick check, confidence check |
| dummy variable | placeholder (or, in statistics, indicator variable) |

Also: no jargon you haven't defined. If a term is load-bearing, gloss it in
parentheses on first use or link a definition. If it isn't, write around it —
"when the project is finished, review what worked" instead of "hold a
post-mortem."

Avoid figures of speech generally. Metaphors, idioms, sports references, and
holidays translate badly and exclude readers. Ableist metaphors go regardless of
how idiomatic they feel — *crazy, insane, blind to, cripple, dumb, sanity check*
all have a more precise replacement ("baffling outliers," "slows the service,"
"final check"). So do the violent ones: a connection *doesn't respond* rather
than *hangs*, and you *click* rather than *hit*.

When an established non-inclusive term would confuse readers if it vanished,
name it once in parentheses on first use, then use the inclusive term
throughout.

## Sentences and paragraphs

Short sentences. Standard subject-verb-object order, with the subject and verb
near the front. If a sentence has more than one idea, it's usually two
sentences.

Keep helper words that conversational English drops — *that, then, of, which*.
They cost a syllable and remove a garden path.

> If the attribute key isn't found, then the default value is returned.
> ~~If the attribute key is not found, the default value is returned.~~

> You can update the rules that you previously defined.
> ~~You can update the rules you previously defined.~~

Use contractions, especially negative ones. *Don't* is harder to misread than
*do not* when someone is skimming, because the eye can skip a standalone "not."

Keep terminology identical across a document. If it's a "job" in one section,
it's not a "task" in the next. Variation reads as a distinction the reader then
hunts for.

One idea per paragraph, most important sentence first. Past five or six
sentences, a paragraph is usually two paragraphs — though a single-idea
paragraph can run long, and a one-sentence paragraph is fine.

Don't start every sentence the same way ("You can… You can… You can…").

## Headings

Sentence case. No terminal period. No links, no numbers for sequence, no empty
headings, no skipped levels, one H1 per page.

Task sections get a bare verb: "Create an instance," not "Creating an instance."
Concept sections get a noun phrase: "Migration to Google Cloud," not "Migrating
to Google Cloud." Avoid an -ing word as the first word of any heading — it
translates inconsistently and eats space. ("Billing" and "Pricing" are fine;
there's no alternative.)

Prefix a heading with `Optional:` when the section only applies to some readers.

## Lists

Introduce a list with a complete sentence, not a fragment the items complete.

> Use the Submit button for any of the following purposes:
> ~~Use the Submit button to:~~

Colon if the list follows immediately; period if something sits in between. A
heading alone can introduce a list with no lead-in sentence.

Numbered for sequence, bulleted for everything else, description lists for
term-and-definition pairs. Never a one-item list.

Keep the items parallel — same grammatical shape throughout. Start each with a
capital letter. End each with a period *unless* the item is a single word, has
no verb, is entirely code, or is entirely link text. Inconsistent punctuation
within one list means the list needs rewriting, not patching.

Serial comma always: "zones, regions, and multi-regions."

## Procedures

One action per step, each step a complete sentence starting with an imperative
verb. Combine only sequential menu picks: "Click File > New > Document."

Order within a complex step: the action, then the command, then what the
placeholders mean, then any explanation, then the output, then the result in its
own paragraph.

Say `Optional:` at the front of an optional step, not "(optional)" at the end.

Skip "run the following command" — say what the command accomplishes and let the
code block speak. "In Cloud Shell, deploy the load generator:" beats "Run the
following command to deploy the load generator:".

A single-step procedure is a single bullet, not a numbered list of one.

Don't send readers to keyboard shortcuts or directional language ("the button in
the upper right," "see the diagram below"). Use the element's name, or
"preceding"/"following."

## Links

Link text must make sense read alone, because screen reader users jump link to
link. Use the destination's title or a descriptive phrase with the important
words first. Never "click here," "this document," "read more," or a bare URL.

When a cross-reference gets its own sentence, use the standard phrasing: "For
more information, see X." Or "For more information about Y, see X" when the
reason isn't obvious from context. It's *about*, not *on*.

Be selective — every link is a chance for the reader to leave and not come back.
If two sentences of context would do the job, write the two sentences.

## Formatting

**Bold** for UI element names and run-in headings. Nothing else.

*Italics* for a term you're defining on first mention, for words used as words,
for full-length work titles, and for math variables. Sparingly.

`Code font` for anything the reader would type or that appears verbatim in code:
filenames, paths, class and method names, flags, HTTP status codes, console
output, placeholders. Give code elements a noun to attach to — "the `example.yaml`
file," not a bare `example.yaml`. Don't form a possessive from a code item.

Underline is only for links. Never override fonts, sizes, or colors.

Sentence case for headings, titles, table cells, captions, list items, glossary
definitions, and text after a colon.

## Punctuation

Em dashes with no surrounding spaces, for a genuine break in the sentence — like
this. En dashes: don't. Hyphens for ranges: 2012-2016.

Never a spaced hyphen or dash as a substitute for a colon: "Example: this is an
example," not "Example - this is an example."

Semicolons: avoid unless joining two closely related independent clauses, or
separating list items that carry their own commas.

Parentheses: readers skip them, so nothing important goes inside. Prefer "—for
example, `my-instance-99`" over "(for example, `my-instance-99`)".

Straight quotation marks and apostrophes, never curly. Commas and periods go
inside quotation marks — except around a literal string, where anything extra
inside would be wrong.

No ellipses in your own prose. No ampersands as "and." No slashes as
alternatives — write "or." One space between sentences.

## Numbers, dates, and units

Spell out zero through nine and any number that starts a sentence. Numerals for
10 and up, and always for versions, technical quantities, measurements,
percentages, prices, decimals, and dimensions ("6 queries per second," "version
3," "8 pixels," "40%", "192x192").

Spell out ordinals: first, twelfth.

Dates get the month spelled out and a four-digit year: January 19, 2017. Numeric
form only when forced, and then ISO: 2017-04-15. Never 04/05/09 — it means three
different dates in three different places.

Times use the 12-hour clock with capital AM/PM and a space: 3:45 PM, 3 PM.

No seasons. "In November and December," not "in winter" — the hemispheres
disagree.

Space between number and unit; don't pluralize the abbreviation: 64 GB, not
64GBs.

## Examples and names

Use `example.com` and its siblings for domains. Use a genuinely diverse set of
personal names in examples, not five variations on the same culture. Prefer a
calendar day above 12 in a sample date so it can't be read as a month.

## Working on someone else's text

When you're editing rather than drafting:

- Fix the voice and clarity problems first — passive constructions with a
  missing actor, hedges, filler, anthropomorphism, time words. That's where the
  reading experience actually changes.
- Preserve the author's meaning and their technical claims exactly. If a
  sentence is unclear because the underlying fact is unclear, ask rather than
  guess a meaning into it.
- Don't restyle text that's already fine to prove you did something.
- Say what you changed and why, briefly, if the user will need to defend the
  edits to someone.

## When the rules fight the reader

This guide is a house style, not grammar law. Deviate when following it would
make a passage worse — and be able to say why. What doesn't bend: sentence case
in headings, descriptive link text, second person, active voice, present tense,
and the inclusive-language entries in the word list. Those exist because
readers, translators, and screen readers depend on them, not because someone
preferred the look.
