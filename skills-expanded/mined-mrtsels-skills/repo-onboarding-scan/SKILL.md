---
name: repo-onboarding-scan
description: Use when scanning a repo, or identifying/reconning a GitHub repo remotely before development.
metadata:
  imported_from: hermes
---

# Repo Onboarding Scan

Trigger: user says "扫描仓库 / 为继续开发做好准备 / scan the repo / onboard", or asks what a GitHub repo/URL is ("what is X", "does it exist", "what's its CLI") before any checkout. Prepare an unfamiliar repository for continued development. The deliverable is a **verified** state report: architecture map, working environment, and development hazards — every claim backed by an actual read or executed command. No filename-based inference (user has zero tolerance for fabrication: read the file, run the command, cite `path:line`).

## Steps (in order)

### 0. Remote recon first — no checkout yet? Identify before you scan
When the repo is only a URL (or a guessed URL) and may not exist — or you need its metadata/CLI surface before cloning — follow `references/remote-repo-recon.md`: existence check → 404 shorthand detection → `default_branch` → README/file-tree via API → CLI-package discovery in monorepos. Key rule: fetch `default_branch` from repo metadata before ANY `raw.githubusercontent.com` or `git/trees` call (not always `main` — DeepSeek Harness uses `master`).

### 1. Git state first — the workspace snapshot may be stale
```bash
git status && git branch -vv && git log --oneline -10
```
Note untracked files, branch vs origin, and recent commit themes (they tell you what the team is actively fixing — e.g. a `fix(...)` series points at known-buggy areas). Never commit/push anything during a scan (user rule: only `git add` specific paths, never `add .`/`-A`).

### 2. Batch independent reads in ONE turn
- Manifest: `pyproject.toml` / `requirements.txt` / `package.json` / `Cargo.toml` — entry point scripts (`[project.scripts]`), Python version floor
- `README.md` (usage + architecture claims), `.env.example` (which API keys are needed), `main.py`/entry module
- `AGENTS.md` / `CLAUDE.md` / `.cursorrules` — if present they override your defaults
- Then map the package: for each subpackage read the `__init__.py` (exports = public surface), the orchestrator module (e.g. `graph/trading_graph.py`), and one representative leaf module per layer (agent factory, data adapter, client wrapper). Read a leaf to learn the pattern, don't read all leaves.

### 3. Check environment state — never assume deps are installed
```bash
conda env list; ls -d .venv venv 2>/dev/null; which uv; uv --version
python3 -c "import <core_pkg>" 2>&1 | tail -3
```
Distinguish: "repo uses uv (uv.lock)" vs "deps actually installed". `import` succeeding at package level does NOT mean the full import chain works — test the heavy module too.

### 4. Set up env in background while you finish scanning
```bash
uv sync   # background=true, notify_on_complete=true
```
Keep reading source while it installs. uv-managed projects: `.venv/bin/python` is the interpreter for all later verification.

### 5. Verification ladder (each rung verified before moving on)
```bash
.venv/bin/python -c "from <pkg>.core import MainClass; print('imports OK')"
# Instantiate the main object — but see pitfall: LLM clients validate at __init__
OPENAI_API_KEY=sk-dummy .venv/bin/python -c "..."   # compile-only smoke test
```
- Full graph/object instantiation, then a **subset configuration** (fewer components) to prove configurability works
- Data-layer smoke test with a real call (e.g. yfinance needs no key): `get_stock_data('AAPL', ...)` — verify output shape, not just no-exception
- Print `len(nodes)` / component counts in the test so the numbers appear in your report

### 6. Hazard scan — the highest-value findings
- **Dead config**: grep each `DEFAULT_CONFIG`/settings key, then check the constructor call sites. Classic bug: key defined + documented, but component instantiated with no args so the config never takes effect. Verify with grep: `grep -rn "KeyName\|ClassName(" <pkg>`
- **TODO/FIXME files**: e.g. `llm_clients/TODO.md` — read them, the maintainers' own list
- **Recent fix commits**: `git show --stat <fix_commit>` shows which file/data source was wrong — check sibling call paths for the same flaw
- **Public exposure audit**: check `git ls-files` for files that shouldn't ship in a public repo. See `references/public-exposure-checklist.md` for the full taxonomy. Quick triage: `git ls-files` then scan for `.map` files, build scripts, generated output, debug reports, and `package.json` export paths that leak source. Always cross-check `package.json` `exports`/`files` fields vs what's tracked — gaps mean either leaks or dead config.
- **UI screenshot for README**: when the user asks for screenshots, render the **bare elements only** on a white background — no dark theme, no mock chrome, no annotations, no composer-card wrappers. Crop tightly to content. One HTML file per element type, screenshot each separately. Over-engineering this (full demo pages with themes and labels) will get corrected. See `references/chip-screenshot-template.html` for the pattern.
- Untracked junk (`.DS_Store`, caches): mention, don't clean without asking

### 7. Report
Lead with repo state + architecture map (1-2 lines per layer, pipeline order), then environment status (what's installed/verified), then numbered development hazards with `path:line` evidence. Separate **verified** facts from **suspected** issues. End by offering to fix the top hazard — don't fix during a scan unless asked.

## Pitfalls
- **LLM clients often validate env at `__init__`** (e.g. `ChatOpenAI` raises `OpenAIError: api_key client option must be set`). That's a missing-key error, NOT a code bug. Re-run with `OPENAI_API_KEY=sk-dummy` to test graph compilation; real runs still need the real key in `.env`.
- **Package-level import ≠ working import chain**: `import tradingagents` can succeed while `from tradingagents.graph.trading_graph import X` fails on missing `langgraph`. Test the deepest module you actually need.
- **Filename inference lies**: a module named `risk_manager.py` was recently fixed precisely because it pulled data from the wrong report. Read the body.
- **`wc -l` the tree** early (`git ls-files '*.py' | xargs wc -l | sort -rn | head -40`) to find where the weight is — the 1000-line file is usually the CLI/UI, and the 400-line file is usually the critical data path.
- **Config-wiring gaps hide silently**: `default_config.py` keys exist, README documents them, component constructors take no args → changes never apply. Always grep instantiation sites.
- **DI wrapper ≠ DI dependency (vendor libs)**: Upstream classes wrapped in DI plugins (e.g., Cordis `apply(ctx)`) may be fully standalone. Check the class source file, not the plugin wrapper — constructor without `Context` param = standalone. See `references/dsh-dedup-migration-feasibility.md` for the analysis technique.

## Verification
- [ ] `uv sync` exited 0 and `.venv/bin/python` exists
- [ ] Deep import chain works
- [ ] Main object instantiates (dummy key if needed) with expected node/component count
- [ ] Subset configuration also works
- [ ] Data-layer call returns real data
- [ ] Every hazard in the report has `path:line` evidence

## Per-repo maps
- `references/trading-agents.md` — TradingAgents framework map (graph pipeline, config wiring, known gaps)
- `references/remote-repo-recon.md` — identify/recon a GitHub repo remotely without cloning (404 shorthand detection, default_branch, monorepo CLI discovery)
- `references/dsh-for-vscode-vendor-architecture.md` — dsh-for-vs-code vendor workspace structure, import access strategies, and upstream type compatibility table for wire.ts alignment
- `references/dsh-dedup-migration-feasibility.md` — D2/D3 migration feasibility: DI-free analysis technique, WebApiClient/ConnectionController standalone construction, baseUrl adaptation, wrapper patterns for feature gaps
