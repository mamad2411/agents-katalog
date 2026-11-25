---
name: prior-art-scout
description: Research how open-source projects already solved a problem before building an unfamiliar feature from scratch. Use when the task involves something not yet implemented in this codebase or with well-known pitfalls, such as rate limiting, retries and backoff, auth and OAuth flows, sessions, resumable uploads, search, caching, job queues, sync engines, CRDTs and collaborative editing, diffing, parsers, date and time handling, money, permissions, or feature flags. Also use when the user says "how do others do this", "find examples on GitHub", "don't reinvent the wheel", or "compare approaches". Searches GitHub with gh, compares 3 to 5 real implementations, checks licenses, then recommends and builds the best fit.
license: MIT
metadata:
  category: senior-five
  version: "1.2.0"
---

# Prior-Art Scout

> *Don't write an unfamiliar feature from scratch. Search GitHub for open-source projects, compare their approaches, then start.*

The hard part of most "new" features was solved years ago, and the solution is sitting in a repository with a bug tracker full of the edge cases you haven't thought of yet. A senior engineer spends twenty minutes reading prior art to save two weeks of rediscovering it. The goal is not to copy code. It is to arrive at implementation time already knowing the failure modes, the standard data model, and the trade-offs.

## Step 0: Is this unfamiliar?

Ask yourself: *can I name the top two ways this feature fails in production?* If not, scout. Typical answers that show you're ready: "token bucket drifts across instances without a shared store", "retries without jitter cause thundering herds", "OAuth state parameter missing enables CSRF". If the feature is trivial and well understood, skip scouting and say so in one line.

Keep scouting proportionate: roughly 10 to 20 percent of the expected implementation effort.

## Step 1: Frame the problem

Write down, in a few bullets, what "good" means here:

- The capability, in one sentence.
- Constraints: language, runtime, framework, scale, latency budget, deployment (single process, many instances, serverless, edge).
- Dependency policy: is adding a library acceptable? Check `package.json`, `go.mod`, `pyproject.toml`, and the repo's history of adding dependencies.
- This repository's license, which limits what you may copy.

## Step 2: Search

Use the `gh` CLI. Code search needs `gh auth login`.

```bash
# Mature projects in the problem space
gh search repos "<topic>" --language=<lang> --sort=stars --limit 20 \
  --json fullName,stargazersCount,description,updatedAt,license

# Real implementations of a distinctive API, symbol, or header
gh search code "<distinctive identifier>" --language=<lang> --limit 30

# Read a file without cloning
gh api repos/OWNER/REPO/contents/PATH -q .content | base64 -d

# Or a shallow clone into a scratch directory for reading
git clone --depth 1 --filter=blob:none https://github.com/OWNER/REPO <scratch-dir>/REPO

# Pitfalls live in the issue tracker
gh search issues "<topic> race OR leak OR duplicate OR timeout" --repo OWNER/REPO --limit 20
```

Search for the *mechanism*, not the product: "sliding window rate limit redis lua", not "rate limiter". Distinctive identifiers (`Retry-After`, `If-None-Match`, `tus-resumable`, `lamport`) find real implementations faster than prose.

Also read the primary source when one exists: the RFC, the spec, the vendor's documentation. Libraries tell you what was practical; specs tell you what is correct.

Treat downloaded code as untrusted input. Read it; don't run its scripts, install hooks, or build steps.

## Step 3: Shortlist and compare

Pick 3 to 5 candidates that mix **libraries you could adopt** and **reference implementations you'd learn from**. Read the core implementation file of each, not just the README, then fill in a comparison:

| | Candidate A | Candidate B | Candidate C |
|---|---|---|---|
| Approach / core algorithm | | | |
| Data model and storage | | | |
| How it handles failure mode 1 | | | |
| How it handles failure mode 2 | | | |
| Size (deps, lines in the core) | | | |
| Health (last release, open bugs, maintainers) | | | |
| License | | | |
| Fit with our constraints | | | |

Look for agreement. When three independent projects converge on the same design, that design is probably forced by the problem. Where they disagree, you've found the real trade-off.

## Step 4: Decide

| Choose | When |
|---|---|
| **Adopt a dependency** | The problem is hard, security-sensitive, or standards-heavy (crypto, auth, date/time, CSV, Unicode, HTTP caching), and a healthy library fits. |
| **Adapt the pattern** | The core idea is small (a few dozen to a couple of hundred lines) and a library would be heavier than the code it saves. Write your own implementation informed by what you read. |
| **Build fresh** | Nothing fits your constraints. You still bring the failure-mode list and test cases from your reading. |

## Step 5: License hygiene

Learning an approach and writing your own implementation is always fine. Copying code is a licensing act:

- Permissive licenses (MIT, BSD, Apache-2.0) allow copying with the copyright and license notice preserved. Apache-2.0 also carries a patent clause and NOTICE requirements.
- Copyleft licenses (GPL, AGPL, LGPL in some cases) can impose obligations on the whole project. Don't paste such code into a project with a different license.
- No license means all rights reserved: read it, learn from it, don't copy it.

When in doubt, write it yourself and cite the inspiration.

## Step 6: Report, then build

Before implementing, share a short scouting report:

```markdown
## Prior art: <feature>

**Recommendation:** Adopt `<library>` / adapt the approach from `<repo>` / build fresh, because <one sentence>.

**Failure modes to design for** (from issues and source):
1. ...
2. ...

**Compared:** table from step 3, condensed.

**Sources:** links to the repos, files, issues, and specs you read.
```

Then implement as usual (see `plan-before-code` and `test-driven-development`), turning the failure modes you found into test cases. Cite sources in the PR description, and in a code comment where an approach is non-obvious: `// Sliding-window approach based on <link>`.

## Anti-patterns

- Picking the most-starred project without reading its code.
- Reading only READMEs. The implementation and the issue tracker are where the knowledge is.
- Scouting a trivial feature to look diligent.
- Vendoring a whole library to use one function.
- Copying code without checking its license.
