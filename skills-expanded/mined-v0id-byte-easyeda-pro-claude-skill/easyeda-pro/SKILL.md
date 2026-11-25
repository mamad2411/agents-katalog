---
name: easyeda-pro
description: Edit, fix, audit, or reverse-engineer schematics in EasyEDA Pro / LCEDA Pro / JLCEDA / 嘉立创EDA专业版 (立创EDA) — driving it through the official Extension API & WebSocket bridge, a third-party MCP server, or computer-use as a GUI fallback — and verifying every change against the exported netlist instead of the canvas. Use when the user wants to modify a schematic, fix circuit/connectivity defects, rename nets, connect floating/unconnected pins, add / move / delete / replace components, swap a chip part variant, wire SPI/power/ground, ground a thermal pad, or check a design's connectivity in EasyEDA Pro / LCEDA Pro / 嘉立创EDA / JLCEDA / EasyEDA. Encodes the netlist-first verification discipline (works no matter how you edit), the per-pin net-port connectivity model, the official API / MCP options (easyeda-api-skill, pro-api-sdk, jlcmcp, EasyEDA Pro MCP), the delete-no-connect-flag → place-net-port → draw-wire GUI workflow, Allegro .tel netlist export + grep/diff recipes, the .eprj2/.epro2 file formats, computer-use gotchas (stuck tools, occlusion freeze, 900s idle-timeout connector drops), and the "hand the user a precise change-list and verify via netlist" division of labor. Also covers PCB autorouting & copper (§10): the native autorouter (布线→自动布线 with 忽略网络 + 移除) beats the Freerouting DSN→SES round-trip (which drops pours + the per-object clearance matrix and yields near-0 via gaps), copper-rebuild is GUI-only (铺铜管理器→重建所有), DRC rules read via API but write-via-API hangs (edit in the GUI 设计规则 dialog), the pcb_PrimitiveLine/Via/Pour/Component copper API + layer IDs, an API routing-quality audit (detour ratio), and save/tab-reopen context traps that can silently lose a whole route.
version: 1.3.0
---

# EasyEDA Pro / LCEDA Pro / 嘉立创EDA专业版 — schematic editing & netlist-verified fixes

For editing, fixing, and auditing **schematics** in EasyEDA Pro (international name) =
LCEDA Pro = JLCEDA = **嘉立创EDA专业版** (立创EDA专业版) — JLCPCB's pro EDA tool.

You can drive it **programmatically** (official Extension API / WebSocket bridge, or a third-party
MCP server) or, as a fallback, by **computer-use** on the GUI. Whatever the editing channel, the one
discipline that makes AI-driven schematic work reliable is the same:

## 0. Prime directive: verify with the NETLIST, not your eyes (or the API's "OK")

A change that *looks* applied — on the canvas, or in a successful API call — can still be wrong: a net
port one pixel off a pin doesn't connect; an API edit can land on the wrong net; a part swap silently
remaps pin functions. So, regardless of how you edit:

> **After every change, export the netlist and check connectivity in the exported text — never trust
> the screenshot or a bare "success".**

The netlist is the single source of truth. It catches the failures everything else hides:
- **Virtual connections** — a port/wire/edit that looks attached but isn't (the pin is simply absent
  from the net).
- **Silent net merges** — e.g. one bad import collapsed three separate 5 V rails
  (`5V_A`/`5V_B`/`5V_SYS`) into a single 71-pin net. Invisible on the canvas, obvious in the netlist.
- **Part-swap pin remaps** — a pin-compatible variant keeps pin *numbers* but changes pin *functions*;
  the netlist (pin-number based) shows whether you wired the new function.

Workflow shape for any task, any channel:
1. Open the project. **Export a baseline netlist** and read it — ground truth for "before".
2. Make a small, scoped change.
3. **Re-export the netlist**, grep/diff the affected nets/pins against what you intended.
4. Only move on once the netlist confirms it. Repeat.

## 1. Editing channels — prefer the API/MCP; computer-use is the fallback

EasyEDA Pro **does** have programmatic access (this surprises people — there's no REST API, but there
is an in-app JS Extension API reachable over a local WebSocket bridge). Prefer it:

- **Official Extension API + WebSocket bridge** — the most authoritative path.
  - [`easyeda/easyeda-api-skill`](https://github.com/easyeda/easyeda-api-skill) — EasyEDA's *own* AI
    skill: load the `run-api-gateway.eext` extension, it starts a local bridge on ports
    **49620–49629**, then run any EasyEDA Pro JS API call via `curl -X POST localhost:49620/execute -d
    '{"code":"..."}'`. Works with Claude / the Agent Skills standard.
  - [`easyeda/pro-api-sdk`](https://github.com/easyeda/pro-api-sdk) + docs at
    `prodocs.easyeda.com/en/api/` — the full Extension API surface (project, schematic, PCB,
    components, DRC, export).
  - ⚠️ **macOS bridge gotcha (verified, fixable):** `easyeda-api-skill`'s bridge binds
    **`127.0.0.1` (IPv4 only)** but the in-EDA extension dials `localhost`, which on macOS resolves
    to **IPv6 `::1`** first — so the extension can't find the bridge ("未找到 Bridge 服务 / Bridge not
    found", retries N/5 then gives up) even though `curl http://127.0.0.1:49620/health` works for you.
    Fix `scripts/bridge-server.mjs`: bind **dual-stack** (`LISTEN_HOST = '::'`) **and reject
    non-loopback peers** in the HTTP + WS handlers (so the code-exec endpoint stays local-only), or
    listen on both `127.0.0.1` and `::1`. Verify with `curl` on `127.0.0.1`, `localhost`, and `[::1]`.
    After fixing the bridge, the extension must **re-attempt** once (re-open/re-run it, or restart the
    EDA) — it doesn't auto-rescan after giving up.
  - ⚠️ **#1 connect blocker — extension settings:** in EasyEDA's **扩展管理器 (Extension Manager)** the
    `run-api-gateway` extension must have **"允许外部交互" (Allow external interaction)** *and* **"显示在顶部菜单"
    (Show in top menu)** checked. Without "allow external interaction" it **silently never connects** (no error
    on the bridge — just `edaConnected:false` forever). It also does **not** auto-connect on EDA launch; once the
    setting is on, run it from the top **API Gateway** menu.
  - ⚠️ **Before SCH/netlist APIs work:** a **project must be open** and a **schematic document active** in the
    editor, or calls return `null` / `"i is not iterable"`. `getAllProjectsUuid()` does **not** list local on-disk
    projects (returns 0) — open the project from the start page first (computer-use double-click, or `openProject`).
  - ⚠️ **`eda.sch_Netlist.getNetlist()` can exceed the bridge's 30 s request timeout** on a real multi-sheet board
    (`REQUEST_TIMEOUT_MS` in bridge-server.mjs). Raising it requires restarting the bridge — which drops the EDA
    connection (must re-open the extension after). For per-edit verification, prefer a **GUI netlist export (.tel)**
    or targeted SCH reads over `getNetlist`. Net read/edit on the schematic is via the `SCH_*` primitive classes
    (`getAllPrimitiveId({allSchematicPages:true})`, etc.), not a single netlist call.
- **Third-party MCP servers** (stdio MCP → WebSocket gateway → in-app bridge extension):
  - [`hyl64/jlcmcp`](https://github.com/hyl64/jlcmcp) — ~39 tools incl. **read schematic, export
    netlist, schematic DRC**, component move/place, routing, copper, impedance calc.
  - [`QuincySx/easyeda-pro`](https://www.pulsemcp.com/servers/quincysx-easyeda-pro) — ~72 tools,
    schematic→PCB→manufacturing.
  - [`sengbin/JLCEDA-MCP`](https://github.com/sengbin/JLCEDA-MCP),
    [`txwilliam/LCEDApro-mcp-extension`](https://github.com/txwilliam/LCEDApro-mcp-extension).
- **EasyEDA's in-app AI assistant** also ships an MCP build (real-time schematic refresh/review).

Use **computer-use** (sections 5–6) only when the bridge/MCP isn't set up, for a quick one-off, or for
cross-app workflows. It's slow and brittle (see the gotchas) — set up the API/MCP for anything beyond
a few edits.

> Reality check: these channels let you *make* changes faster, but none of them *verify* connectivity
> for you. Section 0 still applies. The unique value of this skill is the verification discipline +
> mental model + fallback playbook below — it sits on top of whatever channel you use.

## 1.5 Driving the official API directly — the recipes this skill was forged on

When the bridge is up (§1) you edit via `eda.sch_*` JS classes over `curl /execute`. Mechanics, all
**verified live on a real 5-sheet board**:

**Reads — arrays in, plain values out.**
- `eda.sch_PrimitiveComponent.get(id)` returns an **array**; the component is `[0]`. Its getters
  (`designator`, `net`, `x`, `y`, `componentType`…) are live accessors that **don't survive
  `JSON.stringify`** — extract the fields **inside** the executed code, return plain values.
- `componentType` ∈ `"part"|"netport"|"netflag"`. **Net ports/flags are components** whose **`.net`** is
  the net name and `.x/.y` the location — that's how you read connectivity.
- `getAllPinsByPrimitiveId(id)` → `{pinNumber, pinName, x, y, noConnected}`. Pins **don't carry their
  net** (the net is whatever port/wire sits at the pin's coordinate). `noConnected` is a **static
  load-time attribute**, *not* live connectivity — it won't flip when you wire the pin.
- `getAllPrimitiveId()` is scoped to the **active page only** (`{allSchematicPages:true}` → 0). To work
  another page the **user switches the page tab** — there's no reliable API page-switch.

**The verification oracle: a geometric netlister (because `getNetlist()` HANGS).**
`eda.sch_Netlist.getNetlist()` **hangs forever** on a real board (pops a GUI dialog; never returns, not
even at a raised 90 s bridge timeout). Build the netlist yourself:
- `eda.sch_PrimitiveWire.getAll()` → each wire has **`.net`** (resolved name, may be `""`) and **`.line`**
  = flat `[x1,y1,x2,y2,…]` polyline.
- **Union-find over coincident coordinates**: union all vertices of each wire; a port at `(x,y)` and a pin
  at `(x,y)` are the same node. Propagate **names** from ports (`.net`) + named wires. A pin's net = the
  named net of its component. Reproduces `getNetlist` in ms — your per-edit check.
- ⚠️ `wire.net` is a **stale cache** — after you add/remove a port it may not refresh until export. Trust
  the **port** names + geometry; the GUI `.tel`/`.net` export re-resolves and is final ground truth.

**Editing primitives:**
- **`createNetPort(type, net, x, y, rotation, mirror)`** — `type` ∈ `"IN"|"OUT"|"BI"`. The port's
  **connection pin lands exactly at `(x,y)` for any rotation** (calibrate: create one at a free spot, read
  its pin back, delete). **To connect a pin, place a port at the pin's exact `(x,y)`** — coincidence =
  connection, no wire needed.
- ⚠️🔄 **Created net ports face INWARD → DRC fails → flip them 180°.** A fresh port's pentagon points
  back at the pin/component; EasyEDA DRC flags it. The connection point is at the origin either way, so the
  flip is DRC-cosmetic — but **the board won't pass DRC until each created port is rotated 180° to point
  outward**. (Re-orienting a net port = delete + re-create with the flipped rotation — see below.)
- **`modify(idOrObj, {x,y,rotation,designator,…})` works on PARTS ONLY** — it **throws on net ports**
  ("仅当器件类型为元件时允许修改"). So **rename / re-orient / move a net port by delete + `createNetPort`**, never
  modify. (modify negates y internally — `r=-r` — but that matches `create`'s `y:-this.y`, so passing only
  `{designator}` keeps a part's position.)
- **`delete([ids])`** on `sch_PrimitiveComponent` / `sch_PrimitiveWire`.

**Delete / replace leave debris the NETLIST hides but DRC catches:**
- ⚠️ **Deleting a net port leaves a stale zero-length stub wire** at its coord with the **old net name** →
  coincides with your replacement → **phantom short** in the union-find. After every port rename, **delete
  the leftover stub**.
- ⚠️ **Deleting a *component* orphans its net-port labels + wires** (float in space, no pin under them).
  The **netlist won't show them** (floating ports add no pins) — **DRC will** ("单网络 / floating port").
  Sweep for ports whose node has no part pin (and wires touching none) and delete.
- ⚠️ **Replacing a part with a different footprint disconnects EVERY pin** (SOT-23 → SO-8: all pin coords
  move, old wires dangle). Re-wire **all** pins, and **tie every paralleled pin** (an SO-8 MOSFET has
  3×Source + 4×Drain — all must reach the same net or they read floating). Name the previously-unnamed
  local nodes (e.g. gate/drain) so you can attach the new pins by net name.

**Bridge ops:** restarting the bridge is **safe** — the extension **auto-reconnects in ~18 s**, no user
action (but raising `REQUEST_TIMEOUT_MS` won't rescue `getNetlist` — it hangs, not times-out).

**Verify design intent against DATASHEETS, not just connectivity.** A perfectly-connected netlist can
still be a **don't-fab** board. Pull the real datasheet for the critical ICs and check what the netlist
can't see — e.g. TI **DRV8316C**: *"If the buck regulator is unused, SW_BK/GND_BK/FB_BK cannot be left
floating or connected to ground"* (must add RBK/LBK + CBK); ams **AS5047P**: *"In 3.3V operation, VDD and
VREG must be tied together"* (so VDD→5V **and** VDD3V3→3V3 is a wrong mix — LDO output fighting external
3.3V). These are P0s a connectivity check sails right past.

## 2. Mental model: per-pin **net ports** define connectivity

In EasyEDA Pro schematics, nets are usually defined by **per-pin net ports / net labels**
(网络端口 / 网络标签) — the flags carrying a net name next to each pin — **not** by long drawn wires.
Two pins share a net because their ports share the same **name**.

Consequences (true for API edits and GUI edits alike):
- **Renaming a net = renaming net ports.** Changing one port's name moves *only that pin*. To rename a
  whole net you must change **every** port on it, or the net splits.
- **Moving a pin to another net = renaming its port** (e.g. move a cap's hot pin from `24V_BUS` to `VM`).
- **Connecting a floating pin = adding a port** (after removing any no-connect flag).
- A net's true membership is whatever the netlist says — always re-derive it from the export.

## 3. File formats (so you know what's editable)

| File | What it is | Editable? |
|---|---|---|
| `*.eprj2` | The project. **SQLite**; schematic data is an **encrypted blob** in `history_data`. | Not directly — edit via the API/MCP or GUI. |
| `*.epro2` | An **export** of the project. A **zip**; inside, the `.epru` is **plaintext** (`head\|\|body\|`, `\n`-separated), round-trips losslessly. | Scriptable, **but re-importing can silently merge nets** — verify hard, or avoid the import path. |
| `*.tel` | A **netlist** export (Allegro Telesis format). Plaintext, lists every net and its pins. | **Read-only ground truth — your verification oracle.** |

⚠️ Component `id`s can repeat **across pages**; if you parse `.epru`, index **per page** (`SCH_PAGE`).

## 4. Operation goals (express via API, MCP, or GUI)

These are the connectivity goals; achieve them through whichever channel, then verify in the netlist.

- **Rename a net / move a pin to another net** — change the pin's net-port name to the target net.
- **Connect a floating pin to a net** — remove its no-connect flag, then give the pin a port on the
  target net.
- **Add / delete / move a component**; **change a value**; **replace / swap a part variant** ⚠️ — after
  a swap, pin *numbers* stay but pin *functions* change (e.g. a motor driver's pins 33–36 go from
  `MODE/SLEW/OCP/GAIN` on the hardware variant to `SDO/SDI/SCLK/nSCS` on the SPI variant). Re-wire by the
  **new** function and verify the netlist pin assignments.
- **Export the netlist** for verification (Allegro `.tel`).

## 5. Fallback channel — driving the GUI with computer-use

When you must use the GUI. Menu names in English (中文).

- **Export netlist**: `Export → Netlist` (导出 → 网表文件) → **Allegro(.tel)** → save to disk. Give each
  export a distinct name; don't overwrite your baseline.
- **Rename a net / move a pin**: click the pin's net port → Properties → **名称 (Name)** → type the new
  net → Enter. Changes only that port; repeat for every port that must move. Then re-export & verify.
- **Connect a floating pin** (robust recipe):
  1. Delete the **no-connect flag** (非连接标识, green ✗): click it → `Del`.
  2. `Place → Net Port` (放置 → 网络端口, the "input" pentagon): single-click *next to* the pin.
  3. Name it: select → Properties → **名称** → target net (`GND`/`AVDD`/`3V3`…).
  4. `Place → Wire` (放置 → 导线): draw from the **pin endpoint** to the **port's connection point**.
  5. `Esc` (if it won't exit, **right-click** to cancel — see gotchas). Re-export & verify.
- **Add a component**: `Place → Component` (放置 → 器件, Shift+F) → search part → place → wire.
- **Batch the select→edit cycle** in one `computer_batch`: `left_click(port)` →
  `triple_click(Properties 名称 field)` → `type(name)` → `key(Return)`; chain several pins per batch.
- **Zoom before clicking tiny targets**; **cross-probe** via the Networks panel (网络) to jump to a pin;
  **save** (`Cmd/Ctrl+S`) before exporting.

## 6. computer-use gotchas (macOS — hard-won)

- **Placement tools get STUCK active.** After `Place → Net Label/Wire`, the tool often **won't exit on
  `Esc`**, and then **every click places another element** (NET1, NET2, … pile up; stray wires grow).
  Fix: **right-click to cancel**, *then* the tool is off and `Cmd+Z` works.
- **`Cmd+Z` follows focus.** If the panel search box has focus, undo edits the search text, not the
  schematic. Click an empty canvas spot to focus first — but only when no placement tool is active.
- **Copy-paste of a net port can spawn junk** (once produced a stray capacitor). Prefer place-port+wire.
- **Occlusion render-freeze.** If the agent's window is fully covered, macOS suspends its painting —
  stale frame, can't read/reply, though input still works. Use a **second display**, or tile so a sliver
  stays visible; never run the target app in true-fullscreen. (Launch flags
  `--disable-renderer-backgrounding --disable-backgrounding-occluded-windows
  --disable-background-timer-throttling` are the deeper fix.)
- **Connector drops after ~15 min idle.** The desktop app's IdleManager tears down computer-use after
  ~900 s idle with no auto-reconnect (`ToolSearch "computer-use"` returns nothing mid-task). Work in
  continuous bursts; re-verify the connector after any lull. This idle drop is a big reason to prefer
  the API/MCP, or the hand-off pattern below, for long jobs.
- **Frontmost-app gate.** If a non-allowlisted app is frontmost, clicks are rejected; bring the EDA
  forward (`open_application`) and retry.

## 7. When automation is slow/flaky: hand off + verify

If the API/MCP isn't set up and the GUI work is dozens of placements over a flaky connector, the
high-leverage split is:
- **You** produce a precise, netlist-grounded **change list** — per sheet, each item
  `[location] current → target + exact action`, with done-markers and a how-to cheat sheet.
- **The user** (fast in the EDA) executes it.
- **They export a netlist per page and send it; you verify it to the net** — every intended connection
  present, no shorts, no typos, no virtual connections — and point to the exact pin/net to fix.

The human is faster at GUI manipulation; you are better at exhaustive, exact connectivity checking.

## 8. Netlist verification recipes (shell)

The `.tel` is Allegro Telesis: a `$PACKAGES` block (`footprint ! footprint ! value ; REFDES…`) then a
`$NETS` block (`'NETNAME' ; refdes.pin refdes.pin …`), with indented continuation lines.

```bash
# Which net is a pin on, and is it where you intended?
grep -nE "U10\.26( |$)" netlist.tel

# Full membership of a net (handles multi-line continuations):
awk '/^.?GND.? ;/{p=1} p{print} p&&/^[^ '\'']/&&!/GND ;/{exit}' netlist.tel \
  | grep -oE "U10\.[0-9]+" | sort -t. -k2 -n

# Did a part-swap wire SPI correctly? (pin numbers, by net)
grep -E "^'SPI_(MISO|MOSI|SCLK|CS_DRV)'" netlist.tel

# Are rails still separate (no silent merge)?
grep -E "^'?5V_(A|B|SYS)'? ;" netlist.tel        # expect three distinct lines

# Any stray auto-named nets from a botched placement?
grep -nE "^'?NET[0-9]+'? ;" netlist.tel || echo "clean"
```

Confirm per change: the **new** net contains the pins it should, the **old** net no longer does, and no
third net absorbed anything.

## 9. End-of-job checklist
- [ ] Every net port you **created via the API is flipped 180° to face outward** (else DRC fails).
- [ ] No **orphaned ports / dangling wires / stale stubs** left by deletes, port-renames, or part-replaces.
- [ ] Critical ICs checked against their **datasheets** (unused-pin handling, supply modes) — not just connectivity.
- [ ] Global **DRC** passes: no unconnected, no single-pin nets, no shorts.
- [ ] Rails that should be separate are still separate in the netlist.
- [ ] Every "connect X to Y" landed (pin present in the target net) — from a fresh export.
- [ ] Any swapped part is wired by its **new** pin functions.
- [ ] One final full-project netlist export, diffed against the baseline, reviewed end to end.

## 10. PCB autorouting, copper & the PCB API (hard-won on a dense 4-layer board)

§0–9 are about **connectivity** (schematic). This section is the **PCB layout/routing** playbook —
different APIs (`pcb_*`), different traps. Layout-time, the netlist is already fixed; here the oracle is
the **DRC panel** + per-net geometry you read back over the API.

### Decision: use the **native autorouter**, not Freerouting
EasyEDA Pro's built-in autorouter (`布线 → 自动布线`) **respects the in-app DRC rules + copper pours
natively** and gave a clean result (signals routed with ~2 spacing errors on a dense board where only
Top+Bottom carry signal). **Freerouting via the DSN→jar→SES round-trip is a dead end for the *final*
board** (below). Reach for the native router first; don't sink hours into Freerouting.

### ⚠️ Why Freerouting round-trips fail here (so you can skip it)
The toolchain *runs* but the output is unmanufacturable:
- **Export DSN:** `eda.pcb_ManufactureData.getDsnFile(name)` → `File`; `await f.text()`.
- **Pours export as `plane 0` (i.e. NOT exported)** → Freerouting is blind to your copper pours, so you
  must **strip the poured nets from the DSN `(network)` AND `(class)` blocks** (paren-balanced delete) or
  it routes GND/power as tracks fighting the pours.
- **The per-object-type clearance matrix collapses** to one per-class clearance in the DSN (track-track
  ~4mil exported; track-**via** 6mil / track-**copper** 10mil are LOST) → it packs tracks too tight.
- **Run headless** (Java 25 runs the 2.2.4 jar): `java -Djava.awt.headless=true -jar
  freerouting-2.2.4.jar -de in.dsn -do out.ses -mp 30 -da` (`-da` = no telemetry).
- **Import SES:** `eda.pcb_Document.importAutoRouteSesFile(file)` — build the `File` from **base64**
  inside the bridge eval. It **ADDS, doesn't replace** → delete existing tracks/vias first.
- **The killer:** after import, track-to-via gaps land at **~0–4mil regardless of the DSN clearance**
  (re-routing at 4→6mil gave *identical* violations — 107 on our board). It's an SES-import artifact,
  not fixable from the DSN. Abandon → native router.

### Native autorouter — the winning config (`布线 → 自动布线`)
- **忽略网络 (ignore nets):** add every **poured** net (power, and GND if you pour/plane it) so the router
  leaves them to the copper. (Dropdown adds one net per click then closes; the nets you want cluster at
  the top of the list.)
- **布线图层:** uncheck the inner layers (15/16) → route signals on **Top+Bottom only**, keep inner as
  solid GND/power planes.
- **已有导线/过孔:** **移除 (remove)** for a fresh full route. ⚠️ **保留 (keep) + 所有网络 re-processes
  already-routed nets and spawns DUPLICATE vias** (drill-to-drill at 0mil — 114 of them once). For a fresh
  route use **移除**; to add *only* a missing net, select it and use **所选网络**.
- 45° corners, 完成度优先.

### GND strategy trap
**Ignoring GND** → GND pads not physically covered by a GND pour read as **connectivity opens** (62 on
our board; the ratsnest shows far fewer — GND ratsnest is partly suppressed, so trust the DRC count, not
飞线). Either **route GND too** (include it; costs some Top/Bottom congestion + a few tight via spots) or
**stitch a via from each open GND pad down to the inner GND plane**.

### Copper rebuild is **GUI-only** and mandatory after routing
No API method exists. `工具 → 铺铜管理器 → 重建所有 → 确认`. **After ANY routing the pours are stale** and
DRC reports spurious spacing errors until you rebuild. (The right-panel `重建铺铜区` button only rebuilds
the *selected* pour.)

### DRC rules: read via API, **write via GUI**
- **Read:** `eda.pcb_Drc.getCurrentRuleConfiguration()` → `{config, name}`. Spacing matrix at
  `config.Spacing["Safe Spacing"].copperThickness1oz.tables["1"].content` — per **object-type** (rows/cols
  `[Track, SMD Pad, TH Pad, …, Via, Copper Zone, …]`; `content[5][0]` = Via-to-Track) **and** per **copper
  weight** (`copperThickness1oz / 2oz / Inner0.5oz`).
- ⚠️ **Write HANGS:** `overwriteCurrentRuleConfiguration()` (BETA) blocks forever and never applies. Edit
  the matrix in the **GUI 设计规则 dialog** (gear ⚙ next to 网络间距规则, or 设计→设计规则): double-click the
  cell → type → 确认.

### ⚠️ Save / context traps (these cost us a full route — read this)
- **Closing + reopening a PCB tab DESYNCS the bridge** — the API then reads `0 tracks` / a stale context
  even though the board clearly displays routing. **Reconnect: `API Gateway → 重新连接`.**
- **API `save()` can silently fail to persist** when the doc context is stale — we lost a complete route
  because the on-disk file was an earlier pours-only state. **After routing: save with GUI `Cmd+S` AND
  verify** by re-querying the track count over the API. Don't trust a bare `save() → true`.
- A project often holds **several PCB copies** (`PCB1`, `PCB1_1`…); reopen the *right* one.
- **Undo after a big autoroute is unreliable** (multi-step; over/under-shoots; desyncs API vs display).
  Prefer **reload-from-saved** or a **fresh re-route** over deep undo chains.

### PCB API quick reference (copper)
- **Layer IDs:** Top=**1**, Bottom=**2**, Inner1=**15**, Inner2=**16** (silk 3/4, mask 5/6, outline 11,
  multi 12, ratline 57). On PCB, `.get()` returns the object **directly** (not array-wrapped like SCH's
  `[0]`). Resolve designator→id **fresh** — changing a primitive's layer gives it a NEW id.
- `pcb_PrimitiveLine` (tracks): `get`→`{net, layer, startX, startY, endX, endY, lineWidth}`;
  `create(net, layer, x1,y1,x2,y2, width)`.
- `pcb_PrimitiveVia`: `get`→`{net, x, y, holeDiameter, diameter}`; `create(net,x,y,hole,dia,…)`.
- `pcb_PrimitivePour`/`Fill`/`Region`: pour `get`→`{net, layer, pourName,
  complexPolygon:{polygon:["R",x,y,w,h]}}` (pours are simple shapes — easy to read/emit).
- `pcb_PrimitiveComponent`: `get`→`{designator, layer, x, y, otherProperty.Footprint}`;
  `getAllPinsByPrimitiveId`→pads `{padNumber, net, x, y, layer, diameter, holeDiameter}`.
- `pcb_Layer.getAllLayers()` / `getTheNumberOfCopperLayers()`; `pcb_Document`:
  `importAutoRouteSesFile/importAutoRouteJsonFile/clearRouting/save/zoomToBoardOutline/navigateToRegion/getCalculatingRatlineStatus`.

### Routing-quality audit via API (no screenshot needed)
Grade trace lengths/paths objectively: per net, routed length = Σ `hypot(endX-startX, endY-startY)` over
`PrimitiveLine` on copper layers; via count; pad span = max pairwise pad distance; **detour ratio =
length / span**. 2-pad nets at ratio ~1.0–1.5 are direct; **>2 = convoluted** (this flagged the one
badly-routed signal — a PWM net at 13 vias / 2.2×) — all without opening a screenshot. Lengths are mostly
driven by component placement (far-apart pads), so judge *paths* by the ratio, not raw length.

### PCB end-of-job checklist
- [ ] Autoroute done with poured nets ignored, signals on Top+Bottom, inner left as planes.
- [ ] **Copper rebuilt** (`铺铜管理器 → 重建所有`) after the last routing change, *then* DRC.
- [ ] Power/three-phase widened or poured (≥40mil@1oz or copper); SW/charge-pump nets short & local.
- [ ] GND pads all connected (route GND or stitch vias to the inner plane) — DRC connectivity = 0.
- [ ] Teardrops (`工具 → 泪滴`) as the **last** step, after all tracks are final.
- [ ] Antenna keep-out honored (no copper under a module's antenna).
- [ ] **Saved via `Cmd+S` and verified persisted** (re-query track count), not just `save()→true`.
</content>
