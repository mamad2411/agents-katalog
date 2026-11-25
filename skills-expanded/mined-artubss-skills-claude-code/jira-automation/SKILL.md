---
name: jira-automation
description: "Automatize tarefas do Jira via Rube MCP (Composio): issues, projetos, sprints, boards, comentários, usuários. Sempre pesquise ferramentas primeiro para esquemas atuais."
risk: critical
source: community
date_added: "2026-02-27"
---

# Automação do Jira via Rube MCP

Automatize operações do Jira através do toolkit Jira do Composio via Rube MCP.

## Pré-requisitos

- Rube MCP deve estar conectado (RUBE_SEARCH_TOOLS disponível)
- Conexão ativa do Jira via `RUBE_MANAGE_CONNECTIONS` com toolkit `jira`
- Sempre chamar `RUBE_SEARCH_TOOLS` primeiro para obter esquemas atuais de ferramentas

## Configuração

**Obter Rube MCP**: Adicione `https://rube.app/mcp` como servidor MCP na configuração do seu cliente. Nenhuma chave de API necessária — basta adicionar o endpoint e funcionará.

1. Verifique se Rube MCP está disponível confirmando que `RUBE_SEARCH_TOOLS` responde
2. Chame `RUBE_MANAGE_CONNECTIONS` com toolkit `jira`
3. Se a conexão não estiver ATIVA, siga o link de autenticação retornado para completar o OAuth do Jira
4. Confirme que o status da conexão mostra ATIVA antes de executar qualquer workflow

## Workflows Principais

### 1. Pesquisar e Filtrar Issues

**Quando usar**: O usuário quer encontrar issues usando JQL ou navegar issues do projeto

**Sequência de ferramentas**:
1. `JIRA_SEARCH_FOR_ISSUES_USING_JQL_POST` - Pesquisar com query JQL [Obrigatório]
2. `JIRA_GET_ISSUE` - Obter detalhes completos de uma issue específica [Opcional]

**Parâmetros principais**:
- `jql`: String de query JQL (ex: `project = PROJ AND status = "In Progress"`)
- `maxResults`: Máximo de resultados por página (padrão 50, máximo 100)
- `startAt`: Offset de paginação
- `fields`: Array de nomes de campos a retornar
- `issueIdOrKey`: Chave de issue como 'PROJ-123' para GET_ISSUE

**Armadilhas**:
- Nomes de campos JQL são case-sensitive e devem corresponder à configuração do Jira
- Campos personalizados usam IDs como `customfield_10001`, não nomes de exibição
- Resultados são paginados; verifique `total` vs `startAt + maxResults` para continuar

### 2. Criar e Editar Issues

**Quando usar**: O usuário quer criar novas issues ou atualizar as existentes

**Sequência de ferramentas**:
1. `JIRA_GET_ALL_PROJECTS` - Listar projetos para encontrar chave do projeto [Pré-requisito]
2. `JIRA_GET_FIELDS` - Obter campos disponíveis e seus IDs [Pré-requisito]
3. `JIRA_CREATE_ISSUE` - Criar uma nova issue [Obrigatório]
4. `JIRA_EDIT_ISSUE` - Atualizar campos em uma issue existente [Opcional]
5. `JIRA_ASSIGN_ISSUE` - Atribuir issue a um usuário [Opcional]

**Parâmetros principais**:
- `project`: Chave do projeto (ex: 'PROJ')
- `issuetype`: Nome do tipo de issue (ex: 'Bug', 'Story', 'Task')
- `summary`: Título da issue
- `description`: Descrição da issue (Atlassian Document Format ou texto simples)
- `issueIdOrKey`: Chave de issue para edições

**Armadilhas**:
- Tipos de issue e campos obrigatórios variam por projeto; use GET_FIELDS para verificar
- Campos personalizados requerem IDs de campo exatos, não nomes de exibição
- Descrição pode precisar de Atlassian Document Format (ADF) para conteúdo rico

### 3. Gerenciar Sprints e Boards

**Quando usar**: O usuário quer trabalhar com boards ágeis, sprints e backlogs

**Sequência de ferramentas**:
1. `JIRA_LIST_BOARDS` - Listar todos os boards [Pré-requisito]
2. `JIRA_LIST_SPRINTS` - Listar sprints para um board [Obrigatório]
3. `JIRA_MOVE_ISSUE_TO_SPRINT` - Mover issue para um sprint [Opcional]
4. `JIRA_CREATE_SPRINT` - Criar um novo sprint [Opcional]

**Parâmetros principais**:
- `boardId`: ID do board de LIST_BOARDS
- `sprintId`: ID do sprint para operações de movimento
- `name`: Nome do sprint para criação
- `startDate`/`endDate`: Datas do sprint em formato ISO

**Armadilhas**:
- Boards e sprints são específicos do Jira Software (não Jira Core)
- Apenas um sprint pode estar ativo por vez por board

### 4. Gerenciar Comentários

**Quando usar**: O usuário quer adicionar ou visualizar comentários em issues

**Sequência de ferramentas**:
1. `JIRA_LIST_ISSUE_COMMENTS` - Listar comentários existentes [Opcional]
2. `JIRA_ADD_COMMENT` - Adicionar comentário a uma issue [Obrigatório]

**Parâmetros principais**:
- `issueIdOrKey`: Chave de issue como 'PROJ-123'
- `body`: Corpo do comentário (suporta ADF para texto formatado)

**Armadilhas**:
- Comentários suportam ADF (Atlassian Document Format) para formatação
- Menções usam IDs de conta, não nomes de usuário

### 5. Gerenciar Projetos e Usuários

**Quando usar**: O usuário quer listar projetos, encontrar usuários ou gerenciar funções de projeto

**Sequência de ferramentas**:
1. `JIRA_GET_ALL_PROJECTS` - Listar todos os projetos [Opcional]
2. `JIRA_GET_PROJECT` - Obter detalhes do projeto [Opcional]
3. `JIRA_FIND_USERS` / `JIRA_GET_ALL_USERS` - Pesquisar usuários [Opcional]
4. `JIRA_GET_PROJECT_ROLES` - Listar funções do projeto [Opcional]
5. `JIRA_ADD_USERS_TO_PROJECT_ROLE` - Adicionar usuário a função [Opcional]

**Parâmetros principais**:
- `projectIdOrKey`: Chave do projeto
- `query`: Texto de pesquisa para FIND_USERS
- `roleId`: ID da função para operações de função

**Armadilhas**:
- Operações de usuário usam IDs de conta (não email ou nome de exibição)
- Funções de projeto diferem de permissões globais

## Padrões Comuns

### Sintaxe JQL

**Operadores comuns**:
- `project = "PROJ"` - Filtrar por projeto
- `status = "In Progress"` - Filtrar por status
- `assignee = currentUser()` - Issues do usuário atual
- `created >= -7d` - Criado nos últimos 7 dias
- `labels = "bug"` - Filtrar por label
- `priority = High` - Filtrar por prioridade
- `ORDER BY created DESC` - Ordenar resultados

**Combinadores**:
- `AND` - Ambas as condições
- `OR` - Uma ou outra condição
- `NOT` - Negar condição

### Paginação

- Use parâmetros `startAt` e `maxResults`
- Verifique `total` na resposta para determinar páginas restantes
- Continue até `startAt + maxResults >= total`

## Armadilhas Conhecidas

**Nomes de Campos**:
- Campos personalizados usam IDs como `customfield_10001`
- Use JIRA_GET_FIELDS para descobrir IDs e nomes de campos
- Nomes de campos em JQL podem diferir de nomes de campos de API

**Autenticação**:
- Jira Cloud usa IDs de conta, não nomes de usuário
- URL do site deve estar configurada corretamente na conexão

## Referência Rápida

| Tarefa | Tool Slug | Parâmetros Principais |
|--------|-----------|----------------------|
| Pesquisar issues (JQL) | JIRA_SEARCH_FOR_ISSUES_USING_JQL_POST | jql, maxResults |
| Obter issue | JIRA_GET_ISSUE | issueIdOrKey |
| Criar issue | JIRA_CREATE_ISSUE | project, issuetype, summary |
| Editar issue | JIRA_EDIT_ISSUE | issueIdOrKey, fields |
| Atribuir issue | JIRA_ASSIGN_ISSUE | issueIdOrKey, accountId |
| Adicionar comentário | JIRA_ADD_COMMENT | issueIdOrKey, body |
| Listar comentários | JIRA_LIST_ISSUE_COMMENTS | issueIdOrKey |
| Listar projetos | JIRA_GET_ALL_PROJECTS | (nenhum) |
| Obter projeto | JIRA_GET_PROJECT | projectIdOrKey |
| Listar boards | JIRA_LIST_BOARDS | (nenhum) |
| Listar sprints | JIRA_LIST_SPRINTS | boardId |
| Mover para sprint | JIRA_MOVE_ISSUE_TO_SPRINT | sprintId, issues |
| Criar sprint | JIRA_CREATE_SPRINT | name, boardId |
| Encontrar usuários | JIRA_FIND_USERS | query |
| Obter campos | JIRA_GET_FIELDS | (nenhum) |
| Listar filtros | JIRA_LIST_FILTERS | (nenhum) |
| Funções do projeto | JIRA_GET_PROJECT_ROLES | projectIdOrKey |
| Versões do projeto | JIRA_GET_PROJECT_VERSIONS | projectIdOrKey |

## Quando Usar

Esta skill é aplicável para executar o workflow ou ações descritas na visão geral.