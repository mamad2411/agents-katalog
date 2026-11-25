---
name: reviewer-risk-and-false-green
description: Use when review must challenge security, consistency, lifecycle, disclosure, and passing evidence.
---

# Audit risk and attack false greens

## Inputs
Pinned diff, acceptance trace, test source and receipts, fixtures, topology, negative controls, ownership/disclosure policy, and known gaps.

## Procedure
1. Inspect caller ownership, authorisation ordering, error disclosure, lifecycle cutoffs, stale writes, expected-version checks, and repeated-intent precedence.
2. Inspect idempotency scope, fingerprint/replay equality, key misuse, and whether mutation, version, event, and record share the claimed consistency boundary.
3. Compare synchronisation with actual processes, workers, stores, transactions, and failure modes.
4. Read assertions, not names or summaries. Separate import/syntax/harness RED from a semantic negative control and require fresh restored GREEN on the same target.
5. Apply deletion attacks: ask whether removing state, version, payload, record, forbidden-effect, or race assertions could leave the suite green.
6. Reject stale, truncated, self-attested, fixture-derived, or package-only proof; preserve missing dimensions as unassessed rather than defects.
7. Write each finding with locator, consequence, remediation, owner path, and recheck condition.

## Output
Security/consistency findings, negative-control assessment, deletion-attack list, unsupported claims, and exact supported-boundary statement.

## Stop condition
Stop on unanswered critical authorisation, integrity, or disclosure risk, wrong-cause RED, absent restoration/fresh GREEN, or evidence that cannot be bound to exact bytes.
