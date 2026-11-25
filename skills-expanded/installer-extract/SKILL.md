---
name: installer-extract
metadata:
  version: "1.0.2"
description: Windows 安装器无法启动或用户要求免安装部署时，识别安装包并解出应用，完成快捷方式、启动验证和更新处理。
---

# 应用解包部署

不运行安装器，将可信安装包中的程序提取到 `%LOCALAPPDATA%\Programs\<应用名>`。优先使用官方便携包；需要驱动、系统服务或安装脚本才能运行的软件不适用。

## 判断与准备

- 安装包下载校验成功、启动安装器失败，而普通程序能运行时，可尝试解包；错误码本身不能证明是安全软件拦截。
- 优先复用现有安装包，可在 `%TEMP%\WinGet` 查找缓存；核对来源、架构和完整性。
- 先在临时目录列出包内容，再解包。工具优先复用本机已有版本；缺少时从 [7-Zip](https://www.7-zip.org/download.html) 或 [innoextract](https://constexpr.org/innoextract/) 获取。

## 按格式解包

以下为 PowerShell 示例，`$tool`、`$package`、`$out` 均使用实际绝对路径。

| 格式 | 操作与关键点 |
| --- | --- |
| 7z 自解压 | 使用 `7zr.exe` 或 `7za.exe`：`& $tool x $package "-o$out"`。 |
| NSIS / Electron 安装包 | 使用支持 NSIS 的 `7z.exe` 和配套 `7z.dll`，命令同上；`7za.exe` 不能通用解析 NSIS。若解出嵌套 `.7z`，选匹配架构继续提取。 |
| Inno Setup | 使用 `innoextract.exe`：`& $tool --extract --output-dir $out $package`。根据文件用途映射 `app`、`code$GetDestDir` 等目录，勿无差别合并。 |
| Squirrel | 找到完整 `.nupkg`，按 ZIP 解开，应用通常在 `lib\net45`；增量包不能直接部署，外层 exe 不一定是 ZIP。 |

检查退出码和文件完整性。尾部数据提示需核查附加负载；CRC、缺卷或损坏错误不能忽略。找到主 exe 后，保持资源与运行库的相对路径，复制应用根目录到目标位置；升级时保留旧版供回退。

## 收尾

1. 仅在自动更新会再次触发受阻安装器时，于首次启动前处理更新设置：优先使用应用支持的设置。仅在确认适用时，将 `resources\app-update.yml` 改名备份，或备份后通过 JSON 解析删除 `resources\app\product.json` 中的 `updateUrl` 属性；不要按文本行删 JSON。
2. 用 `WScript.Shell` 创建当前用户的开始菜单快捷方式，设置主 exe 和工作目录；验证实际界面及快捷方式能正常打开。若调整了更新设置，一并验证修改有效且不影响启动，失败则恢复。
3. 清理本次临时文件，保留必要备份。告知部署路径、启动结果、更新状态；关闭自动更新后，手动下载新版重复流程。
4. 卸载时删除部署目录和快捷方式；用户数据默认保留，明确要求清除时再定位删除。这种部署通常不会出现在系统卸载列表。

应用本体仍被拦截或缺少安装期配置时，停止并说明原因，不反复尝试或修改安全策略。
