# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo layout

This is a hackathon repo (HRA x HPO, August 2026). Each contributor works in their own top-level folder, mostly independently — there is no root-level build. Look for a `CLAUDE.md` inside the relevant folder for details specific to that work:

- `3d-web-work/` — Andreas's Angular + BabylonJS web app visualizing Human Reference Atlas (HRA) 3D organ models. See `3d-web-work/CLAUDE.md`.
- `hpo-uberon-terms/data/` — source CSV data mapping HPO (Human Phenotype Ontology) terms to HRA digital objects; consumed by `3d-web-work`'s preprocessing script.

When adding a new top-level folder for your own work, add a one-line entry here and create a `CLAUDE.md` inside it describing its own commands/architecture.
