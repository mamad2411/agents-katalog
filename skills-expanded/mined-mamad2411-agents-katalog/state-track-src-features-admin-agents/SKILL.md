# Admin Module Knowledge Base

## OVERVIEW
Handles system administration, report management, and analytics. Features precision real-time synchronization and conflict resolution.

## STRUCTURE
```text
src/features/admin/
├── AdminDashboard.tsx      # Analytics & Report Table (Conflict Detection)
├── AdminSettings.tsx       # System configuration entry
├── settings/               # Sub-settings modules
└── useSystemSettings.ts    # Centralized configuration hook
```

## CORE LOGIC
- **Conflict Resolution**: Uses `updated_at` comparison to detect remote changes during local edits.
- **Real-time Stats**: Subscribes to `reports` channel to update dashboard metrics regardless of active tab.
- **WhatsApp Integration**: Mocked notification trigger for report status updates.

## CONVENTIONS
- **Synchronization**: Always trigger `fetchStats()` on real-time events.
- **Audit Logs**: All manual changes to reports must be logged to the `report_logs` table.

## ANTI-PATTERNS
- **Silent Failures**: Always wrap Supabase mutations in try-catch with `handleApiError`.
- **Overwrite**: Never save without checking timestamp unless `force=true`.

