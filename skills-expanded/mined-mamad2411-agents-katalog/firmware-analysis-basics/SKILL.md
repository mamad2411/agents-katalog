---
name: firmware-analysis-basics
description: >
  Firmware analysis basics for owned devices, vendor-supplied images, and CTF firmware
  blobs: identification, binwalk unpack, filesystem extract (squashfs, jffs2, ubifs,
  initramfs), credential/config triage, and hand-off to binary RE. Use when analyzing
  router/IoT/embedded firmware dumps under authorization—not for unauthorized device
  exploitation.
---

# Firmware Analysis Basics

## Scope And Authorization

- **In scope:** firmware you own, vendor images provided for review, CTF challenges, authorized hardware labs.
- **Out of scope:** extracting or attacking firmware on devices/networks without permission.
- Keep originals immutable; work on copies.
- Redact default credentials found if they map to live customer gear in reports shared broadly.
- Pair tool scripts with `code-quality-standards`.

## When To Use

- First-pass **firmware dump** analysis before deep reverse engineering.
- Recovering rootfs, web UI, and init scripts from router/IoT images.
- Hunting hardcoded secrets, backdoor accounts, and outdated services.
- Preparing extracted binaries for `binary-re/static-analysis` or dynamic lab work.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deep static RE of a binary | `binary-re/static-analysis` (canonical) |
| Tool install for RE | `binary-re/tool-setup` |
| Firmware update signature crypto | `firmware-update-signing` |
| Mobile app SSL pinning | `mobile-ssl-pinning-bypass` |
| Network protocol RE | `protocol-reverse-engineering` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Stage | Tools / artifacts |
| --- | --- |
| Identify | `file`, `binwalk -e`, entropy plots, header signatures |
| Extract | binwalk, `sasquatch`/`unsquashfs`, jefferson, ubireader, cpio for initramfs |
| Triage FS | `/etc/passwd`, shadow, dropbear/ssh keys, web root, `etc/config` |
| Strings | `strings`, `rg` for password/URL/private key |
| Emulate later | qemu-user/system, firmadyne-class setups (separate careful lab) |

## Workflow

### 1. Confirm scope and success criteria

1. Source of image (vendor download, device dump method), architecture hints, authorization.
2. Success: reproducible extract directory; architecture known; initial secret/service findings list; binaries staged for RE.
3. Hash original image before any modification.

```bash
sha256sum firmware.bin | tee firmware.sha256
file firmware.bin
```

### 2. Map image structure

```bash
binwalk firmware.bin
binwalk -e firmware.bin
# Optional entropy
binwalk -E firmware.bin
```

1. Note bootloader, kernel, rootfs regions, compression (lzma/gzip/xz).
2. If encrypted/unknown, document offset and stop for crypto skill—not blind guessing production keys.

### 3. Extract filesystems

```bash
# Squashfs example after binwalk carve
unsquashfs -d rootfs squashfs-root.sqsh 2>/dev/null || true
# Initramfs cpio
# skip header; cpio -idmv < initramfs.cpio
# JFFS2 / UBIFS: use dedicated extractors when binwalk alone is insufficient
```

1. Record endianness and CPU from kernel or ELF binaries: `file rootfs/bin/busybox`.
2. Preserve permissions if needed for later qemu.

### 4. Triage for credentials and attack surface

```bash
rg -n "password|passwd|private_key|BEGIN RSA|api_key|telnet|root:" rootfs/etc rootfs/www 2>/dev/null | head
ls -la rootfs/etc
cat rootfs/etc/passwd
# Web
find rootfs -type d \( -name www -o -name htdocs -o -name lighttpd \) 2>/dev/null
# Services
ls rootfs/etc/init.d rootfs/etc/rc.d 2>/dev/null
```

1. Check for world-writable scripts, setuid binaries, outdated busybox applets.
2. Inventory listening service configs (dropbear, httpd, mqtt).
3. Note update client URLs and whether signatures verified (`firmware-update-signing`).

### 5. Stage binaries for deeper RE

```bash
find rootfs -type f -exec file {} \; | rg "ELF|executable"
# Copy interesting CGI/binaries to analysis workspace; keep path metadata
```

1. Hand off with arch, libc type (uClibc/musl/glibc), and stripped or not.
2. Dynamic analysis only in isolated lab network.

### 6. Verify findings quality

1. Confirm secrets are not false positives (example.com placeholders).
2. Cross-check version strings against known CVEs carefully—cite evidence.
3. Re-run extract from clean copy if workspace contaminated.

### 7. Hand off

1. Report: hashes, extract tree summary, creds/services, recommended next RE targets.
2. Store derived artifacts separately from original.
3. Do not weaponize against unauthorized targets.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Originals | Hashed immutable copy | Overwrite dump in place |
| Extract | Documented tool versions | Random GUI unpack no notes |
| Secrets | Redacted customer-impacting | Paste live device passwords in public |
| Scope | Owned/CTF image | Random vendor firmware from customer without OK |
| Next steps | Specific ELF paths for RE | “Firmware pwned” without FS |
| Crypto | Note encrypted regions | Brute without legal/auth basis |

## Output Checklist

- [ ] Authorization and image provenance recorded
- [ ] SHA-256 of original
- [ ] binwalk map and extract path
- [ ] CPU/ABI identified
- [ ] Rootfs triage for users, keys, web, services
- [ ] Interesting binaries listed for RE hand-off
- [ ] Update signing posture noted
- [ ] Residual encrypted/unknown regions documented
- [ ] Scripts meet `code-quality-standards` if any

## Rules

- Authorization required; evidence-driven RE.
- Prefer unpack and triage before exploitation narratives.
- Keep customer-impacting credentials controlled.
- Route signing verification depth to `firmware-update-signing`; deep binary work to binary-re skills.
