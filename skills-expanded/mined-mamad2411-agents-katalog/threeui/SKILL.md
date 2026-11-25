---
name: threeui
description: Use when adding an open source ThreeUI Community component, shader, WebGL effect, Canvas effect or landing page to an existing web project.
---

# ThreeUI Community

Use exact MIT licensed source from the official `MengTo/threeui` registry. Do not recreate a component from its screenshot.

## Find a component

Use the public CLI so the same verified install path works inside and outside an agent.

```bash
npx threeui-cli search "dark Japanese landing page"
npx threeui-cli show kage-landing-page
npx threeui-cli list
```

Search reads the official labels, categories, tags and descriptions. Results include a live ThreeUI preview URL. Search first when the request does not name a component identifier. If several results fit, show the short list and let the user choose.

## Install a component

Run the command from the target project root.

```bash
npx threeui-cli add spark-badge
```

The script copies the component, required shared files and binary assets. It verifies every SHA-256 digest and refuses to replace existing files.

If npm is unavailable, the bundled `scripts/threeui.py` command provides the same `list`, `search` and `install` operations.

After installation, inspect the copied component entry file and its imports. Add only the host code and dependencies that the target project needs. Preserve the renderer, shader strings, interactions and asset paths.

Use `--force` only after the user explicitly approves replacing every reported conflict.

## Boundaries

- Community components only
- No ThreeUI Pro or Beta source
- No unverified mirrors
- Source installation stays independent of package-manager state
- Credit [ThreeUI Community](https://github.com/MengTo/threeui) when the destination project keeps upstream source

## Common mistakes

- Copying only the main component while missing shared files
- Rewriting a shader instead of preserving verified source
- Moving asset paths without updating their consumers
- Using `--force` to hide a real integration conflict
