---
name: code-review-checklist
description: "Lista de verificação abrangente para conduzir revisões de código minuciosas, cobrindo funcionalidade, segurança, desempenho e manutenibilidade"
---

# Lista de Verificação para Revisão de Código

## Visão Geral

Fornece uma lista de verificação sistemática para conduzir revisões de código minuciosas. Esta habilidade ajuda revisores a garantir qualidade de código, capturar bugs, identificar problemas de segurança e manter consistência em toda a base de código.

## Quando Usar Esta Habilidade

- Use ao revisar pull requests
- Use ao conduzir auditorias de código
- Use ao estabelecer padrões de revisão de código para um time
- Use ao treinar novos desenvolvedores em práticas de revisão de código
- Use quando quiser garantir que nada seja perdido nas revisões
- Use ao criar documentação de revisão de código

## Como Funciona

### Etapa 1: Entenda o Contexto

Antes de revisar o código, vou ajudar você a entender:
- Qual problema este código resolve?
- Quais são os requisitos?
- Quais arquivos foram alterados e por quê?
- Existem issues ou tickets relacionados?
- Qual é a estratégia de testes?

### Etapa 2: Revise a Funcionalidade

Verifique se o código funciona corretamente:
- Ele resolve o problema declarado?
- Casos extremos são tratados?
- O tratamento de erros é apropriado?
- Existem erros lógicos?
- Ele corresponde aos requisitos?

### Etapa 3: Revise a Qualidade do Código

Avalie a manutenibilidade do código:
- O código é legível e claro?
- Os nomes são descritivos?
- Está adequadamente estruturado?
- As funções/métodos são focadas?
- Há complexidade desnecessária?

### Etapa 4: Revise a Segurança

Verifique se há problemas de segurança:
- As entradas são validadas?
- Os dados sensíveis estão protegidos?
- Existem riscos de SQL injection?
- A autenticação/autorização está correta?
- As dependências são seguras?

### Etapa 5: Revise o Desempenho

Procure por problemas de desempenho:
- Existem loops desnecessários?
- O acesso ao banco de dados está otimizado?
- Existem vazamentos de memória?
- O cache é usado adequadamente?
- Existem problemas de consulta N+1?

### Etapa 6: Revise os Testes

Verifique a cobertura de testes:
- Existem testes para o novo código?
- Os testes cobrem casos extremos?
- Os testes são significativos?
- Todos os testes passam?
- A cobertura de testes é adequada?

## Exemplos

### Exemplo 1: Lista de Verificação de Revisão de Funcionalidade

```markdown
## Revisão de Funcionalidade

### Requisitos
- [ ] O código resolve o problema declarado
- [ ] Todos os critérios de aceitação são atendidos
- [ ] Casos extremos são tratados
- [ ] Casos de erro são tratados
- [ ] Entrada do usuário é validada

### Lógica
- [ ] Sem erros lógicos ou bugs
- [ ] Condições estão corretas (sem erros off-by-one)
- [ ] Loops terminam corretamente
- [ ] Recursão possui casos base apropriados
- [ ] Gerenciamento de estado está correto

### Tratamento de Erros
- [ ] Erros são capturados apropriadamente
- [ ] Mensagens de erro são claras e úteis
- [ ] Erros não expõem informações sensíveis
- [ ] Operações falhadas são revertidas
- [ ] Logging é apropriado

### Exemplos de Problemas a Capturar:

**❌ Ruim - Validação ausente:**
\`\`\`javascript
function createUser(email, password) {
  // Sem validação!
  return db.users.create({ email, password });
}
\`\`\`

**✅ Bom - Validação apropriada:**
\`\`\`javascript
function createUser(email, password) {
  if (!email || !isValidEmail(email)) {
    throw new Error('Endereço de email inválido');
  }
  if (!password || password.length < 8) {
    throw new Error('Senha deve ter pelo menos 8 caracteres');
  }
  return db.users.create({ email, password });
}
\`\`\`
```

### Exemplo 2: Lista de Verificação de Revisão de Segurança

```markdown
## Revisão de Segurança

### Validação de Entrada
- [ ] Todas as entradas do usuário são validadas
- [ ] SQL injection é prevenido (use consultas parametrizadas)
- [ ] XSS é prevenido (escape output)
- [ ] Proteção CSRF está em vigor
- [ ] Upload de arquivos é validado (tipo, tamanho, conteúdo)

### Autenticação & Autorização
- [ ] Autenticação é exigida quando necessário
- [ ] Verificações de autorização estão presentes
- [ ] Senhas são criptografadas (nunca armazenadas em texto plano)
- [ ] Sessões são gerenciadas com segurança
- [ ] Tokens expiram apropriadamente

### Proteção de Dados
- [ ] Dados sensíveis são criptografados
- [ ] Chaves de API não estão hardcoded
- [ ] Variáveis de ambiente são usadas para secrets
- [ ] Dados pessoais seguem regulamentações de privacidade
- [ ] Credenciais de banco de dados estão seguras

### Dependências
- [ ] Sem dependências vulneráveis conhecidas
- [ ] Dependências estão atualizadas
- [ ] Dependências desnecessárias são removidas
- [ ] Versões de dependências estão fixadas

### Exemplos de Problemas a Capturar:

**❌ Ruim - Risco de SQL injection:**
\`\`\`javascript
const query = \`SELECT * FROM users WHERE email = '\${email}'\`;
db.query(query);
\`\`\`

**✅ Bom - Consulta parametrizada:**
\`\`\`javascript
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);
\`\`\`

**❌ Ruim - Secret hardcoded:**
\`\`\`javascript
const API_KEY = 'sk_live_abc123xyz';
\`\`\`

**✅ Bom - Variável de ambiente:**
\`\`\`javascript
const API_KEY = process.env.API_KEY;
if (!API_KEY) {
  throw new Error('A variável de ambiente API_KEY é obrigatória');
}
\`\`\`
```

### Exemplo 3: Lista de Verificação de Revisão de Qualidade de Código

```markdown
## Revisão de Qualidade de Código

### Legibilidade
- [ ] Código é fácil de entender
- [ ] Nomes de variáveis são descritivos
- [ ] Nomes de funções explicam o que fazem
- [ ] Lógica complexa possui comentários
- [ ] Números mágicos são substituídos por constantes

### Estrutura
- [ ] Funções são pequenas e focadas
- [ ] Código segue princípio DRY (Don't Repeat Yourself)
- [ ] Separação adequada de responsabilidades
- [ ] Estilo de código consistente
- [ ] Sem código morto ou comentado

### Manutenibilidade
- [ ] Código é modular e reutilizável
- [ ] Dependências são mínimas
- [ ] Mudanças são retrocompatíveis
- [ ] Mudanças disruptivas estão documentadas
- [ ] Débito técnico é anotado

### Exemplos de Problemas a Capturar:

**❌ Ruim - Nomes pouco claros:**
\`\`\`javascript
function calc(a, b, c) {
  return a * b + c;
}
\`\`\`

**✅ Bom - Nomes descritivos:**
\`\`\`javascript
function calculateTotalPrice(quantity, unitPrice, tax) {
  return quantity * unitPrice + tax;
}
\`\`\`

**❌ Ruim - Função fazendo muita coisa:**
\`\`\`javascript
function processOrder(order) {
  // Validar pedido
  if (!order.items) throw new Error('Sem itens');
  
  // Calcular total
  let total = 0;
  for (let item of order.items) {
    total += item.price * item.quantity;
  }
  
  // Aplicar desconto
  if (order.coupon) {
    total *= 0.9;
  }
  
  // Processar pagamento
  const payment = stripe.charge(total);
  
  // Enviar email
  sendEmail(order.email, 'Pedido confirmado');
  
  // Atualizar inventário
  updateInventory(order.items);
  
  return { orderId: order.id, total };
}
\`\`\`

**✅ Bom - Responsabilidades separadas:**
\`\`\`javascript
function processOrder(order) {
  validateOrder(order);
  const total = calculateOrderTotal(order);
  const payment = processPayment(total);
  sendOrderConfirmation(order.email);
  updateInventory(order.items);
  
  return { orderId: order.id, total };
}
\`\`\`
```

## Boas Práticas

### ✅ Faça Isto

- **Revise Mudanças Pequenas** - PRs menores são mais fáceis de revisar minuciosamente
- **Verifique Testes Primeiro** - Certifique-se que testes passam e cobrem código novo
- **Execute o Código** - Teste localmente quando possível
- **Faça Perguntas** - Não assuma, peça esclarecimentos
- **Seja Construtivo** - Sugira melhorias, não apenas critique
- **Foque em Problemas Importantes** - Não seja excessivamente crítico com problemas menores de estilo
- **Use Ferramentas Automatizadas** - Linters, formatadores, scanners de segurança
- **Revise Documentação** - Verifique se documentação está atualizada
- **Considere Desempenho** - Pense em escala e eficiência
- **Verifique Regressões** - Garanta que funcionalidade existente ainda funciona

### ❌ Não Faça Isto

- **Não Aprove Sem Ler** - Realmente revise o código
- **Não Seja Vago** - Forneça feedback específico com exemplos
- **Não Ignore Segurança** - Problemas de segurança são críticos
- **Não Pule Testes** - Código sem testes causará problemas
- **Não Seja Rude** - Seja respeitoso e profissional
- **Não Aprovação Automática** - Cada revisão deve agregar valor
- **Não Revise Quando Cansado** - Você perderá problemas importantes
- **Não Esqueça Contexto** - Entenda o quadro maior

## Lista de Verificação Completa para Revisão

### Antes da Revisão
- [ ] Leia a descrição do PR e issues relacionadas
- [ ] Entenda qual problema está sendo resolvido
- [ ] Verifique se testes passam em CI/CD
- [ ] Baixe o branch e execute localmente

### Funcionalidade
- [ ] Código resolve o problema declarado
- [ ] Casos extremos são tratados
- [ ] Tratamento de erros é apropriado
- [ ] Entrada do usuário é validada
- [ ] Sem erros lógicos

### Segurança
- [ ] Sem vulnerabilidades de SQL injection
- [ ] Sem vulnerabilidades de XSS
- [ ] Autenticação/autorização está correta
- [ ] Dados sensíveis estão protegidos
- [ ] Sem secrets hardcoded

### Desempenho
- [ ] Sem consultas de banco de dados desnecessárias
- [ ] Sem problemas de consulta N+1
- [ ] Algoritmos eficientes usados
- [ ] Sem vazamentos de memória
- [ ] Cache usado apropriadamente

### Qualidade de Código
- [ ] Código é legível e claro
- [ ] Nomes são descritivos
- [ ] Funções são focadas e pequenas
- [ ] Sem duplicação de código
- [ ] Segue convenções do projeto

### Testes
- [ ] Código novo possui testes
- [ ] Testes cobrem casos extremos
- [ ] Testes são significativos
- [ ] Todos os testes passam
- [ ] Cobertura de testes é adequada

### Documentação
- [ ] Comentários de código explicam por quê, não o quê
- [ ] Documentação de API está atualizada
- [ ] README é atualizado se necessário
- [ ] Mudanças disruptivas estão documentadas
- [ ] Guia de migração fornecido se necessário

### Git
- [ ] Mensagens de commit são claras
- [ ] Sem conflitos de merge
- [ ] Branch está atualizado com main
- [ ] Sem arquivos desnecessários commitados
- [ ] .gitignore está adequadamente configurado

## Armadilhas Comuns

### Problema: Casos Extremos Ausentes
**Sintomas:** Código funciona no caminho feliz mas falha em casos extremos
**Solução:** Faça perguntas "E se...?"
- E se a entrada for null?
- E se o array estiver vazio?
- E se o usuário não estiver autenticado?
- E se a requisição de rede falhar?

### Problema: Vulnerabilidades de Segurança
**Sintomas:** Código expõe riscos de segurança
**Solução:** Use lista de verificação de segurança
- Execute scanners de segurança (npm audit, Snyk)
- Verifique OWASP Top 10
- Valide todas as entradas
- Use consultas parametrizadas
- Nunca confie em entrada do usuário

### Problema: Cobertura de Testes Inadequada
**Sintomas:** Código novo não possui testes ou testes inadequados
**Solução:** Exija testes para todo código novo
- Testes unitários para funções
- Testes de integração para features
- Testes de casos extremos
- Testes de casos de erro

### Problema: Código Pouco Claro
**Sintomas:** Revisor não consegue entender o que código faz
**Solução:** Solicite melhorias
- Melhores nomes de variáveis
- Comentários explicativos
- Funções menores
- Estrutura clara

## Modelos de Comentários de Revisão

### Solicitando Mudanças
```markdown
**Problema:** [Descreva o problema]

**Código atual:**
\`\`\`javascript
// Mostre código problemático
\`\`\`

**Sugestão de correção:**
\`\`\`javascript
// Mostre código melhorado
\`\`\`

**Por quê:** [Explique por que isto é melhor]
```

### Fazendo Perguntas
```markdown
**Pergunta:** [Sua pergunta]

**Contexto:** [Por que você está perguntando]

**Sugestão:** [Se você tiver uma]
```

### Elogiando Código Bom
```markdown
**Legal!** [O que você gostou]

Isto é ótimo porque [explique por quê]
```

## Habilidades Relacionadas

- `@requesting-code-review` - Prepare código para revisão
- `@receiving-code-review` - Lide com feedback de revisão
- `@systematic-debugging` - Debug de problemas encontrados na revisão
- `@test-driven-development` - Garanta que código possui testes

## Recursos Adicionais

- [Guias de Revisão de Código do Google](https://google.github.io/eng-practices/review/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Boas Práticas de Revisão de Código](https://github.com/thoughtbot/guides/tree/main/code-review)
- [Como Revisar Código](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html)

---

**Dica Profissional:** Use um modelo de lista de verificação para cada revisão a fim de garantir consistência e minuciosidade. Personalize-o conforme as necessidades específicas do seu time!