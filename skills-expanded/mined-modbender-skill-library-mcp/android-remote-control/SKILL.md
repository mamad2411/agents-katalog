---
name: android-remote-control
description: Զ̿ Android 豸ֽ֧ͼ App ʹ uiautomator2 Ϊײ棬ͨ ADB 豸ûҪ(1) 鿴ֻĻ(2) Զֻ App(3) Զ̰װ/ж(4) 豸Эʱʹô˼ܡ
---

# Android Remote Control (׿Զ̷)

ͨ `uiautomator2` ʵֶ Android 豸Զ̲ٿء

## ?? Ĺ߽ű

- **λ**: `scripts/remote_control.py`
- ****:
  - `snap [path]`: ȡĻͼ
  - `click <x> <y>`: ָ
  - `start <package_name>`: ָ App

## ? ָ

### 1. 豸
ȷֻѿUSB ԡҵʶ豸
Ĭ ADB ·Ϊ`C:\Program Files (x86)\Camo Studio\Adb`

### 2. òָ
- **ͼԤ**: 
  ```bash
  python scripts/remote_control.py snap workspace/last_snap.jpg
  ```
- **Ӿ**:
  ȽͼʹӾģͣ Qwen-VLλִ꣬У
  ```bash
  python scripts/remote_control.py click 0.5 0.5
  ```

### 3. ע
- ״ʹÿҪֻȷϡ USB ԡ
-  `node command not allowed`  Gateway İȫԡ
