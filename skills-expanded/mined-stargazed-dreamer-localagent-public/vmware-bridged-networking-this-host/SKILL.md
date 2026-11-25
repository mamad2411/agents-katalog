---
name: vmware-bridged-networking-this-host
description: 在本机（Windows 真机）配置 VMware Workstation 虚拟机网络：桥接到唯一可用的物理网卡、收敛 VMnet0 的自动桥接、以及澄清「桥接不改变公网出口 IP」这个最常见的误解。当用户问「虚拟机怎么桥接 / VM 上不了网 / 虚拟机要独立 IP / 想避开按公网 IP 的风控 / vmnetcfg / vmware_bridge」时使用。含 2026-08-30 实测的网卡白名单与注册表判据。
agent_created: true
task_type: daily.vmware_bridged_networking_this_host
---

# 本机 VMware 桥接网络（2026-08-30 实测）

## 1. 环境

- Workstation **16.2.3**，装在 `<data_drive>:/<apps_root>/VMware/`（`vmnetcfg.exe` / `vmrun.exe` 都在；以注册表 `HKLM:\SOFTWARE\WOW6432Node\VMware, Inc.\VMware Workstation` 的 InstallPath 为准）。
- 虚拟机目录 `<data_drive>:/<vm_store>/`（Win10 x64 / ubuntu-22.04 / RHEL8 ×2）。**别全盘搜 .vmx**，直接问用户。
- 已改：Win10 虚拟机 `.vmx` 于 2026-08-30 设 `ethernet0.connectionType="bridged"`（备份 `.vmx.bak.20260830-2058`），MAC `00:0C:29:CA:E1:18`。

## 2. 唯一可桥接的物理网卡

`以太网` Realtek Gaming 2.5GbE（ifIndex 18，192.168.4.105/24，网关 192.168.4.1）。

⚠ **宿主地址会漂，下列 IP 是 2026-08-30 快照**：2026-10-05 复测该网卡已变成 `192.168.4.104`，
而 `.105` 变成了宿主 **WLAN** 网卡的地址（从宿主扫到 `.105:445` 其实是宿主自己）⇒ **动手前先 `ipconfig`
认清各网卡**，别抄本文的地址。详见 `docs/vm-ops.md` 第 20 条。

⛔ 不可桥接：WLAN、**Radmin VPN**（26.x 网段，**自带默认网关 26.0.0.1 —— 自动桥接的最大误选源**）、TAP-Windows / UU TAP、Wi-Fi Direct 虚拟卡、WAN Miniport、VMnet1/2/8。

## 3. 收敛自动桥接（需管理员）

- `Disable-NetAdapterBinding -Name <网卡> -ComponentID vmware_bridge -IncludeHidden`
- 或管理员跑 `vmnetcfg.exe`，把 VMnet0 从 Automatic 改为指定网卡。

判据：绑定**不存** `C:/ProgramData/VMware/netmap.conf`（那只是 vmnet 编号 → 设备名映射）；注册表 `…\VMnetLib\VMnetConfig\vmnet0` **只有 DisplayName** ⇒ 处于自动桥接。

## 4. 概念澄清（最容易误判的一条）

桥接只让虚拟机**在局域网内独立**（独立内网 IP + MAC），**公网出口 IP 仍与宿主相同** ⇒ 想规避按公网 IP 的风控，必须另开链路（VM 内代理 / 手机 USB 共享 / 第二条宽带）。`00:0C:29` 是 VMware OUI，抹特征要改 MAC + BIOS/硬盘 UUID。

## 5. 提权偏好

系统配置要提权时**直接弹 UAC 让用户点确认**，不要生成脚本让他手动跑。
