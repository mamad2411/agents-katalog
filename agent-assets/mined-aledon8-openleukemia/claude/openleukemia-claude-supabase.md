# Supabase Instructions

Supabase is the MVP platform layer for auth, Postgres, storage, Row Level Security, consent records, and lightweight Edge Functions.

## Rules

- Treat Row Level Security as a primary protection layer.
- Keep consent behavior explicit, auditable, and revocable.
- Prefer Supabase for routine product workflows and `ai-service/` for Python, ML, OCR, extraction, and compute-heavy work.
- Keep migrations and policies readable and reversible where practical.
- Do not weaken privacy, authorization, or consent checks without an explicit product reason.
- For schema or policy changes, plan affected data flows and access paths before editing.
