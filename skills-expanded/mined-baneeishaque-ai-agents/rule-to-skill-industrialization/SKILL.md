---
name: rule-to-skill-industrialization
description: Meta-automation protocol for transforming redundant rule files into
  high-fidelity AI Agent Skills with 100% industrial fidelity.
category: Meta-Automation
---

# Rule-to-Skill Industrialization Skill (v1)

This skill provides the mandatory industrial protocol for transforming flat, redundant rules into authoritative,
high-fidelity AI Agent Skills. It is the definitive process for achieving a Single Source of Truth (SSOT) across
the repository.

***

## 0. Rationale — Why Skills, Not Rules

Rules and instruction files are **vendor-specific**: each agent runtime
defines its own location and format
(`.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `AGENTS.md`,
`CLAUDE.md`, `.windsurfrules`, etc.). A rule authored for one vendor
is invisible to every other.

The **Agent Skills** standard ([agentskills.io](https://agentskills.io),
Anthropic-originated, multi-vendor adopted) is the open, portable
alternative: a single `SKILL.md` with YAML frontmatter is consumable
by every conformant runtime. Industrializing a rule into a skill is
therefore not cosmetic — it is the migration from a vendor-locked
artifact to a portable one.

This is the **adoption** half of the "why". The **fidelity** half
(zero data loss, traceability matrix) is covered in §1–§3 below. The
**determinism** half — pushing deterministic steps out of prose and
into scripts — is covered by
[`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md)
and MUST be applied during §2.6 of this skill.

***

## 1. Preparation: The Fidelity Scan

Before beginning the transformation, the agent MUST perform a surgical audit of the source rule to prevent data loss.

1. **Mandate Extraction**: Identify every technical mandate, command payload, and safety guardrail in the source rule.
2. **Anti-Loss Validation**: Create a "Traceability Matrix" (Mapping) to ensure every source mandate is tracked to a
   specific section in the target Skill.
3. **Summarization Block**: **Summarization is STRICTLY FORBIDDEN**. Every technical detail must be preserved with
   literal fidelity or enhanced with additional context.

***

## 2. Phase-by-Phase Execution

### 2.1 Phase 1: Mapping & Gap Analysis

- **Audit**: Compare the source rule against the target skill (if it exists).
- **Gap Identification**: Explicitly document what is missing from the skill that exists in the rule (and vice-versa).
- **Conclusion**: Document the "Final Verdict" on what needs to be blended to reach 100% coverage.

### 2.2 Phase 2: High-Fidelity Blending

- **Integration**: Blend all missing pieces into the `SKILL.md`.
- **Greater-Than-Before**: The resulting skill document MUST be more detailed and industrially hardened than the
  original rule.
- **Portability Hardening**: Apply Section 4.2.8 (Hosted VCS Links) for any cross-repository references.

### 2.3 Phase 3: SSOT Promotion & Re-linking

- **Decommissioning**: Once 100% coverage is verified, the source rule file is officially **REDEEMED REDUNDANT**.
- **Global Refactoring**: Perform a search-and-replace across the repository to update all links pointing to the
  old rule file.
- **Hosted VCS Protocol**: If the link is in a submodule and the target is in the parent, you MUST use the
  **Hosted VCS Permanent Link (SHA)** protocol as defined in
  **[markdown-generation-rules.md Section 4.2.8](../../../ai-agent-rules/markdown-generation-rules.md#428-cross-repository--submodule-isolation-links)**.

### 2.4 Phase 4: Tier Decomposition (Script vs Prose)

Before declaring the skill final, the agent MUST apply
[`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md)
to the freshly blended `SKILL.md`:

1. Walk every step of every procedure.
2. Classify each step as **Tier A** (deterministic — parse, transform,
   validate, file-mutate) or **Tier C** (judgement, branching, gates).
3. Extract every Tier-A step into an executable script under the new
   skill's `scripts/` directory. Prose retains only Tier C plus a
   one-line invocation example.

A rule industrialized into a skill that still contains long bash
recipes or Python heredocs in its prose has only completed half the
migration. The vendor-lock is gone; the determinism gap remains.

### 2.5 Phase 5: CI/CD & Output Integrity

- **Output Restriction**: The agent is **BLOCKED** from manually editing auto-generated files (e.g., `README.md`,
  `agent-rules.md`).
- **Template SSOT**: All structural changes to generated indices MUST be made in the `templates/*.template` files.
- **Automation Reliance**: Allow the CI/CD pipeline/sync scripts to update indices automatically once the source
  rule is deleted.

### 2.6 Portability & Depth Audit

Before the final commit, the agent MUST perform a **Portability & Redaction Audit** as defined in the
**[Skill Factory Section 3](../skill-factory/SKILL.md#3-post-drafting-checklist)**. This ensures all documentation
is functionally independent from ephemeral session storage and correctly path-referenced.

***

## 3. Rule Decommissioning Mandate

The source rule file MUST be deleted only after the following conditions are met:

1. 100% technical mandate coverage in the Skill.
2. All static (non-generated) references correctly refactored.
3. A final `markdownlint-cli2` audit passes with **ZERO** errors.

***

## 4. Environment & Dependencies

- **Verification Tool**: `markdownlint-cli2` (Mandatory for compliance checks).
- **Search Tool**: `grep` or `ripgrep` (Mandatory for global reference audit).
- **VCS Tool**: `git` (Mandatory for commit-SHA retrieval).

***

## 5. Traceability & Pedagogical Audit

This skill was established to codify the resolution of the `git_history_refinement` industrialization.

- **Originating Plan**: `implementation_plan.md` (2026-03-29).
- **Industrial Resolution Trace**: [Walkthrough](./docs/walkthrough_init.md).
- **Rule Mapping Documentation**: [Traceability Matrix](./docs/history_refinement_rule_mapping.md).
