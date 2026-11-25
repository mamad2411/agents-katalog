---
name: lyra-security-containers
description: "Container runtime hardening with Podman: rootless + non-root defense in depth, capability dropping, read-only rootfs, seccomp/SELinux kept on, user-namespace isolation, no socket mounts, no host networking, resource limits as DoS containment, and scan-and-rebuild image lifecycle. Use when hardening container deployments, reviewing podman/docker run flags or quadlets for security, or deciding whether a container needs a privilege it asks for."
compatibility: "Podman-first (rootless by default; userns=auto applies to rootful/system podman only — see rule 5); most rules apply to Docker with noted differences. Optional: trivy/grype. Composes with lyra-podman-images, lyra-podman-deploy, lyra-security-secrets, lyra-security-supply-chain. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-security-containers

## What it does

Hardens the boundary between a workload and the host it runs on. Containers are not VMs — they share the host kernel, and their isolation is exactly the sum of the mechanisms this skill keeps enabled: namespaces, capabilities, seccomp, SELinux, cgroups. The operating principle is **defense in depth against your own image**: assume the app will be compromised, and make the container a dead end. The most dangerous flags are the ones that make problems disappear — `--privileged`, `seccomp=unconfined`, `setenforce 0` — because each converts a diagnosable error into a disabled defense.

## The rules

### 1. Two layers of "not root": rootless engine, non-root user

Rootless Podman means a container escape lands as an unprivileged host user — the engine-level defense. `USER app` in the image means an app compromise doesn't even own the container — the container-level defense. Run both: root-in-container under a rootless engine is *mapped* root, still able to modify the image's filesystem, bind low ports internally, and exercise every capability the container was granted. The pair costs nothing and cuts both escape stories.

### 2. Drop all capabilities, add back what's proven needed

```
--cap-drop=all --cap-add=NET_BIND_SERVICE   # only if it truly binds <1024
```

Default capability sets exist for compatibility, not for your app. Almost every service needs zero capabilities — it listens on an unprivileged port and talks to a database. Each `--cap-add` is a claim; make the workload prove it (run without, read the actual error). `--privileged` is not a capability grant, it's the *absence of all containment* (all caps, no seccomp, no SELinux, all devices) — it never ships to production, and a third-party image that "requires" it gets investigated, not obeyed.

### 3. Read-only rootfs; writable paths are declared

`--read-only` with explicit `--tmpfs /tmp` (and named volumes for real state) means malware can't write itself into the filesystem and config can't be tampered at runtime. Podman nuance: `--read-only` still auto-mounts tmpfs on `/tmp`, `/run`, and `/var/tmp` by default (`read_only_tmpfs=true`) — convenient, but it means writable paths you didn't declare. For "every writable path is documented by construction" to be literally true, add `--read-only-tmpfs=false` and declare each tmpfs explicitly. Apps that "need" a writable rootfs usually need two tmpfs mounts you haven't identified yet. In quadlets: `ReadOnly=true`, `Tmpfs=/tmp`.

### 4. Seccomp and SELinux stay on — fix labels, not enforcement

The default seccomp profile blocks the syscalls container escapes are made of; `--security-opt seccomp=unconfined` as a fix is the disease pretending to be the cure. On SELinux hosts, volume errors mean missing `:Z`/`:z` labels (lyra-podman-deploy rule 7), never `--security-opt label=disable` or permissive mode. Add `--security-opt no-new-privileges` so nothing in the container gains privileges via setuid binaries. If a profile genuinely blocks a legitimate syscall, write a *narrower* custom profile — allow that syscall, not all of them.

### 5. `userns=auto` isolates containers from each other

Isolating containers *from each other* takes different mechanisms per engine mode — don't mix them up. **Rootful/system podman:** `--userns=auto` gives each container its own non-overlapping UID range allocated from the `containers` system user's subordinate IDs — container A's root and container B's root are different host UIDs, so one compromised container can't touch another's files even where volumes or leaked paths overlap. **Rootless podman does not support `--userns=auto`** (a user can't subdivide its own subordinate range that way; the flag errors) — there, the equivalent separation is running each service under its own dedicated user account (separate subuid ranges, separate user journals, quadlets per user), which composes naturally with lyra-podman-deploy's user units. Either way, know the ceiling: namespaces isolate neighbors, not a determined kernel-exploit attacker — for *genuinely untrusted* code (running customer submissions, executing LLM-generated programs), escalate to a sandboxed runtime (gVisor's userspace kernel, Kata's microVMs) where the workload never talks to the host kernel directly.

### 6. The socket is the host — never mount it

Mounting `podman.sock`/`docker.sock` into a container hands it the ability to start a privileged container on the host: root, full stop. Tools that "need" the socket (CI runners, reverse-proxy dockware, monitoring agents) get: rootless socket if unavoidable, a socket proxy that filters the API surface, or — better — designs that don't touch it (podman remote over SSH, quadlet-managed services, event streams). Treat any compose file mounting the socket as a finding.

### 7. Network least privilege — no host networking, no gratuitous exposure

`--network=host` removes the network namespace: the container sees and binds everything the host can — it's `--privileged` for the network. Use named networks per stack (lyra-podman-deploy rule 6), `internal: true` networks for tiers that never talk out (databases), publish only required ports bound to `127.0.0.1` behind the proxy, and remember rootless port-forwarding specifics (pasta) when reasoning about what's actually reachable.

### 8. Limits are security controls, not tuning

`--memory`, `--cpus`, and above all `--pids-limit` (a fork bomb in an unlimited container is a host outage) contain the blast radius of both bugs and compromises. Add `--memory-swap` equal to memory to prevent swap thrash, and treat "no limits set" in a production spec the way you'd treat "no authentication" (lyra-podman-deploy rule 9 has the quadlet directives).

### 9. Minimal images are runtime security

Every binary in the image is post-compromise tooling for the attacker: shells, package managers, curl, interpreters. Distroless/scratch images (lyra-podman-images rule 2) turn "attacker got RCE" into "attacker got RCE in a room with no tools". No secrets in images or env — file-mounted secrets only (lyra-security-secrets rule 4; lyra-podman-deploy rule 8). Debug variants (`:debug` tags, ephemeral `podman exec` sidecars) exist so prod images never grow a shell "temporarily".

### 10. Scan, rebuild, and re-verify on a cycle

Images are frozen dependency snapshots: they rot. Scan (trivy/grype) in CI as a promotion gate and on a schedule against what's *deployed*; rebuild on base-image updates (digest bumps via Renovate + auto-update rollout, lyra-podman-deploy rule 4) rather than patching running containers — containers are replaced, never repaired. A container running for 400 days is 400 days of unpatched kernel-adjacent software. Close the loop at the pull: `/etc/containers/policy.json` can require valid signatures host-wide so an image that didn't come from your CI never runs (lyra-security-supply-chain rule 7 owns the signing side).

### 11. When something is denied, diagnose — don't disable

The debugging ladder for "works locally, permission-denied deployed": exact error → which mechanism (SELinux label? capability? seccomp? read-only path? userns ownership?) → narrowest fix (`:Z`, one `--cap-add`, one tmpfs, `:U`) → document why. Every "fixed it with `--privileged`/unconfined/permissive" is a disabled defense wearing a resolved-ticket costume — the flags that end debugging fastest are the ones attackers thank you for.

---

_Part of the [skill collection](../README.md)._
