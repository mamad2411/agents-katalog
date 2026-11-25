---
name: infra-frankenphp
description: Use when running PHP on FrankenPHP — worker mode, Caddy config, Docker images, hot reload, vs PHP-FPM+nginx.
metadata:
  added: 2026-05-23
  last_reviewed: 2026-05-23
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-23"
  related: [infra-nginx, infra-docker-images, php-symfony, security]
---

# Infra FrankenPHP

**Iron Law: in worker mode the kernel boots ONCE and serves thousands of requests in the same process — so any state that leaks between requests (mutable statics, accumulated EM identity map, request-scoped services held by long-lived ones) is a cross-request data-bleed bug. Reset the container/EM per request. Classic mode behaves like FPM; worker mode does NOT. Treating worker mode like FPM is THE failure.**

**Versions:** FrankenPHP `1.12.x` (1.12.1 bundles **PHP 8.5** + **Caddy 2.11.2**) · — _Built on Caddy, so you get automatic HTTPS, HTTP/2, and HTTP/3 for free. The binary embeds PHP — no separate `php` install, no FPM pool. Worker mode is the headline perf feature and the headline footgun._

## Classic mode vs worker mode

| Aspect       | Classic mode                      | Worker mode                                 |
| ------------ | --------------------------------- | ------------------------------------------- |
| Kernel boot  | Once **per request** (like FPM)   | **Once per worker**, reused across requests |
| Throughput   | Baseline                          | Multiples higher (no per-request bootstrap) |
| State safety | Clean slate each request          | **You** must reset state between requests   |
| Mental model | "PHP as you know it"              | Long-running app server (think Node/Go)     |
| When         | Legacy apps, scripts, low traffic | Symfony/Laravel hot paths, high throughput  |

Worker mode skips the autoloader warm-up, framework boot, and DI compilation on every request — that bootstrap is the bulk of a PHP request's CPU, so eliminating it is the big win. The cost: the process state persists, and you own its hygiene.

## Worker mode — the state-leakage hazard

```php
// public/worker.php — the worker loop (Symfony runtime generates this for you)
$kernel = new Kernel($_SERVER['APP_ENV'], (bool) $_SERVER['APP_DEBUG']);
$kernel->boot();                                  // ONCE — the expensive part, amortised

$handler = function () use ($kernel) {            // called per request
    $request  = Request::createFromGlobals();
    $response = $kernel->handle($request);
    $response->send();
    $kernel->terminate($request, $response);      // flushes, then RESET happens
};

$maxRequests = (int) ($_SERVER['MAX_REQUESTS'] ?? 1000);
for ($i = 0; $i < $maxRequests; $i++) {
    $keepRunning = \frankenphp_handle_request($handler);
    gc_collect_cycles();                          // reclaim per-request garbage
    if (!$keepRunning) break;                     // graceful: finish then exit, recycled by Caddy
}
```

The Symfony runtime resets the container between requests automatically (services tagged `kernel.reset` get `reset()` called). What it does NOT save you from:

- **Mutable `static` / global state** accumulated mid-request and never cleared — leaks into the next request in the same worker.
- **Doctrine EntityManager** — its identity map grows unboundedly and a closed EM stays closed. Inject `ManagerRegistry` and call `$registry->resetManager()` (or rely on the `doctrine.reset_manager` reset subscriber), never hold an `EntityManagerInterface` field in a long-lived service.
- **Request-scoped data captured by singletons** — a logger or service that cached `$request->getLocale()` at boot serves stale data forever.

`MAX_REQUESTS` caps requests per worker before recycling — a pragmatic guard against slow leaks while you hunt the real one. It is a mitigation, not a fix.

## Caddyfile — basics + automatic HTTPS

```caddyfile
# Caddyfile
{
    frankenphp {
        worker /app/public/worker.php   # enables worker mode for this entrypoint
    }
}

app.example.com {                       # named host → Caddy provisions a real cert via ACME
    root * /app/public
    encode zstd br gzip
    php_server                          # routes everything through FrankenPHP
}

:80 {                                   # local/dev — no cert, plain HTTP
    root * /app/public
    php_server
}
```

A bare domain name as the site address triggers Caddy's automatic HTTPS (ACME) — no cert paths, no renewal cron. `:80`/`localhost` stays plain for dev. `php_server` is the batteries-included directive (static files, `index.php` front controller, trailing-slash redirects).

## Docker — multi-stage, non-root

```dockerfile
FROM dunglas/frankenphp:1.12-php8.5 AS base   # also published as php/frankenphp
# install extensions with the bundled helper (compiles against the embedded PHP)
RUN install-php-extensions intl opcache pdo_pgsql redis

FROM base AS app
WORKDIR /app
COPY --chown=www-data:www-data . .
ENV FRANKENPHP_CONFIG="worker ./public/worker.php"   # turn on worker mode via env
ENV APP_ENV=prod
USER www-data                                  # never run the server as root
EXPOSE 443 443/udp 80                          # 443/udp = HTTP/3 (QUIC)
```

Pull `dunglas/frankenphp` — the canonical Docker Hub image (the project now lives at `github.com/php/frankenphp`). `install-php-extensions` builds against the embedded PHP — don't `apt install php-*`, there is no system PHP to extend. Run as `www-data`, not root. Expose `443/udp` or HTTP/3 silently won't work. Disable Caddy's admin API in production (`admin off` in the Caddyfile) — left on, anything that reaches `localhost:2019` can hot-swap your running config.

## Symfony runtime integration

Install `runtime/frankenphp-symfony`; the runtime auto-detects worker mode and generates the loop — you set the entrypoint with one env var:

```bash
FRANKENPHP_CONFIG="worker ./public/index.php"   # index.php IS the worker entrypoint
```

```jsonc
// composer.json — wire the runtime class
"extra": { "runtime": { "class": "Runtime\\FrankenPhpSymfony\\Runtime" } }
```

With the runtime in place, `public/index.php` doubles as the worker script — no separate `worker.php`. The runtime calls `$kernel->reset()` between requests for you; your job is making services genuinely resettable (`kernel.reset` tag or stateless design).

## 103 Early Hints

FrankenPHP can emit a `103 Early Hints` response so the browser starts fetching critical assets while PHP still works:

```php
use Symfony\Component\WebLink\Link;

$response->headers->set('Link', (new Link('preload', '/app.css'))->__toString());
// with symfony/web-link the kernel emits 103 before the final 200 under FrankenPHP
```

Pairs with `symfony/web-link`; measurable LCP win on asset-heavy pages. No FPM equivalent.

## Dev hot-reload

```bash
frankenphp run --watch                     # restart workers on source change
# or in env: FRANKENPHP_CONFIG="worker ./public/index.php\nwatch ./src"
```

`--watch` recycles workers when files change so you don't re-edit-restart by hand. Dev only — never ship `--watch` to prod (filesystem watching + restarts under load). In dev you may prefer classic mode entirely so every request re-reads code with zero reset reasoning.

## When to switch from PHP-FPM+nginx

Switch when bootstrap cost dominates (heavy Symfony/Laravel DI compilation per request) and you can guarantee request isolation. Stay on FPM+nginx when the app has deep mutable static state you can't audit, or when ops familiarity with the nginx+FPM split outweighs the throughput gain. FrankenPHP collapses two processes (nginx + php-fpm) into one — fewer moving parts, but the app code must earn the long-lived process.

## Worker count + graceful reload

- **Worker count**: start at `2 × CPU cores` and tune by latency/memory. Each worker holds a full booted kernel in RAM — too many workers OOM; too few queue requests. Set via `worker { num 8 }` in the Caddyfile block or `FRANKENPHP_NUM_WORKERS`.
- **Graceful reload**: `POST` to Caddy's admin API restart endpoint (or `caddy reload`) drains in-flight requests, then swaps workers — zero-downtime deploy. Don't `kill -9` the process; you drop connections and skip `terminate()`.

## Anti-patterns

- Shared mutable `static` / global state in worker mode — leaks across requests in the same worker; the canonical FrankenPHP bug.
- Holding `EntityManagerInterface` as a long-lived field — identity map grows, a closed EM never reopens. Inject `ManagerRegistry`, reset per request.
- Treating worker mode like FPM — assuming a clean slate each request. It is a long-running process; reason like Node/Go.
- Running the server as root in the container — drop to `www-data`.
- `apt install php-extension` — there is no system PHP; use `install-php-extensions`.
- Shipping `--watch` to production — filesystem watching + restart churn under load.
- Forgetting `443/udp` in `EXPOSE`/firewall — HTTP/3 silently disabled.
- Tuning workers blindly to a huge number — each is a full kernel in RAM; you OOM.

## Red flags

| Thought                                          | Reality                                                          |
| ------------------------------------------------ | ---------------------------------------------------------------- |
| "User B saw User A's data, randomly"             | Cross-request state leak in a worker — audit statics + the EM    |
| "Memory climbs until the pod restarts"           | EM identity map / unbounded static cache never reset per request |
| "Works in dev, breaks under load in prod"        | Dev ran classic mode; prod runs worker mode — different model    |
| "I installed a PHP extension and it's not found" | `apt` PHP ≠ embedded PHP; use `install-php-extensions`           |
| "Deploy drops live connections"                  | `kill`/restart instead of graceful Caddy reload                  |
| "HTTP/3 advertised but never used"               | `443/udp` not exposed / not open in the firewall                 |

## Hand-off

If you keep nginx in front of FrankenPHP (TLS offload, rate limiting, multi-app routing) or are weighing the nginx+FPM split it replaces: `Skill(devkit:infra-nginx)`. The Symfony side — making services `kernel.reset`-clean, the runtime component, Doctrine reset behaviour: `Skill(devkit:php-symfony)`. Building and slimming the container image (multi-stage layers, base image choice): `Skill(devkit:infra-docker-images)`. TLS posture, the non-root user, and exposing only what's needed: `Skill(devkit:security)`.
