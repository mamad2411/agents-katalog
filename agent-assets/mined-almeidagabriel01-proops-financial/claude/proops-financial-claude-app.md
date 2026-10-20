# src/app/ — Next.js App Router

Todas as páginas, layouts e API routes do projeto. Usa App Router do Next.js 14+.

---

## Estrutura de Route Groups

```
app/
├── layout.tsx          # Root layout (providers, fontes, metadata global)
├── page.tsx            # Redirect: autenticado → /dashboard, anônimo → /login
├── globals.css         # Tailwind base + CSS custom properties
│
├── (auth)/             # Grupo: páginas públicas (sem app shell)
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   └── callback/route.ts   # OAuth callback do Supabase Auth
│
├── (app)/              # Grupo: rotas autenticadas (com app shell + auth guard)
│   ├── layout.tsx      # App shell: navbar, bottom-nav, auth guard
│   ├── dashboard/      # Server Component — dados no servidor
│   ├── transactions/   # Server Component com filtros client-side
│   ├── import/         # Client Component — upload interativo
│   ├── chat/           # Client Component — streaming de IA (Premium)
│   └── settings/       # Client Component — formulários de preferências
│
└── api/                # API Routes — lógica server-only
    ├── import/route.ts     # POST: parse OFX/CSV → categorizar → salvar
    ├── chat/route.ts       # POST: stream resposta IA (Claude Sonnet)
    ├── webhook/asaas/      # POST: eventos de pagamento Asaas
    └── health/route.ts     # GET: status Supabase + Claude API
```

---

## Convenções de Componentes

### Server Components (padrão)
- Buscar dados diretamente no servidor (sem `useEffect`)
- Não usar hooks React, event handlers, ou estado
- Passar dados como props para Client Components filhos

```tsx
// dashboard/page.tsx — Server Component
export default async function DashboardPage() {
  const supabase = createServerClient()
  const { data: transactions } = await supabase
    .from('transactions')
    .select('*')
    .order('date', { ascending: false })

  return <DashboardView transactions={transactions} />
}
```

### Client Components (quando necessário)
- Marcar com `'use client'` no topo
- Apenas quando precisar de: hooks, event handlers, browser APIs, estado
- Tentar manter Client Components nas folhas da árvore

```tsx
'use client'
// import/page.tsx — Client Component (upload interativo)
```

---

## API Routes — Padrões

### Autenticação obrigatória
```typescript
// Toda API route protegida verifica sessão
const supabase = createServerClient()
const { data: { user } } = await supabase.auth.getUser()
if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
```

### Verificação de plano Premium (server-side obrigatória)
```typescript
// NUNCA confiar apenas no frontend para verificar Premium
const { data: profile } = await supabase
  .from('profiles')
  .select('plan, trial_ends_at')
  .eq('id', user.id)
  .single()

const isPremium = profile.plan === 'premium' ||
  (profile.trial_ends_at && new Date(profile.trial_ends_at) > new Date())

if (!isPremium) return NextResponse.json({ error: 'Premium required' }, { status: 403 })
```

### Resposta padronizada
```typescript
// Sucesso
return NextResponse.json({ data: result }, { status: 200 })
// Erro
return NextResponse.json({ error: 'Mensagem em PT-BR' }, { status: 400 })
```

---

## Middleware (`src/middleware.ts`)

Protege todas as rotas do grupo `(app)`:
- Verifica sessão Supabase via cookies
- Redireciona `/` e `/(app)/*` para `/login` se não autenticado
- Redireciona `/login` e `/signup` para `/dashboard` se autenticado

---

## Regras Importantes

- **Não colocar lógica de negócio em pages/components** — fica em `src/lib/`
- **API Routes são server-only** — nunca importar código de API routes no cliente
- **`/api/webhook/*`** — validar token do Asaas antes de processar eventos
- **`/api/import`** — tamanho máximo de arquivo: 5MB; tipos: OFX e CSV apenas
- **`/api/chat`** — rate limit: 20 msgs/dia, verificar server-side
- **Edge Functions** para processamento assíncrono longo (>10s) — ver `supabase/functions/`
