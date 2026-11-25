---
name: docker_deploy
description: Inspect repo, author Dockerfile/compose, long builds, run with a clear deploy report
triggers: [docker, compose, dockerfile, container, image, deploy, build image, docker compose, .dockerignore, staging, prod, контейнер, образ, деплой, разверни]
tools: [shell]
platform: all
---

## Docker / Compose (test or prod stack)

Default chain: **inspect project → artifacts → validate config → build (may take long) → detached run for daemons → report**.

Work inside the target project tree (relative paths, `cd` into the service directory). With **HOST SHELL MODE** you may use absolute paths to other project roots on this machine.

If the user asks for **apt / OS-level commands on a remote VPS**, use skill **vps_host_ssh** (`ssh -F /data/.ssh/config vps '...'`), not local compose unless they explicitly want local only.

Public URL, Traefik/Nginx/frp, and REG.RU DNS — skills **ops_reverse_proxy** and **ops_dns_regru** (inspect proxy on the VPS first, then config).

Do not read or paste `.env`, keys, or tokens into the user-facing reply.

### Steps

1. **Analyze:** language/runtime from `pyproject.toml`, `package.json`, `go.mod`, `requirements.txt`, existing `Dockerfile`; entrypoint (CMD), ports, env var **names** only (not secret values).
2. **Files:** minimal working `Dockerfile`, sensible `.dockerignore`, `docker-compose.yml` if needed (`build`, `ports`, `env_file:` without baking secrets into the image).
3. **Config:** `docker compose config` (or `docker-compose config`) — fix until clean.
4. **Build:** `docker compose build` — iterate from logs; **do not treat a long build as failure** until the command exits with an error.
5. **Run:** for APIs/web/daemons use **`docker compose up -d`** so the session does not block on foreground logs unless the user asks for attached logs.
6. **Verify:** `docker compose ps` or `docker ps --filter name=...`; on failure `docker compose logs --tail=80 <service>`.
7. **Report:** briefly what changed, service/container names, published ports, commands to verify and tail logs. State clearly e.g. “Deployed; check …”.

### Do not

- Put real secrets in `Dockerfile` or print `.env` contents.
- Suggest `rm -rf /`, chmod-the-world, or destructive actions outside the task.
