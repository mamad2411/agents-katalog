---
name: firmware-probe
description: Use when analyzing a declared firmware image or embedded artifact under an engagement contract (extraction, SBOM, CVE mapping, config/credential review). Routes to extensions/offsec-tools/wrapper.py tools: binwalk, unblob, emba; deep RE of extracted binaries goes to re-binary.
triggers: [user, model]
---

# Firmware Probe

Firmware/embedded analysis under contract, via
`extensions/offsec-tools/wrapper.py` (domain `firmware`).

## Contract (mandatory)

`--target` (image path), `--window`, `--roe`. Extraction is read-only
against the image; emulated boot is out of scope unless the ROE says so.

## Tools

| Tool | Mode | Backend | Use |
|---|---|---|---|
| `binwalk` | passive | wsl/native | signature scan + extraction (v3, Rust) |
| `unblob` | passive | docker | deep extraction, deps in image |
| `emba` | passive | docker | full audit: SBOM, CVEs, configs, secrets scan |

## Commands

```bash
W=extensions/offsec-tools/wrapper.py

python $W run --tool binwalk --target fw.bin --window "..." --roe "..." \
  --backend wsl -- -Me fw.bin
python $W run --tool unblob --target fw.bin --window "..." --roe "..." \
  --backend docker -- fw.bin
python $W run --tool emba --target fw.bin --window "..." --roe "..." \
  --backend docker -- -f /work/fw.bin -l /work/emba_logs
```

Docker backend auto-mounts the target's directory read-only at `/work`
and rewrites the target arg. Extracted binaries needing real RE go to
`re-binary` (rea-ops wrapper, same contract).

## Workflow

1. `binwalk`/`unblob` to unpack; hash the image (`sha256`) first.
2. Inventory filesystem: versions, init scripts, certs, configs.
3. `emba` for SBOM + CVE correlation when a full report is needed.
4. Interesting binaries -> `re-binary`; interesting services ->
   `net-probe`-style reasoning (offline only).

## Evidence

Per finding: image sha256, extraction tool+version, file path inside
image, CVE/SBOM reference, confidence. Emba/CVE hits are `likely` until
version-confirmed in the extracted filesystem.

## Boundaries

- Analysis only; no flashing or writing to live devices.
- Full device emulation (firmadyne/FirmAE class) is native-linux-only --
  report `unsupported_platform` on this host rather than approximating.
- Found secrets are evidence of exposure, not material for use.
