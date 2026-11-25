---
description: Inicia uma nova demanda em projeto privado Conn2Flow. Use quando a tarefa for nova, quando o split entre repositório privado e conn2flow ainda estiver nebuloso, ou quando um escopo local em project/ puder controlar a rodada.
disable-model-invocation: true
argument-hint: [demanda]
---

# Kickoff de projeto privado

Trate `$ARGUMENTS` como a demanda nova a ser coordenada e executada.

## Antes de agir

1. Identifique a âncora mais concreta da tarefa: arquivo, módulo, erro, comportamento, tela, comando, spec, batch ou frente local.
2. Se o split entre privado e `conn2flow` estiver em dúvida, carregue `private-project-context`.
3. Se a tarefa estiver ancorada em `project/<frente>/` com artefatos locais de SDD, carregue `project-sdd-context`.
4. Se tocar `gestor/**/*.php`, carregue `gestor-module-integration`.
5. Se a etapa dominante for ambiente, logs, Docker, JWT, Phinx ou DB, carregue `local-validation`.
6. Se a etapa dominante for testes locais do ecossistema Conn2Flow, carregue `local-tests`.

## Como conduzir

1. Classifique cedo: privado apenas, core apenas ou split.
2. Leia apenas o contexto mínimo necessário para formar uma hipótese local falsificável.
3. Parta para a menor mudança plausível assim que houver âncora suficiente.
4. Valide no menor escopo possível logo após a primeira edição substantiva.
5. Se a tarefa crescer, mantenha batches pequenos e não empilhe contexto ad hoc.

## Entrada atual

$ARGUMENTS