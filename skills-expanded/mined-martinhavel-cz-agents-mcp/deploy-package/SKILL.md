---
name: deploy-package
description: Build a cz-agents-mcp package locally, rsync changed source files to Hetzner, rebuild the Docker image, hot-swap the container, and verify health. Usage: /deploy-package <package-name> (e.g. realestate, dd, sanctions, ares, cnb, isir, adis)
disable-model-invocation: true
---

# deploy-package

Deploy a cz-agents-mcp package to Hetzner production.

## Steps

1. **Validate** — check the package name is one of: ares, cnb, sanctions, isir, adis, dd, realestate, shared
2. **Local build + test** — run `npm test --workspace=@czagents/<pkg>` then `npm run build --workspace=@czagents/<pkg>`
3. **Rsync src/** — sync `packages/<pkg>/src/` and `packages/<pkg>/package.json` to `/opt/docker/compose/cz-agents-mcp/packages/<pkg>/` on Hetzner (`martin@91.98.119.223`, key `~/.ssh/id_rsa_macbook`)
4. **Docker rebuild** — `docker compose build --no-cache <pkg>` in `/opt/docker/compose/cz-agents-mcp/`
5. **Hot-swap** — `docker compose up -d <pkg>` (zero-downtime replace)
6. **Health check** — `docker exec cz-agents-<pkg> wget -qO- http://localhost:<port>/health` and show result

## Port map
| package   | port |
|-----------|------|
| ares      | 3030 |
| cnb       | 3031 |
| sanctions | 3032 |
| dd        | 3033 |
| isir      | 3034 |
| adis      | 3035 |
| realestate| 3036 |

## Notes
- If `shared` is changed, rebuild ALL packages that depend on it (run full monorepo build)
- Never restart reality-webapp or cz-agents-webapp — those are separate compose projects
- If health check fails, immediately roll back: `docker compose up -d <pkg>` with previous image tag
