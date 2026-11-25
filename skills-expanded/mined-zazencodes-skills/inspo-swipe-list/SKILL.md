---
name: inspo-swipe-list
description: Use or add to the user's saved design inspiration. Use for swipe list or inspo requests, or design work that could draw on the list.
---

# Inspo Swipe List

The list lives at `~/obsidian/AzathHouse/Areas/Inspo Swipe List.md`
in the user's Obsidian vault. It holds things they found online that inspire them:
mostly visual design, also how a video, tool or app looks and feels. Entries
are newest first. It is growing, so always read the current file.

## If the list is not available

When you cannot read the file (other machine, sandbox, no access):

- If the user explicitly asked you to use the swipe list or add to it, stop. Tell
  them you can't reach the list and do not finish the task without it.
- If you loaded this skill on your own because the work could use inspiration,
  give them a one-line warning and carry on without it.

## Using the list for inspiration

1. Read the whole list.
2. Pick the entries relevant to the task. Open their links when the
   description alone isn't enough to work from.
3. If the user named a specific entry, use it. Otherwise, unless one entry is
   obviously right, ask them which to use with your question-asking tool
   (e.g. `AskUserQuestion`), not in prose. Offer your best single
   suggestion first, marked recommended, then an alternative or a group of
   entries to combine. Keep the options to the entries you found relevant.
   They can always answer with something else.
4. Say which entries you drew on and what you took from each.

## Adding to the list

When the user says "add this to my swipe list" (a link, plus what they like about
it):

1. Insert a new entry at the top, directly under the `---` that follows the
   intro, in the existing format:

   ```markdown
   ## YYYY-MM-DD . Short title

   https://link

   One or two sentences on what it is and why the user likes it, in their words
   where possible.
   ```

   Use today's date. Write the title yourself if they didn't give one. Ask for
   the reason only if they gave none and the link doesn't make it obvious.
2. Commit and push in the vault (`git -C ~/obsidian/AzathHouse`),
   staging only this file, following the vault's `AGENTS.md` commit
   convention.
