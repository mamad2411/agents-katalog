# HOME FEATURE KNOWLEDGE BASE

## OVERVIEW
The Home feature serves as the landing page and public dashboard, providing real-time statistics, report trends, and quick access to core platform functions.

## WHERE TO LOOK
| Component | Responsibility |
|-----------|----------------|
| `Home.tsx` | Main entry point, handles global stats fetching and realtime subscriptions. |
| `RecentReports.tsx` | Displays the latest 5 reports with caching and fallback logic. |
| `CategoryLegend.tsx` | Visual guide for report categories used in charts and maps. |
| `StatusLegend.tsx` | Visual guide for report lifecycle states (Baru, Diproses, Selesai). |
| `FAQ.tsx` | Static informational section for user onboarding. |
| `BottomCTA.tsx` | Final conversion point for guest users. |

## CONVENTIONS
- **Realtime Sync**: Uses Supabase `postgres_changes` to refresh stats and charts immediately when reports are updated.
- **Caching**: `RecentReports` uses `cachedQuery` with a 30s TTL to reduce database load on high-traffic landing pages.
- **Visual Feedback**: Uses `LoadingOverlay` and `Skeleton` shimmers for all async data fetching.
- **Responsive Charts**: Recharts components are wrapped in `ChartContainer` with `withAspect={false}` for better mobile scaling.

## ANTI-PATTERNS
- **Direct Supabase Calls**: Avoid raw `supabase.from()` calls in sub-components; prefer passing data down or using the caching layer.
- **Hardcoded Labels**: Never hardcode Indonesian strings for status or categories; use `STATUS_LABELS` or `CATEGORY_LABELS` constants.
- **Silent Failures**: Charts must show "Tidak ada data" or a warning instead of an empty white space if fetching fails.
- **Heavy Re-renders**: Keep the realtime subscription in `Home.tsx` and avoid redundant listeners in child components.
