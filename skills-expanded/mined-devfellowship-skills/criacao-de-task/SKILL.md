---
name: criacao-de-task
description: Use sempre que for abrir uma task de trabalho pela ferramenta `create_task` do MCP — inclusive quando a task nasce de um plano, de uma conversa ou de uma PR. Garante que a task nasça com etapa, com o "por quê" e ligada ao plano certo. Não use para editar task existente.
author: devfellowship
tags: [task, mcp, plano, kanban, handoff]
---

# Abrir task pelo MCP

## Visão geral

Uma task criada é uma linha válida no banco em qualquer cenário. Não existe erro
para você notar. É por isso que os dois modos de falha aqui são **silenciosos**: a
task nasce, a ferramenta responde sucesso, e a informação que faltava só aparece
semanas depois — quando alguém precisa dela e não tem como recuperar.

**Princípio central:** quem abre a task é a última parte do sistema que ainda tem o
contexto. Depois de você, ninguém reconstrói o "por quê" a partir do nome da task.

## Quando usar

- Vai chamar `create_task`
- Está transformando uma conversa, um plano ou uma PR em trabalho rastreável
- Está abrindo várias tasks de uma vez a partir de um plano

**Não usar** para atualizar task existente — `update_task` não passa por aqui.

## Regra 1 — etapa e andamento são eixos diferentes

`stage_id` responde **que tipo de trabalho é isso**. `status` responde **quanto já
andou**. São perguntas independentes: uma task de design pode estar em andamento,
uma task de execução pode estar parada.

A ferramenta exige `stage_id` porque enquanto ele era opcional 1160 tasks nasceram
sem etapa. Task sem etapa não aparece no board — ela existe no banco e some da
vista, que é a pior combinação possível.

Escolha por **onde o trabalho começa**, não por onde ele vai terminar:

| Etapa | Aparece no board como | Use quando |
|---|---|---|
| `design` | Ideation | ainda é exploração: referência, ideia, alternativa |
| `decision` | Design Review | tem proposta pronta esperando alguém bater o martelo |
| `qa` | QA / Test | é conferência de acabamento — texto, estado de borda |
| `spec` | Spec | o requisito ainda está sendo detalhado |
| `execution` | Execução | está pronto para ser construído |
| `review` | QA / Test (selo Engineering) | é validação final de trabalho já feito |

O que você passa é sempre o **id** da coluna da esquerda. O nome do meio é só o
rótulo do board e já mudou uma vez sem que o id mudasse — não use o rótulo como
valor.

Na dúvida entre duas, pergunte o que impede a task de andar hoje. É essa a etapa.

## Regra 2 — o pacote de contexto é a task

`why` e `what` são obrigatórios e não são a mesma coisa:

- **`why`** — a dor que originou. Sem isso quem não estava na conversa não sabe se
  aprova, questiona ou despriorize. É a única parte que não se reconstrói depois.
- **`what`** — o que foi efetivamente feito ou proposto.

Os campos de link (`pr_url`, `storybook_url`, `playground_url`, `files`) são
opcionais mas quase sempre existem quando a task nasce de código. Preencha: eles
são a diferença entre um card que se explica sozinho e um card que gera três
perguntas no canal do time.

Um `why` ruim é o resumo do diff. Um `why` bom é a frase que a pessoa disse antes
de o trabalho existir.

## Regra 3 — task de plano exige um segundo passo

Esta é a falha que já aconteceu e vai acontecer de novo.

`create_task` escreve a task e **nada mais**. Ela não liga a task a nenhum plano, e
nenhuma ferramenta desse mesmo servidor faz isso. Um plano monta a lista de
execução a partir das ligações dele — então, até você criar a ligação, a task é
invisível no plano.

O sintoma: 18 tasks criadas, reportadas como ligadas, e a página do plano em
branco. Plano vazio se lê como "ninguém começou".

Depois de criar as tasks, chame `set_plan_tasks` **no MCP de plans** (é outro
servidor) com o slug do plano e **todos** os ids que o plano deve mostrar. Ela
**substitui** o conjunto — passar só os ids novos apaga os antigos.

## Regra 4 — dono e canal você não escolhe do jeito que imagina

- **Dono:** omitir `owner_id` atribui a task a quem chamou a ferramenta. Isso é o
  certo na maioria dos casos. Só passe explícito quando a task é de outra pessoa.
  Nunca existe caminho que grave dono nulo — task sem dono some do board.
- **Canal do Discord:** não é campo da task. A notificação segue o canal amarrado
  à **épica**, e a task herda. Se a task nasce muda, a épica é que está sem canal —
  não adianta procurar o campo na task.

## Regra 5 — não relate como pronto sem ler de volta

Sucesso da ferramenta prova que a linha foi gravada. Não prova que a task está
visível no board, nem que apareceu no plano, nem que o time foi avisado.

Antes de dizer que está pronto: leia a task de volta e, se ela pertence a um plano,
abra o plano e confirme que ela aparece lá.

## Checklist

- [ ] `stage_id` escolhido por tipo de trabalho, não por andamento
- [ ] `why` conta a dor original, não resume o diff
- [ ] `what` diz o que foi feito ou proposto
- [ ] Links preenchidos quando a task nasce de código
- [ ] `owner_id` omitido, salvo se a task é de outra pessoa
- [ ] Se pertence a plano: `set_plan_tasks` chamada com a lista **completa**
- [ ] Task lida de volta antes de reportar pronto
