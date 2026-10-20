# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-02
**Commit:** ddc607f
**Branch:** update/production-grade-refactor

## OVERVIEW
SIPASDA is an Enterprise-Grade Geospatial Reporting application for public infrastructure. It features a unified "Liquid Glass" design system, AI-driven categorization, OSRM routing optimization, and real-time synchronization.

## STRUCTURE
```text
src/
├── components/   # Reusable UI (shadcn/ui + glass components)
├── features/     # Domain-driven modules
│   ├── admin/    # Dashboard, stats, conflict resolution
│   ├── map/      # OSRM routing, geospatial analysis, Leaflet
│   ├── reports/  # AI-assisted forms, outbox sync
│   └── home/     # Feature highlights & landing page
├── hooks/        # Shared React hooks (useAuth, useNotifications)
├── lib/          # Utilities (formatters, security, logger)
└── services/     # Supabase client, AI services & types
```

## CORE FEATURES (ENTERPRISE)
- **AI Vision**: Automatic category and severity recommendation in `ReportForm`.
- **OSRM Routing**: Precision technical team navigation implemented in `MapView`.
- **Conflict Resolution**: Timestamp-based collision detection in `AdminDashboard`.
- **Real-time Sync**: Bi-directional data flow using Supabase Realtime.
- **Offline Intelligence**: PWA with offline map tile caching.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| UI System | `src/index.css` | 3-tier Liquid Glass elevation |
| AI Service | `src/services/ai.ts` | Vision-based analysis |
| Routing Logic | `src/features/map/routeOptimization.ts` | OSRM pathing |
| Conflict UI | `src/features/admin/AdminDashboard.tsx` | Sync Collision Dialog |
| Shared Logic | `src/lib/formatters.ts` | Consolidated date/loc formatters |

## CONVENTIONS
- **Elevations**: `glass-surface` (base), `glass-floating` (cards), `glass-overlay` (drawers).
- **Motion**: `layoutId` for indicators, `AnimatePresence` for lifecycle.
- **Language**: Strictly Bahasa Indonesia for all user-facing strings.
- **Verification**: Zero errors policy (`npm run typecheck && npm run lint`).

## ANTI-PATTERNS
- **CLS**: Never use spinners; use `Skeleton` shimmers.
- **State Traps**: Be careful with `backdrop-filter` on `fixed` children (containing block).
- **Hardcoding**: No API keys or Indonesian strings in logic; use constants/services.

## COMMANDS
```bash
npm run dev           # Start development server
npm run typecheck      # Run TypeScript compiler
npm run lint           # Run ESLint
npm run build          # Production build
npm run test           # Run unit tests
npm run knip           # Dead code detection
```
