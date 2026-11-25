---
name: project-markdown
description: >-
  Write or revise a project's Markdown docs (README.md, ARCHITECTURE.md,
  CONTRIBUTING.md, CHANGELOG.md, SECURITY.md, LICENSE). Load whenever the
  task is to create, restructure, or polish repo documentation, or when a
  .md doc file is the input or output. Produces concrete, skimmable,
  slop-free docs that match the codebase as it actually is.
---

## When to use

Reach for this when you're authoring or rewriting any of a repo's standard docs. It covers the six files above and the conventions they share. If you only need prose-level slop removal, pair it with a dedicated editing pass; this skill is about *structure plus voice* for project docs specifically.

## Core principles

These hold across every file.

- **Describe what is, not what should be.** Document the code as it exists. If the project has no bundler, say so plainly — don't paper over reality with conventional advice. Wrong claims in a README are worse than missing ones.
- **Lead with the reader's question.** Each section answers one concrete question: What is this? How do I install it? How does it work? Where does this code live? Order sections by how soon a reader needs them.
- **Concrete over abstract.** Name the actual files, commands, flags, env vars, and defaults. `cargo tauri dev` beats "run the dev server." A defaults table beats "configurable options are available."
- **Skimmable structure.** Short sections, descriptive headings, and tables for anything with repeating shape (downloads, config keys, file responsibilities). A reader should find their answer by scanning headings.
- **No slop.** Cut throat-clearing ("In today's fast-paced world"), empty hype ("powerful, seamless, robust"), and filler transitions. Don't pad with obvious caveats. Every sentence should carry information a maintainer would actually write.
- **Earn every adjective.** "Agent-agnostic" is fine because the next line lists the agents. "Blazingly fast" with no benchmark is noise.
- **Match the repo's voice and stay consistent.** Same tense, same terminology, same code-fence languages throughout. Pick "frontend" or "front-end" and never switch.

## README.md

The front door. Optimize for a stranger who landed from a link and has thirty seconds.

Recommended spine:

1. **Title block + one-line pitch.** Logo (optional, centered), the name, and a single bold sentence stating what it is. Follow with one plain sentence on what problem it solves. Badges (version, license, platform, key runtime) go here if they're accurate and maintained — skip vanity badges.
2. **Hero shot.** A screenshot or GIF right after the pitch, ideally linking to the latest release. Show the thing working.
3. **Two-sentence overview.** What it does and what it's built with. State notable architectural facts up front (e.g. "no bundler, no `package.json`").
4. **Download / Install.** Make the "which file do I grab?" decision for the reader. A per-platform table plus a note on which artifacts to ignore. If there's a toolchain path, separate it from the prebuilt path.
5. **Build & Run.** A copy-pasteable fenced block with comments per step (clone, verify, dev, build). Match the real commands exactly.
6. **Features.** A tight bulleted list, each item bolded label + concrete detail. No more than a line each.
7. **Visual gallery** (optional). A few labeled screenshots for UI projects.
8. **How it works.** A short, honest paragraph or two on the runtime model — enough to orient, with the deep version deferred to `ARCHITECTURE.md`.
9. **Prerequisites.**
10. **Project structure.** A directory tree (wrap it in `<details>` if long) with a one-line comment per important path.
11. **Configuration.** Where settings live (per-platform table) and a defaults table: `Parameter | Default | Description`.
12. **Tech stack.** A single line of the real dependencies.
13. **Contributing / Security / Credits / License.** Short pointers that link out to the dedicated files rather than duplicating them.

Notes: don't repeat the project name as an H1 in the body if a title block already shows it. Link to sibling docs (`CONTRIBUTING.md`, `ARCHITECTURE.md`, `SECURITY.md`) instead of inlining their content.

## ARCHITECTURE.md

Writes for a contributor who needs to find where code lives and why it's shaped that way.

- Open with a one-paragraph **high-level view** and a diagram. A Mermaid `flowchart` showing the major subsystems and the boundaries between them (e.g. frontend ↔ backend over an IPC bridge) pays for itself.
- Walk the codebase **by directory / concern**, one section per subsystem. Use a `File | Owns` table when many files each own one thing.
- Document the **contracts between parts** — the IPC surface, event names, the response-wrapping shape. Call out non-obvious gotchas ("responses are wrapped, so the field isn't the bare return value").
- Explain **lifecycles** for anything stateful (spawn → stream → teardown) as numbered steps.
- End with **key design decisions**: each as a bolded claim plus the tradeoff it accepts ("No bundler — a build step adds more friction than value; the cost is manual DOM work"). This is the highest-value section; it answers "why is it like this?"
- Link back to `CONTRIBUTING.md` for build steps rather than repeating them.

## CONTRIBUTING.md

Gets a new contributor from clone to merged PR.

- **Prerequisites** with linked install pages and exact versions.
- **Build and run** — the exact commands, in a fenced block, including the typecheck/test shortcuts.
- **How to run tests**, separately and explicitly.
- **Project layout** in one paragraph, deferring detail to `ARCHITECTURE.md`.
- **Code style** — the rules that actually matter here ("match surrounding style," "no new build tool or framework"), not a generic style lecture.
- **Reporting bugs / requesting features** — point at the issue templates and say what info to include.
- **Pull requests** — branch naming, which branch to target, scope expectations, what reviewers check. Be specific about the base branch if it isn't `main`.

## CHANGELOG.md

Follow Keep a Changelog and Semantic Versioning. Don't invent a custom format.

- Header note stating both conventions.
- One section per release: `## [x.y.z] - YYYY-MM-DD`, newest first.
- Group entries under **Added / Changed / Fixed / Removed / Deprecated / Security** — only the groups that apply.
- Write entries from the **user's / reader's** perspective and describe the observable change, then the cause if it clarifies. Concrete is good ("Window could not be dragged from the titlebar on macOS") — generic is useless ("bug fixes").
- Keep an `[Unreleased]` section if you stage changes between releases.
- Maintain the **link-reference footer** comparing tags (`[x.y.z]: .../compare/v...`), and add a row each release.
- Bump versions by impact: breaking → major, feature → minor, fix → patch.

## SECURITY.md

State the real security posture; don't copy a boilerplate policy.

- **Supported versions** table.
- **How to report** — a private channel (e.g. GitHub private advisory), what to include, and the expected acknowledgment window. Say "don't open public issues."
- **What the project accesses** — for anything that touches the user's system (spawns processes, reads directories, stores data), spell it out plainly and say what leaves the machine (ideally "nothing").
- **Auto-update / signing** — how updates are verified, and an honest note on anything not yet in place (e.g. "installers aren't OS-code-signed yet, so SmartScreen may warn").

## LICENSE

Use the verbatim text of a recognized license (MIT, Apache-2.0, etc.) with the correct year and copyright holder. Don't paraphrase or hand-edit license bodies — the wording is legally load-bearing. Make sure the README's license line and the actual file agree.

## Shared conventions

- **Relative links** between docs (`ARCHITECTURE.md`), not absolute URLs, so they work on any fork.
- **Tables** for any repeating structure; prose for explanation.
- **Fenced code blocks** always carry a language ( ``bash `,`  `rust` ,  ``yaml `). Use real, runnable commands.
- **`<details>`** to fold long blocks (directory trees, verbose lists) so the page stays scannable.
- **Mermaid** for architecture diagrams when the platform renders it.
- Keep line wrapping and heading levels consistent within a file.
- Cross-check every command, path, version, and default against the actual repo before shipping.

## Pre-ship checklist

- [ ]  Pitch answers "what is this and why" in the first two lines
- [ ]  Every command, path, flag, and default verified against the code
- [ ]  Install/download section makes the artifact choice for the reader
- [ ]  Sibling docs are linked, not duplicated
- [ ]  Tables used for downloads, config, and file responsibilities
- [ ]  Changelog follows Keep a Changelog + SemVer, newest first, with compare links
- [ ]  Security doc states real access scope and a private report channel
- [ ]  License is verbatim with correct year/holder and matches the README
- [ ]  No slop: no empty hype, no filler, no unearned adjectives
- [ ]  Consistent voice, tense, and terminology throughout