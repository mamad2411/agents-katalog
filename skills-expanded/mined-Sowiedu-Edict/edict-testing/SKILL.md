---
name: edict-testing
description: >
  How to write and run tests for the Edict compiler. Covers vitest conventions, test directory
  structure, patterns for testing each pipeline stage, structured error assertions, and coverage
  expectations. Use this skill when writing tests, fixing failing tests, adding coverage for new
  features, or understanding the test suite organization. Also use when asked about test patterns,
  how to test a specific compiler stage, or when investigating test failures.
---

# Edict Testing

Edict uses **vitest** for testing. The test suite covers all 6 pipeline stages plus MCP integration.

## Commands

```bash
npm test              # Run all tests (vitest run)
npm run test:watch    # Watch mode (vitest)
npm run test:coverage # Coverage report (vitest run --coverage)
```

## Directory Structure

```
tests/
├── validator/              # Phase 1: Schema validation
│   ├── valid-programs.test.ts    # Valid ASTs that should pass
│   ├── invalid-programs.test.ts  # Invalid ASTs that should fail with specific errors
│   ├── edge-cases.test.ts        # Boundary conditions
│   └── examples.test.ts          # All example programs validate
├── resolver/               # Phase 2a: Name resolution
│   ├── resolve.test.ts           # Core resolution tests
│   ├── coverage.test.ts          # Additional coverage
│   └── coverage-extended.test.ts # Extended edge cases
├── checker/                # Phase 2b: Type checking
│   ├── check.test.ts             # Core type checking tests
│   ├── coverage.test.ts          # Additional coverage
│   └── coverage-extended.test.ts # Extended edge cases
├── effects/                # Phase 3: Effect checking
│   ├── effect-check.test.ts      # Effect propagation and violation tests
│   └── call-graph.test.ts        # Call graph construction
├── contracts/              # Phase 4: Contract verification
│   ├── verify.test.ts            # Z3 contract verification
│   └── translate.test.ts         # Expression → Z3 translation
├── codegen/                # Phase 5: WASM code generation
│   ├── codegen.test.ts           # AST → WASM compilation
│   ├── runner.test.ts            # WASM execution
│   ├── e2e.test.ts               # End-to-end compile + run
│   └── string-table.test.ts      # String interning
├── errors/                 # Error system
│   └── fix-suggestions.test.ts   # Fix suggestion generation
├── mcp/                    # Phase 6: MCP server
│   ├── handlers.test.ts          # Tool handler tests
│   ├── agent-simulation.test.ts  # Simulated agent session
│   ├── http-transport.test.ts    # HTTP/SSE transport
│   └── version.test.ts           # Version tool
└── pipeline/               # Full pipeline
    └── check.test.ts             # End-to-end check pipeline
```

## Test Patterns

### Testing valid programs

```typescript
import { describe, it, expect } from "vitest";
import { validate } from "../../src/index.js";

describe("valid programs", () => {
  it("accepts a minimal module", () => {
    const ast = {
      kind: "module", id: "mod-test-001", name: "test",
      imports: [], definitions: []
    };
    const result = validate(ast);
    expect(result.ok).toBe(true);
  });
});
```

### Testing structured errors

```typescript
import { validate, type StructuredError } from "../../src/index.js";

it("rejects duplicate IDs", () => {
  const ast = { /* AST with duplicate IDs */ };
  const result = validate(ast);
  expect(result.ok).toBe(false);
  if (!result.ok) {
    const err = result.errors.find(e => e.error === "duplicate_id");
    expect(err).toBeDefined();
    expect(err!.nodeId).toBe("fn-dup-001");
  }
});
```

### Testing the type checker

```typescript
import { validate, resolve, typeCheck } from "../../src/index.js";

it("catches type mismatch", () => {
  const ast = { /* AST with type error */ };
  const vResult = validate(ast);
  expect(vResult.ok).toBe(true);
  if (!vResult.ok) return;

  const rResult = resolve(vResult.value);
  expect(rResult.ok).toBe(true);
  if (!rResult.ok) return;

  const tResult = typeCheck(rResult.value);
  expect(tResult.ok).toBe(false);
  expect(tResult.errors[0]?.error).toBe("type_mismatch");
});
```

### Testing contract verification (Z3)

```typescript
import { contractVerify, getZ3, resetZ3 } from "../../src/index.js";
import { afterAll } from "vitest";

afterAll(() => resetZ3()); // Clean up Z3 context

it("finds counterexample for failing contract", async () => {
  // ... set up AST with a failing postcondition
  const result = await contractVerify(module);
  expect(result.ok).toBe(false);
  const err = result.errors.find(e => e.error === "contract_failure");
  expect(err).toBeDefined();
  expect(err!.counterexample).toBeDefined();
});
```

### End-to-end compile and run

```typescript
import { compileAndRun } from "../../src/index.js";

it("runs hello world", async () => {
  const ast = { /* hello world AST */ };
  const result = await compileAndRun(ast);
  expect(result.ok).toBe(true);
  if (result.ok) {
    expect(result.output).toContain("Hello, World!");
    expect(result.exitCode).toBe(0);
  }
});
```

## Key Conventions

- **Always test both success and failure paths** — valid programs should pass, invalid should produce the exact expected error type
- **Test error content, not just error existence** — verify `nodeId`, `expected`, `actual`, `candidates`, etc.
- **Use the public API** — import from `../../src/index.js`, not internal modules
- **Clean up Z3** — call `resetZ3()` in `afterAll` when testing contracts
- **Test incrementally through the pipeline** — validate first, then resolve, then type check, etc.
- **Every new feature needs tests** — for EACH pipeline stage it touches

## Coverage

The project targets high coverage. Run `npm run test:coverage` and check the report in `coverage/`.
