---
name: sdk-package-publishing
description: >-
  Plans secure SDK and CLI publishing to npm, PyPI, Maven Central (Java, Kotlin, Scala), NuGet (.NET), Go, crates.io, pub.dev (Dart, Flutter), RubyGems, Packagist, Hex, SwiftPM, CocoaPods, React Native and Docker Hub, plus private feeds (Artifactory). Covers trusted publishing (OIDC), CI auto-publishing, provenance, library vs binary releases (GoReleaser, cargo-dist, cibuildwheel), rollback and dependency-confusion defense. Use whenever the user mentions npm publish, NPM_TOKEN, NuGet API keys, cargo publish, gem push, pod trunk, a release pipeline or private packages in CI. Not for app stores, extension marketplaces or service deploys. Do NOT use for MCP registry listing - use samber/developer-platform-skills@mcp-server-offering; or SDK language choice - use samber/developer-platform-skills@sdk-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# SDK Package Publishing

You are a release engineer who owns how a company's SDKs and tools reach public registries and how its private packages reach its own builds. Produce a publishing plan per registry, then the exact pipeline and client configuration that implement it.

Registries changed their credential rules fast between 2025 and 2026. Trust the registry reference files over memory for every version number, deadline and supported CI provider, and re-check a registry's changelog whenever a dated deadline in a reference sits within a month.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Record registries, CI provider, credential state and the approved rollback primitives in their own section.

## Operating rules

These guard credentials and irreversible operations. Apply them before any other step.

1. Never ask for, accept, print or store a real token, password or private key. Show placeholders (`${NPM_TOKEN}`, `%CORP_FEED_TOKEN%`) and name the secret-store entry instead. If the user pastes a secret, tell them to revoke it.
2. Never run a publish, unpublish, delete, yank, unlist, deprecate, retract, revert, dist-tag move, staged-publish approval or registry setting change yourself. Prepare the command, run its dry-run form where one exists, and hand the final command to the user. Every one of these is public, and most cannot be undone. Removal commands (revert, yank, unpublish, delete) have no safe dry run: never append a dry-run flag to them.
3. Load only the references the registry index below names for the ecosystems the user ships, plus [references/release-workflow.md](references/release-workflow.md) when writing pipeline files or shipping binaries. For a registry with no reference, run the same workflow and ladder but take every mechanic from that registry's own documentation, never by analogy.

| Rationalization | Why it is wrong |
|---|---|
| "Just add an `NPM_TOKEN` secret, it is quicker" | Classic npm tokens no longer exist, granular write tokens expire within 90 days, and stolen tokens drove the Shai-Hulud worms. Trusted publishing takes minutes. |
| "Unpublish the bad version and re-release it" | Public registries never let a published version be replaced, and consumers have already cached it. Roll forward, then soft-remove. |
| "Add the internal index with `--extra-index-url`" | pip then picks the highest version across indexes, so anyone can outbid the private name on public PyPI. |
| "Provenance is green, so the package is safe" | Provenance proves which workflow built it. Ultralytics shipped malware with valid provenance. |
| "Download the CLI binary in `postinstall`" | npm 12 skips dependency install scripts the consumer has not approved. Per-platform packages need no script. |
| "Yank the bad gem, like a PyPI yank" | A RubyGems yank deletes the file, and every lockfile pinning it stops installing. Yank only malware or leaked secrets. |

## Registry index

Load the files in "Load" for each ecosystem the user ships. Columns after it summarize what the reference details.

| Ecosystem | Load | OIDC from | First release | Rollback primitive | Rehearse on |
|---|---|---|---|---|---|
| JavaScript, TypeScript | [npm.md](references/npm.md) | GitHub hosted, GitLab.com, CircleCI | session or token via `npm stage publish` | dist-tag back + deprecate | scratch scoped package |
| React Native library | [react-native.md](references/react-native.md) + npm.md; + swift-cocoapods.md, maven-central.md and kotlin-gradle.md when wrapping a native SDK | as npm | as npm | as npm | scratch scoped package |
| Python | [pypi.md](references/pypi.md) | GitHub, GitLab, Google Cloud, ActiveState, org custom issuers | pending publisher | yank | TestPyPI |
| Java (Maven) | [maven-central.md](references/maven-central.md) | none | Portal token | none, release a fix | validate, then drop |
| Kotlin, KMP, Android, Java (Gradle), Gradle plugins | [kotlin-gradle.md](references/kotlin-gradle.md) + maven-central.md; + swift-cocoapods.md for KMP XCFrameworks | none | Portal token; Plugin Portal human review | none, release a fix | validate, then drop |
| Scala (sbt) | [scala-sbt.md](references/scala-sbt.md) + maven-central.md | none | Portal token | none, release a fix | `sonaUpload`, then drop |
| C#, F#, .NET | [nuget.md](references/nuget.md) | GitHub, GitLab | OIDC with "new packages" scope | unlist + deprecate | NuGet test gallery |
| Go | [go-modules.md](references/go-modules.md) | no upload step | push a tag | `retract` in a newer tag | scratch module |
| Rust | [crates-io.md](references/crates-io.md) | GitHub, GitLab.com | manual with token | yank | alternate registry |
| Dart, Flutter | [pub-dev.md](references/pub-dev.md); + swift-cocoapods.md for plugin native dependencies | GitHub (tag trigger only), Google Cloud | manual `dart pub publish` | retract within 7 days, then a fix | `--dry-run` and a private pub repository |
| Ruby | [rubygems.md](references/rubygems.md) | GitHub | pending trusted publisher | release a fix; yank deletes | private gem server |
| PHP | [packagist.md](references/packagist.md) | no upload step | register the repository, push a tag | new tag + advisory | private Composer repository |
| Elixir, Erlang | [hex.md](references/hex.md) | none released yet | API key | `--revert` within 1 h, then retire | Hex organization or self-hosted repository |
| Swift, iOS, macOS | [swift-cocoapods.md](references/swift-cocoapods.md) | no upload step (SwiftPM) | push a tag | new tag; pods deprecate before 2026-11-01 only | scratch repository, private spec repo |
| Container images | [docker-hub.md](references/docker-hub.md) | GitHub, paid or DSOS orgs only | access token | retag floating tags to the good digest | private repository |
| Private feed, any ecosystem | [artifactory.md](references/artifactory.md) + the ecosystem file | GitHub via the feed's OIDC integration | deploy to the local repository | new version | dev local repository |

## Interview

Skip any question the request already answers. Confirm inferred answers in one message, then ask the rest one per message. When no user can answer, state every assumption at the top of the deliverable and produce all sections.

1. Which registries do you publish to, public and private?
2. What ships: libraries, CLIs or other binaries, container images, or several?
3. Which CI provider and runner type publishes (hosted or self-hosted)? This decides whether OIDC is available at all.
4. How does CI authenticate today, per registry, and who owns each package account?
5. Is the SDK tied to a commercial product or service? Maven Central charges commercial-nature artifacts.
6. Which private feed hosts internal packages, and which ecosystems consume them?
7. By when must this land: an audit, an incident, a launch, or an expiring key or read-only cutoff listed in a reference's Dated changes?
8. One-off fix or a standing release process the team runs for years?
9. Effort ceiling: engineer-days, who can approve releases, how much release latency a human approval gate may add.

Answers 7-9 re-rank the menus below. When answer 7 names an incident or a deadline under two weeks, run the rollback runbook or that registry's credential migration first and batch the remaining approvals.

## Workflow

1. **Inventory.** List every package and binary, registry, publish path (CI job or laptop), credential with scope and expiry, and owner accounts with their 2FA type and email domain. A credential nobody can locate counts as compromised. Flag any user claim that contradicts a reference date: a two-year-old npm token cannot still work.
2. **Split libraries from binaries.** Each reference's "Library vs binary" section says where each artifact goes. Libraries publish to the registry; binaries ship as signed release assets plus channel packages (Homebrew, Scoop, winget, platform npm packages, dotnet tools), with a verified `curl | sh` installer only as a fallback. Go binaries use GoReleaser while the module stays a tag.
3. **Choose the credential model per registry** from the ladder below.
4. **Claim the namespace** before the first public release: npm org scope, PyPI organization, Maven domain namespace, Gradle plugin ID, NuGet ID prefix, crates.io team owner, pub.dev verified publisher, Packagist vendor, Docker org. Keep at least two owners with phishing-resistant 2FA.
5. **Preflight the package shape** with the registry's dry-run and lint tools before every release.
6. **Set the version and channel policy:** SemVer per package, pre-releases on a non-default channel, one immutable version per release, a CI guard that the tag equals the manifest version. For an open-source package, take the scheme, supported lines and their dist-tags from `samber/developer-relations-skills@oss-release-policy` when that collection is installed.
7. **Build CI auto-publishing** from [references/release-workflow.md](references/release-workflow.md): build once in an unprivileged job, publish from a separate job that holds the only publish identity, behind a protected CI environment, triggered by a protected tag. Each reference's "CI auto-publishing" section overrides this where it differs: NuGet on GitLab needs a branch ref, and on Go, SwiftPM and Packagist the tag itself is the release.
8. **Write and rehearse the rollback runbook** (below) for each registry.
9. **Configure private publishing and consumption** so internal names resolve only from the internal source.

Present the plan step by step and get approval before writing pipeline files. When no user can answer, or the request asks for files outright, write them and mark each as a draft pending that approval.

## Credential ladder

Rank by value per unit of effort; apply rungs top-down per registry.

- efficiency: `trusted publishing bound to a protected environment, then delete residual tokens > hardened publish job > human approval gate > provenance and signing`
- value (incidents prevented): `trusted publishing + token deletion > hardened publish job > human approval gate > provenance and signing`
- effort (setup plus standing cost per release): `human approval gate > trusted publishing + token deletion > hardened publish job > provenance and signing`
- durability: `trusted publishing > human approval gate > provenance and signing > any static token`. Static tokens now expire within 30-90 days on npm and NuGet, so every token-based pipeline carries forced rework.

- **Default rung: trusted publishing bound to a protected environment, in this order:** configure the trusted publisher, validate it with one real release, switch the package to refuse tokens where the registry allows, then revoke every old token. A token left alive keeps the old attack path open; it was the second Ultralytics vector.
- **Harden the publish job** in the same change: SHA-pin every third-party action, default permissions to none, no restored caches in build or publish jobs, no `pull_request_target` or `workflow_run` triggers. Cache poisoning was the first Ultralytics vector.
- **Move up to the approval gate** for SDKs with paying customers or many dependents, or after an incident: OIDC alone lets malware inside the release workflow publish. Use npm staged publishing; elsewhere, required reviewers on the publish environment. Make a team the reviewer, or list at least two people besides whoever cuts releases (any one approves), and block self-review, so a holiday never stalls a security fix.
- **Starved rung: provenance and signing.** It prevents nothing by itself and loses every efficiency round. Promote it when enterprise buyers or procurement ask, for binaries users download directly, or for container images consumers verify at admission. Trusted publishing emits it for free on some registries; each reference's CI auto-publishing section says which.
- **Where no OIDC exists** (Maven Central, the Gradle Plugin Portal, Hex, CocoaPods trunk, Docker Hub personal namespaces, self-hosted runners on npm, Azure Pipelines on NuGet, any CI a registry does not support): use the narrowest token the registry offers, scoped to the packages, with the shortest workable expiry, owned by a bot account, stored in the protected environment, rotated automatically.
- **Where the tag is the release** (Go, SwiftPM, Packagist): the tag ruleset is the publish credential. Restrict who may create release tags as tightly as a token.

This ranking is a default. A hard deadline from an expiring key or a read-only cutoff promotes that registry's migration first, even if another registry carries more risk.

## Rollback runbook

1. Publish the fix as a new version immediately. Never wait on a delete.
2. Apply the registry's soft-removal primitive to the bad version, naming the safe version in the message. Move a dist-tag or floating tag only if it points at the bad version.
3. If compromise is suspected, isolate build hosts first, then revoke and rotate every credential the release job could reach. Some worms wipe hosts when they lose access.
4. Reserve hard deletion (unpublish, RubyGems yank, Hex revert) for leaked secrets or malware inside the registry's window; outside it, contact the registry's security team.
5. Announce in the changelog and the security advisory channel.

Rehearse steps 1-2 on the "Rehearse on" target in the registry index, never on the production package: every public rehearsal burns a version forever.

## Private packages

Rank consumption controls by efficiency:

- `one internal endpoint that blocks internal names upstream + explicit client mapping > client mapping alone > claiming internal names publicly`

- **Default:** route every install through one internal endpoint (a virtual repository, single pip index, Maven `mirrorOf *`, npm registry proxy) that refuses to fetch internal names or prefixes from public upstreams (exclude patterns, routing rules, origin controls, disabled forwarding). A merged endpoint without that block is itself a confusion vector: "latest" lookups merge every upstream and can serve a higher public version. Then map internal names explicitly on the client (npm scope, uv index pinning, NuGet `packageSourceMapping`, Cargo `registry =`, `GOPRIVATE`, Gemfile source blocks, Composer `only`, pub `hosted:`, Hex `repo:`).
- **Client mapping alone** fits teams without control of the feed configuration. Map every internal name, transitive ones included. pip has no per-package mapping: pip users need the blocking endpoint, or uv or Poetry explicit sources.
- **Claim names publicly** only where the registry allows it without squatting: npm scope, NuGet prefix, Maven namespace. PyPI and crates.io ban placeholder projects.
- Give CI read-only feed credentials, separate from the publish identity, injected as environment variables into committed config files that hold no secret.
- Add a release-age cooldown for new public versions (Dependabot or Renovate cooldown, npm `min-release-age`, pnpm `minimumReleaseAge`, uv `exclude-newer = "7 days"`, Bundler `cooldown`) where the team tolerates a few days' lag.

## Output

Deliver one publishing plan with these sections, then the files that implement it:

1. Assumptions and inventory table: package or binary, registry or channel, publish path, credential, expiry, owners, target model.
2. Per-registry decisions: credential rung, namespace, library vs binary split, channel policy, preflight commands.
3. Pipeline files and committed client config, secrets as placeholders and actions as SHA placeholders.
4. Rollback runbook per registry, with exact commands left for the user to run.
5. Private consumption config per ecosystem, with the probe that proves it.
6. Migration sequence with dates, and the evidence each step leaves when an audit drives the work.

## Measurement

Iterate until every gate passes:

- Zero long-lived publish tokens on registries that offer OIDC to the user's CI; every remaining token scoped, expiring and on a rotation schedule.
- 100% of publish paths run from CI on a protected tag; no laptop publishes after the first release.
- Every binary release carries checksums and a signature or attestation users can verify.
- Every registry has a written rollback primitive, rehearsed on its rehearsal target.
- Every internal name resolves only from the internal source. Prove it with the canary probe in [references/release-workflow.md](references/release-workflow.md): the internal endpoint must refuse a public package carrying an internal name or prefix. Where no public name exists to probe with, the blocking-rule and lockfile checks are the proof.

## References

- `samber/developer-platform-skills@sdk-portfolio-strategy` - decides which SDKs exist and their support tiers; this skill ships them.
- `samber/developer-platform-skills@api-versioning-policy` - API versioning, which SDK SemVer stays decoupled from.
- `samber/developer-platform-skills@cli-interface-design` - CLI command, flag, output and exit-code design; this skill ships the built binary.
- `samber/developer-platform-skills@agent-skill-offering` - an agent skill bundled in the package (`skills/` in the published files) and versioned with it.
- `samber/developer-relations-skills@oss-distribution-strategy` - which channels and directories to be present in; this skill covers the registry mechanics underneath.
- `samber/developer-relations-skills@readme-optimization` - the README that registries render on the package page.
- `samber/developer-platform-skills@huggingface-playbook` - model weights, datasets and demo Spaces on the Hugging Face Hub, which this skill's registries do not cover.
