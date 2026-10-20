# supabase/ — Database, Migrations & Edge Functions

PostgreSQL gerenciado pelo Supabase. Sem ORM — SQL puro para migrations, Supabase JS Client para queries.

---

## Estrutura

```
supabase/
├── migrations/                    # SQL migrations versionadas
│   ├── 001_initial_schema.sql     # Schema inicial (profiles, transactions, etc.)
│   ├── 002_unaccent_search.sql    # Full-text search sem acentos
│   ├── 003_plan_restructure.sql   # Rename free/premium → basic/pro, +audio_enabled
│   └── 004_budgets_goals.sql      # Tabelas budgets e goals (function calling Pro)
├── functions/                     # Supabase Edge Functions (Deno runtime)
│   └── categorize-import/         # Async categorization após import
│       └── index.ts
├── seed.sql                       # Dados de desenvolvimento (não vai para prod)
└── config.toml                    # Configuração local do Supabase CLI
```

---

## Schema — Tabelas Principais

| Tabela | Propósito |
|--------|-----------|
| `profiles` | Extensão do auth.users — plan (`basic`\|`pro`), trial, AI quota mensal |
| `bank_accounts` | Contas bancárias importadas pelo usuário |
| `imports` | Histórico de uploads OFX/CSV |
| `transactions` | Transações financeiras (core do produto) |
| `category_dictionary` | Regras de categorização aprendidas por usuário |
| `category_cache` | Cache global de categorização (cross-user) |
| `chat_messages` | Histórico do chat com IA |
| `subscriptions` | Controle de assinaturas Asaas (billing_cycle: `monthly`\|`yearly`) |
| `budgets` | Orçamentos mensais por categoria (Pro, function calling) |
| `goals` | Objetivos financeiros com meta e prazo (Pro, function calling) |

---

## RLS — Row Level Security

**Toda tabela pública TEM RLS habilitado.** É a camada de segurança primária.

### Padrão de política
```sql
-- Habilitar RLS
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;

-- Política: usuário vê apenas seus próprios dados
CREATE POLICY "transactions_user_isolation" ON public.transactions
  USING (user_id = auth.uid());

-- Política de insert: só para si mesmo
CREATE POLICY "transactions_insert_own" ON public.transactions
  FOR INSERT WITH CHECK (user_id = auth.uid());
```

### Exceções controladas
- `category_cache` — leitura pública (cross-user), escrita apenas por service role
- Funções `security definer` — em schema privado, nunca em `public`

---

## Migrations — Convenções

```bash
# Criar nova migration
supabase migration new nome_descritivo

# Aplicar localmente
supabase db push

# Status das migrations
supabase migration list

# Resetar banco local
supabase db reset
```

### Nomenclatura
`001_initial_schema.sql`, `002_add_category_correction.sql`, etc.

### Regras
- Migrations são **irreversíveis** em produção — testar localmente antes
- Usar `IF NOT EXISTS` em DDL quando possível
- Nunca alterar migration já aplicada em produção — criar nova migration
- Constraints de categoria nas 3 tabelas que armazenam `category` (ver schema)

---

## Edge Functions (`functions/`)

Deno runtime — usar para processamento assíncrono que excede 10s (limite Vercel Hobby).

### `categorize-import/`
Acionada após upload de extrato para categorizar transações em background:
1. Recebe `import_id` via POST
2. Busca transações do import com `category_source = 'pending'`
3. Verifica dicionário do usuário primeiro
4. Verifica `category_cache` global
5. Chama Claude Haiku em batch para o restante
6. Atualiza `transactions` e `category_cache`
7. Atualiza `imports.status` para `'completed'`

```bash
# Deploy de Edge Function
supabase functions deploy categorize-import

# Invocar localmente para teste
supabase functions serve categorize-import
```

---

## Queries Comuns

### Transações do mês atual com categoria
```typescript
const { data } = await supabase
  .from('transactions')
  .select('*')
  .eq('user_id', userId)
  .gte('date', startOfMonth)
  .lte('date', endOfMonth)
  .order('date', { ascending: false })
```

### Resumo por categoria
```typescript
const { data } = await supabase
  .rpc('get_category_summary', { p_user_id: userId, p_month: month })
// Ou via query group — definir função SQL para agregação
```

### Verificar quota de IA (mensal por plano)
```typescript
const { data: profile } = await supabase
  .from('profiles')
  .select('ai_queries_this_month, ai_queries_reset_at, plan, trial_ends_at, audio_enabled')
  .eq('id', userId)
  .single()

// Limite mensal: Basic = 50, Pro = 200
// Reset no primeiro dia do mês: ai_queries_reset_at < date_trunc('month', now())
```

---

## Tipos Gerados

Nunca escrever tipos do banco manualmente. Sempre gerar:
```bash
supabase gen types typescript --local > src/lib/supabase/types.ts
```

Usar no código:
```typescript
import type { Tables, TablesInsert } from '@/lib/supabase/types'
type Transaction = Tables<'transactions'>
type NewTransaction = TablesInsert<'transactions'>
```

---

## Segurança — Checklist

- [ ] RLS habilitado em toda tabela do schema `public`
- [ ] `service_role` key apenas server-side (nunca `NEXT_PUBLIC_`)
- [ ] Funções `security definer` em schema privado
- [ ] Views com `security_invoker = true` (Postgres 15+)
- [ ] Validação de `user_id` em toda query de insert
- [ ] Webhook Asaas validado por token antes de processar
- [ ] Dados pessoais: LGPD — endpoint de exclusão implementado (FR Art. 18)
