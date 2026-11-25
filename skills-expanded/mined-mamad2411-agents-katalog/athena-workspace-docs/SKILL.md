---
name: athena-workspace-docs
description: Maintain repo-local documentation and workspace manifests for `C:\\Users\\floris\\Documents\\GitHub\\athena`. Use when Codex needs to thin or restructure the root README, refresh `docs/` workspace navigation, regenerate `crates/`, `apps/`, `benches/`, or `examples/` manifests, or add/update per-crate or per-app READMEs in this repository.
---

# Athena Workspace Docs

## Overview

Keep Athena documentation split across the right surfaces instead of letting the root README grow into the whole repo. Prefer the repo generator for repeated workspace-doc changes and preserve detailed app runbooks where they already exist.

## Workflow

1. Start at `C:\\Users\\floris\\Documents\\GitHub\\athena`.
2. Read [references/doc-surfaces.md](references/doc-surfaces.md).
3. If the change touches workspace navigation, manifests, or package READMEs, update `scripts/generate_workspace_docs.py` first instead of hand-editing generated files.
4. Regenerate docs with:

```powershell
python scripts/generate_workspace_docs.py
```

5. Verify that the generated surfaces are clean:

```powershell
python scripts/generate_workspace_docs.py --check
```

6. If the user adds a new crate, app, example, or bench surface, extend the generator metadata first and then rerun it.
7. If the request also needs Rust validation, use WSL2 for `cargo` commands on this machine.

## Guardrails

- Keep `README.md` thin. Move durable detail into `docs/`, folder `MANIFEST.md` files, or package-level READMEs.
- Treat `crates/MANIFEST.md`, `apps/MANIFEST.md`, `benches/MANIFEST.md`, and `examples/MANIFEST.md` as the whole-workspace maps.
- Do not casually replace detailed manual runbooks in `apps/cloudflare-athena`, `apps/cloudflare-d1-proxy`, `apps/desktop`, or `apps/wss-gateway` with generic generated text.
- When package metadata is stale or template-shaped, document the real folder role in the README instead of blindly mirroring the package name.
- If the user wants product docs content, update `apps/docs/content/docs/`. If they want repo-maintainer docs, update `docs/`.

## Output targets

- Root navigation: `README.md`
- Repo docs hub: `docs/README.md`, `docs/index.md`, `docs/workspace-scale.md`, `docs/workspace-manifest.md`
- Folder maps: `crates/`, `apps/`, `benches/`, `examples/` READMEs and MANIFESTs
- Package docs: generated crate READMEs and selected generated app READMEs
