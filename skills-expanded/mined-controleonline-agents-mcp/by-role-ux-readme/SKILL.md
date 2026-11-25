# UX Skills

## Papel

O agent UX faz review de jornada na **tela real aberta no browser**. Pode processar mais de uma issue na mesma rodada.

## Skills essenciais

- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`
- `agents/skills/controleonline/by-role-ux-checklist/SKILL.md`

## Labels

| Label | Significado |
| --- | --- |
| `agent:ux` | Solicitacao de review de jornada |
| `agent:ux:accepted` | Aprovado; etapa encerrada nesta passagem |
| `agent:ux:rejected` | Recusado; devolve ao Developer |

## Handoff

- Aceitar: `agent:ux:accepted`, remover `agent:ux`
- Recusar: `agent:ux:rejected`, issue open, comentario com fluxo/URL percorrido

## Fontes

- `agents/roles/ux/agent.md`
- `agents/skills/controleonline/by-role-ux-checklist/SKILL.md`
