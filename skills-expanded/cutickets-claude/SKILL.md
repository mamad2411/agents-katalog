# Morningside Tickets

This is a fixed-price ticket marketplace for verified Columbia and Barnard
students. Sellers create listings; buyers reserve a quantity and enter a private
deal chat. The app never handles payment or ticket transfer.

## Commands

```bash
npm run dev
npm run build
npm run db:push
npm run db:seed
npm run db:studio
npx tsc --noEmit
```

## Core lifecycle

- Listing: `OPEN | SOLD_OUT | CANCELLED`. Expiry is computed from `expiresAt`.
- Deal: `RESERVED | COMPLETED | CANCELLED | EXPIRED`.
- `reserveListing` atomically decrements available inventory before creating a deal.
- A deal opens chat and reveals contact details immediately.
- Cancelling or expiring a deal restores quantity unless the listing was cancelled or expired.
- Public-facing sale stats (event sale counts, last-sale price, seller reputation, sold history) count a deal as sold the moment it's `RESERVED`, per `soldDealWhere()` in `src/lib/deals.ts` — only a `CANCELLED`/`EXPIRED` reservation falls back out. This is separate from `Deal.status` itself: both parties still independently confirm before a deal becomes `COMPLETED`, which gates chat-thread lifecycle messages and unlocks rating.
- Reservation expiry is handled by the protected cron route.
- Events auto-archive the day after they start, via the protected `/api/cron/archive-events` route (~4am NYC), reusing the same archive path as the manual admin action — open listings get cancelled and sellers notified. An archived event's page 404s for non-admins; admins can still open it directly or via the "Archived" tab in `/admin/events`.

Money is stored as integer cents. Acting user IDs always come from the server
session. Event listing pages do not select seller identity. Email, phone, and
notes are otherwise restricted to deal participants or the allowlisted admin
area.

There is one admin tier. Access is controlled only by the two-email allowlist in
`src/lib/admin.ts`; do not add database roles or admin invitations. Admins can
inspect all users and their histories at `/admin/users`, and all trades at
`/admin/deals`. Each paginated sale row exposes its full chat transcript inline;
`/admin/deals/[id]` remains the dedicated record for that chat and its ratings.

Mutations live in `src/lib/actions/`. Schema changes that ship require a committed
PostgreSQL migration because Vercel runs `prisma migrate deploy` during builds.

Local dev login is controlled by `ALLOW_DEV_LOGIN=true` and is always disabled in
production. Phone onboarding requires Firebase unless test data is marked verified
directly in the database.
