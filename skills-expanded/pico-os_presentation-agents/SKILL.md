# Instructions

- `/home/areo/Documents/Studium/Pico-OS/README.md` is authoritative; keep slide order aligned with its chapters. Consult PicoC-Compiler and RETI-Emulator READMEs only for contracts/details it newly references.
- Keep slides sparse and visual (diagrams, maps, flows, progressive reveals, focused code) in the existing dark/cyan/amber style. Preserve unrelated manual edits.
- Every slide needs an invisible `SOURCE ` comment with a stable PicoOS README anchor. Insert new slides beside their matching section.
- Do not update `speaker-notes.md` as part of `UPDATE_PRESENTATION`.
- Do not regenerate or export the PDF; the user always handles PDF generation.
- Preserve `<!-- SHORT_VERSION_DISABLED -->` markers with their slides during
  README-driven updates. Before an update, apply any pending numbered selection
  with `make apply-short-version-selection`; after a successful update, run
  `make sync-short-version-selection` so `short-version-disabled-slides.txt`
  reflects the slides' new full-deck numbers. See `docs/short-version.md`.
- Keep a short, summarized outline only on the title page, with seven topics: toolchain extensions; boot and kernel startup; interrupts, system calls and exceptions; processes, memory and I/O; shell and user applications; test system; OS and RTOS lectures. Place topics 01–06 on the left and topic 07 below the decorative artwork on the right, aligned with the bottom row (topics 05 and 06). Preserve the original title-page composition and decorative artwork. Do not add a separate Contents slide or expand the cover into a full README chapter list.

- Use the shared terminal styling for all shell transcripts and command examples, even when the README omits prompts: match regular code blocks with a light background, subtle border, and restrained syntax colors; no decorative window-control dots; retain a concise caption in the header’s right corner describing the session.
- Prefix each host command with `$ ` and each PicoOS command with `PicoOS> `. This includes compiler/build commands and commands supplied as test input. Do not prefix output, explanatory comments, blank lines, continued lines of a command, or commands after a pipe with another prompt. Preserve command text, quoting, and line continuations.

# README headings and slide titles

Use the actual heading hierarchy of `/home/areo/Documents/Studium/Pico-OS/README.md`, rather than invented topic names or descriptive taglines, for the slide title area. Follow README section order; insert a new slide beside the section it belongs to. The summarized cover outline is the explicit exception described above.

- For a nested section, use its exact README heading as the subtitle (the second line of the title area).
- Combine **all preceding heading levels** into the main title, in order, separated by middle dots: `<heading> · <subheading> · <subsubheading>`. Do not add an ancestor that is not part of the README hierarchy. Preserve the README's section numbers and code names.
- For example, the README's `PicoOS` → `Intended physical hardware` becomes main title `PicoOS` and subtitle `Intended physical hardware`. Do not use `Intended physical hardware` as the main title with an invented subtitle such as `Physical setup and verified SRAM capacity`.
- For a deeper section, `PicoOS` → `Intended physical hardware` → `RETI execution model` becomes main title `PicoOS · Intended physical hardware` and subtitle `RETI execution model`.
- If one subsection needs several slides, repeat its main title and number **every** subtitle as `<Exact README heading> (1)`, `(2)`, … through the last slide for that section. Restart numbering for the next section; do not number a section that fits on one slide.
- For a top-level section with no ancestor, use the exact heading as its main title; do not invent a subtitle. Section introductions without separate content may be represented by the main titles of their subsection slides.
- Give each slide exactly one invisible source marker in the form `<!-- SOURCE Pico-OS/README.md#stable-readme-anchor -->`. Multiple slides for the same section share its anchor. Omitted function catalogs do not need placeholder slides.

# Content selection and visual design

- Largely reuse the README's diagrams, tables, code boxes, memory maps, and other visuals. Adapt their layout and scale for slides while preserving their meaning. **Do not include tables cataloging all kernel functions.**
- Reduce prose to essential points. Use short bullets where useful; omit text that merely repeats a diagram or an explanation the presenter can give while showing it. Select only the table columns that help the audience understand the topic.
- Choose each slide's layout individually. Use two or three columns, full-width sections beneath columns, nested boxes, timelines, flows, or grids when they make the content easier to grasp. Show application and shell-built-in inventories as compact labeled tiles when a large table would be cumbersome.
- Use font sizes, colors, spacing, and alignment deliberately to establish emphasis and make the content readable quickly from a distance. Compactness must not come at the expense of clarity. Preserve useful existing visual ideas such as the cover artwork, hardware layout, focused compiler example, memory map, initialization timeline, and application/test grids.

# Enlarging visuals

Keep click-to-enlarge available for diagrams, code blocks, tables, and other potentially small visuals. Clicking or activating such a visual must open the enlarged view **without also advancing the slide**. Keep the full content readable in the viewer, with zoom/fit controls, scrolling, text selection, and a way to close it and return to the same slide. Verify both normal and selectable-text presentation behavior when changing this functionality.

# Exact README source record

[`source-state.json`](source-state.json) is the version record for the README used to create the current slides. [`.source/Pico-OS-README.md`](.source/Pico-OS-README.md) stores the exact source bytes, including any uncommitted README edits used at generation time.

Record the repository commit, SHA-256 of those exact bytes, whether the README differs from that commit, the generation/update date, and the slide count. `primarySource.dirtyAtGeneration` describes the README, not unrelated dirty files in the repository. A commit alone is insufficient if the README has uncommitted changes; the snapshot and hash identify the actual source used. Preserve this baseline until an update succeeds, then refresh it using `UPDATE_PRESENTATION`. Do not record a newer README as the source until its changes have been incorporated into the slides.

# UPDATE_PRESENTATION

1. Read `source-state.json` and `.source/Pico-OS-README.md`.
2. In `/home/areo/Documents/Studium/Pico-OS`, inspect `git status`, commits after the stored primary commit, `git diff <stored-commit>..HEAD -- README.md`, and `git diff HEAD -- README.md`.
3. Treat `git diff --no-index -- .source/Pico-OS-README.md /home/areo/Documents/Studium/Pico-OS/README.md` as the exact authoritative delta.
4. Map changed README headings to `SOURCE ` comments in `slides.md`; update slides in place or insert at the matching chapter. Apply the heading, content, and visual rules above; give every new slide the exact source-marker format documented above.
5. Build only this presentation; do not run the PicoOS test suite.
6. On success, replace `.source/Pico-OS-README.md` with the exact README used and refresh commits, SHA-256 hashes, dirty state, date, and slide count in `source-state.json`.

# COMMIT_SUMMARY and PUSH

Please read: /home/areo/.config_stow/codex/Documents/Studium/PicoC-Compiler/AGENTS.md
