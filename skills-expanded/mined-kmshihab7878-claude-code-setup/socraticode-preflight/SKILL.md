---
name: socraticode-preflight
description: Run SocratiCode-assisted exploration before broad Read/Grep on a non-trivial code task. Falls back gracefully to code-review-graph MCP when SocratiCode isn't installed. Used implicitly by /ship, /audit-deep, /fix-root, /review.
disable-model-invocation: false
---

# socraticode-preflight — Code-aware exploration first

> Optional preflight that swaps blind grep/Read for AST-aware search before any non-trivial code work. When SocratiCode isn't installed, falls back to `code-review-graph` MCP (already live). When neither is available, falls back to native tools.

## When to use
- Before `/ship` on any change > 1 file
- Before `/audit-deep` on any module
- Before `/fix-root` on any bug whose call-path isn't obvious
- Before any refactor that crosses file boundaries

## When NOT to use
- Single-file edits with known scope
- Doc-only changes
- Quick "what does X do" lookups in a known file

## Preflight algorithm

1. **Detect tooling** (in this order):
   - SocratiCode CLI present? `which socraticode` → use it
   - `code-review-graph` MCP responding? → use `query_graph_tool`, `get_impact_radius_tool`, `semantic_search_nodes_tool`
   - Neither → fall back to `Grep` + `Read` and document the fallback in the calling skill's output

2. **Establish what changes / what's being investigated:**
   - Files touched (from git status, or explicit user input)
   - Symbols / functions involved
   - Domain area in `domains/` if classified

3. **Run the preflight queries** (whichever tool is available):
   - **Search** for prior implementations of similar patterns
   - **Graph / dependency** — what depends on the touched files
   - **Impact** — blast radius of the proposed change
   - **Call-flow** — for bugs only, trace from symptom backwards

4. **Surface results** to the calling skill in a compact form:
   ```
   Touch points: <files>
   Direct dependents: <count>
   Indirect dependents (depth 2): <count>
   Likely impact zones: <areas>
   Similar patterns elsewhere: <list>
   ```

5. **Recommend** — proceed / split / abandon — based on impact size:
   - Impact < 5 files → proceed
   - Impact 5-20 files → recommend splitting
   - Impact 20+ files → recommend abandoning and reframing

## Inputs
- Files / symbols / area to analyse
- (Optional) the change description

## Outputs
- Compact preflight summary (above)
- Recommendation
- Tool used (so the caller can document the fallback)

## Hard rules
- **MUST detect tooling before assuming** SocratiCode exists
- **MUST NOT block** if all three tools are absent — return a "no preflight available" verdict and let the caller decide
- **MUST log** which tool was used in the calling skill's output

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| SocratiCode times out on first run | Indexing the repo for the first time | Patience — subsequent runs are fast |
| `code-review-graph` returns stale results | Index out of date | Run `mcp__code-review-graph__build_or_update_graph_tool` |
| Preflight says "20+ impacted files" but caller proceeds anyway | Tool is advisory; operator overrode | Log the override; flag in next `/audit` if it happens repeatedly |

## Reference files
- `docs/SOCRATICODE.md` — install + protocol
- CLAUDE.md § Active MCP Servers — what's live now
- `code-review-graph` MCP server instructions (loaded as MCP server context at session start)

## Improvement loop
After each preflight:
1. Did the recommendation match what the operator did? If override → log
2. Did the implementation hit unexpected files? If yes → impact analysis underestimated; tune
3. Was the preflight slower than the work it saved? If yes → skip preflight for this task class in future
