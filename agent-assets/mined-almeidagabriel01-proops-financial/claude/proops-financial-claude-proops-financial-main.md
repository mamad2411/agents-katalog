# App Financeiro Pessoal com IA — Visão Geral

SaaS financeiro pessoal mobile-first para o Brasil. Usuários importam extratos OFX/CSV, a IA categoriza as transações automaticamente em PT-BR, e um assistente conversacional responde perguntas financeiras sobre os dados reais do usuário.

**Docs completos:** `docs/prd/prd.md` (requisitos) | `docs/architecture/architecture.md` (arquitetura)

---

## Navegação Rápida

| Área | Path | O que tem |
|------|------|-----------|
| App Router | `src/app/` | Pages, layouts, API routes |
| Lógica de negócio | `src/lib/` | Parsers, IA, billing, utils |
| Componentes UI | `src/components/` | shadcn/ui, dashboard, chat, import |
| Hooks React | `src/hooks/` | use-user, use-transactions, use-premium |
| Database | `supabase/` | Migrations, Edge Functions, seed |
| Testes | `tests/` | Unit + integration + fixtures |
| Stories | `docs/stories/` | Development stories por Epic |

---

## Estrutura de Rotas

```
/ → redirect para /dashboard (autenticado) ou /login
/(auth)/login        → Login email/Google
/(auth)/signup       → Cadastro
/(auth)/callback     → OAuth callback Supabase
/(app)/dashboard     → Dashboard principal (Server Component)
/(app)/transactions  → Lista de transações com filtros
/(app)/import        → Upload OFX/CSV (Client Component)
/(app)/chat          → Chat IA Premium (Client Component)
/(app)/settings      → Perfil, plano, preferências
/api/import          → POST: parse + categorize + save
/api/chat            → POST: stream resposta IA
/api/webhook/asaas   → POST: eventos de pagamento
/api/health          → GET: status das dependências
```

---

## Stack

| Camada | Tech |
|--------|------|
| Frontend | Next.js 14+ App Router + TypeScript |
| Estilização | shadcn/ui + Tailwind CSS (mobile-first) |
| Backend | Next.js API Routes + Supabase Edge Functions |
| Banco | PostgreSQL via Supabase (sem ORM, RLS) |
| Auth | Supabase Auth (email/senha + Google OAuth) |
| IA | Gemini 2.0 Flash (batch/Basic) + Gemini 2.5 Flash (chat Pro) |
| Pagamentos | Asaas (Pix + Boleto + Cartão) |
| Deploy | Vercel + Supabase Cloud |

---

## Comandos Essenciais

```bash
npm run dev                              # Dev server local
npm run typecheck                        # Verificar tipos
npm run lint                             # ESLint
npm test                                 # Vitest
supabase db push                         # Aplicar migrations
supabase gen types typescript --local > src/lib/supabase/types.ts
```

---

## Regras Críticas

1. **RLS obrigatório** em toda tabela do schema `public` — nunca vazar dados entre usuários
2. **Service role key** nunca vai para o cliente (variáveis sem `NEXT_PUBLIC_`)
3. **Verificação server-side** de plano Premium na API route — nunca confiar apenas no frontend
4. **SHA-256 para deduplicação** de transações CSV: `hash(date + amount + normalized_description)`
5. **LGPD desde o dia 1** — consentimento explícito, direito de exclusão implementado
6. **Gemini Flash para batch**, Gemini Pro apenas para chat interativo — controle de custo IA
7. **Absolute imports** com `@/` para todos os módulos internos

---

## Agentes AIOX Disponíveis

| Comando | Agente | Usa para |
|---------|--------|----------|
| `@dev` | Dex | Implementação de código |
| `@qa` | Quinn | Testes, QA gate |
| `@architect` | Aria | Decisões arquiteturais |
| `@data-engineer` | Dara | Schema, RLS, migrations |
| `@ux-design-expert` | Uma | UI/UX mobile-first |
| `@devops` | Gage | git push, PR (exclusivo) |

---

## Regras de Git

**NUNCA adicionar `Co-Authored-By` ou qualquer trailer de autoria de IA nos commits.**
Commits têm um único autor: Gabriel Almeida. Não incluir referência a Claude, Anthropic ou qualquer ferramenta de IA nas mensagens de commit.

---

## Regras Obrigatórias de Qualidade

**NUNCA commitar sem rodar antes:**
```bash
npm run lint    # zero warnings/erros
npm run build   # build de produção sem falhas
```

**Supressão de warnings é proibida sem justificativa:**
- `eslint-disable` — só com comentário explicando o motivo e issue de tracking
- `@ts-ignore` / `@ts-expect-error` — idem; preferir corrigir o tipo

**Se lint ou build retornar erro, corrigir antes de avançar — nunca ignorar.**

**Cobertura mínima de testes:** 80% para toda lógica de negócio em `src/lib/`.

**Gate obrigatório antes de marcar story como Ready for Review:**
```bash
npm run quality   # lint + build + test em sequência
```

O hook `pre-commit` (Husky) reforça automaticamente: bloqueia o commit se lint ou build falharem.

---

## Stories Ativas

Ver `docs/stories/` — numeradas por Epic (1.x Foundation, 2.x IA, 3.x Premium, 4.x Polish)
