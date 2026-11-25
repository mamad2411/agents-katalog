---
name: jfrog-artifactory-configuration
description: >
  Configures JFrog Artifactory's local/remote/virtual repository types,
  multi-region replication, retention/cleanup policies, and Xray
  security-scanning integration, with an honest compare/contrast against
  Sonatype Nexus. Use when a user asks to "set up Artifactory," "configure
  an Artifactory remote/virtual repository," "set up multi-region
  replication in Artifactory," "add Xray scanning to Artifactory," "clean up
  old artifacts in Artifactory," or is comparing Artifactory against Nexus
  for a private registry.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# JFrog Artifactory Configuration

## Purpose

JFrog Artifactory is a commercial (with a free Community/JCR tier) artifact
registry serving the same core need as Nexus — one server for otherwise
disparate package ecosystems (npm, Maven, Docker, PyPI, NuGet, Go, and many
more) — using an equivalent but differently-named three-tier repository
model: **local** (your own published artifacts, equivalent to Nexus's
"hosted"), **remote** (a caching proxy to an upstream registry, equivalent
to Nexus's "proxy"), and **virtual** (an aggregating endpoint clients
connect to, equivalent to Nexus's "group"). Where Artifactory
differentiates most in practice is **multi-region replication** (built-in,
first-class support for keeping repositories in sync across geographically
distributed Artifactory instances) and its tight, same-vendor integration
with **JFrog Xray** for security and license scanning of stored artifacts.
This skill covers configuring Artifactory itself — for the vendor-neutral
registry concepts this applies to, see
[artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md),
and for the comparable open-source-rooted alternative, see
[sonatype-nexus-repository-configuration](../sonatype-nexus-repository-configuration/SKILL.md),
which this skill cross-references throughout rather than repeating.

## When to use

- Standing up a new Artifactory instance (self-hosted or JFrog-hosted SaaS)
  as a private registry and/or caching proxy for one or more package
  ecosystems.
- Deciding whether a given use case needs a local, remote, or virtual
  repository (or a combination), mirroring the same three-way decision
  covered for Nexus in
  [sonatype-nexus-repository-configuration](../sonatype-nexus-repository-configuration/SKILL.md).
- Setting up multi-region replication so teams in different geographies (or
  a DR site) have a low-latency, locally-served copy of shared artifacts.
- Writing or debugging a retention policy to clean up old Docker tags,
  superseded Maven snapshots, or generic build artifacts.
- Mentioning or wiring in JFrog Xray for vulnerability/license scanning of
  artifacts already stored in Artifactory, as distinct from scanning source
  code or dependency manifests before they're published.
- Comparing Artifactory against Nexus for a registry decision — licensing
  model, replication capability, and Xray integration are the concrete
  differentiators to weigh.

## Prerequisites & environment

- Artifactory version 7.x (the current major line, using the unified
  "JFrog Platform" UI) — Artifactory 6.x used a different UI and some API
  paths; confirm the version before assuming a UI walkthrough or REST API
  call below applies as-is.
- A tier decision: **JFrog Artifactory Community Edition (JCR)** (free,
  self-hosted, no replication or Xray), **Artifactory Pro** (paid,
  self-hosted, adds most enterprise features), or **JFrog-hosted SaaS**
  (fully managed, tiered by usage) — replication and Xray integration
  generally require a paid tier; confirm current tier boundaries against
  JFrog's own documentation before assuming a specific feature is available
  on a given tier, since packaging has changed across JFrog's release
  history.
- For multi-region replication: network connectivity (and, typically, a
  paid tier license) between the Artifactory instances that will
  participate in a replication topology.
- For Xray integration: a licensed Xray instance connected to the
  Artifactory instance, plus defined scanning policies (severity
  thresholds, license allow/deny rules) — Xray is a separate product
  connected to Artifactory, not a built-in feature of Artifactory alone.
- Admin access to Artifactory's UI/REST API for repository, replication,
  and retention configuration; a realm/identity provider (LDAP, SAML, OIDC)
  for authenticating publishers separately from read-only consumers.

## Step-by-step guidance

1. **Create a remote repository** for each upstream public registry,
   analogous to a Nexus proxy repository:
   ```
   Administration → Repositories → Remote → Create repository
     Package type: npm
     Repository key: npm-remote
     URL: https://registry.npmjs.org
   ```
   Artifactory's remote repositories cache responses the same way Nexus
   proxy repositories do — the caching behavior itself is functionally
   equivalent between the two products; the naming ("remote" vs. "proxy")
   is the main surface difference to keep straight when moving between
   them.

2. **Create a local repository** for artifacts your own pipelines publish:
   ```
   Administration → Repositories → Local → Create repository
     Package type: docker
     Repository key: docker-local
   ```
   Docker in Artifactory does **not** require a dedicated connector port
   per repository the way Nexus does — Artifactory routes Docker traffic by
   repository path/subdomain instead, which is a genuine operational
   difference worth knowing before assuming Nexus's port-per-repository
   convention carries over.

3. **Create a virtual repository** aggregating local and remote
   repositories into the single endpoint clients actually use:
   ```
   Administration → Repositories → Virtual → Create repository
     Package type: npm
     Repository key: npm-virtual
     Repositories: npm-local, npm-remote   (order matters — local first)
   ```
   As with Nexus's group repository, list the local repository ahead of
   the remote/proxy repository so an internal package name can't
   accidentally resolve to a same-named public package — the same
   dependency-confusion risk applies regardless of vendor.

4. **Point CI and developers at the virtual repository URL**, never at
   individual local/remote repositories:
   ```bash
   npm config set registry https://artifactory.example.com/artifactory/api/npm/npm-virtual/
   ```
   ```bash
   docker login artifactory.example.com
   docker pull artifactory.example.com/docker-virtual/myapp:1.4.2
   ```

5. **Configure multi-region replication** for a repository that needs a
   low-latency local copy at a second site, choosing push (source instance
   initiates) or pull (target instance initiates) replication depending on
   which side should own scheduling:
   ```json
   // Push replication config (conceptual — set via UI or REST API)
   {
     "repoKey": "maven-local",
     "targetUrl": "https://artifactory-eu.example.com/artifactory/maven-local",
     "cronExp": "0 0 */6 * * ?",
     "enableEventReplication": true
   }
   ```
   `enableEventReplication: true` triggers near-real-time replication on
   artifact upload/delete events, in addition to the scheduled `cronExp`
   sync — rely on event replication for freshness and the cron schedule as
   a reconciliation backstop, not the other way around.

6. **Define a retention/cleanup policy** to remove old build artifacts,
   superseded snapshots, or untagged Docker images:
   ```
   Administration → Repositories → Retention Policy (or the newer
   "Cleanup Policies" UI depending on version) → Create policy
     Repository: docker-local
     Criteria: Keep last N tags per image; delete images not pulled in 90 days
   ```
   Exclude explicitly-tagged release versions (`v*`, `stable`, `latest` if
   meaningful in your workflow) from any age/pull-based cleanup rule, the
   same exclusion discipline described in
   [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md).

7. **Connect JFrog Xray for scanning artifacts already in Artifactory** —
   mention this as a distinct capability rather than assuming it's
   automatic: Xray scans artifacts stored in Artifactory repositories
   (and their dependency graphs) against vulnerability and license
   databases, and can block a `docker pull`/`npm install` of a
   policy-violating artifact via a configured Xray watch/policy. This is
   scanning *stored* artifacts, distinct from scanning source code before
   it's built (SAST) or scanning a dependency manifest before it's
   published — see
   [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md)
   for the vendor-neutral SCA concept and
   [snyk-vulnerability-and-license-scanning](../../../devsecops/skills/snyk-vulnerability-and-license-scanning/SKILL.md)
   for a comparable commercial scanner covering similar license-policy
   ground from a different product.

8. **Scope publish (deploy) permissions separately from read/pull
   permissions** via Artifactory's permission-target model, applied
   per-repository or per-repository-pattern, mirroring the least-privilege
   publish/read separation in
   [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md).

## Best practices

- Treat "remote" (Artifactory) and "proxy" (Nexus) as the same concept
  under different names when translating guidance or migrating between the
  two products — don't assume a behavioral difference just because the
  term differs.
- Order virtual/group repository members with local/hosted repositories
  first, in both Artifactory and Nexus, to avoid dependency-confusion
  resolution ambiguity.
- Use event-based replication as the primary freshness mechanism and a
  periodic cron-based replication as a reconciliation backstop, not a
  cron-only schedule alone — a purely scheduled replication window means a
  remote site can serve a stale artifact for up to the full interval.
- Reserve Xray policy-blocking (failing a pull/install on a policy
  violation) for well-understood, already-tuned policies — an
  under-tuned Xray policy applied as a hard block can break builds across
  every consumer of a repository at once, a wider blast radius than a
  single pipeline's own SCA gate failing.
- Confirm which tier (JCR / Pro / SaaS) a given feature actually requires
  before designing around it — replication and Xray are commonly
  paid-tier-gated, and assuming JCR parity with Pro is a common planning
  mistake.
- Keep retention/cleanup criteria explicit about exemptions (release tags,
  `latest`) the same way as for Nexus — an unscoped age-based cleanup
  policy is equally destructive regardless of vendor.

## Common pitfalls

- **Symptom:** A team migrating from Nexus to Artifactory (or vice versa)
  assumes "proxy" and "remote" repositories behave differently and spends
  time re-architecting repository structure unnecessarily.
  **Fix:** They're functionally equivalent concepts under different vendor
  terminology — map Nexus hosted → Artifactory local, Nexus proxy →
  Artifactory remote, Nexus group → Artifactory virtual, and carry over the
  same member-ordering and cleanup-policy discipline rather than
  re-designing from scratch.

- **Symptom:** Docker pulls fail intermittently after migrating from Nexus,
  where each Docker repository had its own connector port, to Artifactory.
  **Fix:** Artifactory doesn't use per-repository ports for Docker the way
  Nexus does — it routes by repository path/subdomain instead. Update
  client configuration (registry URL structure) to match Artifactory's
  routing model rather than trying to replicate Nexus's port-per-repository
  scheme.

- **Symptom:** A remote site served a stale (pre-update) artifact for
  several hours after a new version was published at the primary site.
  **Fix:** Check whether event-based replication (`enableEventReplication`)
  is actually enabled, not just the scheduled cron replication — a
  cron-only setup means the remote site is stale for up to the full
  interval between scheduled runs by design, not a bug.

- **Symptom:** Enabling an Xray blocking policy immediately breaks builds
  across many unrelated teams that were previously pulling from the
  affected repository without issue.
  **Fix:** Roll out a new or tightened Xray policy in watch/report-only
  mode first, review the resulting findings against real usage, and only
  switch to blocking once the policy's false-positive rate is understood —
  the same phased-rollout discipline used for any new blocking security
  gate.

- **Symptom:** Someone assumes multi-region replication or Xray scanning is
  available on the free Community Edition (JCR) and it silently isn't
  configurable in the UI.
  **Fix:** Confirm the current tier's feature set against JFrog's own
  documentation before planning around a specific capability — these are
  commonly paid-tier features, and JCR's feature set is intentionally
  narrower than Pro/SaaS.

## Worked example

**Scenario:** A global engineering org with teams in the US and EU
standardizes on Artifactory for Docker and Maven artifacts, replicating a
shared Maven local repository to an EU instance for low-latency reads, with
Xray scanning gating pulls on critical vulnerabilities.

Repositories (US primary instance):
```
maven-local     (local)   — published releases and snapshots
maven-remote    (remote → repo.maven.apache.org)
maven-virtual   (virtual: [maven-local, maven-remote])

docker-local    (local)
docker-remote   (remote → registry-1.docker.io)
docker-virtual  (virtual: [docker-local, docker-remote])
```

Replication (US → EU, push, event-based plus 6-hour cron backstop):
```json
{
  "repoKey": "maven-local",
  "targetUrl": "https://artifactory-eu.example.com/artifactory/maven-local",
  "cronExp": "0 0 */6 * * ?",
  "enableEventReplication": true
}
```
EU-based build agents point at `artifactory-eu.example.com`'s
`maven-virtual` for reads, getting near-real-time replicated artifacts
without a transatlantic round trip on every dependency resolution.

Xray policy (watch-only for 30 days, then switched to blocking):
```
Watch: "maven-local-critical-cves"
  Repositories: maven-local
  Policy: fail build on CVSS >= 9.0 with an available fix
  Mode: report-only for first 30 days → block after review
```
After the 30-day report-only period surfaces no unexpected false
positives against real usage, the watch is switched to blocking mode, so a
newly-published artifact with a critical, fixable vulnerability is rejected
by Xray before any consumer can pull it — while artifacts already resolved
before the block was enabled are handled through the normal SCA
remediation/triage workflow instead of being retroactively purged.

## Cross-references

- [sonatype-nexus-repository-configuration](../sonatype-nexus-repository-configuration/SKILL.md) — the comparable open-source-rooted alternative; this skill maps Artifactory's local/remote/virtual model directly onto Nexus's hosted/proxy/group model throughout.
- [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md) — the vendor-neutral registry concepts (retention policy design, publish/read credential separation, lockfile discipline) this skill implements concretely in Artifactory.
- [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md) — the vendor-neutral dependency-scanning concept that Xray implements for artifacts already stored in Artifactory.
- [snyk-vulnerability-and-license-scanning](../../../devsecops/skills/snyk-vulnerability-and-license-scanning/SKILL.md) — a comparable commercial scanner covering similar vulnerability/license-policy ground as Xray, useful for a direct feature/cost comparison.
- [container-build-and-release](../container-build-and-release/SKILL.md) — the container build workflow that publishes to an Artifactory Docker local repository configured here.
