---
name: "artifact-first-workflow"
description: "Claude Code Artifact-First Workflow: single source of truth specifications. Draft, version, and edit specifications (SPEC.md) first, treating the actual codebase implementation as a compilable/generated output"
---

# Artifact-First Workflow — Specification-Driven Code Generation

## When to activate
- Starting a new feature, module, or database migration.
- Designing multi-file integrations, workflows, or microservices.
- When requirements are complex, ambiguous, or likely to change.
- Striving to enforce structural architectural alignment across multiple developers/agents.

## When NOT to use
- Simple bug fixes, minor typography edits, or updating isolated variables.
- One-off shell scripts, scratchpad files, or quick debugging spikes.
- Flat documentation edits.

## Instructions

The Artifact-First Workflow reverses the traditional development model: the specification document (`SPEC.md` or a dedicated spec file under `.claude/specs/`) is the single source of truth, and the actual codebase is treated as a derivative output compiled from it.

```
       ┌───────────────────┐
       │   1. Spec File    │ ◄─────── Requirement Changes
       │     (SPEC.md)     │          (Edited by human/AI)
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ 2. Implementation │ ◄─────── Refactored / Generated
       │    (Code Files)   │          (Targeted by compilation)
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │  3. Verification  │
       │   (Tests & CI)    │
       └───────────────────┘
```

### 1. Spec Artifact Structure
Every spec artifact must live in `.claude/specs/[feature-name].md` (or `SPEC.md` for single-purpose projects) and follow this template:

```markdown
# Spec: [Feature Name]
**Version:** 1.0.0
**Last Updated:** 2026-06-17
**Status:** [Draft | Approved | Deprecated]

## 1. Goal
- [Measurable high-level business objective]

## 2. Architecture & Data Flow
- [Flow diagrams or structural descriptions]

## 3. Interface Design
- [API signatures, components, props, or database schema]

## 4. Invariants & Guardrails
- [Logical rules that must NEVER be violated under any circumstances]

## 5. Implementation Files
- [List of paths to files containing the concrete code]

## 6. Verification Criteria
- [Tested scenarios, input/output values, and execution steps]
```

### 2. The Development Loop

1.  **Drafting the Spec:** First, edit or create the Spec file. Describe *what* needs to be done, including schema, interfaces, invariants, and tests.
2.  **User Review & Approval:** Present the Spec to the user. Do not write a single line of code until the Spec is approved.
3.  **Code Compilation:** Read the approved Spec and generate or edit the target implementation files. Add a spec reference header to every source file:
    *   JS/TS/Go: `// Spec-Ref: .claude/specs/my-feature.md#v1.0.0`
    *   Python: `# Spec-Ref: .claude/specs/my-feature.md#v1.0.0`
    *   CSS/HTML: `/* Spec-Ref: .claude/specs/my-feature.md#v1.0.0 */`
4.  **Verification:** Run the tests matching the verification criteria.
5.  **Refactoring Loop:** If tests fail due to coding errors, fix the code. If tests reveal a design flaw or missing requirement, **re-edit the Spec first**, get approval, and then re-generate the code.

### 3. Benefits & Anti-Patterns

*   **Benefits:** Reduces drift, prevents hallucinated features, maintains clean architectural decisions, and simplifies complex handoffs between sessions.
*   **Anti-Patterns:**
    *   *Direct Hacking:* Modifying the code files directly without updating the Spec first.
    *   *Vague Specs:* Writing "implement user authentication" without listing the actual API endpoints or database fields.
    *   *Outdated Spec:* Code and spec versions getting out of sync.

---

## Example

**Implementing a Token Vault Service using Artifact-First Workflow:**

### Step 1: Spec Created (`.claude/specs/token-vault.md`)
```markdown
# Spec: Token Vault
**Version:** 1.1.0

## 3. Interface Design
```typescript
interface TokenVault {
  saveToken(id: string, token: string): Promise<void>;
  getToken(id: string): Promise<string | null>;
}
```

## 4. Invariants
- Tokens must be encrypted using AES-256-GCM before database insertion.
- Raw unencrypted tokens must NEVER be logged to stdout or file logs.
```

### Step 2: User Approves
User: "Looks good. Implement it."

### Step 3: Code Compilation (`src/services/vault.ts`)
```typescript
// Spec-Ref: .claude/specs/token-vault.md#v1.1.0
import crypto from 'crypto';

export class CryptVault implements TokenVault {
  // Implementation details following the spec invariants...
}
```
If requirements change (e.g., adding token expiry), the `.claude/specs/token-vault.md` is updated to `v1.2.0` first, then `src/services/vault.ts` is regenerated and the header tag is updated.
