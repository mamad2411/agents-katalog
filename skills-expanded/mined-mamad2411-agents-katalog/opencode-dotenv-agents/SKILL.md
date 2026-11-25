# Agent Guide: opencode-dotenv

This document provides essential information for AI agents working on the opencode-dotenv project.

## Project Overview

OpenCode plugin that loads `.env` files at startup. This is a Bun runtime plugin that parses environment files and makes variables available to the OpenCode environment.

**Runtime**: Bun (required - not compatible with Node.js)
**Type**: OpenCode plugin
**Language**: TypeScript (ESM)

### Critical Architectural Limitation

This plugin **cannot** set environment variables for use in OpenCode's config file. OpenCode parses `opencode.jsonc` (including `{env:VAR}` resolution) **before** loading plugins. Therefore:

- Variables set by this plugin are available to chat sessions and tool executions
- Variables set by this plugin are **NOT** available to `{env:VAR}` references in `opencode.jsonc`
- For config variables (API keys, etc.), users must set them in shell profile before starting OpenCode

See `docs/ARCHITECTURE.md` for detailed startup sequence diagrams.

## Essential Commands

### Build & Install
```bash
# Install dependencies
bun install
# or
make install

# Build project (compiles src/index.ts to dist/)
bun run build
# or
make build

# Clean build artifacts and dependencies
make clean
```

### Testing
```bash
# Run tests
make test
# or
bun test

# Note: Uses bun:test framework
# Test files are located alongside source files (src/index.test.ts)
```

### Benchmarking
```bash
# Run performance benchmarks
make bench
# or
bun run bench/init.bench.ts
```

### Code Quality
```bash
# Lint code (placeholder - not configured)
make lint

# Format code (placeholder - not configured)
make fmt
```

### Publishing
```bash
# Build and publish to npm
npm publish
# or
make publish

# Dry-run publish to preview
make publish-dry
```

### Manual Testing (Bun-specific)
```bash
# Run with Bun directly
bun run src/index.ts
```

## Code Organization

```
opencode-dotenv/
├── src/
│   ├── index.ts              # Entry point, re-exports
│   ├── plugin.ts             # Main plugin implementation
│   ├── test-utils.ts         # Internal test utilities
│   └── profiler/
│       ├── index.ts          # Profiler exports
│       └── profiler.ts       # Performance profiler
├── bench/
│   ├── utils.ts              # Benchmark utilities
│   └── init.bench.ts         # Initialization benchmarks
├── docs/
│   └── ARCHITECTURE.md       # Plugin architecture and startup sequence
├── dist/                     # Built output (generated, not in git)
├── package.json
├── Makefile
└── README.md
```

**Key Points**:
- Main plugin entry at `src/index.ts`
- Profiler module at `src/profiler/` for performance tracking
- Benchmarks in `bench/` directory
- Tests co-located with source code
- Only `dist/` directory is published to npm (see `package.json` `files` field)
- Source files are excluded from npm package via `.npmignore`
- Architecture docs in `docs/` directory

## Naming Conventions & Style

### Constants
Upper case with underscores:
```typescript
const PLUGIN_NAME = "opencode-dotenv"
const CONFIG_NAME = "dotenv.jsonc"
const LOG_FILE = `${homedir()}/.local/share/opencode/dotenv.log`
const LOAD_GUARD = "__opencodeDotenvLoaded"
```

### Interfaces & Types
PascalCase:
```typescript
interface DotEnvConfig {
  files: string[]
  load_cwd_env?: boolean
  logging?: {
    enabled?: boolean
  }
}
```

### Functions
camelCase:
```typescript
function parseDotenv(content: unknown): Record<string, string>
function expandPath(path: string): string
async function loadConfig(): Promise<DotEnvConfig>
```

### Exports
- Named exports for utilities: `export { parseDotenv, globalProfiler }`
- Default export for main plugin: `export default DotEnvPlugin`
- Named export for plugin type: `export const DotEnvPlugin: Plugin`

### Import Style
Named imports from packages:
```typescript
import type { Plugin } from "@opencode-ai/plugin"
import { homedir } from "node:os"
import { parse } from "jsonc-parser"
import { globalProfiler } from "./profiler"
```

## Testing Approach

### Framework
- Uses `bun:test` (Bun's built-in test framework)
- Test files use `*.test.ts` naming pattern
- Tests located in same directory as source code

### Test Patterns
Comprehensive coverage including:
- Edge cases (empty lines, comments, mixed whitespace)
- Quote handling (single, double, unquoted values)
- Error handling (non-string content, type safety)
- Complex scenarios (multiple variables, special characters)

Example test structure:
```typescript
import { test, expect } from "bun:test"
import { parseDotenv } from "../src/index"

test("descriptive test name", () => {
  const result = parseDotenv("KEY=value")
  expect(result.KEY).toBe("value")
})
```

### Running Tests
```bash
make test
# or directly
bun test
```

## Key Code Patterns

### Async/Await Pattern
All file operations use async/await with Bun API:
```typescript
const file = Bun.file(configPath)
const content = await file.text()
```

### Non-Blocking Logging
Fire-and-forget async logging (never blocks):
```typescript
function log(message: string): void {
  if (!loggingEnabled || isTestEnv) return

  const timestamp = new Date().toISOString()
  const line = `[${timestamp}] ${message}\n`

  // Fire and forget - never block
  mkdir(LOG_DIR, { recursive: true })
    .then(() => appendFile(LOG_FILE, line))
    .catch(() => {
      // Ignore errors - never block
    })
}
```

### Configuration Loading
Multi-path search with first-match strategy:
1. Local config: `./dotenv.jsonc`
2. Global config: `~/.config/opencode/dotenv.jsonc`

First found file is used; no merging.

### Path Expansion
Tilde (`~`) expansion for home directory:
```typescript
function expandPath(path: string): string {
  return path.replace(/^~/, homedir())
}
```

### Load Guard Pattern
Prevents double plugin initialization:
```typescript
if ((globalThis as any)[LOAD_GUARD]) {
  return {}
}
(globalThis as any)[LOAD_GUARD] = true
```

### Profiler Integration
Performance tracking with the profiler module:
```typescript
import { globalProfiler } from "./profiler"

// Start timing
globalProfiler.initStart()

// Record file load metrics
globalProfiler.recordFileLoad(filePath, duration, varCount, success)

// Complete initialization
globalProfiler.initComplete("ready")

// Export performance report
const report = globalProfiler.export()
```

## Performance Optimizations

The plugin is optimized for fast startup (<1ms typical):

### Sequential Config Loading
- Config files are checked in order (local first, then global)
- First successful config is used; no merging
- Fast failure on missing/invalid configs

### Sequential File Loading
- .env files are loaded sequentially to maintain order
- Later files override earlier ones (important for variable precedence)
- Performance metrics recorded for each file

### Non-Blocking Logging
- Logging is **disabled by default** for maximum performance
- When enabled, uses async fire-and-forget writes
- Never blocks the main plugin execution
- Skipped entirely in test environments

### Load Guard
- Early return if plugin already loaded (`globalThis.__opencodeDotenvLoaded`)
- Prevents redundant initialization (subsequent calls: ~0.01ms)
- Essential for performance when plugin is called multiple times

### Profiler
- Built-in profiler for performance tracking
- Records config load times, file load times, and total initialization
- Can be exported for analysis via `getPerformanceReport()`

**To run benchmarks:**
```bash
make bench
```

## Important Gotchas

### Runtime Requirement
- **Must use Bun runtime** - this plugin uses Bun-specific APIs (`Bun.file()`)
- Not compatible with Node.js

### Configuration Format
- Uses JSONC format (JSON with Comments)
- Supports trailing commas and inline comments
- Parsed with `jsonc-parser` library
- **Config file name**: `dotenv.jsonc`

### Logging Behavior
- Defaults to **disabled** for performance
- Only enabled when explicitly set to `true` in config (`logging.enabled = true`)
- Uses async fire-and-forget writes (never blocks)
- Skipped in test environments (`NODE_ENV=test` or `BUN_TEST` set)
- Writes to `~/.local/share/opencode/dotenv.log`
- Silent failures in logging - won't crash if log file is unwritable

### Makefile Targets
The following targets are **stubs/placeholders**:
- `make lint` - only echoes "Linting code..."
- `make fmt` - only echoes "Formatting code..."

Functional targets:
- `make test` - runs `bun test`
- `make bench` - runs `bun run bench/init.bench.ts`

### Type Assertions
Code uses type assertions in some places:
```typescript
const config = parse(content, [], { allowTrailingComma: true }) as DotEnvConfig
(globalThis as any)[LOAD_GUARD] = true
```

### Config File Search Order
Config files are searched in this order; first found wins:
1. `./dotenv.jsonc` (project-specific)
2. `~/.config/opencode/dotenv.jsonc` (global)

No merging between config files.

### Environment Variable Load Order
Variables are loaded in this order; later values override earlier ones:
1. Files from `config.files` array (in specified order)
2. `.env` from current working directory (if `load_cwd_env !== false`)

### Process.cwd() Usage
The plugin uses `process.cwd()` to determine the current working directory, which is where OpenCode was launched from.

## Dependencies

### Production
- `jsonc-parser` - Parses JSONC configuration files with comments support

### Peer Dependencies
- `@opencode-ai/plugin` - OpenCode plugin type definitions

### Dev Dependencies
None specified (uses Bun's built-in test runner)

## Publishing

The package is published to npm with:
- Main entry: `./dist/index.js`
- Includes only: `dist/`, `README.md`, `LICENSE`
- Prepublish hook: automatically builds before publishing (`prepublishOnly: "bun run build"`)

## Development Workflow

1. Make changes to `src/index.ts`
2. Add/update tests in `src/index.test.ts`
3. Run `bun test` to verify
4. Run `make bench` to check performance
5. Run `make build` to compile
6. Test locally with Bun
7. Publish with `make publish`

## Debugging

View plugin activity logs:
```bash
tail -f ~/.local/share/opencode/dotenv.log
```

Logs include:
- Plugin startup/shutdown
- Config file loading
- File loading attempts
- Variable counts
- Errors (with details)

Get performance report programmatically:
```typescript
import { getPerformanceReport } from "opencode-dotenv"

const report = getPerformanceReport()
console.log(JSON.stringify(report, null, 2))
```
