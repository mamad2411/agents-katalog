# Zolta HTTP Response — Cline Rules

- Always review the local README files (package root + Response README) when needed to refresh context.
- Follow the current architecture: **framework-agnostic core concepts** with **Laravel and Symfony adapters** using Zolta Forge.
- Keep Response code modular and aligned with the independent Response concept.
- Respect SOLID principles in all classes and services.
- This package is consumed by:
  - `apps/symphonyapp` (Symfony)
  - `apps/example-app` (Laravel test app)
  Both live under the monorepo `apps/` directory.
- When making changes, **update the README files** to reflect progress toward the official docs.
- Prefer clean contracts/ports and adapter boundaries; avoid leaking framework details into core logic.
- Do **not** delete or refactor the legacy `src/Core` and `src/Adapters` trees; treat them as reference/backup context.
- Any new or updated code should be compatible with **PHPStan level 6**.
- Do **not** run tests automatically (ask before running any test suite).
- Provide clear PHPDoc blocks and intent comments for any public or reusable helpers.