# Agent Instructions

- Keep the project dependency-light unless a task clearly requires a package.
- Preserve the static app shape: `index.html`, `src/main.js`, `src/styles.css`, and `scripts/validate.mjs`.
- Do not commit credentials, `.env` files, private keys, service account JSON, Firebase mobile config files, or generated dependency folders.
- Prefer focused UI improvements that make the agent workspace more usable instead of turning the app into a marketing page.
- Run `npm run build` after changing app code or validation logic.
