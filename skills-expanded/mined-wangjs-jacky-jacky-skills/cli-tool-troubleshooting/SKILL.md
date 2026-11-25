---
name: cli-tool-troubleshooting
description: "通用 CLI 工具故障排查。当 npm 全局包安装后运行报错、二进制文件损坏、optional 依赖缺失、postinstall 静默失败、spawnSync 错误时触发此 skill。"
---

<role>CLI 工具链故障排查助手，擅长定位 npm/node 全局包的安装、二进制执行、平台依赖等问题。</role>
<purpose>用系统化诊断流程快速定位 CLI 工具故障根因，给出最短修复路径并完成验证。</purpose>
<trigger>

```text
触发词：
- CLI 工具安装后运行报错
- spawnSync 错误 / Unknown system error
- command not found 但已安装
- npm 全局包二进制损坏
- optional 依赖缺失导致运行失败
- postinstall 脚本失败但安装显示成功
- binary / bin 文件为空或损坏

示例：
- "opencode 运行报 spawnSync error -88"
- "安装了 xxx 但运行报 command not found"
- "npm install -g xxx 成功但二进制文件损坏"
```

</trigger>
<gsd:workflow xmlns:gsd="urn:gsd:workflow">
  <gsd:meta>priority=diagnosis-first; key_checks=binary-integrity,optional-deps,postinstall,codesign,architecture</gsd:meta>
  <gsd:goal>系统化排查 CLI 工具安装/运行故障，在最少步骤内恢复可用状态。</gsd:goal>
  <gsd:phase>收集症状：错误信息、工具名称、安装方式、Node/npm 版本。</gsd:phase>
  <gsd:phase>按错误类型匹配诊断路径：二进制损坏 / 依赖缺失 / 签名问题 / 权限问题。</gsd:phase>
  <gsd:phase>应用修复方案并验证工具可正常运行。</gsd:phase>
  <gsd:phase>输出根因分析和预防建议。</gsd:phase>
</gsd:workflow>

# CLI 工具故障排查指南

> 本 skill 帮助快速诊断和解决命令行工具安装、运行中的常见问题。
> 覆盖 npm 全局包、二进制文件、optional 依赖、postinstall 脚本等场景。

## 快速诊断流程

```
CLI 工具运行报错
    ↓
1. 定位错误类型（spawnSync / ENOENT / EACCES / 其他）
    ↓
2. 检查二进制文件完整性（大小、架构、签名）
    ↓
3. 检查 optional 依赖是否完整安装
    ↓
4. 检查 postinstall 脚本执行情况
    ↓
5. 应用修复 → 验证
```

## 一、错误类型分类

### 1.1 错误类型速查

| 错误关键词 | 大概率原因 | 诊断路径 |
|-----------|-----------|---------|
| `spawnSync ... Unknown system error -88` | 二进制文件损坏或为空 | → 二进制完整性检查 |
| `spawnSync ... ENOENT` | 二进制文件不存在 | → 安装路径检查 |
| `EACCES permission denied` | 权限不足 | → 权限修复 |
| `command not found` | PATH 未包含 / 未安装 | → PATH 和安装检查 |
| `invalid or unsupported format` | 架构不匹配 | → 架构检查 |
| `SIGKILL` / `Killed` | 内存不足或安全策略 | → 系统资源检查 |
| 安装成功但功能异常 | postinstall 静默失败 | → 依赖完整性检查 |

### 1.2 诊断步骤模板

```bash
# Step 1: 确认工具是否在 PATH 中
which <tool-name>

# Step 2: 检查二进制文件信息
file $(which <tool-name>)
ls -la $(which <tool-name>)

# Step 3: 检查实际二进制（非 wrapper 脚本）
file <npm-global>/lib/node_modules/<package>/bin/.<binary>
ls -la <npm-global>/lib/node_modules/<package>/bin/
```

## 二、二进制完整性检查

### 2.1 检查二进制文件状态

```bash
# 找到实际二进制路径（通常在 node_modules 下）
BINARY_PATH=$(npm root -g)/<package>/bin/.<binary>

# 检查文件类型和架构
file "$BINARY_PATH"

# 检查文件大小（正常应为 MB 级别，空文件为 0 bytes）
ls -la "$BINARY_PATH"

# macOS: 检查扩展属性（quarantine 标记会阻止执行）
xattr "$BINARY_PATH"

# macOS: 检查代码签名（Go 二进制可能无签名，但不应报格式错误）
codesign -vvv "$BINARY_PATH"
```

### 2.2 常见异常和修复

| 异常现象 | 说明 | 修复方案 |
|---------|------|---------|
| 文件大小为 0 或异常小（如 33MB 应为 118MB） | postinstall 未正确写入 | 重装 + 手动补依赖 |
| `empty file` 或 `data` | 损坏或为占位文件 | 删除后重装 |
| quarantine 属性 `com.apple.quarantine` | macOS 安全限制 | `xattr -d com.apple.quarantine <path>` |
| `Non-executable` | 缺少执行权限 | `chmod +x <path>` |

## 三、optional 依赖缺失

> **最常见的静默故障源**：npm 会静默跳过安装失败的 optional 依赖。

### 3.1 识别 optional 依赖缺失

```bash
# 查看包的 optionalDependencies
cat $(npm root -g)/<package>/package.json | grep -A20 '"optionalDependencies"'

# 检查对应平台包是否存在（以 opencode-ai 为例）
ls $(npm root -g) | grep <package-prefix>
# 期望：opencode-darwin-arm64
# 实际：可能缺失
```

### 3.2 根因：为什么会缺失？

| 场景 | 原因 |
|------|------|
| 网络波动 | npm 在 optional 依赖下载超时时静默跳过 |
| npm 版本差异 | 不同 npm 版本对 optional 依赖策略不同 |
| registry 不稳定 | 私有 registry 可能缺少特定平台包 |
| Node 版本过新 | 新版 Node/npm 可能有行为变更 |

### 3.3 修复方案

```bash
# 方案 A：手动安装缺失的平台包（推荐）
npm install -g <platform-package>
# 例如：npm install -g opencode-darwin-arm64

# 方案 B：重装主包（确保网络稳定）
npm uninstall -g <package>
npm install -g <package>

# 方案 C：强制安装所有 optional 依赖
npm install -g <package> --install-strategy=nested

# 修复后手动运行 postinstall（如果需要）
cd $(npm root -g)/<package> && node postinstall.mjs
```

## 四、postinstall 脚本静默失败

> **高危模式**：安装显示成功，实际二进制文件损坏。

### 4.1 识别方法

```bash
# 1. 查看 postinstall 脚本内容
cat $(npm root -g)/<package>/postinstall.mjs

# 2. 检查是否有 process.exit(0) 吞错误
grep -n "process.exit(0)" $(npm root -g)/<package>/postinstall.mjs

# 3. 手动运行 postinstall 观察输出
cd $(npm root -g)/<package> && node postinstall.mjs
# 正常：无输出或成功信息
# 异常：报错但之前被 exit(0) 吞掉
```

### 4.2 典型故障模式

```javascript
// 危险模式：吞掉所有错误
try {
  main()  // ← 如果依赖缺失会 throw
} catch (error) {
  console.error(error.message)
  process.exit(0)  // ← npm 认为安装成功！
}
```

### 4.3 修复策略

1. **先修复根因**（补依赖、修复路径等）
2. **手动运行 postinstall**
3. **验证二进制文件是否正确生成**

## 五、架构不匹配

### 5.1 检查架构

```bash
# 当前系统架构
uname -m
# arm64 = Apple Silicon
# x86_64 = Intel Mac

# 二进制文件架构
file <binary-path>
# Mach-O 64-bit executable arm64 ← 应与系统匹配
# Mach-O 64-bit executable x86_64 ← 在 Apple Silicon 上需要 Rosetta
```

### 5.2 常见问题

| 系统架构 | 二进制架构 | 结果 |
|---------|-----------|------|
| arm64 | arm64 | 正常 |
| arm64 | x86_64 | 需要 Rosetta，可能运行缓慢 |
| x86_64 | arm64 | 无法运行，需要重新安装对应架构版本 |

## 六、权限问题

### 6.1 检查和修复

```bash
# 检查全局 npm 目录权限
ls -la $(npm root -g)/<package>/bin/

# 修复执行权限
chmod +x $(npm root -g)/<package>/bin/*

# 如果使用 nvm，确保 npm 全局目录在用户空间
npm root -g
# 应该在 ~/.nvm/versions/node/... 下（用户空间）
# 不应该在 /usr/local/lib/node_modules/ 下（系统空间）
```

### 6.2 nvm 环境 vs 系统 Node

```bash
# nvm 环境（推荐）— 权限通常没问题
which node
# /Users/<user>/.nvm/versions/node/v24.9.0/bin/node

# 系统 Node — 可能有权限问题
which node
# /usr/local/bin/node → 需要 sudo，不推荐
```

## 七、实战案例库

### 案例 1：opencode-ai spawnSync error -88

**症状**：
```
spawnSync /path/.opencode Unknown system error -88
```

**诊断过程**：
```bash
# 1. 检查文件
file .opencode → Mach-O 64-bit executable arm64  # 架构正确
ls -la .opencode → 33MB  # 异常小（应为 118MB）

# 2. 检查签名
codesign -vvv .opencode → invalid signature  # 签名无效

# 3. 检查平台依赖
ls $(npm root -g) | grep opencode → 只有 opencode-ai  # 缺少 opencode-darwin-arm64

# 4. 查看包配置
cat package.json → optionalDependencies 包含 opencode-darwin-arm64

# 5. 查看 postinstall
cat postinstall.mjs → process.exit(0) 吞错误
```

**根因**：`opencode-darwin-arm64` optional 依赖未安装 + postinstall `exit(0)` 静默吞错

**修复**：
```bash
npm install -g opencode-darwin-arm64
cd $(npm root -g)/opencode-ai && node postinstall.mjs
```

**预防建议**：
- 安装后验证二进制文件大小
- 关注 npm 安装日志中的 optional dependency 警告

### 案例 2：全局包安装成功但 command not found

**症状**：
```
npm install -g xxx → added 1 package
xxx → command not found
```

**诊断**：
```bash
# 检查安装位置
npm root -g

# 检查 bin 链接
ls $(npm bin -g) | grep xxx

# 检查 PATH
echo $PATH | tr ':' '\n' | grep nvm
```

**常见原因**：
1. `npm bin -g` 不在 PATH 中（nvm 未正确加载）
2. bin 链接未创建（package.json 缺少 bin 字段）
3. 多个 Node 版本混用

## 八、通用排查清单

遇到 CLI 工具问题时，按顺序执行：

```bash
# 1. 基本信息
node --version
npm --version
uname -m

# 2. 工具位置
which <tool>

# 3. 二进制完整性
file $(readlink -f $(which <tool>))  # Linux
file $(npm root -g)/<pkg>/bin/.<binary>  # 通用

# 4. 平台依赖
ls $(npm root -g) | grep <pkg-prefix>

# 5. 重装测试
npm uninstall -g <pkg>
npm install -g <pkg>

# 6. 验证
<tool> --version
```

## 九、预防建议

| 场景 | 建议 |
|------|------|
| 新安装全局包 | 安装后立即运行 `<tool> --version` 验证 |
| optional 依赖 | 检查 `npm ls -g` 输出，确认平台包已安装 |
| postinstall 脚本 | 关注 `npm install` 输出中的 postinstall 日志 |
| 版本升级 | 升级后重新验证二进制文件完整性 |
| CI 环境 | 使用 `npm ci` 替代 `npm install` 确保一致性 |
