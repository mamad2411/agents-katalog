# Supabase Policies Memory

Apply this inside `supabase/policies/`.

- RLS is a primary protection layer, not a later add-on.
- Policies should make patient ownership and explicit consent enforceable.
- Keep access paths narrow and auditable.
- Treat document storage and normalized clinical data as separate access concerns.
- Review policy changes as security-sensitive even when the SQL diff is small.
