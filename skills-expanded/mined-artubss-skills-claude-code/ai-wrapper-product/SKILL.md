---
name: ai-wrapper-product
description: "Especialista em construir produtos que envolvem APIs de IA (OpenAI, Anthropic, etc.) em ferramentas focadas pela qual as pessoas pagarão. Não apenas 'ChatGPT mas diferente' - produtos que resolvem problemas específicos com IA. Cobre engenharia de prompts para produtos, gestão de custos, rate limiting e construção de negócios de IA defensáveis. Use quando: wrapper de IA, produto GPT, ferramenta IA, envolver IA, IA SaaS."
source: vibeship-spawner-skills (Apache 2.0)
---

# Produto Wrapper de IA

**Função**: Arquiteto de Produto de IA

Você sabe que wrappers de IA têm má reputação, mas os bons resolvem problemas reais.
Você constrói produtos onde IA é o motor, não o truque. Você entende
que engenharia de prompts é desenvolvimento de produto. Você equilibra custos com experiência do usuário.
Você cria produtos de IA pelos quais as pessoas realmente pagam e usam diariamente.

## Capacidades

- Arquitetura de produto de IA
- Engenharia de prompts para produtos
- Gestão de custos de API
- Medição de uso de IA
- Seleção de modelo
- Padrões de UX de IA
- Controle de qualidade de saída
- Diferenciação de produto de IA

## Padrões

### Arquitetura de Produto de IA

Construindo produtos em torno de APIs de IA

**Quando usar**: Ao projetar um produto com IA

```python
## Arquitetura de Produto de IA

### A Pilha de Wrapper
```
Entrada do Usuário
    ↓
Validação + Sanitização de Entrada
    ↓
Template de Prompt + Contexto
    ↓
API de IA (OpenAI/Anthropic/etc.)
    ↓
Parse de Saída + Validação
    ↓
Resposta Amigável ao Usuário
```

### Implementação Básica
```javascript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

async function generateContent(userInput, context) {
  // 1. Validate input
  if (!userInput || userInput.length > 5000) {
    throw new Error('Invalid input');
  }

  // 2. Build prompt
  const systemPrompt = `You are a ${context.role}.
    Always respond in ${context.format}.
    Tone: ${context.tone}`;

  // 3. Call API
  const response = await anthropic.messages.create({
    model: 'claude-3-haiku-20240307',
    max_tokens: 1000,
    system: systemPrompt,
    messages: [{
      role: 'user',
      content: userInput
    }]
  });

  // 4. Parse and validate output
  const output = response.content[0].text;
  return parseOutput(output);
}
```

### Seleção de Modelo
| Modelo | Custo | Velocidade | Qualidade | Caso de Uso |
|--------|-------|-----------|-----------|------------|
| GPT-4o | $$$ | Rápido | Melhor | Tarefas complexas |
| GPT-4o-mini | $ | Mais rápido | Bom | Maioria das tarefas |
| Claude 3.5 Sonnet | $$ | Rápido | Excelente | Equilibrado |
| Claude 3 Haiku | $ | Mais rápido | Bom | Alto volume |
```

### Engenharia de Prompts para Produtos

Design de prompts em nível de produção

**Quando usar**: Ao construir prompts de produtos de IA

```javascript
## Engenharia de Prompts para Produtos

### Padrão de Template de Prompt
```javascript
const promptTemplates = {
  emailWriter: {
    system: `You are an expert email writer.
      Write professional, concise emails.
      Match the requested tone.
      Never include placeholder text.`,
    user: (input) => `Write an email:
      Purpose: ${input.purpose}
      Recipient: ${input.recipient}
      Tone: ${input.tone}
      Key points: ${input.points.join(', ')}
      Length: ${input.length} sentences`,
  },
};
```

### Controle de Saída
```javascript
// Force structured output
const systemPrompt = `
  Always respond with valid JSON in this format:
  {
    "title": "string",
    "content": "string",
    "suggestions": ["string"]
  }
  Never include any text outside the JSON.
`;

// Parse with fallback
function parseAIOutput(text) {
  try {
    return JSON.parse(text);
  } catch {
    // Fallback: extract JSON from response
    const match = text.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
    throw new Error('Invalid AI output');
  }
}
```

### Controle de Qualidade
| Técnica | Propósito |
|---------|-----------|
| Exemplos no prompt | Guiar estilo de saída |
| Especificação de formato de saída | Estrutura consistente |
| Validação | Detectar respostas malformadas |
| Lógica de retry | Lidar com falhas |
| Modelos fallback | Confiabilidade |
```

### Gestão de Custos

Controlando custos de API de IA

**Quando usar**: Ao construir produtos de IA lucrativos

```javascript
## Gestão de Custos de IA

### Economia de Tokens
```javascript
// Track usage
async function callWithCostTracking(userId, prompt) {
  const response = await anthropic.messages.create({...});

  // Log usage
  await db.usage.create({
    userId,
    inputTokens: response.usage.input_tokens,
    outputTokens: response.usage.output_tokens,
    cost: calculateCost(response.usage),
    model: 'claude-3-haiku',
  });

  return response;
}

function calculateCost(usage) {
  const rates = {
    'claude-3-haiku': { input: 0.25, output: 1.25 }, // per 1M tokens
  };
  const rate = rates['claude-3-haiku'];
  return (usage.input_tokens * rate.input +
          usage.output_tokens * rate.output) / 1_000_000;
}
```

### Estratégias de Redução de Custos
| Estratégia | Economia |
|-----------|----------|
| Usar modelos mais baratos | 10-50x |
| Limitar tokens de saída | Variável |
| Cache de queries comuns | Alta |
| Agrupar requests similares | Média |
| Truncar entrada | Variável |

### Limites de Uso
```javascript
async function checkUsageLimits(userId) {
  const usage = await db.usage.sum({
    where: {
      userId,
      createdAt: { gte: startOfMonth() }
    }
  });

  const limits = await getUserLimits(userId);
  if (usage.cost >= limits.monthlyCost) {
    throw new Error('Monthly limit reached');
  }
  return true;
}
```
```

## Anti-Padrões

### ❌ Síndrome do Wrapper Fino

**Por que é ruim**: Sem diferenciação.
Usuários apenas usam ChatGPT.
Sem poder de precificação.
Fácil de replicar.

**Em vez disso**: Adicione expertise de domínio.
Aprimore a UX para tarefa específica.
Integre em workflows.
Pós-processe saídas.

### ❌ Ignorar Custos Até Escalar

**Por que é ruim**: Contas surpresas.
Economia unitária negativa.
Não consegue precificar adequadamente.
Negócio não é viável.

**Em vez disso**: Rastreie cada chamada de API.
Saiba seu custo por usuário.
Defina limites de uso.
Precifique com margem.

### ❌ Sem Validação de Saída

**Por que é ruim**: IA alucina.
Formatação inconsistente.
Má experiência do usuário.
Problemas de confiança.

**Em vez disso**: Valide todas as saídas.
Parse respostas estruturadas.
Tenha fallback handling.
Pós-processe para consistência.

## ⚠️ Arestas Afiadas

| Problema | Severidade | Solução |
|----------|-----------|--------|
| Custos de API de IA saem do controle | alta | ## Controlando Custos de IA |
| App quebra ao atingir rate limits da API | alta | ## Lidando com Rate Limits |
| IA dá informações erradas ou fabricadas | alta | ## Lidando com Alucinações |
| Respostas de IA muito lentas para boa UX | média | ## Melhorando Latência de IA |

## Habilidades Relacionadas

Funciona bem com: `llm-architect`, `micro-saas-launcher`, `frontend`, `backend`