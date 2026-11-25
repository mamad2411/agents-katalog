---
name: smart-card-usb-direct
description: 'Bypass PC/SC/CCID middleware and communicate directly with USB smart
  card readers via vendor DLLs (Windows) or libusb/WinUSB (cross-platform). Covers
  Alcor AU9540/AK9543, DCULC, SpringCard, and similar Chinese OEM readers for synchronous
  memory cards (SLE4442, SLE4428, AT24Cxx, AT88SCxxx).

  '
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- smart-card
- usb
- synchronous-card
- vendor-dll
- pcsclite-bypass
- SLE4442
- AL9543
related_skills: []
---

# Smart Card USB Direct Access

## When to Use This Skill

- PC/SC `SCardConnect` fails with `0x00000005` (SCARD_E_NO_SMARTCARD) on synchronous cards
- Microsoft CCID driver `GET_FEATURE_REQUEST` returns empty — no `FEATURE_SET_CARD_TYPE`
- Reader uses Alcor AU9540/AK9543, DCULC RD600-ULC, SpringCard, or similar OEM chips
- Target cards: SLE4442, SLE4428, AT24C01/02/04/08/16/64, AT88SCxxx, SSF1101
- Vendor provides a DLL/SO with functions like `IC_InitComm`, `IC_Check_4442`, `IC_Read`, `IC_Write`

## The Core Problem

Standard PC/SC + CCID stack only supports **ISO 7816 T=0/T=1** asynchronous cards.
**Synchronous memory cards** (SLE4442, SLE4428, I²C EEPROMs) use proprietary command sets.
Microsoft's inbox CCID driver (`wudfusbcciddriver`) exposes **zero features** for them.

**Solution**: Use the vendor's private DLL that talks raw USB/CCID escape commands.

---

## 1. RECONNAISSANCE: Identify the Reader & Vendor DLL

### 1.1 USB VID/PID
```powershell
# Device Manager → Smart card readers → Properties → Details → Hardware Ids
# Example: USB\VID_2CE3&PID_9563  (Pincop ICU02 = Alcor AK9543)
```

### 1.2 Locate Vendor Driver Package
- Check vendor website (pincop.com.tw, alcormicro.com, dculc.com)
- Or Windows Update Catalog search: "Alcor Micro Smart Card Reader"
- Driver package typically contains:
  ```
  x64/
    CTAlc001.dll      ← Main API DLL (Alcor)
    SzCcidV1900.dll   ← CCID transport DLL
    SZCCID.sys        ← Kernel driver
    SZCCID.inf        ← Installer
  ```

### 1.3 Extract Exported Functions
```bash
# Linux/macOS
strings CTAlc001.dll | grep -iE "(IC_|Check|Init|Read|Write|Status|Comm)"

# Windows (PowerShell)
dumpbin /exports CTAlc001.dll

# Python (pefile)
python3 -c "
import pefile
pe = pefile.PE('CTAlc001.dll')
for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    if exp.name: print(exp.name.decode())
"
```

### 1.4 Common Alcor/DCULC API Pattern
```c
// Connection
HANDLE IC_InitComm(short port);           // port=100 for USB
void   IC_ExitComm(HANDLE h);

// Card detection
short  IC_CheckCard(HANDLE h);            // returns type code
short  IC_Check_4442(HANDLE h);           // 0 = SLE4442 present
short  IC_Check_4428(HANDLE h);           // 0 = SLE4428 present
short  IC_Check_CPU(HANDLE h);            // 0/1 = T=0/T=1 CPU card

// Type initialization (must call before read/write)
short  IC_InitType(HANDLE h, short type); // 0x10=SLE4442, 0x04=SLE4428, 0x40=AT24Cxx

// Data transfer
short  IC_Read(HANDLE h, short offset, short len, BYTE* buf);
short  IC_Write(HANDLE h, short offset, short len, BYTE* buf);
short  IC_Write24(HANDLE h, short offset, short len, BYTE* buf); // AT24Cxx

// SLE4442/4428 password (hex string "ffffff" = 3 bytes FF FF FF)
short  IC_CheckPass_4442hex(HANDLE h, char* hexPass);
short  IC_CheckPass_4428hex(HANDLE h, char* hexPass);
short  IC_ChangePass_4442hex(HANDLE h, char* newHexPass);
short  IC_ChangePass_4428hex(HANDLE h, char* newHexPass);
short  IC_ReadCount_SLE4442(HANDLE h);    // remaining PIN attempts
short  IC_ReadCount_SLE4428(HANDLE h);
short  IC_ReadPass_4442hex(HANDLE h, char* outHexPass);
```

---

## 2. PYTHON WRAPPER (ctypes)

```python
import ctypes
from ctypes import c_short, c_void_p, c_char_p, POINTER, c_ubyte, create_string_buffer

class AlcorDirect:
    def __init__(self, dll_path):
        self.dll = ctypes.windll.LoadLibrary(dll_path)
        self.handle = -1
        
        # Define signatures
        self.dll.IC_InitComm.argtypes = [c_short]
        self.dll.IC_InitComm.restype = c_void_p
        
        self.dll.IC_ExitComm.argtypes = [c_void_p]
        
        self.dll.IC_Check_4442.argtypes = [c_void_p]
        self.dll.IC_Check_4442.restype = c_short
        
        self.dll.IC_InitType.argtypes = [c_void_p, c_short]
        self.dll.IC_InitType.restype = c_short
        
        self.dll.IC_Read.argtypes = [c_void_p, c_short, c_short, POINTER(c_ubyte)]
        self.dll.IC_Read.restype = c_short
        
        self.dll.IC_Write.argtypes = [c_void_p, c_short, c_short, POINTER(c_ubyte)]
        self.dll.IC_Write.restype = c_short
        
        self.dll.IC_CheckPass_4442hex.argtypes = [c_void_p, c_char_p]
        self.dll.IC_CheckPass_4442hex.restype = c_short
        
        self.dll.IC_ReadCount_SLE4442.argtypes = [c_void_p]
        self.dll.IC_ReadCount_SLE4442.restype = c_short
        
        # Type codes (from DCULC/driver docs)
        self.TYPE_SLE4442 = 0x10
        self.TYPE_SLE4428 = 0x04
        self.TYPE_AT24CXX = 0x40
        self.USB_PORT = 100

    def connect(self):
        self.handle = self.dll.IC_InitComm(self.USB_PORT)
        return self.handle and self.handle > 0

    def disconnect(self):
        if self.handle > 0:
            self.dll.IC_ExitComm(self.handle)
            self.handle = -1

    def detect_sle4442(self):
        return self.dll.IC_Check_4442(self.handle) == 0

    def init_type(self, type_code):
        return self.dll.IC_InitType(self.handle, type_code) == 0

    def read(self, offset, length):
        buf = (c_ubyte * length)()
        ret = self.dll.IC_Read(self.handle, offset, length, buf)
        return list(buf) if ret == 0 else None

    def write(self, offset, data):
        buf = (c_ubyte * len(data))(*data)
        return self.dll.IC_Write(self.handle, offset, len(data), buf) == 0

    def verify_pin(self, pin_hex):  # e.g. "ffffff"
        buf = create_string_buffer(pin_hex.encode() + b'\x00')
        return self.dll.IC_CheckPass_4442hex(self.handle, buf) == 0

    def read_pin_counter(self):
        return self.dll.IC_ReadCount_SLE4442(self.handle)
```

---

## 3. READING SLE4442 — COMPLETE FLOW

```python
reader = AlcorDirect(r"C:\path\to\CTAlc001.dll")

if not reader.connect():
    raise RuntimeError("Cannot connect to reader")

if not reader.detect_sle4442():
    raise RuntimeError("No SLE4442 detected")

if not reader.init_type(reader.TYPE_SLE4442):
    raise RuntimeError("Failed to init SLE4442 type")

# Default PIN is usually FF FF FF
if not reader.verify_pin("ffffff"):
    raise RuntimeError("PIN verification failed")

print(f"Remaining attempts: {reader.read_pin_counter()}")

# Read entire 256-byte EEPROM
data = reader.read(0, 256)
print(f"Card data: {bytes(data).hex()}")

# Read error counter at 0x1F
err_byte = reader.read(0x1F, 1)
print(f"Error counter: {err_byte[0] if err_byte else 'N/A'}")

reader.disconnect()
```

---

## 4. ALTERNATIVE: WINUSB + RAW CCID (No Vendor DLL)

**⚠️ IMPORTANT**: This section only works if you can replace the Microsoft CCID driver
with WinUSB via Zadig. If the device is currently bound to Microsoft WUDF CCID:
- `CreateFileW` opens the device OK
- But **all** smartcard IOCTLs return `ERROR_INVALID_FUNCTION` (err=1)
- `WriteFile`/`ReadFile` return 0 bytes written
- WUDF CCID only responds to 2 IOCTLs: +0x028 (ack) and +0x038 (version DWORD)
- **No workaround exists** — must use Method 1 (vendor driver) or replace driver with WinUSB

If vendor DLL unavailable, bind WinUSB via Zadig and speak CCID directly:

### 4.1 Install WinUSB
```powershell
# Zadig: Options → List All Devices → Select "Alcor Micro USB Smart Card Reader"
# → Replace Driver → WinUSB (v6.1.7600.16385)
```

### 4.2 Python CCID over WinUSB (pyusb)
```python
import usb.core
import usb.util
import struct

# CCID message types
PC_TO_RDR_ICCPOWERON = 0x62
PC_TO_RDR_ICCPOWEROFF = 0x63
PC_TO_RDR_XFRBLOCK   = 0x6F
PC_TO_RDR_ESCAPE     = 0x6B
PC_TO_RDR_SETCARDTYPE = 0x72  # Alcor-specific (may vary)

RDR_TO_PC_DATABLOCK  = 0x80
RDR_TO_PC_ESCAPE     = 0x83

def ccid_msg(msg_type, data, slot=0, seq=0):
    length = len(data)
    header = struct.pack('<BIBBBBBB', msg_type, length & 0xFF, (length>>8)&0xFF, 
                         (length>>16)&0xFF, (length>>24)&0xFF, slot, seq, 0)
    return header + data

def parse_ccid(resp):
    if len(resp) < 10: return None
    msg_type, length, slot, seq, status = struct.unpack('<BIBBH', resp[:10])
    data = resp[10:10+length]
    return {'type': msg_type, 'status': status, 'data': data}

dev = usb.core.find(idVendor=0x2CE3, idProduct=0x9563)
if dev is None: raise RuntimeError("Device not found")

# Detach kernel driver if needed
if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)
dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]
ep_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
ep_in  = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

seq = 0
def send_cmd(msg_type, data):
    global seq
    seq = (seq + 1) & 0xFF
    msg = ccid_msg(msg_type, data, seq=seq)
    ep_out.write(msg)
    resp = ep_in.read(64, timeout=1000)
    return parse_ccid(bytes(resp))

# 1. Power on
r = send_cmd(PC_TO_RDR_ICCPOWERON, b'')
print(f"PowerOn: {r}")

# 2. Escape: Set card type SLE4442 (Alcor: 0x1A 0x02)
r = send_cmd(PC_TO_RDR_ESCAPE, bytes([0x1A, 0x02]))
print(f"SetCardType: {r}")

# 3. XfrBlock with pseudo-APDU
# FF B0 00 00 04 = READ 4 bytes at offset 0
apdu = bytes([0xFF, 0xB0, 0x00, 0x00, 0x04])
# XfrBlock data: bBWI(0) + level(0) + APDU
r = send_cmd(PC_TO_RDR_XFRBLOCK, bytes([0x00, 0x00]) + apdu)
print(f"Read: {r}")
```

---

## 5. REFERENCE PROJECTS TO STUDY

| Repo | Language | Approach | Cards |
|------|----------|----------|-------|
| `hk2022gd/DCULC` | Python + ctypes | Vendor DLL (`dculc.dll`) | SLE4442, SLE4428, AT24Cxx, AT88SC, CPU |
| `liblogicalaccess` | C++ + SWIG | PC/SC + proprietary backends | SLE4442, many RFID/NFC |
| `vamanea/scard-sle4442` | C | SpringCard `SCard2WBP*` API | SLE4442 |
| `hvfrancesco/SLE4442-card-manager` | Python + pyscard | Standard PC/SC (T=0 only) | ❌ Not for sync cards |

---

## 6. PITFALLS & GOTCHAS

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Wrong DLL arch** | `OSError: [WinError 193] %1 is not a valid Win32 application` | Match Python bitness (64-bit Python → x64 DLL) |
| **DLL not found** | `FileNotFoundError` | Use absolute path; check `C:\Windows\System32` vs `SysWOW64` |
| **Calling convention** | Crashes / garbage returns | Alcor uses `__stdcall` → `ctypes.windll` (not `cdll`) |
| **Handle type** | `IC_InitComm` returns 0 on 64-bit | Use `c_void_p` restype, check `handle and handle > 0` |
| **String encoding** | PIN verify fails | Pass ASCII hex string + null terminator: `"ffffff\x00"` |
| **Card not powered** | All reads return error | Call `IC_InitType` AFTER `IC_Check_4442` succeeds |
| **Multiple readers** | Wrong reader opened | Enumerate via `IC_InitComm(port)` with different ports |
| **MS CCID → NO_SMARTCARD (0x6)** | `SCardConnect(DIRECT)` returns 0x6 on sync cards | MS CCID tries ISO 7816 ATR negotiation which fails — **no workaround**, must use vendor driver |
| **WUDF CCID no CCID_ESCAPE** | `DeviceIoControl(SCARD_CTL_CODE+0x004)` → err=1 | WUDF CCID driver only responds to 0x028 (ack) and 0x038 (version=2) — cannot send raw CCID commands |
| **Secure Boot blocks test signing** | `bcdedit /set testsigning on` → "protected by Secure Boot" | Must disable Secure Boot in UEFI BIOS first, or buy reader with WHQL-signed INF |
| **Registry force-bind reverts** | Set `Service=SzCCID` but PnP restores WUDFRd on enable | PnP matches `USB\Class_0B` CompatibleID to highest-ranked signed driver — registry edits don't stick |

---

## 7. DEBUGGING CHECKLIST

1. **Confirm DLL exports** — `dumpbin /exports CTAlc001.dll` shows `IC_InitComm`, `IC_Check_4442`, etc.
2. **Test in vendor tool first** — Run SimEdit / DCULC Reader → if it works, DLL is good
3. **Minimal ctypes test** — Load DLL, call `IC_InitComm(100)`, check handle > 0
4. **Card detection** — `IC_Check_4442(handle) == 0` means card present
5. **Type init** — `IC_InitType(handle, 0x10) == 0` before any read/write
6. **PIN verify** — `IC_CheckPass_4442hex(handle, b"ffffff\x00") == 0`
7. **Read** — `IC_Read(handle, 0, 256, buffer) == 0`

---

## 8. RELATED SKILLS

- `digital-forensics` — when the challenge involves smart card data extraction
- `flipper-zero-backup` — Flipper can also read SLE4442 via GPIO/UART
- `hardware/esp32-nrf24-jammer-builder` — RF side-channel perspective

---

*Maintained by Nous Research. Add new vendor DLL mappings and API signatures as discovered.*