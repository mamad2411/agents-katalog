---
name: factorio-blueprints
description: Creates and validates extendible Factorio blueprints from installed game and mod data. Use for Factorio factory planning, blueprint generation, or import debugging.
---

# Factorio Blueprints

Use the installed game as the referee. Model invocation is enabled so a request for a factory production line reaches this workflow.

For planning, inspect recipes and give the next useful production step. For a new or changed blueprint, follow all phases. For an import problem, unpack the string first and reproduce the failure in isolation.

## 1. Establish the build

Infer the requested product and current factory stage from the conversation. Ask only for missing constraints that change the design.

- Specify available technology, inputs, output destination, and starter capacity.
- Choose the optimization objective: early material cost, throughput, footprint, or expansion without moving buildings. Do not claim global optimality without comparing alternatives.
- Treat screenshot dates as evidence. Do not describe an old screenshot as the current factory.

Run `python3 scripts/blueprint.py inspect`. Resolve paths relative to this skill directory. Read the installed mod sources for the recipes, footprints, port positions, and final prototype conversions involved. Read [GAME-DATA.md](GAME-DATA.md) before interpreting mod sources. Use online blueprints as references; verify their assumptions against the installation.

## 2. Design and encode

Read [DESIGN.md](DESIGN.md) before creating or changing a layout.

Create editable JSON for a starter and an expansion. Keep existing inputs and buildings fixed where practical. Include recipes, chest limits, and copper wires. Keep miners and shoreline-dependent pumps separate unless the request includes them.

Use the helper to encode, summarize, and compare:

```bash
python3 scripts/blueprint.py pack starter.json starter.txt
python3 scripts/blueprint.py summary starter.txt
python3 scripts/blueprint.py compare starter.json expanded.json
```

An expansion comparison must account for changed entity settings and wires as well as positions. Read its report, including any changes that require user action.

## 3. Validate in isolation

Read [VALIDATION.md](VALIDATION.md) before starting a simulation. Use `scripts/blueprint.py simulate` with a case manifest. The helper creates an isolated config, write-data directory, mod directory, test save, and validator mod. Never load or save the live factory, replace user settings, or interrupt the running game.

Validate imports, entity placement, recipes, pipe connections, power coverage, belt lanes, and collected output. Use no inserter-capacity research by default. Test output after warmup, with bounded ticks and measured acceptance criteria. A compressed-string round trip alone is not a game test.

If the matching game cannot run, finish static checks and identify exactly what remains untested. Never label a design game-tested on that basis.

## 4. Deliver

- Save the JSON, standalone strings, optional blueprint book, and validation report in a persistent artifact directory outside the game and skill directories.
- Generate a tile placement diagram from the final JSON. Label inputs, outputs, power connection, orientation, and expansion anchor. State whether the picture is a schematic or game render.
- Explain expansion concretely: keep the same rotation, align the named anchor, check existing machines overlap, then build new ghosts.
- Copy only the requested standalone blueprint or book. On macOS, use `python3 scripts/blueprint.py copy artifact.txt`; it verifies the clipboard readback.
- Report tested game/mod versions, nominal and measured output where relevant, and material limits. Keep a backup file link available after the clipboard changes.

## Completion

The delivered string must match the final JSON and diagram. Check that the expansion preserves the stated existing buildings and ports. Passing simulation evidence must cover every delivered variant. Leave unrelated files and the live factory untouched.

`scripts/render.py input.json footprints.json output.png` renders the greenhouse example using Pillow. Supply verified footprint sizes. Adapt its product-specific labels for other production lines.

For a worked example, inspect [examples/greenhouses.py](examples/greenhouses.py). It generates two and four greenhouse variants plus their simulation manifest. Recheck its recipe assumptions before reuse with another mod version.
