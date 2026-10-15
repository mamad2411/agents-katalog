---
name: sdw-build-install
description: Build the securedrop-workstation RPM from the work VM and install it in dom0
---

To build and install the RPM in dom0:

```bash
echo 'source ~/sdw.env && cd ~/securedrop-workstation && make clone 2>&1' | qrexec-client-vm dom0 local.RunInDom0
```

This builds the RPM on the work VM, clones it to dom0, and leaves it at:
`~/securedrop-workstation/rpm-build/RPMS/noarch/securedrop-workstation-dom0-config-<version>.fc41.noarch.rpm`

To install it (use `rpm -Uvh --force` to reinstall the same version):

```bash
echo 'source ~/sdw.env && sudo rpm -Uvh --force ~/securedrop-workstation/rpm-build/RPMS/noarch/securedrop-workstation-dom0-config-*.fc41.noarch.rpm 2>&1' | qrexec-client-vm dom0 local.RunInDom0
```

`dnf install -y` will no-op if the same version is already installed. `dnf reinstall` may fail if the Qubes update repo cache is missing. Use `rpm -Uvh --force` to reliably install regardless.

To apply the Salt states after installing:

```bash
echo 'source ~/sdw.env && sdw-admin --apply 2>&1' | qrexec-client-vm dom0 local.RunInDom0
```

Do not use `make dev` — it runs `bootstrap-keyring.py` which calls `qubes-dom0-update` and will fail if another update process is running.

Notes:
- `~/sdw.env` must be sourced — it sets the dev VM name (not `sd-dev` by default)
- `make clone` does both: builds the RPM inside a container on the work VM, then rsync/copies it to dom0
- Use `make clone-norpm` to skip the RPM build and only sync the repo
