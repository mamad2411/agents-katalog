---
license: CC-BY-4.0
description: >-
  Write and debug integration tests that run real dependencies (databases,
  brokers, cloud emulators, mock HTTP servers) in throwaway Docker containers
  with Testcontainers. Use when adding Testcontainers to a Java, Go, .NET,
  Node.js, Python, Rust, or other project; replacing H2/in-memory fakes or
  mocks with a real service; wiring Spring Boot, Quarkus, Micronaut or ASP.NET
  Core tests to a container; or when a Testcontainers test is flaky, cannot
  find Docker/Podman, times out waiting, or leaks containers. Also triggers on
  "testcontainers", "integration test with a real Postgres/Kafka/Redis",
  LocalStack, WireMock, MockServer, Ryuk, or Testcontainers Cloud/Desktop.
compatibility: >-
  Checked 2026-09-26 against testcontainers-java 2.0.5, testcontainers-go
  v0.44.0, testcontainers-dotnet 4.15.0, testcontainers-node v12.1.0,
  testcontainers-python 4.15.0, testcontainers-rs 0.28.0
  (testcontainers-modules 0.15.0). Requires a Docker-API-compatible runtime
  (Docker Engine/Desktop, Podman, Rancher Desktop, Colima, or Testcontainers Cloud).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Testcontainers — Integration Tests Against Real Services

Testcontainers is a family of per-language libraries that start Docker
containers from test code, wait until they are ready, hand back connection
details, and remove them afterwards. The concepts are shared; the APIs are not.

**Verify against the canonical docs when being wrong would mislead.** Every
language moves independently and several made breaking changes in 2025–2026
(see below). Check the language's docs/release notes in
[references/languages.rst](references/languages.rst) before pinning an API.

## Workflow

1. **Detect the language and test framework** from the build files
   (`pom.xml`/`build.gradle`, `go.mod`, `*.csproj`, `package.json`,
   `pyproject.toml`, `Cargo.toml`). Open the matching section of
   [references/languages.rst](references/languages.rst).
2. **Check the runtime** before writing code: `docker info` (or
   `podman info`). No reachable socket → fix the environment first
   (see *Runtime environment*), not the test.
3. **Prefer a module over a generic container.** Modules (`postgres`, `kafka`,
   `localstack`, …) ship correct wait strategies and connection helpers.
   Catalog: <https://testcontainers.com/modules/>.
4. **Pin the image tag** to the version production runs. Never `latest`.
5. **Choose the lifecycle** (per suite/class by default, see below) and write
   the test using the mapped host/port from the API.
6. **Pick a guide** from [references/guides.rst](references/guides.rst) when
   the user's stack matches one (Spring Boot, Quarkus, Micronaut, ASP.NET
   Core, LocalStack, WireMock, Kafka, jOOQ/Flyway) — but apply the version
   notes below, because most guides predate the current majors.

## Rules that hold in every language

- **Explicit image, pinned tag.** Node (v11+) and .NET (4.10+) removed default
  module images; the parameterless .NET builders are `[Obsolete]`. Java, Go,
  Python and Rust modules take the image as an argument too — always pass it.
- **Never hard-code `localhost` or the container port.** Ask the container
  for host and mapped port (`getHost()`/`getMappedPort()`,
  `Host(ctx)`/`MappedPort(ctx, …)`, `get_container_host_ip()`/
  `get_exposed_port()`, `get_host()`/`get_host_port_ipv4()`). The Docker host
  can be remote (`DOCKER_HOST`, Testcontainers Cloud, DinD in CI).
- **Container → container uses a shared network + alias + the internal port**,
  never the mapped port. Container → host-process uses the library's
  host-port exposure (`host.testcontainers.internal`).
- **Set a wait strategy for anything generic.** Defaults differ and changed:
  Go v0.38 dropped the implicit exposed-port readiness check; Node v12 now
  waits on the image `HEALTHCHECK` when present, else listening ports. A
  missing or wrong wait strategy is the #1 source of flaky tests.
- **Go modules do not always wait by default.** `postgres.Run(...)` needs
  `postgres.BasicWaitStrategies()` (it logs "ready" twice — it restarts once
  during init). Check each Go module's options for a wait helper.
- **Start once, reuse, isolate data.** Starting a container per test method is
  slow. Share one per class/suite/package (singleton or framework fixture),
  and isolate tests with transactions, truncation, or a schema/database per
  test. Parallel tests must not share mutable state in one container.
- **Leave Ryuk (the reaper sidecar) on.** It removes containers when the test
  process dies. Disable it only where it cannot run (rootless Podman, some
  locked-down CI) — then every container needs explicit cleanup.
- **Reusable containers are a local-dev speed-up only** (Java `withReuse(true)`
  plus `testcontainers.reuse.enable=true` in `~/.testcontainers.properties`;
  Node `.withReuse()`; Go `WithReuseByName`). Never rely on them in CI.

## Version traps (non-obvious, recent)

| Language | Trap |
|---|---|
| Java 2.x | Artifacts renamed `org.testcontainers:<m>` → `org.testcontainers:testcontainers-<m>` (e.g. `testcontainers-postgresql`, `testcontainers-junit-jupiter`). Classes moved to `org.testcontainers.<module>` and are non-generic (`org.testcontainers.postgresql.PostgreSQLContainer`, not `PostgreSQLContainer<?>`). JUnit 4 support removed. The old `org.testcontainers.containers.*` classes remain but are deprecated. |
| Java < 1.21.4 / 2.0.0–2.0.1 | Fails against Docker Engine 29+ ("client version … is too old"). Upgrade to ≥ 1.21.4 or ≥ 2.0.2. |
| Python 4.15 | Modules moved to `testcontainers.community.<module>`. `from testcontainers.postgres import PostgresContainer` still works but emits `DeprecationWarning` (fatal under `-W error`). The decorator `wait_container_is_ready` and `wait_for_logs` are deprecated in favour of `testcontainers.core.wait_strategies`. |
| Node v12 | Requires Node ≥ 22.22; default wait strategy changed (see above). v11 removed default module images. Modules are separate packages: `@testcontainers/<module>`. |
| .NET 4.10+ | Builders require the image: `new PostgreSqlBuilder("postgres:16-alpine")`. LocalStack module requires an auth token for LocalStack image ≥ 4.15 (since 4.12). |
| Rust | Add `testcontainers-modules` (it re-exports a version-aligned `testcontainers`); choose `SyncRunner` or `AsyncRunner` via its features. Don't add both crates at unaligned versions. |
| Guides | Most guides on testcontainers.com were written for Java 1.x, Node < 11, Python < 4.15 — translate coordinates/imports before copying. |

## Runtime environment

| Variable / file | Use |
|---|---|
| `DOCKER_HOST` | Non-default socket or remote daemon. |
| `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` | Socket path *inside* containers (Ryuk) when it differs from the host path, e.g. Podman machine on macOS → `/var/run/docker.sock`. |
| `TESTCONTAINERS_HOST_OVERRIDE` | Host name to reach mapped ports when auto-detection is wrong (DinD, remote daemon). |
| `TESTCONTAINERS_RYUK_DISABLED=true` | Rootless Podman / no privileged containers. |
| `~/.testcontainers.properties` | Per-user equivalents of the above (Java, Go, Node, .NET honour it; check others). |

- **Podman (RHEL/Fedora):** `systemctl --user enable --now podman.socket`,
  then `export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/podman/podman.sock`;
  rootless also needs `TESTCONTAINERS_RYUK_DISABLED=true`. Use fully-qualified
  image names (`docker.io/library/postgres:16`) if short-name resolution is
  set to prompt/enforcing.
- **CI:** GitHub-hosted Ubuntu runners have Docker; macOS and Windows runners
  do not run Linux containers. In DinD, set `TESTCONTAINERS_HOST_OVERRIDE`
  (or mount the host socket) so mapped ports are reachable.
- **Apple Silicon:** pin images that publish `linux/arm64`, or tests run
  under emulation (slow, sometimes crashing).

## Debugging checklist

1. `Could not find a valid Docker environment` / connection refused →
   runtime or `DOCKER_HOST` (above); on Java also check the Docker Engine 29
   trap.
2. Timeout waiting for container → print container logs (all libraries
   expose them; Python 4.15 includes them in the `TimeoutError`), then fix the
   wait strategy — log text, HTTP path, or healthcheck — not the timeout.
3. Works locally, fails in CI → host/port hard-coding, missing
   `TESTCONTAINERS_HOST_OVERRIDE` in DinD, or registry rate limits (use a
   mirror via image name substitution, e.g. Java/Go `hub.image.name.prefix`).
4. Leftover containers → Ryuk disabled or blocked; `docker ps -a --filter
   label=org.testcontainers=true`.

## References

- [references/languages.rst](references/languages.rst) — all 13 supported
  languages: docs, install coordinates, current release, idiomatic snippet
  and lifecycle hook for the main six.
- [references/guides.rst](references/guides.rst) — every official guide at
  <https://testcontainers.com/guides/>, by language and technology, with
  "use when" notes.
