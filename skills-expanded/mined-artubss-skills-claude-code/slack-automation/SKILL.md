---
name: slack-automation
description: "Automatize operações de workspace do Slack, incluindo mensagens, busca, gerenciamento de canais e workflows de reações através do toolkit Slack do Composio."
risk: critical
source: community
date_added: "2026-02-27"
---

# Automação do Slack via Rube MCP

Automatize operações de workspace do Slack, incluindo mensagens, busca, gerenciamento de canais e workflows de reações através do toolkit Slack do Composio.

## Pré-requisitos

- Rube MCP deve estar conectado (RUBE_SEARCH_TOOLS disponível)
- Conexão ativa do Slack via `RUBE_MANAGE_CONNECTIONS` com toolkit `slack`
- Sempre chame `RUBE_SEARCH_TOOLS` primeiro para obter os schemas atuais das ferramentas

## Configuração

**Obtenha Rube MCP**: Adicione `https://rube.app/mcp` como servidor MCP na configuração do seu cliente. Nenhuma chave de API necessária — apenas adicione o endpoint e funciona.

1. Verifique se Rube MCP está disponível confirmando que `RUBE_SEARCH_TOOLS` responde
2. Chame `RUBE_MANAGE_CONNECTIONS` com toolkit `slack`
3. Se a conexão não estiver ACTIVE, siga o link de autenticação retornado para completar o OAuth do Slack
4. Confirme se o status da conexão mostra ACTIVE antes de executar qualquer workflow

## Workflows Principais

### 1. Enviar Mensagens para Canais

**Quando usar**: Usuário deseja postar uma mensagem em um canal Slack ou DM

**Sequência de ferramentas**:
1. `SLACK_FIND_CHANNELS` - Resolver nome de canal para ID de canal [Pré-requisito]
2. `SLACK_LIST_ALL_CHANNELS` - Fallback se FIND_CHANNELS retornar resultados vazios/ambíguos [Fallback]
3. `SLACK_FIND_USERS` - Resolver usuário para DMs ou @menções [Opcional]
4. `SLACK_OPEN_DM` - Abrir/reutilizar canal de DM se mensagear um usuário diretamente [Opcional]
5. `SLACK_SEND_MESSAGE` - Postar a mensagem com ID de canal resolvido [Obrigatório]
6. `SLACK_UPDATES_A_SLACK_MESSAGE` - Editar a mensagem postada se correções forem necessárias [Opcional]

**Parâmetros principais**:
- `channel`: ID ou nome do canal (sem prefixo '#')
- `markdown_text`: Campo preferido para mensagens formatadas (suporta cabeçalhos, negrito, itálico, blocos de código)
- `text`: Fallback de texto bruto (deprecado em favor de markdown_text)
- `thread_ts`: Timestamp da mensagem pai para responder em uma thread
- `blocks`: Blocos de layout Block Kit (deprecado, use markdown_text)

**Armadilhas**:
- `SLACK_FIND_CHANNELS` requer parâmetro `query`; sua ausência gera erro "Invalid request data provided"
- `SLACK_SEND_MESSAGE` requer um canal válido mais um de markdown_text/text/blocks/attachments
- Payloads de bloco inválidos retornam error=invalid_blocks (máx 50 blocos)
- Respostas se tornam postagens de nível superior se `thread_ts` for omitido
- Persista `response.data.channel` e `response.data.message.ts` de SEND_MESSAGE para operações de edição/thread

### 2. Buscar Mensagens e Conversas

**Quando usar**: Usuário deseja encontrar mensagens específicas em todo o workspace

**Sequência de ferramentas**:
1. `SLACK_FIND_CHANNELS` - Resolver canal para busca com escopo usando `in:#channel` [Opcional]
2. `SLACK_FIND_USERS` - Resolver usuário para filtro de autor com `from:@user` [Opcional]
3. `SLACK_SEARCH_MESSAGES` - Executar busca por palavra-chave em conversas acessíveis [Obrigatório]
4. `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` - Expandir threads para hits relevantes [Obrigatório]

**Parâmetros principais**:
- `query`: String de busca suportando modificadores (`in:#channel`, `from:@user`, `before:YYYY-MM-DD`, `after:YYYY-MM-DD`, `has:link`, `has:file`)
- `count`: Resultados por página (máx 100), ou total com auto_paginate=true
- `sort`: 'score' (relevância) ou 'timestamp' (cronológico)
- `sort_dir`: 'asc' ou 'desc'

**Armadilhas**:
- A validação falha se `query` estiver ausente/vazio
- `ok=true` ainda pode significar sem resultados (`response.data.messages.total=0`)
- Correspondências estão sob `response.data.messages.matches` (às vezes também em `response.data_preview.messages.matches`)
- `match.text` pode estar vazio/truncado; informações-chave podem aparecer em `matches[].attachments[]`
- Expansão de thread via FETCH_MESSAGE_THREAD pode truncar quando `response.data.has_more=true`; pagine via `response_metadata.next_cursor`

### 3. Gerenciar Canais e Usuários

**Quando usar**: Usuário deseja listar canais, usuários ou informações do workspace

**Sequência de ferramentas**:
1. `SLACK_FETCH_TEAM_INFO` - Validar conectividade e obter identidade do workspace [Obrigatório]
2. `SLACK_LIST_ALL_CHANNELS` - Enumerar canais públicos [Obrigatório]
3. `SLACK_LIST_CONVERSATIONS` - Incluir canais privados e DMs [Opcional]
4. `SLACK_LIST_ALL_USERS` - Listar membros do workspace [Obrigatório]
5. `SLACK_RETRIEVE_CONVERSATION_INFORMATION` - Obter metadados detalhados do canal [Opcional]
6. `SLACK_LIST_USER_GROUPS_FOR_TEAM_WITH_OPTIONS` - Listar grupos de usuários [Opcional]

**Parâmetros principais**:
- `cursor`: Cursor de paginação de `response_metadata.next_cursor`
- `limit`: Resultados por página (padrão varia; defina explicitamente para workspaces grandes)
- `types`: Filtro de tipos de canal ('public_channel', 'private_channel', 'im', 'mpim')

**Armadilhas**:
- Metadados do workspace estão aninhados sob `response.data.team`, não no nível superior
- `SLACK_LIST_ALL_CHANNELS` retorna apenas canais públicos; use `SLACK_LIST_CONVERSATIONS` para cobertura privada/IM
- `SLACK_LIST_ALL_USERS` pode atingir limites de taxa HTTP 429; honre o cabeçalho Retry-After
- Sempre pagine via `response_metadata.next_cursor` até estar vazio; deduplicar por `id`

### 4. Reagir e Gerenciar Threads de Mensagens

**Quando usar**: Usuário deseja adicionar reações ou gerenciar conversas com threads

**Sequência de ferramentas**:
1. `SLACK_SEARCH_MESSAGES` ou `SLACK_FETCH_CONVERSATION_HISTORY` - Encontrar a mensagem alvo [Pré-requisito]
2. `SLACK_ADD_REACTION_TO_AN_ITEM` - Adicionar reação com emoji [Obrigatório]
3. `SLACK_FETCH_ITEM_REACTIONS` - Listar reações em uma mensagem [Opcional]
4. `SLACK_REMOVE_REACTION_FROM_ITEM` - Remover uma reação [Opcional]
5. `SLACK_SEND_MESSAGE` - Responder em thread usando `thread_ts` [Opcional]
6. `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` - Ler thread completa [Opcional]

**Parâmetros principais**:
- `channel`: ID do canal onde a mensagem vive
- `timestamp` / `ts`: Timestamp da mensagem (identificador único como '1234567890.123456')
- `name`: Nome do emoji sem dois-pontos (ex: 'thumbsup', 'wave::skin-tone-3')
- `thread_ts`: Timestamp da mensagem pai para respostas com thread

**Armadilhas**:
- Reações requerem par exato de ID de canal + timestamp de mensagem
- Nomes de emoji usam a convenção de nomenclatura do Slack sem dois-pontos
- `SLACK_FETCH_CONVERSATION_HISTORY` retorna apenas a timeline do canal principal, NÃO respostas com thread
- Use `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` com `thread_ts` da mensagem pai para obter respostas de thread

### 5. Agendar Mensagens

**Quando usar**: Usuário deseja agendar uma mensagem para entrega futura

**Sequência de ferramentas**:
1. `SLACK_FIND_CHANNELS` - Resolver ID de canal [Pré-requisito]
2. `SLACK_SCHEDULE_MESSAGE` - Agendar a mensagem com timestamp `post_at` [Obrigatório]

**Parâmetros principais**:
- `channel`: ID de canal resolvido
- `post_at`: Timestamp Unix para entrega (até 120 dias adiantado)
- `text` / `blocks`: Conteúdo da mensagem

**Armadilhas**:
- Agendamento é limitado a 120 dias adiantado
- `post_at` deve ser um timestamp Unix, não ISO 8601

## Padrões Comuns

### Resolução de ID
Sempre resolva nomes de exibição para IDs antes de operações:
- **Nome de canal -> ID de canal**: `SLACK_FIND_CHANNELS` com parâmetro `query`
- **Nome de usuário -> ID de usuário**: `SLACK_FIND_USERS` com `search_query` ou `email`
- **Canal de DM**: `SLACK_OPEN_DM` com IDs de usuários resolvidos

### Paginação
A maioria dos endpoints de lista usa paginação baseada em cursor:
- Siga `response_metadata.next_cursor` até estar vazio
- Defina valores explícitos de `limit` (ex: 100-200) para paginação confiável
- Deduplicar resultados por `id` entre páginas

### Formatação de Mensagem
- Prefira `markdown_text` sobre `text` ou `blocks` para mensagens formatadas
- Use formato `<@USER_ID>` para mencionar usuários (não @username)
- Use `\n` para quebras de linha em markdown_text

## Armadilhas Conhecidas

- **Resolução de canal**: `SLACK_FIND_CHANNELS` pode retornar resultados vazios se o canal for privado e o bot não foi convidado
- **Limites de taxa**: `SLACK_LIST_ALL_USERS` e outros endpoints de lista podem atingir HTTP 429; honre o cabeçalho Retry-After
- **Respostas aninhadas**: Resultados podem estar aninhados sob `response.data.results[0].response.data` em execuções encapsuladas
- **Thread vs canal**: `SLACK_FETCH_CONVERSATION_HISTORY` retorna apenas timeline principal; use `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` para respostas de thread
- **Edição de mensagem**: Requer tanto `channel` quanto `ts` da mensagem original; persista estes da resposta SEND_MESSAGE
- **Atrasos de busca**: Mensagens postadas recentemente podem não aparecer nos resultados de busca imediatamente
- **Limitações de escopo**: Escopos OAuth ausentes podem causar erros 403; verifique com `SLACK_GET_APP_PERMISSION_SCOPES`

## Referência Rápida

| Tarefa | Tool Slug | Parâmetros Principais |
|--------|-----------|----------------------|
| Encontrar canais | `SLACK_FIND_CHANNELS` | `query` |
| Listar todos os canais | `SLACK_LIST_ALL_CHANNELS` | `limit`, `cursor`, `types` |
| Enviar mensagem | `SLACK_SEND_MESSAGE` | `channel`, `markdown_text` |
| Editar mensagem | `SLACK_UPDATES_A_SLACK_MESSAGE` | `channel`, `ts`, `markdown_text` |
| Buscar mensagens | `SLACK_SEARCH_MESSAGES` | `query`, `count`, `sort` |
| Obter thread | `SLACK_FETCH_MESSAGE_THREAD_FROM_A_CONVERSATION` | `channel`, `ts` |
| Adicionar reação | `SLACK_ADD_REACTION_TO_AN_ITEM` | `channel`, `name`, `timestamp` |
| Encontrar usuários | `SLACK_FIND_USERS` | `search_query` ou `email` |
| Listar usuários | `SLACK_LIST_ALL_USERS` | `limit`, `cursor` |
| Abrir DM | `SLACK_OPEN_DM` | IDs de usuários |
| Agendar mensagem | `SLACK_SCHEDULE_MESSAGE` | `channel`, `post_at`, `text` |
| Obter informações do canal | `SLACK_RETRIEVE_CONVERSATION_INFORMATION` | ID de canal |
| Histórico do canal | `SLACK_FETCH_CONVERSATION_HISTORY` | `channel`, `oldest`, `latest` |
| Informações do workspace | `SLACK_FETCH_TEAM_INFO` | (nenhum) |

## Quando Usar
Esta skill é aplicável para executar o workflow ou ações descritas na visão geral.