---
name: sops-nix-ops
description: >-
  Operate SOPS + sops-nix + agenix across Cooper's stack — provision encrypted
  secrets into repos (himitsu → sops encrypt → age recipients), diagnose
  nix-darwin/agenix identity and activation failures, and fix app configs that
  stop updating because sops-nix templates own the live path. Use when creating
  *.sops.json, rebuild leaves /run/agenix missing, LaunchDaemon activate-agenix
  fails, or Zed/settings edits don't stick after SOPS rendering.
version: 1.0.0
metadata:
  hermes:
    tags: [sops, sops-nix, agenix, secrets, nix-darwin, age, himitsu]
    category: devops
    related_skills: [nix-darwin-hermes-deployment, sops-secret-access, hermes-dashboard-ops]
---

# SOPS / sops-nix / agenix ops (umbrella)

One class for **encrypted secrets lifecycle** on Cooper's machines and repos.
Three modes share age/SOPS mechanics; pick the section that matches the task.

| Mode | When |
|---|---|
| **A. Provision** | Create `secrets.sops.json` / `*.sops.yaml`, wire runtime decrypt, AI provider keys |
| **B. nix-darwin activation** | Rebuild OK but `/run/agenix/*` missing, `activate-agenix` nonzero, identity path bugs |
| **C. Mutable app config** | Editor/CLI settings stop sticking because `sops.templates` owns `~/.config/…` |

**Safety (all modes):** never print, paste, commit, or report decrypted secret values. Decryptability checks write to `/dev/null`. Report placeholder names, token *kind*, or length only.

Hub/import **`sops-secret-access`** remains the narrow “decrypt a SOPS file for this task” read path (shadcn `components.sops.json` etc.). This skill owns **provision + host activation + path-ownership**.

---

# Mode A — Provision encrypted secrets into a repo

Creating and wiring ciphertext — the write side.

## Terminal masking: never inline secret substitution

Hermes terminal masks secret-looking content. Inline `KEY=$(himitsu read path)` gets mangled (`syntax error near unexpected token ')'`) or empties the var.

**Two-step pattern:**
1. Plain redirect: `himitsu openrouter/api-key > /tmp/cfg-or-key`
2. Consume from a bun/node script written via `write_file`. Never re-inline the secret into a shell string.
3. Clean up temp key files when done.

## Creating a new SOPS file

- **Input path must match a creation rule.** `sops --encrypt` selects `creation_rules` by matching the *input* path against `path_regex`. A plaintext temp named `secrets-plain.XXX.json` against rule `.*\.sops\.json$` fails: `no matching creation rules found`. Name the temp to match (`/tmp/sops-work/secrets.sops.json`) and pass `--config path/to/.sops.yaml` explicitly.
- **Plaintext never sits in the repo.** Build plaintext in temp → encrypt → write ciphertext to the repo path. Ciphertext is commit-safe.
- **Verify round-trip immediately:** `sops -d file | jq 'keys'` (derived facts only — never values).

## Recipient design (`.sops.yaml`)

Darkmatter standard recipients: AWS KMS dev key + tailscale keyservice age + himitsu age (see `sops.dm.sh/.well-known/.sops.yaml`). **Fleet recipients alone usually can't decrypt on the workstation** — if an agent or dev process must decrypt at runtime, add the local age key as a recipient too.

macOS age key locations:
```text
~/Library/Application Support/sops/age/keys.txt
~/.config/age/keys.txt
~/.config/sops/age/keys.txt
```

## Runtime decrypt in TypeScript (`alchemy-sops`)

`runSopsAge` decrypts age-encrypted SOPS in-process — **no `sops` binary**. Age key auto-discovery: XDG on Linux, Application Support on macOS.

```ts
import * as Effect from "effect/Effect";
import { runSopsAge } from "alchemy-sops";

const text = await Effect.runPromise(
  runSopsAge({ path, binary: "sops", inputType: "json", outputType: "json" }),
);
const secrets = JSON.parse(text);
```

Pitfalls:
- alchemy 2.x / alchemy-sops require **effect 4**. Plain `bun add effect` installs v3 — pin `effect@4.0.0-beta.x`.
- Don't spin up `Alchemy.Stack(...)` just to decrypt — call `runSopsAge` / `SopsFile` with `backend: "sops-age"` directly.
- `@ai-sdk/openrouter` does **not exist** on npm — use `createOpenAI({ baseURL: "https://openrouter.ai/api/v1", ... })` from `@ai-sdk/openai`.

## Verify model ids BEFORE wiring providers

1. Catalog: `GET /v1/models` → exact id, context, modalities.
2. Live ping: 1-token completion per id — `scripts/ping-models.mjs`.

HTTP 200 with empty content at `max_tokens: 5` can be fine (reasoning spend); only error bodies mean broken.

**Detail:** `references/darkmatter-recipe.md` — himitsu paths, standard recipients, worked example, provider table.

---

# Mode B — nix-darwin / agenix activation

Use when rebuild succeeds but secrets are absent, `org.nixos.activate-agenix` exits nonzero, or a generated service needs safe identity/path diagnosis.

## Workflow

1. **Confirm declarations and encryption material**
   - Host imports the Darwin module aggregator containing `secrets.nix`.
   - Encrypted file exists in `secrets/`; recipient policy includes an identity on the host.
   - Missing `/run/agenix/<name>` ≠ missing encrypted file.

2. **Separate build from activation**
   - Build the exact Darwin target as the target user.
   - Apply with interactive sudo.
   - Successful Nix build ≠ launchd/agenix activation.

3. **Diagnose launchd failures**
   ```bash
   launchctl print system/org.nixos.activate-agenix
   launchctl print system/org.nixos.sops-install-secrets
   find /private/var/run/agenix.d -maxdepth 2 -type f -print
   ```
   Inspect generated `activate-agenix-start` for identity paths and first failing op. On macOS, RAM-disk under `/private/var/run/agenix.d` can succeed while decryption fails before `/run/agenix` is published.

4. **Validate identities without exposing secrets**
   ```bash
   age --decrypt -i "$HOME/.config/age/keys.txt" \
     -o /dev/null ~/darwin/secrets/openrouter-api-key.age
   ```

5. **Identity-path pitfalls**
   - Do not put an ECDSA SSH private key in `age.identityPaths` — `age` rejects it.
   - Filename `~/.ssh/id_ed25519` is not proof of Ed25519 type.
   - Keep `age.identityPaths` distinct from `sops.age.sshKeyPaths`.
   - Typo omitting `Library` from Application Support path silently drops a valid identity.

6. **Verify after the fix**
   ```bash
   test -r /run/agenix/openrouter-api-key && echo available || echo missing
   launchctl print system/org.nixos.activate-agenix | grep -E 'state =|last exit code'
   ```
   Also verify the consuming app’s non-secret status (provider config, MCP) without printing secrets.

**Detail:** `references/darwin-agenix-identity-validation.md`.

### Common mistakes (activation)

- Treating `nix build` success as proof secrets published.
- Debugging only `/run/agenix`; also inspect `/private/var/run/agenix.d` + launchd exit.
- Fixing ciphertext/recipients when the issue is an invalid local identity path.
- Copying plaintext secrets machine-to-machine instead of fixing declarative identities.

---

# Mode C — Mutable app config (sops-nix templates hijack live paths)

When `sops.templates` writes **directly** to an app's live config path, the editor no longer owns that file. UI edits and git-tracked “source of truth” stop sticking.

Distinct from Mode A (creating ciphertext) and from hub `sops-secret-access` (one-off decrypt). Here the problem is **path ownership / mutability**.

## Diagnose first

```bash
ls -la ~/.config/<app>/settings.json
readlink ~/.config/<app>/settings.json || true
ls -la <repo>/files/config/<app>/settings.json
readlink <repo>/files/config/<app>/settings.json || true
git -C <repo> ls-files -s path/to/settings.json   # 120000 = symlink
rg -n 'sops\.templates|placeholder\.|Path .*/settings' <repo>/modules
```

**Red flags:** live path → `/run/secrets/rendered/…`; repo SoT is symlink (`120000`) into `/run/secrets`; Nix `sops.templates."…" = { path = "${home}/.config/…"; … }`; sync tool ignores that path.

## Temporary undo (validation)

Cooper's preferred first step when debugging mutability:

1. **Backup** rendered content to a gitignored path.
2. **Placeholders** in the mutable source (`__ZED_GITHUB_TOKEN__` style).
3. If repo path is a secrets symlink, **unlink and write a real file**.
4. Point live config at the real file: `ln -sfn <repo>/…/settings.json ~/.config/…`.
5. **Disable** the `sops.templates` entry (and paired unison/rsync ignores).
6. **Do not rebuild** unless asked — current generation can re-link until rebuild.

## Re-enable design

- Prefer a **sidecar** render path the app merges/includes — not the primary watched settings file.
- Or inject tokens outside settings (env, MCP host secret store).
- Never leave the git path as a symlink into `/run/secrets`.
- Never commit rendered secret bodies.

**Detail:** `references/darwin-zed-settings.md` — ~/darwin Zed case.

---

## Support files

| Path | Topic |
|---|---|
| `references/darkmatter-recipe.md` | Provisioning recipe, recipients, providers |
| `references/darwin-agenix-identity-validation.md` | macOS agenix identity/path failures |
| `references/darwin-zed-settings.md` | Zed settings template/unison/symlink chain |
| `references/absorbed-sops-secrets-provisioning.md` | Pre-merge Mode A body |
| `references/absorbed-nix-darwin-secrets.md` | Pre-merge Mode B body |
| `references/absorbed-sops-nix-mutable-config.md` | Pre-merge Mode C body |
| `scripts/ping-models.mjs` | Live 1-token model id pings |

## Related

- `nix-darwin-hermes-deployment` — Studio Hermes+CuaDriver deploy (uses agenix; defers identity deep-dives here)
- `hermes-dashboard-ops` — sops-rendered dashboard env on NixOS devbox
- `sops-secret-access` (hub) — one-off decrypt for task config
- `financial-operations` — 1P/himitsu for cards (not SOPS files)
