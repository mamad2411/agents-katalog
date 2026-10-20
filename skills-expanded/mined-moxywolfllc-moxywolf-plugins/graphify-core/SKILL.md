---
name: graphify-core
description: >
  This skill should be used when the user asks to "graphify this", "build a
  knowledge graph of <directory|database|corpus>", "graph this codebase",
  "show me the god nodes", "map the communities in this code", "graph my
  Supabase schema", or when another plugin (notably github-repo-analyzer's
  Step 0) needs a graphify graph generated over a prepared corpus. It is the
  canonical MoxyWolf graphify runner protocol: corpus directory in,
  LLM-named-community knowledge graph out. It does NOT build corpora itself —
  the /graphify and /graphify-supabase commands (and other plugins) prepare
  the corpus and hand it here.
version: 0.1.0
---

# Graphify Core — the canonical runner protocol

[graphify](https://github.com/safishamsi/graphify) (the pinned MoxyWolf tool — see `MoxyWolf Vault/_Shared Knowledge/Tech Stack/tool-graphify-knowledge-graph.md`) builds a code knowledge graph: **god nodes** (most-connected core abstractions), **communities** (module clusters), **import cycles**, and **isolated/weakly-connected nodes**.

This skill is the **single source of truth** for running graphify at MoxyWolf. Other plugins (github-repo-analyzer Step 0, the corpus adapter commands in this plugin) must invoke this protocol rather than carrying their own copy. If the protocol changes, it changes here.

## Contract

- **Input:** a prepared corpus directory (`<code-scope>`) containing only code-like files. Corpus construction is the caller's job — see *Corpus rules* below.
- **Output:** `<code-scope>/graphify-out/` containing `graph.json`, `GRAPH_REPORT.md`, and `graph.html`, with **real LLM-named communities** (not `Community N`).
- **Modes:** keyed (default, mandatory when the team key resolves) or keyless code-only fallback (`--keyless` request, or when the key genuinely cannot be loaded).

## Corpus rules (callers must obey these)

- Include only code extensions: `.ts .tsx .js .mjs .py .go .rs .java .c .cpp .rb .cs .kt .php .prisma .sql`. Exclude `node_modules`, `.next`, `dist`, `.git`, build output.
- **Strip `.md`/`.mdx`/images from the Pass-A corpus** — `graphify extract` refuses a mixed corpus when no LLM key is set ("a code-only corpus needs no key"), and docs belong only in the optional keyed Pass C.
- Copy the **whole** relevant tree, not a subset — on a monorepo include both `apps/*` and `packages/*`. Partial corpora produce misleading god nodes.

### Docs-first corpora (Obsidian vaults, paper sets, knowledge bases)

When the corpus is mostly or entirely markdown — an Obsidian vault is the canonical case — the two-pass code flow above does not apply: **docs require the LLM, so the keyed `extract --backend openrouter` IS the primary pass and there is no keyless fallback.** Run it over the docs corpus directly, iterating within the sandbox time box (semantic chunks cache across calls, so repeated invocations make progress where a code AST pass would restart). Then `cluster-only` + `label` as usual. Exclude template and archive folders (`_Templates/`, `99 – Archive/`, `.obsidian/`) via a `.graphifyignore` in the corpus root — same syntax as `.gitignore`.

**Mandatory docs-corpus extraction defaults (proven 2026-06-11; without them extraction collapses to one node per file):**

- `--mode deep --token-budget 4000` — the default 60k budget puts the whole corpus in one chunk and yields file-level summary nodes, not concepts. **The small chunk budget is the load-bearing fix** (A/B-verified 2026-06-11: `gpt-4o-mini` at 4000 produced 26 concept nodes where the same model at 60k produced 9 file nodes). The provider-default `gpt-4o-mini` is fine; escalate `GRAPHIFY_OPENROUTER_MODEL` to a stronger model only if concepts still come back shallow.
- **Cache trap:** the semantic cache is keyed by file content, not extraction settings — after changing `--mode`, model, or budget, `rm -rf <corpus>/graphify-out` first, or the re-run silently returns the stale shallow graph (`semantic cache: N hit / 0 miss`).
- **Large corpora must run host-side** (Desktop Commander), not in the sandbox: the cache does not persist across the sandbox's ~45s per-command kills, so a multi-hundred-chunk extraction restarts forever (observed: 9 sandbox attempts, 1 cache file). Host-side install via `uv tool install "graphifyy[openai]"`; a 593-doc vault (273 chunks, `--max-concurrency 16`) completed in ~6 minutes.
- **Community assignments live in `graph.html`**, not `graph.json` — after `label`, parse the embedded vis.js node array (`community`, `community_name` fields) when generating exports.
- **Scale the Obsidian export to the corpus**: per-node notes for everything is wrong at thousands of nodes (it floods the vault and Drive sync). Default tiering — index + one page per community with 3+ members + individual notes only for hub nodes (degree ≥ 4); leaf nodes are listed as plain text on their community page.

## The protocol

1. **Ensure the CLI + OpenAI-compat client** (idempotent): `pip install graphifyy openai --break-system-packages -q`. The PyPI package is `graphifyy`; the CLI is `graphify`, installed to `~/.local/bin` — add it to `PATH`. **`openai` is required** — the team OpenRouter backend goes through graphify's OpenAI-compatible client, and the keyed pass silently fails its semantic/label chunks without it (the error is `the 'openai' package is required for this backend`).
2. **Resolve the LLM key + register OpenRouter as a graphify backend (keyed pass is mandatory).** graphify does **not** read `OPENROUTER_API_KEY` natively and has **no built-in OpenRouter backend**, but OpenRouter is OpenAI-compatible, so register it as a custom provider:
   - Load the team key (value never printed) from the canonical DR-010 path: `set -a; . "$VAULT/_Shared Knowledge/Agents and Plugins/openrouter.env"; set +a` where `$VAULT` is the mounted MoxyWolf Vault. The env-var path wins if `OPENROUTER_API_KEY` is already exported.
   - Write `~/.graphify/providers.json` once:
     ```json
     {"openrouter": {"base_url": "https://openrouter.ai/api/v1", "default_model": "openai/gpt-4o-mini", "model_env_key": "GRAPHIFY_OPENROUTER_MODEL", "env_key": "OPENROUTER_API_KEY", "pricing": {"input": 0.15, "output": 0.60}, "temperature": 0, "max_tokens": 16384, "vision": true}}
     ```
   - All keyed graphify commands then take `--backend openrouter`. (Native keys still work if present: `ANTHROPIC_API_KEY` → `--backend claude`, `GEMINI_API_KEY`/`GOOGLE_API_KEY` → `--backend gemini`, etc. Prefer whichever is available; OpenRouter is the always-available default for MoxyWolf.)
3. **Build the graph as TWO passes** (this is what survives the Cowork sandbox — a single full keyed `extract` over a large corpus exceeds the per-command timeout and does not checkpoint AST progress):
   - **Pass A — full-corpus AST graph (deterministic, fast, writes `graph.json`).** `graphify extract <code-scope> --no-cluster -o <code-scope>/graphify-out`.
   - **Pass B — cluster + LLM-name communities (the keyed payoff).** `graphify cluster-only <code-scope> --no-label` (Leiden, deterministic) to assign communities, then `graphify label <code-scope> --backend openrouter` to NAME them. `label` re-clusters + names + regenerates `GRAPH_REPORT.md` and `graph.html` in one call and is bounded by community count, so it fits the time box where a full `extract` does not. **Do not** run `cluster-only --no-label` *after* `label` — it wipes the names; `label` must be the last mutation.
   - **Optional Pass C — multimodal concept folding (best-effort).** To fold README/docs/diagrams in as concept nodes, run a keyed `graphify extract <corpus-with-docs> --backend openrouter` over a corpus that *includes* `.md`/`.mdx`; iterate within the time box (semantic chunks cache). Skip if it can't complete — Pass A+B already deliver the mandatory keyed, named-community graph.
4. **Confirm** `graphify-out/graph.json` exists and `GRAPH_REPORT.md` shows real community names (verify with `grep -v 'Community [0-9]' graphify-out/.graphify_labels.json`), then hand the output path back to the caller.

## Execution notes (failure modes seen in practice in the Cowork sandbox)

- **`openai` package is mandatory** for the OpenRouter backend. Without it, AST extraction succeeds but every semantic/label chunk fails silently and you get `Community N` placeholders.
- A **single full keyed `extract`** over a real corpus (hundreds of files) **exceeds the ~45s per-command sandbox limit** and its AST pass does not checkpoint across calls — it restarts each time and never reaches the LLM stage. The two-pass split is the working pattern.
- Community **naming** needs the LLM; AST extraction and Leiden **clustering do not**.
- Leiden over-fragments large graphs (hundreds of small communities on a big corpus). That's expected — lean on the **largest** named communities and the **god nodes** as the load-bearing signal, not the raw community count.
- The `anthropic` Python package is only needed for `--backend claude`; it is **not** needed for the OpenRouter/`openai`-compat default.
- graphify's signal is strong on **code-bearing corpora** (functions, classes, imports, data flow) and noticeably noisier on **markdown/config-heavy ones** (key fragments surface as isolated nodes and near-duplicate "metadata" communities). Weight accordingly when interpreting.

## Consuming the graph

Parse `graphify-out/graph.json` and read the signal, not the noise:

- **God nodes** → the core abstractions, with edge counts as evidence. On a database corpus these are your hub tables.
- **Communities** → module/domain decomposition. On a database corpus these are schema domains.
- **Import cycles** → technical-debt / circular-dependency evidence.
- **Isolated/weakly-connected nodes** → candidate dead code, orphan tables, or undocumented seams.

Cross-reference graph findings against the underlying files; where they disagree, trust the source and note the discrepancy.

## Export surfaces (post-Pass-B, optional)

Upstream graphify can re-render a finished graph in several formats. These run **after** Pass B (never between `cluster-only` and `label`):

- **Obsidian vault — generate from `graph.json` (primary path).** The headless CLI (verified at 0.8.37) has **no** `--obsidian` or `--wiki` flags — those exist only in the `/graphify` skill invocation. The working pattern is to generate the export directly from `graph.json` + `.graphify_labels.json`: one note per node (frontmatter: `type: graph-node`, `generated_by: graphify`, `derived_artifact: true`, `community: "<label>"`), a `## Connections` section of `[[wikilinks]]` from the edge list (relation-labeled, both directions), and an `index.md` listing communities with members sorted by degree. Filenames are sanitized node titles so wikilinks resolve. Copy `graph.json`, `GRAPH_REPORT.md`, and `graph.html` alongside (note: `graph.html` opens in a browser, not Obsidian).
- **Other** — `--svg`, `--graphml` (Gephi/yEd), `--neo4j` exist upstream as extract-time extras; use only on request.

**MoxyWolf vault routing convention** for Obsidian-format outputs:

- Per-project graphs (a repo, a database) → `MoxyWolf Vault/Projects/<project>/06-Engineering/graphs/<target>/`
- The vault-wide graph (corpus = the vault itself) → `MoxyWolf Vault/_Shared Knowledge/Vault Graph/`

Always land the export in its **own subfolder** so its generated `[[wikilinks]]` are filterable in Obsidian's graph view and don't blend into hand-written notes. Generated graph notes are derived artifacts — obsidian-update/memory extraction should not treat them as session knowledge.

**Cross-graph registry.** To combine graphs across targets (repo + database + vault), register each into upstream's global graph: `graphify global add <graphify-out>/graph.json <name>`, or merge explicitly with `graphify merge-graphs a.json b.json --out merged.json`.

## Graceful degradation

Never hard-fail the caller's task on graphify. If the keyed pass can't run, fall back to the keyless code-only graph (extract + cluster, unnamed communities). If no graph can be produced at all, report why and let the caller fall back to its own analysis (e.g. the repo-analyzer's plain tree walk).
