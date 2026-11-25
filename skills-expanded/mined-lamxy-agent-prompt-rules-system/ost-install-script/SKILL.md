---
name: ost-install-script
description: 'Write scripts_for_install/install.sh for any open-source library in the open_supports/ system. Use when adding a new support package that needs a one-click installation script. Produces a POSIX sh script with platform detection, flag-driven interface, and idempotent behavior.'
argument-hint: 'GitHub owner/repo of the target library, e.g. colbymchenry/codegraph'
---

# 编写 open_supports 一键安装脚本（install.sh）

## When to Use

- 为 `open_supports/` 新增支持包时，编写 `scripts_for_install/install.sh`
- 官方安装方式有变动时，更新现有脚本

## Pre-read

1. 目标库的**官方安装文档**（主要依据）
2. 该支持包的 `repo_readme_summary.md` — 确认平台要求和安装命令
3. `.ost-refs/` 目录（如存在）— 了解本地路径约定
4. `SCOPE-CONTRACT-CASES.md` — 按用例审查生成设计，不运行真实安装

先从 `repo_readme_summary.md` Part 2 提取并核对以下**安装作用域契约**；缺失任一字段不得开始写脚本：

| 字段 | 必须记录的事实 |
|---|---|
| 分类 | `A` 仅全局、`B` 项目本地且 CWD 敏感、`C` 原生项目路径参数、或 `D` 同时支持全局和项目模式 |
| 官方默认 | 官方命令不带 flag 时究竟写入全局还是项目目录 |
| 目标目录 | 是否需要、默认值、是否由 CWD 决定、或是否有原生路径 flag |
| 执行机制 | 直接执行、`( cd "$ABS_TARGET_DIR" && command )`、或 `command --project "$ABS_TARGET_DIR"` |
| 证据 | 对应官方一手文档链接和原始命令 |

## GitHub Source Policy

读取 GitHub 仓库事实、README、目录、release、issue、PR 或文件内容时，优先使用 GitHub connector / GitHub app 的结构化工具；若工具不可见，先通过 `tool_search` 搜索 GitHub 工具。仍不可用时，再考虑 `gh` CLI、GitHub 官方 API 或官方文档网站。

`curl` / raw GitHub URL 只用于官方安装命令本身，或作为明确记录的 fallback。安装脚本可以保留官方文档规定的 `curl | sh` 或 release 下载命令，但这不等同于资料获取时默认使用 `curl`。

作为 workflow 阶段子代理返回结果时，必须包含：

- `sources_used`: 来源类别和关键路径摘要
- `fallbacks`: 降级原因摘要；没有降级时返回空数组

## Clarification / Blocking

如果执行本阶段所需信息无法从官方安装文档、`repo_readme_summary.md` 或 `.ost-refs/` 中可靠判断：

1. 不要猜测关键行为
2. 向 workflow 返回一个澄清问题
3. 标明 blocked 字段：
   - `stage`: `install_script`
   - `reason`
   - `question`
   - `suggested_default`（如有）
4. 等用户回答后再继续本阶段

典型阻塞点：

- 无法确定脚本语言应使用 sh、Node.js 还是 Python
- 官方安装方式包含破坏性或高权限操作，无法判断是否适合一键脚本
- 客户端接入命令、配置范围或默认 flag 无法可靠确定
- 安装作用域分类、官方默认、CWD 语义或原生路径参数无法可靠确定
- 已有安装时的升级行为不明确
- 验证命令无法确认工具可用

## 设计决策（编写前确认）

| 决策点 | 默认值 | 说明 |
|--------|--------|------|
| 脚本语言 | POSIX sh | 库有 Node.js / Python 运行时时可改用对应语言 |
| 平台覆盖 | macOS、Linux、WSL | 不包含 Windows native；Windows 安装命令在报错提示中给出 |
| 驱动方式 | 纯 flag 驱动 | 无交互式提示 |
| 安装作用域 | 以官方契约为准 | 不得把所有库一律设为 local 或 global |
| 已安装时 | 提示版本 + 执行升级 | 升级命令见官方文档 |
| 卸载策略 | 默认不实现卸载 | 只记录官方卸载方法；仅当官方卸载命令明确且用户要求时，才可扩展 `--uninstall` |

## 卸载策略

默认一键脚本只负责安装、更新、配置和验证，不加入删除或卸载逻辑。

- 官方提供卸载文档时，必须优先在 `repo_readme_summary.md` Part 5 记录原文链接；setup Skill 的 Troubleshooting 可补充指向同一官方说明
- 不要默认删除二进制、配置文件、缓存目录或 Agent 客户端配置
- 只有同时满足以下条件时，才允许把 `--uninstall` 作为可选扩展加入脚本：
  1. 官方文档明确提供卸载命令或可验证的卸载流程
  2. 用户明确要求脚本支持卸载
  3. 脚本在执行前打印将删除或修改的路径 / 配置范围

## [库特定] 替换清单

编写前，确认以下占位符对应的实际值：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{LibraryName}` | 库名 | `CodeGraph` |
| `{owner}/{repo}` | GitHub 路径 | `colbymchenry/codegraph` |
| `INSTALL_URL` | 官方 curl 脚本地址 | `https://raw.githubusercontent.com/.../install.sh` |
| `{binary}` | 安装后的命令名 | `codegraph` |
| `install_cli()` | 安装方式：curl / npm / pip 等 | 见官方文档 |
| `configure()` | 接入 / 配置命令（无则整块删除） | `codegraph install ...` |
| `upgrade_cmd` | 升级命令 | `codegraph upgrade` |
| Windows 提示 | detect_platform `*` 分支中填写 Windows 安装命令 | `irm ... \| iex` |

## 安装作用域生成规则（必须逐库选择）

不要把下方骨架中的 flag 当成固定接口；只保留官方能力和为正确传递目标目录所必需的封装参数。脚本顶部注释、`--help`、运行时错误和下一步提示均使用中文。

| 分类 | 安装器行为 |
|---|---|
| `A` 仅全局 | 直接执行官方全局命令。不得伪造项目目录参数、`--local` 或 `--target`。帮助必须说明写入的用户级范围。 |
| `B` 项目本地／CWD 敏感 | 接受项目目录位置参数（默认 `.`），先解析为绝对路径并验证为目录；本地命令只能在 `( cd "$ABS_TARGET_DIR" && command )` 子 shell 中运行，绝不改变调用端 CWD。若官方另有全局模式，作为显式 `--global` 分支。 |
| `C` 原生路径参数 | 接受项目目录位置参数（默认 `.`），先解析和验证；优先执行官方的 `command --project "$ABS_TARGET_DIR"`（或等效原生 flag），不得用自行 `cd` 代替已支持的原生路径。 |
| `D` 双模式 | 分别实现全局和项目分支。默认值必须与官方命令默认一致；只有官方默认项目模式时，才可默认目标目录 `.`。项目分支再按 `B` 或 `C` 的规则实现；全局分支不得悄悄消费或忽略项目目录。 |

### 目录与参数规则

1. 项目模式的接口必须显式表达模式和目录：`D` 且官方默认全局时用 `install.sh --local 项目目录`（或等效明确接口），不能把裸项目目录隐含解释为 local；`B` 才可在帮助中明确声明位置参数默认 `.`；`C` 使用实际需要的 `--project DIR` 或等效原生路径接口。
2. 通过 `pwd -P` 或等效 POSIX 方式取得 `ABS_TARGET_DIR`，并在运行任何会写入项目的命令前检查 `[ -d "$ABS_TARGET_DIR" ]`。
3. `B` 的 `cd` 必须在子 shell；不要使用裸 `cd`，也不要在支持包目录下执行后假称写入用户项目。
4. 全局模式和项目模式有不同副作用时，在运行前 `printf` 说明实际写入范围；未知目录、冲突 flag、或 global 模式携带项目目录必须非零退出。
5. 只接受官方明确支持的模式。官方事实不足时返回 `NEEDS_CLARIFICATION`，不要凭经验指定 `--location=local`。

## 脚本骨架模板

```sh
#!/bin/sh
# =============================================================================
# install.sh — {LibraryName} 安装脚本
# 仓库：https://github.com/{owner}/{repo}
#
# 用法（以下是 D 类「官方默认全局、--local 为 CWD 敏感项目模式」的安全范例；必须按实际分类替换）：
#   ./install.sh
#   ./install.sh --local /绝对/项目/目录
#
# 选项：
#   --local 项目目录     显式项目级安装（仅 D 的项目分支示例；目标目录必须存在）
#   --global             显式全局安装（仅官方支持且非默认时保留）
#   --help               显示中文帮助
# =============================================================================

set -eu

# --- [库特定] 安装源 ---
INSTALL_URL="..."           # 官方 curl 脚本 URL

# --- 作用域默认值：D 的官方默认全局范例；A/B/C 必须按 Part 2 事实替换 ---
MODE="global"
TARGET_DIR=""
SCOPE_SET=0

# --- flag 解析 ---
while [ "$#" -gt 0 ]; do
  case "$1" in
    --local)
      [ "$#" -ge 2 ] || { printf '%s\n' '错误：--local 需要项目目录。' >&2; exit 1; }
      [ "$SCOPE_SET" -eq 0 ] || { printf '%s\n' '错误：不能同时指定多个安装范围。' >&2; exit 1; }
      MODE="local"; TARGET_DIR=$2; SCOPE_SET=1; shift
      ;;
    --global) [ "$SCOPE_SET" -eq 0 ] || { printf '%s\n' '错误：不能同时指定多个安装范围。' >&2; exit 1; }; MODE="global"; SCOPE_SET=1 ;;
    --help|-h) sed -n '/^# 用法/,/^# ===/p' "$0" | sed 's/^# \?//'; exit 0 ;;
    --*) printf '错误：未知选项 "%s"。运行 "%s --help" 查看用法。\n' "$1" "$0" >&2; exit 1 ;;
    *) printf '错误：未知参数 "%s"。运行 "%s --help" 查看用法。\n' "$1" "$0" >&2; exit 1 ;;
  esac
  shift
done

if [ "$MODE" = "local" ]; then
  [ -d "$TARGET_DIR" ] || { printf '错误：项目目录不存在：%s\n' "$TARGET_DIR" >&2; exit 1; }
  ABS_TARGET_DIR=$(CDPATH= cd -- "$TARGET_DIR" && pwd -P)
fi

# =============================================================================
# 平台检测（通用，直接复用）
# =============================================================================
detect_platform() {
  _uname="$(uname -s 2>/dev/null || echo unknown)"
  case "$_uname" in
    Darwin) PLATFORM="macos" ;;
    Linux)
      if grep -qi "microsoft\|wsl" /proc/version 2>/dev/null; then
        PLATFORM="wsl"
      else
        PLATFORM="linux"
      fi
      ;;
    *)
      printf 'Error: 不支持的平台 "%s"。本脚本支持 macOS、Linux 和 WSL。\n' "$_uname" >&2
      # [库特定] 若有 Windows native 安装命令，在此补充提示：
      # printf 'Windows 用户请在 PowerShell 中执行：\n  irm <url> | iex\n' >&2
      exit 1
      ;;
  esac
}

# =============================================================================
# PATH 修复（通用）
# curl | sh 安装后，新增的二进制在当前 session PATH 中可能不可见，
# 主动在常见路径搜索并临时扩展 PATH。
# =============================================================================
refresh_path() {
  for _dir in "$HOME/.local/bin" "$HOME/bin" "/usr/local/bin" "/opt/homebrew/bin"; do
    if [ -x "$_dir/{binary}" ]; then   # [库特定] 替换 {binary}
      export PATH="$_dir:$PATH"
      return 0
    fi
  done
}

# =============================================================================
# [库特定] CLI 安装
# =============================================================================
install_cli() {
  printf '→ 正在安装 {LibraryName} CLI...\n'
  curl -fsSL "$INSTALL_URL" | sh
  # 若通过 npm 安装，替换为：npm i -g {pkg-name}
  refresh_path
}

# =============================================================================
# [库特定] 接入 / 配置（若库无此步骤，整块删除）
# =============================================================================
configure() {
  # 仅在官方有配置步骤时保留。项目分支必须遵循上方 B/C 规则。
  # B/D-local 示例：( cd "$ABS_TARGET_DIR" && {binary} install --local --yes )
  # C 示例：{binary} install --project "$ABS_TARGET_DIR" --yes
}

# =============================================================================
# [库特定] 安装后提示
# =============================================================================
print_next_steps() {
  printf '\n✓ 安装完成。\n\n'
  # 按库的实际使用方式填写下一步提示
  printf '下一步：...\n'
}

# =============================================================================
# 主流程（通用骨架）
# =============================================================================
main() {
  detect_platform
  printf '平台：%s\n\n' "$PLATFORM"

  # 已安装检测
  if command -v {binary} >/dev/null 2>&1; then    # [库特定] {binary}
    _ver="$({binary} version 2>/dev/null || printf 'unknown')"
    printf 'ℹ {LibraryName} 已安装（%s），检查更新...\n\n' "$_ver"
    {binary} upgrade || true    # [库特定] 升级命令；|| true 防止"已是最新"时非零退出码中断脚本
    printf '\n提示：如需重新配置，重新运行本脚本。\n'
    exit 0
  fi

  # 首次安装
  printf '=== {LibraryName} 首次安装 ===\n'
  install_cli

  # CLI 可用性验证
  if ! command -v {binary} >/dev/null 2>&1; then    # [库特定] {binary}
    printf '\nError: 安装后仍找不到 {binary} 命令。\n' >&2
    printf '请重新打开终端后重试，或手动安装：npm i -g {pkg-name}\n' >&2
    exit 1
  fi

  configure
  print_next_steps
}

main
```

## Quality Checklist

- [ ] `set -eu` 已保留（出错立即退出，避免静默失败）
- [ ] `printf` 使用 `%s` 占位，不将变量拼入格式字符串
- [ ] 升级命令后有 `|| true`（防止"已是最新"时非零退出码中断脚本）
- [ ] `refresh_path` 中的 `{binary}` 已替换为实际命令名
- [ ] 无关的 flag 和函数块已删除（如库没有 configure 步骤）
- [ ] `--help` 有用法说明和示例
- [ ] 顶部注释、帮助、错误和提示均为中文
- [ ] 已从 Part 2 记录 A/B/C/D 分类、官方默认、目录机制和官方证据
- [ ] `B` 项目安装先验证绝对目标目录，并只在 `( cd "$ABS_TARGET_DIR" && command )` 中执行
- [ ] `C` 项目安装优先传递官方原生路径参数，不以 `cd` 模拟
- [ ] `D` 的默认值与官方一致，global/project 分支不会静默混用目录
- [ ] `SCOPE-CONTRACT-CASES.md` 的相应用例已逐项审查
- [ ] `print_next_steps` 告知用户安装后该做什么
- [ ] 未默认加入删除、卸载或清理配置等破坏性逻辑；如支持 `--uninstall`，已确认官方依据和用户要求
