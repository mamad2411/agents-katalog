---
name: confidential
description: >-
  Use when encrypting, decrypting, password-protecting, locking, unlocking,
  signing, or verifying confidential content. Routes across cryptoid (Hugo
  markdown), pagevault (HTML and files for the browser), and gpg (signing and
  offline archives).
---

# Confidentiality Toolkit

Pick the right tool for what needs protecting, apply it, and optionally sign the result.

## Tool Selection

| Signal | Tool | Why |
|--------|------|-----|
| Hugo site, markdown under `content/`, `_index.md` cascade, `.cryptoid.yaml` | **cryptoid** | Multi-user/group whole-page encryption integrated with the Hugo build |
| HTML files, built site output, PDFs/images for web delivery, `<pagevault>` tags | **pagevault** | Section-level or whole-file encryption, self-contained HTML with viewers |
| Signing, signature verification, offline archives, `.gpg`/`.sig` files | **gpg** | Detached signatures, public-key encryption, passphrase archives |

### Decision Tree

```
Is the target Hugo MARKDOWN content (files under content/)?
  YES -> cryptoid
  NO  -> Is this HTML, built site output, or a file meant for browser viewing?
    YES -> pagevault
    NO  -> gpg
```

Hugo carve-out: cryptoid encrypts markdown only. Hugo assets (PDFs, images in
`static/`) and built HTML go to pagevault, even on a Hugo site.

Override: if the user names a tool explicitly, use it.

### Compound Workflows

- **Encrypt and sign**: lock with pagevault (or build the cryptoid-encrypted site), then `gpg --detach-sign` the output.
- **Verify then decrypt**: verify the signature against the expected signer's fingerprint (not just "Good signature"), then `pagevault unlock`. Recipe in `gpg.md`.
- **Web delivery plus archive**: `pagevault lock` for browser access, `gpg -e` the original for offline backup.

## Safety Rules (apply to every tool)

- **Secrets never on argv.** Do not pass passwords with `-p`, `--passphrase`, or `echo "pw" |`: argv is visible in `ps` and literals land in shell history. Use the tool's prompt, its config file (`.pagevault.yaml`, `.cryptoid.yaml`), the `PAGEVAULT_PASSWORD` environment variable, or gpg's `--passphrase-file`/`--passphrase-fd 3`.
- **Config files hold cleartext credentials.** `.cryptoid.yaml` and `.pagevault.yaml` must be in `.gitignore`.
- **Private source repo.** cryptoid restores plaintext after each build and pagevault leaves the unlocked originals in place, so the source repo holds plaintext. It must be private, or the plaintext must never be committed.
- **Strong passphrases.** Ciphertext is published and PBKDF2 (310,000 iterations) is the only brake on offline guessing. Use long random passphrases, not memorable words.
- **Deploy the locked files.** pagevault never overwrites its input: HTML goes to `_locked/` (or `-d DIR`), other files to a sibling `.html` (or `-o FILE`). cryptoid encrypts `content/` in place until `cryptoid decrypt`. Confirm the deployed files are the locked ones.

## Tool References

Read the reference for exact commands before running anything:

- cryptoid (config, cascade rules, build workflow, user/group management): `${CLAUDE_PLUGIN_ROOT}/skills/confidential/references/cryptoid.md`
- pagevault (lock/unlock/mark, output paths, multi-user sync, Hugo integration): `${CLAUDE_PLUGIN_ROOT}/skills/confidential/references/pagevault.md`
- gpg (signing, pinned verification, offline archives): `${CLAUDE_PLUGIN_ROOT}/skills/confidential/references/gpg.md`
