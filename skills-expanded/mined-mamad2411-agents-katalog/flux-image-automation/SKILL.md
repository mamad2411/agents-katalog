---
name: flux-image-automation
description: >
  Secure Flux image automation (ImageRepository, ImagePolicy, ImageUpdateAutomation):
  registry credentials, tag policies (semver/allowlist), write-back permissions to Git,
  and prevention of untrusted tag promotion. Use when enabling or reviewing owned Flux
  image update pipelines that open PRs or commits for new container tags.
---

# Flux Image Automation

## Scope And Authorization

- **In scope:** Flux image automation on clusters/repos you own.
- **Out of scope:** forcing image updates on third-party clusters or poisoning public registries you do not control (except authorized red-team with contract).
- Image update write-back can deploy arbitrary tags—gate tightly.
- Redact registry tokens and Git write credentials.
- Pair with `flux-gitops-security` and `code-quality-standards`.

## When To Use

- Configuring **ImageRepository / ImagePolicy / ImageUpdateAutomation**.
- Auto-bumping image tags in Git for continuous delivery.
- Restricting which tags are eligible (semver ranges, regex allowlists).
- Reviewing blast radius of Git write keys used by automation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Overall Flux GitOps security | `flux-gitops-security` |
| GCP Binary Authorization | `gcp-binary-authorization` |
| Registry cleanup GC | `gcp-artifact-registry-cleanup` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| CRD | Role |
| --- | --- |
| ImageRepository | Scans registry for tags |
| ImagePolicy | Selects “latest allowed” tag from scan |
| ImageUpdateAutomation | Commits/PRs marker updates in Git |

| Risk | Mitigation |
| --- | --- |
| `latest` mutable tag | Prefer digests or immutable semver; policy exclude `latest` |
| Compromised registry push | Admission verify signatures; restrict who can push |
| Automation pushes to main | PR-only write-back; human approve prod |
| Broad Git write | Fine-scoped app; path-limited |

## Workflow

### 1. Confirm scope and success criteria

1. Apps in automation scope; registries; prod vs non-prod promotion model.
2. Success: only allowlisted tags applied; Git writes limited; malicious tag name cannot force deploy without policy pass.
3. Decide commit-to-branch vs PR bots.

### 2. Inventory

```bash
flux get images all -A
kubectl get imagerepository,imagepolicy,imageupdateautomation -A -o yaml
```

1. Map credentials secrets for registry pull/list.
2. Map Git credentials for automation user.

### 3. Policy design

```yaml
# Conceptual ImagePolicy — prefer semver ranges
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: ">=1.2.0 <2.0.0"
  # filterTags / alphabetical patterns per version docs for non-semver
```

1. **Ban** unlimited `latest` promotion for production.
2. Prefer digests in production manifests when possible; automation can update digests if supported in your workflow.
3. Separate policies for staging (wide) vs prod (narrow).

### 4. Harden automation write-back

```yaml
# ImageUpdateAutomation: review git repo URL, path, branch strategy
# Prefer updating a staging branch or opening PRs via CI rather than direct main
```

1. Git credential: contents write only to specific repo; no org owner.
2. Signed commits optional but helpful; still require review for prod.
3. Path scope markers only under app deploy dirs.
4. Rate-limit intervals to avoid noisy commits.

### 5. Registry auth and supply chain

1. Read-only robot accounts for ImageRepository scan when possible.
2. Combine with admission controllers / Binary Authorization for deploy-time verify.
3. Mirror internal registry to reduce dependency on public mutability.

### 6. Verify with evidence

| Test | Expect |
| --- | --- |
| Push tag `evil-latest` outside policy | Not selected |
| Push valid semver in range | Policy updates; PR/commit created per config |
| Revoke Git token | Automation fails closed |
| Malicious YAML outside markers | Not rewritten |

```bash
flux logs --kind=ImageUpdateAutomation --tail=50
```

### 7. Observe and hand off

1. Alert on automation errors and on unexpected high-frequency commits.
2. Periodic review of ImagePolicy ranges.
3. Document promotion path staging→prod (may be manual digest pin).
4. Apply `code-quality-standards` for policy YAML.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tags | Semver allowlist | Auto-deploy `latest` to prod |
| Git write | PR + review | Direct main with cluster token |
| Registry auth | Read-only scanner | Admin registry creds in cluster |
| Prod | Digest pins + admission | Mutable tags only |
| Scope | Per-app automation | One automation rewrites monorepo root |
| Secrets | Short-lived / fine PAT | Org-wide classic PAT |

## Output Checklist

- [ ] Image* resources inventoried
- [ ] Tag policies strict for prod
- [ ] Git write scope minimized
- [ ] Registry credentials least privilege
- [ ] Promotion workflow documented
- [ ] Failure fail-closed evidenced
- [ ] Linked to broader Flux security controls
- [ ] Admission/signature strategy noted
- [ ] `code-quality-standards` applied

## Rules

- Owned registries/repos/clusters only.
- Image automation is continuous delivery power—default to review gates for production.
- Prefer immutable references and supply-chain verification over trusting tag strings.
- Use with `flux-gitops-security` for controller RBAC and source trust.
