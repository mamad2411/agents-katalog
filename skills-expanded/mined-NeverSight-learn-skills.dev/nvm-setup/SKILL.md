---
name: nvm-setup
description: Configure shell initialization and environment variables so nvm loads correctly across bash, zsh, and fish.
license: Complete terms in LICENSE.txt
---

## When to use this skill

**ALWAYS use this skill when the user mentions:**
- Loading nvm in a new shell session
- Setting NVM_DIR or sourcing nvm.sh
- Bash/zsh/fish profile configuration
- XDG_CONFIG_HOME profile location differences

**Trigger phrases include:**
- "nvm not found", "nvm 命令找不到", "source nvm.sh"
- "NVM_DIR", "profile", "bashrc", "zshrc", "fish"
- "--no-use", "手动加载"

## How to use this skill

**CRITICAL: This skill focuses on shell initialization and environment variables.** For installation or version usage, use other nvm-* skills.

1. Identify the active shell and the correct profile file path.
2. Add NVM_DIR and nvm.sh sourcing lines from the template.
3. Add bash completion or optional config as needed.
4. Start a new shell session and verify nvm loads.

**Important notes:**
- XDG_CONFIG_HOME changes the expected profile path.
- Use --no-use when you only want nvm loaded without switching versions.

### Example file map

- templates/shell-config.md
- examples/environment-variables.md
- examples/bash-completion.md
- examples/bash-completion-usage.md

## Keywords

nvm setup, NVM_DIR, nvm.sh, profile, bash, zsh, fish, XDG_CONFIG_HOME, shell init

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
