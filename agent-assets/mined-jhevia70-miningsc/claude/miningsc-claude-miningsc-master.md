# MiningSC — Claude Code Guide

## Project overview

**MiningSC** (`H:\Projects\SC`) is a community mining intelligence platform for Star Citizen. Three components:

1. **Web app** — Next.js 16 + Supabase, live at https://miningsc.vercel.app
2. **Desktop overlay** — Python tray app that OCRs the in-game mining panel and records GPS position
3. **Data pipeline** — Python tools that extract mineral spawn data from game files and push to Supabase

---

## Critical rules

### i18n — always bilingual
**Never hardcode user-visible strings in components.** Every string must go through `next-intl`:
1. Add key to `web/messages/en.json`
2. Add Spanish translation to `web/messages/es.json`
3. Use `t("key")` in the component via `useTranslations` / `getTranslations`

### Temp files
All intermediate/temp files go to `F:\SC_temp\` — never to `C:\` or the repo.

---

## Directory layout

```
H:\Projects\SC/
├── web/                          # Next.js web app
│   ├── src/app/[locale]/         # Pages: home, map, minerals, auth/*, account, scanner
│   ├── src/app/api/download/scanner/route.ts  # Gated installer download
│   ├── src/components/           # Navbar, Footer, AuthProvider, PlanetGlobe
│   ├── src/lib/supabase/         # client.ts (browser), server.ts (SSR)
│   ├── src/lib/mineral-aliases.ts
│   ├── src/i18n/                 # routing.ts, request.ts
│   ├── src/proxy.ts              # next-intl middleware (Next.js 16 uses proxy.ts, not middleware.ts)
│   ├── messages/                 # en.json, es.json
│   └── public/images/planets/   # Planet textures + overlay PNGs
├── supabase/
│   ├── migrations/               # SQL schema + seed data (10 migration files)
│   └── functions/                # Deno edge functions (verify-sc-handle, sync-uex)
├── src/                          # Python overlay modules
│   ├── panel_detector.py         # Screenshot -> MineralLine list
│   ├── digit_reader.py           # Template matching + CNN fallback
│   ├── digit_cnn.py              # ONNX Runtime inference (CPU only)
│   ├── sc_location.py            # /showlocation → clipboard → GPS coords
│   ├── log_reader.py             # Game.log tail → session/shard/body context
│   ├── uploader.py               # Supabase RPC upload with deduplication
│   ├── pricer.py                 # Mineral price cache + value calculation
│   ├── config.py                 # Config persistence to config.json
│   └── config_window.py          # Tkinter settings UI
├── tools/                        # Data pipeline scripts
│   ├── update_spawn_data.py      # StarBreaker -> DCB -> mineral_spawns table
│   ├── gen_mineral_overlays.py   # Splat DDS -> zone overlay PNGs
│   ├── gen_clim_overlays.py      # Clim DDS -> polar/equatorial zone PNGs
│   ├── gen_biome_overlays.py     # Splat DDS -> colorized biome PNGs
│   ├── process_ui_starmap.py     # UI starmap DDS -> 1024x512 web PNGs
│   ├── extract_hpp_zones.py      # Mineral -> biome tag from HPP JSON
│   ├── analyze_clims.py          # Per-channel stats for clim PNGs
│   ├── body_map.json             # HPP stem -> planet metadata
│   └── mineral_map.json          # Name substrings -> canonical mineral names
├── data/
│   ├── digit_templates/          # Pre-extracted digit images (0-9, ., %)
│   ├── digit_cnn.onnx            # Trained ONNX model (611 KB, CPU only)
│   └── fonts/Electrolize-Regular.ttf
├── overlay.py                    # Main overlay window + tray app entry point
├── scanner.spec                  # PyInstaller build spec
├── installer.iss                 # Inno Setup script (v1.0.2+)
├── build_installer.py            # Full build: PyInstaller → Inno Setup → GitHub Release
├── export_onnx.py                # One-time: digit_cnn.pt → digit_cnn.onnx
├── requirements.txt
└── INSTALL.md                    # Spanish installation guide
```

---

## Web app

### Tech stack
- Next.js 16.2.6, React 19, TypeScript, Tailwind CSS 4
- Supabase JS (`@supabase/ssr` for SSR, `@supabase/supabase-js` for browser)
- next-intl (locales: `en`, `es`, default `en`)
- Three.js for 3D planet globes
- Deployed on Vercel

### Deploy
```powershell
cd H:\Projects\SC\web
vercel --prod --yes
```

### Next.js 16 — proxy.ts not middleware.ts
Next.js 16 renamed `middleware.ts` to `proxy.ts`. The next-intl middleware lives at `web/src/proxy.ts`.

**Critical matcher rule:** The matcher must exclude `/api` routes or next-intl will redirect `/api/*` to `/en/api/*` (404):
```ts
export const config = {
  matcher: ["/((?!api|_next|_vercel|.*\\..*).*)"],
};
```

### Routes
| Route | Component | Notes |
|-------|-----------|-------|
| `/` | `app/page.tsx` | Redirects to `/en` |
| `/[locale]` | `app/[locale]/page.tsx` | Homepage (hero, features, stats) |
| `/[locale]/map` | `MapClient.tsx` | Interactive spawn map + 3D globe |
| `/[locale]/minerals` | `MineralsTable.tsx` | Pricing table (raw + refined) |
| `/[locale]/auth/login` | `auth/login/page.tsx` | Email + Google OAuth |
| `/[locale]/auth/register` | `auth/register/page.tsx` | Email + Google signup |
| `/[locale]/auth/callback` | `auth/callback/route.ts` | OAuth callback |
| `/[locale]/account` | `AccountClient.tsx` | SC handle verification |
| `/[locale]/scanner` | `ScannerClient.tsx` | Scanner info + download button |
| `/api/download/scanner` | `route.ts` | Gated download — redirects to GitHub Release |

### Scanner download gate
`/api/download/scanner` verifies the user has `sc_verified = true` in the `players` table, then redirects to:
```
https://github.com/JHevia70/miningsc/releases/latest/download/MiningScanner_Setup.exe
```
- Returns `401` if not logged in, `403` if not verified.
- The installer is hosted on GitHub Releases (no size limit), not in the repo or Vercel bundle.

### Minerals page classification
- No `is_raw`/`is_refined` filter on fetch (those flags are unreliable for FPS/GV minerals)
- Classification logic: suffix `(Raw)`/`(Ore)` + `is_refined` flag
- FPS/GV minerals (Aphorite, Beradom, Dolivine, Feynmaline, Glacosite, Hadanite, Janalite, Ouratite) have no refinery prices — fall back to `commodities.price_sell` for raw column
- Mineral name links to `/map?mineral=<name>`
- Alias table: `web/src/lib/mineral-aliases.ts`

### Planet globe assets (`public/images/planets/`)
- `<stem>.png` — base texture (e.g. `stanton1a.png`, `pyro1.png`)
- `<stem>_biome.png` — colorized biome overlay (Stanton only: 1a/1b/1c/1d/2b/2c/3b)
- `<stem>_zone_<tag>.png` — mineral zone mask (e.g. `stanton1a_zone_acidic.png`)
- `BODY_TEXTURE` map in `MapClient.tsx` maps body name → stem
- `BODY_HAS_BIOME` set lists bodies that have biome overlay
- `BODY_ZONES` map lists zone→mineral mappings per body

---

## Supabase

**Project**: `dtfkyacafqkrbyhgoxjk.supabase.co`

### Key tables
| Table | Access | Notes |
|-------|--------|-------|
| `systems` | Public SELECT | Stanton, Pyro, Nyx |
| `bodies` | Public SELECT | Planets, moons, belts |
| `minerals` | Public SELECT | 23 canonical names |
| `commodity_prices` | Public SELECT | Per-terminal refined prices (UEX) |
| `commodity_raw_prices` | Public SELECT | Per-terminal raw prices (UEX) |
| `mineral_spawns` | Public SELECT | 400+ rows, spawn prob data v4.x |
| `players` | Own row SELECT; anon INSERT | SC handle + verification state |
| `scans` | Public INSERT via RPC | One row per F9 scan — insert via `insert_scan_dedup` |
| `scan_minerals` | Public INSERT via RPC | One row per mineral — inserted atomically by the RPC |

### scans table columns (full)
| Column | Type | Source |
|--------|------|--------|
| `id` | bigint | auto |
| `player_id` | uuid | overlay `config.json` |
| `scanned_at` | timestamptz | overlay clock |
| `system_id` | smallint | resolved from `log_reader` body name |
| `body_id` | smallint | resolved from `log_reader` body name |
| `zone` | text | unused (null) — reserved for future biome zone |
| `station` | text | unused (null) |
| `altitude_m` | real | unused (null) — OCR removed |
| `coord_x/y/z` | double precision | `/showlocation` clipboard (metres, global system coords) |
| `raw_location` | text | raw clipboard text from `/showlocation` |
| `session_id` | text | hex session from `Game.log` Channel Connected (32 chars) |
| `shard` | text | shard name from `Game.log` @env_session |

### Deduplication RPC: `insert_scan_dedup`
**Do not INSERT directly into `scans` or `scan_minerals` from the overlay.** Always use this RPC.

Signature:
```sql
insert_scan_dedup(
  p_player_id, p_scanned_at, p_system_id, p_body_id, p_zone, p_station,
  p_altitude_m, p_coord_x, p_coord_y, p_coord_z, p_raw_location,
  p_session_id, p_shard, p_minerals jsonb
) returns jsonb  -- {duplicate: bool, scan_id: bigint}
```

Logic:
- If coordinates + session_id are present: checks for a scan by the **same player** in the **same session** within **200 m** and **±1 hour**. If found → returns `{duplicate: true}`, no insert.
- Different sessions at the same location → **allowed** (two players or two server instances).
- No coordinates → always inserts (no spatial check possible).

### RLS policies
- Static reference tables (systems, bodies, minerals, commodities): public SELECT
- `players`: authenticated users SELECT own row; anon INSERT allowed (overlay creates player row)
- `scans`/`scan_minerals`: no direct INSERT policy — all writes go through the `insert_scan_dedup` RPC which is granted to `anon`

### Edge functions
- `verify-sc-handle` — POST, auth required. Fetches RSI profile HTML, checks bio for `SCMINE-XXXXXX` code.
- `sync-uex` — POST (internal). Syncs commodities/prices from UEX Corp API.

### RPC
- `generate_sc_verify_code(p_sc_handle)` — Generates `SCMINE-XXXXXX` code, stores in `players` row.
- `insert_scan_dedup(...)` — Atomic scan insert with deduplication (see above).

### Triggers
- `on_auth_user_created` — auto-creates `players` row when `auth.users` record is inserted.

### Migrations (in order)
| File | Description |
|------|-------------|
| `20260507200246_initial_schema.sql` | Base schema: systems, bodies, minerals, players, scans, scan_minerals |
| `20260507201628_auth_and_sc_verification.sql` | Auth + SC handle verification flow |
| `20260507203306_uex_commodities.sql` | commodity_prices + commodity_raw_prices |
| `20260508120000_mineral_spawns.sql` | mineral_spawns table |
| `20260508140000_commodity_prices.sql` | Commodity price seed data |
| `20260508150000_commodity_raw_prices.sql` | Raw price seed data |
| `20260511000000_scans_location_and_bodies.sql` | zone column + missing bodies (Aaron Halo, Delamar, etc.) |
| `20260511010000_scans_coord_z.sql` | coord_z column |
| `20260609000000_scans_showlocation_coords.sql` | Spatial index on coords + updated comments |
| `20260609201044_scans_dedup_rpc.sql` | `insert_scan_dedup` RPC (initial version) |
| `20260609202708_scans_session_and_body.sql` | session_id + shard columns; updated dedup RPC with session scope |

### Applying migrations
```powershell
cd H:\Projects\SC
supabase db push
```

---

## Desktop scanner (MiningScanner)

### Architecture
Windows tray app compiled with PyInstaller + Inno Setup installer. **Does NOT require admin** — `uac_admin=False` in spec. The installer asks for admin only to write to `Program Files` (standard Windows behavior), but the app itself runs as the current user.

Entry point is `overlay.py` (name kept for historical reasons).

### Key files
| File | Purpose |
|------|---------|
| `overlay.py` | Main window: tkinter transparent always-on-top, tray icon, F9/F10 hotkeys |
| `src/panel_detector.py` | Screenshot via MSS, color-masks orange panel region, returns `MineralLine` list |
| `src/digit_reader.py` | Template matching against `data/digit_templates/`, CNN fallback |
| `src/digit_cnn.py` | ONNX Runtime inference — loads `data/digit_cnn.onnx`, CPU only |
| `src/sc_location.py` | Sends `/showlocation` to SC via WM_CHAR, reads clipboard, returns `SCCoords` |
| `src/log_reader.py` | Tails `Game.log` in background thread, extracts session/shard/body |
| `src/uploader.py` | Calls `insert_scan_dedup` RPC — never INSERTs directly |
| `src/pricer.py` | Mineral price cache + value calculation |
| `src/config.py` | Config persistence to `config.json` beside `.exe` |
| `src/config_window.py` | Settings dialog (transparency, font size, alignment, upload toggle) |
| `scanner.spec` | PyInstaller spec |
| `installer.iss` | Inno Setup script |
| `build_installer.py` | Full build orchestrator |
| `export_onnx.py` | One-time: `digit_cnn.pt` → `digit_cnn.onnx` |

### F9 scan flow (in order)
1. `get_coords()` launched in parallel thread — sends `/showlocation\r` via `WM_CHAR` to SC window, waits up to 2.5 s for clipboard update
2. MSS screenshot of the SC monitor
3. `scan_screenshot()` — OCR of the mining panel (orange region detection + digit CNN)
4. Background thread waits for coords thread to finish
5. `get_session_info()` — snapshot from `log_reader` (session_id, shard, system, body)
6. `upload_scan()` — calls `insert_scan_dedup` RPC with all data
7. Overlay redraws with mineral table + coordinates

### GPS: how `/showlocation` works
Star Citizen's `/showlocation` chat command copies to clipboard:
```
Coordinates: X: 12345678.123 Y: -98765432.456 Z: 1234567.789
```
These are **global cartesian coordinates in metres** relative to the system origin (not planet-relative). `sc_location.py` sends the command character by character via `WM_CHAR` (15 ms between chars) so SC's chat input receives it without losing characters, then polls the clipboard until it changes.

**What is NOT available without memory reading:**
- Camera/player orientation (heading, pitch, yaw)
- Shield/power/ship status
- Mineral data without OCR

### Session tracking: how Game.log works
`log_reader.py` tails `Game.log` (searched in common install paths) from the last 200 KB at startup, then follows new lines in a daemon thread. Extracts:

| Data | Log pattern | Example |
|------|-------------|---------|
| `shard` | `@env_session: 'X'` | `pub-sc-alpha-480-11825000` |
| `session_id` | `<Channel Created> ... session=X remoteAddr=<real IP>` | `c4b094984f0ae9fd1f1070757201a5c1` |
| `body` | `name: OOC_Stanton_1_Hurston` | `Hurston` |
| `system` | same OOC line | `Stanton` |

`session_id` is cleared on `<Channel Disconnected>`. `body` is set during map loading and holds until the next load. The `Game.log` path comes from `game_path` in `config.json` — the user must configure it pointing to the branch folder (e.g. `G:\Roberts Space Industries\StarCitizen\StarCitizen\LIVE` or `...\PTU`). If not configured, the log reader prints an error and session context is unavailable.

### Model: ONNX, not PyTorch
The digit CNN (`src/digit_cnn.py`) uses **onnxruntime** (CPU only), NOT torch.

**Why:** torch+CUDA weighs ~800 MB. The CNN classifies 16×16 px glyphs into 12 classes — CPU inference takes <1 ms.

**If the model is retrained** (via `train_digits.py`), re-export to ONNX before building:
```powershell
cd H:\Projects\SC
python export_onnx.py   # reads data/digit_cnn.pt → writes data/digit_cnn.onnx
```

**Do NOT reintroduce torch as a runtime dependency** in `src/digit_cnn.py`.

### PyInstaller excludes — what NOT to exclude
These stdlib modules look unused but are required at runtime by `pkg_resources` (PyInstaller bootstrap):
- `email` — **must NOT be excluded** (`pkg_resources` imports it at startup → `ModuleNotFoundError`)
- `html` — **must NOT be excluded** (same reason)

Current safe excludes: `torch`, `torchvision`, `torchaudio`, `tensorflow`, `keras`, `onnxruntime GPU providers`, `pyarrow`, `pandas`, `scipy`, `grpc`, `IPython`, `matplotlib`, `unittest`, `xmlrpc`, `http.server`.

### GPU DLL stripping
`onnxruntime` may ship GPU provider DLLs even if not installed. `build_installer.py` deletes them after PyInstaller:
```
dist/MiningScanner/_internal/onnxruntime/capi/
  onnxruntime_providers_cuda.dll      ← deleted if present
  onnxruntime_providers_tensorrt.dll  ← deleted if present
  onnxruntime_providers_rocm.dll      ← deleted if present
```
Newer onnxruntime versions may not include them at all — the build script handles both cases (`if p.exists(): unlink`).

### Current build sizes
| Artifact | Size |
|---|---|
| `data/digit_cnn.onnx` | 611 KB |
| PyInstaller bundle (`dist/MiningScanner/`) | ~133 MB |
| `MiningScanner_Setup.exe` | ~85 MB |

### Build (full, recommended)
```powershell
cd H:\Projects\SC
python build_installer.py
```

After build completes, publish to GitHub Releases:
```powershell
gh release create vX.Y.Z "F:\SC_temp\installer\MiningScanner_Setup.exe" --title "MiningScanner vX.Y.Z" --latest --notes "..."
```

The download route (`/api/download/scanner`) always points to `releases/latest/download/MiningScanner_Setup.exe` — no code change needed when releasing a new version, just publish the release with that exact filename.

### Build (manual steps)
```powershell
# Step 1 — PyInstaller
python -m PyInstaller scanner.spec --distpath F:/SC_temp/dist --workpath F:/SC_temp/build --noconfirm

# Step 2 — strip GPU DLLs (if present)
$ort = "F:\SC_temp\dist\MiningScanner\_internal\onnxruntime\capi"
@("onnxruntime_providers_cuda.dll","onnxruntime_providers_tensorrt.dll","onnxruntime_providers_rocm.dll") |
  ForEach-Object { if (Test-Path "$ort\$_") { Remove-Item "$ort\$_" } }

# Step 3 — Inno Setup
& "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss

# Step 4 — publish to GitHub
gh release create vX.Y.Z "F:\SC_temp\installer\MiningScanner_Setup.exe" --latest
```

### Inno Setup
- Installed at: `C:\Program Files (x86)\Inno Setup 6\iscc.exe`
- Script: `installer.iss`
- Features: Start Menu shortcut, optional Desktop shortcut, optional startup entry, uninstaller, kills running process before upgrade, bilingual (EN + ES)
- Admin required for installer only (writes to `Program Files`) — the exe itself runs without elevation

### GitHub repository
- Repo: https://github.com/JHevia70/miningsc
- Releases: https://github.com/JHevia70/miningsc/releases
- CLI authenticated as `JHevia70` (keyring)

### Runtime notes
- Font (`Electrolize-Regular.ttf`) registered at startup via `AddFontResourceExW`
- `config.json` written beside `.exe`, not inside the PyInstaller bundle
- `uac_admin=False` — no elevation required
- `sys._MEIPASS` used in `digit_cnn.py`, `digit_reader.py`, `config.py` for correct paths inside bundle

---

## Data pipeline

### Game files
- **Data.p4k**: `G:\Roberts Space Industries\StarCitizen\StarCitizen\LIVE\Data.p4k` (143 GB)
- **StarBreaker** (primary extractor): `F:\SC_temp\starbreaker\starbreaker.exe`
  - `unp4k` does NOT work with the current p4k format — use StarBreaker only.

### StarBreaker commands
```bash
# List files:
starbreaker p4k list --p4k <p4k> --filter "<glob>"

# Extract files (DDS -> PNG conversion):
starbreaker p4k extract --p4k <p4k> --output <outdir> --filter "<glob>" --convert dds-png

# Extract DCB to JSON:
starbreaker dcb extract --p4k <p4k> --output <outdir> --format json
```

### Extracted data locations (all on F:)
| Data | Path |
|------|------|
| DCB records | `F:\SC_temp\dcb_unfiltered\libs\foundry\records\` |
| Splat maps (biome index DDS) | `F:\SC_temp\splats\Data\Textures\planets\global\stanton\<planet>\` |
| Clim maps | `F:\SC_temp\clims\Data\Textures\planets\global\{system}\{body}\` |
| UI starmap textures (Pyro/Nyx) | `F:\SC_temp\ui_starmap\Data\UI\starmap\textures\` |
| Stanton planet textures | `F:\SC_temp\planet_textures\Data\Textures\planets\global\stanton\` |
| Planet PNGs (web-ready) | `F:\SC_temp\planet_png\` |
| Biome overlay PNGs | `F:\SC_temp\biome_overlays\` |

### Pipeline tools
| Script | Input | Output |
|--------|-------|--------|
| `update_spawn_data.py` | DCB HPP JSON | `mineral_spawns` Supabase table |
| `gen_mineral_overlays.py` | Splat DDS | Zone mask PNGs (white alpha) — Hurston, Yela, Lyria |
| `gen_clim_overlays.py` | Clim DDS | Polar/equatorial zone PNGs — all other bodies |
| `gen_biome_overlays.py` | Splat DDS | Colorized biome overlay PNGs |
| `process_ui_starmap.py` | UI starmap DDS | 1024×512 RGB PNGs for web |
| `extract_hpp_zones.py` | HPP JSON | Mineral → biome tag mapping |
| `analyze_clims.py` | Clim PNGs | Per-channel stats |

---

## Biome zone overlays

### Splat-based (Hurston, Yela, Lyria)
Splat DDS: R8_UINT 512×512 — pixel ÷ 16 = biome index (0..15)

| Body | Zone tag | Splat indices | Coverage |
|------|----------|---------------|---------|
| Hurston | acidic | 13, 15 | ~29% |
| Yela | ice | 3, 5, 6, 8 | ~90% |
| Lyria | crystaline | 3, 15 | ~51% |

### Clim-based (all other bodies)
Clim DDS channel G = temperature/latitude (0 = cold/pole, ~200 = equator)

| Body | Zone | Type | Threshold |
|------|------|------|-----------|
| Aberdeen, Arial, Ita, Daymar | desert | equatorial | G > 100 |
| MicroTech | ice | polar | G < 40 |
| Calliope | ice | polar | G < 100 |
| Pyro I, Monox, Pyro III, Bloom, Pyro V | ice | polar | G < 100 |
| Pyro VI | ice | polar (inverted) | G > 120 |

### Known limitations
- Pyro/Nyx: no biome overlays (Pyro splats only exist for pyro5a, but its HPP has `areas=[]`)
- MicroTech, Calliope, Clio (stanton4a/4b/4c): no splat files in p4k
- Aberdeen, Arial, Ita, Daymar: HPPs have `areas=[]` or all `modifiers=0` → no zone minerals
- Biome tag → splat index mapping was inferred from sparsity (not readable directly from shaders)

---

## What GPS data is available from Star Citizen (no memory reading)

| Data | Available | Source |
|------|-----------|--------|
| Position X/Y/Z (global, metres) | ✓ | `/showlocation` → clipboard |
| System name | ✓ | `Game.log` OOC lines during map load |
| Body name (planet/moon) | ✓ | `Game.log` OOC lines during map load |
| Server session ID | ✓ | `Game.log` Channel Connected |
| Shard name | ✓ | `Game.log` @env_session |
| Altitude above surface | ✗ | Only via `r_displayinfo` OCR (removed — resolution-dependent) |
| Camera orientation / heading | ✗ | Not exposed by any API |
| Shield / power / ship status | ✗ | Not exposed (GameGlass only sends key inputs, reads nothing) |

---

## Known gaps / TODO

- Home page stats ("scans", "players") are hardcoded placeholders — need live Supabase aggregation
- No scan history UI or per-user scan filtering
- No way to unlink/change a verified SC handle
- No Discord integration (referenced in footer)
- UEX sync (`sync-uex` edge function) has no pg_cron schedule — must be triggered manually
- RSI profile scraper in `verify-sc-handle` may need updates if RSI changes their HTML structure
- `zone` column in `scans` always null — planned for future biome zone detection from coords
- `Game.log` path search only covers C/D/E/G drives — could miss custom install locations
