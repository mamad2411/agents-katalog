---
name: dwara-plugins
description: Extend the Dwara API gateway - develop and load proxy-wasm plugins (scaffold with dwara-cli plugin new, build for wasm32-wasip1, load via the plugins config block with fuel/memory/timeout limits, publish to a plugin registry), write native Rust filters, use the five extension traits (RateLimiter, ConfigSource, CacheStore, AnalyticsSink, SecretSource), and customize filter-chain order. Use for any task adding custom request/response behavior to Dwara or embedding it as a library.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Plugin development needs Rust with the wasm32-wasip1 target; registry installs need curl.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.2"
---

# Extending Dwara

Four extension surfaces, pick by need:

| Surface | Use when | Status | Cost |
| --- | --- | --- | --- |
| **proxy-wasm plugin** | Portable filters in Rust, hot-loadable, sandboxed (fuel/memory/timeout limits), community Kong/Envoy filters | Scaffolded: config + tooling + runtime exist; request-path dispatch not yet wired (the dataplane runs a no-wasm placeholder) | WASM overhead |
| **Native Rust filter** | Maximum performance, full dwara-core access, compiled in | Scaffolded: trait + registry exist; config-driven registration not wired | Rebuild the gateway |
| **Extension trait impl** | You're embedding dwara-core as a library and want to swap a subsystem (rate limiter, cache store, analytics sink, config source, secret source) | Live (library integration) | It's a Rust integration, not config |
| **nano-service** | Route handler AS a WASM module (route action, not a filter) | Live: compiled into every build, dispatched from the route action | Sandboxed compute per route |

First: check what the build actually accepts. The `plugins:` block and
`plugin_registry:` exist in the config schema of current builds - but
surface availability moves faster than docs, so always pre-flight with
`dwara-cli schema | grep -A5 plugins` and `dwara-cli validate` before
committing to a design.

## proxy-wasm in 60 seconds

```sh
dwara-cli plugin new my-plugin      # scaffolds Cargo.toml (cdylib + proxy-wasm
                                    # dep), src/lib.rs (4 callbacks stubbed),
                                    # dwara.yaml manifest, README
rustup target add wasm32-wasip1
cargo build --release --target wasm32-wasip1
# -> target/wasm32-wasip1/release/my_plugin.wasm
```

Declare it (config parses and validates today; request-path dispatch is
the remaining wiring - verify against your build before relying on it):

```yaml
plugins:
  - name: my-plugin
    wasm: ./target/wasm32-wasip1/release/my_plugin.wasm
    phases: [request_headers, request_body, response_headers, response_body]
    limits:
      fuel: 1000000        # execution fuel
      memory_mb: 32
      timeout_ms: 100
    config: ...            # raw bytes delivered via proxy_on_vm_start
# routes opt in with:  plugins: [my-plugin]
```

The lifecycle model: `Healthy` / `Crashed {error,
crash_count}` (routes referencing a crashed plugin fail **closed** with
500) / `Disabled {reason}`. Loads are checksum-verified (SHA-256),
exports-validated, hot-swappable by checksum. Plugin status is
observable via `GET /plugins` on the admin API and the `dwara-cli
status` plugins section. Plugins can also rewrite the request target
(`:path`/`:method`/`:authority`) and make HTTP callouts
(`proxy_http_call` with pause/resume, 5s cap, loop guard).

Full walkthrough + registry distribution:
[references/proxy-wasm.md](references/proxy-wasm.md).

## Native filters and extension traits

- **Native filter**: implement the `NativeFilter` trait (`FilterOutcome`:
  `Continue` / `LocalResponse` / `Error`), register at startup in the
  `NativeRegistry`, load via a plugin entry with `native: <registered-name>`
  (mutually exclusive with `wasm:`). Same `phases`/`config` fields.
  Like the wasm path, config-driven registration is scaffolded - the
  registry has no production registration from config yet.
- **Extension traits** (the seams enterprise backends also plug into):

| Trait | Hook point |
| --- | --- |
| `RateLimiter` | Rate-limit decisions per scope (traffic-policy stage) |
| `ConfigSource` | Where config generations come from (feeds the snapshot publish pipeline) |
| `CacheStore` | Response-cache get/set/invalidate (caching stage, post route-match) |
| `AnalyticsSink` | Receives the fire-and-forget record of every completed request |
| `SecretSource` | Resolves `${...}` references at config-build time, before publish |

Details: [references/native-filters-and-traits.md](references/native-filters-and-traits.md).

## Filter chain ordering (what runs before your plugin)

Built-in order (the `filter_chain.order` config validates as a permutation
of all eight stages and per-route overrides parse, but applying a custom
order on the live path is not wired - the dataplane runs this fixed order;
per-attachment `dry_run` flags are the live dry-run mechanism):

```
1 acl -> 2 rate_limit -> 3 authn -> 4 authz -> 5 validate -> 6 transform
      -> 7 cache -> 8 route
```

If you need
auth context in your plugin, note authn/authz run **before** route match -
your plugin executes within a request pipeline that already has a consumer
resolved (on `auth_required` routes).

## Decision guide

- Only need header/query surgery, canary tagging, custom denials?
  Check built-ins first: `transforms`, `authorization`, `waf`, policies -
  most "plugin ideas" are config.
- Need custom logic at the edge without rebuilding the gateway?
  proxy-wasm plugin (live on the request path: rewrites, short-circuits,
  HTTP callouts).
- Tight-loop performance or dwara-core types? Native filter (rebuild).
- Building a product on dwara-core? Extension traits.
- Whole route as sandboxed code? `action.type: nano_service`
  (`module: path.wasm`, `config:` JSON init payload; WASI languages;
  capabilities must be granted explicitly; metric
  `dwara_nano_service_total{route,outcome}`) - live in every build, no
  cargo feature.

## Gotchas

- wasm32-wasip1 target: plugins are **Rust** with the proxy-wasm ABI
  (other proxy-wasm-language plugins may load if ABI-compatible, but the
  scaffold and docs are Rust-first).
- Crashed plugins fail closed (500 on routes referencing them) - a plugin
  crash is an outage on those routes by design; gate rollouts with
  `Disabled`/config removal and watch crash_count.
- `fuel`/`memory_mb`/`timeout_ms` limits are real - infinite loops die at
  the fuel bound, not the request timeout.
- Registry installs are signature-optional but **digest-required**
  (SHA-256) - pin digests in config.
- eBPF hooks (dwara-ebpf crate) are a research spike - no traffic is
  steered through them; do not design around them.
