---
name: licence-audit
description: Build the dependency licence inventory from the resolved transitive tree and the shipped artefact, determine which obligations are actually triggered by how the software is conveyed (distributed binary, container, SaaS, on-prem, model weights), flag incompatibilities against the project's own outbound licence, check contributor IP through CLA or DCO, and produce NOTICE and attribution output. Use before a release, before funding or acquisition diligence, when adding a dependency with an unfamiliar licence, or when a customer asks for a licence report. Not legal advice.
disallowed-tools: Write Edit NotebookEdit
user-invocable: true
argument-hint: "[--conveyance saas|binary|container|onprem|library] [--notice-only] [--fail-on copyleft|unknown]"
context: fork
agent: foundry-legal:licence-analyst
model: opus
effort: high
metadata:
  foundry.vertical: compliance
  foundry.io: "lockfiles + artefact -> SBOM + licence inventory + conflicts + NOTICE draft"
license: Apache-2.0
---

# Licence audit

> **Automated technical assessment. Not legal advice.** Licence compatibility turns on facts a tool
> cannot see: your contracts, how the software is conveyed, what was linked and how, and which
> jurisdiction's copyright law applies. Have a qualified lawyer confirm anything before you rely on
> it in a release, a contract or a diligence response.

Two facts drive the whole audit:

1. **Obligations trigger on conveyance, not on use.** The same dependency imposes nothing on a pure
   SaaS deployment and a great deal on a shipped binary. Determine conveyance first, or every
   conclusion below is unconditioned and therefore wrong.
2. **Unknown provenance beats strong copyleft for risk.** GPL is a known, manageable constraint. A
   vendored file with no header and no upstream URL is an unbounded one.

## When to use this

- Before any release that leaves your infrastructure.
- Before funding or acquisition diligence — this is the report they will ask for.
- When a dependency was added, upgraded across a major version, or relicensed.
- When a customer or a public buyer requests a licence report or an SBOM.

## When NOT to use this

- You need an opinion on whether something infringes, or you have received a compliance demand from
  a copyright holder. Stop and go to counsel.
- You need to choose an outbound licence. That is business strategy.
- You need vulnerability data. The SBOM is shared, but the analysis is the security reviewer's.
- Patents, trademarks, export control — all out of scope, all separate regimes.

## Procedure

### Step 1 — Conveyance determination

Answer every row before touching a licence. Record the answers as `standard` evidence; every later
conclusion is explicitly conditional on them.

| Question | Effect |
|---|---|
| Does anyone outside the organisation receive a copy? | If not, most obligations of most licences never trigger. |
| In what form: source, binary, container image, app bundle, firmware, published package, model weights? | Container images and app bundles **are** distribution. Teams routinely believe they are not. |
| Is it only accessed over a network? | Network copyleft triggers on interaction; classic copyleft generally does not. |
| Deployed onto customer infrastructure? | On-prem and appliances are distribution however the contract words it. |
| Do you ship an SDK, plugin or library others embed? | Your outbound licence then constrains your users. |

`--conveyance` overrides the derivation. Use it only when you know; a wrong override silently
invalidates the report.

### Step 2 — Resolve the transitive tree

Use the package manager's resolver, not the manifest — the problems are transitive.

```
npm ls --all --json            pip list / poetry show --tree / uv pip list
mvn dependency:tree            gradle dependencies
go list -m all                 cargo tree / cargo metadata
dotnet list package --include-transitive
```

Then scan the **final container image**, not the build stage — the base image brings an OS
distribution with it, and that is where GPL userland tools appear.

Generate or validate an SBOM (`syft`, `cdxgen`, native exporters) in SPDX or CycloneDX. It is the
evidence artefact for this audit and for the SBOM controls in `global-baseline` and `eu`.

If a tool is unavailable, fall back to the lockfile, say so, and mark confidence. Never present a
partial tree as complete.

### Step 3 — Normalise licences

Per component: name, version, declared licence as an SPDX identifier, where the declaration came
from, direct or transitive.

Three classes the tooling reports as fine and are not:

- **Dual/multi-licensed** (`MIT OR Apache-2.0`, `GPL-2.0 WITH Classpath-exception-2.0`) — record which
  option you elect. An unrecorded election is a gap.
- **Metadata disagreeing with the file** — spot-check the highest-risk components by reading the
  actual `LICENSE` in the package.
- **`NOASSERTION` / `UNKNOWN` / empty / custom string** — these are not licences. Count them
  separately; the count is a headline number.

### Step 4 — Reason about compatibility

Classify into families and reason from the obligation conditioned on Step 1. Do not recall a pairwise
matrix. Family table and the eight high-risk patterns: `references/licence-families.md`.

Hunt in this order: strong or network copyleft inside a conveyed proprietary artefact; AGPL anywhere
in a network service including via the runtime image; static LGPL without relink means; Apache-2.0
NOTICE dropped by the build; copyleft assets and fonts; GPL-2.0-only with Apache-2.0; a dependency
that relicensed across a version bump; unknown provenance.

For each conflict state: component, licence, the conveyance that triggers the obligation, the
obligation, and the three options — comply, replace, obtain a commercial licence. **Do not recommend
one.** That is a business and legal decision.

### Step 5 — Provenance of your own code

The riskiest code has no dependency entry: vendored directories, files with no licence header, copied
snippets, AI-generated code without provenance, and contributions from people whose IP assignment you
cannot see. Method: `references/provenance-checks.md`.

### Step 6 — Contributor IP

CLA or DCO — and is it **enforced** by a CI check, or only stated in `CONTRIBUTING.md`? Verify against
actual recent merged commits; squash merges routinely lose DCO trailers. Where a public-sector reuse
obligation applies (the `it` pack), the question inverts: do you hold the rights needed to publish?

### Step 7 — Attribution output

Draft NOTICE content into `.foundry/scratch/<session>/NOTICE.draft` per
`references/notice-generation.md`: grouped by licence, full licence texts where reproduction is
required, copyright lines verbatim, upstream Apache-2.0 NOTICE content propagated, elections
recorded, generation date and SBOM digest.

Then verify **where it must land**: inside the distributed artefact, and reachable from the UI for a
user-facing product. A NOTICE that exists only in the repository does not satisfy a licence requiring
it to accompany the distribution.

`--notice-only` runs Steps 1–3 and 7.

## Output

```
.foundry/blackboard/<wave>/licence-analyst.json    compliance-check.v1[] + finding.v1[]
.foundry/scratch/<session>/sbom.json               generated or validated SBOM
.foundry/scratch/<session>/licence-inventory.md    component table
.foundry/scratch/<session>/NOTICE.draft            attribution draft for human review
```

To the caller: four numbers — total components / with a recognised SPDX licence / conflicting under
the recorded conveyance / unknown provenance — plus the worst conflict in one line and the disclaimer.

## Gates

`--fail-on` makes this usable in CI as a release gate:

| Value | Fails when |
|---|---|
| `copyleft` | a strong or network copyleft component is present in a conveyed artefact |
| `unknown` | any component has `NOASSERTION`, `UNKNOWN` or an empty licence |

A gate is only honest if the conveyance is correct. Wire the conveyance into the CI invocation
explicitly rather than letting it be derived per run.

## Exit criteria

- [ ] Conveyance recorded, every row of the Step 1 table answered.
- [ ] Transitive tree resolved per ecosystem, plus the shipped image where one exists. Uncovered
      ecosystems named explicitly.
- [ ] Four headline numbers stated.
- [ ] Every dual-licensed component has a recorded election or is listed as an open decision.
- [ ] Every conflict names component, licence, conveyance path, obligation, three options.
- [ ] The distributed artefact — not just the repository — checked for NOTICE propagation.
- [ ] Non-code assets (images, fonts, data) inventoried or their absence stated.
- [ ] CLA/DCO enforcement verified against real recent commits.
- [ ] NOTICE draft exists with full licence texts and a generation date.
- [ ] Artifacts pass `mcp__plugin_foundry-core_foundry__contract_validate`.

## Degradation

| Missing | Behaviour |
|---|---|
| `syft` / `cdxgen` | fall back to package-manager output; mark the SBOM control `undetermined` and say the SBOM is derived, not generated by the build |
| A package manager for a present ecosystem | name the ecosystem as uncovered; never imply completeness |
| Container runtime | audit the source tree only and state that the shipped image was not scanned — the most common place AGPL and GPL userland hides |
| Network access | work from local metadata; licence text not present locally is `undetermined`, never assumed from the identifier |

## Deliberately not covered

Infringement opinions · choosing an outbound licence · interpreting a licence in a dispute · patents
and freedom to operate · trademark · export control and sanctions · proprietary vendor contract terms
· whether AI-generated code is copyrightable (reported as a fact pattern, escalated).

## References

- `references/licence-families.md` — families, obligations and the eight high-risk patterns
- `references/provenance-checks.md` — finding code that has no dependency entry
- `references/notice-generation.md` — NOTICE structure and where it must be delivered
