---
name: specsfy-mvp-milestone-interviewer
description: Use quando uma ideia de produto precisar de uma entrevista adaptativa para definir o MVP, suas milestones, condições de saída, vínculos iniciais com specs e o que ficará para depois. Não use para capturar Inbox sem perguntas, detalhar tarefas técnicas ou planejar a evolução depois do MVP aceito.
---

# Entrevistar para definir o MVP e seus marcos

## Modo de interação

Modo de interação: `perguntas`.
Antes de formular qualquer pergunta, leia e aplique o
`Contrato de perguntas numeradas` de `.specsfy/Spec.md`.

Leia `PROJECT.md`, a Inbox ou backlog que originou a conversa e as specs já
existentes. Preserve formulações confirmadas. Esta skill conduz a descoberta do
MVP antes de transformar o material em specs e backlog.

## Conduzir uma conversa adaptativa

1. Comece pela finalidade, pela pessoa atendida e pelo problema observável.
2. Após cada rodada, apresente uma síntese curta do que foi entendido e formule
   pelo menos três perguntas numeradas a partir das lacunas que ainda impedem
   definir um fluxo utilizável.
3. Explore somente o assunto necessário: fluxo principal, dados indispensáveis,
   papéis, regras, integrações, limites, demonstração e validação. Não aplique
   formulário fixo nem repita resposta confirmada.
4. Continue enquanto faltar informação para declarar quem conclui qual jornada,
   em qual contexto e como a jornada será verificada. Não há máximo de
   rodadas.
5. Registre respostas aprovadas em `PROJECT.md` e, quando a pessoa aprovar a
   síntese, crie ou atualize `specs/milestones/MNN.md`.

## Propor milestones do MVP

Proponha de quatro a oito marcos orientados por estados demonstráveis do
produto. Cada marco precisa conter:

- `Objetivo`: estado relevante alcançado pelo produto;
- `Condição de saída`: jornada verificável, não uma lista de tarefas;
- `Fora de escopo`: capacidades deliberadamente adiadas;
- `Specs vinculadas`: IDs principais e complementares quando existirem;
- `Dependências`: marcos anteriores quando houver ordem obrigatória.

Apresente a proposta inteira para confirmação antes de criar ou reorganizar
arquivos. Marque uma spec com uma milestone principal e inclua marcos
complementares somente quando a mesma capacidade contribuir de fato para mais
de um resultado.

## Materializar e manter o mapa

Depois da confirmação:

1. Use `M01`, `M02` e assim por diante, em sequência estável.
2. Inclua `Milestones | MNN` na tabela de cada spec ou backlog associado.
3. Execute `specsfy milestones sync --project .` para atualizar `specs.md` e
   os blocos derivados dos arquivos de milestone.
4. Encaminhe cada capacidade ainda geral para `$specsfy-02-backlog`; encaminhe
   uma capacidade suficientemente definida para `$specsfy-03-specify`.

O sincronizador calcula progresso por specs completas e mostra backlog
relacionado, mas não escreve objetivo, condição de saída ou fora de escopo.

## Condição para encerrar

Encerre esta entrevista somente quando houver uma afirmação verificável no
formato: "o MVP estará pronto quando [pessoa] conseguir [resultado] por meio
de [jornada], sob [limites confirmados]". Entregue a síntese, os marcos, as
lacunas remanescentes e o próximo handoff.

## Limites

- Não invente respostas, marcos, condições de saída ou vínculos.
- Não trate sprint, versão, componente ou tarefa como milestone.
- Não aprova gates, implementa código nem conclui uma spec.
- Não use o entrevistador de roadmap para ampliar o MVP sem confirmação.
