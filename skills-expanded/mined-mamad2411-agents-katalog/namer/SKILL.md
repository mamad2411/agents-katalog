---
name: namer
description: >-
  Name anything: projects, products, companies, packages. Generates creative
  names across linguistic archetypes, checks handle/username availability across
  platforms, checks domain availability with pricing, and ranks options with
  scored rationales. Use when naming projects, products, startups, packages,
  or brands. NOT for domain management (infrastructure-coder) or branding
  strategy beyond naming (host-panel).
license: MIT
argument-hint: "<thing to name> [--context description] [--style playful|serious|technical|abstract] [--thorough]"
model: opus
metadata:
  author: wyattowalsh
  version: "1.0.0"
hooks:
  PreToolUse:
    - matcher: Edit
      hooks:
        - command: 'bash -c "echo BLOCKED: namer skill is read-only — no file edits permitted >&2; exit 1"'
---

# Namer

Generate, evaluate, and validate names across linguistic, technical, and platform dimensions. Produces ranked options with availability matrices and actionable next steps.

Not for domain registration, branding strategy, or logo design. Not for reviewing naming conventions in existing code.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<thing to name>` (with optional flags) | **Name** — full pipeline: brief → generate → filter → check → score → rank |
| `check <name> [name2...]` | **Check** — availability audit only (skip generation) |
| `expand <name>` | **Expand** — generate variations/modifications of an existing name |
| `compare <name1> vs <name2> [vs...]` | **Compare** — side-by-side scoring of specific names |
| `resume [# or keyword]` | **Resume** — load prior naming session |
| `list` | **List** — show saved naming sessions |
| `preferences` | **Preferences** — show accumulated naming profile and memory stats |
| Empty | **Gallery** — show examples + "what are you naming?" prompt |

### Gallery (Empty Arguments)

| # | Context | Example |
|---|---------|---------|
| 1 | CLI Tool | "I'm building a terminal file manager in Rust" |
| 2 | SaaS Product | "Developer productivity tool for code review" |
| 3 | OSS Library | "Python library for data validation" |
| 4 | Startup | "AI-powered hiring platform" |
| 5 | Side Project | "Weekend project — a bookmark manager" |
| 6 | Brand | "Design agency specializing in developer tools" |

> Pick a number, describe what you're naming, or type "guide me".

### Guided Intake

If the user types "guide me", ask three questions:

1. **What are you naming?** "A CLI tool, a SaaS product, an OSS library, a startup, a brand, or something else?"
2. **What does it do?** "Describe it in one sentence."
3. **What vibe?** "Playful, serious, technical, warm, edgy, minimal, or describe your own."

## Dynamic Context Classification

Auto-detect from the user's description. Adjusts both platform priority AND scoring weights.

| Context Signal | Category | Primary Platforms | Secondary |
|----------------|----------|-------------------|-----------|
| "CLI tool", "command", "binary" | **CLI Tool** | GitHub, npm/PyPI/Crates, Homebrew, .dev | Social |
| "package", "library", "framework", "SDK" | **OSS Library** | GitHub, npm/PyPI/Crates, .dev/.io | Social |
| "app", "product", "startup", "SaaS" | **Product** | .com, X/Twitter, LinkedIn, GitHub | Dev registries |
| "company", "brand", "agency", "studio" | **Brand** | .com, X/Twitter, Instagram, LinkedIn, YouTube | Dev registries |
| "game", "content", "media", "community" | **Creative** | .com, YouTube, TikTok, X/Twitter, Reddit, Discord | Dev registries |
| "open source", "OSS", "contrib" | **OSS Project** | GitHub, npm/PyPI/Crates, .dev, Discord | Social |
| Ambiguous | **Balanced** | .com, GitHub, X/Twitter, npm/PyPI | All others |

**Scoring presets** — each context uses different intrinsic/extrinsic dimension weights AND a different intrinsic/extrinsic split ratio. See `references/scoring-rubric.md` § Context Presets for the full weight tables. Key differences:

- **CLI Tool**: 30/70 intrinsic/extrinsic split — typeability (30%) and registry (35%) dominate extrinsic
- **Brand**: 50/50 split — phonetics (30%) and domain (35%) are top priorities
- **Side Project**: 25/75 split — availability-first; typeability (40%) and registry (20%) lead extrinsic

Present the classification and preset to the user. User can override with `--style` or adjust weights manually.

## Core Workflow (6 Phases)

### Phase -1: Memory Load (runs once per session)

`!uv run python skills/namer/scripts/memory.py load`

If memory exists, integrate into session:

- **Archetype affinities** → bias Phase 1 generation distribution (e.g., 35% evocative if user favors it)
- **Phonetic likes/dislikes** → add to Phase 1 hard filters (dislikes) and soft scoring boosts (likes)
- **Length preferences** → adjust length constraints in Phase 1
- **Weight overrides** → pre-fill Phase 3 scoring weights
- **Context defaults** → suggest context in Phase 0 Brief ("Last time you named a CLI tool — same context?")
- **Inspirations** → reference in Phase 1 generation as stylistic anchors
- **Past selections** → avoid regenerating names the user already picked

If no memory exists, proceed normally. Memory is additive — never block a phase on missing memory.

### Phase 0: Brief (sequential, interactive)

1. Parse what's being named, context, constraints
2. Auto-classify naming context → select preset
3. Present classification + adjusted weights to user
4. Accept overrides: `--style`, `--thorough`, manual weight adjustment
5. Accept inspirations: "I like names like Vercel, Stripe, Neon"

### Phase 1: Generate & Filter (inline, single-pass)

Load `references/naming-strategies.md` for archetype details and sound symbolism guide.

Generate 40-60 candidates across **6 naming archetypes**:

| Archetype | Description | Examples |
|-----------|-------------|----------|
| Invented words | Phonetically constructed neologisms | Kodak, Xerox, Hulu, Roku |
| Metaphorical transfers | Concepts from other domains | Amazon, Safari, Slack, Rust |
| Compound blends | Portmanteaus, morpheme combos | Instagram, Pinterest, YouTube |
| Classical roots | Latin, Greek, Sanskrit etymology | Nike, Astra, Veritas, Lumen |
| Evocative fragments | Short, punchy, abstract feel | Figma, Sumo, Neon, Zed |
| Descriptive-creative | Clear meaning with flair | Cloudflare, Datadog, Fastly |

**Hard filters** (binary pass/fail, run BEFORE availability checking):

Run `!uv run python skills/namer/scripts/generate.py filter --input candidates.json` for automated filters, then apply AI-only filters inline:

1. Profanity/vulgarity in English (script: `generate.py filter`)
2. Offensive meaning in top 10 world languages (AI-only: use `brave_web_search`)
3. Exact collision with top-1000 brand in same category (AI-only: use `brave_web_search`)
4. Exceeds length limit (15 chars product, 8 chars CLI, 12 chars library) (script: `generate.py filter`)
5. Unpronounceable consonant clusters (script: `generate.py filter`)
6. Reserved word in major programming languages (script: `generate.py filter`)
7. Contains hyphens/special chars (for package names) (script: `generate.py filter`)

Score **intrinsic dimensions** (phonetics, semantics, memorability, morphological flexibility, visual quality). Use `!uv run python skills/namer/scripts/generate.py analyze <name>` for phonetic breakdown to inform phonetic quality scoring. Select **top 20-25** for availability checking.

`--thorough` mode: Run multiple generation passes with varied prompting for more diversity.

### Phase 2: Availability Sweep (parallel subagents)

Load `references/platform-checks.md` for per-platform check methods.

Dispatch **4 parallel subagents**, each checking ALL candidates in its category:

**Subagent A — Domain Checker:**
- .com/.net via RDAP: `GET https://rdap.verisign.com/com/v1/domain/{name}.com` → 404 = available
- .dev/.io/.ai/.app via brave_web_search
- Pricing: brave_web_search for top 5 candidates

**Subagent B — Dev Registry Checker (Direct API):**
- GitHub: `GET https://api.github.com/users/{name}` → 404 = available
- npm: `GET https://registry.npmjs.org/{name}` → 404 = available
- PyPI: `GET https://pypi.org/pypi/{name}/json` → 404 = available
- Crates: `GET https://crates.io/api/v1/crates/{name}` → 404 = available

**Subagent C — Social & Handle Checker:**
- Reddit: `GET https://www.reddit.com/api/username_available.json?user={name}`
- Bluesky: AT Protocol handle resolution
- X/Twitter, YouTube, Instagram, LinkedIn: brave_web_search with `site:` prefix

**Subagent D — Conflict & Distinctiveness:**
- Search collision volume: `brave_web_search '"{name}" software'`
- Trademark (--thorough): `brave_web_search "USPTO TESS {name}"`

Or run deterministic checks via script:
`!uv run python skills/namer/scripts/check.py check-all candidate1 candidate2 ...`

**Scaling:**
- ≤10 candidates: 4 parallel subagents
- 11-25 candidates: Pre-filter with quick .com RDAP, full check top 10-15
- `--thorough`: All social + trademark + Wikipedia checks

### Phase 2.5: Variant Generation (conditional)

For top 5 intrinsic-scored candidates that FAILED availability:
- Generate 3-5 variants each: prefix (`go-`, `un-`), suffix (`-kit`, `-lab`, `-ify`), vowel dropping (`namr`), respelling (`nomer`), scoped (`@scope/name`)
- Run availability checks on variants (same subagent pattern, smaller batch)

### Phase 3: Score & Rank (inline)

Load `references/scoring-rubric.md` for detailed criteria.

**10 scoring dimensions** (0-10 scale, context-weighted):

| Dimension | Method |
|-----------|--------|
| Domain availability | .com=10, .dev/.io=7, .ai/.app=5, parked=3, none=0 |
| Registry availability | % of target registries available |
| Handle consistency | % of target social platforms available |
| Memorability | Length bonus + syllable count + imagery |
| Phonetic quality | Consonant/vowel flow, stress, sound symbolism |
| Semantic fit | Domain relevance, emotional tone, metaphor richness |
| Typeability | Character count, keyboard locality, no specials |
| Search distinctiveness | Inverse of search result count |
| Morphological flexibility | Can verb/noun/compound? Product family support? |
| Visual quality | Letter balance, ascenders/descenders, URL aesthetics |

**Composite**: `(0.4 × intrinsic_avg) + (0.6 × extrinsic_avg)` — user can adjust split.

Run `!uv run python skills/namer/scripts/score.py score --input candidates.json` for deterministic scoring. Input JSON must have `{"candidates": [{"name": "...", "intrinsic": {...}, "availability": {...}}], "preset": "cli-tool"}`.

### Phase 4: Present (inline)

Load `references/output-formats.md` for templates.

**Three ranked views:**

1. **Best Names** — ranked by intrinsic quality (availability shown but not factored)
2. **Best Available** — ranked by composite score (default recommendation)
3. **Best with Variants** — top intrinsic names with available modifications

Each view: ranked table with availability matrix (✅ ❌ ⚠️ ❓), scores, rationale.

**Detailed cards** for top 3 per view: full scoring breakdown, strengths, risks, next steps.

**Actionable next steps**: "Register neon.dev at $12/yr", "Claim @neon on GitHub", "`npm init neon`"

**Interactive refinement**: "more like #3", "shorter", "more technical", "avoid X sounds"

**Dashboard**: After all views and cards are produced, assemble the full session into the JSON schema from `references/output-formats.md § Structured Output Schema`. Read `templates/dashboard.html`, replace `{}` in `<script id="data" type="application/json">{}</script>` with the JSON, and write the result to `~/.claude/namer/{session-slug}-dashboard.html`. Print the open command: `open ~/.claude/namer/{slug}-dashboard.html`

### Save Session

Save to `~/.claude/namer/{YYYY-MM-DD}-{context}-{slug}.md` with YAML frontmatter after Phase 1 (candidates), Phase 2 (availability), Phase 4 (ranking). Supports resume.

## Memory Save Triggers

Save memories at natural decision points. NEVER slow down a phase for a memory write — always save AFTER delivering primary output.

| Trigger | Command |
|---------|---------|
| Phase 0: User states style preference | `memory.py save-preference --type vibe --value "..."` |
| Phase 0: User cites inspiration names | `memory.py save-inspiration --name "..." --context "..."` |
| Phase 0: User adjusts weights | `memory.py save-weights --intrinsic-split F --extrinsic-split F` |
| Phase 1: User says "avoid X sounds" | `memory.py save-rejection --pattern "X" --type phonetic --reason "..."` |
| Phase 4: User selects a name | `memory.py save-selection --name "..." --archetype "..." --context "..." --score N --query "..."` |
| Refinement: "more like #N" | `memory.py save-preference --type archetype --value "..." --like` |
| Refinement: "shorter" / "longer" | `memory.py save-preference --type length --value "max=5"` or `"min=8"` |
| Any: User rejects a style | `memory.py save-rejection --pattern "..." --type archetype --reason "..."` |

Batch multiple saves in a SINGLE message when a session produces several memories. All `memory.py` commands are prefixed with `!uv run python skills/namer/scripts/`.

## Canonical Vocabulary

| Term | Definition |
|------|-----------|
| **brief** | Naming requirements: what, context, style, constraints |
| **candidate** | A generated name before availability checking |
| **archetype** | Naming strategy: invented, metaphorical, compound, classical, evocative, descriptive |
| **intrinsic score** | Quality from linguistic/creative dimensions (no I/O) |
| **extrinsic score** | Availability from platform checks (I/O intensive) |
| **composite score** | Weighted combination of intrinsic + extrinsic |
| **hard filter** | Binary pass/fail gate: profanity, length, pronounceability |
| **variant** | Modification of a candidate: prefix, suffix, respelling |
| **namespace report** | Per-candidate availability matrix across all platforms |
| **context preset** | Auto-configured weights + platforms for what's being named |
| **memory** | Persistent naming preferences at `~/.claude/namer/memory.json` |
| **archetype affinity** | Weighted distribution of user's preferred naming archetypes, computed from selections |
| **selection** | A name the user chose as their winner, stored for preference learning |
| **rejection** | An explicitly unwanted pattern (phonetic, archetype, or specific name) |

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/naming-strategies.md` | 6 archetypes, sound symbolism, phonetic guide, morpheme library | Phase 1 (generation) |
| `references/platform-checks.md` | Per-platform: URLs, methods, response parsing, rate limits | Phase 2 (availability) |
| `references/scoring-rubric.md` | 10 dimensions detailed, 6 presets, hard filters, composite formula | Phase 3 (scoring) |
| `references/output-formats.md` | Templates for 3 views, name cards, variant tables, next-steps | Phase 4 (presentation) |
| `templates/dashboard.html` | Self-contained GUI — inject structured JSON from § Structured Output Schema | Phase 4 (dashboard render) |
| `scripts/memory.py` | CLI for persistent naming preferences (load, save, prune, stats) | Phase -1 (load), end of session (save) |

Load ONE reference at a time per the "Read When" column.

## Critical Rules

1. Never skip availability checking — unchecked names are worthless recommendations
2. Always present scoring rubric transparently — no black-box rankings
3. Never fabricate availability data — if a check fails, mark "❓ unknown", never "✅ available"
4. Always run hard filters before availability checks — don't waste API calls on disqualified names
5. Maximum 25 candidates through full availability pipeline — budget tool calls
6. Always surface trademark/conflict risks — legal issues trump name quality
7. Never modify user files — namer is read-only except session journals in `~/.claude/namer/`
8. Always produce all three output views — Best Names, Best Available, Best with Variants
9. Always provide actionable next steps — "register X at Y for $Z" not just "X is available"
10. Generation must use multiple archetypes — never produce candidates from only one strategy
11. Context classification before generation — weights and platforms depend on it
12. Intrinsic and extrinsic scores shown separately — user needs to see the trade-off
13. Load user memory before Phase 0 (Phase -1). Save memories AFTER delivering primary output — never block a phase for a memory write
