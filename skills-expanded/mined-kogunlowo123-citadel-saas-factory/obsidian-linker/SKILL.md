---
name: obsidian-linker
description: Automatically generates Obsidian backlinks and wikilinks when creating or modifying any markdown file — use when writing docs, agents, rules, runbooks, or any .md file
allowed-tools: Read, Write, Grep, Glob
---

# obsidian-linker

Generates and maintains bidirectional `[[wikilinks]]` between every markdown file in the repository and the Obsidian vault at `docs/vault/`. Enforced by [[../../rules/obsidian-backlinks|obsidian-backlinks rule]].

## When to invoke

- Whenever you write or modify any `.md` file anywhere in the repo.
- Before committing any change that touches markdown.
- When `/project:vault-link` is invoked.
- When the `obsidian-curator` agent is auditing the vault.

## Procedure

1. **Read the vault index.** Open `docs/vault/_index.md` and the per-domain `_index.md` files under `docs/vault/agents/`, `docs/vault/architecture/`, `docs/vault/runbooks/`, `docs/vault/memory/`, `docs/vault/knowledge-graph/`. These enumerate every existing note.

2. **Extract concept candidates from the target file.** Scan for:
   - **Agent identifiers** — anything matching `[a-z]+-[a-z-]+` that exists as a vault note under `docs/vault/agents/<domain>/<id>.md`.
   - **Service / component names** — `FastAPI`, `PostgreSQL`, `Redis`, `K3s`, `ArgoCD`, `Linkerd`, `Vault`, `MinIO`, `RabbitMQ`, `Keycloak`, `Traefik`. Map to `docs/vault/architecture/component-*.md`.
   - **ADR references** — `ADR-\d+` → `docs/vault/architecture/adr-*.md`.
   - **Rule references** — any token matching the basename of a file in `.claude/rules/`.
   - **Skill references** — any token matching a skill name in `.claude/skills/`.
   - **MCP server names** — anything from `.claude/mcp/`.
   - **Domain keywords** — `engineering`, `frontend`, `devops`, `security`, etc. Map to `docs/vault/agents/<domain>/_index.md`.

3. **Match by keyword and domain.** For each candidate, use `Grep` to confirm the target note exists. Discard misses.

4. **Insert into target file:**
   - If the file is **inside** `docs/vault/`, replace the content between `<!-- linked-notes:start -->` and `<!-- linked-notes:end -->` with a bullet list of `[[wikilinks]]`. Create the markers if missing.
   - If the file is **outside** `docs/vault/`, append (or update) a `## Vault Links` section at the bottom with a bullet list of `[[../../docs/vault/...]]` style relative wikilinks.

5. **Enforce bidirectionality.** For every note linked from the target, open that note and ensure the target appears in *its* `## Linked Notes` block. If not, add it. This is the critical step — without it, links are one-way and the graph is misleading.

6. **Preserve existing content.** Never edit anything outside the `## Vault Links` or `<!-- linked-notes -->` regions.

## Output format

Inside vault notes (between markers):

```markdown
<!-- linked-notes:start -->
- [[../engineering/eng-api-designer|API Designer]]
- [[../../architecture/component-backend|Backend (FastAPI)]]
- [[../../runbooks/deployment-rollback|Deployment Rollback]]
<!-- linked-notes:end -->
```

Outside the vault:

```markdown
## Vault Links

- [[../../docs/vault/agents/engineering/eng-api-designer|API Designer]]
- [[../../docs/vault/architecture/component-backend|Backend]]
```

## Idempotency

Re-running the skill on an unchanged file must produce no diff. The marker comments and the relative-link normalization ensure that.

## Vault Links

- [[../../rules/obsidian-backlinks|obsidian-backlinks rule]]
- [[../../commands/vault-link|vault-link command]]
- [[../../agents/obsidian-curator|obsidian-curator agent]]
- [[../../../docs/vault/_index|Vault Home]]
