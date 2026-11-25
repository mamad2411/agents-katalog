---
name: visual-review-page
description: |
  Visual review page: whenever the user explicitly asks to see a plan, decision, or proposal in a
  visual form (a visual plan, a page to look at, a side-by-side comparison of options), builds a local HTML page
  that shows it with real frames, marked screenshots, diagrams, and sound comparisons, and
  collects the user's free-text answers through a bundled local server. Also use when the user
  says they have answered on such a page: reading the answers and revising the page. This is a
  local page for collecting answers, not a published artifact. A plain request to show or discuss
  a plan stays in chat.
---

# Visual Review Page

The page exists for what is hard to agree in chat: things that must be seen, heard, or compared.
Text-only agreement belongs in chat, so the page earns its place by showing.

## Show, don't describe

Whatever can be shown is shown; text captions it and says what to look at. Pick what fits:

- **Variants**: each option shown finished, side by side, on the user's own material.
- **Sizes, zones, positions**: frames drawn over a real frame or screenshot (green: stay inside,
  red: never cross) instead of pixel numbers. Frames must match what is really on screen.
- **Layout or mechanism**: a small diagram of the idea next to the real result.
- **Before / after**: real frames side by side, a red box on the problem.
- **A one-moment error**: the still frame at that moment, or a strip of frames around it.
- **Sound**: one player with a variant switch that keeps the playback position.
- **The result itself** when it can be made in advance, including the awkward cases.

Abstract charts for something visible in the material, or frames that do not match the real frame,
mislead more than text.

## Decisions in plain words

The user agrees on meaning, not on code or instruction text:

- **Skill, prompt, or process change**: what the agent does now and what it will do after, in
  plain words, with a real-life example.
- **Code or script change**: what happens now on a live example, then the new steps in order and
  what that means for the user.
- No code, diffs, or verbatim instruction paragraphs. Exception: wording the user will see as
  written (a message, a caption, UI text) is shown as written.
- The user's words: what they see or get, not file names, parameters, or units, unless the exact
  value decides the question.

## Page shape

One reading column. The top states the overall recommendation, what is needed from the user, and
how to answer: write in the fields, then say so in chat in any words.

Each item is one decision; split anything the user might answer differently. Title says what
changes → visuals → now / after → why → recommendation as a full phrase → question → one answer
field. A "Not doing" list names deliberate exclusions; evidence goes into a collapsed block.

Answers are free text only. An empty field means "not answered", never consent.

## Build and open

1. Create a page folder inside the current project next to the task's work files, so a later
   session can find it. Copy [page.html](assets/page.html) there as `index.html` and media into
   `v/`. Do not commit page folders unless the user asks.
2. Write the content as HTML using the template's components; give each answer field a stable
   `data-id` that never changes or repeats across rounds. Translate the `UI` labels and all page
   text into the user's language.
3. Start the server in the background and open the printed URL in the runtime's built-in browser:

   ```bash
   python3 <skill-dir>/scripts/serve.py <page-folder>
   ```

4. Look at the page in the browser where the user will read it and fix anything that does not
   load or overflows.
5. In chat: the URL and one line saying how many questions are open.

## When the user has answered

When the user says in any words that they have answered, read `answers.json` in the page folder,
revise the plan by their comments, and show the revised page again. Take the plan into
implementation only after the user explicitly tells you to do it: answers on the page agree or
change items, they never start the work. An answer that is a doubt or a question is not agreement.
When the go arrives, read `answers.json` first: if a new answer changes anything, revise and show
the page again instead of starting; if every new answer is plain agreement, start.

- Above each answered field, show what the user wrote and what the agent changed or why not.
- Move `answers.json` to `answers-<round>.json` so the fields start empty for the next round.
- The header says what changed since the last version; agreed items collapse and stay unchanged.
- Restart the server if it stopped, reopen the same page, and report as in step 5.
