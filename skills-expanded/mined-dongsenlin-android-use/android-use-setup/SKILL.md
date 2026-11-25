---
name: android-use-setup
description: 安装、配对和排查 Android Use（让 Agent 经 Wi‑Fi 操作安卓手机）。用户要"装安卓 use / 连接我的安卓手机 / 配对手机"、给出 androiduse:// 配对信息，或 android_* 工具报 not_paired、phone_refused、phone_unreachable、phone_timeout、unauthorized、截屏失败时使用。
---

# 安装与配对 Android Use

整套由两部分组成：手机上的 **Android Use App**（无障碍服务 + 局域网接口），电脑上的 **android_use MCP 服务**（本插件）。不需要 ADB、不需要开发者模式、不用插线；手机和电脑在同一个 Wi‑Fi 即可。

先调 `android_setup(action="status")` 看现状：已配对且 `reachable=true` 就直接 `android_ready`，不要重装。

## 第一次安装（需要用户在手机上操作）

把下面步骤原样告诉用户，每一步等用户说完成再继续：

1. **装 App**：安装包从 GitHub Releases 下载（`android-use-<版本>.apk`），或在源码目录运行 `sh app/build.sh` 自己打包到 `dist/`。传到手机的办法任选：在源码目录运行 `python3 scripts/serve_apk.py`，用手机浏览器打开它打印的地址下载；或用微信 / QQ 文件传输、网盘；有 adb 的话 `adb install`。安装时允许"安装未知来源应用"，Play 保护机制拦截时选「仍然安装」。要求 Android 11 及以上（截屏能力需要）。
2. **开无障碍**：打开 Android Use，点「去开启」→ 已下载的应用（或"已安装的服务"）→ Android Use → 开启并确认。
   - 开关是灰的、提示"受限制的设置"：回到 App 点「应用信息」→ 右上角 ⋮ →「允许受限制的设置」，再去开启（Android 13 起对浏览器 / 文件管理器装的 App 都这样）。
3. **打开「允许 Agent 远程控制」**，看到"正在监听端口 8787"。手机顶部会出现紫色提示条。
4. **复制配对信息**：点「复制配对信息」，把 `androiduse://IP:8787/?token=…` 发给你（用户可以直接粘贴到对话里）。
5. 你调用 `android_setup(action="pair", pairing="androiduse://…")`，成功后 `android_ready`。

配对码相当于遥控器钥匙：只在本对话里使用，不要写进文件、提交到 Git 或转述给第三方。手机上点「换一个配对码」后旧码立即失效。

## 常见问题

| 报错 / 现象 | 原因与处理 |
| --- | --- |
| `not_paired` | 还没配对，按上面第 4、5 步。 |
| `phone_refused`（拒绝连接）、`remote_paused` | App 的远程控制没开，或无障碍服务被系统关掉了。刚才还在用、突然断开的，多半是有人点了顶部紫色提示条（点一下就暂停）。请用户打开 App 看第 ① ② 项状态，重新打开远程控制。 |
| `phone_unreachable` / `phone_timeout` | ① 手机和电脑不在同一 Wi‑Fi（访客网络、AP 隔离、公司网常见）；② **macOS 本地网络权限**：系统设置 → 隐私与安全性 → 本地网络，打开 Codex / Claude / 终端 / VS Code 中正在运行本服务的那个；③ 手机 IP 变了：重新复制配对信息再 pair。连 `curl http://手机IP:8787/v1/ping` 都不通时就是网络问题。 |
| `unauthorized` | 手机上换过配对码，重新复制配对信息再 pair。 |
| 一会儿就断、无障碍自己关掉 | 国产系统杀后台：让用户把 Android Use 设为电池「无限制」、允许自启动、在最近任务里锁定（App 第 ④ 项有入口）。 |
| `screenshot_failed`（禁止截屏） | 支付、银行、密码页设置了防截屏，改读控件树或请用户自己操作。 |
| 截屏不支持 | Android 10 及以下没有无障碍截屏，只能读控件树。 |
| 想走 USB / 网络不通 | 有 adb 时：`adb forward tcp:8787 tcp:8787`，然后 `android_setup(action="pair", url="127.0.0.1:8787", token=…)`。 |

`android_doctor` 会逐层检查（配置 → 网络 → 配对码 → 屏幕与锁屏）并给出下一步，排查时先跑它。

## 卸载 / 停用

- 临时停用：手机顶部提示条点一下，或 App 里关掉远程控制。
- 彻底删除：手机上卸载 Android Use；电脑上 `android_setup(action="forget")` 删除配对，再运行源码目录的 `scripts/uninstall.sh` 移除插件。
