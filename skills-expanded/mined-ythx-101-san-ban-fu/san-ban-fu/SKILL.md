---
name: san-ban-fu
description: 三板斧 - Claude 写，Codex 审，循环改。双 AI 交叉验证的代码生成工具。Cross-model code review loop - Claude Code writes, OpenAI Codex CLI reviews, Claude fixes.
allowed-tools: Bash
---

# 三板斧 (San Ban Fu)

Claude 写，Codex 审，循环改 — 双 AI 交叉验证的代码生成工具。

## 用法

```
/san-ban-fu <议题>
/san-ban-fu <议题> --rounds N      # 指定审核轮数（默认3）
/san-ban-fu <议题> --dir <path>    # 指定输出目录
/san-ban-fu <议题> --clean         # 清空目录后开始（会删除整个目录，仅用于专用输出目录）
```

## 示例

```
/san-ban-fu "JWT 认证中间件"
/san-ban-fu "WebSocket 聊天服务器" --rounds 5
/san-ban-fu "OAuth2 登录流程" --dir ./auth-service
```

## 流程

```
1. Claude 生成原型代码
2. Codex 独立审核（找 bug/安全/并发问题）
3. Claude 根据审核修复
4. 重复 2-3 共 N 轮
5. 输出最终代码 + REVIEW_REPORT.md
```

## 前置条件

- Claude Code 订阅 (`claude` CLI)
- Codex 订阅 (`codex` CLI)

## 执行

脚本位于本 skill 目录下的 `san_ban_fu.py`（默认安装位置 `~/.claude/skills/san-ban-fu/san_ban_fu.py`）。

```bash
_ARGS="$ARGUMENTS"
_SCRIPT="${SAN_BAN_FU_SCRIPT:-$HOME/.claude/skills/san-ban-fu/san_ban_fu.py}"

_ROUNDS="3"
_DIR=""
_CLEAN=""

# 从 ARGUMENTS 解析参数（只用 POSIX sed，兼容 macOS / Linux）
if echo "$_ARGS" | grep -q -- '--rounds'; then
  _ROUNDS=$(echo "$_ARGS" | sed -nE 's/.*--rounds[[:space:]]+([0-9]+).*/\1/p')
fi

if echo "$_ARGS" | grep -q -- '--dir'; then
  _DIR=$(echo "$_ARGS" | sed -nE 's/.*--dir[[:space:]]+([^[:space:]]+).*/\1/p')
fi

if echo "$_ARGS" | grep -q -- '--clean'; then
  _CLEAN="--clean"
fi

# 议题 = 去掉各参数后剩下的部分（xargs 去掉外层引号和多余空白，不会执行任何内容）
_TOPIC=$(echo "$_ARGS" | sed -E 's/--rounds[[:space:]]+[0-9]+//g; s/--dir[[:space:]]+[^[:space:]]+//g; s/--clean//g' | xargs)

if [ -z "$_TOPIC" ]; then
  echo "用法: /san-ban-fu <议题> [--rounds N] [--dir path] [--clean]"
  exit 1
fi

# 用数组构建命令，不使用 eval
_CMD=(python3 "$_SCRIPT" "$_TOPIC" --rounds "${_ROUNDS:-3}")
[ -n "$_DIR" ] && _CMD+=(--dir "$_DIR")
[ -n "$_CLEAN" ] && _CMD+=(--clean)

echo "🪓 三板斧启动..."
echo "📝 议题: $_TOPIC"
echo "🔄 轮数: ${_ROUNDS:-3}"
echo ""

"${_CMD[@]}"
```

注意：`--clean` 会删除整个输出目录，只用于三板斧自己的输出目录。
