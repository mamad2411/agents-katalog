---
name: linear-automation
description: "Automatize tarefas do Linear via Rube MCP (Composio): issues, projetos, ciclos, times, labels. Sempre busque ferramentas primeiro para schemas atuais."
risk: critical
source: community
date_added: "2026-02-27"
---

# Automação do Linear via Rube MCP

Automatize operações do Linear através do toolkit Linear do Composio via Rube MCP.

## Pré-requisitos

- Rube MCP deve estar conectado (RUBE_SEARCH_TOOLS disponível)
- Conexão Linear ativa via `RUBE_MANAGE_CONNECTIONS` com toolkit `linear`
- Sempre chame `RUBE_SEARCH_TOOLS` primeiro para obter schemas de ferramentas atuais

## Configuração

**Obtenha o Rube MCP**: Adicione `https://rube.app/mcp` como servidor MCP na configuração do seu cliente. Nenhuma chave de API necessária — apenas adicione o endpoint e funciona.


1. Verifique se Rube MCP está disponível confirmando que `RUBE_SEARCH_TOOLS` responde
2. Chame `RUBE_MANAGE_CONNECTIONS` com toolkit `linear`
3. Se a conexão não estiver ATIVA, siga o link de autenticação retornado para completar o OAuth do Linear
4. Confirme que o status da conexão mostra ATIVO antes de executar qualquer workflow

## Workflows Principais

### 1. Gerenciar Issues

**Quando usar**: Você quer criar, buscar, atualizar ou listar issues do Linear

**Sequência de ferramentas**:
1. `LINEAR_GET_ALL_LINEAR_TEAMS` - Obter IDs de times [Pré-requisito]
2. `LINEAR_LIST_LINEAR_STATES` - Obter estados de workflow para um time [Pré-requisito]
3. `LINEAR_CREATE_LINEAR_ISSUE` - Criar uma nova issue [Opcional]
4. `LINEAR_SEARCH_ISSUES` / `LINEAR_LIST_LINEAR_ISSUES` - Encontrar issues [Opcional]
5. `LINEAR_GET_LINEAR_ISSUE` - Obter detalhes da issue [Opcional]
6. `LINEAR_UPDATE_ISSUE` - Atualizar propriedades da issue [Opcional]

**Parâmetros principais**:
- `team_id`: ID do time (obrigatório para criação)
- `title`: Título da issue
- `description`: Descrição da issue (Markdown suportado)
- `state_id`: ID do estado de workflow
- `assignee_id`: ID do usuário designado
- `priority`: 0 (nenhuma), 1 (urgente), 2 (alta), 3 (média), 4 (baixa)
- `label_ids`: Array de IDs de labels

**Armadilhas**:
- ID do time é obrigatório ao criar issues; use GET_ALL_LINEAR_TEAMS primeiro
- IDs de estado são específicos do time; use LIST_LINEAR_STATES com o time correto
- Priority usa valores inteiros 0-4, não nomes de string

### 2. Gerenciar Projetos

**Quando usar**: Você quer criar ou atualizar projetos do Linear

**Sequência de ferramentas**:
1. `LINEAR_LIST_LINEAR_PROJECTS` - Listar projetos existentes [Opcional]
2. `LINEAR_CREATE_LINEAR_PROJECT` - Criar um novo projeto [Opcional]
3. `LINEAR_UPDATE_LINEAR_PROJECT` - Atualizar detalhes do projeto [Opcional]

**Parâmetros principais**:
- `name`: Nome do projeto
- `description`: Descrição do projeto
- `team_ids`: Array de IDs de times associados ao projeto
- `state`: Estado do projeto (ex: 'planned', 'started', 'completed')

**Armadilhas**:
- Projetos abrangem times; podem ser associados com múltiplos times

### 3. Gerenciar Ciclos

**Quando usar**: Você quer trabalhar com ciclos do Linear (sprints)

**Sequência de ferramentas**:
1. `LINEAR_GET_ALL_LINEAR_TEAMS` - Obter ID do time [Pré-requisito]
2. `LINEAR_GET_CYCLES_BY_TEAM_ID` / `LINEAR_LIST_LINEAR_CYCLES` - Listar ciclos [Obrigatório]

**Parâmetros principais**:
- `team_id`: ID do time para operações de ciclo
- `number`: Número do ciclo

**Armadilhas**:
- Ciclos são específicos do time; sempre escope por team_id

### 4. Gerenciar Labels e Comentários

**Quando usar**: Você quer criar labels ou comentar em issues

**Sequência de ferramentas**:
1. `LINEAR_CREATE_LINEAR_LABEL` - Criar um novo label [Opcional]
2. `LINEAR_CREATE_LINEAR_COMMENT` - Comentar em uma issue [Opcional]
3. `LINEAR_UPDATE_LINEAR_COMMENT` - Editar um comentário [Opcional]

**Parâmetros principais**:
- `name`: Nome do label
- `color`: Cor do label (hex)
- `issue_id`: ID da issue para comentários
- `body`: Corpo do comentário (Markdown)

**Armadilhas**:
- Labels podem ter escopo de time ou escopo de workspace
- Corpo do comentário suporta formatação Markdown

### 5. Queries GraphQL Customizadas

**Quando usar**: Você precisa de queries avançadas não cobertas por ferramentas padrão

**Sequência de ferramentas**:
1. `LINEAR_RUN_QUERY_OR_MUTATION` - Executar GraphQL customizado [Obrigatório]

**Parâmetros principais**:
- `query`: String de query ou mutation GraphQL
- `variables`: Variáveis para a query

**Armadilhas**:
- Requer conhecimento do schema GraphQL do Linear
- Rate limits se aplicam a queries GraphQL

## Padrões Comuns

### Resolução de IDs

**Nome de time -> ID do time**:
```
1. Chame LINEAR_GET_ALL_LINEAR_TEAMS
2. Encontre o time por nome na resposta
3. Extraia o campo id
```

**Nome de estado -> ID de estado**:
```
1. Chame LINEAR_LIST_LINEAR_STATES com team_id
2. Encontre o estado por nome
3. Extraia o campo id
```

### Paginação

- Ferramentas do Linear retornam resultados paginados
- Verifique por cursores de paginação em respostas
- Passe o cursor para a próxima requisição para páginas adicionais

## Armadilhas Conhecidas

**Escopo de Time**:
- Issues, estados e ciclos são específicos do time
- Sempre resolva team_id antes de criar issues

**Valores de Priority**:
- 0 = Sem prioridade, 1 = Urgente, 2 = Alta, 3 = Média, 4 = Baixa
- Use valores inteiros, não nomes de string

## Referência Rápida

| Tarefa | Tool Slug | Parâmetros Principais |
|------|-----------|------------|
| Listar times | LINEAR_GET_ALL_LINEAR_TEAMS | (nenhum) |
| Criar issue | LINEAR_CREATE_LINEAR_ISSUE | team_id, title, description |
| Buscar issues | LINEAR_SEARCH_ISSUES | query |
| Listar issues | LINEAR_LIST_LINEAR_ISSUES | team_id, filters |
| Obter issue | LINEAR_GET_LINEAR_ISSUE | issue_id |
| Atualizar issue | LINEAR_UPDATE_ISSUE | issue_id, fields |
| Listar estados | LINEAR_LIST_LINEAR_STATES | team_id |
| Listar projetos | LINEAR_LIST_LINEAR_PROJECTS | (nenhum) |
| Criar projeto | LINEAR_CREATE_LINEAR_PROJECT | name, team_ids |
| Atualizar projeto | LINEAR_UPDATE_LINEAR_PROJECT | project_id, fields |
| Listar ciclos | LINEAR_LIST_LINEAR_CYCLES | team_id |
| Obter ciclos | LINEAR_GET_CYCLES_BY_TEAM_ID | team_id |
| Criar label | LINEAR_CREATE_LINEAR_LABEL | name, color |
| Criar comentário | LINEAR_CREATE_LINEAR_COMMENT | issue_id, body |
| Atualizar comentário | LINEAR_UPDATE_LINEAR_COMMENT | comment_id, body |
| Listar usuários | LINEAR_LIST_LINEAR_USERS | (nenhum) |
| Usuário atual | LINEAR_GET_CURRENT_USER | (nenhum) |
| Executar GraphQL | LINEAR_RUN_QUERY_OR_MUTATION | query, variables |

## Quando Usar
Esta skill é aplicável para executar o workflow ou ações descritas na visão geral.