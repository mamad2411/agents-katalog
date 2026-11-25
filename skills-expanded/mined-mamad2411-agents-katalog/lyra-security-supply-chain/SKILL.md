---
name: lyra-security-supply-chain
description: "Software supply-chain security: lockfile and pinning discipline, install-script containment, dependency cooldown against worm-speed attacks, digest-pinned base images, SBOMs, keyless signing with deploy-time verification, provenance attestations, and CI hardening — plus the incident drill for when a poisoned package lands. Use when adding or updating dependencies, hardening CI, setting registry policy, responding to a dependency CVE or compromise, or designing release integrity."
compatibility: "No tools required to apply the policies. Optional: syft (SBOM), cosign (signing), trivy/grype (scanning), osv-scanner. Composes with lyra-ci-cd-automation, lyra-podman-images, lyra-security-secrets, lyra-security-containers. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-security-supply-chain

## What it does

Protects the path from "someone published code" to "your production runs it." The 2020s taught the pattern: attackers stopped attacking your code and started attacking your *inputs* — typosquatted packages, hijacked maintainer accounts publishing wormed versions within hours, install scripts exfiltrating CI credentials, backdoored build inputs à la xz. The defense is not vigilance, it's **mechanism**: every input pinned and verified, every artifact attested, every install unable to run arbitrary code, and an inventory that answers "are we affected?" in minutes.

## The rules

### 1. Lockfiles are law

Committed, enforced in CI with frozen installs (`pnpm install --frozen-lockfile`, `npm ci`, `uv sync --frozen`, `cargo build --locked`), and *reviewed*: a lockfile diff that changes packages the manifest change doesn't explain is a finding, not noise. Resolved-URL and integrity-hash changes for unchanged versions are a red flag.

### 2. Install scripts don't run — contain the code you haven't read

Postinstall scripts are arbitrary code execution at install time, on dev machines and CI — the primary payload delivery of the npm-worm era. pnpm ≥10 ignores them by default; allowlist the handful that genuinely need to build via `onlyBuiltDependencies` in `pnpm-workspace.yaml` (on pnpm 9 and earlier the default is *run everything* — set `--ignore-scripts` explicitly). Elsewhere use `--ignore-scripts` and an allowlist. The same logic gates dev tooling: dependency code runs at build/test anyway, so CI runs least-privileged (see rule 8) and dev containers/sandboxes are the belt to the braces.

### 3. Cooldown: never install what was published this week

Fast-spreading compromises (worm-style, typosquats) are typically detected and yanked within days, so a mandatory release age (e.g. 7–14 days — pnpm ≥10.16 `minimumReleaseAge` in `pnpm-workspace.yaml`, Renovate `minimumReleaseAge`/stability days) usually means the poisoned version is gone before your window opens. Be honest about the limit: cooldown is probabilistic risk reduction against *noisy* attacks, not a guarantee — patient backdoors (xz sat undetected for weeks) sail through any window, which is why rules 6–8 exist. Exceptions: explicit security fixes, consciously fast-tracked with a diff review.

### 4. Adding a dependency is a decision, not a reflex

Before adopting: does the stdlib or an existing dep already do this; is it maintained (bus factor, release cadence); what does *its* dependency tree drag in; exact-name check against typosquats (`lodash` vs `1odash`)? Prefer fewer, bigger, boring dependencies over many micro-packages — every package is a maintainer account that can be phished. Update deliberately (grouped, reviewed, cooldown-aged), not automatically-merged.

### 5. Base images and actions are dependencies too

`FROM` pinned by digest (lyra-podman-images rule 2), CI actions pinned by commit SHA (lyra-ci-cd-automation rule 2), toolchains by exact version — a mutable tag or `@v4` ref is an unreviewed code injection point owned by someone else. Renovate/dependabot bump the pins so deliberateness doesn't become staleness. The 2026 additions to the dependency list: **models, weights, datasets, and MCP servers**. An MCP server is arbitrary code with tool access wired into your agents — vet, pin, and cooldown it like an npm package (typosquatted MCP servers are the new typosquatted packages), pin model/dataset versions by hash, and inventory them in the SBOM like everything else.

### 6. SBOM every release — the inventory that answers "are we affected?"

Generate at build (`syft <image> -o cyclonedx-json`), attach to the release artifact, and keep them queryable across deployed versions. When the next Log4Shell/xz drops, the difference between a five-minute answer and a week of archaeology is whether SBOMs exist for what's *running*, not what's building. Scan continuously against fresh CVE feeds (osv-scanner, trivy) — vulnerabilities are published after your build passed.

### 7. Sign artifacts; verification is the point

Keyless cosign signing (OIDC identity, no key custody) at build; **deploy-time verification** of signature and identity is what turns it from decoration into a control — an image that didn't come from your CI on your repo doesn't run. On podman hosts that control exists off-the-shelf: `/etc/containers/policy.json` can require a valid sigstore signature per registry scope, host-wide, so unsigned images refuse to *pull* — pair it with the CI verify step rather than choosing one. And protect what you *publish* the same way: registry **trusted publishing** (npm/PyPI OIDC with `--provenance`) replaces the long-lived publish token — the exact credential class the worm era phishes — with a per-release federated identity. Add provenance attestations (SLSA-style: what repo, what commit, what builder produced this) so consumers can verify the build path, not just the publisher — and use the SLSA levels as the maturity ladder: L1 provenance exists → L2 signed by the build platform → L3 hardened, non-forgeable builds. Knowing which level you're on turns "improve supply-chain security" into a concrete next step.

### 8. CI is the crown-jewel target — harden it like production

CI holds the signing identity, registry write access, and (badly configured) cloud credentials; compromising it compromises everything downstream, which is why supply-chain attacks aim there. Least-privilege job tokens, OIDC over stored secrets, SHA-pinned actions, no secrets in PR-triggered workflows from forks, protected branches and required review on workflow files themselves. Egress is a mechanism, not awareness: default-deny or allowlist runner egress (an egress proxy, or a runner-hardening agent that inventories outbound calls) so "a build phoned home to a new domain" is a blocked connection and an alert, not a line in a log nobody reads. lyra-ci-cd-automation rule 2 implements the token/pinning half; this rule is why.

### 9. Registry hygiene: one trusted door

A pull-through proxy/private registry gives you: an allowlist point, a cache that survives upstream yanks, immutable tags, and audit logs of what entered. Scope registries per ecosystem in config (`.npmrc`/`pip.conf`/`registries.conf`) so a stray dependency can't fetch from an untrusted host — dependency confusion lives in the gap between internal names and public registries; reserve/claim your internal namespaces publicly.

### 10. The incident drill: assume it happened

A dependency compromise lands. In order: (1) SBOM query — which services, which versions, running where; (2) contain — pin to known-good, freeze deploys of affected artifacts; (3) rotate every credential the compromised code could reach (it ran in CI with your env — see lyra-security-secrets rule 7); (4) audit what it did while present (egress logs, registry audit, new commits); (5) postmortem the mechanism that let it in — the fix is a new rule above, not a resolution to be more careful.

---

_Part of the [skill collection](../README.md)._
