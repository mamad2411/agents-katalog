---
name: cortex-prune
behavior: ["prune", "recall"]
description: Health check the vault — detects dead links, orphan pages, missing provenance, and unprocessed sources. Invoke when the user asks "is everything organized?", "check if something is broken", "are there orphan pages?", "run a vault health check", or "prune the vault".
argument-hint: "[vault-name]"
---

Begin your response by outputting exactly: `Pruning vault...`

Health check the active vault in three layers: structural (script), semantic (agents), and drift (metadata comparison).

## Available scripts

- **`scripts/cortex-prune.sh`** — Layer 1 structural check; single writer of `wiki/meta/vault-report.json` (step 2)
- **`scripts/cortex-validate-schema.sh`** — Validates `vault-report.json` schema drift, called by `cortex-prune.sh` as a sibling

## Steps

1. **Resolve vault** — read `~/.cortex-forge/config.yml`:
   - Config format: `vaults: {name: {path, locale}, ...}` + `default: name`
   - If the first argument matches a registered vault name (e.g., `/cortex-prune personal`) → use that vault.
   - Otherwise: check if CWD is inside any registered vault → use that vault.
   - If not, use the `default` vault.
   - If no default and multiple vaults → ask the user to pick one.
   - If no vaults registered → stop and prompt to run `/cortex-forge-setup`.

   **Confirmation gate:** if the vault was resolved from an explicit argument (not from CWD), confirm with the user before proceeding: "About to prune `{vault-name}` at `{path}`. Continue?" — do not proceed until confirmed.

   Confirm vault is a Cortex Forge vault: path contains `wiki/` and `AGENTS.md`.

   Read **Domains** and **Out of scope** from `AGENTS.md` (`## Vault identity`) — use them to flag pages whose topics fall outside the vault's defined scope.

2. **Layer 1 — Structural check**: Run `bash scripts/cortex-prune.sh {vault}`, where `cortex-prune.sh` is the script co-located with this skill (`scripts/` subdirectory — resolve its path from wherever this file was read from). If the script is missing, the skill installation is incomplete — reinstall with `npx skills add itsmistermoon/cortex-forge --skill cortex-prune` (or `/cortex-forge-setup`, sub-task `skills`).

3. **Layer 2 — Semantic analysis**: Run the four semantic checks below. For each check, spawn subagents as described — do not attempt to reason about the wiki pages from memory alone.

3a. **Layer 3 — Drift detection**: For each `wiki/sources/` page, check whether its `.raw/` file was modified after the page was last synthesized.

   1. For each file in `{vault}/wiki/sources/`, read its `raw:` and `updated:` frontmatter fields. Skip pages with no `raw:` field.
   2. Run `stat -f "%Sm" -t "%Y-%m-%d" {vault}/{raw}` (macOS) or `date -r {vault}/{raw} "+%Y-%m-%d"` to get the `.raw/` file's modification date. If the file does not exist, skip — already covered by Layer 1's `raw_without_source_page` check.
   3. If `.raw/` mtime > `updated:` → MEDIUM finding: "`.raw/{slug}.md` was modified after `wiki/sources/{slug}.md` was last synthesized — source page may be stale."
   4. If no drift found, note: "Layer 3: no drift detected."

4. **Report** all findings (Layer 1 + Layer 2 + Layer 3) grouped by severity. For each: path(s), problem, proposed action.

4a. **Verify `wiki/meta/vault-report.json`** — the Layer 1 script (step 2) writes or overwrites this file on every run. Confirm it was refreshed (its `generated` date matches today) and report its path to the user. Do not write it yourself — the script is the single writer. The canonical schema:

   ```json
   {
     "generated": "YYYY-MM-DD",
     "health": {
       "dead_links": [],
       "raw_without_source_page": [],
       "missing_confidence": [],
       "orphan_pages": []
     }
   }
   ```

   Field definitions:
   - `health.dead_links` — array of `{"from": "wiki/...", "broken_target": "[[X]]"}` objects, from Layer 1.
   - `health.raw_without_source_page` — array of `.raw/` file paths with no corresponding `wiki/sources/` page, from Layer 1.
   - `health.missing_confidence` — array of page paths where `confidence:` is absent from frontmatter, from Layer 1.
   - `health.orphan_pages` — array of page paths with no incoming `[[wikilinks]]` from any other vault page, from Layer 1. Matched by full vault-relative path (e.g. `wiki/concepts/foo.md`) to avoid basename collisions.

   This file is the session-startup health signal read in `AGENTS.md`. It is gitignored — a local artifact, not versioned content. This schema is canonical: do not add fields that have no consumer in `AGENTS.md` or in this skill.

5. **Consolidate findings** — if your environment supports subagent spawning, delegate to a subagent using the lightest capable model available. This task requires only structured formatting of pre-classified findings — prioritize speed. If subagent spawning is not supported, execute inline.

   Prompt: "You are synthesizing the results of a vault health check. Here is the Layer 1 structural report: {layer1_json}. Here are the Layer 2 semantic findings: {layer2_findings}. Produce a single grouped report with this structure:
   - HIGH findings (list each: path, problem, proposed action)
   - MEDIUM findings (same)
   - LOW findings (same)
   - Summary line: '{N} HIGH / {N} MEDIUM / {N} LOW findings'
   For each finding, output exactly three fields: path, problem (one sentence), proposed action (one imperative sentence). No additional explanation, context, or justification."

   The main agent presents this consolidated report verbatim — it does not re-process or summarize the output.

6. **Ask** whether to proceed with corrections per the auto-correct / requires-confirmation rules below.

---

## Layer 2 — Semantic checks

**Hard cap**: evaluate at most 20 candidate pairs in 2a and at most 20 uncovered sources in 2c. If there are more, pick the 20 with the strongest surface-level signal and note the total count skipped. Do not write scripts, external files, or spawn more than 3 subagents total — inline evaluation is always acceptable and preferred for small vaults.

### 2a. Unlinked relationships between entities and concepts

Read `wiki/index.md` to get the full list of entities and concepts. Then:

1. Identify candidate pairs where EITHER is true (read the files directly — no scripts):
   - One page's `title`, `aliases`, or `tags` contains a term in the other page's title or aliases
   - One page's body text mentions the other entity/concept by name without `[[wikilink]]` syntax
2. Evaluate each candidate pair inline: read both pages and classify as RELATED or COINCIDENCE with one sentence of justification. If RELATED, note the exact wikilink to add to each page. Do not spawn subagents for this step.
3. Report RELATED findings as MEDIUM. Discard COINCIDENCE.

### 2b. Body text mentions without wikilinks

For each page in `wiki/concepts/`, `wiki/entities/`, and `wiki/pages/`:

1. Extract entity and concept titles + aliases from the index.
2. Scan the page body for plain-text mentions of those names (case-insensitive) not already wrapped in `[[...]]`.
3. Report as LOW: "Page X mentions 'Y' without a wikilink — consider `[[wiki/entities/Y]]`."

Do not flag mentions inside code blocks or frontmatter.

### 2c. Sources without a covering concept

For each page in `wiki/sources/`:

1. Check if any page in `wiki/concepts/` or `wiki/entities/` lists this source in its `sources:` frontmatter.
2. For uncovered sources: read the source page and classify inline — NEEDS_PAGE, COVERED_BY {page}, or BORDERLINE with one sentence. Do not spawn subagents for this step.
3. Report NEEDS_PAGE as MEDIUM. Report BORDERLINE for user decision. Discard COVERED_BY.

### 2d. Potential page merges (debate pattern)

Trigger only when check 2a finds two pages with significant overlap (not just a component relationship, but potentially duplicate coverage of the same topic).

Evaluate inline: read both pages, argue FOR merge (max 3 bullets), argue AGAINST (max 3 bullets), render a verdict: MERGE, KEEP_SEPARATE, or RESTRUCTURE with one paragraph.

Report verdict as MEDIUM. Never auto-apply — always requires user confirmation.

---

## Auto-correctable (propose + apply on confirmation)

- Add missing `confidence:` or `tags:` to source pages
- Add `[[wikilink]]` to a body mention identified in check 2b
- Add entry to `wiki/index.md` for unindexed pages
- Add `wiki/meta/log.md` entry: `## [YYYY-MM-DD] prune | {N} findings`

`wiki/meta/vault-report.json` is written automatically by the co-located `cortex-prune.sh` on every Layer 1 run — it is not a correction and needs no confirmation.

## Requires confirmation (never auto-apply)

- Add cross-links between entities/concepts (check 2a verdict: RELATED)
- Create missing concept/entity pages (check 2c verdict: NEEDS_PAGE)
- Merge pages (check 2d verdict: MERGE or RESTRUCTURE)
- Delete orphan pages

---

## Detection criteria — Layer 1 (cortex-prune.sh, co-located with this skill)

| Severity | Check |
|---|---|
| HIGH | Dead `[[wikilinks]]` pointing to non-existent pages |
| HIGH | `.raw/` files with no corresponding `wiki/sources/` page |
| HIGH | Pages without YAML frontmatter (excl. `index.md`, `log.md`) |
| MEDIUM | Orphan pages — no incoming wikilinks from any other vault page |
| MEDIUM | Concepts/entities without `sources:` or `confidence:` frontmatter |
| MEDIUM | Source pages without `confidence:` frontmatter |
| LOW | Source pages without `tags:` (or `tags: []`) |

## Rules

- Always run the script for Layer 1 — never reproduce its logic ad-hoc
- For Layer 2, always spawn subagents — never reason about page relationships from memory alone
- `index.md` and `log.md` without frontmatter is expected, not a finding
- Source pages use `source:` (URL) and `raw:` for provenance — `raw:` is the page's context pointer back to its `.raw/` primary. `sources:` (wiki links) is for concepts and entities only
- Orphan sources are normal if freshly ingested and not yet linked from concepts/entities
- Never delete or merge pages without explicit user confirmation
- Debate pattern (2d) only triggers on genuine ambiguity — not on clear component relationships
- Layer 3 drift findings are informational — never auto-re-synthesize; always ask the user

## Changelog

- 2026-07-01 [Claude Code]: Added Layer 3 — drift detection: mtime of `.raw/` vs `updated:` in `wiki/sources/`; intro updated from two to three layers
