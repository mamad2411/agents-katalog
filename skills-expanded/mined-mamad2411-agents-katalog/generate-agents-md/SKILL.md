---
name: generate-agents-md
description: Generate a project-specific NeoHive topology block in ./AGENTS.md by surveying connected indexes (list_indexes + memory_stats + sampled memory_recall probes). Runs as Phase 3 of the getting-started skill, and is also invocable on its own for re-runs when indexes change. Use when the user says "generate my NeoHive AGENTS.md", "regenerate the topology", "re-survey my indexes", or after adding/removing/renaming indexes.
---

# Generate Project-Specific NeoHive AGENTS.md Block

You are surveying the user's connected NeoHive Indexes and writing a **project-specific** topology block into `./AGENTS.md`. This block tells the model — at session start, before `memory_context` is even called — which Indexes exist, what each one holds, and where new writes should land. Without this block, NeoHive tool calls run blind: the model has to guess which Index to query and where to route writes.

**Three non-negotiable rules:**

1. **Read-only until the user confirms the diff.** Cartography, synthesis, and the proposed table are all preview-only. Do NOT write `./AGENTS.md` until the user explicitly approves the diff.
2. **Marker-bounded writes only.** Generated content always lives between `<!-- BEGIN neohive-managed v=1 -->` and `<!-- END neohive-managed v=1 -->`. Never modify content outside the markers.
3. **Evidence-grounded synthesis.** Every column of the topology table must be traceable to `list_indexes`, `memory_stats`, or sampled `memory_recall` results. When inference is uncertain, mark the cell `(verify)` rather than guess confidently.

## Three internal stages

The skill runs as three stages. Stages B and C each have one user gate; Stage A is silent unless it errors.

- **Stage A — Cartography** — read-only data gathering against the NeoHive MCP.
- **Stage B — Synthesis** — produce a draft topology block; user reviews the table.
- **Stage C — Write** — show diff, user confirms, write to `./AGENTS.md`.

(Stage names use letters specifically to avoid collision with `getting-started`'s "Phase N" numbering, since this skill is invoked from there.)

## Stage A — Cartography (silent, no user input)

```
A.1  list_indexes                         → name, UUID, type, description per index
A.2  memory_stats                       → type-distribution per index (one call, all indexes)
A.3  for each index:
       probes = derive_probes(index.name, index.description)
       memory_recall(index=<uuid>, queries=probes, limit=10)
       → 5–10 sample memories per index
```

### Probe derivation

For each Index, generate 2–3 probe query strings:

1. Tokenize `name` and `description`. Drop stopwords and MCP boilerplate ("stores", "Index", "default", "main").
2. Combine remaining content words with intent suffixes: `"<token> convention"`, `"<token> directive"`, `"<token> example pattern"`.
3. If `description` is missing or generic, fall back to: `"convention"`, `"directive"`, `"insight"`, `"example pattern"`.
4. Cap probes at 3 per index.

### Stage A failure handling

| Failure                                      | Response                                                                                                                                                               |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `list_indexes` returns empty / errors        | Abort. Tell the user: "Cannot generate topology — no Indexes reachable. Confirm Phase 1 of the getting-started skill passed before re-running." Do NOT write anything. |
| `memory_stats` unavailable                   | Continue. Mark every Index's `Write to it?` cell `(verify)`. Surface a one-line warning at the Stage B review gate.                                                    |
| `memory_recall` returns nothing for an Index | Re-attempt with the generic fallback probes. If still empty, set `What it holds` to the Index's `description` verbatim and append `(no sampled memories)`.             |

## Stage B — Synthesis

Produce one row per Index with these columns:

| Column          | Source                                                 | Inference rule                                                                                                                                                                                                                                                                                                                                        |
| --------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Index (UUID)    | `list_indexes`                                         | verbatim                                                                                                                                                                                                                                                                                                                                              |
| Name            | `list_indexes`                                         | verbatim                                                                                                                                                                                                                                                                                                                                              |
| Type            | `list_indexes`                                         | verbatim                                                                                                                                                                                                                                                                                                                                              |
| Embedding model | `list_indexes.description` + heuristic                 | code-tuned (e.g. `jinaai/jina-embeddings-v2-base-code`) if Index is type `repo` or description mentions "code"/"indexed". Prose-tuned (e.g. `nomic-ai/nomic-embed-text-v1.5`) if type is `knowledge`/`markdown` or description mentions "prose"/"curated". When uncertain → `(verify)`.                                                               |
| What it holds   | sampled memories from A.3 + type-distribution from A.2 | 1–2 sentences grounded in real content. Cite the type composition (e.g., "Mostly `convention` and `insight` entries — curated knowledge").                                                                                                                                                                                                            |
| Write to it?    | type-distribution from A.2                             | Heavy `example_pattern` / `syntax_rule` / `stdlib_reference` → "**NO** — auto-managed; manual writes risk being overwritten by indexing." Mixed `convention` / `directive` / `insight` → "**YES** — default write target." Small + `directive`-heavy → "**RARELY** — only for durable, language-level conventions. Ask the user before writing here." |

### Default write target

Pick the Index with the largest write-safe (`YES`) memory count. Tie-break alphabetically by name. If no Index is write-safe, set the default to `<none — ask before any write>` and emit a warning row.

### Stage B review gate

Render the proposed table to the terminal as a markdown table (so the user can read it). Then ask the user:

> Topology table looks right?
>
> - **Looks good — proceed to write** (recommended)
> - **Edit a row** — name the row + column, accept free-text override, re-render and re-confirm
> - **Re-sample with different probes** — ask for probe terms, re-run A.3 only, re-synthesize
> - **Cancel** — exit cleanly, no file writes

`Cancel` → exit cleanly. No file writes.

## Stage C — Write

### Pre-write git safety check

If the target file is in a git worktree:

```bash
if git -C "$(dirname ./AGENTS.md)" rev-parse --is-inside-work-tree 2>/dev/null; then
  if [ -n "$(git status --porcelain -- ./AGENTS.md)" ]; then
    # warn + ask user to confirm or cancel
  fi
fi
```

Warning text: "`AGENTS.md` has uncommitted changes — recommend committing first so this skill's diff is easy to review separately. Continue?" Do not auto-commit. If `rev-parse` fails (not a git repo), skip the check silently.

### Write-behavior matrix

| Existing `./AGENTS.md` state                                   | Action                                                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| File absent                                                    | Create `./AGENTS.md` containing only the marker block.                                                 |
| File present with `<!-- BEGIN neohive-managed v=N -->` markers | Replace content between markers; preserve everything outside. Update `v=N` to current version (`v=1`). |
| File present without markers                                   | Append the marker block to end-of-file. Preserves user-authored content at the top.                    |

**v1 upgrade behavior:** any existing block, regardless of `v=`, is replaced wholesale. v1 does not implement format-aware migration.

### Diff-and-confirm gate

1. Compute proposed file content in memory.
2. Allocate temp file via `mktemp` in `$TMPDIR` (NOT in the project worktree). Register a cleanup trap so the temp file is removed on any exit path including SIGINT.
3. Run `diff -u AGENTS.md "$tmp"` (treat absent `AGENTS.md` as `/dev/null`); print the unified diff to terminal.
4. Ask the user:
    > Write this block to ./AGENTS.md?
    >
    > - **Write** (recommended)
    > - **Edit block first** — spawn `$EDITOR` on the temp file, re-show diff, re-confirm
    > - **Cancel** — cleanup trap fires, exit
5. `Write` → atomic `mv "$tmp" ./AGENTS.md`.

## Generated content template

Always wrap in markers. Use these substitution variables; fill them from Stage B output.

The Codex plugin has no plugin-level rules surface, so the generated block is **self-contained** — it inlines the session-start non-negotiables rather than referencing an external rule file.

```markdown
<!-- BEGIN neohive-managed v=1 -->
<!-- Generated by the generate-agents-md skill on {{DATE}}. Re-run to refresh. -->

## NeoHive Cognitive Memory — Project Topology

You have access to a persistent semantic memory system via MCP tools
(`list_indexes`, `memory_context`, `memory_recall`, `memory_store`,
`memory_forget`, `memory_stats`). This block is the **project-specific**
topology that tells you which index serves which query, and where new
writes should land.

### Index Topology

| Index (UUID) | Name | Type | Embedding model | What it holds | Write to it? |
| ------------ | ---- | ---- | --------------- | ------------- | ------------ |

{{ROWS}}

**Why query phrasing matters here.** {{QUERY_PHRASING_GUIDANCE}}

**Interpreting `[index: <uuid>]` in recall results.** {{HIVE_PROVENANCE_GUIDE}}

### Session Start — Non-Negotiable

1. **`memory_context` is your FIRST action in every session.** Call it with a brief
   description of the task before doing anything else — before reading files, before
   exploring code, before answering questions. Describe the task in **affirmative form
   with specific domain terms**, e.g. `"implementing authentication middleware for Express"`
   not `"what do we know about auth?"`.
2. **Call `list_indexes` once per session** to confirm the topology above has not changed.
   If an index is added / removed / renamed, re-run the `generate-agents-md` skill.
3. **Follow up with a targeted `memory_recall`** for this project's domain. Suggested seeds:
   {{DOMAIN_RECALL_SEEDS}}

### What Goes Where: Cognitive Memory vs AGENTS.md

| Store in **Cognitive Memory** | Store in **AGENTS.md** |
| ----------------------------- | ---------------------- |

{{ROUTING_TABLE}}

### Index routing for writes

Writes default to **{{DEFAULT_WRITE_HIVE}}** — {{DEFAULT_WRITE_RATIONALE}}.
**Do not pass an explicit `index` parameter to `memory_store` unless you have a
specific reason.** When you do, write one sentence in the memory body explaining why.

{{ADDITIONAL_WRITE_HIVES_DISAMBIGUATION}}

<!-- END neohive-managed v=1 -->
```

### Substitution variables

| Variable                                    | Format                                                                                                                                                                                                              |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{{DATE}}`                                  | `YYYY-MM-DD`                                                                                                                                                                                                        |
| `{{ROWS}}`                                  | One markdown table row per Index (Stage B output).                                                                                                                                                                  |
| `{{QUERY_PHRASING_GUIDANCE}}`               | One paragraph. Mention code-token queries iff any code-tuned Index is present; mention affirmative-statement queries iff any prose-tuned Index is present; recommend both styles via `queries` parameter when both. |
| `{{HIVE_PROVENANCE_GUIDE}}`                 | One paragraph. Per-index 1-liner mapping name → typical content profile (e.g., "a hit from `<name>` came from indexed code; treat as factual").                                                                     |
| `{{DOMAIN_RECALL_SEEDS}}`                   | 3–5 example query strings as a markdown bullet list, scoped to the project's domain (synthesized from sampled content).                                                                                             |
| `{{ROUTING_TABLE}}`                         | 2-column markdown table; row contents reference user's actual Index names. **N=1 case:** still emit both columns — the conceptual split is independent of Index count.                                              |
| `{{DEFAULT_WRITE_HIVE}}`                    | Index name in backticks.                                                                                                                                                                                            |
| `{{DEFAULT_WRITE_RATIONALE}}`               | One sentence; cite why this Index was chosen.                                                                                                                                                                       |
| `{{ADDITIONAL_WRITE_HIVES_DISAMBIGUATION}}` | Bulleted disambiguation rules; only emit when ≥2 Indexes are write-safe. Empty otherwise.                                                                                                                           |

## End-of-run summary

Print a single line:

```
generate-agents-md: 3 indexes mapped, default write target: Knowledge,
written to ./AGENTS.md (block lines 42-87, +35 lines vs previous version).
```

When replacing an existing block, additionally report **only changed rows**:

```
  Topology changes:
    + added index: StarlangLearnings (markdown, prose-tuned, RARELY write)
    ~ updated index: patterns ("What it holds" updated; sampled count grew 12 → 38)
```

If nothing changed: `Topology changes: none — block already up to date.`

## Common mistakes

| Mistake                                              | Fix                                                                                                                                               |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Writing the file before Stage C diff confirmation    | Cartography and synthesis are read-only. The first write is after the user picks `Write` at the diff gate.                                        |
| Modifying content outside the marker block           | Markers are a hard boundary. Anything outside `<!-- BEGIN ... -->` / `<!-- END ... -->` is user-owned.                                            |
| Confidently guessing embedding model from Index name | When uncertain, mark `(verify)`. The user fixes it once; the next regeneration preserves their override only if they keep the row content stable. |
| Inferring write-policy from Index description alone  | `memory_stats` is the load-bearing signal. If it's unavailable, mark `(verify)` everywhere — do NOT fall back to description-only inference.      |
| Putting the temp file in the project worktree        | Use `mktemp` in `$TMPDIR`. Otherwise the temp file shows up in `git status` mid-run and can be accidentally committed.                            |

## Important rules

- **NEVER write `./AGENTS.md` before the diff-and-confirm gate completes.**
- **NEVER touch content outside the marker block.** Idempotent re-runs depend on this.
- **NEVER skip the synthesis review gate.** The table is the highest-leverage artifact this skill produces; if it's wrong, everything downstream is wrong.
- **NEVER auto-commit.** The user owns commit timing.
- **If Stage A errors, abort and surface plainly.** Do not write a partial / placeholder block.
