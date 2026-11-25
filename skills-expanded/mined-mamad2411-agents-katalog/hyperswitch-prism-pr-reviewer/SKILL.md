---
name: hyperswitch-prism-pr-reviewer
description: >
  Reviews pull requests in the hyperswitch-prism (UCS) Rust codebase using a strict,
  fail-closed, scenario-aware review system. Supports Rust core and TypeScript/Python/Java SDKs.
license: Apache-2.0
compatibility: Requires git and gh CLI. Works with any AI coding tool.
metadata:
  author: parallal
  version: "1.0-portable"
  domain: code-review
  scope: global
---

# Hyperswitch Prism PR Reviewer

## Overview

This skill reviews pull requests in `hyperswitch-prism` with a strict, evidence-driven, code-only posture. It uses a nested-subagent workflow:

**orchestrator -> classifier -> scenario subagents -> aggregator**

Each PR is classified into one or more of 13 repo-specific scenarios, then reviewed by the exact specialist subagents that match.

**Supported Languages:**
- **Core:** Rust (primary codebase)
- **SDKs:** TypeScript, Python, Java

## When to Use

| Request | Workflow |
|---------|----------|
| Review any PR | Full PR Review |
| Review a GRACE-authored PR | GRACE PR Review |
| Batch review all open GRACE PRs | Batch GRACE Review |
| Re-review after updates | Incremental Review |

**Trigger phrases:**
- "Review PR https://github.com/juspay/hyperswitch-prism/pull/123"
- "Review PR #123 in hyperswitch-prism"
- "Review all open GRACE PRs"
- "Re-review PR #123 after the latest commits"

---

## Using Existing Skills

This skill provides the framework and checklists. For deep language-specific review, invoke the appropriate skill:

| Code Type | Invoke Skill |
|-----------|--------------|
| Rust core code | `/skill rust-pro` |
| TypeScript SDK | `/skill typescript-pro` |
| Python SDK | `/skill python-pro` |
| Java SDK | `/skill java-pro` |
| General code review | `/skill code-reviewer` |
| Security focus | `/skill security-audit` |

**How to combine:**
1. Use this skill to classify the PR and identify scenarios
2. For each language-specific file, invoke the appropriate language skill
3. Aggregate findings using the rubric in this skill

---

## Workflows

### 1. Full PR Review (Default)

**Purpose:** Review any PR in hyperswitch-prism.

**Steps:**

**Phase 0 - Load Configuration**
- Read system overview and rubric (below)
- Load scenario taxonomy and path rules
- Review output template format

**Phase 1 - Gather PR Context**
- Collect PR author, changed files list
- Get full unified diff
- Capture PR title/body for scope classification

**Phase 2 - Classify**
Determine:
- Primary and secondary scenarios
- Metadata scenarios (e.g., grace-generated-pr)
- Subagents and reviewer families to dispatch
- Companion files to check

**Phase 3 - Review**
For each matched scenario, execute checklists:
- Rust core files → Rust checklist + invoke `rust-pro` skill
- TypeScript SDK → TypeScript checklist + invoke `typescript-pro` skill
- Python SDK → Python checklist + invoke `python-pro` skill
- Java SDK → Java checklist + invoke `java-pro` skill

**Phase 4 - Aggregate**
- Deduplicate findings
- Normalize severities
- Produce final verdict using output template

**Phase 5 - Final Answer**
Must include:
- Verdict (approve/comment/request_changes)
- Classification
- Blocking/non-blocking findings
- Missing code companions
- Suggested fixes

---

### 2. GRACE PR Review

**Purpose:** PRs raised by `10xGRACE` need extra code-pattern scrutiny.

**Additional Step (Step 4): GRACE Code-Pattern Pass**
Check for:
- Copy-paste remnants from other connectors
- Scope drift (widened support without proper guards)
- Incomplete wiring (registration, transformer, test gaps)
- Brittle parsing/serialization
- Missing companion code updates

**Detection:** Author is `10xGRACE` OR branch matches `feat/grace-*`

---

### 3. Batch GRACE Review

**Purpose:** Review all open GRACE PRs in parallel.

**Process:**
1. List open PRs where author is `10xGRACE` or branch matches `feat/grace-*`
2. Run GRACE PR Review workflow on each
3. Aggregate batch results with per-PR verdicts

---

### 4. Incremental Review

**Purpose:** Re-verify only changes since last review.

**Delta-Only Approach:**
1. Gather files changed since last review
2. Re-classify only if scope changed (new files, scenario mix change)
3. Smart re-run:
   - Always re-run if blocker files changed
   - Always re-run `ci-config-security` if workflows/config changed
   - Always re-run `tests-docs` if tests/specs changed
4. Track: prior blockers fixed, remaining, new blockers introduced

---

## 13 Scenarios (Taxonomy)

| # | Scenario ID | Description | Path Triggers | Reviewer |
|---|-------------|-------------|---------------|----------|
| 1 | `connector-new-integration` | Adds new connector | `connectors/{new}/mod.rs`, `connectors.rs` | connector |
| 2 | `connector-flow-addition` | Adds flow to existing | `transformers.rs` flow methods | connector |
| 3 | `connector-payment-method-addition` | New payment method | Payment method specific files | connector |
| 4 | `connector-bugfix-webhook` | Bugfix, auth, webhook | Webhook handlers, auth modules | connector |
| 5 | `connector-shared-plumbing` | Registry, utils, macros | `connectors.rs`, `macros.rs` | connector |
| 6 | `core-flow-framework` | Shared types, traits, enums | `domain_types/`, `interfaces/` | core-flow |
| 7 | `proto-api-contract` | Protobuf contracts | `proto/*.proto`, `build.rs` | proto-api |
| 8 | `server-composite` | gRPC handlers, HTTP facade | Composite service code | server-composite |
| 9 | `sdk-ffi-codegen` | SDKs, FFI, bindgen | SDK generation, FFI boundary | sdk-ffi-codegen |
| 10 | `tests-specs-docs` | Tests, specs, docs | `test.rs`, `specs/`, `docs/` | tests-docs |
| 11 | `ci-config-security` | CI, config, secrets | `.github/`, workflow files | ci-config-security |
| 12 | `grace-tooling` | GRACE subproject | `grace/` directory changes | ci-config-security |
| 13 | `grace-generated-pr`* | GRACE automation | Author `10xGRACE` or `feat/grace-*` | grace-generated-pr |

*Metadata scenario - adds extra scrutiny

---

## Severity Rubric

### Levels

| Level | ID | Name | Merge Allowed | Examples |
|-------|-----|------|---------------|----------|
| Critical | S0 | critical-blocker | **NO** | Security exposure, payment correctness risk, weakened auth/webhook, API break |
| Major | S1 | major-blocker | **NO** | Production regression risk, incomplete implementation, missing companions/tests |
| Moderate | S2 | moderate-nonblocker | YES | Localized correctness with evidence, maintainability issue, low-risk gap |
| Minor | S3 | minor-nit | YES | Naming cleanup, wording, optional refactor |

### Hard Blockers (Always Request Changes)
- Any S0 finding
- Any S1 finding
- Unresolved safety question in high-risk area

### Decision Matrix

| Condition | Decision |
|-----------|----------|
| No S0/S1 findings, code safe | **approve** |
| Only S2/S3 findings remain | **comment** |
| Any hard blocker present | **request_changes** |
| Cannot verify safety | **request_changes** |
| PR too broad to review safely | **request_changes** + recommend split |

---

## Language-Specific Review

### Rust Core Code

**Invoke:** `/skill rust-pro` for deep analysis

**Key Areas to Check:**
- Ownership and borrowing patterns
- Trait implementation completeness
- Error handling (Result/Option, ? operator)
- Async/await and runtime usage
- Unsafe code blocks (if any)
- Lifetime annotations
- Macro hygiene

**Checklist:**
- [ ] No unwrap/expect in production paths without justification
- [ ] Proper error propagation with `?`
- [ ] Trait bounds are necessary and sufficient
- [ ] Lifetimes minimized and explicit
- [ ] Unsafe code has safety comments
- [ ] No blocking operations in async contexts
- [ ] Clone usage justified for large structs
- [ ] change_context() includes ResponseTransformationErrorContext with http_status_code and descriptive additional_context
- [ ] attempt_status mapping distinguishes between integration errors (pending) and connector-declared failures (failed)
- [ ] No Default::default() used for error context - always provide detailed diagnostic information (S1 if found)

### TypeScript SDK

**Invoke:** `/skill typescript-pro` for deep analysis

**Key Areas to Check:**
- Type definitions match API contracts
- Promise/async handling
- Null/undefined safety
- Interface vs type usage
- Export/public API surface

**Files:**
- `sdk/typescript/src/**/*.ts`
- `sdk/javascript/src/**/*.js`

**Checklist:**
- [ ] Types match protobuf/gRPC definitions
- [ ] Async functions handle errors properly
- [ ] No implicit any types
- [ ] Public API documented
- [ ] Generated files not manually edited

### Python SDK

**Invoke:** `/skill python-pro` for deep analysis

**Key Areas to Check:**
- Type hints completeness
- Async/await patterns (asyncio)
- Exception handling hierarchy
- Dataclass vs Pydantic models
- Package structure

**Files:**
- `sdk/python/src/**/*.py`

**Checklist:**
- [ ] Type hints on public functions
- [ ] Proper async/await usage
- [ ] Exceptions inherit from appropriate base
- [ ] Generated files not manually edited
- [ ] Poetry/pyproject.toml consistent

### Java SDK

**Invoke:** `/skill java-pro` for deep analysis

**Key Areas to Check:**
- POJO/Data class patterns
- Null safety (Optional usage)
- Exception handling
- Builder patterns
- Package organization

**Files:**
- `sdk/java/src/**/*.java`

**Checklist:**
- [ ] Classes follow Java naming conventions
- [ ] Null handling explicit
- [ ] Checked vs unchecked exceptions appropriate
- [ ] Builder patterns for complex objects
- [ ] Generated files not manually edited

---

## Base Checklist (Universal)

### File Coverage
- [ ] Every changed file reviewed
- [ ] Required companion files reviewed
- [ ] No file approved from title/summary alone

### Code Integrity
- [ ] No debug prints or dead code
- [ ] No TODO/FIXME without ticket reference
- [ ] No unwrap/expect/panic in production paths without justification
- [ ] No hand-edited generated files
- [ ] Error handling includes comprehensive context (http_status_code, descriptive messages) when using change_context() (ignore for stub implementations)
- [ ] attempt_status remains pending for integration errors; only set to failed when connector explicitly reports failure

### Code Correctness
- [ ] Inputs validated, outputs handled
- [ ] Error paths intentional with proper logging
- [ ] Backward compatibility preserved
- [ ] Idempotency and retries considered

### Companion Sync
- [ ] Registrations aligned (connector enum, router)
- [ ] Traits implemented or defaulted
- [ ] Tests match behavior changes
- [ ] Specs updated for contract changes

### SDK Cross-Language Consistency
- [ ] All three SDKs (TS, Python, Java) updated for contract changes
- [ ] Generated artifacts refreshed consistently
- [ ] FFI bindings match Rust implementation
- [ ] Client sanity tests pass

### Mixed PR Escalation Rules
- **3+ scenarios matched:** Recommend split
- **Proto + SDK/FFI:** Require regeneration review
- **Core-flow + Connector:** Assume blast radius risk
- **CI/Security + Production code:** Require coupling explanation
- **Generated files changed without source:** Flag manual edit/stale gen

---

## Scenario-Specific Checklists

### Connector New Integration

**Files to Check:**
- `crates/integrations/connector-integration/src/connectors/{name}/mod.rs`
- `crates/integrations/connector-integration/src/connectors.rs`
- `crates/integrations/connector-integration/src/default_implementations.rs`
- `crates/integrations/connector-integration/src/types.rs`
- `crates/types-traits/domain_types/src/connector_types.rs`
- `**/connectors/{name}/test.rs`

**Checklist:**
- [ ] New connector file follows transformer layout
- [ ] Registered in `connectors.rs`
- [ ] `default_implementations.rs` updated if needed
- [ ] `types.rs` updated for connector-specific types
- [ ] `ConnectorEnum` has variant
- [ ] Auth credentials, URLs properly configured
- [ ] Status mapping defined
- [ ] Error mapping complete
- [ ] Tests exist (`test.rs`)
- [ ] No copy-paste remnants from other connectors
- [ ] Provider names/endpoints correct

**Language Review:**
- [ ] Rust: `rust-pro` skill invoked for core connector code

### Connector Flow Addition

**Checklist:**
- [ ] `ConnectorIntegrationV2` flow implementation complete
- [ ] Request transformer handles all fields
- [ ] Response transformer parses all statuses
- [ ] Status mapping explicit (not catch-all)
- [ ] ID, amount, currency semantics preserved
- [ ] Prerequisite flows documented
- [ ] Flow-specific failures have explicit mapping
- [ ] Tests cover new flow
- [ ] No silent support claims for unimplemented methods
- [ ] Response transformer correctly maps attempt_status: pending for integration errors, failed only on explicit connector failure

**Language Review:**
- [ ] Rust: `rust-pro` skill for transformer logic

### Connector Bugfix/Webhook

**Checklist:**
- [ ] Bugfix scope matches PR description
- [ ] Webhook verification logic intact
- [ ] Auth signing not weakened
- [ ] Webhook parsing validates source
- [ ] Redirect handling correct
- [ ] Dispute/refund/sync logic sound
- [ ] No secrets in errors/logs
- [ ] Regression tests added
- [ ] Security-sensitive code not degraded

**Language Review:**
- [ ] Rust: `rust-pro` skill for security-critical code
- [ ] Security: `security-audit` skill for auth/webhook changes

### Core Flow Framework

**Files to Check:**
- `crates/types-traits/domain_types/src/connector_flow.rs`
- `crates/types-traits/interfaces/src/connector_types.rs`
- `crates/types-traits/domain_types/src/router_data.rs`
- `crates/common/common_enums/src/enums.rs`

**Checklist:**
- [ ] Flow markers and `FlowName` consistent
- [ ] Trait changes have downstream proof
- [ ] Enum semantics preserved or migration noted
- [ ] Shared request/response types backward compatible
- [ ] Helper changes tested across consumers
- [ ] Blast radius documented for connector changes
- [ ] No behavioral change hidden in refactor

**Language Review:**
- [ ] Rust: `rust-pro` skill for trait/enum changes

### Proto/API Contract

**Files to Check:**
- `crates/types-traits/grpc-api-types/proto/*.proto`
- `crates/types-traits/grpc-api-types/build.rs`
- `buf.yaml`, `buf.gen.yaml`

**Checklist:**
- [ ] Field numbers preserved
- [ ] Service names unchanged
- [ ] No field reuse or renumbering
- [ ] Removed fields have migration story
- [ ] Generated code regenerated and included
- [ ] SDK/FFI fallout coherent
- [ ] `build.rs` extern paths correct
- [ ] Serde attributes match intended types

**SDK Impact:**
- [ ] TypeScript SDK regenerated (`sdk/typescript/`)
- [ ] Python SDK regenerated (`sdk/python/`)
- [ ] Java SDK regenerated (`sdk/java/`)
- [ ] All SDKs reflect proto changes

### SDK/FFI Codegen

**Files to Check:**
- `sdk/Makefile`, `sdk/common.mk`
- `crates/ffi/ffi/src/bindings/_generated_*.rs`
- `crates/ffi/ffi/src/handlers/_generated_*.rs`
- `sdk/python/src/payments/_generated_*.py`
- `sdk/javascript/src/payments/_generated_*.ts`
- `sdk/java/src/**/*Generated*.java`
- `.github/workflows/sdk-client-sanity.yml`

**Checklist:**
- [ ] Generated artifacts refreshed and internally consistent
- [ ] FFI layer matches proto and server behavior
- [ ] All three SDKs reflect shared contract changes
- [ ] No manual edits to generated flow files
- [ ] Partial regeneration flagged across languages
- [ ] Packaging metadata coherent
- [ ] Client sanity tests pass

**Language Review:**
- [ ] TypeScript: `typescript-pro` skill for TS SDK
- [ ] Python: `python-pro` skill for Python SDK
- [ ] Java: `java-pro` skill for Java SDK

### GRACE Generated PR

**Extra Pattern Checks:**
- [ ] No copy-paste remnants from other connectors
- [ ] No scope drift in match arms/guards
- [ ] Complete wiring: registration, transformer, test, spec
- [ ] No brittle raw parsing (justified if present)
- [ ] No placeholder code in production paths
- [ ] Provider names/endpoints specific (not generic)
- [ ] Broadened support has explicit guards
- [ ] Tests/specs/registration align with claimed support

---

## Output Format Template

```markdown
## Verdict
- Decision: approve | comment | request_changes
- Risk: low | medium | high | critical
- Primary scenario: <scenario_id>
- Secondary scenarios: <list or none>
- Code summary: <one-line change description>

## Scope
- Files reviewed: <list all changed files>
- Areas reviewed: <reviewer families>
- Core code paths: <key functions/modules>
- Companion files: <tests/specs/registries/traits>
- Skills invoked: <rust-pro, typescript-pro, etc.>

## Blocking Code Findings
- [S0|S1] <title> - <why it matters> - <file:line>

## Non-Blocking Code Findings
- [S2|S3] <title> - <why it matters> - <file:line>

## Missing Code Companions
- <registration, test, spec, enum, trait, generated file>

## Suggested Code Fixes
- <concise code-level fix>

## Style Rules Applied
- Concrete file paths cited
- Code findings over praise
- No labels, approvals, CI status mentioned
- Evidence-backed concerns only
- Root-cause focused
```

---

## Quick Reference

### Severity Quick Lookup

| Finding Type | Severity |
|--------------|----------|
| Security exposure | S0 |
| Payment correctness risk | S0 |
| Weakened auth/webhook | S0 |
| API break without migration | S0 |
| Production regression likely | S1 |
| Incomplete implementation | S1 |
| Missing companion updates | S1 |
| Missing tests for behavior change | S1 |
| Error context uses `Default::default()` | S1 |
| Localized correctness concern | S2 |
| Maintainability issue | S2 |
| Low-risk test gap | S2 |
| Missing http_status_code in change_context when available | S2 |
| Missing additional_context in error transformation | S2 |
| Naming/wording cleanup | S3 |

### Scenario Detection Quick Lookup

| File Pattern | Scenario | Language Skill |
|--------------|----------|----------------|
| `connectors/{new}/` | connector-new-integration | rust-pro |
| `transformers.rs` | connector-flow-addition | rust-pro |
| `webhook/` or `auth/` | connector-bugfix-webhook | rust-pro + security-audit |
| `domain_types/` | core-flow-framework | rust-pro |
| `proto/*.proto` | proto-api-contract | - |
| `sdk/typescript/` | sdk-ffi-codegen | typescript-pro |
| `sdk/python/` | sdk-ffi-codegen | python-pro |
| `sdk/java/` | sdk-ffi-codegen | java-pro |
| `test.rs` | tests-specs-docs | - |
| `.github/workflows/` | ci-config-security | - |

---

## Example Usage

### Review Rust connector PR
```
"Review PR #123 in hyperswitch-prism"

Process:
1. Classify: connector-new-integration scenario
2. Run connector checklist
3. Invoke: /skill rust-pro for transformer code
4. Aggregate findings
5. Deliver verdict
```

### Review SDK PR
```
"Review PR #456 that updates the Python SDK"

Process:
1. Classify: sdk-ffi-codegen scenario
2. Run SDK checklist
3. Invoke: /skill python-pro for Python files
4. Verify TypeScript and Java SDKs also updated
5. Deliver verdict
```

### Review proto change affecting all SDKs
```
"Review PR #789 which changes the payment proto"

Process:
1. Classify: proto-api-contract + sdk-ffi-codegen
2. Run proto checklist
3. Invoke: /skill rust-pro for build.rs changes
4. Verify generated code in all SDKs
5. Invoke: /skill typescript-pro for TS SDK
6. Invoke: /skill python-pro for Python SDK
7. Invoke: /skill java-pro for Java SDK
8. Aggregate all findings
```

---

## Core Principles

1. **Read everything** — Never approve from title, summary, or snippets
2. **Classify first** — Route to matching scenario specialists
3. **Use language skills** — Invoke `rust-pro`, `typescript-pro`, `python-pro`, `java-pro` for deep analysis
4. **Companion files** — Check related files, not just changed ones
5. **Cross-SDK consistency** — All three SDKs must stay aligned
6. **Fail closed** — Block when safety cannot be verified

## Style Guidelines

- Cite concrete file paths (e.g., `src/connectors/stripe/mod.rs:45`)
- Prefer code findings over praise
- Do not mention labels, approvals, PR titles, CI status
- Never report vague concerns without evidence
- Merge duplicate findings into root-cause statements
- Document which skills were invoked for language-specific review
