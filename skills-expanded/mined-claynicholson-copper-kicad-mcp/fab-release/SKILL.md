---
name: fab-release
description: Produce a manufacturing package (Gerbers, Excellon drill, BOM and placement file) for a PCB fab from a KiCad project with Copper, after verification gates pass. Works with any fab through fab profiles — JLCPCB by default, PCBWay, OSH Park, a generic Gerber X2 pack, or a user-defined profile. Use when the user asks to "order", "export gerbers", "make fab files", "release", "send to the fab" or wants a cost estimate for PCB/PCBA.
---

# Releasing a board to a fab with Copper

Which fab the pack is for is **configuration, not an assumption**. `copper_status` (or `project_summary`) shows the
project's active fab profile under `config`; `fab_export(profile='list')` lists every profile with its design rules,
what blocks an order, and a `notes` field saying which numbers were checked against the fab and which were not.
Never quote a fab's limits from memory: read them from the profile.

Built-in profiles: `jlcpcb` (the default), `pcbway`, `oshpark` (bare boards), `generic` (Gerber X2 + Excellon +
KiCad position file + plain BOM, for any other fab). Users add their own as JSON in `$COPPER_HOME/fabs/` or
`<project>/.copper/fabs/`. To use another profile for one export, pass `profile=`; to switch the project, set
`"fab": {"profile": "<name>"}` in `<project>/.copper/config.json` and run `pcb_setup(rules='fab')` so the design
rules follow.

## Gate: do not release a board that fails verification

1. `verify` (ERC + DRC with zone refill + schematic↔PCB parity) → **0 errors, 0 unconnected items**.
2. `parts_source_bom(write=false)` → every assembled part is sourced (for the default setup: an LCSC number with
   JLC stock; with other parts providers: the project's part-number field, or just value + footprint for generic parts).
3. `design_review` → no `high` findings (or the user explicitly accepts each one).
4. Bump the revision: set the title block `rev` and add a dated silkscreen revision text. Make a
   `checkpoint(action="create", label="release vX")`.

## Generate

`fab_export()` writes the order pack to `<project>/copper-out/fab/`. Exact paths are in the tool result:

| Output | Content |
|---|---|
| `gerbers/` + zip | Gerbers for all copper, mask, silk, paste and Edge.Cuts layers and the Excellon drill, plotted with the profile's settings (Protel extensions or `.gbr`, X2 or not, PTH/NPTH split or merged) |
| BOM CSV | the profile's columns; one line per unique part, DNP excluded |
| placement CSV | the profile's own columns with its rotation corrections, or KiCad's standard position file |

With the default `jlcpcb` profile that is `<name>-JLCPCB.zip`, a BOM with `Comment, Designator, Footprint, LCSC Part #`
and a CPL with `Designator, Mid X, Mid Y, Layer, Rotation` (JLC rotation corrections applied), plus Basic/Extended
counts and the estimated Extended-part loading fee.

The tool refuses (`FAB_BLOCKED`) when something the profile lists under `blocks` is wrong. Pass `waive=[...]`
(`erc`, `drc`, `parts`, `outline`, `parity`, `unrouted`, `empty`) only with the user's explicit consent, and state in
your answer what was waived. `assembly=false` makes a bare-board pack.

## Upload checklist (tell the user)

The result's `summary.order_notes` are written for the active profile: relay them. In general:

1. Upload the Gerber zip and check the fab's online viewer: outline, drill holes, silkscreen orientation.
2. FR-4, 1.6 mm, 1 oz copper suits most boards; pick ENIG for fine-pitch QFN/BGA. A 4-layer board needs the fab's
   matching stackup selected.
3. For assembly, upload the BOM and the placement file, confirm every line matched a part, and **check the rotation
   of every polarized part** (diodes, LEDs, ICs, electrolytics, connectors) in the fab's placement preview. Assembly
   houses do not all share KiCad's zero orientation; a profile's rotation table fixes the common cases for that fab,
   but the preview has the final word.
4. Single-side assembly is usually far cheaper than double-sided.

## After ordering

Keep the exact fab folder with the commit/checkpoint. When the boards arrive: check the power rails with a
current-limited supply before plugging in USB, then flash firmware.
