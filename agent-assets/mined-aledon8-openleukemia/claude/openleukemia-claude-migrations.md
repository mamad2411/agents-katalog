# Supabase Migrations Memory

Apply this inside `supabase/migrations/`.

- Model identity, medical data, consent records, documents, and audit events deliberately.
- Prefer explicit constraints, timestamps, and readable names.
- Pair sensitive tables with RLS policies.
- Do not weaken privacy or authorization behavior in a migration without a clear reason.
- Verify migrations against expected schema shape and name any rollback or data-risk assumptions.
