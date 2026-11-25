---
name: zimaboard-pfsense-router
description: Configuring the ZimaBoard as a dedicated hardware firewall and software router using pfSense or OPNsense.
---

# ZimaBoard as a Router & Firewall

The ZimaBoard's dual Gigabit Ethernet ports make it an ideal, low-power hardware appliance for routing and network security. By replacing standard consumer routers with open-source software like pfSense or OPNsense, you unlock enterprise-level network control.

## 1. Hardware Requirements
- **ZimaBoard**: Any model (216, 432, or 832).
- **Network Interfaces**:
  - `eth0`: Connects to your ISP Modem (WAN).
  - `eth1`: Connects to a network switch or Wi-Fi Access Point (LAN).

## 2. Flashing the OS
CasaOS is not suitable for routing. You must flash a dedicated firewall OS.
1. Download the `pfSense CE` or `OPNsense` AMD64/x86 image.
2. Flash the image to a USB drive using BalenaEtcher or Rufus.
3. Plug the USB into the ZimaBoard, connect a Mini-DisplayPort monitor and keyboard, and boot from the USB.
4. Follow the installer to write the OS to the internal eMMC storage.

## 3. Initial Configuration
1. **Assign Interfaces**: During setup, the installer will ask you to assign WAN and LAN interfaces. 
   - Plug a live cable into one port to identify its MAC address. Assign this as WAN.
2. **Access the WebGUI**: Connect a laptop to the LAN port and navigate to the default gateway (usually `192.168.1.1`).
3. **Setup Wizard**: Complete the initial setup wizard to configure DNS, timezone, and WAN DHCP settings.

## 4. Advanced Networking
With pfSense/OPNsense running on the ZimaBoard, you can implement:
- **VLANs**: Isolate IoT devices from your primary network using a managed switch.
- **VPN Server**: Host WireGuard or OpenVPN to securely access your home network remotely.
- **Traffic Shaping / QoS**: Prioritize gaming or video call traffic over bulk downloads.
- **Network-Wide Ad Blocking**: Use pfBlockerNG to filter DNS queries directly at the router level.
