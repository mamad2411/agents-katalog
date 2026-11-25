---
name: disk_manager
description: >
  磁盘空间分析与清理建议、系统环境全面备份（浏览器/游戏存档/桌面/系统设置/文件关联）、
  设置看门狗（PATH/环境变量、默认浏览器/URL协议、开机自启、Winlogon登录劫持 等"会被偷改"的机器设置的 快照/篡改对比/恢复）。
  触发词：清理硬盘、磁盘清理、空间不足、备份系统、环境备份、游戏存档备份、SpaceSniffer、sns快照、文件关联、默认打开程序、默认应用被改、恢复关联、环境变量被改、PATH被篡改、默认浏览器被改、开机自启、自启项、URL协议、设置看门狗、Winlogon、登录劫持、开机shell、Userinit、系统迁移、换机、WiFi密码、浏览器密码导出、壁纸备份、输入法词库、防火墙规则导出、计划任务导出、驱动离线备份、IDE配置迁移。
  当用户提到磁盘空间、清理垃圾文件、备份电脑环境、系统迁移/换机、后缀默认程序/默认浏览器/PATH/自启被偷改或想还原时触发。
  ⚠️ 全面备份功能未经测试，执行时必须提醒用户并全程跟进；凭据组会以明文导出密码/token，须先与用户确认。
task_type: adhoc.disk_cleanup
---

# 磁盘管理 Skill

## 概述

协助清理硬盘空间和全面备份系统，所有操作必须经过用户审核确认，**绝不擅自删除或移动任何文件**。

> **⚠️ 未测试提醒：全面备份功能（`backup_env.py` 的全量备份模式）尚未经过实际测试。**
> 当用户要求执行全面备份时，必须明确告知此功能未测试，执行过程中需全程跟进并记录问题。

---

## 软件名称对应关系
```
.lmstudio / lm-studio-updater     → LM Studio（已卸载）
.paddlex                           → PaddleX
.lingma                            → 通义灵码
.catpawai / CatPawAI               → CatPawAI
.codex                             → OpenAI Codex
.qq-chat-exporter                  → QQ聊天导出工具
.abdm                              → ABDownloader（在用）
.trae-cn / .trae                   → Trae AI（在用）
.secoresdk / 360se6               → 360安全浏览器（已卸载）
.GreenCore7z / greencore           → 360安全浏览器（已卸载）
.360safe                           → 360安全卫士
.KRLauncher                        → 鸣潮启动器（在用，不删）
.ima.copilot / ima.copilot         → 知识库工具（在用）
.sankuai                           → 美团内部工具
HT                                 → 异环游戏（在用，不删）
GeePlayer                          → 爱奇艺播放器
EBWebView                          → Outlook内嵌浏览器
.modelscope                        → ModelScope模型
.cache\huggingface                 → HuggingFace模型
.cache\puppeteer                   → Chromium/Puppeteer
.cache\modelscope                  → ModelScope模型缓存
QQMusicCache                       → QQ音乐播放缓存（可达10GB+）
```

---

## 一、文件清理方案

### 铁律
1. **所有操作必须用户审核确认** - 脚本只生成报告和建议，不执行任何删除/移动
2. **尽量减少磁盘扫描** - 使用轻量级扫描策略，避免全盘遍历
3. **分类清晰** - 每个建议都标注原因和风险等级
4. **★ 开清理前先翻 `pending_decisions.md` 并逐条反问** - 那里登记了「用户不敢删 / 拿不准」的资产。
   **目的**：用户不必每次重扫全盘才想起某处留了一坨。规则：
   - 状态为 `待反问` / `暂缓` 的条目，**必须向用户复述 + 反问**，按答复更新该文件的「决策史」
   - 未获答复的条目**一律不进删除清单**，也不计入「可释放空间」
   - 状态为 `永久保留` 的条目，**不再反问**（如异环/鸣潮标注「在用，不删」）
   - 新发现的大块拿不准资产 → 按同样格式登记进去，别只在当次会话里提一句

### 用户的清理决策判据（2026-09-24 从用户手写清单提炼，给建议时**先用这套预判**）

用户判断「能不能删」从来不靠体量，靠的是下面九条。给建议时套一遍，能显著提高命中率：

| # | 判据 | 用户原话 | 怎么落到建议里 |
|---|---|---|---|
| 1 | **有冷备份 = 可删** | 「有冷备份可删」 | 看到大目录，**第一件事**查别处有无备份/副本，别先问「还有用吗」 |
| 2 | **偶尔用 ≠ 现在删** | `.phone`「有时候可能需要调些图，所以留在最后」 | 分「常用→偶尔→不看」三段渐进；偶尔用的**现在不删但要记得问**（进台账） |
| 3 | **使命完结 = 直接删** | ISO「已安装的大件垃圾」、MemoTrace「自己 decode 可用后」 | 判据是**功能是否被替代**，不是占多大 |
| 4 | **不知道是什么 → 先搞清楚再删** | `Microsoft_Visual_Studio`「想清理但不清楚是什么」 | 这类**先补一段说明再给勾**，绝不靠名字猜 |
| 5 | **留重装能力、删安装过程** | 「UnityDownload.zip 得留着作为重装的备份」 | 程序/环境类**默认保留离线安装包**，只删临时解压物 |
| 6 | **同类软件要收敛** | 「两个微信以后只用一个」 | 发现功能重复的东西，主动问「是不是该二选一」 |
| 7 | **优先「文件少、块头大」的** | 「清理效率高」 | 算 **GiB ÷ 文件数**，「几个文件换几 GiB」的排最前 |
| 8 | **中间产物必须自己擦屁股** | 「这怎么老是冒出来……乱七八糟的东西太多」 | 构建/staging/解码中间目录**默认应自清理**；留在盘上算缺陷，要顺藤摸瓜修源头 |
| 9 | **模型类资产：查引用，不看大小** | 「我更好奇 qwen 的谁在用」 | 先看 `<models_root>\model_registry.json` 的 `referenced_by` / `orphaned_models`，再查 `docs/adr/` 有没有移除记录。**最大的那块往往最没用**（实测：14 GiB 的 Qwen 零引用，0.85 GiB 的 Florence-2-large 却必须留）；HF hub 必查 `models--*` 是 `snapshots`/`blobs` 硬链接，**只有删整个 `models--<name>` 才释放** |
| 10 | **48h 活跃规则** | 「我是让你选里面要用的，比如最近读过的」 | **选旧删新**：缓存类按**文件粒度**删 mtime >48h 的、保留 48h 内活跃的（DXCache 实证：208 旧文件删、51 个新的留）。不是整项跳过 |
| 11 | **软件难用 ≠ 数据可删** | Sandboxie rubbish「要的，我只是觉得这些软件很差劲但是不得不用」 | 去留只看「还要不要用」，不看评价 |

> **★ 第 8 条的延展（本次最重要的收获）**：用户眼中的「清理」不只是删文件，
> 还包括**堵住不断产生垃圾的那个源头**。发现反复出现的中间产物时，除了删当前的，
> 还要定位生成它的代码路径并给出修复建议 —— 只删不治会被当成没解决问题。

**给用户的交付形式**：必须是**可直接勾选的 `- [ ]` 清单**，每条带「大小 + 我的建议标记 + 依据」。
不要只给散文式结论 —— 用户明确反馈过「你说了一堆我也没法告诉你哪个我想删」。
标记用 `[建议]` / `[建议不勾]` / `[待条件]` / `[先答你]` 四档。

**⛔ 用户回传勾选结果后，必须用 `diff` 提取改动，不许肉眼看**。

**⚠ 用户在清单里的行间批注是对着「上面一行」说的**（09-24 实证：批注写在
「[x] DXCache」的下一行，实际约束的是 DXCache 而非下面那行）——按行号
`hunk 新行号 = 批注行`，其约束对象是**批注行的上一行**，配对错了会删错东西。

用户习惯「留原版 + 改副本」（`xxx.md` 旁边放 `xxx (2).md`），原话：
> 「你注意力不够用就别自己看，去用diff一查不就知道我改了文档什么吗，我特意留了原版给你的」

```
diff -u "temp/删除名单_v2.md" "temp/删除名单_v2 (2).md"
```

肉眼会漏勾 —— 实测漏过 B1/B2 两个已勾项，且漏掉的恰恰是要执行的操作。

**⛔ 删除默认只走到「回收站」，永久删由用户自己清**。

原话：「我觉得要不还是走回收站，我自己清回收站以防你命令写错，以前出过这种事。」
⇒ 就算用户在清单里勾了「永久删」，执行前也要**把条目 ID 摊开核对一遍再征询**，别一次性不可逆到底。

### 空间分析工作流（scan → drill → find → dry-run → delete）

用户说"清理磁盘/空间不足"时，走以下闭环：

**Step -1（必做，先于一切分析）: 翻 `pending_decisions.md`，把拿不准的项反问用户**

见上方铁律 4。这一环绝不能跳过 —— 跳过就等于让用户重新想起那些「当时说不清为什么留着」的东西。

**Step 0（推荐起点）: 有 .sns 快照则导入，跳过 live scan**

用户有 SpaceSniffer 导出的 .sns 快照（或愿意先开 SpaceSniffer 扫一遍盘导出）时，优先走快照导入——GUI 并行扫描 + 二进制导入，等效一次全盘 Python scan，且零磁盘 IO、无截断、可离线反复分析：

```
parse_sns.py parse <快照.sns> --json          # 导入 → temp/disk_scan_cache/sns_*.json
scan_disk.py tree --cache <cache_path> -n 10   # Step 1 以下查询全部复用 scan_disk，只是加 --cache
scan_disk.py caches --cache <cache_path>       # 缓存清单直接匹配
scan_disk.py files --cache <cache_path> -n 20  # 大文件
```

- 快照是全量扫描结果（导入结果 `unknown_bytes=0` 即完整），比 live scan 的硬上限截断更可信
  - ⚠ 但 `unknown_bytes=0` **不等于扫全了**：权限不足时受保护目录压根不会被枚举，此时
    「卷 used − Σ顶层子项」会差出几十 GiB。超过 ~8 GiB 就用 elective 提示怀疑这份快照。
- 快照体积 ≈ 盘内容 0.06%（百万级文件 ≈ 67MB），建议清理前后各留一份做对比
- 没有快照、或只分析局部目录时，回退 Step 1 的 live scan
- .sns 二进制格式规范见 `references/sns_format.md`；解析失败会报结构违例（截断/栈不平衡），此时不要信任该快照
- **★ 分析阶段一律以快照为准，不要对照真实文件系统**（用户 2026-09-24 拍定的口径）
  - 理由：磁盘分析的价值在于「一次导入、反复离线分析」，实时 `os.path.exists` / `stat`
    校验既慢又会把结论绑定在当时的盘状态上
  - 快照内就能判断的事就在快照内判：例如「压缩包有没有被解压过」用快照收集的目录路径集去比对，
    不要去 stat 磁盘
  - **唯一例外：真正执行删除之前**，必须确认目标仍在预期路径上，然后才动手

**Step 1: scan — 空间概览（无快照时）**
```
scan_disk.py scan <path> --json
```
单次物理遍历建缓存（JSON 输出 `cache_path`），紧凑 tree 快速定位大目录。

**Step 2: drill — 下钻定位**
```
scan_disk.py tree --cache <cache_path> --path <大目录> --depth 5
```
对 scan/导入发现的大目录下钻（`--path` 前缀过滤），收窄看更细的 tree。注意 `--cache` 必传：slug 匹配按 scan 根路径生成，下钻路径不同会查不到。

**Step 3: find — 按目录名定位（可选）**
```
scan_disk.py find --cache <cache_path> --names node_modules .venv __pycache__
```
全树搜指定目录名，返回路径+大小，适合批量定位已知费空间目录。

**Step 4: dry-run — 出清理回执**
```
cleanup.py --dry-run --json
```
拿到逐项可回收字节回执（id/path/size_bytes/size_human），不删任何文件。

**Step 5: 用户勾选 → delete**
```
cleanup.py --delete --items cache-0,cache-3,cache-6 --json
```
用 AskUserQuestion 把 dry-run 回执交给用户勾选，只删确认项，走 ctypes 回收站（可恢复）。

**补充：**
- Chrome缓存提醒用户用 `chrome://settings/clearBrowserData` 清理
- E/F盘用户自行管理，不干预
- 需要找最大单个文件时用 `scan_disk.py files --cache <cache_path> -n 10`
- 缓存目录批量匹配用 `scan_disk.py caches --cache <cache_path>`（内置清单：node_modules/.venv/DXCache/Temp/updater 等 30+ 类）

### 定期清理清单（每次清理检查这些位置）

**第一梯队：安全删除，自动重建**
```
%LOCALAPPDATA%\NVIDIA\DXCache                                               # DX着色器缓存（可达15GB+）
%LOCALAPPDATA%\pip\cache                                                    # pip缓存（可达9GB+）
%LOCALAPPDATA%\npm-cache                                                    # npm缓存
%LOCALAPPDATA%\CrashDumps                                                   # 崩溃转储
%LOCALAPPDATA%\Temp                                                         # 临时文件
%APPDATA%\Tencent\WeChat\log                                                # 微信日志
%LOCALAPPDATA%\GameViewer\webviewcache                                      # 向日葵缓存
%LOCALAPPDATA%\Steam\htmlcache                                              # Steam商店缓存
%APPDATA%\Trae CN\logs                                                      # Trae日志
%APPDATA%\Tencent\WeChat\radium\WmpfCache                                   # 微信WmpfCache
%APPDATA%\Tencent\WeMeet\Global\Data\WebkitCacheData                        # 腾讯会议WebKit缓存
C:\ProgramData\NVIDIA Corporation\NVIDIA app\UpdateFramework\ota-artifacts  # NVIDIA驱动安装包（可达7GB+）
%LOCALAPPDATA%\NVIDIA Corporation\NVIDIA App\CefCache                       # NVIDIA App浏览器缓存
%LOCALAPPDATA%\NVIDIA Corporation\NVIDIA Overlay\CefCache                   # NVIDIA覆盖层缓存
%LOCALAPPDATA%\Microsoft\Windows\Explorer                                   # 缩略图缓存
<data_drive>:/<system_data_root>\QQMusicCache\downloadproxyNew\tp2p\.tpfs\duty     # QQ音乐播放缓存（可达10GB+）
```

**第二梯队：需关闭对应程序**
```
Chrome缓存 → chrome://settings/clearBrowserData（勾选缓存，所有时间）
```

**第三梯队：软件更新器（安装后可删）**
```
%LOCALAPPDATA%\*-updater  # 所有updater目录
```

**第四梯队：可选清理（删了会重建，但重建可能较慢）**
```
%LOCALAPPDATA%\Unity\cache                    # Unity包缓存（2.6GB+）
%LOCALAPPDATA%\Unity\npm                      # Unity包管理器缓存（921MB+）
%LOCALAPPDATA%\Microsoft\Olk\EBWebView        # Outlook WebView缓存（737MB+）
%APPDATA%\IQIYI Video\GeePlayer               # 爱奇艺播放器缓存（458MB+）
%USERPROFILE%\.cache\modelscope               # ModelScope模型缓存（2.2GB+）
%USERPROFILE%\.cache\huggingface              # HF模型缓存（1.5GB+）
%USERPROFILE%\.cache\puppeteer                # Chromium缓存（583MB+）
%LOCALAPPDATA%\Google\Chrome\User Data\Default\Service Worker\CacheStorage  # 网站缓存（3GB+）
%APPDATA%\Code\CachedExtensionVSIXs           # VS Code扩展缓存（648MB+）
```

**Windows系统清理命令**
```
dism /online /cleanup-image /startcomponentcleanup /resetbase  # 组件存储清理（释放assembly/Installer/LCU空间）
cleanmgr /d C                                                   # 磁盘清理工具
```

---

## 二、全面备份方案

### 设计理念

备份不仅仅是复制文件，而是**完整迁移一个工作环境**。目标是：换一台电脑，运行恢复脚本后，能快速恢复到熟悉的工作状态。

### 备份层次

```
┌─────────────────────────────────────────┐
│  L1: 文件同步（已有filesync）             │  ← 你已有
├─────────────────────────────────────────┤
│  L2: 系统环境备份（新增）                  │  ← 本次设计
│  - 浏览器数据（书签/扩展/密码/设置）        │
│  - 游戏存档                              │
│  - 桌面布局                              │
│  - 系统设置/注册表                        │
│  - 已安装软件列表                         │
├─────────────────────────────────────────┤
│  L3: 一键恢复脚本（新增）                  │  ← 本次设计
│  - 自动恢复L2备份项                       │
│  - 环境调整清单（需手动确认的项）           │
└─────────────────────────────────────────┘
```

### L2: 系统环境备份详情

#### 1. 浏览器数据

| 数据 | Chrome路径 | 备份方式 |
|------|-----------|----------|
| 书签 | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks` | 直接复制 |
| 扩展列表 | `chrome://extensions` 导出ID列表 | 脚本提取 |
| 密码 | Chrome不提供明文导出，需用户手动导出CSV | 提示用户 |
| 搜索引擎 | `Preferences` JSON中的`search_engines` | 直接复制 |
| 油猴脚本 | `Extensions\*tampermonkey*\` | 直接复制 |

#### 2. 游戏存档

| 游戏/平台 | 存档位置 |
|-----------|----------|
| Steam云存档 | 自动同步，无需备份 |
| Steam本地存档 | `C:\Program Files (x86)\Steam\userdata\` |
| Epic | `%LOCALAPPDATA%\Epic Games\*` |
| 单机游戏常见路径 | `%DOCUMENTS%\My Games\`, `%APPDATA%\*`, `%LOCALAPPDATA%\*` |
| 特殊游戏 | 需用户补充列表 |

#### 3. 桌面布局

| 数据 | 方式 |
|------|------|
| 桌面图标位置 | 注册表 `HKCU\Software\Microsoft\Windows\Shell\Bags` |
| 任务栏固定 | 注册表 + 快捷方式文件 |
| 开始菜单布局 | PowerShell导出 `Export-StartLayout` |

#### 4. 系统设置

| 数据 | 方式 |
|------|------|
| 环境变量 | `reg export "HKCU\Environment"` + `reg export "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"` |
| 右键菜单 | `HKCR\Directory\Background\shell`, `HKCR\*\shell` |
| 文件关联 | `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts` |
| 输入法设置 | 注册表导出 |
| 电源计划 | `powercfg /export` |
| Windows Terminal配置 | `%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_*/LocalState/settings.json` |
| hosts文件 | `C:\Windows\System32\drivers\etc\hosts` |
| PATH变量 | 环境变量备份中已包含 |

#### 4.5 文件关联专项（备份 / 篡改对比 / 恢复）

> 背景：有些软件会**偷偷改后缀的默认打开程序**。本模块用于事前留快照、事后能查到"被改了什么"并还原。
> 触发词：文件关联、默认打开程序、被改了、.py/.md 打不开、恢复关联。

三个独立脚本（`workspace/disk_manager/scripts/`），只读采集用 `winreg`，快照用免管理员的 `reg export`：

| 脚本 | 作用 | 典型命令 |
|------|------|----------|
| `assoc_snapshot.py` | 快照：`reg export` 原始 hive（`raw/*.reg`）+ 可读清单（`inventory.json`/`associations.csv`，后缀→生效ProgID/exe/命令行） | `--set-baseline` 建立基线；`--list` 看历史快照 |
| `assoc_diff.py` | 查看/反篡改：当前 vs 基线，列出**哪个后缀从什么变成什么** | 直接跑=当前vs基线；`--show`=列出全部；`--from A --to B`=两快照互比 |
| `assoc_restore.py` | 分档恢复：默认干跑，`--apply` 才写 | `--apply`（逐个确认）/`--apply --yes`/`--ext .pdf --apply` |

快照存放：`<data_drive>:/<backup_root>\SystemBackup\file_associations\{时间戳}\`，另有 `baseline.json` 指向基线。
全量备份时 `backup_env.py --system`（或 `--assoc`）也会顺带产出一份关联清单到 `system\file_associations\`。

**⚠️ 恢复的核心陷阱（诚实边界，别踩）**：Windows 10/11 真正生效的默认程序是
`HKCU\...\FileExts\<ext>\UserChoice`，它带一个 **Hash**（绑定 SID+后缀+ProgID+时间+开机密钥）。
**用 `reg import` 把旧的 UserChoice 导回，Windows 会判哈希失败直接忽略**——这就是"备份了却恢复不回来"、
也是软件能偷改的同一套机制。所以 `assoc_restore.py` **不走 reg import**，改用哈希无关两步法（已端到端实测）：

1. `reg add HKCU\Software\Classes\<ext> /ve /d <目标ProgID>`（设每用户经典默认，无哈希）
2. `reg delete HKCU\...\FileExts\<ext>\UserChoice`（移走带哈希的覆盖，让经典层生效）
3. 重新采集校验：生效==目标 → ✅；仍不达标（多为商店/UWP 应用 ProgID 解析不出）→ 打开 `ms-settings:defaultapps` **引导手动点一下**，脚本不谎称已自动恢复。

推荐节奏：装完新机/配好环境后 `assoc_snapshot.py --set-baseline`；怀疑被改时 `assoc_diff.py`；确认要还原 `assoc_restore.py --apply`，再 `assoc_diff.py` 复核。
（可选：以后要"当场发现偷改"，把 `assoc_diff.py` 挂成 loop/todo 定期跑，返回码非0即有改动。当前按需手动触发，未自动挂。）

#### 4.6 设置看门狗（通用引擎，纳管一整类"会被偷改"的机器设置）

> 背景：4.5 的文件关联只是"被软件偷偷改、你不专门存就想不起来"这类设置的**第一例**。
> 把它抽象成一个**声明式引擎**，之后每类设置只要写一个 provider 就自动获得 snapshot→diff→restore 闭环。

代码：`workspace/disk_manager/settings_watch/`（`base.py` 引擎 + `items.py` 内置条目 + `watch.py` 统一 CLI）。
统一入口 `watch.py` 驱动所有条目：

| 子命令 | 作用 |
|--------|------|
| `snapshot [--set-baseline] [--item ID]` | 采集当前所有纳管项存快照；`--set-baseline` 同时设为基线 |
| `diff [--vs TS] [--item ID]` | 当前 vs 基线（或指定快照），列出被偷偷改动的项；**有改动返回码 1**（可直接挂 loop） |
| `restore [--item ID] [--apply] [--yes]` | 按基线产出恢复动作，默认干跑；`--apply` 执行自动档，手动档始终需你处理 |
| `list` / `status` | 看内置条目 / 看基线时间与各条目记录数 |

命令示例：`.venv\Scripts\python.exe workspace\disk_manager\settings_watch\watch.py diff`

**当前纳管条目**（`list` 可核对，新增一类=在 `items.py` 写一个 `@register` provider）：

| 条目 id | 覆盖 | 恢复能力（诚实边界） |
|---------|------|----------------------|
| `file_associations` | 每个后缀的默认打开程序 | 自动（哈希无关两步法，同 4.5）；商店/UWP 类仍引导 `ms-settings` |
| `env_path` | 用户/系统 环境变量 + PATH（按条目增删/顺序比对） | 用户级自动 `reg add` 回写并广播 `WM_SETTINGCHANGE`；**系统级(PATH)需管理员，仅报告** |
| `url_browser` | 默认浏览器 + http/https 生效程序 + 自定义 URL 协议(steam 等) | http/https 与用户级协议认领可自动（同 UserChoice 哈希无关杠杆 / 删认领键）；**默认浏览器 Windows 11 锁得死，引导手动**；机器级协议仅报告 |
| `autostart` | HKCU/HKLM Run/RunOnce(+WOW6432Node) + 启动文件夹 | **新增**的用户级 Run 项可自动删（撤销偷加的自启）；命令被改/机器级/启动夹项仅报告，交你判断 |
| `winlogon` | HKCU/HKLM 的 `Shell`、`Userinit`（经典登录劫持面，正常恒为 explorer.exe / userinit.exe） | HKCU 层被凭空加的 Shell 自动删回基线（"未设置"）；**HKLM 层被改需管理员，仅报告**；diff 附带"是否偏离标准值"软提示 |

快照存放：`<data_drive>:/<backup_root>\SystemBackup\settings_watch\{时间戳}\snapshot.json` + `baseline.json`。
全量备份 `backup_env.py --system`（或单独 `--settings`）会顺带跑一次引擎快照并设基线。

⚠️ 引擎内所有 reg 写一律走 `subprocess` 列表形式（绕开 git-bash/MSYS 把 `/ve /d /f` 当路径转换）；打印只用 ASCII 符号+中文（GBK 终端禁 emoji/箭头）；写 `HKLM` 需管理员、`HKCU` 免提权。恢复"哈希无关"的原理与 4.5 相同——UserChoice/URL UserChoice 的 Hash 会让 `reg import` 旧值被忽略，所以只能"设经典层 + 删带哈希的覆盖"。

#### 4.7 迁移专用导出组（凭据 / 外观 / 策略 / 开发配置）

> 背景：整机备份偏科在"文件+注册表+清单"，真正换机时最痛的三类东西没覆盖——① 只存在原机、
> 且被 DPAPI/SID 绑死的凭据，② 个人化外观与输入法词库，③ 系统策略/外设/开发工具配置。
> 代码 `workspace/disk_manager/scripts/backup_groups.py`，`backup_env.py` 全量时自动跑这四组，
> 也可单独 `--credentials/--appearance/--policy/--drivers/--devtools`。产物落 `{日期}\{credentials|appearance|policy|devtools|browser}\`。

**⚠️ 明文安全**：凭据组会以明文导出 WiFi 密码、浏览器隐私、各类 token 到备份目录，filesync 会把它同步到移动硬盘。
全量或 `--credentials` 前必须让用户知情确认（用户当前选择"明文一起备"）。

| 组 | 覆盖 | 诚实边界 |
|----|------|----------|
| `credentials` | WiFi(`netsh wlan export key=clear` 明文)、SSH/AWS/npm/git/claude 等 dotfiles、**Chrome/Edge 隐私** | 凭据管理器无官方批量导出（只留 README 指引）；单拷 `Login Data` 到新机因 DPAPI 无用 |
| `appearance` | 壁纸文件本体+样式注册表、深浅色/透明、字体清单+用户字体、输入法用户词库 | 系统自带字体不拷（重装即有）；壁纸路径新机多半不存在，故连图一起备 |
| `policy` | 防火墙(.wls)、计划任务(XML)、打印机清单、VPN 拨号(pbk) | 防火墙导出常需管理员→降级为提示；`printbrm` 是按需功能多半没有；**驱动默认不导(数 GB)，`--drivers` 才导** |
| `devtools` | VSCode/Cursor/Trae 的 `settings/keybindings/snippets`、JetBrains options、扩展清单、改键 Scancode、PowerToys、WSL 名、shell dotfiles | **只拷配置白名单**，绝不整包拷 `globalStorage/workspaceStorage`(上 GB 且机器绑定)；WSL 命令在本机可能报错→甄别 |

**Chrome/Edge 隐私导出用 [HackBrowserData](https://github.com/moonD4rk/HackBrowserData)（Go 单文件，v1.1.0，实测可解 Chrome 140 的 App-Bound 加密）**：
脚本调 `archive`(可迁移 profile 归档 zip) + `dumpkeys`(跨机解密主密钥 json) + `dump -f csv`(可读清单) 三件套。
`archive + dumpkeys` 组合正是"新机也能解密"的关键——离开原机前先导出主密钥，到新机用 `restore` 还原。
二进制缓存在 `%LOCALAPPDATA%\Parcae\bin\hbd\`，缺失时脚本自动 curl 下载（冷启动 TLS 抖动已做重试）；旧 `%LOCALAPPDATA%\LocalAgent\bin\hbd\` 里已有的会由脚本首次使用时自动迁移。脚本**只打印文件名/记录数/大小，绝不回显明文密码**。

#### 5. 已安装软件列表

| 方式 | 命令 |
|------|------|
| 已安装程序 | `wmic product get name,version` 或 PowerShell `Get-ItemProperty HKLM:\Software\*` |
| Chocolatey | `choco list --local-only` |
| Scoop | `scoop list` |
| pip | `pip list --format=freeze` |
| npm全局 | `npm list -g --depth=0` |
| uv | `uv tool list` |

### L3: 一键恢复脚本设计

```
恢复流程：
1. 运行 restore_env.bat
2. 自动恢复：
   - 注册表项（环境变量、右键菜单、文件关联）
   - 桌面图标位置
   - hosts文件
   - Windows Terminal配置
   - 浏览器书签
3. 半自动恢复（需确认）：
   - 安装软件（从列表生成安装命令）
   - 恢复游戏存档（确认游戏已安装后复制）
   - 恢复浏览器扩展（逐个确认安装）
4. 手动恢复（生成清单）：
   - 密码导入
   - 需要重新配置的软件设置
   - 系统偏好设置（深色模式、缩放比例等）
```

### 备份文件组织

```
<data_drive>:/<backup_root>\SystemBackup\{日期}\
├── registry\              # 注册表导出
│   ├── env_user.reg
│   ├── env_system.reg
│   ├── context_menu.reg
│   └── desktop_layout.reg
├── browser\               # 浏览器数据
│   ├── bookmarks.json
│   ├── extensions_list.txt
│   └── preferences.json
├── game_saves\            # 游戏存档
│   └── {game_name}\
├── system\                # 系统配置
│   ├── file_associations\ # 文件关联快照（raw\*.reg + inventory.json）
│   ├── power_plan.pow
│   ├── terminal_settings.json
│   ├── hosts
│   └── start_layout.xml
├── software\              # 软件列表
│   ├── installed_programs.txt
│   ├── choco_list.txt
│   ├── pip_requirements.txt
│   └── npm_global.txt
├── desktop\               # 桌面文件和快捷方式
│   └── *.lnk
├── restore_env.bat        # 一键恢复脚本
└── manual_checklist.md    # 需手动确认的清单
```

> 设置看门狗（4.6）的快照是**独立滚动存储**，落在 `<data_drive>:/<backup_root>\SystemBackup\settings_watch\{时间戳}\`（与 `{日期}` 平级，含 `snapshot.json` + `baseline.json`），供 `watch.py diff/restore` 增量消费；全量备份 `--system`/`--settings` 会顺带在此新建一份快照并设基线。

---

## 三、与filesync的协作

你的filesync工具处理文件同步，新增的系统环境备份需要加入filesync配置：

```
<data_drive>:/<backup_root>\SystemBackup → <backup_drive> |重复文件:检查日期和大小 |增删文件处理:增量更新 |状态:启用
```

备份脚本执行后，filesync会自动同步到移动硬盘。

---

## 四、扫描策略（保护磁盘寿命）

1. **紧凑 tree**：`scan` 默认深度 4、每层 top 10，`other` 折叠小目录，JSON 通常几 KB
2. **下钻收窄**：`drill` 对大目录逐层下钻，不做一次性全盘深扫
3. **按名定位**：`find` 全树搜指定目录名（如 node_modules），匹配后计算大小即停（不重复下钻）
4. **硬上限保护**：`--max-files`（默认10万）、`--max-dirs`（默认2万）、`-d` 深度上限，达到即停报告 `stop_reason`
5. **symlink/junction 不跟随**：用 `st_file_attributes & 0x400` 检测 reparse point，跳过不递归
6. **增量备份**：只备份变更的文件，不全量复制

---

## 触发词
- 清理硬盘、磁盘清理、空间不足、清理文件
- 备份系统、全面备份、系统迁移、环境备份
- 游戏存档备份、浏览器备份
- SpaceSniffer、sns 快照、快照导入

## 工具脚本
- `parse_sns.py` - SpaceSniffer .sns 快照导入（`parse <快照> --json` → scan_disk 兼容缓存 `temp/disk_scan_cache/sns_*.json`，后续 tree/files/find/caches/dups 全部 --cache 复用；格式规范见 `references/sns_format.md`）
- `scan_disk.py` - 磁盘空间扫描（子命令：scan/tree/files/find/caches/dups/resume，--json 直返上下文，symlink/junction 不跟随，硬上限保护）
- `cleanup.py` - 磁盘清理（--dry-run 出逐项回执 → --delete --items <ids> 走 ctypes 回收站，路径白名单保护）
- `backup_env.py` - 系统环境备份（浏览器数据/游戏存档/桌面布局/系统设置/软件列表）
- `backup_groups.py` - 迁移易漏项四组导出（凭据/外观/策略/开发配置，被 backup_env.py 全量调用，见 4.7；浏览器隐私走 HackBrowserData，明文含密码需谨慎）