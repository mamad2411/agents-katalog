---
name: write
description: Load before drafting text for a reader outside this conversation, such as a README, documentation, a docstring, release notes, a pitch, an email, or a draft shaped in chat. An opinionated house style that puts correct facts and clear ideas ahead of brevity.
license: MIT
---

# Write

## When It Applies

The skill applies at handover, and the project's own conventions come first.

- **Handover** is the moment a text is finished for you. It comes when the
  text goes out, when you hand a draft to someone to send or publish, or when
  the person accepts the text, or a part of it, and the conversation moves on.
- **Text that stays in the conversation is exempt,** such as thinking on
  paper, exploration, or a draft you and the person are still shaping.
- **The project decides structure.** Its conventions set which sections exist,
  their order, their headings, and the line width. This skill writes what goes
  inside them. A section the convention requires stays, even when one sentence
  fills it.
- **A requested tone wins.** When the person asks for a level of formality,
  write to it.
- **Other languages** keep the principles and the facts. The sentence traps and
  examples are written for English, so let the language's own grammar decide
  their details.

## Principles

These call for judgment. A text can avoid every trap below and still read like
paperwork.

1. **Write to a person, not for a record.** Say what you mean plainly, as you
   would to a colleague who asked, in a tone that is neither stiff nor chummy.
2. **Spend the reader's attention on what's new to them.** Leave out what they
   already know, and say what they would otherwise have to find out alone.
3. **Clarity comes from the idea and its context, not from the wording
   alone.** When a sentence stays unclear after a few rewordings, work out the
   idea, or the context the reader is missing, before writing it again.
4. **Give a reference a refresher when the reader may need one.** A synonym, a
   phrase, or a sentence beside a term or a link often spares the reader a
   detour.
5. **Be concise, never compressed.** Cut whole sentences that carry nothing,
   and keep every word that lets the rest read in one pass.

## Collect Facts and Sources

An invented sentence reads as smoothly as a checked one, so rereading a draft
won't catch it. That is why the facts come first.

- **List the facts before any prose,** each with its source: a file and line,
  a URL, a command you ran with what it printed, or something the person told
  you.
- **Source every claim specific to the subject,** such as its people, its
  numbers, or its history. General knowledge, such as how a standard library
  behaves, needs none.
- **Use the facts that serve the reader,** and drop the rest even when they're
  true. The full list, with every source, would clutter the text, so keep it in
  your working notes. The text still cites a source wherever the reader needs
  one.
- **Mark your own inferences as yours.** A consequence you worked out from the
  sources is often the most useful part of the text, so say it, and say it's
  yours. In someone else's voice, put it beside the draft as a note for them
  to confirm.

  The venue confirmed a hall for 80, and you're drafting the invitation Marta
  will send to her club.

  > **Before**, in the invitation: "We've confirmed room for up to 120, so bring
  > a friend."
  >
  > **After**, in the invitation: "The hall seats 80."
  > Beside it, for Marta: "From the floor plan, I think the hall could take 120
  > without the tables. I haven't checked with the venue, so confirm it before
  > you promise it."

## Sentence Traps

These patterns can make a reader stop and reparse. The ones marked *Fix* are
almost always worth fixing. The ones marked *Judge* depend on the reader and
the medium. None of them governs vocabulary, so a technical term or a name stays
as it is.

- **Garden-path sentence:** an early word invites a reading that the rest of
  the sentence overturns. *Fix:* add a comma or a word, or change the order:
  "while Anna dressed, the baby played in the crib", not "while Anna dressed
  the baby played in the crib".
- **Stacked negation:** negatives that make the reader flip the meaning more
  than once. *Fix:* rewrite with one: "the train often skips this station",
  not "it's not unusual for the train not to stop here".
- **Hidden actor:** a passive that leaves out an actor you know. *Fix:* name
  it: "the script deletes the old logs", not "the old logs are deleted".
- **Nominalization:** an action turned into a noun, which hides what happens.
  *Fix:* use the verb: "the upload stops and shows an error", not "an upload
  failure occurs".
- **Telegraphic style:** articles, verbs, and connectives dropped to save
  space. *Judge:* match the register your audience expects, such as a team
  that writes terse status notes, and when in doubt, keep the small words that
  carry the logic. When you replace a colon, a semicolon, or a dash with a full
  stop, write out the link it stood for.

  > **Before.** "Meeting moved: Thursday. Room TBC, bring slides."
  >
  > **After.** "The meeting has moved to Thursday. The room is still to be
  > confirmed. Bring your slides."

- **Center embedding:** one clause nested inside another, so the reader holds
  the outer one open. *Judge:* unnest it where you can: "The manager hired a
  team. The team wrote the report, which was late", not "The report the team
  the manager hired wrote was late."
- **Overloaded sentence:** several ideas packed into one sentence. *Judge:*
  split it when its parts read better apart, and keep it whole when splitting
  would sound unnatural. No word count decides it.
- **Noun stack:** nouns piled up as modifiers, which leaves the reader to work
  out how they relate. *Judge:* "the account deletion request form" reads more
  easily as "the form a user fills in to delete their account".
- **Distant antecedent:** a pronoun such as "it", "they", or "this" that the
  reader can't tie at a glance to its antecedent, the noun it stands for. The
  noun sits far back, or other nouns stand in between and any of them could be
  the one meant. *Judge:* name the noun again.

  > **Before.** "The script reads the config, checks the cache, and writes the
  > report. If it is missing, the run stops."
  >
  > **After.** "… If the config is missing, the run stops."

## Revising

An edit follows the same order as a draft, starting from the facts. A
sentence's structure was built for the facts it carried, so a new fact can
outgrow it.

- **Patch or rewrite.** If the sentence still makes its point with the new
  fact, patch it. If the point shifts, list the facts again and write the
  sentence fresh.
- **Read one level up.** An added sentence can repeat, contradict, or bury
  something the paragraph already said. If the paragraph's point has shifted,
  rewrite the paragraph, then check the section the same way.
- **Ask before the climb outgrows a paragraph.** When a small edit starts to
  pull in more than a paragraph of rewriting, stop, say what you'd change, and
  confirm with the person before going on.
- **Stop climbing** at the first level whose point still holds.
- **Fix the old sentence** when a new fact makes it wrong, rather than adding a
  correction after it.

## Final Check

Every text gets your own reread before it goes out. Some also get a cold
read.

- **Reread it yourself first,** as the person it's for, and look twice
  wherever one of these turns up. Each marks a place to look, never a verdict:
  - a hedge on something you know
  - a paragraph you could delete with nothing lost
  - a reference they can't place, or one the text never introduced
  - a fact missing from your fact list, or listed there without a source
  - one of the sentence traps
- **Add a cold read,** a reading by someone with none of your context, when
  your audience won't share your context and the text gets one shot, as with
  an email, a README, release notes, or an instruction file. The next section
  says how.
- **Stop at your own reread** for text that stays in the chat, or a small local
  edit. A draft shaped in chat that the person will send or publish still gets
  a cold read.

## Cold Read

A cold read hands the text to a reader with none of your context. That reader
finds the gaps your own reread passes over, since your context fills them in
for you.

- **Start a reader with the text and one line on who it's for,** in a
  subagent or a new session. It never sees this conversation, the files you
  read, your notes, or this skill.
- **Ask for questions, not rewrites.** Tell it to read as that person, and to
  list what it had to reread, what it couldn't resolve, and what it would need
  another source to follow. For each one, it quotes the passage.
- **Judge each question yourself.** A question shows where the reader lost
  the thread, not what to change. The cause may be a word, missing context, or
  an idea you haven't settled yet, as the third principle says, so fix the
  cause, which may sit outside the passage the reader quoted. Some questions
  need no fix: a cold reader may ask for more precision than the text means to
  give.
- **Offer more when the person may want it:** a second reader, more rounds
  until the text settles, or the readers' reports to see.

## Environment

What a cold read takes depends on the tools you have.

- **Where you can start a subagent or a new session,** run the cold read
  without asking, unless the person's instructions limit background work.
- **Where you can choose the reader's model,** pick one a tier below yours. It
  shares fewer of your guesses, so it stalls where a hurried person would, and
  it costs less. With two readers, run the second on your own model. Go no
  lower than a mid-tier model for either.
- **For Claude models,** the first reader is Opus for a Fable session and
  Sonnet for any other. A second reader runs on the session's own model, or on
  Sonnet for a Haiku session.
- **Where you can't,** suggest how the person could run one: open a new
  session or chat, paste the text with the request under "Ask for questions,
  not rewrites" in Cold Read, and bring back the questions.
