---
name: twelve-factor-app
description: Evaluate and apply the Twelve-Factor App methodology with modern 2025 interpretations. Covers all 12 factors with actionable checks for cloud-native applications running on containers, Kubernetes, and serverless platforms.
invoke_when: Use when designing a new service, evaluating cloud readiness, preparing for containerization, reviewing application architecture, or discussing deployment practices, configuration management, or service design principles.
---

# Twelve-Factor App (Modern 2025 Interpretation)

## Core Principle

The Twelve-Factor App methodology describes how to build software-as-a-service applications that are portable, scalable, and operationally mature. Originally written in 2011 by Heroku engineers, these principles remain foundational -- but the implementation details have evolved with containers, Kubernetes, and serverless.

---

## I. Codebase -- One Codebase, One App

**Principle:** One codebase tracked in version control, many deploys (staging, production, etc.).

**Modern interpretation:**
- One Git repository per deployable service (monorepo is acceptable if each service has clear boundaries and independent deployment).
- The same codebase is deployed to dev, staging, and production. Differences between environments come from configuration, not code branches.
- Feature flags control behavior differences, not separate codebases.

**Actionable checks:**
- [ ] Every service has exactly one repository (or one clear path in a monorepo).
- [ ] There is no "production branch" that diverges from main -- main is always deployable.
- [ ] Environment-specific behavior is controlled by config or feature flags, never by code branching.

---

## II. Dependencies -- Explicitly Declare and Isolate

**Principle:** Never rely on system-level packages. Declare all dependencies explicitly and isolate them.

**Modern interpretation:**
- Use lockfiles: `package-lock.json`, `poetry.lock`, `go.sum`, `Cargo.lock`.
- Container images pin base image versions: `FROM node:20.11.0-slim`, not `FROM node:latest`.
- Do not install tools globally in CI/CD -- declare them in the project.

**Actionable checks:**
- [ ] A lockfile exists and is committed to version control.
- [ ] Dockerfiles use pinned base image digests or exact version tags.
- [ ] `npm install` / `pip install` / `go build` works from a clean clone with no manual steps.
- [ ] No dependency is fetched from an unversioned URL or a curl pipe to shell.

---

## III. Config -- Store Config in the Environment

**Principle:** Configuration that varies between deploys (credentials, resource URLs, feature flags) is stored in environment variables, not in code.

**Modern interpretation:**
- Use environment variables or a secrets manager (AWS Secrets Manager, Vault, GCP Secret Manager).
- Never commit `.env` files with real credentials. Commit `.env.example` with dummy values.
- Use structured config loading that validates required variables at startup and fails fast if anything is missing.

```typescript
// Config loaded and validated at startup -- fail fast if misconfigured
const config = {
  databaseUrl: requireEnv('DATABASE_URL'),
  redisUrl: requireEnv('REDIS_URL'),
  apiKey: requireEnv('STRIPE_API_KEY'),
  logLevel: process.env.LOG_LEVEL ?? 'info',
  port: parseInt(process.env.PORT ?? '3000', 10),
};

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required env var: ${name}`);
  return value;
}
```

**Actionable checks:**
- [ ] No credentials, API keys, or connection strings appear in source code.
- [ ] The application fails fast at startup if required config is missing.
- [ ] `.env` files are in `.gitignore`.
- [ ] `.env.example` exists with all required variables documented.

---

## IV. Backing Services -- Treat Backing Services as Attached Resources

**Principle:** Databases, caches, message queues, and SMTP servers are attached resources, swappable via configuration without code changes.

**Modern interpretation:**
- Switching from a local Postgres to an RDS instance requires only changing `DATABASE_URL`.
- Switching from Redis to Memcached may require a code change (different API), but the connection is always configurable.
- Use connection pooling appropriate for the backing service.

**Actionable checks:**
- [ ] Every backing service is configured via a URL or connection string from the environment.
- [ ] No service hostname or port is hardcoded.
- [ ] The application can point to a different database/cache/queue instance by changing one environment variable.

---

## V. Build, Release, Run -- Strictly Separate Build and Run Stages

**Principle:** The build stage creates an artifact. The release stage combines the artifact with config. The run stage executes the release.

**Modern interpretation:**
- **Build:** Compile code, install dependencies, create a container image. Tag with Git SHA.
- **Release:** Apply environment-specific config (via Kubernetes ConfigMaps/Secrets, Helm values, or environment variables).
- **Run:** Start the container. The running process should not modify the release.

**Actionable checks:**
- [ ] Container images are built once and promoted across environments (same image in staging and production).
- [ ] Images are tagged with the Git SHA, not `latest`.
- [ ] No `npm install` or `pip install` happens at runtime.
- [ ] Release configuration is managed by the deployment system, not baked into the image.

---

## VI. Processes -- Execute the App as Stateless Processes

**Principle:** Processes are stateless and share-nothing. Any data that needs to persist is stored in a backing service.

**Modern interpretation:**
- No local file system storage for user data, sessions, or uploads. Use object storage (S3).
- No sticky sessions. Any request can be handled by any instance.
- In-memory caches are optimization only -- the app must work if the cache is cold.

**Actionable checks:**
- [ ] The application stores no user data on the local filesystem.
- [ ] Sessions are stored in Redis/database, not in-memory.
- [ ] The app works correctly when scaled to 2+ instances behind a load balancer.
- [ ] Restarting a process loses no user data.

---

## VII. Port Binding -- Export Services via Port Binding

**Principle:** The app is self-contained and binds to a port to serve requests. It does not depend on an external web server.

**Modern interpretation:**
- The application starts an HTTP server on `$PORT`.
- In Kubernetes, the container exposes a port and the Service/Ingress handles routing.
- Health check endpoints (`/healthz`, `/readyz`) are bound on the same port.

**Actionable checks:**
- [ ] The app listens on a configurable port (default 3000 or 8080, overridable by `$PORT`).
- [ ] No external web server (Apache, Nginx) is required inside the container to serve the app.
- [ ] Health check endpoints are available at `/healthz` (liveness) and `/readyz` (readiness).

---

## VIII. Concurrency -- Scale Out via the Process Model

**Principle:** Scale by running more instances of the application, not by making a single instance bigger.

**Modern interpretation:**
- Horizontal pod autoscaling in Kubernetes based on CPU, memory, or custom metrics.
- Separate process types for different workloads: web processes, worker processes, scheduled job processes.
- Use queue-based workers for background jobs, not threads within the web process.

**Actionable checks:**
- [ ] The app can run multiple replicas simultaneously without conflicts.
- [ ] Background work is handled by separate worker processes consuming from a queue.
- [ ] Autoscaling is configured based on relevant metrics (not just CPU).
- [ ] No singleton processes that become bottlenecks.

---

## IX. Disposability -- Maximize Robustness with Fast Startup and Graceful Shutdown

**Principle:** Processes start fast and shut down gracefully. They handle SIGTERM and drain in-flight requests.

**Modern interpretation:**
- Cold start time under 10 seconds. Under 2 seconds for serverless.
- On SIGTERM: stop accepting new requests, finish in-flight requests (with a timeout), close database connections, then exit.
- Kubernetes readiness probes stop routing traffic before shutdown begins.

```typescript
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, starting graceful shutdown');
  server.close();                      // Stop accepting new connections
  await drainInFlightRequests(30_000); // Wait up to 30s for in-flight requests
  await db.close();                    // Close database connections
  await cache.close();                 // Close cache connections
  process.exit(0);
});
```

**Actionable checks:**
- [ ] The app handles SIGTERM and shuts down gracefully.
- [ ] In-flight requests complete before the process exits.
- [ ] Startup time is under 10 seconds.
- [ ] Database connections and file handles are properly closed on shutdown.

---

## X. Dev/Prod Parity -- Keep Development, Staging, and Production as Similar as Possible

**Principle:** Minimize gaps between development and production: time gap, personnel gap, and tools gap.

**Modern interpretation:**
- Use Docker Compose or similar to run the same backing services locally (Postgres, Redis, Kafka) -- not SQLite in dev and Postgres in production.
- CI/CD pipelines deploy to staging automatically on merge. Production deploy follows within hours, not weeks.
- The same container image runs in all environments.

**Actionable checks:**
- [ ] Local development uses the same database engine as production.
- [ ] A `docker-compose.yml` exists that starts all backing services locally.
- [ ] Time from merge to production deploy is under 24 hours.
- [ ] No "works on my machine" issues caused by environment differences.

---

## XI. Logs -- Treat Logs as Event Streams

**Principle:** The app writes logs to stdout/stderr. The environment (container runtime, log aggregator) handles collection, routing, and storage.

**Modern interpretation:**
- Use structured JSON logging. Never log unstructured text in production.
- Do not write to log files inside the container. Write to stdout.
- Use a correlation ID (trace ID) on every log line so you can trace a request across services.

```typescript
// Structured JSON logging to stdout
const logger = {
  info: (message: string, context: Record<string, unknown> = {}) => {
    console.log(JSON.stringify({
      level: 'info',
      message,
      timestamp: new Date().toISOString(),
      traceId: getTraceId(),
      ...context,
    }));
  },
};

logger.info('Order created', { orderId: 'ord_123', customerId: 'cust_456' });
// Output: {"level":"info","message":"Order created","timestamp":"2025-...","traceId":"abc","orderId":"ord_123","customerId":"cust_456"}
```

**Actionable checks:**
- [ ] All logs are written to stdout/stderr, never to files.
- [ ] Logs are structured JSON with consistent fields (level, message, timestamp, traceId).
- [ ] No sensitive data (passwords, tokens, PII) appears in logs.
- [ ] A correlation/trace ID is included in every log entry.

---

## XII. Admin Processes -- Run Admin/Management Tasks as One-Off Processes

**Principle:** Database migrations, console sessions, and one-off scripts run as one-off processes in the same environment as the app, using the same codebase and config.

**Modern interpretation:**
- Database migrations run as Kubernetes Jobs or init containers, not as part of app startup.
- One-off scripts are invoked via `kubectl exec` or dedicated job runners, using the same container image.
- Never run migrations by SSHing into a production server.

**Actionable checks:**
- [ ] Database migrations run as a separate job, not during app boot.
- [ ] Admin scripts use the same container image and config as the running app.
- [ ] There is no SSH access required for routine operations.
- [ ] Migration history is tracked (e.g., Flyway, Alembic, Prisma Migrate).

---

## Quick Compliance Scorecard

| Factor | Key Question | Pass/Fail |
|---|---|---|
| I. Codebase | One repo, one app, deployed everywhere? | |
| II. Dependencies | Lockfile committed, images pinned? | |
| III. Config | All config from env vars, fail-fast on missing? | |
| IV. Backing Services | All services swappable via config? | |
| V. Build/Release/Run | Same image promoted across environments? | |
| VI. Processes | Stateless, no local storage? | |
| VII. Port Binding | Self-contained HTTP server on $PORT? | |
| VIII. Concurrency | Scales horizontally with no conflicts? | |
| IX. Disposability | Graceful shutdown, fast startup? | |
| X. Dev/Prod Parity | Same DB engine and services in dev and prod? | |
| XI. Logs | Structured JSON to stdout with trace IDs? | |
| XII. Admin Processes | Migrations as jobs, no SSH required? | |
