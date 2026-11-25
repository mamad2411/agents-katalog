# Supabase Functions Memory

Apply this inside `supabase/functions/`.

- Edge Functions are for lightweight orchestration close to Supabase data and storage.
- Keep heavy ML, OCR, document parsing, and model workflows in `ai-service/`.
- Validate inputs and preserve consent checks at server boundaries.
- Do not bypass RLS assumptions without documenting why.
