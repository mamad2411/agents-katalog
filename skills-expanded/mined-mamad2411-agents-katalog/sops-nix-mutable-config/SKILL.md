---
name: sops-nix-mutable-config
description: Diagnose and fix app configs that stop updating because sops-nix templates own the live path (Zed settings, editor/CLI JSON under ~/.config). Use when settings edits don't stick after SOPS rendering, live files point at /run/secrets/rendered, or the user wants placeholders restored to validate mutability on nix-darwin/home-manager.
---

# sops-nix mutable app config

When sops-nix `sops.templates` writes **directly** to an app's live config path, the editor no longer owns that file. UI edits and git-tracked "source of truth" files stop sticking.

This is distinct from decrypting `*.sops.yaml` for one-off secret use (see hub/import `sops-secret-access` for shadcn/`components.sops.json`). Here the problem is **path ownership / mutability**.

## When to use

- "Zed / app no longer updates when I edit settings.json"
- Live config is under `~/.config/…` but changes vanish or never reload
- Recent work added `sops.templates`, placeholder substitution, or unison ignores for a settings file
- User asks to **undo SOPS rendering** and put **placeholders** back so they can validate

## Diagnose first

```bash
ls -la ~/.config/<app>/settings.json
readlink ~/.config/<app>/settings.json || true
ls -la <repo>/files/config/<app>/settings.json
readlink <repo>/files/config/<app>/settings.json || true
git -C <repo> ls-files -s path/to/settings.json   # 120000 = symlink
rg -n 'sops\.templates|placeholder\.|Path .*/settings' <repo>/modules
```

**Red flags**

- Live path → `/run/secrets/rendered/…` or `/private/var/run/secrets.d/…`
- Repo "SoT" is itself a symlink (`git` mode `120000`) into `/run/secrets`
- Nix: `sops.templates."<name>" = { path = "${home}/.config/…"; … }`
- Sync tool ignores that path so the secret-filled render never returns to git

Do **not** print secret values. Report placeholder names, token *kind*, or length only.

## Temporary undo (validation)

Cooper's preferred first step when debugging mutability — not a permanent secrets redesign:

1. **Backup** rendered content to a gitignored path (e.g. `~/.config/<app>/settings.json.sops-rendered.bak`).
2. **Placeholders** in the mutable source (`__ZED_GITHUB_TOKEN__` style), matching `*.example` if present.
3. If the repo path is a symlink into `/run/secrets`, **unlink and write a real file**. Editing through the symlink only mutates the rendered blob.
4. Point live config at the real file: `ln -sfn <repo>/…/settings.json ~/.config/…/settings.json`.
5. **Disable** the `sops.templates` entry (and any unison/rsync `-ignore` for that path) so the next rebuild does not re-hijack.
6. **Do not rebuild** unless asked. Warn that the *current* generation can still re-link on later activation until rebuild.

## Re-enable design notes

If secrets must stay out of git later:

- Prefer a **sidecar** render path the app can merge/include — not the primary watched settings file.
- Or inject tokens outside settings (env, MCP host secret store).
- Never leave the git path as a symlink into `/run/secrets`.
- Never commit rendered secret bodies.

## Pitfalls

- Assuming `cat`/edit of the repo path is enough when it is a secrets symlink.
- Leaving real PATs in the git-tracked file after "undo" — use placeholders while validating.
- Rebuilding immediately when the user only wanted a mutable file to test reload.
- Pasting decrypted tokens into chat during diagnosis.
- Forgetting paired sync ignores (`unison -ignore Path zed/settings.json`) that were added with the template.

## References

- `references/darwin-zed-settings.md` — ~/darwin Zed case (template, unison, live symlink chain)
