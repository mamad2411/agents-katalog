---
name: cad-fusion
description: >-
  Drive Vantage CAD → Autodesk Fusion 360 via the local relay (vantage-cad CLI +
  fusion360-official-connector). Use when pairing desktops, installing the Fusion
  add-in on Windows/macOS, debugging relay jobs, or explaining that Fusion is
  never hosted on Vercel. Linux has no Fusion app — use mock or Onshape instead.
---

# Vantage CAD → Fusion 360 (local relay)

## Architecture (locked)

- **Fusion 360 is local only.** Vantage/Vercel signs approved, expiring job envelopes.
- The paired **`vantage-cad`** CLI claims jobs and POSTs them to the Fusion add-in on **loopback** (`http://127.0.0.1:32145`).
- Never claim hosted Fusion, Autodesk cloud control from Vercel, or Linux Fusion support.

## OS matrix

| OS | CLI | Fusion Autodesk app | Vantage add-in |
|----|-----|---------------------|----------------|
| Windows | Yes | Yes | Yes |
| macOS | Yes | Yes | Yes |
| Linux | Yes | **No** | **No** — use Onshape or `VANTAGE_CAD_MOCK=1` |

## Install

```bash
# Windows one-shot (CLI + Fusion add-in)
powershell -ExecutionPolicy Bypass -File .\scripts\cad\install-windows.ps1

# CLI (macOS/Linux)
bash scripts/cad/install-cli.sh

# Fusion add-in (macOS; Windows covered by install-windows.ps1)
bash scripts/cad/install-fusion-addin.sh
```

Add-in source: `packages/fusion360-official-connector/VantageCadRelay/` (see `VERSION.json`)

Optional package (unsigned): `npm run cad:package` → `dist/cad-relay/`
macOS pkg/dmg: `npm run cad:package:macos` → `dist/cad-macos/`
Linux tarball/AppDir: `npm run cad:package:linux` → `dist/cad-linux/` (no Fusion add-in)

Future signed MSI stub: `scripts/cad/windows/VantageCadRelay.wxs` (needs Authenticode cert)

## Pair + run

1. `export VANTAGE_URL=https://vantagefrc.vercel.app` (or local `http://localhost:3001`)
2. `vantage-cad setup` → approve code at `/cad/pair` for **Fusion 360**
3. Open Fusion → run **VantageCadRelay** add-in
4. `vantage-cad start` (keep running)
5. `vantage-cad doctor` — Onshape env (local) + Fusion relay `/health`
6. In Vantage CAD Builder: create Fusion job → confirm brief → plan → approve steps
7. Relay claims approved steps automatically

Mock without Autodesk: `VANTAGE_CAD_MOCK=1 vantage-cad start`

## Claude Code in the terminal

Keep Fusion open with **VantageCadRelay** running, then:

```text
npx vantage-cad fusion ping
npx vantage-cad fusion sketch --width 40 --height 20
npx vantage-cad fusion extrude --depth 10
```

Or use the repo `.mcp.json` (`fusion_status`, `fusion_sketch_rectangle`, `fusion_extrude`). Full steps: `docs/CLAUDE_CODE_CAD.md`.

## Secrets

- `FUSION_RELAY_SIGNING_SECRET` must match between Vantage server and the Fusion add-in process env (default local secret is for demos only).
- Device token stored via OS keychain/`~/.vantage-cad/credentials.json` — never commit.

When no desktop is paired or the relay is offline, CAD Builder shows **Setup required** on Fusion steps — jobs do not run on Vercel.

## Agent rules

- Mutations require human approval in the web UI (allowlisted ops only).
- Implemented add-in ops today: `create_sketch`, `create_extrude`, `verify_*` / checkpoint / render.
- Other allowlisted ops return a clear not-implemented error — do not fake geometry.
- Terminal CLI brain = `$0` Vantage model charge (`key_source=local_cli`); still not certified engineering.

## Docs

See `CAD_RELAY.md` and the Fusion connector README.
