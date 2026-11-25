---
name: update-harness
description: Use when the user asks to update the template or the harness (any language: "update the template", "actualiza el arnés", "mettre à jour le template", "template aktualisieren"). Applies ownership rules, resolves conflicts and updates the manifest/state.
license: MIT
---

# Update the harness

Flow to bring a new template version into a configured project. **It never overwrites `owned` files and never deletes files.**

## When

- The user asks to update the template/harness, or a new tag/commit exists.
- Not mid-change: finish or archive first.
- **Trigger phrases may arrive in any language** — match the intent ("actualiza el arnés", "update the template",
  "mettre à jour", "aktualisieren"), not the exact wording.

## Steps

1. **Check state**: `.atlas/state.json` (`template_source`) and `.atlas/manifest.json`.
2. **Get the new template** in a temp directory (`git clone` + `checkout <tag|commit>`).
3. **Run the script** from the project root:
   `node .atlas/scripts/actualizar-arnes.mjs --template <path>`
   - `owned` → skipped · `generated` → regenerated (adapters with resolved placeholders) ·
     `managed` → replaced if the hash matches, otherwise `<file>.new`.
   - It backs up and **rewrites `manifest.json` and `state.json`** (version, commit, hashes).
4. **Resolve conflicts**: `diff -u <file> <file>.new`, merge by hand and remove the `.new`.
5. **Validate**: `validar-manifiesto`, `validar-contrato`, `validar-perfiles`, `openspec doctor` and
   `openspec context`.
6. **Commit**: `chore(harness): update to <version>` and report updated/conflicts/skipped.

## Rules

- **Do not improvise hashes**: use `sha256.sh`/`sha256.ps1` or the scripts.
- **Do not overwrite `owned`** (AGENTS.md, config, docs, adr, specs).
- If the template removes a file, **report it**; do not delete it.
- Packs are enabled/disabled by hand (`.atlas/packs/README.md`).

Human guide: `docs/harness/es/UPDATE.md` (or `docs/harness/en/UPDATE.md`).
