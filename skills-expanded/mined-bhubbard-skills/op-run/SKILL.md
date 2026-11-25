---
name: op-run
description: Use 1Password CLI `op run` to pass environment variables securely to applications and scripts.
---
# 1Password CLI - `op run`

`op run` allows you to inject secrets as environment variables into a process without exposing them in your shell environment or saving them to disk.

## Usage
Create an `.env` file containing secret references instead of actual secrets:
```env
API_KEY=op://Vault/Item/Field
```
Then run your application using `op run`:
```bash
op run --env-file=".env" -- npm start
```

## Best Practices
- Do not export secrets globally in your shell (e.g. `export API_KEY=...`).
- Pass the `.env` file directly to `op run` with `--env-file`.
- `op run` ensures secrets only exist in the memory of the specific process.
