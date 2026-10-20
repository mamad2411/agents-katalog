# Docker-First Verification — MANDATORY FOR ALL AI AGENTS

## RULE ZERO — NON-NEGOTIABLE

**Before writing ANY code, running ANY task, or making ANY changes:**

1. Verify Docker Desktop is running
2. Verify ALL required containers are healthy
3. Verify connectivity to each service

**If Docker is not running, START IT FIRST. Do not proceed without live runtime.**

## Required containers

| Container | Purpose | Health check |
|-----------|---------|-------------|
| `local-vista-utf8` | VistA runtime (RPC broker port 9434) | `docker exec local-vista-utf8 bash -c "echo ok"` |
| `ve-platform-db` | Platform PostgreSQL (port 5433) | `docker exec ve-platform-db pg_isready -U cp_admin -d control_plane` |

## Startup commands

```powershell
# 1. Check Docker is running
docker ps --format "table {{.Names}}\t{{.Status}}"

# 2. If Docker Desktop is not running:
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
# Wait 45-60 seconds for initialization

# 3. Start VistA (from distro repo or existing container)
docker start local-vista-utf8
# OR from distro: docker compose -f docker/local-vista-utf8/docker-compose.yml up -d

# 4. Start Platform DB
docker compose -f apps/control-plane-api/docker-compose.yml up -d

# 5. Verify both are healthy
docker ps --format "table {{.Names}}\t{{.Status}}"
```

## Starting the tenant-admin server

**CRITICAL:** The `.env` file MUST be loaded explicitly. Node.js does not auto-load `.env` files.

```powershell
cd apps/tenant-admin
node --env-file=.env server.mjs
```

**NEVER** use bare `node server.mjs` — it won't load VISTA_ACCESS_CODE, VISTA_VERIFY_CODE, etc.
and all logins will silently fail with "Invalid access code or verify code".

## After writing ANY backend route or VistA-facing code

You MUST verify against the live system:

```powershell
# Login and get token
$body = '{"accessCode":"PRO1234","verifyCode":"PRO1234!!","tenantId":"default"}'
Set-Content -Path "$env:TEMP\login.json" -Value $body -Encoding ASCII -NoNewline
$resp = curl.exe -s -X POST http://127.0.0.1:4520/api/tenant-admin/v1/auth/login -H "Content-Type: application/json" -d "@$env:TEMP\login.json"
$token = ($resp | ConvertFrom-Json).token

# Test VistA routes
curl.exe -s -H "Authorization: Bearer $token" "http://127.0.0.1:4520/api/tenant-admin/v1/users?tenantId=default"

# For PG routes — verify the table exists and query works
docker exec ve-platform-db psql -U cp_admin -d control_plane -c "SELECT count(*) FROM tenants;"
```

## VistA container environment (UTF-8 lane)

The `local-vista-utf8` container uses the distro build. When running MUMPS commands
inside the container, you MUST set env vars directly — do NOT rely on `ydb_env_set`
which points to the wrong global directory.

```bash
# CORRECT way to run MUMPS inside the container:
export ydb_dist=/opt/yottadb/current
export ydb_gbldir=/opt/vista/g/vista.gld
export ydb_chset=UTF-8
export ydb_routines="/opt/vista/r $ydb_dist/plugin/o/utf8/_ydbposix.so $ydb_dist/utf8/libyottadbutil.so"
$ydb_dist/yottadb -run %XCMD 'W $D(^VA(200))'

# WRONG — ydb_env_set points ydb_gbldir to .yottadb subdir which has no VistA data:
source /opt/yottadb/current/ydb_env_set && mumps -run %XCMD 'W $D(^VA(200))'
```

This was solved previously and documented in the distro repo's entrypoint.sh (line 20-22)
and run-install.sh (lines 5-9). The entrypoint INTENTIONALLY bypasses ydb_env_set.

## NEVER ALLOWED

- Claiming code "works" without showing actual HTTP response from live runtime
- Marking a task "completed" without a live test against Docker
- Saying "verification deferred" or "should work" or "looks correct"
- Writing more than 1 route without testing the first one against live Docker
- Coding ANY VistA-facing feature without Docker running
- Coding ANY PG-backed feature without the database container running
- Skipping Docker startup because "it takes too long"

## What "done" means

1. Docker containers are running and healthy
2. The route/feature was tested against LIVE Docker
3. Real data was returned (not mocked, not stubbed, not assumed)
4. The response was captured and verified
5. Edge cases were tested (missing data, invalid input, auth denial)

## If Docker cannot start

If Docker Desktop fails to start or containers won't come up:

1. Report the exact error
2. Do NOT proceed with code changes
3. Fix the Docker issue first
4. Only then continue with the task

This rule has no exceptions. Every AI agent, every task, every time.
