# Agent Wrapper Contract

Wrappers locais em `.github/agents/*.agent.md` devem permanecer finos.

## Regras

1. apontar para `agents/roles/<role>/agent.md` como fonte canônica
2. listar apenas o contexto local mínimo (repo, branch base, AGENTS.md)
3. não duplicar biblioteca operacional que vive em `agents/skills/`
4. regenerar via `workers/scripts/sync-paperclip-agents.mjs` quando a estrutura canônica mudar


## Paperclip

1. wrappers usam `target: github-paperclip` no frontmatter
2. todo papel estende `agents/skills/controleonline/shared-operations-paperclip-direct-execution/SKILL.md`
3. nao omita a cooperacao com workers/runners/Actions quando forem uteis
4. apos mudanca estrutural, rode `workers/scripts/sync-paperclip-agents.mjs`
