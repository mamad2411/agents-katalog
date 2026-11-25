---
name: testing-patterns
description: Testing standards and patterns across TypeScript (Vitest), Rust (cargo test), Swift (Swift Testing), and Go (go test). Covers file conventions, mock strategies, async testing, CI integration, and anti-patterns based on real project usage.
---

# Testing Patterns

## TypeScript / JavaScript Testing (Vitest)

### File Conventions
- **Colocated tests**: `src/foo.test.ts` next to `src/foo.ts` (primary pattern)
- **E2E tests**: `*.e2e.test.ts` in `test/` directory or colocated
- **Live tests**: `*.live.test.ts` for tests requiring real API keys
- **Setup file**: `test/setup.ts` for global beforeEach/afterEach hooks
- **Config layering**: base `vitest.config.ts` extended by `vitest.unit.config.ts`, `vitest.e2e.config.ts`, `vitest.live.config.ts`

### Test Structure
```typescript
import { describe, expect, it, vi } from "vitest";

describe("resolvePermission", () => {
  it("auto-approves safe tools without prompting", async () => {
    const prompt = vi.fn(async () => true);
    const res = await resolvePermission(makeRequest(), { prompt });
    expect(res).toEqual({ outcome: "allow" });
    expect(prompt).not.toHaveBeenCalled();
  });

  it("prompts for dangerous operations", async () => {
    const prompt = vi.fn(async () => true);
    await resolvePermission(makeDangerousRequest(), { prompt });
    expect(prompt).toHaveBeenCalledTimes(1);
    expect(prompt).toHaveBeenCalledWith("exec", "exec: rm -rf /");
  });
});
```

### Mock Patterns
```typescript
// Function mocks for dependency injection
const sendFn = vi.fn(async () => ({ messageId: "test" }));

// Module mocks (use sparingly -- prefer DI)
vi.mock("./network.js", () => ({
  fetch: vi.fn().mockResolvedValue({ ok: true }),
}));

// Spy on existing methods
const spy = vi.spyOn(store, "save");
expect(spy).toHaveBeenCalledWith(expectedData);

// Stub environment variables (auto-cleaned with unstubEnvs: true)
vi.stubEnv("API_KEY", "test-key-123");

// Fake timers (guard against leaks in afterEach)
vi.useFakeTimers();
vi.advanceTimersByTime(5000);
// Always restore: vi.useRealTimers()
```

### Test Setup Pattern (Global)
```typescript
// test/setup.ts
import { afterAll, afterEach, beforeEach, vi } from "vitest";
import { withIsolatedTestHome } from "./test-env.js";

process.env.VITEST = "true";
const testEnv = withIsolatedTestHome(); // Isolated HOME per worker
afterAll(() => testEnv.cleanup());

afterEach(() => {
  if (vi.isFakeTimers()) vi.useRealTimers(); // Prevent cross-test leaks
});
```

### Factory Functions for Test Data
```typescript
// Prefer factory functions over raw object literals
function makePermissionRequest(
  overrides: Partial<PermissionRequest> = {},
): PermissionRequest {
  const base: PermissionRequest = {
    sessionId: "session-1",
    toolCall: { toolCallId: "tool-1", title: "read: src/index.ts", status: "pending" },
    options: [{ kind: "allow_once", optionId: "allow" }],
  };
  return { ...base, ...overrides };
}
```

### Coverage Configuration
```typescript
// vitest.config.ts
coverage: {
  provider: "v8",
  reporter: ["text", "lcov"],
  all: false, // Only count files exercised by tests
  thresholds: { lines: 70, functions: 70, branches: 55, statements: 70 },
  include: ["./src/**/*.ts"],
  exclude: ["src/**/*.test.ts", "src/cli/**", "src/gateway/**"],
}
```

### Anti-Patterns
- Do NOT set `maxWorkers` above 16 (diminishing returns, flaky on CI)
- Do NOT test implementation details (internal state, private methods)
- Do NOT use `vi.mock` when dependency injection via function params works
- Do NOT leak fake timers across tests -- always restore in `afterEach`
- Do NOT skip edge cases: empty input, null, boundary values, error paths

---

## Rust Testing (cargo test)

### File Conventions
- **Inline unit tests**: `#[cfg(test)] mod tests` at the bottom of each source file (primary pattern)
- **Integration tests**: `tests/` directory at crate root (rare in workspace projects)
- **Test-only dependencies**: in `[dev-dependencies]` of each crate's `Cargo.toml`
- **Run all**: `cargo test --lib` | **Single crate**: `cargo test -p claudio-gateway --lib`
- **Filter by name**: `cargo test --lib test_name_substring`
- **Skip slow tests**: `cargo test --lib -- --skip concurrent`

### Unit Test Structure
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;

    #[test]
    fn insert_and_get() {
        let map = BoundedMap::new(10, Duration::from_secs(60));
        assert!(map.insert("a", 1));
        assert_eq!(map.get("a"), Some(1));
    }

    #[test]
    fn capacity_enforced() {
        let map = BoundedMap::new(3, Duration::from_secs(60));
        map.insert("a", 1);
        map.insert("b", 2);
        map.insert("c", 3);
        map.insert("d", 4); // should evict one
        assert!(map.len() <= 3);
    }

    #[test]
    fn ttl_expiry_on_get() {
        let map = BoundedMap::new(10, Duration::from_millis(1));
        map.insert("a", 1);
        std::thread::sleep(Duration::from_millis(5));
        assert_eq!(map.get("a"), None);
    }
}
```

### Async Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;

    #[tokio::test]
    async fn returns_immediately_when_no_tool_calls() {
        let provider = Arc::new(MockToolProvider::new(vec![final_response("Hello!")]));
        let mut executor = AgentExecutor::new(provider, "http://unused:9999", 10);

        let result = executor.execute(test_request()).await.unwrap();
        assert_eq!(result.iterations, 1);
        assert_eq!(result.tool_calls_made, 0);
    }

    #[tokio::test]
    async fn max_iterations_produces_final_response() {
        // Provider always returns tool calls -- should hit max iterations
        let provider = Arc::new(MockToolProvider::new(vec![tool_call_response()]));
        let mut executor = AgentExecutor::new(provider, "http://unused:9999", 3);
        let result = executor.execute(test_request()).await.unwrap();
        assert!(result.iterations <= 3);
    }
}
```

### Stub/Mock Providers (Trait-Based Mocking)
```rust
/// Stub: always returns a fixed response. No network calls.
pub struct StubProvider { provider_name: String }

#[async_trait]
impl Provider for StubProvider {
    fn name(&self) -> &str { &self.provider_name }
    async fn chat_completion(&self, req: &ChatCompletionRequest)
        -> Result<ChatCompletionResponse, ProviderError> {
        Ok(ChatCompletionResponse { /* canned fields */ })
    }
}

/// Scripted: returns pre-configured responses in sequence.
/// Useful for multi-turn agent loops.
pub struct ScriptedProvider {
    responses: std::sync::Mutex<Vec<ChatCompletionResponse>>,
}
```

### Testing Patterns for Workspace Projects
- Each crate has its own `#[cfg(test)]` modules (typical: 100+ test files in a workspace)
- Shared test utilities live in dedicated stub modules (e.g., `providers/src/stub.rs`)
- Use `Arc<dyn Trait>` for mock injection in async contexts
- Test crates independently: `cargo test -p crate-name --lib`

### Tauri Command Testing
```rust
// Minimal inline tests for Tauri commands
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_newer_detects_version_bump() {
        assert!(is_newer("1.0.1", "1.0.0"));
        assert!(!is_newer("1.0.0", "1.0.0"));
        assert!(!is_newer("0.9.9", "1.0.0"));
    }
}
```

---

## Swift / iOS Testing (Swift Testing)

### Framework: Swift Testing (not XCTest)
Projects use the modern `Testing` framework with `@Test` macros and `#expect` assertions.

### Test Structure
```swift
import Foundation
import Testing
@testable import YourApp

@Suite struct KeychainStoreTests {
    @Test func saveLoadUpdateDeleteRoundTrip() {
        let service = "com.example.tests.\(UUID().uuidString)"
        let account = "value"

        #expect(KeychainStore.delete(service: service, account: account))
        #expect(KeychainStore.loadString(service: service, account: account) == nil)
        #expect(KeychainStore.saveString("first", service: service, account: account))
        #expect(KeychainStore.loadString(service: service, account: account) == "first")
    }
}
```

### Serialized Suites (Shared State)
```swift
@Suite(.serialized) struct GatewayConnectionControllerTests {
    @Test @MainActor func resolvedDisplayNameSetsDefaultWhenMissing() {
        withUserDefaults([displayKey: nil, "node.instanceId": "ios-test"]) {
            let appModel = NodeAppModel()
            let controller = GatewayConnectionController(appModel: appModel, startDiscovery: false)
            let resolved = controller._test_resolvedDisplayName(defaults: .standard)
            #expect(!resolved.isEmpty)
        }
    }
}
```

### Async Test Methods
```swift
@Suite(.serialized) struct VoiceWakeManagerStateTests {
    @Test @MainActor func suspendAndResumeCycleUpdatesState() async {
        let manager = VoiceWakeManager()
        manager.isEnabled = true
        manager.isListening = true

        let suspended = manager.suspendForExternalAudioCapture()
        #expect(suspended == true)
        #expect(manager.isListening == false)

        manager.resumeAfterExternalAudioCapture(wasSuspended: true)
        try? await Task.sleep(nanoseconds: 900_000_000)
        #expect(manager.statusText.contains("Voice Wake") == true)
    }
}
```

### Testing @Observable ViewModels
- Instantiate the `@Observable` class directly in the test
- Use `@MainActor` annotation for UI-bound state
- For UserDefaults-dependent code, use a `withUserDefaults` helper that snapshots and restores

### Test Helper Pattern: Expose Internals
```swift
// In production code, expose test-only accessors:
func _test_resolvedDisplayName(defaults: UserDefaults) -> String { ... }
func _test_currentCaps() -> [String] { ... }
func _test_handleRecognitionCallback(transcript: String?, ...) { ... }
```

### Actor-Based Test Capture
```swift
actor CaptureBox {
    var value: String?
    func set(_ next: String) { self.value = next }
}

let capture = CaptureBox()
manager.configure { cmd in await capture.set(cmd) }
```

### Build & Test Commands
```bash
# Run tests on simulator
xcodebuild test -project App.xcodeproj -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro'

# Build only (catches compile errors)
xcodebuild -project App.xcodeproj -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build
```

---

## Go Testing (go test)

### File Conventions
- Test files: `*_test.go` in the same package as the code under test
- Same package access: tests use `package crypto` (not `package crypto_test`) for internal access
- Run: `go test ./...` | Single package: `go test ./internal/crypto/`

### Standard Test Pattern
```go
package crypto

import (
    "bytes"
    "testing"
)

func TestEncryptDecrypt(t *testing.T) {
    key := make([]byte, chacha20poly1305.KeySize)
    rand.Read(key)
    plaintext := []byte("Hello, World!")

    encrypted, err := Encrypt(plaintext, key, nil)
    if err != nil {
        t.Fatalf("Encrypt failed: %v", err)
    }

    decrypted, err := Decrypt(encrypted, key, nil)
    if err != nil {
        t.Fatalf("Decrypt failed: %v", err)
    }

    if !bytes.Equal(decrypted, plaintext) {
        t.Errorf("Decrypted text doesn't match.\nGot:  %q\nWant: %q", decrypted, plaintext)
    }
}
```

### Error Case Testing
```go
func TestEncryptInvalidKey(t *testing.T) {
    shortKey := make([]byte, 16)
    _, err := Encrypt([]byte("test"), shortKey, nil)
    if err == nil {
        t.Error("Encrypt should reject short key")
    }
}
```

### Integration Tests with Channels
```go
func TestHandshakeClientServer(t *testing.T) {
    serverResult := make(chan *HandshakeResult, 1)
    serverErr := make(chan error, 1)

    server := network.NewServer(handler)
    if err := server.Listen("127.0.0.1:0"); err != nil {
        t.Fatalf("Failed to listen: %v", err)
    }
    go server.Serve()
    defer server.Close()

    conn, err := network.Dial(server.Addr().String())
    if err != nil {
        t.Fatalf("Failed to dial: %v", err)
    }
    defer conn.Close()

    select {
    case err := <-serverErr:
        t.Fatalf("Server handshake failed: %v", err)
    case result := <-serverResult:
        if result.PeerID != "test-client" {
            t.Errorf("Server got peer ID = %q, want %q", result.PeerID, "test-client")
        }
    case <-time.After(2 * time.Second):
        t.Fatal("Server handshake timeout")
    }
}
```

### Uniqueness / Determinism Tests
```go
func TestGenerateKeyUniqueness(t *testing.T) {
    k1, _ := GenerateIdentityKey()
    k2, _ := GenerateIdentityKey()
    if bytes.Equal(k1.PublicKey, k2.PublicKey) {
        t.Error("Generated identical public keys (should be unique)")
    }
}

func TestFingerprintDeterministic(t *testing.T) {
    keypair, _ := GenerateIdentityKey()
    f1 := keypair.Fingerprint()
    f2 := keypair.Fingerprint()
    if f1 != f2 {
        t.Error("Fingerprint is not deterministic")
    }
}
```

### Race Detection
```bash
go test -race ./...   # Always run in CI
```

---

## Cross-Language Guidelines

### When to Write Tests
- **Always test**: boundary logic, parsing, serialization, crypto, state machines, error paths
- **Always test**: bug fixes (write the failing test first)
- **Skip testing**: trivial getters/setters, framework wiring, one-line delegation
- **Skip testing**: third-party library behavior (that is their job)

### Test Naming Conventions
| Language   | Convention                                    | Example                                    |
|------------|-----------------------------------------------|--------------------------------------------|
| TypeScript | `describe("module") > it("does X when Y")`   | `it("auto-approves safe tools")`           |
| Rust       | `snake_case` function names                   | `fn insert_and_get()`                      |
| Swift      | `camelCase` method names on `@Suite` struct    | `func saveLoadUpdateDeleteRoundTrip()`     |
| Go         | `TestXxx` with `PascalCase`                   | `func TestEncryptDecrypt(t *testing.T)`    |

### The Testing Pyramid
```
        /  E2E  \        *.e2e.test.ts, Docker scripts
       / Integration \   Server tests, handshake tests
      /    Unit Tests  \  #[test], @Test, TestXxx, it()
```
Ratio target: ~70% unit, ~20% integration, ~10% e2e.

### What NOT to Test
- Framework internals (Tauri IPC plumbing, axum routing wiring, SwiftUI view layout)
- Third-party API responses (mock them instead)
- Trivial wrappers that just delegate to another function
- Generated code (protocol buffers, codegen output)

### CI Integration (GitHub Actions)

**TypeScript (Vitest)**:
```yaml
- name: Test
  run: pnpm test
- name: Coverage
  run: pnpm test:coverage
```

**Rust (cargo test)**:
```yaml
- name: Test
  run: cargo test --lib
- name: Clippy
  run: cargo clippy -- -D warnings
```

**Swift (xcodebuild)**:
```yaml
- name: Test
  run: |
    xcodebuild test -project App.xcodeproj -scheme App \
      -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```

**Go (go test)**:
```yaml
- name: Test
  run: go test -race -cover ./...
```

---

## Quick Reference

| Language   | Framework       | Run Command                          | Config File             | Convention              |
|------------|-----------------|--------------------------------------|-------------------------|-------------------------|
| TypeScript | Vitest 4.x      | `pnpm test` / `vitest run`          | `vitest.config.ts`      | `*.test.ts` colocated   |
| Rust       | cargo test       | `cargo test --lib`                   | `Cargo.toml` (workspace)| `#[cfg(test)] mod tests`|
| Swift      | Swift Testing    | `xcodebuild test`                    | `.xcodeproj` scheme     | `*Tests.swift` in Tests/|
| Go         | go test          | `go test ./...`                      | None (built-in)         | `*_test.go` same pkg    |

### Mock Strategy Per Language
| Language   | Primary Mock Approach                        | Avoid                              |
|------------|----------------------------------------------|------------------------------------|
| TypeScript | `vi.fn()` + dependency injection via params  | Heavy `vi.mock()` of whole modules |
| Rust       | Trait-based stubs (`StubProvider`)            | `mockall` for simple cases         |
| Swift      | `_test_` accessor methods + actor captures   | Swizzling, runtime patching        |
| Go         | Interface-based injection + channels         | Monkey patching, `reflect`         |

## Property-Based Testing

Use when the function has invariants you can express as a rule (commutativity, round-trip, idempotency, monotonicity). One property test replaces dozens of example cases.

| Language   | Library     | Quick example |
|------------|-------------|---------------|
| TypeScript | `fast-check` | `fc.assert(fc.property(fc.string(), s => decode(encode(s)) === s))` |
| Rust       | `proptest`   | `proptest! { #[test] fn round_trip(s in any::<String>()) { prop_assert_eq!(decode(&encode(&s)), s); } }` |
| Swift      | `swift-testing` + manual generators | Loop with `Int.random(in:)` over `#expect` |
| Go         | `testing/quick` (stdlib) or `gopter` | `quick.Check(func(s string) bool { return decode(encode(s)) == s }, nil)` |

Sweet spots: parsers, codecs, serialization, math utilities, sort/merge logic. Skip for pure I/O wrappers.

## Coverage Targets

| Layer                  | Target  |
|------------------------|---------|
| Pure logic, parsers    | 90%+    |
| Service / handler code | 70-80%  |
| UI / view layer        | 40-60%  |
| Glue, framework wiring | not measured |

Coverage is a floor, not a goal. 100% line coverage with no assertions on outputs proves nothing.
