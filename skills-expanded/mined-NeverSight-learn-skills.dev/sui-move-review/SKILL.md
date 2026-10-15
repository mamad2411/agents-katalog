---
name: sui-move-review
description: Audit a Sui Move pull request, branch, package, or release against the complete engineering standard. Use when the user wants a comprehensive review that applies every suite convention together; use focused skills for narrow architecture, security, event, error, source-style, or test reviews.
---

# Sui Move Review

Perform one evidence-based review across the complete standard.

## Load the standards

Read these sibling skills completely before reviewing:

1. [sui-move-architecture](../sui-move-architecture/SKILL.md)
2. [sui-move-source-style](../sui-move-source-style/SKILL.md)
3. [sui-move-security](../sui-move-security/SKILL.md)
4. [sui-move-events-errors](../sui-move-events-errors/SKILL.md)
5. [sui-move-testing](../sui-move-testing/SKILL.md)

Read [Package upgrade posture](references/package-upgrade-posture.md)
completely when the target is unpublished or the review concerns publication,
deployment, upgrades, immutability claims, package-capability custody, or
operational versioning. Also read it when the evidence does not establish one
of the three postures. Otherwise apply the classification in step 2 without
loading the reference.

Read the target repository instructions, package manifest, relevant design records, implementation, tests, and structural gates. Treat reference repositories as evidence, not authority over the target's accepted protocol decisions.

## Review in this order

1. Establish intended behavior, assets and invariants, threat assumptions, required liveness and exits, publication status, accepted future `Publisher` uses, and the published compatibility boundary.
2. Classify each package as intentionally immutable, simple upgradeable, or
   evolving shared-state upgradeable. Verify that the following agree with that
   posture:
   - `UpgradeCap` lifecycle and custody;
   - `Publisher` decision;
   - operational version seam;
   - deployment flow;
   - public promises.
   Do not recommend upgrade machinery without a concrete risk or roadmap
   requirement.
3. For an upgrade, compare against the published package and active
   `UpgradeCap` policy:
   - preserve existing public function signatures except for permitted
     relaxation of generic ability constraints;
   - preserve struct and enum layouts and abilities;
   - do not rely on module initializers;
   - keep old package versions safe or operationally gated;
   - use a new type and an authorized migration, or a dynamic-extension seam
     designed before publication, for state-shape changes.
4. Map package and module responsibilities, state ownership, dependency direction, and every authority issuance and custody-changing path.
5. Run a redundancy pass over stored fields, event types and fields, public
   seams, parameters, helpers, and locals. Name each fact's authority and
   consumer. Preserve type and ability boundaries plus replay-critical
   redundancy.
6. Search callers and trace every changed or transitively affected production
   transition through fail-fast guards, read-only dependency data, proposed values,
   postconditions, effectful handoffs, mutation, asset movement, emission, and
   returns. Require the owner function to read as that ordered summary. When it
   mixes independently nameable phases or phase-specific nested branches,
   extract cohesive domain-named private helpers without changing the sequence.
7. Reconcile arithmetic, rounding, balances, fees, burns, refunds, and residuals.
8. Check event replay, payload necessity, error ownership, abort location, and
   guard precedence. In simple packages, reject bare module-local `u64` errors:
   errors declared and raised by one module must use `#[error(code = N)]` with
   descriptive `vector<u8>` messages and preserved codes. Reserve package error
   macros for namespaces shared by multiple modules.
9. Check naming, sections, imports, visibility, abilities, signatures, `self`
   receiver naming, receiver syntax, direct UID access, pinned framework reuse,
   macro choices, local usage, and test-only seams.
10. Check test evidence across positive, negative, boundary, stateful invariant,
    adversarial composition, signatures, time, oracle, randomness,
    hostile-asset, replay, emergency, upgrade, and dependency risks.
11. Run the relevant pinned build, lint, test, source-boundary, ABI, dependency, coverage, and diff checks when available.

## Report findings

Lead with actionable findings ordered by severity. For each finding, include:

- exact file and tight line range;
- violated invariant or published contract;
- concrete failure or exploit path;
- smallest correct remediation;
- missing regression test when applicable.

Do not report personal style preferences as defects. Do not recommend a new abstraction without a concrete requirement. Distinguish confirmed defects from questions and evidence gaps.

After findings, list residual validation gaps or state that none remain. If there are no actionable findings, say so directly and summarize which gates and risk surfaces were checked.
