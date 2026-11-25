---
name: prdoc-generator
description: Generates prdoc YAML files for Polkadot SDK pull requests. Analyzes git diffs to determine affected crates, appropriate bump levels, audiences, and descriptions. Use when creating or updating PR documentation files.
---

# PRDoc Generator

## 1. Purpose

Generate proper `prdoc` YAML files that document PR changes for the Polkadot SDK. These files drive release notes, crate publishing decisions, and stakeholder communication. Every PR needs a prdoc file unless labeled `R0-no-crate-publish-required`.

## 2. When to Use This Skill

- Creating a new prdoc for a pull request
- Updating an existing prdoc after PR changes
- Determining which crates are affected by changes
- Choosing appropriate semver bump levels and audiences

## 3. How This Skill Works

When invoked, I will:

1. Analyze `git diff` against the base branch to identify all changed files
2. Map changed files to their crate names (from nearest `Cargo.toml`)
3. Analyze the nature of changes to determine semver bump levels
4. Identify the appropriate audience(s) for the changes
5. Draft a title and description summarizing the changes
6. Generate the prdoc YAML file at `prdoc/pr_<NUMBER>.prdoc`

---

## 4. PRDoc File Format

The schema is defined at `prdoc/schema_user.json`.

### Required Fields

```yaml
# Schema: Polkadot SDK PRDoc Schema (prdoc) v1.0.0
# See doc at https://raw.githubusercontent.com/paritytech/polkadot-sdk/master/prdoc/schema_user.json

title: Short descriptive title of the change

doc:
  - audience: Runtime Dev
    description: |
      Description of changes relevant to this audience.

crates:
  - name: pallet-example
    bump: minor
```

### Optional Fields

```yaml
author: github-handle
topic: some-topic

migrations:
  db: []
  runtime:
    - reference: pallet_example::migrations::v2::MigrateV1ToV2
      description: |
        Description of what the migration does.

host_functions:
  - name: host_function_name
    description: Description of the host function
```

### File Naming

- File must be named `pr_<NUMBER>.prdoc`
- Placed in the `prdoc/` directory at the repository root
- Example: `prdoc/pr_11064.prdoc`

---

## 5. Audience Types

| Audience | Description | When to Use |
|----------|-------------|-------------|
| `Runtime Dev` | Parachain teams using pallets, DApp developers who rely on the runtime | Pallet changes, Config trait changes, storage changes, new extrinsics |
| `Node Dev` | Alternative client builders, RPC consumers, those who work with client-side code | Client/node changes, RPC changes, networking changes |
| `Node Operator` | Those who don't write code and only run nodes | CLI flag changes, configuration changes, operational changes |
| `Runtime User` | Token holders, front-end developers, anyone using the runtime | User-facing behavior changes, fee changes, governance changes |

Multiple audiences can be specified per doc entry or as separate entries:

```yaml
# Single audience
doc:
  - audience: Runtime Dev
    description: ...

# Multiple audiences on one entry
doc:
  - audience: [Node Dev, Node Operator]
    description: ...

# Separate entries per audience
doc:
  - audience: Runtime Dev
    description: Changes relevant to runtime devs...
  - audience: Node Operator
    description: Changes relevant to operators...
```

---

## 6. Bump Level Determination

| Bump | When to Use | Examples |
|------|-------------|---------|
| `major` | Breaking API changes | Config trait changes, removed/renamed public items, changed function signatures |
| `minor` | New features, non-breaking additions | New extrinsics, new storage items, new events, new trait implementations |
| `patch` | Bug fixes, internal refactoring | Bug fixes, documentation, performance improvements |
| `none` | No effect on crate consumers | Test-only changes, CI changes |

### Decision Tree

1. Does it change a public API (types, traits, function signatures)? -> `major`
2. Does it add new public functionality without breaking existing? -> `minor`
3. Does it fix a bug or refactor internals? -> `patch`
4. Does it only change tests, docs, or non-published code? -> `patch` or `none`

### Crate Bump Notes

You can add a `note` field to explain non-obvious bumps:

```yaml
crates:
  - name: pallet-multisig
    bump: major
    note: Config trait replaces `type Currency` with `type Fungible`
```

---

## 7. Identifying Affected Crates

### Workflow

1. Run `git diff --name-only <base-branch>...HEAD` to get changed files
2. For each changed file, find the nearest `Cargo.toml` up the directory tree
3. Extract the `name` field from each `Cargo.toml`
4. Consider downstream crates that re-export or depend on changed types
5. Runtime crates that wire the pallet should also be listed if their configuration changes

### Common Mappings

| Path Pattern | Crate Name Pattern |
|-------------|-------------------|
| `substrate/frame/<name>/` | `pallet-<name>` |
| `substrate/primitives/<name>/` | `sp-<name>` |
| `polkadot/node/<name>/` | `polkadot-node-<name>` |
| `cumulus/pallets/<name>/` | `cumulus-pallet-<name>` |
| `cumulus/parachains/runtimes/assets/asset-hub-*/` | `asset-hub-*-runtime` |

---

## 8. Migration Documentation

When PRs include storage migrations, document them in the `migrations` field:

```yaml
migrations:
  runtime:
    - reference: pallet_multisig::migrations::v2::LazyMigrationV1ToV2
      description: |
        Stepped migration that converts multisig deposits from Currency::reserve
        to Fungible::hold with HoldReason::MultisigOperation. Iterates through
        all Multisigs storage entries, unreserves the old deposit, and creates
        a new hold.
  db: []
```

---

## 9. Real Examples

### Simple patch fix

```yaml
title: 'revive: fix revive post_upgrade assert'
doc:
  - audience: Runtime Dev
    description: Fix post_upgrade assertion logic in revive v2 migration
crates:
  - name: pallet-revive
    bump: patch
```

### Major breaking change with migration

```yaml
title: Refactor multisig pallet to use fungible traits instead of Currency
doc:
  - audience: Runtime Dev
    description: |
      The multisig pallet now uses the modern `fungible` traits (`Inspect`, `Mutate`,
      `InspectHold`, `MutateHold`) instead of the deprecated `Currency` / `ReservableCurrency`
      traits. Deposits are now managed via hold/release with a `HoldReason::MultisigOperation`
      reason instead of reserve/unreserve.

      Breaking change: the `Config` trait replaces `type Currency` with `type Fungible`.
      Runtimes must update their multisig configuration accordingly:
      ```rust
      // Before
      type Currency = Balances;
      // After
      type Fungible = Balances;
      ```

      A multi-block migration (`LazyMigrationV1ToV2`) is provided to convert existing reserved
      deposits to holds. Runtimes with `pallet_migrations` should register it in their
      `Migrations` tuple.
migrations:
  runtime:
    - reference: pallet_multisig::migrations::v2::LazyMigrationV1ToV2
      description: |
        Stepped migration that converts multisig deposits from Currency::reserve to
        Fungible::hold with HoldReason::MultisigOperation.
crates:
  - name: pallet-multisig
    bump: major
```

---

## 10. Generation Workflow

### Step 1: Gather Information
```bash
# Get the PR number (from branch or user input)
git log --oneline <base>...HEAD

# See all changed files
git diff --name-only <base>...HEAD

# See the actual changes
git diff <base>...HEAD
```

### Step 2: Map Files to Crates
For each changed file, find its crate by looking at the nearest `Cargo.toml`.

### Step 3: Analyze Changes
- Read the diff to understand what changed
- Determine if changes are breaking, additive, or fixes
- Identify the audience(s) affected

### Step 4: Write the PRDoc
Generate the YAML file with proper structure and save to `prdoc/pr_<NUMBER>.prdoc`.

---

## 11. Checklist

Before finalizing a prdoc:

- [ ] Title is concise and descriptive (what changed, not how)
- [ ] At least one `doc` entry with appropriate audience and description
- [ ] All affected crates listed with correct bump levels
- [ ] Description explains the "why" and impact, not just the "what"
- [ ] Breaking changes are explicitly called out in description
- [ ] Migration information included if applicable
- [ ] File named correctly as `pr_<NUMBER>.prdoc`
- [ ] YAML is valid and follows the schema
