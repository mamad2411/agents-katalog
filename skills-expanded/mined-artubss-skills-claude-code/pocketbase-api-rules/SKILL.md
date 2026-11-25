---
name: "PocketBase API Rules"
description: "Regras de API e expressões de filtro para controle de acesso do PocketBase. Use ao definir permissões, escrever expressões de filtro, configurar quem pode acessar o quê ou depurar respostas 403/404. Cobre todos os 5 tipos de regra, sintaxe de filtro, operadores, macros de request/collection e modificadores de campo."
---

# Regras de API e Expressões de Filtro do PocketBase

## Tipos de Regra

Cada collection tem 5 tipos de regra. Cada regra é uma **expressão de filtro** que deve ser avaliada como `true` para que a requisição prossiga.

| Regra | Controla | Bloqueada = | String vazia = |
|-------|----------|-------------|----------------|
| **List** | `GET /api/collections/{name}/records` | apenas superusers | todos podem listar |
| **View** | `GET /api/collections/{name}/records/{id}` | apenas superusers | todos podem visualizar |
| **Create** | `POST /api/collections/{name}/records` | apenas superusers | todos podem criar |
| **Update** | `PATCH /api/collections/{name}/records/{id}` | apenas superusers | todos podem atualizar |
| **Delete** | `DELETE /api/collections/{name}/records/{id}` | apenas superusers | todos podem deletar |

**Crítico**: `null`/bloqueada significa que apenas superusers podem executar a ação (usuários regulares e visitantes são negados). String vazia `""` significa TODOS, incluindo visitantes. Superusers sempre contornam as regras de API integralmente — veja abaixo.

## Bypass de Superuser

Superusers (anteriormente admins) **sempre contornam as regras de API**. As regras se aplicam apenas a registros de autenticação regulares e visitantes.

## Sintaxe de Filtro

### Operadores

| Operador | Significado | Exemplo |
|----------|-------------|---------|
| `=` | Igual | `status = "active"` |
| `!=` | Não igual | `status != "draft"` |
| `>` | Maior que | `count > 5` |
| `>=` | Maior ou igual | `count >= 5` |
| `<` | Menor que | `count < 10` |
| `<=` | Menor ou igual | `count <= 10` |
| `~` | LIKE (contém) | `title ~ "hello"` |
| `!~` | NOT LIKE | `title !~ "spam"` |
| `?=` | Qualquer/tem (array contém) | `tags ?= "TAG_ID"` |
| `?!=` | Nenhum (array não contém) | `tags ?!= "TAG_ID"` |
| `?>` | Qualquer maior que | `scores ?> 90` |
| `?>=` | Qualquer maior ou igual | `scores ?>= 90` |
| `?<` | Qualquer menor que | `scores ?< 10` |
| `?<=` | Qualquer menor ou igual | `scores ?<= 10` |
| `?~` | Qualquer LIKE | `emails ?~ "@gmail.com"` |
| `?!~` | Qualquer NOT LIKE | `emails ?!~ "@test.com"` |

**Crítico**: use `?=` (não `=`) para campos com múltiplos valores (multi-select, multi-relation, multi-file). `=` verifica a string JSON bruta, `?=` verifica valores individuais.

### Operadores Lógicos

```
status = "active" && author = @request.auth.id
status = "active" || status = "featured"
```

Parênteses para agrupamento: `(a = 1 || b = 2) && c = 3`

### Valores

- Strings: `"value"` ou `'value'`
- Números: `123`, `45.67`
- Booleanos: `true`, `false`
- `null` — valor vazio/ausente
- Identificadores: nomes de campos, macros

## Macros de Request (`@request.*`)

Acesse o contexto da requisição atual nas regras:

| Macro | Tipo | Descrição |
|-------|------|-----------|
| `@request.auth.id` | `string` | ID do registro de autenticação atual (vazio se visitante) |
| `@request.auth.email` | `string` | Email do registro de autenticação atual |
| `@request.auth.verified` | `bool` | Se o email está verificado |
| `@request.auth.collectionId` | `string` | ID da collection de autenticação |
| `@request.auth.collectionName` | `string` | Nome da collection de autenticação |
| `@request.auth.*` | `any` | Qualquer campo do registro de autenticação |
| `@request.body.fieldName` | `any` | Valor do campo do corpo da requisição |
| `@request.query.paramName` | `string` | Parâmetro de query da URL |
| `@request.headers.name` | `string` | Header da requisição (chave em minúsculas) |
| `@request.method` | `string` | Método HTTP (GET/POST/PATCH/DELETE) |

### Relações de registro de autenticação

Você pode percorrer relações no registro de autenticação:
```
@request.auth.team.owner = @request.auth.id
```

## Macros de Collection (`@collection.*`)

Buscas entre collections sem joins explícitos:

```
@collection.memberships.user ?= @request.auth.id &&
@collection.memberships.team ?= team
```

Isso verifica se um registro existe na collection `memberships` onde o usuário corresponde ao usuário de autenticação atual e o team corresponde ao campo team do registro atual.

**Nota**: `@collection.*` executa uma subquery EXISTS implícita. É poderoso, mas pode ser lento em grandes conjuntos de dados — adicione índices.

## Modificadores de Campo

Use em regras de create/update para validar comportamentos específicos de campo:

| Modificador | Funciona em | Descrição |
|-------------|------------|-----------|
| `:isset` | `@request.body.*` | True se o campo foi enviado na requisição (mesmo que vazio) |
| `:changed` | campo de registro | True se o valor do campo difere do valor armazenado atual (apenas update) |
| `:length` | `string`/`array` | Retorna o comprimento |
| `:each` | `array` | Aplica a condição a cada elemento |
| `:lower` | `string` | Valor em minúsculas |

### Exemplos

```
// Permitir alterar status apenas se o usuário é o proprietário
status:changed = false || author = @request.auth.id

// Prevenir definir role na criação
@request.body.role:isset = false

// Exigir pelo menos 2 tags
@request.body.tags:length >= 2

// Verificar se cada tag está na lista permitida
@request.body.tags:each ?= @collection.allowed_tags.id
```

## Macros de Datetime

| Macro | Exemplo de saída |
|-------|------------------|
| `@now` | `2024-01-15 10:30:00.000Z` |
| `@second` | `2024-01-15 10:30:00.000Z` |
| `@minute` | `2024-01-15 10:30:00.000Z` |
| `@hour` | `2024-01-15 10:00:00.000Z` |
| `@day` | `2024-01-15 00:00:00.000Z` |
| `@month` | `2024-01-01 00:00:00.000Z` |
| `@year` | `2024-01-01 00:00:00.000Z` |
| `@todayStart` | `2024-01-15 00:00:00.000Z` |
| `@todayEnd` | `2024-01-15 23:59:59.999Z` |
| `@monthStart` | `2024-01-01 00:00:00.000Z` |
| `@monthEnd` | `2024-01-31 23:59:59.999Z` |
| `@yearStart` | `2024-01-01 00:00:00.000Z` |
| `@yearEnd` | `2024-12-31 23:59:59.999Z` |

Aritmética: `@now - 7d`, `@now + 1h`, `@now - 30m`

## `geoDistance()`

Para filtros baseados em localização:

```
geoDistance(lat, lon, 40.7128, -74.0060) <= 10000
```

Argumentos: `geoDistance(latField, lonField, targetLat, targetLon)` — retorna metros.

## Padrões Comuns

### Acesso apenas do proprietário
```
// Regra View/Update/Delete:
author = @request.auth.id
```

### Apenas usuários autenticados
```
@request.auth.id != ""
```

### Apenas usuários verificados
```
@request.auth.verified = true
```

### Acesso baseado em role
```
@request.auth.role = "admin" || author = @request.auth.id
```

### Filiação em team
```
@collection.team_members.user ?= @request.auth.id &&
@collection.team_members.team ?= team
```

### Leitura pública, escrita do proprietário
```
// List/View: ""  (vazio = todos)
// Create: @request.auth.id != ""
// Update/Delete: author = @request.auth.id
```

### Prevenir modificação de campo
```
// Regra Update: prevenir alterar `owner` após criação
owner:changed = false
```

### Acesso com limite de tempo
```
expires > @now
```