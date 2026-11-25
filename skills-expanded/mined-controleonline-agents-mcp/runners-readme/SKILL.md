# Runner Skills

Este arquivo mapeia o modelo atual de execução do ecossistema sem misturar o papel dos agents pares no ChatGPT com o papel do runner gerencial no GitHub.

## Execução direta pelo Paperclip

QA é executado e decidido localmente pelo agent no workspace Paperclip. Nenhum
workflow ou check do GitHub participa da aprovação/reprovação; Actions são
sinal suplementar e jamais substituem testes locais ou impedem a decisão.
O GitHub Manager Runner não lê comentários/reviews para inferir QA nem promove
tasks a `In Review`; essa transição pertence ao Manager após os gates locais.

O fluxo operacional não usa workflow, composite action, wrapper ou assignment Paperclip. Consulte as skills de fila, handoff e execução dos agents em `agents/skills/controleonline/`.

Existe uma trilha operacional oficial:

- os agents do Paperclip executam diretamente os papeis usando `agents/roles/*/agent.md`
- os agents pares no ChatGPT podem executar correcao estrutural ou apoio operacional quando acionados pelo humano
- o workflow `.github/workflows/github-operations.yml` e os runners em `workers/src/` / `workers/automate/` permanecem como referencia tecnica/diagnostico, nao como canal principal

Com isso:

- `Developer`, `QA`, `Security`, `Design`, `UX` e `DevOps` continuam tendo comportamento real definido pelas roles canonicas
- Labels canonicos de validacao ativos: `agent:qa:accepted`/`rejected`, `agent:security:accepted`/`rejected`, `agent:design:accepted`/`rejected`, `agent:ux:accepted`/`rejected`
- Design e UX foram reativados junto com QA e Security; o gate de RC exige o quarteto
- quando o quarteto aceito existe e o Manager revalidou a entrega, `DevOps` cria/congela a RC; uma pessoa aprova a tarefa movendo-a para `Deploy`, e a partir de `Deploy` `DevOps` publica a RC em produção
- `DevOps` permanece responsável pela fila própria de deploy e pela reconciliação operacional

## GitHub Manager Runner

- workflow: `.github/workflows/github-operations.yml`
- lógica final: `workers/automate/scripts/github-operations.mjs`
- guia operacional: `workers/automate/github-operations.md`

Este workflow nao substitui a execucao direta do Paperclip.

## Runners por papel

- `workers/src/developer-runner.js` -> `workers/automate/scripts/developer-pr-dispatch.mjs`
- `workers/src/security-runner.js` -> `workers/automate/scripts/pr-label-review-runner.mjs` com `PR_REVIEW_ROLE=security`
- `workers/src/qa-runner.js` -> `workers/automate/scripts/pr-label-review-runner.mjs` com `PR_REVIEW_ROLE=qa`
- `workers/src/devops-runner.js` -> `workers/src/agent-dispatch-runner.js` com `AGENT_DISPATCH_ROLE=devops`
- `workers/src/cto-runner.js` -> `workers/automate/scripts/cto-project-supervisor.mjs` (nao faz parte da trilha atual `Developer` -> `QA/Security/Design/UX` -> `Manager` -> `DevOps`)
- `workers/automate/scripts/cto-pr-finalizer.mjs` -> nao faz parte da consolidacao atual; a trilha vigente usa `Deploy` -> `DevOps`

## Regra de leitura

Quando a duvida envolver ownership, fila ou runtime:

1. confira primeiro os entry points reais em `workers/src/*-runner.js`
2. confira a logica final em `workers/automate/scripts/`
3. use `agents/skills/controleonline/shared-README/SKILL.md` e `workers/automate/agents/runner-map.md` como mapa de governanca
4. trate scripts ou workflows fora desse caminho como inativos até reativação explícita
