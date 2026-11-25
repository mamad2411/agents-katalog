## Distincao obrigatoria: GitHub Blocked e Paperclip blocked

Proibicao de tags de bloqueio: agents nao criam nem aplicam labels `agent:*:blocked`
no GitHub. Isso nao impede a recuperacao prioritaria de
issues Paperclip com status `blocked`.

- `Blocked` no GitHub Project #1 e `Backlog` sao estados de board sob controle
  humano. Agents/workers nao comentam, validam, rotulam, editam nem movem itens
  dessas colunas.
- `blocked` no Paperclip (`issue.status=blocked` / `/CON/inbox/blocked`) e a fila
  de recuperacao e prioridade maxima do Manager. Investigue a causa, retome ou
  corrija a execucao/task Paperclip e confirme por readback antes de capturar
  nova task.
- Se uma task Paperclip blocked apontar para uma issue GitHub em `Blocked`, a
  recuperacao limita-se ao estado Paperclip que possa ser corrigido sem mutar a
  issue/board GitHub; o trabalho GitHub aguarda acao humana.
- Nao crie/aplique/remova/solicite labels GitHub `agent:*:blocked` nem mova
  itens GitHub para `Blocked`. Essa vedacao nao se aplica ao status Paperclip.

# Manager Skills

## Papel

O Manager cria e acompanha a task de coordenação no Paperclip e suas subtasks
ativas de Developer, QA, Security, Design, UX e DevOps. QA, Security, Design e
UX sao validadores ativos em paralelo. A entrega do Developer
retorna como task de entrega para o Manager. Somente o Manager pode alterar
labels, status ou colunas no board GitHub; os demais agentes apenas entregam
evidências nas próprias subtasks. Após todas as subtasks concluírem, o Manager
faz a checagem final e movimenta o board.

Ordem resumida:

1. **DevOps** — sempre primeiro. Tasks com o quarteto `agent:qa:accepted` + `agent:security:accepted` + `agent:design:accepted` + `agent:ux:accepted` e revalidacao do Manager entram em uma RC tecnica congelada de no maximo 5 tasks; DevOps **deve** deixar `staging` no tip da RC antes do Manager mover para `In Review` (homologacao humana no staging). Depois da autorizacao humana em `Deploy`, a mesma RC, com manifesto e SHAs identicos, e promovida para `master`. O Manager decide `Done`/revalidacao por task.
2. **Hotfix** — validadores e promocao hotfix → staging.
3. **Documentacao**
4. **Developer — rejeicoes** (`agent:qa:rejected` / `agent:security:rejected`) — corrigir até a entrega ficar publicável, inclusive workflow/build; problemas de publicação/deploy vão para o DevOps com evidências.
5. **QA, Security, Design e UX** (paralelo)
6. **Developer — novos desenvolvimentos** — exatamente uma issue elegível.
7. **Higiene** — fallback estrito, somente sem trabalho elegível em P1–P6.

Toda rodada executa. Documentacao nao e fallback de P1/P2.

P4 e P6 do Developer consultam exclusivamente a coluna `Working`. O Manager
nao captura ou encaminha Developer a partir de `Ready`; a task precisa estar
em `Working` antes da primeira passagem e permanecer nessa coluna enquanto a
entrega estiver em andamento.

Na primeira passagem, o Developer deve ler e registrar o checklist QA de
`workers/automate/review-checklists.md` antes de alterar o alvo. Cada correção
ou retomada deve atualizar a branch com o `master` remoto atual. Impedimentos
de checklist ou de sincronização devem voltar ao Manager com evidência.

Toda rodada segue `agents/skills/controleonline/shared-operations-delivery-proof-contract/SKILL.md`:
comentário ou handoff sem mutação verificável não encerra trabalho. Sem delta
novo, labels/coluna novas ou mudança externa comprovada, a mesma issue deve ser
registrada com `NEXT_ACTION` e responsavel pela proxima acao; nunca repetida e
nunca convertida em tag ou estado de bloqueio.

Governança publicada no próprio `agents-mcp` é exceção direta: commit remoto e
estado da issue/board comprovados encerram a entrega, sem aprovação ou
handoff para QA, Security, Design ou UX.

Não repita uma issue com os mesmos SHAs, labels, coluna e evidência da rodada
anterior. Sem delta novo, o resultado é `NEXT_ACTION`.

O Manager é consumidor global da recuperação de backlog; consumidores globais
recuperacao de backlog e schedulers nao dependem de novo push. P4 (rejeicoes)
tem precedencia sobre P5 (Security) e P6 (novos desenvolvimentos). P7 é
fallback estrito. A capacidade global de `Working` é **5 tasks**; ao atingir
cinco, nenhuma nova task entra até uma task ativa sair da coluna. A exceção é
P1 `DevOps`, que continua publicando tasks em `Deploy`.

## Gate de staging

o quarteto `agent:qa:accepted` + `agent:security:accepted` + `agent:design:accepted` + `agent:ux:accepted` + revalidacao do Manager com
evidencia da entrega em `dev`.
Conclusão da task exige RC publicada e o quarteto QA+Security+Design+UX aceito. Depois que o
Manager mover para `Done`, ele cria no Paperclip as tasks filhas documentais
aplicáveis; a conclusão dos documentadores não é pré-requisito para o `Done` da
publicação.

## Output Contract

Prioridade tentada, acao executada, `DELIVERY_PROOF`, `DONE` ou `NEXT_ACTION`.
Comentário não substitui commit/ref remoto, decisão de label ou mudança de coluna.
Issues closed e itens Done exigem RC publicada e o quarteto aceito. Uma task
publicada em `master` sem o quarteto/evidencia local permanece aberta e volta
para `Working` para uma segunda rodada de validacao.

## Fontes principais

- `agents/roles/manager/agent.md`
- `agents/roles/devops/agent.md`
- `agents/skills/controleonline/shared-github-github-flow/SKILL.md`
- `agents/skills/controleonline/shared-operations-delivery-proof-contract/SKILL.md`
