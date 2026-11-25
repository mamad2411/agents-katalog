---
name: n8n-code-javascript
description: Escreva código JavaScript em nós Code do n8n. Use quando estiver escrevendo JavaScript no n8n, usando sintaxe $input/$json/$node, fazendo requisições HTTP com $helpers, trabalhando com datas usando DateTime, resolvendo erros do nó Code ou escolhendo entre modos de Code node.
---

# Nó de Código JavaScript

Orientação especializada para escrever código JavaScript em nós Code do n8n.

---

## Início Rápido

```javascript
// Template básico para nós Code
const items = $input.all();

// Processar dados
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));

return processed;
```

### Regras Essenciais

1. **Escolha o modo "Run Once for All Items"** (recomendado para a maioria dos casos)
2. **Acesse dados**: `$input.all()`, `$input.first()`, ou `$input.item`
3. **CRÍTICO**: Deve retornar formato `[{json: {...}}]`
4. **CRÍTICO**: Dados de webhook estão sob `$json.body` (não diretamente em `$json`)
5. **Built-ins disponíveis**: $helpers.httpRequest(), DateTime (Luxon), $jmespath()

---

## Guia de Seleção de Modo

O nó Code oferece dois modos de execução. Escolha de acordo com seu caso de uso:

### Run Once for All Items (Recomendado - Padrão)

**Use este modo para:** 95% dos casos de uso

- **Como funciona**: Código executa **uma única vez** independente da quantidade de entradas
- **Acesso a dados**: `$input.all()` ou array `items`
- **Melhor para**: Agregação, filtragem, processamento em lote, transformações, chamadas API com todos os dados
- **Performance**: Mais rápido para múltiplos itens (execução única)

```javascript
// Exemplo: Calcular total de todos os itens
const allItems = $input.all();
const total = allItems.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: allItems.length,
    average: total / allItems.length
  }
}];
```

**Quando usar:**
- ✅ Comparar itens em todo o conjunto de dados
- ✅ Calcular totais, médias ou estatísticas
- ✅ Ordenar ou classificar itens
- ✅ Remover duplicatas
- ✅ Construir relatórios agregados
- ✅ Combinar dados de múltiplos itens

### Run Once for Each Item

**Use este modo para:** Casos especializados apenas

- **Como funciona**: Código executa **separadamente** para cada item de entrada
- **Acesso a dados**: `$input.item` ou `$item`
- **Melhor para**: Lógica específica de item, operações independentes, validação por item
- **Performance**: Mais lento para grandes conjuntos de dados (múltiplas execuções)

```javascript
// Exemplo: Adicionar timestamp de processamento a cada item
const item = $input.item;

return [{
  json: {
    ...item.json,
    processed: true,
    processedAt: new Date().toISOString()
  }
}];
```

**Quando usar:**
- ✅ Cada item precisa de chamada API independente
- ✅ Validação por item com tratamento de erro diferente
- ✅ Transformações específicas do item baseadas em propriedades do item
- ✅ Quando itens devem ser processados separadamente por lógica de negócio

**Atalho de Decisão:**
- **Precisa examinar múltiplos itens?** → Use o modo "All Items"
- **Cada item é completamente independente?** → Use o modo "Each Item"
- **Não tem certeza?** → Use o modo "All Items" (você sempre pode fazer loop dentro)

---

## Padrões de Acesso a Dados

### Padrão 1: $input.all() - Mais Comum

**Use quando**: Processar arrays, operações em lote, agregações

```javascript
// Obter todos os itens do nó anterior
const allItems = $input.all();

// Filtrar, mapear, reduzir conforme necessário
const valid = allItems.filter(item => item.json.status === 'active');
const mapped = valid.map(item => ({
  json: {
    id: item.json.id,
    name: item.json.name
  }
}));

return mapped;
```

### Padrão 2: $input.first() - Muito Comum

**Use quando**: Trabalhar com objetos únicos, respostas de API, primeiro a entrar primeiro a sair

```javascript
// Obter apenas o primeiro item
const firstItem = $input.first();
const data = firstItem.json;

return [{
  json: {
    result: processData(data),
    processedAt: new Date().toISOString()
  }
}];
```

### Padrão 3: $input.item - Apenas Modo Each Item

**Use quando**: No modo "Run Once for Each Item"

```javascript
// Item atual no loop (apenas modo Each Item)
const currentItem = $input.item;

return [{
  json: {
    ...currentItem.json,
    itemProcessed: true
  }
}];
```

### Padrão 4: $node - Referenciar Outros Nós

**Use quando**: Precisar de dados de nós específicos no workflow

```javascript
// Obter saída de nó específico
const webhookData = $node["Webhook"].json;
const httpData = $node["HTTP Request"].json;

return [{
  json: {
    combined: {
      webhook: webhookData,
      api: httpData
    }
  }
}];
```

**Veja**: [DATA_ACCESS.md](DATA_ACCESS.md) para guia completo

---

## Crítico: Estrutura de Dados de Webhook

**ERRO MAIS COMUM**: Dados de webhook estão aninhados sob `.body`

```javascript
// ❌ ERRADO - Retornará undefined
const name = $json.name;
const email = $json.email;

// ✅ CORRETO - Dados de webhook estão sob .body
const name = $json.body.name;
const email = $json.body.email;

// Ou com $input
const webhookData = $input.first().json.body;
const name = webhookData.name;
```

**Por quê**: O nó webhook envolve todos os dados de requisição sob a propriedade `body`. Isso inclui dados POST, parâmetros de query e payloads JSON.

**Veja**: [DATA_ACCESS.md](DATA_ACCESS.md) para detalhes completos da estrutura de webhook

---

## Requisitos de Formato de Retorno

**REGRA CRÍTICA**: Sempre retorne array de objetos com propriedade `json`

### Formatos de Retorno Corretos

```javascript
// ✅ Resultado único
return [{
  json: {
    field1: value1,
    field2: value2
  }
}];

// ✅ Múltiplos resultados
return [
  {json: {id: 1, data: 'first'}},
  {json: {id: 2, data: 'second'}}
];

// ✅ Array transformado
const transformed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({
    json: {
      id: item.json.id,
      processed: true
    }
  }));
return transformed;

// ✅ Resultado vazio (quando não houver dados para retornar)
return [];

// ✅ Retorno condicional
if (shouldProcess) {
  return [{json: processedData}];
} else {
  return [];
}
```

### Formatos de Retorno Incorretos

```javascript
// ❌ ERRADO: Objeto sem wrapper de array
return {
  json: {field: value}
};

// ❌ ERRADO: Array sem wrapper json
return [{field: value}];

// ❌ ERRADO: String simples
return "processed";

// ❌ ERRADO: Dados brutos sem mapeamento
return $input.all();  // Falta .map()

// ❌ ERRADO: Estrutura incompleta
return [{data: value}];  // Deveria ser {json: value}
```

**Por que importa**: Nós seguintes esperam formato de array. Formato incorreto causa falha na execução do workflow.

**Veja**: [ERROR_PATTERNS.md](ERROR_PATTERNS.md) #3 para soluções detalhadas de erro

---

## Visão Geral de Padrões Comuns

Com base em workflows de produção, aqui estão os padrões mais úteis:

### 1. Agregação de Dados de Múltiplas Fontes
Combine dados de múltiplas APIs, webhooks ou nós

```javascript
const allItems = $input.all();
const results = [];

for (const item of allItems) {
  const sourceName = item.json.name || 'Unknown';
  // Analisar estrutura específica da fonte
  if (sourceName === 'API1' && item.json.data) {
    results.push({
      json: {
        title: item.json.data.title,
        source: 'API1'
      }
    });
  }
}

return results;
```

### 2. Filtragem com Regex
Extrair padrões, menções ou palavras-chave de texto

```javascript
const pattern = /\b([A-Z]{2,5})\b/g;
const matches = {};

for (const item of $input.all()) {
  const text = item.json.text;
  const found = text.match(pattern);

  if (found) {
    found.forEach(match => {
      matches[match] = (matches[match] || 0) + 1;
    });
  }
}

return [{json: {matches}}];
```

### 3. Transformação e Enriquecimento de Dados
Mapear campos, normalizar formatos, adicionar campos calculados

```javascript
const items = $input.all();

return items.map(item => {
  const data = item.json;
  const nameParts = data.name.split(' ');

  return {
    json: {
      first_name: nameParts[0],
      last_name: nameParts.slice(1).join(' '),
      email: data.email,
      created_at: new Date().toISOString()
    }
  };
});
```

### 4. Filtragem Top N e Ranking
Ordenar e limitar resultados

```javascript
const items = $input.all();

const topItems = items
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 10);

return topItems.map(item => ({json: item.json}));
```

### 5. Agregação e Relatórios
Somar, contar, agrupar dados

```javascript
const items = $input.all();
const total = items.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: items.length,
    average: total / items.length,
    timestamp: new Date().toISOString()
  }
}];
```

**Veja**: [COMMON_PATTERNS.md](COMMON_PATTERNS.md) para 10 padrões de produção detalhados

---

## Prevenção de Erros - Top 5 Equívocos

### #1: Código Vazio ou Falta de Return (Mais Comum)

```javascript
// ❌ ERRADO: Sem statement de return
const items = $input.all();
// ... código de processamento ...
// Esqueceu de retornar!

// ✅ CORRETO: Sempre retornar dados
const items = $input.all();
// ... processamento ...
return items.map(item => ({json: item.json}));
```

### #2: Confusão de Sintaxe de Expressão

```javascript
// ❌ ERRADO: Usando sintaxe de expressão n8n em código
const value = "{{ $json.field }}";

// ✅ CORRETO: Use template literals JavaScript
const value = `${$json.field}`;

// ✅ CORRETO: Acesso direto
const value = $input.first().json.field;
```

### #3: Wrapper de Retorno Incorreto

```javascript
// ❌ ERRADO: Retornando objeto em vez de array
return {json: {result: 'success'}};

// ✅ CORRETO: Wrapper de array obrigatório
return [{json: {result: 'success'}}];
```

### #4: Falta de Verificações de Null

```javascript
// ❌ ERRADO: Quebra se campo não existir
const value = item.json.user.email;

// ✅ CORRETO: Acesso seguro com optional chaining
const value = item.json?.user?.email || 'no-email@example.com';

// ✅ CORRETO: Guard clause
if (!item.json.user) {
  return [];
}
const value = item.json.user.email;
```

### #5: Aninhamento de Body de Webhook

```javascript
// ❌ ERRADO: Acesso direto a dados de webhook
const email = $json.email;

// ✅ CORRETO: Dados de webhook sob .body
const email = $json.body.email;
```

**Veja**: [ERROR_PATTERNS.md](ERROR_PATTERNS.md) para guia completo de erros

---

## Funções Built-in e Helpers

### $helpers.httpRequest()

Fazer requisições HTTP dentro do código:

```javascript
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});

return [{json: {data: response}}];
```

### DateTime (Luxon)

Operações de data e hora:

```javascript
// Hora atual
const now = DateTime.now();

// Formatar datas
const formatted = now.toFormat('yyyy-MM-dd');
const iso = now.toISO();

// Aritmética de data
const tomorrow = now.plus({days: 1});
const lastWeek = now.minus({weeks: 1});

return [{
  json: {
    today: formatted,
    tomorrow: tomorrow.toFormat('yyyy-MM-dd')
  }
}];
```

### $jmespath()

Consultar estruturas JSON:

```javascript
const data = $input.first().json;

// Filtrar array
const adults = $jmespath(data, 'users[?age >= `18`]');

// Extrair campos
const names = $jmespath(data, 'users[*].name');

return [{json: {adults, names}}];
```

**Veja**: [BUILTIN_FUNCTIONS.md](BUILTIN_FUNCTIONS.md) para referência completa

---

## Melhores Práticas

### 1. Sempre Validar Dados de Entrada

```javascript
const items = $input.all();

// Verificar se dados existem
if (!items || items.length === 0) {
  return [];
}

// Validar estrutura
if (!items[0].json) {
  return [{json: {error: 'Formato de entrada inválido'}}];
}

// Continuar processamento...
```

### 2. Usar Try-Catch para Tratamento de Erro

```javascript
try {
  const response = await $helpers.httpRequest({
    url: 'https://api.example.com/data'
  });

  return [{json: {success: true, data: response}}];
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message
    }
  }];
}
```

### 3. Preferir Métodos de Array sobre Loops

```javascript
// ✅ BOM: Abordagem funcional
const processed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({json: {id: item.json.id}}));

// ❌ MAIS LENTO: Loop manual
const processed = [];
for (const item of $input.all()) {
  if (item.json.valid) {
    processed.push({json: {id: item.json.id}});
  }
}
```

### 4. Filtrar Cedo, Processar Tarde

```javascript
// ✅ BOM: Filtrar primeiro para reduzir processamento
const processed = $input.all()
  .filter(item => item.json.status === 'active')  // Reduzir dataset primeiro
  .map(item => expensiveTransformation(item));  // Depois transformar

// ❌ DESPERDÍCIO: Transformar tudo, depois filtrar
const processed = $input.all()
  .map(item => expensiveTransformation(item))  // Desperdiça CPU
  .filter(item => item.json.status === 'active');
```

### 5. Usar Nomes de Variável Descritivos

```javascript
// ✅ BOM: Intenção clara
const activeUsers = $input.all().filter(item => item.json.active);
const totalRevenue = activeUsers.reduce((sum, user) => sum + user.json.revenue, 0);

// ❌ RUIM: Propósito unclear
const a = $input.all().filter(item => item.json.active);
const t = a.reduce((s, u) => s + u.json.revenue, 0);
```

### 6. Depurar com console.log()

```javascript
// Statements de debug aparecem no console do navegador
const items = $input.all();
console.log(`Processando ${items.length} itens`);

for (const item of items) {
  console.log('Dados do item:', item.json);
  // Processar...
}

return result;
```

---

## Quando Usar Code Node

Use Code node quando:
- ✅ Transformações complexas exigindo múltiplas etapas
- ✅ Cálculos customizados ou lógica de negócio
- ✅ Operações recursivas
- ✅ Parsing de resposta de API com estrutura complexa
- ✅ Condicionais multi-passo
- ✅ Agregação de dados entre itens

Considere outros nós quando:
- ❌ Mapeamento simples de campo → Use nó **Set**
- ❌ Filtragem básica → Use nó **Filter**
- ❌ Condicionais simples → Use nó **IF** ou **Switch**
- ❌ Apenas requisições HTTP → Use nó **HTTP Request**

**Code node é excelente em**: Lógica complexa que exigiria encadear muitos nós simples

---

## Integração com Outras Skills

### Funciona Com:

**Sintaxe de Expressão n8n**:
- Expressões usam sintaxe `{{ }}` em outros nós
- Nós Code usam JavaScript direto (sem `{{ }}`)
- Quando usar expressões vs código

**n8n MCP Tools Expert**:
- Como encontrar Code node: `search_nodes({query: "code"})`
- Obter ajuda de configuração: `get_node_essentials("nodes-base.code")`
- Validar código: `validate_node_operation()`

**n8n Node Configuration**:
- Seleção de modo (All Items vs Each Item)
- Seleção de linguagem (JavaScript vs Python)
- Entender dependências de propriedade

**n8n Workflow Patterns**:
- Code nodes em passo de transformação
- Padrão Webhook → Code → API
- Tratamento de erro em workflows

**n8n Validation Expert**:
- Validar configuração de Code node
- Tratar erros de validação
- Auto-corrigir problemas comuns

---

## Checklist de Referência Rápida

Antes de implantar Code nodes, verifique:

- [ ] **Código não está vazio** - Deve ter lógica significativa
- [ ] **Statement de return existe** - Deve retornar array de objetos
- [ ] **Formato de retorno correto** - Cada item: `{json: {...}}`
- [ ] **Acesso a dados correto** - Usando `$input.all()`, `$input.first()`, ou `$input.item`
- [ ] **Sem expressões n8n** - Use template literals JavaScript: `` `${value}` ``
- [ ] **Tratamento de erro** - Guard clauses para entradas null/undefined
- [ ] **Dados de webhook** - Acessar via `.body` se vindo de webhook
- [ ] **Seleção de modo** - "All Items" para a maioria dos casos
- [ ] **Performance** - Preferir map/filter sobre loops manuais
- [ ] **Saída consistente** - Todos os caminhos de código retornam mesma estrutura

---

## Recursos Adicionais

### Arquivos Relacionados
- [DATA_ACCESS.md](DATA_ACCESS.md) - Padrões completos de acesso a dados
- [COMMON_PATTERNS.md](COMMON_PATTERNS.md) - 10 padrões testados em produção
- [ERROR_PATTERNS.md](ERROR_PATTERNS.md) - Top 5 erros e soluções
- [BUILTIN_FUNCTIONS.md](BUILTIN_FUNCTIONS.md) - Referência completa de built-ins

### Documentação n8n
- Guia de Code Node: https://docs.n8n.io/code/code-node/
- Métodos Built-in: https://docs.n8n.io/code-examples/methods-variables-reference/
- Documentação Luxon: https://moment.github.io/luxon/

---

**Pronto para escrever JavaScript em nós Code do n8n!** Comece com transformações simples, use o guia de padrões de erro para evitar erros comuns, e consulte a biblioteca de padrões para exemplos prontos para produção.