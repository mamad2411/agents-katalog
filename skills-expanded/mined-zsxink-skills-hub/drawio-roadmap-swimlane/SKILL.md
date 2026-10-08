---
name: drawio-roadmap-swimlane
description: Generate a "swimlane flow" learning roadmap as a draw.io (.drawio) file — horizontal stage lanes stacked top-to-bottom, each a colored rounded band holding titled unit cards, connected by directional arrows showing strict learning order. Color advances stage by stage. Use when the user wants a roadmap / 学习路线图 / 知识地图 as a drawio where sequence matters and each unit has a title + subtitle. For poster-like parallel skill overviews prefer drawio-roadmap-snake.
---

# Swimlane-flow roadmap

Produce a `.drawio` file with horizontal stage lanes stacked top→bottom: each lane is a colored rounded band of titled unit cards, wired by directional arrows that make learning order explicit. Best when sequence and prerequisites matter.

## When to use

- **This skill (swimlane)** — strict order / prerequisites; each unit has title+subtitle; arrows show "learn A before B". Cleaner for courses.
- **drawio-roadmap-snake** — poster visual impact; many parallel items per category.

If unsure, ask which they want, or offer to produce both.

## Design rules

1. **Stage lanes** — one rounded rect per stage (`rounded=1;strokeWidth=2`), full width, stacked top→bottom. A colored lane-header chip on the left holds the stage name + unit count.
2. **Stage color gradient** — advance top→bottom. Suggested (fill / stroke):
   - Blue `#E3F2FD`/`#1565C0` → Green `#E8F5E9`/`#2E7D32` → Orange `#FFF3E0`/`#E65100`
   - Purple `#F3E5F5`/`#6A1B9A` → Cyan `#E0F7FA`/`#00838F` → Pink `#FCE4EC`/`#AD1457`
   - Side-branch (加餐): dashed yellow `#FFFDE7`/`#F9A825`
3. **Unit cards** — white rounded rect `rounded=1`, value `title&#10;subtitle`. Core/highlight units get `fontStyle=1` (bold) + ⭐ in the title.
4. **Directional arrows** — use `shape=flexArrow;endArrow=classic` (thick filled arrow shape, not a thin line). Route from the bottom center of the last card in a lane, down to the midpoint between lanes, then horizontally left to the entry point of the next lane. Each arrow's `fillColor` uses a light tint of the source lane color; `strokeColor=#6c8ebf`. Set `exitX=0.5;exitY=1` on the source card and `entryX=0.25;entryY=0` on the target lane. Provide explicit waypoints in `<Array as="points">`.
5. **Title + legend** — big bold title on top; one-line legend explaining solid vs. dashed and ⭐ marks.

## Color palette

| Stage role | Lane fill | Stroke |
|---|---|---|
| Foundation | `#E3F2FD` | `#1565C0` |
| Sub-Agents | `#E8F5E9` | `#2E7D32` |
| Skills | `#FFF3E0` | `#E65100` |
| Core Mechanisms | `#F3E5F5` | `#6A1B9A` |
| Engineering | `#E0F7FA` | `#00838F` |
| Closing | `#FCE4EC` | `#AD1457` |
| Side-branch | `#FFFDE7` dashed | `#F9A825` |

## Build procedure

1. Collect outline: stages (lanes) → ordered units (title, subtitle, core?). If pointed at course dir/spec, derive and confirm lanes + order.
2. Geometry: lane height ≈150, card width 200×70, card gap ≈20, lane start x≈195. Stack lanes with ≈30 vertical gap.
3. Draw lanes (background) → header chips → unit cards → flexArrow arrows (bottom→down→left→top) → optional dashed branches → title + legend.
4. Save to `assets/<name>.drawio`; give open instructions.
5. Run `python3 scripts/validate_drawio.py <file.drawio>`. Read [references/design-spec.md](references/design-spec.md) for exact palette values.

## Checklist

- [ ] One lane per stage, stacked top→bottom, full width
- [ ] Color advances stage by stage (exact hex in design-spec)
- [ ] Arrows form a continuous ordered main line across lanes
- [ ] Each unit card has title + subtitle; core units bold + ⭐
- [ ] Title + legend present
- [ ] Valid `<mxfile>` XML, opens in draw.io without errors
