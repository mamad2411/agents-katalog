---
name: firmware-analyze
description: 嵌入式固件静态分析工具。解析 ELF/Mach-O 文件、导出内存布局与符号表、反汇编关键函数、提取字符串/常量、分析 Flash/RAM 占用。使用 arm-none-eabi 工具链 (objdump/readelf/nm/size) 和 Python 脚本进行自动化分析。当用户提到固件分析、ELF 解析、内存布局、反汇编、符号表、段分析、Flash 占用、RAM 占用、objdump、readelf、size、nm、固件逆向 时自动触发。也兼容 /firmware-analyze 显式调用。
---

# Firmware Analyze

嵌入式固件静态分析：ELF 解析、内存布局、符号表、反汇编。

## 前置条件

- `arm-none-eabi-*` 工具链（或对应架构的 GNU 工具链）
- 编译产物：`.elf` + 可选 `.map`

## 分析工作流

### 1. 基本信息

```bash
file firmware.elf
arm-none-eabi-readelf -h firmware.elf
```

### 2. 内存布局 (Sections)

```bash
arm-none-eabi-objdump -h firmware.elf
arm-none-eabi-readelf -S firmware.elf
```

关键段说明：
| 段名 | 说明 |
|------|------|
| `.text` | 代码段 |
| `.rodata` | 只读常量 |
| `.data` | 已初始化数据 |
| `.bss` | 未初始化数据 (不占 Flash) |
| `.heap` | 堆空间 |
| `.stack` | 栈空间 |

### 3. Flash / RAM 占用

```bash
arm-none-eabi-size firmware.elf
arm-none-eabi-size -A firmware.elf  # 详细分项
```

输出示例：
```
   text    data     bss     dec     hex filename
  45678    1024    8192   54894    d66e firmware.elf
```

- Flash 占用 ≈ text + data
- RAM 占用 ≈ data + bss

### 4. 符号表

```bash
# 所有符号（含排序）
arm-none-eabi-nm -n -S --size-sort firmware.elf

# 只显示大对象 (>1KB)
arm-none-eabi-nm -n -S --size-sort firmware.elf | awk '$2>1024'
```

### 5. 反汇编

```bash
# 反汇编全部 .text
arm-none-eabi-objdump -d firmware.elf

# 反汇编指定函数
arm-none-eabi-objdump -d --disassemble=main firmware.elf

# 混合源码（需编译时 -g）
arm-none-eabi-objdump -S firmware.elf

# 生成反汇编到文件
arm-none-eabi-objdump -d firmware.elf > disasm.txt
```

### 6. 字符串提取

```bash
arm-none-eabi-strings -n 4 firmware.elf | sort -u
# 提取可打印字符串最小长度 4
```

### 7. 链接脚本 (Linker Script) 分析

从 Map 文件提取内存布局：
```bash
grep -E "^(\.text|\.rodata|\.data|\.bss|\.heap|\.stack)" firmware.map
```

### 8. 中断向量表

```bash
arm-none-eabi-objdump -s -j .isr_vector firmware.elf
```

## 内存区使用速查

```python
# Python 分析脚本示例
import subprocess, re

def parse_size(elf_path):
    out = subprocess.check_output(
        ['arm-none-eabi-size', '-A', elf_path]).decode()
    sections = {}
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            sections[parts[0]] = int(parts[1])
    return sections

def top_symbols(elf_path, n=20):
    out = subprocess.check_output(
        ['arm-none-eabi-nm', '-n', '-S', '--size-sort', elf_path]).decode()
    symbols = []
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) >= 4:
            addr = parts[0]
            size = int(parts[1], 16) if parts[1] else 0
            name = parts[3]
            symbols.append((name, size, addr))
    symbols.sort(key=lambda x: x[1], reverse=True)
    return symbols[:n]
```

## 脚本

- `scripts/elf_report.py` — 生成 ELF 综合分析报告
- `scripts/memory_map.py` — 可视化内存布局
- `scripts/top_symbols.py` — 按大小排序符号表
