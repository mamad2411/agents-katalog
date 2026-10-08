# CLAUDE.md

> This file is auto-loaded by Claude Code and similar coding agents at the start of every chat in this repo. Keep it **skimmable** — bullets, not prose. Deep references live in `AGENTS.md`, `steady_rise_ui_rules.md`, and `docs/design_system.md`.

---

## System Purpose

SRFM (SteadyRise Family Money) is a multi-tenant household finance system — replaces EveryDollar, Mint, Quicken, Excel for families tracking budgets, transactions, accounts, net worth.

Two personas (UI must serve both):
- **Family budget managers** (majority) — non-experts from EveryDollar/Mint/spreadsheets. Guided, plain-language, mobile-first.
- **Accountants/bookkeepers** (minority) — power users from Quicken/Excel. Dense data, reconciliation, detailed reporting.

Stack:
- Backend: .NET 8 + `Npgsql` direct SQL in `/api`. Supabase/Postgres = source of truth. Firebase auth.
- Frontend: Quasar + Vue 3 + Pinia SPA in `/q-srfm`.
- Flow: UI → stores/composables → `q-srfm/src/dataAccess.ts` → REST → controllers → services → Postgres.

Migration state is mixed — most domain CRUD is Supabase; auth/email verification still Firestore (`AuthController`); `StatementService` write paths and parts of account import are `NotImplementedException`.

---

## Design System — READ BEFORE TOUCHING UI

The authoritative design system for SRFM lives at **`design-system/`**. Canonical files:

- **`design-system/README.md`** — full brand, content, visual, and iconography foundations.
- **`design-system/colors_and_type.css`** — CSS custom properties for every token. Matches `q-srfm/src/css/quasar.variables.scss` and `app.scss`.
- **`design-system/assets/`** — the turtle mascot (full / sm / icon).
- **`design-system/ui_kits/srfm-app/`** — React/JSX reference mocks for sidebar, Dashboard, Budget, Transactions, Inspector. **Reference only** — Quasar is Vue; do not import.
- **`design-system/preview/`** — small standalone HTML cards documenting the system (colors, type, spacing, buttons, chips, etc.). Open directly for a visual reference.
- **`design-system/SKILL.md`** — agent-invokable skill entrypoint (`srfm-design`).

Long-form v0.1 rules (typography scale, ledger appendix, form/modal standards) live in **`steady_rise_ui_rules.md`**. Team-facing implementation standard in **`docs/design_system.md`**.

### Mode — pick one per page

- **Coaching** (comfortable density, encouraging): Dashboard, Budget, Goals.
- **Auditing** (compact, precise): Transactions, Registers, Account Register.
- Never mix modes inside one page.

### The rules that most often get violated

1. **Color = state, not style.** `$primary` (`#2563EB`) for interactive elements only. Neutrals carry ~90% of the UI.
2. **`$warning` (`#E65100`) is "over budget" and "needs attention." `$negative` (`#DC2626`) is destructive + error only.** Never use red for over-budget.
3. **Dates display as `mm/dd/yyyy`.** Storage stays ISO `YYYY-MM-DD` for sortability; convert at the input/display boundary.
4. **Cards summarize, tables audit.** Never wrap a ledger/register in a decorative card.
5. **Tabular numerals on every numeric column.** Right-aligned.
6. **Icons: Google Material only, by name.** No inline SVG, no emoji in chrome.
7. **Inter only.** One type scale. 14px body min on desktop; 16px on mobile viewports (prevents iOS zoom-on-focus).
8. **Spacing is 4 / 8 / 12 / 16 / 24 / 32 only.** Map to Quasar `q-pa-*` / `q-ma-*`. Arbitrary values are rejected.
9. **Dialogs are last resort; prefer inspector drawer on desktop, full-screen dialog on mobile.**
10. **One primary action per surface.** Secondaries = outline / flat. Destructive = separated, always confirmed.

### Token reference

| Token | Hex | Usage |
|-------|-----|-------|
| `primary` | `#2563EB` | Primary actions, links, active states |
| `secondary` | `#0F766E` | Rare secondary emphasis |
| `accent` | `#6366F1` | Very limited highlights |
| `positive` | `#16A34A` | Income received, completed goals |
| `warning` | `#E65100` | Over budget, needs attention |
| `negative` | `#DC2626` | Destructive, error |
| `info` | `#0284C7` | Informational messaging |
| `grey-1` | `#F8FAFC` | Page background |
| `grey-3` | `#E2E8F0` | Borders / dividers |
| `grey-7` | `#475569` | Muted text |
| `grey-9` | `#0F172A` | Primary text |

Reference by token name (`color="primary"`, `text-warning`, `--color-surface-card`) — never hard-code hex.

### Before you commit UI changes

Grep for these — they indicate regressions against the system:

```bash
rg "text-negative"                 q-srfm/src/   # should only appear on destructive/error, not "over budget"
rg 'mask="####-##-##"'             q-srfm/src/   # old ISO date mask — replace with ##/##/####
rg "#F59E0B|#f59e0b"               q-srfm/src/   # old warning hex — should be #E65100
rg "🎉|Great job|All good"         q-srfm/src/   # celebration copy — violates "calm, not cheerleading"
```

### When adding a new page or component

1. Pick the **mode**: Coaching or Auditing. Never mix inside one page.
2. Commit to existing primitives in `q-srfm/src/components/` before adding new ones.
3. Use tokens (`color="primary"`, `text-warning`, `--color-surface-card`) — never hard-code hex.
4. Verify at **375px viewport** before calling it done. 44×44px tap targets. Responsive table pattern (card view or scroll with affordance) — never just column truncation.
5. Every accounting term (Cleared / Reconciled / Uncleared / Budget Register / Account Register) must ship with a `q-tooltip`. See README "Tooltips — the knowledge bridge" for fixed copy.

### Mobile-first requirements

- Mobile is ~50% of usage — primarily on-the-go transaction entry. Users from EveryDollar/Mint expect a polished mobile-native experience.
- Evaluate every UI change at **375–430px** before considering it complete.
- 44×44px tap targets. Correct input types (`number`, `date`, `tel`).
- Prefer bottom sheets or full-screen modals over inline panels on mobile.
- Base font ≥ 16px on mobile (iOS auto-zoom prevention).
- No `user-scalable=no` / `maximum-scale=1` in viewport meta (WCAG 2.1 AA violation).
- Sidebar drawer must **not** auto-open on mobile navigation — known critical bug. Bottom tab bar is primary mobile nav.
- Tables use responsive patterns (card views, expandable rows, scroll with affordance) — never column truncation alone.

### UX and terminology

- Accounting terms (Reconciled, Cleared, Uncleared, Budget Register, Account Register) ship with `q-tooltip`. **Labels remain unchanged; tooltips bridge the gap.**
- Empty states always include guidance and actionable next steps — never just "No data."
- Destructive actions require a confirmation dialog that names the affected item and states the impact. Use `color="negative"`, never plain text links or unlabeled icons.
- Budget page unmatched-transaction trash icons perform **soft delete** (restorable from "Deleted" tab). Style muted/outlined + tooltip explaining restore.
- All write operations provide visible success feedback via `$q.notify`.
- Page titles are semantic `h1`. Maintain heading hierarchy.
- Transactions page has no subtitle.
- Default post-login landing is the **Budget page**, not Dashboard.

### Onboarding

- **Hybrid model.** `/setup` is a single-page seed form (`q-srfm/src/components/onboarding/SetupSeedForm.vue` mounted by `SetupPage.vue`) that creates family + entity + Income group + first budget + optional accounts in one transactional submit via `POST /api/onboarding/seed` (`OnboardingService.SeedAsync`). It uses a dedicated `OnboardingLayout.vue` — no sidebar, no bottom tab bar, just a small SRFM header and a Sign-out escape — so brand-new users can focus.
- **Two modes.** `seed` (fresh user, no family yet — entered via the auto-redirect from `BudgetPage` when `family` or `entities[]` is empty) and `add-entity` (existing user from Settings → "Quick setup with starter budget"). Both render the same form; mode just toggles the family-name input and the headline copy.
- **Persistent checklist.** Everything past the seed (link a bank, set up a goal, verify email, reconcile, invite a partner) is surfaced via the existing `GettingStartedChecklist` component backed by `useTourStore` (`q-srfm/src/store/tour.ts`). The store has 7 derived items as of PR 4 of the SetupWizard rewrite. Items tick automatically as the underlying data appears (e.g. `verify-email` ticks when `auth.user.emailVerified === true`).
- **Email verification.** `EmailVerificationBanner.vue` mounts on Budget + Dashboard whenever `auth.user.emailVerified === false`. Resend has a 60s cooldown to avoid Brevo rate-limits. `VerifyEmailPage` auto-redirects authenticated users back to `/budget` after a 1.5s confirmation.
- **`SetupWizardPage` and `GroupNamingForm` are deleted** (Vuetify-era stepper that silently dropped `templateBudget` and `taxFormIds`). Don't reintroduce a stepper. `EntityForm.vue` is kept for the "edit existing entity" flow accessible from Settings.
- **`Entity.templateBudget` and `Entity.taxFormIds` are persisted** as of the 2026-04-21 migration (JSONB + TEXT[] on `entities`). Forms that collect these fields can rely on round-trip persistence.

---

## Core Invariants (Must Not Be Broken)

- Firebase Bearer token is the auth primitive. `AuthorizeFirebase` populates `HttpContext.Items["UserId"]` and `HttpContext.Items["Email"]`.
- `family_members` membership is the primary authorization relation for family-scoped resources.
- Budget carryover applies only to `BudgetCategory.IsFund == true`. Negative results propagate forward — an overspent fund carries the deficit into subsequent months instead of resetting to zero, so users see the fund is still in the hole. `CurrencyInput` accepts negative values when `allow-negative` is set (used on the carryover field in the budget editor).
- Every persisted transaction has ≥ 1 category split (`Income` / `Uncategorized` fallback). Transaction category rows are replaced on write.
- `entity_id` is a first-class partition key for budgets/goals; stay consistent on merge/derive.
- Goal-linked budget categories are hidden from regular budget/category queries via `goals_budget_categories` exclusion in `BudgetService.LoadBudgetDetails`. Reconciliation/match flows (batch matching, account ledger, Transactions-page Budget Register) opt out via `includeGoalOnlyTransactions=true` so pure goal contributions/withdrawals stay reachable for clearing — those callers must fetch fresh and not write back into `useBudgetStore` (the store keeps the goal-filtered cache for the Budget page).
- Goal funding is two-effect, single-entry. A goal-funded expense is a *standard* `Transaction` (counts toward the destination category's spend) carrying `funded_by_goal_id` (persisted FK to `goals.id`). The same column drives the goal's spend rollup. Do not auto-convert goal-funded expenses to transfers — that pattern was removed because it credited the destination category's available and erased the expense.
- `goals.notes` is persisted HTML emitted by Quasar `q-editor` in `GoalDialog.vue`. The client MUST sanitize via DOMPurify before any `v-html` rendering (see `GoalDetailsPanel.vue`). Sanitization is render-side, not save-side — legacy plaintext and any future policy tightening stay safe; never `v-html` raw `goal.notes`.
- Category-level funding source defaults: `BudgetCategory.fundingSourceCategory` (name of another category) and `BudgetCategory.fundingSourceGoalId` (UUID FK to a goal) are mutually exclusive (DB CHECK). `fundingSourceGoalId` requires the goal to belong to the same entity as the budget — enforced in `BudgetService.SaveBudget`. `TransactionForm` reads these to default the per-transaction source/goal at save time.
- Account enums: `Bank / CreditCard / Investment / Property / Loan`, `Asset / Liability`. Keep frontend aligned with API/DB.
- Month ordering is lexicographic `YYYY-MM`.
- `status` (`U` Uncleared / `C` Cleared / `R` Reconciled) and `matched` are **independent** concepts on a transaction. Matching links a bank row to a budget transaction; reconciling finalizes a statement. **Unmatch must revert status `C → U` on both the imported row and the linked budget transaction** (and clear the budget row's bank-linkage fields). The revert is unconditional — the `R` guard lives in the UI (`LedgerTable` hides Unmatch on reconciled rows), not in SQL. See `docs/adr/0001-unmatch-reverts-status-to-uncleared.md`.
- A budget transaction's link to the bank row it was matched to is the explicit `transactions.imported_transaction_id` (the composite TEXT id of `imported_transactions`). Set on match, nulled on unmatch. Do not reconstruct matches from `account_number` + payee + date except as a legacy fallback for rows whose link is NULL.

---

## Data & State Ownership

**Server = source of truth.** Supabase/Postgres: `families`, `family_members`, `entities`, `budgets`, `budget_groups`, `budget_categories`, `transactions`, `transaction_categories`, `goals`, `goals_budget_categories`, `accounts`, `snapshots`, `imported_*`. Firestore remains source for auth verification metadata in `AuthController`.

**Group taxonomy is entity-scoped.** Every category group lives in `budget_groups (entity_id, name UNIQUE, sort_order, kind)` with `kind IN ('income','expense','savings')`. `budget_categories.group_id` FKs to it; `budget_categories.sort_order` orders within a group. Renaming/reordering applies to every month automatically. **Income detection uses `kind === 'income'`, never string equality on group name.** Helpers in `q-srfm/src/utils/groups.ts`: `isIncomeCategory`, `categoryGroupKind`, `categoryGroupName`.

**Client:**
- `useBudgetStore` owns in-memory budget cache by `budgetId` — intentionally **not** persisted (localStorage quota).
- `useFamilyStore` owns current family + `selectedEntityId`. Most pages assume it's set.
- `dataAccess` normalizes shapes before state enters stores.
- `store/entities.ts` duplicates the family store and is unused — don't add references.

---

## API Contracts

- Protected endpoints: `Authorization: Bearer <Firebase ID Token>`.
- IDs mostly UUIDs; some API fields use strings (`budget.id`).
- `src/dataAccess.ts` is the single contract surface — all API changes flow through it first.

Known drift (preserve awareness, don't paper over):
- Frontend calls `POST /api/statements/finalize`; no matching controller route.
- `StatementService` write/unreconcile are `NotImplementedException`.
- `AcceptInvitePage` links to `/signup`; router has no `/signup` route.

Recent additions worth knowing:
- `GET /budget/batch?ids=...&includeGoalOnly=true` and `GET /budget/{id}?includeGoalOnly=true` skip the `LoadBudgetDetails` goal-only-transaction filter. Used by match/registry surfaces. `dataAccess.getBudgetsBatch(ids, { includeGoalOnly: true })` and `dataAccess.getBudget(id, { includeGoalOnly: true })` are the typed entry points.
- `GET /budget/imported-transactions` is **family-scoped** as of 2026-05-09, not importer-scoped — any family member sees imports done by any other member. `BudgetService.GetImportedTransactions(uid)` filters by `EXISTS family_members fm WHERE fm.family_id = d.family_id AND fm.user_id = @uid`. Don't reintroduce a `d.user_id = @uid` filter on shared-account reads.
- `GET /reports/by-payee?entityId=&from=&to=&excludeGroupIds=&excludeCategoryNames=&excludeMerchants=` (2026-05-10) aggregates net spend by payee over a `YYYY-MM` range. `ReportsService` enforces entity-membership via a single JOIN against `entities → family_members` (closes the `GoalController`-style gap — do not copy that gap into new report endpoints). The canonical payee key in SQL trims, collapses whitespace, folds curly/grave/acute apostrophe variants to ASCII `'`, then `LOWER()`s for case-insensitive grouping; display value comes from `MODE() WITHIN GROUP (ORDER BY …)` so the table reads naturally. The same `LOWER(payeeCanonical)` is reused in the `excludeMerchants` `WHERE`, and `NormalizePayeeKey` in `ReportsService` mirrors the SQL transform for client-supplied strings — keep them in lockstep. Typed entry point: `dataAccess.getSpendingByPayee(entityId, from, to, opts)`.
- `POST /budget/imported-transactions/{importedId}/unmatch` (2026-06-12) is the canonical, account-agnostic unmatch: it reverts the bank row to `U` and resets every linked budget transaction (via `transactions.imported_transaction_id`, with the legacy account+payee+date heuristic as fallback for NULL-link rows), shedding bank-linkage fields. `BudgetService.UnmatchImported` returns the count of budget rows reset. Typed entry point: `dataAccess.unmatchImported(importedId)`. The frontend register Unmatch uses this — it no longer requires a single account to be selected. `BatchReconcileTransactions` also sets/clears the link and reverts status on its match/unmatch branches.

Validation assumptions:
- Some controllers enforce explicit validation (account enums, statement ID match, merge preconditions).
- Others rely on service/DB failures for invalid IDs (`Guid.Parse`).
- Don't silently broaden enum/domain values without DB/schema changes.

---

## Security Model

- Client → API: Firebase ID token.
- API → Postgres: connection string secret.
- API → Brevo/Stripe/Plaid: configured secrets.
- `[AuthorizeFirebase]` + resource-level checks (membership/owner) on most sensitive controllers.
- Family owner-only ops: `FamilyController` compares `family.OwnerUid` with authenticated `uid`.

Known gaps (do not replicate):
- `BudgetController.GetBudget` does not verify caller access to the requested budget.
- `GoalController` accepts `entityId` without membership check.
- CORS origins are hardcoded allowlist in `Program.cs`.
- `UseAuthorization()` runs without ASP.NET auth scheme middleware — security relies on the custom filter.

Resolved gaps (kept here as guardrails — don't regress):
- `AuthorizeFirebaseAttribute` reads the `email` claim with `?.Value` so tokens without an email (e.g. anonymous, phone, custom-token sign-in) don't throw NRE. `HttpContext.Items["Email"]` may legitimately be `null`; consumers must handle that.
- `AuthorizeFirebaseAttribute` invokes `await next()` *outside* the token-verification try/catch. Don't merge them — that previously masked controller exceptions as "Token verification failed" and made debugging unrelated NREs nearly impossible.

---

## Concurrency & Side Effects

- Handlers are async and mostly stateless.
- `BudgetService` uses `SemaphoreSlim` to memoize existence check for `budget_edit_history`.
- `SupabaseLogger` serializes DB log writes with a static lock.
- `SaveBudget` upsert runs in a DB transaction; transaction rows may persist afterward via separate calls.
- Batch transaction saves use `NpgsqlBatch` + transaction.
- Carryover recalc reads sequential budgets and writes in a transaction.
- Reconciliation updates imported + budget transactions in separate statements without a wrapping DB transaction — eventually consistent within the request.
- Invite email send is compensating — pending invite is deleted on send failure.
- Writes are upsert-by-ID; callers usually generate IDs client-side (UUID).

---

## Extension Guidelines

**Adding a feature:**
- Backend: controller endpoint → matching service → parameterized SQL via `NpgsqlCommand`.
- Frontend: method in `src/dataAccess.ts` first → wire store/composable/page.
- Prefer existing `family_id` / `entity_id` / membership-check patterns.

**UI changes (governance):**
- `design-system/` + `docs/design_system.md` are authoritative. Markers in `docs/design_system.md`:
  - `[ENFORCED]` — mandatory, no exceptions without explicit human approval.
  - `[SUGGESTED]` — preferred default; deviations must be intentional and justified.
  - `[ASSUMPTION/UNCLEAR]` — don't guess silently; call out and request clarification.
- Reuse Quasar primitives + existing SRFM components before creating new ones.
- Tokenized styling only — no hard-coded hex, no arbitrary spacing when tokens cover the use case.
- Preserve accessibility minimums (contrast, keyboard operation, dialog behavior, semantic labels, reduced motion).
- When touching legacy inconsistent code, move toward canonical direction — don't extend legacy patterns.
- New token / variant / theming mode requires updating `design-system/` (and `docs/design_system.md`) in the same change.

**Modifying existing logic:**
- Preserve `YYYY-MM` month strings and carryover semantics.
- Preserve goal-bound category exclusion.
- Never persist a split-less transaction.
- Keep optimistic store updates synchronized with API responses.

**Dependencies:**
- API: direct SDK usage + lightweight services — no heavy ORMs without a migration plan.
- Frontend: keep `fetch` in `dataAccess` — no second HTTP client.

**Naming / conventions:**
- Backend: `*Controller`, `*Service`, PascalCase DTOs.
- Frontend: `useXStore`, `useX` composables, types in `src/types.ts`.
- API returns `BadRequest` for operation failures + logs details.
- Frontend throws on non-OK; pages surface messages.

---

## Anti-Patterns to Avoid

- Bypassing `family_members` / owner checks for new family-scoped endpoints.
- **User-scoping shared family resources.** Family-shared data (imported transactions, budgets, accounts, goals) must be visible to every member of the family, not just the importer/creator. Filter by `family_id` membership, never by the doc's `user_id`. `BudgetService.GetImportedTransactions` was bug-fixed in this direction (2026-05-09); don't add new endpoints that scope by `user_id` for shared resources.
- UI components calling `fetch` directly instead of extending `dataAccess`.
- Persisting large budget datasets to localStorage.
- Mixing entity-scoped and non-entity-scoped data in one query without explicit `entity_id` logic.
- Non-transactional multi-table writes in hot paths where existing code expects atomic behavior.
- Creating parallel store implementations for the same domain (existing duplication is already a risk).
- Ignoring design-system tokens; inline styles, direct hex values, arbitrary spacing/radius.
- Mixing Vuetify-era classes/APIs into Quasar components.
- **Bypassing the transfer model for true transfers.** A category-to-category move is a `transactionType: 'transfer'` with signed splits — negative on the source, positive on the destination. Aggregations that branch on `transaction.isIncome` must also branch on `transactionType === 'transfer'`; see `q-srfm/src/utils/reportAggregations.ts` for the canonical pattern. Do not record an inter-category transfer as a standard income/expense pair.
- **Modeling goal-funded expenses as transfers.** Goal funding is *not* a transfer. A goal-funded expense is a regular standard expense recorded on the destination category (so it counts toward that category's spent / available) with `funded_by_goal_id` persisted on the transaction. The goal's savedToDate / spentToDate are derived server-side in `GoalService.GetGoals` (see the `funded_agg` sub-aggregation) and listed in `GoalService.GetGoalDetails`. New write paths must persist `fundedByGoalId` on a standard expense; do not auto-convert to a transfer at save time. Historical goal-funded transfers in the DB still work via the existing transfer-source-split path — the goal reader supports both shapes.
- Desktop-only UI. Any new page, dialog, or form must be usable at 375px without horizontal scroll or broken tap targets.
- `user-scalable=no` / `maximum-scale=1` in viewport meta (WCAG violation).
- Empty states without actionable guidance; error states while data is still loading.
- Destructive actions as plain text links or small unlabeled icons.
- Placeholder-only form labels that disappear on focus.
- Base font below 16px on mobile viewports.
- Sidebar drawer auto-opening on mobile page navigation.
- Accounting terminology without accompanying tooltips or plain-language help.
- Celebration copy (`🎉`, "Great job", "All good") — violates "calm, not cheerleading."
- **Grouping by free-text user input (merchant/payee names) without normalization.** Raw `transactions.merchant` carries curly vs ASCII apostrophes ("McDonald's" vs "McDonald's"), case differences ("COSTCO" vs "Costco"), and stray whitespace — each variant hashes to its own row and the report fragments. Reuse the `ReportsService` `payeeCanonical` pattern (trim → collapse whitespace → fold apostrophe variants → `LOWER`) for any aggregation, and mirror the same transform server-side on user-supplied filter strings so exclusions match the grouped key.
- **`v-html` on user-supplied content without DOMPurify.** Any field that round-trips through Quasar `q-editor` (today: `goals.notes`) is HTML and must be sanitized at render time. Don't move sanitization to the save path; sanitizing on render also cleans legacy plaintext and lets policy tighten without rewriting stored content.

---

## Testing Expectations

Baseline:
- Frontend: Node-based TS tests in `q-srfm/tests/transactions.test.ts` (duplicate/date-window helpers, budget month sorting).
- Backend: no meaningful automated tests.

Minimum for new changes:
- Unit tests for pure logic in composables/utils (reconciliation matching, carryover math, sorting/filtering).
- API behavior changes: targeted endpoint checks + negative authorization cases.
- Contract changes: verify API endpoint and `dataAccess` caller paths together.

Unclear: no established integration-test harness, no CI-enforced gates visible in repo.

---

## Change Risk Map

**High-risk zones:**
- `api/Services/BudgetService.cs` — central financial state, carryover propagation, reconciliation, import updates.
- `api/Controllers/FamilyController.cs` + `api/Services/FamilyService.cs` — tenancy and ownership boundaries.
- `api/Filters/AuthorizeFirebaseAttribute.cs` — auth context foundation for most protected routes.
- `q-srfm/src/dataAccess.ts` — single frontend contract adapter; drift breaks multiple pages.
- `q-srfm/src/pages/TransactionsPage.vue` + `q-srfm/src/components/TransactionRegistry.vue` — reconciliation workflows depend on interrelated assumptions.

**Migration-sensitive:**
- Firestore/Supabase seam in `AuthController` + Firebase profile setup.
- Statement/account import paths with `NotImplementedException`.
- Feature-flagged optional tables (`budget_edit_history`, `goals_budget_categories`).
- `goals.notes` TEXT column (2026-05-11 migration, `db/migrations/20260510_goals_notes.sql`). Nullable; legacy rows untouched. Persisted HTML from `q-editor`, sanitized via DOMPurify at render time. Plumbed through `GoalService.InsertGoal` / `UpdateGoal` / `GetGoals` (SELECT + GROUP BY include `g.notes`).
- `transactions.imported_transaction_id` TEXT column (2026-06-12 migration, `db/migrations/20260612_transactions_imported_transaction_id.sql`). Soft link to the composite `imported_transactions.id` (no hard FK — composite TEXT key, rows hard-deleted on doc delete). Indexed; best-effort backfill of unambiguous existing matches. **The match/unmatch SQL in `BudgetService` references this column unconditionally — the migration must run before deploying that code.** Used by `UnmatchImported` and the `BatchReconcileTransactions` match/unmatch branches.
- `BudgetService.EnsureGroupAsync(conn, tx, entityId, name, kind)` — canonical inline upsert for a group by name within an entity. Callers can persist a `BudgetCategory` carrying only `groupName`; backend resolves/creates.
- `BudgetService.WriteBudgetAndCategoriesAsync(conn, tx, budgetId, budget, logger)` — `internal static` helper that writes the budget row + replaces its categories within an existing transaction. Used by both `SaveBudget` and `OnboardingService.SeedAsync` so seed flows can compose budget creation with family/entity inserts inside a single Postgres transaction.
- `BudgetService.LoadBudgetDetails(conn, budget, includeTransactions, includeGoalOnlyTransactions=false)` — when the second flag is true, the SQL drops the `goals_budget_categories` EXISTS filter so pure goal contributions/withdrawals come through. Threaded into `GetBudgets(ids, includeGoalOnlyTransactions)` and `GetBudget(id, includeGoalOnlyTransactions)`; surfaced as `?includeGoalOnly=true` on the controller routes. Frontend callers using this flag (`MatchBankPanel`, `TransactionRegistry`, `useTransactions.hydrateBudgets`) must NOT write back into `useBudgetStore` — the store stays goal-filtered for Budget/Dashboard consumers.

**Known UI/UX violations requiring remediation (March 2026 review):**
- Viewport meta `user-scalable=no` / `maximum-scale=1` — WCAG, one-line fix.
- Sidebar auto-open on mobile navigation — critical bug in `MainLayout.vue`.
- 14px base font on mobile — needs 16px minimum.
- Missing heading hierarchy (Dashboard H4 only, no H1) across all pages.
- Transactions + Accounts pages — tables not responsive on mobile.
- Bottom tab bar missing Reports, Data Mgmt, Settings.
- Accounts — no delete confirmation.
- Data Mgmt — loading race renders error before fetch completes.

**Cross-system contracts:**
- DTO shapes in `api/Models/*` → frontend TS types and data mappers.
- Route names + payload shapes in `BudgetController`, `FamilyController`, `AccountController`, `GoalController`.

---

## Agent Skill

If you support Skills, invoke `srfm-design` (declared in `design-system/SKILL.md`). It pulls the README, tokens, and UI kit into context so you don't have to re-learn the system each turn.

---

## Deployments

- **Single entry point: repo-root `./deploy.sh`** with `--bump=patch|minor|major|none` (default patch), `--target=all|api|web` (default all), `--web-host=firebase|cloudrun` (default firebase), `--firebase-project=<id>`. API → Cloud Run via Docker; Web → Firebase Hosting (default) or Cloud Run via Docker.
- `deploy.sh` reuses `q-srfm/scripts/updateVersionAndDeploy.js <bump> --no-deploy` for the version bump + `.env.production` sync — single source of truth for that logic.
- The Firebase Hosting path runs `npm run build` (not `yarn build`) so the active Node version (set via `nvm use`) is honored. Yarn 1's shebang resolves to whatever Node it was installed under, which often disagrees with the LTS the script just selected.
- `ensure_lts_node` in `deploy.sh` auto-sources nvm and runs `nvm install --lts && nvm use --lts` if the host's `node -v` isn't an LTS major (`18|20|22|24|26|28`). `q-srfm/package.json` engines are LTS-only — non-LTS hosts (e.g. Node 25 "Current") fail engines checks unless this path runs.
- Firebase CLI is invoked via `npx --yes --package=firebase-tools firebase deploy ...` because the package's bin (`firebase`) doesn't match its package name; plain `npx firebase` resolves to the JS SDK and fails.
- `api/deploy.sh.old` and `q-srfm/deploy.sh.old` are kept around as legacy single-service scripts for reference; the unified `deploy.sh` supersedes both.

---

## See Also

- **`CONTEXT.md`** — domain glossary: the shared vocabulary (Family/Entity, Status vs Matched, Budget vs Account Register, Transfer vs goal-funded expense, recurring estimates, payee canonicalization). Read it when a term is ambiguous.
- **`docs/adr/`** — architecture decision records (e.g. `0001-unmatch-reverts-status-to-uncleared.md`).
- **`AGENTS.md`** — longer-form architecture, invariants, security model, extension rules (source for this file's non-UI sections).
- **`steady_rise_ui_rules.md`** — v0.1 deep UI rules: typography scale, ledger appendix, form/modal standards, buttons/actions detail.
- **`design-system/`** — canonical brand, tokens, iconography, and UI-kit reference.
- **`docs/design_system.md`** — team-facing implementation standard; complements `design-system/`.
- **`UI_UX_Review_SteadyRise.md`** — March 2026 review findings driving current remediation items.
- **`README.md`** — local dev + deployment.
