# agent-whiteboard Integration, Documentation, and Agent Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the complete product through real binary/HTTP/CLI/browser tests, document every supported contract and security boundary, publish the agent skill, and enforce reproducible cross-platform CI.

**Architecture:** Go process tests build and execute the actual binary against a unique `t.TempDir` root, use OS-assigned ports, and terminate real processes. Playwright launches the same binary and real CLI from JavaScript fixtures. Documentation is contract-driven, while the root skill teaches agents the safe CLI-first workflow without embedding server responsibilities in the skill.

**Tech Stack:** Go 1.25/1.26, standard `testing`/`os/exec`/`net/http`, Node.js 24.x, pnpm 11.4, Playwright 1.61.1 with pinned Chromium, GitHub Actions

## Global Constraints

- Complete the first three plans on the same feature branch before starting this plan.
- Full process and browser tests use no mocks and no external network service.
- Every test server gets a unique temporary storage root and temporary HOME; cleanup is registered immediately.
- Tests use `--port 0`, parse the actual listener address, and wait for `/readyz` rather than sleeping.
- A forced-kill cleanup fallback is always installed before a test starts interacting with a process.
- Public behavior is tested through the actual CLI and HTTP routes, not internal service calls.
- Browser assets remain fully bundled; tests fail if a public resource requests a CDN or another external origin.
- Documentation must describe public-but-non-indexed capability URLs and trusted same-origin HTML precisely.
- The skill never publishes secrets, opens a browser, or invents an edit token.

---

### Task 1: Build a hermetic real-process integration harness

**Files:**
- Create: `tests/integration/main_test.go`
- Create: `tests/integration/process_test.go`
- Create: `tests/integration/process_unix_test.go`

**Interfaces:**
- Produces a package-wide built binary and per-test server/CLI helpers; it does not import mocks.

- [ ] **Step 1: Write the failing harness smoke test**

```go
func TestProcessHealthAndShutdown(t *testing.T) {
    server := startServer(t)
    requireStatus(t, server.URL+"/healthz", http.StatusOK)
    requireStatus(t, server.URL+"/readyz", http.StatusOK)
    server.Signal(t, syscall.SIGTERM)
    require.NoError(t, server.Wait(t))
}
```

Run: `go test ./tests/integration -run TestProcessHealthAndShutdown -v`

Expected: FAIL because the process harness does not exist.

- [ ] **Step 2: Build the actual binary once per test package**

In `TestMain`, create a directory with `os.MkdirTemp`, run:

```text
go build -trimpath -o <temporary>/agent-whiteboard ../../cmd/agent-whiteboard
```

Set the resulting absolute path in package state, run tests, and remove the whole directory before returning the exit code. If build fails, print captured stdout/stderr and exit non-zero.

- [ ] **Step 3: Implement per-test server isolation and cleanup**

`startServer(t, extraArgs...)` must:

1. call `t.TempDir()` for storage and a separate `t.TempDir()` for HOME;
2. start the built binary with `serve --host 127.0.0.1 --port 0 --storage <root> --log-mode json`;
3. set HOME and no stateful user configuration;
4. capture stdout/stderr concurrently without scanner token limits;
5. immediately register `t.Cleanup` that sends SIGKILL if still running, waits, and closes pipes;
6. parse the JSON `server listening` log to obtain `url` and `address`;
7. poll `/readyz` with a bounded context and 20 ms backoff;
8. expose `RunCLI(ctx, args...)`, `Signal`, `Wait`, `Root`, and `URL`.

Use deadlines/polling; never use a fixed startup sleep. Serialize only the two signal tests if process-global behavior requires it; ordinary test servers may run independently.

- [ ] **Step 4: Verify both termination signals**

On macOS/Linux, run separate tests for `os.Interrupt` and `syscall.SIGTERM`. Assert readiness becomes unavailable, the process exits within the shutdown timeout, the exit status is zero, and logs contain no unexpected internal error. Keep Unix signal constants in `process_unix_test.go`.

- [ ] **Step 5: Verify and commit**

Run: `go test ./tests/integration -run 'TestProcessHealth|TestProcessSIG' -v -count=1`

Expected: PASS and test-created directories/processes are gone when the command exits.

```bash
git add tests/integration
git commit -m "test: add real process integration harness"
```

### Task 2: Cover whiteboard, image, expiration, limits, and timeout flows

**Files:**
- Create: `tests/integration/whiteboard_test.go`
- Create: `tests/integration/image_test.go`
- Create: `tests/integration/expiration_test.go`
- Create: `tests/integration/limits_test.go`
- Create: `tests/integration/timeout_test.go`

**Interfaces:**
- Exercises actual CLI subprocesses, real HTTP requests, and real filesystem persistence only.

- [ ] **Step 1: Write the Markdown lifecycle test**

Create a Markdown fixture inside `t.TempDir`, call the real CLI with `--server <url> --json create markdown <file>`, and assert schema version 1 plus a URL on `/whiteboards/markdown/{id}`. Fetch it and assert inline viewer assets, JSON-encoded exact source, non-index headers, and no external asset references. Update through the real CLI, verify the same URL exposes new source, delete, and assert both public GET and later update return the same 404 code.

- [ ] **Step 2: Write the standalone HTML lifecycle test**

Publish a complete HTML document containing inline CSS/JS. Assert public bytes are exactly identical and headers are non-indexing. Update/delete it. Submit separate fixtures with `script src`, stylesheet link, missing doctype, missing head, and invalid UTF-8; assert each fails without creating a directory under `<root>/whiteboards`.

- [ ] **Step 3: Write ordered image lifecycle tests**

Keep valid 1x1 PNG, JPEG, GIF, and WebP fixtures as literal base64 constants in `image_test.go`, then decode them into files under `t.TempDir()` for each test. Upload all four together. Assert ordered JSON results, generated filenames/extensions/media types, extensionless URLs, exact bytes, `nosniff`, `noimageindex`, and inline content disposition. Update the PNG ID with WebP, assert the public URL is unchanged and type/filename change, then delete all IDs.

- [ ] **Step 4: Prove validation atomicity and service rollback**

For the real binary, upload one valid image followed by invalid/SVG data and inspect the temporary `<root>/images` directory; assert no resource directory remains because all validation occurs before persistence.

For the persistence-failure branch that cannot be induced portably through a black-box disk, add a full-stack test in `tests/integration/image_test.go` that wraps the real `internal/store.FS.Images()` view in a deterministic fail-after-first-create decorator, injects it through `agentwb.Config.ImageStore`, starts the real application handler on a real TCP listener, submits a multi-image HTTP request, and inspects the real temporary root. The decorator delegates every operation to real filesystem storage and injects only one persistence error; it is hand-written fault injection, not a mock and has no expectations. Assert the first image directory is compensating-deleted and the HTTP response is the stable storage error.

- [ ] **Step 5: Test expiration with observable boundaries**

Start servers with explicit short defaults. Assert omitted creation expires, `--expires-in 0` stays permanent across the test, update without the flag preserves the original absolute expiration, update with a positive value moves it from update time, negative input is rejected, and an expired resource cannot be revived. Poll within bounded deadlines; do not assert at an exact timer tick.

- [ ] **Step 6: Test all size limits and client timeout**

Start a server with small explicit byte limits. Exercise one byte below/at/above each whiteboard, per-image, and total-image boundary through the real CLI. Assert 413 JSON errors and no persisted directories on rejected requests.

For timeout, start a dedicated `httptest.Server` that accepts but delays its response, execute the actual binary's client command with `--timeout 20ms`, and assert non-zero exit, stable timeout text/JSON, clean stdout separation, and server-side request-context cancellation.

- [ ] **Step 7: Run integration tests repeatedly**

```bash
go test ./tests/integration -v -count=1
go test ./tests/integration -run 'TestExpiration|TestLimits' -count=10
```

Expected: PASS without leaked processes or temporary data.

- [ ] **Step 8: Commit**

```bash
git add tests/integration
git commit -m "test: cover end-to-end resource workflows"
```

### Task 3: Add real-browser Playwright coverage

**Files:**
- Modify: `package.json`
- Modify: `pnpm-lock.yaml`
- Create: `playwright.config.js`
- Create: `tests/browser/fixture.js`
- Create: `tests/browser/whiteboard.spec.js`
- Create: `tests/browser/security.spec.js`

**Interfaces:**
- Launches the compiled production binary and real CLI, then verifies user-visible Markdown behavior in pinned Chromium.

- [ ] **Step 1: Pin Playwright and configure a network-hermetic project**

Add exact dev dependency `@playwright/test@1.61.1` and script `test:browser`. Configure one Chromium project, one worker by default, trace on first retry, and a 30-second test timeout. The fixture rejects every request whose origin differs from the local test server and records all requested URLs for assertions.

Run:

```bash
corepack pnpm install
corepack pnpm exec playwright install chromium
```

- [ ] **Step 2: Implement process fixtures with unconditional cleanup**

`fixture.js` creates a unique directory using `fs.promises.mkdtemp(path.join(os.tmpdir(), "agent-whiteboard-browser-"))`, builds the actual binary into it, starts `serve --port 0 --storage <temp>/storage --log-mode json`, waits on `/readyz`, and publishes through real CLI subprocesses. Register Playwright fixture teardown before yielding; in `finally`, send SIGTERM, wait with a deadline, SIGKILL on timeout, and `fs.promises.rm(root, {recursive:true, force:true})`.

- [ ] **Step 3: Write the failing rendering test**

Publish one Markdown document containing headings, table, blockquote, task list, highlighted Go code, safe/unsafe links, and two Mermaid fences. Open the returned CLI URL and assert:

- correct rendered structures and disabled task checkboxes;
- highlight.js classes exist;
- two sanitized Mermaid SVGs render;
- the first H1 is `document.title`;
- no raw Markdown source is exposed as visible text outside intended content;
- every requested URL is local and there are no CDN requests.

- [ ] **Step 4: Write theme, error-isolation, and sanitization tests**

Assert light/dark/system selection survives reload through `agent-whiteboard-theme`, system mode reacts to emulated color-scheme changes, and each theme change re-renders Mermaid. Publish one valid and one invalid diagram; assert the valid SVG remains and only the invalid placeholder displays an error.

Publish Markdown containing raw script/style HTML, event handlers, `javascript:` links, SVG payloads, and a `</script>` source sequence. Assert none executes or survives sanitization, while ordinary code text remains. Assert robots meta and response header values match.

- [ ] **Step 5: Run browser and asset tests**

```bash
corepack pnpm test
corepack pnpm run check:assets
corepack pnpm run test:browser
```

Expected: all tests PASS in pinned Chromium with no external requests.

- [ ] **Step 6: Commit**

```bash
git add package.json pnpm-lock.yaml playwright.config.js tests/browser
git commit -m "test: verify browser whiteboard rendering"
```

### Task 4: Write user, API, storage, security, and machine-output documentation

**Files:**
- Modify: `README.md`
- Create: `docs/http-api.md`
- Create: `docs/go-api.md`
- Create: `docs/storage.md`
- Create: `docs/security.md`
- Create: `docs/cli-json.md`
- Create: `docs/examples/diagram.md`
- Create: `docs/examples/standalone.html`

**Interfaces:**
- Documents the supported behavior implemented by the first three plans; examples are executable in integration checks.

- [ ] **Step 1: Write contract-checking tests before prose**

Create `tests/integration/docs_test.go` that reads fenced shell commands and example paths used by README smoke sections, verifies every documented CLI command appears in `agent-whiteboard --help`, verifies every HTTP route appears in `docs/http-api.md`, and publishes both example files through the real binary. The test need not execute installation commands.

Run: `go test ./tests/integration -run TestDocumentationContracts -v`

Expected: FAIL because the documentation is incomplete.

- [ ] **Step 2: Rewrite README as the product entry point**

Include purpose, install/build, five-minute local quick start, remote `--server`, Markdown/Mermaid, trusted standalone HTML, images, updates/deletes, expiration, defaults table, supported macOS/Linux and Go versions, public-but-non-indexed warning, development commands, and links to all detailed documents. Examples return URLs but never open them.

- [ ] **Step 3: Document HTTP and Go contracts exactly**

`docs/http-api.md` includes all routes, methods, multipart names, limits, path-only success schemas, nullable Unix expiration, error codes/statuses, public headers, and curl examples.

`docs/go-api.md` includes facade construction, DI/custom store examples, context rules, models, service methods, handler embedding, listener injection, lifecycle, idempotent close, and error inspection with `errors.As`.

- [ ] **Step 4: Document storage and security boundaries**

`docs/storage.md` includes both domain-owned interfaces, external implementation obligations, schema/layout, immutable generations, atomic metadata, expiration, granular keyed locks, cleanup, symlink/path safety, and the single-process-per-root assumption.

`docs/security.md` states that IDs are bearer capabilities; resources are public but non-indexed; non-indexing is not authorization; secrets/sensitive data must not be published; standalone HTML is trusted same-origin active content; the origin must have no auth cookies/sensitive state; SVG images are rejected; logs avoid bodies/full IDs.

- [ ] **Step 5: Document versioned CLI JSON**

`docs/cli-json.md` freezes `schema_version: 1`, single and multi success envelopes, nullable `expires_at`, permanent flag, stable error envelope, stdout/stderr separation, timeout output, exit codes 0/1/2/3/4, and compatibility expectations.

- [ ] **Step 6: Verify and commit**

Run:

```bash
go test ./tests/integration -run TestDocumentationContracts -v
rg -n --glob '!superpowers/**' 'TODO|TBD|localhost:[0-9]+/api/v1/.+generated-id' README.md docs
```

Expected: documentation test PASS; `rg` returns no placeholder markers or server-generated absolute-URL claims.

```bash
git add README.md docs tests/integration/docs_test.go
git commit -m "docs: publish usage and API contracts"
```

### Task 5: Add third-party notices and the agent skill

**Files:**
- Create: `internal/assets/licenses/THIRD_PARTY_NOTICES.txt`
- Modify: `internal/assets/assets.go`
- Modify: `internal/assets/assets_test.go`
- Create: `skills/agent-whiteboard/SKILL.md`
- Create: `skills/agent-whiteboard/references/cli.md`
- Create: `skills/agent-whiteboard/references/mermaid.md`
- Create: `skills/agent-whiteboard/references/security.md`
- Create: `tests/integration/skill_test.go`

**Interfaces:**
- Embeds exact browser dependency notices and gives agents a safe CLI-first publication workflow.

Before editing `skills/agent-whiteboard`, invoke the available skill-creation workflow and follow its validation requirements; the product requirements below still take precedence.

- [ ] **Step 1: Write failing notice and skill tests**

Assert the embedded notice contains names, exact versions, license identifiers, copyright notices, and upstream URLs for markdown-it, DOMPurify, Mermaid, and highlight.js. Assert `SKILL.md` has valid YAML frontmatter with `name: agent-whiteboard`, references only files that exist, contains every approved CLI command, and includes the mandatory security prohibitions.

- [ ] **Step 2: Generate and verify third-party notices**

Read each package's installed license file from `node_modules` and assemble one committed notice file with clear separators and exact version metadata. Do not copy minified source. Extend `assets.go` with `ThirdPartyNotices() []byte` and its mutation-isolation test.

- [ ] **Step 3: Write the concise root skill**

The root `SKILL.md` must teach this decision flow:

1. prefer CLI; use direct HTTP only when shell execution is unavailable;
2. choose Markdown for ordinary boards, standalone HTML only for trusted active documents, images for binary visuals;
3. publish images first when Markdown references them;
4. author Mermaid with ordinary fenced `mermaid` blocks;
5. use `--server`, `--json`, `--timeout`, and `--expires-in` deliberately;
6. return final public URLs without opening them;
7. update/delete using the capability ID;
8. never publish credentials, tokens, personal/sensitive data, or private source.

Keep detailed command matrices, Mermaid guidance, and the security model in the three reference files so the root skill stays scannable. State supported formats/limits, browser-side Markdown rendering, non-indexing limitations, same-origin HTML risk, and no separate edit token.

- [ ] **Step 4: Verify and commit**

Run:

```bash
go test ./internal/assets ./tests/integration -run 'TestThirdParty|TestAgentSkill' -v
rg -n 'open.*browser|secret|sensitive|noindex|mermaid|--timeout' skills/agent-whiteboard
```

Expected: tests PASS; inspection confirms the skill prohibits browser opening and publishing secrets while documenting non-indexing, Mermaid, and timeout usage.

```bash
git add internal/assets skills/agent-whiteboard tests/integration/skill_test.go
git commit -m "docs: add agent skill and dependency notices"
```

### Task 6: Add reproducible macOS/Linux CI

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Enforces supported Go toolchains, race behavior, generated artifacts, real-process tests, and pinned browser integration.

- [ ] **Step 1: Define the Go matrix**

Create jobs for Ubuntu and macOS with Go 1.25.x and 1.26.x. Use `actions/checkout@v6` with `persist-credentials: false` and `actions/setup-go@v6` with `cache-dependency-path: go.sum`, then run:

```bash
go mod download
go vet ./...
go test ./...
go test -race ./...
go build -trimpath ./cmd/agent-whiteboard
```

Set explicit job timeouts. Do not run process tests in parallel with another suite sharing a root; every test already creates its own root.

- [ ] **Step 2: Define the generated-assets/browser job**

On Ubuntu, use `actions/checkout@v6`, `actions/setup-go@v6` with Go 1.26.x, and `actions/setup-node@v6` with Node 24.x. Then run:

```bash
corepack enable
corepack prepare pnpm@11.4.0 --activate
pnpm install --frozen-lockfile
pnpm test
pnpm run check:assets
pnpm exec playwright install --with-deps chromium
pnpm run test:browser
git diff --exit-code
```

After activating pnpm, capture `pnpm store path --silent` as a step output and use `actions/cache@v5` for that path plus `~/.cache/ms-playwright`, keyed by the runner OS and `pnpm-lock.yaml` hash. No test may fetch a CDN at runtime.

- [ ] **Step 3: Verify workflow syntax locally**

Parse `.github/workflows/ci.yml` with a small Go YAML-free structural test in `tests/integration/ci_test.go`: assert required OS/Go strings and all required commands are present. Run `go test ./tests/integration -run TestCIContract -v`.

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ci.yml tests/integration/ci_test.go
git commit -m "ci: verify supported platforms and browsers"
```

### Task 7: Final acceptance and release-readiness checkpoint

**Files:**
- Modify only if acceptance reveals a defect.

**Interfaces:**
- Confirms implementation, generated output, docs, skill, and real integrations agree with the approved design.

- [ ] **Step 1: Verify no generator drift**

```bash
go run github.com/vektra/mockery/v3@v3.7.1
corepack pnpm install --frozen-lockfile
corepack pnpm run check:assets
git diff --exit-code
```

Expected: no changed generated mocks, lockfile, manifest, or bundles.

- [ ] **Step 2: Run all Go verification**

```bash
gofmt -w cmd internal pkg tests
git diff --exit-code
go vet ./...
go test ./... -count=1
go test -race ./... -count=1
go build -trimpath -o /tmp/agent-whiteboard-release ./cmd/agent-whiteboard
```

Expected: every command PASS and formatting makes no diff.

- [ ] **Step 3: Run all browser verification**

```bash
corepack pnpm test
corepack pnpm run test:browser
```

Expected: PASS with no external network requests.

- [ ] **Step 4: Perform contract audits**

```bash
rg -n --glob '!superpowers/**' 'TODO|TBD|FIXME|context\.Background\(\)|context\.TODO\(\)' cmd internal pkg tests skills README.md docs
rg -n 'http(s)?://.*(jsdelivr|unpkg|cdnjs)' internal/assets README.md docs skills
```

Expected: no placeholders, no request-path background contexts, and no CDN runtime references. Manually confirm the only intentional `context.Background()` uses are process roots, cleanup lifetime, and bounded graceful shutdown setup.

- [ ] **Step 5: Remove temporary binary and commit corrections**

Run: `rm -f /tmp/agent-whiteboard-release`

If acceptance required corrections:

```bash
git add -A
git commit -m "test: complete release acceptance"
```

Skip the commit only when the worktree is already clean. Confirm `git status --short` is empty before handoff.
