---
name: cilicon-mac-runner-fleet
description: "Manage darkmatter Cilicon + Tart self-hosted macOS GitHub Actions runners — org vs enterprise registration, fleet hosts, labels, images, troubleshooting. Use when moving Mac runners to enterprise, editing cilicon.yml, Macly/OakHost ops, nixmac-mac labels, or comparing to ARC enterprise runners."
---

# Cilicon macOS Runner Fleet

Manage self-hosted GitHub Actions **macOS** runners using **Cilicon + Tart** on dedicated Mac hosts for darkmatter.

## When to use

- Org → **enterprise** Mac runner cutover
- `cilicon.yml`, LaunchAgent, labels, disk/Tart cache
- Macly / OakHost / Studio fleet work
- Why Cilicon cannot use GitHub App auth like org runners for enterprise
- Parity with gitops ARC enterprise pattern (`apps/arc-runners-enterprise.yaml`)

## Architecture (current)

- **Cilicon** (`/Applications/Cilicon.app`) — ephemeral macOS VMs via Virtualization.framework + Tart images
- **Tart** cache `~/.tart` (optional `TART_HOME`); per-run clone `~/vmclone` (do not delete while VM runs)
- Hosts register runners; Cilicon cycles VM → register → job → destroy

### Live org registration (baseline)

```yaml
# ~/cilicon.yml on fleet hosts
source: oci://ghcr.io/darkmatter/nixmac-runner-tahoe:<immutable-tag>
consoleDevices:
  - tart-version-2
sshConnectMaxRetries: 30
provisioner:
  type: github
  config:
    appId: 3999123              # darkmatter-runner GitHub App
    organization: darkmatter
    privateKeyPath: ~/github.pem
    extraLabels:
      - nixmac-mac
```

Live labels typically include: `self-hosted`, `macOS`, `ARM64`, `cilicon-*`, `nixmac-mac`, image ref.

### Fleet hosts (Macly primary)

| Public IP | Notes | Himitsu |
|---|---|---|
| 45.74.241.119 | primary | `mac-macly/password` |
| 45.74.241.209 | | `macly/45-74-241-209` |
| 45.74.241.215 | image builder | `macly/45-74-241-215` |

Also historically: OakHost, Studio (varies). SSH as fleet user; restart Cilicon from **GUI/login session** (SSH-started GUI often idle).

## Org vs enterprise registration (critical)

| | Org (today) | Enterprise (goal) |
|---|---|---|
| Auth | GitHub App install token | Classic **PAT `admin:enterprise`** |
| Token API | `POST /orgs/{org}/actions/runners/registration-token` | `POST /enterprises/{slug}/actions/runners/registration-token` |
| `config.sh --url` | `https://github.com/darkmatter` | `https://github.com/enterprises/darkmatter` |
| Cilicon github provisioner | Supported | **Not supported** in Cilicon 2.4.2 |

**Hard GitHub constraint (same as ARC):** GitHub Apps cannot register **enterprise** runners. Do not try to extend `appId: 3999123` for enterprise scope.

**Cilicon 2.4.2 limit:** `GithubService` only builds `/orgs/...` and `/repos/...` paths. Fields of note:

- `organization` / optional `repository` — org or repo scope only
- `runnerGroup` — optional **name** passed to `config.sh --runnergroup`; still only after **org** registration. Setting `runnerGroup: dm-aarch64-darwin` while staying org-scoped is **not** enterprise migration
- Optional `url` override exists in config but provisioner auth still goes through org installation + org runners API

### How ARC already does enterprise (pattern to mirror)

From gitops `apps/arc-runners-enterprise.yaml` + `manifests/arc-runners/README.md`:

```yaml
githubConfigUrl: "https://github.com/enterprises/darkmatter"
githubConfigSecret: <REDACTED>
runnerGroup: "public"                           # or Default for private-only
```

PAT source of truth: himitsu `github/darkmatter-pat` (also appears as enterprise runner secrets elsewhere). Enterprise slug: **`darkmatter`**.

### Recommended Mac enterprise path

1. **PAT** with `admin:enterprise`, SSO-authorized — reuse ARC PAT class; place on host as mode-600 file (never bake into OCI image).
2. Prefer Cilicon **`provisioner.type: script`** so VM lifecycle stays Cilicon, registration is enterprise.
3. Mint token: `POST /enterprises/darkmatter/actions/runners/registration-token`
4. `config.sh --url https://github.com/enterprises/darkmatter --token … --runnergroup '<group>' --labels … --ephemeral --unattended --replace`
5. Put Mac runners in an enterprise group with correct public-repo policy:
   - Inherited **`dm-aarch64-darwin`** exists at org view (`inherited: true`) — natural home
   - Enterprise **`Default`**: `allows_public_repositories: false`
   - Enterprise/inherited **`public`**: allows public repos (ARC `arc` pool uses this)
6. Fix **per-org inherited group visibility** after new orgs join (jobs otherwise queue forever; routing decided at queue time — **re-dispatch** after fix):

```bash
gh api /orgs/<org>/actions/runner-groups
gh api -X PATCH /orgs/<org>/actions/runner-groups/<id> -f visibility=all
```

7. Drain old **org-scoped** Cilicon runners so identical labels don’t dual-route.
8. Verify enterprise API (needs enterprise-capable token; plain `gh` often 404 without `admin:enterprise`):

```bash
gh api enterprises/darkmatter/actions/runners \
  --jq '.runners[] | select(.os=="macOS") | {name,status,labels:[.labels[].name]}'
# Cross-org smoke: runs-on from voytravel/convertify/stack-panel with same labels
```

### Medium-term

Fork/patch Cilicon github provisioner for enterprise URL + PAT auth. Until then, script provisioner or private build.

### Not sufficient

```yaml
organization: darkmatter
runnerGroup: dm-aarch64-darwin   # still org registration token path
```

## Durable labels

REST `POST .../runners/{id}/labels` does **not** survive ephemeral re-register. Put durable labels in:

- github provisioner: `extraLabels`
- script provisioner: `config.sh --labels`

Ensure LaunchAgent passes explicit config:

```xml
<string>--args</string>
<string>-config-path</string>
<string>~/cilicon.yml</string>
```

Restart:

```bash
kill $(pgrep -f "Cilicon -config-path" | head -1) 2>/dev/null || true
launchctl kickstart -k gui/$(id -u)/com.traderepublic.cilicon
# wait 60–90s for re-provision
```

## App / PEM safety

- Production Cilicon app: **`3999123`** `darkmatter-runner` (org self-hosted runners R/W)
- Himitsu `github/darkmatter-bot` **`3663660`** is a **different** app — do not swap PEMs casually
- Validate PEM: JWT → authenticated `GET /app` before rewriting `github.pem` / appId
- Keep `cilicon.yml.bak*` / `github.pem.bak` during experiments

## Images & private GHCR

- Custom image: `ghcr.io/darkmatter/nixmac-runner-tahoe:<tag>` (Packer: nixmac `ops/images/`)
- Prefer pre-`tart pull` on each host; Cilicon OCI auth ≠ Tart keychain
- Himitsu pull token: `github/ghcr-pull-token` (SAML authorized); do not make package public for Xcode redistribution reasons
- Use **immutable tags**, not `latest`; prefer tag form over bare `@sha256` in `source:` for Cilicon 2.4.2

### Tahoe SSH / Cilicon

Cilicon uses password SSH `admin`/`admin`. OpenSSH 10.x may need guest `MACs hmac-sha2-256,hmac-sha2-512` baked into image (host ssh can work while Cilicon still “SSH not ready”). Fix in image — `~/vmclone` patches die next cycle.

## Health checks

```bash
# Org runners (current)
gh api orgs/darkmatter/actions/runners --paginate \
  --jq '.runners[] | select(.os=="macOS") | {name,status,busy,labels:[.labels[].name]}'

# Host
ssh … 'df -h /; du -sh ~/.tart ~/vmclone 2>/dev/null'
ssh … 'ps aux | grep -iE "[C]ilicon|[V]irtualMachine"; launchctl print gui/$(id -u)/com.traderepublic.cilicon | grep -E "state =|last exit"'
```

## Disk

- Single base image can be ~140G under `~/.tart`
- Safe prune: stop VM → `tart delete` unused / `tart prune`
- Prefer APFS-aware size; `du` overcounts shared extents

## Related gitops

- Linux enterprise ARC: `apps/arc-runners-enterprise.yaml`, `apps/arc-runners-enterprise-dind.yaml`
- Secrets: `manifests/arc-runners/secrets-enterprise.sops.yaml`, `apps/arc-secrets.yaml`
- Do not conflate k8s ARC scale sets with bare-metal Cilicon hosts

## Pitfalls

1. **App auth cannot enterprise-register** — PAT only
2. **`runnerGroup` alone ≠ enterprise** with org provisioner
3. **Inherited group visibility `selected` + empty repos** → infinite queue; fix org-side + re-dispatch
4. **Enterprise Default vs public** — public repos need a group with `allows_public_repositories: true`
5. **Dual pool same labels** — drain org runners after enterprise cutover
6. **SSH-launched Cilicon** often won’t serve GUI session requirements — use login/VNC
7. **Ephemeral** — every job re-registers; auth path must work cold

## References

- `references/enterprise-registration.md` — token endpoints, script provisioner sketch, group matrix, cutover checklist
