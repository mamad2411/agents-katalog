---
name: remote-setup
description: Use when setting up Niles phone access through a Tailscale relay, including Caddy, host tags, shared push and Wake-on-LAN. Fresh installs only; not for migrating existing remote deployments or configuring project setups.
---
# Remote setup

Set up an always-on relay that also runs Niles. The request path is phone → Tailscale
Serve HTTPS → localhost Caddy → each Niles host's tailnet IPv4 listener. Serve cannot
proxy directly to other tailnet IPs: its dialer bypasses Tailscale routes. No CORS,
Funnel, public listeners or extra authentication headers are needed.

## Inventory before changing anything

1. Collect the relay and host SSH/access details, OS users running Niles, host display
   names and routing IDs for the manifest, permitted phone users, and whether push/WoL
   are wanted. For push collect a mailto: or https: contact URI. Include the relay as
   a host. For WoL collect target MACs and LAN broadcasts from the operator/network.
   Ask only for information you cannot discover through authorized access.
2. Read the deployment's existing config and service state. Inspect
   `tailscale serve status --json`, Funnel status, Caddy configuration and listeners,
   `~/.niles/config.yaml`, and Niles user services on every machine.
   Existing remote deployments need a separate migration plan: stop and report the
   conflict instead of overwriting services, Serve mounts, push keys or tailnet policy.
   An occupied Serve root, chosen port or service path is also a conflict, even if unrelated.
   Preserve unrelated config. Do not use `tailscale serve reset`.
   Existing path/Unix-socket mounts gate the whole Serve config: even step 13's HTTP
   proxy may need sudo. Preserve those mounts and report missing privileges.
   [Tailscale #22117](https://github.com/tailscale/tailscale/pull/22117) makes root
   mandatory for configs containing these mounts; operator privileges no longer suffice.
3. Verify `type -a niles tailscale`, `niles --version`, `niles remote --help`,
   `tailscale version --daemon --json`, `tailscale status --json`, and
   `tailscale ip -4` on each machine. Require a remote-enabled Niles binary, matching
   Tailscale CLI/daemon versions >=1.96.2, a running authenticated daemon, and stable
   tailnet IPv4 addresses. Record the relay's DNS name, Self.ID and IPv4; confirm its
   stable node ID with `tailscale whois --json <relay-tailnet-ip>` → Node.StableID.
   Do not use a node key, machine key, DNS name or IP as `remote.relay_node`.
4. On the relay enable MagicDNS and HTTPS certificates in the tailnet DNS settings.
   Verify its DNS name is listed in CertDomains. The phone joins the same tailnet
   as a user-owned device: tagged clients have no Serve login header.
   Use open-source Homebrew tailscaled on macOS. Check the LaunchDaemon's PATH
   includes the directory containing the tailscale CLI; Homebrew service regeneration
   can undo this. Keep this PATH check until the relay includes Tailscale #22117,
   which removes the daemon's `sudo --list` check.
   Check Tailscale operator privileges for the service account; if
   needed, give the operator the exact `sudo tailscale set --operator=<user>` fix.
   Report privileged prerequisites that authorized access cannot complete.
5. Install matching remote-enabled Niles binaries on all hosts and built PWA assets
   on the relay. Use the release's `niles-web.tar.gz` with
   `cargo install niles --locked --version <version> --features remote`, or a trusted
   checkout's `scripts/install-remote.sh` (Node 24, pnpm 10.8.1, Rust 1.89+, OpenSSL).
   Confirm `index.html` is at the asset root. Serve only this dedicated built directory
   plus hosts.json; never serve a checkout, home directory or `~/.niles/`.
   Install Caddy on the relay and record `caddy version`.

## Restrict the tailnet

6. Merge tags and grants into the existing tailnet policy. Substitute actual owners
   and users; this fragment is not a replacement policy:

   ```json
   {
     "tagOwners": {
       "tag:niles-relay": ["autogroup:admin"],
       "tag:niles-host": ["autogroup:admin"]
     },
     "grants": [
       {"src": ["you@example.com"], "dst": ["tag:niles-relay"], "ip": ["tcp:443"]},
       {"src": ["tag:niles-relay"], "dst": ["tag:niles-host"], "ip": ["tcp:8765"]},
       {"src": ["tag:niles-relay"], "dst": ["tag:niles-relay"], "ip": ["tcp:8765"]}
     ]
   }
   ```

   Assign only the relay tag to the relay node; assign the host tag to other hosts.
   The third grant lets the relay reach its own backend. Adapt ports if needed.
   Inspect all existing grants/ACLs: permissions are additive, so a broad allow rule defeats these restrictions. Preserve needed
   SSH/admin access; verify policy tests permit chosen phone users on relay:443 and
   relay on every backend port, and deny unwanted users/devices. Apply tags through
   the admin console or `tailscale set --advertise-tags=...`, preserving existing tags.
   Recheck the relay's stable ID after tagging. Tags control network reachability;
   the backend additionally pins one exact relay node, not every node with its tag.
   Tailnet policy reference: https://tailscale.com/docs/reference/syntax/policy-file

## Configure hosts and push

7. Merge this into each host user's `~/.niles/config.yaml`, including the relay:

   ```yaml
   remote:
     relay_node: nYOUR_RELAY_STABLE_NODE_ID
   ```

   `remote.allowed_users` no longer exists. Every login admitted by Serve and the
   tailnet policy has shell authority on every configured host. The backend binds
   `tailscale ip -4`, not localhost; Caddy must connect to that address even for the
   relay's own backend so WhoIs sees the relay node.
8. For push, generate one key with
   `niles remote init --subject mailto:you@example.com` on the relay as the Niles user.
   Securely copy that same `~/.niles/remote/vapid.json` to every host user's same path.
   Keep its parent directory mode 0700 and file mode 0600, owned by the service user.
   Compare files without printing private contents. Do not generate independent keys,
   overwrite an existing key, put keys in the web root, or copy subscriptions.
   If push is declined, skip initialization and report push as unconfigured.
9. If WoL is requested, keep the relay awake on the targets' LAN. Enable WoL in
   each target's firmware and OS, determine the correct NIC MAC and subnet broadcast, and add this
   server-side map only on the relay, alongside its relay_node:

   ```yaml
     wake_hosts:
       desktop:
         mac: "01:23:45:67:89:ab"
         broadcast: 192.168.1.255
   ```

   IDs must match hosts.json. Invalid targets stop backend startup. No MAC or
   broadcast address belongs in hosts.json, JavaScript or a phone request.
   If a target cannot support WoL, leave it out and report that limitation.
10. Create a user service for `niles remote --port 8765` on each host, using the
    absolute binary path and an explicit PATH containing tailscale, tmux and the
    agent CLIs. Preserve the user's HOME and credential environment; shell startup
    files are not loaded. On Linux use `~/.config/systemd/user/niles-remote.service`,
    with After=network-online.target, Restart=on-failure, RestartSec=5 and
    WantedBy=default.target, then daemon-reload and
    enable --now; enable user lingering if it must survive logout. On macOS use
    `~/Library/LaunchAgents/dev.niles.remote.plist`, Label=dev.niles.remote,
    ProgramArguments as an array, RunAtLoad=true, KeepAlive=true and stdout/stderr logs,
    then `launchctl bootstrap gui/<uid> <plist>`. Escape paths for the service format;
    validate with systemd-analyze verify or plutil -lint before loading.
    Create log directories first. Check startup logs and listener address. Restart after config or key changes.

## Configure the relay origin

11. Write hosts.json in the built PWA root. IDs are unique, match
    `[A-Za-z0-9][A-Za-z0-9_-]*`, and stay stable; names are nonempty display text.
    Choose lowercase IDs: Caddy path matching cannot distinguish IDs by case alone.
    Example (replace with the inventory):

    ```json
    {"hosts":[{"id":"relay","name":"Relay"},{"id":"desktop","name":"Desktop"}]}
    ```

12. Write a dedicated Caddyfile outside the web root, e.g.
    `~/.config/niles/Caddyfile`. Replace example IPs with the recorded tailnet IPv4s,
    and extend one explicit handle_path per manifest host. NILES_WEB_DIR must be an
    absolute path to the built PWA root, set in Caddy's service environment:

    ```caddyfile
    {
        admin off
        auto_https off
    }
    http://127.0.0.1:8080 {
        bind 127.0.0.1
        handle /api/hosts/*/wake {
            reverse_proxy 100.64.0.1:8765
        }
        handle_path /h/relay/* {
            reverse_proxy 100.64.0.1:8765
        }
        handle_path /h/desktop/* {
            reverse_proxy 100.64.0.2:8765
        }
        @unknown path /api /api/* /h /h/*
        handle @unknown {
            respond 404
        }
        handle {
            root * "{$NILES_WEB_DIR}"
            header /hosts.json Cache-Control no-store
            file_server
        }
    }
    ```

    handle_path strips /h/<id>, retaining /api/... and query strings. The wake route
    retains its full path and always targets the relay. Caddy preserves Serve's
    Tailscale-User-Login header by default; do not synthesize or append an identity.
    Caddy streams text/event-stream automatically. Use its normal HTTP transport,
    not a userspace Tailscale transport. Reference:
    https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
13. With NILES_WEB_DIR set, run `caddy validate --config <Caddyfile> --adapter caddyfile`.
    Install a separate Caddy service as the relay user, with absolute binary/config
    paths and that environment, using the same OS service manager as step 10.
    Check that port 8080 listens only on 127.0.0.1. Start Caddy before Serve.
    Run `tailscale serve --bg --https=443 http://127.0.0.1:8080` as the configured
    operator. Check Serve status and confirm Funnel is disabled. Serve owns TLS and
    strips forged identity headers; Caddy is reachable only locally.
    Reference: https://tailscale.com/docs/features/tailscale-serve

## Verify and hand back

14. From an allowed user-owned tailnet device, require 200 HTML at the relay HTTPS
    root and a valid, noncached hosts.json. Fetch every `/h/<id>/api/sessions` and
    `/h/<id>/api/projects`; require 200 JSON with api_version=1, the corresponding
    arrays and Cache-Control: no-store. Check an SSE feed
    emits its initial snapshot promptly. Confirm an unknown /h/ ID returns 404.
    A direct request to a backend from a different tailnet node, even with a forged
    Tailscale-User-Login, must be denied by policy or return 403. Also test an unwanted
    user cannot access relay HTTPS. Do not treat local spoofed-header curls as proof
    of end-to-end identity. On failures inspect service logs, policy and proxy paths;
    stop and report the failed layer rather than claiming installation succeeded.
15. Open the relay URL on the phone, send a harmless message and verify it at the desk.
    Install/Add to Home Screen (iOS push requires 16.4+ and the installed app). With all
    hosts awake and push configured, Enable notifications must register one shared
    subscription through every host; fix any named failure and retry. Check each public VAPID key matches,
    trigger a notification per host, and confirm it opens the correct host/session.
    Rerun registration after adding hosts. Opening notifications needs Tailscale.
16. If WoL is configured, test `POST /api/hosts/desktop/wake` through relay HTTPS with
    Content-Type: application/json and body `null`; require 204, then check actual
    wake/reachability and the phone's asleep-host Wake button. A sent packet is not
    proof of waking; unknown IDs return 404. Never accept a phone-supplied destination.
17. Record exactly which mounts, files and services this run created. Report the relay
    URL, host/route inventory, changed files and policy, service/log
    locations, restart commands, verification results and anything untested. For
    recovery remove only files/services and the Serve mount created in this run
    (`tailscale serve --bg --https=443 --set-path=/ off`), after rechecking ownership;
    preserve keys, config and
    unrelated mounts. Upgrade binary and PWA together and close/reopen app windows.
