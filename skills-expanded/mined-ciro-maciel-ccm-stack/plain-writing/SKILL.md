---
name: plain-writing
description: Write and clean up text with no emoji, filler, machine tells, invented facts or jargon. Use for docs, READMEs, PRs, release notes, UI copy.
---

# Write like a person

Plain writing respects the reader's time: every sentence carries something they need, in words they already use.

## Remove

- **Emoji and decorative symbols.** An icon from the design system carries a state; the word carries the meaning. A hook refuses new emoji in files.
- **Filler openers and closers.** "Great question", "It's worth noting", "In today's fast-paced world", "I hope this helps", "Let me know if you have any questions".
- **Inflated words.** "Leverage", "robust", "seamless", "cutting-edge", "delve", "elevate", "unlock", "empower", "game-changer".
- **Hedging stacks.** "It might potentially be possible that". Say what you know and how you know it.
- **Belittling words** about the reader's work or business: "just a small shop", "simple little app", diminutives.
- **Internal names.** Code names, file paths, team jargon and project nicknames the reader has never seen.
- **Invented facts.** Every number, date, quote and comparison must come from a source you can point at. If you have none, cut it.
- **Promised effects.** "Faster", "more reliable", "should finish sooner", "so you can...": an effect nobody measured or stated is an invented fact. Say what changed ("sync reuses one connection across pages") and stop. In release notes and changelogs, each item says only what its commit says; a doubt goes to the author as a question outside the notes.

## Prefer

- **Short sentences, active voice, concrete subjects.** "The hook refuses the commit", not "The commit is refused by the hook mechanism".
- **The specific over the general.** "Saves the draft every 5 seconds", not "keeps your work safe".
- **Lists only for parallel items** a reader scans; prose for reasoning.
- **One term per idea.** Pick "workspace" or "project" and keep it.
- **Headings that say the point**, not "Overview" or "Introduction".

## Check before you hand it over

Read it aloud. Cut every sentence that would not be missed. Search for the words in "Remove". Confirm that every claim has its source. Then say in one line what you cut.
