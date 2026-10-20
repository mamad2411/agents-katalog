# Frontend Source Memory

Apply this inside `frontend/src/`.

- Keep React components typed and simple; prefer local state until shared state is clearly needed.
- Use existing feature folders before creating new top-level source areas.
- Keep copy patient-safe: explanatory, calm, and never diagnostic.
- Preserve theme behavior via `document.documentElement.dataset.theme` and CSS variables.
- Tests live near app behavior in `src/app` or shared test setup in `src/test`.
