---
name: tart
description: Manage macOS and Linux virtual machines using the Tart CLI (tart.run). Use this skill whenever the user wants to create, run, stop, configure, or manage VMs on Apple Silicon — including pulling pre-built images, SSH into VMs, executing commands inside guests, sharing directories, importing/exporting VMs, or adjusting CPU/memory/disk. Trigger when the user mentions Tart, VMs, virtual machines, guest OS, or wants to spin up macOS or Linux environments locally. Also trigger when the user is setting up CI runners, testing across OS versions, or needs an isolated macOS/Linux environment.
---

# Tart VM Management

Manage macOS and Linux virtual machines on Apple Silicon using the [Tart CLI](https://tart.run) and Apple's Virtualization.framework.

## Quick Reference

| Task | Command |
|------|---------|
| List VMs | `tart list` |
| Pull an image | `tart clone ghcr.io/cirruslabs/<image>:latest <name>` |
| Run a VM | `tart run <name>` |
| Run headless | `tart run --no-graphics <name>` |
| Get VM IP | `tart ip <name> --wait 30` |
| SSH in | `ssh admin@$(tart ip <name>)` |
| Run command in guest | `tart exec <name> -- <command>` |
| Stop a VM | `tart stop <name>` |
| Suspend (save state) | `tart suspend <name>` |
| Configure VM | `tart set <name> --cpu 4 --memory 8192` |
| Delete a VM | `tart delete <name>` |

## Pre-built Images

Cirrus Labs provides ready-to-use images on GitHub Container Registry. Pull them with `tart clone`.

### macOS Images
| Image | What's included |
|-------|-----------------|
| `ghcr.io/cirruslabs/macos-tahoe-base:latest` | macOS Tahoe, minimal (~26 GB) |
| `ghcr.io/cirruslabs/macos-sequoia-base:latest` | macOS Sequoia, minimal |
| `ghcr.io/cirruslabs/macos-sequoia-xcode:latest` | macOS Sequoia + Xcode (~45 GB) |
| `ghcr.io/cirruslabs/macos-sonoma-base:latest` | macOS Sonoma, minimal |
| `ghcr.io/cirruslabs/macos-sonoma-xcode:latest` | macOS Sonoma + Xcode |

### Linux Images
| Image | What's included |
|-------|-----------------|
| `ghcr.io/cirruslabs/ubuntu:latest` | Ubuntu (~1 GB, quick to test) |
| `ghcr.io/cirruslabs/fedora:latest` | Fedora |

**Default credentials for all Cirrus Labs images: `admin` / `admin`**

### Creating from Scratch
```bash
# macOS VM from the latest IPSW
tart create my-mac --from-ipsw latest --disk-size 80

# Empty Linux VM
tart create my-linux --linux --disk-size 30
```

## Running VMs

```bash
# GUI window (default)
tart run my-vm

# Headless — useful for CI or when accessing via SSH only
tart run --no-graphics my-vm

# With a shared directory (appears at /Volumes/My Shared Files in macOS guest)
tart run --dir ~/projects my-vm

# With a named shared directory
tart run --dir="code:~/projects" --dir="data:~/data:ro" my-vm

# Mount an ISO or additional disk
tart run --disk ubuntu.iso:ro my-vm

# Enable nested virtualization
tart run --nested my-vm
```

### Suspend and Resume

To suspend a VM (saves full running state to disk for instant resume), it must have been started with `--suspendable`:

```bash
tart run --suspendable my-vm    # start with suspend support
tart suspend my-vm              # save state and stop
tart run my-vm                  # resumes from suspended state
```

The `--suspendable` flag disables audio and entropy devices to make state serialization possible. Suspended state is local only — it cannot be exported.

## Accessing the Guest

### SSH
```bash
# Wait up to 30s for the VM to boot and get an IP
tart ip my-vm --wait 30

# SSH in (password: admin for cirruslabs images)
ssh admin@$(tart ip my-vm)
```

### tart exec (no SSH needed)
Requires the Tart Guest Agent (pre-installed on all non-vanilla Cirrus Labs images):
```bash
tart exec my-vm -- uname -a
tart exec my-vm -- brew install node
tart exec my-vm -- ls /Users/admin/Desktop
```

## Configuring VMs

Use `tart set` when the VM is stopped:

```bash
tart set my-vm --cpu 4 --memory 8192            # 4 cores, 8 GB RAM
tart set my-vm --disk-size 100                   # grow disk to 100 GB (cannot shrink)
tart set my-vm --display 1920x1080px             # set display resolution
tart set my-vm --random-mac                      # new MAC (useful for clones to avoid DHCP conflicts)
```

View current config:
```bash
tart get my-vm              # text format
tart get my-vm --format json # JSON format
```

## Cloning and Snapshots

Clones use APFS copy-on-write, so they're fast and space-efficient:

```bash
tart clone my-vm my-vm-snapshot          # local clone (instant, CoW)
tart clone ghcr.io/cirruslabs/ubuntu:latest my-ubuntu  # pull from registry
```

## Import / Export

Export creates a compressed `.tvm` file containing the disk image and config (not running state):

```bash
tart export my-vm ~/backups/my-vm.tvm    # export
tart import ~/backups/my-vm.tvm my-vm    # import on another machine
```

## Networking

By default, VMs use shared (NAT) networking via `vmnet`.

```bash
# Bridged networking (VM gets an IP on your local network)
tart run --net-bridged=en0 my-vm

# Softnet (better isolation, prevents DHCP exhaustion in CI)
tart run --net-softnet my-vm

# Expose guest ports to the network via Softnet
tart run --net-softnet --net-softnet-expose 2222:22,8080:80 my-vm

# Host-only networking
tart run --net-host my-vm
```

## Housekeeping

```bash
tart list                              # all VMs with disk usage
tart list --format json                # JSON output
tart list --source local               # only local VMs
tart rename old-name new-name          # rename a VM
tart delete my-vm                      # delete a VM
tart prune                             # clean OCI/IPSW caches
tart prune --older-than 7              # caches unused for 7+ days
tart prune --entries vms --older-than 30  # delete VMs unused for 30+ days
```

## CI / GitHub Actions Usage

Tart pairs well with [Cirrus Runners](https://github.com/cirruslabs/cirrus-cli) for self-hosted GitHub Actions on Apple Silicon. The typical pattern:

1. Pull a base image with dev tools pre-installed
2. Clone it per-job (CoW makes this fast)
3. Run the job headless with `tart run --no-graphics`
4. Use `tart exec` or SSH to run commands inside the VM
5. Delete the clone when done

## Tips

- Use `--wait 30` with `tart ip` to handle boot delays
- For DHCP exhaustion on machines running many VMs, reduce lease time: `sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.InternetSharing.default.plist bootpd -dict DHCPLeaseTimeSecs -int 600`
- Clone instead of pulling again — APFS CoW makes local clones nearly free
- On macOS Tahoe+, use `--disk-format asif` with `tart create` for better disk performance
- `tart list --format json` is useful for scripting
