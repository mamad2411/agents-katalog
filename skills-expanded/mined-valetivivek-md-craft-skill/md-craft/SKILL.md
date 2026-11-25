---

## name: md-craft
description: Write or improve any project markdown file (README, PR template, CONTRIBUTING, CHANGELOG, docs). Use this skill automatically whenever the user asks to write, draft, generate, create, update, rewrite, polish, fix, clean up, modernize, or improve a .md file in a repo. Triggers include "write a readme", "draft a pr template", "update the changelog", "fix my contributing guide", "my readme sucks", "generate docs", "make a better readme", "make my profile readme", "animated readme", "showcase readme", "make it look cool", and any request whose deliverable is a markdown file describing a project. Also triggers when the user pastes an existing markdown file and asks to improve it. Picks a project-type archetype (library, cli, app, framework, side-project, showcase), matches the repo's existing tone, supports animated and visually-stunning showcase READMEs when the user asks for them, and remembers the choice in `.md-craft.json` so later runs in the same repo skip the style question.

# md-craft

A skill for writing and updating project markdown files (READMEs, PR templates, CONTRIBUTING, CHANGELOG, docs) that actually look like they belong to the project they're in.

## Core philosophy

Most AI-generated markdown reads the same way: a generic badge row, a robotic "Features" bullet list, an "Installation" section written like a textbook, and an "MIT License" footer. It's instantly recognizable and instantly forgettable.

The goal of this skill is the opposite: markdown that reads like the maintainer wrote it on a good day. That means:

1. **The project decides the vibe, not the skill.** A minimal Vercel-style codebase gets a minimal README. A playful side project with a mascot gets personality. A serious enterprise repo gets dense, precise docs. Match the existing tone, don't overwrite it.
2. **Context before keystrokes.** Never write a README without reading what the project actually is. Never update a CHANGELOG without looking at recent commits. Never draft a PR template without understanding what the team actually reviews.
3. **User intent gates everything.** On first run in a repo, ask for archetype/tone before writing; on later runs, the saved choice in `.md-craft.json` answers silently. Always show a plan before writing. Always write after approval, never before.

## README quality bar

A generated README is only done when all three of these are true. Measure against every draft before showing it to the user.

1. **10-second scan.** A reader skimming the top of the file (hero + first section) should understand what the project is, who it's for, and whether it's alive. This means the hero needs a concrete tagline (not "a revolutionary tool for X"), and the first section has to commit to a point. If someone reads the first screenful and still doesn't know what the project does, the draft fails.
2. **2-minute local run.** From landing on the README to a working dev loop: 2 minutes max. This means the install section is minimal prose around real commands, prerequisites are stated plainly (exact versions when they matter), and the quick-start example is the smallest thing that works. No "then configure your environment variables" without saying which ones.
3. **First-paragraph audience filter.** The first paragraph of prose should make it obvious whether this project is for the reader. A library for internal Anthropic tooling says so. A side project says so. A production-grade tool says so. Readers shouldn't have to dig to find out they're in the wrong place.

If a draft fails any of these, fix it before showing the user. Don't ship a README that looks polished but doesn't pass these tests.

## When this skill runs

Any request that ends with a markdown file as the deliverable and isn't purely a conversational question. Examples:

- "Write a README for this project"
- "This README is messy, clean it up"
- "Set up a PR template for the team"
- "Draft a CONTRIBUTING.md"
- "Add a changelog entry for v1.2.0"
- "The docs folder is a mess, help me restructure"
- "Make this readme look like [project X]'s"

If the user just asks a question about markdown syntax or wants to discuss what should go in a README without actually producing one, skip the skill and answer normally.

## The workflow

Follow these five phases in order. Don't skip phases. Each one exists because the phase before it doesn't produce enough signal on its own.

### Phase 1: Gather project context

Before asking the user anything, read what's available. This makes Phase 2 much more productive because you can say "I see this is a Next.js library with a minimal vibe, should I match that?" instead of asking cold.

Read, in order of priority, whichever exist:

1. `**.md-craft.json`** (at repo root): if present, this records the archetype, tone, visual element choices, and notes from past runs in this repo. Read it first; it answers most of Phase 2 silently. See `references/preferences-file.md` for the schema.
2. **CLAUDE.md** (or `.claude/CLAUDE.md`, `AGENTS.md`): the single highest-signal file. Often contains project description, architecture, conventions, and tone hints.
3. **Existing target file**: if updating a README, read the current README. Same for CHANGELOG, CONTRIBUTING, PR templates. The existing voice is the voice to match.
4. **Package manifests**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`. Pull name, description, version, dependencies, scripts.
5. **Docs folder**: skim `docs/`, `ARCHITECTURE.md`, `DESIGN.md` if they exist. Don't read everything; look for structure and tone.
6. **Config files**: `tsconfig.json`, `next.config.js`, `Dockerfile`, CI configs. Tells you the actual stack, not just the claimed stack.
7. **Recent git log**: run `git log --oneline -30` (or `-50` for a CHANGELOG task). Pulls commit message style, recent features, and whether the team uses conventional commits.
8. **Top-level file tree**: `ls` or equivalent. Tells you if it's a monorepo, what the entry points are, whether there's a `public/`, `examples/`, etc.

Keep this phase fast. Don't read every file in `src/`. You're gathering signal, not auditing the codebase.

Produce an internal context summary (don't show it to the user verbatim unless they ask) covering:

- What the project is (one sentence)
- Stack / language / framework
- Apparent tone (minimal / playful / formal / technical-dense / startup-marketing / etc.)
- Existing markdown conventions (emoji usage, heading depth, badge style, example density)
- Anything unusual (monorepo, custom CLI, unusual license, branded naming)

### Phase 2: Pick the archetype and tone (or skip if `.md-craft.json` already answered)

This phase decides two things:

1. **Archetype**: which kind of project this is. Drives section structure and visual elements.
2. **Tone**: how the prose sounds. Drives voice and word choice.

#### If `.md-craft.json` exists

Skip the asking. Use the stored `archetype`, `tone`, `visual` overrides, and `notes` as the answer. Briefly tell the user what you're using so they can object cheaply:

> Using your saved settings: **library** archetype, **modern-clean** tone, no emojis, npm + pnpm install commands. Going to Phase 3 next.

If the project has clearly changed since the file was written (e.g. archetype was `library` but the repo now has a `Dockerfile`, a `Procfile`, and a `web/` UI), surface the mismatch and offer to re-pick:

> Your `.md-craft.json` says this is a **library**, but the repo now has a `web/` Next.js app and a `Dockerfile`. Want to switch to **app**, or keep library?

Don't auto-change. Ask once, then update the file.

#### If `.md-craft.json` does not exist (first run in this repo)

Pick the archetype yourself from Phase 1 signal, then confirm with the user using a short preview.

**Archetype detection (rules of thumb):**


| Signal                                                                                                                                                 | Likely archetype               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| `package.json` with `"main"` / `"exports"` and no UI                                                                                                   | Library                        |
| `bin` field in `package.json`, or a `cmd/` Go folder                                                                                                   | CLI                            |
| `next.config.js` / `vite.config.ts` + `public/` + `Dockerfile`                                                                                         | App / Product                  |
| Many concepts in `docs/`, plus a docs site, plus comparison with alternatives in CLAUDE.md                                                             | Framework / Heavy tool         |
| Single author, no CI, hobby vibe in CLAUDE.md or git log                                                                                               | Side-project                   |
| Inside a monorepo, owned by a team, internal-only                                                                                                      | Side-project (internal flavor) |
| Repo name matches the owner's GitHub username (profile README), or user said "animated" / "showcase" / "make it look cool" / "portfolio" / "hackathon" | Showcase                       |


If two archetypes look plausible, present both. If one is clearly correct, present that one and a fallback.

**Showcase is opt-in only.** Even if a project README would technically render with banners and typing animations, do not propose Showcase for libraries, CLIs, frameworks, apps, or internal repos unless the user explicitly asks for that flavor. Showcase fits profile READMEs, portfolios, hackathon submissions, and side projects whose author has asked for visual flair.

**How to present:**

Show one preview (6 to 10 lines) of the hero + first section in the chosen archetype, written with the project's real details. If you're presenting two options, show both. Follow with a one-line question.

Example, single-archetype confirmation:

> This looks like a **Library** archetype to me (npm package, single import surface, small API).
> Quick preview of how the hero would land:
>
> ```md
> # drift
>
> Typed environment variable loader for Node, zero dependencies.
>
> ```bash
> npm install drift
> ```
>
> ```
>
> Tone: modern-clean. Want me to go with this, or pick something else?
> ```

Example, two-option:

> Could go two ways here. Short previews:
>
> **A. Library archetype, modern-clean tone**
>
> ```md
> # drift
>
> Typed environment variable loader for Node, zero dependencies.
> ```
>
> **B. Side-project archetype, narrative tone**
>
> ```md
> # drift
>
> I got tired of writing `process.env.PORT ? parseInt(...) : 3000` on every project. So I wrote drift.
> ```
>
> Which lands closer?

Wait for the answer. If the user says "just do it, you decide," proceed with the most likely archetype and tone, and say which one you picked and why.

After the choice is confirmed, read the matching file under `references/archetypes/` to get the structure and visual element toolkit before moving to Phase 3.

#### Visual elements

Each archetype's reference file has a "visual elements toolkit" listing what to include. Defaults are good for most projects. Ask the user only if a default is ambiguous for this project, e.g.:

> The App archetype usually has a hero screenshot. Do you have one to include, or should I leave a placeholder?

Don't ask about every possible toggle. Defaults plus one targeted question beats a long checklist.

#### Non-README files

For PR template, CONTRIBUTING, CHANGELOG, and docs, skip archetype selection. Those files don't have the same project-type fork; see their reference files for the patterns that matter.

### Phase 3: Show the plan before writing

Never go from "gathered context" straight to "wrote the file." Show a plan that the user can correct cheaply.

**For new files**, show the section outline plus a one-line note for each section saying what it will contain. Example:

```
Plan for README.md:

1. Hero:         project name, one-line tagline, install command
2. Why:          two short paragraphs on what problem this solves
3. Quick start:  3-step code block (install, configure, run)
4. API:          table of the 4 main exports with link to docs/
5. Examples:     link to examples/ folder, one inline snippet
6. Contributing: link to CONTRIBUTING.md
7. License:      MIT, one line

Roughly matching the current file's structure but adding Quick start and tightening the API section. Sound right?
```

**For updates to existing files**, show a diff-style plan: what you'll keep, what you'll change, what you'll remove. Example:

```
Plan for updating README.md:

KEEP:
  - Hero section (works well)
  - Install instructions
  - License footer

REWRITE:
  - "Features" bullet list → replace with a short paragraph + code example (the bullets are generic)
  - API reference → move to docs/ and link, README is 300 lines today

ADD:
  - Quick start section after Install
  - Badges row (build, npm version, license), you mentioned wanting these

REMOVE:
  - "Motivation" section (redundant with Why)
  - Contributor avatars block (stale, 3 of 5 links are 404)

Want me to proceed, or adjust anything?
```

Wait for confirmation. Accept corrections. Don't skip this step even for small files; small files are where over-eager changes hurt most.

### Phase 4: Write the file

Once the plan is approved, write the file. Follow these principles:

**Structure**

- Use the sections you agreed to. Don't sneak in extras.
- Follow the structure in the chosen archetype's reference file (`references/archetypes/<archetype>.md`).
- Lead with whatever the reader needs most. For a library, that's usually an install command and a 5-line usage example. For a CLI, that's a GIF or a command example. For a CONTRIBUTING guide, that's the dev setup.
- If the project is small, the file should be small. A 200-line README for a 300-line utility is noise.

**Voice**

- Match the tone confirmed in Phase 2 (`modern-clean`, `narrative-personal`, or `dry-operational`).
- If `.md-craft.json` has `notes[]`, treat each note as an additional rule for this write. Notes from past corrections take precedence over generic archetype defaults.
- Don't invent marketing copy. If the project is described as "a small JSON diff tool" in CLAUDE.md, don't call it "the next generation of data transformation infrastructure."
- Don't use em dashes (`—` or `--`) in the markdown files you write for the user. Use commas, periods, colons, or parentheses instead. This is a hard rule for any output file.
- Avoid AI-slop phrasing: "seamlessly", "in the ever-evolving landscape", "revolutionize", "unlock", "leverage", "robust", "comprehensive solution". Write like a tired engineer describing their own project.

**Formatting**

- Use fenced code blocks with language tags (`ts`, `bash`, ````py`).
- Keep headings shallow. `##` for top-level sections, `###` for subsections, avoid `####` unless the section is genuinely deep.
- Tables are good for API references, feature comparisons, and config options. Don't force a table where a bullet list is clearer.
- Badges follow the archetype default unless `.md-craft.json` overrides. If badges are on, use shields.io and keep them to one row.
- Emojis: use what the project already uses, or follow the `.md-craft.json` setting. If the existing file has no emojis and there's no preference saved, don't add them.

**File-type specifics**

See `references/` for per-file guidance:

- `references/readme.md`: shared README guidance (hero, sections, anti-patterns, archetype router).
- `references/archetypes/library.md`: Library archetype (npm/pip/cargo packages, SDKs).
- `references/archetypes/cli.md`: CLI archetype (terminal tools, binaries).
- `references/archetypes/app.md`: App / Product archetype (web apps, desktop, mobile, browser extensions).
- `references/archetypes/framework.md`: Framework / Heavy tool archetype (frameworks, ORMs, design systems).
- `references/archetypes/side-project.md`: Side-project / Internal archetype (hobby projects, internal monorepo packages).
- `references/archetypes/showcase.md`: Showcase archetype (profile READMEs, portfolios, hackathon submissions; animated banners, typing SVGs, stats cards). Opt-in only.
- `references/preferences-file.md`: `.md-craft.json` schema, evolution flow, edge cases.
- `references/pr-template.md`: PR template patterns for different team sizes and workflows.
- `references/contributing.md`: CONTRIBUTING.md patterns.
- `references/changelog.md`: CHANGELOG conventions (Keep a Changelog, conventional commits, release-drift).
- `references/docs.md`: `docs/` folder structure and tone.

Read the relevant reference file before writing. Don't try to remember patterns from memory; the references have concrete examples.

### Phase 5: Show, react, and capture taste

Writing the file is not the last step. Two things still happen:

**Show and iterate.**

- Show the file to the user. Don't write it and disappear.
- If the file is long (over 150 lines), offer to walk through specific sections.
- Ask: "Anything you want to change?" Then iterate. Don't treat the first draft as final.

**Capture taste back into `.md-craft.json`.**

- **First run in a repo**: after the user accepts the file, write `.md-craft.json` with the chosen `archetype`, `tone`, any explicit `visual` choices, the `preferences` you used, and an empty `notes[]`. See `references/preferences-file.md` for the schema.
- **Every run**: listen for two kinds of feedback and distill each into a one-line note appended to `notes[]`:
  1. **In-chat corrections** ("drop the emojis," "make the install section shorter," "always include a pnpm command too").
  2. **Post-write edits**: if the user edits the file before the next message, diff it against what you wrote. Material removals or rewrites are signal worth capturing.
- Only capture things the user actually said or visibly changed. Don't invent notes.
- Update `lastUpdated` on every write.
- If `notes[]` exceeds 12 entries or contains contradictions, propose a consolidation in the next session. Don't consolidate silently.

## What this skill does not do

- Generate fake content. If you don't know the install command, ask; don't make one up.
- Add sections the user didn't approve. No sneaking in a "Star History" badge because it "looks good."
- Restructure docs/ without explicit permission. You can suggest it; don't do it.
- Write the full CHANGELOG from scratch by reading every commit in history. For CHANGELOG work, scope to a version range and ask.

## Quick escape hatches

- `**.md-craft.json` already exists**: skip the Phase 2 question. Announce the saved settings in one line, then go to Phase 3.
- **User says "just write it, don't ask me"**: skip Phase 2 and Phase 3, but still do Phase 1. Tell them which direction you picked. Still write `.md-craft.json` so the next run is consistent.
- **User pastes an existing file with "improve this"**: Phase 1 is just reading the file and its context. Phase 2 becomes "what specifically bothers you about it?" Phase 3 is a diff plan.
- **User asks for something tiny ("add a license section")**: compress all phases into one message. Still ask once before writing if there's any ambiguity.
- **Running in CI or any non-interactive context**: read `.md-craft.json` if it exists, but never write to it. Writing requires user confirmation; CI has no user.

