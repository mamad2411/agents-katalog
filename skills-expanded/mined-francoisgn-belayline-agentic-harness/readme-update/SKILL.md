---
name: readme-update
description: Brings the project README up to the Belayline standard and keeps it true (technology badges in the header, product image, Excalidraw architecture diagram, lot progress table, getting started, Contributing section). Use at the end of a lot, after a merge that changes the architecture or the state of a lot, or when the README is missing, empty or out of date.
argument-hint: "[lot or section to update, default: everything]"
---

# Update the README

Target: $ARGUMENTS (default: the whole README). Standard: `.harness/docs/README-STANDARD.md` (otherwise
`${CLAUDE_PLUGIN_ROOT}/docs/README-STANDARD.md`). What the project turned off in `.harness/config.json` › `readme`
is not put back.

1. **Assess**: `python3 .harness/scripts/readme-check.py` lists the gaps. README missing: start from the harness's
   `README.md` template; `CONTRIBUTING.md` missing: same.
2. **Badges**: one per building block actually used, read from the manifests (`Package.swift`, `Cargo.toml`,
   `package.json`, `pyproject.toml`, workflows), not from memory. Version = the one in the manifest. Status badge
   (CI, release) = the workflow's live badge. Remove those that are no longer true.
3. **Architecture diagram**: if the modules, flows or external services changed, edit
   `docs/diagrams/architecture.json`, then `python3 .harness/scripts/diagrams-render.py` and commit `.json`, `.svg`,
   `.excalidraw` together. The diagram shows what is shipped, not the target; 5 to 9 boxes, one verb on each useful
   arrow. A text overflow reported by the render gets fixed (wider box or shorter text).
4. **Progress**: never write the rows by hand. `python3 .harness/scripts/readme-progress.py` (token in `GH_TOKEN`)
   regenerates the block between `<!-- harness:begin progress -->` and `<!-- harness:end progress -->` from GitHub
   now: one row per `type: epic` lot (otherwise per milestone), state read from the issues and their PRs. Exit 2
   (no token, no network, no markers): say so in the report, leave the block as it is; add the markers if they are
   missing. A ⚠ in a row (epic without sub-issue, zero or several `status:` labels) is fixed on the issue, not in
   the README.
5. **Images**: a screenshot goes in only if it shows the current product; alt text that describes what is seen;
   file under `docs/images/`. A screenshot that needs a specific device or machine: an issue, not an invented
   image.
6. **Getting started and Contributing**: replay the commands quoted (or say which ones could not be replayed here);
   the Contributing section points to `CONTRIBUTING.md`.
7. **Verify**: `python3 .harness/scripts/readme-check.py` with no gap, `diagrams-render.py --check` green. The
   changes go into the lot's commit (or a draft docs PR outside a lot).

Report: gaps found, sections modified, what the operator still has to provide (screenshot, licence).
