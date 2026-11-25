---
name: ficc-setup
description: Help install, connect, and qualify a FICC controller for local or remote operation, including first node enrollment. Use for FICC setup and compatibility checks, not general coding-agent installation.
---

# Set up FICC

This skill describes FICC v0.2.5-stable. Check the selected binary's `--version`
and command help. For another version, inspect that release's manuals before
changing state; do not assume that the latest online manual matches the install.

## Select the installation

Identify the coding-agent execution host, FICC controller, and managed nodes.
They can be different machines. Select the controller account, absolute FICC
binary, state directory, launcher configuration if present, and intended project.
Resolve missing target information before acting on a machine. Installing this
skill does not install FICC, create credentials, or approve SSH aliases.

The CLI below uses the controller owner's private socket. Use it only with
existing authority to act as that account. A project-scoped browser session is
not permission to switch to the owner CLI. Existing task authority persists;
ask only for genuinely missing scope or permission.

```sh
ficc --version
ficc status --launcher-config /home/operator/.config/ficc/launcher.json
ficc nodes --state-dir /home/operator/.local/state/ficc
```

`status` checks a launcher, while `nodes` needs the selected running controller.
A missing launcher does not establish that no foreground controller exists.
Do not start another controller merely because a status check fails.

## Install or demonstrate

For a new installation, use the verified binary or source procedure in the
[v0.2.5 Linux packages](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/releases.md)
or [installation guide](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/install.md).
Preserve existing state and launcher settings during an update. Binary packages
bundle Python for FICC; do not assume they supply a public Python interpreter
for unrelated helpers. Do not run downloaded scripts before establishing their
source and the user's intended installation scope.

For an explicitly requested demonstration, select a fresh state directory and
an available port distinct from live service settings:

```sh
ficc serve --demo --state-dir /tmp/ficc-harness-demo --port 8187
# In a second terminal on the same machine:
ficc open --state-dir /tmp/ficc-harness-demo
```

Stop this foreground process when finished. Demo mode cannot prove live SSH,
enrollment, workloads, or mutation behavior. `open --print-url` produces a
credential-bearing URL; do not capture it in agent output or share it.

## Connect a managed node

Establish key authentication and independently verify the node's SSH host key.
Use the controller's existing trusted alias and approved profile. A first
foreground setup can select it with `ficc serve --profile compute-01` plus the
intended state and optional `--ssh-config`. Do not replace an existing service's
profile list or launch a competing controller.

```sh
ficc enroll --state-dir /home/operator/.local/state/ficc \
  --profile compute-01 --name 'Compute 01'
```

This shows a preview. Check its machine, account and fingerprint against the
independent trusted value. To commit an authorized enrollment, repeat the command
with `--fingerprint VERIFIED_FINGERPRINT` and add `--install-helper` only when
installation is required and covered by the task. Then inspect `ficc nodes` and
refresh the selected enrolled ID. A changed host key needs investigation, not
disabled verification. Job requirements are stricter than observation requirements.

For normal desktop startup, stop the foreground process and install the launcher
with the same state, profiles, port and SSH configuration. Use the released
[operation guide](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/operations.md)
for `install-launcher`; it changes service configuration. Do not enable autostart
unless requested.

## Remote administration

An agent on a laptop can run the controller's installed CLI over approved SSH,
or the agent can run on the controller itself. Preserve host-key verification;
use bounded connection checks. A managed-node SSH alias is not necessarily the
controller. Keep private keys, credentials and controller state on their owners.

Remote browser use requires FICC's configured HTTPS gateway, verified TLS,
individual identity mapping and project membership. Do not tunnel or publish
the local-mode listener. Follow the
[remote access guide](https://github.com/Federated-Industrial-Laboratories/ficc/blob/v0.2.5-stable/docs/remote-access.md)
when remote-mode deployment itself is authorized. Selecting a remote role does
not authorize installing identity services or changing firewall rules.

Report the selected target, observed version, working access method, and any
unavailable capability. Distinguish a configured connection from successful
enrollment and a demo result from a live check.
