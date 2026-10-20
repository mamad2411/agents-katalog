---
name: hermes-skill-source-management
description: "Use when backing Hermes skills with external sources."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, synchronization, external-sources, deployment]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Hermes Skill Source Management

## Overview

Use this skill to make a Hermes skill editable somewhere other than its runtime skill directory: a cloud-synchronized folder, Git checkout, network mount, workstation-to-server sync, or another durable external source.

The core invariant is **one live source of truth**. The external source owns the files; Hermes discovers that same directory through a registration symlink. Do not maintain two writable copies and hope they stay equivalent.

This skill covers source topology, durable mounting/synchronization, secret handling, atomic cutover, rollback, and end-to-end verification. It does not teach how to write the content of `SKILL.md`; use `hermes-agent-skill-authoring` for frontmatter and prose conventions.

## When to Use

- The user wants to edit a skill manually from another machine.
- A skill should live in Dropbox, Drive, a Git worktree, NFS, SSHFS, Unison, Mutagen, Syncthing, or another synchronized directory.
- A generated skill needs a transparent editable source while remaining loadable by Hermes.
- A skill registration must move from one backing directory to another without downtime or duplicate sources.
- A mount or sync process must survive reboot before Hermes can depend on it.

Don't use this merely to install a hub skill, publish a skill, or make a one-time copy. A copied file is not a live source unless changes flow back to the runtime path.

## Topology and Invariants

Model the setup as three layers:

```text
external source of truth
        ↓ mount / sync / checkout
local backing directory
        ↓ registration symlink
$HERMES_HOME/skills/<category>/<skill-name>
```

Maintain these invariants:

1. **One writable source.** The registered skill resolves to the external backing directory itself, not to an independently copied mirror.
2. **Narrow exposure.** Mount or synchronize only the subtree needed for skills when the transport permits it.
3. **Durable transport.** A background terminal process is suitable for proving the design, not for the final state. Use the host's service manager or declarative configuration.
4. **Secret separation.** OAuth tokens and remote credentials stay outside Git, the Nix store, skill files, and command output. Restrict credential-file permissions.
5. **Atomic registration.** Prepare and validate the new target before replacing the runtime symlink.
6. **Rollback until proven.** Keep the prior source until loader, hash, and two-way propagation checks pass.
7. **Bidirectional evidence.** A healthy-looking mount is not enough. Verify cloud/remote → Hermes host and Hermes host → cloud/remote separately.

## Procedure

### 1. Resolve the active Hermes scope

Determine the effective `$HERMES_HOME`, active profile, target category, skill name, current registration path, and whether the current skill is bundled, hub-installed, externally owned, pinned, user-owned, or curator-managed.

Do not overwrite a protected skill. If customization is needed, create a distinct personal skill or obtain explicit foreground ownership/adoption first.

Done when the exact runtime registration and ownership boundary are known.

### 2. Choose the source and transport

Select a source based on the user's editing workflow:

| Source | Good for | Main constraint |
|---|---|---|
| Git checkout | Reviewed, versioned edits | Requires commit/push/pull discipline |
| Cloud drive mount | Finder/Explorer editing across devices | OAuth scope and mount durability |
| Syncthing/Unison/Mutagen | Direct machine-to-machine sync | Conflict policy and daemon ownership |
| NFS/SSHFS | Server-hosted shared tree | Network availability and boot ordering |
| Local external directory | Simple manual editing | No cross-machine transport by itself |

Prefer a transport already operated by the user. When a provider’s native sync client is installed or becomes available, detect its authoritative account root and prefer it over adding or retaining a second API mount—provided the target skill is fully hydrated and independent two-way propagation checks pass. A daemon binary or running process is discovery evidence, not sync readiness; keep the known-good source live until the actual skill directory and support files appear and match. If introducing a new credential, explain its scope and transfer it through a secure file channel rather than chat text.

Done when the source directory, local backing path, directionality, conflict policy, and credential boundary are explicit.

### 3. Seed the external source without changing registration

Create the destination directory and copy the complete skill directory, including `SKILL.md` and any `references/`, `templates/`, `scripts/`, or `assets/` files. Preserve bytes where possible.

Compute a digest of the current and seeded `SKILL.md`; they must match before cutover. Do not delete or mutate the old source yet.

Done when the destination contains the complete skill and the source/destination digest matches.

### 4. Make the transport durable

Prove the mount or sync interactively first. Confirm the local backing path is readable and writable by the Hermes runtime identity.

Then replace the proof process with a durable mechanism:

- Linux: system or user service as permitted by FUSE and credential ownership.
- NixOS: declare the service in the system or Home Manager configuration; do not imperatively write into a read-only `/etc`.
- macOS: launchd, a managed sync daemon, or the cloud provider's native client.
- Windows: a Windows service, scheduled startup task, or native sync client.

If unprivileged FUSE is unavailable but a root-managed mount works, map presented ownership to the Hermes user and use the narrowest `allow-other` exposure necessary. Ensure the consumer starts only after the mount is ready when boot-time skill availability matters.

Done when the durable service is enabled, active, the backing directory is an actual mount/sync target, and the skill file is readable and writable as the runtime user.

### 5. Repoint registration atomically

Construct a temporary symlink beside the existing registration, then atomically rename it over the old link. This avoids an interval where the skill path is missing and avoids ambiguous `ln -sfn` behavior around directory symlinks.

Conceptually:

```text
new link:  .<skill>.new -> <validated backing directory>/<skill>
rename:    .<skill>.new -> $HERMES_HOME/skills/<category>/<skill>
```

Read the link and its fully resolved `SKILL.md` afterward. Keep the old source as a rollback copy until all verification is complete.

Done when the registration resolves to the intended external backing directory and no duplicate registration exists.

### 6. Verify behavior, not just configuration

Run all of the following:

1. **Service:** durable service enabled and active, when applicable.
2. **Mount/sync readiness:** local backing directory is the expected live target, not an empty mountpoint directory.
3. **Registration:** runtime symlink resolves to the new backing directory.
4. **Loader:** `skill_view` parses the skill and returns the expected name/description.
5. **Integrity:** local and remote `SKILL.md` hashes match.
6. **Remote → host probe:** create a uniquely named harmless file through the remote API/source and observe it locally within a bounded timeout.
7. **Host → remote probe:** create a uniquely named harmless file locally and observe it through the remote API/source within a bounded timeout.
8. **Cleanup:** delete both probes from both sides and verify no verification artifacts remain.

For rclone-backed mounts, use `scripts/verify-rclone-skill-source.sh`. It performs the service, registration, digest, two-way propagation, and cleanup checks from environment variables.

Describe this honestly as focused ad-hoc integration verification unless a repository's canonical suite was also run.

Done when every check passes with fresh output and all probes are gone.

### 7. Retire the old source and reload

After successful verification, remove or clearly archive the previous writable source so the user cannot accidentally edit the wrong copy. Preserve a rollback only when its name makes clear that it is not live.

Use `/reload-skills` when adding or removing skill registrations. If the current conversation already loaded the skill content, use a fresh session when you need guaranteed prompt-level reload semantics.

Done when there is one obvious editable source, Hermes loads it, and the user knows where to edit it.

## Security and Approval Boundaries

- Treat OAuth responses and rclone token JSON as credentials. Never paste them into chat, logs, Git, Nix expressions, or tool summaries.
- Prefer a secure one-time file transfer for remote authorization. Remove the transfer artifact after storing the token in a mode-restricted config file.
- Do not expose an entire cloud drive when mounting one skills subtree is sufficient.
- Do not replace a user's existing source or delete the rollback until the seeded copy and both propagation directions are verified.
- A cloud mount token may grant broader account access than the mounted subtree. Distinguish API credential scope from mount-path scope when explaining risk.
- Keep runtime skill files non-secret. Skills may describe where credentials live, but must not contain the credentials themselves.

## Provider and Platform References

- Native Dropbox client detection and staged migration from another transport: `references/dropbox-native-client.md`
- Dropbox + rclone + NixOS system service: `references/dropbox-rclone-nixos.md`
- Reusable focused verifier for rclone-backed sources: `scripts/verify-rclone-skill-source.sh`

Load provider detail only when that branch applies.

## Common Pitfalls

1. **Making a copy instead of a live source.** A file in Dropbox and a separate runtime file create two authorities. Register the mounted/synchronized directory itself.
2. **Cutting over before mount readiness.** A service can be `active` before the mount becomes observable. Check the actual mount and target file with a bounded readiness loop.
3. **Testing only one direction.** A remote file appearing locally does not prove local edits upload, and vice versa.
4. **Leaking OAuth tokens through command arguments or output.** Parse and store token material without printing it; avoid process arguments when a protected config file can be written directly.
5. **Putting mutable credentials in declarative stores.** Reference a protected runtime credential file from Nix; do not interpolate token contents into a derivation or unit in the store.
6. **Imperatively editing managed `/etc`.** On declarative systems, add the service to the configuration and activate it from a clean source revision.
7. **Activating unrelated dirty changes.** If the configuration repo contains unrelated edits, commit only the intended file and activate from a clean worktree or exact revision.
8. **Deleting the old source too early.** Keep rollback until loader, hashes, and both propagation probes pass.
9. **Leaving two editable-looking copies.** Retire or unmistakably archive the old path after verification.
10. **Claiming a full test-suite result.** Bidirectional probes are focused integration evidence, not a canonical repository suite.
11. **Ignoring boot ordering.** If Hermes scans skills at startup, order or require the mount service appropriately so a reboot cannot expose a dangling registration.
12. **Assuming reload semantics.** Re-scan registrations with `/reload-skills`; start a new session when already-loaded skill instructions must be refreshed.
13. **Equating daemon discovery with completed sync.** A native cloud client can be installed and running while the target subtree is absent, selectively excluded, or still hydrating. Discover the account root, wait for the complete skill directory, and verify both propagation directions before cutover.

## Verification Checklist

- [ ] Active `$HERMES_HOME`, profile, category, and skill name confirmed
- [ ] Skill ownership/protection boundary respected
- [ ] Exactly one intended writable source of truth
- [ ] External destination seeded with the complete skill directory
- [ ] Original and seeded `SKILL.md` hashes matched before cutover
- [ ] Credentials stored outside Git/store/skill files with restricted permissions
- [ ] Mount/sync mechanism is durable and enabled
- [ ] Backing path is ready, readable, and writable by the Hermes runtime
- [ ] Registration was replaced atomically and resolves to the backing directory
- [ ] `skill_view` loads expected frontmatter and content
- [ ] Local and remote skill hashes match
- [ ] Fresh remote → host probe passed within a bounded timeout
- [ ] Fresh host → remote probe passed within a bounded timeout
- [ ] Verification probes and temporary credential-transfer files removed
- [ ] Prior editable source retired or clearly marked as rollback-only
- [ ] User received the human-facing edit location and reload instruction
