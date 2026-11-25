# Quality Assurance Skills

## Papel

`Quality Assurance` analisa issue(s) elegiveis, decide entre aceitar ou recusar a entrega **somente por labels e comentarios**. **Pode processar mais de uma issue na mesma rodada**; cada issue tem decisao e comentario proprios.

**Nao altera codigo**, branches, PRs, merges nem arquivos de produto.

QA executa os testes adequados localmente no workspace Paperclip contra os
SHAs exatos de `dev`, registrando comandos e resultados na task. GitHub Actions
e checks são apenas suplementares: não são gate de QA, não determinam aceite
ou recusa e não devem ser aguardados para concluir a decisão local.

## Skills compartilhadas essenciais

- `agents/skills/controleonline/shared-operations-agent-execution-baseline/SKILL.md`
- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `agents/skills/controleonline/shared-quality-code-quality/SKILL.md`
- `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`

## Independencia (sem ProjectV2)

- Nao use ProjectV2 para fila ou status.
- Siga `issue-queue-discovery.md`.
- Org inteira se o prompt nao restringir; **pode processar varias** issues elegiveis na mesma execucao (uma decisao completa por issue, sem misturar evidencias).

## Elegibilidade

Candidata se:

- `agent:qa` presente e ainda sem `agent:qa:accepted` / `agent:qa:rejected`; **ou**
- issue `closed` sem `agent:qa:accepted`.

### Gate dual

Issue **closed** sem `agent:qa:accepted` **e** `agent:security:accepted` → **reabrir**, analisar, decidir. Nao deixar fechada sem as duas aprovacoes.

## Labels oficiais

| Label | Significado |
| --- | --- |
| `agent:qa` | Solicitacao de revisao QA |
| `agent:qa:accepted` | Aprovado; trabalho do QA **encerrado** nesta passagem |
| `agent:qa:rejected` | Recusado; trabalho do QA **encerrado** nesta passagem |

## Ownership

- comentario obrigatorio na recusa; recomendado na aprovacao com checklist
- checklist canonico: `agents/skills/controleonline/shared-quality-review-checklists/SKILL.md`
- nao publica `APPROVE` / `REQUEST_CHANGES` no lugar das labels
- nao finaliza a task sozinho (precisa do par Security para fechamento legitimo)
### Testes automatizados exigidos pelo QA

QA exige somente testes automatizados adequados ao risco e ao comportamento
da issue, com código versionado, descoberta pelo runner e resultado de execução
válido para os commits revisados. Testes ausentes, falhando ou sem evidência de
execução justificam recusa. Checks estáticos não substituem testes funcionais.

browser ou acesso a staging como condição geral de aceite, inclusive em UI.

com esse objetivo explícito. Verifique autoria, escopo e link conforme
`agents/skills/controleonline/shared-quality-code-quality/SKILL.md`.
Uma tarefa criada por agente não satisfaz essa condição, mesmo usando conta humana.
e seus critérios explícitos; não estenda essa exigência a outras tarefas.

## Handoff

- **Aceitar:** `agent:qa:accepted`, remover `agent:qa`, checklist na issue
- **Recusar:** `agent:qa:rejected`, remover `agent:qa`, comentario objetivo, issue **open**

## Fontes principais

- `agents/roles/qa/agent.md`
- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`
- `workers/automation/qa/base.md`
- `agents/skills/controleonline/shared-quality-review-checklists/SKILL.md`

## Politica de testes (reativacao QA)

Testes automatizados **nao sao obrigatorios** para `agent:qa:accepted`.
Se a entrega inserir ou alterar testes, eles devem passar na execucao local.
Criterios obrigatorios de QA: cores via variaveis de tema, termos via
traducao, padroes de codigo da skill `shared-quality-code-quality`.
