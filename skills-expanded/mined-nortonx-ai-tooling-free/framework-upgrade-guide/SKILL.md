---
name: framework-upgrade-guide
description: "Stepwise major-by-major upgrade guide for TypeScript and Node projects (Angular, React, Vue), analyzing dependencies, deprecations, and EOL packages. Args: [<path-to-repo-or-package.json>]"
argument-hint: "[<path-to-repo-or-package.json>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<path-to-repo-or-package.json>]`

- Optional. Path to the target project root or its `package.json`. If omitted, use the current
  working directory.
- **Examples**: `/framework-upgrade-guide`, `/framework-upgrade-guide ./apps/web`, `/framework-upgrade-guide ../client/package.json`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Framework upgrade guide

Analyze a JavaScript/TypeScript front-end project, determine where it stands relative to the latest
stable release of its framework, and write a **stepwise, minimum-impact upgrade guide** to a file in
the repo. The guide must walk the project up **one major at a time** wherever the framework requires
it (Angular always; the others when codemods or breaking changes make a single jump unsafe), so the
person executing it never has to reverse-engineer the order or guess which packages move together.

The whole point is to remove risk and guesswork from a major upgrade. A guide that lists "upgrade to
the latest" without the intermediate hops, the lockstep version matrix, and the breaking changes per
hop is worse than useless; it gives false confidence. Be specific and be honest about what will break.

## Workflow

### 1. Detect: read only, never install

Read these from the target path (do not run `npm install`, builds, or anything that mutates state;
the project may be on someone else's machine and may not have `node_modules`):

- `package.json`: `dependencies`, `devDependencies`, `engines`, `packageManager`.
- The lockfile (`package-lock.json`, `yarn.lock`, or `pnpm-lock.yaml`): this has the **exact resolved
  versions**, which `package.json` ranges (`^`, `~`) do not. The resolved version is what you reason about.
  **If no lockfile exists**, say so prominently in the guide header: analysis falls back to `package.json`
  ranges, which may over- or under-state the installed versions. Ask the user to share the lockfile or
  paste the output of a read-only `npm ls --depth=0`.
- Framework config: `angular.json`, `vite.config.*`, `vue.config.*`,
  `next.config.*`, `nuxt.config.*`, `remix.config.*` (or `vite.config.*` importing `@remix-run/*`
  plugins): these disambiguate the framework and toolchain.
- `tsconfig.json` (current TypeScript target/strictness), `.nvmrc` / `.node-version` (runtime).

From this, fix three facts: **framework**, **current major version**, and **toolchain** (CLI vs Vite vs
CRA vs Nuxt/Next). Then read the matching `references/<framework>.md`: it holds the
per-hop breaking changes, lockstep matrix, and codemods you will need.

If the framework cannot be determined unambiguously from these signals (e.g. both `react` and `vue`
present), surface the candidates in the Clarify step and ask which is the primary framework; do not
guess. If the project is not one of Angular/React/Vue, say so and offer a generic dependency-bump plan
instead of forcing a framework template onto it.

### 2. Research the current truth

Your training data lags real releases. Before committing to a target version or listing breaking
changes, confirm against live sources:

- **context7**, if available: `resolve-library-id` then `query-docs` for the framework official
  upgrade/migration docs and the per-major changelog.
- **WebSearch / WebFetch**: the official update guide (e.g. `update.angular.dev`, the React and Vue
  upgrade guides) for the **current latest stable major** and the breaking changes per hop.

At least one live-source lookup is required; never rely on training data alone for version numbers or
breaking-change lists.

Confirm the latest stable major specifically; do not assume the number in your training data is current.

### 3. Clarify: ask probing questions and wait

Before writing anything, show the detected state (framework, current -> latest, toolchain) and
ask the questions that change the plan. Do not skip this: the right path depends on answers you cannot
read from files:

- Target version: latest stable, or pin to a specific major (e.g. an LTS the team standardizes on)?
- Risk tolerance and time budget: big-bang over a weekend, or incremental over sprints?
- Test coverage and CI: is there a suite that can verify each hop? (No tests changes the verification advice.)
- Monorepo / workspaces? (affects how `ng update`, codemods, and version pinning are applied)
- SSR / SSG in use (Angular Universal/hydration, Next, Nuxt)?
- Third-party UI / component libraries (Angular Material/CDK, PrimeNG, MUI, Vuetify, Tailwind plugins...):
  these often **gate the pace**: you cannot outrun the slowest core-coupled library.
- Node runtime constraints (a fixed Node version in prod can block a target major).
- Custom or ejected build (custom webpack, ejected CRA): automated migrations may not apply cleanly.
- Must the app stay shippable in prod throughout? (favors smaller, independently-releasable hops)

**Blocking** (do not write the guide without answers): target version, monorepo/workspaces, the
third-party UI/component library list. **Non-blocking** (state your assumption in the guide if
unanswered): risk tolerance, SSR, test coverage, Node constraints, custom build, prod-shippability.

Wait for the blocking answers before producing the guide.

### 4. Assess current state

Classify every dependency into **core** (the framework and its first-party companions, see the
reference file for the exact list per framework) and **ecosystem** (everything else). The guide focuses
on core; ecosystem packages are handled in the risk table (step 6).

Flag:
- Majors that are **EOL / unsupported** (no security patches): these raise urgency.
- **Deprecated** packages and APIs you can see in use.
- **Peer-dependency conflicts** that already exist or that the target will introduce.

**Security**: map the resolved lockfile versions to known advisories using your research (context7 /
WebSearch against the advisory databases). Note which vulnerabilities the upgrade resolves and which
need a separate bump. Recommend `npm audit` (or `pnpm audit` / `yarn audit`) as a verification step the
user runs themselves (read-only, optional, not something you require to produce the guide).

### 5. Compute the upgrade path

Build the hop sequence from current major to target. **One major per hop wherever the framework requires
sequential upgrades.** Mandatory for Angular (`ng update` refuses multi-major jumps). For React, split
at any intermediate major that ships official codemods or deprecation removals (currently 18 and 19):
running a later major's codemods on earlier source can mis-transform. For Vue 2->3, the migration-build
phases (install `@vue/compat` -> fix warnings -> remove compat) are the hops.

Assign each hop a Low/Medium/High risk rating based on: breaking changes needing manual edits,
third-party ecosystem blockers, and how much automated migration covers; this feeds the path
overview table.

For **each hop**, document:

- The official command (`ng update @angular/core@N @angular/cli@N`, React codemods, Vue migration build, etc.).
- The **lockstep core packages** that must move together, with the version each lands on (a small matrix).
- Breaking changes and the concrete code edits they require.
- Available automated migrations / codemods (and `--dry-run` to preview where supported).
- Minimum **TypeScript / Node** and other floor versions (RxJS, zone.js, etc. per framework).
- **Per-hop verification**: build, test, and a smoke check, so a hop is proven before the next starts.

### 6. Ecosystem risk table

List the non-core packages most likely to break, with the **evidence** (the peer-dependency range that
will not be satisfied at the target) and the version that does support the target, or "no compatible
release yet", which is itself a blocking finding the user needs up front.

### 7. Write the guide

Write to `docs/upgrades/<framework>-<from>-to-<to>.md` in the target repo (create the directory if
needed), using the template below.

## Output template

Use this exact structure so every guide this skill produces is consistent and scannable:

```markdown
# Upgrade guide: <Framework> <from> -> <to>

## Summary
<2 to 4 sentences: current state, target, number of hops, main risks.>

## Prerequisites
- Node, TypeScript, package manager (minimum versions)
- Dedicated branch / backup; test suite green before starting

## Path overview
| Hop | From | To | Main command | Risk |
|---|---|---|---|---|

## Step N: <X> -> <Y>
- **Command**: ...
- **Lockstep packages**: table (package -> target version)
- **Breaking changes**: ...
- **Codemods / automated migrations**: ...
- **Manual edits**: ...
- **Verification**: build / tests / smoke
<repeat per hop>

## Security
<vulnerabilities found, which the upgrade resolves, which need a separate bump>

## Ecosystem packages at risk
| Package | Current version | Peer constraint | Version compatible with the target |
|---|---|---|---|

## Final checklist
- [ ] ...

## Rollback
<must specify: (1) the branch/tag to restore, (2) the lockfile restore command
(`git checkout HEAD -- <lockfile>`), (3) clear and reinstall node_modules after a lockfile revert,
(4) note that migration schematics/codemods rewrite source; reverting the lockfile alone is not
enough; check out the hop's starting commit to restore source too>
```
