---
name: n8n-node-configuration
description: Orientação de configuração de nós com conhecimento de operação. Use ao configurar nós, entender dependências de propriedades, determinar campos obrigatórios, escolher entre get_node_essentials e get_node_info, ou aprender padrões comuns de configuração por tipo de nó.
---

# Configuração de Nós n8n

Orientação especializada para configuração de nós com conhecimento de operação e dependências de propriedades.

---

## Filosofia de Configuração

**Divulgação progressiva**: Comece de forma mínima, adicione complexidade conforme necessário

Melhores práticas de configuração:
- get_node_essentials é o padrão de descoberta mais utilizado
- 56 segundos de média entre edições de configuração
- 91,7% de taxa de sucesso com configuração baseada em essenciais

**Insight-chave**: A maioria das configurações precisa apenas de essenciais, não do schema completo!

---

## Conceitos Principais

### 1. Configuração com Conhecimento de Operação

**Nem todos os campos são sempre obrigatórios** - depende da operação!

**Exemplo**: Nó Slack
```javascript
// Para operation='post'
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",  // Obrigatório para post
  "text": "Hello!"        // Obrigatório para post
}

// Para operation='update'
{
  "resource": "message",
  "operation": "update",
  "messageId": "123",     // Obrigatório para update (diferente!)
  "text": "Updated!"      // Obrigatório para update
  // channel NÃO é obrigatório para update
}
```

**Chave**: Recurso + operação determinam quais campos são obrigatórios!

### 2. Dependências de Propriedades

**Campos aparecem/desaparecem baseado em valores de outros campos**

**Exemplo**: Nó HTTP Request
```javascript
// Quando method='GET'
{
  "method": "GET",
  "url": "https://api.example.com"
  // sendBody não é exibido (GET não tem body)
}

// Quando method='POST'
{
  "method": "POST",
  "url": "https://api.example.com",
  "sendBody": true,       // Agora visível!
  "body": {               // Obrigatório quando sendBody=true
    "contentType": "json",
    "content": {...}
  }
}
```

**Mecanismo**: displayOptions controlam a visibilidade dos campos

### 3. Descoberta Progressiva

**Use a ferramenta certa para o trabalho certo**:

1. **get_node_essentials** (91,7% de taxa de sucesso)
   - Visão geral rápida
   - Campos obrigatórios
   - Opções comuns
   - **Use primeiro** - cobre 90% das necessidades

2. **get_property_dependencies** (para nós complexos)
   - Mostra o que os campos dependem uns dos outros
   - Revela requisitos condicionais
   - Use quando essenciais não forem suficientes

3. **get_node_info** (schema completo)
   - Documentação completa
   - Todos os campos possíveis
   - Use quando essenciais + dependências não forem suficientes

---

## Fluxo de Trabalho de Configuração

### Processo Padrão

```
1. Identifique o tipo de nó e operação
   ↓
2. Use get_node_essentials
   ↓
3. Configure os campos obrigatórios
   ↓
4. Valide a configuração
   ↓
5. Se as dependências não forem claras → get_property_dependencies
   ↓
6. Adicione campos opcionais conforme necessário
   ↓
7. Valide novamente
   ↓
8. Implante
```

### Exemplo: Configurando HTTP Request

**Passo 1**: Identifique o que você precisa
```javascript
// Objetivo: POST JSON para API
```

**Passo 2**: Obtenha essenciais
```javascript
const info = get_node_essentials({
  nodeType: "nodes-base.httpRequest"
});

// Retorna: method, url, sendBody, body, authentication obrigatório/opcional
```

**Passo 3**: Configuração mínima
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none"
}
```

**Passo 4**: Valide
```javascript
validate_node_operation({
  nodeType: "nodes-base.httpRequest",
  config,
  profile: "runtime"
});
// → Erro: "sendBody obrigatório para POST"
```

**Passo 5**: Adicione o campo obrigatório
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none",
  "sendBody": true
}
```

**Passo 6**: Valide novamente
```javascript
validate_node_operation({...});
// → Erro: "body obrigatório quando sendBody=true"
```

**Passo 7**: Complete a configuração
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "={{$json.name}}",
      "email": "={{$json.email}}"
    }
  }
}
```

**Passo 8**: Validação final
```javascript
validate_node_operation({...});
// → Válido! ✅
```

---

## get_node_essentials vs get_node_info

### Use get_node_essentials Quando:

**✅ Iniciando configuração** (91,7% de taxa de sucesso)
```javascript
get_node_essentials({
  nodeType: "nodes-base.slack"
});
```

**Retorna**:
- Campos obrigatórios
- Opções comuns
- Exemplos básicos
- Lista de operações

**Rápido**: ~18 segundos de média (da busca aos essenciais)

### Use get_node_info Quando:

**✅ Essenciais insuficientes**
```javascript
get_node_info({
  nodeType: "nodes-base.slack"
});
```

**Retorna**:
- Schema completo
- Todas as propriedades
- Documentação completa
- Opções avançadas

**Mais lento**: Mais dados para processar

### Árvore de Decisão

```
┌─────────────────────────────────┐
│ Iniciando nova configuração?    │
├─────────────────────────────────┤
│ SIM → get_node_essentials       │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Essenciais têm o necessário?    │
├─────────────────────────────────┤
│ SIM → Configure com essenciais  │
│ NÃO → Continuar                 │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Precisa de info de dependência? │
├─────────────────────────────────┤
│ SIM → get_property_dependencies │
│ NÃO → Continuar                 │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Ainda precisa de mais detalhes? │
├─────────────────────────────────┤
│ SIM → get_node_info             │
└─────────────────────────────────┘
```

---

## Mergulho Profundo em Dependências de Propriedades

### Mecanismo displayOptions

**Os campos têm regras de visibilidade**:

```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Tradução**: O campo "body" é exibido quando:
- sendBody = true E
- method = POST, PUT ou PATCH

### Padrões Comuns de Dependência

#### Padrão 1: Alternância Booleana

**Exemplo**: HTTP Request sendBody
```javascript
// sendBody controla a visibilidade de body
{
  "sendBody": true   // → campo body aparece
}
```

#### Padrão 2: Mudança de Operação

**Exemplo**: Slack resource/operation
```javascript
// Operações diferentes → campos diferentes
{
  "resource": "message",
  "operation": "post"
  // → Exibe: channel, text, attachments, etc.
}

{
  "resource": "message",
  "operation": "update"
  // → Exibe: messageId, text (campos diferentes!)
}
```

#### Padrão 3: Seleção de Tipo

**Exemplo**: Condições do nó IF
```javascript
{
  "type": "string",
  "operation": "contains"
  // → Exibe: value1, value2
}

{
  "type": "boolean",
  "operation": "equals"
  // → Exibe: value1, value2, operadores diferentes
}
```

### Usando get_property_dependencies

**Exemplo**:
```javascript
const deps = get_property_dependencies({
  nodeType: "nodes-base.httpRequest"
});

// Retorna árvore de dependências
{
  "dependencies": {
    "body": {
      "shows_when": {
        "sendBody": [true],
        "method": ["POST", "PUT", "PATCH", "DELETE"]
      }
    },
    "queryParameters": {
      "shows_when": {
        "sendQuery": [true]
      }
    }
  }
}
```

**Use isto quando**: A validação falha e você não entende por que um campo está faltando/obrigatório

---

## Padrões Comuns de Nós

### Padrão 1: Nós Resource/Operation

**Exemplos**: Slack, Google Sheets, Airtable

**Estrutura**:
```javascript
{
  "resource": "<entidade>",    // Que tipo de coisa
  "operation": "<ação>",       // O que fazer com ela
  // ... campos específicos da operação
}
```

**Como configurar**:
1. Escolha o recurso
2. Escolha a operação
3. Use get_node_essentials para ver requisitos específicos da operação
4. Configure os campos obrigatórios

### Padrão 2: Nós Baseados em HTTP

**Exemplos**: HTTP Request, Webhook

**Estrutura**:
```javascript
{
  "method": "<HTTP_METHOD>",
  "url": "<endpoint>",
  "authentication": "<tipo>",
  // ... campos específicos do método
}
```

**Dependências**:
- POST/PUT/PATCH → sendBody disponível
- sendBody=true → body obrigatório
- authentication != "none" → credentials obrigatórios

### Padrão 3: Nós de Banco de Dados

**Exemplos**: Postgres, MySQL, MongoDB

**Estrutura**:
```javascript
{
  "operation": "<query|insert|update|delete>",
  // ... campos específicos da operação
}
```

**Dependências**:
- operation="executeQuery" → query obrigatório
- operation="insert" → table + values obrigatórios
- operation="update" → table + values + where obrigatórios

### Padrão 4: Nós de Lógica Condicional

**Exemplos**: IF, Switch, Merge

**Estrutura**:
```javascript
{
  "conditions": {
    "<tipo>": [
      {
        "operation": "<operador>",
        "value1": "...",
        "value2": "..."  // Apenas para operadores binários
      }
    ]
  }
}
```

**Dependências**:
- Operadores binários (equals, contains, etc.) → value1 + value2
- Operadores unários (isEmpty, isNotEmpty) → value1 apenas + singleValue: true

---

## Configuração Específica da Operação

### Exemplos de Nó Slack

#### Postar Mensagem
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",      // Obrigatório
  "text": "Hello!",           // Obrigatório
  "attachments": [],          // Opcional
  "blocks": []                // Opcional
}
```

#### Atualizar Mensagem
```javascript
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890",  // Obrigatório (diferente de post!)
  "text": "Updated!",         // Obrigatório
  "channel": "#general"       // Opcional (pode ser inferido)
}
```

#### Criar Canal
```javascript
{
  "resource": "channel",
  "operation": "create",
  "name": "new-channel",      // Obrigatório
  "isPrivate": false          // Opcional
  // Nota: text NÃO é obrigatório para esta operação
}
```

### Exemplos de Nó HTTP Request

#### Solicitação GET
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpHeaderAuth",
  "sendQuery": true,                    // Opcional
  "queryParameters": {                  // Exibido quando sendQuery=true
    "parameters": [
      {
        "name": "limit",
        "value": "100"
      }
    ]
  }
}
```

#### POST com JSON
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,                     // Obrigatório para POST
  "body": {                             // Obrigatório quando sendBody=true
    "contentType": "json",
    "content": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### Exemplos de Nó IF

#### Comparação de Strings (Binária)
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"              // Binária: precisa de value2
      }
    ]
  }
}
```

#### Verificação de Vazio (Unária)
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.email}}",
        "operation": "isEmpty",
        // Sem value2 - operador unário
        "singleValue": true             // Auto-adicionado por sanitização
      }
    ]
  }
}
```

---

## Tratando Requisitos Condicionais

### Exemplo: Body do HTTP Request

**Cenário**: campo body obrigatório, mas apenas às vezes

**Regra**:
```
body é obrigatório quando:
  - sendBody = true E
  - method IN (POST, PUT, PATCH, DELETE)
```

**Como descobrir**:
```javascript
// Opção 1: Leia o erro de validação
validate_node_operation({...});
// Erro: "body obrigatório quando sendBody=true"

// Opção 2: Verifique dependências
get_property_dependencies({
  nodeType: "nodes-base.httpRequest"
});
// Exibe: body → shows_when: sendBody=[true], method=[POST,PUT,PATCH,DELETE]

// Opção 3: Tente configuração mínima e itere
// Comece sem body, validação dirá se necessário
```

### Exemplo: singleValue do Nó IF

**Cenário**: propriedade singleValue aparece para operadores unários

**Regra**:
```
singleValue deve ser true quando:
  - operation IN (isEmpty, isNotEmpty, true, false)
```

**Boa notícia**: Auto-sanitização corrige isso!

**Verificação manual**:
```javascript
get_property_dependencies({
  nodeType: "nodes-base.if"
});
// Exibe dependências específicas do operador
```

---

## Anti-padrões de Configuração

### ❌ Não Faça: Sobre-configurar Antecipadamente

**Ruim**:
```javascript
// Adicionar todos os campos possíveis
{
  "method": "GET",
  "url": "...",
  "sendQuery": false,
  "sendHeaders": false,
  "sendBody": false,
  "timeout": 10000,
  "ignoreResponseCode": false,
  // ... 20 campos opcionais a mais
}
```

**Bom**:
```javascript
// Comece mínimo
{
  "method": "GET",
  "url": "...",
  "authentication": "none"
}
// Adicione campos apenas quando necessário
```

### ❌ Não Faça: Pule a Validação

**Ruim**:
```javascript
// Configure e implante sem validar
const config = {...};
n8n_update_partial_workflow({...});  // YOLO
```

**Bom**:
```javascript
// Valide antes de implantar
const config = {...};
const result = validate_node_operation({...});
if (result.valid) {
  n8n_update_partial_workflow({...});
}
```

### ❌ Não Faça: Ignore o Contexto da Operação

**Ruim**:
```javascript
// Mesma config para todas as operações Slack
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "..."
}

// Depois trocar operação sem atualizar config
{
  "resource": "message",
  "operation": "update",  // Trocado
  "channel": "#general",  // Campo errado para update!
  "text": "..."
}
```

**Bom**:
```javascript
// Verifique requisitos ao trocar operação
get_node_essentials({
  nodeType: "nodes-base.slack"
});
// Veja o que a operação update precisa (messageId, não channel)
```

---

## Melhores Práticas

### ✅ Faça

1. **Comece com get_node_essentials**
   - 91,7% de taxa de sucesso
   - Mais rápido que get_node_info
   - Suficiente para a maioria das necessidades

2. **Valide iterativamente**
   - Configure → Valide → Corrija → Repita
   - Média de 2-3 iterações é normal
   - Leia os erros de validação com cuidado

3. **Use dependências de propriedades quando preso**
   - Se um campo parece faltando, verifique dependências
   - Entenda o que controla a visibilidade do campo
   - get_property_dependencies revela as regras

4. **Respeite o contexto da operação**
   - Operações diferentes = requisitos diferentes
   - Sempre verifique essenciais ao trocar operação
   - Não assuma que configurações são transferíveis

5. **Confie na auto-sanitização**
   - Estrutura de operador corrigida automaticamente
   - Não adicione/remova singleValue manualmente
   - Metadados IF/Switch adicionados ao salvar

### ❌ Não Faça

1. **Pule direto para get_node_info**
   - Tente essenciais primeiro
   - Apenas escale se necessário
   - Schema completo é avassalador

2. **Configure às cegas**
   - Sempre valide antes de implantar
   - Entenda por que campos são obrigatórios
   - Verifique dependências para campos condicionais

3. **Copie configurações sem entender**
   - Operações diferentes precisam de campos diferentes
   - Valide após copiar
   - Ajuste para novo contexto

4. **Corrija manualmente problemas de auto-sanitização**
   - Deixe auto-sanitização lidar com estrutura de operador
   - Foque na lógica de negócio
   - Salve e deixe o sistema corrigir a estrutura

---

## Referências Detalhadas

Para guias abrangentes em tópicos específicos:

- **[DEPENDENCIES.md](DEPENDENCIES.md)** - Mergulho profundo em dependências de propriedades e displayOptions
- **[OPERATION_PATTERNS.md](OPERATION_PATTERNS.md)** - Padrões comuns de configuração por tipo de nó

---

## Resumo

**Estratégia de Configuração**:
1. Comece com get_node_essentials (91,7% de sucesso)
2. Configure campos obrigatórios para operação
3. Valide a configuração
4. Verifique dependências se preso
5. Itere até válido (média 2-3 ciclos)
6. Implante com confiança

**Princípios-chave**:
- **Com conhecimento de operação**: Operações diferentes = requisitos diferentes
- **Divulgação progressiva**: Comece mínimo, adicione conforme necessário
- **Com conhecimento de dependência**: Entenda as regras de visibilidade de campos
- **Orientado por validação**: Deixe validação guiar configuração

**Habilidades Relacionadas**:
- **Especialista em n8n MCP Tools** - Como usar as ferramentas de descoberta corretamente
- **Especialista em Validação n8n** - Interpretar erros de validação
- **Sintaxe de Expressão n8n** - Configurar campos de expressão
- **Padrões de Workflow n8n** - Aplicar padrões com configuração apropriada