---
name: tpl-frontend-nextjs-prisma-postgres
description: Template do pack (frontend/04-nextjs-prisma-postgres.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/04-nextjs-prisma-postgres.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do SaaS]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/04-nextjs-prisma-postgres.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Next.js 15 + Drizzle ORM + Stripe + Resend (SaaS Template)
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Next.js (App Router) | 15.x |
| Linguagem | TypeScript | 5.x (strict) |
| Database | Neon Postgres (servless) + Drizzle ORM + Drizzle Kit | latest |
| Auth | NextAuth.js (Auth.js) | v5 |
| Payments | Stripe (subscriptions + webhooks) | latest |
| Email | Resend + React Email | latest |
| Styling | Tailwind CSS + shadcn/ui | v4 |

---

## DATABASE LAYER

```
db/
├── schema/
│   ├── users.ts
│   ├── teams.ts
│   ├── subscriptions.ts
│   └── index.ts           # Re-exports all schemas
├── migrations/            # Gerado pelo Drizzle Kit (NEVER edit manually)
├── queries/               # Funções de query reutilizáveis
│   ├── users.ts           # getUserById, getUserByEmail, etc.
│   └── subscriptions.ts   # getActiveSubscription, isProUser, etc.
└── index.ts               # Conexão Neon + Drizzle instance
```

---

## DRIZZLE SCHEMA TEMPLATE

```typescript
// db/schema/users.ts
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  email: text('email').unique().notNull(),
  name: text('name'),
  avatarUrl: text('avatar_url'),
  stripeCustomerId: text('stripe_customer_id').unique(),
  plan: text('plan', { enum: ['free', 'pro', 'enterprise'] }).default('free').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;

// db/schema/subscriptions.ts
export const subscriptions = pgTable('subscriptions', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => users.id, { onDelete: 'cascade' }).notNull(),
  stripeSubscriptionId: text('stripe_subscription_id').unique().notNull(),
  stripePriceId: text('stripe_price_id').notNull(),
  status: text('status', {
    enum: ['active', 'canceled', 'past_due', 'incomplete', 'trialing'],
  }).notNull(),
  currentPeriodEnd: timestamp('current_period_end').notNull(),
  cancelAtPeriodEnd: boolean('cancel_at_period_end').default(false).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});
```

---

## STRIPE INTEGRATION RULES

### Webhook Handler (CRITICAL)

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers';
import Stripe from 'stripe';
import { db } from '@/db';
import { subscriptions, users } from '@/db/schema';
import { eq } from 'drizzle-orm';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const sig = (await headers()).get('stripe-signature')!;

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return new Response('Webhook signature verification failed', { status: 400 });
  }

  switch (event.type) {
    case 'customer.subscription.created':
    case 'customer.subscription.updated': {
      const sub = event.data.object as Stripe.Subscription;
      await db.insert(subscriptions).values({
        id: crypto.randomUUID(),
        userId: sub.metadata.userId,
        stripeSubscriptionId: sub.id,
        stripePriceId: sub.items.data[0].price.id,
        status: sub.status,
        currentPeriodEnd: new Date(sub.current_period_end * 1000),
        cancelAtPeriodEnd: sub.cancel_at_period_end,
      }).onConflictDoUpdate({
        target: subscriptions.stripeSubscriptionId,
        set: {
          status: sub.status,
          stripePriceId: sub.items.data[0].price.id,
          currentPeriodEnd: new Date(sub.current_period_end * 1000),
          cancelAtPeriodEnd: sub.cancel_at_period_end,
          updatedAt: new Date(),
        },
      });
      break;
    }
    case 'customer.subscription.deleted': {
      const sub = event.data.object as Stripe.Subscription;
      await db.update(subscriptions)
        .set({ status: 'canceled', updatedAt: new Date() })
        .where(eq(subscriptions.stripeSubscriptionId, sub.id));
      break;
    }
  }

  return new Response('ok', { status: 200 });
}
```

### Checkout Session

```typescript
// lib/stripe.ts
export async function createCheckoutSession(userId: string, priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId },
    subscription_data: { metadata: { userId } },
  });
  return session.url;
}
```

### Feature Gating

```typescript
// lib/auth-utils.ts
export async function requirePro(userId: string) {
  const sub = await db.query.subscriptions.findFirst({
    where: (s, { eq, and, gt }) => and(
      eq(s.userId, userId),
      eq(s.status, 'active'),
      gt(s.currentPeriodEnd, new Date()),
    ),
  });
  if (!sub) throw new Error('Pro subscription required');
  return sub;
}
```

---

## EMAIL WITH RESEND + REACT EMAIL

```typescript
// lib/email.ts
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendWelcomeEmail(to: string, name: string) {
  await resend.emails.send({
    from: 'SaaS <noreply@yourdomain.com>',
    to,
    subject: `Bem-vindo, ${name}!`,
    react: WelcomeEmail({ name }),
  });
}
```

---

## MIGRATION WORKFLOW

```bash
# Development
npx drizzle-kit generate   # Gera SQL migration do diff
npx drizzle-kit migrate    # Aplica ao banco local/staging
npx drizzle-kit studio     # UI visual para inspecionar banco

# Production (NEVER edit existing migrations)
npx drizzle-kit migrate    # Aplica no Neon via DATABASE_URL

# Se deu errado: NUNCA deletar migration — crie nova que reverte
```

---

## ROUTING TABLE (trigger → action)

| Trigger | Action |
|---------|--------|
| New DB table | Create schema file → `npx drizzle-kit generate` → `npx drizzle-kit migrate` |
| Schema change | NEVER edit old migration — run generate → review SQL diff → migrate |
| Payment webhook | Add case to webhook handler → test with `stripe listen --forward-to` |
| Feature gate | `requirePro(userId)` in Server Action or Server Component |
| Email send | Create React Email template → send via Resend in Server Action |
| New plan/price | Create in Stripe Dashboard → add priceId to `lib/plans.ts` |
| Customer portal | Use `stripe.billingPortal.sessions.create()` |

---

## TESTING PATTERNS

```typescript
// __tests__/webhooks/stripe.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('Stripe webhook', () => {
  it('rejects requests with invalid signature', async () => {
    const res = await fetch('/api/webhooks/stripe', {
      method: 'POST',
      body: '{}',
      headers: { 'stripe-signature': 'invalid' },
    });
    expect(res.status).toBe(400);
  });
});

// Para testes de integração com Stripe CLI:
// stripe listen --forward-to localhost:3000/api/webhooks/stripe
// stripe trigger payment_intent.succeeded
// stripe trigger customer.subscription.updated
```

---

## ENV VARS

```env
DATABASE_URL=postgresql://...neon.tech/...?sslmode=require
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_APP_URL=http://localhost:3000
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRO_PRICE_ID=price_...
RESEND_API_KEY=re_...
```

## BUILD COMMANDS

```bash
npm run dev          # Dev server (turbopack)
npm run build        # Production build
npm run start        # Start production
npm test             # Vitest
npm run db:generate  # Drizzle Kit generate
npm run db:migrate   # Apply migrations
npm run db:studio    # Visual DB browser
npm run email:dev    # React Email preview server
npm run stripe:listen # Forward Stripe webhooks to localhost
```

---

## QUALITY GATES

□ All schema changes have migration file (NEVER manual SQL in production)
□ Stripe webhook handler tested with `stripe trigger` CLI
□ Feature gates tested for free + paid tiers
□ Email templates render correctly in React Email preview
□ `next build` passes — 0 errors
□ No DB calls in Client Components (use Server Actions)
□ All pricing info from Stripe API — NEVER hardcoded prices in UI
□ Webhook signature always verified before processing events

---

## FORBIDDEN

- NEVER hardcode prices in the UI (fetch from Stripe or config)
- NEVER store raw card data (Stripe handles PCI compliance)
- NEVER skip webhook signature verification
- NEVER edit existing migration files (create new migration instead)
- NEVER expose `STRIPE_SECRET_KEY` to client side
- NEVER use `NEXT_PUBLIC_` prefix for sensitive keys
- NEVER trust client-side plan checks for access control (verify server-side)
