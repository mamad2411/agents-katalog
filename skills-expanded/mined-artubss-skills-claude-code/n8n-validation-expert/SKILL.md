---
name: n8n-validation-expert
description: Interprete erros de validação e guie o conserto deles. Use quando encontrar erros de validação, avisos de validação, falsos positivos, problemas de estrutura de operadores ou quando precisar entender resultados de validação. Use também ao perguntar sobre perfis de validação, tipos de erro ou o processo de loop de validação.
---

# n8n Validation Expert

Guia especializado para interpretar e corrigir erros de validação n8n.

---

## Filosofia de Validação

**Valide cedo, valide frequentemente**

Validação é tipicamente iterativa:
- Espere loops de feedback de validação
- Geralmente 2-3 ciclos de validação → correção
- Média: 23s pensando sobre erros, 58s consertando-os

**Insight principal**: Validação é um processo iterativo, não pontual!

---

## Níveis de Severidade de Erro

### 1. Erros (Deve Corrigir)
**Bloqueia execução do workflow** - Deve ser resolvido antes da ativação

**Tipos**:
- `missing_required` - Campo obrigatório não fornecido
- `invalid_value` - Valor não corresponde às opções permitidas
- `type_mismatch` - Tipo de dado incorreto (string em vez de número)
- `invalid_reference` - Nó referenciado não existe
- `invalid_expression` - Erro de sintaxe de expressão

**Exemplo**:
```json
{
  "type": "missing_required",
  "property": "channel",
  "message": "Channel name is required",
  "fix": "Provide a channel name (lowercase, no spaces, 1-80 characters)"
}
```

### 2. Avisos (Deveria Corrigir)
**Não bloqueia execução** - Workflow pode ser ativado mas pode ter problemas

**Tipos**:
- `best_practice` - Recomendado mas não obrigatório
- `deprecated` - Usando API/recurso antigo
- `performance` - Possível problema de performance

**Exemplo**:
```json
{
  "type": "best_practice",
  "property": "errorHandling",
  "message": "Slack API can have rate limits",
  "suggestion": "Add onError: 'continueRegularOutput' with retryOnFail"
}
```

### 3. Sugestões (Opcional)
**Legal ter** - Melhorias que poderiam aprimorar o workflow

**Tipos**:
- `optimization` - Poderia ser mais eficiente
- `alternative` - Forma melhor de atingir o mesmo resultado

---

## O Loop de Validação

### Padrão da Telemetria
**7.841 ocorrências** deste padrão:

```
1. Configurar nó
   ↓
2. validate_node_operation (23 segundos pensando sobre erros)
   ↓
3. Ler mensagens de erro com atenção
   ↓
4. Corrigir erros
   ↓
5. validate_node_operation novamente (58 segundos consertando)
   ↓
6. Repetir até válido (geralmente 2-3 iterações)
```

### Exemplo
```javascript
// Iteração 1
let config = {
  resource: "channel",
  operation: "create"
};

const result1 = validate_node_operation({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Error: Missing "name"

// ⏱️  23 segundos pensando...

// Iteração 2
config.name = "general";

const result2 = validate_node_operation({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Error: Missing "text"

// ⏱️  58 segundos consertando...

// Iteração 3
config.text = "Hello!";

const result3 = validate_node_operation({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"
});
// → Valid! ✅
```

**Isso é normal!** Não se desanime com múltiplas iterações.

---

## Perfis de Validação

Escolha o perfil certo para seu estágio:

### minimal
**Use quando**: Verificações rápidas durante edição

**Valida**:
- Apenas campos obrigatórios
- Estrutura básica

**Prós**: Mais rápido, mais permissivo
**Contras**: Pode perder problemas

### runtime (RECOMENDADO)
**Use quando**: Validação pré-deployment

**Valida**:
- Campos obrigatórios
- Tipos de valor
- Valores permitidos
- Dependências básicas

**Prós**: Balanceado, pega erros reais
**Contras**: Alguns casos extremos perdidos

**Este é o perfil recomendado para a maioria dos casos de uso**

### ai-friendly
**Use quando**: Configurações geradas por IA

**Valida**:
- O mesmo que runtime
- Reduz falsos positivos
- Mais tolerante com problemas menores

**Prós**: Menos ruído para workflows IA
**Contras**: Pode permitir algumas configs questionáveis

### strict
**Use quando**: Deployment em produção, workflows críticos

**Valida**:
- Tudo
- Best practices
- Preocupações de performance
- Problemas de segurança

**Prós**: Máxima segurança
**Contras**: Muitos avisos, alguns falsos positivos

---

## Tipos de Erro Comuns

### 1. missing_required
**O que significa**: Um campo obrigatório não foi fornecido

**Como corrigir**:
1. Use `get_node_essentials` para ver campos obrigatórios
2. Adicione o campo faltante à sua configuração
3. Forneça um valor apropriado

**Exemplo**:
```javascript
// Erro
{
  "type": "missing_required",
  "property": "channel",
  "message": "Channel name is required"
}

// Correção
config.channel = "#general";
```

### 2. invalid_value
**O que significa**: Valor não corresponde às opções permitidas

**Como corrigir**:
1. Verifique a mensagem de erro para valores permitidos
2. Use `get_node_essentials` para ver opções
3. Atualize para um valor válido

**Exemplo**:
```javascript
// Erro
{
  "type": "invalid_value",
  "property": "operation",
  "message": "Operation must be one of: post, update, delete",
  "current": "send"
}

// Correção
config.operation = "post";  // Use operação válida
```

### 3. type_mismatch
**O que significa**: Tipo de dado incorreto para o campo

**Como corrigir**:
1. Verifique o tipo esperado na mensagem de erro
2. Converta o valor para o tipo correto

**Exemplo**:
```javascript
// Erro
{
  "type": "type_mismatch",
  "property": "limit",
  "message": "Expected number, got string",
  "current": "100"
}

// Correção
config.limit = 100;  // Número, não string
```

### 4. invalid_expression
**O que significa**: Erro de sintaxe de expressão

**Como corrigir**:
1. Use a skill n8n Expression Syntax
2. Verifique se há `{{}}` faltando ou erros de digitação
3. Verifique referências de nó/campo

**Exemplo**:
```javascript
// Erro
{
  "type": "invalid_expression",
  "property": "text",
  "message": "Invalid expression: $json.name",
  "current": "$json.name"
}

// Correção
config.text = "={{$json.name}}";  // Adicione {{}}
```

### 5. invalid_reference
**O que significa**: Nó referenciado não existe

**Como corrigir**:
1. Verifique a ortografia do nome do nó
2. Verifique se o nó existe no workflow
3. Atualize a referência para o nome correto

**Exemplo**:
```javascript
// Erro
{
  "type": "invalid_reference",
  "property": "expression",
  "message": "Node 'HTTP Requets' does not exist",
  "current": "={{$node['HTTP Requets'].json.data}}"
}

// Correção - corrija o typo
config.expression = "={{$node['HTTP Request'].json.data}}";
```

---

## Sistema de Auto-Sanitização

### O que Faz
**Corrige automaticamente problemas comuns de estrutura de operadores** em QUALQUER atualização de workflow

**Executa quando**:
- `n8n_create_workflow`
- `n8n_update_partial_workflow`
- Qualquer operação de salvamento de workflow

### O que Corrige

#### 1. Operadores Binários (Dois Valores)
**Operadores**: equals, notEquals, contains, notContains, greaterThan, lessThan, startsWith, endsWith

**Correção**: Remove propriedade `singleValue` (operadores binários comparam dois valores)

**Antes**:
```javascript
{
  "type": "boolean",
  "operation": "equals",
  "singleValue": true  // ❌ Errado!
}
```

**Depois** (automático):
```javascript
{
  "type": "boolean",
  "operation": "equals"
  // singleValue removido ✅
}
```

#### 2. Operadores Unários (Um Valor)
**Operadores**: isEmpty, isNotEmpty, true, false

**Correção**: Adiciona `singleValue: true` (operadores unários verificam um valor)

**Antes**:
```javascript
{
  "type": "boolean",
  "operation": "isEmpty"
  // singleValue faltando ❌
}
```

**Depois** (automático):
```javascript
{
  "type": "boolean",
  "operation": "isEmpty",
  "singleValue": true  // ✅ Adicionado
}
```

#### 3. Metadados IF/Switch
**Correção**: Adiciona metadados completos `conditions.options` para IF v2.2+ e Switch v3.2+

### O que NÃO PODE Corrigir

#### 1. Conexões Quebradas
Referências a nós que não existem

**Solução**: Use operação `cleanStaleConnections` em `n8n_update_partial_workflow`

#### 2. Incompatibilidades de Contagem de Branches
3 regras de Switch mas apenas 2 conexões de saída

**Solução**: Adicione conexões faltantes ou remova regras extras

#### 3. Estados Corrompidos Paradoxais
API retorna dados corrompidos mas rejeita atualizações

**Solução**: Pode exigir intervenção manual no banco de dados

---

## Falsos Positivos

### O que São?
Avisos de validação que estão tecnicamente "errados" mas aceitáveis no seu caso de uso

### Falsos Positivos Comuns

#### 1. "Missing error handling"
**Aviso**: Nenhum tratamento de erro configurado

**Quando aceitável**:
- Workflows simples onde falhas são óbvias
- Workflows de teste/desenvolvimento
- Notificações não críticas

**Quando corrigir**: Workflows em produção lidando com dados importantes

#### 2. "No retry logic"
**Aviso**: Nó não tenta novamente em caso de falha

**Quando aceitável**:
- APIs com lógica de retry própria
- Operações idempotentes
- Workflows com trigger manual

**Quando corrigir**: Serviços externos instáveis, automação em produção

#### 3. "Missing rate limiting"
**Aviso**: Nenhum rate limiting para chamadas de API

**Quando aceitável**:
- APIs internas sem limites
- Workflows de baixo volume
- APIs com rate limiting no servidor

**Quando corrigir**: APIs públicas, workflows de alto volume

#### 4. "Unbounded query"
**Aviso**: SELECT sem LIMIT

**Quando aceitável**:
- Conjuntos de dados pequenos conhecidos
- Queries de agregação
- Desenvolvimento/teste

**Quando corrigir**: Queries em produção em tabelas grandes

### Reduzindo Falsos Positivos

**Use perfil `ai-friendly`**:
```javascript
validate_node_operation({
  nodeType: "nodes-base.slack",
  config: {...},
  profile: "ai-friendly"  // Menos falsos positivos
})
```

---

## Estrutura de Resultado de Validação

### Resposta Completa
```javascript
{
  "valid": false,
  "errors": [
    {
      "type": "missing_required",
      "property": "channel",
      "message": "Channel name is required",
      "fix": "Provide a channel name (lowercase, no spaces)"
    }
  ],
  "warnings": [
    {
      "type": "best_practice",
      "property": "errorHandling",
      "message": "Slack API can have rate limits",
      "suggestion": "Add onError: 'continueRegularOutput'"
    }
  ],
  "suggestions": [
    {
      "type": "optimization",
      "message": "Consider using batch operations for multiple messages"
    }
  ],
  "summary": {
    "hasErrors": true,
    "errorCount": 1,
    "warningCount": 1,
    "suggestionCount": 1
  }
}
```

### Como Ler

#### 1. Verifique campo `valid`
```javascript
if (result.valid) {
  // ✅ Configuração é válida
} else {
  // ❌ Tem erros - deve corrigir antes do deployment
}
```

#### 2. Corrija erros primeiro
```javascript
result.errors.forEach(error => {
  console.log(`Error in ${error.property}: ${error.message}`);
  console.log(`Fix: ${error.fix}`);
});
```

#### 3. Revise avisos
```javascript
result.warnings.forEach(warning => {
  console.log(`Warning: ${warning.message}`);
  console.log(`Suggestion: ${warning.suggestion}`);
  // Decida se precisa resolver isso
});
```

#### 4. Considere sugestões
```javascript
// Melhorias opcionais
// Não obrigatórias mas podem aprimorar o workflow
```

---

## Validação de Workflow

### validate_workflow (Estrutura)
**Valida workflow inteiro**, não apenas nós individuais

**Verifica**:
1. **Configurações de nó** - Cada nó válido
2. **Conexões** - Sem referências quebradas
3. **Expressões** - Sintaxe e referências válidas
4. **Fluxo** - Estrutura lógica do workflow

**Exemplo**:
```javascript
validate_workflow({
  workflow: {
    nodes: [...],
    connections: {...}
  },
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"
  }
})
```

### Erros Comuns de Workflow

#### 1. Conexões Quebradas
```json
{
  "error": "Connection from 'Transform' to 'NonExistent' - target node not found"
}
```

**Correção**: Remova conexão obsoleta ou crie nó faltante

#### 2. Dependências Circulares
```json
{
  "error": "Circular dependency detected: Node A → Node B → Node A"
}
```

**Correção**: Reestruture workflow para remover loop

#### 3. Múltiplos Nós de Início
```json
{
  "warning": "Multiple trigger nodes found - only one will execute"
}
```

**Correção**: Remova triggers extras ou divida em workflows separados

#### 4. Nós Desconectados
```json
{
  "warning": "Node 'Transform' is not connected to workflow flow"
}
```

**Correção**: Conecte nó ou remova se não usado

---

## Estratégias de Recuperação

### Estratégia 1: Comece do Zero
**Quando**: Configuração está severamente quebrada

**Passos**:
1. Anote campos obrigatórios de `get_node_essentials`
2. Crie configuração válida mínima
3. Adicione features incrementalmente
4. Valide após cada adição

### Estratégia 2: Busca Binária
**Quando**: Workflow valida mas executa incorretamente

**Passos**:
1. Remova metade dos nós
2. Valide e teste
3. Se funciona: problema está nos nós removidos
4. Se falha: problema está nos nós restantes
5. Repita até isolar o problema

### Estratégia 3: Limpar Conexões Obsoletas
**Quando**: Erros "Node not found"

**Passos**:
```javascript
n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [{
    type: "cleanStaleConnections"
  }]
})
```

### Estratégia 4: Use Auto-fix
**Quando**: Erros de estrutura de operador

**Passos**:
```javascript
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: false  // Visualize primeiro
})

// Revise correções, depois aplique
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: true
})
```

---

## Melhores Práticas

### ✅ Faça

- Valide após cada mudança significativa
- Leia mensagens de erro completamente
- Corrija erros iterativamente (um por vez)
- Use perfil `runtime` para pré-deployment
- Verifique campo `valid` antes de assumir sucesso
- Confie em auto-sanitização para problemas de operador
- Use `get_node_essentials` quando incerto sobre requisitos
- Documente falsos positivos que aceita

### ❌ Não Faça

- Pule validação antes da ativação
- Tente corrigir todos os erros de uma vez
- Ignore mensagens de erro
- Use perfil `strict` durante desenvolvimento (muito ruído)
- Assuma que validação passou (sempre verifique resultado)
- Corrija manualmente problemas de auto-sanitização
- Deployment com erros não resolvidos
- Ignore todos os avisos (alguns são importantes!)

---

## Guias Detalhados

Para catálogos de erro abrangentes e exemplos de falsos positivos:

- **[ERROR_CATALOG.md](ERROR_CATALOG.md)** - Lista completa de tipos de erro com exemplos
- **[FALSE_POSITIVES.md](FALSE_POSITIVES.md)** - Quando avisos são aceitáveis

---

## Resumo

**Pontos-chave**:
1. **Validação é iterativa** (média 2-3 ciclos, 23s + 58s)
2. **Erros devem ser corrigidos**, avisos são opcionais
3. **Auto-sanitização** corrige estruturas de operador automaticamente
4. **Use perfil runtime** para validação balanceada
5. **Falsos positivos existem** - aprenda a reconhecê-los
6. **Leia mensagens de erro** - elas contêm orientação de correção

**Processo de Validação**:
1. Valide → Leia erros → Corrija → Valide novamente
2. Repita até válido (geralmente 2-3 iterações)
3. Revise avisos e decida se aceitável
4. Deployment com confiança

**Skills Relacionadas**:
- n8n MCP Tools Expert - Use ferramentas de validação corretamente
- n8n Expression Syntax - Corrija erros de expressão
- n8n Node Configuration - Entenda campos obrigatórios