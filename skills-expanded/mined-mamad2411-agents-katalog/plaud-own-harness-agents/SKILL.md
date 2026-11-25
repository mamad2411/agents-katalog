# HARNESS ENGINEERING SYSTEM — AGENTS.md
# Version 3.0

---

## PURPOSE

This harness implements a multi-role software engineering system designed to produce
production-ready code with maximum architectural integrity, security, maintainability, and
alignment with business objectives.

---

## HOW TO LOAD THIS HARNESS

This file is the INDEX. It does not contain full roles.
Each role lives in its own file to preserve the context window.

**Only load the active role at any given moment:**

| Phase | File to load |
|------|-----------------|
| New request / strategy | `roles/cto.md` |
| Planning / architecture | `roles/chief_architect.md` |
| Security review | `roles/security_architect.md` |
| Implementation | `roles/principal_engineer.md` |
| Testing and QA | `roles/qa_engineer.md` |
| Complexity audit | `roles/entropy_auditor.md` |
| Release review | `roles/release_governor.md` |

**Always load alongside the active role:**
- `project_context.md` — technical context of the project
- `conflict_resolution.md` — decision hierarchy

---

## CORE PRINCIPLES (inherited by all roles)

1. **Customer Value First** — the customer matters more than technical elegance
2. **Security By Default** — never as an afterthought
3. **Simplicity Over Complexity** — the simplest solution that works
4. **Reuse Before Creation** — look before creating
5. **Architecture Before Implementation** — plan before coding
6. **Verification Before Approval** — test before approving
7. **Eliminate Before Adding** — remove before adding
8. **Long-Term Maintainability Over Short-Term Speed** — the future matters

---

## GOLDEN RULE

Before creating new code, evaluate in order:

```
1. Can it be solved with configuration?
2. Can it be solved by reusing existing code?
3. Can it be solved by refactoring existing code?
4. → Only then: create new code
```

New code is the last resort.

---

## AVAILABLE WORKFLOWS

| Workflow | File | When to use |
|----------|---------|-------------|
| New feature | `workflows/feature_workflow.md` | New functionality |
| Hotfix | `workflows/hotfix_workflow.md` | Critical bug in production |
| Refactor | `workflows/refactor_workflow.md` | Technical debt / cleanup |

---

## PERSISTENT MEMORY STRUCTURE

```
.harness/
├── AGENTS.md                  ← this file (index)
├── project_context.md         ← technical context of the project
├── conflict_resolution.md     ← veto and decision hierarchy
│
├── roles/                     ← one file per role
├── workflows/                 ← one file per workflow type
│
├── architecture/
│   ├── vision.md
│   ├── tech_stack.md
│   ├── coding_standards.md
│   ├── api_conventions.md
│   ├── database_conventions.md
│   └── decision_log.md
│
├── contracts/
│   └── feature_contract.md
│
├── adrs/
│   └── ADR-XXX.md
│
└── audits/
    ├── security_report.md
    ├── entropy_report.md
    └── release_report.md
```

---

## FINAL RULE

The goal is not to generate the largest amount of code.
The goal is to create the simplest, most secure, and maintainable solution
that satisfies the business objective.
