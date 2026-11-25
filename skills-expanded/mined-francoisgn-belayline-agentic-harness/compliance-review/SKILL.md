---
name: compliance-review
description: Runs, on the current diff, the compliance reviewers declared in .harness/config.json whose scope is touched (the harness's built-in agents gdpr, eu-ai-act, nis2, iso27001, soc2, tisax, pci, hds; the company's own agents; or project specs applied by the generic reviewer), in parallel, and consolidates their verdicts for the PR. Use before "Ready for review" in a project subject to a compliance framework.
argument-hint: "[comma-separated ids, default: config] [base]"
---

# Compliance review

Reference: `.harness/docs/COMPLIANCE.md`.

1. **Plan**: `python3 .harness/scripts/compliance-plan.py --base origin/<base>` (base: argument, otherwise
   `integration_branch`). It resolves `compliance` in `.harness/config.json`: a **built-in** agent, a **project** agent
   (the company has its own), or a project **spec** applied by `compliance-reviewer`. Exit code 1 → show the errors to
   the operator and stop (the config must be fixed). Restrict to the ids in `$ARGUMENTS` if it names any; add those
   required by a `compliance: <id>` label on the linked issues. None → "no compliance framework enabled", stop.
2. **Scope**: `out of scope` (configured paths and keywords not touched) → `OUT OF SCOPE` without launching;
   `to assess` → read the "When to step in" section of the agent or the spec and decide.
3. **Launch in parallel** the relevant subagents (`compliance-<id>`), named `<project>.<orc>.conf-<id>.<target>`
   (ORCHESTRATION §7; description `conf-<id> <target> — compliance`); in `spec` mode, the `compliance-reviewer` agent
   gets `Spec: <file>` at the top of its prompt. Each one receives: the diff, the head (SHA), the linked spec,
   `ESSENTIALS.md`. Never the author's conclusions. They are read-only.
4. **Consolidate** in a table `Framework | Verdict | Open findings | To be confirmed by` and add the "Compliance"
   section to the PR. A security flaw: no public detail.
5. High / Medium gaps: fix in one commit then relaunch only the agents concerned, or open a `compliance: <id>` issue
   for the owner's decision (accepted risk = ADR).
