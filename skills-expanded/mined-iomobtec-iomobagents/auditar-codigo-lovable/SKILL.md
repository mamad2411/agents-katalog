---
name: auditar-codigo-lovable
description: "Analisa código exportado do Lovable — mapeia schema, RLS policies, chamadas Supabase e edge functions — produzindo um mapa de migração. Use quando o arquiteto vai planejar a saída de Lovable e Supabase."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: auditar-codigo-lovable

Analisa o código exportado de um projeto Lovable antes da migração para NestJS + Prisma: mapeia tabelas, RLS policies, padrões de autenticação, chamadas diretas ao Supabase, edge functions e lógica de negócio misturada com infraestrutura. Produz o mapa de migração em `plans/arquitetura/<ticket>-lovable-audit.md` — entrada obrigatória para a skill `migrar-supabase`.

**Agente:** arquiteto
**Guardrails aplicáveis:** `supabase.md §1`, `supabase.md §3`, `supabase.md §4`

---

## Quando usar

- Ao iniciar a migração de qualquer projeto Lovable para NestJS + Prisma
- Antes de qualquer decisão arquitetural sobre o projeto migrado
- Output obrigatório antes de executar `migrar-supabase` — nunca pular esta etapa

---

## Processo de execução

### Passo 1 — Mapear schema de banco

Ler todos os arquivos de migration do Supabase (`supabase/migrations/*.sql`) ou inspecionar o schema via dump (`supabase db dump --schema public`).

Para cada tabela identificada, registrar:
- Nome e colunas com tipos
- Chave primária (uuid vs serial)
- Relacionamentos e foreign keys
- Colunas de auditoria (`created_at`, `updated_at`)
- Índices existentes

---

### Passo 2 — Mapear RLS policies

Identificar todos os arquivos SQL ou migrations com `CREATE POLICY` ou `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`.

Para cada policy, registrar:
- Tabela afetada
- Operação (SELECT, INSERT, UPDATE, DELETE)
- Expressão `USING` e `WITH CHECK`
- Classificação: **segura** / **fraca** / **ausente**

| Classificação | Critério |
|---|---|
| segura | `auth.uid() = user_id` ou role check explícito |
| fraca | `using (true)` sem filtro, ou apenas SELECT protegido |
| ausente | Tabela sem RLS habilitada com dados sensíveis |

Sinalizar como **CRÍTICO** qualquer `using (true)` sem filtro ou tabela com dados sensíveis sem RLS.

---

### Passo 3 — Mapear chamadas ao Supabase client

Varrer todos os arquivos `.tsx` e `.ts` buscando:
```
supabase.from(
supabase.auth.
supabase.storage.
supabase.rpc(
supabase.channel(
```

Para cada ocorrência, registrar:
- Arquivo e linha
- Tabela ou recurso acessado
- Operação (select, insert, update, delete, upsert)
- Se há lógica de negócio embutida no filter ou transform

---

### Passo 4 — Mapear autenticação

Identificar como o Supabase Auth é usado:
- `supabase.auth.signIn`, `signUp`, `signOut`, `onAuthStateChange`
- Campos do `session.user` consumidos (`id`, `email`, `user_metadata`, `app_metadata`)
- Se há roles customizados em `app_metadata`
- Rotas protegidas e como a proteção é feita (check local vs dependência de RLS)

---

### Passo 5 — Mapear edge functions

Listar todos os diretórios em `supabase/functions/`.

Para cada edge function, registrar:
- Nome e propósito inferido
- Dependências externas chamadas (APIs, webhooks, serviços de email)
- Se acessa banco diretamente via Supabase client
- Classificação: **lógica de negócio** / **integração** / **mista**

---

### Passo 6 — Identificar dependências externas

Varrer `package.json` e código buscando integrações com terceiros que passam pelo Supabase (webhooks recebidos, storage, realtime subscriptions). Listar o que precisará de substituto após a migração.

---

### Passo 7 — Produzir mapa de migração

Escrever `plans/arquitetura/<ticket>-lovable-audit.md`:

```markdown
## Audit Report — <nome do projeto>
**Data:** <YYYY-MM-DD>
**Auditor:** arquiteto

### Tabelas identificadas
| Tabela | Colunas | RLS habilitada | Classificação | Risco |
|---|---|---|---|---|

### Mapa de autorização (RLS → Guards NestJS)
| Tabela | Operação | Expressão USING | Guard equivalente | Classificação |
|---|---|---|---|---|

### Chamadas Supabase no frontend
| Arquivo:linha | Operação | Tabela/recurso | Lógica de negócio embutida? |
|---|---|---|---|

### Padrões de autenticação
- Campos consumidos de session.user: <lista>
- Roles customizados: <sim/não — detalhar>
- Rotas protegidas: <lista>

### Edge functions
| Nome | Propósito | Classificação | Dependências externas |
|---|---|---|---|

### Dependências externas a substituir
- <lista>

### Riscos identificados
- **CRÍTICO:** <lista>
- **ALTO:** <lista>
- **MÉDIO:** <lista>

### Estimativa de esforço de migração
| Componente | Esforço estimado | Observação |
|---|---|---|
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "O projeto é simples, posso pular a auditoria" | RLS fraca ou ausente é o risco mais comum em projetos Lovable — sem auditoria vira vulnerabilidade no NestJS |
| "Posso migrar enquanto audito" | Não — o mapa de migração é a entrada obrigatória da skill `migrar-supabase`; sem ele a migração não tem escopo definido |
| "A RLS do Lovable já está correta" | Lovable frequentemente gera `using (true)` ou RLS apenas em SELECT — auditar todas as policies antes de confiar |
| "Vou documentar depois" | O `plans/arquitetura/<ticket>-lovable-audit.md` é o artefato de handoff — sem ele o dev-backend não tem como iniciar |

---

## Checklist de conclusão

- [ ] Todas as tabelas do schema `public` mapeadas com tipos e relacionamentos
- [ ] Todas as RLS policies classificadas (segura / fraca / ausente)
- [ ] Todas as chamadas `supabase.*` no frontend rastreadas por arquivo e linha
- [ ] Padrões de autenticação documentados com campos consumidos
- [ ] Edge functions listadas com classificação lógica de negócio / integração / mista
- [ ] Dependências externas a substituir identificadas
- [ ] Riscos críticos sinalizados explicitamente
- [ ] `plans/arquitetura/<ticket>-lovable-audit.md` escrito e revisado
- [ ] Handoff para `migrar-supabase` documentado no arquivo de plano
