---
name: continuous-learning
description: Continuous conversational learning protocol (CLP) skill. Persists user corrections and project conventions to .agents/learned_conventions.md to prevent repeating mistakes.
---

# Continuous Conversational Learning (`/continuous-learning`)

> **Philosophy**: *Mistakes happen once; repeating them is unacceptable. Absorb developer corrections immediately, record invariants to disk, and enforce them forever.*

This skill governs the Conversational Learning Protocol (CLP). It turns user corrections, preferred patterns, architecture rules, and repo idioms into persisted project invariants that survive across agent contexts, sub-agent invocations, and session restarts.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/continuous-learning-protocol.md](references/continuous-learning-protocol.md) | Signal detection, invariant extraction criteria, zero repeated mistakes. |
| **Reference** | [references/convention-persistence.md](references/convention-persistence.md) | File schema for `.agents/learned_conventions.md`, programmatic recording CLI. |
| **Utility** | [scripts/record_learning.py](scripts/record_learning.py) | CLI utility to append formatted invariants with timestamps and duplicate checks. |

---

## 2. The Continuous Learning Cycle

```mermaid
flowchart TD
    A["Developer Feedback or Correction"] --> B["1. Signal Detection & Invariant Extraction"]
    B --> C["2. Conflict Check against Existing Rules"]
    C --> D["3. Write to .agents/learned_conventions.md"]
    D --> E["4. Pre-Flight Verification on Every Future Task"]
    E --> F["Zero Repeated Mistakes & Constant Alignment"]
```

### 1.1 Detection Signals: When to Record Invariants
Trigger the learning protocol automatically whenever:
1. **Direct Correction**: The user corrects an implementation choice (e.g. *"Use Tailwind v4 instead of v3"*, *"Never use Axios, use native fetch"*).
2. **Architecture Enforcement**: The user clarifies an organizational rule (e.g. *"All models must reside in src/domain/models"*).
3. **Naming & Schema Conventions**: The user defines an entity convention (e.g. *"All table IDs must use ULID prefixes like usr_..."*).
4. **Environment Quirks**: A unique workaround is discovered during build or test execution (e.g. *"On macOS ARM64, invoke python3 with specific DYLD path"*).

---

## 2. Invariant Taxonomy & Schema

Every learned rule is stored in `.agents/learned_conventions.md` using strict semantic prefixes:

| Category Code | Domain | Scope & Example |
| :--- | :--- | :--- |
| `[UI-xxx]` | Design & Styling | Palette restrictions, typography scales, icon library preference. |
| `[ARCH-xxx]` | System Architecture | Layer boundaries, dependency inversion, package prohibitions. |
| `[API-xxx]` | API Contracts | Error payload envelope, idempotency headers, versioning schemes. |
| `[DATA-xxx]` | Persistence & DB | Migration tooling, soft delete policies, indexing rules. |
| `[SEC-xxx]` | Security & Auth | Token storage mechanisms, allowed JWT algorithms, CORS whitelist. |
| `[TOOL-xxx]` | Tooling & Build | Custom test runner flags, linter rules, compiler arguments. |

### Canonical Entry Format:
```markdown
- **[ARCH-004] (2026-10-25)**: Standardize all HTTP network calls on Node 18+ native `fetch`. Do not install `axios` or `request`.
```

---

## 3. Pre-Flight Enforcement Workflow

Before generating or modifying any code in the repository:
1. Read `.agents/learned_conventions.md` if present in the workspace root or parent directory.
2. Cross-reference the proposed solution against all recorded invariants.
3. If a conflict is detected between standard practices and a project-specific learned convention, the **project learned convention takes absolute precedence**.
4. Confirm compliance silently in the thought process before delivering the code.

---

## 4. Learning Recorder CLI

Record and query learned conventions automatically via script:

```bash
# Record an architectural convention
python3 skills/continuous-learning/scripts/record_learning.py --category ARCH --text "Standardize on native fetch; do not install axios"

# Record a UI convention
python3 skills/continuous-learning/scripts/record_learning.py --category UI --text "Use SF Pro font stack with -0.02em tracking for headings"

# List and audit all recorded conventions
python3 skills/continuous-learning/scripts/record_learning.py --list
```
