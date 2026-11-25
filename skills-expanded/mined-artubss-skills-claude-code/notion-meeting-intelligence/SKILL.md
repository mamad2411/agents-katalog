---
name: notion-meeting-intelligence
description: Prepare materiais de reunião com contexto Notion e pesquisa Codex; use ao reunir contexto, rascunhar agendas/pré-leituras e personalizar materiais para participantes.
metadata:
  short-description: Prepare reuniões com contexto Notion e agendas personalizadas
---

# Meeting Intelligence

Prepare reuniões buscando contexto Notion, personalizando agendas/pré-leituras e enriquecendo com pesquisa Codex.

## Início rápido
1) Confirme o objetivo da reunião, participantes, data/hora e decisões necessárias.
2) Reúna contexto: busque com `Notion:notion-search`, depois busque com `Notion:notion-fetch` (notas anteriores, especificações, OKRs, decisões).
3) Escolha o template certo via `reference/template-selection-guide.md` (status, decisão, planejamento, retro, 1:1, brainstorming).
4) Rascunhe agenda/pré-leitura em Notion com `Notion:notion-create-pages`, incorporando links de fonte e proprietário/timeboxes.
5) Enriqueça com pesquisa Codex (insights de setor, benchmarks, riscos) e atualize a página com `Notion:notion-update-page` conforme os planos mudam.

## Fluxo de trabalho
### 0) Se alguma chamada MCP falhar porque o Notion MCP não está conectado, pause e configure:
1. Adicione o Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Ative cliente MCP remoto:
   - Defina `[features].rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login notion`

Após login bem-sucedido, o usuário terá que reiniciar codex. Você deve encerrar sua resposta e informá-lo para que, quando tentar novamente, possa continuar na Etapa 1.

### 1) Reúna entradas
- Pergunte pelo objetivo, resultados/decisões desejadas, participantes, duração, data/hora e materiais anteriores.
- Busque Notion por documentos relevantes, notas anteriores, especificações e itens de ação (`Notion:notion-search`), depois busque páginas-chave (`Notion:notion-fetch`).
- Capture bloqueadores/riscos e perguntas em aberto desde o início.

### 2) Escolha o formato
- Status/atualização → template de status.
- Decisão/aprovação → template de decisão.
- Planejamento (sprint/projeto) → template de planejamento.
- Retro/feedback → template de retrospectiva.
- 1:1 → template de um-para-um.
- Ideação → template de brainstorming.
- Use `reference/template-selection-guide.md` para confirmar.

### 3) Construa a agenda/pré-leitura
- Comece pelo template escolhido em `reference/` e adapte seções (contexto, objetivos, agenda, proprietário/tempo por item, decisões, riscos, solicitações de preparação).
- Inclua links para páginas Notion buscadas e qualquer pré-leitura necessária.
- Atribua proprietários para cada item de agenda; chame atenção para timeboxes e saídas esperadas.

### 4) Enriqueça com pesquisa
- Adicione pesquisa Codex concisa onde útil: fatos de mercado/setor, benchmarks, riscos, melhores práticas.
- Mantenha reivindicações citadas com links de fonte; separe fato de opinião.

### 5) Finalize e compartilhe
- Adicione próximos passos e proprietários para acompanhamentos.
- Se tarefas surgirem, crie/vincule tarefas no banco de dados Notion relevante.
- Atualize a página via `Notion:notion-update-page` quando detalhes mudarem; mantenha um changelog breve se houver múltiplas edições.

## Referências e exemplos
- `reference/` — seletor de template e templates de reunião (ex: `template-selection-guide.md`, `status-update-template.md`, `decision-meeting-template.md`, `sprint-planning-template.md`, `one-on-one-template.md`, `retrospective-template.md`, `brainstorming-template.md`).
- `examples/` — preps de reunião ponta a ponta (ex: `executive-review.md`, `project-decision.md`, `sprint-planning.md`, `customer-meeting.md`).