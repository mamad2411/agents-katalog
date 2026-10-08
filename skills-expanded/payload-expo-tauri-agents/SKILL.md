# AGENTS.md

This workspace contains two upstream codebases. You must follow their local guides when you touch files inside them.
- Payload: payload-main/CLAUDE.md
- Spacedrive: spacedrive-main/AGENTS.md

General rules for this workspace
- Use rg for search and keep changes scoped to the files you touch.
- Keep Payload config as the single source of truth for schema and admin behavior.
- Keep server only logic in Payload packages. Do not leak secrets or hooks to clients.
- Keep platform neutral logic in a shared package. Keep web and native UI in separate packages.

Platform best practices
- Web: avoid Next APIs in shared packages. Keep DOM use in web only modules.
- Tauri: use a Vite based web build and a thin native adapter for file dialogs and OS features.
- Mobile: use Expo and NativeWind. Do not use DOM specific APIs in React Native components.

Data and types
- Use payload generate:types as the type source.
- Use createClientConfig and the schema map builders as the admin schema source.
- Use @payloadcms/sdk for data access in client apps so API usage stays consistent.

Quality
- Add tests for schema generation and form state changes.
- Keep write ups short, direct, and focused on action.
