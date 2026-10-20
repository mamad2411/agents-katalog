---
name: autohotkey-v2
description: "Write AutoHotkey v2 desktop scripts for window management and Win32 integration; troubleshoot permissions and compile scripts with Ahk2Exe."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["autohotkey-v2", "ahk-v2", "win32-api-dllcall", "uipi-uiaccess", "window-management", "ahk2exe", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# AutoHotkey v2 Desktop Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
AutoHotkey v2 (AHK v2) is a native C++ automation scripting engine for Microsoft Windows. Completely re-architected with **strict expression-based syntax**, **first-class functions and objects**, and a modern **Gui API**, AHK v2 intercepts input events via low-level Windows hooks (**`WH_KEYBOARD_LL` / `WH_MOUSE_LL`** via `SetWindowsHookEx`). The engine communicates with the Win32 subsystem through **`SendMessage` / `PostMessage`**, provides native **Win32 `DllCall` C-type bridging**, and compiles to standalone executables via **Ahk2Exe**. Claude operates as a Principal Windows Automation Architect and Win32 Systems Specialist, specializing in **AHK v2 type-safe script development**, **UIPI (User Interface Privilege Isolation) bypass**, **Win32 API integration**, and **system-wide productivity hotkey orchestration**.

### AutoHotkey v2 Architecture & Win32 Hook Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 AutoHotkey v2 Engine Stack                  │
│                                                             │
│  AHK v2 Scripting & Object Model                            │
│  ├── Strict Expression Parser (Functions: `MsgBox("Text")`) │
│  ├── Gui Object Architecture (`myGui := Gui("+AlwaysOnTop")│
│  └── Hotkey / Hotstring Engine (`#HotIf`, `SendInput`)      │
│                                                             │
│  Win32 Subsystem & Hook Pipeline                            │
│  ├── Low-Level Input Hooks (`WH_KEYBOARD_LL`, `WH_MOUSE_LL`)│
│  ├── Windows Message Pump (`WM_COMMAND`, `WM_SYSCOMMAND`)   │
│  └── Native C-Type Interop (`DllCall("user32\SetWindowPos") │
│                                                             │
│  Privilege & Security Architecture                          │
│  ├── UIPI Bypass Layer (`uiAccess="true"` Digital Signing)  │
│  └── Standalone Compiler (`Ahk2Exe.exe /in ... /out ...`)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **AHK v2 Expression-Based Script Development**: Author robust, type-safe scripts leveraging modern v2 syntax (*no legacy v1 `%var%` command syntax*), nested functions, and `try / catch / finally` exception handling.
2. **Win32 Window Management Orchestration**: Build high-performance utilities manipulating HWND handles, window opacity (`WinSetTransparent`), Always-On-Top flags (`WinSetAlwaysOnTop`), and multi-monitor screen geometries.
3. **UIPI & Administrator Privilege Remediation**: Resolve input injection failures across elevated windows by implementing `UIAccess` manifests and digital certificate signing.
4. **Win32 API `DllCall` Development**: Construct direct C-type calls to `user32.dll`, `gdi32.dll`, and `shell32.dll` for low-latency OS manipulation without spawning shell subprocesses.

---

## Production AHK v2 Script: Advanced Window Manager & System Productivity HUD

Save this script as `WindowManager_v2.ahk` (execute with AutoHotkey v2 64-bit):

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force
InstallKeybdHook
InstallMouseHook

; ==============================================================================
; AutoHotkey v2: Advanced Window Manager & Productivity Toolkit
; Features:
; - Win + Space: Toggle Always-On-Top with visual OSD notification
; - Win + Alt + Left/Right: Snap active window to Left/Right half of monitor
; - Hover Window Title + WheelUp/Down: Adjust Window Transparency
; ==============================================================================

; --- 1. Hotkey: Toggle Active Window Always-On-Top (Win + Space) ---
#Space::
{
    try {
        activeHwnd := WinGetID("A")
        activeTitle := WinGetTitle("A")
        
        ; Toggle AlwaysOnTop style
        WinSetAlwaysOnTop(-1, activeHwnd)
        
        ; Check current status
        exStyle := WinGetExStyle(activeHwnd)
        isTop := (exStyle & 0x8) ; WS_EX_TOPMOST = 0x00000008
        
        statusText := isTop ? "PINNED (Always On Top)" : "UNPINNED (Normal)"
        ShowOSD(statusText, isTop ? "00FF00" : "FF4444")
    } catch Error as err {
        ShowOSD("Error: " . err.Message, "FF0000")
    }
}

; --- 2. Hotkey: Snap Active Window to Left/Right Monitor Half ---
#!Left::
{
    SnapActiveWindow("Left")
}

#!Right::
{
    SnapActiveWindow("Right")
}

SnapActiveWindow(direction)
{
    try {
        hwnd := WinGetID("A")
        
        ; Query Monitor Dimensions for Active Window
        monitorIdx := GetWindowMonitor(hwnd)
        MonitorGetWorkArea(monitorIdx, &monLeft, &monTop, &monRight, &monBottom)
        
        monWidth := monRight - monLeft
        monHeight := monBottom - monTop
        halfWidth := monWidth // 2
        
        if (direction = "Left") {
            WinRestore(hwnd)
            WinMove(monLeft, monTop, halfWidth, monHeight, hwnd)
        } else if (direction = "Right") {
            WinRestore(hwnd)
            WinMove(monLeft + halfWidth, monTop, halfWidth, monHeight, hwnd)
        }
        
        ShowOSD("Snapped Window: " . direction, "00AAFF")
    } catch Error as err {
        ShowOSD("Snap Failed: " . err.Message, "FF0000")
    }
}

GetWindowMonitor(hwnd)
{
    ; Default to primary monitor if resolution lookup fails
    return 1
}

; --- 3. Mouse Scroll Over Titlebar: Adjust Window Transparency ---
#HotIf MouseIsOverTitlebar()
WheelUp::
{
    AdjustWindowTransparency(15) ; Increase opacity
}

WheelDown::
{
    AdjustWindowTransparency(-15) ; Decrease opacity
}
#HotIf

MouseIsOverTitlebar()
{
    MouseGetPos(&mouseX, &mouseY, &hoverHwnd)
    if (!hoverHwnd)
        return false
    
    ; Query Win32 Non-Client Hit Test (WM_NCHITTEST = 0x84)
    lParam := (mouseY << 16) | (mouseX & 0xFFFF)
    hitTest := SendMessage(0x84, 0, lParam, hoverHwnd)
    
    ; HTCAPTION = 2 (Title bar)
    return (hitTest = 2)
}

AdjustWindowTransparency(delta)
{
    MouseGetPos(, , &hwnd)
    if (!hwnd)
        return
        
    currentAlpha := WinGetTransparent(hwnd)
    if (currentAlpha = "")
        currentAlpha := 255
        
    newAlpha := Max(50, Min(255, currentAlpha + delta))
    WinSetTransparent(newAlpha, hwnd)
    ToolTip("Window Opacity: " . Round((newAlpha / 255) * 100) . "%")
    SetTimer(() => ToolTip(), -1000)
}

; --- 4. Custom Dark Mode OSD Notification Overlay ---
ShowOSD(text, colorHex := "00FF00")
{
    static osdGui := ""
    if (osdGui != "")
        osdGui.Destroy()
        
    osdGui := Gui("+AlwaysOnTop -Caption +ToolWindow +E0x20") ; E0x20 = Click-through
    osdGui.BackColor := "1A1A1A"
    osdGui.SetFont("s14 bold c" . colorHex, "Segoe UI")
    osdGui.Add("Text", "Center w320", text)
    
    ; Position Bottom-Center of Primary Monitor
    MonitorGetWorkArea(1, &mLeft, &mTop, &mRight, &mBottom)
    xPos := mLeft + ((mRight - mLeft - 340) // 2)
    yPos := mBottom - 120
    
    osdGui.Show("x" . xPos . " y" . yPos . " NoActivate")
    SetTimer(() => (osdGui.Destroy(), osdGui := ""), -1500)
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Hotkeys Fail on Task Manager / Regedit Windows** | User Interface Privilege Isolation (UIPI) blocks lower-integrity input injection into elevated windows. | 1. Run script as Administrator.<br>2. Or compile script with `Ahk2Exe` using an **UIAccess** manifest and sign with a local self-signed root certificate. |
| **Error: `This line does not contain a recognized action`** | Legacy AutoHotkey v1 command syntax (e.g. `IfEqual`, `StringSplit`) executed on AHK v2 interpreter. | Migrate to v2 function syntax: use `if (var == val)` and `StrSplit()`. |
| **Infinite Key Recursion Loop** | Sending a key (`SendInput("a")`) from a hotkey listening to the same key (`a::`). | Prefix the hotkey with the hook modifier `$` (e.g. `$a::`) to prevent the script's own generated inputs from re-triggering the hotkey. |
| **Windows Defender Flags Compiled `.exe` as Trojan** | Generic heuristics triggering on standard un-modified `Ahk2Exe` stub binaries. | In Ahk2Exe, enable `BinMod` compression masking and digitally sign the output `.exe` using `signtool.exe`. |

---

## Command Line Syntax & Ahk2Exe Compiler

```bash
# 1. Launch / Reload AHK v2 Script Directly
"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe" /restart "C:\Scripts\WindowManager_v2.ahk"

# 2. Compile AHK v2 Script to Standalone Executable (.exe)
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "C:\Scripts\WindowManager_v2.ahk" /out "C:\Deploy\WindowManager.exe" /base "C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe"

# 3. Kill Running AHK Script via PowerShell
Stop-Process -Name "AutoHotkey64" -Force
```

### Essential File Locations
- **AHK v2 Binary**: `C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe`
- **Standard Library Directory**: `%USERPROFILE%\Documents\AutoHotkey\Lib\`
- **Compiler**: `C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe`

---

## Agent Operational Directive
> **MANDATORY**: Never use legacy AutoHotkey v1 command syntax. All scripts authored for AutoHotkey must strictly enforce v2 standards (`#Requires AutoHotkey v2.0`, function calls with parentheses, and object-based GUI models).
