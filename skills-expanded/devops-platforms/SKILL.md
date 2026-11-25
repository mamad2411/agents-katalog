---
name: devops-platforms
description: "Choosing and using a hosting platform: static and frontend hosts, container PaaS, self-hosted PaaS like Coolify, serverless functions and their limits, the big clouds' container services, managed databases, and what each costs in cold starts, regions, persistent disks, WebSockets and lock-in. Read before choosing where an app runs or configuring a platform."
---

# Hosting platforms

The generated choice is whatever the tutorial used: a WebSocket server on
serverless functions that cannot hold a socket, a queue worker on a free tier
that sleeps after fifteen minutes, the app in one continent and its database
in another, SQLite on a disk that vanishes on every deploy, Kubernetes for one
service run by one person, and an egress bill nobody expected. This is how to
match the app's shape (stateless or stateful, requests or long-running work,
one region or several) to a platform, and the settings each one needs. One
part of devops; the whole is in the `devops` skill.

## 1. Choosing

| The app | Default | Also good | Not |
|---|---|---|---|
| Static site, SPA, docs | Cloudflare (Workers static assets or Pages), Netlify, Vercel | Object storage behind a CDN | A server for static files |
| SSR framework (Next.js, Nuxt, SvelteKit) | Vercel for Next.js, Netlify, Cloudflare | A container on Fly, Render, Cloud Run, Coolify | |
| Stateless API or web app in a container | Cloud Run, Fly.io, Render, Railway | ECS Express Mode, Azure Container Apps, Coolify | |
| WebSockets, long streams, queue workers | Fly.io, Render, Railway, Coolify, ECS on Fargate | Cloudflare Durable Objects; Cloud Run within its 60-minute request limit | Serverless functions |
| A persistent disk (SQLite, files, an index) | Fly volume, Render disk, Railway volume, a VPS | Move the state to Postgres and object storage | Hosts with ephemeral disks |
| Spiky, event-driven glue | AWS Lambda, Cloudflare Workers, Vercel Functions | Cloud Run jobs | Idle always-on containers |
| Many services and teams, compliance | ECS on Fargate, managed Kubernetes (`devops-kubernetes`) | | A self-managed cluster |
| Small budget, several small apps | A VPS (Hetzner, OVH, DigitalOcean) with Coolify or Kamal | Dokku | Hand-built, unpatched servers |

Weigh, in order: the state the app keeps (disks, sockets, long jobs); where
its data lives (app and database in the same region: a cross-region query
costs 50 to 200ms and more, every time); traffic shape (steady, spiky, idle
most of the day); who patches and is on call; cost at rest and at ten times
the traffic, including egress and per-seat pricing; data residency and
compliance reports; and lock-in (a container, Postgres and the S3 API move in
a day, platform-specific stores and runtimes take a rewrite).

## 2. Frontend and function limits

- Build settings live in the repository (`vercel.json`, `netlify.toml`,
  `wrangler.jsonc`) with the Node version pinned, not only in a dashboard.
- Variables per environment (production, preview, development). Anything
  prefixed `NEXT_PUBLIC_` or `VITE_` is compiled into the bundle and public.
- Previews for every PR, protected (Vercel Deployment Protection, Cloudflare
  Access) when the app is not public.

| | Vercel Functions | Cloudflare Workers | AWS Lambda |
|---|---|---|---|
| Duration | 300s default; up to 800s on Pro and Enterprise | No wall limit while the client is connected; CPU 10ms on Free, 30s default and 5 min maximum on paid | 15 min |
| Memory | 2 GB (4 GB on Pro) | 128 MB per isolate | Up to 10,240 MB |
| Request body | 4.5 MB | 100 MB on Free and Pro zones | 6 MB synchronous (streamed responses up to 200 MB) |
| WebSockets | Public beta | Yes, through Durable Objects | Through API Gateway WebSocket APIs |
| Node APIs | Full Node | Partial, with the `nodejs_compat` flag | Full |

- Edge runtimes start in milliseconds near the user, but the database sits in
  one region, so edge code that queries it pays the round trip on every
  query. Default to the Node runtime in the database's region; keep edge for
  redirects, headers, auth checks and cached reads. Vercel runs functions in
  `iad1` unless told otherwise.
- Cold starts: close to none for Workers isolates, hundreds of milliseconds
  to seconds for Lambda with large bundles or a JVM (SnapStart helps). Keep
  bundles small, initialise lazily, and use provisioned concurrency or
  minimum instances where latency matters.
- Database connections: every instance opens its own, and a burst exhausts
  Postgres. Use a pooler or an HTTP driver: RDS Proxy, Cloudflare Hyperdrive,
  Supabase's pooler, Neon's pooled endpoint or serverless driver, PgBouncer
  in transaction mode (no session state).
- Workers are V8 isolates, not Node: KV is eventually consistent (a write can
  take a minute to show elsewhere), D1 is SQLite, R2 is S3-compatible with no
  egress fees, Durable Objects give single-threaded consistency and sockets.
- Long work moves to queues and jobs (`backend-jobs`), never a function held
  open.

## 3. Container platforms

```toml
# fly.toml
app = "acme-api"
primary_region = "sin"
kill_signal = "SIGTERM"
kill_timeout = 30

[deploy]
  release_command = "node dist/migrate.js"
  strategy = "rolling"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 1
  [http_service.concurrency]
    type = "requests"
    soft_limit = 200
    hard_limit = 250

[[http_service.checks]]
  grace_period = "10s"
  interval = "15s"
  method = "GET"
  path = "/healthz"
  timeout = "2s"

[[vm]]
  size = "shared-cpu-1x"
  memory = "512mb"
```

- Fly.io: the defaults are `kill_signal = "SIGINT"` and a 5s `kill_timeout`,
  hence the two lines above. `release_command` runs in a temporary Machine
  without volumes (5 minutes by default, `release_command_timeout`). A volume
  belongs to one Machine in one region, is not replicated, and keeps
  snapshots for 5 days by default; with volumes only rolling and immediate
  deploys work. `min_machines_running = 0` saves money and costs a cold start.
- Render (`render.yaml`): `runtime: docker`, `healthCheckPath`,
  `preDeployCommand` for migrations, `envVars` with `fromDatabase`,
  `generateValue: true` for generated secrets and `sync: false` for values
  entered in the dashboard. A disk disables zero-downtime deploys and
  scaling; the shutdown delay is 30s (`maxShutdownDelaySeconds`, up to 300).
  Free services sleep after 15 minutes idle.
- Railway (`railway.json`): Railpack builds by default, `healthcheckPath`,
  `preDeployCommand`, `overlapSeconds` and `drainingSeconds`; a service with
  a volume redeploys with a short gap rather than an overlap.
- Google Cloud Run: concurrency 80 per instance by default (up to 1000),
  request timeout 300s (up to 3600), 100 instances maximum by default, 10s
  after `SIGTERM`. With request-based billing the CPU is throttled outside
  requests, so work after the response stalls: use `--no-cpu-throttling` or
  a job. `--min-instances=1` removes cold starts;
  `--set-secrets=DATABASE_URL=database-url:latest` reads Secret Manager.
- AWS: App Runner stopped taking new customers on 30 April 2026; use ECS
  Express Mode (a Fargate service, load balancer and autoscaling from one
  call) or ECS on Fargate. Azure Container Apps scale on KEDA rules, to zero.

## 4. Self-hosted PaaS

- Coolify (4.3), Dokku, CapRover, Kamal: one server or a few, a proxy in
  front with automatic certificates (Traefik v3 by default in Coolify, Caddy
  optional), deploys on Git push or webhook. You patch the server, watch its
  disk and back it up.
- Coolify builds with Nixpacks, Railpack, a Dockerfile, a Compose file, an
  image or static files; previews come through its GitHub App; database
  backups go to S3-compatible storage on a schedule.
- Coolify's rolling update starts the new container, waits for its health
  check, then stops the old one: two copies run at once. A process that locks
  a volume, a SQLite file or a lock file fails in the new copy; switch on
  "Consistent container name" for that app (stop, then start). Rolling is
  also off with a published host port, a custom container name, Compose
  deployments and previews.
- Configure a health check on every Coolify app, or a broken build replaces
  a working one; its dashboard checks run `curl` or `wget` inside the
  container (`devops-containers`).
- Set memory and CPU limits per app: one leaking process otherwise pushes the
  host into swap and slows every app on it, and a restart that starts the new
  container first needs headroom for two.
- Keep "Make it publicly available" off for databases; reach them through an
  SSH tunnel or Tailscale. Back up `/data/coolify` and the volumes, not only
  the databases.
- Dokku is Heroku-like (`git push dokku main`, checks from `app.json`);
  CapRover runs on Docker Swarm; Kamal 2 deploys containers over SSH with
  kamal-proxy switching traffic, and `kamal rollback <version>`.
- The server: automatic security updates, a firewall with only 80, 443 and
  SSH (or SSH through Tailscale), disk alerts at 80%, Docker log rotation
  (`max-size` and `max-file`, or the `local` log driver; the default
  `json-file` never rotates), off-site backups (`devops-security`).

## 5. Big clouds

- AWS ECS on Fargate is the default container service there: task
  definitions, services behind an ALB, rolling deploys with the circuit
  breaker, no nodes to patch.
- EKS, GKE or AKS when the organisation already runs Kubernetes or needs its
  ecosystem; GKE Autopilot and EKS Auto Mode take node management away.
- Their quiet costs: NAT gateway data processing, traffic between zones, a
  load balancer per service, idle clusters, log ingestion.

## 6. Managed data

| Need | Defaults | Watch |
|---|---|---|
| Postgres | Neon, Supabase, RDS or Aurora, Cloud SQL, Fly Managed Postgres | Same region as the app, point-in-time recovery, connection limits, a pooler for serverless |
| Redis-compatible | Upstash (per request, HTTP API), managed Valkey (ElastiCache, Memorystore) | Eviction policy; not a primary store |
| Object storage | S3, Cloudflare R2, GCS, Backblaze B2, Hetzner Object Storage | Egress fees (none on R2), public access blocked by default, lifecycle rules |

- Supabase's direct connection is IPv6 only unless the IPv4 add-on is
  bought; from IPv4-only hosts (many PaaS and CI runners) use its shared
  pooler: session mode on 5432, transaction mode on 6543.
- Neon scales to zero, so the first query after idle waits for a cold start;
  its branches suit preview environments.
- Backups: automated daily with point-in-time recovery (7 days at least, 30
  for important data), a restore tested every quarter, and a periodic
  `pg_dump` kept with another provider.
- SQLite in production means one writer on a persistent volume, WAL mode and
  continuous backup (Litestream).

## 7. Cost and lock-in

- Scale to zero trades money for cold starts; minimum instances trade back.
- Egress: the big clouds charge per GB leaving (and crossing zones); a CDN in
  front and R2 for downloads cut it.
- Per-seat plans grow with the team, not the traffic; free tiers sleep or
  stop, and are not production.
- Keep business logic out of platform-specific APIs unless they earn it.
- Never invent a price: link the pricing page and state the assumptions
  (requests, GB, hours) behind any estimate.
- Domains and certificates on each platform: `devops-networking`.

## Check it

- The platform's config validates: `fly config validate`,
  `npx wrangler deploy --dry-run`, `vercel build`, `docker compose config -q`
  for Compose apps on Coolify.
- App and database are in the same region; one query's latency measured from
  the app, not guessed.
- The largest upload, longest request and any WebSocket or stream fit the
  limits table above.
- Health check configured; one deploy to staging watched from start to
  healthy; shutdown timing set (`kill_signal` and `kill_timeout` on Fly).
- A cost estimate written with its assumptions, or marked as not done.

## Avoid

WebSockets or long jobs on serverless functions; a database in a different
region from its app; SQLite or uploads on an ephemeral disk; Kubernetes for a
single small service; a free tier in production; Coolify apps with no health
check, no memory limit, or a volume lock under rolling updates; databases
published to the internet; Docker logs left to fill the disk; App Runner for
new AWS work; edge functions that query a one-region database on every
request; prices stated without a source.
