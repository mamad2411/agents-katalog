---
name: authentik-gitops
description: Use when inspecting or changing darkmatter Authentik in ~/git/darkmatter/gitops — SMTP/email, MFA/2FA enforcement, blueprints, secrets, ArgoCD app values, auth flows, notification transports, or voytravel twin install.
---

# Authentik GitOps (darkmatter)

## Overview

Darkmatter Authentik is declared in `~/git/darkmatter/gitops`: Helm chart + KSOPS secret + curated blueprints. Answer “how is X wired?” from those files before guessing UI state.

**Repo roots**
- Primary: `apps/authentik.yaml` + `manifests/authentik/`
- Twin: `apps/voytravel-authentik*.yaml` + `manifests/voytravel-authentik/`

## Quick map

| Concern | Where |
|---|---|
| Argo app + Helm values | `apps/authentik.yaml` |
| Secrets (SMTP, secret key, storage, outpost flags) | `manifests/authentik/secrets.sops.yaml` via KSOPS `secret-generator.yaml` |
| Blueprint pack + mount notes | `manifests/authentik/kustomization.yaml`, `blueprints/README.md` |
| Email / notifications | `blueprints/notification-transports.yaml` + `AUTHENTIK_EMAIL__*` |
| Auth flows (passkey / password) | `blueprints/authentication-flows.yaml` |
| 2FA helper (unenforced) | `blueprints/security-factor-policies.yaml` |
| Brand / recovery flow slug | `blueprints/branding.yaml` |
| Non-blueprint tenant tweaks | `system-settings-job.yaml` (PostSync) |

## Email (SMTP)

1. **Provider (current):** **Mailgun** SMTP — `smtp.mailgun.org:587` STARTTLS, user/from `mail@mg.darkmatter.io`.
   - OP item (drkmttr): **`mailgun smtp`** UUID `sknbd7xv5ohn2lzehc7li77hhq` (vault `shared`).
   - Primary: `username=mail@mg.darkmatter.io` + top-level `password`.
   - Alt section `alt server mg.drkmttr.dev`: `mail@mg.drkmttr.dev` + second password (legacy).
   - Prior: Resend (`smtp.resend.com`, `noreply@darkmatter.io`). Cutover commit pattern: `fix(authentik): switch outbound email from Resend to Mailgun`.
2. **Env keys** on Secret `authentik-secrets` (chart `authentik.existingSecret.secretName`):
   - `AUTHENTIK_EMAIL__FROM|HOST|PORT|USERNAME|PASSWORD|USE_SSL|USE_TLS|TIMEOUT`
3. **Injection:** server + worker `envFrom` that Secret (chart existingSecret). KSOPS decrypts at Argo render time.
4. **Consumers:**
   - Blueprint transport `default-email-transport` (`mode: email`, template `email/event_notification.html`, subject prefix `darkmatter ///`)
   - Stock stages/flows (recovery, verification) use the same global Django email settings — no custom EmailStage blueprint in-repo
5. **Pitfalls:**
   - Do **not** set event transport template to `account_confirmation.html` (email-stage only). Missing `email/` prefix → `TemplateDoesNotExist` before SMTP.
   - **ArgoCD self-heal wins over bare `kubectl apply` on the Secret.** Live patch without git push reverts; worker/server can disagree. Always: SOPS → commit/push → apply/restart → verify **both** components.
   - Pods only reload `envFrom` after rollout restart.
   - Local `~/.config/sops/age/keys.txt` is often **not** the k3s recipient. Use cluster `argocd/sops-age` or OP `sops-k3s` (my.1password.com / vault `cm`).

### Decrypt / edit secrets (k3s)

```bash
kubectl config use-context default   # hz-ex63-1 — not docker-desktop
kubectl get secret -n argocd sops-age -o jsonpath='{.data.keys\.txt}' | base64 -d > /tmp/sops-age-k3s.txt
chmod 600 /tmp/sops-age-k3s.txt
export SOPS_AGE_KEY_FILE=/tmp/sops-age-k3s.txt

sops -d manifests/authentik/secrets.sops.yaml | rg 'AUTHENTIK_EMAIL' | sed -E 's/(PASSWORD):.*/\1: ***REDACTED***/'
sops set manifests/authentik/secrets.sops.yaml '["stringData"]["AUTHENTIK_EMAIL__HOST"]' '"smtp.mailgun.org"'
# ...FROM USERNAME PASSWORD PORT USE_TLS USE_SSL TIMEOUT
rm -f /tmp/sops-age-k3s.txt
```

Never paste passwords into chat/commits. Stage **only** authentik email files; leave unrelated dirty litellm/worktree noise unstaged.

### Live email outage investigation

1. Secret + **worker and server** env (`HOST/USER/FROM/PWLEN`).
2. Django via `ak shell` on worker: `settings.EMAIL_*` + `send_mail(...)`.
3. Optional raw SMTP from worker; transport template still `email/event_notification.html`.
4. Himitsu `resend/*` is for other apps — Authentik is Mailgun via OP + SOPS now.

Details: `references/email-and-mfa.md`.

## 2FA / MFA — current truth

**2FA is NOT required today.**

Evidence in gitops:
- `Has secure 2FA` expression policy checks WebAuthn enrollment but is **unbound** (file says NOT YET ENFORCED).
- Passkey validate stage: `device_classes: [webauthn]`, **`not_configured_action: skip`** → no device still proceeds.
- `password-auth-flow`: identification → login only; **no** authenticator-validate stage.
- Brand default auth flow is passkey-first; footer still offers password escape hatch via system-settings job.

| Path | Required 2nd factor? |
|---|---|
| Passkey + enrolled WebAuthn | Yes (passkey is the factor) |
| Passkey, no WebAuthn | No (skip) |
| Password flow | No |
| Policy `Has secure 2FA` | Defined only |

### Enforcing 2FA (when asked)

Decide with user first: **WebAuthn-only** vs **any MFA (webauthn/totp/…)**, and whether password login remains.

Typical levers (blueprint-first):
1. `passkey-authentication-validate.not_configured_action`: `skip` → `deny` or `configure`
2. Bind `Has secure 2FA` (or broaden expression to allowed device classes) on stage bindings — deny on false
3. Add authenticator-validate stage to `password-auth-flow` before login
4. Optionally remove/narrow password footer escape hatch in `system-settings-job.yaml`

Do not claim enforcement from policy existence alone — check bindings + `not_configured_action`.

## Blueprint workflow

1. Curate YAML under `manifests/authentik/blueprints/` with **name**-based identifiers (not pk).
2. Register file in `kustomization.yaml` `configMapGenerator` → ConfigMap `authentik-blueprints`.
3. Chart mounts ConfigMap at `/blueprints/local/` on server + worker; discovery ~5 min; no restart required for content-only changes.
4. Never commit full `ak export_blueprint` dumps (users, tokens, MFA devices, secrets).

Details: `manifests/authentik/blueprints/README.md`.

## Investigation checklist

When user asks how something is wired:
1. `rg` under `manifests/authentik` + `apps/authentik.yaml` for the concern
2. Read blueprint + secret key names (not necessarily decrypt)
3. Trace Helm values for env/volume mounts
4. State **gitops intent** clearly; live DB may drift until next blueprint apply — call out if only UI/DB could differ

## Common mistakes

- Treating unbound `Has secure 2FA` as enforced MFA
- Assuming password path has MFA because passkey path mentions WebAuthn
- Confusing user-email property mappings / GWS SCIM with outbound SMTP
- Editing chart values for secrets instead of `secrets.sops.yaml`
- Putting runtime MFA device state into blueprints
- **`kubectl apply` Secret without git push** while Argo auto-sync/self-heal is on
- Checking only worker **or** only server env after a secret change
- Using personal age key when recipient is k3s `<REDACTED>…` / `argocd/sops-age`
- Committing unrelated dirty paths (`manifests/litellm/*`) in an email fix
- Assuming Resend still serves Authentik because himitsu still has `resend/*`

## References

- `references/email-and-mfa.md` — Mailgun OP fields, path diagram, cutover/verify, MFA enforce checklist
