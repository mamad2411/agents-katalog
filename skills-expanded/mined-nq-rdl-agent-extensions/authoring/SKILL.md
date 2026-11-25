---
license: CC-BY-4.0
description: >-
  Use when the user asks about Writerside topics, markup tags, documentation
  templates, or building/deploying Writerside projects. Covers semantic XML
  markup, topic structure, procedures, code blocks, diagrams, navigation,
  templates, Docker-based builds, documentation quality inspections, and prose
  style guides for JetBrains Writerside.
compatibility: >-
  Requires the Writerside plugin for a JetBrains IDE, or Docker for builds
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Writerside Skill

Navigate JetBrains Writerside's semantic markup, project structure, and quality tooling to produce well-structured technical documentation.

---

## Scope

This skill covers **Writerside tool mechanics** — how to use the markup, structure topics, build with Docker, configure style guides, manage navigation, and run quality checks.

It does **not** cover:
- General technical writing craft (use a copywriting or editing skill)
- Documentation strategy or information architecture (separate concern)

---

## Key Concepts

**Topics** — The fundamental unit of Writerside content. Topics can be authored as `.md` (Markdown) or `.topic` (semantic XML) files. Both formats can be mixed within a single project, and Markdown files can embed semantic XML tags.

**Instances** — A build target that produces one documentation website. A Writerside project can contain multiple instances (e.g., user guide, API reference), each defined in a module configuration. Docker builds target a specific instance via `MODULE_INSTANCE`.

**Semantic markup** — Writerside's XML tag system that adds meaning beyond formatting. Tags like `<procedure>`, `<step>`, `<chapter>`, `<deflist>`, and `<tldr>` encode document structure so the builder can generate navigation, search, and cross-references automatically.

**Chapters** — Hierarchical sections within a topic, created with `<chapter>` tags (XML) or `##` headings (Markdown). Chapters support nesting, collapsibility, and per-instance filtering.

**Procedures** — Step-by-step instruction blocks using `<procedure>` and `<step>` tags. These render as numbered sequences with clear visual separation — the primary pattern for how-to content.

**Inspections** — Built-in quality checks that run in the IDE editor and during Docker builds. They catch invalid markup, broken references, duplicate IDs, and structural issues.

Writerside is a plugin for JetBrains IDEs (the standalone IDE was sunset in March 2025). Builder version and Docker/CI builds: [references/docker-deployment.rst](references/docker-deployment.rst).

---

## Diagrams

Writerside renders diagrams directly from fenced code blocks. Two options are supported:

**Mermaid (default)** — use `lang="mermaid"` in a `<code-block>`. No server setup required. Supported types: flowcharts, sequence diagrams, state diagrams, git graphs, Gantt charts, pie charts. Install the Mermaid IDE plugin for editor support.

**PlantUML (acceptable alternative)** — use `lang="plantuml"`. Requires Graphviz on the build system. Use when Mermaid lacks the required diagram type (use case diagrams, mind maps, JSON visualisation, detailed UML class diagrams).

See [references/diagrams.rst](references/diagrams.rst) for syntax, examples, and a decision guide.

---

## Spell Checker

Writerside uses the JetBrains IDE spell checker. Configure the language for your project (e.g., `English (Australian)` for en-AU):

1. Settings → Editor → Natural Languages → set Project language to your preferred locale
2. Commit `.idea/dictionaries/` to share the project dictionary with the team
3. Add custom terms (product names, acronyms, domain vocabulary) via right-click → **Save to project-level dictionary**

Prose style enforcement (banned words, substitutions) is separate — use `.wrs-style-guide.yaml`. See [references/style-guide.rst](references/style-guide.rst).

---

## Navigation

The sidebar TOC is defined in a `.tree` file using nested `<toc-element>` tags. Key patterns:

- **Ordering** — topics appear in tree-file order; drag-and-drop in the tool window or edit the file directly
- **Wrappers** — empty `<toc-element toc-title="Section">` groups topics without needing an intro page
- **Hidden topics** — `hidden="true"` excludes from sidebar but keeps accessible via direct link
- **Short sidebar labels** — `toc-title` attribute overrides the full topic title in the sidebar
- **Home page** — `start-page="topic.topic"` on `<instance-profile>`

See [references/navigation.rst](references/navigation.rst) for full tree file examples.

---

## Authoring Mode Decision

| Factor | Markdown (`.md`) | Semantic XML (`.topic`) |
|--------|------------------|------------------------|
| Learning curve | Familiar CommonMark syntax | Requires learning Writerside XML tags |
| Best for | Small docs, quick content, developer-facing | Large projects, multi-contributor, formal docs |
| Semantic features | Embed XML tags inline as needed | Full access to all semantic elements |
| Recommended when | Speed matters, contributors know Markdown | Structure matters, content is reused across instances |

Writerside does not require choosing one mode — Markdown files can contain semantic XML tags directly.

---

## Reference Files

| File | Contents |
|------|----------|
| [references/markup-reference.rst](references/markup-reference.rst) | Complete semantic XML tag reference — block elements, inline elements, metadata, conditional content, with examples |
| [references/docker-deployment.rst](references/docker-deployment.rst) | Docker build process — commands, environment variables, CI/CD integration, multi-instance builds |
| [references/documentation-quality.rst](references/documentation-quality.rst) | Built-in inspections, quality workflow, suppressing warnings, CI integration |
| [references/templates.rst](references/templates.rst) | How-to guide template and Standard Operating Procedure template with Writerside XML examples |
| [references/linting.rst](references/linting.rst) | Linting strategy — Writerside inspections as primary, optional external tools, recommended workflow |
| [references/topics.rst](references/topics.rst) | Topic file formats (.md vs .topic), topic IDs, metadata attributes, when to use each format |
| [references/diagrams.rst](references/diagrams.rst) | Mermaid (default) and PlantUML (acceptable) — syntax, supported types, embedding, decision guide |
| [references/style-guide.rst](references/style-guide.rst) | Style guide configuration (.wrs-style-guide.yaml), rule types, spell checker setup for Australian English (en-AU) |
| [references/navigation.rst](references/navigation.rst) | TOC tree structure, section wrappers, navigation ordering, hidden topics, toc-title overrides |
| [references/lists.rst](references/lists.rst) | Definition lists, ordered/unordered lists, multi-column lists, nested lists — Markdown and XML |
