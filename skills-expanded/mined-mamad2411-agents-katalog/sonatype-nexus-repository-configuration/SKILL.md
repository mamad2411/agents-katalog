---
name: sonatype-nexus-repository-configuration
description: >
  Configures Sonatype Nexus Repository Manager's hosted, proxy, and group
  repository types, cleanup/retention policies, blob store sizing, and
  per-format setup for npm, Maven, and Docker registries. Use when a user
  asks to "set up Nexus," "configure a Nexus proxy repository," "create a
  Nexus group repository," "clean up old artifacts in Nexus," "size a Nexus
  blob store," "configure the Docker registry in Nexus," or is comparing
  Nexus against Artifactory for a private registry.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Sonatype Nexus Repository Configuration

## Purpose

Nexus Repository Manager is a self-hostable artifact registry that unifies
otherwise-separate package ecosystems (npm, Maven/Java, Docker, PyPI, NuGet,
and more) behind one server, one authentication model, and one storage
layer. Its core configuration abstraction is the **repository type**:
**hosted** (a repository you publish your own artifacts to), **proxy** (a
caching pass-through to a remote registry like npmjs.org or Docker Hub),
and **group** (a single virtual endpoint that aggregates one or more
hosted/proxy repositories into one URL for clients to point at). Getting
this three-way distinction right — and configuring cleanup policies and
blob store sizing before storage grows unbounded — is what separates a
Nexus instance that stays fast and manageable from one that silently fills
disk or serves stale/duplicate artifacts. This skill covers Nexus
specifically; for the vendor-neutral concepts (why a private registry
matters, lockfile/version-pinning discipline, retention policy design) see
[artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md),
and for a direct product comparison see
[jfrog-artifactory-configuration](../jfrog-artifactory-configuration/SKILL.md).

## When to use

- Standing up a new Nexus Repository Manager instance to serve as a private
  package registry and/or pull-through proxy in front of public registries.
- Deciding whether a given use case needs a hosted, proxy, or group
  repository (or which combination), for npm, Maven, Docker, or another
  supported format.
- Writing or debugging a cleanup policy so old snapshot builds, untagged
  Docker images, or superseded npm/Maven artifacts don't accumulate
  indefinitely.
- Sizing or troubleshooting a Nexus blob store that's approaching disk
  capacity, or planning blob store layout before initial rollout.
- Configuring the Docker registry realm in Nexus (repository connectors,
  port assignment, HTTPS) for a private container registry.
- Comparing Nexus Repository Manager (including the free Community Edition
  vs. paid Pro tier) against JFrog Artifactory for a registry decision.

## Prerequisites & environment

- Nexus Repository Manager 3.x (the current major line; Nexus 2.x is
  end-of-life and uses a substantially different UI/API — confirm which
  major version you're on before applying any guidance below, since 2.x
  configuration doesn't map directly to 3.x's repository-type model).
- A decision on edition: Community Edition (free, self-hosted, no
  vendor SLA) vs. Nexus Repository Pro (paid, adds features like
  high-availability clustering and additional format support) — confirm
  which edition a given feature (e.g. clustering) requires before assuming
  parity with Artifactory's tiering.
- Sufficient disk (or S3-compatible object storage, supported for blob
  stores in more recent 3.x releases) sized for expected artifact volume —
  underestimating this is the single most common operational issue,
  covered in the sizing guidance below.
- Admin access to Nexus's own web UI/REST API for repository and blob store
  configuration, plus a realm/role setup (LDAP, SAML, or Nexus's built-in
  user database) for authenticating publishers separately from anonymous or
  read-only consumers.
- Reverse proxy/TLS termination (nginx, an ALB, or equivalent) in front of
  Nexus for anything beyond local/internal-only use — Nexus's built-in HTTP
  listener is not typically exposed directly to the internet.

## Step-by-step guidance

1. **Create a blob store before creating repositories** — every repository
   writes to a named blob store, and the default `default` blob store is
   rarely the right long-term choice for a production instance with
   multiple formats:
   ```
   Administration → Repository → Blob Stores → Create blob store
     Type: File (local disk) or S3 (object storage, Pro or newer OSS releases)
     Name: npm-blobs
     Path: /nexus-data/blobs/npm    (File type)
   ```
   Use **separate blob stores per format or per team** (`npm-blobs`,
   `maven-blobs`, `docker-blobs`) rather than one shared blob store — this
   isolates disk pressure from one format's growth (Docker layers are
   usually the biggest) from starving another format's repositories, and
   makes capacity planning per-format tractable.

2. **Create a proxy repository** for each public registry your builds
   depend on, rather than pointing CI directly at the public internet:
   ```
   Repository → Create repository → npm (proxy)
     Name: npm-proxy
     Remote storage: https://registry.npmjs.org
     Blob store: npm-blobs
     Negative cache enabled: true, TTL 1440 min   (cache "not found" too, avoid repeat misses)
   ```
   Equivalent for Docker Hub:
   ```
   Repository → Create repository → docker (proxy)
     Name: docker-hub-proxy
     Remote storage: https://registry-1.docker.io
     Docker Index: Use Docker Hub
     HTTP port: 8082    (Docker requires a dedicated connector port per repo, unlike npm/Maven which share the base URL path)
   ```
   Docker's requirement for a dedicated repository connector port (rather
   than a path-based route like npm/Maven) is a frequent point of confusion
   when migrating from a different registry product — plan port allocation
   for every Docker (proxy, hosted, and group) repository up front.

3. **Create a hosted repository** for artifacts your own builds publish:
   ```
   Repository → Create repository → maven2 (hosted)
     Name: maven-releases
     Blob store: maven-blobs
     Version policy: Release        (a separate maven-snapshots hosted repo
                                      should use Version policy: Snapshot)
     Deployment policy: Disable redeploy   (release immutability — see pitfalls)
   ```
   Keep **releases and snapshots in separate hosted repositories** for
   Maven — this is Nexus's standard convention and lets cleanup policy and
   deployment-policy (redeploy allowed vs. not) differ correctly between
   the two.

4. **Create a group repository as the single URL clients actually use**,
   combining the proxy and hosted repositories so consumers never need to
   know which underlying repository actually served a given artifact:
   ```
   Repository → Create repository → npm (group)
     Name: npm-group
     Member repositories (in order): npm-hosted, npm-proxy
   ```
   Order matters: Nexus checks member repositories in the listed order and
   returns the first match, so list your **hosted** repository before the
   **proxy** — otherwise a package name collision could resolve to the
   public proxy's version instead of your intentionally-published internal
   one.

5. **Point CI and developer tooling at the group repository URL**, never at
   individual hosted/proxy repositories directly:
   ```bash
   npm config set registry https://nexus.example.com/repository/npm-group/
   ```
   ```xml
   <!-- ~/.m2/settings.xml -->
   <mirror>
     <id>nexus</id>
     <mirrorOf>*</mirrorOf>
     <url>https://nexus.example.com/repository/maven-group/</url>
   </mirror>
   ```
   Pointing at the group repository is what gives you the resilience and
   single-point-of-scanning benefits described generically in
   [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md)
   — changing or adding a member repository later requires no client-side
   reconfiguration.

6. **Configure a cleanup policy** to reclaim space from artifacts that no
   longer need to be retained, rather than growing the blob store
   unbounded:
   ```
   Administration → Repository → Cleanup Policies → Create cleanup policy
     Name: snapshots-older-than-30-days
     Format: maven2
     Criteria: Component age (30 days), Last downloaded (14 days)
   ```
   Attach the policy to `maven-snapshots` (never to `maven-releases`, which
   should generally be retained indefinitely) and either run cleanup
   on-demand or schedule it via a Nexus task:
   ```
   Administration → System → Tasks → Create task → Admin - Cleanup repositories using their associated policy
     Repositories: maven-snapshots
     Schedule: Weekly
   ```

   > **Warning:** a cleanup policy attached to the wrong repository (e.g.
   > accidentally attached to `maven-releases` instead of
   > `maven-snapshots`), or a subsequent blob store compaction, permanently
   > deletes the underlying artifact bytes — this is not reversible from
   > within Nexus itself. Double-check the target repository before
   > enabling or scheduling a cleanup policy, and confirm a separate backup
   > of the blob store/data directory exists before running compaction for
   > the first time against a production instance.

7. **Configure Docker-specific cleanup separately**, since untagged/
   superseded image layers are usually the fastest-growing storage
   category:
   ```
   Cleanup Policies → Create cleanup policy
     Name: docker-untagged-30d
     Format: docker
     Criteria: Component age (30 days)
   ```
   Follow cleanup with the separate **compact blob store** task — Nexus
   cleanup policies delete component metadata and mark blobs for deletion,
   but reclaiming actual disk space requires running blob store compaction
   afterward:
   ```
   Administration → System → Tasks → Create task → Admin - Compact blob store
     Blob store: docker-blobs
   ```

8. **Size the blob store with real numbers, not a guess** — estimate
   per-format growth rate (average artifact size × publish frequency ×
   retention window) per blob store, and alert well before the underlying
   disk/volume approaches capacity; Nexus's own health check UI surfaces
   blob store free-space percentage, but don't rely on manually checking it
   — wire it into your existing monitoring stack instead.

## Best practices

- Separate blob stores by format (and, for high-volume orgs, by team or
  business unit) so one format's storage growth doesn't crowd out another's
  capacity headroom, and so a compaction/cleanup task on one blob store
  doesn't affect I/O on repositories backed by a different one.
- Order group repository members deliberately (hosted before proxy) to
  avoid an internal package name accidentally resolving to a same-named
  public package — this is a real dependency-confusion risk, not just a
  performance nicety.
- Set Maven hosted release repositories to disallow redeploy
  (`Deployment policy: Disable redeploy`) so a published release version's
  artifact is immutable — silently overwriting a released version breaks
  the "same version means same bytes" guarantee that
  [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md)
  depends on for reproducible builds.
- Always run blob store compaction after a cleanup task if disk space
  needs to be reclaimed promptly — cleanup alone only removes component
  metadata references, not the underlying blob bytes, until compaction
  runs.
- Scope publish credentials (write access to hosted repositories) separately
  from the broad, org-wide read access most CI jobs and developers need to
  pull dependencies — mirrors the least-privilege publish/read separation
  in [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md).
- Enable negative caching on proxy repositories (cache "not found" results
  for a bounded TTL) so a burst of requests for a nonexistent/mistyped
  package doesn't repeatedly hit the remote registry.

## Common pitfalls

- **Symptom:** A Docker pull through Nexus returns "no matching manifest"
  or connects to the wrong repository entirely.
  **Fix:** Confirm the client is pointed at the correct repository
  connector port — unlike npm/Maven, each Docker repository (hosted, proxy,
  and group) in Nexus needs its own dedicated HTTP/HTTPS connector port,
  and a misconfigured or reused port is the most common cause of Docker
  registry connectivity issues in Nexus specifically.

- **Symptom:** Disk usage keeps climbing even after a cleanup policy is
  configured and running successfully.
  **Fix:** Cleanup policies remove component metadata/references but the
  underlying blob bytes aren't actually reclaimed from disk until the
  separate **Compact blob store** task runs — schedule compaction to run
  after cleanup, not assume cleanup alone frees space.

- **Symptom:** An internal npm package name accidentally resolves to a
  same-named public npm package (or vice versa) through the group
  repository.
  **Fix:** Check the group repository's member ordering — the
  hosted repository (your internal packages) must be listed before the
  proxy repository (the public registry mirror) so Nexus's first-match
  resolution favors your internal package; this is a real dependency
  confusion/supply-chain risk, not just a minor misconfiguration.

- **Symptom:** A Maven release artifact was accidentally overwritten by a
  redeploy of the same version, and builds that pinned that version now
  resolve to different bytes than before.
  **Fix:** Set the hosted release repository's deployment policy to
  "Disable redeploy" so this is rejected at publish time going forward;
  for the already-corrupted version, republish under a new patch version
  rather than trying to restore exact original bytes, and audit which
  builds consumed the corrupted artifact in the meantime.

- **Symptom:** The Nexus blob store fills to capacity unexpectedly, causing
  publish failures across every format sharing that blob store.
  **Fix:** This is the direct consequence of not separating blob stores per
  format — split high-growth formats (typically Docker) into their own
  dedicated blob store going forward, and in the immediate term, run
  cleanup + compaction against the offending format's oldest/least-used
  components to free emergency headroom.

## Worked example

**Scenario:** Standing up Nexus to serve as the private npm and Docker
registry for a mid-size engineering org, with a 30-day cleanup policy on
snapshots/untagged images and separate blob stores per format.

Blob stores created: `npm-blobs`, `docker-blobs` (each a `File` type blob
store on its own disk volume, sized independently).

Repositories:
```
npm-hosted   (hosted, blob store: npm-blobs)   — internal packages
npm-proxy    (proxy → registry.npmjs.org, blob store: npm-blobs)
npm-group    (group: [npm-hosted, npm-proxy])  — what CI/devs actually use

docker-hosted (hosted, blob store: docker-blobs, connector port 8081)
docker-proxy  (proxy → registry-1.docker.io, blob store: docker-blobs, connector port 8082)
docker-group  (group: [docker-hosted, docker-proxy], connector port 8083)
```

Cleanup policies:
```
npm-untagged-90d    → format: npm,    criteria: component age 90 days
                       (attached to npm-proxy cache only, not npm-hosted)
docker-untagged-30d → format: docker, criteria: component age 30 days
                       (attached to docker-proxy cache only, not docker-hosted)
```

Scheduled task: `Admin - Cleanup repositories using their associated
policy` weekly, followed by `Admin - Compact blob store` for both
`npm-blobs` and `docker-blobs`, so metadata cleanup and actual disk
reclamation both run on the same weekly cadence rather than metadata being
cleaned while disk usage keeps climbing.

CI configuration points at `npm-group` and `docker-group` exclusively:
```bash
npm config set registry https://nexus.example.com/repository/npm-group/
docker login nexus.example.com:8083
docker pull nexus.example.com:8083/library/alpine:3.20
```

Six months later, when a new internal team's build system needs the same
registries, they point at the same two group URLs with no changes to
repository structure required — the group indirection is what makes this
addition transparent to every existing consumer.

## Cross-references

- [jfrog-artifactory-configuration](../jfrog-artifactory-configuration/SKILL.md) — the comparable commercial alternative, including where Artifactory's repository model and Xray security-scanning integration differ from Nexus's approach.
- [artifact-and-dependency-management](../artifact-and-dependency-management/SKILL.md) — the vendor-neutral concepts (why a private registry matters, lockfile discipline, retention policy design, publish/read credential separation) that this skill implements concretely in Nexus.
- [container-build-and-release](../container-build-and-release/SKILL.md) — the container build workflow that publishes to a Docker hosted repository configured here.
- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — where registry configuration fits into the broader build/publish pipeline stage sequence.
