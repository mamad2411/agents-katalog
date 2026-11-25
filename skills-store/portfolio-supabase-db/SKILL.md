---
name: portfolio-supabase-db
description: "Create or review Supabase migrations and row-level access policies."
---

# portfolio-supabase-db

Use versioned migrations and explicit ordering; inspect the current schema before changing it. Coordinate ownership of backend client integration with the backend worker. Test anonymous, authenticated, and cross-user access including denied operations.

Use local isolated data for verification. Database reset is destructive and is not the generic migration-apply command; identify the target and authorization first. Never apply remote migrations implicitly. Keep service-role secrets server-side. Record rollout/rollback and generated type changes with candidate evidence.
