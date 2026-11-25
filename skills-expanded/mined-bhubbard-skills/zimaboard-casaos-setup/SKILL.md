---
name: zimaboard-casaos-setup
description: A guide for initializing a ZimaBoard and installing CasaOS to create a low-power, user-friendly personal cloud and home server.
---

# ZimaBoard & CasaOS Initial Setup

The ZimaBoard is a low-power x86 single-board server designed for makers and homelab enthusiasts. Paired with CasaOS—a lightweight, Docker-based personal cloud operating system—it becomes a powerful, easy-to-manage home server.

## 1. Operating System Foundation
While CasaOS acts like an operating system, it actually runs on top of a standard Linux distribution.
1. **Base OS**: ZimaBoards come pre-installed with Debian or CasaOS. If you are starting fresh or want to upgrade the underlying OS, install the latest version of **Debian** (recommended) or **Ubuntu Server**.
2. **Access**: Connect the ZimaBoard to your router via Ethernet and access it via SSH (`ssh root@<zimaboard-ip>`).

## 2. Installing CasaOS
CasaOS can be installed with a single command. It will automatically install Docker and set up the web dashboard.
```bash
curl -fsSL https://get.casaos.io | sudo bash
```
*Note: This process takes a few minutes depending on your internet connection.*

## 3. Accessing the Dashboard
Once installed, open a web browser and navigate to the IP address of your ZimaBoard (e.g., `http://192.168.1.100`).
- Create your initial admin account.
- The dashboard will display system resource widgets (CPU, RAM, Storage).

## 4. Storage Expansion
The ZimaBoard features dual SATA ports and a PCIe slot.
- **SATA Drives**: Connect 2.5" SSDs or 3.5" HDDs (requires an external power source or the official Y-cable).
- **Storage Manager**: Use the built-in CasaOS "Files" app and Storage Manager to format and mount new drives. Choose `ext4` or `btrfs` for best compatibility.

## 5. Next Steps
- Open the **App Store** to install one-click Docker applications like Nextcloud, Pi-hole, or Jellyfin.
