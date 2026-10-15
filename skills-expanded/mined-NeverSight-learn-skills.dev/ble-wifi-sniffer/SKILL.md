---
name: ble-wifi-sniffer
description: 蓝牙 BLE 与 Wi-Fi 无线抓包分析工具。支持 nRF Sniffer for Bluetooth LE、ESP32 promiscuous Wi-Fi 抓包、Wireshark 实时分析。用于抓取 BLE 广播/连接包、Wi-Fi 管理帧、解析协议交互、分析连接时序。当用户提到 BLE 抓包、Wi-Fi 抓包、nRF Sniffer、ESP32 抓包、蓝牙协议分析、Wireshark 无线、BLE sniffer、Wi-Fi promiscuous、nRF52840 dongle 时自动触发。也兼容 /ble-wifi-sniffer 显式调用。
---

# BLE / Wi-Fi Sniffer

BLE 与 Wi-Fi 无线协议抓包分析。

## 支持的工具

| 工具 | 对象 | 硬件 | 输出格式 |
|------|------|------|---------|
| nRF Sniffer for BLE | BLE 4.x/5.x | nRF52840/nRF52833 Dongle | pcap → Wireshark |
| ESP32 promiscuous | Wi-Fi 11b/g/n | ESP32 开发板 | pcap → Wireshark |
| Ubertooth One | BLE | Ubertooth | pcap |
| TI CC2540 | BLE | CC2540 USB Dongle | pcap |

## 前置条件

- Wireshark (含 extcap 路径配置)
- nRF Sniffer: [nRF Sniffer for BLE](https://www.nordicsemi.com/Products/Development-tools/nrf-sniffer-for-bluetooth-le)
- ESP32: 已烧录 sniffer 固件

## BLE 抓包工作流

### 1. nRF Sniffer 初始化

```bash
# 烧录 sniffer 固件到 nRF52840 Dongle
nrfutil dfu usb-serial -pkg nrf_sniffer_for_bluetooth_le_4.1.0.zip -p COM3
```

Wireshark 中：
1. 打开 Wireshark → Capture → Options
2. 选择 `nRF Sniffer for Bluetooth LE` 接口
3. 配置 Target Device Address（针对某设备）或 All

### 2. BLE 广告包分析

过滤表达式：
```
btle.advertising_header.pdu_type
btle.advertising_address == xx:xx:xx:xx:xx:xx
btcommon.assigned_numbers.company_name
```

### 3. BLE 连接追踪

```
btle.connection_info.access_address
btle.connection_info.aa == 0xXXXXXXXX
btle.ll_data.channel_map
btle.connection_update.win_size
```

### 4. 导出 BLE 报文

```bash
tshark -r capture.pcapng -Y "btle" -T json > ble_packets.json
```

## Wi-Fi 抓包工作流 (ESP32)

### 1. ESP32 Sniffer 固件

烧录 [ESP32-Wi-Fi-Sniffer](https://github.com/ESP-EOS/ESP32-Wi-Fi-Sniffer) 固件。

### 2. 抓取 Wi-Fi 帧

```bash
# 通过串口输出到 Wireshark pipe
python esp32_sniffer.py COM3 --channel 1,6,11 | wireshark -k -i -
```

### 3. Wi-Fi 过滤

```
wlan.fc.type_subtype == 0x08      # Beacon 帧
wlan.fc.type_subtype == 0x04      # Probe Request
wlan.fc.type_subtype == 0x05      # Probe Response
wlan.sa == xx:xx:xx:xx:xx:xx      # 源 MAC
wlan.da == xx:xx:xx:xx:xx:xx      # 目标 MAC
wlan.ssid == "MySSID"             # SSID 过滤
```

### 4. 信道跳变策略

- BLE: 37/38/39 广播信道 + 0-36 数据信道（自适应跳频）
- Wi-Fi: 固定信道 (1/6/11 最常用)

## 常见分析场景

### BLE 连接建立
1. `ADV_IND` ← 广播包
2. `CONNECT_REQ` → 连接请求
3. `LL_DATA` ↔ 数据交互
4. `LL_CONNECTION_UPDATE_REQ` 参数更新

### Wi-Fi 设备发现
1. STA: `Probe Request` 广播
2. AP: `Probe Response` 回复
3. STA: `Auth` 认证
4. AP: `Auth` 确认
5. STA: `Assoc Request` 关联
6. AP: `Assoc Response` 关联确认

## 脚本

- `scripts/ble_sniffer_start.py` — 启动 nRF BLE 抓包并生成 pcap
- `scripts/esp32_wifi_sniffer.py` — ESP32 Wi-Fi 抓包到 pcap
- `scripts/ble_connection_analyzer.py` — 解析 BLE 连接时序
