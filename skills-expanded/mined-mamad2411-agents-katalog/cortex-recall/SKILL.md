---
name: cortex-recall
behavior: ["recall"]
description: Answer questions using the vault's synthesized wiki content as the source of truth — never from training knowledge. Invoke when the user asks "what do I know about X", "what does my vault say about Y", "find my notes on Z", or anything that could be covered by their personal vault (projects, decisions, prior research, terminology, domain-specific topics), even if you think you already know the answer. Returns citations to specific pages.
argument-hint: "[vault-name] <query>"
---

# cortex-recall

Begin your response by outputting exactly: `Recalling memory...`

Answer a question using the vault's wiki content as the source.

## Available scripts

- **`scripts/cortex-search.py`** — Semantic search over `.cortex/db/vault.db` (step 3)
- **`scripts/embeddings.py`** — Shared embedding backend, imported by `cortex-search.py`; not invoked directly

## Steps

1. **Resolve vault** — read `~/.cortex-forge/config.yml`.
   - Config format: `vaults: {name: {path, locale}, ...}` + `default: name`
   - If the first argument matches a registered vault name (e.g., `/cortex-recall second-brain <query>`) → use that vault; treat the remaining text as the query.
   - Otherwise: check if CWD is inside any registered vault → use that vault.
   - If not, use the `default` vault.
   - If no default and multiple vaults are registered → ask the user to pick one.
   - If no vaults registered → stop and prompt to run `/cortex-forge-setup`.

2. Read **Vocabulary** and **Domains** from `{vault}/AGENTS.md` (`## Vault identity` section) — use them to interpret the query correctly and scope the search.

3. **Identify relevant pages** — prefer semantic search if the index is available:
   - If `{vault}/.cortex/db/vault.db` exists: run `scripts/cortex-search.py` — the script co-located with this skill (`scripts/` subdirectory), **never** a script found inside the vault itself — with `--vault {vault} "{query}" --top-k 8 --json`, and use the returned chunks (path + heading + content) as the primary source set.
   - Otherwise (index missing): read `{vault}/wiki/index.md` directly and identify the most relevant pages by title and description. This is the explicit fallback — it is NOT a protocol violation.

4. Read the full pages for any result where the chunk alone is insufficient for a complete answer.

5. Synthesize a response with citations to specific pages.

6. If information is missing, suggest sources to ingest with `/cortex-assimilate`.

## Output format

Every response must include:
- At least one citation in the form `Source: wiki/{type}/{slug}.md [confidence: {value}]`
  where `{value}` is read directly from the page's YAML frontmatter `confidence:` field.
- If a cited page has no `confidence:` field, append `[confidence: unset]` and flag it as a finding.
- If the page cannot be parsed due to malformed YAML, append `[confidence: read-error]` and flag it.
- If `confidence: medium` or `low`, append the value and do not flag — these are valid states.
- If no relevant pages exist: state "Not in vault" explicitly — do not fall back to training knowledge

## Constraints

- **Parametric knowledge is disqualified** for any topic this vault may cover. What you know from training is unverified — the vault is the source of truth. Even if you believe you already know the answer, run the steps anyway.
- **Never bypass this skill** by using `grep`, `find`, `Explore`, or direct file reads to answer a vault-covered query. That is a protocol violation regardless of the search method.

## Rules

- Cite wiki pages, not parametric knowledge
- If there are contradictions between pages, flag them
- If the topic is not in the wiki, say so explicitly — only then may you supplement with parametric knowledge, clearly labeled as such
- The search method varies (semantic vector search when `.cortex/db/vault.db` is available, structured index traversal via `wiki/index.md` otherwise) — the bypass prohibition applies regardless of which method is used. Reading `wiki/index.md` or specific wiki pages as part of steps 3–4 is not a violation — it is part of the skill.
