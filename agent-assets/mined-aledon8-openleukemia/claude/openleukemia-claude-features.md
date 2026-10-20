# Frontend Features Memory

Apply this inside `frontend/src/features/`.

- Keep each feature self-contained with its component, local types, and feature-specific helpers.
- Prefer explicit props and domain names over generic UI abstractions.
- Patient-facing UI should explain data and choices without implying diagnosis or medical advice.
- When feature behavior changes, add or update the nearest Vitest coverage.
- For new feature work, map empty, loading, error, and edge states before implementation.
