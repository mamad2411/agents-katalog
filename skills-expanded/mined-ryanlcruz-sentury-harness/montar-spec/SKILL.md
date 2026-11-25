---
name: montar-spec
vitrine:
  grupo: 'Trabalho'
  rotulo: 'especificar software antes de implementar'
description: "Spec/especificação software/API/módulo: requisitos EARS; design técnico."
version: 1.0.0
author: Sentury
license: MIT
category: cognitive
priority: 70
metadata:
  # Frases de projeto de software, não palavras soltas como plano ou tarefa.
  gatilhos:
    - '\b(montar|monte|criar|crie|fazer|faca|escrever|escreva|elaborar|elabore|definir|defina)\s+(uma?\s+)?spec\b'
    - '\bespecifica(?:r|cao)\s+(?:d[eo]\s+)?(?:software|sistema|feature|funcionalidade|api|modulo)\b'
    - '\b(requisitos?\s+em\s+ears|requirements?\s+em\s+ears)\b'
    - '\b(requisitos?\s*(?:->|→|,|e)\s*design\s*(?:->|→|,|e)\s*tarefas?)\b'
---

# Especificar software

Use esta skill para projetar uma feature, API, módulo, sistema ou correção de
software **antes da implementação**. Não a use para plano de ação, investigação,
rotina, workflow ou trabalho pessoal. Se a pessoa só pediu para implementar uma
mudança pequena, implemente; não imponha três documentos.

## Requisitos: o que o sistema deve fazer

Inspecione o código e as instruções do projeto quando existirem. Produza uma
primeira versão completa a partir do pedido, sem começar com um questionário.
Separe fatos observados, hipóteses e decisões que dependem da pessoa; não
invente comportamento atual. Dê identificadores estáveis (`1.1`, `1.2`, etc.)
a critérios verificáveis. Defina no glossário termos técnicos que possam ser
entendidos de mais de uma forma.

Escreva cada critério em **um** molde EARS adequado:

- Sempre: "O sistema DEVE ...".
- Evento: "QUANDO ..., o sistema DEVE ...".
- Estado: "ENQUANTO ..., o sistema DEVE ...".
- Erro: "SE ..., ENTÃO o sistema DEVE ...".
- Opção: "ONDE ... estiver habilitado, o sistema DEVE ...".
- Composto, só quando necessário: opção → estado → evento/erro → resposta.

Cubra casos de erro e limites relevantes. Quando houver parser ou serializador,
declare a ida e volta como requisito observável. Apresente os requisitos e
**espere a aprovação ou ajustes**. Não trate silêncio como aprovação.

## Design: como atender aos requisitos aprovados

Depois da aprovação, proponha arquitetura e fluxo de dados, componentes e
interfaces tocados, modelo de dados, tratamento de erros, segurança e testes
pertinentes. Ligue decisões aos IDs dos requisitos e explique alternativas
rejeitadas quando houver trade-off real. Cite arquivos e fontes realmente lidos;
um diagrama Mermaid só entra se esclarecer uma relação difícil de explicar.

Converta critérios adequados em propriedades de corretude testáveis. Para UI,
CRUD simples ou infraestrutura, testes de exemplo podem ser suficientes; não
invente propriedades universais só para preencher seção. Apresente o design e
**espere a aprovação ou ajustes** antes das tarefas. Se o design mudar um
requisito, volte e peça aprovação da versão corrigida.

## Tarefas: execução rastreável

Só depois do design aprovado, gere checklist de implementação. Use no máximo
dois níveis (`1.`, `1.1`); cada item deve ser uma alteração de código ou teste
que o agente possa executar. Inclua teste de regressão primeiro em bugfixes.
Subtarefas de teste podem ser opcionais com `- [ ]*`, mas não torne opcional o
teste que prova um requisito crítico. Acrescente `_Requisitos: 1.1, 2.3_` logo
abaixo do item correspondente. Todo requisito aprovado deve aparecer em ao
menos uma tarefa; nenhuma tarefa deve depender de requisito inventado. Inclua
checkpoints de testes entre blocos quando fizer sentido, sem criar tarefa de
"reunir", "aprovar" ou "fazer deploy".

Apresente o checklist para ajuste. Depois da aprovação, chame `criar_plano`
uma vez: `nome` identifica a spec; `contexto` contém os **requisitos e o
design aprovados**, com seus títulos e IDs; `tarefas` contém as linhas prontas
do checklist, inclusive `_Requisitos:`. A ferramenta grava `contexto.md` e
`tarefas.md` no projeto e devolve o caminho. Não prometa `requirements.md` ou
`design.md` separados: o contrato atual de `criar_plano` não os cria. Não use
`executar_python` nem `escrever_arquivo` para fabricar os arquivos internos do
plano. Antes de recriar um plano com o mesmo nome, use `ver_plano` para não
sobrescrever trabalho existente. Criar o plano propõe a execução; começar a
executar continua sujeito à aprovação no card.
