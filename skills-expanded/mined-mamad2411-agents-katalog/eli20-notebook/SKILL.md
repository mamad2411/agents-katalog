---
name: eli20-notebook
description: Use when substantial or initially unstructured source material should become a browsable HTML notebook organized into understandable sections, with both visual explainers and concise summaries.
license: MIT
---

# eli20-notebook

Create one standalone notebook directory. It runs from local files and needs no package installation or web server. Treat that directory as the complete portable unit: keep every runtime asset and generation script inside it, and use same-directory relative paths so it continues to work when copied or moved.

## Build

1. Resolve the directory containing this `SKILL.md`, create the output directory, and copy every bundled notebook file into it:

   ```sh
   cp -R "<this-skill-directory>/assets/notebook/." "<output-directory>/"
   ```

2. Survey the whole source before producing documents. Make an ordered section plan. For every section, record its number, title, source range or relevant parts, and a short list of the ideas or operations it must explain. Use the source's existing chapters when they help. For unstructured material such as a program, derive sections from its purpose, entry points, major flows or responsibilities, dependencies, and practical operation. Include enough local context that a newcomer can follow a section without having to rediscover omitted basics.

   Use the [live sample](https://game-dev-rta-club.github.io/eli20/sample/) as a format reference only. It condenses an English source of about 16,000 words; its six sections and screen counts are examples, not targets. Let the source's length and conceptual density determine how many sections and Visual screens the notebook needs.

   When an existing chapter is too dense to teach comfortably, split it into smaller sections. Section markers are text, so `1-1`, `1-2`, `1-3`, `2-1`, and so on can preserve the source hierarchy while giving each Visual and Summary a readable scope.
3. Replace the sample data in `book-config.js` from the section plan. Keep the information needed to create the notebook in its free-form `creationNotes` strings: use the notebook-level string for shared source context, audience, language, translation approach, and requester guidance; use each section's string for its source range, required coverage, and any context needed to create that section without rediscovery. These strings are creation context, not progress tracking. Also set the notebook title, the `titlePage` id and `00-title.html` source, optional external `resources`, and each section's id, optional marker, title, and documents. Leave the timestamp fields in place; the bundled build system automatically records its creation and update times. List each section's documents in the fixed order `visual`, then `summary`, give each document an id, type, and source, and point the summary entry to the generated `.html` file. The runtime ignores `creationNotes` and supplies the English interface labels `Title`, `Section`, `Visual`, and `Summary`. Unless the requester chooses another language, write notebook titles and generated explanations in English.
4. Organize execution for the current host:

   - **Codex:** Call `create_goal` after `book-config.js` contains the complete section plan and creation context. Restate all remaining production steps from this skill in the goal so the workflow stays intact across turns, while keeping source and content details in `book-config.js`. Finish the current turn immediately after creating it; the first automatic continuation starts the first section.
   - **Claude Code:** Its `/goal` command cannot be started by the agent. Use `book-config.js` as the durable section plan and creation context, skip goal-tool discovery, and continue directly into section production in the same task.

5. Produce every section in plan order. In Codex, complete exactly one section in each goal continuation and then finish the current turn. In Claude Code, use the same ordered procedure and continue directly to the next section after the current section is checked:

   1. Read the notebook-level and current section `creationNotes`, then read only that section's source range and the nearby context needed to understand it.
   2. First use eli20 to create its visual HTML explainer as `NN-<section>-visual.html`.
   3. Then read that source range again from the beginning and write `NN-<section>-summary.md`. Use linked or plain `#`–`###` headings and plain paragraphs; heading links may point back to the relevant source location. This Markdown is the only editable summary source.
   4. Generate its display HTML with `node build-summaries.mjs .` and confirm the Visual and Summary files exist and are non-empty. In Codex, end the turn so the next continuation handles the next configured section. In Claude Code, report the completed files and checks, then continue with the next planned section.

6. Create the title page after every section is complete. Use a dedicated next continuation in Codex; continue directly after the final section in Claude Code:

   1. Read every completed Visual and Summary from beginning to end. Identify the one relationship that best explains how the notebook's parts form a useful whole.
   2. Then use eli20 to create `00-title.html`. Replace the bundled placeholder with a visual-first title page that presents the notebook title, one short introductory sentence, and a large illustration or diagram. Place the title and introduction above the illustration so the diagram can use the notebook's full content width. Give the screen one clear idea and one meaningful relationship. Use only the short labels needed to understand the illustration.
   3. Keep document navigation and external resources in the notebook shell. Let the title page serve as a simple visual entrance to the material.
   4. Run `node build-navigation.mjs .`. This adds a one-column contents list to the title page and removes obsolete embedded navigation from Visual files. The notebook shell owns the compact previous/next-section footer, reveals it when the active Visual reaches its own scroll end, and keeps it correctly positioned for short documents. The first Visual links back to Title on the left, the final Visual links forward to Title on the right, and long button labels automatically shrink to fit their available width. Confirm that `book-config.js` points `titlePage.src` to `00-title.html`, the file is non-empty, and opening the notebook without a hash displays it. In Codex, record the title page as complete and end the turn. In Claude Code, report the title file and checks, then continue to final verification.

7. Use a separate final verification continuation in Codex, or continue after the title page in Claude Code. Generate and check every summary, validate the notebook's own scripts, and inspect the complete notebook:

   ```sh
   cd "<output-directory>"
   node build-summaries.mjs .
   node build-navigation.mjs .
   node build-summaries.mjs --check .
   node build-navigation.mjs --check .
   node --check book-config.js
   node --check book-reader.js
   node --check build-navigation.mjs
   node --check notebook-metadata.mjs
   ```

8. Confirm that neither `book-config.js` nor `00-title.html` contains `Untitled notebook`, `book-config.js` no longer contains `Section title`, every configured file exists and is non-empty, all runtime and generated-file references resolve within the notebook directory, and `index.html` opens on the title page with every Visual and Summary selectable. Edit a `*-summary.md` and regenerate when summary content changes; generated `*-summary.html` files and navigation blocks are display artifacts. When all checks pass, report the final commands and results. In Codex, call `update_goal` with `complete`, then call `get_goal` to confirm that no active goal remains. In Claude Code, finish the task without attempting to clear a goal.

Use the source provided in the user's request.
