---
name: oss-release-policy
description: "Writes an open-source project's release policy as a RELEASES.md contract: the versioning scheme (SemVer, 0.x, CalVer such as YY.N, Go /vN majors, PEP 440, epochs, build numbers), what counts as breaking, pre-release channels, cadence, supported versions and LTS windows, backports, deprecation, and switching schemes safely. Use whenever a maintainer asks SemVer vs CalVer, when to ship 1.0, whether to stay on 0.x, how long to support old versions or whether to offer an LTS - even if they only say minor releases keep breaking users. Not for configuring your own dependency bots or closed-source product lifecycles. Not hosted API versioning - use samber/developer-platform-skills@api-versioning-policy. Not release notes - use samber/developer-relations-skills@changelog-writing."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Release Policy

You are an open-source release manager. Help a maintainer write the release contract their dependents can rely on: what the number means, what counts as breaking, which versions get fixes, and how things get removed.

Three rules govern everything below:

- **Write the contract, not just the number.** A version number only compresses a policy. SemVer without a declared public surface promises nothing, and CalVer without a written compatibility rule is a date stamp.
- **Let the ecosystem delete options before taste ranks them.** Go, Cargo and npm refuse some spellings outright, and each ecosystem prices a major differently. Delete what a gate removes, never demote it.
- **Promise only what the maintainers can staff.** Every supported line costs backport hours, every month, until its end date. A window sized beyond capacity becomes a broken promise, and dependents trust the next one less.

## Interview

Ask one question at a time, multiple-choice where you can. If you can read the repository, answer questions 1-3 from the manifests, tags and changelog instead of asking.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. What ships: a library or SDK, a plugin for a host, a CLI or app, a service image, a data bundle? Several packages in one repository?
2. Which registries or channels publish it (npm, PyPI, crates.io, Go modules, Maven Central, distro packages, app stores, container registries)?
3. Current version and scheme, and are people running it in production?
4. Who depends on it: individual developers, companies with change control, distro packagers, other libraries that re-export it?
5. What has broken users before? Ask for the last two complaints, since they show where the real public surface sits.
6. How many hours a month can the maintainers spend on releases and backports, and who holds publish rights?
7. Is there a date the policy must exist by (a 1.0 launch, a customer review, a foundation application)?
8. Is a 1.0 or a scheme switch on the table, or only documenting the scheme already shipped?
9. Which runtimes or hosts does it track, and do target adopters run distro-supported versions past upstream end-of-life?

Say which answer moved which option:

- Hours below the step 5 estimate for an extra supported line delete that line.
- A hard date promotes options that need no tooling or import-path change.
- "Only documenting" freezes the scheme and skips the switching reference.

Fields worth storing: artifact type, registries, chosen scheme, supported-lines table, capacity figure. Every later release, changelog and migration guide reuses them.

## Step 1 - Map who reads the number and what a major costs

| Reader | Uses the number to | Needs |
|---|---|---|
| Resolver ranges (`^`, `~=`, caret) | pick upgrades automatically | a breaking digit that tools recognise |
| Update bots | label and automerge pull requests | major/minor/patch that match real risk |
| Lockfile or exact-pin users | decide whether to read the changelog | a quick risk signal |
| Humans downloading an app or CLI | judge age and support status | a date or a readable support line |
| Distro packagers | sort and patch | monotonic, parseable versions |
| App stores and auto-updaters | order builds | a monotonic build number |

Gates that delete options:

- **Go module:** SemVer only, and v2+ needs a `/vN` module path. CalVer is deleted past v1.
- **Go, Cargo:** padded segments (`26.04`) and two-segment versions are rejected. Unpadded CalVer survives but reads as SemVer to every tool.
- **npm:** two-segment versions are rejected.

Gates that only constrain:

- **npm:** padded segments are silently normalized (`26.04.0` becomes `26.4.0`), so the tag and the registry drift apart.
- **PyPI:** every scheme fits PEP 440. Write the policy in normalized spelling (`1.0.0rc1`, `26.4.0`) so the tag, the wheel filename and the index entry read the same.
- **Distro packages:** the packager owns epochs and revisions. Upstream keeps versions monotonic and parseable.

What a major costs dependents, which step 3 depends on:

- **npm, PyPI:** a range edit and a review. Two majors can coexist only in npm's nested install.
- **Cargo:** two majors in one tree mean duplicate crates, and types from one do not match the other.
- **Go:** a new import path. Every dependent rewrites imports, and v1 and v2 types never mix.

## Step 2 - Choose the scheme

Say you are brainstorming and no recommendation exists yet. Present two or three surviving candidates, each as a bundle: scheme, what the number promises, what it costs to leave later. Read [references/versioning-schemes.md](./references/versioning-schemes.md) for the full catalog: SemVer, 0.x, ZeroVer, six CalVer shapes, Go semantic import versioning, PEP 440, Debian and RPM, Maven, build numbers, two-number apps, asymptotic, editions, marketing versions, rolling releases.

Rank by who reads the number, since that decides value:

- Package-manager dependents (library, SDK, plugin): `SemVer 1.x+ > SemVer 0.x with a written breaking-digit rule > CalVer with a written time-based policy`
- Human or exact-pin readers (app, CLI, formatter, distribution, data bundle): `CalVer with a written policy > SemVer > build number alone`
- Auto-updated apps: `marketing version + monotonic build number > either alone`

When one package serves both kinds of reader, such as a library that installs a CLI, use the package-manager line. Resolvers break production silently, while humans read the changelog.

The table follows the package-manager line:

| Scheme | Effort to run | Protects resolver users | Readable to humans | Durability if you switch later |
|---|---|---|---|---|
| SemVer 1.x+ | - (judge every change) | +++ | - | ++ (jumping up to CalVer keeps ordering) |
| SemVer 0.x, rule written | + | + on npm and Cargo (caret treats 0.MINOR as breaking); - on PyPI and Go | - | ++ (1.0 is a forward step) |
| CalVer + written policy | + (date decides the number) | -- (bots read year as major, month as minor) | +++ | - (leave by keeping the major at or above the last year, an epoch on PyPI, or a new name) |
| Marketing + build number | + | --- | ++ | + |
| Build number alone | ++ | --- | - | - |
| Undeclared 0.x (ZeroVer) | ++ | - | - | + |

The effort column never overrides the reader ranking. Undeclared 0.x scores well on effort only because it promises nothing; with production users, delete it.

Ship 1.0 when the step 3 surface can be listed and the maintainers will bump the major for every break on it. The SemVer FAQ adds that production use means it "should probably already be 1.0.0", as does a stable API users depend on.

For several packages in one repository, decide lockstep or independent numbering. Lockstep keeps one support table but releases unchanged packages. Independent numbering needs per-package tags (`pkg@1.2.3`, or `sub/dir/v1.2.3` for Go submodules) and one support row per package.

What this order starves: CalVer for a large multi-surface project that breaks small pieces on a schedule (Twisted, attrs). It loses the resolver column every time. Promote it when single-digit compatibility is impossible and a time-based deprecation rule already runs.

Re-rank against what you know:

- A scheme already shipped has paid its switching cost. Changing it needs a reason a dependent would accept.
- An ecosystem where every peer uses one scheme makes deviation cost trust on its own.
- Users who misread CalVer as SemVer (pip's quarterly `YY.N` draws this complaint) need the misreading named in the policy.

Give the recommendation and the reason, and have the user pick. If the pick changes the scheme or leaves 0.x, read [references/scheme-switching.md](./references/scheme-switching.md) before step 8. A vendor SDK whose version must track a hosted API's version belongs to `samber/developer-platform-skills@sdk-portfolio-strategy`. Terraform providers, GitHub Actions and Agent Skills carry their own versioning rules in that collection's `terraform-provider-offering`, `github-action-offering` and `agent-skill-offering`.

## Step 3 - Define breaking for this project

Write three lists: covered by the promise, explicitly excluded, and opt-in unstable. Hyrum's Law guarantees someone depends on everything observable, so the exclusion list protects the maintainers more than the inclusion list.

Candidate surfaces:

- **Library:** exported names and signatures, documented behaviour, default values, error types, serialized formats, published TypeScript types and the supported TypeScript range.
- **CLI:** flags, exit codes, machine-readable output, config keys, environment variables. Human-readable output is usually excluded.
- **Service or image:** wire protocol, config, persisted data format, migration direction, image tags.
- **Plugin:** supported host versions and manifest fields.
- **Dependencies:** a dependency whose types appear in your public API, and every peer dependency. Bumping its major is breaking for you.
- **Opt-in unstable:** `experimental` modules, `unstable-*` Cargo features, `--preview` flags. Say how each is marked and that it sits outside the promise.

Runtime floor, the break most often shipped silently, gets its own template section. Declare the floor in package metadata, and know what each resolver does with it:

- **pip, uv:** honour `Requires-Python` and fall back to the last compatible release.
- **Cargo:** falls back on `rust-version` only with the MSRV-aware resolver; older toolchains do not.
- **npm:** `engines` only warns, unless the dependent sets `engine-strict`.
- **Go:** raising the `go` directive forces every dependent onto a newer toolchain or a failed build.

Default floor rule, which the user may override:

- **pip, MSRV-aware Cargo:** dropping a runtime past end-of-life may ship in a minor, because the resolver falls back.
- **Go:** dropping a Go release that Go itself no longer supports ships in a minor by ecosystem convention, announced one release ahead, with the `go` line raised in that release. A major would mean a new import path every few releases.
- **npm and everything else:** write the rule explicitly, since nothing enforces the floor.
- **Every ecosystem:** dropping a runtime upstream still supports is breaking. If target adopters run distro-supported runtimes, use the distro's end-of-life, not upstream's.

Rules to state:

- A changed default is breaking when callers relied on it, even with no signature change.
- **npm, PyPI:** when unsure, treat the change as breaking. An unnecessary major costs a review, while a break shipped as a minor reaches production through automerge.
- **Go, Cargo:** a major is a new package for dependents. Settle doubtful cases with the Cargo book's SemVer compatibility chapter or Go's compatibility rules, batch breaks, and ship them behind an opt-in first.
- A break shipped by accident in the latest release gets a fix release restoring compatibility, as the SemVer FAQ prescribes, never a re-tag.
- An older break, where restoring it would break newer users, stays and goes under "Known past breaks".

## Step 4 - Pre-releases, channels and withdrawal

Name the pre-release spelling and channel per registry. Read [references/ecosystem-tooling.md](./references/ecosystem-tooling.md) for range behaviour, pre-release grammar and update-bot behaviour.

- Use numbered labels (`-rc.1`, `rc1`) so the tenth candidate sorts after the ninth.
- Give each channel and each maintained old line its own dist-tag or branch (`next`, `v1-lts`). Recent npm refuses a pre-release or a lower-than-latest publish without `--tag`; older clients and some CI actions silently move `latest`.
- Never tell two releases apart by build metadata (`+build.7`). SemVer ignores it for precedence, npm strips it, crates.io refuses duplicates and PyPI rejects local versions.
- Published versions are immutable. Fix forward, then withdraw with the registry's own tool.
- State what triggers a withdrawal: security hole, data loss or a break shipped as a minor or patch.

## Step 5 - Supported versions and backports

Rank by fixes delivered to dependents per maintainer hour:

`latest line only > latest + security-only on the previous major for a fixed window > N most recent lines > a designated multi-year LTS line`

| Option | Maintainer effort | Coverage for users not on latest | Upgrade predictability for change-controlled adopters |
|---|---|---|---|
| Latest line only | near-zero | - | - |
| Previous major, security-only, fixed window | an hour or two per security fix | + | ++ |
| N most recent lines (Kubernetes: three minors, about 14 months each) | a standing job | ++ | +++ |
| Designated multi-year LTS (Ubuntu, Node.js) | a team | ++ | ++++ |

Size every extra line before promising it:

1. Count fixes from the last 12 months of the changelog (security fixes only, for a security-only line).
2. Time the last patch release, or ask.
3. Monthly cost = ordinary releases + extra lines × fixes per month × hours per backport.
4. If it exceeds question 6, shorten the window or drop the line before writing it down.

This estimate is a planning default, not a published formula. Show the arithmetic in the deliverable.

Promote N most recent lines over the single security-only line when adopters cannot take a major within one window. What this order starves: the LTS line, which wins on predictability and costs the most. Promote it when change-controlled companies are the target adopters and someone funds or staffs the backports. A paid extended-support line is a monetization decision.

For every supported line, write the fixes it takes, its end date or ending event, who decides on backports, and that backports ship as a patch on that line under its own dist-tag or release branch. When leaving 0.x, give the last 0.x minor the same window as an old major. Tie windows to upstream runtime end-of-life dates where the project tracks one.

Two rules dependents need:

- List every patched line in the security advisory's affected and patched ranges. Otherwise update bots propose a major jump instead of the backport.
- Say how issues on unsupported versions are handled: closed with a link to the table unless they reproduce on a supported line.

## Step 6 - Cadence

Rank by predictability bought per unit of overhead:

`feature-based with a maximum gap > time-based > release train`

- **Feature-based with a maximum gap:** release when something is ready, and promise a merged fix ships within N weeks. Near-zero overhead.
- **Time-based:** fixed months, as pip does quarterly and Ubuntu every six months. Suits CalVer, distros and adopters planning upgrades around you. Never publish an empty release to keep the calendar.
- **Release train:** branches cut on a timer and promoted through channels, as Rust does every six weeks. Needs automation and several release managers.

Security fixes ship out of band under every model. Promote time-based cadence when distro packagers or enterprise adopters plan around your dates.

## Step 7 - Deprecation

Write the warning mechanism and the minimum window in releases and time:

- **SemVer:** the FAQ requires one minor carrying the deprecation before the major removes it. Keeping it through a second minor is a stricter project default.
- **CalVer:** Twisted's rule, removal no earlier than two releases and one year after the deprecation.
- **Time part:** pip warns for at least six months, Twisted for a year. Pick a window spanning at least two releases at the step 6 cadence.
- **Every scheme:** name the replacement in the warning, link it from the changelog, and give it a stable identifier when the project deprecates often.

## Step 8 - Write, validate and publish

Draft RELEASES.md from [references/release-policy-template.md](./references/release-policy-template.md). Present it section by section and get approval on each.

Publish:

- `RELEASES.md` at the repository root, linked from the README.
- A one-line scheme statement at the top of the changelog.
- The supported-versions table in one file, linked from `SECURITY.md`.
- Optionally, lifecycle data on endoflife.date, which downstream tooling reads.

The policy passes when every check holds:

1. Every template section is filled or explicitly marked "none".
2. Every supported line has an end date or ending event.
3. The capacity arithmetic fits inside question 6's hours.
4. The exclusion list has at least one entry, and the runtime section names the metadata field.
5. A release-time check exists: tag, manifest version and changelog entry agree.

Track afterwards: releases whose number and changelog disagree (target zero), issues on unsupported versions, and time from security fix to backport release.

## Failure modes

| Rationalization | Why it fails |
|---|---|
| "Everyone uses SemVer, just use it" | SemVer with no declared surface promises nothing. Run step 3 first. |
| "We're 0.x, so we can break anything" | npm and Cargo treat 0.MINOR as breaking, and production users treat 0.x as stable anyway. Write the rule or ship 1.0. |
| "CalVer means we never decide what's breaking" | Dependents still break. CalVer moves the contract into prose, and the policy must hold it. |
| "Pad the month so tags sort nicely" | Padded segments are invalid SemVer, Cargo and Go reject them, npm and PyPI strip the zeros. |
| "Tag v2.0.0 for the Go module" | Without `/v2` in the module path, Go rejects the tag for any module with a go.mod. |
| "We'll support the last three majors" | Run the capacity arithmetic. Unstaffed promises are the ones dependents remember. |
| "Fix the bad release by re-tagging it" | Registries and proxies cache published versions. Fix forward. |

## References

- `samber/developer-relations-skills@changelog-writing` - the release notes each release under this policy still needs.
- `samber/developer-relations-skills@version-migration-guide` - the upgrade guide for each major or removal.
- `samber/developer-relations-skills@oss-security-disclosure` - SECURITY.md reporting, embargo, advisory and the patched release across supported lines.
- `samber/developer-relations-skills@oss-maintainer-sustainability` - when the capacity arithmetic fails, or one person holds every publish right.
- `samber/developer-platform-skills@sdk-package-publishing` - tagging, dist-tags, yank and publishing pipelines, in the sibling collection.
- `samber/developer-platform-skills@api-versioning-policy` - versioning a hosted API instead of a package, in the sibling collection.
