---
name: nixcf-secrets-agenix
description: Safely audit or change Agenix-managed credentials and their runtime wiring in the nixcf repository. Use for secrets/default.nix declarations, secrets/secrets.nix recipient mappings, encrypted .age payload metadata, Xray settings, user password secrets, or the cross-layer Attic client/server/netrc credential path, including recipient changes, rotation planning, plaintext-to-Agenix migration, and credential leak remediation.
---

# nixcf Agenix Secrets

Follow this low-freedom workflow. Protect credential material even when the user asks for a quick fix.

## Enforce the safety boundary

- Never decrypt, print, copy, summarize, diff, grep, checksum, encode, or otherwise inspect secret plaintext.
- Never read `.age`, `*.env`, netrc, token-bearing TOML, private keys, password hashes, or editor swap/backup files. Treat a suspicious tracked file as secret until proven otherwise.
- Never run `agenix -e`, `agenix -r`, `age`, `rage`, `strings`, `cat`, `head`, `tail`, `sed`, `xxd`, or similar commands against a payload. Do not open it with a general file-reading tool.
- Never place plaintext or a plaintext-bearing file in a Nix expression, interpolated command, derivation, `environment.etc.*.text`, Home Manager `*.text`, or `source = ./...`; these can copy it into `/nix/store`.
- Never expose credentials in patches, logs, commentary, final answers, documentation, commit messages, process arguments, or shell history.
- Treat every path marked credential-bearing in the reference as opaque while the source-safety gate fails. Do not open them with `cat`, `sed`, an editor, a generic file-reading tool, or a content-producing search.
- Use only `scripts/check-nix-source-safety.sh` for automated inspection of known plaintext-source blockers. It performs fixed no-output marker checks; never modify or replace it with a command that prints matches.
- Do not deploy, restart services, update inputs, commit, rekey, rotate, revoke, or rewrite Git history without separate explicit authorization for that action.
- Preserve current recipients, credential values, runtime paths, ownership, modes, and consumers unless the approved task requires a specific change.

If a requested step crosses this boundary, stop that step. Explain the safe user-operated action without asking the user to paste the value back.

## Read only the required context

1. Read root `README.md` and `flake.nix`.
2. Read the `readme.md` files for `secrets/` and every affected `host/`, `home/`, `os/`, or `fool/` directory.
3. Run `.agents/skills/nixcf-secrets-agenix/scripts/check-nix-source-safety.sh` before opening a potential credential source or running any command that evaluates, builds, checks, locks, activates, or deploys this flake. A nonzero result is a hard stop for those operations, not permission to inspect the flagged file.
4. Read only non-secret source needed to trace declarations and consumers. While the gate is blocked, use filename/status metadata and safe non-secret sources; do not scan or open flagged sources broadly.
5. Read [references/repo-map-and-checks.md](references/repo-map-and-checks.md) before tracing Attic, Xray, password, recipient, migration, or validation work.
6. Treat documentation as navigation; verify current hosts, imports, inputs, and enabled state only through sources that the gate permits.

## Classify the request before editing

Choose exactly one primary class and state it to the user:

1. **Audit only**: report names, paths, ownership, modes, recipients as identities, and consumer relationships; do not mutate files.
2. **Declaration/runtime wiring**: add or change an `age.secrets` declaration, consumer reference, runtime path, owner, group, or mode without changing credential material.
3. **Recipient change**: change public-key mapping in `secrets/secrets.nix`; this also requires user-operated rekeying of every affected encrypted payload.
4. **Credential rotation**: replace credential material and coordinate consumers, cutover, verification, and revocation. Structural edits alone are not a rotation.
5. **Git-history remediation**: remove exposed material from current files, rotate/revoke it, assess Nix-store and log exposure, and separately plan a coordinated history rewrite. Deleting a file from the current tree does not remediate history.

Do not silently expand one class into another. A task may use multiple classes only after each material action is explicitly authorized.

## Resolve decision gates

Before a material change, establish all applicable facts:

- exact logical secret and affected hosts, services, users, and Home Manager profiles;
- intended runtime consumer, path, owner, group, and least-privilege mode;
- exact recipient identities to add or remove and whether access loss is intentional;
- whether credential material stays unchanged, is rotated, or was already rotated outside the agent;
- cutover order, rollback credential, revocation timing, and acceptable service or login interruption;
- whether any action targets a live machine, production service, remote cache, Git history, or Nix-store exposure.

Ask the smallest interactive question that resolves a material ambiguity. Do not guess recipient scope, rotate a shared credential, change login access, revoke an old credential, or touch production based on an inference. Continue independently when the answer is evident from current source and the action remains structural and local.

## Trace the complete credential chain

Build a compact mapping before editing:

`logical secret -> encrypted payload -> recipient set -> age declaration -> runtime path/metadata -> consumer -> enabled host/profile`

For Attic, additionally trace:

`client token/config -> Home Manager service -> cache endpoint -> Nix substituter/netrc -> server environmentFile -> atticd service -> Pi host`

Record paths and identifiers only. Never quote values. Treat duplicate or legacy-looking Attic environment files as unresolved until source proves which one is active; do not delete either by assumption.

## Implement structural changes

1. Keep declarations in `secrets/default.nix` and recipient mappings in `secrets/secrets.nix` unless current source establishes a different project convention.
2. Reference runtime files through `config.age.secrets.<name>.path`; do not interpolate secret content.
3. Give each consumer the minimum required owner/group/mode. Check that its service user can read the file and unrelated users cannot.
4. Keep runtime plaintext outside `/nix/store`. Prefer an Agenix-managed runtime path over tracked environment files, Nix strings, or Home Manager-generated token files.
5. Update every affected consumer and the nearest `readme.md` when behavior or ownership changes.
6. Preserve host/profile boundaries and Pi's `aarch64-linux` constraints.
7. Never edit an encrypted payload with `apply_patch` or a normal text tool.
8. Never patch a flagged plaintext-bearing source using surrounding credential content. Have the user remove or replace the sensitive span in a trusted editor, or use a separately reviewed migration mechanism that cannot emit the old value.

For new or rotated material, finish structural wiring first. Then instruct the user to create/edit/rekey the payload locally with Agenix in a trusted interactive session, verify the intended recipients there, close the editor, and report only completion or failure. Never request the plaintext.

## Validate without exposing content

Use only the name/metadata and evaluation checks in the reference. At minimum:

1. Run the source-safety gate. If it is blocked, report its path/category-only output and do not run any repo-consuming Nix command.
2. Confirm the changed-file set contains only intended paths; use `git status --short` and `git diff --name-status`, never a content diff for secret-bearing files.
3. Confirm every declared payload name has a recipient mapping and every consumer uses the intended runtime path.
4. Confirm runtime path, owner, group, and mode are appropriate and no plaintext-bearing source is copied into `/nix/store`.
5. Run `git diff --check -- <explicit non-secret changed paths>` after reviewing the name-only change list. Never run a content check over `.age`, environment, netrc, token-bearing TOML, or other secret-bearing files.
6. For Nix changes, run `just chk` only after the gate succeeds. If the gate or check cannot complete, report the exact unvalidated item and reason.
7. Do not run `just pi`, `just xps`, or `just gtr7` unless the user separately requests deployment and the gate succeeds immediately beforehand.

## Report safely

Report the request class, source-safety gate state, affected logical names and layers, structural files changed, validation results, remaining user-operated Agenix step, and any unperformed deployment/restart/revocation/history action. Refer to credentials only by logical name. Never include values, hashes, ciphertext excerpts, recipient key bodies, or sensitive command output.
