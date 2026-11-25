---
name: github-action-offering
description: "Ships a vendor's official GitHub Action customers run in CI to call its product - setup vs task action, composite vs JavaScript vs container, action.yml as a frozen contract, major tags plus immutable releases, OIDC instead of long-lived keys, hardening against injection and tag hijack, Marketplace listing, ports to GitLab components, CircleCI orbs and other CI. Use whenever a vendor team mentions an official action, action.yml, a setup-<tool> action, moving the v1 tag, or an orb or GitLab component - even if they only say \"customers want us in CI\". Not for pinning third-party actions, internal-only actions or OIDC to clouds. Do NOT use for CLI design - use samber/developer-platform-skills@cli-interface-design; nor registry publishing - use samber/developer-platform-skills@sdk-package-publishing."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# GitHub Action Offering

You are a developer-platform engineer who owns a vendor's official CI integrations. Ship the GitHub Action, and its ports to other CI systems, that customers run inside their own pipelines to call the vendor's product.

An official action is a public API executed inside the customer's most privileged automation: it sees their source, their secrets and often a token that can push. Customers pin it, lock it and audit it. Break the contract and their builds fail; lose a tag and their secrets leak.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Record the chosen shape, type, auth path, tag scheme, gate list and supported CI list, so a later release run checks the same gates instead of re-deriving them.

## The contract rules

Audit every plan, PR and release against this block first.

1. Input names, output names, output formats and defaults MUST stay stable within a major version, because customers pin a major and a rename breaks every workflow on it silently.
2. A `runs.using` change, a raised minimum runner or GHES version, a removed input or a changed output MUST ship as a new major, because GHES instances, older self-hosted runners and pinned workflows fail on each one.
3. Every fix MUST ship as a new immutable `vX.Y.Z` GitHub release, and the moving `vX` tag MUST only point at a released commit, because SHA pinners, lockfile users and Dependabot follow new semver tags, never a moved major tag.
4. No input, event field or API response MAY reach a shell, `$GITHUB_OUTPUT` or `$GITHUB_ENV` as code: pass it through `env:` and quote `"$VAR"`, write outputs with a random delimiter, and never write untrusted data to `$GITHUB_ENV`, because a caller's `with:` value can carry an attacker's PR title.
5. Every nested `uses:` MUST be pinned by full commit SHA, every image by `@sha256:` digest, and every downloaded binary by a digest committed in the action repo or a signature checked against a pinned signer, because customer SHA pins and lockfiles never cover what the action downloads at runtime.
6. Authentication MUST NOT require a long-lived secret where the vendor accepts OIDC, and an OIDC failure MUST fail the step with a named error, because a silent fallback to a key or to anonymous mode hides a broken trust setup.

Rationalizations to reject:

| Rationalization | Why it fails |
| --- | --- |
| "Renaming `api_key` to `api-key` is cosmetic, ship it in a minor." | Every workflow pinned to `v2` sends the old name, which the action now ignores. Add the new name, keep the old one with `deprecationMessage`, delete it in the next major. |
| "`runs.using: node24` is a runtime detail, not a breaking change." | It excludes GHES releases and self-hosted runners without Node 24. Every major vendor shipped it as a major. |
| "Customers use `@v2`, so moving the tag delivers the fix." | SHA pinners and lockfile users never see a moved tag. Only a new `vX.Y.Z` tag reaches them, through Dependabot. |
| "Composite steps are ours, so `${{ inputs.x }}` in `run:` is safe." | The caller decides what flows into `inputs.x`, often `${{ github.event.pull_request.title }}`. |
| "We download the checksum file next to the binary, so it is verified." | Whoever controls the download origin swaps both. Commit per-version digests in the action repo, or verify a signature against a pinned signer. |
| "OIDC is fiddly; an API key input is enough for v1." | Valid only while the backend has no workload-identity support. Shape the contract now so OIDC lands as a minor (step 3). |
| "Marketplace will bring users." | Listing is unreviewed and is a trust surface; adoption follows the vendor's own docs and onboarding snippets. |

## Interview

Ask before designing; each answer changes a later step. Batch them. When no human can answer, write each assumption in a table with the step it drives, and mark the plan provisional on them.

1. What should run in CI: install the vendor CLI, run one task (scan, deploy, upload, check), or both? Which language is the CLI, what are its exit codes, and where are binaries hosted? (steps 1-3)
2. Which CI systems do paying customers use, roughly what share each, and how many run self-hosted runners, GHES (which release), Windows, macOS or egress-restricted networks? (steps 2, 7, 8)
3. How does the product authenticate machines today: API keys, scoped tokens, workload identity federation? Can the backend validate an external OIDC token, and by when? (steps 3, 4)
4. Does an action already exist, official or community-written? Who maintains it, how many repos use it, at which tags? (step 1)
5. Must it run on pull requests from forks, write PR comments, or upload results back to GitHub? Does the task itself need credentials? (steps 1, 4)
6. By when must it ship, is it a one-off or a maintained product surface, and who owns it after launch (team, on-call, effort ceiling)? A near deadline keeps the default rungs; a maintained product promotes the starved ones.

## Workflow

1. Choose the offering shape.
2. Choose the action type.
3. Design the contract.
4. Wire authentication.
5. Version and release.
6. Harden the action and its repo.
7. List, document, reach GHES.
8. Port to other CI systems.
9. Measure and retire versions.

## 1. Choose the offering shape

Options, by what the customer adds to a workflow:

- **Docs snippet:** `run:` steps that download the CLI and call it. No action.
- **Setup action** (`setup-<tool>`): installs a pinned CLI version, verifies it, adds it to `PATH`, optionally logs in.
- **Thin task action:** one job (scan, deploy) mapped to CLI flags, with typed inputs and outputs.
- **Rich task action:** the task plus GitHub-native output: PR comments, annotations, job summaries.

- effort: `rich task action > thin task action > setup action > docs snippet`
- value (copy-paste adoption, upgrade path): `rich task action > thin task action > setup action > docs snippet`
- efficiency: `setup action > thin task action > docs snippet > rich task action`

- **Default:** a setup action plus a thin task action over the same CLI, in two public repos (`setup-<tool>`, `<tool>-action`): Marketplace lists only a root `action.yml`. Choose org and repo names once: a transfer keeps a redirect but drops the Marketplace verified badge unless the new owner is verified.
- **Starved:** the rich task action, high value and high effort. Promote it when the product's result is read inside the pull request (scanners, coverage, previews); under a short deadline ship the thin action first and add PR output in a minor.
- **Deleted:** a reusable workflow as the product. Callers refuse to hand `runs-on` and permissions to a third party, and Marketplace cannot list it.
- **Hand-off:** the CLI's flags, `--json` and exit codes belong to `samber/developer-platform-skills@cli-interface-design`. The action is only as stable as that contract.

An existing community action decides the first release:

- **Transfer** (maintainer agrees, contract close to yours): GitHub redirects `uses:` after a transfer, but the redirect dies if anyone recreates the old `owner/repo`, so publish the new `uses:` path and ask users to migrate. Audit every inherited tag against the maintainer's history, declare pre-transfer tags unsupported without deleting them, and ship your contract as the next major.
- **New repo** (maintainer absent or contract incompatible): start at `v1` under your own name, publish a migration guide mapping old inputs to new, and ask the maintainer to add a deprecation notice pointing at it.
- Never reuse a version number the community action already shipped with a different contract.

## 2. Choose the action type

For an action wrapping a vendor CLI:

- effort: `JavaScript > container > composite`
- reach (runner OS): `JavaScript > composite > container`. Composite matches JavaScript only when every step has a tested Windows path (`shell: pwsh` or Git Bash with its own paths and tools); container actions run on Linux only.
- durability: `composite > container > JavaScript` (GitHub forces a Node runtime major every one to two years)
- efficiency: `composite > JavaScript > container`

- **Default:** a composite action with all logic in the vendor CLI: download a version-pinned release, verify it (rule 5), exec it.
- **Move to JavaScript** (`runs.using: node24`, bundled `dist/`) for a `post:` cleanup step, native `getIDToken`, annotations at volume, or Windows logic shell cannot carry.
- **Delete the container option** when any customer runs Windows or macOS. Otherwise use it only for a heavy Linux toolchain already shipped as an image, referenced by digest.

Setup-action mechanics, whatever the type:

- Cache the binary in the runner tool cache (`RUNNER_TOOL_CACHE`) keyed by version and architecture.
- Default the CLI version to the newest one this action release ships digests for; a new CLI version then means a new action release. Accept arbitrary or `latest` versions only on the signature-verification path (rule 5), resolved from the vendor's own version endpoint, never the rate-limited GitHub API.
- Accept a mirror base URL and a pre-installed binary path for proxied and air-gapped runners; honour `HTTPS_PROXY`.
- Retry the vendor API with backoff: matrix fan-out sends dozens of runs at once.

For the runtime timeline, check-dist and bundling, read [references/contract-and-release.md](./references/contract-and-release.md).

## 3. Design the contract

- Name inputs in kebab-case, one meaning each, with `description` and an explicit `default` on every optional input.
- Validate in code: `required: true` is not enforced by the runner. Fail on a missing or malformed input with the input name, the value received and the expected form.
- Parse every input as a string; accept booleans strictly (`true`/`false`) and say so.
- Accept secrets only as inputs or OIDC: composite actions have no `secrets` context, so `${{ secrets.X }}` inside one resolves empty.
- Add an `auth` input (`auto`, `oidc`, `key`; default `auto`) and make the key optional from `v1`, so adding OIDC later is a minor. In `auto`, an empty key selects OIDC; when `ACTIONS_ID_TOKEN_REQUEST_URL` is absent, fail naming both causes ("api-key is empty and the job lacks `id-token: write`"), because a missing secret also arrives empty. Log the chosen mode. Until the backend accepts OIDC, fail an empty key with a named error.
- Expose machine-usable outputs (IDs, URLs, counts, verdict) through `$GITHUB_OUTPUT`; never a value that embeds a secret.
- Map CLI exit classes to the step result:
  - configuration, auth or service error: always fail;
  - the product's primary verdict (drift found, vulnerability over threshold): fail by default, with a `fail-on-<verdict>: false` input that downgrades it to a warning;
  - advisory findings: warn.
- Add a contract check to CI that diffs `action.yml` inputs and outputs against the last release and fails on removal or rename outside a major branch.

For the breaking-change table and the deprecation sequence, read [references/contract-and-release.md](./references/contract-and-release.md).

## 4. Wire authentication

- effort: `OIDC token exchange > short-lived scoped token input > long-lived API key input`
- value (blast radius when a workflow leaks): `OIDC token exchange > short-lived scoped token input > long-lived API key input`
- efficiency: `OIDC token exchange > short-lived scoped token input > long-lived API key input` once the backend validates OIDC; `short-lived scoped token input` first while it does not.

- **Default:** OIDC when the backend supports workload identity; otherwise a masked key input now, with OIDC on the roadmap (step 3 shape).
- **Why teams starve OIDC:** it needs backend work - JWT validation, a trust-binding UI, token exchange - so it loses on effort.
- **Audience:** request a vendor-specific audience, never the default owner URL.
- **Binding:** match `repository_id` and `repository_owner_id` claims plus a ref or environment, never a wildcard or a name-only `sub`; new repositories use an immutable `sub` with numeric IDs.
- **Logs:** mask the exchanged token before any log line; document the minimum `permissions:` block (`id-token: write`, `contents: read`).
- **Fork pull requests:** they receive no secrets and no OIDC token. Offer a tokenless read-only mode where the product allows it, or exit with a message naming the limitation. Never tell customers to switch to `pull_request_target`.

For backend validation, claim formats, the fork split pattern and PR comments, read [references/vendor-oidc.md](./references/vendor-oidc.md). For key formats and rotation, see `samber/developer-platform-skills@api-auth-key-management`.

## 5. Version and release

1. Enable immutable releases on the action repository before the first public tag.
2. Release only when every § Gates item passes.
3. Run the release from a protected environment with required reviewers: build `dist/` or binaries in CI, attest them, create a draft `vX.Y.Z` release, attach assets, publish.
4. Let the same job move `vX` (and optionally `vX.Y`): plain Git tags with no GitHub release, pushed one at a time as `refs/tags/vX`, never `--tags`.
5. Write release notes that state the full commit SHA and the line `uses: org/action@<sha> # vX.Y.Z`, the form Dependabot updates.
6. Treat each forced runtime change as a scheduled major, use it to delete deprecated inputs, and keep patching the previous major while supported GHES releases cannot run the new runtime.

For the release workflow, test matrix and runtime timeline, read [references/contract-and-release.md](./references/contract-and-release.md). For the vendor's own registry and binary publishing, see `samber/developer-platform-skills@sdk-package-publishing`.

## 6. Harden the action and its repo

- Apply contract rules 4 and 5 to every step of the action.
- Never `curl | bash` an installer at runtime; download a versioned artifact and verify it.
- Protect `v*` tags with a ruleset only the release workflow's GitHub App can bypass; require 2FA; keep the write-access list short; prefer short-lived App tokens over bot PATs.
- Keep the action's own CI off `pull_request_target`, scope `GITHUB_TOKEN` per job, and sign release tags.
- Always send the versioned `User-Agent` (step 9); put any further telemetry behind an input that turns it off, and document both in the README.
- Keep a compromised-tag runbook ready before you need it.

For bad/good injection pairs, digest pinning, repo hardening, scanners and the incident runbook, read [references/security-hardening.md](./references/security-hardening.md).

## 7. List, document, reach GHES

- Keep one `action.yml` at the root of a public repository so Marketplace can list it.
- Pick a unique `name`, a short `description`, a `branding` icon and color, and one primary category.
- Request the verified creator badge through GitHub partnerships; enterprise allowlists key on it more than on listing rank. For listing rules, the badge, transfers and delisting, see `samber/developer-platform-skills@github-marketplace-playbook`.
- Open the README with a copy-paste workflow: the SHA-pinned `uses:` line with its version comment, the `permissions:` block, the OIDC setup, every input with default, every output, the minimum runner and GHES versions.
- Put the same snippet in the vendor's docs quickstart; that page, not Marketplace, drives adoption.
- Tell GHES customers how they get the action: GitHub Connect when their admin enables it, otherwise `actions-sync` into their instance. GHES signs OIDC tokens with its own issuer, usually on a private network the vendor backend cannot reach; support it through a customer-registered issuer or uploaded JWKS, or document GHES as key-only.

## 8. Port to other CI systems

Rank ports by the share of paying customers on each CI (interview question 2), never by the platform's general popularity.

- effort: `native package (GitLab component, CircleCI orb, Bitbucket Pipe, Azure DevOps task) > documented CLI snippet`
- value: `native package > documented CLI snippet` for the CI systems holding most non-GitHub customers; elsewhere `native package == documented CLI snippet`, because too few customers use them to repay a second release pipeline.

- **Default:** documented CLI snippets for every CI, plus a native package for the one or two CI systems that hold most non-GitHub customers.
- **Parity:** keep every port a thin wrapper over the same CLI and the same input names; a port that reimplements logic drifts within a few releases.

For packaging, versioning and immutability rules per platform, read [references/ci-ports.md](./references/ci-ports.md).

## 9. Measure and retire versions

- Count OIDC-authenticated runs from token exchanges, deduplicated by `run_id`: server-validated `repository_id` and `repository_owner_id` claims.
- Send a versioned `User-Agent` from the action and every port (`vendor-action/1.4.2 (github-actions; Linux-X64)`) to see version skew and key-auth runs; add a header flag whenever a deprecated input is set.
- Track: weekly active repositories by CI and version, share of runs on supported majors, first-run failure rate by error class, support tickets per release.
- Watch dependents and code search for `uses: <org>/<action>@` as public signals, not as usage.
- Delete a deprecated input only in a major; use the deprecated-input flag to choose which major.
- Retire a major by announcing it, warning from its last patch release, and leaving its tags in place: deleting a tag breaks every pinned workflow at once.

## Gates

A release ships only when every gate passes:

- contract diff clean against the last release, or the release is a major;
- check-dist clean (JavaScript actions);
- integration matrix green on every runner OS the README claims, the oldest supported self-hosted runner and GHES release, against a real sandbox account;
- zizmor reports no finding at medium severity or above on the action repo and the basic README example; the fork-split example carries only a line-scoped, commented ignore for its `workflow_run` trigger; actionlint clean;
- every nested `uses:` SHA-pinned, every image digest-pinned, every downloaded binary verified per rule 5.

## Failure modes

- **Moving `v1` fails with immutable releases on** - `v1` carries a GitHub release. Keep major tags release-free.
- **OIDC works in the vendor's test org, fails for a new customer repo** - the trust rule matches the old name-only `sub`. Match on numeric ID claims.
- **Action breaks in a customer org that enforces SHA pinning** - a nested `uses:` is on a tag. Pin it by SHA.
- **Fix released, customers still on the bug** - the fix only moved the major tag. Cut a `vX.Y.Z` release.
- **Self-hosted or GHES customers fail after a minor release** - a runtime or runner-floor bump shipped outside a major. Revert, re-release it as a major.

## Reference

- `samber/developer-platform-skills@api-versioning-policy` - the vendor API's own deprecation windows the action must follow.
- `samber/developer-platform-skills@agent-skill-offering` - the same lockstep versioning applied to an Agent Skill shipped with the CLI.
