---
name: code-variable-audit
description: "Audit pull requests, branches, diffs, or local source files for semantically suspicious variable, identifier, member-access, and payload-field usage. Use when checking wrong-object bugs such as product.id versus rexProduct.id, source-system identity confusion, alias erasure, mismatched payload keys, or cross-system variable mixups; optionally publishes open-PR comments or merged-PR investigation issues and hands explicit issue targets to issue-to-green-pr when publication is authorized."
---

# Code Variable Audit

Use this skill for audit-only review of variable and member usage. It is designed for bugs where code is syntactically valid but uses the wrong source object or identity, such as assigning `product.id` to a REX field, passing a Shopify identifier into a local-product function, or erasing `rexProduct.id` into a generic `id` in a mixed-source scope.

## Guardrails

- Do not edit repo code from this skill.
- Do not claim semantic correctness from syntax alone. Treat the script as a coverage and suspicion generator, then review findings against source truth.
- Scan every changed JavaScript, TypeScript, JSX, TSX, MJS, CJS, MTS, and CTS file. Record skipped files in the coverage ledger.
- Fail closed on unreadable changed files and parser failures. For PR and publication modes, also fail closed on unresolved GitHub state.
- Use the full skill body and bundled scripts from the invoked skill directory.
  Keep the Codex and Claude copies in sync; do not replace either copy with a
  redirect-only wrapper.
- Default to dry-run. Add `--publish` only when the user explicitly authorizes GitHub publication. Publication may create the missing `needs-investigation` repo label so the issue can be tagged correctly.

## Workflow

1. Restate the target PR, branch, diff, or file list and whether publication is authorized.
2. Run the collector. For a GitHub PR:

```bash
/Users/ben/.codex/skills/code-variable-audit/scripts/code-variable-audit.cjs --repo anotherben/helpdesk --pr 123 --dry-run --output /tmp/code-variable-audit-123.md
```

For batch/evaluation runs, write JSON to a file. When `--json --output` are both set,
stdout is a compact receipt and the full JSON is written only to the output file:

```bash
/Users/ben/.codex/skills/code-variable-audit/scripts/code-variable-audit.cjs --repo anotherben/helpdesk --pr 123 --dry-run --fail-on never --json --output /tmp/code-variable-audit-123.json
```

3. For local changes:

```bash
/Users/ben/.codex/skills/code-variable-audit/scripts/code-variable-audit.cjs --base origin/dev --head HEAD --dry-run --output /tmp/code-variable-audit-local.md
```

4. For a focused file or file list:

```bash
/Users/ben/.codex/skills/code-variable-audit/scripts/code-variable-audit.cjs --file apps/api/src/services/example.js --dry-run --output /tmp/code-variable-audit-file.md
```

5. If publication was authorized:

```bash
/Users/ben/.codex/skills/code-variable-audit/scripts/code-variable-audit.cjs --repo anotherben/helpdesk --pr 123 --publish --output /tmp/code-variable-audit-123.md --handoff-output /tmp/code-variable-audit-123-issue-to-green-pr.json
```

6. If the report includes an `Issue-To-Green-PR Handoff` section or `issueToGreenPrHandoff` JSON, immediately invoke `$issue-to-green-pr` with the emitted issue URL. Pass only the explicit target issue; do not copy or restate the downstream workflow.
7. Review findings manually against source truth, domain docs, schemas, and callers. The report is the audit deliverable; do not fix code from this skill.

## What The Script Checks

The detector is tuned for **precision**: it flags only cross-source-system identity
confusion between REX (Retail Express — `rex`, `retailExpress`) and Shopify
(`shopify`), where a NAME claims one system and a **reference value** (an identifier
or member access — never a string/number/object literal) provably comes from the other.

- Variable declarations: `const rexOrderId = shopifyOrder.id`.
- Assignments: `target.shopifyVariantId = rexVariant.id`.
- Object payload keys: `{ rexProductId: shopifyProduct.id }`.
- Destructuring that erases a system identity in a multi-system scope:
  `const { id } = rexProduct` where the scope also references a Shopify object.

Leaf-property precedence and in-file provenance are applied, so `shopifyOrder.rexProductId`
reads as REX (correct), and a generic-named variable that holds a Shopify id
(`const orderId = shopifyOrder.id`) is still tracked when later stored in a REX field.

### Deliberately NOT flagged (precision guards)

- String/number/template/object/array **literal** values (`retailExpressProductId: 'REX-10'`, `product_name: 'PO Detail Scope'`).
- Receiver/namespace tokens (`localStorage.setItem`, `skuMappingsRouteService.create*`).
- Domain-entity-only mismatches that are not source-system confusion (`order` vs `payment`, `product` vs `supplier`).
- Same-system references, and foreign-holder fields named to hold another system's id by design (`rexExternalId`, `rexSourceId`).
- Resolver / lookup / linker calls (`getRexOrderId(shopifyOrderId)`) that legitimately translate between systems — a function name cannot reveal the expected system of its arguments, so call-argument checking is intentionally not performed.
- Test files (`*.test.*`, `*.spec.*`, `__tests__/`, `__mocks__/`, `e2e/`, `cypress/`) are excluded by default; pass `--include-tests` to analyze them.

## Severity

- `CRITICAL`: a name claims one source system (REX or Shopify) and a reference value provably comes from the other.
- `HIGH`: a source-system identity is erased by destructuring in a multi-system scope, or a changed file could not be parsed/read.
- `LOW`: partial-parse diagnostics — a coverage note only; never flips the verdict.

## Publication Rules

- Open PR with findings: post one PR comment with the coverage summary and first findings.
- Merged PR with findings: open or reuse one GitHub issue labeled `bug` and `needs-investigation`, emit an `issueToGreenPrHandoff` target, then run `$issue-to-green-pr` on that issue URL.
- Closed-unmerged PR with findings: do not open an investigation issue by default because the change did not ship. Return the report and publication plan instead.
- Passing audit: do not publish.
- Publication must include a stable marker so reruns can detect prior output instead of spamming. Existing investigation issues must be relabeled with `bug` and `needs-investigation` before handoff.

## Output Requirements

A valid report includes:

- Zoom-out trace: target, changed files, parse method, and publication route.
- Blast radius counts: files, scanned files, skipped files, member accesses, identifiers, assignments, payload keys, calls, and findings.
- Coverage ledger for every changed source file scanned or skipped.
- Suspicion ledger with stable `CVA-*` finding IDs, file, line, severity, rule, evidence, and required review.
- Ambiguity ledger for functions/files containing multiple identity-bearing bases.
- Trace boundaries that state the script does not execute code, infer business intent, or fix findings.
- Publication result and, for merged failing PRs, an explicit `$issue-to-green-pr` handoff issue URL.
