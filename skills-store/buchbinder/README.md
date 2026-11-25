# Buchbinder — Professional Book Writing Workflow for OpenCode

**Buchbinder** is a professional-grade book writing workflow for OpenCode that guides authors from initial concept to completed, publishable manuscript. It supports fiction, non-fiction, mixed, and series projects through a structured phase system with fine-grained outlining, XML-structured drafting, 25 hard-block quality gates, 8 critique modes, three-pass editing, multi-pass revision, and pandoc-based publishing.

Named after the German *Buchbinder* — the bookbinder, the craftsperson who folds, sews, and binds printed sheets into a finished, durable book — Buchbinder is a tool for the writer's craft in the age of AI-assisted composition.

---

## Origin

Buchbinder is a substantial expansion and re-architecture of [novel-writer-english](https://github.com/JeroTan/novel-writer-english) by JeroTan, which was itself a translation and platform-agnostic adaptation of [novel-writer-skills](https://github.com/wordflowlab/novel-writer-skills) by wordflowlab. See [ATTRIBUTION.md](./ATTRIBUTION.md) for the full chain.

The author's earlier non-agentic project, [Fiction Fabricator](https://github.com/Thomashighbaugh/fiction-fabricator) — a Python CLI for multi-phase novel generation with XML state management, lorebook support, and multi-format export — contributed key concepts that were refined and re-architected for the agentic context. Fiction Fabricator itself drew inspiration from [pulpgen](https://github.com/pulpgen-dev/pulpgen) and the broader AI creative writing ecosystem, including SillyTavern character card formats and lorebook structures from the AI roleplay community.

The shift from non-agentic Python scripts to an agentic workflow design was inspired by the terminal-based agentic coding approach of [Claude Code](https://www.anthropic.com/claude-code) by Anthropic and made possible by [OpenCode](https://github.com/sst/opencode) — the agentic coding platform whose hub-and-skill architecture, slash command system, per-project configuration model, and TypeScript tool loading are the foundation Buchbinder runs on.

**What Buchbinder adds beyond its antecedents:**

- 25-subcommand workflow with 26 spec files, 40 library files, and 34 skill files
- Fine-grained outline with scene beats, setup/payoff chains, and continuity anchors
- Outline quality gate with 3-cycle revision — blocks drafting if outline is too coarse
- XML-structured drafting with awareness maps — each chapter loads only its outline slice
- 26 hard-block quality gates across 8 categories (outline, pre-draft, post-draft, revision, structural, linguistic, experience, non-negotiables)
- 8 critique modes: alpha, beta, peer, sensitivity, cold-read, comprehensive, adversarial (two-agent dialectic), personas (3-5 reader types)
- Three-pass editing: line-edit (craft) → copy-edit (mechanics) → proofread (typos)
- Multi-pass revision with `--depth full` (structural → language → pacing)
- Per-character and per-narration voice fingerprinting
- Modular style sheets (5 modules: prose, dialogue, description, pacing, POV)
- JSON checkpoint system with content hashing for resume
- Series lorebook infrastructure with cross-book knowledge inheritance
- External lorebook import (SillyTavern, JanitorAI, CharacterAI formats)
- Premise stress-test (6 criteria, hard block) before specification
- Thematic statement (required, hard block) in constitution
- Phase 2 structural analyses: reverse outline, character arc, Q/A accounting, promise audit, escalation curve, subtext, rhythm, purple prose, immersion, trust, cognitive load, knowledge state, opening/closing, cliché detection
- Pandoc integration for production-quality export with fallback generators
- Agentic workflow design (inspired by Claude Code, built on OpenCode) replacing Fiction Fabricator's non-agentic Python CLI model
- 8 human-in-the-loop features: phase preview, authorial intent capture, diff-based approval, suggestion severity tiers, veto system (`|`), feedback memory, non-negotiables (creative constraints), change provenance tracking
- Per-project encapsulation rather than an MCP server: the entire workflow installs into each project's own `.opencode/`, so it can be tailored per book and leaves nothing behind in a global config (see [Why per-project, not an MCP server](#why-per-project-not-an-mcp-server))

---

## Why per-project, not an MCP server

Buchbinder's direct inspiration, [novel-writer-english](https://github.com/JeroTan/novel-writer-english), ships a **read-only story-lookup MCP server**: its installer registers a `novel-writer` server in each AI tool's project configuration (`.mcp.json`, `opencode.json`, `.gemini/settings.json`, `.codex/config.toml`) so that any agent can call tools like `list_chapters` or `search_character` against canonical story data.

Buchbinder deliberately does the opposite. It is not a server a project connects to; it is an **agentic workflow a project contains**, installed only into that project's own `.opencode/` directory. That choice is not incidental — it buys several things a shared MCP server cannot:

- **Granular, per-project configuration.** The 26 subcommand specs, the quality gates, the skills, the templates, and the style sheets are files *inside your project*, not a shared service. You can rewrite the outline gate for one novel, swap the critique modes for another, and add a genre-specific phase for a third without any change leaking into your other books. Configuration granularity bottoms out at the individual project — and, through the HTML-comment override workflow, at the individual phase spec within it.
- **Nothing lingers where it is not needed.** No global install, no mutation of `~/.config/opencode`, no machine-wide server registration to remember and later remove. A project that uses Buchbinder carries the whole workflow in its own `.opencode/`; a project that stops using it can delete that directory and be free of it entirely. An MCP server, by contrast, stays registered in each tool's configuration long after the one project that needed it is finished.
- **One install, many private projects.** Install the package once and scaffold as many book projects as you like. Because each project's workflow, manuscripts, and research live only in that project's own tree — and because Buchbinder never requires a project to be a public repository or an MCP-visible workspace — you can run a dozen unpublished, sensitive, or embargoed projects side by side without exposing any of them to a shared service or to public VCS. The tooling is public; the work stays private.
- **A guided workflow, not a tool surface.** An MCP server hands an agent a set of callable functions and leaves the *when* and *how* to the agent's judgement. Buchbinder instead encodes the writing process itself: a `/buchbinder` hub with state detection, an ordered phase system with hard-block gates, and a TUI menu that reports what the project needs next. The author is guided through constitution → specify → clarify → research → outline → draft → critique → revise → edit → review → publish, rather than handed a toolbox and left to orchestrate it.
- **Modular by construction.** Skills activate by description, tools load per project, and templates instantiate per book. A fiction project gets the fiction track's phases and gates; a non-fiction project gets citation and fact-check phases instead. The same core is recombined to fit each project's real needs rather than a lowest-common-denominator tool contract.

In short: an MCP server is infrastructure a project *connects to*; Buchbinder is a workflow a project *contains*. For long-form writing — where the unit of work is one book, with its own canon and its own evolving process — containment gives the better ergonomics and the better security story.

---

## Agentic AI, end to end

Buchbinder is a **compound, agentic AI system** — not a prompt pack and not a single chat loop. It orchestrates LLM inference across a deterministic state machine of writing phases, calls its own typed tools, retrieves from a per-project semantic index, evaluates every transition against hard-block gates, and returns control to the author at deliberate checkpoints. The engineering surface spans the full modern agent stack:

- **LLM orchestration** across a twelve-phase workflow (fiction), with per-phase agents, context budgets, and explicit exit criteria
- **Tool use / function calling** through project-local TypeScript tools (`hubMenu`, `split-outline`, `cite`, `track`, …) registered with OpenCode's tool API
- **Retrieval-augmented generation** with a local embedding index and reranking over each project's canon — semantic lore injection instead of context stuffing
- **Context engineering** — awareness maps that load a chapter's own outline slice, pinned adjacent chapters, and modular style sheets rather than the whole manuscript
- **Evaluation and quality gates** — 26 evidence-based, hard-block gates across 8 categories that make "the model says it's good" an unacceptable answer
- **Multi-agent critique** — an adversarial two-agent dialectic and 3–5 persona readers as first-class critique modes
- **Human-in-the-loop (HITL)** — phase preview, authorial-intent capture, diff-based approval, severity tiers, a veto key, and feedback memory
- **Observability and provenance** — per-change provenance tracking and JSON checkpoints with content hashing for reproducible resume

The goal is **output quality, not output volume**: given a premise, the workflow is engineered to produce a manuscript that is internally consistent, voice-stable, structurally sound, and — for non-fiction — correctly cited. Human-quality or better, with the review, revision, and proofreading loops a professional editor would run.

Exactly one artifact is deliberately left to a human: the **book cover**. Everything else is produced end to end — outline, draft, critique, revision, three-pass edit, continuity audit, bibliography, and multi-format export. Covers are excluded on purpose: today's generic image models return covers that are interchangeable and forgettable, and a cover is the one place a book most needs a distinct visual identity. Buchbinder would rather hand you a finished, publishable interior and let a designer (or a carefully art-directed image model) give it a face.

As a **reference implementation**, Buchbinder is a complete, shipped example of end-to-end agentic system design — a working case study in pairing an LLM workflow with deterministic guardrails, semantic retrieval, first-class UI, and reproducible per-project packaging.

---

## Built on OpenCode's SDK and plugin surface

Buchbinder exercises OpenCode's **SDK and plugin API** in ways most coding agents simply do not permit. It registers a project-local TUI plugin that renders a custom sidebar (SolidJS + OpenTUI), defines its own keybinds, opens select dialogs, raises toasts, and injects prompts back into the agent — a bespoke interface, versioned alongside the workflow it drives.

That is a real differentiator. Where other coding agents expose no supported extension surface — or leave UI extension to **third-party plugins** with no maintainer and no compatibility guarantee — OpenCode's native, project-local plugin model means Buchbinder's interface ships with the project, needs no external dependency, and cannot silently rot when a third party stops shipping updates.

---

## Nix-flake-inspired architecture

Buchbinder's packaging is a deliberate nod to **Nix flakes**: declarative, per-project, pinned, and composable.

- **Declarative per-project definition** — a project's `.opencode/` is its manifest: the plugin, its commands, its skills, its tools, and its templates, all described in place.
- **Dependency isolation** — every project pins its own copy and its own versions. A book project created today installs and behaves the same way a year from now on another machine.
- **Diff-based, non-destructive sync** — `buchbinder-refresh` updates only what changed and preserves local edits; the HTML-comment override workflow plays the role of an overlay.
- **Maximum control through granularity** — modularity at the level of skills, tools, templates, and even individual phase specs means you override exactly what you want and inherit the rest.

The payoff is control without sprawl: reproducibility and isolation in the Nix tradition, scoped to a single book rather than a whole system.

---

## On dependencies, and when "Not Invented Here" does not apply

The usual advice — *don't reinvent the wheel; use a dependency* — treats "Not Invented Here" as an anti-pattern. That framing assumes a reimplementation means owning and maintaining a library, with a team, for years.

The assumption collapses when three things hold at once:

1. the needed functionality is small and self-contained,
2. a correct implementation costs **minutes to hours** (when done well), and
3. the code can be produced by a well-prompted LLM through multi-pass review-and-revise cycles at **pennies on the dollar**.

Under those conditions, vendoring the functionality is not Not-Invented-Here stubbornness — it is a rational trade of a trivial, one-time cost for permanent control. No third-party maintainer to depend on, no abandoned plugin to migrate away from, no supply-chain surface you did not choose, and a result you can read, audit, and change in place. Buchbinder applies this deliberately, and still reaches for a dependency where a dependency genuinely is the better tool (`fs-extra`, `fast-xml-parser`, `solid-js`, `@opentui/*`). The point is not to avoid dependencies; it is to stop cargo-culting the heuristic that says reimplementation is always wrong.

---

## Quick Start

```bash
# In your book project directory
npx buchbinder
```

The interactive installer will:
1. Ask which track you want (fiction / non-fiction / mixed)
2. Create the project directory structure under `book/`
3. Install commands, skills, templates, tools, and lib files into `.opencode/`
4. Initialize track metadata

After installation, type `/buchbinder` in OpenCode to open the workflow menu, or type `/buchbinder <subcommand>` for direct dispatch.

---

## The 25-Subcommand Workflow

All functionality is accessed through the `/buchbinder` hub command. `/buchbinder` with no arguments opens an interactive menu via state detection. `/buchbinder <subcommand>` routes directly to the specified phase.

### Phase Subcommands

| # | Subcommand | Purpose | Key Features |
|---|------------|---------|--------------|
| 1 | `constitute` | Establish creative/intellectual principles | Thematic statement (required, hard block), series lorebook inheritance |
| 2 | `specify` | Build story specification | Premise stress-test (6 criteria, hard block) before specification |
| 3 | `clarify` | Resolve specification ambiguities | Consistency checker, forgotten elements scan |
| 4 | `research` | Active research | Sources, annotation, literature review, field notes, interviews |
| 5 | `outline` | Fine-grained chapter structure | Scene beats (min 2/chapter), setup/payoff chains, continuity anchors, quality gate + 3 revision cycles |
| 6 | `task-manager` | Break outline into tracked tasks | Per-chapter sub-status lifecycle |
| 7 | `draft` | Write chapters | Batch-first (up to 6), XML structure, awareness map, prose quality, echo detection, beat arc check |
| 8 | `critique` | Structured critique | 8 modes: alpha, beta, peer, sensitivity, cold-read, comprehensive, adversarial, personas |
| 9 | `revise` | Apply revisions | Batch revision, revision-verify gate, `--depth full` (structural→language→pacing) |
| 10 | `edit` | Line-level editing | Three-pass: line-edit → copy-edit → proofread + linguistic gates (subtext, purple-prose, cliché, rhythm) |
| 11 | `review` | Broad project QA | Continuity scan + 7 Phase 2 structural analyses + 2 visualization outputs |
| 12 | `publish` | Export manuscript | Pandoc integration + post-export verification |

### Utility Subcommands

| Subcommand | Purpose |
|------------|---------|
| `guided` | Automatic state detection — recommends next phase |
| `track` | Unified tracking: character state, plot progress, timeline, sources |
| `timeline` | Chronological consistency verification |
| `meta` | Bibliographic metadata management |
| `cite` | Citation lifecycle (non-fiction): add, format, validate, bibliography |
| `drafter` | Loose draft jumpstart from raw ideas |
| `verify` | On-demand quality gate runner — 25 gates available |
| `resume` | JSON checkpoint resume with file diff |
| `cycle` | Full draft→critique→revise→edit cycle for all chapters |
| `pacing-audit` | Cross-chapter pacing analysis |
| `hook-review` | Opening/closing hook audit + book-level opening/closing strength |
| `read-through` | Full reader experience audit + immersion + trust accounting |
| `series` | Series lorebook operations: init, sync, audit, register, status, import |

---

## Quality Gate System

Buchbinder uses **hard-block quality gates** — gates produce evidence-based pass/fail results that block progression on failure. No soft warnings: a gate either passes or stops the workflow with specific evidence.

### 26 Gates Across 8 Categories

| Category | Gates | When Run |
|----------|-------|----------|
| **Outline** | `outline` | Before drafting — checks scene beats (min 2/chapter), setup/payoff bidirectionality, continuity anchors, pacing distribution |
| **Pre-Draft** | `pre-draft` | Before each draft session — 13 context items must be loaded with evidence |
| **Post-Draft** | `post-draft`, `prose-quality`, `echo-detection`, `beat-arc` | After drafting — XML structure, metadata, scenes, tracking, voice, awareness map verification, prose metrics (filter words, adverbs, passive, info-dumps, tense/POV), echo/repetition, beat arc trajectory |
| **Revision** | `revision-verify` | After revision — critique items cross-referenced against revision log |
| **Structural** | `reverse-outline`, `character-arc`, `qa-accounting`, `promise-audit`, `escalation-curve`, `cognitive-load`, `knowledge-state`, `thread-matrix`, `dependency-graph` | During review — Phase 2 deep analyses |
| **Linguistic** | `subtext`, `purple-prose`, `cliche`, `rhythm` | During edit — on-the-nose dialogue, overwriting, clichés, sentence monotony |
| **Experience** | `immersion`, `trust`, `opening-closing`, `continuity`, `style` | During read-through/review — immersion breaks, trust violations, hook strength, cross-chapter contradictions, style sheet compliance |
| **Non-negotiables** | `non-negotiables` | During draft/revise/edit — checks content against author's declared creative constraints (plot, character, tone, content, structure, world) |

### Gate Severity Levels

| Level | Behavior |
|-------|----------|
| **Hard block** | Workflow stops. Evidence cited. Must fix before proceeding. |
| **Warning** | Flagged for review. Does not block progression. |

Prose quality scorecard: 5 hard-block metrics (filter words, adverbs, passive voice, info-dumps, tense/POV drift) + 4 warning metrics (showing/telling, concrete ratio, crutch words, dialogue ratio).

Echo detection: 2 hard-block checks (word echo, crutch words) + 2 warning checks (structural echo, beat echo).

Run `/buchbinder verify` to run any gate on demand. Run `/buchbinder verify --all` to run all gates.

---

## Track System

| Track | Phase Sequence | Use Case |
|-------|---------------|----------|
| **Fiction** | Constitute → Specify → Clarify → (Research) → Outline (gate) → Tasks → Draft → Critique → Revise → Edit (3-pass) → Review → Read-Through → Publish | Novels, short stories, serials, creative non-fiction |
| **Non-Fiction** | Constitute → Research → (Cite) → Outline → Tasks → Draft → Fact Check → Cite → Revise → Edit (3-pass) → Review → Publish | Academic works, journalism, biography, technical books |
| **Mixed** | Constitute → Specify + Research → Clarify → Outline → Tasks → Draft → Fact Check → Cite → Critique → Revise → Edit → Review → Read-Through → Publish | Creative non-fiction, memoir with research, narrative journalism |
| **Series** | Series Lorebook Init → Constitute (inherit) → Specify → Outline → [per-book cycle] → Series Audit → Sync Lorebook | Multi-book series with shared world/characters |

---

## XML-Structured Drafting

Drafts use internal XML tags for verification. Tags are stripped on save to produce clean prose.

```xml
<chapter number="3" title="The Summons">
<metadata>
  <wordcount>3200</wordcount>
  <pov>Mira</pov>
  <timeline>Day 4, evening</timeline>
  <characters-present>Mira, Theron, Captain Voss</characters-present>
</metadata>

<awareness-map>
  <payoff-from>ch2:Theron's-suspicion, ch1:summons-arrival</payoff-from>
  <sets-up>ch5:betrayal-revelation</sets-up>
  <continuity-anchors>Mira's scar (ch1), Voss's loyalty (ch2)</continuity-anchors>
</awareness-map>

<scene number="1" goal="Mira confronts Theron about his disappearance">
<beatchange emotion="dread" intensity="3" reason="Theron's evasion suggests guilt"/>
...

<tracking>
  <open-threads>summons-origin, Theron's-absence, Voss's-secret</open-threads>
  <resolved-threads>none</resolved-threads>
</tracking>
</chapter>
```

The post-draft gate verifies:
- XML structure completeness (metadata, scenes, tracking)
- Awareness map honored (payoff-from items addressed, sets-up items planted, continuity anchors present)
- Voice profile compliance (per-character + per-narration)
- Style sheet compliance (5 modules)
- Prose quality scorecard (9 metrics)
- Echo detection (4 checks)
- Beat arc trajectory (flat streak detection, cross-chapter arc)

---

## Critique Modes

| Mode | Description |
|------|-------------|
| **alpha** | Structural critique: pacing, plot logic, character arcs, scene necessity, causality |
| **beta** | Experience critique: engagement, comprehension, emotional investment, clarity |
| **peer** | Academic/peer review methodology (non-fiction) |
| **sensitivity** | Sensitivity assessment: representation, stereotypes, harmful tropes |
| **cold-read** | First-impression reader with no context — surfaces confusion points |
| **comprehensive** | All dimensions in a single pass |
| **adversarial** | Two-agent dialectic: defender agent + challenger agent + synthesis agent for blind-spot surfacing |
| **personas** | 3-5 reader types: Genre Fan, Casual Reader, Literary Critic, Subject Expert, Skeptical Reviewer |

---

## Three-Pass Editing

| Pass | Focus | What It Checks |
|------|-------|----------------|
| **line-edit** | Craft | Sentence-level quality, word choice, rhythm, imagery, scene construction, dialogue tags, showing vs telling |
| **copy-edit** | Mechanics | Grammar, punctuation, spelling, consistency (tense, POV, names), formatting, style sheet compliance |
| **proofread** | Typos | Final pass — typos, missing words, doubled words, punctuation errors, formatting glitches |

Linguistic analyses run during editing:
- **Subtext analysis**: on-the-nose dialogue detection
- **Purple prose**: modifier ratio, metaphor density, elevated vocabulary
- **Cliché detection**: 5 phrase categories + 5 genre-trope overuse categories
- **Sentence rhythm**: length distribution, monotony score, consecutive similar-length detection

---

## Phase 2 Structural Analyses

Run during `/buchbinder review` — 14 dedicated analysis libraries:

| Analysis | What It Detects |
|----------|----------------|
| **Reverse outline** | Draft vs planned outline comparison — missing beats, added beats, drift |
| **Character arc** | Per-character arc completeness (intro→escalation→crisis→transformation→resolution) |
| **Q/A accounting** | Narrative question tracking — answered, unanswered, deliberately unresolved |
| **Promise audit** | Genre/tone/thematic/structural/mystery/romantic promises kept by book end |
| **Escalation curve** | Stakes escalation from act to act, plateau detection, descending stretches |
| **Subtext analysis** | On-the-nose dialogue detection, surface vs subtext comparison |
| **Sentence rhythm** | Length distribution, monotony score, consecutive similar-length detection |
| **Purple prose** | Modifier ratio, metaphor density, elevated vocabulary, purple passages |
| **Immersion audit** | Anachronisms, authorial intrusion, meta-references, tone shifts, logic breaks |
| **Trust audit** | Coincidences, deus ex machina, stupid-for-plot, plot armor |
| **Cognitive load** | Per-chapter named characters/active threads/open questions tracking |
| **Knowledge state** | Character vs reader knowledge matrix, dramatic irony detection |
| **Opening/closing** | First/last 500 words analysis, hook scoring, resonance scoring |
| **Cliché detection** | Cliché phrases (5 categories), genre-trope overuse (5 genres) |

---

## Series Lorebook Infrastructure

For multi-book series, Buchbinder provides a shared knowledge base:

```
book/series/lorebook/
├── characters.md    # Cross-book character profiles
├── glossary.md       # Shared terminology
├── threads.md        # Active plot threads across books
├── timeline.json     # Master timeline (all books)
└── world.md          # World-building canon
```

- `/buchbinder series init` — Initialize series lorebook
- `/buchbinder series sync` — Sync book-level knowledge to lorebook
- `/buchbinder series audit` — Audit lorebook for inconsistencies
- `/buchbinder series register` — Register a new book in the series
- `/buchbinder series status` — Show series status and per-book progress
- `/buchbinder series import` — Import external lorebook (SillyTavern, JanitorAI, CharacterAI)

### Semantic Lore Injection

When generating content (outline, draft, critique, revise, review), Buchbinder uses **semantic lore retrieval** to inject only the most relevant lore into the prompt — not the entire lorebook. This keeps the context window focused and reduces token usage.

The retrieval pipeline is **two-stage** and fully local. Both stages default to **ONNX** (in-process, via `@huggingface/transformers`) — Ollama is an opt-in extra backend, not a requirement:

1. **Embedding** — `Xenova/bge-base-en-v1.5` (ONNX, 768-d; `EMBED_BACKEND=onnx`, the default) or `pedrohml/mxbai-embed-large:latest` (Ollama, 1024-d; `EMBED_BACKEND=ollama`) — Chunks lore files by section (## headings) and embeds each chunk
2. **Vector search** — Cosine similarity between the task query and lore chunks
3. **Reranking** (optional, `--rerank`) — an **in-process ONNX cross-encoder** (`Xenova/bge-reranker-base`) re-scores the top candidates jointly. Because a cross-encoder sees the query and the passage together, it reorders candidates more accurately than distance alone.

**Setup:** nothing to pull by hand — `npx buchbinder` fetches the ONNX models (embedder + reranker + classifier, ≈0.5 GB) into a shared cache (`~/.cache/buchbinder/models`) during install. To fetch or re-fetch them later:

```bash
npx buchbinder-models
```

Everything runs locally — no data leaves your machine, and no provider API requests are made. The query script (`lore-query.mjs`) is installed as `.opencode/lib/scripts/lore-query.mjs` and called automatically by the phase workflows. The ONNX runtime (`@huggingface/transformers`) is added to the project's `.opencode/package.json` by the installer.

If a model or the ONNX runtime is unavailable, the system degrades gracefully — embedding falls back to distance-only retrieval, then to reading lore files directly. No functionality is lost, only the selective retrieval optimization.

External lorebook import supports:
- **SillyTavern** character cards (PNG embedded JSON, JSON files)
- **JanitorAI** character definitions
- **CharacterAI** character exports
- Heuristic classification of entries into characters, locations, items, concepts

#### On-disk Index (v3)

Lore retrieval is fast because Buchbinder maintains an on-disk embedding index at:

```
.opencode/cache/lore-index/index.json
```

The index is built once and reused on every phase invocation. Without the index, `lore-query.mjs` re-embeds every chunk on every call (slow for multi-book series). With the index, query time is O(chunks) cosine comparisons in memory + one Ollama call for the query embedding.

**Index coverage** — these source files are scanned:

| Path | Chunked by | Notes |
|------|-----------|-------|
| `series/lorebook/*` | Markdown headings | characters, world, glossary, timeline.json, threads |
| `series/outline.md` | Markdown headings | Cross-book condensed outline (series-level beats) |
| `book/knowledge/*` | Markdown headings | character-profiles, voice-profiles, locations, world-rules, character-voices |
| `book/constitution.md` | Markdown headings | Project canon — highest priority |
| `book/specification.md` | Markdown headings | Book specification |
| `book/outline.md`, `book/outline/chapter_*.md` | Markdown headings / one-per-file | Whole-book + per-chapter outline |
| `book/drafts/chapter_*.xml` | **XML chunker** (see below) | Drafted chapters |

**Build / refresh the index:**
```bash
# Build or incrementally update the index
npx buchbinder-index

# Or from the lore-query script itself
bun .opencode/lib/scripts/lore-query.mjs --build

# Check status (chunk count, age, embedder version)
bun .opencode/lib/scripts/lore-query.mjs --status
```

The index build is **incremental**: re-running on an up-to-date index is a no-op. Only source files whose content has changed since the last build are re-chunked and re-embedded. `npx buchbinder-refresh` (see below) rebuilds the index automatically when source files have changed.

**Env overrides.** Retrieval defaults, all overridable:

| Var | Default | Purpose |
|-----|---------|---------|
| `EMBED_BACKEND` | `onnx` | `onnx` (default) \| `ollama` |
| `ONNX_EMBED_MODEL` | `Xenova/bge-base-en-v1.5` | ONNX embedding model (768-d) |
| `OLLAMA_EMBED_MODEL` | `pedrohml/mxbai-embed-large:latest` | Ollama embedding model (`EMBED_MODEL` is an alias) |
| `RERANK_MODEL` | `Xenova/bge-reranker-base` | ONNX cross-encoder |
| `RERANK_BACKEND` | `onnx` | `onnx` \| `ollama` \| `none` |
| `CLASSIFIER_MODEL` | `Xenova/nli-deberta-v3-xsmall` | zero-shot / NLI classifier |
| `ONNX_DTYPE` | `q8` | ONNX weight dtype |
| `ONNX_CACHE_DIR` | `~/.cache/buchbinder/models` | shared ONNX model cache |
| `ONNX_OFFLINE` | unset | `1` — never download; use cache or fall back |
| `RERANK_MAX_LENGTH` | `512` | reranker tokenizer truncation length |
| `RERANK_DISABLED` | unset | `1` — force distance-only retrieval |
| `OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama endpoint (only for the `ollama` backends) |

#### Local ONNX model stack

Three small Transformers.js models power retrieval and quality evidence. They are fetched once into a shared, machine-wide cache and reused by every Buchbinder project:

| Role | Model | ≈Size |
|------|-------|-------|
| Embeddings | `Xenova/bge-base-en-v1.5` | 110 MB |
| Reranking | `Xenova/bge-reranker-base` | 280 MB |
| Classification (NLI) | `Xenova/nli-deberta-v3-xsmall` | 70 MB |

The classifier turns qualitative judgements into local, reproducible evidence — useful for the hard-block quality gates ("does this chapter entail its outline beat?"), the premise stress-test, and non-fiction claim↔source checks:

```bash
# Zero-shot ranking of labels for a passage
node .opencode/lib/classifier.mjs --labels "foreshadowing,pacing,continuity" "the passage text"
# NLI entailment between a premise and a hypothesis
node .opencode/lib/classifier.mjs --entail "Chapter 7 pays off the locket from Chapter 2" "the locket resurfaces"
```

**Wired into the gates.** The classifier runs as a step *inside* two quality gates, chosen because NLI is decisive when a delivered artifact must entail a claimed property: `post-draft` (does the prose entail the draft's own awareness-map claims) and `revision-verify` (does each revision entry entail the critique recommendation it claims to address). Gates whose relation is *correspondence* rather than entailment — such as the outline's setup↔payoff pairing — are deliberately left out, because NLI scores those unreliably and a noisy step erodes gate trust:

```bash
node .opencode/lib/nli-gates.mjs --gate post-draft . --chapter 3
```

Findings are deliberately surgical — lowest entailment first, capped — and persisted to `.opencode/cache/nli-evidence/<gate>.{json,md}` so the evidence is available exactly when the gate runs.

#### Pinned Adjacent Chapters

For draft, critique, and revise phases, the lore query can **pin** specific chapters to be included **verbatim** in the context, regardless of semantic score. This is critical for continuity — the agent drafting chapter N needs the exact last scene of N-1.

```bash
# /buchbinder draft Chapter 5 → include the entire prior chapter (4) verbatim
bun .opencode/lib/scripts/lore-query.mjs \
  --query "Draft context for chapter 5" \
  --pin-chapter 5 --pin-side previous --top 5 --rerank

# /buchbinder critique Chapter 5 → include both N-1 and N+1 verbatim
bun .opencode/lib/scripts/lore-query.mjs \
  --query "Critique context for chapter 5" \
  --pin-chapter 5 --pin-side both --top 5 --rerank
```

- `--pin-side previous` → pin chapter N-1
- `--pin-side next` → pin chapter N+1
- `--pin-side both` → pin both N-1 and N+1

The pinned chapter is loaded from disk directly (bypassing the index). It's emitted in the context block as raw XML, clearly marked as `PINNED — verbatim for continuity`.

#### XML Draft Chunker

`book/drafts/chapter_*.xml` files use a **separate chunker** that understands the draft schema:

```xml
<chapter number="N" title="...">
  <metadata>...</metadata>              <!-- 1 chunk: who/where/when -->
  <awareness-map>
    <sets-up ref="ChM: ...">...</sets-up>
    <payoff-from ref="ChM: ...">...</payoff-from>
    <continuity-anchors>
      <anchor name="...">...</anchor>
    </continuity-anchors>
  </awareness-map>                     <!-- 1 chunk: cross-chapter refs -->
  <scene number="K" type="..." goal="..." conflict="...">
    <narration>...</narration>
    <interiority .../>
    <sensory-inject .../>
  </scene>                              <!-- 1 chunk per <scene> -->
  <scene continuation="true" ...>       <!-- continuation scenes get inferred numbers -->
</chapter>
```

Emits four chunk kinds per file: `metadata`, `awareness`, `scene` (one per `<scene>`), and `whole-chapter` (used only by the pinned path). Continuation scenes (`<scene continuation="true">` with no `number=` attribute) get an inferred sequential number so a 7-scene chapter always produces 7 scene chunks.

The chunker is permissive: missing `<metadata>` or `<awareness-map>` blocks are skipped silently; unknown `<scene>` children are flattened to text. The markdown chunker handles the lore, outline, canon, and spec sources; the XML chunker handles only the drafts.

### Lore as Canonical Truth (Doctrine)

The lorebook — `series/lorebook/*`, `book/knowledge/*`, `book/constitution.md`, `book/specification.md`, and the project `series/outline.md` / `book/outline.md` — is the **absolute source of truth** for a project. Between agents (outline, draft, critique, revise, review), the lorebook is taken as literal, beyond-reproach canon. Only the human user's explicit direction can alter lore; agents must work hard to make internally-consistent sense of canon before suggesting any change.

**If you believe a lore entry is wrong, do NOT silently rewrite it.** Flag it in the critique report (`./book/critique/chapter_NN.md`) and ask the user. If a draft would substantially contradict established lore, halt and ask the user before proceeding.

This doctrine is restated in each phase spec (`outline`, `draft`, `critique`, `revise`, `review`) so every agent invocation sees it.

### Local Overrides via HTML Comments

Buchbinder ships a set of phase specs (`src/tools/hubs/buchbinder/{outline,draft,critique,revise,review}.ts`) that you may want to customize for your project. Because the `npx buchbinder-refresh` command preserves locally-modified files (see below), a common workflow is:

1. Run `npx buchbinder-refresh` once after install to set up the baseline.
2. Edit a phase spec (e.g. `.opencode/tools/hubs/buchbinder/outline.ts`) to add a custom instruction wrapped in HTML comments for clarity.
3. Subsequent refreshes leave your edit alone — the file appears in the `locallyModified[]` list in the refresh summary.

Example:
```ts
// .opencode/tools/hubs/buchbinder/draft.ts
// <!-- buchbinder:override -->
// Custom: always end chapters on a sensory beat, not a dialogue beat.
// <!-- /buchbinder:override -->
```

The override survives refreshes because `npx buchbinder-refresh` diffs your file against the source and skips the copy when the SHA differs. Use `--force` to override (destructive).

### Per-project Install Model

Buchbinder installs **per-project**, not globally. Each book project has its own `.opencode/` directory containing its own copy of the plugin's skills, tools, templates, slash commands, and TUI sidebar plugin. This mirrors the Nix/dependency-isolation pattern: pinning per project means a project created today will build the same way a year from now on a different machine. This containment — and why it is preferable to an MCP-server approach — is covered in [Why per-project, not an MCP server](#why-per-project-not-an-mcp-server).

The install writes `.opencode/opencode.jsonc`, `.opencode/tui.json`, and `.opencode/package.json` to register the buchbinder-sidebar plugin as a project-local plugin. It does **not** touch your global opencode config, `~/.config/opencode`, or your global `node_modules`. Plugin-owned subtrees are: `skills/`, `tools/`, `templates/`, `commands/`, `plugins/`, plus the three config files. Everything else under `.opencode/` (and the project-root `book/`, `memory/`, `output/`, `series/` directories) is project-owned and never touched by install or refresh.

The first time you install, the installer prints an acknowledgement screen explaining the per-project model and asks you to confirm before proceeding. The acknowledgement is not recorded — you re-acknowledge on every fresh install.

### Refreshing an Existing Install

Once a project is installed, use `npx buchbinder-refresh` to sync updates:

```bash
# Default: sync changed/new files, preserve your local edits
npx buchbinder-refresh

# Also remove files that disappeared from source
npx buchbinder-refresh --prune

# Overwrite locally-modified files (destructive)
npx buchbinder-refresh --force

# Skip the sidebar TypeScript build (faster, for iteration)
npx buchbinder-refresh --skip-build

# Skip the lore index rebuild
npx buchbinder-refresh --skip-index

# For postinstall / CI: skip prompts, defaults track='fiction'
npx buchbinder-refresh --postinstall
```

`buchbinder-refresh`:
- Always rebuilds the TypeScript-derived sidebar bundle (`npm run build:sidebar` in the package).
- Always rebuilds the lore index (incrementally).
- Preserves files you've locally modified (HTML-comment override workflow).
- Never touches project-owned paths.

The `postinstall` script in `package.json` calls `node bin/refresh.mjs --postinstall || true` so `npm install buchbinder` from a consumer project also triggers a sync. This is idempotent — re-running on an up-to-date project is a no-op.

Exit codes:
- `0` — success, no drift
- `1` — success, but locally-modified files were preserved (drift detected; review the `locallyModified[]` list)
- `2` — refresh failed

---

## Voice & Style System

### Voice Profiles

Per-character AND per-narration voice fingerprints:

```json
{
  "narration": {
    "register": "literary",
    "sentenceLength": "varied",
    "figurativeDensity": "moderate",
    "sensoryPriority": ["tactile", "auditory", "visual"]
  },
  "characters": {
    "Mira": {
      "register": "blunt",
      "vocabulary": "sparse",
      "speechPattern": "short-declarative",
      "contractions": true
    }
  }
}
```

### Modular Style Sheets

5 separate modules in `book/style-sheet/`:

| Module | What It Covers |
|--------|---------------|
| `prose.md` | Sentence structure, paragraph rhythm, figurative language density |
| `dialogue.md` | Dialogue tags, speech patterns, attribution conventions |
| `description.md` | Sensory emphasis, description density, exposition handling |
| `pacing.md` | Scene length, chapter rhythm, tension/release cycles |
| `pov.md` | POV type, head-hopping rules, narrator distance |

---

## Human-in-the-Loop Features

Buchbinder integrates 8 HITL features to keep the author in control of the AI-assisted process:

### Phase Preview

Before any phase executes, the author sees a preview: which chapters will be affected, estimated duration, what context will be loaded, which gates will run. The author confirms before execution.

```
## Phase Preview: DRAFT
Chapters: 3, 4, 5, 6, 7, 8 (6 total)
Estimated duration: ~36 minutes (18000 words)
Gates to run: pre-draft, post-draft, prose-quality, echo-detection, beat-arc, non-negotiables
Confirm to proceed.
```

### Authorial Intent

Before each phase (draft, revise, edit), the author states their intent in 1-2 sentences. If unsure, a generic intent is used: "Produce the best possible output consistent with the outline and constitution." After the phase, the AI verifies the output honors the stated intent.

### Diff-Based Approval

After revise or edit passes, the author sees a structured diff (before/after). Approve line-by-line, reject specific hunks, or accept all. Rejected hunks preserve the original text.

### Suggestion Severity Tiers

All AI suggestions are tiered:

| Tier | Behavior |
|------|----------|
| **must-fix** | Blocks progression (maps to gate failure) |
| **should-consider** | Warning — flagged but not blocking |
| **your-call** | Preference — author's choice |
| **FYI** | Observation — no action needed |

Author controls the filter level — only must-fix shown by default.

### Veto System

The author types `|` to veto any suggestion:
- `|` — silent veto (no explanation required)
- `| keeping this rhythm for effect` — veto with reason

Vetoed suggestions are never re-suggested. Vetoes with reasons feed into feedback memory.

### Feedback Memory

When the author rejects a suggestion with a reason, the reason is logged as an avoidance pattern. The AI checks preferences before making future suggestions and avoids patterns the author has consistently rejected.

### Non-Negotiables (Creative Constraints)

At constitution, the author declares creative elements that must not be changed by any AI pass — the author's red lines:

| Category | Example |
|----------|---------|
| **Plot** | "Mira must die in chapter 12" |
| **Character** | "Theron never lies" |
| **Tone** | "Always melancholic, never hopeful" |
| **Content** | "No on-page violence against children" |
| **Structure** | "Each chapter must end on a turn" |
| **World** | "Magic always has a cost" |

The `non-negotiables` gate checks all content against these constraints during draft, revise, and edit phases. Violations block progression.

### Provenance Tracking

Every line of prose is tagged with its origin:

| Origin | Meaning |
|--------|---------|
| `author` | Written by the author |
| `ai-drafted` | Generated by AI in draft phase |
| `ai-revised` | Revised by AI (approved as-is) |
| `ai-edited` | Edited by AI (approved as-is) |
| `ai-modified` | AI-suggested, modified by author before acceptance |
| `author-revised` | Author revised AI output |

Manuscript-level statistics show the author vs AI percentage, per chapter and aggregate.

---

## Checkpoint System

JSON checkpoints save state after each phase, enabling resume:

```json
{
  "phase": "draft",
  "chapter": 7,
  "batchSize": 6,
  "contentHash": "sha256:...",
  "gates": { "pre-draft": "pass", "post-draft": "pass" },
  "timestamp": "2026-07-07T..."
}
```

`/buchbinder resume` loads checkpoint, diffs files against content hash, and reports what changed since the checkpoint was saved.

---

## Project Structure

```
project/
├── .opencode/               # Installed workflow
│   ├── commands/buchbinder-router.md  # Hub phase router (direct phase execution)
│   ├── skills/               # 34 SKILL.md files across 5 categories
│   │   ├── quality-assurance/
│   │   ├── critique/
│   │   ├── research/
│   │   ├── fiction/writing-techniques/
│   │   ├── fiction/genre-knowledge/
│   │   └── non-fiction/
│   ├── tools/
│   │   ├── hubs/buchbinder/    # 26 subcommand spec files
│   │   └── lib/             # 32 library files
│   └── templates/           # Track + series templates
├── book/                    # All book content
│   ├── track.json           # Track selection: fiction | non-fiction | mixed
│   ├── constitution.md      # Core rules + thematic statement
│   ├── specification.md     # Story spec (with premise stress-test)
│   ├── outline/             # Fine-grained chapter structure
│   ├── content/             # Clean prose (tags stripped)
│   ├── drafts/              # XML-structured drafts (with verification tags)
│   ├── critique/            # Critique artifacts (8 modes)
│   ├── revisions/           # Revision tracking + verify gate results
│   ├── knowledge/           # Character profiles, locations, glossary
│   ├── tracking/            # State tracking JSON
│   ├── style-sheet/         # 5 modular style sheets
│   ├── checkpoints/         # JSON checkpoint state
│   ├── research/            # Sources, bibliography, interviews
│   └── series/lorebook/     # Series lorebook (if series project)
├── memory/                  # Durable reference
└── output/                  # Published exports
```

---

## Batch-First Defaults

All pipeline phases default to batch processing:
- **draft**: All chapters or up to 6 at a time
- **critique**: All chapters with shared context loaded once per batch
- **revise**: All chapters or up to 6
- **edit**: All chapters or up to 6
- **cycle**: Full draft→critique→revise→edit for all chapters

Single-chapter is an explicit override: `/buchbinder draft 5` or `/buchbinder edit Chapter 3`.

Shared context (constitution, specification, knowledge, tracking, style sheet) is loaded **once per batch**, not per chapter.

---

## Development

```bash
git clone <repo>
cd buchbinder
npm install
npx tsc --noEmit    # Type check
node bin/install.mjs test-dir   # Test installation
```

Source structure:
- `src/commands/buchbinder-router.md` — Hub phase router (direct `/buchbinder-router <phase>`)
- `src/tools/hubs/buchbinder/` — 26 subcommand spec files
- `src/lib/` — 32 library files (gates, voice, checkpoints, analyses, etc.)
- `src/skills/` — 34 SKILL.md files across 5 categories
- `src/templates/` — Track templates (fiction, non-fiction, series)
- `bin/install.mjs` — Interactive installer

---

## Keywords

Agentic AI · LLM orchestration · multi-agent systems · compound AI systems · tool calling / function calling · retrieval-augmented generation (RAG) · semantic search · embeddings · reranking · vector retrieval · prompt engineering · context engineering · evaluation harness · quality gates · deterministic pipelines · workflow state machines · human-in-the-loop (HITL) · Model Context Protocol (MCP) · TypeScript · OpenCode SDK · OpenCode plugin API · SolidJS · OpenTUI · TUI design · per-project configuration · dependency isolation · Nix flakes · reproducible builds · supply-chain security · checkpointing · observability · provenance · structured output · XML structuring · long-form content generation · creative-writing automation · publishing pipeline · Pandoc.

---

## License

MIT. See [LICENSE](./LICENSE).

---

## Attribution

This project builds upon the work of multiple antecedent projects:

- **wordflowlab** — [novel-writer-skills](https://github.com/wordflowlab/novel-writer-skills) (MIT) — original Chinese-language methodology and skill architecture
- **JeroTan** — [novel-writer-english](https://github.com/JeroTan/novel-writer-english) (MIT) — English translation and eight-step fiction workflow
- **Thomas Highbaugh** — [Fiction Fabricator](https://github.com/Thomashighbaugh/fiction-fabricator) (MIT) — the author's earlier non-agentic AI novel generator; contributed multi-phase generation, XML state management, lorebook system, and export concepts that were refined for the agentic context
- **pulpgen-dev** — [pulpgen](https://github.com/pulpgen-dev/pulpgen) (MIT) — AI novel drafting agent that inspired Fiction Fabricator's multi-phase approach and patch-based state tracking
- **OpenCode team** — [OpenCode](https://github.com/sst/opencode) — the agentic coding platform whose hub-and-skill architecture, slash command system, and per-project configuration model are the foundation Buchbinder runs on
- **Anthropic** — [Claude Code](https://www.anthropic.com/claude-code) — terminal-based agentic coding approach that inspired the shift from non-agentic Python scripts to an agentic workflow design

See [ATTRIBUTION.md](./ATTRIBUTION.md) for the full attribution chain and a detailed accounting of what Buchbinder adds.