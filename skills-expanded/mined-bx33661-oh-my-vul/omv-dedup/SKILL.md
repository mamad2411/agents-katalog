---
name: omv-dedup
description: |
  Checks whether an Evidence.v1 finding is likely already disclosed. Use when the user asks to deduplicate a finding, check CNA duplicate risk, search NVD/GHSA/OSV/ecosystem advisory databases or public discussion (issues, PRs, commits, blogs), or invokes `/omv-dedup`. Produces deterministic queries, grades novelty risk, and writes Evidence.v1 dedup fields only after confirmation.
---

# omv-dedup

Assess duplicate disclosure risk for a local finding.

## Invocation

```text
/omv-dedup <id>
```

## Core Rule

Advisory databases lag public discussion. A bug can be well known in issue
trackers, fix PRs, or blog posts for months or years before any CVE or GHSA
entry exists — and sometimes no advisory ever appears. "Advisory-clean" does
NOT mean novel.

A public issue, pull request, or commit that discloses the same vulnerability
makes the finding a duplicate for submission purposes, even without a CVE.
First-disclosure credit belongs to whoever reported it publicly first.

## Workflow

1. Read `.omv/findings/<id>.yaml` using `contracts/evidence.v1.yaml` as the local schema reference.
2. Run `omv dedup <id>` to produce deterministic queries for all six sources:
   - Advisory: NVD, GHSA, OSV, ecosystem advisory database.
   - Public discussion: upstream GitHub issues **and pull requests** (open and
     closed), upstream commit history, and a public web search (blogs,
     aggregators, VulDB-style databases).
3. Show the queries before conclusions.
4. Execute each query passively. For issues/PRs search the repo for the
   vulnerability class keywords (eval, traversal, RCE, prototype, sandbox...),
   not just the package name — reporters rarely use canonical class names.
5. Compare package, ecosystem, affected range, vulnerability class, CWE, source, sink, guard, and fixed version signals.
6. Grade novelty risk as `High`, `Medium`, or `Low`.
7. Only after user confirmation, write fields with:
   - `omv dedup <id> --confirm --existing-cve <CVE|none> --notes <summary>`

## Risk Rules

- `High`: same package plus same vulnerability class plus overlapping affected
  range or sink behavior — OR any public issue/PR/commit disclosing the same
  bug, regardless of whether a CVE exists.
- `Medium`: same package or same sink behavior, but incomplete version or
  guard overlap; or a locked/obscure discussion that might describe the bug
  ambiguously.
- `Low`: no close advisory match AND no public discussion match after
  source-specific searches of all six sources.

Do not block a novel finding solely from package-name overlap.

## Comparison Method

Build a table before assigning risk:

- Query source: NVD, GHSA, OSV, ecosystem database, maintainer advisory,
  upstream issues/PRs, upstream commits, public web.
- Identity overlap: ecosystem, registry name, repository, vendor/product.
- Version overlap: affected range, fixed version, release date, vulnerable component.
- Behavior overlap: source type, sink API, guard/fix description, CWE, exploitability preconditions.
- Provenance quality: primary advisory, maintainer fix, public disclosure
  thread, or secondary mention.
- Disclosure timeline: date of the earliest public mention versus the local
  verification date.

## Pre-Submission Recheck

Dedup results go stale. Before `/omv-report` submits anything, re-run the web
and GitHub searches if the last dedup pass is older than a few days — public
disclosure can appear at any time, and submitting a just-disclosed bug burns
credibility.

## Honest Outcomes

When dedup finds a public disclosure, say so plainly: recommend against
submission, record the earliest public reference in `dedup.notes`, and surface
the variant angle instead (the same bug class in sibling packages is often
still unreported — see `/omv-radar` variant playbooks). An independent
rediscovery validates the audit pipeline even when it earns no submission.

Use sanitized fixture names in examples and evals. Real packages are allowed
only when supplied by the user as active research context.
