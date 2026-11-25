---
name: ccmoma
description: 切换 Claude Code 后端模型（moma）
---

# ccmoma - Claude Code 模型切换工具

一键切换 Claude Code 的 API 后端和模型。

## 路径说明

本 skill 可安装在 `~/.claude/skills/ccmoma/` 或 `~/.agents/skills/ccmoma/`，以下用 `$CCMOMA_DIR` 指代实际安装路径。Claude 执行时应先探测实际路径：

```bash
CCMOMA_DIR=$(test -d ~/.agents/skills/ccmoma && echo ~/.agents/skills/ccmoma || echo ~/.claude/skills/ccmoma)
```

## 安装

安装后配置脚本权限：

```bash
chmod +x $CCMOMA_DIR/ccmoma.sh
```

## 使用

```bash
$CCMOMA_DIR/ccmoma.sh init           # 首次配 API Key
$CCMOMA_DIR/ccmoma.sh glm           # 切到 BigModel（智谱）
$CCMOMA_DIR/ccmoma.sh glm glm-4.7   # 切到 BigModel 并指定模型
$CCMOMA_DIR/ccmoma.sh moma          # 切到 九天（自动启动本地代理）
$CCMOMA_DIR/ccmoma.sh moma deepseek/deepseek-v4-flash  # 切到 九天并指定模型
$CCMOMA_DIR/ccmoma.sh status        # 看当前配置
```

如果觉得路径太长，可以设置别名：

```bash
alias ccmoma="$CCMOMA_DIR/ccmoma.sh"
```

## 九天本地代理

`ccmoma moma` 依赖本地代理 `jt-proxy.py`（skill 目录已自带）。切换到 moma 时脚本会自动启动代理，也支持手动启动：

```bash
nohup python3 $CCMOMA_DIR/jt-proxy.py &
```

## 工作原理

修改 `~/.claude/settings.json` 的 `env` 字段，切换 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`。

切换后新开的对话生效，当前对话维持之前的配置。

### 背景

`ccmoma` 是为了让 Claude Code 接入国内 LLM 后端（MOMA / 聚合 API）而写的切换工具。Claude Code 原生只支持 Anthropic 官方 API，通过修改环境变量指向兼容层即可使用第三方模型。

### 关于 jt-proxy

`jt-proxy.py` 是一个本地代理，解决以下问题：

- MOMA 等聚合 API 的端点格式与 Anthropic SDK 不完全兼容，需要中间层做协议转换
- 某些 provider 需要自定义请求头或鉴权逻辑，Claude Code 原生不支持
- 通过本地代理可统一管理超时、重试等策略

`ccmoma moma` 会自动检测并启动 `jt-proxy.py`，无需手动操作。

## 首次使用

运行 `init` 命令，按提示输入 BigModel 和/或九天的 API Key。

## 安装后引导

skill 安装完成后，Claude 应主动提示用户运行初始化：

```
$CCMOMA_DIR/ccmoma.sh init
```

如果用户尚未配置任何 API Key，主动建议运行 init。如果用户已有配置文件（`~/.claude/ccmoma-config.json`），则跳过提示。

## 依赖

- Python 3
- bash
