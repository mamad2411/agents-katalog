---
description: "Spring Boot README contract for required sections, actionable run/test docs, and no-filler project documentation."
globs: "README.md,**/README.md"
alwaysApply: false
---

# Spring Boot README Contract

These rules apply to the root `README.md` of an application repository. A
deployable app must ship one.
Do not restate pom, configuration, or API design contracts here—link to behavior
only when the README must tell a human how to run the app.

## Required structure

Every real application `README.md` includes these sections, in this order:

1. **Title** — project name as an H1.
2. **Purpose** — one short sentence stating what the application does.
3. **Overview** — a short bullet list (typically 3–7 items) of the main
   capabilities that exist in the code (not aspirational features).
4. **Prerequisites** — runtime and tools actually required (for example Java
   version, Maven, PostgreSQL, Docker when used).
5. **Configuration** — environment variables and important settings by name.
   Never commit real secrets; show placeholders or local-only examples clearly
   labeled as local development.
6. **Run** — commands for the `development` and `production` profiles (full
   profile names; never `dev`/`prod`).
7. **Access** — primary URLs (API base path, Actuator health, Swagger UI when
   the app exposes it).
8. **Tests** — how to run tests (`mvn test`) and any environment-dependent
   caveats. When k6 scripts exist, also document the `k6` CLI and `k6 run`
   (k6 contract).
9. **API summary** — brief endpoint list or pointer to OpenAPI/Swagger. Keep
   this short; do not paste a full OpenAPI document into the README.

Optional footer: **Created by** (or equivalent attribution).

## Writing rules

- Prefer concrete commands, paths, ports, and env var names over marketing
  prose.
- Document only features that exist in the repository.
- Keep the Overview factual; do not invent JPA, OAuth, or other stacks that the
  project does not use.
- Use the same profile and port conventions as the configuration contract.
- When SQL/DDL is DBA-owned, say so briefly instead of implying the app migrates
  the schema at startup (JDBC contract).

## Forbidden

- Never omit a root `README.md` from a real application repository.
- Never use short profile aliases (`dev`, `prod`) in run instructions.
- Never paste plaintext production secrets into the README.
- Never claim capabilities the codebase does not implement.
- Never replace the Tests section with “tests coming soon” for a shipped app.
- Never dump large generated OpenAPI JSON/YAML into the README.
