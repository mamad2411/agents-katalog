---
name: upgrade-research
description: "Researches each inventoried runtime and dependency: the deployment ceiling first, then latest stable and in-major versions, support status, EOL date and published advisories, ranked by exposure. Use when dependency-inventory has run, or when asked whether a runtime is still supported, what version a platform allows, or what to upgrade first. Not for building the inventory (use dependency-inventory) or ordering steps (use upgrade-plan); not a vulnerability scanner."
when_to_use: "is Node 20 still supported, what Python version does Lambda allow, is our runtime end of life, what is the latest version of, what should we upgrade first, how far behind are we, research these dependencies, which upgrades are security relevant"
argument-hint: "[inventory table, or a runtime/package to check, e.g. \"python 3.9 on Lambda\"]"
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Bash(npm view *), Bash(npm outdated *), Bash(npm audit --json *), Bash(pip index versions *), Bash(go list -m *), Bash(govulncheck *), Bash(cargo search *), Bash(bundle outdated *), Bash(poetry show *), Bash(docker manifest inspect *)
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# upgrade-research

Stage 2 of the upgrade pipeline. Input: $ARGUMENTS. If that is an inventory table, or the
conversation already holds one from `dependency-inventory`, research every row. If it names a single
runtime or package, research just that (rows `Q1`, `Q2`, …). If it is empty and there is no
inventory, run `dependency-inventory` first.

This skill reads and queries; it changes nothing. It reads advisories that registries and lockfile
auditors already publish; it is not a vulnerability scanner and finds nothing undisclosed.

**Without a shell (Cowork/web):** every registry and EOL source in
[references/registries.md](references/registries.md) has an HTTP endpoint, so use web fetch against
those. Mark `Advisories` as `not-checked` where only a local auditor could answer.

## The ceiling comes first

Latest stable is often the wrong target. The ceiling is the highest version the deployment target
accepts, and it bounds every other number: finding it first turns the question into "what is the
best version at or below this line" and stops a plan from proposing a runtime the platform rejects.

For each `runtime` and `base-image` row, and any row the platform constrains, find the ceiling from
the deployment target:

| Target | Ceiling source |
| --- | --- |
| Serverless functions (Lambda, Cloud Functions, Azure Functions) | The provider's supported-runtimes page, plus the runtime identifier already in the IaC |
| Managed containers (Cloud Run, App Runner, ECS/Fargate) | Usually no language cap; the base image tag and architecture you need must exist in the registry |
| Managed Kubernetes (EKS, GKE, AKS) | The cluster's control-plane version and the provider's version-support page; it caps kubelet, node images and client skew |
| HCP Terraform / Terraform Enterprise | The workspace's Terraform version setting, which overrides `required_version` intent |
| CI | The runner image's preinstalled toolchains and the versions the `setup-*` actions can install |
| Organisational policy | An approved-versions list or internal image registry; only the user can tell you |
| Downstream consumers (libraries) | The oldest runtime the library promises to support (`engines`, `requires-python`, `rust-version`) |

Search the IaC first, because the ceiling is often already encoded there: use Grep for `runtime`,
`image`, `kubernetes_version` / `cluster_version` / `engine_version`, and `terraform_version` across
`*.tf`, `*.yaml`, `*.yml` and `*.hcl`.

Record the result in one of three states:

- a version (`22.x`, `1.9.x`) with its source;
- `none-found`: you checked the deployment target and it imposes no cap (say what you checked);
- `unknown`: the deployment target itself is unknown, or only the user can answer.

`none-found` is a research result; `unknown` is an open question. Collect every `unknown` row and ask
the user about them together in one message before recommending a version for those rows. If the
user cannot answer, keep `unknown` and set `Recommended` to `needs-ceiling`.

## Versions, support and advisories

For each row, using [references/registries.md](references/registries.md):

1. **Latest stable**: from the registry (the `latest` dist-tag or newest non-prerelease), never
   from memory. Prereleases, RCs and `next` tags are never targets.
2. **In-major latest**: the highest stable version within the current major, which is what one
   low-risk step can reach.
3. **Recommended**: the highest stable version at or below the ceiling. Name what bound it in
   `Bound by`:
   - `upstream`: nothing newer exists;
   - `ceiling`: the platform caps it here;
   - `breaking`: the next version is a major, so the recommendation stays in-major; `upgrade-plan`
     sees the available major as `Latest stable` above `In-major latest` and decides whether to
     schedule it;
   - `unknown`: ceiling unknown, no recommendation yet.
4. **Support status and EOL**: registries do not carry support policy, so this is the one place
   for web research. Use endoflife.date or the project's own release-policy page, and the cloud
   provider's runtime deprecation page for managed runtimes. A support window cannot be derived from
   the version number; if no source answers, write `unknown`.
5. **Advisories**: run the ecosystem's auditor against the resolved versions, or query OSV by
   package and version. For `govulncheck`, report the vulnerabilities it finds in called code and
   say that is the scope.

Advisories found on transitive packages absent from the inventory get new rows `T1`, `T2`, … with
Kind `transitive`.

## Rank by exposure, not distance

Assign each row the highest rank that applies:

| Rank | Condition |
| --- | --- |
| 1 | Out of support now: no security patches are issued for the resolved version |
| 2 | Out of support soon: EOL falls within the planning horizon (default 6 months; use the user's horizon if given) |
| 3 | Known advisory against the resolved version |
| 4 | Feature-blocked: the user named something that needs a newer version |
| 5 | Merely behind, or current |

A runtime three minors behind but supported ranks below one a single minor behind that loses
support next month. Distance from latest never changes the rank.

## Handoff contract

`upgrade-plan` reads this exact format. The input is the `dependency-inventory` table (columns
`ID | Ecosystem | Manifest | Name | Kind | Declared | Resolved | Resolved from | Lockfile | Pin |
Notes`); carry `ID`, `Name` and `Kind` over unchanged and copy `Resolved` into `Current`. Changing
a column or enum here requires the same change in `upgrade-plan`.

```markdown
## Upgrade research — <repo name>
Planning horizon: <N months> · Researched: <YYYY-MM-DD>

| ID | Name | Kind | Current | Latest stable | In-major latest | Ceiling | Ceiling source | Recommended | Bound by | Support | EOL | Advisories | Rank | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Unknowns
- **Ceiling unknown:** <row IDs, or "none">
- **EOL unknown:** <row IDs, or "none">
- **Queries failed:** <row IDs and the command or URL that failed, or "none">
```

| Column | Allowed values |
| --- | --- |
| `ID` | Inventory ID (`I…`); `T…` for new transitive advisory rows; `Q…` for ad-hoc questions |
| `Name`, `Kind` | Copied from the inventory (`Kind` enum: `runtime`, `direct`, `dev`, `transitive`, `provider`, `module`, `base-image`, `action`, `hook`, `tool`) |
| `Current` | The inventory's `Resolved` value, including `unresolved` |
| `Latest stable`, `In-major latest` | A version, or `unknown` |
| `Ceiling` | A version or version line (`22.x`), `none-found`, or `unknown` |
| `Ceiling source` | Where the ceiling came from (file:line, provider page, user), or what was checked for `none-found` |
| `Recommended` | A target version or version line (`24.x`), `keep` (already at the best allowed version), or `needs-ceiling` |
| `Bound by` | `upstream`, `ceiling`, `breaking`, `unknown` |
| `Support` | `supported`, `eol-soon`, `eol`, `unknown`, `n/a` (no support policy exists, e.g. most libraries) |
| `EOL` | `YYYY-MM-DD`, `none-published`, `unknown`, or `n/a` |
| `Advisories` | Comma-separated IDs (`GHSA-…`, `CVE-…`, `GO-…`, `RUSTSEC-…`, `PYSEC-…`), `none` (checked, clean), `not-checked`, or `n/a` (no package to audit, e.g. a bare runtime question) |
| `Rank` | `1`–`5` from the ladder above |
| `Sources` | Short citations for Latest, EOL and Advisories: command run or URL fetched |

Order rows by `Rank` (1 first), runtimes before other kinds within a rank.

## Verify

Before handing off:

- Every inventory ID appears exactly once; no row has a blank cell.
- Every `runtime` and `base-image` row has a `Ceiling` of a version, `none-found` or `unknown`, and
  every `unknown` is listed under Unknowns.
- Every value that is not `unknown`, `not-checked` or `n/a` has a matching entry in `Sources`.
- `Rank` agrees with `Support` and `Advisories`: `eol` → 1, `eol-soon` → 2 or better, any advisory ID
  → 3 or better.

Fix any failure and re-check, then tell the user the next stage is `/dependency-upgrades:upgrade-plan`,
which they start themselves because it runs the test suite and writes `.upgrade/`.

## Examples

<example>
Illustrative values, not current facts. A Node service deployed to Lambda:

| ID | Name | Kind | Current | Latest stable | In-major latest | Ceiling | Ceiling source | Recommended | Bound by | Support | EOL | Advisories | Rank | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1 | node | runtime | 20.11.1 | 26.1.0 | 20.19.2 | 22.x | `infra/lambda.tf:14` + Lambda runtimes page | 22.x | ceiling | eol | 2026-04-30 | none | 1 | endoflife.date/nodejs; nodejs.org/dist/index.json |
| I3 | express | direct | 4.19.2 | 5.2.1 | 4.21.2 | none-found | Lambda imposes no cap on libraries | 4.21.2 | breaking | n/a | n/a | GHSA-xxxx-xxxx-xxxx | 3 | `npm view express`; `npm audit --json` |
| I5 | hashicorp/aws | provider | 5.62.0 | 6.4.0 | 5.100.0 | none-found | checked HCP workspace and CI | 5.100.0 | breaking | n/a | n/a | none | 5 | Terraform registry versions API |
</example>

<example>
Ad-hoc question "is Python 3.9 OK on our Cloud Function?" with no repo: one row `Q1`. The
deployment target is known (Cloud Functions), so fetch its supported-runtimes page for the ceiling
and endoflife.date for EOL. `Advisories` is `n/a` for a runtime with no package context, and the
answer leads with the Rank and the date.
</example>

<example>
No IaC in the repo and the user has not said where it deploys: ask once, listing every `runtime`
and `base-image` row. If the user does not know, those rows get `Ceiling` = `unknown`,
`Recommended` = `needs-ceiling`, `Bound by` = `unknown`, and appear under **Ceiling unknown**.
Their EOL and advisory research still goes ahead.
</example>
