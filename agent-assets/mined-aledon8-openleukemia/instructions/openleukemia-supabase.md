---
applyTo: "supabase/**/*"
---

# Supabase Instructions

- Use Supabase for auth, CRUD, storage, consent records, RLS, and lightweight Edge Functions.
- Keep heavy ML, OCR, extraction, parsing, and model workflows in `ai-service`.
- Treat RLS as a primary protection layer.
- Pair sensitive tables with narrow, auditable policies.
- Plan affected data flows and access paths before schema or policy changes.
