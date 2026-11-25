---
name: gpg-signing
description: "Configure GPG commit and tag signing, verify signatures, and plan key revocation or recovery."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["gpg", "signing", "git", "keys", "verification", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# GPG Signing AI Skill Guide

## Overview & Engine Architecture

GNU Privacy Guard (GPG) provides OpenPGP keys for signing and encryption. In engineering workflows, the common use is signing git commits and tags so remotes can verify author authenticity. Agents help generate keys safely, configure git, export public keys to GitHub/GitLab, and never paste private key material into chat logs or tickets.

```
Private key (local / hardware token)
   -> gpg signs commit/tag payload
       -> Public key on Git forge
           -> UI shows Verified
```

## When to use this skill

- Enabling verified commits for a team
- Signing release tags
- Verifying a downloaded artifact signature
- Rotating or revoking a compromised signing key

## Operational directives

1. Protect private keys with a strong passphrase; prefer hardware tokens when available.
2. Never commit private keys, `.gnupg` private material, or passphrases to git.
3. Use a dedicated signing subkey when practical; keep certification key offline if policy requires.
4. Publish the public key to the forge; set `user.signingkey` and `commit.gpgsign`.
5. If a key is exposed, revoke promptly and replace signing keys in all machines/CI.

## Git signing setup

```bash
gpg --full-generate-key   # choose RSA 4096 or Ed25519 per policy
gpg --list-secret-keys --keyid-format=long

git config --global user.signingkey <KEYID>
git config --global commit.gpgsign true
git config --global tag.gpgsign true

git commit -S -m "Explain why"
git tag -s v1.2.3 -m "Release 1.2.3"
git verify-commit HEAD
git verify-tag v1.2.3
```

## Export / import sketches

```bash
gpg --armor --export <KEYID> > pubkey.asc
gpg --armor --export-secret-keys <KEYID>   # ONLY to secure backup media - never tickets
```

## Common pitfalls

| Pitfall | Result | Fix |
| --- | --- | --- |
| Email mismatch vs forge account | Unverified commits | Use the same email or add it to the forge + key UID |
| CI signs with shared unprotected key | Weak trust | Use ephemeral OIDC/sigstore where possible, or HSM |
| Lost passphrase, no revocation cert | Unrecoverable trust story | Store revocation certificate offline at key creation |
| Agent prints private key | Compromise | Refuse; rotate if already leaked |

## Best practices

- Generate a revocation certificate immediately after key creation; store offline.
- Prefer Ed25519 where org policy allows for smaller keys and modern defaults.
- Document onboarding: how new laptops import keys or use company tokens.
- For package registries, prefer ecosystem-native signing (Sigstore, npm provenance) in addition to git signing.

## Limitations

- GPG UX and agent pinentry differ across OS platforms.
- Corporate S/MIME or SSH commit signing may be mandated instead of GPG.
- Verified badges depend on forge configuration, not only local signing success.

## Related skills

- `@github-actions` - release pipelines that verify tags
- `@github-packages-npm` - publish path often paired with signed tags
- `@incident-runbooks` - steps when a signing key is compromised
