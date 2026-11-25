---
name: docs-vault
description: Build an Obsidian vault of project docs that humans and LLMs read the same way, eight flat top-level domain docs (PRODUCT/RUNTIME/ARCHITECTURE/DATA/AUTH/ENGINEERING/TESTING/DESIGN) over folder-level deep specs, a single entry point, bidirectional wikilinks that form a real dependency graph, and a `DESIGN.md` that conforms to the google-labs-code/design.md spec with tokens derived from the project's existing design sources. Progressive disclosure governs the vault (each layer carries a summary and links one level deeper, so an agent loads only the context its task needs), the structure is outlined before any prose is written, links may only point at files that exist, and a second pass verifies budgets and links. Use when asked to "set up project docs", "write project documentation", "create an Obsidian vault from this repo", "document this codebase for agents", "add a DESIGN.md", or "make the design system machine-readable".
---

# docs-vault

Build a `docs/` folder that works both as an Obsidian vault (a folder of markdown notes that the Obsidian app opens with graph view, backlinks, and color-coded tags) and as a flat GitHub-readable index. Pair it with a `DESIGN.md` that follows the [google-labs-code/design.md](https://github.com/google-labs-code/design.md) spec so the design system becomes machine-readable. The vault serves two readers at once: a human who opens it in Obsidian or on GitHub, and an LLM (large language model) that should load only the context its task needs.

TRIGGER when: bootstrapping documentation for an application, service, library, platform, or multi-package repository; introducing a flat top-level domain-doc pattern over an existing tangle of docs; or making the design system machine-readable for agents.

> **Stack assumed.** None. Inspect the repository first and adapt the docs to the language, framework, package manager, runtime, UI layer, infrastructure, and test stack actually present.

> **Notation.** `<project>`, `docs/`, `<design-source>`, `<NNNN>` are placeholders. Resolve to the project's actual project name, root, design token/theme source, and ADR numbering scheme. Frontmatter examples (`aliases`, `tags`) follow Obsidian conventions; adjust to whatever tag taxonomy your team prefers.

> **Precedence.** Project rules (CLAUDE.md / AGENTS.md / contributing guide) win. This skill produces those files for projects that don't have them; if they already exist, extend rather than replace.

> **Scope.** Skill is about *how* to write the docs and *which* docs. The content of any given doc is the project's own; this skill provides the structure, the read order, the link conventions, and the DESIGN.md template.

---

## Governing principles

Five principles govern every artifact this skill produces. The workflow refers to them by number.

**1. Progressive disclosure.** Each layer carries only what a reader needs at that depth, plus links one level deeper. The point is context economy: an agent loads the pointer, follows links only while its question is open, and never pays for layers it did not need. Humans get the same benefit as files short enough to hold in your head. Detail lives at the deepest layer that needs it, stated once.

| Layer | Artifact | Carries |
|-------|----------|---------|
| 1 | `CLAUDE.md` | 3-line pointer to layer 2 |
| 2 | `AGENTS.md` | Read order, stack summary, non-negotiables |
| 3 | Top-level domain docs | 50-150 line summaries that link into layer 4 |
| 4 | Folder deep docs | Full specs (`architecture/*`, `conventions/*`, ...) |
| 5 | Source code | Ground truth |

`DESIGN.md` is the one exception: the design.md spec requires a complete single file, so it holds full token data at layer 3. When a structure question is not covered here, put the detail one layer down and leave a link behind.

**2. One entry point.** `docs/Home.md` is the vault's only hub, and the way in is always the same chain: `CLAUDE.md` → `AGENTS.md` → `Home.md` → domain docs. `docs/README.md` exists only because GitHub renders it in folder view; it points at Home and stops. No file duplicates Home's link list.

**3. Links form a dependency graph.** A wikilink states a real relation: a down-link says "this doc elaborates me", the `↑` up-link says "I summarize that doc". Never add a link for decoration or to make the graph look connected. Done right, the Obsidian graph shows the layers radiating from Home, and the backlinks panel reads as a reverse dependency list.

**4. Two audiences, one voice.** Humans and LLMs read the same files, so write prose that reads naturally when spoken: short sentences, simple words, technical terms explained at first use, no filler. If the `deslop` skill is installed (in `.agents/skills/` or the session skill list), apply it to every doc you write.

**5. No invented references.** Every wikilink, file path, and code reference points at something you opened during this run, in the repo or in a file the run creates. Never cite a file, function, or decision from memory of similar projects. When a fact cannot be verified in the repo, ask the user or label it [Unverified].

## Outputs

When this skill finishes, the repo has:

```
CLAUDE.md                       single pointer (3 lines, points at AGENTS.md)
AGENTS.md                       primary entry for any AI agent
docs/
├── .obsidian/                  vault config (committed)
│   ├── app.json
│   ├── core-plugins.json
│   ├── community-plugins.json
│   ├── graph.json              color groups by tag
│   ├── appearance.json
│   └── bookmarks.json
├── Home.md                     the vault's single hub (map of content, alias: Vault Home)
├── README.md                   short GitHub pointer to Home
│
├── PRODUCT.md                  ┐
├── RUNTIME.md                  │
├── ARCHITECTURE.md             │  Flat top-level domain docs.
├── DATA.md                     │  Each is a short summary (~50-150 lines)
├── AUTH.md                     │  that links into the deeper folder content.
├── ENGINEERING.md              │
├── TESTING.md                  │
├── DESIGN.md                   ┘  ← spec-compliant (google-labs-code/design.md)
│
├── architecture/               deeper specs per domain
├── conventions/                rules per layer (language, styling, data access, ...)
├── workflows/                  step recipes (new-domain, diagnose-bug, ...)
├── quality/                    perf, accessibility, reliability, security, design polish
├── decisions/                  architecture decision records (ADRs), lazy
└── upgrades/                   what the repo lacks vs skill defaults
```

## Workflow

The build takes an outline plus two passes. The outline (step 2) fixes the structure before any prose exists. Pass 1 (steps 3-8) writes the files. Pass 2 (step 9) rereads everything and verifies the principles held. Do not skip pass 2.

### 1. Sweep the codebase (read, don't write yet)

Before writing a single doc, read enough to map the project:

- **Surfaces:** list screens, routes, CLIs, APIs, jobs, packages, or user-facing entry points; identify public vs restricted surfaces.
- **Stack:** manifest files, language/runtime config, dependency manager files, workspace config, database schemas, infrastructure manifests, and design token/theme sources if present.
- **Entry points:** app/server/CLI/library entry files, provider/bootstrap files, global styles, config loaders, and deployment adapters.
- **Interface primitives:** components, views, screens, templates, API resources, command handlers, or other primary user/developer-facing building blocks.
- **Data layer:** persistence, validation, caching, service clients, query modules, schema files, and equivalent abstractions.
- **Continuous integration (CI) / tooling:** workflow files, hooks, lint/format/test/build configs, release automation.
- **Existing docs:** `README.md`, anything in `docs/`. **Don't overwrite.** If they exist, extend.

Use Glob + Grep + Read in parallel. Don't open every file; open enough to fill out PRODUCT/RUNTIME/ARCHITECTURE.

### 2. Outline the vault (structure before prose)

Before writing a single sentence of documentation, write the outline: one line per planned file with its path, layer, one-sentence purpose, planned up- and down-links, and line budget. Then check it:

- Every planned link targets a file that exists or is itself in the outline (principle 5).
- Every folder doc has exactly one `↑` parent, and `Home.md` is the only hub (principle 2).
- Any top-level doc whose outline already wants more than its lines target loses content one layer down (principle 1).

Start writing only when the outline passes all three checks. A structure mistake costs one outline line now and a rewrite later.

### 3. Create vault config

Drop `.obsidian/` into `docs/` so opening the folder in Obsidian works immediately. Templates: see [VAULT-STRUCTURE.md](VAULT-STRUCTURE.md) §Vault config.

Required: `app.json` (sets `useMarkdownLinks: false` so wikilinks are the default), `core-plugins.json` (graph/backlinks/tag-pane on), `graph.json` (color groups by tag).

### 4. Write the eight top-level domain docs (flat)

Order, and what each must cover:

| File | Covers | Lines target |
|------|--------|--------------|
| `PRODUCT.md` | Audiences (roles), surfaces (screens/routes/APIs/commands), domain glossary, revenue model, open questions | 60-120 |
| `RUNTIME.md` | Stack, services, env vars, local setup, available commands, deploy target | 80-150 |
| `ARCHITECTURE.md` | Code layout tree, canonical data flow, state boundaries, ownership boundaries | 50-100 |
| `DATA.md` | DB choice, ORM, validation lib, query cache, layers, naming conventions | 70-150 |
| `AUTH.md` | Auth/session system, credential shape, role gating, access patterns | 40-80 |
| `ENGINEERING.md` | Daily commands, lint/format rules, language config, hooks, Git/PR style, CI | 60-110 |
| `TESTING.md` | Test runner, co-location, behavior-over-impl, mocking guidance, coverage | 50-90 |
| `DESIGN.md` | Spec-compliant. See [DESIGN-MD-TEMPLATE.md](DESIGN-MD-TEMPLATE.md). | 200-400 |

**Frontmatter on every file:**

```yaml
---
aliases: [Display Name, Alternative Name]
tags: [moc, architecture]   # see tag list below
---
```

Each top-level file is a **summary that links into deeper folder content**. Don't duplicate; link down (principle 1). The `architecture/data-layer.md` deep doc may be 200 lines; `DATA.md` is 100 lines and points at it.

**Read order goes in `Home.md` and `AGENTS.md`:** PRODUCT → RUNTIME → ARCHITECTURE → DATA → AUTH → ENGINEERING → TESTING → DESIGN.

### 5. Write folder docs (deeper specs)

Folders + tag mapping:

| Folder | Tag | Up-link target(s) |
|--------|-----|-------------------|
| `architecture/` | `#architecture` | `[[ARCHITECTURE]]` (+ `[[DATA]]`, `[[AUTH]]`, `[[RUNTIME]]` per topic) |
| `conventions/` | `#convention` | `[[ENGINEERING]]`, `[[DESIGN]]`, `[[DATA]]`, `[[TESTING]]` per topic |
| `workflows/` | `#workflow` | `[[ENGINEERING]]` + the topic top-level (`[[DATA]]`, `[[DESIGN]]`, `[[TESTING]]`) |
| `quality/` | `#quality` | `[[DESIGN]]`, `[[RUNTIME]]`, `[[ENGINEERING]]` per topic |
| `decisions/` | `#adr` | `[[ENGINEERING]]` · `[[ARCHITECTURE]]` |
| `upgrades/` | `#upgrade` | Multi (the doc lists the relevant tiers) |

Per-file scaffolds (overview, conventions, workflows, quality, decisions, upgrades): see [VAULT-STRUCTURE.md](VAULT-STRUCTURE.md).

### 6. Wire bidirectional links

Link only where a real dependency exists (principle 3). For Obsidian's graph + backlinks panel to work well:

- **Use wikilinks `[[file]]`** for in-vault navigation. Obsidian resolves by basename; aliases let you target by display name.
- **Use external markdown links** for files outside the vault (`../AGENTS.md`, `../package.json`).
- **Give every folder doc a `↑` up-link** in its **See also** section pointing to its parent top-level file:

```markdown
## See also

- ↑ [[DATA]] · [[ENGINEERING]]
- (peer wikilinks)
- ↩ [[overview]]   (or [[Home]])
```

- **Give every top-level domain doc a See also** linking to its deep docs and to peer top-levels.

### 7. Write the spec-compliant `DESIGN.md`

Follow [DESIGN-MD-TEMPLATE.md](DESIGN-MD-TEMPLATE.md). Hard requirements:

1. **YAML frontmatter** with the canonical token schema (`colors`, `typography`, `rounded`, `spacing`, `components`).
2. **Token values derived from existing project sources** (design token files, theme configs, CSS variables, component styles, native/mobile style definitions, Figma exports, brand docs), not invented. The template explains the derivation step-by-step.
3. **Sections in canonical order:** Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts.
4. **`primary` must pass Web Content Accessibility Guidelines (WCAG) AA contrast against `on-primary`** (4.5:1). If the brand color is too light/dark, introduce a `primary` / `primary-container` split (Material-style).
5. **Component definitions reference tokens** via `{colors.primary}`, `{rounded.lg}`, `{typography.label-md}`. No hex values inside the `components:` block except for `transparent` and `rgba(...)`.
6. **Lint clean:** `npx @google/design.md lint docs/DESIGN.md` reports `0 errors, 0 warnings`.
7. **Obsidian frontmatter (`aliases`, `tags`)** lives alongside spec keys; the YAML parser accepts unknown keys.

### 8. Write the entry chain

One chain leads into the vault: `CLAUDE.md` → `AGENTS.md` → `docs/Home.md` (principle 2). Update or create:

- **`CLAUDE.md`** at repo root: a 3-line pointer to `AGENTS.md`, the vault entry, and the one hard don't.
- **`AGENTS.md`** at repo root: the entry for any agent. It carries the read-order table, the non-negotiables, and skill discipline (point at `skills-lock.json` if applicable; do not maintain a separate skills index in the vault, because it creates SKILL graph noise). Its vault entry link is `docs/Home.md`.
- **`docs/Home.md`**: the vault's single hub (alias `Vault Home`). The top section lists all 8 top-level docs with a one-line description each.
- **`docs/README.md`**: a short pointer for GitHub browsing. It names the vault, links to `Home.md`, repeats the read order (GitHub does not render wikilinks), and shows the folder tree. Nothing else.
- **`docs/.obsidian/bookmarks.json`**: pin Home + 3-4 most-touched files (PRODUCT, ARCHITECTURE, DESIGN, "Immediate upgrades" if you wrote one).

### 9. Second pass: verify the vault (mandatory)

Progressive disclosure fails silently: bloat and broken links appear while writing, and only a reread finds them. Reread every file in read order and fix:

- **Budgets:** each doc is within its lines target; move anything over one layer down (principle 1).
- **Duplication:** no fact lives at two depths; the shallower copy becomes a link.
- **References:** open every wikilink and path target. Fix or delete any that does not resolve (principle 5).
- **Entry:** the only way in is `CLAUDE.md` → `AGENTS.md` → `Home.md`; no other file duplicates Home's link list (principle 2).
- **Prose:** if the `deslop` skill is installed, run it over every doc; otherwise reread one paragraph per file aloud-style and cut filler (principle 4).

If this pass moved content between layers, reread the affected files once more before declaring done.

## Tag set (source of Obsidian graph color groups)

```
#moc          , index / map-of-content files (Home, README, top-level domain docs)
#architecture , architecture/* + ARCHITECTURE.md
#convention   , conventions/* + ENGINEERING.md
#workflow     , workflows/*
#quality      , quality/* + DESIGN.md (also #moc)
#adr          , decisions/*
#upgrade      , upgrades/*
```

`graph.json` (provided in [VAULT-STRUCTURE.md](VAULT-STRUCTURE.md)) maps each tag to a color group.

## Hard rules

- **Never** move deep-spec content up a layer. Upper layers summarize and link down; the folder doc holds the detail (principle 1).
- **Never** write a wikilink or path you have not resolved. If the target is planned but not yet written, create it in the same run or drop the link (principle 5).
- **Never** grow `docs/README.md` into a second index. It points at `Home.md` and stops (principle 2).
- **Never** put SKILL.md backlinks (`🌐 Live skill: [name](.../SKILL.md)`) in vault docs: every link to a `SKILL.md` becomes a "SKILL" node in the graph view and clusters visual noise. Reference skills as plain code-fenced text (`` `zod-prisma-tanstack` ``) and point readers at `skills-lock.json` once at the top level.
- **Never** maintain a parallel skills index inside the vault. `skills-lock.json` is the inventory. The relevant skill name is mentioned inline in the doc that distills it.
- **Never** invent token values for `DESIGN.md`, derive from the project's existing design sources and call out drift in prose.
- **Never** skip the `↑` up-link in folder docs; without it the graph becomes one-directional and the backlinks panel becomes the only path back up.
- **Never** use broad transitions (such as CSS `transition: all`), ad-hoc type sizes, or hardcoded brand values outside the project's token/theme source; flag those in the DESIGN.md "Do's and Don'ts" so agents reading the file produce code that matches.
- **Never** read `.env` / `.env.local` while writing docs. Read `.env.example` and ask the user for live values.

## Anti-patterns

- ❌ Writing docs before the outline exists. A structure mistake costs one line in the outline and a rewrite after pass 1.
- ❌ Wikilinks to docs "to be written later". They render as broken graph nodes and teach readers to distrust every link.
- ❌ `README.md` and `Home.md` competing as indexes. README points; Home indexes.
- ❌ A single 1000-line `docs/INDEX.md` with everything inline. Split into the 8 top-level domain files; each links into its folder.
- ❌ Top-level docs that duplicate folder content. Top-level summarizes; folder doc is the deep spec.
- ❌ Folder docs that don't link up to their top-level parent (graph becomes one-directional).
- ❌ DESIGN.md that defines tokens but no components: every color token should be referenced by at least one component (the linter flags orphans).
- ❌ DESIGN.md `primary` with white text but contrast < 4.5:1. Split into `primary` (action) and `primary-container` (soft surface) so the brand color survives both contexts.
- ❌ Wikilinks pointing to ambiguous basenames (e.g. multiple `README.md` files). Use frontmatter aliases (`Vault Home`, `Skills Index`) and reference by alias.
- ❌ Markdown links to `.agents/skills/<name>/SKILL.md` from inside the vault. Use a plain code-fenced reference instead.
- ❌ Inventing typography levels not present in the project. If the project hasn't codified a typography scale, define one in DESIGN.md from the sizes the interface repeats most and call it out as "newly codified" in prose.

## Checklist (before declaring done)

- [ ] `docs/.obsidian/` committed with at least `app.json`, `core-plugins.json`, `graph.json`, `bookmarks.json`
- [ ] `docs/Home.md` exists with `aliases: [Vault Home]` and lists all 8 top-level docs
- [ ] `docs/README.md` is a short pointer to `Home.md` (read order + folder tree, nothing else)
- [ ] All 8 top-level docs exist with frontmatter (`aliases`, `tags`)
- [ ] Every folder doc has a `↑ up-link` in its **See also** section
- [ ] No `🌐 Live skill: [...](.../SKILL.md)` links anywhere in the vault
- [ ] `npx @google/design.md lint docs/DESIGN.md` → `0 errors, 0 warnings`
- [ ] `CLAUDE.md` and `AGENTS.md` exist at repo root and point at the vault
- [ ] Read order is documented in **both** `Home.md` and `AGENTS.md`
- [ ] Tags applied consistently per the tag set table
- [ ] Progressive disclosure holds: `CLAUDE.md` is a 3-line pointer, each top-level doc stays within its lines target, and no top-level doc repeats folder-doc content
- [ ] The outline existed before any doc was written, and pass 2 ran over every file
- [ ] Every wikilink and path resolves to a file that exists
- [ ] Prose is plain and reads naturally (run the `deslop` skill on every doc if it is installed)

## Reference files

- [VAULT-STRUCTURE.md](VAULT-STRUCTURE.md), full file inventory + per-file scaffolds (`.obsidian/*.json`, top-level templates, folder doc templates)
- [DESIGN-MD-TEMPLATE.md](DESIGN-MD-TEMPLATE.md), general-purpose DESIGN.md template + step-by-step token derivation from the project's existing design sources
