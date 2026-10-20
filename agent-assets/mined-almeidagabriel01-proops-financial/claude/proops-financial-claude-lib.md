# src/lib/ — Core Business Logic

Toda a lógica de negócio reutilizável fica aqui. Nenhuma lógica de negócio em components ou pages — eles são camada de apresentação.

---

## Módulos

```
lib/
├── supabase/           # Clientes Supabase + tipos gerados
├── parsers/            # Parsing de OFX e CSV bancários
├── ai/                 # Integração Claude API (categorização + chat)
├── billing/            # Integração Asaas + gerenciamento de planos
└── utils/              # Utilitários gerais (formatação, constantes)
```

---

## supabase/

### Dois clientes distintos — usar o correto
```typescript
// client.ts — Browser (usa cookies, funciona com RLS, seguro expor)
import { createBrowserClient } from '@supabase/ssr'
// Usar em Client Components e hooks

// server.ts — Server (API Routes, Server Components, middleware)
import { createServerClient } from '@supabase/ssr'
// Usar no servidor — nunca expor service_role no browser
```

### Tipos (`types.ts`)
Gerados automaticamente via Supabase CLI — **não editar manualmente**:
```bash
supabase gen types typescript --local > src/lib/supabase/types.ts
```

---

## parsers/

### OFX Parser (`ofx-parser.ts`)
- Extrai: data, valor, descrição, tipo (débito/crédito), `FITID` (ID nativo do banco)
- `FITID` é o `external_id` — usado para deduplicação em OFX

### CSV Parser (`csv-parser.ts`)
- Detecta delimitador automaticamente (`,` ou `;`)
- Detecta formato do banco via `bank-formats/`
- Gera `external_id` sintético: `SHA-256(date + amount + normalized_description)`

### Formatos suportados (`bank-formats/`)
- `nubank.ts` — formato Nubank CSV
- `itau.ts` — formato Itaú CSV
- `bradesco.ts` — formato Bradesco CSV
- `index.ts` — detector automático de banco

### Interface de saída (`types.ts`)
```typescript
interface ParsedTransaction {
  external_id: string   // OFX: FITID; CSV: SHA-256 hash
  date: string          // ISO 8601 (YYYY-MM-DD)
  description: string   // Descrição bruta do banco
  amount: number        // Positivo = crédito, negativo = débito
  type: 'credit' | 'debit'
}
```

---

## ai/

### Hierarquia de categorização (ordem de prioridade)
```
1. Dicionário do usuário (category_dictionary)  ← mais alta prioridade
2. Cache global (category_cache)
3. Gemini 2.0 Flash via API                     ← último recurso (fallback: keyword rules)
```

### categorizer.ts — Batch categorization
- Sempre processar em batch (array de transações de uma vez)
- Nunca categorizar transação por transação (custo proibitivo)
- Fallback para `'outros'` quando confiança < threshold
- Salvar resultado no `category_cache` para reutilização cross-user

### chat.ts — Conversational AI
- **Basic:** Gemini 2.0 Flash (`gemini-2.0-flash`), sem tools, 50 msgs/mês
- **Pro:** Gemini 2.5 Flash (`gemini-2.5-flash`), com function calling, 200 msgs/mês
- Contexto: transações categorizadas do usuário (últimos 3 meses, agregado)
- Responde APENAS com base nos dados reais — nunca inventar números
- Rate limit verificado server-side ANTES de chamar a API (campo `ai_queries_this_month`)

### prompts/
- `categorize.ts` — prompt otimizado para 14 categorias + contexto BR
- `chat-system.ts` — system prompt do assistente financeiro PT-BR

### cache.ts
- Consulta `category_cache` antes de chamar a IA
- Chave: `description_normalized` (lowercase, trim, whitespace-collapse)

---

## billing/

### plans.ts — FONTE DE VERDADE para planos
```typescript
import { PLAN_LIMITS, CATEGORIES, Category, getEffectiveTier } from '@/lib/billing/plans'
```
- `PLAN_LIMITS.basic` / `PLAN_LIMITS.pro` — limites por tier
- `getEffectiveTier(plan, trial_ends_at)` — retorna tier efetivo considerando trial
- **Usar apenas server-side** para decisões de autorização

Planos:
- **Basic** (R$19,90/mês): 3 contas, Gemini Flash, 50 msgs/mês, sem áudio, sem function calling
- **Pro** (R$49,90/mês): contas ilimitadas, Gemini Pro, 200 msgs/mês, áudio Whisper, function calling

### asaas.ts
- Cliente HTTP para Asaas API
- Criar/cancelar assinaturas, consultar status

### webhook-handler.ts
- Processar eventos: `PAYMENT_CONFIRMED`, `PAYMENT_OVERDUE`, `SUBSCRIPTION_CANCELED`
- Atualizar `subscriptions` table → trigger sincroniza `profiles.plan` e `audio_enabled`
- Período de graça de 3 dias para `PAYMENT_OVERDUE`

---

## utils/

### constants.ts
```typescript
// Apenas constantes gerais — NÃO contém CATEGORIES, PLANS ou limites de IA
export const APP_NAME = 'Finansim'
export const MAX_FILE_SIZE_MB = 5
export const TRIAL_DAYS = 7
```

Para categorias, planos e limites de IA: usar `@/lib/billing/plans`

### format.ts
- `formatCurrency(amount)` — R$ 1.234,56 (locale pt-BR)
- `formatDate(date)` — DD/MM/YYYY
- `normalizeDescription(text)` — lowercase + trim + whitespace-collapse (para cache)

### rate-limit.ts
- `checkAndIncrementAIQuota(userId, plan)` — verifica + incrementa `ai_queries_this_month`
- Limite mensal por plano: Basic = 50, Pro = 200 (via `PLAN_LIMITS`)
- Reset automático via `ai_queries_reset_at` (primeiro dia do mês corrente)

---

## Schema DB — Campos relevantes em profiles

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `plan` | `'basic' \| 'pro'` | Tier do plano (fonte de verdade para features) |
| `trial_ends_at` | `timestamptz` | Fim do trial Pro (7 dias do signup) |
| `audio_enabled` | `boolean` | Hint de performance — verificar junto com plan/trial |
| `ai_queries_this_month` | `int` | Contador mensal de uso de IA |
| `ai_queries_reset_at` | `date` | Primeiro dia do mês do último reset |

**Gate de áudio correto (server-side):**
```typescript
const inTrial = profile.trial_ends_at
  ? new Date(profile.trial_ends_at) > new Date()
  : false;
const canUseAudio = (profile.plan === 'pro' || inTrial) && profile.audio_enabled;
```

---

## Regras

- **Imports absolutos:** `import { ... } from '@/lib/supabase/server'`
- **Sem lógica de negócio em pages/components** — tudo vai em `lib/`
- **Service role key** apenas em `lib/supabase/server.ts` — nunca no client
- **Testar tudo em `tests/unit/`** — especialmente parsers e lógica de billing
