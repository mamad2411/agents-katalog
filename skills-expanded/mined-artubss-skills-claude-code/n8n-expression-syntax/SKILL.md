---
name: n8n-expression-syntax
description: Valide a sintaxe de expressões n8n e corrija erros comuns. Use ao escrever expressões n8n, usando sintaxe {{}}, acessar variáveis $json/$node, solucionar erros de expressão ou trabalhar com dados de webhook em workflows.
---

# Sintaxe de Expressões n8n

Guia especializado para escrever expressões n8n corretas em workflows.

---

## Formato de Expressão

Todo conteúdo dinâmico em n8n usa **chaves duplas**:

```
{{expression}}
```

**Exemplos**:
```
✅ {{$json.email}}
✅ {{$json.body.name}}
✅ {{$node["HTTP Request"].json.data}}
❌ $json.email  (sem chaves - tratado como texto literal)
❌ {$json.email}  (chaves simples - inválido)
```

---

## Variáveis Principais

### $json - Saída do Nó Atual

Acesse dados do nó atual:

```javascript
{{$json.fieldName}}
{{$json['field with spaces']}}
{{$json.nested.property}}
{{$json.items[0].name}}
```

### $node - Referencie Outros Nós

Acesse dados de qualquer nó anterior:

```javascript
{{$node["Node Name"].json.fieldName}}
{{$node["HTTP Request"].json.data}}
{{$node["Webhook"].json.body.email}}
```

**Importante**:
- Nomes de nós **devem** estar entre aspas
- Nomes de nós são **sensíveis a maiúsculas/minúsculas**
- Devem corresponder exatamente ao nome do nó no workflow

### $now - Timestamp Atual

Acesse data/hora atual:

```javascript
{{$now}}
{{$now.toFormat('yyyy-MM-dd')}}
{{$now.toFormat('HH:mm:ss')}}
{{$now.plus({days: 7})}}
```

### $env - Variáveis de Ambiente

Acesse variáveis de ambiente:

```javascript
{{$env.API_KEY}}
{{$env.DATABASE_URL}}
```

---

## 🚨 CRÍTICO: Estrutura de Dados de Webhook

**Erro Mais Comum**: Dados de webhook **NÃO** estão na raiz!

### Estrutura de Saída do Nó Webhook

```javascript
{
  "headers": {...},
  "params": {...},
  "query": {...},
  "body": {           // ⚠️ DADOS DO USUÁRIO ESTÃO AQUI!
    "name": "John",
    "email": "john@example.com",
    "message": "Hello"
  }
}
```

### Acesso Correto aos Dados de Webhook

```javascript
❌ ERRADO: {{$json.name}}
❌ ERRADO: {{$json.email}}

✅ CORRETO: {{$json.body.name}}
✅ CORRETO: {{$json.body.email}}
✅ CORRETO: {{$json.body.message}}
```

**Por quê**: O nó webhook encapsula os dados recebidos sob a propriedade `.body` para preservar headers, params e query parameters.

---

## Padrões Comuns

### Acesse Campos Aninhados

```javascript
// Aninhamento simples
{{$json.user.email}}

// Acesso a array
{{$json.data[0].name}}
{{$json.items[0].id}}

// Notação de colchetes para espaços
{{$json['field name']}}
{{$json['user data']['first name']}}
```

### Referencie Outros Nós

```javascript
// Nó sem espaços
{{$node["Set"].json.value}}

// Nó com espaços (comum!)
{{$node["HTTP Request"].json.data}}
{{$node["Respond to Webhook"].json.message}}

// Nó webhook
{{$node["Webhook"].json.body.email}}
```

### Combine Variáveis

```javascript
// Concatenação (automática)
Hello {{$json.body.name}}!

// Em URLs
https://api.example.com/users/{{$json.body.user_id}}

// Em propriedades de objeto
{
  "name": "={{$json.body.name}}",
  "email": "={{$json.body.email}}"
}
```

---

## Quando NÃO Usar Expressões

### ❌ Nós de Código

Nós de código usam acesso direto a **JavaScript**, NÃO expressões!

```javascript
// ❌ ERRADO em nó Code
const email = '={{$json.email}}';
const name = '{{$json.body.name}}';

// ✅ CORRETO em nó Code
const email = $json.email;
const name = $json.body.name;

// Ou usando API de nó Code
const email = $input.item.json.email;
const allItems = $input.all();
```

### ❌ Caminhos de Webhook

```javascript
// ❌ ERRADO
path: "{{$json.user_id}}/webhook"

// ✅ CORRETO
path: "user-webhook"  // Apenas caminhos estáticos
```

### ❌ Campos de Credencial

```javascript
// ❌ ERRADO
apiKey: "={{$env.API_KEY}}"

// ✅ CORRETO
Use o sistema de credenciais n8n, não expressões
```

---

## Regras de Validação

### 1. Sempre Use {{}}

Expressões **devem** ser envolvidas em chaves duplas.

```javascript
❌ $json.field
✅ {{$json.field}}
```

### 2. Use Aspas para Espaços

Nomes de campos ou nós com espaços requerem **notação de colchetes**:

```javascript
❌ {{$json.field name}}
✅ {{$json['field name']}}

❌ {{$node.HTTP Request.json}}
✅ {{$node["HTTP Request"].json}}
```

### 3. Corresponda Nomes Exatos de Nós

Referências de nó são **sensíveis a maiúsculas/minúsculas**:

```javascript
❌ {{$node["http request"].json}}  // minúsculas
❌ {{$node["Http Request"].json}}  // maiúsculas erradas
✅ {{$node["HTTP Request"].json}}  // corresponde exatamente
```

### 4. Sem {{ }} Aninhadas

Não envolva expressões duas vezes:

```javascript
❌ {{{$json.field}}}
✅ {{$json.field}}
```

---

## Erros Comuns

Para catálogo completo de erros com correções, veja [COMMON_MISTAKES.md](COMMON_MISTAKES.md)

### Correções Rápidas

| Erro | Correção |
|------|----------|
| `$json.field` | `{{$json.field}}` |
| `{{$json.field name}}` | `{{$json['field name']}}` |
| `{{$node.HTTP Request}}` | `{{$node["HTTP Request"]}}` |
| `{{{$json.field}}}` | `{{$json.field}}` |
| `{{$json.name}}` (webhook) | `{{$json.body.name}}` |
| `'={{$json.email}}'` (Code node) | `$json.email` |

---

## Exemplos Funcionais

Para exemplos de workflow reais, veja [EXAMPLES.md](EXAMPLES.md)

### Exemplo 1: Webhook para Slack

**Webhook recebe**:
```json
{
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello!"
  }
}
```

**No campo de texto do nó Slack**:
```
New form submission!

Name: {{$json.body.name}}
Email: {{$json.body.email}}
Message: {{$json.body.message}}
```

### Exemplo 2: HTTP Request para Email

**HTTP Request retorna**:
```json
{
  "data": {
    "items": [
      {"name": "Product 1", "price": 29.99}
    ]
  }
}
```

**No nó Email** (referencia HTTP Request):
```
Product: {{$node["HTTP Request"].json.data.items[0].name}}
Price: R${{$node["HTTP Request"].json.data.items[0].price}}
```

### Exemplo 3: Formatar Timestamp

```javascript
// Data atual
{{$now.toFormat('yyyy-MM-dd')}}
// Resultado: 2025-10-20

// Hora
{{$now.toFormat('HH:mm:ss')}}
// Resultado: 14:30:45

// Data e hora completas
{{$now.toFormat('yyyy-MM-dd HH:mm')}}
// Resultado: 2025-10-20 14:30
```

---

## Manipulação de Tipo de Dado

### Arrays

```javascript
// Primeiro item
{{$json.users[0].email}}

// Comprimento do array
{{$json.users.length}}

// Último item
{{$json.users[$json.users.length - 1].name}}
```

### Objetos

```javascript
// Notação de ponto (sem espaços)
{{$json.user.email}}

// Notação de colchetes (com espaços ou dinâmicos)
{{$json['user data'].email}}
```

### Strings

```javascript
// Concatenação (automática)
Hello {{$json.name}}!

// Métodos de string
{{$json.email.toLowerCase()}}
{{$json.name.toUpperCase()}}
```

### Números

```javascript
// Uso direto
{{$json.price}}

// Operações matemáticas
{{$json.price * 1.1}}  // Adiciona 10%
{{$json.quantity + 5}}
```

---

## Padrões Avançados

### Conteúdo Condicional

```javascript
// Operador ternário
{{$json.status === 'active' ? 'Active User' : 'Inactive User'}}

// Valores padrão
{{$json.email || 'no-email@example.com'}}
```

### Manipulação de Data

```javascript
// Adicione dias
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}

// Subtraia horas
{{$now.minus({hours: 24}).toISO()}}

// Defina data específica
{{DateTime.fromISO('2025-12-25').toFormat('MMMM dd, yyyy')}}
```

### Manipulação de String

```javascript
// Substring
{{$json.email.substring(0, 5)}}

// Substituir
{{$json.message.replace('old', 'new')}}

// Dividir e juntar
{{$json.tags.split(',').join(', ')}}
```

---

## Depurando Expressões

### Teste no Editor de Expressões

1. Clique no campo com expressão
2. Abra o editor de expressões (clique no ícone "fx")
3. Veja visualização ao vivo do resultado
4. Procure por erros destacados em vermelho

### Mensagens de Erro Comuns

**"Cannot read property 'X' of undefined"**
→ Objeto pai não existe
→ Verifique seu caminho de dados

**"X is not a function"**
→ Tentando chamar método em não-função
→ Verifique tipo de variável

**Expressão aparece como texto literal**
→ {{ }} faltando
→ Adicione chaves duplas

---

## Auxiliares de Expressão

### Métodos Disponíveis

**String**:
- `.toLowerCase()`, `.toUpperCase()`
- `.trim()`, `.replace()`, `.substring()`
- `.split()`, `.includes()`

**Array**:
- `.length`, `.map()`, `.filter()`
- `.find()`, `.join()`, `.slice()`

**DateTime** (Luxon):
- `.toFormat()`, `.toISO()`, `.toLocal()`
- `.plus()`, `.minus()`, `.set()`

**Number**:
- `.toFixed()`, `.toString()`
- Operações matemáticas: `+`, `-`, `*`, `/`, `%`

---

## Boas Práticas

### ✅ Faça

- Sempre use {{ }} para conteúdo dinâmico
- Use notação de colchetes para nomes de campo com espaços
- Referencie dados de webhook de `.body`
- Use $node para dados de outros nós
- Teste expressões no editor de expressões

### ❌ Não Faça

- Não use expressões em nós Code
- Não esqueça aspas em torno de nomes de nó com espaços
- Não envolva duas vezes com {{ }} extras
- Não assuma que dados de webhook estão na raiz (estão sob .body!)
- Não use expressões em caminhos de webhook ou credenciais

---

## Habilidades Relacionadas

- **Especialista em Ferramentas n8n MCP**: Aprenda como validar expressões usando ferramentas MCP
- **Padrões de Workflow n8n**: Veja expressões em exemplos de workflow reais
- **Configuração de Nó n8n**: Entenda quando expressões são necessárias

---

## Resumo

**Regras Essenciais**:
1. Envolva expressões em {{ }}
2. Dados de webhook estão sob `.body`
3. Sem {{ }} em nós Code
4. Coloque aspas em nomes de nó com espaços
5. Nomes de nó são sensíveis a maiúsculas/minúsculas

**Erros Mais Comuns**:
- {{ }} faltando → Adicione chaves
- `{{$json.name}}` em webhooks → Use `{{$json.body.name}}`
- `{{$json.email}}` em Code → Use `$json.email`
- `{{$node.HTTP Request}}` → Use `{{$node["HTTP Request"]}}`

Para mais detalhes, veja:
- [COMMON_MISTAKES.md](COMMON_MISTAKES.md) - Catálogo completo de erros
- [EXAMPLES.md](EXAMPLES.md) - Exemplos de workflow reais

---

**Precisa de Ajuda?** Referencie a documentação de expressões n8n ou use ferramentas de validação n8n-mcp para verificar suas expressões.