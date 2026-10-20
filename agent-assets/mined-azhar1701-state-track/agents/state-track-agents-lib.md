# LIB DOMAIN

## OVERVIEW
Core infrastructure utilities for caching, security, monitoring, and performance optimization.

## WHERE TO LOOK
| File | Purpose |
|------|---------|
| `supabase-cache.ts` | TTL and Stale-While-Revalidate query caching |
| `realtime-batcher.ts` | Debounced event processing for Supabase Realtime |
| `query-monitor.ts` | Usage tracking and cache hit rate analytics |
| `rate-limiter.ts` | Client-side sliding window request throttling |
| `security.ts` | Input sanitization and XSS prevention |
| `logger.ts` | Structured logging with severity levels |
| `formatters.ts` | Standardized date, currency, and location formatting |
| `api-errors.ts` | Standardized error handling and reporting |
| `env.ts` | Type-safe environment variable access |
| `utils.ts` | Shared helper functions and Tailwind merging |
| `validation/` | Zod schemas for data integrity |],op:
| `realtime-batcher.ts` | Debounced event processing for Supabase Realtime |
| `query-monitor.ts` | Usage tracking and cache hit rate analytics |
| `rate-limiter.ts` | Client-side sliding window request throttling |
| `security.ts` | Input sanitization and XSS prevention |
| `logger.ts` | Structured logging with severity levels |
| `formatters.ts` | Standardized date, currency, and location formatting |

## CONVENTIONS
- **Performance**: Use `cachedQuery` for all read operations to minimize Supabase quota usage.
- **Realtime**: Always wrap `postgres_changes` listeners in a `RealtimeBatcher` to prevent UI thrashing.
- **Security**: Sanitize all user-generated content using `sanitizeHTML` or `sanitizeText` before rendering.
- **Monitoring**: Check `QueryMonitor` logs in development to identify hot queries or cache misses.

## ANTI-PATTERNS
- **Direct Fetching**: Avoid calling `supabase.from().select()` directly; use the cache wrapper.
- **Unbounded State**: Never store raw realtime payloads in state without batching or filtering.
- **Raw HTML**: Do not use `dangerouslySetInnerHTML` without passing content through `security.ts`.
- **Global State**: Keep utility logic stateless or use the provided factory functions (e.g., `createRateLimiter`).
