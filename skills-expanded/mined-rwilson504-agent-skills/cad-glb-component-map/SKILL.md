---
name: cad-glb-component-map
description: 'Export named, colour-tagged GLB component maps from build123d so a human and an AI can name parts of a model out loud ("make the blue plates thicker") and inspect them in a glTF viewer. USE FOR: colour in STL, does STL support colour, name parts in a viewer, GLB hierarchy, glTF node names, component map, assembly view, interference check, view model in VS Code, shared vocabulary for design review.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","glb","gltf","assembly","visualization"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD GLB Component Maps

> **Prerequisite:** Load `cad-build123d-general` (for `EXPORT_MODE` and the
> `ORIENTATION` map). Sibling of `cad-feature-inventory` (text) and
> `cad-layout-map-2d` (2D diagram) — this is the interactive 3D one.

## Purpose

Directional language fails during design review. "The +X face", "the
front wall", "the plate on the right" are all easy to misread, and a
misread costs a whole rebuild cycle. A **colour-tagged, named GLB** fixes
this: the user opens one file, sees `plates` highlighted in blue, and
says *"make the blue plates thicker."* No axis arithmetic, no ambiguity.

This skill covers producing that file from build123d, making the names
actually appear in a viewer, and rendering it to PNG for chat.

## Which formats carry colour

**STL cannot.** ASCII STL has no colour field. Binary STL has a 2-byte
"attribute byte count" that Materialise/VisCAM hijacked for 15-bit RGB,
but it is non-standard, ignored by every slicer, and cannot name
anything. Never build a review workflow on STL colour.

| Format | Colour | Names | Use for |
|--------|--------|-------|---------|
| **GLB / glTF** | ✅ per-component materials | ✅ node names | **design review** — this skill |
| **3MF** | ✅ | partial | slicer handoff, static renders (`cad-render-images` §4) |
| **STEP** | ✅ AP242 | ✅ | CAD interchange |
| **STL** | ❌ | ❌ | printing only |

Viewer: the **glTF/GLB Viewer** VS Code extension shows the outline tree,
so named nodes are immediately usable.

## The component-split pattern

Build each named component as its own function, then produce **two**
outputs from one source of truth: a fused printable STL, and a coloured
multi-body GLB.

```python
COMPONENT_COLOURS = {
    "boss":    (0.78, 0.78, 0.80),   # grey
    "rails":   (0.30, 0.70, 0.40),   # green
    "plates":  (0.25, 0.50, 0.90),   # blue
    "gussets": (0.95, 0.65, 0.20),   # orange
    "threads": (0.85, 0.25, 0.35),   # red
}

def _boss():
    with BuildPart() as p:
        Box(...)
    return p.part

# printable: fuse everything, then cut
with BuildPart() as body:
    add(_boss()); add(_rails()); add(_plates())
    ...            # bores, slots, etc.
part = body.part
export_stl(part, "part.stl")

# reviewable: same components, trimmed the SAME way, kept separate
coloured = []
for name, solid in components.items():
    solid = solid - bore - open_slot          # mirror every cut
    if solid.volume <= 0:
        raise RuntimeError(f"component {name!r} vanished when trimmed")
    solid.color = Color(*COMPONENT_COLOURS[name])
    solid.label = name
    coloured.append(solid)
export_gltf(Compound(children=coloured), "components.glb", binary=True,
            linear_deflection=0.05, angular_deflection=0.2)
```

**Apply every cut to the components too.** If the GLB shows un-bored
solids it is lying about what prints, which defeats the purpose. Assert
each component survives trimming — a silently vanished component looks
identical to one you forgot to add.

**Pick distinct colours.** The labelling step below identifies components
*by colour*, so two components sharing an RGB collapse into one name.

## Node names: build123d does not export them

`export_gltf()` sets OCAF names via `TDataStd_Name`, but never calls the
writer's `SetNodeNameFormat`, so OCCT falls back to entry paths and every
node comes out as `=>[0:1:1:2]`.

**Diagnostic:** dump the JSON chunk and look at `nodes[*].name`.

```python
import json, struct
raw = open("components.glb", "rb").read()
n = struct.unpack("<I", raw[12:16])[0]
doc = json.loads(raw[20:20 + n])
print([x.get("name") for x in doc["nodes"]])
```

**Why colours work but names don't:** the exporter applies colour to a
node *and* its sub-solids as a fallback, but applies the name only to the
node itself — which comes back null for these shapes. Seeing colour
survive is not evidence that naming will.

**Fix:** patch the JSON chunk after export. Simpler and far less fragile
than reimplementing the exporter. Identify components by **material
colour**, not by export order, so adding or reordering components cannot
silently mislabel anything.

```python
def label_glb(path, colour_by_name, root_name="assembly", tol=0.02):
    path = Path(path)
    data = path.read_bytes()
    magic, version, _ = struct.unpack("<III", data[:12])

    off, chunks = 12, []
    while off < len(data):
        clen, ctype = struct.unpack("<II", data[off:off + 8])
        chunks.append([ctype, data[off + 8:off + 8 + clen]])
        off += 8 + clen

    doc = json.loads(chunks[0][1].decode("utf-8"))
    nodes, meshes = doc.get("nodes", []), doc.get("meshes", [])

    mat_name = {}
    for i, mat in enumerate(doc.get("materials", [])):
        rgba = mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [])
        for name, rgb in colour_by_name.items():
            if len(rgba) >= 3 and all(abs(a - b) <= tol
                                      for a, b in zip(rgba[:3], rgb)):
                mat_name[i] = name
                mat["name"] = name
                break

    def materials_under(idx):
        found, node = set(), nodes[idx]
        if "mesh" in node:
            for prim in meshes[node["mesh"]].get("primitives", []):
                if prim.get("material") is not None:
                    found.add(prim["material"])
        for child in node.get("children", []):
            found |= materials_under(child)
        return found

    def rename(idx, base, seen):
        node = nodes[idx]
        if "mesh" in node:                 # number only mesh-bearing nodes
            seen[0] += 1
            node["name"] = f"{base}.{seen[0]}"
        else:
            node["name"] = base            # OCCT assembly wrapper
        for child in node.get("children", []):
            rename(child, base, seen)

    root = doc["scenes"][doc.get("scene", 0)]["nodes"][0]
    nodes[root]["name"] = root_name
    for child in nodes[root].get("children", []):
        found = {mat_name[m] for m in materials_under(child) if m in mat_name}
        rename(child, found.pop() if len(found) == 1 else "group", [0])

    for mesh in meshes:
        found = {mat_name[p["material"]] for p in mesh.get("primitives", [])
                 if p.get("material") in mat_name}
        if len(found) == 1:
            mesh["name"] = found.pop()

    blob = json.dumps(doc, separators=(",", ":")).encode("utf-8")
    blob += b" " * ((4 - len(blob) % 4) % 4)      # chunks must stay 4-aligned
    chunks[0][1] = blob
    body = b"".join(struct.pack("<II", len(c), t) + bytes(c) for t, c in chunks)
    path.write_bytes(struct.pack("<III", magic, version, 12 + len(body)) + body)
    return path
```

The scene graph OCCT produces is already correctly structured — one
subtree per component under a single root. It only lacks names.

Result in the viewer outline:

```
traveler
  boss     → boss.1
  rails    → rails.1, rails.2
  plates   → plates.1, plates.2
```

## Rendering a GLB to PNG

Two traps, both of which produce a **blank image** rather than an error.

### glTF is metres and Y-up; build123d is millimetres and Z-up

A camera placed at model scale sits kilometres away from the imported
geometry. Convert directions and scale to the *imported* bounds:

```python
def to_gltf(v):
    x, y, z = v
    return (x, z, -y)          # Z-up mm -> Y-up m

b = pl.renderer.bounds
centre = ((b.x_min + b.x_max) / 2, (b.y_min + b.y_max) / 2,
          (b.z_min + b.z_max) / 2)
radius = max(b.x_max - b.x_min, b.y_max - b.y_min, b.z_max - b.z_min)
d = to_gltf(direction)
norm = sum(c * c for c in d) ** 0.5
pos = tuple(centre[k] + d[k] / norm * radius * 2.4 for k in range(3))
pl.camera_position = [pos, centre, to_gltf(up)]
```

### `pyvista.import_gltf` only populates the active renderer once

In a `Plotter(shape=(2,2))` the first subplot renders and the rest come
out blank. Use **one `Plotter` per view** and tile the screenshots:

```python
tiles = [shot(d, u, n) for n, d, u in VIEWS]     # each makes its own Plotter
grid = np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])])
plt.imsave(out, grid)
```

Keep the render script **generic**: read component names back out of the
GLB's material list rather than importing the model module, so one script
serves every labelled export.

## Assembly views and interference checks

Combining parts into one GLB is how you catch fit problems early. Do the
check numerically as well — a render can look perfectly fine while two
solids occupy the same space.

```python
overlap = carrier.part.intersect(blade)
if (overlap.volume if overlap is not None else 0.0) > 1e-6:
    raise RuntimeError("parts interfere; this would not assemble")
```

Print the derived fit numbers next to it — engagement depth, clearance
per side, how far a part protrudes past its support. Those numbers
routinely expose design problems that no dimension list would (e.g. a
blade gripped over 6 mm but protruding 6.6 mm is a lever arm aimed
straight at the failure site).

## Quick reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| Everything one colour in the viewer | Exported STL | Export GLB; STL has no colour |
| Nodes named `=>[0:1:1:2]` | build123d never sets the glTF node-name format | Post-process with `label_glb()` |
| Two components share a name | Duplicate RGB in the colour map | Give every component a distinct colour |
| A component missing from the GLB | Trimmed to zero volume | Assert `solid.volume > 0` after each cut |
| Blank render | glTF metres/Y-up vs model mm/Z-up | Convert axes, scale camera to imported bounds |
| Only the first subplot renders | `import_gltf` populates one renderer | One `Plotter` per view, tile after |
| GLB won't open after patching | JSON chunk not 4-byte aligned | Pad with spaces; update header length |
| Colours right but names wrong | Assumed colour success implies name success | They use different code paths — verify names separately |

## See Also

- `cad-render-images` §4 — colour via **3MF** for static publication
  renders. This skill is for **interactive review**; that one is for
  finished imagery.
- `cad-feature-inventory` — the text equivalent of this vocabulary.
- `cad-layout-map-2d` — the 2D equivalent.
- `cad-build123d-tools` — other viewers (OCP CAD Viewer, YACV).
