# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project: Subscription Slasher Dashboard
Next.js 14 app that detects recurring subscriptions from transaction data and helps users identify wasteful spending.

## Commands
- `npm run dev` - Start development server
- `npm run build` - Production build
- `npm run lint` - Run Next.js linter

## Non-Obvious Architecture

### State Management (Zustand)
- Store in [`lib/store.ts`](lib/store.ts) uses derived getters (e.g., `getFilteredSubscriptions()`) computed on-demand from state
- `loadTransactions()` auto-runs [`detectSubscriptions()`](lib/detect.ts:76) and stores results—don't call detection separately
- `slashedItems` tracks cancelled subscriptions; getters filter them out automatically

### Subscription Detection Logic ([`lib/detect.ts`](lib/detect.ts))
- Requires 2+ transactions per merchant to detect subscription
- Monthly pattern: ANY interval between 25-35 days (not all intervals)
- Amount consistency: max 10% variation between min/max charges
- Cancel score calculation: +30 for >500 INR, +25 for price spike >5%, +20 for duplicate category, +15 for Entertainment, +10 for <3 occurrences

### Merchant Normalization ([`lib/normalize.ts`](lib/normalize.ts))
- Pattern replacements run FIRST (e.g., `/nflx/i` → `'netflix'`)
- `MERCHANT_MAP` provides canonical display names (e.g., `'netflix'` → `'Netflix'`)
- Categories determined by keyword matching in `CATEGORY_KEYWORDS`

### Currency & Locale
- All amounts in INR (Indian Rupees), formatted with `en-IN` locale
- Price spike detection threshold: 5% increase

### File Parsing ([`lib/parser.ts`](lib/parser.ts))
- Auto-detects CSV/JSON by file extension
- CSV uses PapaParse with header:true
- JSON accepts both array and `{ transactions: [] }` format
- Date normalization: converts to ISO format (YYYY-MM-DD)

### Path Aliases
- Use `@/*` for imports (e.g., `@/lib/store`, `@/types`)
- Configured in [`tsconfig.json`](tsconfig.json:20-22)

### Dark Mode
- Uses next-themes with class-based approach
- `suppressHydrationWarning` on `<html>` tag required
