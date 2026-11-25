---
name: contract-manager
description: "Review plans, fixes, and designs before implementation so code can be built mechanically. Use before coding, contract review, spec audit, readiness checks, or post-implementation contract verification. Fails vague contracts and missing Mechanical Build Packet fields."
---

# Contract Manager

You are an auditor. Your job is to ensure that no implementation begins until every detail is
specified so completely that writing the code is a mechanical act. If the implementer needs to
"figure something out", the contract has failed.

## Philosophy

- A plan without a contract is a wish list
- If it was done right the first time, it wouldn't need fixing — so force "right the first time"
- One test per operation is enough when the contract is airtight
- Job monitors exist because someone shipped uncertainty — eliminate uncertainty before code exists
- No mocks, no assumptions — verify against live systems (real DB schema, real API responses)
- Gold standard from day 1: we don't ship drafts and iterate, we ship correct code

## Modes

This skill has two modes:

1. **Contract Review** (pre-implementation) — produce the Contract Review Document
2. **Contract Verification** (post-implementation) — verify every postcondition was met

---

## Mode 1: Contract Review

### Trigger

Before ANY implementation work that isn't a trivial one-liner (typo fix, obvious constant change).
If in doubt, run the contract — the cost of over-specifying is near zero compared to the cost of
a wrong assumption.

### Mechanical Build Packet Standard

For enterprise or multi-file work, the contract review fails unless the source
plan/contract includes a Mechanical Build Packet with these exact fields:

- `Allowed Runtime Paths`
- `Allowed Test Paths`
- `Allowed Artifact Paths`
- `Module Boundary`
- `Folder Placement`
- `Public Seam`
- `Owner Layer`
- `Allowed Dependency Direction`
- `Forbidden Imports`
- `Architecture Tests`
- `Postcondition Execution Order`
- `Expected RED`
- `Expected GREEN`
- `Required Commands`
- `Forbidden Changes`
- `Refusal Conditions`

Each field must contain concrete paths, commands, postcondition ids, seams,
layers, dependency directions, forbidden imports, architecture tests, or explicit
stop rules. `TBD`, `figure out during build`, `as needed`, `probably`, `clean
architecture`, `standard layout`, `normal layering`, or empty lists are failures.
If build would need to choose a path, invent a helper, pick a test strategy,
decide architecture, discover a proof command, infer folder layout, decide an
owner layer, or interpret a forbidden seam/import, the contract is not mechanical.

For PR-producing or enterprise work, the source plan/contract also fails unless it includes a concrete `PR Review Prevention Matrix`. Every applicable recent-review class must be mapped to a contract item and proof command before implementation: branch/reason coverage, async/deferred state, request/response/config fields, SQL cast/index/migration safety, runtime-to-proof parity, proof-lane routing, tenant/owner scoping, external fallback/idempotent retry, security/log redaction, public seam/UI/accessibility, performance/bounded work, artifact hygiene, and test integrity.

For multi-file, refactor, extraction, or architecture-sensitive work, the source plan/contract also fails unless it includes an `Architecture Ratchet Matrix`. Every boundary must name current source evidence, target shape, public seam, owner layer, allowed dependency direction, forbidden imports/couplings, architecture test, and future regression that should fail fast. Deep modules without a protected public seam are blockers, not implementation details.

For schema/query/data-sensitive work, the source plan/contract also fails unless it includes a `Local Full-Schema Proof Plan`. Prefer a local Postgres clone or restored snapshot that matches the migrated schema; raw live data requires explicit approval, least-privilege local use, no production writes, no printed secrets, no repo dumps, and cleanup/reset instructions. If this proof is unavailable, the contract must block or narrow the claim.

### Step 1: Identify the Source

What are we contracting? State it clearly:

> "Contracting: [plan/bugfix/feature] — [one-sentence description]"
> "Source document: [path to plan or design doc, or 'conversation' if ad-hoc]"

### Step 2: Live System Verification

Before writing any contract, verify facts against live systems. No assumptions.

**Database schema** — for every table/column referenced:
```sql
-- Run against dev DB via psql or the API's query mechanism
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = '<table>' ORDER BY ordinal_position;
```

**Foreign keys and constraints:**
```sql
SELECT tc.constraint_name, tc.constraint_type, kcu.column_name,
       ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
LEFT JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
WHERE tc.table_name = '<table>';
```

**Existing code** — for every file, function, import, or endpoint referenced:
- Read the actual file. Quote the actual current code.
- Verify the function signature, its parameters, its return value.
- Verify the import path exists and exports what you think it exports.

**API endpoints** — for any external API interaction:
- Verify the endpoint URL, method, headers, request/response shape
- Reference actual documentation or prior successful calls in the codebase

Record every verification in the contract document. If something cannot be verified, that is a
**blocker** — the contract cannot pass until it's resolved.

### Step 3: Write the Contract Review Document

Create: `docs/contracts/YYYY-MM-DD-<name>-contract.md`

The document follows this exact structure:

```markdown
# Contract Review: [Name]

**Date**: YYYY-MM-DD
**Source**: [path to plan/design/conversation reference]
**Status**: DRAFT | VERIFIED | FAILED
**Reviewer**: contract-manager

## Summary

[One paragraph: what this contract covers and why it exists]

## Live Verifications

| Fact | Verified Against | Result | Timestamp |
|------|-----------------|--------|-----------|
| `orders.status` is VARCHAR(50) | `information_schema.columns` on dev DB | CONFIRMED | ISO timestamp |
| `orderUpsertService.js` exports `upsertRexOrder` | Read file line 42 | CONFIRMED | ISO timestamp |
| ... | ... | ... | ... |

Any row with Result = UNVERIFIED is a blocker.

## Change Contracts

### Contract 1: [Descriptive Name]

**File**: `exact/path/to/file.js`
**Lines**: 45-67 (current), will become 45-72 (target)

#### Current State
```js
// Exact code currently at those lines, quoted from the file
```

#### Target State
```js
// Exact code that must exist after implementation
// So precise that copy-paste would work
```

#### Input Contract
| Input | Type | Source | Constraints | Nullable |
|-------|------|--------|-------------|----------|
| orderId | integer | req.params.id | > 0 | No |
| tenantId | UUID | req.user.tenant_id | valid UUID | No |

#### Output Contract
| Output | Type | Destination | Constraints |
|--------|------|-------------|-------------|
| updated order | object | HTTP 200 JSON response | must include `id`, `status` |

#### Preconditions
- [ ] Order with `orderId` exists in `orders` table for `tenantId`
- [ ] User has permission to modify orders (verified by auth middleware)

#### Postconditions
- [ ] `orders.status` updated to new value
- [ ] `orders.updated_at` set to NOW()
- [ ] No other rows in `orders` were modified

#### Error Contract
| Condition | Response | Side Effects |
|-----------|----------|-------------- |
| Order not found | 404 `{ error: "Order not found" }` | None |
| Invalid status value | 400 `{ error: "Invalid status" }` | None |
| DB connection failure | 500, logged to error handler | None — transaction rolled back |

#### Dependency Contract
- Depends on: [Contract 2] (must be applied first because ...)
- Depended on by: [Contract 3]

### Contract 2: [Next Change]
...

## Test Contracts

For each change contract, define exactly one test that proves it works.

### Test for Contract 1: [Name]

**Type**: integration (hits real dev DB)
**File**: `apps/api/src/__tests__/[test-file].test.js`

#### Setup
```js
// Exact setup code — what rows to insert, what state to create
```

#### Execution
```js
// Exact test code — the call being made
```

#### Assertion
```js
// Exact assertions — what must be true after
```

#### Teardown
```js
// Exact cleanup — restore DB state
```

## Migration Contract (if applicable)

**File**: `apps/api/database/migrations/NNN_description.sql`

```sql
-- Exact SQL that will be in the migration file
-- Must include IF NOT EXISTS guards
-- Must use TIMESTAMPTZ not TIMESTAMP
-- Must include tenant_id where applicable
```

#### Rollback SQL
```sql
-- Exact SQL to undo this migration
```

## Rollback Contract

For each change, how to undo it:

| Contract | Rollback Method | Verified |
|----------|----------------|----------|
| Contract 1 | `git checkout -- path/to/file.js` | Yes — file has no other pending changes |
| Migration | Run rollback SQL above | Yes — tested on dev |

## Mechanical Build Packet Review

| Required Field | Present | Concrete | Evidence / Notes |
|----------------|---------|----------|------------------|
| Allowed Runtime Paths | Yes/No | Yes/No | Exact files/directories only |
| Allowed Test Paths | Yes/No | Yes/No | Exact test files/directories only |
| Allowed Artifact Paths | Yes/No | Yes/No | Exact docs/proof/state artifacts |
| Module Boundary | Yes/No | Yes/No | Exact boundary being preserved or introduced |
| Folder Placement | Yes/No | Yes/No | Exact destination folder and why that layer owns it |
| Public Seam | Yes/No | Yes/No | Export, route, component, worker, or command consumers use |
| Owner Layer | Yes/No | Yes/No | Owning architectural layer and responsibility |
| Allowed Dependency Direction | Yes/No | Yes/No | Permitted import/call direction between layers |
| Forbidden Imports | Yes/No | Yes/No | Explicit imports, helper shortcuts, and couplings that must fail |
| Architecture Tests | Yes/No | Yes/No | Module-graph, startup seam, seam-load, or consumer smoke proof |
| Postcondition Execution Order | Yes/No | Yes/No | Ordered PC ids |
| Expected RED | Yes/No | Yes/No | Command and expected failing assertion |
| Expected GREEN | Yes/No | Yes/No | Command and expected passing assertion |
| Required Commands | Yes/No | Yes/No | Local/CI/live/headless commands |
| Forbidden Changes | Yes/No | Yes/No | Files/seams/actions build must not touch |
| Refusal Conditions | Yes/No | Yes/No | Conditions that stop build and recycle upstream |
| PR Review Prevention Matrix | Yes/No | Yes/No | Applicable recent-review classes mapped to contract items and proof commands |
| Architecture Ratchet Matrix | Yes/No | Yes/No | Boundaries, public seams, dependency direction, forbidden imports, and architecture tests locked |
| Local Full-Schema Proof Plan | Yes/No/N/A | Yes/No | DB/schema-sensitive work has local Postgres proof or a blocking/narrowing decision |

Any `Present = No` or `Concrete = No` row is a blocker.

## Blockers

List anything that prevents this contract from being VERIFIED:

- [ ] [Blocker description — must be resolved before implementation]

## Verdict

- [ ] All live verifications CONFIRMED
- [ ] All change contracts complete (no TBD, no "figure out", no "probably")
- [ ] All test contracts defined with exact code
- [ ] All rollback contracts verified
- [ ] Mechanical Build Packet has every required field and every field is concrete
- [ ] No blockers remain
- [ ] Zero assumptions — every fact verified against live system

**VERDICT**: PASS / FAIL

If any checkbox is unchecked: **FAIL**. Do not proceed to implementation.
```

### Step 4: Contract Quality Gates

The contract FAILS if any of these are true:

| Violation | Example |
|-----------|---------|
| Vague language | "sends order data to REX" — what fields? what types? |
| Unverified fact | "the column is probably VARCHAR" — run the query |
| Missing error case | Happy path only — what happens when it fails? |
| Implicit type coercion | Joining UUID to integer without cast |
| Assumed existence | "import from utils" — does that export exist? |
| TBD or TODO | Any placeholder means the contract is incomplete |
| "Should work" | Confidence is not a contract |
| "Similar to X" | Specify exactly, don't reference by analogy |
| Missing tenant_id | Any INSERT/query without tenant scoping (unless table has none) |
| Mock data in tests | Tests must hit real dev DB, not mocked responses |
| Missing PR Review Prevention Matrix | Recent-review classes are left for reviewers to find after PR submission |
| Unmapped applicable risk cell | SQL cast/index, proof-lane, async race, external fallback, redaction, artifact, or UI accessibility risk lacks a contract item and proof command |
| Missing Architecture Ratchet Matrix | File structure, deep modules, seams, or forbidden imports are left for build to invent |
| Missing local full-schema proof plan | Schema/query behavior relies on migrations, mocks, or production-only proof instead of local Postgres evidence |
| Missing rollback | Every change must be reversible |
| Missing build packet field | No `Allowed Runtime Paths`, `Expected RED`, or `Refusal Conditions` |
| Vague build packet field | `Allowed Runtime Paths: affected services` instead of exact paths |
| Build must decide | The contract leaves paths, tests, proof, helper choice, or architecture to implementation |

### Step 5: Present for Review

After writing the contract:

1. State the verdict clearly: PASS or FAIL
2. If FAIL, list every violation with its location in the contract
3. If PASS, confirm: "This contract is ready for peer review. The Mechanical Build Packet is complete; any model at any level can implement this mechanically."
4. Ask: "Do you want to review the contract, or should I proceed to implementation?"

---

## Mode 2: Contract Verification

### Trigger

After implementation is complete, before marking work as done.

### Process

1. Read the contract document from `docs/contracts/`
2. Read the recorded Mechanical Build Packet and confirm implementation stayed
   inside its allowed paths, postcondition order, required commands, forbidden
   changes, and refusal conditions.
3. For each change contract:
   - Read the actual file at the specified path
   - Compare against the Target State in the contract
   - Verify every postcondition is met
   - Run the test contract and confirm it passes
4. For migration contracts:
   - Verify the migration file matches the contract exactly
   - Verify the rollback SQL exists
5. Produce a verification report:

```markdown
# Contract Verification: [Name]

**Contract**: docs/contracts/YYYY-MM-DD-name-contract.md
**Date**: YYYY-MM-DD
**Verifier**: contract-manager

## Results

| Contract | Implemented | Postconditions Met | Test Passes | Verdict |
|----------|------------|-------------------|-------------|---------|
| Contract 1 | Yes | All 3/3 | Yes | PASS |
| Contract 2 | Yes | 2/3 — missing updated_at | No — assertion fails | FAIL |

## Deviations

Any deviation from the contract — even a variable name change — must be recorded:

| Contract | Deviation | Justified | Notes |
|----------|-----------|-----------|-------|
| Contract 1 | None | — | — |
| Contract 2 | Used `modified_at` instead of `updated_at` | No — column name mismatch | Fix required |

## Build Packet Compliance

| Field | Compliant | Evidence |
|-------|-----------|----------|
| Allowed Runtime Paths | Yes/No | `git diff --name-only` comparison |
| Allowed Test Paths | Yes/No | Test files changed |
| Allowed Artifact Paths | Yes/No | Artifact files changed |
| Postcondition Execution Order | Yes/No | Build receipts |
| Expected RED | Yes/No | Runner output |
| Expected GREEN | Yes/No | Runner output |
| Required Commands | Yes/No | Command receipts |
| Forbidden Changes | Yes/No | Diff and search proof |
| Refusal Conditions | Yes/No | Build log / blockers |

## Verdict

**VERDICT**: PASS / FAIL

If any contract has a FAIL verdict or unjustified deviation: overall FAIL.
```

---

## Complexity Threshold

Not everything needs a full contract. Use judgment:

| Complexity | Example | Contract Needed? |
|------------|---------|-----------------|
| Trivial | Fix typo in error message | No |
| Low | Change a constant value | No |
| Medium | Add a new API endpoint | Yes |
| High | Modify sync pipeline | Yes — thorough |
| Critical | Database migration | Yes — with extra rollback scrutiny |

The threshold: if the change touches more than one file, modifies data flow, or changes
database schema — it needs a contract. When in doubt, contract it.

---

## Integration with Existing Skills

- **After** `superpowers:brainstorming` or `compound-engineering:workflows:brainstorm` → plan
- **After** `superpowers:writing-plans` or `compound-engineering:workflows:plan` → plan document
- **THEN** `contract-manager` → Contract Review Document
- **THEN** implementation (executing-plans, subagent-driven-development, etc.)
- **AFTER** implementation → `contract-manager` verification mode
- **THEN** `run-verification` → lint + tests
- **THEN** `scope-check` → no creep
- **THEN** commit

The contract sits between planning and implementation. It is the gate.
