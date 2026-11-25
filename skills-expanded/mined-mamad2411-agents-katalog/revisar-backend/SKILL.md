---
name: revisar-backend
description: "Revisa código backend quanto a arquitetura, testes e conformidade de segurança. Use quando o dev-backend vai autorrevisar o código antes do PR."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-backend

Revisa **código backend Node.js/NestJS** antes de abertura de PR: verifica aderência aos guardrails, qualidade de implementação, cobertura de testes, segurança e consistência com os padrões do projeto.

**Agente:** dev-backend  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `dados.md`, `seguranca.md`, `testes.md`, `operacional.md`

---

## Quando usar

- Antes de abrir PR com implementação backend
- Ao revisar PR de outro desenvolvedor no code review
- Para auto-revisão antes de solicitar revisão do arquiteto ou tech lead

---

## Entrada esperada

- Diff ou conjunto de arquivos a revisar
- Contexto: qual feature ou correção foi implementada
- Contrato de API definido (para verificar conformidade)

---

## Processo de execução

### Passo 1 — Verificar pré-condições (DoD obrigatório)

Checklist antes de qualquer revisão de código — `operacional.md §1` e `§2`:

- [ ] Branch está atualizada com `main`/`master`
- [ ] Testes unitários passando (`npm test`)
- [ ] Testes de integração passando (`npm run test:e2e`)
- [ ] `npm run build` sem erros de tipo

Se qualquer item falhar, interromper a revisão e reportar antes de continuar.

### Passo 2 — Revisar segurança

Verificar `seguranca.md §1` e `§2`:

- [ ] Nenhum dado pessoal em claro em response (CPF, e-mail sem mascaramento quando desnecessário)
- [ ] Nenhum dado pessoal em log (`console.log` ou logger com objeto completo)
- [ ] Nenhum secret em código (`JWT_SECRET`, `DATABASE_URL`, tokens em hardcode)
- [ ] Nenhum arquivo `.env` com valores reais commitado
- [ ] Stack trace não exposto em response de erro 500

### Passo 3 — Revisar qualidade do código backend

Verificar `backend.md`:

**Floating promises (`backend.md §2`):**
```typescript
// ⛔ promise sem await
someAsyncOperation();
this.prisma.user.create({ data });

// ✅ awaited
await someAsyncOperation();
```

**Validação de entrada (`backend.md §3`):**
```typescript
// ⛔ sem validação
async create(@Body() body: any) { ... }

// ✅ DTO com class-validator
async create(@Body() dto: CreateUserDto) { ... }
```

**Logging sem console.log (`backend.md §5`):**
```typescript
// ⛔ console.log de debug esquecido
console.log('user created:', user);

// ✅ logger estruturado ou nenhum log de debug
this.logger.log(`User created: ${user.id}`);
```

**Event loop (`backend.md §7`):**
```typescript
// ⛔ leitura síncrona de arquivo no handler
const data = fs.readFileSync('./large-file.json');

// ✅ assíncrono
const data = await fs.promises.readFile('./large-file.json');
```

### Passo 4 — Revisar camada de dados

Verificar `dados.md`:

**SQL injection (`dados.md §1`):**
```typescript
// ⛔ concatenação de string
await db.query(`SELECT * FROM users WHERE id = ${id}`);

// ✅ parâmetro vinculado ou ORM
await prisma.user.findUnique({ where: { id } });
```

**Paginação (`dados.md §3`):**
```typescript
// ⛔ sem limite
await prisma.user.findMany();

// ✅ com paginação
await prisma.user.findMany({ take: pageSize, skip: (page - 1) * pageSize });
```

**Transação (`dados.md §4`):**
```typescript
// ⛔ writes múltiplos sem transação
await prisma.order.create({ data: orderData });
await prisma.inventory.update({ ... }); // falha aqui = estado inconsistente

// ✅ transação explícita
await prisma.$transaction([
  prisma.order.create({ data: orderData }),
  prisma.inventory.update({ ... }),
]);
```

**Migrations (`dados.md §2`, `seguranca.md §3`):**
- Nenhuma migration com `DROP`, `TRUNCATE` ou `DELETE` sem `WHERE`
- Migration adicionando coluna NOT NULL em tabela existente: deve ser nullable primeiro (`dados.md §2.3`)

### Passo 5 — Revisar testes

Verificar `testes.md`:

- [ ] Testes nomeados com `should <comportamento> when <condição>` (`testes.md §1`)
- [ ] Mocks apenas nas fronteiras de infraestrutura (não de módulos internos) (`testes.md §2`)
- [ ] Sem `if (process.env.NODE_ENV === 'test')` no código de produção (`testes.md §4`)
- [ ] Sem dado pessoal real em fixtures ou seeds de teste (`testes.md §7`)
- [ ] Testes cobrem casos de erro e não apenas o caminho feliz

### Passo 6 — Verificar estrutura NestJS

- [ ] Controller sem lógica de negócio (delega para service)
- [ ] Service sem conhecimento de HTTP (não usa `Request`/`Response` diretamente)
- [ ] DTOs com decorators de validação (`@IsString`, `@IsEmail`, etc.)
- [ ] Módulos registram corretamente controllers e providers
- [ ] `PrismaModule` não é importado diretamente em módulos de domínio (usar o `@Global()`)

### Passo 7 — Verificar resposta de erros

Verificar `padronizar-erros`:

- [ ] Erros lançam exceções NestJS (`ConflictException`, `NotFoundException`, etc.) — não retornam objetos de erro manualmente
- [ ] Nenhum `throw new Error('message')` genérico onde deveria ser exceção tipada
- [ ] Nenhum `catch` vazio silenciando erros

---

## Saída produzida

```markdown
## Revisão Backend: <nome do PR ou feature>

**Veredicto:** ✅ Aprovado | ⚠️ Aprovado com ressalvas | ⛔ Bloqueado

---

### Bloqueios (impedem merge)
- [ ] <arquivo>:<linha> — <descrição do problema> — `<guardrail citado>`

### Ressalvas (devem ser tratadas, não impedem merge)
- <descrição + recomendação>

### Pontos positivos
- <o que foi feito bem>

### Checklist DoD
- [x] Branch atualizada
- [x] Testes passando
- [x] Sem secret exposto
- [x] Sem console.log
- [x] Paginação nas listas
- [x] `Dockerfile` multi-stage presente (`operacional.md §4.1`)
- [x] `.dockerignore` presente (`operacional.md §4.2`)
- [x] `docker-compose.yml` com banco e healthcheck (`operacional.md §4.3`)
- [x] `docker compose up --build` executa sem erro
```
