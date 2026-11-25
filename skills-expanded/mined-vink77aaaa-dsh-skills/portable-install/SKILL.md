---
name: portable-install
description: "Use for installing anything (DSH plugins/skills/CLI/npm/software; 安装/装/便携包/portable/拷到U盘/install/add/enable) into the portable bundle, or locating its built-in tools (gh/node/npm/pnpm/dsh 在哪/怎么调用): check the bundle folder FIRST before system paths."
---

# 便携安装纪律 (Portable Install Discipline)

DeepSeek-Harness-Portable 是"拷贝即用"的便携包：整个文件夹复制到任何 Windows x64 电脑即可运行。所以每次安装都必须守住一条底线——**安装产物和配置全部落在包内，绝不散落到系统目录**，否则便携包拷走后就缺胳膊少腿。

## 定位便携包根目录

包根 = `$env:DSH_HOME`（即 `data` 目录）的上一级；技能自身就住在 `data\skills\` 下，所以：

```powershell
$root = Split-Path $env:DSH_HOME -Parent   # e.g. D:\CODEX\deepseek\DeepSeek-Harness-Portable
```

写脚本、建目录、改 PATH 时一律基于 `$root`，不要硬编码盘符路径（包可能被移到别处）。

## 内置工具清单（先查这里，再查系统路径！）

**教训**：查找/调用任何 CLI 工具（gh、git、node、npm、pnpm、dsh…）时，**第一步先看便携包根目录**，不要先去 Program Files / scoop / choco / PATH 里找——工具都装在包内。本包现状（实测）：

| 工具 | 位置 | 启动器 |
|---|---|---|
| gh (GitHub CLI) | `$root\gh\gh.exe` | `$root\gh.cmd`（`GH_CONFIG_DIR` 指向 `data\gh`，已登录） |
| node | `$root\node\node.exe` | `$root\node\npm.cmd` / `npx.cmd` / `corepack.cmd` |
| pnpm | — | `$root\pnpm.cmd` |
| dsh | `$root\node_modules\@deepseek-ai\dsh` | `$root\dsh.cmd` / `dsh-web.cmd` |
| 备份/快捷键 | — | `$root\backup.cmd` / `make-shortcut.cmd` |

根目录布局：`data\`（DSH_HOME）、`gh\`、`node\`、`node_modules\`、`ZIP\`（下载缓存）。
判断命令是否在 PATH：`Get-Command <tool>` 为空时，**直接试 `$root\<tool>.cmd` / `$root\<tool>\<tool>.exe`**，不要假定没装。

## 分类安装位置

| 要装的东西 | 安装到哪 | 做法 |
|---|---|---|
| DSH 插件 (cordis 型) | `data\profiles\web\` + `data\pnpm-store` | `dsh plugin --profile web add <pkg>`（不要用系统 pnpm/npm 全局装） |
| agent skill（含 `SKILL.md`） | `data\skills\<skill-name>\` | git clone / 复制到该目录；DSH watcher 自动发现 |
| CLI 工具（gh、git、ffmpeg…） | `$root\<tool>\` | 下载官方 zip 解压到包内独立目录，不跑系统安装器 |
| 工具的配置/数据 | `data\<tool>\` | 用环境变量指进包内（如 `GH_CONFIG_DIR=%ROOT%data\gh`） |
| 全局 npm/pnpm 包 | **不装全局** | 改用包内依赖或 `dsh` 内置 pnpm（store 在 `data\pnpm-store`） |

## CLI 工具的固定结构（照 gh 的先例）

每个装进包里的命令行工具都要有这四件套，保证在别的电脑可用、且可撤销：

```
$root\<tool>\
    <tool>.exe          # 便携本体（zip 解压，免安装）
    <tool>.cmd          # 启动器：指向包内 exe + 把配置目录设到 data\<tool>\
setup-<tool>.cmd        # 把 $root\<tool> 加进"当前用户"PATH（无需管理员）
unsetup-<tool>.cmd      # 从用户 PATH 移除对应条目（可逆）
$root\data\<tool>\      # 配置/数据随包迁移
```

启动器模板（cmd）：

```bat
@echo off
setlocal
set "ROOT=%~dp0"
set "TOOL_CONFIG_DIR=%ROOT%data\<tool>"
if not exist "%TOOL_CONFIG_DIR%" mkdir "%TOOL_CONFIG_DIR%"
"%ROOT%<tool>\<tool>.exe" %*
set "EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %EXIT_CODE%
```

## 禁止做的事

- 安装到 `C:\Program Files`、`%APPDATA%` 全局位置、写注册表、装系统服务
- 用 winget/choco/scoop 等会写系统目录的默认安装器装便携工具（除非确认有 `--portable` 之类选项且仍落包内）
- 全局 `npm i -g` / `pip install` 到用户目录

唯一允许的系统改动：**用户级 PATH 一个条目**（通过 `setup-<tool>.cmd`，`unsetup-<tool>.cmd` 可撤销）。这是"便携"与"方便"的平衡点。

## 安装完成后的验证清单（必做）

1. 列出新增文件，确认全部在 `$root` 内（`Get-ChildItem` 核对）
2. 从任意工作目录运行启动器成功（如 `$root\<tool>.cmd --version`）
3. `data\<tool>\` 配置目录已生成且能写入
4. 模拟新电脑环境（用最新 Machine+User PATH 拼出环境变量）确认命令可解析
5. 卸载/撤销方式可用（`unsetup-<tool>.cmd` 不报错）

## 参考先例

- **gh**：`gh\gh.exe` + `gh.cmd`（`GH_CONFIG_DIR` 指向 `data\gh`）+ `setup-gh.cmd` / `unsetup-gh.cmd` —— 新工具照抄这个结构即可。
- 装 DSH 插件的完整踩坑记录见 `installing-dsh-plugins` 技能（pnpm store 盘符坑、`dsh plugin` 用法）。
