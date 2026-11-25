---
name: repo-impact
description: 'Answer whether a specific advisory reaches anything in THIS repository — which manifest declares the package, at what version, whether the version is in range, and whether the vulnerable code is reachable. Use when someone asks "does CVE-… affect us", when triaging an advisory against a real codebase, or before spending effort on a fix.'
license: Apache-2.0
allowed-tools: Bash(vulnetix:*) Read Grep Glob
argument-hint: <CVE-…|GHSA-…>
user-invocable: true
model: sonnet
metadata:
  outputBudget: short
  chain: "fix, dependency-choice"
---

# Repository impact

## Use when

- "Does CVE-2021-44228 affect us?" — the only question that matters when an
  advisory is in the news.
- Triaging an advisory that names a package this repository might pull in
  transitively.
- Deciding whether a fix is worth the effort before starting it.

## Don't use for

- Looking the advisory up. That is `vulnetix_vuln` over MCP, or
  `vulnetix vdb vuln <id>`, and it needs no skill. This skill exists for the half
  that needs the working tree.
- Applying the fix — `fix`.
- Confirming a fix landed — `verify-fix`.

## Conventions

Follows `skills/_lib/contract.md` for surface selection, output style and memory
writes.

## What "affects us" actually means

Four questions, in order, and each one can end the enquiry:

1. **Is the package here at all?** Directly, or pulled in transitively.
2. **Is the installed version in the affected range?** Being on the package is
   not being vulnerable.
3. **Is there a fixed version, and how far away is it?** A patch release and a
   major rewrite are different answers.
4. **Is the vulnerable code reachable?** Present in the tree is not the same as
   called.

Report which of these you could answer and which you could not. An unreachable
finding and an unanswered reachability question look identical in a summary and
mean opposite things.

## Step 1: Ask the tree, not the internet

```bash
vulnetix scan --sca -o json
```

This resolves the actual dependency graph, including transitives, and anchors each
package to the manifest line that declares it. Grep is not a substitute: it misses
transitives entirely, which is where most advisories land.

If a scan was already recorded, `.vulnetix/memory.yaml` has it, and
`vulnetix agent hook` puts a summary in front of the agent at session start.
Reuse that when it is current, and say it is a snapshot.

## Step 2: Get the advisory's own facts

```bash
vulnetix vdb vuln "$ARGUMENTS" -o json
```

Or `vulnetix_vuln` with `detail: summary` over MCP, which is about 10 KB rather
than megabytes.

Take the affected ranges, the fixed versions, the affected routines, and whether
it is known-exploited.

## Step 3: Intersect

Match the advisory's affected ranges against the versions actually resolved in
step 1. Be exact about ranges — `>=2.0.0 <2.17.1` does not include 2.17.1, and an
off-by-one here is the difference between an emergency and a non-event.

## Step 4: Reachability, when the CLI can answer it

```bash
vulnetix scan --reachability -o json
```

The advisory names affected routines; reachability says whether this repository
calls them. When it cannot answer — no analyser for the language, a dynamic call
graph — say so rather than reporting UNKNOWN as if it were UNREACHABLE.

## Step 5: Answer the question that was asked

```
<CVE-…>: <AFFECTED | NOT AFFECTED | CANNOT DETERMINE>

  Package    <name>@<installed>
  Declared   <manifest>:<line>   (<direct | transitive via X>)
  Affected   <range>  ->  fixed in <version>
  Reachable  <yes: path | no | not analysed for <language>>
  Exploited  <known exploited | no evidence>
```

Lead with the verdict. If the answer is NOT AFFECTED, say why in one line — wrong
version, wrong platform, not present — because "no" without a reason gets asked
again next week.

Record the verdict in `.vulnetix/memory.yaml` so the next session, and
`dashboard`, can see the decision rather than repeat the work.

Next: `fix <CVE-…>` when the answer is AFFECTED.
