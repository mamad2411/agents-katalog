---
name: install-hermes-vps
description: Guide a user interactively through a secure, native, portable Hermes Agent installation on a fresh Debian VPS. Use when the user wants to install, reinstall, recover, document, or migrate NousResearch Hermes Agent on a VPS; run its Dashboard continuously with systemd; access it through an SSH tunnel; configure a persistent Telegram Gateway; or diagnose the known installer, dependency, ownership, Dashboard, and Gateway failures. Defend the documented architecture with reasons, obtain approval at material decision gates, let the user run VPS commands, and verify each result before continuing.
---

# Install Hermes on a VPS

Guide the user through an opinionated deployment without connecting to the VPS
or taking control of their terminal. Let the user paste commands and return raw
output. Move one verified stage at a time.

## Load the right resources

Read these files before giving installation commands:

- `references/architecture.md` for mandatory defaults, decision arguments, and
  allowed exceptions.
- `references/procedure.md` for the ordered command-and-verification workflow.

Read `references/troubleshooting.md` only when a command fails or its output
matches a documented failure. Read `references/operations.md` when the user
asks about updates, backups, migration, or routine management. Read
`references/telegram-gateway.md` only when the user explicitly asks to configure
or repair Telegram or the Hermes Gateway.

Use the copy-ready files in `assets/` rather than reconstructing them:

- `assets/hermes-dashboard.service`
- `assets/ssh-config.example`

## Operating contract

1. State that the user will make every VPS connection and run every command.
   Never initiate SSH, SCP, a remote shell, or a remote write unless the user
   explicitly changes this boundary.
2. Never request or repeat passwords, private keys, API keys, OAuth tokens, or
   bot tokens. Ask the user to enter secrets directly into the relevant trusted
   prompt or local file.
3. Fetch current official Hermes documentation before installation. Prefer
   Context7 with `/nousresearch/hermes-agent` when available; otherwise consult
   only the official NousResearch repository and Hermes website. Verify the
   installer URL, supported flags, Dashboard flags, and service guidance. Treat
   the bundled commands as a tested baseline, not proof that upstream is
   unchanged.
4. Lead with the result and reason. Explain the current stage in a few sentences,
   then provide exactly one copyable command block. Put no prose, prompt symbols,
   comments, placeholders mistaken for literal values, or expected output in
   that block.
5. Tell the user which terminal runs the block: `VPS (root)`, `VPS (hermes)`, or
   `yerel bilgisayar`. Do not mix terminals in one block.
6. Wait for raw output. Check it against the stage's acceptance criteria before
   proceeding. Never infer success from silence and never claim a check that the
   user has not shown.
7. On failure, stop the main path, identify the first meaningful error, and use
   the narrowest matching recovery. Do not restart the entire installer, update
   lockfiles, force npm, edit TypeScript, or add unrelated packages speculatively.
8. Keep a deployment receipt during the conversation: OS, architecture,
   resources, chosen options, Hermes version, Git commit, paths, service status,
   Dashboard bind address, access method, and deferred work.
9. Preserve user-owned changes. Before a command that could overwrite a file or
   change remote security, show the exact target and obtain explicit approval.
10. Prefer reversible actions. Before deletion, replacement, firewall changes,
    disabling SSH login, or destroying an old VPS, require a backup/rollback path
    and explicit approval.

## Approval gates

Do not ask for approval after every harmless diagnostic. Obtain it at these
material gates:

1. **Architecture:** native Debian install; root performs installation; locked,
   non-sudo `hermes` user runs Hermes; code and data are separated.
2. **Resource policy:** no swap by default for the reproduced 4 GB setup, with an
   explicit OOM warning and an option to add swap later.
3. **Official installation:** run the current official installer from the
   official URL with model setup deferred.
4. **Dashboard exposure:** bind only to `127.0.0.1:9119`; never open public 9119;
   use SSH local forwarding for one computer.
5. **Persistence:** install and enable the Dashboard systemd unit.
6. **Security hardening:** create a key-based admin, change firewall rules, or
   disable root/password SSH only after proving a second working login.
7. **Backups/migration:** choose the external encrypted backup destination and
   retention before enabling automation.
8. **Gateway/Telegram:** enable linger, install a persistent user service, and
   add platform dependencies only after the user explicitly chooses messaging.

At each gate, recommend the documented default first, explain why, name the
tradeoff, and ask for a short yes/no approval. If the user rejects a default,
record the exception and its consequence; do not silently force it.

## Workflow

### 1. Establish scope

Collect only missing facts: VPS provider, IP or hostname, OS/version,
architecture, RAM, disk, CPU, current login user, intended client computer, and
whether the host is clean. Do not collect credentials. If the VPS is reachable,
have the user run the preflight block from `references/procedure.md`.

### 2. Present the architecture gate

Recommend the invariant architecture from `references/architecture.md`. Make
clear that root installation does not mean root runtime. Get approval and record
any deliberate exception.

### 3. Execute verified stages

Follow `references/procedure.md` in order:

1. preflight,
2. Debian update,
3. `hermes` runtime identity,
4. official Hermes install,
5. ownership and version receipt,
6. Dashboard web and embedded-chat TUI asset builds,
7. systemd service,
8. SSH local forward,
9. end-to-end verification, including Dashboard Chat and a local `/help` test,
10. final receipt and deferred-work list.

Do not enter model-provider, Gateway, Telegram, backup automation, or SSH
hardening setup merely because core installation completed. These are separate
decisions unless the user explicitly adds them to scope.

If the user explicitly adds Telegram or Gateway, read
`references/telegram-gateway.md` and execute that workflow only after core
Dashboard acceptance. Prepare linger and the Telegram adapter dependency before
Dashboard Quick Setup so credential creation is not mistaken for a connected
Gateway.

### 4. Apply conditional recovery

If a stage fails, open `references/troubleshooting.md`, match the full signature,
and apply only that branch. After recovery, repeat that stage's acceptance test,
not the entire installation.

### 5. Hand off cleanly

Finish with:

- what is verified and the evidence,
- the deployment receipt,
- the exact everyday access command and URL,
- what remains intentionally deferred,
- the backup/migration boundary,
- a warning that a running Dashboard is not proof that model or Gateway setup is
  complete.
