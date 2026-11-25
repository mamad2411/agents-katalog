---
name: notion-knowledge-capture
description: Capture conversas e decisões em páginas Notion estruturadas; use ao transformar chats/anotações em entradas de wiki, how-tos, decisões ou FAQs com vinculação apropriada.
metadata:
  short-description: Capture conversas em páginas Notion estruturadas
---

# Captura de Conhecimento

Converta conversas e anotações em páginas Notion estruturadas e vinculáveis para fácil reutilização.

## Início rápido
1) Esclareça o que capturar (decisão, how-to, FAQ, aprendizado, documentação) e o público-alvo.
2) Identifique o banco de dados/template certo em `reference/` (wiki de equipe, how-to, FAQ, registro de decisões, aprendizado, documentação).
3) Extraia contexto anterior do Notion com `Notion:notion-search` → `Notion:notion-fetch` (páginas existentes para atualizar/vincular).
4) Rascunhe a página com `Notion:notion-create-pages` usando o schema do banco de dados; inclua resumo, contexto, links de origem e tags/owners.
5) Vincule de páginas hub e registros relacionados; atualize status/owners com `Notion:notion-update-page` conforme a origem evolui.

## Fluxo de trabalho
### 0) Se alguma chamada MCP falhar porque o Notion MCP não está conectado, faça uma pausa e configure:
1. Adicione o Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Ative o cliente MCP remoto:
   - Defina `[features].rmcp_client = true` em `config.toml` **ou** execute `codex --enable rmcp_client`
3. Faça login com OAuth:
   - `codex mcp login notion`

Após o login bem-sucedido, o usuário terá que reiniciar o codex. Você deve finalizar sua resposta e informá-lo de que, na próxima vez, poderá continuar com a Etapa 1.

### 1) Defina a captura
- Pergunte sobre propósito, público-alvo, atualização e se é novo ou uma atualização.
- Determine o tipo de conteúdo: decisão, how-to, FAQ, entrada de conceito/wiki, aprendizado/nota, página de documentação.

### 2) Localize o destino
- Escolha o banco de dados correto usando os guias em `reference/*-database.md`; confirme propriedades obrigatórias (título, tags, owner, status, data, relações).
- Se houver múltiplos bancos de dados candidatos, pergunte ao usuário qual usar; caso contrário, crie no banco de dados wiki/documentação primário.

### 3) Extraia e estruture
- Extraia fatos, decisões, ações e fundamentação da conversa.
- Para decisões, registre alternativas, fundamentação e resultados.
- Para how-tos/docs, capture etapas, pré-requisitos, links para ativos/código e casos extremos.
- Para FAQs, formule como Q&A com respostas concisas e links para documentação mais profunda.

### 4) Crie/atualize no Notion
- Use `Notion:notion-create-pages` com o `data_source_id` correto; defina propriedades (título, tags, owner, status, datas, relações).
- Use templates em `reference/` para estruturar conteúdo (headers de seção, checklists).
- Se atualizar uma página existente, busque e edite via `Notion:notion-update-page`.

### 5) Vincule e exponha
- Adicione relações/backlinks para páginas hub, specs/docs relacionadas e equipes.
- Adicione um resumo breve/changelog para futuros leitores.
- Se existirem tarefas de acompanhamento, crie tarefas no banco de dados relevante e as vincule.

## Referências e exemplos
- `reference/` — schemas de banco de dados e templates (ex: `team-wiki-database.md`, `how-to-guide-database.md`, `faq-database.md`, `decision-log-database.md`, `documentation-database.md`, `learning-database.md`, `database-best-practices.md`).
- `examples/` — padrões de captura na prática (ex: `decision-capture.md`, `how-to-guide.md`, `conversation-to-faq.md`).