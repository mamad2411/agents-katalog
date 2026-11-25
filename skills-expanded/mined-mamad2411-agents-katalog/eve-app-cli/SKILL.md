---
name: eve-app-cli
description: Build agent-friendly CLIs for Eve-compatible apps. Wrap REST APIs with domain commands, auto-auth, structured errors, and --json output. Agents use CLIs instead of curl/fetch.
triggers:
  - app cli
  - build a cli
  - cli for agents
  - agent cli
  - app cli design
  - cli wrapper
  - rest api cli
  - reduce agent calls
  - agent api interaction
  - eden cli
  - app command line
  - cli pattern
  - agent-friendly api
  - domain cli
  - cli instead of curl
---

# Eve App CLI

Build domain-specific CLIs for Eve-compatible apps so agents interact via commands instead of raw REST calls.

## Why

Agents waste 3-5 LLM calls per REST interaction on URL construction, JSON quoting, auth headers, and error parsing. A CLI reduces this to 1 call:

```bash
# Before (3-5 calls, error-prone)
curl -X POST "$EVE_APP_API_URL_API/projects/$PID/changesets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EVE_JOB_TOKEN" \
  -d @/tmp/changeset.json

# After (1 call, self-documenting)
eden changeset create --project $PID --file /tmp/changeset.json
```

## Quick Start

### 1. Create the CLI Package

```
your-app/
  cli/
    src/
      index.ts          # Entry point
      client.ts         # API client (reads env vars)
      commands/
        projects.ts     # Domain commands
    bin/
      your-app          # Built artifact (single-file bundle)
    package.json
    tsconfig.json
```

### 2. Implement the API Client

```typescript
// cli/src/client.ts — Copy this, change SERVICE name
const SERVICE = 'API';

export function getApiUrl(): string {
  const url = process.env[`EVE_APP_API_URL_${SERVICE}`];
  if (!url) {
    console.error(`Error: EVE_APP_API_URL_${SERVICE} not set.`);
    console.error('Are you running inside an Eve job with with_apis: [api]?');
    process.exit(1);
  }
  return url;
}

export async function api<T = unknown>(
  method: string,
  path: string,
  body?: unknown,
): Promise<T> {
  const url = getApiUrl();
  const token = process.env.EVE_JOB_TOKEN;
  const res = await fetch(`${url}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({} as Record<string, string>));
    console.error(`${method} ${path} → ${res.status}: ${err.message || res.statusText}`);
    process.exit(1);
  }
  return res.json() as Promise<T>;
}
```

### 3. Define Commands

```typescript
// cli/src/index.ts
import { Command } from 'commander';
import { api } from './client.js';
import { readFile } from 'node:fs/promises';

const program = new Command();
program.name('myapp').description('My App CLI').version('1.0.0');

program.command('items')
  .command('list')
  .option('--json', 'JSON output')
  .action(async (opts) => {
    const items = await api('GET', '/items');
    if (opts.json) return console.log(JSON.stringify(items, null, 2));
    for (const i of items) console.log(`${i.id}  ${i.name}`);
  });

program.command('items')
  .command('create')
  .requiredOption('--file <path>', 'JSON file')
  .action(async (opts) => {
    const body = JSON.parse(await readFile(opts.file, 'utf8'));
    const result = await api('POST', '/items', body);
    console.log(`Created: ${result.id}`);
  });

program.parse();
```

### 4. Bundle for Zero-Dependency Distribution

Create a build script (`cli/build.mjs`):

```javascript
import { build } from 'esbuild';
import { readFile, writeFile, chmod } from 'node:fs/promises';

await build({
  entryPoints: ['cli/src/index.ts'],
  bundle: true,
  platform: 'node',
  target: 'node20',
  format: 'cjs',          // CJS — commander uses require() internally
  outfile: 'cli/bin/myapp',
});

// Prepend shebang (esbuild banner escapes the !)
const code = await readFile('cli/bin/myapp', 'utf8');
await writeFile('cli/bin/myapp', '#!/usr/bin/env node\n' + code);
await chmod('cli/bin/myapp', 0o755);
```

Add to `package.json`:
```json
{
  "scripts": {
    "build": "node build.mjs"
  }
}
```

**Important:** Do NOT set `"type": "module"` in `package.json` — it causes `require()` errors at runtime. Use `.mjs` extension for the build script instead.

### 5. Declare in Manifest

```yaml
# .eve/manifest.yaml
services:
  api:
    build:
      context: ./apps/api
    ports: [3000]
    x-eve:
      api_spec:
        type: openapi
      cli:
        name: myapp           # Binary name on $PATH
        bin: cli/bin/myapp     # Path relative to repo root
```

The platform automatically makes the CLI available to agents that have `with_apis: [api]`.

## Design Rules

### Command Structure

Map CLI commands to your domain, not HTTP endpoints:

```
# Good — domain vocabulary
eden map show
eden changeset create --file data.json
eden changeset accept CS-45

# Bad — HTTP vocabulary
eden get /projects/123/map
eden post /changesets --body data.json
```

### Output Contract

- **Default**: human-readable (tables, summaries)
- **`--json`**: machine-readable JSON on stdout
- **Errors**: stderr, exit code 1, actionable message

```bash
eden projects list              # Table: ID  NAME  CREATED
eden projects list --json       # [{"id":"...","name":"..."}]
eden changeset accept BAD-ID    # stderr: "Changeset BAD-ID not found"
```

### Auto-Detection Pattern

When only one resource exists, auto-detect instead of requiring flags:

```typescript
async function autoDetectProject(): Promise<string> {
  const projects = await api('GET', '/projects');
  if (projects.length === 1) return projects[0].id;
  if (projects.length === 0) {
    console.error('No projects found.');
    process.exit(1);
  }
  console.error('Multiple projects. Use --project <id>:');
  for (const p of projects) console.error(`  ${p.id}  ${p.name}`);
  process.exit(1);
}
```

### Progressive Help

Every command and subcommand has `--help`:

```
$ eden --help
Eden story map CLI

Commands:
  projects    Manage projects
  map         View story map
  changeset   Create and review changesets
  persona     Manage personas
  question    Manage questions
  search      Search the map
  export      Export project data

$ eden changeset --help
Commands:
  create   Create a changeset from JSON file
  accept   Accept a pending changeset
  reject   Reject a pending changeset
  list     List changesets for a project
```

## Environment Variables

The CLI reads these from the environment (injected automatically by Eve):

| Variable | Purpose | Set By |
|----------|---------|--------|
| `EVE_APP_API_URL_{SERVICE}` | Base URL of the app API | Platform (`--with-apis`) |
| `EVE_JOB_TOKEN` | Bearer auth token | Platform (per job) |
| `EVE_PROJECT_ID` | Eve platform project ID | Platform |
| `EVE_ORG_ID` | Eve platform org ID | Platform |

The CLI never requires manual configuration.

## Testing Locally

Set env vars and run directly:

```bash
export EVE_APP_API_URL_API=http://localhost:3000
export EVE_JOB_TOKEN=$(eve auth token)

# Test individual commands
./cli/bin/myapp projects list
./cli/bin/myapp items create --file test-data.json
```

## Bundling Details

Use esbuild to produce a single file with zero runtime dependencies:

- `--bundle` inlines all imports (including `commander`)
- `--platform=node` targets Node.js built-ins
- `--target=node20` matches Eve runner environment
- `--format=cjs` uses CommonJS (commander uses `require()` internally)
- Shebang prepended separately (esbuild `--banner` escapes `!` in `#!/usr/bin/env`)
- Result: 50-200KB single file, no `node_modules` needed at runtime

Commit `cli/bin/myapp` to the repo so it's available immediately after clone.

## Image-Based Distribution (Compiled CLIs)

For Go, Rust, or other compiled CLIs:

```yaml
services:
  api:
    x-eve:
      cli:
        name: myapp
        image: ghcr.io/org/myapp-cli:latest
```

Build a Docker image with the CLI binary at `/cli/bin/myapp`:

```dockerfile
FROM rust:1.77 AS build
COPY . .
RUN cargo build --release

FROM busybox:stable
COPY --from=build /app/target/release/myapp /cli/bin/myapp
```

The platform injects it via init container (same pattern as toolchains, ~2-5s latency).

## See Also

- `references/app-cli.md` in eve-read-eve-docs for the full technical reference
- `references/manifest.md` for manifest schema details
- `references/eve-sdk.md` for the Eve Auth SDK (server-side token verification)
