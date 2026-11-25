---
name: inline-doc-governance
description: Govern inline documentation coverage and comment quality in repo-owned source files. Use when Codex needs to audit or fix file headers, type docs, function or method contract docs, non-obvious inline comments, generated-file exclusions, or repo documentation rules for TypeScript, JavaScript, and Swift projects, including setting up a reusable docs/rules policy in a project-agnostic way.
---

# Inline Doc Governance

## Overview

Use this skill to keep documentation close to the code it explains without creating low-signal comment noise. It combines a deterministic audit for coverage checks with a judgment-based review for contracts, side effects, and "why" comments.

The default posture is repo-agnostic: discover local rules first, skip generated and vendor-owned files, and adapt strictness to the project instead of imposing a universal comment quota.

## Default Recommendation

Prefer this baseline for new repos:

- Require file headers for repo-owned source files.
- Require docs for exported, public, package-visible, cross-boundary, or otherwise important types.
- Require function and method contract docs only for public surfaces, cross-module seams, services, stores, adapters, coordinators, resolvers, and side-effectful operations.
- Add inline comments only when they explain a decision the code does not make obvious.
- Use strict "all types need docs" mode only when the repo has adopted that rule.

If a repo already has stronger rules, follow the repo. If the repo has no rules, propose the baseline and explain the strictness options before making broad edits.

## Trigger Checklist

Use this skill when any of these are true:

- the user asks to audit or improve comment coverage
- the user asks to set up repo rules for inline docs or code comments
- source files need file headers, type docs, or public API docs
- comments are stale, vague, tutorial-style, or restating code
- generated-file exclusions need to be made explicit
- a PR review asks for more documentation around contracts, side effects, or boundary decisions
- a repo is adopting a durable docs/rules policy for comments and inline docs

Skip this skill for prose-only docs work that does not affect code comments, or for one-line code changes where no public surface, boundary, or non-obvious behavior changes.

## Workflow

### 1. Discover local rules

Before auditing or writing comments, inspect the repo for existing guidance:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or similar agent instructions
- `docs/rules/`, `CONTRIBUTING.md`, `README.md`, package docs, and architecture docs
- boundary manifests, module ownership docs, or public API guidance
- generated-file rules in codegen docs, lint config, ignore files, or package scripts
- language and validation commands from package manifests, Makefiles, CI, or local docs

State what you found and what rule set you will apply. If there are multiple valid strictness levels, recommend one explicitly.

### 2. Choose the policy strictness

Use one of these modes:

- `public` - file headers plus docs for exported, public, package-visible, or cross-boundary types. This is the recommended default.
- `all` - file headers plus docs for every type declaration. Use only when the repo already prefers high inline-doc coverage.
- `none` - file headers only. Use for early adoption or when type-doc coverage would be too noisy.

For new repo setup, use [comment-doc-policy-template.md](references/comment-doc-policy-template.md) as the starting policy and adapt it to the repo's languages and validation commands.

### 3. Run the deterministic audit

Run the audit script from the target repo root or against selected paths:

```bash
python3 path/to/inline-doc-governance/scripts/audit_inline_docs.py --type-doc-policy public .
```

Strict mode:

```bash
python3 path/to/inline-doc-governance/scripts/audit_inline_docs.py --type-doc-policy all src packages/app/src
```

Use `--fix` only for mechanical cleanup, such as moving an existing doc above decorators or attributes. It does not invent missing documentation text:

```bash
python3 path/to/inline-doc-governance/scripts/audit_inline_docs.py --type-doc-policy public --fix src
```

The script enforces only deterministic checks:

- supported repo-owned source files have a top-of-file header that is not just a tool directive
- selected type declarations have docs immediately above the declaration or decorators/attributes
- generated, vendor-owned, build-output, and test files are skipped by default

If the script flags generated or third-party code, update the exclusion rules before editing that file.

### 4. Fix hard failures first

Resolve deterministic failures before adding body comments:

- add or strengthen file headers before imports
- add type docs immediately above the declaration, decorators, or attributes
- move misplaced docs above decorators or attributes when needed
- keep comments short and specific

Do not edit generated files or files with generated headers. If a generated file needs different output, change the source or generator.

### 5. Do the semantic pass

Read only the relevant language reference when needed:

- TypeScript and JavaScript: [typescript.md](references/typescript.md)
- Swift: [swift.md](references/swift.md)
- Audit loop: [audit-and-fix.md](references/audit-and-fix.md)

Look for missing docs the script cannot prove:

- public or exported functions and methods missing contract docs
- cross-module adapters, stores, services, resolvers, coordinators, and remote sources with weak docs
- parameters or return values whose meaning is not obvious from the type
- side effects such as network I/O, persistence, file writes, logging, mutation, caching, retries, or task scheduling
- boundary, fallback, timeout, ordering, normalization, compatibility, or provider-quirk decisions without a local why-comment

Skip comments that restate syntax. Prefer a better name or smaller helper over a comment when that fully explains the code.

### 6. Set up repo rules when requested

When the user asks to govern documentation coverage or set rules for a repo:

1. Discover the repo's docs/rules convention.
2. Propose where the durable rule should live.
3. Adapt [comment-doc-policy-template.md](references/comment-doc-policy-template.md).
4. Link the new rule from agent guidance only when the repo already uses a central guidance file.
5. Add the audit command to the repo's validation guidance when it is practical for contributors to run.
6. Run the narrowest validation command that proves the policy and references are valid.

Do not create repo docs just to satisfy this skill. Add durable policy only when it will guide future contributors.

## Comment Quality Rules

- Explain why, contract, ownership, side effects, edge cases, or tradeoffs.
- Do not narrate the code.
- Prefer plain language and active voice.
- Keep comments close to the code they describe.
- Keep temporary comments traceable with an owner, issue, expiry, or removal condition.
- Reference constants by name instead of duplicating values that may drift.
- Date or version-gate workaround comments when the workaround is expected to expire.
- Remove stale comments while editing the code they describe.

## Comment Sync Rules

When changing code, keep nearby comments in the same edit pass:

- Read the file header, type docs, method docs, and inline comments before changing behavior.
- Update comments whose stated contract, side effect, ownership, fallback, or edge case changed.
- Delete comments that no longer match the code.
- Do not leave "almost right" comments for a later cleanup pass.
- If a change makes a comment unnecessary because the code is now self-explanatory, remove the comment instead of rewriting it.
- If a public API change affects docs in another file, update the local caller-facing docs in the same PR.

## Generated File Rules

Never edit generated files or files with generated headers.

Treat these as generated or vendor-owned unless local repo rules say otherwise:

- generated directories such as `generated/`, `Generated/`, `__generated__/`
- declaration outputs such as `.d.ts`
- GraphQL generated Swift files such as `*.graphql.swift`
- build outputs such as `dist/`, `build/`, `.build/`, `.next/`, `DerivedData/`, and `Pods/`
- vendored code and dependency folders such as `node_modules/`
- files whose opening banner says generated, do not edit, do not modify, or generated by

## Output Expectations

For audit or fix tasks, report:

- deterministic audit command and result
- file headers or type docs fixed
- semantic contract or inline why-comments fixed
- deliberate skips, especially generated files
- recommended next step if the repo should adopt or tighten a policy

For setup tasks, report:

- policy file path created or updated
- strictness level selected and why
- validation command added or recommended
- checks run

## Bundled Files

- `scripts/audit_inline_docs.py` - deterministic audit and mechanical doc-placement fixer for TypeScript, JavaScript, and Swift files.
- `scripts/test_audit_inline_docs.py` - smoke tests for the audit helper.
- `references/audit-and-fix.md` - focused audit loop for applying the script and semantic pass.
- `references/typescript.md` - TypeScript and JavaScript doc patterns.
- `references/swift.md` - Swift doc patterns.
- `references/comment-doc-policy-template.md` - repo policy template for durable docs/rules setup.
