---
name: comfyui-workflow-sharing-risk
description: >
  Assess and reduce risks when sharing ComfyUI workflows: embedded credentials, remote
  custom-node supply chain, malicious pickles/models, path traversal in loaders, and
  accidental PII in graphs/images. Use for owned genAI workstations and team workflow
  exchange — not for distributing malware graphs or bypassing others’ safety systems.
---

# ComfyUI Workflow Sharing Risk

## Scope And Authorization

- **In scope:** ComfyUI installs, models, and workflow JSON/PNG you own or are allowed to review.
- **Out of scope:** planting malicious nodes/workflows; scraping private Civitai/HF content against ToS; attacking third-party Comfy deployments.
- Prefer isolated VMs/containers for untrusted workflows.
- Redact API keys, proxy URLs, and face/PII from shared graphs.
- Pair with `secrets-management-hygiene` and `code-quality-standards` for custom nodes.

## When To Use

- Publishing or receiving `workflow.json` / graph-in-PNG metadata.
- Enabling **custom nodes** from git URLs in shared packs.
- Corporate policy for genAI asset exchange.
- Tokens: ComfyUI, custom nodes, workflow JSON, pickle model risk, RCE via nodes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General ML supply chain | `ai-ml-security` |
| Secrets program | `secrets-management-hygiene` |
| Web app CMDi on a server | `cmdi-command-injection` |
| Container hardening broad | container security skills |

## Risk Catalog

| Risk | How it shows up | Mitigation |
| --- | --- | --- |
| Secrets in graph | API keys in node widgets, env echoes | Strip before share; use env/secret store |
| Malicious custom node | `pip install` / git clone on import | Pin reviewed repos; allowlist; no auto-update |
| Pickle / model exec | `.ckpt`/`.pt` arbitrary code on load | Prefer safetensors; scan; sandbox |
| Path abuse | Nodes read/write absolute paths | Constrain to output dirs; review nodes |
| Remote fetch | Nodes pull URLs at run | Block egress or allowlist |
| PII / faces | Training images, OCR text in previews | Consent + retention policy |
| Supply chain zip | “Workflow pack” with binaries | Hash pin; virus scan; offline review |

## Workflow

### 1. Confirm scope and success criteria

1. Who shares with whom; network isolation level; allowed model sources.
2. Success: shared workflows contain no secrets; untrusted graphs run only in sandbox; custom nodes allowlisted.
3. Incident path if key leaked in a public workflow.

### 2. Inventory local Comfy setup

```bash
# Typical layout (paths vary)
ls custom_nodes/
ls models/
# Search workflows for secrets
rg -n "api[_-]?key|token|password|sk-|BEGIN " workflows/ --glob '*.json'
```

1. List third-party custom nodes and git remotes.
2. Note whether Comfy listens on `0.0.0.0` (network exposure risk).

### 3. Sanitize before share

1. Export workflow; open JSON; remove:
   - API keys, cookies, proxy credentials
   - Absolute internal paths with usernames
   - Private URLs with tokens in query string
2. Prefer **safetensors** references; document required models by hash/name without bundling untrusted binaries if policy requires.
3. Strip PNG metadata workflows if policy forbids hidden graphs.

### 4. Receiving untrusted workflows

| Step | Action |
| --- | --- |
| 1 | Open JSON in editor **before** run; no auto-execute |
| 2 | Diff custom node requirements vs allowlist |
| 3 | Run in VM/container without secrets mounted |
| 4 | Deny network unless required; monitor outbound |
| 5 | Load models only as safetensors when possible |
| 6 | Promote to trusted only after review |

### 5. Harden runtime (owned servers)

1. Do not expose ComfyUI admin UI to Internet without Access/VPN (`cloudflare-access-policies` / tunnel patterns).
2. Separate service account; no home-directory secrets.
3. Read-only model volumes where possible; dedicated output dir.
4. Pin custom node commits; record SBOM-like list.

### 6. Verify

```bash
# After sanitization
rg -n "api[_-]?key|token|password|sk-" share/workflow.json && echo "FAIL: secrets?" || echo "no obvious secrets"
# Sandbox run produces expected images without unexpected egress (firewall logs)
```

1. Confirm shared pack installs only allowlisted nodes.
2. Spot-check that pickle ckpt load is blocked or warned per policy.

### 7. Hand off policy

1. Written team rules: allowlisted nodes, model formats, share checklist.
2. Incident: rotate keys if published; take down public gist.
3. Training for artists/engineers on graph hygiene.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Share | Sanitized JSON + model list | Full home directory zip |
| Nodes | Pinned allowlist | Random git install on prod GPU box |
| Models | safetensors + hashes | Mystery .pt from chat |
| Network | Isolated Comfy | Open UI on 0.0.0.0/0 |
| Secrets | Env injection on trusted only | Keys in node defaults |

## Output Checklist

- [ ] Share/receive policy defined
- [ ] Secret scan of workflows clean
- [ ] Custom nodes allowlisted and pinned
- [ ] Untrusted path uses sandbox
- [ ] Prefer safetensors documented
- [ ] UI not anonymously Internet-exposed
- [ ] Incident rotation path ready
- [ ] Residual risks accepted (research nodes, etc.)

## Rules

- Owned/authorized genAI environments only.
- Never weaponize workflow packs.
- Prefer isolation and allowlists over trust-me sharing.
- Focus on **workflow sharing risk**; broad ML system review is `ai-ml-security`.
