---
name: fixture-management
description: |
  Fixture.md parsing, validation, and test orchestration. Provides fixture-to-worktree sync,
  precondition verification, expected outcome assertion, and test report generation.
  Use when managing test fixtures, validating fixture specs, or running fixture-driven tests.
  Keywords: fixture, test management, sync, validation, test report, fixture.md.
triggers:
  - /e2e fixture-management
  - /fixture-management
  - fixture validation
  - fixture sync check
  - test fixture management
  - fixture.md parsing
negative_triggers:
  - vault PARA structure (use e2e:vault-testing)
  - frontmatter assertions (use e2e:vault-testing)
  - visual testing (use e2e:e2e)
  - Cypress tests (use e2e:e2e)
version: 1.4.0
author: Christian Kusmanow / Claude
last_updated: 2026-04-12
security:
  trust_model: File system read/write within .worktrees/test-fixtures/ only. No network access.
  api_endpoints: []
  notes: Fixture operations are confined to test worktrees. Production vault is never modified.
---

# Skill: Fixture Management

Manages the lifecycle of fixture.md specs — parsing, validation, worktree sync, test execution,
and report generation. This is the operational counterpart to `e2e:vault-testing` (which provides
vault-specific test knowledge).

## Trigger

- `/e2e fixture-management` — Load fixture management context
- `/fixture-management` — Alias

---

## fixture.md Parsing

### Frontmatter Extraction

Parse the YAML frontmatter from a fixture.md file into a structured object.

```javascript
import { readFileSync } from 'fs';
import { parse as parseYaml } from 'yaml';

/**
 * Parse a fixture.md file into { frontmatter, sections } structure.
 * @param {string} fixturePath - Absolute path to the fixture.md file
 * @returns {{ frontmatter: object, sections: Record<string, string> }}
 */
function parseFixture(fixturePath) {
  const raw = readFileSync(fixturePath, 'utf8');

  // Extract frontmatter
  const fmMatch = raw.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) throw new Error(`No frontmatter in fixture: ${fixturePath}`);
  const frontmatter = parseYaml(fmMatch[1]);

  // Extract named sections (## headings)
  const sections = {};
  const sectionRegex = /^## (.+)\n([\s\S]*?)(?=\n## |\n*$)/gm;
  let match;
  while ((match = sectionRegex.exec(raw)) !== null) {
    sections[match[1].trim()] = match[2].trim();
  }

  return { frontmatter, sections };
}
```

### Required Fields Validation

```javascript
const FIXTURE_REQUIRED_FIELDS = [
  'type', 'fixture_id', 'name', 'fixture_path',
  'test_mode', 'dependencies', 'category', 'created', 'status'
];

const FIXTURE_ENUMS = {
  type: ['fixture'],
  test_mode: ['test-first', 'test-after'],
  category: ['unit', 'integration', 'e2e'],
  status: ['active', 'deprecated', 'draft'],
};

function validateFixtureFrontmatter(fm) {
  const errors = [];

  // Required fields
  for (const field of FIXTURE_REQUIRED_FIELDS) {
    if (fm[field] === undefined) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // Enum validation
  for (const [field, allowed] of Object.entries(FIXTURE_ENUMS)) {
    if (fm[field] && !allowed.includes(fm[field])) {
      errors.push(`Invalid ${field}: "${fm[field]}" (allowed: ${allowed.join(', ')})`);
    }
  }

  // fixture_id format
  if (fm.fixture_id && !/^FIX-\d{3,}$/.test(fm.fixture_id)) {
    errors.push(`Invalid fixture_id format: "${fm.fixture_id}" (expected FIX-NNN)`);
  }

  // dependencies must be array
  if (fm.dependencies && !Array.isArray(fm.dependencies)) {
    errors.push('dependencies must be an array');
  }

  return { valid: errors.length === 0, errors };
}
```

### Section Validation

```javascript
const FIXTURE_REQUIRED_SECTIONS = [
  'Preconditions',
  'Fixture Data',
  'Steps',
  'Expected Outcomes',
  'Verification Commands',
];

function validateFixtureSections(sections) {
  const errors = [];
  for (const name of FIXTURE_REQUIRED_SECTIONS) {
    if (!sections[name]) {
      errors.push(`Missing required section: ## ${name}`);
    } else if (sections[name].length < 20) {
      errors.push(`Section too short (stub?): ## ${name}`);
    }
  }
  return { valid: errors.length === 0, errors };
}
```

---

## Reproduction Step Execution

### Step Parser

Extract ordered steps from the `## Steps` section.

```javascript
/**
 * Parse numbered steps from fixture body.
 * @param {string} stepsSection - Raw markdown of ## Steps section
 * @returns {Array<{ number: number, label: string, description: string }>}
 */
function parseSteps(stepsSection) {
  const stepRegex = /^(\d+)\.\s+\*\*(.+?)\*\*\s+[—–-]\s+(.+)$/gm;
  const steps = [];
  let match;
  while ((match = stepRegex.exec(stepsSection)) !== null) {
    steps.push({
      number: parseInt(match[1]),
      label: match[2].trim(),
      description: match[3].trim(),
    });
  }
  return steps;
}
```

### Step Executor

Execute each step in sequence, collecting results.

```javascript
/**
 * Execute fixture steps sequentially.
 * Uses readiness utilities for wait steps.
 */
async function executeSteps(steps, context) {
  const results = [];

  for (const step of steps) {
    const start = Date.now();
    try {
      switch (step.label.toLowerCase()) {
        case 'setup':
          await context.setup();
          break;
        case 'trigger':
          await context.trigger(step.description);
          break;
        case 'wait':
          // Delegate to readiness utilities — never setTimeout
          await context.waitReady(step.description);
          break;
        case 'act':
          await context.act(step.description);
          break;
        case 'assert':
          await context.assert(step.description);
          break;
        default:
          await context.custom(step);
      }
      results.push({ step: step.number, label: step.label, ok: true, ms: Date.now() - start });
    } catch (err) {
      results.push({ step: step.number, label: step.label, ok: false, ms: Date.now() - start, error: err.message });
      break; // Stop on first failure
    }
  }

  return results;
}
```

---

## Expected Outcome Verification

### Outcome Parser

Extract expected outcomes from the `## Expected Outcomes` table.

```javascript
/**
 * Parse the Expected Outcomes markdown table.
 * @returns {Array<{ step: number, assertion: string, evidence: string }>}
 */
function parseExpectedOutcomes(section) {
  const rows = section.split('\n')
    .filter(line => line.startsWith('|') && !line.includes('---'))
    .slice(1); // Skip header

  return rows.map(row => {
    const cells = row.split('|').map(c => c.trim()).filter(Boolean);
    return {
      step: parseInt(cells[0]),
      assertion: cells[1],
      evidence: cells[2],
    };
  });
}
```

### Outcome Matcher

Compare actual results against expected outcomes.

```javascript
function matchOutcomes(actualResults, expectedOutcomes) {
  const report = [];

  for (const expected of expectedOutcomes) {
    const actual = actualResults.find(r => r.step === expected.step);
    if (!actual) {
      report.push({ ...expected, status: 'SKIP', reason: 'Step did not execute' });
    } else if (actual.ok) {
      report.push({ ...expected, status: 'PASS' });
    } else {
      report.push({ ...expected, status: 'FAIL', reason: actual.error });
    }
  }

  return report;
}
```

---

## Fixture-to-Worktree Sync Verification

Ensure the worktree contents match what the fixture.md declares.

### Full Sync Check

```javascript
/**
 * Compare fixture spec declarations against actual worktree contents.
 * @returns {{ synced: boolean, diffs: Array<{ path: string, issue: string }> }}
 */
function syncCheck(fixtureSpec, worktreePath) {
  const diffs = [];

  // 1. Check all declared files exist
  for (const file of fixtureSpec.files) {
    const fullPath = join(worktreePath, file.path);
    if (!existsSync(fullPath)) {
      diffs.push({ path: file.path, issue: 'MISSING — declared in fixture but not in worktree' });
      continue;
    }

    // 2. Check frontmatter matches
    if (file.frontmatter) {
      const actual = parseFrontmatter(fullPath);
      for (const [key, expected] of Object.entries(file.frontmatter)) {
        if (actual[key] !== expected) {
          diffs.push({
            path: file.path,
            issue: `MISMATCH — ${key}: expected "${expected}", got "${actual[key]}"`,
          });
        }
      }
    }
  }

  // 3. Check for undeclared files (unexpected content in worktree)
  const declaredPaths = new Set(fixtureSpec.files.map(f => f.path));
  const actualFiles = walkDir(worktreePath);
  for (const actual of actualFiles) {
    const rel = relative(worktreePath, actual);
    if (!declaredPaths.has(rel) && !rel.startsWith('.git')) {
      diffs.push({ path: rel, issue: 'EXTRA — exists in worktree but not declared in fixture' });
    }
  }

  return { synced: diffs.length === 0, diffs };
}
```

### Incremental Sync Check

For fast CI runs, only check files modified since last sync.

```javascript
function incrementalSyncCheck(fixtureSpec, worktreePath, since) {
  const modifiedFiles = execSync(
    `git -C "${worktreePath}" diff --name-only --since="${since}"`,
    { encoding: 'utf8' }
  ).trim().split('\n').filter(Boolean);

  const relevantFiles = fixtureSpec.files.filter(f =>
    modifiedFiles.includes(f.path)
  );

  return syncCheck({ files: relevantFiles }, worktreePath);
}
```

---

## Test Report Generation

### Report Structure

```javascript
/**
 * Generate a structured test report from fixture execution results.
 */
function generateReport(fixtureSpec, stepResults, outcomeReport) {
  const passed = outcomeReport.filter(o => o.status === 'PASS').length;
  const failed = outcomeReport.filter(o => o.status === 'FAIL').length;
  const skipped = outcomeReport.filter(o => o.status === 'SKIP').length;
  const totalMs = stepResults.reduce((sum, r) => sum + r.ms, 0);

  return {
    fixture_id: fixtureSpec.frontmatter.fixture_id,
    name: fixtureSpec.frontmatter.name,
    category: fixtureSpec.frontmatter.category,
    timestamp: new Date().toISOString(),
    duration_ms: totalMs,
    summary: { passed, failed, skipped, total: passed + failed + skipped },
    steps: stepResults,
    outcomes: outcomeReport,
    verdict: failed === 0 ? 'PASS' : 'FAIL',
  };
}
```

### Markdown Report

```javascript
function reportToMarkdown(report) {
  const icon = report.verdict === 'PASS' ? 'PASS' : 'FAIL';
  let md = `# Fixture Report: ${report.name} (${icon})\n\n`;
  md += `| Field | Value |\n|-------|-------|\n`;
  md += `| Fixture ID | ${report.fixture_id} |\n`;
  md += `| Category | ${report.category} |\n`;
  md += `| Duration | ${report.duration_ms}ms |\n`;
  md += `| Passed | ${report.summary.passed} |\n`;
  md += `| Failed | ${report.summary.failed} |\n`;
  md += `| Skipped | ${report.summary.skipped} |\n\n`;

  md += `## Step Results\n\n`;
  md += `| # | Label | Status | Time |\n|---|-------|--------|------|\n`;
  for (const s of report.steps) {
    md += `| ${s.step} | ${s.label} | ${s.ok ? 'OK' : 'FAIL'} | ${s.ms}ms |\n`;
  }

  md += `\n## Outcome Assertions\n\n`;
  md += `| Step | Assertion | Status | Reason |\n|------|-----------|--------|--------|\n`;
  for (const o of report.outcomes) {
    md += `| ${o.step} | ${o.assertion} | ${o.status} | ${o.reason || '—'} |\n`;
  }

  return md;
}
```

---

## Fixture Runner Architecture (S233)

### `spawnAndWait()` — No-Timeout Execution

The fixture runner uses `spawnAndWait()` for all test execution. There are no timeouts
(`AbortController`, `AbortSignal.timeout()`, `setTimeout`) per LR-TMO-001. If a test
hangs, that is a real bug to investigate, not a timeout to manage.

```javascript
function spawnAndWait(cmd, cwd, env) {
  return new Promise((resolve) => {
    const child = spawn(cmd, { shell: true, cwd, env, stdio: 'pipe' });
    let stdout = '', stderr = '';
    child.stdout.on('data', (d) => { stdout += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('close', (code) => { resolve({ code, stdout, stderr }); });
  });
}
```

### Cross-Fixture Jest Batching (`planBatchSegments`)

Multiple fixtures that share `runtime::cwd` (e.g., 7 Jest plugin fixtures all targeting
`.obsidian/plugins/harness-telemetry/`) are merged into a single process invocation.
This eliminates redundant cold-starts (~8-12s each for Jest module resolution + transform).

**Batching rules:**
- Eligible: has tests, single runtime::cwd group, runtime is `jest` or `node` (not `bun`)
- `bun` fixtures cannot batch — each bootstraps a full server in `beforeAll` causing port conflicts
- Consecutive eligible fixtures with the same key are grouped into one process
- Results are mapped back to per-fixture granularity

### Baseline Report Format

The baseline report at `coordination/tests/baseline-report.json` tracks fixture results:

```json
{
  "timestamp": "2026-04-12T...",
  "vault_root": ".worktrees/e2e-fixture",
  "test_mode": "fixture",       // "fixture" or "production"
  "fixtures_total": 41,
  "pass": 41, "fail": 0, "skip": 0,
  "results": [
    { "fixture_id": "FIX-001", "name": "...", "status": "pass", "duration_ms": 1234 }
  ]
}
```

**`test_mode` field:** Distinguishes fixture-only baselines (`"fixture"`) from production-vault
baselines (`"production"`). Consumers use this to determine which environment produced the results.

**Filter + merge:** When `--filter` is used, the runner merges current results with the
existing baseline — only filtered fixture rows are replaced, all others are preserved.
This enables per-fixture re-runs without destroying the broader baseline.

### Seed Pattern (Future)

Option B: `coordination/tests/fixtures/_seed/` — a directory for seed data files shared
across multiple fixtures. Not currently needed (fixtures are self-contained) but documented
as the designated location if cross-fixture shared state becomes necessary.

---

## Workflow: Fixture Validation

When invoked, guide the agent through fixture validation:

1. **Discover** — Find all `*.fixture.md` files in the project
2. **Parse** — Extract frontmatter and sections from each
3. **Validate** — Check required fields, enums, sections
4. **Report** — Summarize valid/invalid fixtures with specific errors

```
/fixture-management validate
→ Found 3 fixture.md files
→ FIX-001: VALID (inbox-frontmatter-validation)
→ FIX-002: INVALID — Missing section: ## Verification Commands
→ FIX-003: VALID (policy-scanner-detection)
```

## Workflow: Fixture Run

Execute a specific fixture end-to-end:

1. **Parse** the fixture.md
2. **Create** fixture worktree
3. **Populate** with declared files
4. **Verify** preconditions
5. **Execute** steps sequentially
6. **Assert** expected outcomes
7. **Report** results
8. **Teardown** worktree

```
/fixture-management run FIX-001
→ Parsing FIX-001...
→ Creating worktree .worktrees/test-fixtures/
→ Populating 3 files...
→ Preconditions: 3/3 passed
→ Step 1 (Setup): OK (120ms)
→ Step 2 (Trigger): OK (45ms)
→ Step 3 (Wait): OK (1200ms)
→ Step 4 (Act): OK (89ms)
→ Step 5 (Assert): OK (12ms)
→ Outcomes: 4/4 PASS
→ Teardown: OK
→ VERDICT: PASS (1466ms)
```

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Correct Pattern |
|-------------|---------|-----------------|
| Fixture with no `## Steps` | Not reproducible | Always include ordered steps |
| Inline fixture data in test JS | Can't validate independently | External fixture.md |
| Skipping sync check | Stale fixtures silently pass | Always run `syncCheck()` before test |
| Mutable fixture data | Tests interfere with each other | Fresh worktree per run |
| No teardown | Worktree accumulation | Always remove worktree after test |

---

## Related Skills

- `e2e:vault-testing` — PARA fixture knowledge, frontmatter assertion patterns
- `e2e:e2e` — General E2E testing workflow (test-first, progressive, iterative)
- `vault:vault-metadata` — Canonical frontmatter schema reference

---

## Metadata

**Last Updated:** 2026-04-12
**Version:** 1.4.0
**Author:** Christian Kusmanow / Claude
**Scope:** Fixture lifecycle management for Docker-based testing
**Changelog:**
- v1.4.0: Added fixture runner architecture (spawnAndWait, cross-fixture batching, baseline report format, seed pattern)
- v1.0.0: Initial release — parsing, validation, sync check, step execution, report generation
