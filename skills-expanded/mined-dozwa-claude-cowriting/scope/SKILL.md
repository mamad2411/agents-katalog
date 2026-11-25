---
name: scope
description: The paper's scope and progress against it: goal, points to make, words or pages, figures, tables, references, sections, deadline. Alone it shows the progress; check asks a small model which points the text already makes; edit sets the scope with you.
argument-hint: "[check|edit]"
disable-model-invocation: true
---

The plugin answers `/cowrite:scope` and `/cowrite:scope check` itself. What reaches you is `edit` or `setup`, in any capitalisation: setting the scope with the author.

Help the author set the scope of this paper in `scope.md`. Interview them, one question at a time: the goal (what should a reader know or believe afterwards), the points they want to make, the length in words or pages, figures, tables and references, the sections with word targets and how far each one is (outline, draft, revised, final), and the deadline. Then write their answers into `scope.md` in their words, following its structure (`## Goal`, `## Targets`, `## Sections`, `## Points` as `- [ ] …` lines) and keeping its comment lines. Add no points of your own; you may ask whether something is missing. Show them the result.

If `$ARGUMENTS` is anything but `edit` or `setup`, the plugin's module did not answer: tell the author in one line that the CoWriting plugin needs a restart of Claude Code (or an update), and do nothing else.
