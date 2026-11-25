# AGENTS.md

Ansible-driven personal infrastructure repo for Fedora and Void desktops, Fedora IoT, WSL, a Rocky Linux 9 server, and an Atlas NAS.

## Source Of Truth
- Main orchestration: `ansible/site.yml`
- Inventory and layering inputs: `ansible/inventory/hosts.yml`, `ansible/inventory/group_vars/*.yml`, `ansible/inventory/host_vars/*.yml`
- Dotfiles live under `dotfiles/`
- AI agent instructions (bootstrap, rules, knowledge) are centralized in `dotfiles/common/.config/ai/` and shared between OpenCode, Codex, and Gemini CLI.
- OpenCode loads its entrypoint configuration from `dotfiles/common/.config/opencode/opencode.json`.
- Codex config is rendered from `dotfiles/common/.codex/config.toml.j2` so `model_instructions_file` points to the deployed `~/.config/ai/bootstrap.md`.

## Topology
- Current personal desktop: `ikaros = platform_fedora + role_personal_workstation + graphical_desktop + desktop_gnome`
- Current laptop: `nymph = platform_fedora + graphical_desktop + desktop_gnome`
- Void desktop profile is also the base for other future/reference hosts via `platform_void + graphical_desktop`
- Workstation: `deadalus` is Windows + Fedora WSL.
- Rocky server: `prometheus` belongs to `rocky_server`.
- NAS: `atlas` (Rocky Linux 9, reached through SSH)
- Always-on LAN node: `aegis` (Fedora IoT on Raspberry Pi 4, reached through SSH)
- Hosts intentionally belong to multiple groups; trust `ansible/site.yml` over hostname assumptions.
- Inventory axes are independent: `platform_*`, `role_*`, and `desktop_*`. Legacy `void` and `desktop` remain compatibility parents.

## Working Rules
- Preserve layering `all -> platform -> role -> desktop -> host`.
- Keep `ansible/site.yml` small; orchestration belongs there, implementation belongs in roles.
- Prefer minimal, targeted edits. Preserve idempotency and existing ordering.
- Use Git Flow branch prefixes: `feature/` for new functionality, `bugfix/` for non-urgent fixes,
  `hotfix/` for urgent production fixes, `release/` for release preparation, and `support/` for
  maintained release lines. Do not use abbreviated prefixes such as `feat/`.
- Desktop and WSL hosts use `ansible_connection: local`; remote infrastructure hosts use SSH.
- Treat `secrets/` as sensitive. Never print secret values.
- Tmux plugins are bootstrapped by TPM on the host; the repo only keeps tmux config and custom helper scripts.
- Read the relevant role tasks, templates, vars, and deployed dotfiles before editing.

## Validation
- Default minimum:
  - `ansible-playbook ansible/site.yml --syntax-check`
- Repo-wide checks:
  - `ansible-lint ansible/site.yml`
  - `ansible-lint ansible/roles`
  - `yamllint ansible/`
- Host-focused dry runs:
  - Fedora desktop work: `ansible-playbook ansible/site.yml --limit ikaros --check --diff`
  - Fedora laptop work: `ansible-playbook ansible/site.yml --limit nymph --check --diff`
  - WSL workstation dev: `ansible-playbook ansible/site.yml --limit deadalus --check --diff`
  - Server: `ansible-playbook ansible/site.yml --limit prometheus --check --diff`
  - Rocky server after activation: `ansible-playbook ansible/site.yml --limit <host> --check --diff`
  - Atlas NAS: `ansible-playbook ansible/site.yml --limit atlas --check --diff`
  - Aegis IoT: `ansible-playbook ansible/site.yml --limit aegis --check --diff`
  - Aegis NFS client layer: `ansible-playbook ansible/site.yml --limit aegis --tags nfs --list-tasks`
  - Aegis host DNS: `ansible-playbook ansible/site.yml --limit aegis --tags dns --check --diff`
- Focused checks:
  - Emacs is disabled by default; temporary Emacs check: `ansible-playbook ansible/site.yml --limit <host> --tags emacs --check --diff -e emacs_enabled=true`
  - AI coding agents: `ansible-playbook ansible/site.yml --limit <host> --tags ai_agents --check --diff`
  - Mail bootstrap: `sh -n scripts/bootstrap_mail.sh` and `shellcheck scripts/bootstrap_mail.sh`
  - Server compose render: `podman-compose -f /opt/docker/server/docker-compose.yml config` and `systemctl status podman-compose-server`
  - Atlas media stack:
    `ansible-playbook ansible/site.yml --limit atlas --tags storage,sharing,containers --check --diff`
  - Atlas network/share hardening:
    `ansible-playbook ansible/site.yml --limit atlas --tags hardening,sharing --check --diff`
  - Atlas ZFS snapshot retention and scrub timers:
    `ansible-playbook ansible/site.yml --limit atlas --tags snapshots,scrub --check --diff`
  - Atlas encrypted Borg backup:
    `ansible-playbook ansible/site.yml --limit atlas --tags packages,borg --check --diff`
  - Prometheus/Aegis WireGuard gateway:
    `ansible-playbook ansible/site.yml --limit prometheus,aegis --tags wireguard --check --diff`
  - DuckDNS config only: `ansible-playbook ansible/site.yml --limit prometheus --tags duckdns --check --diff`

## Conventions
- Use FQCN Ansible modules.
- Prefer declarative modules over `command`/`shell`; when `shell` is required, make idempotency and failure behavior explicit.
- Start YAML files with `---`, use 2-space indentation, and keep file modes quoted like `"0644"`.
- Keep booleans as booleans and structured vars as YAML lists/maps.
- Put host-specific overrides in `host_vars`, not shared `group_vars`.
- Use `no_log: true` for secret-bearing task inputs or outputs.

## Desktop Notes
- `desktop_profile` names independently selectable desktop groups such as `desktop_gnome`, `desktop_sway`, and `desktop_niri`. Keep platform-specific session bootstrap in platform-specific roles.
- `desktop_environment` is fixed to `minimal` for Void desktops. `profile_desktop_common` owns shared Void bootstrap; `profile_desktop_sway` and `profile_desktop_niri` manage the enabled sessions, while `profile_desktop_gnome` copies shared desktop dotfiles for Fedora/GNOME without managing GNOME settings. `desktop_sessions_enabled` and `desktop_default_session` apply to the minimal mode.
- Emacs has one authoring-oriented `.emacs.d`, deployed by `dotfiles_common` when `emacs_enabled` is true. Fedora/GNOME desktops and workstation profiles enable it; keep platform dependencies in package group vars rather than branching in Emacs Lisp.
- NTFS filesystem support is provided by `ntfs-3g` in `ansible/inventory/group_vars/void.yml`.
- Void user services are managed by `turnstile` and live under `dotfiles/desktop/.config/service/`.
- `ssh-agent` keeps the stable socket `~/.local/state/ssh-agent/socket`.
- Critical session entrypoints:
  - `dotfiles/desktop/.config/sway/config` plus `host.conf` and `session-env` deployed via `host_sway_dotfiles` (sway / Wayland)
  - `dotfiles/desktop/.config/niri/config.kdl` and `session-env` deployed via `desktop_niri_dotfiles` (Niri / Wayland)
- Void Niri lives in `profile_desktop_niri`, gated on `'niri' in desktop_sessions_enabled`; it installs the `emptty` `niri.desktop` session, the `/usr/local/bin/start-niri` launcher, and the xdg-desktop-portal config, mirroring `profile_desktop_sway`.
- Fedora GNOME (`desktop_gnome`) assumes GNOME comes from the Fedora Workstation base install; Ansible deploys shared desktop dotfiles and git/GPG config for `ikaros` and `nymph`, not GNOME settings.
- Do not switch or restart the display manager during a playbook run from an active graphical session.
- `nymph` is the Fedora/GNOME laptop target; keep GNOME settings unmanaged for now and add host-specific tuning only after real use.

## Void Package And Dotfile Bucket Rules
`platform_void` is the reusable Void platform selection. The legacy `void` group remains a compatibility parent so existing `group_vars/void.yml` and `when: "'void' in group_names"` checks keep working during the transition.
The Void desktop package lists in `ansible/inventory/group_vars/void.yml` are kept disjoint by role:
- `void_packages_base` — system runtime only (init/services, kernel, audio core, networking, filesystem, firewall, hardware daemons, runit logging).
- `desktop_common_packages` — GUI infrastructure shared by the minimal desktop mode.
- `desktop_minimal_packages` — applications, integration components, and the `emptty` display manager.
- `desktop_sway_packages` — binaries specific to the Sway session.
`profile_packages` remains the shared package bucket for Void and Fedora profiles. Rocky uses
`rocky_profile_packages` so RPM-specific names do not leak back into the other platforms; do not move
desktop-specific Void entries through either bucket.
The dotfile vars follow the same split: `desktop_common_dotfiles` carries mode-independent content and `desktop_minimal_dotfiles` carries Thunar, Udiskie, and MIME defaults. `desktop_void_dotfiles` remains reserved for files that need the Void runtime.

## Workstation Notes
- `deadalus` is modeled as Windows + Fedora WSL and is the sole workstation target.
- Fedora WSL belongs to `platform_fedora`, `workstation_dev_fedora`, and the shared WSL layer. It must not receive Flatpak or Snap runtimes.
- Fedora WSL installs Mise from the official `jdxcode/mise` COPR and uses its pinned Temurin Java 11 JDK; update the declared Mise version deliberately.
- Windows applications are installed manually and are not managed from the WSL profile.

## Rocky Server Notes
- DuckDNS is rendered by `profile_server` from host-local `server_duckdns_domain` and
  `vault_duckdns_token`. Keep the rotated token in encrypted Vault or untracked local vars, never in
  dotfiles. The private `~/duckdns/duck.sh` keeps the existing entrypoint; rendering uses `no_log`
  and disables diffs. Provisioning does not execute the updater or change its external schedule.
- `rocky_server` is a child of both `platform_rocky` and `server`; `prometheus` is its active target.
- The target must already provide `server_username` with local sudo access before the profile runs.
- The Rocky profile installs Podman and podman-compose, uses firewalld, preserves SELinux enforcement, and renders the
  existing Nginx Proxy Manager/Gitea Compose stack with a `podman-compose-server` systemd unit. PostgreSQL and
  Navidrome are no longer part of the desired Prometheus configuration. The role does not stop or remove legacy
  containers, delete `/opt/postgres/data`, start the Compose stack, update DNS, or cut over traffic.
- Firewalld enables SSH, Cockpit (`9090/tcp`), HTTP and HTTPS. Nginx Proxy Manager publishes `80/tcp` and
  `443/tcp`; bind its administration interface only to `127.0.0.1:81` and use `npm-tunnel` from Ikaros or Nymph.
  Nextcloud remains disabled; do not provision `/srv/nextcloud` directories.
- `scripts/migrate_prometheus_data.sh` is the separate, source-host-run NPM/Gitea migration path. It dry-runs by
  default and requires explicit source-stack quiescing before copying persistent Docker data with rsync.
- Atlas-only OpenZFS, NFS, Samba, and Syncthing stay selected through Atlas host variables and must not
  leak into `rocky_server`. Cockpit plus its Navigator and Podman extensions are selected explicitly for
  Prometheus through its host variables.

## Atlas NAS Notes
- `atlas` is a remote Rocky Linux 9 NAS. Keep its connection, LAN, pool and mountpoint values in
  `host_vars/atlas.yml`. Bootstrap it once with `-e atlas_connection_username=<existing-admin>`;
  subsequent runs use the dedicated Atlas account.
- The pool is normally pre-existing. A one-time bootstrap may create it only when `atlas_create_pool=true`
  is explicitly supplied and `atlas_zpool_disks` contains exactly four real `/dev/disk/by-id/...` paths.
  Never partition, force, destroy, roll back, or modify the vdev layout of an existing pool.
- `atlas_manage_storage`, `atlas_manage_sharing`, and `atlas_manage_firewall` are enabled in Atlas host vars as
  the declared steady state; set one false only for a deliberate suspension. `atlas_manage_media_stack` remains false
  until the future rootful Immich stack has its required Vault inputs and target validation.
- Atlas requires `vault_atlas_admin_password_hash` for Cockpit and, while sharing is enabled,
  `vault_atlas_samba_password`. The future rootful media stack also requires
  `vault_atlas_immich_db_password`. Never print these values.
- Atlas creates the complete declared hierarchy only under the verified existing or explicitly bootstrapped pool: `archive`,
  `services`, `services/data`, `services/data/navidrome`, `services/data/syncthing`, `media`, `media/music`,
  `media/photobook`, `backup`, `backup/hosts`, and `backup/hosts/prometheus`. `backup` has a `500G`
  reservation covering its descendants. `archive` is the SMB-shared raw-data namespace; container state is never beneath it.
- The `immich` system account is fixed to UID/GID `1100`, has no login shell or `wheel` membership, and receives only
  the `video` and `render` supplementary groups. Immich's rootful Quadlets run as `1100:1100`; Server and ML receive
  `/dev/dri`, while the Photobook external library is read-only at `/external/photobook`.
- Atlas applies persistent kernel network hardening: redirects and source routes are rejected, martians logged, reverse-path filtering remains loose for WireGuard, and IPv4 forwarding is disabled. SSH permits only the declared administrator using public-key authentication; root login, passwords, agent and remote forwarding
  are disabled, while local forwarding remains available for private administrative tunnels. Photobook is exported only to the configured Aegis IP with all access squashed to UID/GID
  `1100`. Targeted SELinux is enforced persistently; a required reboot is reported but never initiated automatically. The primary LAN interface is assigned explicitly to the managed firewalld zone, and firewall rules are applied before NFS or SMB are started; their service state and TCP listeners are then verified. SMB3 exposes `Archive` to Vault-backed authorized accounts on mandatory encrypted, signed SMB3 over TCP/445 only and admits the configured LAN without host-specific exclusions.
- Atlas NPM and Immich share a rootful Podman network. NPM publishes HTTP/HTTPS, but its administration port remains
  bound to `127.0.0.1:81`; do not expose it directly to the LAN or Internet.
- `profile_backend_phase1` temporarily runs rootless Navidrome and Syncthing on Atlas until Uranus replaces
  them. It binds only to Atlas' LAN IP, never `wg0`; Navidrome and the Syncthing GUI admit only Aegis as
  the source-NAT gateway, while native Syncthing ports admit the configured LAN. It initializes fresh
  state only and never migrates or deletes source application data.
- `wireguard_overlay` manages `wg0` between Prometheus (`10.0.0.1`) and Aegis (`10.0.0.2`). It persists private
  keys only on their respective hosts, exchanges only derived public keys through Ansible, and verifies a real peer
  handshake. Prometheus opens `51820/udp`; Aegis is the LAN gateway. Its persistent IPv4 forwarding, narrowly scoped
  WireGuard-to-LAN firewalld policy, and source masquerading permit Prometheus to reach LAN services without a static
  route on the router. Prometheus includes `192.168.178.0/24` in Aegis' peer `AllowedIPs`; add the Uranus VIP there
  when it is assigned. After a firewalld reload, restore Prometheus' rootful Podman networking with
  `podman network reload --all` so the existing proxy stack retains container DNS.

## Atlas NAS TODO
Completed validation: the existing RAIDZ2 pool and datasets, SELinux, LAN firewall, SSH, Cockpit with
the selected 45Drives plugins, encrypted SMB3 `Archive`, the Aegis-only NFSv4 `photobook` export, and the
Prometheus--Aegis WireGuard gateway are operational. The gateway handshake, forwarding, source masquerading,
and TCP reachability to Atlas were verified. Temporary Navidrome and Syncthing are available through their
manual NPM Proxy Hosts; Syncthing uses `/data/Org` backed by the SMB-shared Archive dataset. Aegis has also
validated NFSv4.2 read, write, delete, and `all_squash` mapping to UID/GID `1100` end-to-end. The ZFS
snapshot timers are active and the first recursive hourly snapshot completed successfully; the first
scheduled retention prune and monthly scrub remain runtime checks.

### Priority 1 - Data protection
- [x] Deploy Ansible-managed recursive ZFS snapshots with 24 hourly, 30 daily, 8 weekly, and 12 monthly
  generations, plus a monthly scrub on the first Sunday at 03:00. The timers and first hourly snapshot were
  verified on Atlas. Still observe the first scheduled retention prune and scrub; Cockpit Scheduler is for
  visibility or manual operations only, and snapshot rollback is never automated.
- [x] Activate and validate the encrypted offsite Borg backup to the Hetzner Storage Box. Atlas uses the
  dedicated SSH identity, pinned ED25519 host key, Vault-backed `repokey` encryption, and a locked
  non-login `borg` account with no sudo or supplementary groups. The initial snapshot-consistent backup,
  Borg repository check, and temporary-directory restore completed successfully; the restored `Archive`
  tree matched the live data, and temporary snapshots and mounts were removed. The exported recovery key
  was copied offline. Daily backup retries and logging, 30 daily, 8 weekly and 12 monthly archives,
  compaction, and monthly repository checks are enabled.
- [ ] Add the UUID-bound offline USB backup with versioned rsync, locking, capacity checks, verification,
  safe unmounting and a tested restore procedure; never trigger it for an arbitrary USB disk.
- [ ] Test restores independently from a ZFS snapshot, Borg, and the offline USB backup before relying on
  any backup path.
- [ ] Add monitoring and alerting for pool health, scrub/resilver, SMART data, temperatures, free space,
  snapshot/backup capacity growth, and failed maintenance or backup timers.

### Priority 2 - NAS operability and recovery
- [ ] Document and test disaster recovery: rebuild Atlas with Ansible, import the existing pool, restore
  from snapshot/USB/Hetzner, preserve Vault and Borg recovery material offline, and define RPO/RTO.
- [ ] Define a controlled Rocky kernel/OpenZFS update and reboot procedure.
- [ ] Add the Atlas-initiated least-privilege Prometheus backup pull: Prometheus exposes only prepared
  read-only dumps through a dedicated account and Atlas retains the private SSH key, pinned host key,
  atomic pull, verification, retention and systemd service/timer.
- [ ] Decide whether a common SMB/NFS namespace is required. `Archive` (SMB) and `photobook` (NFS) are
  intentionally distinct today; only if a shared namespace is selected, finalize its UID/GID, group,
  and POSIX ACL model and test the same files through both protocols.

### Priority 3 - Service expansion
- [ ] After data protection and recovery are validated, populate `/zpool/media/music` and validate Navidrome.
- [ ] Design and deploy Nextcloud as another explicitly temporary Atlas service before Uranus. Give it
  separate persistent application, database, and cache storage; keep credentials in Vault; publish it only
  through NPM over the Prometheus--Aegis gateway; and define backup, upgrade, and eventual Uranus-migration
  procedures before exposing user data. Do not deploy Nextcloud before the data-protection checklist is complete.
- [ ] Keep `atlas_manage_media_stack` disabled until the future Immich deployment has validated `/dev/dri`,
  container paths, and the required Vault database secret.

### Priority 4 - Optional workflows
- [ ] Optionally design iCloud photo ingestion and an Aegis persistent NFS mount as a separate workflow
  after the storage and backup layers are validated; do not make either a dependency of the Atlas
  baseline.

## Coding Agent Notes
- Shared agent definitions and lifecycle flags live in `ai_agents` in `ansible/inventory/group_vars/all.yml`.
- Shared agent dotfiles live in `ai_agents_dotfiles`; rendered configs live in `ai_agents_templates`.
- Every `ai_agents.<agent>` entry has independent `install_enabled`, `deploy_enabled`, and `uninstall_enabled` flags. Installation and removal must not both be true for the same agent; the common pre-task fails before changes when they conflict.
- Fedora, Void desktop, and WSL workstation profiles consume the shared agent definitions; do not duplicate package entries in profile-specific vars. IBM Bob on the workstation follows its own flags.
- `dotfiles_common` deploys `ai_agents_dotfiles` and renders `ai_agents_templates` only when deployment is enabled.
- Removal is limited to the managed npm packages and `/usr/local/bin/bob`; never remove agent dotfiles, instructions, credentials, or user data.
- Keep `.config/ai/` as the common instruction source; update agent-specific entrypoints to reference it rather than duplicating instruction text.

## Tooling Notes
- Install local tooling with:
  - `python3 -m pip install ansible ansible-lint yamllint shellcheck-py`
  - `ansible-galaxy collection install -r ansible/collections/requirements.yml`
- Required collections currently include `ansible.posix` and `community.general`.
- `.yamllint` treats `line-length` as a warning at 120 chars and disables `document-start` and `comments-indentation`.

## When Updating Docs
- Keep `README.md` and `AGENTS.md` aligned when workflows materially change.
- If you add a new operational area, also add the narrowest validation command for it.
- Call out checks you could not run and any follow-up verification needed.

## Aegis Fedora IoT Notes
- `aegis` is a remote Fedora IoT Raspberry Pi 4 node. Bootstrap it once with
  `ansible/bootstrap/aegis.bu`; the remaining configuration is applied by `profile_aegis` over SSH.
- Fedora IoT is immutable. Do not add it to mutable Fedora package or shared dotfile roles.
- `profile_aegis` owns the `nfs-utils` and `wireguard-tools` rpm-ostree layers and reports the required reboot
  without initiating it. `wireguard_overlay` then configures Aegis as the WireGuard LAN gateway with persistent IPv4
  forwarding, a scoped inter-zone policy, and source masquerading. It also owns rootful Podman Quadlets, persistent container
  state under `/var/lib`, the Podman auto-update timer, LAN-restricted firewalld rules, and SSH hardening. Keep
  `aegis_lan_subnet`, `aegis_adguard_web_port`, and `aegis_network_connection_uuid` host-specific;
  SSH permits only the declared
  key-authenticated users, never root or password authentication. Keep Apple IDs and other
  credentials in Vault and use `no_log` for their rendering.
- `aegis_adguard_web_port` defaults to `80`. The initial AdGuard Home wizard port `3000` is intentionally unmanaged: open and close it manually only while
  completing initial setup. Disable the local systemd-resolved stub through `profile_aegis` before
  AdGuard binds port 53; keep
  `/etc/resolv.conf` linked to `/run/systemd/resolve/resolv.conf`. LAN clients may use AdGuard, but
  Aegis must use the independent upstream DNS declared by `aegis_host_dns_servers` so Greenboot does
  not depend on the AdGuard container during startup.
- iCloudPD requires post-deployment interactive MFA initialization; its cookie/configuration state is
  persisted in `/var/lib/icloudpd/config`.
