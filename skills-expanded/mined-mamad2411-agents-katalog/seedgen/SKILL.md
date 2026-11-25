---
name: seedgen
description: Analyze a repository's real data model (SQL migrations, Prisma, Django, SQLAlchemy, Mongoose, Solidity, etc.) and generate a runnable, schema-aware test-data seed script that respects enums, NOT NULL, unique and foreign-key constraints. Stack-agnostic — web2, web3, Python, or anything with a data model. Supports a locale/filter argument that localizes generated names, phones, addresses and currency. Use when the user wants seed data, test fixtures, sample records, or a database populated for development. Trigger phrases: "seed the database", "generate test data", "create fixtures", "/seed".
argument-hint: "[locale/filter] [count] e.g. indian 50 users, web3 only, us"
---

# seedgen

You are generating a **test-data seed script** for the current repository. Be surgical and concise — produce something that runs on the first try.

If the user supplied arguments (a locale, a count, a scope), treat them as the request/filters; otherwise use the defaults noted in step 3.

## 1. Analyze the repo (read, don't guess)

Detect the stack and locate every place data is defined. Check for, in order of what exists:

- **SQL / migrations**: `*.sql`, `migrations/`, `schema.sql`, Flyway/Liquibase.
- **ORM schemas**: Prisma (`schema.prisma`), Django (`models.py`), SQLAlchemy, TypeORM/Sequelize/Mongoose, Rails (`db/schema.rb`), Laravel migrations, GORM/Ent structs, Ecto.
- **Python**: dataclasses, Pydantic models, `models.py`.
- **Web3**: Solidity (`*.sol`), Hardhat/Foundry configs, ABI JSON, deploy scripts — data = on-chain seeding (mint, deploy, fund accounts, populate mappings).
- **APIs / types**: OpenAPI/GraphQL schemas, TypeScript interfaces, protobuf.
- **Config**: `.env.example`, `docker-compose.yml`, package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`) to learn the runtime, DB, and how existing scripts run.

Extract: entities/tables, field types, **enums**, **NOT NULL / required**, **unique** constraints, **foreign keys** and insertion order, and default values.

## 2. Pick the right output

Write the seed script in the **project's own language and idiom** so it drops in cleanly:

- Use the project's existing DB client / ORM / connection config (reuse `.env`, never hardcode secrets).
- Prefer the project's existing faker/factory lib if present; otherwise use a lightweight, well-known one for that ecosystem (`@faker-js/faker`, `faker`/`Faker`, etc.), and add it to the manifest.
- Respect FK order, satisfy every constraint, cover enums with a spread of values, and produce **referentially consistent** data (child rows point at real parents).
- Make it **idempotent** (safe to re-run: truncate/upsert or guard) and parameterized by count.
- Web3: emit a script for the project's toolchain (Hardhat/Foundry/ethers/web3.py) that deploys/uses contracts and seeds on-chain state against a local node.

## 3. Apply filters / locale

Parse the user's argument for a **locale** (e.g. `indian`, `us`, `uk`, `japanese`), **counts** (`50 users`), and **scope** (`web3 only`, `users and orders`). When a locale is given, localize generated names, emails, phone numbers, addresses, and currency so the data looks native to that region. Read the compact profiles in `references/locales.md` (in this skill's own directory — `${CLAUDE_PLUGIN_ROOT}/references/locales.md` on Claude Code, `${extensionPath}/references/locales.md` on Gemini CLI) and follow the matching one; if the locale isn't listed, infer sensible equivalents. Default to a neutral/`us` profile when none is specified.

## 4. Deliver

- Write the seed script to a conventional path (`seeds/`, `prisma/seed.ts`, `scripts/seed.py`, `db/seeds.rb`, `scripts/seed.js`, etc.).
- Add/adjust the run wiring (npm script, `manage.py` command, Makefile target, or a one-line command) and any new dependency.
- End with a short **"How to run"** block: the exact command, prerequisites (DB up, `.env` set, local chain running), and what gets created.

Keep the script readable and commented only where non-obvious. Do not invent tables or fields that aren't in the schema.
