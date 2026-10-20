---
name: rootkit-analysis
description: MBR / VBR / UEFI firmware / Linux kernel module / DKOM / eBPF abuse な kernel-level マルウェアと bootkit を解析する。disk image / firmware dump / memory dump からの抽出と reverse engineering を組合せる。CTF DFIR / APT 解析で発火。layer 別の深掘りは references/ 参照
category: reverse
tags:
  - bootkit
  - rootkit
  - mbr
  - uefi
  - kernel
  - persistence
  - low-level
---

# Rootkit / Bootkit Analysis

## When to Use

- 高度 APT 系 sample (TrickBoot / FinSpy / MosaicRegressor / CosmicStrand 等) の解析
- 不審 disk image で MBR / VBR / UEFI firmware に異常
- Linux kernel rootkit (LKM / DKOM / eBPF abuse) の検出と reverse
- BIOS / UEFI dump からの persistence 抽出
- memory dump で隠蔽 process / hooked syscall / 改竄 kernel 構造体を検出

**使わない場面**: user-land malware (→ `reverse-engineering`)、user-land memory artefact のみ (→ `memory-analysis`)。

variant 別の深掘りは references/ を参照: UEFI bootkit / SPI flash 内 firmware implant = `references/uefi-bootkit.md`、Linux kernel rootkit (LKM / DKOM / eBPF) = `references/linux-kernel.md`、隠蔽 process / hooked syscall / 改竄 kernel 構造体の memory-based detection = `references/detection.md`。

## Approach / Workflow

### Phase 1 — 入手 artefact

```
- disk image: MBR (sector 0)、VBR (filesystem 先頭 sector)
- firmware dump: SPI flash / UEFI capsule / chipsec dump
- memory dump (running rootkit が user-land hook を仕込んでいる)
```

### Phase 2 — MBR / VBR 解析

```bash
dd if=disk.dd bs=512 count=1 of=mbr.bin
xxd mbr.bin
```

正常 MBR は最初 446 byte の bootstrap code + partition table + 0x55AA。bootkit は bootstrap を改造し OS loader より先に実行:

```
- 0x7c00 にロードされた直後に attacker stub が走る
- VBR (NTLDR / BOOTMGR の sector) を patch
- 自前の loader が memory に乗り、その後 OS bootloader を呼ぶ
```

bootkit identification: ghidra で 16-bit real mode の disassemble (`Language: x86:LE:16:Real Mode`)。

### Phase 3 — UEFI module 解析

UEFI firmware dump (`spi_flash.bin`):

```bash
UEFITool spi_flash.bin
# Volume / Module 階層を navigate
# Suspicious module: 標準にない GUID、SMM driver の追加
```

抽出した PE (`.efi`) を Ghidra で解析。entry point は `EfiMain(ImageHandle, SystemTable)`。

```
- BootService (BS) hook
- RuntimeService (RT) hook
- gST (System Table) の改造
- Variable (NVRAM) の改竄
- Boot order 操作 (SetBootOptions)
- 永続化 GUID と payload
```

### Phase 4 — 検知 (chipsec)

```bash
chipsec_main.py -m common.bios_wp        # BIOS write protection
chipsec_main.py -m common.spi_lock
chipsec_main.py -m common.bios_kbrd_buffer
chipsec_main.py -m tools.uefi.scan_image
chipsec_main.py -m tools.uefi.scan_blocked
```

unsigned UEFI image / SecureBoot bypass / SPI write 可能の組合せが攻撃面。

### Phase 5 — 主要 family

```
TrickBoot / Sednit BlackLotus  Windows UEFI bootkit
LoJax (Sednit/Fancy Bear)       LoJack 改造 UEFI rootkit
MosaicRegressor                 Hacking Team firmware に類似
CosmicStrand                    UEFI bootkit (中華系 APT)
MoonBounce (UEFI/SPI)           SPI flash 直接書込
ESPecter                        EFI System Partition
FinFisher BootKit               commercial spyware
```

family identification: yara firmware ruleset / FwHunt rule / VT lookup。

### Phase 6 — memory 上の hook

bootkit が runtime に user / kernel コードを hook して隠蔽する場合:

```
- Volatility でカーネルの inline hook / SSDT 改竄を検出
- callbacks / driverirp で 動的に追加された driver
- 永続化のために registry / service を作る version も
```

詳細: `rootkit-analysis`、`memory-analysis`。

### Phase 7 — レポート / IOC

```
- 感染部位 (MBR / VBR / EFI / SMM / SPI flash / NVRAM)
- 解析したサンプルの hash
- 推定 family / 既知 sample との類似
- 永続化機構の詳細
- 検知方法 (chipsec rule / yara / fwhunt)
- 修復: SPI flash 再書込み / disk wipe + secure reinstall
```

## Tools

```
ghidra (16-bit real mode + UEFI PE)
UEFITool / fwhunt / fwts
chipsec
volatility3 (memory hook 検出)
yara / TLSH
WebFetch
Bash (sandbox)
```

## Related Skills

- `reverse-engineering` (user-land malware RE)
- `memory-analysis` (memory dump 解析)
- `firmware-iot-security`
- `ioc-hunting`

## Rules

1. **隔離環境** — UEFI module を実機で試さない
2. **integrity**
3. **共有禁止**
4. **修復は OS reinstall + firmware reflash**: 通常 OS 再インストールでは bootkit は残る
