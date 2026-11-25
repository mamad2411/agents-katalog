---
name: gitnexus-repo-map
description: >-
  Use GitNexus as a lightweight repo-exploration tool to read unfamiliar codebases, generate architecture/module/dependency maps, and inspect functional clusters. Treat GitNexus as a hand-held knife, NOT a harness subsystem — never run `gitnexus setup` automatically, never register Claude Code hooks, never modify global `~/.claude/`, and never promote `.claude/skills/generated/` into the canonical manifest. CLI-first; web UI is opt-in. Trigger phrases include: "GitNexus / repo map / visual code graph / architecture topology / read this open-source repo / 仓库架构 / 代码拓扑 / 模块地图 / clusters / 读开源项目".
---

# gitnexus-repo-map

> Supporting utility skill (Layer 11 Meta · "Code Reading Tools" pair with `codegraph-cli`).
> Wraps the GitNexus CLI (`npm i -g gitnexus` · npm `gitnexus`) so the harness can use it for **repo-level visual mapping and architectural reading** without letting GitNexus take over the orchestrator stack.
> Upstream: <https://github.com/abhigyanpatwari/GitNexus> · License: PolyForm Noncommercial (read the LICENSE before any commercial use).

## 1. Purpose

GitNexus indexes a repository into a knowledge graph (LadybugDB) and exposes:

- A web UI graph explorer
- An MCP server with tools like `query / context / impact / detect_changes / cypher / rename`
- An HTTP `serve` backend
- Per-area generated agent skills under `.claude/skills/generated/`

This skill uses **only the parts that act as a repo-exploration tool**:

- `gitnexus analyze` (indexing)
- `gitnexus serve` (local web UI backend, opt-in)
- `gitnexus list / status / clean` (registry inspection)
- `gitnexus wiki` (LLM-generated docs from the graph, opt-in)

It does **not** wire GitNexus into Claude Code's MCP layer, does **not** auto-install its agent skills into your global config, and does **not** register its Claude Code hooks. The harness already has its own orchestrators, hooks, agents, and SDKs (GSD / UIUX / QA / AppSec / L12); GitNexus stays a hand-held tool you summon when you want to *see* the repo.

## 2. Use this skill when

- The user asks to read or understand an **unfamiliar** repository.
- The user wants a **codebase map**, architecture graph, module map, dependency graph, or functional-cluster overview.
- The user wants to study an open-source project before adapting patterns into their own work.
- The user wants the **GitNexus web UI** for visual exploration.
- The user wants `gitnexus wiki` to LLM-generate documentation pages from the graph.

## 3. Do NOT use this skill when

- The task is a small single-file edit → use direct Read/Grep.
- The user only needs **callers / callees / impact / affected tests** for a local symbol → use [[codegraph-cli]] instead. CodeGraph is faster for local symbol traversal; GitNexus is heavier and optimized for global architecture.
- The user is doing normal project initialization → that is `claude-env-bootstrap`'s job.
- The user did not ask for repo exploration, visual mapping, or architectural reading.
- The repo is the user's own active product workspace and the question is "what should I build next" → that is the GSD / UIUX / QA / AppSec orchestrator's job, not a reading tool's.

## 4. Pre-flight check

Before running any `gitnexus` command:

```bash
# Is it installed?
gitnexus --version 2>/dev/null || echo "GitNexus not installed"
```

If it is **not** installed:

1. Tell the user it is not installed.
2. Offer the install command but do **not** run it without explicit user consent:
   - Standard: `npm install -g gitnexus`
   - Skip native parser build (faster, drops Dart/Proto/Swift): `GITNEXUS_SKIP_OPTIONAL_GRAMMARS=1 npm install -g gitnexus`
3. If the user is fine using `npx`, you may run `npx gitnexus@latest <command>` instead of installing globally, but warn them the first cold-start can take a while.

## 5. Commands (the curated surface)

### 5.1 Inspect first

```bash
gitnexus status                    # index status for current repo
gitnexus list                      # all repos GitNexus has indexed (~/.gitnexus/registry.json)
```

### 5.2 Index a repo (safe defaults for this skill)

```bash
# Standard indexing — does NOT call any LLM
gitnexus analyze --skip-embeddings           # faster default
gitnexus analyze --skip-embeddings --skip-agents-md   # also preserve any existing AGENTS.md/CLAUDE.md

# Full rebuild (re-parse + graph rebuild + FTS rebuild)
gitnexus analyze --force

# Fast path: rebuild only FTS indexes on existing index data
gitnexus analyze --repair-fts

# Verbose run when you suspect skipped files
gitnexus analyze --verbose --skip-embeddings
```

> `analyze` is the side-effect-heaviest command. It writes `.gitnexus/` in the repo, registers a pointer in `~/.gitnexus/registry.json`, and may rewrite `AGENTS.md` / `CLAUDE.md`. Always pass `--skip-agents-md` if you don't want it touching those files. Always pass `--skip-embeddings` unless the user explicitly wants embeddings (slower).

### 5.3 Generate repo-specific area skills (opt-in only)

```bash
gitnexus analyze --skills --skip-embeddings --skip-agents-md
```

Writes per-area `SKILL.md` files into `.claude/skills/generated/`. These are:

- **Project-local** and **disposable** — they live inside the project, not in `~/.claude/skills/`.
- **Not** added to `manifests/skills.manifest.json`.
- Regenerated on each `--skills` run.

Treat them as throwaway scaffolding, the same way you'd treat generated build output.

### 5.4 Web UI + HTTP backend (opt-in only)

```bash
gitnexus serve                     # starts local HTTP server (default port 4747)
# Then open https://gitnexus.vercel.app — the page auto-detects the local backend.
```

Stop the server (Ctrl-C) when you are done. Do not leave `serve` running as a daemon under the harness.

### 5.5 Cleanup

```bash
gitnexus clean                     # delete index for current repo
gitnexus clean --all --force       # delete every indexed repo (destructive — confirm with user first)
```

### 5.6 Wiki generation (requires LLM key)

```bash
gitnexus wiki                      # uses OPENAI_API_KEY by default
gitnexus wiki --model gpt-4o
gitnexus wiki --base-url https://api.anthropic.com/v1
gitnexus wiki --lang chinese
```

Wiki is an opt-in capability — only suggest it when the user explicitly asks for repo-level LLM documentation, and confirm they're OK spending API tokens.

## 6. Hard safety rules (do not violate)

1. **Never run `gitnexus setup` automatically.** It writes editor MCP configs (`~/.cursor/mcp.json`, `~/.codex/config.toml`, Claude Code MCP via `claude mcp add gitnexus`, etc.). The harness has its own integration model; auto-running `setup` couples GitNexus to every project Claude touches.
2. **Never auto-modify `~/.claude/`.** Do not call any GitNexus command that mutates files outside the current project unless the user has explicitly asked.
3. **Never register GitNexus's Claude Code hooks automatically.** GitNexus's PreToolUse/PostToolUse hooks enrich searches with graph context and re-trigger indexing — they're useful but they belong under user-initiated `gitnexus setup`, not under this skill.
4. **Never claim GitNexus is the harness's source of truth.** It is a *reading* tool. Decisions, gates, evidence, and orchestration stay with GSD / UIUX / QA / AppSec / L12.
5. **Treat `.gitnexus/` (per-repo) and `~/.gitnexus/` (registry) as tool caches.** Do not promote them into harness evidence roots (`.appsec/evidence/<tag>/` / `.qa/evidence/<tag>/` / `evidence/discoverability/<tag>/` / `.planning/`).
6. **Treat `.claude/skills/generated/` as project-local generated context.** Do not copy it into `~/.claude/skills/`. Do not add its skill names to `~/.claude/manifests/skills.manifest.json`.
7. **Always pass `--skip-agents-md` when the project already has a managed `AGENTS.md` / `CLAUDE.md`.** Otherwise GitNexus may overwrite or append into them.
8. **License awareness.** GitNexus OSS is licensed under **PolyForm Noncommercial 1.0.0**. Before suggesting it for any commercial deliverable, point the user at <https://akonlabs.com> for commercial licensing.

## 7. Handoff matrix

GitNexus is a context tool. It does not own decisions. After a `gitnexus analyze`, hand back to:

| Downstream | When to hand off |
|---|---|
| [[codegraph-cli]] | User now wants local symbol-level callers / callees / impact / affected tests on a known function. CodeGraph is leaner for this. |
| `gsd-pipeline-orchestrator` | User now wants to plan / execute concrete work in the repo. |
| `uiux-product-orchestrator` | User now wants to design / refactor UI in the repo. |
| `enterprise-qa-testing` | User now wants to set up the test matrix for the repo. |
| `appsec-security-orchestrator` | User now wants threat modeling / SAST / supply-chain review for the repo. |
| `discoverability-orchestrator` | User now wants SEO/AEO/Local-SEO/ASO on the public surfaces of the repo. |

Pass forward as **supporting context only**:

> "GitNexus indexed N files / M symbols / K processes. The architecture clusters are A / B / C, entry points are X / Y. Use this as background; the harness still owns decisions."

## 8. Two-line decision card (for when you're routing in a hurry)

- **"I want to see this repo"** → `gitnexus-repo-map`
- **"I want to know who calls this function"** → `codegraph-cli`

## 9. Anti-patterns (will silently break the harness)

- ❌ Running `gitnexus setup` from this skill — couples Claude Code MCP layer to GitNexus globally.
- ❌ Letting `gitnexus analyze` rewrite the project's `AGENTS.md` / `CLAUDE.md` without warning (use `--skip-agents-md`).
- ❌ Treating `.claude/skills/generated/<area>/SKILL.md` as canonical and adding it to `~/.claude/manifests/skills.manifest.json`.
- ❌ Citing GitNexus output as the final word on architecture without sanity-checking against the actual code — graph extraction has gaps (especially around dynamic dispatch, reflection, runtime composition).
- ❌ Using GitNexus to answer "what should I change?" — it answers "what is there?".
- ❌ Quoting GitNexus's `impact` / `detect_changes` numbers as a release gate. Release gates live in GSD / QA / AppSec / L12, not in a code-reading tool.

## 10. Maintenance

- Tool updates → only touch this file and (optionally) the version note in `~/.claude/SKILLS-INDEX.md`. Do not propagate GitNexus internals deeper into the harness.
- If GitNexus rename / deprecate a command upstream, update §5 and §7. Do not preserve dead aliases.
- If the user wants the full MCP integration, that is a deliberate decision they make outside this skill — point them at the official `gitnexus setup` flow and document it in their project's CLAUDE.md, not in `~/.claude/`.
