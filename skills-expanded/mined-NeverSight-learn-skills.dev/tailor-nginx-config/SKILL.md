---
name: tailor-nginx-config
description: Design, generate, review, and troubleshoot production Nginx configurations that are tailored to the application runtime, deployment topology, and traffic behavior. Use when Codex needs to configure Nginx for FastAPI, Next.js, Django, Spring Boot, or another HTTP application; deploy on premises, on a VM, with Docker, Podman, Compose, or another container platform, on AWS EC2 with or without an ALB, or behind another trusted proxy; or support static and protected files, reverse proxying, API gateways, uploads, caching, load balancing, WebSockets, SSE, streaming responses, or gRPC. Also use for nginx.conf and conf.d reviews, TLS termination, forwarded-client-IP handling, rate limiting, security headers, performance tuning, syntax validation, and safe reload planning.
---

# Tailor Nginx Configuration

Produce the smallest complete Nginx configuration that fits the observed workload. Treat “optimal” as workload-specific: preserve correctness first, then security, operability, latency, throughput, and resource efficiency in that order unless the user states another priority.

## Adopt the requested posture

- For creation or change requests, inspect, implement, and validate the requested configuration.
- For review, diagnosis, or explanation requests, remain read-only unless the user also asks for a fix.
- Keep changes inside the requested Nginx scope. Do not refactor application or infrastructure files merely because an alternative architecture exists.
- Add an application setting, service definition, firewall rule, or load-balancer change only when the requested outcome requires it and the user has authorized that scope. Otherwise, report it as a required companion change.

## Build an evidence-based workload model

Inspect the repository and deployment artifacts before asking questions. Look for:

- application manifests and settings (`pyproject.toml`, `package.json`, `manage.py`, `settings.py`, `pom.xml`, `application.yml`);
- process commands, ports, Unix sockets, health endpoints, path prefixes, static roots, upload limits, and graceful-shutdown behavior;
- `Dockerfile`, `Containerfile`, Compose, Quadlet, systemd, cloud-init, Terraform, CDK, CloudFormation, Kubernetes, load-balancer, CDN, and DNS configuration;
- existing `nginx.conf`, `conf.d`, included snippets, image tags, compiled modules, certificate automation, and log conventions;
- routes using WebSocket, SSE, streaming SSR, gRPC, long polling, large request bodies, byte ranges, or protected downloads.

Resolve these decision inputs:

1. **Application:** runtime/framework, production server, upstream address, base path, static/media ownership, and framework proxy settings.
2. **Topology:** client-facing hops in order, Nginx placement, network reachability, service discovery, instance count, and health checks. For container deployments, identify the engine or platform, Compose implementation or orchestrator, rootless or rootful mode, and network mode.
3. **Protocol:** HTTP versions on each hop, TLS termination point, WebSocket/SSE/gRPC needs, and connection lifetime.
4. **Traffic:** request rate, concurrency, body and response sizes, latency budget, caching semantics, and abuse-sensitive routes.
5. **Trust:** accepted hostnames, trusted proxy CIDRs or security groups, authentication boundary, and which layer owns headers and rate limits.
6. **Packaging:** whether the target is a complete `nginx.conf`, a file under `conf.d`, a site file, an image template, or an ingress-specific resource.

If a missing value materially changes routing, trust, or TLS behavior, ask one concise question. When container deployment is known but the platform is not, ask which engine or platform runs it (for example, Docker Engine, Podman, or an orchestrator) before choosing DNS resolver addresses, host aliases, network names, bind-mount options, port-publishing behavior, or validation commands. Do not infer Docker merely from a Docker-compatible image or Compose file. If work can safely continue, state the assumption and use a clearly marked placeholder. Do not claim runtime validation while a required placeholder remains.

## Load only the relevant guidance

- Read [applications.md](references/applications.md) for FastAPI, Next.js, Django, Spring Boot, or generic upstream decisions.
- Read [deployments.md](references/deployments.md) for on-premises, VM, Docker, Podman, Compose, EC2, ALB, or Kubernetes topology.
- Read [services.md](references/services.md) for files, API gateways, uploads, caching, load balancing, WebSocket, SSE, streaming, and gRPC.
- Read [configuration-principles.md](references/configuration-principles.md) for directive contexts, the complete-`nginx.conf` baseline, proxy URI behavior, headers, TLS, limits, logging, and version compatibility.

Read every reference whose condition applies. Combine profiles; do not choose only one when, for example, a Next.js service on EC2 behind an ALB also streams responses.

## Design before writing

Make each of these choices explicit:

- Decide whether Nginx terminates TLS or receives already-terminated traffic.
- Define a default server that does not proxy unknown hosts.
- Choose exact, prefix, and regex locations deliberately; model the resulting URI for each `proxy_pass`, especially trailing slashes.
- Define trusted client-IP restoration only for known proxy addresses. Never trust all sources merely to obtain the apparent client IP.
- Decide buffering separately for ordinary responses, streaming responses, and request uploads.
- Preserve application cache semantics unless Nginx is intentionally made a cache owner with a correct cache key and bypass rules.
- Set body-size and timeout values from observed behavior rather than copying large global values.
- Rate-limit abuse-sensitive operations separately from ordinary traffic. Account for NAT, IPv6, authenticated identity availability, and upstream limits.
- Retry only when request semantics and failure behavior make replay safe. Do not enable non-idempotent retries by default.
- Assign each security header to exactly one layer. Treat CSP, CORS, HSTS, COOP, COEP, and framing policy as application/deployment decisions, not a universal paste-in block.
- Confirm that every referenced module and directive exists in the deployed Nginx build and version.

## Compose a self-consistent configuration

- Match the existing packaging. Do not put `events` or `http` inside a file already included from `http`.
- When the deliverable is a complete `nginx.conf`, start from the working baseline in [configuration-principles.md](references/configuration-principles.md): MIME-type includes, `sendfile` with `tcp_nopush`, `server_tokens off`, and conditional gzip. Minimalism removes unproven tuning, not the directives a working server needs.
- Put `map`, `upstream`, cache zones, log formats, and rate-limit zones only in valid contexts.
- Prefer explicit upstream names and stable service discovery. Bind host-local application servers to loopback or Unix sockets when appropriate; use container DNS names inside container networks.
- Forward the original host, scheme, client identity, and request ID only through a defined trust boundary. Clear or replace spoofable headers at the public edge; do not append an untrusted client-supplied forwarding chain.
- Include `proxy_http_version 1.1` when required for compatibility with deployed versions and upgraded connections, even if a newer Nginx release defaults differently.
- Preserve framework-generated `Cache-Control` for dynamic or revalidated content. Apply long immutable caching only to content-addressed assets.
- Use `alias` and `root` with correct slash semantics. Keep user uploads non-executable and outside application source paths.
- Use a `map` for WebSocket `Connection` handling when upgraded and ordinary HTTP share a server.
- Disable response buffering and caching only on streaming locations that need it; do not globally disable buffering without evidence.
- Use `grpc_pass` for native gRPC. Do not treat gRPC as an ordinary HTTP/1.1 proxy.
- Keep secrets, private keys, credentials, and environment-specific tokens out of generated configuration and logs.
- Explain non-obvious decisions with short comments. Do not annotate obvious syntax line by line.

Avoid stale cargo-cult settings:

- Do not emit `X-XSS-Protection: 1; mode=block`.
- Do not invent a generic CSP containing `'unsafe-inline'`.
- Do not add `includeSubDomains` or `preload` to HSTS without confirming the entire domain tree is HTTPS-ready.
- Do not override Next.js or application cache headers with extension-wide regex rules.
- Do not set `client_max_body_size`, long timeouts, worker counts, buffers, compression levels, or cipher lists to arbitrary “high performance” values.
- Do not hardcode an Nginx image version unless the repository or user owns that pin.

## Validate in the target environment

Validate proportionately to risk and use the exact binary or container image that will run the configuration.

1. Inspect `nginx -V` for the version, configure arguments, and required modules.
2. Run `nginx -t` with the actual prefix, includes, mounted certificates, DNS visibility, and environment. Use `nginx -T` when the merged configuration must be audited.
3. Validate the packaged container or VM unit, not just an isolated snippet. Ensure every included file and certificate path is mounted.
4. Exercise representative behavior: allowed and unknown hosts, HTTP-to-HTTPS flow, upstream health, redirects, path prefixes, missing files, cache headers, body-size boundaries, and client IP logs.
5. Exercise each special protocol end to end: a WebSocket upgrade, an SSE or streamed first chunk without buffering delay, a gRPC call, a byte-range request, or a protected download as applicable.
6. Test rate limits in dry-run mode or controlled traffic before enforcement when production thresholds are not already established.
7. Reload only when the user asked to apply the change. Prefer a graceful reload after syntax and behavior checks; keep a rollback copy or deployment revision.

If Nginx, certificates, DNS, upstreams, or the target network are unavailable, perform static checks and state that runtime and deployment behavior remain unverified.

## Deliver the result

Provide:

1. the observed application, topology, workload, and trust assumptions;
2. the exact file path and configuration, fitted to its include context;
3. any required companion application or infrastructure changes, clearly separated from changes actually made;
4. validation commands and observed results;
5. remaining placeholders, operational risks, and the safe reload or rollout action.

Prefer one production-ready configuration over a menu of unrelated examples. Offer variants only when a genuine unresolved architecture choice changes the correct result.
