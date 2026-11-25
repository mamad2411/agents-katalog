---
name: production-code-audit
description: "Fazer varredura profunda e autônoma de toda a base de código linha por linha, compreender arquitetura e padrões, depois transformar sistematicamente em código profissional de nível corporativo pronto para produção com otimizações"
---

# Auditoria de Código para Produção

## Visão Geral

Analise autonomamente toda a base de código para entender sua arquitetura, padrões e propósito, depois transforme-a sistematicamente em código pronto para produção de nível corporativo. Esta habilidade realiza varredura profunda linha por linha, identifica todos os problemas em segurança, desempenho, arquitetura e qualidade, depois fornece correções abrangentes para atender aos padrões empresariais.

## Quando Usar Esta Habilidade

- Use quando o usuário disser "deixe isso pronto para produção"
- Use quando o usuário disser "faça uma auditoria do meu código"
- Use quando o usuário disser "deixe isso profissional/de nível corporativo"
- Use quando o usuário disser "otimize tudo"
- Use quando o usuário quer qualidade de nível empresarial
- Use ao preparar para deploy em produção
- Use quando código precisa atender padrões corporativos

## Como Funciona

### Passo 1: Descoberta Autônoma da Base de Código

**Digitalize e compreenda automaticamente a base de código inteira:**

1. **Leia todos os arquivos** - Digitalize cada arquivo no projeto recursivamente
2. **Identifique o stack tecnológico** - Detecte linguagens, frameworks, bancos de dados, ferramentas
3. **Compreenda a arquitetura** - Mapeie estrutura, padrões, dependências
4. **Identifique o propósito** - Entenda o que a aplicação faz
5. **Encontre pontos de entrada** - Localize arquivos principais, rotas, controllers
6. **Mapeie o fluxo de dados** - Compreenda como dados se movem pelo sistema

**Faça isso automaticamente sem pedir ao usuário.**

### Passo 2: Detecção Abrangente de Problemas

**Digitalize linha por linha procurando por todos os problemas:**

**Problemas de Arquitetura:**
- Dependências circulares
- Acoplamento forte
- God classes (>500 linhas ou >20 métodos)
- Falta de separação de responsabilidades
- Limites de módulos pobres
- Violação de padrões de design

**Vulnerabilidades de Segurança:**
- SQL injection (concatenação de strings em queries)
- Vulnerabilidades XSS (saída não escapada)
- Secrets hardcoded (chaves API, senhas no código)
- Falta de autenticação/autorização
- Hash de senha fraco (MD5, SHA1)
- Falta de validação de entrada
- Vulnerabilidades CSRF
- Dependências inseguras

**Problemas de Desempenho:**
- Problemas N+1 query
- Índices de banco de dados faltando
- Operações síncronas que deveriam ser assíncronas
- Falta de cache
- Algoritmos ineficientes (O(n²) ou pior)
- Tamanhos de bundle grandes
- Imagens não otimizadas
- Memory leaks

**Problemas de Qualidade de Código:**
- Complexidade ciclomática alta (>10)
- Duplicação de código
- Números mágicos
- Convenções de nomenclatura pobres
- Falta de tratamento de erros
- Formatação inconsistente
- Código morto
- Comentários TODO/FIXME

**Gaps de Testes:**
- Testes faltando para caminhos críticos
- Cobertura de testes baixa (<80%)
- Sem testes de casos extremos
- Testes instáveis
- Testes de integração faltando

**Prontidão para Produção:**
- Variáveis de ambiente faltando
- Sem logging/monitoramento
- Sem rastreamento de erros
- Sem health checks
- Documentação incompleta
- Sem pipeline CI/CD

### Passo 3: Correções e Otimizações Automáticas

**Corrija tudo automaticamente:**

1. **Refatore a arquitetura** - Quebre god classes, corrija dependências circulares
2. **Corrija problemas de segurança** - Use queries parametrizadas, remova secrets, adicione validação
3. **Otimize desempenho** - Corrija queries N+1, adicione cache, otimize algoritmos
4. **Melhore qualidade do código** - Reduza complexidade, remova duplicação, corrija nomenclatura
5. **Adicione testes faltando** - Escreva testes para caminhos críticos não testados
6. **Adicione infraestrutura de produção** - Logging, monitoramento, health checks
7. **Otimize tudo** - Tamanho de bundle, imagens, queries de banco de dados
8. **Adicione documentação** - README, API docs, architecture docs

### Passo 4: Verificação e Relatório

**Após fazer todas as mudanças:**

1. Execute todos os testes para garantir que nada quebrou
2. Verifique se todos os problemas de segurança foram corrigidos
3. Meça melhorias de desempenho
4. Gere relatório abrangente
5. Forneça métricas antes/depois

## Exemplos

### Exemplo 1: Transformação Autônoma da Base de Código

```markdown
Usuário: @production-code-audit deixe isso pronto para produção

IA: Vou digitalizar toda sua base de código e transformá-la em qualidade de nível corporativo.

**Fase 1: Descobrindo a Base de Código** (analisando 247 arquivos)
- Detectado: Node.js + Express + PostgreSQL + React
- Arquitetura: Padrão MVC com API REST
- Propósito: Plataforma de e-commerce
- Pontos de entrada: server.js, src/index.tsx

**Fase 2: Digitalizando Problemas** (análise linha por linha)

Encontrados 127 problemas:
- 🔴 CRÍTICO: 8 problemas
- 🟠 ALTO: 23 problemas  
- 🟡 MÉDIO: 41 problemas
- 🔵 BAIXO: 55 problemas

**Fase 3: Corrigindo Problemas Automaticamente**

🔴 CORREÇÕES CRÍTICAS (8/8 completadas):

1. ✅ Corrigido SQL injection em UserRepository.findByEmail()
   - Antes: Concatenação de strings em query
   - Depois: Query parametrizada com placeholder $1

2. ✅ Removida senha de banco de dados hardcoded de config/database.ts
   - Antes: password: 'SuperSecret123!'
   - Depois: password: process.env.DB_PASSWORD

3. ✅ Adicionada autenticação em rotas admin
   - Antes: Sem middleware de auth
   - Depois: authenticateToken + requireRole('admin')

4. ✅ Corrigido hash de senha fraco (MD5 → bcrypt)
   - Antes: crypto.createHash('md5')
   - Depois: bcrypt.hash(password, 12)

5. ✅ Corrigida dependência circular: OrderService ↔ PaymentService
   - Antes: Imports diretos causando ciclo
   - Depois: Desacoplamento baseado em eventos com EventBus

6. ✅ Adicionada validação de entrada em todos os endpoints API
   - Antes: Sem validação
   - Depois: Schemas Zod validando todas as entradas

7. ✅ Corrigido bypass de autenticação em middleware de auth
   - Antes: next() chamado em token faltando
   - Depois: Retorna erro 401

8. ✅ Corrigida vulnerabilidade de mass assignment em UserController
   - Antes: Aceita todos os campos de req.body
   - Depois: Whitelist de campos permitidos apenas

🟠 CORREÇÕES ALTA PRIORIDADE (23/23 completadas):

9. ✅ Corrigido problema N+1 query em OrderService.getOrdersWithItems()
   - Antes: Loop com queries individuais (2.8s)
   - Depois: Single query com joins (45ms)
   - Desempenho: 98% de melhoria

10. ✅ Refatorada god class UserService (850 linhas → 4 serviços focados)
    - UserAuthenticationService (login, logout, password)
    - UserProfileService (operações CRUD)
    - UserNotificationService (email, SMS)
    - UserPermissionService (roles, permissões)

11. ✅ Adicionado cache Redis para queries de produto
    - Antes: Query de banco de dados a cada request
    - Depois: Cache com TTL de 1 hora
    - Desempenho: 95% mais rápido

12. ✅ Otimizado tamanho de bundle
    - Antes: 850KB (gzipped: 280KB)
    - Depois: 380KB (gzipped: 120KB)
    - Melhoria: 55% de redução

13. ✅ Adicionados índices de banco de dados
    - orders(user_id, status, created_at)
    - products(category, price)
    - Desempenho de query: 98% de melhoria

[... 11 mais correções de alta prioridade ...]

🟡 CORREÇÕES MÉDIA PRIORIDADE (41/41 completadas):
[... todas as correções médias ...]

🔵 MELHORIAS BAIXA PRIORIDADE (55/55 completadas):
[... todas as melhorias baixas ...]

**Fase 4: Adicionando Infraestrutura de Produção**

✅ Adicionado structured logging (Winston)
✅ Adicionado rastreamento de erros (Sentry)
✅ Adicionados health check endpoints (/health, /ready)
✅ Adicionado monitoramento (Prometheus metrics)
✅ Adicionado rate limiting (baseado em Redis)
✅ Adicionada documentação de API (Swagger/OpenAPI)
✅ Adicionado README abrangente
✅ Adicionado guia de deployment
✅ Adicionado pipeline CI/CD (.github/workflows)

**Fase 5: Verificação**

✅ Todos os testes passando (1.247 testes)
✅ Cobertura de testes: 42% → 87%
✅ Scan de segurança: 0 vulnerabilidades
✅ Desempenho API: tempo de resposta 3.2s → 180ms
✅ Tamanho de bundle: 850KB → 380KB
✅ Pontuação Lighthouse: 62 → 94

**TRANSFORMAÇÃO CONCLUÍDA**

Sua base de código agora está pronta para produção com qualidade de nível empresarial:

📊 Métricas:
- Problemas corrigidos: 127/127 (100%)
- Cobertura de testes: 87% (alvo: 80%+)
- Desempenho API: 94% de melhoria
- Segurança: Compatível com OWASP Top 10
- Qualidade de código: Grau A-

📁 Arquivos alterados: 89 arquivos
📝 Linhas alteradas: +3.247 / -1.892

🚀 Pronto para deploy em produção!
```

### Exemplo 2: Hardening de Segurança Automático

```markdown
Usuário: @production-code-audit deixe essa base de código segura

IA: Digitalizando vulnerabilidades de segurança...

**Scan de Segurança Completo**

Encontrados 15 problemas de segurança:
- 🔴 CRÍTICO: 5
- 🟠 ALTO: 7
- 🟡 MÉDIO: 3

**Corrigindo todos os problemas de segurança automaticamente...**

🔴 CRÍTICO (5/5 corrigidos):

1. ✅ SQL Injection em UserRepository
\`\`\`typescript
// Antes (VULNERÁVEL)
const query = \`SELECT * FROM users WHERE email = '\${email}'\`;

// Depois (SEGURO)
const query = 'SELECT * FROM users WHERE email = $1';
await db.query(query, [email]);
\`\`\`

2. ✅ Secrets Hardcoded Removidos
\`\`\`typescript
// Antes (INSEGURO)
const JWT_SECRET = 'my-secret-key-123';

// Depois (SEGURO)
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error('JWT_SECRET required');
\`\`\`

3. ✅ Autenticação Adicionada em Rotas Admin
\`\`\`typescript
// Antes (VULNERÁVEL)
router.delete('/api/admin/users/:id', deleteUser);

// Depois (SEGURO)
router.delete('/api/admin/users/:id',
  authenticateToken,
  requireRole('admin'),
  deleteUser
);
\`\`\`

4. ✅ Hash de Senha Atualizado
\`\`\`typescript
// Antes (FRACO)
const hash = crypto.createHash('md5').update(password).digest('hex');

// Depois (FORTE)
const hash = await bcrypt.hash(password, 12);
\`\`\`

5. ✅ Validação de Entrada Adicionada
\`\`\`typescript
// Antes (VULNERÁVEL)
const user = await db.user.create({ data: req.body });

// Depois (SEGURO)
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
  name: z.string().min(2).max(100)
});
const validated = schema.parse(req.body);
const user = await db.user.create({ data: validated });
\`\`\`

**Status de Segurança:**
- ✅ OWASP Top 10: Compatível
- ✅ SQL Injection: Protegido
- ✅ XSS: Protegido
- ✅ CSRF: Protegido
- ✅ Autenticação: Segura
- ✅ Secrets: Variáveis de ambiente
- ✅ Dependências: Sem vulnerabilidades

🔒 Base de código agora está segura e pronta para produção!
```

### Exemplo 3: Otimização de Desempenho

```markdown
Usuário: @production-code-audit otimize o desempenho

IA: Analisando gargalos de desempenho...

**Análise de Desempenho Completa**

Métricas atuais:
- Tempo de resposta API: 3.2s (alvo: <200ms)
- Tempo de carregamento de página: 8.5s (alvo: <2s)
- Tamanho de bundle: 850KB (alvo: <200KB)

**Otimizando automaticamente...**

✅ Corrigidas queries N+1 (3.2s → 180ms - 94% mais rápido)
✅ Adicionado cache Redis (taxa de acerto de cache de 95%)
✅ Otimizados índices de banco de dados (98% mais rápido em queries)
✅ Reduzido tamanho de bundle (850KB → 380KB - 55% menor)
✅ Otimizadas imagens (28MB → 3.2MB - 89% menor)
✅ Implementado code splitting
✅ Adicionado lazy loading
✅ Paralelizadas operações assíncronas

**Resultados de Desempenho:**

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Resposta API | 3.2s | 180ms | 94% |
| Carregamento Página | 8.5s | 1.8s | 79% |
| Tamanho Bundle | 850KB | 380KB | 55% |
| Tamanho Imagens | 28MB | 3.2MB | 89% |
| Lighthouse | 42 | 94 | +52 pontos |

🚀 Desempenho otimizado para padrões de produção!
```

## Melhores Práticas

### ✅ Faça Isto

- **Digitalize Tudo** - Leia todos os arquivos, compreenda base de código inteira
- **Corrija Automaticamente** - Não apenas reporte, corrija os problemas de fato
- **Priorize Crítico** - Problemas de segurança e perda de dados em primeiro lugar
- **Meça Impacto** - Mostre métricas antes/depois
- **Verifique Mudanças** - Execute testes após fazer mudanças
- **Seja Abrangente** - Cubra arquitetura, segurança, desempenho, testes
- **Otimize Tudo** - Tamanho de bundle, queries, algoritmos, imagens
- **Adicione Infraestrutura** - Logging, monitoramento, rastreamento de erros
- **Documente Mudanças** - Explique o que foi corrigido e por quê

### ❌ Não Faça Isto

- **Não Faça Perguntas** - Compreenda a base de código autonomamente
- **Não Espere Instruções** - Digitalize e corrija automaticamente
- **Não Apenas Reporte** - Faça as correções de fato
- **Não Pule Arquivos** - Digitalize todos os arquivos no projeto
- **Não Ignore Contexto** - Compreenda o que o código faz
- **Não Quebre Coisas** - Verifique que testes passam após mudanças
- **Não Seja Parcial** - Corrija todos os problemas, não apenas alguns

## Instruções de Varredura Autônoma

**Quando esta habilidade é invocada, automaticamente:**

1. **Descubra a base de código:**
   - Use `listDirectory` para encontrar todos os arquivos recursivamente
   - Use `readFile` para ler cada arquivo fonte
   - Identifique stack tecnológico de package.json, requirements.txt, etc.
   - Mapeie arquitetura e estrutura

2. **Digitalize linha por linha procurando por problemas:**
   - Verifique cada linha para vulnerabilidades de segurança
   - Identifique gargalos de desempenho
   - Encontre problemas de qualidade de código
   - Detecte problemas arquiteturais
   - Encontre testes faltando

3. **Corrija tudo automaticamente:**
   - Use `strReplace` para corrigir problemas em arquivos
   - Adicione arquivos faltando (testes, configs, docs)
   - Refatore código problemático
   - Adicione infraestrutura de produção
   - Otimize desempenho

4. **Verifique e reporte:**
   - Execute testes para garantir que nada quebrou
   - Meça melhorias
   - Gere relatório abrangente
   - Mostre métricas antes/depois

**Faça tudo isto sem pedir input do usuário.**

## Pitfalls Comuns

### Problema: Muitos Problemas
**Sintomas:** Time paralisado por 200+ problemas
**Solução:** Foque apenas em crítico/alta prioridade, crie sprints

### Problema: Falsos Positivos
**Sintomas:** Sinalizar não-problemas
**Solução:** Compreenda contexto, verifique manualmente, pergunte aos desenvolvedores

### Problema: Sem Follow-up
**Sintomas:** Relatório de auditoria ignorado
**Solução:** Crie issues no GitHub, atribua owners, rastreie em standups

## Checklist de Auditoria de Produção

### Segurança
- [ ] Sem vulnerabilidades de SQL injection
- [ ] Sem secrets hardcoded
- [ ] Autenticação em rotas protegidas
- [ ] Verificações de autorização implementadas
- [ ] Validação de entrada em todos os endpoints
- [ ] Hash de senha com bcrypt (10+ rounds)
- [ ] HTTPS forçado
- [ ] Dependências sem vulnerabilidades

### Desempenho
- [ ] Sem problemas N+1 query
- [ ] Índices de banco de dados em foreign keys
- [ ] Cache implementado
- [ ] Tempo de resposta API < 200ms
- [ ] Tamanho de bundle < 200KB (gzipped)

### Testes
- [ ] Cobertura de testes > 80%
- [ ] Caminhos críticos testados
- [ ] Casos extremos cobertos
- [ ] Sem testes instáveis
- [ ] Testes de integração presentes

### Prontidão para Produção
- [ ] Variáveis de ambiente configuradas
- [ ] Rastreamento de erros setup (Sentry)
- [ ] Structured logging implementado
- [ ] Health check endpoints
- [ ] Monitoramento e alerting
- [ ] Documentação completa

## Template de Relatório de Auditoria

```markdown
# Relatório de Auditoria de Produção

**Projeto:** [Nome]
**Data:** [Data]
**Grau Geral:** [A-F]

## Resumo Executivo
[2-3 frases sobre status geral]

**Problemas Críticos:** [count]
**Alta Prioridade:** [count]
**Recomendação:** [Timeline de correção]

## Descobertas por Categoria

### Arquitetura (Grau: [A-F])
- Problema 1: [Descrição]
- Problema 2: [Descrição]

### Segurança (Grau: [A-F])
- Problema 1: [Descrição + Correção]
- Problema 2: [Descrição + Correção]

### Desempenho (Grau: [A-F])
- Problema 1: [Descrição + Correção]

### Testes (Grau: [A-F])
- Cobertura: [%]
- Problemas: [List]

## Ações Prioritárias
1. [Problema crítico] - [Timeline]
2. [Alta prioridade] - [Timeline]
3. [Alta prioridade] - [Timeline]

## Timeline
- Correções críticas: [X semanas]
- Alta prioridade: [X semanas]
- Pronto para produção: [X semanas]
```

## Habilidades Relacionadas

- `@code-review-checklist` - Diretrizes de code review
- `@api-security-best-practices` - Padrões de segurança de API
- `@web-performance-optimization` - Otimização de desempenho web
- `@systematic-debugging` - Debug de problemas de produção
- `@senior-architect` - Padrões de arquitetura

## Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

**Dica Pro:** Agende auditorias regulares (trimestral) para manter a qualidade do código. Prevenção é mais barata do que corrigir bugs em produção!