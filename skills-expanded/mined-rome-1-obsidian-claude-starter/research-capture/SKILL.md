---
name: research-capture
description: Turns a link, article, paper, video transcript, book passage or chat conversation into a research note in Knowledge/ that keeps what the source says separate from the user's own view, records where every claim came from, and links related notes. Use when the user says "save this article", "take notes on this paper", "research X and write it up", "capture what we just figured out", "add this to my knowledge base", runs /research-capture, or pastes a URL with "remember this". Not for meeting notes (use meeting-notes) or decisions (use decision-record).
argument-hint: "[URL, file, or topic]"
---

# Research capture

A research note is useful later only if you can tell what a source said, what you concluded, and how much to trust each.

## 1. Get the material

- URL: fetch it. If it cannot be fetched (paywall, login, error), say so and ask the user to paste the text. Never write a note from the title or from memory as if you had read the source.
- File (PDF, transcript): read the parts that matter to the user's question.
- A topic to research: search, then read the sources you will cite. Prefer primary sources over summaries of them.
- A conversation: the source is the conversation; note that it is unverified.

## 2. Find the question

Ask, or infer from context: what does the user want to know or remember?
A note organized around a question is easier to reuse than a summary of a whole source.

## 3. Check for an existing note

Grep `Knowledge/` for the topic. If a note exists, add to it (new source, new claims, updated view) instead of creating a duplicate.

## 4. Write the note

From `System/Templates/Research-Note.md`, in `Knowledge/Title-Case-Name.md`:

- **Question**: one line.
- **What the sources say**: claims, each followed by its source. Quote only when wording matters, and mark quotes.
- **What I think**: the user's view if they gave one; otherwise leave a prompt for them, or offer your own reading clearly marked as yours.
- **Open questions**: what is still unknown, including anything you could not verify.
- **Related**: typed links (`related_to::`, `part_of::`) to projects and other notes.
- Frontmatter: `sources:` lists every URL or reference; `status: draft` until the user has reviewed it.

Before finishing, run the checks in [references/source-checklist.md](references/source-checklist.md).

## 5. Hand over

Give the user a three-line summary and the link to the note.
Name any claim you could not verify and any source you could not open.
