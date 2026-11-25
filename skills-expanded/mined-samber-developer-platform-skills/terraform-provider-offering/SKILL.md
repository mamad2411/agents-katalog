---
name: terraform-provider-offering
description: "Decides whether a SaaS or API platform should ship its own Terraform/OpenTofu provider, then builds and maintains it - API readiness gate, adopting a community provider, resources vs data sources, secrets, import and drift, state upgrades, sandbox acceptance tests, signed releases on the Terraform and OpenTofu registries, versioning and deprecation. Use whenever a vendor mentions building or maintaining a Terraform provider, OpenTofu provider, terraform-plugin-framework, publishing a provider, perpetual diffs in a provider they maintain, or customers wanting to manage the product as infrastructure as code. Not for using or upgrading a third-party provider, nor for modules. Do NOT use for SDK package registries - use samber/developer-platform-skills@sdk-package-publishing."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Terraform Provider Offering

You are a platform engineer who owns a vendor's Terraform/OpenTofu provider. Decide whether the platform should ship one, then make every plan it produces correct and every upgrade survivable.

A provider is a reconciliation client: each run reads the real object and diffs it against configuration. Every gap in the API's semantics becomes a diff users see on every plan, and every schema change becomes an upgrade project for every user. The provider's schema is a second public contract on top of the API.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Record the chosen path, the gate matrix, the resource map, the namespace, the minimum Terraform and OpenTofu versions and the deprecation schedule in their own section, so later releases check against them instead of re-deciding.

## The provider contract

Audit every plan, design and pull request against these rules before anything else.

1. A resource MUST NOT ship while its row in the API readiness gate (step 2) reads FAIL or UNKNOWN, because no Go code fixes an object that cannot be read back or created idempotently.
2. Read MUST set every attribute the API returns, preserve from prior state the ones it never returns, and remove the resource from state when the object is gone, because an attribute dropped on Read is a perpetual diff and a Read that errors on 404 traps users.
3. Removals, renames, incompatible type or default changes, stricter validation, and import-ID format changes MUST ship only in a major, after a minor that deprecates them, because users pin versions and the Registry cannot say who depends on what.
4. Every change to stored state shape MUST ship a state upgrader from every schema version ever released, tested from the last release, because a missing upgrader fails every plan for users on that version.
5. Every release MUST be signed with an RSA key registered on both the Terraform and OpenTofu registries, and never retagged or deleted, because unsigned or mutated versions break `init` and lock files.
6. The provider MUST publish under the vendor's final GitHub organization from its first release, because a later address change forces every user to edit `source` and run `terraform state replace-provider`.

Rationalizations to reject:

| Rationalization | Why it fails |
| --- | --- |
| "Generate it from the OpenAPI spec and ship everything as v1." | Generation solves coverage, not semantics: the spec rarely encodes normalization, sets, write-once fields or propagation delays. Gate each generated resource on its own acceptance tests. |
| "The API doesn't return that field; document the diff." | Users cannot ignore a diff on every plan. Preserve it from prior state, make it write-only if it is a secret, or fix the API. |
| "It's a rename, not a removal, so a minor is fine." | Old configurations still name the old attribute. Rename = deprecate in a minor, remove in a major. |
| "Nobody uses the old schema version, skip the upgrader." | You cannot see who does. One missing upgrade path breaks plans for everyone still on it. |
| "OpenTofu mirrors the Terraform Registry, nothing to do." | It indexes your GitHub releases, but your key is not there until you submit it. Without it, strict users cannot install you. |
| "Ship it under the engineer's account and move it later." | A namespace move is a breaking change for every user. |

## Interview

Ask before designing; each answer changes a later step. Batch questions where possible. When an answer is missing, record the assumption and mark the dependent gate row UNKNOWN.

1. Does a Terraform provider for this API exist already (community, partner, internal)? Its address, license, downloads, open issues, last release, and whether its maintainer responds.
2. What demand is real: deals or security reviews asking for a Partner-badged provider, customers scripting the API in CI, support tickets from community-provider users, customers asking for Pulumi or Crossplane?
3. Which API objects do customers configure once and keep (projects, policies, users, monitors), versus records they create constantly (orders, messages)?
4. API shape, per object: stable server-assigned ID; GET returning every writable field; secrets returned once or never; in-place update (PUT or PATCH); idempotent create; time until readable after create, update and delete; async operations and whether the 202 body carries the object ID; whether collections are ordered and whether list responses keep that order; rate limits; OpenAPI spec and its drift.
5. Who owns the provider: team, Go experience, on-call for its issue queue; is a sandbox account available for tests?
6. Target tier and audience: Partner badge, Partner Premier, OpenTofu users, oldest Terraform and OpenTofu versions customers run? Default to the oldest upstream-supported minor when unknown; write-only arguments need 1.11+ on both.
7. By when must the first release land, is this a one-off launch or a standing product, and what is the effort ceiling? Say which answer moved which rung in step 1: a near deadline keeps the default rungs, a standing product with a Partner target promotes the starved one only when its own promotion condition also holds.

## Workflow

1. Decide whether to ship, and by which path.
2. Gate the API.
3. Map API objects to constructs.
4. Design plan-time behaviour.
5. Choose the build stack.
6. Test against a sandbox.
7. Release to both registries.
8. Version, deprecate, upgrade.
9. Measure.

Run step 2 before announcing a go: the gate can turn "build now" into "fix the API first". Gate matrix, resource map, community-provider audit and first-release plan templates: [references/plan-templates.md](references/plan-templates.md).

## 1. Decide whether to ship, and by which path

Ship when at least two signals hold:

- a community provider with real downloads or issues;
- deals or security reviews asking for a Partner-badged provider;
- long-lived configuration objects (interview Q3);
- customers already scripting the API in pipelines.

A provider also feeds Pulumi (its Terraform bridge) and Crossplane (Upjet-generated providers), so one well-built schema reaches three IaC audiences. Public data does not quantify how much enterprise buying depends on IaC support; weigh your own pipeline evidence, not industry percentages.

Paths, ranked:

- effort: `vendor-owned generated, full coverage > vendor-owned hand-written, core resources > fork-adopt the community provider > transfer-adopt the community provider > support the community provider`
- value (correct plans plus buyer trust): `transfer-adopt > vendor-owned hand-written > fork-adopt > vendor-owned generated > support the community provider`
- efficiency: `transfer-adopt > vendor-owned hand-written > fork-adopt > support the community provider > vendor-owned generated`
- durability: `vendor-owned hand-written > transfer-adopt > fork-adopt > vendor-owned generated > support the community provider`

- **Default rung, community provider whose schema passes the audit, maintainer cooperates: transfer-adopt.** The repo moves into your organization; users keep their schema and state shape but still change the provider address.
- **Maintainer silent after a stated, announced time box: fork-adopt**, if the repo carries an OSI license file (a repo without one cannot be forked). Same address change for users, but you start without the original key, release history or the old address.
- **Default rung, no usable community provider: vendor-owned hand-written** covering the five to fifteen objects customers configure most, on the Plugin Framework.
- **Support the community provider** (contribute fixes, fund or co-maintain) only as a bridge while the API fails the gate or headcount is missing. It earns no Partner badge and depends on a volunteer.
- **Starved: vendor-owned generated, full coverage.** Highest coverage, highest effort and the worst durability, because generated schemas inherit every gap in the spec. Promote it when the API has well over a hundred resource types and the spec carries semantics (sensitive, write-only, sets, normalization, async) as vendor extensions; keep a hand-owned override layer either way.

The Official tier belongs to HashiCorp's own namespaces. Partner, then Partner Premier, is the highest badge a vendor earns. Partner requires the Technology Partner Program, the Plugin Framework, nightly acceptance tests in GitHub Actions, and fixing critical issues within 48 hours and others within 5 business days; size interview Q5 against that commitment. When Partner is a target (Q6) and the adopted provider is on SDKv2, schedule the mux migration of the core resources before the badge request: it moves both adopt rungs up the effort line.

## 2. Gate the API

Score every row per object as PASS, FAIL, UNKNOWN or COMP (compensation below accepted). A resource ships only when its rows read PASS or COMP; UNKNOWN counts as FAIL until answered.

| Check | Failure users see | Provider-side compensation |
| --- | --- | --- |
| Stable server-assigned ID | import, `moved` and identity impossible | none - fix the API |
| GET returns every writable non-secret field | perpetual diff | preserve from prior state, document undetectable drift |
| In-place update for mutable fields | edits destroy and recreate the object | `RequiresReplace`, documented |
| Idempotent create | retried creates leave untracked duplicates | synchronous: no client retry on create, or look up by a unique name before retrying; async: none - fix the API |
| Bounded propagation after create, update, delete | 404 after create, "inconsistent result after apply" | bounded waiters |
| Pollable long operations, object ID in the 202 body | applies hang, time-outs orphan objects | none without the ID - fix the API |
| Deterministic normalization and ordering | diff on every plan | normalize in the provider; sets for unordered collections |
| Secrets identified | secrets stored in state in plaintext | write-only or sensitive, per step 4 |
| Documented rate limits | 429 storms at Terraform's default parallelism of 10 | client-side throttling and `Retry-After` handling |

Route idempotency-key design to `samber/developer-platform-skills@api-idempotency-retry` and quota design to `samber/developer-platform-skills@api-rate-limit-policy`.

## 3. Map API objects to constructs

- Fill the resource map: one row per API object with its construct, ID and import grammar, mutable versus replace-only fields, secrets, ordering, and consistency class.
- Resources for configured objects; singular and plural data sources for lookups; leave transactional records out.
- Construct order, by value per unit of effort: `resources with import > data sources > write-only arguments for input secrets > ephemeral resources for tokens > resource identity plus list resources > actions > provider functions`. Skip a rung that has no matching API object and write why.
- Partner Premier promotes identity plus list resources, ephemeral resources or actions: it requires at least one of them, plus an SBOM.
- List resources and actions are Terraform-only; identity import works on Terraform and OpenTofu 1.12+. Every resource still imports by plain ID for older binaries.

Mapping table, data-source rules, naming and version gates per construct: [references/resource-design-rules.md](references/resource-design-rules.md).

## 4. Design plan-time behaviour

Apply each rule to each resource in the map and record which ones apply.

- Read sets what the API returns, preserves what it never returns, and removes the resource on not-found; Delete treats already-gone as success.
- Preserved and API-generated-once fields are null after import: list them, and only them, in `ImportStateVerifyIgnore`. Document that a preserved field shows an update on the first plan after import until the user sets it, and that an API-generated secret stays null after import, recoverable only by replacing the resource.
- `RequiresReplace` only where the API cannot update; `UseStateForUnknown` on stable computed values.
- Validators so bad input fails at plan, not mid-apply.
- Secrets, keyed on who creates the value:
  - user supplies it, API never returns it: write-only argument plus a `<name>_wo_version` trigger. If the minimum version is below 1.11, ship a `Sensitive` attribute beside it and steer users with `PreferWriteOnlyAttribute`.
  - API generates it and returns it once: `Sensitive` computed attribute set at create, preserved on Read, null after import, documented as stored in state.
  - short-lived token another resource consumes: ephemeral resource.
- Eventual consistency: diagnose the class, then bounded waiters on typed errors after create, update and delete; never retry broad error classes.
- Configurable timeouts for long operations; no write calls at provider configure time.
- Credentials: Optional attributes, environment fallback, unknown-value guards, eager validation skipped when values are unknown.

Rules, retry windows and failure strings: [references/resource-design-rules.md](references/resource-design-rules.md).

## 5. Choose the build stack

- Plugin Framework, protocol 6, for anything new; HashiCorp recommends it for new functionality, and newer constructs exist only there. Existing SDKv2 providers migrate one resource at a time behind a mux, core resources first.
- `terraform-plugin-testing` for acceptance tests, `tfplugindocs` for docs, GoReleaser for releases.
- Code generation: HashiCorp's OpenAPI generator is a tech preview that produces schemas only, not CRUD; commercial generators produce full providers. On the hand-written path, generate schema and models only for simple synchronous objects from a curated spec; keep CRUD for async or eventually consistent objects hand-owned.
- Build on the platform's Go SDK if one exists, so the provider inherits its retries, pagination and auth.

## 6. Test against a sandbox

- Per resource: `_basic` with import verification, `_disappears`, an update test per mutable attribute, a replacement test per replace-only attribute.
- The harness already fails any step whose post-apply plan is not empty. Never set `ExpectNonEmptyPlan` to turn CI green; a PR that adds it links an API bug.
- Upgrade tests: apply with the last released version, plan with the new build, expect no changes.
- Import config generation: run an import block with `-generate-config-out` and validate the generated HCL.
- A dedicated sandbox account (designed with `samber/developer-platform-skills@api-test-mode-design`), prefixed test objects, sweepers before and after each nightly. Add a `tofu` lane.

Test catalogue, cadence table, address-change upgrade test and fork-PR credential rule: [references/acceptance-testing.md](references/acceptance-testing.md).

## 7. Release to both registries

Low freedom: the registries reject anything that deviates.

1. Public repo `<org>/terraform-provider-<name>`, lowercase, in the final organization.
2. `terraform-registry-manifest.json` with protocol `6.0` (Framework) or `5.0` (SDKv2).
3. An RSA signing key (the Registry rejects GnuPG's default ECC key), stored as CI secrets.
4. GoReleaser config and a tag-triggered workflow copied from HashiCorp's framework scaffolding.
5. Rehearse with a local GoReleaser snapshot build, then a prerelease tag (`v0.1.0-beta1`): range constraints never select prereleases.
6. Register provider and key on registry.terraform.io; submit provider and key through the `opentofu/registry` issue forms the same day.
7. Tag `vX.Y.Z` from the default branch; verify `terraform init` and `tofu init` on a clean machine.

Exact asset names, config fields, key commands and the namespace-move procedure: [references/release-pipeline.md](references/release-pipeline.md).

## 8. Version, deprecate, upgrade

- Semver per HashiCorp's provider guidelines, checked against one test: does an unchanged configuration plus existing state produce a diff, an error or a different object after upgrading? Yes means major.
- Majors at most once a year, staged behind an opt-in beta, each with an upgrade guide.
- Deprecate with an actionable `DeprecationMessage` in a minor; remove in the next major.
- Rename resource types with a state mover so users write `moved` blocks, never imports.
- An address change (adoption) is already one migration: keep the schema compatible across it and owe upgraders from the previous maintainer's schema versions.
- Align the provider's promise with `samber/developer-platform-skills@api-versioning-policy`: an API field sunset becomes a provider deprecation one minor ahead.

Bump table, rename recipes, changelog template and the major-release runbook: [references/versioning-and-deprecation.md](references/versioning-and-deprecation.md).

## 9. Measure

The provider passes when all hold:

- Every resource's acceptance suite passes with no `ExpectNonEmptyPlan`.
- Upgrade tests from the last release of each supported major pass.
- Both `terraform init` and `tofu init` with `OPENTOFU_ENFORCE_GPG_VALIDATION=true` install the latest version.
- No removal has shipped in a minor since 1.0.0.

Track over time: Registry downloads per major (who is stranded), open issues reporting a perpetual diff or "inconsistent result after apply" (none older than a release cycle), nightly flake rate per resource, and deals or reviews where the provider tier came up.

## Failure modes

- Generated full-coverage rewrite shipped as a major -> broken resources for months; gate each resource on tests, keep the previous major supported.
- A popular resource split into many in a major -> users forced into mass imports; ship new types beside the old one and offer `moved`.
- New default that differs from the API -> diff on every existing object; defaults match the API or stay unset.
- Side effects at provider configure -> fails under least-privilege credentials; move them into resources.
- Acceptance tests in a production org, or on fork PRs with secrets -> data loss or credential theft; sandbox plus approval gate.

## Invocation examples

- "Customers keep asking for Terraform support. Should we build a provider, and what goes in v1?"
- "There's a community Terraform provider for our API with 2M downloads and a silent maintainer. Should we take it over?"
- "Set up signed releases for our provider on the Terraform Registry and OpenTofu."
- "We need to rename `acme_widget.color` and change `tags` from a list to a set without breaking users."
- "Our provider shows a diff on `api_key` every plan."

Expected output: the go/no-go with the chosen path and which interview answer moved it, the gate matrix, the resource map, plan-time rules per resource, the test plan, the release checklist, the first-release plan, and the versioning and deprecation schedule.

## References

- `samber/developer-platform-skills@api-integration-surface-strategy` - choosing among all integration surfaces; this skill starts once an IaC surface is on the table.
- `samber/developer-platform-skills@sdk-package-publishing` - registry mechanics for the platform's SDKs and CLI binaries, not the provider.
- `samber/developer-platform-skills@public-api-design-review` - auditing the API surface behind FAIL rows in step 2.
