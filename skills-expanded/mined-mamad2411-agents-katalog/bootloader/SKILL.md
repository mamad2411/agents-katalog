---
name: bootloader
description: 嵌入式 Bootloader 管理与固件升级工具。支持 STM32 DfuSe (USB DFU)、UF2、OpenBLT、MCUboot、自定义 bootloader 协议。通过 dfu-util、uf2conv、stm32flash、串口 YMODEM/XMODEM 等执行固件烧录。当用户提到 bootloader、DFU、DfuSe、UF2、固件升级、在线升级、dfu-util、stm32flash、OpenBLT、MCUboot、YMODEM、IAP 时自动触发。也兼容 /bootloader 显式调用。
---

# Bootloader

嵌入式 Bootloader 管理与固件升级。

## 支持的 Bootloader

| Bootloader | 接口 | 工具 | 适用芯片 |
|------------|------|------|---------|
| STM32 DfuSe | USB DFU | `dfu-util` / DfuSe Demo | STM32F1/F2/F4... |
| UF2 | USB MSC | `uf2conv.py` | RP2040, nRF52, SAMD |
| OpenBLT | CAN/UART/USB | MicroBoot + `OpenBLT_Host` | 多平台 |
| MCUboot | 内部 Flash | `mcumgr` / `newtmgr` | Zephyr, nRF |
| stm32flash | UART | `stm32flash` | STM32 全系列 |
| 自定义串口 | UART | 自定义脚本 | 任意 |

## 前置条件

- `dfu-util` (Windows: `dfu-util.exe`, Linux: `apt install dfu-util`)
- `uf2conv.py` (来自 pico-sdk/tools)
- `stm32flash` (Linux: `apt install stm32flash`)
- 硬件进入 Bootloader 模式（BOOT0 拉高 / 按键组合 / 复位）

## 常用工作流

### 1. STM32 USB DFU

```bash
# 检测 DFU 设备
dfu-util -l

# 烧录固件
dfu-util -a 0 -s 0x08000000:leave -D firmware.bin

# 读取当前固件
dfu-util -a 0 -s 0x08000000:0x10000 -U dump.bin

# 擦除芯片
dfu-util -a 0 -s 0x08000000:mass:force:unprotect -D /dev/null
```

### 2. UF2 (RP2040 / nRF52 / SAMD)

```bash
# HEX → UF2 转换
python uf2conv.py firmware.hex -c -f 0xADA52840 -o firmware.uf2

# BIN → UF2 转换
python uf2conv.py firmware.bin -b 0x10000000 -f 0xE48BFF56 -o firmware.uf2
```

UF2 Family IDs:
- RP2040: `0xE48BFF56`
- nRF52840: `0xADA52840`
- SAMD21: `0x68ED2B88`
- SAMD51: `0x55114460`

### 3. stm32flash (UART Bootloader)

```bash
# 检测芯片
stm32flash /dev/ttyUSB0

# 烧录
stm32flash -w firmware.bin -v -g 0x0 /dev/ttyUSB0

# 读取
stm32flash -r dump.bin /dev/ttyUSB0

# 解除读保护
stm32flash -k /dev/ttyUSB0
```

### 4. OpenBLT

```bash
# 通过 MicroBoot GUI 或 CLI
OpenBLT_Host -t COM3 -b 57600 -f firmware.srec
```

### 5. 自定义串口 Bootloader (YMODEM/XMODEM)

```python
import serial
from xmodem import XMODEM

ser = serial.Serial('COM3', 115200, timeout=1)
def getc(size, timeout=1):
    return ser.read(size) or None
def putc(data, timeout=1):
    return ser.write(data)

modem = XMODEM(getc, putc)
with open('firmware.bin', 'rb') as f:
    modem.send(f)
```

## 安全注意事项

- 烧录前备份原始固件
- 注意 Option Bytes / 读保护设置
- 大容量芯片确认 Flash 起始地址（非全部 `0x08000000`）
- DfuSe 需注意 Alternate Setting 选择

## 脚本

- `scripts/dfu_flash.py` — dfu-util 封装，自动检测与烧录
- `scripts/uf2_pack.py` — BIN/HEX → UF2 批量转换
- `scripts/stm32flash_wrapper.py` — stm32flash 自动化封装
