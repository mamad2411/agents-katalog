---
name: hardened-agent-vps
description: Provision and harden a Hetzner VPS with Terraform and Ansible as a private AI-agent and automation workbench, with optional Claude Code CLI, Codex CLI, Firecrawl, and remote desktop profiles, plus strict SSH/firewall guardrails, secret-safe env management, backups, health checks, and repeatable service lifecycle steps.
---

# SKILL: hardened-agent-vps (Hetzner + Terraform + Ansible private workbench)

## Purpose
Provision and harden a Hetzner Cloud VPS in a repeatable, safe-by-default workflow:
- Terraform: server + Hetzner firewall
- Ansible: base config + security (UFW + fail2ban + unattended-upgrades)
- Baseline tools: Docker, Docker Compose v2, jq, gh, ffmpeg, screen, Python 3/pipx
- Python operator tooling: uv/uvx installed system-wide by default; Poetry remains project-specific compatibility, not a VPS baseline
- Optional: deploy a private Firecrawl self-host stack for crawl/scrape/PDF extraction workflows
- Optional: install a lightweight NoMachine/XFCE remote desktop restricted to the Tailscale path
- Support one VPS as an agent workbench for Claude Code CLI, Codex CLI, and service agents while keeping live apps, staging, repos, and agent services in separate zones
- Provide operator commands for status, backups, off-box backup verification, health alerts, and Docker cleanup

## Core operating workflow
1) Identify request type first: access, infra change, config change, runtime/service change, or assistant capability change.
2) Load current local artifacts before changing anything:
   - `SKILL.md`
   - `LEARNINGS.md`
   - active `.codex/plan/*.md` files, if present
   - `templates/infra/*`
   - `templates/ansible/site.yml`
   - relevant role files under `templates/ansible/roles/*`
3) Confirm whether change is Terraform, Ansible, or both.
4) Before an Ansible run, check `git status`: Ansible copies files from the working tree, so a half-finished change in another session can fail a run midway.
5) Execute the smallest safe change first, then validate with concrete health checks.

## Local config and sharing rule
- The tracked skill must stay generic and shareable. Keep machine/account-specific values in ignored local files.
- Copy examples before first use:
  - `templates/ansible/inventory.ini.example` -> `templates/ansible/inventory.ini`
  - `templates/ansible/vars/local.yml.example` -> `templates/ansible/vars/local.yml`
  - `templates/infra/terraform.tfvars.example` -> `templates/infra/terraform.tfvars`
- `templates/ansible/site.yml` automatically loads `templates/ansible/vars/local.yml` from the controller when present.
- Do not commit local inventory, local Ansible vars, Terraform tfvars/state/plans, Ansible logs, backup archives, optional service `.env` files, OAuth profiles, pairing state, or SSH keys.
- Source-controlled Claude skill templates for VPS users live under `templates/claude-skills/` and are safe to copy because this tree must not contain secrets.

## VPS zoning model
- A single Hetzner VPS may host optional app profiles, Claude Code CLI, Codex CLI, Docker containers, Git checkouts, and websites, but do not run them all as root in one shared directory.
- Keep live applications, staging, source repos, and long-running agent services as separate zones. Good default paths:
  - `/srv/apps/production-site` for live app runtime
  - `/srv/apps/staging-site` for staging/test runtime
  - `/home/<agent_user>/repos/project` for ordinary Git checkouts where Claude Code CLI, Codex CLI, or an operator edits code
  - `/home/<agent_user>/agent-workspaces/claude-code` for disposable/agent-specific workspaces
  - `/home/<agent_user>/agent-workspaces/codex-cli` for Codex CLI scratch work and separate sessions
  - `/opt/firecrawl` plus `/etc/firecrawl` for the optional private Firecrawl stack
  - `/var/backups` for backups
- The Ansible baseline creates the parent zone directories by default: `/srv/apps`, `/home/<agent_user>/repos`, `/home/<agent_user>/agent-workspaces`, and `/var/backups`. The Firecrawl role manages `/opt/firecrawl` and `/etc/firecrawl` only when Firecrawl is enabled. Create concrete app/repo directories only when the real app or repo name is known.
- Run Claude Code and Codex as `agent_user` (default `agent`), never as the admin user. The agent user has no sudo and is not in the `docker` group, because either one gives root on the host. The admin user keeps both for the operator. Start agents from an admin SSH session with `sudo -iu agent`, and give the agent user only its own narrow Git and API credentials.
- Treat Claude Code CLI and Codex CLI as interactive coding tools by default: run them in SSH/tmux/mosh sessions against Git repos or disposable workspaces, with separate auth/config directories when possible.
- Use the dual-agent review pattern when helpful: Claude Code develops, Codex produces a read-only Markdown review. Do not let both agents edit the same worktree at the same time.
- AI agents must not write directly to `/srv/apps/production-*`, `/var/www`, production `.env` files, or production databases. Use Git, reviewed diffs, CI/deploy scripts, Ansible, or a staging promotion step.
- Give agent services dev/staging credentials by default. Use production credentials only after an explicit decision, with the narrowest scope possible and no shared `.env` across optional app profiles, Claude Code CLI, Codex CLI, and app runtimes.
- For a multi-agent VPS with Docker builds, browser automation, crawling, or databases, prefer at least 4-8 GB RAM and choose 8 GB when budget allows; enable swap and validate memory pressure before adding another service.

## Dual-agent review workflow
- Default flow: Claude Code implements, Codex reviews. Only Claude Code edits the worktree.
- The base role installs the `codex-review` Claude skill into `claude_skills_dir` and exposes `claude-codex-review` on the system PATH by default. It asks Codex CLI for a read-only review through `codex review`, not `codex exec`, supports `--uncommitted`, `--commit`, and `--base`, includes recent `.codex/plan/*.md` context when present, and writes a Markdown report under `.claude/reviews/` unless `-o` is provided. It does not commit, stage, or edit source files.
- Example:
  ```bash
  claude-codex-review "Review the current diff as a strict senior engineer. Focus on bugs, tests, and simplification."
  claude-codex-review --base main "Review this branch against main."
  ```
- To choose a stable output path:
  ```bash
  claude-codex-review -o codex-review.md "Check whether this implementation is overengineered."
  ```
- By default it refuses likely secret-bearing paths and diffs larger than `CODEX_REVIEW_MAX_DIFF_BYTES` (default `200000`). Override only after manual review with `CODEX_REVIEW_ALLOW_SENSITIVE_DIFF=1` or `CODEX_REVIEW_ALLOW_LARGE_DIFF=1`.
- Plan context is included by default from the latest `.codex/plan/*.md` files and capped by `CODEX_REVIEW_MAX_PLAN_BYTES` (default `60000`). Set `CODEX_REVIEW_INCLUDE_PLAN=0` when the plan is irrelevant or sensitive.
- Do not let the reviewer commit its own review. If a review report should be versioned, let the primary agent or operator inspect it first, then commit only the Markdown report in a separate commit.

## Controller machine discipline
- When work continues from a different controller machine, rediscover local state instead of assuming previous inventory, SSH keys, shell aliases, Terraform env vars, or `known_hosts` entries exist.
- The default private access model is ordinary OpenSSH over the Tailscale network, not Tailscale SSH. Keep Tailscale connected, but keep the Tailscale SSH intercept disabled unless Steven deliberately chooses that separate access model.
- Prefer ordinary `ssh <admin_user>@<tailscale-ip-or-hostname>` for operator checks and Ansible. Use `tailscale ssh <admin_user>@agent-vps '<command>'` only when the VPS has Tailscale SSH enabled on purpose. The bare `tailscale ssh agent-vps ...` form uses the local controller username and fails if that user does not exist on the VPS.
- Do not create a new SSH key just because ordinary `ssh agent-vps` fails. First verify whether the hostname resolves to the intended Tailscale IP and whether `RunSSH=false` means the Tailscale SSH feature is simply disabled.
- Do not edit `known_hosts` to work around a host-key verification failure unless the operator explicitly approves that cleanup; stale host keys can be expected after a rebuild or IP reuse.
- If `tailscale ssh agent-vps` fails host-key checking but ordinary `ssh agent-vps` connects to the Tailscale IP and `ansible -i templates/ansible/inventory.ini vps -m ping` succeeds, check `sudo tailscale debug prefs` on the VPS. If `RunSSH=false`, this is not a stale local `known_hosts` problem; Tailscale SSH is disabled. Prefer ordinary SSH for Ansible/operator work unless Steven explicitly chooses the Tailscale SSH access model.
- If Ansible must run from the new controller, create or restore ignored local files deliberately (`inventory.ini`, `vars/local.yml`, Terraform vars) and validate connectivity before applying.

## Controller SSH key rotation
- Rotate the controller SSH key when the current private key is lost, has an unknown passphrase, is too awkward for non-interactive Ansible/Codex runs, or should be retired.
- Keep the final controller key filename stable, e.g. `~/.ssh/id_ed25519_agent_vps_controller`. If replacing an existing key, park the old private key under a clearly legacy filename first; do not delete it until the new key has been tested.
- For automation-friendly controllers, an Ed25519 key with an empty passphrase is acceptable when the key stays local, has mode `600`, and VPS SSH remains Tailscale-only. If a passphrase is used on macOS, add it deliberately with `ssh-add --apple-use-keychain <key>` and verify the expected fingerprint appears in `ssh-add -l -E sha256`.
- Add the new public key to ignored `templates/ansible/vars/local.yml` as a separate `admin_authorized_keys` entry before removing the old controller key entry.
- If the current controller cannot SSH yet, use an existing trusted path such as Termius over Tailscale, Tailscale SSH, or the provider console to append only the new public key to `~/.ssh/authorized_keys`; do not reopen public SSH to solve key rotation.
- Validate in this order:
  1. `ssh-keygen -l -f ~/.ssh/id_ed25519_agent_vps_controller.pub`
  2. `ssh <admin_user>@<tailscale-ip-or-hostname> 'hostname && whoami'`
  3. `ansible -i templates/ansible/inventory.ini vps -m ping`
  4. remove the legacy controller key from `admin_authorized_keys`
  5. rerun `ansible-playbook -i templates/ansible/inventory.ini site.yml`
  6. verify `authorized_keys` labels/fingerprints and run `sudo agent-vps backup` plus `sudo agent-vps status`
- Keep phone/tablet/secondary-controller keys as separate entries with stable labels so one device can be revoked without affecting the others.
- Do not rename Terraform `ssh_key_names` just because the local controller key file was renamed; those names refer to Hetzner Cloud SSH key resources and should change only after the cloud key is verified or intentionally renamed.

## Controller SSH helpers
- SSH helpers are optional controller-local convenience only; do not make the tracked skill depend on machine-specific shell aliases.
- Keep helpers in the controller user's shell config, not in this repo. A minimal zsh pattern is:
  ```bash
  export AGENT_VPS_SSH_TARGET='<admin_user>@agent-vps'
  vps-ssh() { ssh "$AGENT_VPS_SSH_TARGET" "$@"; }
  vps-status() { ssh "$AGENT_VPS_SSH_TARGET" 'sudo agent-vps status'; }
  ```
- Validate helpers before relying on them:
  - `vps-ssh 'hostname && whoami'`
  - `vps-status`
- For operator checks, helpers should use OpenSSH over the Tailscale hostname/IP by default. For normal Ansible applies, still use deliberate ignored local inventory/vars and the documented validation flow.
- If a helper fails but direct `ssh <admin_user>@<tailscale-ip-or-hostname> '<command>'` works, prefer fixing the local helper over changing VPS SSH configuration.

## Termius and SSH clients
- Termius should use normal SSH over the Tailscale network, not a public SSH exception.
- The skill default is OpenSSH over Tailscale with Tailscale SSH disabled. Run
  `sudo tailscale set --ssh=false` after joining the tailnet unless Tailscale
  SSH was explicitly chosen as the access model.
- Termius should use OpenSSH on the VPS over the Tailscale IP. If Tailscale SSH
  is enabled on the VPS with `tailscale up --ssh` or `tailscale set --ssh=true`,
  Tailscale may intercept port `22` before OpenSSH sees `authorized_keys`,
  causing Termius to hang on authentication. For Termius access, disable that
  intercept with `sudo tailscale set --ssh=false` while keeping Tailscale itself
  connected and UFW restricted to the tailnet.
- Requirements:
  - Termius device has Tailscale installed and is logged into the same tailnet.
  - Host is the VPS Tailscale IP or MagicDNS name, e.g. `agent-vps` when MagicDNS works.
  - Port is `22`.
  - User is the non-root admin user from `admin_user`.
  - Authentication uses the private key matching `admin_authorized_keys`; password login stays disabled.
- For the current local deployment, the admin user is set in ignored `templates/ansible/vars/local.yml`; do not hard-code that private value into the public-cleaned repo.
- Preferred phone/tablet key flow:
  1. Create a new Ed25519 key inside Termius on the phone/tablet.
  2. Copy only the public key.
  3. Add that public key as a separate entry in `admin_authorized_keys` in ignored `templates/ansible/vars/local.yml`.
  4. Rerun Ansible from the controller.
  5. Connect Termius to the VPS Tailscale IP/hostname as the non-root admin user on port `22`.
  This gives the phone/tablet its own revocable key and avoids copying the controller's private key into Termius.
- After adding a phone/tablet key:
  - give the key a stable label such as `termius-phone` in `admin_authorized_keys`
  - record the public-key fingerprint with `ssh-keygen -l -f <(printf '%s\n' '<public-key>')`
  - verify presence without printing all keys: `grep -F '<public-key-body>' ~/.ssh/authorized_keys >/dev/null && echo present`
  - expect `authorized_keys` to contain more than one key when both controller and phone/tablet access are enabled
  - after a successful Termius login, rename the key inside Termius to a clear name such as `vps-phone`
- Validate from a shell before debugging Termius:
  ```bash
  ssh <admin_user>@<tailscale-ip-or-hostname> 'hostname && whoami'
  ```
- If Termius reaches the VPS but hangs on `Authenticating`, check
  `journalctl -u tailscaled` on the VPS. Logs like `handling conn:
  <phone-tailscale-ip>:<port>-><user>@<vps-tailscale-ip>:22` without an OpenSSH
  login usually mean Tailscale SSH is intercepting the connection. Run
  `sudo tailscale set --ssh=false`, then retry Termius.
- If Termius is on a phone or tablet, install and connect Tailscale on that device first. Do not copy VPS secrets, runtime env files, Terraform state, or backups into Termius.

## Optional non-headless desktop
- Keep the default VPS headless. A desktop increases package count, memory use, and exposed local session surface, so install it only for a concrete need.
- The supported opt-in desktop profile is NoMachine plus XFCE when proprietary free-for-personal-use software is acceptable:
  - set `install_remote_desktop=true` and `install_nomachine=true`
  - rerun Ansible after SSH/Tailscale access is stable
  - NoMachine installs from the official Linux amd64 DEB with MD5 verification
  - NoMachine UPnP/NAT-PMP port mapping is disabled
  - NoMachine automatic firewall changes are disabled and installer-created public UFW rules are removed
  - virtual desktops are forced to start XFCE with `/etc/X11/Xsession startxfce4`
  - `admin_authorized_keys` are copied to `/home/<admin_user>/.nx/config/authorized.crt`
  - NX private-key authentication is required by default
  - UFW allows TCP/UDP `4000` only from `tailscale_ssh_source_cidr`
  - connect from the NoMachine client with protocol `NX`, port `4000`, username `admin_user`, and the private key matching one of `admin_authorized_keys`
  - when NoMachine says it cannot detect a display, choose **Yes** to create a virtual display; this is expected on a VPS
  - do not use NoMachine Network/cloud for this VPS; connect directly to the Tailscale IP or MagicDNS hostname
- Do not open public GUI ports in UFW or the Hetzner firewall. NoMachine is allowed only on TCP/UDP `4000` from the Tailscale CIDR.
- If a full desktop is unavoidable, prefer reviewing package impact explicitly instead of replacing the default with `xubuntu-desktop` casually.
- Resource guidance:
  - minimum for light desktop use: 2 vCPU / 4 GB RAM
  - preferred for browsers, IDEs, and agent tools: 4 vCPU / 8 GB RAM or more
  - validate `free -h`, `swapon --show`, and Docker memory pressure before adding browser-heavy workloads

## macOS controller Ansible setup
- Prefer Homebrew on macOS when it is already installed:
  - `zsh -lc 'brew install ansible'`
  - `zsh -lc 'ansible --version && ansible-playbook --version'`
- Validate local syntax without contacting a real VPS:
  - `zsh -lc 'cd templates/ansible && ansible-playbook -i inventory.ini.example site.yml --syntax-check'`
- Real Ansible runs still require ignored local controller files (`inventory.ini`, `vars/local.yml`) and an explicit apply decision.
- If Homebrew is unavailable, ask before installing a package manager or choosing an alternate pipx-based Ansible install.
- Rollback for a Homebrew install is `zsh -lc 'brew uninstall ansible'`; run `brew autoremove` only after checking it will not remove dependencies used by other tools.

## macOS controller Terraform setup
- Terraform is needed only for Hetzner server/firewall work, not for app-only Ansible changes.
- Prefer the official HashiCorp Homebrew tap on macOS when Homebrew is already installed:
  - `zsh -lc 'brew tap hashicorp/tap && brew install hashicorp/tap/terraform'`
  - `zsh -lc 'terraform version'`
- Validate local Terraform syntax without credentials or remote state:
  - `zsh -lc 'terraform -chdir=templates/infra fmt -check -diff'`
  - `zsh -lc 'terraform -chdir=templates/infra init -backend=false -input=false -lockfile=readonly'`
  - `zsh -lc 'terraform -chdir=templates/infra validate'`
- `terraform init -backend=false` may create an ignored `.terraform/` directory in the infra template folder; do not commit it.
- Real plans still require `templates/infra/terraform.tfvars` or equivalent vars plus a secure Hetzner token source such as `hctf`; never run `apply` unless the plan has been inspected and matches the approved scope.
- Rollback for a Homebrew install is `zsh -lc 'brew uninstall hashicorp/tap/terraform'`; run `brew autoremove` only after checking it will not remove dependencies used by other tools.

## Core principle
- Never expose SSH to the whole internet.
- Bootstrap with a narrow allow-list (your current public IP `/32`) or via Hetzner Console.
- After Tailscale is up, tighten rules to Tailscale-only in both UFW and the Hetzner firewall.

## Access discipline
- Prefer OpenSSH restricted to the Tailscale network.
- Avoid root login unless explicitly requested and still enabled for a bootstrap step.
- Do not change SSH/80/443 public exposure without explicit approval.
- A fresh rebuild is not complete until OpenSSH over Tailscale is proven and public bootstrap SSH is removed from both UFW and the Hetzner firewall.
- Keep all service ports loopback-bound unless a public exposure decision is explicit.
- Keep remote desktop access on Tailscale through NoMachine; do not expose GUI ports publicly.
- Do not reopen public SSH for Termius or another SSH client. Put the client device on the Tailscale tailnet and connect to the VPS Tailscale IP/hostname on port 22 as the non-root admin user with the configured SSH key.

## Hard safety rules
1) Never leave SSH open to the whole internet. SSH must be restricted to a bootstrap `/32`, then Tailscale-only.
2) Never enable UFW without allow rules that preserve access.
3) Root login disable is gated: validate non-root SSH first, then set `disable_root_login=true`.
4) Never enable password login. Keep `PasswordAuthentication no`. The security role sets it in `/etc/ssh/sshd_config.d/00-agent-vps-hardening.conf`, which sshd reads first, and fails the run when `sshd -T` shows another value.
5) Never print secrets. Never commit API keys, bot tokens, OAuth files, pairing state, or service `.env` files.
6) Keep optional service ports private by default: bind published ports to `127.0.0.1` and access via SSH tunnel or Tailscale.
7) Keep Firecrawl private by default: bind the API to `127.0.0.1`.
8) Keep optional desktop access private: NoMachine over Tailscale only, no public GUI ports.
9) For existing servers, never apply Terraform if plan shows `hcloud_server` destroy/replace unless rebuild is explicitly intended.
10) Keep deterministic artifacts as source of truth: Terraform + Ansible templates in this skill.
11) Keep production apps, staging, repos, and agent workspaces isolated; never let an agent directly mutate production runtime files or share production secrets by default.
12) Run coding agents as `agent_user`, never as the admin user or root. The admin user keeps passwordless sudo and the `docker` group on purpose for Ansible and operator work, so an agent started there has root on the host.

## Credential loading (Hetzner token)
- Preferred/default path for local controller work: use the protected `hctf` wrapper when available.
- `hctf` loads the Hetzner token from macOS Keychain service `hcloud-token` and injects `HCLOUD_TOKEN` plus `TF_VAR_hcloud_token` only into one Terraform child process.
- Safe plan example: `hctf -chdir=templates/infra plan -input=false`.
- Allowed helper subcommands should be limited to `fmt`, `init`, `validate`, `plan`, `show`, `state`, `import`, `providers`, `output`, and `version`.
- The helper must refuse `apply` and `destroy`; Steven applies manually after reviewing an approved saved plan.
- If `hctf` is unavailable, export `TF_VAR_hcloud_token` from a secure source for one command only. Never print the token, use command substitution around token helpers, or commit tfvars/state/plans.
- Optional macOS Keychain storage, outside the repo: `security add-generic-password -a "$USER" -s hcloud-token -w '<paste-token-here>'`.

## Hetzner CLI / hcloud
- `hcloud` is optional. Terraform remains the source of truth for managed Hetzner server and firewall changes.
- Install on a macOS controller only when Hetzner read-only inspection or emergency operator checks are useful:
  - `zsh -lc 'brew install hcloud'`
  - `zsh -lc 'hcloud version'`
- Preferred auth for temporary controller sessions: use a narrow operator-controlled `HCLOUD_TOKEN` source for the child command only, then run read-only `hcloud` commands.
- Safe read-only checks:
  - `hcloud server list`
  - `hcloud server describe agent-vps`
  - `hcloud firewall list`
  - `hcloud firewall describe agent-vps-fw`
- Do not use `hcloud` to mutate Terraform-managed resources unless the operator explicitly approves a manual/emergency change. After any approved manual change, reconcile the intended state back into Terraform before the next apply.
- Do not commit `hcloud` contexts, tokens, command output containing account details, Terraform tfvars, plans, or state.

## Python tooling baseline
- Install `uv` by default on VPS workbench hosts; `uvx` is included with `uv`.
- The Ansible base role installs pinned `uv_version` into `uv_install_dir` (default: `/usr/local/bin`) with `UV_NO_MODIFY_PATH=1` so operators and agents can call `uv` and `uvx` from the normal system PATH.
- Use `uvx <tool>` for one-off Python CLI tools and MCP servers, `uv tool install <tool>` for persistent operator tools, and `uv run ...` inside projects that use uv.
- Keep Poetry out of the baseline. If a checked-out repo has `poetry.lock` or explicitly requires Poetry, install it deliberately for that repo, preferably with `pipx install poetry`, then use `poetry run ...` for that repo only.
- Bump `uv_version` deliberately; do not float the installer URL to unpinned latest in templates.

## GitHub CLI on VPS
- `gh` is installed as baseline tooling, but the base workbench does not require GitHub auth for default runtime checks.
- Do not authenticate `gh`, create VPS GitHub SSH keys, or add deploy keys unless host-side repo operations are explicitly needed.
- If repo operations become required, prefer a separate low-privilege GitHub account or repo-scoped deploy keys over the operator's primary GitHub account.
- Use a host-side admin-user key such as `~/.ssh/id_ed25519_github_agent_vps` and a dedicated SSH host alias such as `github-agent-vps`; keep the key out of root, containers, Termius, and Git.
- Use device-flow `gh auth login` only when GitHub API/CLI access is needed in addition to SSH Git transport; keep runtime secrets and service state out of Git repositories.
- Do not expose `/root/.ssh` or mount host SSH keys into optional service containers without an explicit design.

## Inputs / knobs (Ansible)
- `admin_user` (default: `admin`)
- `agent_user` (default: `agent`; unprivileged account for Claude Code and Codex, without sudo or the `docker` group; must differ from `root` and `admin_user`)
- `admin_authorized_keys` (default: `[]`; required before `disable_root_login=true`)
- `disable_root_login` (default: `false`)
- `tailscale_ssh_source_cidr` (default: `100.64.0.0/10`)
- `bootstrap_public_ssh_cidr` (repo default: `""`; first public bootstrap must be your current public IP `/32`)
- `bootstrap_public_ssh_cidr_cleanup` (default: `""`; optional)
- `allow_http`, `allow_https` (defaults: `false`)
- `swap_enabled`, `swap_size_mb`, `swap_swappiness`
- `install_uv` (default: `true`; installs `uv` and `uvx` into `/usr/local/bin`)
- `refresh_uv` (default: `false`; force rerun of the pinned uv installer)
- `uv_version` (default: `0.11.14`)
- `uv_install_dir` (default: `/usr/local/bin`)
- `install_remote_desktop` (default: `false`; optional XFCE baseline for NoMachine)
- `remote_desktop_packages` (default: `xfce4`, `xfce4-terminal`, `dbus-x11`, `xauth`)
- `install_nomachine` (default: `false`; optional NoMachine over Tailscale)
- `nomachine_version`, `nomachine_deb_url`, `nomachine_deb_md5`
- `nomachine_port` (default: `4000`)
- `nomachine_key_auth_only` (default: `true`; requires NX private-key auth)
- `nomachine_allow_tailscale` (default: `true`; allows TCP/UDP `4000` from Tailscale CIDR)
- `nomachine_disable_upnp` (default: `true`)
- `nomachine_disable_firewall_autoconfig` (default: `true`)
- `install_codex_review_helper` (default: `true`; installs `claude-codex-review`)
- `codex_review_helper_path` (default: `/usr/local/bin/claude-codex-review`)
- `claude_skills_dir` (default: `/home/<agent_user>/.claude/skills`)
- `claude_codex_review_skill_src_dir` (default: `templates/claude-skills/codex-review`)
- `vps_zone_dirs_enabled` (default: `true`)
- `vps_zone_dirs` (default parent zones: `/srv/apps`, `/home/<agent_user>/repos`, `/home/<agent_user>/agent-workspaces`, `/var/backups`; VPS ops manages the backup/monitoring paths; Firecrawl role manages `/opt/firecrawl` and `/etc/firecrawl` when enabled)
- `install_vps_ops` (default: `true`; installs `agent-vps` operator commands, backups, health checks, and cleanup timers)
- `vps_ops_env_dir`, `vps_ops_env_file` (defaults: `/etc/agent-vps`, `/etc/agent-vps/.env`; sole source for optional Telegram notification settings for health-state changes)
- `install_claude_code` (default: `false`; installs Claude Code CLI with the official installer)
- `install_codex_cli` (default: `false`; installs Codex CLI with npm plus its sandbox prerequisites)
- `install_firecrawl` (default: `false`; optional private Firecrawl stack)
- `vps_backup_dir` (default: `/var/backups/agent-vps`)
- `vps_backup_offbox_enabled` (default: `false`; opt-in rsync-over-SSH copy and checksum verification)
- `vps_backup_offbox_target` (required when enabled; format `user@host:/path`)
- `vps_backup_offbox_state_file` (default: `/var/lib/agent-vps-monitor/last-offbox-ok`)
- `vps_backup_offbox_pending_file` (default: `/var/lib/agent-vps-monitor/offbox-retry-pending`; records the archive to retry when the target is unavailable)
- `vps_backup_offbox_max_age_hours` (default: `36`; status fails when the last verified off-box copy is older)
- `vps_backup_retention_days` pruning runs only when off-box is enabled and the verified off-box state file is fresh.
- Timer toggles: `vps_backup_timer_enabled`, `vps_docker_cleanup_timer_enabled`, `vps_healthcheck_timer_enabled`
- Firecrawl knobs:
  - `firecrawl_enable_service` (default: `false`)
  - `firecrawl_env_dir`, `firecrawl_env_file` (defaults: `/etc/firecrawl`, `/etc/firecrawl/firecrawl.env`)
  - `firecrawl_dir`, `firecrawl_compose_file` (defaults: `/opt/firecrawl`, `/opt/firecrawl/docker-compose.yml`)
  - `firecrawl_api_bind_address` (default: `127.0.0.1`)
  - `firecrawl_api_port`, `firecrawl_internal_port` (defaults: `3002`)
  - `firecrawl_image`, `firecrawl_playwright_image`, `firecrawl_postgres_image`
  - `firecrawl_postgres_db` (must be `postgres` with upstream `nuq-postgres`)
  - `firecrawl_auto_generate_secrets` (default: `true`)
  - low-concurrency knobs: `firecrawl_num_workers_per_queue`, `firecrawl_crawl_concurrent_requests`, `firecrawl_max_concurrent_jobs`, `firecrawl_browser_pool_size`, CPU/memory limits, `firecrawl_block_media`, `firecrawl_logging_level`

## Inputs / knobs (Terraform)
- `server_name`, `firewall_name`, `image`, `server_type`, `location`
  - for a new default server, use `server_name = "agent-vps"`
  - `firewall_name` is optional; when unset, Terraform uses `<server_name>-fw`
- `ssh_key_names` (list)
- `ssh_source_ips` (list; first bootstrap should be your public IP `/32`)
- `allow_http`, `allow_https` (default false)
- Existing-server caution: changing `server_name` or `ssh_key_names` may force replacement.

## Terraform change discipline
- Treat `templates/infra/terraform.tfvars` as the current server definition.
- Always run `terraform -chdir=templates/infra plan` before `apply`.
- If the plan shows `hcloud_server.vps` destroy/create or replacement, stop and ask before applying.
- Treat `server_name` and `ssh_key_names` as immutable unless a rebuild is explicitly intended.
- `firewall_name`, `ssh_source_ips`, `allow_http`, and `allow_https` should normally update the firewall in place; still inspect the plan before applying.
- Do not use `-refresh=false` for real infrastructure changes. It is only a local syntax/sanity shortcut when credentials are unavailable.

## Deployment workflow
1) Configure Terraform variables and bootstrap SSH CIDR.
2) Run:
   - `terraform -chdir=templates/infra init`
   - `terraform -chdir=templates/infra plan`
   - `terraform -chdir=templates/infra apply` only if the plan matches intent
3) Set generated public VPS IP in `templates/ansible/inventory.ini` for the root bootstrap run.
4) First Ansible run with:
   - `disable_root_login=false`
   - `bootstrap_public_ssh_cidr=<your public IP /32>`
5) Validate non-root SSH, then set:
   - inventory user to the admin user
   - `disable_root_login=true`
   - rerun `ansible-playbook -i inventory.ini site.yml`
   - prove root login is off as the admin user with `sudo sshd -T | grep -i permitrootlogin`, expecting `permitrootlogin no`; never prove it with a failed root login, because fail2ban bans the bootstrap `/32` after 5 failures in 10 minutes, and that address is the only allowed SSH source
6) Join Tailscale on the VPS:
   - run `sudo tailscale up --hostname=agent-vps`
   - approve the auth link
   - disable key expiry for the VPS in the Tailscale admin console; once SSH is Tailscale-only, an expired node key locks the operator out
   - run `sudo tailscale set --ssh=false` unless Tailscale SSH was explicitly chosen
   - validate SSH through the Tailscale IP before closing bootstrap SSH
   - for operator checks from a tailnet-connected controller, prefer `ssh <admin_user>@<tailscale-ip-or-hostname> 'sudo agent-vps status'`
7) Close bootstrap SSH to Tailscale-only in both layers:
   - Terraform: set `ssh_source_ips = ["100.64.0.0/10"]`, plan, and apply only if the plan changes the firewall in place
   - Ansible inventory: set `ansible_host` to the Tailscale IP
   - Ansible vars: set `bootstrap_public_ssh_cidr: ""` and `bootstrap_public_ssh_cidr_cleanup: "<old public IP /32>"`
   - rerun Ansible, then verify public SSH fails and OpenSSH over Tailscale still works
8) Optional remote desktop:
   - set `install_remote_desktop=true` and `install_nomachine=true`
   - rerun Ansible only after OpenSSH over Tailscale is stable
   - connect with NoMachine to the Tailscale IP/hostname using protocol `NX`, port `4000`, username `admin_user`, and the matching private key
   - do not add public firewall rules for VNC, RDP, NoMachine, or X11
9) Optional Firecrawl:
   - set `install_firecrawl=true` and `firecrawl_enable_service=true`
   - rerun Ansible
   - validate `curl -fsS http://127.0.0.1:3002`

## Operator commands on VPS
- `agent-vps status` - full local status check
- `agent-vps backup` - immediate backup
- `agent-vps backup-offbox` - upload and verify the latest backup off-box when enabled
- `agent-vps healthcheck` - status check plus Telegram transition alert when configured
- `agent-vps docker-cleanup` - prune unused Docker artifacts without pruning volumes
- `agent-vps timers` - list installed timers

## Optional Ubuntu Pro / ESM Apps
- Treat Ubuntu Pro / ESM Apps as a manual host-maintenance step, not an Ansible default or public template variable.
- Do not store the Ubuntu Pro token in Ansible vars, Terraform vars, committed files, shell exports, screenshots, support bundles, or chat logs.
- Recommended VPS-side flow:
  ```bash
  sudo agent-vps status
  sudo agent-vps backup

  read -rsp "Ubuntu Pro token: " UBUNTU_PRO_TOKEN; echo
  sudo pro attach "$UBUNTU_PRO_TOKEN"
  unset UBUNTU_PRO_TOKEN

  pro status
  sudo apt update
  sudo apt upgrade
  pro security-status --esm-apps
  sudo agent-vps status
  sudo agent-vps healthcheck

  if [ -f /var/run/reboot-required ]; then cat /var/run/reboot-required; else echo no; fi
  ```
- Reboot only when `/var/run/reboot-required` exists, then rerun `sudo agent-vps status` and `sudo agent-vps healthcheck`.
- If a token is pasted into chat, screenshots, logs, or support artifacts, tell Steven to revoke or rotate it in the Ubuntu Pro dashboard.

## Validation checklist
- Overall status:
  - `sudo agent-vps status`
  - `sudo agent-vps timers`
- Swap and disk:
  - `swapon --show`
  - `free -h`
  - `sysctl vm.swappiness`
  - `df -h /`
- Optional remote desktop when enabled:
  - `dpkg-query -W xfce4 nomachine`
  - `grep -E '^(DefaultDesktopCommand|AcceptedAuthenticationMethods)' /usr/NX/etc/node.cfg /usr/NX/etc/server.cfg`
  - connect with NoMachine over the VPS Tailscale IP/hostname on port `4000`
  - confirm no public GUI ports were added to UFW or the Hetzner firewall
- Port exposure sanity:
  - `sudo ss -ltnp | grep -E ':22 |:3002 ' || true`
  - expected: the optional Firecrawl port is loopback-bound; SSH is reachable only through allowed Tailscale/bootstrap sources.
- Firecrawl when enabled:
  - `curl -fsS http://127.0.0.1:3002`
  - `sudo docker compose --env-file /etc/firecrawl/firecrawl.env -f /opt/firecrawl/docker-compose.yml ps`
  - `curl -fsS -X POST http://127.0.0.1:3002/v1/scrape -H 'Content-Type: application/json' -d '{"url":"https://docs.firecrawl.dev","formats":["markdown"]}'`
- Backup and restore evidence:
  - `sudo agent-vps backup`
  - `sudo agent-vps backup-offbox` should report disabled until `vps_backup_offbox_enabled=true`; when enabled, it must upload and checksum-verify the archive. If the target is unavailable, it writes the retry-pending file and the next run retries that archive.
  - `sudo tar -tzf /var/backups/agent-vps/latest.tar.gz | grep -E '^(etc/agent-vps|etc/firecrawl)' | head`
- Terraform safety before infra changes:
  - run `hctf -chdir=templates/infra plan -input=false`
  - stop before apply if the plan replaces `hcloud_server.vps`

## Firecrawl private stack
- Use official Firecrawl self-host docs and upstream repo as source of truth:
  - `https://docs.firecrawl.dev/contributing/self-host`
  - `https://github.com/firecrawl/firecrawl`
- Current self-host runtime uses Redis, RabbitMQ, and NUQ on Postgres. Keep `POSTGRES_DB=postgres` with the upstream `nuq-postgres` image.
- Keep Firecrawl private:
  - host endpoint: `http://127.0.0.1:3002`
  - laptop tunnel: `ssh -N -L 3002:127.0.0.1:3002 agent-vps`
- Runtime layout:
  - compose: `/opt/firecrawl/docker-compose.yml`
  - env: `/etc/firecrawl/firecrawl.env` (secret-bearing; never commit)
- `agent-vps backup` includes `/etc/firecrawl` when present. Firecrawl Docker volumes are not included by default; use a cold volume backup if Firecrawl job history must survive a rebuild.
- The Firecrawl role is gated by `install_firecrawl`; service state is gated by `firecrawl_enable_service`.
- Redis, RabbitMQ, and Postgres remain on the private `firecrawl_backend` network; only the API port is published, on loopback.
- Env secrets are generated only when missing/placeholder and `firecrawl_auto_generate_secrets=true`.
- If API restarts with `relation "nuq.queue_*" does not exist`, ensure `POSTGRES_DB=postgres`; if this is a fresh failed init, recreate only Firecrawl volumes with `docker compose --env-file /etc/firecrawl/firecrawl.env -f /opt/firecrawl/docker-compose.yml down -v`, then `up -d`.

## Codex CLI Firecrawl access
- Keep Firecrawl hosted as its own private service stack under `/opt/firecrawl` and `/etc/firecrawl`; do not move it under `/home/<agent_user>` just so Codex CLI can use it.
- Codex CLI runs on the VPS host, so it can reach the private Firecrawl API through `http://127.0.0.1:3002` when Firecrawl is enabled.
- Preferred Codex integration is a local MCP server that points to the private host endpoint:
  ```bash
  codex mcp add firecrawl --env FIRECRAWL_API_URL=http://127.0.0.1:3002 -- npx -y firecrawl-mcp
  ```
- When `install_codex_cli=true`, the base role installs `bubblewrap`,
  `apparmor-profiles`, and `apparmor-utils`. On Ubuntu 24.04 it also loads the
  `bwrap-userns-restrict` AppArmor profile required by Codex's Linux sandbox.
- If Codex reports `bwrap: loopback: Failed RTM_NEWADDR: Operation not
  permitted`, first verify the AppArmor profile is installed and loaded; do not
  default to disabling `kernel.apparmor_restrict_unprivileged_userns` unless the
  official profile is unavailable or has been tried and failed.
- This adds user-local Codex config in `~/.codex/config.toml`; do not commit it or copy it into the public skill repo as account state.
- For a VPS workbench, keep `~/.codex/config.toml` host-specific and small:
  use `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"`,
  `sandbox_workspace_write.network_access = true`, and `writable_roots` limited
  to `/home/<agent_user>/repos`, `/home/<agent_user>/agent-workspaces`, and
  `/tmp`. Trust those concrete workbench paths, not the whole home directory.
- Do not copy a macOS Codex config directly to the VPS; rewrite Homebrew paths,
  `/Users/...` project paths, local AWS credential paths, and plugin lists for
  the Linux host.
- Be cautious with custom `default_permissions` filesystem profiles on the VPS.
  They can cause `codex sandbox linux` to fail with `error building bubblewrap
  command: Permission denied (os error 13)` on some CLI versions. If used, smoke
  test from both repo and agent-workspace directories before relying on them.
- Validate without exposing Firecrawl publicly:
  - `codex mcp list`
  - `command -v bwrap && bwrap --version`
  - `bwrap --unshare-user --unshare-net --ro-bind / / /bin/true`
  - `cd /home/<agent_user>/agent-workspaces && codex sandbox linux -- bash -lc 'pwd && echo sandbox_ok'`
  - `curl -fsS http://127.0.0.1:3002`
  - In an interactive Codex session, ask Codex to use the `firecrawl` MCP server to scrape a public test page.
- For non-interactive `codex exec`, MCP tool approval can cancel the tool call unless the run is interactive or explicitly configured to allow the call. Use bypass only for a controlled smoke test in an empty/safe workspace, never as the default operating mode.

## Codex CLI LangChain docs MCP access
- Add the official hosted LangChain docs MCP server for LangChain, LangGraph, and LangSmith documentation lookups:
  ```bash
  codex mcp add langchain-docs --url https://docs.langchain.com/mcp
  ```
- This writes user-local Codex state in `~/.codex/config.toml`; treat it as local account state, not tracked deployment config.
- If `codex mcp add` is unavailable, the equivalent Codex config entry is:
  ```toml
  [mcp_servers.langchain-docs]
  url = "https://docs.langchain.com/mcp"
  ```
- Prefer this official docs MCP for documentation lookups. Do not install third-party LangChain code-search MCP packages unless the operator explicitly wants their login/credit model and has reviewed the package.
- Validate with `codex mcp list` and an interactive Codex prompt such as: "Use the LangChain docs MCP to check the current LangGraph MCP endpoint guidance."

## Restore
For recovery from a fresh VPS, read `references/restore.md`.
