Output the full CashFlow project continuation context below, exactly as written. This is used to orient a new Claude Code session.

---

# CashFlow — Project Context

## What This App Is
CashFlow is a personal finance mobile-first web app combining personal expense tracking and real-time group/individual expense splitting between linked CashFlow users.

- **Live:** cash-flow-zrs8.vercel.app
- **GitHub:** MR-Abdur-Rahman/CashFlow
- **Local:** D:\CashFlow
- **Supabase project ID:** rgarmhwdoyeozkznsjek
- **Test accounts:** User A (Rahman M.R.A), User B, User C, User D, Haneen

## Tech Stack
React 19 + TypeScript + Vite + Tailwind CSS v4 + shadcn/ui + TanStack Query v5 + Supabase + React Router DOM v7 + Sonner (toasts) + Vercel

## Key File Paths
- Routes: `src/routes/_authenticated/`
- Shared queries: `src/lib/queries.ts`
- Components: `src/components/`
- Supabase client: `src/integrations/supabase/client.ts`
- Types: `src/integrations/supabase/types.ts`

## Design System
- Background: #0A0A0A | Card: #1A1A1A | Border: #2A2A2A
- Purple accent: #7C3AED | Income: #22C55E | Expense: #EF4444
- Transfer: #3B82F6 | Split amount: #F59E0B | Lent: #10B981
- All amounts: monospace font
- Date format: "Jun 23, 2026 · 11:11 AM"
- Toast: always use `toast.custom()` — never `toast.success()` / `toast.error()`

## Confirmed Working — DO NOT Re-implement
- Split row formats (Person/People/Group × You Paid / Other Paid)
- Settlement row format (4-line, emerald border, iPaid from split's payer)
- Net balance calculation (bilateral, third-party skip)
- Notification system (DB tables, triggers, bell, dropdown, realtime)
- Cross-user auto-contact (DB trigger, SECURITY DEFINER)
- Pending tab (account selection confirm flow, max 3 limit)
- RLS policies on splits, split_shares, groups tables
- toast.custom() colored backgrounds per type
- Sort order on person detail page (newest first, merged list)
- Account detail page shows split after account selection

## Key Business Rules
- `account_pending = true` → no account deduction at creation; deduct only on confirm
- Settlement direction: iPaid uses split's payer, NOT settlement's share linkage
- Bilateral balance: skip third-party payer splits
- Creator's implicit share has no split_share row — needs manual settlement handling
- Split type in DB = "individual" not "person"
- Cannot mix local contacts + linked CashFlow users in same split/group

## Important Learnings
- `invalidateQueries({ queryKey: ['splits'] })` already does prefix matching — adding `exact: false` is redundant
- Missing joins in a query return wrong data even after a correct re-fetch — check `select()` first
- `SECURITY DEFINER` required for cross-user DB operations
- TanStack Query key mismatches are the #1 cause of history not updating after inserts
- `richColors` prop on Sonner's `<Toaster>` overrides custom toast backgrounds — keep it removed

## Remaining Bug Queue (Priority Order)
1. Payer category selection — hide category on "Other Paid" split creation; add category picker to Pending tab row
2. Reports: splits where current user is PAYER show in Expense tab under split's category
3. Balance restoration on split/settlement delete
4. Split edit corruption bug (Person split → People type with duplicate names)
5. Delete permission: creator OR payer (not creator-only)
6. Settlement account direction fix (Haneen bug)
7. Settle Up dialog redesign (net-balance-only, no split checkboxes)
8. FIFO settlement allocation
9. Group member balances (bilateral, not per-member total)
10. Group split row format fix
