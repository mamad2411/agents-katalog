---
name: smart-card-driver-debug
category: hardware
description: Debug and configure smart card readers for synchronous memory cards (SLE4442/4428,
  AT88SC, etc.) on Windows. Covers driver binding, vendor CT-API usage, Microsoft
  CCID limitations, and 32-bit DLL interop.
triggers:
- SLE4442
- SLE4428
- synchronous card
- memory card
- smart card reader driver Windows
- VID_
- PID_
- CTAlc001
- Alcor
- AU9540
- AK9543
- PC/SC synchronous failure
- Pincop
- 品可
- ICU02
- PSC
- error counter
- SLE4442 PSC
- SLE4442 attack
- SLE4442 crack
- SLE4442 clone
- SLE4442 security
- synchronous card attack
- 冷氣卡
- 校園卡
- Secure Boot smart card
- wudfusbcciddriver
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- hardware
- iot
- embedded
- firmware
- smart
- card
- driver
- debug
related_skills: []
---

# Smart Card Reader Driver Debugging (Windows)

## Core Concept: Synchronous vs Asynchronous Cards

| Card Type | Examples | Protocol | PC/SC Support |
|-----------|----------|----------|---------------|
| **Asynchronous (ISO 7816)** | SIM, bank cards, eID, Java Card | T=0 / T=1 | Yes (Native) |
| **Synchronous (Memory)** | SLE4442, SLE4428, AT88SC, AT24Cxx | I2C / 2-wire / 3-wire | **Not supported by standard PC/SC** |

**Key insight**: Microsoft CCID driver (`wudfusbcciddriver.inf`) only implements ISO 7816 T=0/T=1. It returns empty `GET_FEATURE_REQUEST` (no `SET_CARD_TYPE`), and `SCardConnect` with T=0/T=1 fails with `0x00000005` (SCARD_E_PROTO_MISMATCH).

---

## The Working Path: Vendor CT-API

Alcor Micro readers (AU9540, AK9543, AU9520) ship with **`CTAlc001.dll`** — a proprietary CT-API (ISO 7816-4 CT-BCS) that bypasses PC/SC entirely.

### DLL Exports (CTAlc001.dll)
```
CT_init(ctn: uint16, pn: uint16) -> int16
CT_data(ctn, dad, sad, lenc, command, lenr, response) -> int16
CT_close(ctn) -> int16
```

### Python 32-bit Interop (Required — DLL is 32-bit)
```bash
# Download 32-bit Python embed package
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-win32.zip" -OutFile "python32.zip"
Expand-Archive python32.zip -DestinationPath C:\Temp\py32
```

```python
import ctypes
dll = ctypes.windll.LoadLibrary(r"C:\path\to\CTAlc001.dll")

dll.CT_init.argtypes = [ctypes.c_uint16, ctypes.c_uint16]
dll.CT_init.restype = ctypes.c_int16

dll.CT_data.argtypes = [
    ctypes.c_uint16,
    ctypes.POINTER(ctypes.c_ubyte),  # dad
    ctypes.POINTER(ctypes.c_ubyte),  # sad
    ctypes.c_uint16,                  # lenc
    ctypes.POINTER(ctypes.c_ubyte),   # command
    ctypes.POINTER(ctypes.c_uint16),  # lenr
    ctypes.POINTER(ctypes.c_ubyte),   # response
]
dll.CT_data.restype = ctypes.c_int16

dll.CT_close.argtypes = [ctypes.c_uint16]
dll.CT_close.restype = ctypes.c_int16

# Initialize (port 100 = USB for Alcor)
handle = dll.CT_init(0, 100)  # returns 0 on success
```

### SLE4442 Commands via CT-API
```python
# Verify PSC (default FFFFFF)
cmd = bytes([0xFF, 0x20, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF])

# Read 4 bytes at offset 0
cmd = bytes([0xFF, 0xB0, 0x00, 0x00, 0x04])

# Read error counter (address 0x1F)
cmd = bytes([0xFF, 0xB0, 0x00, 0x1F, 0x01])

# Write byte
cmd = bytes([0xFF, 0xD0, 0x00, offset, 0x01, value])

# Change PSC (after verify)
cmd = bytes([0xFF, 0xD2, 0x00, 0x00, 0x03, new_p1, new_p2, new_p3])
```

---

## Driver Binding Strategies (Critical Blocker)

### Problem
Windows binds Alcor readers (VID_058F) to Microsoft CCID. Rebranded readers (e.g., Pincop ICU02 = VID_2CE3 PID_9563) have no matching INF.

### Strategy 1: Modify Original INF + Test Signing (Most Reliable)
1. Copy original driver folder (contains `.sys`, `.dll`, `.inf`, `.cat`)
2. Edit `SZCCID.INF` → add your VID/PID to `[DeviceList.NTamd64]`
3. Enable test signing: `bcdedit /set testsigning on` (reboot)
4. Re-sign `.cat` with self-cert or use `pnputil /add-driver` with modified INF
5. Force bind: `pnputil /remove-device <instance>` → `pnputil /scan-devices`

### Strategy 2: Registry Force-Bind (No Reboot, Fragile)
```powershell
# Find device instance
$inst = "USB\VID_2CE3&PID_9563\5&3639e268&0&4"

# Set driver to SZCCID (oem58.inf = AlcorMicro)
pnputil /remove-device $inst
# Edit registry:
# HKLM\SYSTEM\CurrentControlSet\Enum\USB\VID_2CE3&PID_9563\...\Driver = "{50dd5230-ba8a-11d1-bf5d-0000f805f530}\0001"
# HKLM\...\Service = "szccid"
pnputil /scan-devices
```

### Strategy 3: DevCon (If Available)
```cmd
devcon update "SZCCID.INF" "USB\VID_2CE3&PID_9563"
```

---

## Alcor Driver Package Structure
```
AU9540_V1.7.2.0\program_files\AlcorMicro\x64\
├── CTAlc001.dll       ← CT-API (32-bit & 64-bit versions exist)
├── SZCCID.sys         ← Kernel driver (binds to device)
├── SzCcidV1900.dll    ← Co-installer / user-mode CCID
├── SCPwrSetSvr.exe    ← Power management
├── SZCCID.INF         ← Installation INF
├── szccid.cat         ← WHQL signature (must re-sign if INF modified)
└── AlcGener.sys       ← Generic helper
```

---

## Common Error Codes

| Code | Meaning | Context |
|------|---------|---------|
| `0x00000005` | SCARD_E_PROTO_MISMATCH | T=0/T=1 connect on synchronous card |
| `0x00000006` | SCARD_E_NO_SMARTCARD | MS CCID can't detect synchronous card (no ATR) |
| `0xFFF8` (-8) | ERR_CT (CT-API) | `CT_init` failed — device not bound to SZCCID.sys |
| `0x00313520` | IOCTL_SMARTCARD_GET_FEATURE_REQUEST | Microsoft CCID returns empty list (no features) |
| `31` (0x1F) | Service STOPPED | `sc query szccid` — driver loaded but not bound |
| `WinError 193` | Wrong bitness | Loading 32-bit DLL in 64-bit Python (or vice versa) |

---

## Critical Blockers (Lessons from Pincop ICU02 = VID_2CE3 PID_9563)

### Secure Boot Blocks Test Signing
```
bcdedit /set testsigning on
→ "The value is protected by Secure Boot policy and cannot be modified or deleted."
```
**If Secure Boot is enabled**, you CANNOT enable test signing. Options:
1. Enter UEFI/BIOS → disable Secure Boot → reboot → enable test signing → reboot → install driver
2. Buy a reader whose VID/PID is in the vendor's WHQL-signed INF (e.g., ACS ACR38U)
3. Buy the same chip with original VID (Alcor AU9540 = VID_058F PID_9540)

### Registry Force-Bind Doesn't Survive `pnputil /enable-device`
Setting `Service=SzCCID` in the Enum key works temporarily, but `pnputil /enable-device`
triggers PnP re-enumeration which **overrides Service back to WUDFRd** based on
`USB\Class_0B` CompatibleID. The registry value remains SzCCID but the actual
driver stack reverts to WUDF CCID.

**Workaround attempted**: Disable device → change registry → enable device.
Result: PnP still re-binds to `wudfusbcciddriver.inf` because it's the highest-ranked
signed driver for `USB\Class_0B&SubClass_00&Prot_00`.

### MS CCID Direct IOCTL Access (Dead End)
Opening `\\?\USB#VID_2CE3&PID_9563#...#{a5dcbf10-...}` via `CreateFileW` succeeds,
but `DeviceIoControl` only responds to 2 IOCTLs:
- `IOCTL+0x028` → returns empty (ack-only)
- `IOCTL+0x038` → returns `02000000` (version/capabilities DWORD)

ALL standard smartcard IOCTLs return `ERROR_INVALID_FUNCTION` (err=1):
- GET_FEATURE_REQUEST, SET_CARD_TYPE, POWER, TRANSMIT, SET_PROTOCOL, IS_PRESENT → all fail
- CCID_ESCAPE (0x004) with raw CCID messages → fails
- WriteFile/ReadFile → written=0 (WUDF doesn't support raw I/O)

**Conclusion**: WUDF CCID driver is a sealed box. Cannot send CCID escape commands
or SET_CARD_TYPE. The only path out is replacing the driver entirely.

### CTAlc001.dll Bitness
- `CTAlc001.dll` from Alcor x64 package is **PE32 (i386, 32-bit)**
- `SZCCID.sys` is **AMD64 (64-bit)**
- Must use **32-bit Python** to load the DLL: `python-3.11.9-embed-win32.zip`
- 64-bit Python → `WinError 193: not a valid Win32 application`
- DLL communicates with kernel driver via DeviceIoControl (works across 32→64 bitness)
- BUT: CT_init still returns -8 if the kernel driver isn't bound to the device

### 32-bit Python Setup (Embed Package)
```powershell
# Download 32-bit embeddable Python (no installer needed)
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-win32.zip" -OutFile "C:\Temp\py311-32.zip"
Expand-Archive -Path C:\Temp\py311-32.zip -DestinationPath C:\Python311-32 -Force

# Verify it's 32-bit
C:\Python311-32\python.exe -c "import struct; print(struct.calcsize('P')*8)"
# → 32
```

---

## ⚠️ SLE4442 Safety Rules (MANDATORY)

**PSC has a 3-strike lockout — PERMANENT if exhausted.**

1. **Always read Security Memory first** → check Error Counter (EC) byte
2. **Never blind-guess PSC** — common defaults: `FF FF FF`, `B2 B2 B2`
3. **Stop when EC ≤ 1 attempt remaining** — preserve at least 1 try
4. **Successful Verify resets EC** — no attempt consumed when PSC is correct

Full attack surface analysis: see `smart-card-reader-sle4442` → `references/sle4442-security-attacks.md`

---

## Debugging Checklist

1. **Verify hardware**: `pnputil /enum-devices` → confirm VID/PID
2. **Check current driver**: Look for `wudfusbcciddriver.inf` (Microsoft) vs `szccid.inf` (Alcor)
3. **Install Alcor driver**: `pnputil /add-driver SZCCID.INF /install`
4. **Force re-enumeration**: Remove device → scan
5. **Test CT-API**: 32-bit Python + `CT_init(0, 100)` → must return 0
6. **If CT_init returns -8**: Device still bound to Microsoft CCID → fix binding

---

## Reader Replacement Recommendations

When driver binding cannot be resolved (Secure Boot enabled, unsigned INF rejected, PnP overrides registry), **replacing the reader is the most practical solution**.

### Recommended Readers for SLE4442 (Taiwan availability)

| Reader | VID:PID | Price (NT$) | Why |
|--------|---------|-------------|-----|
| **ACS ACR38U** | 072B:021C | 300–800 | WHQL-signed driver, full SLE4442/4428 SDK, most Python examples, globally most popular |
| **ACS ACR39U** | 072B:021D | 400–1000 | ACR38U upgraded version |
| **Alcor AU9540 (original VID)** | 058F:9540 | 150–350 | Same chip as Pincop ICU02 but with Alcor's original VID — existing SZCCID driver binds automatically |

### Shopee (蝦皮) Search Keywords
`ACR38U`, `SLE4442 讀卡機`, `冷氣卡 讀卡機`, `AU9540 讀卡機`, `IC卡讀卡器 4442`

### Before Buying — Verify
- ✅ Description mentions **SLE4442 / 4428 / 同步卡 / 記憶卡**
- ❌ Only mentions **CPU卡 / ISO 7816** → cannot read synchronous cards
- ❌ Rebranded readers with non-standard VIDs (unless vendor provides signed driver)

---

## References
- `references/alcor-au9540-driver-notes.md` — Detailed Alcor AU9540/AK9543 driver internals
- `references/sle4442-ctapi-commands.md` — Complete SLE4442 command set for CT-API
- `references/windows-driver-binding-tactics.md` — Registry/INF/test-signing tactics
- `references/sle4442-security-attacks.md` — **Complete SLE4442 attack surface analysis**

## Scripts
- `scripts/test_ctapi_sle4442.py` — Ready-to-run CT-API test (requires 32-bit Python)
- `scripts/force_bind_szccid.ps1` — PowerShell script to force device bind to SZCCID