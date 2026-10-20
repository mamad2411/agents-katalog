---
name: mobile-probe
description: Use when assessing a declared Android or iOS application under an engagement contract (static analysis, decompilation, runtime instrumentation on emulators/devices). Routes to extensions/offsec-tools/wrapper.py tools: jadx, apktool, mobsf, frida, objection. Methodology per OWASP MASVS/MASTG.
triggers: [user, model]
---

# Mobile Probe

Mobile app assessment under contract, via
`extensions/offsec-tools/wrapper.py` (domain `mobile`). Methodology:
OWASP MASVS levels + MASTG test cases.

## Contract (mandatory)

`--target` (APK/IPA path or device id), `--window`, `--roe`. ROE states
emulator vs physical device, rooted/jailbroken status, and whether
dynamic instrumentation is in scope.

## Tools

| Tool | Mode | Use |
|---|---|---|
| `jadx` | passive | DEX -> Java decompile |
| `apktool` | passive | manifest/resources/smali decode |
| `mobsf` | passive | full static+dynamic report (Docker) |
| `frida` | active | runtime instrumentation (rooted emu/device) |
| `objection` | active | runtime exploration built on frida |

## Commands

```bash
W=extensions/offsec-tools/wrapper.py

python $W run --tool jadx --target app.apk --window "..." --roe "..." \
  -- -d out_jadx app.apk
python $W run --tool apktool --target app.apk --window "..." --roe "..." \
  -- d app.apk -o out_smali
python $W run --tool mobsf --target app.apk --window "..." --roe "..." \
  --backend docker
python $W run --tool frida --target emulator-5554 --window "..." \
  --roe "..." --confirm -- -U -n com.app -l script.js
```

Static work is passive; `frida`/`objection` are `active` (attach to a
running process) -> `--confirm` and a rooted/emulated target in ROE.

## Workflow

1. Hash the package (sha256), record version/package name.
2. `jadx`/`apktool` static pass: manifest perms, exported components,
   hardcoded endpoints/keys, crypto misuse -- mapped to MASVS controls.
3. `mobsf` for the consolidated report when scope allows.
4. Dynamic only on declared emulator/device: storage, transport,
   tamper resistance via `frida`/`objection`.

## Evidence

Per finding: package sha256, MASVS control id, file/line or runtime
trace, tool version, confidence. Static findings labeled `likely` until
dynamically confirmed or code-traced.

## Boundaries

- No bypass of store/DRM/licensing mechanisms.
- Instrumentation only on declared test devices/emulators.
- Found tokens/keys are exposure evidence, not for replay against
  backends outside scope.
