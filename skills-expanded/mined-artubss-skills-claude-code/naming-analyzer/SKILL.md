---
name: naming-analyzer
description: Sugira nomes melhores para variáveis, funções e classes com base em contexto e convenções.
---

# Skill Naming Analyzer

Sugira nomes melhores para variáveis, funções e classes com base em contexto e convenções.

## Instruções

Você é um especialista em convenções de nomes. Quando acionado:

1. **Analise Nomes Existentes**:
   - Variáveis, constantes, funções, métodos
   - Classes, interfaces, tipos
   - Arquivos e diretórios
   - Tabelas e colunas de banco de dados
   - Endpoints de API

2. **Identifique Problemas**:
   - Nomes obscuros ou vagos
   - Abreviações que prejudicam a legibilidade
   - Convenções inconsistentes
   - Nomes enganosos (nome não corresponde ao comportamento)
   - Nomes muito curtos ou muito longos
   - Uso incorreto de notação húngara
   - Variáveis de uma única letra fora de loops

3. **Verifique Convenções**:
   - Convenções específicas da linguagem (camelCase, snake_case, PascalCase)
   - Convenções de framework (componentes React, props Vue)
   - Padrões específicos do projeto
   - Padrões da indústria

4. **Forneça Sugestões**:
   - Nomes alternativos melhores
   - Justificativa para cada sugestão
   - Melhorias de consistência
   - Adequação contextual

## Convenções de Nomenclatura por Linguagem

### JavaScript/TypeScript
- Variáveis/funções: `camelCase`
- Classes/interfaces: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Campos privados: `_prefixoUnderscr` ou `#campoPrivado`
- Booleanos: prefixos `is`, `has`, `can`, `should`

### Python
- Variáveis/funções: `snake_case`
- Classes: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Privados: `_prefixo_underscore`
- Booleanos: prefixos `is_`, `has_`, `can_`

### Java
- Variáveis/métodos: `camelCase`
- Classes/interfaces: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Pacotes: `lowercase`

### Go
- Exportados: `PascalCase`
- Não exportados: `camelCase`
- Acrônimos: Todas maiúsculas (`HTTPServer`, não `HttpServer`)

## Problemas Comuns de Nomenclatura

### Muito Vago
```javascript
// ❌ Ruim - Muito genérico
function process(data) { }
const info = getData();
let temp = x;

// ✓ Bom - Específico e claro
function processPayment(transaction) { }
const userProfile = getUserProfile();
let previousValue = x;
```

### Nomes Enganosos
```javascript
// ❌ Ruim - Nome não corresponde ao comportamento
function getUser(id) {
  const user = fetchUser(id);
  user.lastLogin = Date.now();
  saveUser(user); // Efeito colateral! Não é apenas "obter"
  return user;
}

// ✓ Bom - Nome reflete o comportamento real
function fetchAndUpdateUserLogin(id) {
  const user = fetchUser(id);
  user.lastLogin = Date.now();
  saveUser(user);
  return user;
}
```

### Abreviações
```javascript
// ❌ Ruim - Abreviações pouco claras
const usrCfg = loadConfig();
function calcTtl(arr) { }

// ✓ Bom - Claro e legível
const userConfig = loadConfig();
function calculateTotal(amounts) { }

// ✓ Aceitável - Abreviações bem conhecidas
const htmlElement = document.getElementById('main');
const apiUrl = process.env.API_URL;
```

### Nomenclatura de Booleanos
```javascript
// ❌ Ruim - Estado pouco claro
const login = user.authenticated;
const status = checkUser();

// ✓ Bom - Intenção booleana clara
const isLoggedIn = user.authenticated;
const isUserValid = checkUser();
const hasPermission = user.roles.includes('admin');
const canEditPost = isOwner || isAdmin;
const shouldShowNotification = isEnabled && hasUnread;
```

### Números Mágicos
```javascript
// ❌ Ruim - Constantes sem nome
if (age > 18) { }
setTimeout(callback, 3600000);

// ✓ Bom - Constantes nomeadas
const LEGAL_AGE = 18;
const ONE_HOUR_IN_MS = 60 * 60 * 1000;

if (age > LEGAL_AGE) { }
setTimeout(callback, ONE_HOUR_IN_MS);
```

## Exemplos de Uso

```
@naming-analyzer
@naming-analyzer src/
@naming-analyzer UserService.js
@naming-analyzer --conventions
@naming-analyzer --fix-all
```

## Formato do Relatório

```markdown
# Relatório de Análise de Nomes

## Resumo
- Itens analisados: 156
- Problemas encontrados: 23
- Críticos: 5 (nomes enganosos)
- Maiores: 12 (obscuros/vagos)
- Menores: 6 (violações de convenção)

---

## Problemas Críticos (5)

### src/services/UserService.js:45
**Atual**: `getUser(id)`
**Problema**: Nome da função implica apenas leitura, mas tem efeitos colaterais (atualiza lastLogin)
**Severidade**: Crítico - Enganoso
**Sugestão**: `fetchAndUpdateUserLogin(id)`
**Razão**: O nome deve refletir a mutação

### src/utils/helpers.js:23
**Atual**: `validate(x)`
**Problema**: Nome de parâmetro genérico, pouco claro o que está sendo validado
**Severidade**: Crítico - Muito vago
**Sugestão**: `validateEmail(emailAddress)`
**Razão**: Nomes específicos melhoram a clareza

---

## Problemas Maiores (12)

### src/components/DataList.jsx:12
**Atual**: `const d = new Date()`
**Problema**: Variável de uma única letra em escopo amplo
**Severidade**: Maior
**Sugestão**: `const currentDate = new Date()`
**Razão**: Clareza e pesquisabilidade

### src/api/client.js:67
**Atual**: `function proc(data) {}`
**Problema**: Nome de função abreviado
**Severidade**: Maior
**Sugestão**: `function processApiResponse(data) {}`
**Razão**: Palavras completas são mais legíveis

### src/models/User.js:34
**Atual**: `user.active`
**Problema**: Propriedade booleana sem prefixo
**Severidade**: Maior
**Sugestão**: `user.isActive`
**Razão**: Siga a convenção de nomes booleanos

### src/utils/format.js:89
**Atual**: `const MAX = 100`
**Problema**: Nome de constante genérico
**Severidade**: Maior
**Sugestão**: `const MAX_RETRY_ATTEMPTS = 100`
**Razão**: O propósito específico é mais claro

---

## Problemas Menores (6)

### src/config/settings.js:12
**Atual**: `const API_url = '...'`
**Problema**: Capitalização inconsistente (mistura MAIÚSCULA e minúscula)
**Severidade**: Menor
**Sugestão**: `const API_URL = '...'` ou `const apiUrl = '...'`
**Razão**: Consistência na convenção

### src/helpers/string.js:45
**Atual**: `function strToNum(s) {}`
**Problema**: Função e parâmetro abreviados
**Severidade**: Menor
**Sugestão**: `function stringToNumber(value) {}`
**Razão**: Clareza sobre brevidade

---

## Violações de Convenção

### Prefixos de Booleanos Inconsistentes
**Localizações**: 8 arquivos
**Problema**: Uso misto de `is`, `has`, `can` versus sem prefixo
**Recomendação**: Padronize prefixos booleanos
- Use `is` para estado: `isActive`, `isVisible`
- Use `has` para posse: `hasPermission`, `hasError`
- Use `can` para capacidade: `canEdit`, `canDelete`
- Use `should` para decisões: `shouldRender`, `shouldValidate`

### Convenções de Nomenclatura Mistas
**Localização**: src/legacy/
**Problema**: Mistura de camelCase e snake_case em JavaScript
**Recomendação**: Converta tudo para camelCase para consistência

---

## Renomear Sugerido

### Alta Prioridade (Enganoso ou Crítico)
1. `getUser` → `fetchAndUpdateUserLogin` (src/services/UserService.js:45)
2. `validate` → `validateEmail` (src/utils/helpers.js:23)
3. `process` → `processPaymentTransaction` (src/payment/processor.js:67)

### Prioridade Média (Clareza)
1. `d` → `currentDate` (7 localizações)
2. `temp` → `previousValue` (4 localizações)
3. `data` → `apiResponse` ou mais específico (12 localizações)
4. `arr` → `items`, `values` ou mais específico (8 localizações)

### Prioridade Baixa (Convenção)
1. `active` → `isActive` (12 localizações)
2. `error` → `hasError` (6 localizações)
3. `API_url` → `API_URL` (3 localizações)

---

## Padrões de Nomenclatura a Seguir

### Funções/Métodos
- Verbos: `get`, `set`, `create`, `update`, `delete`, `fetch`, `calculate`, `validate`
- Ação clara: `sendEmail()`, `parseJSON()`, `formatCurrency()`

### Classes
- Substantivos: `UserService`, `PaymentProcessor`, `EmailValidator`
- Evite genéricos: Não use `Manager`, `Helper`, `Utility` a menos que necessário

### Variáveis
- Substantivos ou frases nominais: `user`, `emailAddress`, `totalAmount`
- Descritivo: `userList` não `list`, `activeUsers` não `users2`

### Constantes
- Todas maiúsculas com underscores: `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT`
- Inclua unidades: `CACHE_DURATION_MS`, `MAX_FILE_SIZE_MB`

### Booleanos
- Forma de pergunta: `isValid`, `hasPermission`, `canEdit`
- Afirmativo: `isEnabled` não `isDisabled` (prefira positivo)

---

## Script de Refatoração

Deseja que eu crie um script de refatoração para aplicar essas alterações?
Isso fará:
1. Renomear todos os itens sugeridos
2. Atualizar todas as referências
3. Manter o histórico do git
4. Gerar guia de migração

---

## Melhores Práticas

✓ **FAÇA**:
- Use palavras completas em vez de abreviações
- Seja específico e descritivo
- Siga as convenções da linguagem
- Use padrões consistentes
- Deixe os booleanos óbvios
- Inclua unidades em constantes

✗ **NÃO FAÇA**:
- Use uma única letra (exceto em loops: i, j, k)
- Use nomes vagos (data, info, temp, x)
- Misture convenções de nomenclatura
- Use nomes enganosos
- Abrevie em excesso
- Use notação húngara em código moderno
```

## Árvore de Decisão de Nomenclatura

```
É um booleano?
├─ Sim → Use prefixo is/has/can/should
└─ Não → É uma função?
    ├─ Sim → Use frase verbal (ação)
    └─ Não → É uma classe?
        ├─ Sim → Use substantivo (PascalCase)
        └─ Não → É uma constante?
            ├─ Sim → Use UPPER_SNAKE_CASE
            └─ Não → Use substantivo descritivo (camelCase/snake_case)
```

## Notas

- Priorize clareza sobre brevidade
- Contexto importa (contadores de loop podem ser `i`, `j`)
- Abreviações bem conhecidas são aceitáveis (`html`, `api`, `url`, `id`)
- Consistência dentro de um projeto é mais importante que nomes perfeitos
- Refatore nomes conforme o entendimento melhora
- Use renomeação do IDE para atualizar com segurança todas as referências