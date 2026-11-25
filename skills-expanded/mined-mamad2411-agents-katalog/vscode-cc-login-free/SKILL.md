---
name: vscode-cc-login-free
description: 配置 VS Code Claude Code 插件免登录直接使用。自动同步 Claude CLI 配置到 VS Code 插件，解决 spawn EPERM 问题。
---

# VS Code Claude Code 免登录配置工具

此工具将自动配置 VS Code 中的 Claude Code 插件，使其无需登录即可使用。

## 功能

- 自动读取 Claude CLI 配置 (`~/.claude/settings.json`)
- 转换并写入 VS Code 插件配置
- 检测并自动配置 Git Bash 环境变量（解决 spawn EPERM 问题）
- 跨平台支持 (Windows/macOS/Linux)

## 前置条件

1. 已安装 VS Code
2. 已安装 Claude Code CLI
3. 已在终端中完成 Claude Code 登录配置

## 配置映射

| Claude CLI 配置 | VS Code 插件配置 |
|----------------|-----------------|
| `env.ANTHROPIC_API_KEY` | `claudeCode.environmentVariables` → `ANTHROPIC_AUTH_TOKEN` |
| `env.ANTHROPIC_BASE_URL` | `claudeCode.environmentVariables` → `ANTHROPIC_BASE_URL` |
| `env.ANTHROPIC_MODEL` | `claudeCode.selectedModel` |
| `permissionMode: "bypassPermissions"` | `claudeCode.initialPermissionMode` |
| `dangerMode: true` | `claudeCode.allowDangerouslySkipPermissions` |

## 执行配置

请使用 Glob 工具查找脚本路径，然后运行：

```bash
# 查找脚本
# Glob pattern: "**/vscode-cc-login-free/scripts/configure.py"

# 然后执行
python <找到的路径>/configure.py
```

或者使用以下跨平台命令自动定位并运行：

```bash
python -c "
import subprocess,os,glob
paths = glob.glob(os.path.expanduser('~/.claude/skills/vscode-cc-login-free/scripts/configure.py'))
if paths: subprocess.run(['python', paths[0]])
else: print('未找到 configure.py 脚本')
"
```

## 常见问题

### spawn EPERM 错误

如果遇到 `spawn EPERM` 错误，通常是 Git Bash 未添加到 PATH 环境变量导致。

**解决方案：**
1. 运行此脚本会自动检测并尝试添加
2. 如自动添加失败，手动添加 Git Bash 到 PATH：
   - 路径通常是：`C:\Program Files\Git\bin`
3. 重启 VS Code

### 配置未生效

1. 确保 VS Code 已完全关闭后重新打开
2. 检查 VS Code settings.json 是否正确写入
3. 确认 Claude CLI 配置文件存在且格式正确