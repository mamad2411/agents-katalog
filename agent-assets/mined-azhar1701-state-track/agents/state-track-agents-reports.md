# REPORTS DOMAIN KNOWLEDGE

## OVERVIEW
Manages the lifecycle of infrastructure reports, from AI-assisted creation to offline-first synchronization.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Report Creation | `ReportForm.tsx` | Main form with map, camera, and AI integration |
| Offline Storage | `outbox.ts` | IndexedDB schema and operations for pending reports |
| Sync Logic | `useOutboxSync.ts` | Background sync and online/offline transition handling |
| User History | `MyReports.tsx` | List view of submitted and pending reports |
| Success State | `ReportSuccess.tsx` | Post-submission confirmation and routing |

## CONVENTIONS
- **Draft Persistence**: `ReportForm` autosaves to `localStorage` every 500ms using `DRAFT_KEY`.
- **Image Handling**: All photos must be compressed via `browser-image-compression` before upload or outbox storage.
- **Geocoding**: Use `reverseGeocode` from `@/features/map/geocoding` to automatically populate location names.
- **Validation**: Use `reportSchema` (Zod) for both real-time UI feedback and pre-submission checks.

## ANTI-PATTERNS
- **Direct Supabase Calls**: Avoid calling Supabase directly for report submission; use `enqueueReportForSync` to ensure offline resilience.
- **Large Blobs**: Never store uncompressed images in IndexedDB; it causes performance degradation and storage quota issues.
- **Manual Sync Buttons**: Do not add manual sync triggers; the system relies on `navigator.onLine` events and Service Worker background sync.
