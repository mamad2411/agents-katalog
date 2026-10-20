---
name: migrar-supabase
description: "Conduz a migração completa de Lovable e Supabase para NestJS e Prisma — schema, auth, Guards, services e plano de dados. Use quando o arquiteto ou o dev-backend vai executar a migração."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: migrar-supabase

Conduz a migração completa de um projeto Lovable/Supabase para a stack NestJS + Prisma + PostgreSQL. Usa como entrada obrigatória o mapa de auditoria produzido por `auditar-codigo-lovable`. Cobre: conversão de schema para Prisma, definição de serviços NestJS, migração de autenticação, conversão de RLS em Guards, conversão de edge functions em services e plano de migração de dados.

**Agente:** arquiteto (decisões e planejamento), dev-backend (implementação)
**Guardrails aplicáveis:** `supabase.md §1`, `supabase.md §2`, `supabase.md §3`, `supabase.md §4`, `supabase.md §5`

---

## Quando usar

- Após `auditar-codigo-lovable` ter produzido `plans/arquitetura/<ticket>-lovable-audit.md`
- Quando a decisão arquitetural confirmou migração completa para NestJS + Prisma
- Nunca executar sem o mapa de auditoria — bloquear e executar `auditar-codigo-lovable` primeiro

---

## Processo de execução

### Passo 1 — Ler o mapa de auditoria

Abrir `plans/arquitetura/<ticket>-lovable-audit.md` e extrair:
- Lista de tabelas e relacionamentos
- RLS policies com suas classificações de risco
- Chamadas Supabase no frontend (endpoints que o NestJS precisará expor)
- Edge functions com classificação lógica de negócio / integração
- Dependências externas a substituir

Se o arquivo não existir: **bloquear** — executar `auditar-codigo-lovable` primeiro.

---

### Passo 2 — Converter schema para Prisma

Para cada tabela do mapa de auditoria, criar o model Prisma equivalente:

| Tipo Supabase | Tipo Prisma |
|---|---|
| `uuid` (PK) | `String @id @default(uuid())` |
| `text` | `String` |
| `int4` / `int8` | `Int` / `BigInt` |
| `bool` | `Boolean` |
| `timestamptz` | `DateTime` |
| `jsonb` | `Json` |
| `created_at` | `DateTime @default(now())` |
| `updated_at` | `DateTime @updatedAt` |
| foreign key | `@relation(fields: [...], references: [...])` |

Revisar com o arquiteto se o schema Lovable tem redundâncias, colunas desnecessárias ou oportunidades de normalização antes de gerar o schema final.

---

### Passo 3 — Definir estrutura de serviços NestJS

Com base nas tabelas e chamadas Supabase mapeadas, definir:
- Qual System API é responsável por cada domínio
- Quais endpoints são necessários com base nas operações `supabase.from()` identificadas
- Quais operações vão direto ao System API vs passam pelo BFF

Para cada serviço identificado, acionar:
1. `definir-microservico` — estrutura, responsabilidade e contratos
2. `gerar-plano-tarefa` — gerar `plans/arquitetura/<ticket>-<servico>.md`

Emitir a tabela de repositórios a criar (padrão do arquiteto) antes de prosseguir.

---

### Passo 4 — Planejar autenticação NestJS

Com base no mapa de autenticação Supabase:

1. Definir novo formato JWT: claims `sub` (userId), `email`, `role`
2. Mapear campos `user_metadata`/`app_metadata` para colunas da tabela `users` no Prisma
3. Configurar `JwtModule` + `PassportModule` + `JwtStrategy` no serviço de auth
4. Planejar migração de usuários: exportar `auth.users` → popular tabela `users` via script
5. Definir data de corte: quando tokens Supabase expiram e NestJS auth entra em vigor
6. Documentar plano de transição no arquivo de plano do `dev-backend`

---

### Passo 5 — Converter RLS em Guards NestJS

Para cada RLS policy do mapa de auditoria:

| Expressão RLS | Guard NestJS equivalente |
|---|---|
| `auth.uid() = user_id` | `@UseGuards(JwtAuthGuard, ResourceOwnerGuard)` |
| `auth.role() = 'admin'` | `@Roles('admin') @UseGuards(JwtAuthGuard, RolesGuard)` |
| `using (true)` — leitura pública | Endpoint sem guard ou com `@Public()` — revisar intenção |
| `using (false)` — bloqueado | Remover endpoint ou revisar com arquiteto |
| RLS ausente em tabela sensível | Guard obrigatório — **não há equivalente sem guard** |

Policies classificadas como **fraca** ou **ausente** → revisar com arquiteto antes de mapear o Guard.

---

### Passo 6 — Converter edge functions em services NestJS

Para cada edge function do mapa de auditoria:

- **Lógica de negócio**: extrair para NestJS service + controller via skill `implementar-endpoint`
- **Integração com terceiros**: extrair para módulo de integração dedicado (`PaymentModule`, `EmailModule`, etc.)
- **Mista**: separar as responsabilidades antes de converter — nunca migrar diretamente 1:1
- **Webhooks recebidos**: converter para endpoint NestJS com validação de assinatura HMAC

---

### Passo 7 — Produzir plano de migração de dados

Escrever `plans/dev-backend/<ticket>-data-migration.md`:

```markdown
## Plano de migração de dados — <nome do projeto>

### Sequência obrigatória
1. Backup do banco Supabase: `supabase db dump --schema public > backup.sql`
2. Aplicar Prisma migrations no banco destino
3. Validar estrutura (schema diff entre origem e destino)
4. Executar script de migração de dados (tabela por tabela)
5. Validar integridade: contagens, samples, foreign keys
6. Migrar dados de storage para <destino definido>
7. Smoke tests no ambiente staging
8. Definir janela de corte: parar Supabase → ativar NestJS

### Rollback
**Condição:** <quando acionar rollback>
**Procedimento:** <passos para reverter>

### Dados sensíveis
| Tabela | Dados pessoais | Controles aplicados |
|---|---|---|

### Critério de go/no-go
- [ ] Contagem de registros bate entre origem e destino
- [ ] Smoke tests passando em staging
- [ ] Autenticação NestJS validada com usuário migrado
- [ ] Plano de comunicação aos usuários preparado (se necessário)
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Posso pular a auditoria se o projeto é pequeno" | Não — sem mapa de auditoria, RLS fraca vira vulnerabilidade no NestJS sem aviso |
| "O schema do Lovable já está bom para produção" | Não — schemas Lovable priorizam simplicidade; sempre revisar normalização com o arquiteto |
| "Posso migrar os dados depois" | Não — o plano de dados define a data de corte; sem ele o Supabase nunca é desligado |
| "Guards são equivalentes a RLS, posso simplificar" | `using (true)` sem guard não é equivalente — toda policy deve ter mapeamento explícito |
| "Posso manter o @supabase/supabase-js no NestJS temporariamente" | Não — misturar dois sistemas de auth é origem de vulnerabilidades de autorização |

---

## Checklist de conclusão

- [ ] Mapa de auditoria lido — escopo confirmado antes de qualquer decisão
- [ ] Schema Prisma revisado pelo arquiteto e aprovado (normalização + índices)
- [ ] Tabela de repositórios a criar emitida
- [ ] `definir-microservico` + `gerar-plano-tarefa` executados para cada serviço
- [ ] Plano de autenticação documentado com data de corte definida
- [ ] Toda RLS policy mapeada para Guard NestJS equivalente
- [ ] Edge functions separadas em lógica de negócio / integração antes de converter
- [ ] `plans/dev-backend/<ticket>-data-migration.md` escrito com sequência e rollback
- [ ] Planos de tarefa por agente gerados em `plans/<agente>/`
