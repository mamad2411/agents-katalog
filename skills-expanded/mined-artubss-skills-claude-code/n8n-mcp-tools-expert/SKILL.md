---
name: n8n-mcp-tools-expert
description: Guia especializado para usar efetivamente as ferramentas do MCP n8n-mcp. Use ao buscar nodes, validar configurações, acessar templates, gerenciar workflows ou usar qualquer ferramenta n8n-mcp. Fornece orientação de seleção de ferramentas, formatos de parâmetros e padrões comuns.
---

# Especialista em Ferramentas n8n MCP

Guia completo para usar as ferramentas do servidor MCP n8n-mcp na construção de workflows.

---

## Categorias de Ferramentas

O n8n-mcp fornece **40+ ferramentas** organizadas em categorias:

1. **Node Discovery** → [SEARCH_GUIDE.md](SEARCH_GUIDE.md)
2. **Configuration Validation** → [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md)
3. **Workflow Management** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
4. **Template Library** - Pesquise e acesse 2.653 workflows reais
5. **Documentation** - Obtenha documentação de ferramentas e nodes

---

## Referência Rápida

### Ferramentas Mais Usadas (por taxa de sucesso)

| Ferramenta | Use Quando | Taxa de Sucesso | Velocidade |
|-----------|-----------|-----------------|-----------|
| `search_nodes` | Encontrando nodes por palavra-chave | 99,9% | <20ms |
| `get_node_essentials` | Entendendo operações de node | 91,7% | <10ms |
| `validate_node_operation` | Verificando configurações | Varia | <100ms |
| `n8n_create_workflow` | Criando workflows | 96,8% | 100-500ms |
| `n8n_update_partial_workflow` | Editando workflows (MAIS USADA!) | 99,0% | 50-200ms |
| `validate_workflow` | Verificando workflow completo | 95,5% | 100-500ms |

---

## Guia de Seleção de Ferramentas

### Encontrando o Node Correto

**Fluxo de trabalho**:
```
1. search_nodes({query: "palavra-chave"})
2. get_node_essentials({nodeType: "nodes-base.nome"})
3. [Opcional] get_node_documentation({nodeType: "nodes-base.nome"})
```

**Exemplo**:
```javascript
// Etapa 1: Pesquisa
search_nodes({query: "slack"})
// Retorna: nodes-base.slack

// Etapa 2: Obter detalhes (média de 18s entre etapas)
get_node_essentials({nodeType: "nodes-base.slack"})
// Retorna: operações, propriedades, exemplos
```

**Padrão comum**: pesquisa → essentials (média de 18s)

### Validando Configuração

**Fluxo de trabalho**:
```
1. validate_node_minimal({nodeType, config: {}}) - Verificar campos obrigatórios
2. validate_node_operation({nodeType, config, profile: "runtime"}) - Validação completa
3. [Repetir] Corrigir erros, validar novamente
```

**Padrão comum**: validar → corrigir → validar (23s de análise, 58s de correção por ciclo)

### Gerenciando Workflows

**Fluxo de trabalho**:
```
1. n8n_create_workflow({name, nodes, connections})
2. n8n_validate_workflow({id})
3. n8n_update_partial_workflow({id, operations: [...]})
4. n8n_validate_workflow({id}) novamente
```

**Padrão comum**: atualizações iterativas (56s de média entre edições)

---

## Crítico: Formatos de nodeType

**Dois formatos diferentes** para ferramentas diferentes!

### Formato 1: Ferramentas de Pesquisa/Validação
```javascript
// Use prefixo CURTO
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-base.webhook"
"nodes-langchain.agent"
```

**Ferramentas que usam isso**:
- search_nodes (retorna este formato)
- get_node_essentials
- get_node_info
- validate_node_minimal
- validate_node_operation
- get_property_dependencies

### Formato 2: Ferramentas de Workflow
```javascript
// Use prefixo COMPLETO
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"n8n-nodes-base.webhook"
"@n8n/n8n-nodes-langchain.agent"
```

**Ferramentas que usam isso**:
- n8n_create_workflow
- n8n_update_partial_workflow
- list_node_templates

### Conversão

```javascript
// search_nodes retorna AMBOS os formatos
{
  "nodeType": "nodes-base.slack",          // Para ferramentas de pesquisa/validação
  "workflowNodeType": "n8n-nodes-base.slack"  // Para ferramentas de workflow
}
```

---

## Erros Comuns

### ❌ Erro 1: Formato Incorreto de nodeType

**Problema**: erro "Node not found"

```javascript
❌ get_node_essentials({nodeType: "slack"})  // Faltando prefixo
❌ get_node_essentials({nodeType: "n8n-nodes-base.slack"})  // Prefixo incorreto

✅ get_node_essentials({nodeType: "nodes-base.slack"})  // Correto!
```

### ❌ Erro 2: Usar get_node_info em vez de get_node_essentials

**Problema**: taxa de falha de 20%, resposta lenta, payload gigante

```javascript
❌ get_node_info({nodeType: "nodes-base.slack"})
// Retorna: 100KB+ de dados, 20% de chance de falha

✅ get_node_essentials({nodeType: "nodes-base.slack"})
// Retorna: 5KB de dados focados, 91,7% de sucesso, <10ms
```

**Quando usar get_node_info**:
- Depurando problemas complexos de configuração
- Precisa do schema completo de propriedades
- Explorando recursos avançados

**Alternativas melhores**:
1. get_node_essentials - para lista de operações
2. get_node_documentation - para documentação legível
3. search_node_properties - para propriedade específica

### ❌ Erro 3: Não Usar Perfis de Validação

**Problema**: muitos falsos positivos OU erros reais não detectados

**Perfis**:
- `minimal` - Apenas campos obrigatórios (rápido, permissivo)
- `runtime` - Valores + tipos (recomendado para pré-deploy)
- `ai-friendly` - Reduzir falsos positivos (para configuração por IA)
- `strict` - Validação máxima (para produção)

```javascript
❌ validate_node_operation({nodeType, config})  // Usa padrão

✅ validate_node_operation({nodeType, config, profile: "runtime"})  // Explícito
```

### ❌ Erro 4: Ignorar Auto-Sanitização

**O que acontece**: TODOS os nodes são sanitizados em QUALQUER atualização de workflow

**Auto-correções**:
- Operadores binários (equals, contains) → remove singleValue
- Operadores unários (isEmpty, isNotEmpty) → adiciona singleValue: true
- Nodes IF/Switch → adiciona metadados faltantes

**Não consegue corrigir**:
- Conexões quebradas
- Incompatibilidade de contagem de branches
- Estados corrompidos paradoxais

```javascript
// Após QUALQUER atualização, auto-sanitização é executada em TODOS os nodes
n8n_update_partial_workflow({id, operations: [...]})
// → Automaticamente corrige estruturas de operadores
```

### ❌ Erro 5: Não Usar Smart Parameters

**Problema**: cálculos complexos de sourceIndex para nodes de múltiplas saídas

**Forma antiga** (manual):
```javascript
// Conexão de node IF
{
  type: "addConnection",
  source: "IF",
  target: "Handler",
  sourceIndex: 0  // Qual saída? Difícil de lembrar!
}
```

**Nova forma** (smart parameters):
```javascript
// Node IF - nomes de branches semânticos
{
  type: "addConnection",
  source: "IF",
  target: "True Handler",
  branch: "true"  // Claro e legível!
}

{
  type: "addConnection",
  source: "IF",
  target: "False Handler",
  branch: "false"
}

// Node Switch - números de casos semânticos
{
  type: "addConnection",
  source: "Switch",
  target: "Handler A",
  case: 0
}
```

---

## Padrões de Uso de Ferramentas

### Padrão 1: Node Discovery (Mais Comum)

**Fluxo comum**: média de 18s entre etapas

```javascript
// Etapa 1: Pesquisa (rápido!)
const results = await search_nodes({
  query: "slack",
  mode: "OR",  // Padrão: qualquer palavra corresponde
  limit: 20
});
// → Retorna: nodes-base.slack, nodes-base.slackTrigger

// Etapa 2: Obter detalhes (~18s depois, usuário revisando resultados)
const details = await get_node_essentials({
  nodeType: "nodes-base.slack",
  includeExamples: true  // Obter configs reais de templates
});
// → Retorna: operações, propriedades, metadados
```

### Padrão 2: Loop de Validação

**Ciclo típico**: 23s de análise, 58s de correção

```javascript
// Etapa 1: Validar
const result = await validate_node_operation({
  nodeType: "nodes-base.slack",
  config: {
    resource: "channel",
    operation: "create"
  },
  profile: "runtime"
});

// Etapa 2: Verificar erros (~23s de análise)
if (!result.valid) {
  console.log(result.errors);  // "Missing required field: name"
}

// Etapa 3: Corrigir config (~58s de correção)
config.name = "general";

// Etapa 4: Validar novamente
await validate_node_operation({...});  // Repetir até ficar limpo
```

### Padrão 3: Edição de Workflow

**Ferramenta de atualização mais usada**: 99,0% de taxa de sucesso, 56s de média entre edições

```javascript
// Construção iterativa de workflow (NÃO tudo de uma vez!)
// Edição 1
await n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [{type: "addNode", node: {...}}]
});

// ~56s depois...

// Edição 2
await n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [{type: "addConnection", source: "...", target: "..."}]
});

// ~56s depois...

// Edição 3 (validação)
await n8n_validate_workflow({id: "workflow-id"});
```

---

## Guias Detalhados

### Ferramentas de Node Discovery
Veja [SEARCH_GUIDE.md](SEARCH_GUIDE.md) para:
- search_nodes (99,9% de sucesso)
- get_node_essentials vs get_node_info
- list_nodes por categoria
- search_node_properties para campos específicos

### Ferramentas de Validação
Veja [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) para:
- Perfis de validação explicados
- validate_node_minimal vs validate_node_operation
- validate_workflow estrutura completa
- Sistema de auto-sanitização
- Tratamento de erros de validação

### Gerenciamento de Workflow
Veja [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) para:
- n8n_create_workflow
- n8n_update_partial_workflow (15 tipos de operação!)
- Smart parameters (branch, case)
- Tipos de conexão AI (8 tipos)
- Recuperação cleanStaleConnections

---

## Uso de Templates

### Pesquisar Templates

```javascript
// Pesquisar por palavra-chave
search_templates({
  query: "webhook slack",
  limit: 20
});
// → Retorna: 1.085 templates com metadados

// Obter detalhes do template
get_template({
  templateId: 2947,  // Weather to Slack
  mode: "structure"  // ou "full" para JSON completo
});
```

### Metadados de Template

Templates incluem:
- Complexidade (simple, medium, complex)
- Estimativa de tempo de configuração
- Serviços requeridos
- Categorias e casos de uso
- Contagens de visualização (popularidade)

---

## Ferramentas de Auto-Ajuda

### Obter Documentação de Ferramentas

```javascript
// Listar todas as ferramentas
tools_documentation()

// Detalhes de ferramenta específica
tools_documentation({
  topic: "search_nodes",
  depth: "full"
})
```

### Health Check

```javascript
// Verificar conectividade do servidor MCP
n8n_health_check()
// → Retorna: status, features, API availability, version
```

### Estatísticas de Banco de Dados

```javascript
get_database_statistics()
// → Retorna: 537 nodes, 270 ferramentas AI, 2.653 templates
```

---

## Disponibilidade de Ferramentas

**Sempre Disponível** (sem necessidade de API n8n):
- search_nodes, list_nodes, get_node_essentials ✅
- validate_node_minimal, validate_node_operation ✅
- validate_workflow, get_property_dependencies ✅
- search_templates, get_template, list_tasks ✅
- tools_documentation, get_database_statistics ✅

**Requer API n8n** (N8N_API_URL + N8N_API_KEY):
- n8n_create_workflow ⚠️
- n8n_update_partial_workflow ⚠️
- n8n_validate_workflow (por ID) ⚠️
- n8n_list_workflows, n8n_get_workflow ⚠️
- n8n_trigger_webhook_workflow ⚠️

Se ferramentas de API indisponíveis, use templates e workflows apenas com validação.

---

## Características de Desempenho

| Ferramenta | Tempo de Resposta | Tamanho do Payload | Confiabilidade |
|-----------|------|---------|-----------|
| search_nodes | <20ms | Pequeno | 99,9% |
| list_nodes | <20ms | Pequeno | 99,6% |
| get_node_essentials | <10ms | ~5KB | 91,7% |
| get_node_info | Varia | 100KB+ | 80% ⚠️ |
| validate_node_minimal | <100ms | Pequeno | 97,4% |
| validate_node_operation | <100ms | Médio | Varia |
| validate_workflow | 100-500ms | Médio | 95,5% |
| n8n_create_workflow | 100-500ms | Médio | 96,8% |
| n8n_update_partial_workflow | 50-200ms | Pequeno | 99,0% |

---

## Melhores Práticas

### ✅ Faça

- Use get_node_essentials em vez de get_node_info (91,7% vs 80%)
- Especifique o perfil de validação explicitamente
- Use smart parameters (branch, case) para clareza
- Siga o fluxo pesquisa → essentials → validar workflow
- Itere workflows (média de 56s entre edições)
- Valide após cada mudança significativa
- Use includeExamples: true para configs reais

### ❌ Não Faça

- Use get_node_info a menos que necessário (taxa de falha de 20%!)
- Esqueça o prefixo de nodeType (nodes-base.*)
- Pule perfis de validação (use "runtime")
- Tente construir workflows de uma vez (itere!)
- Ignore o comportamento de auto-sanitização
- Use prefixo completo (n8n-nodes-base.*) com ferramentas de pesquisa

---

## Resumo

**Mais Importante**:
1. Use **get_node_essentials**, não get_node_info (5KB vs 100KB, 91,7% vs 80%)
2. Formatos de nodeType diferem: `nodes-base.*` (pesquisa) vs `n8n-nodes-base.*` (workflows)
3. Especifique **perfis de validação** (runtime recomendado)
4. Use **smart parameters** (branch="true", case=0)
5. **Auto-sanitização** é executada em TODOS os nodes durante atualizações
6. Workflows são construídos **iterativamente** (56s de média entre edições)

**Fluxo Comum**:
1. search_nodes → encontrar node
2. get_node_essentials → entender configuração
3. validate_node_operation → verificar configuração
4. n8n_create_workflow → construir
5. n8n_validate_workflow → verificar
6. n8n_update_partial_workflow → iterar

Para detalhes, veja:
- [SEARCH_GUIDE.md](SEARCH_GUIDE.md) - Node discovery
- [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) - Validação de configuração
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Gerenciamento de workflow

---

**Habilidades Relacionadas**:
- n8n Expression Syntax - Escrever expressões em campos de workflow
- n8n Workflow Patterns - Padrões arquiteturais de templates
- n8n Validation Expert - Interpretar erros de validação
- n8n Node Configuration - Requisitos específicos de operação de node