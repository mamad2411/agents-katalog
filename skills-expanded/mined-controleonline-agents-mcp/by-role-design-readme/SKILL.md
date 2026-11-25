# Design Skills

## Papel

O agent Design faz review visual na **tela real aberta no browser**. Pode processar mais de uma issue na mesma rodada.

## Skills essenciais

- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`
- `agents/skills/controleonline/by-role-design-checklist/SKILL.md`

## Labels

| Label | Significado |
| --- | --- |
| `agent:design` | Solicitacao de review visual |
| `agent:design:accepted` | Aprovado; etapa encerrada nesta passagem |
| `agent:design:rejected` | Recusado; devolve ao Developer |

## Handoff

- Aceitar: `agent:design:accepted`, remover `agent:design`
- Recusar: `agent:design:rejected`, issue open, comentario com tela/URL inspecionada

## Fontes

- `agents/roles/design/agent.md`
- `agents/skills/controleonline/by-role-design-checklist/SKILL.md`
