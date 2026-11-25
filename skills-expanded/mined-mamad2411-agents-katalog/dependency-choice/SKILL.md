---
name: dependency-choice
description: 'Work through which package to add for a capability, and what each option costs — maintenance, licence, bundle weight, transitive risk, and whether the platform already does it. Use when someone needs a library for a job and has not picked one yet, when weighing two candidates, or when a package looks convenient but unmaintained.'
license: Apache-2.0
allowed-tools: Bash(vulnetix:*) Read Grep Glob
argument-hint: <capability or package name> [--ecosystem npm|pypi|...]
user-invocable: true
model: sonnet
metadata:
  outputBudget: medium
  chain: "typosquat-check, fix"
---

# Dependency choice

## Use when

- Someone needs a capability — "I need JavaScript crypto", "we need a date
  library" — and has not chosen a package yet.
- Two candidates are on the table and the trade-off is not obvious.
- A package is convenient but looks unmaintained, or is a fork of something that
  was.
- A dependency is about to be added to satisfy one small function.

## Don't use for

- **Deciding whether an already-chosen package is allowed.** That is the
  `dependency-guard` hook, and it runs on its own when the agent tries to install
  something. This skill is the conversation before that point.
- Resolving a blocked upgrade — `dep-resolve`.
- Checking whether a name is impersonating another — `typosquat-check`, which this
  skill calls when a candidate looks suspicious.

The distinction matters. The hook is a guardrail: it fires when nobody weighed
anything, and it stays silent when the repository's policy is already satisfied.
This skill is where somebody deliberately weighs the options, and it may well
conclude that the riskier package is the right call.

## Conventions

Follows `skills/_lib/contract.md` for surface selection, output style and memory
writes.

## The first question is whether to add anything

A dependency has a permanent cost — a supply-chain surface, a licence, an upgrade
treadmill, and a maintainer who may stop. Before comparing packages, check whether
the platform already does the job.

This is the most valuable thing this skill does and the easiest to skip. Worked
example, JavaScript cryptography:

| Option | What you get | What it costs |
|---|---|---|
| `SubtleCrypto` (built in) | AES-GCM, SHA-2, HMAC, ECDSA, key derivation. In every browser and in Node 15+. | Async-only API, and no MD5/SHA-1 — usually a feature. Zero dependencies. |
| `crypto-js` | Feature-complete, synchronous, familiar. | Effectively unmaintained. Ships its own primitives, so a defect is yours to carry. |
| `crypto-es` | The same API, modern targets, actually maintained. | ESM-only; a CommonJS build will not take it without work. |

The honest recommendation for most new code is the first row, and nobody reaches
it by searching npm for "crypto".

Look for the same shape elsewhere: `Intl.DateTimeFormat` before a date library,
`fetch` before an HTTP client, `structuredClone` before a deep-clone package,
`crypto.randomUUID()` before a UUID package.

## Step 1: Establish the candidates

If the user named a package, start there and find its realistic alternatives. If
they named a capability, propose two or three.

```bash
vulnetix vdb packages search "<term>" --ecosystem "<eco>" -o json
```

With MCP available, `vulnetix_package_search` returns the same thing already
shaped.

## Step 2: Get the facts, in one pass

Run these together rather than one after another — they are independent.

```bash
vulnetix vdb packages get "<name>" --ecosystem "<eco>" -o json   # health, EOL, scorecard
vulnetix vdb package-vulns "<name>" --ecosystem "<eco>" -o json  # advisory history
```

MCP equivalents: `vulnetix_package_search`, `vulnetix_package_vulns`,
`vulnetix_purl`.

What to pull out, and why each matters:

- **Last release, and open-issue trend.** A package with no release in two years
  is one you have adopted rather than depend on.
- **Advisory history.** Not the count — the response. A project that shipped a
  fix in days has different risk from one where the CVE sat open.
- **OpenSSF Scorecard.** Branch protection, signed releases, dependency-update
  automation. Low signal alone, useful as a tiebreak.
- **Transitive count.** A package pulling ninety dependencies to do one job is
  ninety more chances for the next incident.
- **Licence.** Against this repository's policy, not against general opinion.
- **EOL.** For runtimes and framework majors.

## Step 3: Check the name before recommending it

If a candidate is unfamiliar, or close to a well-known name, run
`typosquat-check` before saying it out loud. Recommending a typosquat is the worst
possible outcome of this skill.

## Step 4: Put the trade-off to the user

The output is a comparison and a recommendation, not a verdict. The user knows
things this skill does not — the deployment target, the team's tolerance for an
ESM migration, whether the synchronous API is load-bearing.

```
For <capability>, in <ecosystem>:

  <option>   <one line: what it gives you>
             + <the real advantage>
             - <the real cost>

Recommendation: <one>, because <the reason that would change if the facts changed>.

Worth knowing: <the thing they would otherwise find out later>.
```

Say when the platform already covers it, and say when the answer depends on
something only they know. A recommendation that does not survive one follow-up
question was not worth making.

## Step 5: Record it

Once a choice is made, append a `history` event to `.vulnetix/memory.yaml` with
the package chosen and the reason. Six months later the question "why are we on
this?" has an answer, and `dashboard` can surface it.

Next: `typosquat-check <package>` before installing an unfamiliar name.
