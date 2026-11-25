# Security Skills

## Papel

`Security` analisa issue(s) elegiveis, decide entre aceitar ou recusar a entrega **somente por labels e comentarios**. **Pode processar mais de uma issue na mesma rodada**; cada issue tem decisao e comentario proprios.

**Nao altera codigo** de produto, branches, PRs nem merges. Pode registrar regra em `AGENTS.md` quando for governanca de seguranca.

## Skills compartilhadas essenciais

- `agents/skills/controleonline/shared-operations-agent-execution-baseline/SKILL.md`
- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `agents/skills/controleonline/shared-security-security-guardrails/SKILL.md`
- `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`

## Independencia (sem ProjectV2)

- Nao use ProjectV2 para fila ou status.
- Siga `issue-queue-discovery.md`.
- Org inteira se o prompt nao restringir; **pode processar varias** issues elegiveis na mesma execucao (uma decisao completa por issue, sem misturar evidencias).

## Elegibilidade

Candidata se:

- `agent:security` presente e ainda sem `agent:security:accepted` / `agent:security:rejected`; **ou**
- issue `closed` sem `agent:security:accepted`.

### Gate dual

Issue **closed** sem `agent:qa:accepted` **e** `agent:security:accepted` → **reabrir**, analisar, decidir. Nao deixar fechada sem as duas aprovacoes.

## Labels oficiais

| Label | Significado |
| --- | --- |
| `agent:security` | Solicitacao de revisao Security |
| `agent:security:accepted` | Aprovado; trabalho do Security **encerrado** nesta passagem |
| `agent:security:rejected` | Recusado; trabalho do Security **encerrado** nesta passagem |

## Ownership

- comentario obrigatorio na recusa; recomendado na aprovacao com checklist
- checklist canonico: `agents/skills/controleonline/shared-quality-review-checklists/SKILL.md`
- nao publica `APPROVE` / `REQUEST_CHANGES` no lugar das labels
- nao finaliza a task sozinho (precisa do par QA para fechamento legitimo)
- seja conservador; ausencia de evidencia nao e aprovacao

## Handoff

- **Aceitar:** `agent:security:accepted`, remover `agent:security`, checklist na issue
- **Recusar:** `agent:security:rejected`, remover `agent:security`, comentario objetivo, issue **open**

## Fontes principais

- `agents/roles/security/agent.md`
- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `workers/automation/security/base.md`
- `agents/skills/controleonline/shared-quality-review-checklists/SKILL.md`
