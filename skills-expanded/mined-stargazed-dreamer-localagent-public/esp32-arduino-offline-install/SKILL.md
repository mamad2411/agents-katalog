---
name: esp32-arduino-offline-install
description: Arduino IDE / arduino-cli 装 ESP32 板包极慢时，用 gh-proxy 镜像预下载到 staging 再离线安装的完整流程（Windows 实测有效）
task_type: daily.esp32_arduino_offline_install
---

# ESP32 Arduino 板包离线快速安装（Windows）

## 适用场景

Arduino IDE 2.x 里安装 "esp32 by Espressif Systems" 卡在下载（国内典型 ~150KB/s，全套 1.8GB+ 要 3 小时）。
加速器（Watt Toolkit/Steam++ 等）帮不上忙：IDE 内置 arduino-cli **不走系统代理**，且 hosts 劫持式加速节点实测更慢。

## 原理

arduino-cli 安装前会检查缓存目录 `%LOCALAPPDATA%\Arduino15\staging\packages\`，文件名与索引一致且大小正确就直接用，不再联网。

## 流程

1. **测速选镜像**：对大文件 URL 做 Range 测速，实测 `https://gh-proxy.com/` 前缀 ~1.8MB/s（ghfast.top 371KB/s，直连/Watt Toolkit 136KB/s）。URL 拼接方式：`https://gh-proxy.com/<原始github URL>`。
2. **拿索引**：下载 `https://espressif.github.io/arduino-esp32/package_esp32_index.json`（620KB，可直连）。
3. **生成清单**：解析索引，取目标 platform version 的 `toolsDependencies`，匹配 host=`x86_64-mingw32` 的 systems 条目，得到 URL + archiveFileName + size。dfu-util（packager=arduino）不在该索引，体积小可让 CLI 自己下。
4. **批量下载**：`curl -L -C - --retry 5 -o "<staging>/packages/<archiveFileName>" "https://gh-proxy.com/<url>"`，按索引里的 size 字段校验，不符就断点续传重试。
5. **离线安装**：IDE 自带 CLI（`C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe`）：
   `arduino-cli core install esp32:esp32 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json`
   预下载的会全部显示 "already downloaded"。

## 坑

- **命令行编译报 `cc1plus.exe: fatal error: @C:\Windows\TEMP\xxx: Invalid argument`**：会话 TEMP/TMP 指向系统目录导致编译器读响应文件失败。编译前先 `$env:TEMP='<user_home>\AppData\Local\Temp'; $env:TMP=$env:TEMP`（PowerShell）或 `export TMP/TEMP`（bash）。Arduino IDE 图形界面不受影响（自己管理环境）。
- esp32 全套 16 文件 ≈1.8GB，staging 缓存装完可删（解压后在 `Arduino15\packages\`）。
- Watt Toolkit 的 hosts 劫持会把 github.com 解析到 127.0.0.1，若其节点不稳会拖慢所有走 GitHub 的程序，排查网速时记得先查它。
