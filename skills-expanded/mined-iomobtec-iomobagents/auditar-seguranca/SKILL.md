---
name: auditar-seguranca
description: "Revisão completa de PR contra o OWASP Top 10 e o guardrail appsec, classificando achados em CRITICAL, HIGH, MEDIUM e LOW. Use quando o dev-security ou o tech-lead vai auditar a segurança de um PR."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: auditar-seguranca

Auditoria de segurança de um Pull Request contra o OWASP Top 10 e o guardrail appsec, com achados classificados por severidade.

**Agente:** `dev-security`, `tech-lead`  
**Baseado em:** OWASP Top 10 2025 (`https://owasp.org/Top10/2025/`) + OWASP API Security Top 10 2023 (`https://owasp.org/API-Security/editions/2023/en/0x00-header/`) + `Guardrails/appsec.md`  
**Output:** Relatório de segurança estruturado com achados classificados por severidade.  
**Referências rápidas:** `References/security-checklist.md`

---

## Quando usar

Após `dev-qa` concluir os testes E2E e antes da revisão de PR do `tech-lead`. Também usado em re-auditoria após correção de achados CRITICAL/HIGH.

---

## Processo

### Passo 1 — Delimitar escopo

Identificar o que está sendo auditado:

```
- Quais camadas têm PR aberto? (backend, BFF, frontend, mensageria)
- Quais arquivos foram alterados? (listar arquivos do diff)
- Há mudanças em autenticação, autorização ou dados sensíveis?
- É re-auditoria pós-correção? Se sim, quais achados foram corrigidos?
```

Se for re-auditoria: auditar apenas os arquivos/áreas que foram corrigidos, não o PR inteiro.

### Passo 2 — Executar checklist por camada

Execute o checklist completo de cada camada presente no PR. Para cada item, registrar: ✅ Conforme | 🔴 Violação CRITICAL | 🟠 Violação HIGH | 🟡 Violação MEDIUM | 🟢 Violação LOW.

#### Checklist — Backend / BFF (NestJS)

> Referência: OWASP Top 10 2025. Seções do appsec.md indicadas em cada item.

**§1 Injeção — A05:2025 (`appsec.md §1`)**
- [ ] Nenhuma query SQL com concatenação de string
- [ ] Raw SQL usa template literals do Prisma (`$queryRaw\`...\``) com placeholder
- [ ] Consultas NoSQL validam tipo do parâmetro antes do uso
- [ ] `child_process.exec/spawn` não recebe entrada do usuário sem sanitização

**§2 Autenticação — A07:2025 (`appsec.md §2`)**
- [ ] JWT tem campo `exp` (máximo 1h para access token)
- [ ] Algoritmo explícito: `HS256` ou `RS256` (nunca `none`)
- [ ] Refresh token em cookie `httpOnly: true, secure: true, sameSite: strict`
- [ ] Refresh token é rotacionado a cada uso
- [ ] Rate limit em endpoint de login (`@Throttle`)
- [ ] Senhas com bcrypt/argon2, custo ≥ 12
- [ ] Todo endpoint tem guard — exceções marcadas com `@Public()` e comentário

**§3 Exposição de dados — A04:2025 Cryptographic Failures (`appsec.md §3`)**
- [ ] DTOs de response excluem `password`, `passwordHash`, tokens internos
- [ ] Exception filter global intercepta e generaliza erros antes de enviar ao cliente
- [ ] Logs não contêm `Authorization` header, `password`, `cpf`, `cartao`
- [ ] Stack trace nunca aparece na response HTTP

**§4 Controle de acesso — A01:2025 Broken Access Control (`appsec.md §4`)**
- [ ] Operações por ID incluem `userId: req.user.id` no WHERE (anti-IDOR)
- [ ] Endpoints administrativos têm `@Roles` + `RolesGuard`
- [ ] Deleção/edição verifica ownership antes de executar

**§5 Security misconfiguration — A02:2025 (subiu de A05:2021!) (`appsec.md §5`)**
- [ ] `helmet()` configurado no `main.ts`
- [ ] CORS com `origin` explícito (não `*`)
- [ ] `express.json({ limit: '1mb' })` configurado
- [ ] Nenhuma credencial padrão em `.env.example` com valor real

**§9 Logging e alertas — A09:2025 Security Logging and Alerting Failures (`appsec.md §9`)**
- [ ] Falha de autenticação gera log com IP, email, motivo
- [ ] Acesso 403 gera log com userId, recurso tentado
- [ ] Operações destrutivas (delete, bulk update) geram audit log
- [ ] Nenhum `try/catch` vazio silenciando falha de segurança

**§10 SSRF — controle adicional além do Top 10 2025 (`appsec.md §10`)**
- [ ] URLs fornecidas por usuário são validadas contra allowlist de domínios
- [ ] IPs internos e `localhost` são bloqueados explicitamente
- [ ] Apenas protocolo `https:` é aceito

**§12 Rate limiting (`appsec.md §12`)**
- [ ] `ThrottlerModule` configurado globalmente
- [ ] Endpoints sensíveis têm `@Throttle` específico
- [ ] Parâmetros de paginação têm limite máximo (`Math.min(pageSize, 100)`)
- [ ] Uploads têm limite de tamanho

**§13 Mishandling of Exceptional Conditions — A10:2025 NOVA categoria (`appsec.md §13`)**
- [ ] Nenhum `catch {}` ou `catch (e) {}` vazio silenciando exceções de segurança
- [ ] Erros de autenticação/autorização sempre negam acesso (fail secure — nunca concedem em caso de erro)
- [ ] Exception filter global configurado e remove stack trace da resposta HTTP
- [ ] Consumers de mensageria têm tratamento de exceção + dead-letter queue
- [ ] Transações financeiras/críticas têm rollback explícito garantido
- [ ] `process.on('unhandledRejection')` e `process.on('uncaughtException')` configurados

#### Checklist — API Security Top 10 2023

> Referência: OWASP API Security Top 10 2023. Aplicar para todo PR que toca endpoints REST, BFF ou integrações externas.

**§14 Broken Object Property Level Auth — API3:2023 (`appsec.md §14`)**
- [ ] Nenhum `@Body() body: any` — todos os inputs usam DTOs com campos explícitos
- [ ] Respostas usam `ResponseDto` com `plainToInstance` — sem entidade Prisma bruta
- [ ] DTO de response não inclui campos não destinados ao consumidor (role, passwordHash, flags internos)

**§15 Broken Function Level Authorization — API5:2023 (`appsec.md §15`)**
- [ ] Toda função sensível (admin, bulk, export, alteração de permissão) tem `@Roles` declarado individualmente
- [ ] Guard não aplicado apenas no controller — funções críticas têm guard próprio
- [ ] Existe teste que verifica HTTP 403 para usuário sem role tentando acessar endpoint admin

**§16 Sensitive Business Flows — API6:2023 (`appsec.md §16`)**
- [ ] Fluxos de compra, reserva e uso de recurso limitado têm rate limit específico além do global
- [ ] Cupons/vouchers têm limite de uso por conta, não apenas por IP
- [ ] Logs permitem detectar picos de automação em retrospecto

**§17 Improper Inventory Management — API9:2023 (`appsec.md §17`)**
- [ ] Todo endpoint novo tem `@ApiOperation` e `@ApiResponse` no Swagger — atualizado no mesmo PR
- [ ] Versões depreciadas retornam header `Sunset` com data
- [ ] Nenhuma variável de ambiente de produção reutilizada em staging

**§18 Unsafe Consumption of APIs — API10:2023 (`appsec.md §18`)**
- [ ] Dados de APIs externas validados com DTO + class-validator antes de persistir
- [ ] Toda chamada a API externa tem `timeout` configurado (máximo 10s)
- [ ] Respostas de APIs externas mapeadas para DTO interno — sem passthrough ao cliente

#### Checklist — Frontend (React)

**§6 XSS — A05:2025 subvetor de Injection (`appsec.md §6`)**
- [ ] Nenhum `dangerouslySetInnerHTML` sem `DOMPurify.sanitize()`
- [ ] Links com `href` dinâmico validam protocolo (`startsWith('https://')`)
- [ ] Nenhum `element.innerHTML = userContent`

**§3 Exposição de dados em UI — A04:2025 (`appsec.md §3`)**
- [ ] Tokens de acesso não armazenados em `localStorage` ou `sessionStorage`
- [ ] Dados sensíveis (CPF, cartão, senha) não em estado React persistido
- [ ] Nenhum `console.log` com dados pessoais ou tokens

**§7 CSRF (`appsec.md §7`)**
- [ ] Se autenticação é por cookie: `SameSite=strict` configurado
- [ ] Se autenticação é por JWT no header: sem ação necessária

### Passo 3 — Identificar achados

Para cada item marcado como violação, registrar achado no formato:

```
<severidade emoji>
**Vetor:** appsec.md §<n> — <título>
**Arquivo:** <caminho>:<linha>
**Descrição:** <o que o código faz de errado>
**Impacto:** <o que um atacante pode fazer>
**Correção:** <como corrigir, com snippet de código quando possível>
```

### Passo 4 — Emitir relatório

```markdown
## Relatório de Segurança — <PR ou serviço> — <data>

**Camadas auditadas:** backend | BFF | frontend | mensageria
**Status geral:** 🔴 CRITICAL encontrado | ✅ Aprovado sem bloqueadores

---

### Achados

<lista de achados no formato do Passo 3, ordenados: CRITICAL → HIGH → MEDIUM → LOW>

---

### Resumo

| Severidade | Qtd | Ação |
|---|---|---|
| 🔴 CRITICAL | X | Tech-lead aciona dev para correção imediata |
| 🟠 HIGH | X | Tech-lead aciona dev para correção antes do merge |
| 🟡 MEDIUM | X | Issues abertas — não bloqueia merge |
| 🟢 LOW | X | Issues abertas — próximo ciclo |

---

### Próximos passos

Se houver CRITICAL ou HIGH:
  → Reportar ao tech-lead com lista de achados e correções sugeridas
  → Aguardar correção e re-auditoria antes de liberar para merge

Se apenas MEDIUM/LOW:
  → Tech-lead pode prosseguir com revisão de PR
  → Dev abre issues para MEDIUM e LOW no repositório
```

### Passo 5 — Fluxo pós-relatório

**Se CRITICAL ou HIGH encontrado:**
```
1. dev-security entrega relatório ao orquestrador
2. Orquestrador repassa ao tech-lead
3. Tech-lead aciona dev responsável com achado + correção
4. Dev corrige → orquestrador aciona dev-security para re-auditoria (Fluxo C)
```

**Se apenas MEDIUM/LOW ou nenhum achado:**
```
1. dev-security entrega relatório com ✅ liberado para merge (ressalvas documentadas)
2. Tech-lead prossegue com revisão de PR
3. Dev abre issues para MEDIUM/LOW
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Já conheço este código, sei que está seguro" | Conhecimento pessoal não é auditoria. O checklist existe porque segurança deve ser verificável, não presumida. |
| "Vou aprovar com ressalvas e o dev corrige depois" | CRITICAL e HIGH não são ressalvas — são bloqueadores. Aprovar com achado crítico pendente expõe produção. |
| "É só um endpoint interno, não precisa de auditoria completa" | Endpoints internos são vetores frequentes de pivotagem de ataque. "Interno" não significa "sem risco". |
| "A auditoria está demorando, vou fazer só uma parte" | Auditoria parcial sem declarar o escopo auditado é pior que nenhuma — cria falsa sensação de segurança. |
| "O dev-security vai pegar, não preciso verificar no PR" | A auditoria do dev-security é a última linha — não a única. Achado na auditoria final que teria sido pego aqui custou um ciclo completo de correção. |

---

## Anti-padrões bloqueados

- Emitir "aprovado" sem ter executado todos os itens do checklist da camada
- Registrar achado sem indicar arquivo e linha exatos
- Classificar IDOR como MEDIUM — é HIGH no mínimo, CRITICAL se sem autenticação
- Aceitar correção que oculta o sintoma sem endereçar o vetor (ex: try/catch escondendo a falha)
- Marcar como LOW qualquer achado de injeção — injeção começa em HIGH
