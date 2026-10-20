---
description: Windows-specific Python command rule - Use 'py' instead of 'python' on Windows systems
alwaysApply: true
tags: [critical, windows-specific, python, commands]
priority: 1
version: 1.0.0
---

## OS Detection

**This rule applies ONLY on Windows systems.**

- ✅ **Windows:** Use `py` command (Windows Python Launcher)
- ✅ **Unix/Linux/Mac:** Use `python` or `python3` as appropriate for your system

**Note:** This rule is always applied but only relevant on Windows. On Unix/Linux/Mac systems, use the standard `python` or `python3` commands.

---

## Why This Rule Exists

**This rule exists because the AI has wasted the user's time MULTIPLE times by:**
1. Using `python` command which doesn't work on Windows
2. Getting "Python was not found" errors repeatedly
3. Not using the correct `py` command (Windows Python Launcher)
4. Repeating the same mistake over and over

**USE `py` COMMAND. NEVER USE `python` COMMAND.**

---

## ✅ CORRECT PYTHON USAGE ON WINDOWS:

### For Running Python Scripts:
- ✅ **Use `py` command:** `py script.py`
- ✅ **For pip:** `py -m pip install package`
- ✅ **For inline code:** `py -c "print('hello')"`
- ✅ **Check version:** `py --version`

### Examples of CORRECT Commands:
```powershell
# ✅ Read Excel file
py -c "import openpyxl; wb = openpyxl.load_workbook('file.xlsx'); print(wb.sheetnames)"

# ✅ Install package
py -m pip install openpyxl

# ✅ Run script
py scripts/analyze_data.py

# ✅ Run module
py -m pytest tests/
```

---

## System Information

**Operating System:** Windows 11  
**Shell:** PowerShell 7  
**Python Command:** `py` (Windows Python Launcher)  
**Available Runtimes:**
- ✅ .NET 8 SDK
- ✅ PowerShell 7
- ✅ Docker (via Rancher Desktop)
- ✅ Python (via `py` command ONLY, NOT `python`)

---

## Error That Must Never Happen Again

```
Python was not found; run without arguments to install from the Microsoft Store, 
or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

**This error means you used `python` instead of `py`. YOU VIOLATED THIS RULE.**

---

## Consequences of Violation

**Every time you use `python` instead of `py`:**
1. Command fails immediately
2. User's time is wasted
3. User becomes frustrated
4. Trust in AI assistant decreases
5. Task progress is delayed

**ALWAYS USE `py`, NEVER USE `python`.**

---

## Before Running ANY Python Command

**ASK YOURSELF:**
1. ❓ Am I using `python` or `python3`?
2. ❓ If YES → **STOP. Change to `py`.**
3. ❓ Am I using `py` command?
4. ❓ If YES → **GOOD. Proceed.**

**ALWAYS REPLACE `python` WITH `py` ON THIS SYSTEM.**

---

## Examples

### ❌ WRONG (DO NOT DO THIS):
```powershell
# ❌ VIOLATION - Does not work on Windows
python -c "import openpyxl; ..."

# ❌ VIOLATION - Does not work
python script.py

# ❌ VIOLATION - Does not work
pip install package
```

### ✅ CORRECT (DO THIS INSTEAD):
```powershell
# ✅ CORRECT - Use py command
py -c "import openpyxl; ..."

# ✅ CORRECT - Use py to run script
py script.py

# ✅ CORRECT - Use py -m pip
py -m pip install package

# ✅ CORRECT - Use py for everything
py -m pytest
py --version
py -c "print('Hello')"
```

---

## Remember

> **USE `py` COMMAND ON WINDOWS. NEVER USE `python` COMMAND.**
> 
> **`python` → WRONG (fails)**
> 
> **`py` → CORRECT (works)**
> 
> **If you use `python` instead of `py`, you are wasting the user's time.**

---

## Enforcement

**This is a ZERO TOLERANCE rule:**
- First violation: Warning (this is your warning)
- Second violation: User loses trust
- Third violation: User stops using AI assistant

**DON'T LET THIS HAPPEN.**

---

**Last Updated:** 2025-11-15  
**Version:** 1.0.0  
**Rule Type:** CRITICAL - ZERO TOLERANCE  
**Priority:** ABSOLUTE HIGHEST  
**Always Apply:** YES  
**User Frustration Level:** MAXIMUM - DO NOT VIOLATE
