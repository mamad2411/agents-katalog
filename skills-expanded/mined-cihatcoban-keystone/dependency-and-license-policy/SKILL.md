---
name: dependency-and-license-policy
description: Gates every new dependency, model, dataset or copied snippet on necessity, health, license and supply-chain risk. Triggers - should we add this library, is this license compatible, GPL, copied this snippet from Stack Overflow, upgrade a major version, model weights license.
---

# Dependency and License Policy

Every dependency is a permanent commitment: to its bugs, its security patches,
its maintainer's attention span, its transitive tree, and its license. Adding
one takes thirty seconds; removing one takes a quarter. The gate belongs at the
moment of adding.

## Necessity

Ask in order, and stop at the first yes:

1. Does the **standard library** do this? (Usually yes for date handling,
   string manipulation, basic crypto primitives, simple HTTP.)
2. Does an **existing dependency** already do this? Two libraries solving one
   problem is a source of subtle inconsistency.
3. Is this **50 lines we could own**? A tiny dependency for a trivial function
   is supply-chain risk with no upside.
4. Is the problem **genuinely hard** (crypto, parsing, time zones,
   compression, protocol implementations)? Then take the dependency — hand-rolling
   these is worse.

Never write your own cryptography, TLS, password hashing, or timezone database.

## Search before you write

The cheapest dependency is code that already exists in this repository. Agents
in particular write a fresh helper because writing is faster than finding — and
the codebase grows a second date formatter, a third retry loop, a fourth way to
read config, each with its own bugs.

Before writing anything that sounds generic (parsing, formatting, retrying,
validation, pagination, a client for an internal service), spend a few minutes
looking, in this order:

| Where | How to look |
|---|---|
| This repository | Search by **behavior**, not by the name you would give it: the literal it must handle (a date format string, an error code, an endpoint path), the library it would call, a test that describes it. Check `utils`, `common`, `shared`, `lib` |
| Sibling packages the team owns | The organization's internal packages and the services this one already calls |
| The standard library | Then the necessity questions above |
| The ecosystem | Only now — and the result goes through the health and license gates |

What to do with what you find:

- **Fits:** reuse it, even if you would have named it differently.
- **Almost fits:** extend or fix it in place, with tests, as its own commit. A
  near-copy beside the original is two implementations to keep in sync.
- **Wrong:** fix it or replace it everywhere, with a deprecation path
  (`deprecation-and-migration`); never add a parallel one silently.
- **Found in another repository:** that is copying — the rules under "Copied
  code" apply.

Say what you searched in the pull request: "searched for X, reused Y" or
"searched for X, nothing found". A reviewer can then check the search instead of
rediscovering the duplicate.

## Health check

| Criterion | Green | Red |
|---|---|---|
| Last release | Within 12 months | Dormant with open security issues |
| Maintainers | ≥ 2 active | One person, no succession |
| Open critical issues | None, or triaged | Long-standing unacknowledged |
| Transitive dependencies | Few, known | Pulls in dozens |
| Release discipline | Semver honored, changelog | Breaking changes in patches |
| Adoption | Meaningful usage | Zero usage beyond the author |
| Install footprint | Reasonable | Post-install scripts, native build surprises |

Weigh the **transitive tree**, not just the package. A small library with
forty dependencies is forty commitments.

## License compatibility

Check the license of the package **and** its dependencies. Match against the
project's position:

| License class | Proprietary project | Notes |
|---|---|---|
| MIT, BSD, ISC, Apache-2.0, PSF | Allowed | Apache-2.0 also grants patent rights — prefer it |
| MPL-2.0, LGPL | Conditional | File-level / dynamic-linking obligations; keep the boundary intact and record it |
| GPL, AGPL, SSPL | Blocked by default | Can impose source-disclosure obligations; AGPL triggers on network use. Exception requires an ADR and legal review |
| "Source available" (BSL, Elastic, Commons Clause) | Blocked by default | Not open source; usage restrictions vary and change |
| No license file | Blocked | No license means no rights granted, regardless of public availability |

Keep an allow-list and enforce it in CI. Licenses also **change between
versions** — check on major upgrades, not only on first adoption.

## Model weights and datasets

A model's code license and its **weights** license are separate documents, and
the weights usually carry the restrictions.

- Is commercial use permitted? Many prominent models restrict it.
- Are there use-case restrictions, attribution or share-alike obligations on
  outputs?
- Dataset provenance: was it collected lawfully? Does it carry attribution or
  non-commercial terms?
- Record source, version, license and **checksum** in the repository. Never
  commit weights; download and verify.

## Copied code

Anything copied from Stack Overflow, a blog, an LLM's output of a known
implementation, or another repository is licensed by someone.

- More than a trivial snippet: record source and license in the file header and
  in `NOTICE`.
- Incompatible license: do not copy. Understand the approach and write it.
- Unclear provenance: do not copy.

## Upgrades

- Patch and minor: automated, with CI as the gate.
- Major: read the changelog, budget time, do it alone in its own PR.
- Never upgrade a dependency inside a feature change — when something breaks
  you will not know which change caused it.
- Pin with a lockfile; reproducible installs are a security property.
- Automated vulnerability scanning in CI, zero known high/critical.

## Record

One row per dependency in `docs/dependencies.md`:

```markdown
| package | version | license | why | alternatives considered | decided |
```

Six months later, this is what tells you whether it is still needed.

## Exit checklist

- [ ] Standard library and existing dependencies ruled out first
- [ ] Health criteria checked, including the transitive tree
- [ ] License on the allow-list — for the package and its dependencies
- [ ] For models/datasets: commercial use verified, checksum recorded
- [ ] Copied code attributed in the file and in `NOTICE`, or reimplemented
- [ ] Lockfile updated; vulnerability scan clean
- [ ] `docs/dependencies.md` row added with the rationale
