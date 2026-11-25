---
name: vault-testing
description: |
  PARA fixture knowledge for Obsidian vault testing. Provides minimal test vault structure,
  frontmatter assertion patterns, fixture worktree lifecycle, and vault-specific test patterns.
  Use when writing tests that validate vault operations (inbox create, frontmatter parse,
  policy enforcement, dashboard render). Keywords: vault, testing, fixture, PARA, frontmatter.
triggers:
  - /e2e vault-testing
  - /vault-testing
  - vault test patterns
  - fixture worktree
  - PARA test structure
  - frontmatter assertions
negative_triggers:
  - visual testing (use e2e:e2e)
  - Cypress tests (use e2e:e2e)
  - plugin UI testing (use e2e:e2e)
  - performance testing
  - load testing
version: 1.4.0
author: Christian Kusmanow / Claude
last_updated: 2026-04-12
security:
  trust_model: Read-only vault analysis, fixture worktree creation in .worktrees/
  api_endpoints: []
  notes: Fixture worktrees are ephemeral and isolated. No production data access.
---

# Skill: Vault Testing

Provides knowledge and patterns for testing Obsidian vault operations in isolated fixture
worktrees. Covers PARA structure replication, frontmatter schema assertions, and vault-specific
test patterns that work inside Docker containers.

## Trigger

- `/e2e vault-testing` — Load vault testing context
- `/vault-testing` — Alias

---

## Minimal Test Vault Structure

A valid fixture worktree replicates only the PARA directories and files needed for the
specific test. Never copy the full vault.

### Skeleton (all tests need this)

```
fixture-root/
  00_Inbox/
  10_Goals/
  20_Projects/
  30_Areas/
  40_Resources/
  50_Collaborations/
  60_Science/
  70_Skills/
  80_Dashboards/
  90_Archive/
  coordination/
    policies/         # Symlink → real policies (read-only)
```

### Inbox Testing Skeleton

```
fixture-root/
  00_Inbox/
    P99-Test/                    # Project subdirectory (LR-INB-001)
      test-item.md               # Fixture inbox item
      test-item-lifecycle.md     # Generated lifecycle file
  20_Projects/
    vault-infra/
      P99-Test-Project.md        # Stub project
```

### Dashboard Testing Skeleton

```
fixture-root/
  80_Dashboards/
    Dashboard.md                 # Stub dashboard with Dataview queries
  00_Inbox/
    P99-Test/
      test-item.md               # Item for dashboard to render
  20_Projects/
    vault-infra/
      P99-Test-Project.md
```

---

## Frontmatter Assertion Patterns

### Pattern 1: Field Existence

Assert that required frontmatter fields exist after a vault operation.

```javascript
import { readFileSync } from 'fs';
import { parse as parseYaml } from 'yaml';

function parseFrontmatter(filePath) {
  const content = readFileSync(filePath, 'utf8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) throw new Error(`No frontmatter in ${filePath}`);
  return parseYaml(match[1]);
}

// Usage
const fm = parseFrontmatter('00_Inbox/P99-Test/test-item.md');
assert.strictEqual(fm.type, 'inbox');
assert.ok(fm.created, 'created field must exist');
assert.ok(fm.status, 'status field must exist');
```

### Pattern 2: Schema Conformance

Assert that frontmatter matches a complete schema (all required fields, correct types).

```javascript
const INBOX_SCHEMA = {
  required: ['type', 'status', 'project', 'priority', 'created'],
  types: {
    type: 'string',
    status: 'string',
    project: 'string',
    priority: 'string',
    execution_mode: 'string',
    tags: 'object',  // array
    created: 'string',
  },
  enums: {
    type: ['inbox'],
    status: ['active', 'completed', 'on-hold', 'cancelled'],
    priority: ['urgent-important', 'not-urgent-important', 'urgent-not-important', 'not-urgent-not-important'],
  }
};

function assertSchema(frontmatter, schema) {
  for (const field of schema.required) {
    assert.ok(frontmatter[field] !== undefined, `Missing required: ${field}`);
  }
  for (const [field, type] of Object.entries(schema.types)) {
    if (frontmatter[field] !== undefined) {
      assert.strictEqual(typeof frontmatter[field], type, `${field} type mismatch`);
    }
  }
  for (const [field, allowed] of Object.entries(schema.enums)) {
    if (frontmatter[field] !== undefined) {
      assert.ok(allowed.includes(frontmatter[field]), `${field} not in ${allowed}`);
    }
  }
}
```

### Pattern 3: Relationship Integrity

Assert that wikilinks and project references resolve to existing files.

```javascript
function assertRelationships(fixturePath, frontmatter) {
  // Project reference resolves
  if (frontmatter.project) {
    const projDir = join(fixturePath, '00_Inbox', frontmatter.project);
    assert.ok(existsSync(projDir) || existsSync(join(fixturePath, '20_Projects')),
      `Project directory ${frontmatter.project} must exist`);
  }

  // Goal link resolves
  if (frontmatter.goal) {
    const goalFiles = readdirSync(join(fixturePath, '10_Goals'));
    const goalExists = goalFiles.some(f => f.includes(frontmatter.goal));
    assert.ok(goalExists, `Goal ${frontmatter.goal} must exist in 10_Goals/`);
  }
}
```

---

## Test Environment Architecture (S233)

### Docker Compose: `docker-compose.test.yml`

The test environment uses a **standalone** compose file (`docker-compose.test.yml`) that is
fully independent from the production stack. No production vault dependency.

| Container | Port | Image | Isolation |
|-----------|------|-------|-----------|
| `postgres-test` | 5433 | postgres:16-alpine (tmpfs) | Ephemeral, separate from prod (5432) |
| `vault-drone-test` | 3837 | Custom (coordination/drone/) | Fixture VAULT_PATH |
| `vault-mcp-test` | 3938 | Custom (coordination/vault-mcp/) | Fixture VAULT_PATH, VAULT_STATE_DIR isolated |

### Key Mount Structure

```
.worktrees/e2e-fixture  ->  /vault          # Fixture PARA skeleton (not production vault)
.git/modules            ->  /.git/modules:ro # Submodule gitdir resolution (root level, not /vault/)
coordination/drone      ->  /vault/coordination/drone
coordination/vault-mcp  ->  /vault/coordination/vault-mcp
coordination/scripts    ->  /vault/coordination/scripts
coordination/policies   ->  /vault/coordination/policies
coordination/tests      ->  /vault/coordination/tests
```

**Why `.git/modules` mounts to `/.git/modules`:** Fixture worktree symlinks resolve to
absolute submodule paths outside `/vault/`. The container's git machinery follows these
symlinks, so `.git/modules` must be at the container root level.

### Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `FIXTURE_VAULT_PATH` | `.worktrees/e2e-fixture` | Fixture worktree path |
| `VAULT_STATE_DIR` | Isolated path | Prevents shared `embeddings.db` deadlock (SQLITE_BUSY) |
| `DRONE_PORT` | 3837 | Test drone port |
| `MCP_TEST_PORT` | 3938 | Test vault-mcp port |
| `PG_TEST_PORT` | 5433 | Test postgres port |

### Commands

| Command | Description |
|---------|-------------|
| `pnpm docker:test` | Start test containers |
| `pnpm docker:test:down` | Stop and remove test containers |
| `pnpm test:fixtures` | Run all fixtures against fixture worktree |
| `pnpm test:fixtures:ci` | CI mode with regression gating |

## Fixture Worktree

### Structure

The fixture worktree at `.worktrees/e2e-fixture/` is a minimal PARA skeleton:

| Property | Value |
|----------|-------|
| Branch | `e2e-fixture` (orphan) |
| Path | `.worktrees/e2e-fixture/` |
| Content | 11 PARA dirs (`00_Inbox` through `90_Archive`) |
| Seed files | ~5 markdown files (minimal content) |
| Submodule symlinks | `coordination/drone`, `vault-mcp`, `scripts`, `policies`, `tests`, hooks, plugins |
| Environment | `.env.test` (FIXTURE_VAULT_PATH, postgres-test DSN, VAULT_STATE_DIR) |

The fixture worktree is gitignored (`.worktrees/`). It is created by `run-fixtures.js`
if not present, or can be scaffolded manually.

### Fixture Runner Batch Execution Model

The fixture runner (`coordination/tests/run-fixtures.js`) executes fixtures sequentially
with cross-fixture Jest batching for performance:

1. **Scan** — discover all `*.fixture.md` files in `coordination/tests/fixtures/`
2. **Parse** — extract frontmatter, resolve source test files
3. **Dependency check** — skip fixtures whose service dependencies are unavailable
4. **Batch** — group consecutive same-runtime fixtures into single process invocations
5. **Execute** — `spawnAndWait()` with no timeout (hangs are bugs, not timeouts)
6. **Report** — write `baseline-report.json` with per-fixture pass/fail/skip

### Lifecycle (Manual Fixtures)

For custom fixture worktrees outside the standard runner:

```bash
# Create isolated worktree
git worktree add .worktrees/test-fixtures -b test/fixture-run-$(date +%s) --no-checkout

# Populate with fixture data, verify, run tests...

# Teardown
git worktree remove .worktrees/test-fixtures --force
git branch -D test/fixture-run-*
```

---

## Vault-Specific Test Patterns

### Pattern: Inbox Create → Verify

Test that `inbox_create` MCP tool produces a correctly structured file.

```javascript
describe('inbox_create', () => {
  it('creates file with correct frontmatter and directory', async () => {
    // Arrange: populate fixture with project stub
    await populateFixture(worktree, { files: [
      { path: '20_Projects/vault-infra/P99-Test.md',
        frontmatter: { type: 'project', status: 'active' } }
    ]});

    // Act: call inbox_create targeting fixture worktree
    const result = await mcpCall('inbox_create', {
      title: 'Test Item',
      project: 'P99-Test',
      priority: 'not-urgent-important',
    });

    // Assert
    assert.ok(result.ok);
    const created = parseFrontmatter(join(worktree, result.path));
    assertSchema(created, INBOX_SCHEMA);
    assert.match(result.path, /00_Inbox\/P99-Test\//);  // LR-INB-001
  });
});
```

### Pattern: Policy Scanner → Verify

Test that the drone policy scanner detects violations in known-bad fixtures.

```javascript
describe('policy scanner', () => {
  it('detects missing COM-001 attribution', async () => {
    // Arrange: fixture with unattributed commit
    await populateFixture(worktree, { files: [
      { path: '00_Inbox/bad-item.md',
        frontmatter: { type: 'inbox', status: 'active' },
        body: 'No attribution tag in commit' }
    ]});

    // Act: trigger policy scan
    const violations = await fetchJson(`http://localhost:${DRONE_TEST_PORT}/policies/scan`);

    // Assert: COM-001 violation detected
    assert.ok(violations.some(v => v.policy === 'COM-001'));
  });
});
```

### Pattern: Dashboard Render → Verify

Test that Dataview queries return expected results from fixture data.

```javascript
describe('dashboard render', () => {
  it('shows active inbox items in work mode', async () => {
    // Arrange: fixture with active and completed items
    await populateFixture(worktree, { files: [
      { path: '00_Inbox/P99-Test/active-item.md',
        frontmatter: { type: 'inbox', status: 'active', project: 'P99-Test' } },
      { path: '00_Inbox/P99-Test/done-item.md',
        frontmatter: { type: 'inbox', status: 'completed', project: 'P99-Test' } },
    ]});

    // Act: call dashboard_render for work mode
    const result = await mcpCall('dashboard_render', { mode: 'work' });

    // Assert: only active item appears
    assert.ok(result.includes('active-item'));
    assert.ok(!result.includes('done-item'));
  });
});
```

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Correct Pattern |
|-------------|---------|-----------------|
| Reading from `/vault` in tests | Non-deterministic, couples to user data | Use fixture worktree |
| `setTimeout(r, 2000)` | Flaky, slow on CI | `waitForState(fn, opts)` |
| Hardcoded port numbers | Conflicts with production | Use test profile ports (3837, 3938) |
| Inline fixture data in test files | Not reviewable, not reusable | External fixture.md spec |
| Testing frontmatter with regex | Fragile, misses edge cases | YAML parse + schema assertion |

---

## Related Skills

- `e2e:e2e` — General E2E testing workflow (test-first, progressive, iterative)
- `e2e:fixture-management` — Fixture.md parsing, validation, and sync verification
- `vault:vault-metadata` — Canonical frontmatter schema reference

---

## Metadata

**Last Updated:** 2026-04-12
**Version:** 1.4.0
**Author:** Christian Kusmanow / Claude
**Scope:** Vault testing operations within Docker containers
**Changelog:**
- v1.4.0: Rewrote fixture worktree section with S233 test environment architecture (docker-compose.test.yml, PARA skeleton, mount structure, env vars, batch execution model)
- v1.0.0: Initial release — PARA fixture structure, frontmatter assertions, worktree lifecycle, test patterns
