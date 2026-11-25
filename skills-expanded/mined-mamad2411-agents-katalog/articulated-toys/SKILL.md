---
name: articulated-toys
description: Generate print-in-place articulated toys for 3D printing. Creates STL files of segmented creatures (snakes, dragons, caterpillars, fish, robots) with hook-and-axle joints that move freely right off the print bed — no assembly required. Supports wings, legs, and branching body structures. Can also convert existing static 3D models (STL/OBJ/3MF) into articulated print-in-place toys.
---

# Articulated Toys Generator

Generate print-in-place articulated toys for 3D printing. Creates STL files of segmented creatures with hook-and-axle joints that move freely right off the print bed — no assembly required. Now supports **wings** (membrane and feathered), **legs** with ball-socket joints, advanced creature presets, and **conversion of existing 3D models into articulated toys**.

## When to Use

Use this skill when the user wants to:
- Create an articulated / flexi toy for 3D printing
- Generate a print-in-place segmented creature (snake, dragon, griffin, phoenix, bat, pegasus, wolf, etc.)
- Design a custom articulated model with wings, legs, joints, head, tail, and decorations
- Produce STL files of jointed, movable 3D print toys
- Create winged creatures (dragons, griffins, phoenixes, bats) with articulated bodies
- **Convert an existing static 3D model (STL/OBJ/3MF) into an articulated print-in-place toy**
- **Make any 3D model flexible / segmented with ball-socket joints**

## Prerequisites

```bash
sudo pip3 install numpy-stl numpy matplotlib trimesh scipy shapely networkx rtree manifold3d
```

## Quick Start

### 1. Generate from Preset

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/generate_articulated.py \
  --preset winged_dragon --output winged_dragon.stl
```

### 2. List Available Presets

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/generate_articulated.py --list
```

Available presets:

| Preset | Description | Wings | Legs |
|--------|-------------|-------|------|
| `snake` | Classic segmented snake | - | - |
| `dragon` | Spiky dragon (no wings) | - | - |
| `caterpillar` | Round caterpillar | - | - |
| `robot_worm` | Blocky robot worm | - | - |
| `fish` | Scaled fish with fin tail | - | - |
| `lizard` | Long ridged lizard | - | - |
| `centipede` | Multi-segment centipede | - | - |
| `winged_dragon` | Dragon with membrane wings and 4 clawed legs | membrane | 4 |
| `griffin` | Eagle-headed with feathered wings and 4 legs | feathered | 4 |
| `phoenix` | Fire bird with large feathered wings | feathered | 2 |
| `bat` | Small creature with membrane wings | membrane | 2 |
| `pegasus` | Horse-like with feathered wings and hooves | feathered | 4 |
| `winged_wolf` | Wolf with feathered wings and paws | feathered | 4 |

### 3. Customize a Preset

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/generate_articulated.py \
  --preset winged_dragon --segments 15 --body-diameter 20 --wing-span 50 --output big_dragon.stl
```

### 4. Custom Creature from JSON Config

Create a JSON config file (see `templates/custom_creature_config.json`) and run:

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/generate_articulated.py \
  --config /path/to/config.json --output custom_creature.stl
```

JSON config supports `wings` and `legs` sections:

```json
{
  "num_segments": 12,
  "body_diameter": 18,
  "head_type": "dragon",
  "tail_type": "pointed",
  "wings": {
    "type": "membrane",
    "span": 40,
    "chord": 20,
    "attach_segment": 2,
    "num_ribs": 5,
    "taper": 0.35,
    "sweep_angle": 20
  },
  "legs": {
    "count": 4,
    "paw_type": "claws",
    "length_factor": 1.2,
    "front_segment": 3,
    "rear_segment": 8
  }
}
```

### 5. Convert Existing Model to Articulated

Convert any static 3D model (STL, OBJ, 3MF) into an articulated print-in-place toy:

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/articulate_model.py \
  --input model.stl --output model_articulated.stl
```

With custom parameters:

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/articulate_model.py \
  --input model.stl --segments 10 --joint-size 4 --clearance 0.5 --output model_articulated.stl
```

Analyze a model before converting:

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/articulate_model.py \
  --input model.stl --analyze
```

### 6. Generate PNG Preview

```bash
python3 /home/ubuntu/skills/articulated-toys/scripts/preview_articulated.py \
  --input model.stl --output preview.png
```

## Model Conversion Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--input FILE` | Input 3D model (STL/OBJ/3MF) | `--input dragon.stl` |
| `--output FILE` | Output articulated STL | `--output dragon_flex.stl` |
| `--segments N` | Number of segments (auto if not set) | `--segments 8` |
| `--axis x/y/z` | Articulation axis (auto-detected) | `--axis x` |
| `--joint-size N` | Ball joint radius in mm (auto-scaled) | `--joint-size 4` |
| `--clearance N` | Joint clearance in mm (default: 0.4) | `--clearance 0.5` |
| `--socket-thickness N` | Socket wall thickness (default: 1.5) | `--socket-thickness 2` |
| `--method TYPE` | Segmentation: `uniform` or `waist` | `--method waist` |
| `--analyze` | Only analyze model, don't convert | `--analyze` |

The `waist` method detects narrow cross-sections in the model and places joints at natural articulation points. The `uniform` method spaces joints evenly along the principal axis.

## Preset Override Parameters

| Flag | Description | Example |
|------|-------------|---------|
| `--segments N` | Number of body segments | `--segments 12` |
| `--body-diameter N` | Body diameter in mm | `--body-diameter 20` |
| `--body-length N` | Segment length in mm | `--body-length 12` |
| `--clearance N` | Joint clearance in mm | `--clearance 0.5` |
| `--taper N` | Segment taper ratio (0.7-1.0) | `--taper 0.85` |
| `--head TYPE` | Head type | `--head dragon` |
| `--tail TYPE` | Tail type | `--tail fin` |
| `--decoration TYPE` | Surface decoration | `--decoration scales` |
| `--scale N` | Scale entire model | `--scale 1.5` |
| `--wing-type TYPE` | Wing type (membrane/feathered) | `--wing-type feathered` |
| `--wing-span N` | Wing span in mm | `--wing-span 50` |
| `--no-wings` | Remove wings from preset | `--no-wings` |
| `--no-legs` | Remove legs from preset | `--no-legs` |

## Head Types

`snake`, `dragon`, `caterpillar`, `robot`, `fish`, `wolf`, `eagle`, `none`

## Tail Types

`pointed`, `round`, `fin`, `rattle`, `fan`, `none`

## Wing Types

- `membrane` — Bat/dragon style with ribs and thin membrane surface
- `feathered` — Bird/angel style with overlapping feather shapes

## Paw Types

`claws` (3-toed), `hoof`, `paw` (round with toes), `webbed` (aquatic)

## Decoration Types

`spikes`, `ridges`, `plates`, `scales`

## 3D Printing Tips

- **Supports**: OFF (print-in-place)
- **Infill**: 50-100%
- **Layer height**: 0.2mm or finer
- **Raft/Brim**: Recommended
- **Material**: PLA or PETG
- **Post-print**: Gently flex joints to free them
- **Wings**: Print flat on bed, flex gently after printing
- **Legs**: Flex ball-socket joints gently to free them
- **Converted models**: May need `--clearance 0.5` for complex geometry

## References

- See `references/presets_reference.md` for full parameter documentation
- See `templates/custom_creature_config.json` for custom config template

## Workflow

### Creating from Preset
1. Ask user what creature they want (or suggest presets)
2. Run `generate_articulated.py` with appropriate preset/config
3. Run `preview_articulated.py` to generate PNG preview
4. Show preview to user and offer adjustments
5. Deliver final STL file

### Converting Existing Model
1. User provides a 3D model file (STL/OBJ/3MF)
2. Run `articulate_model.py --analyze` to inspect the model
3. Run `articulate_model.py` with appropriate parameters
4. Run `preview_articulated.py` to generate PNG preview
5. Show preview to user and offer adjustments (segments, joint size, axis)
6. Deliver final articulated STL file
