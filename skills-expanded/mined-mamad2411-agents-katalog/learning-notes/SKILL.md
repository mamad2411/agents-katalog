---
name: learning-notes
description: Turn something read, watched or attended into a durable atomic note in the user's Obsidian vault — capture, processing into the user's own words, linking to notes that already exist, extracting the actionable change, and reviewing or quizzing on it later. Use this skill whenever the user pastes an article, paper, talk, RFC or documentation and asks to summarise it, says "add this to my notes", "make a note from this", "process this into my vault", finishes a book, course or conference talk, wants spaced-repetition cards written, or asks to be quizzed on something learned earlier. Trigger on casual phrasings too — "worth keeping?", "what should I remember from this", "quiz me on my Kubernetes notes". Not for drafting original documents, blog posts or specs, and not for answering a one-off factual question the user has no intention of keeping.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Learning Notes

A good note states one thing the user now believes, in their words, linked to what they already know, with the source attached — and it is still useful a year later.

A summary is not a note. A summary compresses someone else's structure, which means it inherits their emphasis, their vocabulary and none of the user's context. It reads fine on the day it was written and is dead within a month, because there is no reason to return to it and nothing in the vault points at it. The three failure modes this skill exists to prevent: hoarding sources instead of processing them, generating the user's beliefs for them, and writing notes nothing links to. The value of a note is created in the act of writing it, so the agent's job is to interrogate and structure, never to author the conclusion.

## Scope

Use for: processing an article, paper, book, course or talk into notes; converting rough capture into permanent notes; building or refreshing an index note; writing spaced-repetition cards; running a review or quiz session from notes that already exist.

Do not use for: writing original prose the user will publish, answering a question they just want answered, or dumping a source into the vault unprocessed. If the user wants the gist of something and nothing kept, just answer them.

## Decide what the source deserves

Not everything earns a permanent note. Classify first, then spend effort accordingly.

| What the source actually gave | Classification | Action |
| --- | --- | --- |
| A claim that changes how the user would act or argue | Permanent note | Full processing, Workflow 1 |
| Useful but only as a record that they read it | Literature note | Metadata plus 3-6 bullets in their words, no claim title |
| A fact they will look up again anyway (flag names, API shapes) | Reference | Link it from an index note; write no note |
| Something they must recall unaided under pressure | Permanent note plus review cards | Workflow 1, then Workflow 4 |
| Nothing they did not already believe | Nothing | Say so plainly and stop |

Say which classification applies before writing anything. "This is a literature note, not a permanent one" is a useful sentence.

## Workflow 1: Process a source into a permanent note

1. **Capture the source metadata first** — URL or ISBN, author, publication date, date read. Retrofitting a citation six months later is how orphan notes are born.
2. **Find the claim, not the topic.** Ask what in the source is contestable. If the source contains three separable claims, that is three notes, not one long one. One idea per note is what makes a note linkable.
3. **Interrogate the user; do not write their beliefs.** Ask two to four short questions and wait for answers: what is the one thing you would defend from this, where do you disagree with the author, what does this connect to that you already have, and what would you do differently at work on Monday. Draft only from their answers. If the user asks for the note to be written outright, write the structure and mark the belief lines as `[TK: your words]` rather than inventing a position for them.
4. **Title the note as a claim.** A claim title can be linked to, argued with and reused; a topic title becomes a junk drawer.

   | Topic title (weak) | Claim title (strong) |
   | --- | --- |
   | Rate limiting | Rate limiting belongs at the edge, not in the service |
   | Postmortems | A postmortem without an owner and a date is a diary entry |
   | Kubernetes autoscaling | HPA on CPU misprices any workload that blocks on I/O |

5. **Link before saving.** Search the vault for related notes and propose three to five wikilinks, including at least one the new note disagrees with or complicates. This is the step everyone skips, and an unlinked note is a note the user will never find again. If nothing in the vault relates, that is a signal the topic is new — say so and suggest where it should hang.
6. **Extract the actionable change, or state that there is none.** One line: what the user will do, change or stop doing. "No action, belief update only" is a legitimate and common answer; a fabricated action item is worse than none.
7. **Write the file** using the standard format below. Read `references/obsidian-conventions.md` for frontmatter fields, tag discipline, filename and folder conventions before writing into the vault.

## Workflow 2: Quick capture

When the user is mid-something and wants it parked, do not run Workflow 1. Write the short capture format below in under a minute, set `status: inbox`, and stop. Processing happens later, deliberately. Offer once — "want me to process this properly now?" — and accept no.

## Workflow 3: Progressive summarisation, done honestly

When the user pastes a long source and wants it condensed for later reading:

- Layer 1 is the source. Layer 2 is a small set of passages worth returning to — target under 5% of the text. Layer 3 is bold inside those passages, only where a sentence carries the whole argument.
- If more than about a fifth of a paragraph is highlighted, nothing in it is. Cut until the highlights alone read as an argument.
- Highlights are input to a note, not a substitute for one. A file of highlights with no permanent note attached is unprocessed material, and should be labelled that way.

## Workflow 4: Write review cards

Only for material the user must recall unaided — an exam, a certification, a command run during an incident, a definition they have to produce in a meeting. Anything they would look up in normal work does not get a card; reviewing it is a hobby, not learning.

Core rules, expanded with examples in `references/spaced-review.md`:

- One fact per card. A card asking for three things is three cards.
- Phrase the question so exactly one answer is correct. "What does `kubectl drain` do?" is vague; "Which two things does `kubectl drain` do that `cordon` does not?" is answerable.
- Prefer "why" and "when" cards over "what" cards for concepts. Recognising a definition is not the same as knowing when to reach for the thing.
- No cloze deletions over list items — they teach position in a list, not the content.
- A card the user cannot answer in ten seconds is a badly written card, not a knowledge gap. Break it up.

## Workflow 5: Review and quiz mode

When asked to quiz, pull questions from notes that already exist in the vault — never from the model's own knowledge of the topic, or the session tests something the user never wrote down.

1. Pick a scope (a tag, a folder, a MOC, or notes due by the schedule in `references/spaced-review.md`) and confirm it in one line.
2. Ask one question at a time. Wait for the answer. Do not reveal the note.
3. Grade against what the note actually says. Say "wrong", or "partial — you missed the second condition", and quote the line they missed. Encouragement that hides an error costs the user the next test.
4. Track misses. At the end, list what was wrong and why, and propose the fix: rewrite the card, split the card, or fix the underlying note if the note itself was vague.
5. Interval changes follow the result, not the mood. Missed cards reset; clean answers step forward.

## Standard output format: processed note

```markdown
---
source: https://example.com/article
author: Author Name
date: 2026-08-04
status: permanent
tags: [note/permanent, source/article]
---

# Rate limiting belongs at the edge, not in the service

**Claim.** One or two sentences stating what the user now believes.

**Why.** The argument in the user's own words — mechanism, not summary.
Three to six sentences. If a phrase is the author's, quote it and attribute it.

**Friction.** Where this is wrong, where it does not apply, or what it
contradicts. A note with no friction section usually means the source was
skimmed rather than read.

**So what.** The one thing that changes, or "belief update only".

**Related.** [[Existing note this supports]] · [[Existing note this contradicts]]

**Source.** Title, author, date read, and the one passage worth rereading.
```

## Standard output format: quick capture

```markdown
---
source: <url>
status: inbox
tags: [note/capture]
---

# <working title, topic is fine here>

- Why I kept it: one line.
- The bit that mattered: one quote or one sentence.
- Open question: what I would need to check before believing it.
```

## Anti-patterns

- **Hoarding sources instead of processing them.** A read-later queue of 400 items is a to-do list the user has already failed. If the inbox is large, propose processing three notes and deleting the rest unread, rather than triaging forever.
- **Letting the model write the note.** A note in the agent's voice records the model's beliefs, not the user's, and it is unusable in an argument later. Structure and interrogate; leave the claim to them.
- **Highlighting everything.** Undifferentiated highlights are a second copy of the source with worse formatting.
- **Building the taxonomy before the notes.** Nested folders and a tag ontology designed on day one is procrastination wearing a system's clothes. Links first; structure emerges from about fifty notes, and an index note is cheaper than a folder tree.
- **Topic titles.** "Kubernetes networking" cannot be linked to meaningfully, so it collects unrelated fragments until it is unreadable.
- **Reviewing what you would look up.** Flags, ports and API signatures belong in a cheatsheet note, not a review queue. Cards for them create work that feels like learning.
- **Notes with no outbound links.** They are write-only. Refuse to finish a permanent note without at least one link or an explicit statement that this is the first note in a new area.

## Reference files

- `references/obsidian-conventions.md` — read before writing into the vault: frontmatter schema, tags as types rather than topics, wikilink and alias conventions, filename and folder rules, when a map of content earns its keep.
- `references/spaced-review.md` — read for Workflows 4 and 5: interval schedule, card patterns with good and bad examples, grading rules, and how to repair a card that keeps failing.
