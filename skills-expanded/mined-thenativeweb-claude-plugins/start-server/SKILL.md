---
name: start-server
description: Start or stop a local EventSourcingDB instance in development mode using Docker, with temporary data storage, plain HTTP, the built-in web UI, and a simple API token. Use when the user wants to spin up a throwaway EventSourcingDB for local development or testing, or wants to stop it again.
allowed-tools: Bash, Read, AskUserQuestion
---

# Start Server (Development Mode)

Run a local EventSourcingDB instance for development and testing via Docker. The instance uses:

- Temporary data storage (`--data-directory-temporary`) – all data is lost when the container stops.
- Plain HTTP instead of HTTPS (`--http-enabled --https-enabled=false`).
- The built-in web UI (`--with-ui`).
- A simple API token (`secret`).

This setup is for development only. Never use it in production.

## Defaults

- Container name: `eventsourcingdb-dev`
- Port: `3000`
- API token: `secret`
- Image: `thenativeweb/eventsourcingdb:latest`

If the user asks for a different port, token, or image version, use their values instead.

## Preflight

Check that Docker is running, and whether a dev instance already exists or the port is taken:

```bash
docker info > /dev/null 2>&1 && echo "Docker: running" || echo "Docker: NOT running"
docker ps --all --filter "name=eventsourcingdb-dev" --format "{{.Names}} ({{.Status}})"
lsof -nP -iTCP:3000 -sTCP:LISTEN || echo "Port 3000 is free"
```

- If Docker is not running, ask the user to start Docker first, then stop.
- If a container named `eventsourcingdb-dev` is already running, do not start a second one. Inform the user that the instance is already available and report the connection details (see below).
- If the port is taken by another process, use AskUserQuestion to ask the user for an alternative port.

## Start

```bash
docker run -d --rm --name eventsourcingdb-dev -p 3000:3000 \
  thenativeweb/eventsourcingdb:latest run \
  --api-token=secret \
  --data-directory-temporary \
  --http-enabled \
  --https-enabled=false \
  --with-ui
```

When using a custom port, only change the host side of the mapping (e.g., `-p 3001:3000`); the container-internal HTTP port stays `3000`.

## Verify

Wait briefly, then ping the instance:

```bash
sleep 2
curl -s -i "http://localhost:3000/api/v1/ping"
```

Check that the response contains HTTP status `200 OK` and the `Server` header starts with `EventSourcingDB/`. If the ping fails, inspect the logs with `docker logs eventsourcingdb-dev` and report the problem.

## Report to the User

After a successful start, report:

- API base URL: `http://localhost:3000`
- Web UI: `http://localhost:3000`
- API token: `secret`
- Data is stored in a temporary directory and is deleted when the container stops.

Suggest exporting the environment variables so the other esdb skills pick up the instance automatically:

```bash
export ESDB_URL="http://localhost:3000"
export ESDB_API_TOKEN="secret"
```

## Stop

When the user wants to stop the instance:

```bash
docker stop eventsourcingdb-dev
```

Since the container was started with `--rm` and `--data-directory-temporary`, the container and all stored data are removed. Remind the user of this before stopping.
