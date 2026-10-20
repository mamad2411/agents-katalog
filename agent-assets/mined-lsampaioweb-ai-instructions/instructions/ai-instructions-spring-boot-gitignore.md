---
description: "Spring Boot .gitignore contract for build output, IDE files, logs, secrets, and certificate material."
applyTo: "**/.gitignore"
---

# Spring Boot Gitignore Contract

These rules apply to the root `.gitignore` of an application repository.
Infrastructure-only folders may add extra ignores for volumes and local data.

## Required baseline

Every real application repository ships a root `.gitignore` that ignores at least:

1. **Build output:** `target/` and `bin/` (Eclipse's default output folder;
   distinct from Maven `target/`)
2. **IDE / editor metadata:**
   - Eclipse/STS: `.apt_generated`, `.classpath`, `.factorypath`, `.project`,
     `.settings`, `.sts4-cache`
   - IntelliJ: `.idea/`, `*.iml`
   - VS Code / Cursor workspace junk: `.vscode/`
3. **Logs:** `*.log`, `*.gz`, and `logs/` when the application writes logs under
   that directory
4. **Local secrets:** `.env`, `.env.*` (allow committing a documented
   `.env.example` when the project uses one)
5. **TLS / key material:** `*.p12`, `*.pfx`, `*.jks`, `*.key`, `*.crt`, `*.pem`
6. **OS junk:** `.DS_Store`, `Thumbs.db`
7. **Maven release leftovers:** `release.properties`, `pom.xml.releaseBackup`

## Writing rules

- Keep one root `.gitignore` for the application module; do not scatter
  duplicate copies unless a nested module is a separate git root.
- Prefer explicit, reviewable patterns over copying an enormous unrelated
  template.
- If the repository intentionally commits public demo certificates, document
  that exception in the README and narrow the ignore pattern instead of
  committing private keys.
- Infrastructure compose projects may additionally ignore local volume data
  (for example `volumes/*`) without removing the application baseline.
- k6 HTML report directories are owned by the k6 contract. Add
  `src/test/k6/output/` when that project writes k6 reports.

## Forbidden

- Never omit a root `.gitignore` from a real application repository.
- Never commit `target/`, `bin/`, `.idea/`, `.vscode/`, or `.env` with secrets.
- Never commit private keys or keystores (`*.key`, `*.p12`, `*.pfx`, `*.jks`)
  for real apps.
- Never use `.gitignore` to hide failing tests or generated sources that should
  be built locally.
