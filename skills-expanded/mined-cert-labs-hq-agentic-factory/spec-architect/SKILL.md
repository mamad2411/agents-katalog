# Skill: Spec Architect
**Description**: Validates the architectural intent and boundaries of a new feature before drafting the formal specification.
**Triggers**: "let's make the spec for", "create a spec for", "/spec"

## Instructions
When this skill is triggered, you MUST NOT write the full specification yet. Instead, provide a **Specification Intent Check** using this template:

### 🎯 Scope & Boundaries
*   What is the "Minimum Viable Logic" this spec aims to define?
*   **Out of Scope**: What will this spec explicitly *not* cover to prevent feature creep?

### 🔗 Integration & Data Flow
*   Which existing Slice IDs (from the Roadmap) does this spec depend on?
*   What data will this spec require from the `index.json` registry?

### 🛡️ The "Guard" Constraints (Security/QA)
*   What specific GitHub Actions (SAST/SCA) must this feature pass once implemented?
*   Are there any deterministic "Hard Rules" (e.g., OIDC, specific permissions) this spec must enforce?

### 💰 FinOps & Token Economics
*   **Complexity Rating**: Categorize based on the following mapping:
    *   **Low**: < 5,000 tokens (Single file refactor/JSON update).
    *   **Medium**: 5,000 - 15,000 tokens (New component/Logic flow).
    *   **High**: > 15,000 tokens (Full slice implementation/Major architectural change).
*   **Quota Constraint**: If Complexity is **High**, you MUST verify that `quota_governance.remaining` in `telemetry.json` is > 20,000 before proposing an implementation date or proceeding to the draft.
*   **Estimated Generation Cost**: How many tokens will it likely take to write the full Markdown spec based on context size?
*   **Implementation Overhead**: Does this spec introduce high-token-cost logic (e.g., recursive loops or heavy reasoning)?

**TERMINAL INSTRUCTION**: "Awaiting your architectural sign-off before I draft the formal Markdown specification."