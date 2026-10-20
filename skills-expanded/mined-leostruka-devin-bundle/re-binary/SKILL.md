---
name: re-binary
description: Use when reverse-engineering a declared binary, library, APK, firmware image, or script artifact under an engagement contract (native code, .NET, Java/Android, Electron/JS, browser extensions). Routes to extensions/rea-ops/wrapper.py, a whitelist passthrough to the rea-agents CLI (Hopper/Ghidra engines probed via doctor).
triggers: [user, model]
---

# RE Binary

Reverse engineering via `extensions/rea-ops/wrapper.py` -- thin passthrough
to `rea-agents` (morluto/rea) over `npx`. The REA MCP server is
deliberately not used (126 tools exceed the per-server budget); the CLI
preserves REA's contract/evidence model.

## Contract (mandatory)

`--target` (artifact path), `--window`, `--roe` on every exec subcommand.
Analysis is read-only; destructive host actions are out of scope.

## Commands

```bash
W=extensions/rea-ops/wrapper.py

python $W doctor          # node/npx/REA + engines (Hopper/Ghidra/...)
python $W capabilities    # whitelisted subcommands + invoker
python $W analyze  --target <path> --window <w> --roe <r> [-- <rea args>]
python $W inspect  --target <path> --window <w> --roe <r>
python $W search   --target <path> --window <w> --roe <r> -- <query>
python $W function --target <path> --window <w> --roe <r> -- <addr|name>
python $W xrefs    --target <path> --window <w> --roe <r> -- <addr|name>
python $W trace    --target <path> --window <w> --roe <r> -- <spec>
python $W compare  --target <path> --window <w> --roe <r> -- <other>
```

All output is JSON; missing toolchain reports `status: missing`.
`doctor` surfaces which engines are actually installed -- absent engine =
capability `unknown`, proceed with what exists.

## Workflow

1. `doctor` once per session; note available engines.
2. `analyze` for the static baseline (imports, strings, structure).
3. `function`/`xrefs`/`search` to drill into specific behavior.
4. `compare` for diffing two artifact versions.
5. Record evidence: argv, engine, artifact sha256 (`Get-FileHash`),
   confidence, limitations.

## Adjacent tooling (fallback when REA engines absent)

`offsec-tools` wraps capa, floss, yara, rizin, ghidra headless
(domain `re`, mode `passive`): capability flags, deobfuscated strings,
signature match, CLI disassembly. Same contract fields via
`run --tool <name>`.

`extensions/rz-ops/wrapper.py` is the structured rizin path:
JSON presets (info/functions/imports/strings/disasm/xrefs/diff/find/
sign/decompile), validated tokens only, `dbg` (target execution) gated
as active mode. Self-contained; use when REA engines are `missing`.

## Boundaries

- Artifacts only; no live-process tampering without explicit ROE line.
- No malware authoring or payload synthesis.
- Findings without engine corroboration are labeled `likely`, not
  `confirmed`.
