# e2e-requires-test

**This skill is a pipeline test — safe to delete after verification.**

Verifies that `requires:` block placeholder resolution works end-to-end
across all enrolled repos. Each repo should receive different resolved values
based on which files actually exist in its tree.

## Resolved values in this repo

- Env config: .env.example
- Docker: [your-docker]
- Next.js: [your-next-config]

## Expected behaviour

| Placeholder | Resolved if repo has... | Stays literal if... |
|-------------|------------------------|---------------------|
| `.env.example` | `.env.example`, `.env.template`, `.env.sample` | none of those exist |
| `[your-docker]` | `docker-compose.yml`, `Dockerfile` | no Docker files |
| `[your-next-config]` | `next.config.js/ts/mjs` | not a Next.js project |

Repos with all three resolved will show unique SHA vs repos with zero resolved.
