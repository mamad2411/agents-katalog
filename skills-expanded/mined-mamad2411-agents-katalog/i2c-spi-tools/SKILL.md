---
name: i2c-spi-tools
description: I2C/SPI 总线调试工具。通过 FTDI/CH341/Aardvark/树莓派/单片机桥接器等适配器扫描总线设备、读写寄存器、收发 SPI 数据。支持 Python smbus2/spidev/pyftdi 以及命令行 i2c-tools。当用户提到 I2C、SPI、总线扫描、i2cdetect、寄存器读写、FTDI、CH341、Aardvark、smbus、i2c-tools、I2C 设备地址、SPI Flash 时自动触发。也兼容 /i2c-spi-tools 显式调用。
---

# I2C / SPI Tools

I2C 和 SPI 总线调试工具集合。

## 支持的适配器

| 适配器 | I2C | SPI | Python 库 |
|--------|-----|-----|-----------|
| FTDI (FT232H/FT2232H) | ✓ | ✓ | `pyftdi` |
| CH341 | ✓ | ✓ | `ch341` |
| Aardvark | ✓ | ✓ | `aardvark` |
| 树莓派 | ✓ | ✓ | `smbus2` / `spidev` |
| Linux /dev/i2c-N | ✓ | ✗ | `smbus2` |
| MCU 桥接器 | ✓ | ✓ | 自定义串口协议 |

## I2C 工作流

### 1. 扫描总线

```bash
# Linux (i2c-tools)
i2cdetect -y 1           # 扫描 /dev/i2c-1
i2cdetect -r 1 0x03 0x77 # 指定范围
```

Python:
```python
from smbus2 import SMBus
bus = SMBus(1)
for addr in range(0x03, 0x78):
    try:
        bus.read_byte(addr)
        print(f"Found: 0x{addr:02X}")
    except OSError:
        pass
```

FTDI:
```python
from pyftdi.i2c import I2cController
i2c = I2cController()
i2c.configure('ftdi://ftdi:232h/1')
for addr in range(0x03, 0x78):
    try:
        dev = i2c.get_port(addr)
        dev.read(1)
        print(f"Found: 0x{addr:02X}")
    except Exception:
        pass
```

### 2. 读寄存器

```python
# smbus2
bus.read_byte_data(dev_addr, reg_addr)
bus.read_i2c_block_data(dev_addr, reg_addr, length)

# pyftdi
port = i2c.get_port(dev_addr)
port.write([reg_addr])
data = port.read(length)
```

### 3. 写寄存器

```python
bus.write_byte_data(dev_addr, reg_addr, value)
# pyftdi
port.write([reg_addr, value])
```

## SPI 工作流

### 1. 收发数据

```bash
# Linux spidev
spidev_test -D /dev/spidev0.0 -s 1000000 -p "\x9F\x00\x00\x00"
```

Python:
```python
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0
# 读取 JEDEC ID
resp = spi.xfer2([0x9F, 0x00, 0x00, 0x00])
```

FTDI:
```python
from pyftdi.spi import SpiController
spi = SpiController()
spi.configure('ftdi://ftdi:232h/1')
port = spi.get_port(cs=0, freq=1E6, mode=0)
data = port.exchange([0x9F, 0x00, 0x00, 0x00])
```

### 2. SPI Flash 操作

- 读 JEDEC ID: `0x9F`
- 读状态寄存器: `0x05`
- 写使能: `0x06`
- 读数据: `0x03 + 3B addr`
- 页编程: `0x02 + 3B addr + data`
- 扇区擦除: `0x20 + 3B addr`

## 常用设备地址速查

| 设备 | I2C 地址 | 常见用途 |
|------|---------|---------|
| EEPROM (24Cxx) | 0x50-0x57 | 存储 |
| 温度传感器 (LM75) | 0x48-0x4F | 测温 |
| RTC (DS3231) | 0x68 | 实时时钟 |
| OLED (SSD1306) | 0x3C/0x3D | 显示屏 |
| IMU (MPU6050) | 0x68/0x69 | 姿态传感器 |
| GPIO (PCA9555) | 0x20-0x27 | IO 扩展 |

## 脚本

- `scripts/i2c_scan.py` — 多适配器 I2C 总线扫描
- `scripts/i2c_reg_rw.py` — I2C 寄存器批量读写
- `scripts/spi_flash_tool.py` — SPI Flash 读写擦除
