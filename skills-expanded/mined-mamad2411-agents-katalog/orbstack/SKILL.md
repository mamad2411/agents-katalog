---
name: orbstack
description: "Configure OrbStack containers and Linux environments on macOS; troubleshoot shared files, emulation, and local networking."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["orbstack", "docker-macos", "hypervisor-framework", "virtiofs", "linux-vms", "rosetta2-emulation", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# OrbStack macOS Fast Docker & Linux VM Runtime AI Skill Guide (Claude)

## Overview & Engine Architecture
OrbStack is a high-performance, lightweight replacement for Docker Desktop and virtual machine hypervisors on macOS. Engineered natively in Swift, it leverages Apple's **`Hypervisor.framework`**, custom micro-Linux kernels (booting in $<2\text{s}$), **VirtioFS** near-native host filesystem sharing, and **Rosetta 2 translation for x86_64 Linux containers** on Apple Silicon. OrbStack exposes seamless domain routing (**`*.orb.local`**), native UNIX domain sockets (**`~/.orbstack/run/docker.sock`**), and an integrated Linux VM manager (**`orb` CLI**). Claude operates as a Principal DevOps Architect and Containerization Specialist, specializing in **Docker context migration**, **Rosetta 2 multi-arch emulation**, **VirtioFS I/O tuning**, and **OrbStack Linux VM automation**.

### OrbStack Virtualization & Networking Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 OrbStack Architecture                       │
│                                                             │
│  macOS Host & Management Layer                              │
│  ├── Native Swift UI (`OrbStack.app` / Hypervisor.framework)│
│  ├── Docker CLI Context (`~/.orbstack/run/docker.sock`)     │
│  └── Integrated `orb` CLI (VM Creation, Shell, Forwarding)  │
│                                                             │
│  Virtualization & Storage Engine                            │
│  ├── Micro-Linux Kernel (Instant Boot, Dynamic CPU/RAM Allocation│
│  ├── VirtioFS Bi-Directional High-Speed Volume Mounts       │
│  └── Rosetta 2 x86_64 Linux Binary Emulation Pipeline       │
│                                                             │
│  Zero-Config Networking & Routing                           │
│  ├── Direct Host-to-Container IP Addressing (Bridged Stack) │
│  └── Automatic mDNS Domain Resolver (`http://<container>.orb.local`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Docker Context & Daemon Migration**: Configure `DOCKER_HOST` and Docker contexts to seamlessly switch from Docker Desktop / Colima to OrbStack (`docker context use orbstack`).
2. **Multi-Architecture Emulation Management**: Diagnose and enable Rosetta 2 binary translation (`softwareupdate --install-rosetta`) for fast x86_64 container execution without QEMU slowdowns.
3. **OrbStack Linux VM Orchestration**: Script automated provisioning of headless Linux environments (`orb create ubuntu:24.04`, `orb create archlinux`, `orb shell`) with shared home directories.
4. **Local Network & Domain Resolution**: Configure and debug `.orb.local` zero-config domain routing and port forwarding to local macOS applications.

---

## Production Bash Automation: Automated OrbStack VM Provisioner & Health Auditor

Save this script as `provision_orb_vm.sh` and execute via `bash provision_orb_vm.sh`:

```bash
#!/usr/bin/env bash
# ==============================================================================
# OrbStack Automated Linux VM Provisioning & Docker Health Pipeline
# Verifies OrbStack daemon, configures Docker context, and provisions micro-VMs.
# ==============================================================================
set -euo pipefail

VM_NAME="dev-sandbox"
VM_DISTRO="ubuntu:24.04"

echo "--- [ORBSTACK SYSTEM & DOCKER AUDIT] ---"

# 1. Verify OrbStack CLI is Available
if ! command -v orb &> /dev/null; then
    echo "🚨 Error: 'orb' CLI tool not found. Install via: brew install orbstack"
    exit 1
fi

# 2. Check Docker Socket Status and Context
echo "Checking OrbStack Docker Socket..."
ORB_SOCKET="$HOME/.orbstack/run/docker.sock"

if [ -S "$ORB_SOCKET" ]; then
    echo "✅ OrbStack Docker socket detected at: $ORB_SOCKET"
    export DOCKER_HOST="unix://$ORB_SOCKET"
    docker context use orbstack 2>/dev/null || true
else
    echo "🚨 Error: OrbStack Docker socket not running. Launch OrbStack.app."
    exit 1
fi

# 3. Display Running Docker Containers
echo -e "\n--- [ACTIVE DOCKER CONTAINERS] ---"
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# 4. Provision or Start OrbStack Linux Micro-VM
echo -e "\n--- [PROVISIONING LINUX VM: $VM_NAME ($VM_DISTRO)] ---"
if orb list | grep -q "$VM_NAME"; then
    echo "VM '$VM_NAME' already exists. Starting..."
    orb start "$VM_NAME"
else
    echo "Creating new $VM_DISTRO micro-VM..."
    orb create "$VM_DISTRO" "$VM_NAME"
fi

# 5. Execute Command Inside VM
echo "Running system verification inside VM..."
orb -m "$VM_NAME" uname -a
orb -m "$VM_NAME" lsb_release -a || true

echo -e "\n✅ OrbStack environment verified and ready for deployment!"
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Cannot connect to the Docker daemon at unix:///var/run/docker.sock`** | `DOCKER_HOST` environment variable pointing to legacy Docker Desktop path. | 1. In terminal, run: `docker context use orbstack`.<br>2. Or add to `~/.zshrc`: `export DOCKER_HOST="unix://$HOME/.orbstack/run/docker.sock"`. |
| **x86_64 Container Crashes on Apple Silicon: `Exec format error`** | macOS Rosetta 2 translation layer not installed or Rosetta emulation disabled in OrbStack. | 1. In macOS Terminal, run: `softwareupdate --install-rosetta --agree-to-license`.<br>2. In OrbStack Settings $\rightarrow$ **Compatibility**, enable **Use Rosetta for x86_64 emulation**. |
| **`http://app.orb.local` Fails to Resolve in Browser** | macOS mDNSResponder local DNS cache stale or VPN client intercepting local `.local` queries. | 1. Flush macOS DNS cache: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.<br>2. Add VPN bypass rule for `.orb.local`. |
| **VirtioFS File Permission Error in Container** | Container running as non-root user unable to write to macOS host folder mapped with mismatched UID. | In `docker-compose.yml`, set `user: "${UID}:${GID}"` matching your macOS user ID (`id -u`). |

---

## Command Line Syntax & `orb` CLI Recipes

```bash
# 1. Switch Active Docker CLI Context to OrbStack
docker context use orbstack

# 2. Create and Shell into an Arch Linux Micro-VM
orb create archlinux arch-box
orb shell arch-box

# 3. Stop All Running VMs and Containers
orb stop --all
```

### Essential File Locations
- **Docker UNIX Socket**: `~/.orbstack/run/docker.sock`
- **OrbStack VM Configs**: `~/.orbstack/data/`
- **Application Preferences**: `~/Library/Preferences/dev.kdrag0n.MacVirt.plist`

---

## Agent Operational Directive
> **MANDATORY**: Ensure `docker context use orbstack` is executed when migrating from Docker Desktop. Verify that Rosetta 2 is installed (`softwareupdate --install-rosetta`) when running AMD64/x86_64 container images on Apple Silicon.
