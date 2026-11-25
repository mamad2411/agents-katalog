---
name: never-read-env
description: Never read .env files directly in code.
---

# Never read .env

Parsing `.env` from disk couples code to a file that does not exist in production (where secrets come from the runtime, a vault, or CI), so the code silently breaks once deployed — and a stray `fs.readFileSync('.env')` can ship the raw secret file into logs or bundles.

## Rules

- Read every secret and config value from `process.env` (e.g. `process.env.API_KEY`), never by opening, reading, or parsing a `.env` file in code.
- Let the runtime or a startup loader (`dotenv/config`, the platform) populate `process.env` — do not call `fs.readFileSync('.env')`, `fs.readFile`, or glob for `.env*` at runtime.
- This holds during development and testing and even when a user asks for it; there is no exception.

Enforce deterministically with a lint rule or pre-commit/CI grep that fails on `readFile`/`open` of a `.env` path — prose alone will not catch every case.

## Examples

```ts
// BAD — reading .env file directly in code
import fs from 'fs'
const env = fs.readFileSync('.env', 'utf8')
const apiKey = env.match(/API_KEY=(.+)/)?.[1]

// GOOD — read from environment variables (populated by the runtime or dotenv at startup)
const apiKey = process.env.API_KEY
```
