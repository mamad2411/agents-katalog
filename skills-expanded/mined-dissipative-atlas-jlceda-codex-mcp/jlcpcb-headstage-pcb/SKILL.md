---
name: jlcpcb-headstage-pcb
description: Distill and apply PCB design knowledge from the user's JLCPCB/Lichuang EDA Pro headstage projects. Use when Codex needs to review, explain, improve, or extract lessons from 嘉立创 PCB, 立创 EDA Pro .eprj2 files, Gerber/CAM manufacturing output folders, Excellon .DRL drill files, FlyingProbeTesting.json, RHS2116/RHD2164/LFP headstage boards, 80channel_v2_top or 80channel_v2_bottom four-layer circular boards, ESP32-S3 or iCE40 control boards, wireless/power-tree boards, USB/SPI/power layout, JLCPCB BOM/LCSC part metadata, or compact 0201/0402/BGA/FPC/BTB PCB design checks.
---

# JLCPCB Headstage PCB

## Core Workflow

Use this skill as a project-specific review guide, not as an official JLCPCB fabrication rulebook.

1. If the user asks about the existing RHS2116/LFP, 80channel_v2, or power-board project family, read `references/project-lessons.md` and `references/pcb-rules.md` first.
2. If the user provides a new `.eprj2` file, run `scripts/extract_eprj2_summary.py <path-to-eprj2>` before making design claims, then compare the result with the reference files.
3. If the user provides a Gerber/CAM export folder, `.DRL` drill files, or `FlyingProbeTesting.json`, run `scripts/summarize_cam_folder.py <path-to-folder>` and read `references/cam-output.md`.
4. If the task is BOM, component choice, JLCPCB/LCSC metadata, SMT assembly, connector choice, BGA/FPC/BTB risk, or footprint risk, read `references/part-library.md`.
5. If the task is parsing or validating `.eprj2` internals, read `references/eprj2-format.md`.
6. If the user asks for current official JLCPCB manufacturing, DFM, or SMT rules, verify against official current sources before treating any number as a manufacturing limit.

## Review Priorities

Start reviews in this order:

1. Power tree: `BAT`, `VBUS+5`, `VCC`, `VCC_SW`, `VCC3V3`, `VCC1V2`, `VSTM-5`, `V_WL`, regulators/chargers/switches, return paths, and decoupling.
2. Analog/electrode interface: RHS2116/RHD2164 inputs, `A0` through `A63`, FE nets, high-impedance routing, local bypassing, quiet ground, and connector or contact-pad pinout sanity.
3. Digital interfaces: `USB_D+`, `USB_D-`, `MISO1`, `MOSI1`, `SCK1`, `CS1`, `MISO2`, `MOSI2`, `SCK2`, `CS2`, FPGA flash nets, line length, layer changes, and nearby ground return.
4. Stackup and copper planes: distinguish the two-layer LFP/power boards, four-layer 80channel_v2 `.eprj2` boards, and six-copper-layer quality-test CAM export before applying any layout heuristic.
5. Manufacturing output: Gerber layer set, board outline, drill tools, flying-probe pin/net coverage, paste/solder mask presence, and top/bottom assembly balance.
6. Compact-board manufacturability: 0201/0402 density, BGA escape, FPC/BTB connector pitch, via size, solder-mask expansion, silkscreen clearance, test pads, contact pads, and extended-part dependency.
7. Lichuang EDA project integrity: schematic-to-PCB conversion, named nets versus generated nets, BOM flags, LCSC supplier fields, active copper layers, and footprint metadata.

## Working With `.eprj2`

Treat `.eprj2` files as SQLite project databases. Do not edit them directly unless the user explicitly asks for a risky low-level repair.

Use the bundled parser:

```bash
python scripts/extract_eprj2_summary.py "C:\path\to\project.eprj2"
```

The script opens the database read-only, decodes `base64` + gzip `dataStr` payloads, counts schematic/PCB records, reports auxiliary project storage such as `project_structures` and `history_data`, reports active copper layers and `LAYER_PHYS` records, summarizes outline geometry, lists named nets and rules, groups line widths and pours by layer, reports via sizes, groups standalone pad shapes by layer, and summarizes BOM/footprint metadata.

Ignore `.eprj2-wal` and `.eprj2-shm` sidecars for skill content. They are SQLite runtime files and should not be copied into this skill.

## JLCEDA Live MCP Closed-Loop Schematic Repair

Use this workflow when the user wants Codex to fix a Lichuang/JLCEDA Pro schematic through the local extension/MCP bridge.

### Preconditions

1. The user must open the intended `.eprj2` in JLCEDA Pro, enable the Codex/JLCEDA extension, allow external interactions, and click the live bridge menu item.
2. Verify the local bridge before editing:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:38425/health' | ConvertTo-Json -Depth 8
```

3. Verify the active JLCEDA runtime project, not just the file on disk. Use `runtime-eval` to inspect `location.href`, `document.title`, and `eda.dmt_Project.getCurrentProjectInfo()`. If the runtime opened a stale historical model, manually open the correct `.eprj2` and restart the live bridge.
4. Always back up the `.eprj2` before runtime edits. After edits, save through `await eda.sch_Document.save()` and then run the bundled `.eprj2` parser read-only.

### Runtime Eval Pattern

Use the bridge endpoint for all live JLCEDA API work:

```powershell
$script = @'
return {
  href: location.href,
  title: document.title,
  project: await eda.dmt_Project.getCurrentProjectInfo()
};
'@
$body = @{ label='inspect-active-project'; timeoutMs=30000; script=$script } | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:38425/api/jlceda/runtime-eval' -ContentType 'application/json' -Body $body
```

Activate pages explicitly before reading or modifying page-local primitives:

```javascript
async function activatePage(pageName) {
  const info = await eda.dmt_Project.getCurrentProjectInfo();
  const page = info.data[0].page.find(p => p.name === pageName);
  if (!page) throw new Error("page not found: " + pageName);
  const tabId = await eda.dmt_EditorControl.openDocument(page.uuid, undefined);
  await eda.dmt_EditorControl.activateDocument(tabId || (page.uuid + "@" + info.uuid));
  await new Promise(r => setTimeout(r, 250));
}
```

Important: `eda.sch_PrimitiveComponent.getAll("part", true)` returns components from all schematic pages. Use `false` after activating a page when making page-local edits; otherwise duplicate designators from other pages can be modified accidentally.

### Getting Real DRC Details

Do not rely on `eda.sch_Drc.check()` for detailed issues. In the observed JLCEDA Pro runtime, `String(eda.sch_Drc.check)` shows that the wrapper drops the `includeVerboseError` argument and returns only a boolean. `false` can mean "warnings exist", not necessarily fatal errors.

For detailed DRC, run UI-mode DRC and capture the DRC panel export blob:

```javascript
function clean(s) { return String(s || "").replace(/\s+/g, " ").trim(); }
await eda.sch_Drc.check(false, true);
await new Promise(r => setTimeout(r, 1200));

const panel = document.querySelector("#schDrcPrimaryLog");
const buttons = Array.from((panel || document).querySelectorAll("button"));
const captured = [];
const promises = [];
const urlOrig = URL.createObjectURL;
URL.createObjectURL = function(obj) {
  const rec = { size: obj && obj.size, text: null };
  captured.push(rec);
  if (obj && obj.text) promises.push(obj.text().then(t => { rec.text = t; }));
  return "blob:codex-captured-drc";
};
const clickOrig = HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click = function() {};
if (buttons[1]) buttons[1].dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
await new Promise(r => setTimeout(r, 800));
await Promise.allSettled(promises);
URL.createObjectURL = urlOrig;
HTMLAnchorElement.prototype.click = clickOrig;

const text = captured.map(c => c.text || "").join("\n");
const lines = text.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
const counts = { fatal: 0, error: 0, warning: 0, info: 0 };
for (const line of lines) {
  if (line.includes("[\u81f4\u547d\u9519\u8bef]")) counts.fatal++;
  else if (line.includes("[\u9519\u8bef]")) counts.error++;
  else if (line.includes("[\u8b66\u544a]")) counts.warning++;
  else if (line.includes("[\u4fe1\u606f]")) counts.info++;
}
return { panelText: panel ? clean(panel.innerText || panel.textContent || "") : null, counts, lines };
```

Avoid matching Chinese button text directly inside PowerShell-injected scripts; encoding can make `"导出"` comparisons fail. Prefer stable IDs such as `#schDrcPrimaryLog`, button order, ASCII attributes, or Unicode escapes.

### Successful Repair Tactics

- For intentional NC pins, do not connect a short wire with an `NC_*` net to a pin that has a no-connect marker. JLCEDA can report "wire cannot connect to no-connect pin" or later produce single-net warnings. Delete the NC stub wire and write the component pin's no-connect state:

```javascript
const pins = await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(component.primitiveId);
const pin = pins.find(p => String(p.pinNumber) === "A8");
pin.setState_NoConnected(true);
await pin.done();
```

- `sch_PrimitivePin.modify(id, ...)` does not write `noConnected`; its wrapper only handles geometry/name/type fields. Use the component pin object returned by `getAllPinsByPrimitiveId()`.
- `sch_PrimitiveComponent.createShortCircuitFlag()` creates a `short_symbol`; it is not the no-connect marker needed by schematic DRC.
- For unused output pins that were represented by one-pin netports/wires, delete the orphan netport and wire, then mark the source output pin NC. This cleared charger status pins and RHS AUXOUT pins cleanly.
- Floating netports with no wire create info messages. A DRC item like `$4I270` maps directly to primitive id `e270` on page 4; inspect it with `eda.sch_Primitive.getPrimitiveByPrimitiveId("e270")`, then connect or delete it.
- Placeholder parts excluded from BOM/PCB can still fail DRC if they have no footprint or if symbol pins do not map to footprint pads. Assign a real same-pin-count footprint via `otherProperty.Footprint`, keep `addIntoBom: false` and `addIntoPcb: false`, and leave a clear description such as "DNI placeholder; replace before PCB layout". Passing a direct `footprint` property to `sch_PrimitiveComponent.modify()` can be ignored; `otherProperty.Footprint` is the reliable route.
- Descriptive designators with underscores trigger DRC info. Rename to standard references such as `R13`, `C22`, `J4`, and preserve the old role in `Original Designator` and `Function Tag`.
- Supplier standardization warnings are metadata, not electrical connectivity. The public API may auto-restore valid LCSC `Supplier Part` values even after attempts to clear them. If fatal/error counts are zero and the only warning is "component properties do not match supplier number", record it and run JLCEDA's device standardization manually before assembly ordering.

### Export Outputs

Use the live bridge request endpoint for JSON export:

```powershell
$body = @{ scope='all'; timeoutMs=120000 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:38425/api/jlceda/request-export' -ContentType 'application/json' -Body $body
```

The exported BOM may be UTF-16LE/base64 and the full JSON can contain large strings/control characters. PowerShell `ConvertFrom-Json` can fail or garble text. Prefer Node.js or Python to parse the JSON and decode file records.

For schematic PDF export, use:

```javascript
const file = await eda.sch_ManufactureData.getExportDocumentFile("schematic.pdf", "PDF");
const buf = new Uint8Array(await file.arrayBuffer());
```

Then write the bytes locally and validate that the output starts with `%PDF` and ends with `%%EOF`; if `pypdf` is available, verify the page count.

## Working With CAM Output

Treat Gerber/DRL/FlyingProbe export folders as manufacturing evidence. They can reveal board layer count, outline geometry, drill sizes, paste/solder-mask outputs, assembly-side distribution, pad dimensions, and testable nets even when the source `.eprj2` is missing, has empty core design tables, or stores only project structure/history metadata in the parser-visible tables.

Use the bundled CAM parser:

```bash
python scripts/summarize_cam_folder.py "C:\path\to\gerber-export-folder"
```

The script summarizes Gerber files, Excellon drill tools and hole counts, approximate board extents, circular outlines, and `FlyingProbeTesting.json` component/pin/net distributions.

When CAM output conflicts with `.eprj2` extraction, call out the conflict explicitly. For this project family, the quality-test `.eprj2` has empty core `documents/components/devices/attributes` tables but does contain `project_structures` and `history_data`; its CAM export folder remains the usable source for manufacturing geometry, layers, nets, pads, and flying-probe data.

## Output Style

Give actionable PCB feedback. Prefer:

- concrete observations tied to nets, rules, component families, stackup, pad/contact geometry, or layout objects;
- "check this in the editor" steps when the file format does not expose enough geometry;
- explicit separation between extracted project practice and official fabrication constraints;
- short prioritized fixes for board review requests.

Avoid generic PCB advice unless it is connected to this headstage project's constraints.
