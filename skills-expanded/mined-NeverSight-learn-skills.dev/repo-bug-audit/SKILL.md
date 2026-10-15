---
name: repo-bug-audit
description: Use when an agent needs repository-level Bug audits, static-analysis Bug discovery, architecture/security/reliability risk review, cross-repo relationship mapping, false-positive triage, deduplication, incremental/resume audits, evidence-backed Bug records, reusable repo knowledge, or fix-ready Bug audit outputs.
---

# Repo Bug Audit

IRON LAW: Do not submit a Bug unless code evidence, trigger path, realistic failure mode, and impact are all explicit.

## Purpose

Find evidence-backed Bugs and architecture risk signals across one or more repositories, then package the results so developers or later Agents can review, reproduce, triage, and fix them safely.

This skill is review-first. Do not patch code unless the user explicitly asks for fixes after the analysis.

## Operating Rules

- Treat findings as static-analysis results until runtime validation proves otherwise.
- Prefer fewer real Bugs over hundreds of weak claims; keep weak leads in `work/candidates/`, not submitted findings.
- Prioritize infra-stability risks: data integrity, recovery, availability, resource leakage, storage/network performance, control-plane safety, security boundaries, and cross-system consistency.
- Use Deep Discussion Mode when the user explicitly asks for `$brainstorming`, when scope/output/risk definitions are still unstable, or when evolving this skill itself.
- Skip Deep Discussion Mode when the user asks for full automatic execution; apply the default workflow and keep progress moving.
- Treat related skills as optional accelerators, not hard dependencies; encourage installation only when they materially improve the current task.
- If a recommended skill is missing, continue by default. Ask before installing anything, and never interrupt explicitly automatic analysis runs for installation.
- Infer safe defaults first. Ask the user only when a missing answer changes safety, scope, or final package semantics.
- Do not infer analyst or author identity from OS username, Git config, directory owner, or model identity; use a provided value or mark it missing.
- In automatic mode, record assumptions in `submit/quality/submission-scope.md` instead of asking.
- Use Chinese for deliverables by default when the user is Chinese. Keep wording natural and developer-facing; avoid meta, self-referential, inflated, or AI-flavored language.
- Keep the skill itself reusable and neutral; do not hardcode real project names, company names, personal names, or analyst identifiers in instructions or examples.
- Do not include SLA fields in Bug records unless the user asks for process management data.
- Use Markdown files with embedded metadata; do not create separate YAML files for individual Bugs.
- Never delete or modify files outside the requested working/output directory unless explicitly asked.

## Deep Discussion Mode

Use this mode before scanning when analysis intent needs design, not just execution.

Do not enter this mode just because a repository group is large. Enter it only when a decision cannot be safely inferred and materially changes scope, risk classification, package format, or user-facing commitments.

Trigger it for:

- User mentions `$brainstorming` or asks to “先思考/先讨论/设计流程”.
- The target includes many repositories, unknown ownership, unclear priorities, or multiple possible output formats.
- The user wants to refine P1-P4 definitions, confidence rules, architecture review style, security scope, package format, image wording, or developer handoff style.
- The task is to improve this Skill or its references/scripts.

In this mode:

- Read `references/deep-discussion.md`.
- If the installed `brainstorming` skill is available, use it to discuss scope, tradeoffs, and deliverable design.
- Keep discussion concrete: produce an analysis charter, not an open-ended brainstorm.
- Ask at most one substantial question at a time unless the user asked for fully automatic execution.
- After the user approves the charter, return to the Workflow Checklist.

## Interaction Policy

- Start work with safe assumptions instead of asking formatting or naming questions.
- Ask at most one question when the answer materially affects safety, target scope, destructive operations, or final package semantics.
- Never ask whether to continue after each phase unless the user requested checkpoints.
- Keep progress updates to phase boundaries or major assumption changes; do not report every candidate Bug.
- Keep optional skill installation suggestions short, one-time, and limited to the most relevant three skills.
- Do not expose `work/` scratch content unless it affects a user decision or the user asks for candidates.
- In automatic mode, do not pause for optional skills, package style choices, image choices, or candidate triage preferences.

## Workflow Checklist

1. **Set scope ⚠️ REQUIRED**
   - Identify target repositories, reference repositories, branch context, output root, provided analyst, analysis date, and package audience.
   - Record audit metadata and repository version evidence when available; use `references/metadata.md`.
   - If the user gives no output root, create a descriptive lowercase workspace under the repo group, with `submit/` for final files and `work/` for temporary artifacts.
   - If the output root already exists or the user asks to continue/deepen/review, read `references/resume-audit.md` before changing findings.

2. **Initialize workspace ⛔ BLOCKING**
   - Run `scripts/init_bug_workspace.py` through Python explicitly to create the output skeleton.
   - Read `references/package-output.md` for directory and packaging conventions.

3. **Build minimal knowledge map ⚠️ REQUIRED**
   - Inventory languages, frameworks, entry points, largest files/functions, external dependencies, background jobs, data stores, and risky integration points.
   - Use `references/language-ecosystems.md` to identify build metadata, framework entry points, and evidence-backed verification command sources.
   - Build enough repo relationship and risk-path knowledge to choose high-risk paths; do not wait for a complete knowledge base before hunting Bugs.
   - Use `references/knowledge-base.md` to separate minimal discovery knowledge from final submitted knowledge.
   - For detailed mapping, use `acquire-codebase-knowledge` if available.

4. **Hunt candidates by risk lens ⚠️ REQUIRED**
   - Use `references/risk-taxonomy.md` for categories, P1-P4 definitions, and confidence rules.
   - Use `references/domain-profiles.md` to choose the primary repository lens.
   - Use `references/security-static-analysis.md` for security-specific checks and tool ideas.
   - Use `references/architecture-review.md` for architecture risk signals.
   - Use `references/candidate-triage.md` for weak leads that should not enter submitted findings yet.

5. **Verify before submitting ⛔ BLOCKING**
   - For each candidate, prove code evidence, trigger path, impact, affected resource, and realistic failure mode.
   - Use `references/deduplication.md` before creating or splitting a Bug.
   - Lower confidence or move to `work/candidates/` if evidence depends on unverified assumptions.
   - Use `systematic-debugging` style reasoning: root cause first, no speculative fixes.

6. **Write Bug records ⚠️ REQUIRED**
   - Use `references/bug-schema.md` for the Markdown metadata and QA-style sections.
   - Use `references/writing-style.md` to keep wording natural and submission-ready.
   - Include priority, confidence, category, issue family, infra domains, fix risk, evidence, static reproduction path, expected behavior, actual behavior, fix boundary, fix suggestion, suggested verification commands, and validation checks.
   - Sort and name files as `P1-BUG-0001-short-description.md`.
   - On continuation runs, keep existing IDs stable and continue from the current maximum `BUG-xxxx`.

7. **Consolidate knowledge and architecture risk ⚠️ REQUIRED**
   - Update `submit/knowledge/` after each evidence-backed Bug batch; final repo knowledge should be complete enough for another Agent to continue without rescanning basics.
   - Do this for multi-repo analysis, repeated issue families, cross-system risk paths, or explicit architecture-review requests.
   - For small single-repo scans with few findings, summarize architecture signals in README instead of creating a large review.
   - Use `references/knowledge-base.md` to check final knowledge completeness.
   - Write `knowledge/architecture-design-review.md` from a discovery perspective.
   - 将“用例、适配器、Saga/Outbox、状态对账”等架构信号写成风险发现，不写成命令或原则。

8. **Generate indexes, validate, and evaluate ⛔ BLOCKING**
   - Run `scripts/generate_bug_index.py`.
   - Run `scripts/validate_bug_package.py`.
   - For final handoff packages in large or multi-repo audits, run `scripts/validate_bug_package.py --require-knowledge --require-image` when `audit-overview.png` is expected.
   - Read `references/evaluation.md`.
   - Evaluate all P1/P2 Bugs; for large packages, also sample each issue family and risk domain.
   - Record material downgrades, removals, merges, priority changes, or weak areas in `quality/submission-scope.md`.
   - Fix missing metadata, stale counts, oversize images, old terminology, duplicate content, weak evidence, or priority inflation.

9. **Package (conditional)**
   - Add `README.md`, indexes, knowledge docs, quality scope, standards, and optional `audit-overview.png` under `submit/`.
   - If creating `audit-overview.png`, use `references/audit-overview-image.md` for content, layout, color, metadata, and wording constraints.
   - Prefer HTML/CSS screenshot for dense text and exact numbers; native image generation is allowed after visual and data consistency review.
   - For HTML/CSS overview images, verify both the exported PNG and a constrained browser preview; avoid long vertical canvases, stale browser tabs, scrolling screenshots, and fixed canvases that crop in common viewports.
   - Apply `references/writing-style.md` to README, knowledge docs, Bug records, and image text.
   - Keep zip packages small; compress images and avoid unused large assets.

## Pre-Delivery Checklist

- `scripts/validate_bug_package.py` reports zero errors.
- `indexes/findings.generated.md` and `indexes/findings.generated.json` are current.
- Every submitted Bug has P1-P4 priority, high/medium/low confidence, `status=open`, and `source=static-analysis`.
- Every submitted Bug has code evidence, static reproduction path, false-positive review, fix boundary, fix suggestion, suggested verification commands, and validation standard.
- P1/P2 Bugs pass `references/evaluation.md` priority and evidence gates.
- Large packages have issue-family and risk-domain samples checked through `references/evaluation.md`.
- `work/candidates/` contains weak leads instead of mixing them into submitted findings.
- Candidate notes follow the lightweight format in `references/candidate-triage.md`.
- Duplicate Bugs have been merged or moved to `work/candidates/`.
- `work/` is excluded from the final zip/package.
- Final `submit/knowledge/` meets `references/knowledge-base.md`; remove empty or repetitive optional files before packaging.
- For large or multi-repo packages, `scripts/validate_bug_package.py --require-knowledge` passes.
- If `audit-overview.png` is part of the package, image content follows `references/audit-overview-image.md`.
- If `audit-overview.html` is used to create the image, a common browser viewport can show the whole artboard without clipping, and the final PNG is visually reviewed for compression, overlap, stale layout, and accidental empty space.
- README counts match generated indexes.
- `quality/repository-versions.md` records branch, commit hash, and dirty status when available; missing version evidence is marked rather than guessed.
- Package text avoids banned/meta wording and project-specific residue.
- Package text has no process explanation, self-reference, vague summary claims, or AI-flavored phrasing.
- Images are compressed and no unused large assets remain.

## Tooling Guidance

- Use `rg` / `rg --files` for searches when available.
- Read `references/cross-platform.md` before running shell commands on Windows, Linux, macOS, or when a suggested command fails.
- Run bundled scripts through Python explicitly; do not rely on Unix executable bits or shebang behavior.
- Use Semgrep, CodeQL, dependency scanners, secret scanners, or language-native linters when available, but never submit raw tool output without human triage.
- Use multiple passes: broad pattern search, module-level tracing, cross-repo call-chain review, then false-positive pass.
- For large repo groups, analyze by domain: compute, storage, network, deployment, identity, billing, monitoring, UI/API.

## Related Skills and References

- Read `references/related-skills.md` when deciding whether to combine this skill with runtime or public companion skills.
- Read `references/agent-compatibility.md` when packaging, sharing, or adapting this skill for another Agent Skills-compatible client.
- Read only the reference files needed for the current task; keep context small.

## Bundled Resources

- `scripts/init_bug_workspace.py` — create output directories and baseline docs.
- `scripts/generate_bug_index.py` — build Markdown/JSON indexes from Bug records.
- `scripts/validate_bug_package.py` — verify package structure, metadata, terminology, and image sizes.
- `references/workflow.md` — full multi-pass workflow.
- `references/deep-discussion.md` — analysis charter and brainstorming prompts.
- `references/resume-audit.md` — continue an existing audit, keep IDs stable, and record downgrade/removal reasons.
- `references/evaluation.md` — Bug-level, package-level, depth, priority, and skill-regression evaluation gates.
- `references/metadata.md` — audit metadata and repository version evidence standard.
- `references/knowledge-base.md` — minimal discovery map and final reusable repo knowledge standard.
- `references/bug-schema.md` — Bug record schema and example.
- `references/risk-taxonomy.md` — priorities, confidence, categories, and sorting.
- `references/domain-profiles.md` — domain-specific audit lenses for infra, backend, frontend, SDK, mobile, and generic repositories.
- `references/language-ecosystems.md` — language/build-system discovery, entry-point hints, verification command evidence, and language-specific false-positive checks.
- `references/candidate-triage.md` — candidate lead format and promotion rules.
- `references/deduplication.md` — merge/split rules for repeated findings.
- `references/architecture-review.md` — architecture-risk analysis vocabulary.
- `references/security-static-analysis.md` — security checks and scanner workflow.
- `references/writing-style.md` — natural developer-facing wording rules and banned AI-flavored phrases.
- `references/package-output.md` — final package structure and README/image conventions.
- `references/audit-overview-image.md` — `audit-overview.png` content, layout, color, and metadata rules.
- `references/cross-platform.md` — Windows/Linux/macOS command, Python, path, and archive guidance.
- `references/related-skills.md` — optional companion skills, public locators, `npx -y skills` commands, and audit lenses.
- `references/agent-compatibility.md` — installation boundary, portability rules, and cross-agent behavior.
