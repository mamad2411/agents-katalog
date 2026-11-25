---
name: notion-spec-to-implementation
description: Transforme especificações do Notion em planos de implementação, tarefas e rastreamento de progresso; use ao implementar PRDs/specs de features e criar planos + tarefas no Notion a partir deles.
metadata:
  short-description: Transforme especificações do Notion em planos de implementação, tarefas e rastreamento de progresso
---

# Spec para Implementação

Converta uma especificação do Notion em planos de implementação vinculados, tarefas e atualizações de status contínuas.

## Início rápido
1) Localize a spec com `Notion:notion-search`, depois busque com `Notion:notion-fetch`.
2) Analise requisitos e ambiguidades usando `reference/spec-parsing.md`.
3) Crie uma página de plano com `Notion:notion-create-pages` (escolha um template: rápido vs. completo).
4) Encontre o banco de dados de tarefas, confirme o schema, depois crie tarefas com `Notion:notion-create-pages`.
5) Vincule spec ↔ plano ↔ tarefas; mantenha o status atualizado com `Notion:notion-update-page`.

## Fluxo de trabalho

### 0) Se alguma chamada MCP falhar porque o Notion MCP não está conectado, pause e configure:
1. Adicione o Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Habilite o cliente MCP remoto:
   - Defina `[features].rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login notion`

Após login bem-sucedido, o usuário terá que reiniciar o codex. Você deve finalizar sua resposta e avisá-lo para que na próxima tentativa possa continuar com a Etapa 1.

### 1) Localize e leia a spec
- Busque primeiro (`Notion:notion-search`); se houver múltiplos resultados, pergunte ao usuário qual usar.
- Busque a página (`Notion:notion-fetch`) e examine requisitos, critérios de aceição, restrições e prioridades. Veja `reference/spec-parsing.md` para padrões de extração.
- Capture lacunas/pressupostos em um bloco de esclarecimentos antes de prosseguir.

### 2) Escolha a profundidade do plano
- Mudança simples → use `reference/quick-implementation-plan.md`.
- Feature multi-fase/migração → use `reference/standard-implementation-plan.md`.
- Crie o plano via `Notion:notion-create-pages`, inclua: visão geral, spec vinculada, resumo de requisitos, fases, dependências/riscos e critérios de sucesso. Vincule novamente à spec.

### 3) Crie tarefas
- Encontre o banco de dados de tarefas (`Notion:notion-search` → `Notion:notion-fetch` para confirmar a fonte de dados e propriedades necessárias). Padrões em `reference/task-creation.md`.
- Dimensione tarefas para 1–2 dias. Use `reference/task-creation-template.md` para conteúdo (contexto, objetivo, critérios de aceição, dependências, recursos).
- Defina propriedades: título/verbo de ação, status, prioridade, relações com spec + plano, data de vencimento/story points/responsável se fornecidos.
- Crie páginas com `Notion:notion-create-pages` usando o `data_source_id` do banco de dados.

### 4) Vincule artefatos
- Plano vincula à spec; tarefas vinculam tanto ao plano quanto à spec.
- Opcionalmente atualize a spec com uma seção "Implementação" curta apontando para o plano e tarefas usando `Notion:notion-update-page`.

### 5) Rastreie o progresso
- Use a cadência em `reference/progress-tracking.md`.
- Publique atualizações com `reference/progress-update-template.md`; feche fases com `reference/milestone-summary-template.md`.
- Mantenha checklists e campos de status em plano/tarefas sincronizados; anote bloqueadores e decisões.

## Referências e exemplos
- `reference/` — padrões de análise, templates de plano/tarefas, cadência de progresso (ex: `spec-parsing.md`, `standard-implementation-plan.md`, `task-creation.md`, `progress-tracking.md`).
- `examples/` — passo a passo completos (ex: `ui-component.md`, `api-feature.md`, `database-migration.md`).