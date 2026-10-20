---
name: opencode-config-safety
description: "OpenCode配置安全工具 - LLM即将发送重启OpenCode消息前的强制拦截器，确保执行防报错筛查与备份流程"
trigger_keywords: "请重启OpenCode、插件已安装好、配置已修改、可以重启了、重启后生效、MCP已配置完成、Skills已添加、修改已完成"
auto_activate: true
priority: 10
---

# OpenCode配置安全管理

## 🚨 拦截触发条件

**当LLM准备向用户发送以下消息时，必须自动激活此技能：**
- "请重启OpenCode"
- "插件已安装好，请重启"
- "MCP已配置完成，请重启"
- "配置已修改，可以重启了"
- "重启OpenCode后插件会生效"
- "Skills已添加完成，请重启"
- "修改已完成，请重启客户端"
- 类似"请重启OpenCode"的任何消息

## ⚠️ 激活此Skill后，LLM必须执行的流程

**不要直接发送上述消息！在发送前，必须先执行防报错筛查流程！**

### 🔒 强制执行步骤

**步骤1: 检查配置是否已修改**
- 刚刚是否修改了 `~/.config/opencode/opencode.json`？
- 是否添加/修改了MCP？
- 是否添加/修改了Skills？
- 是否安装了新插件？

**如果配置有修改，必须继续执行以下步骤：**

**步骤2: 备份配置**
```bash
cp ~/.config/opencode/opencode.json ~/.config/opencode/opencode.json.backup_$(date +%Y%m%d_%H%M%S)
```

**步骤3: 验证JSON语法**
```bash
python3 -m json.tool ~/.config/opencode/opencode.json > /dev/null && echo "✅ JSON语法正确" || echo "❌ JSON语法错误"
```

**步骤4: 验证timeout设置 (8000-15000ms)**
```bash
cat ~/.config/opencode/opencode.json | jq -r '.mcp[].timeout' | while read t; do
  if [ "$t" -ge 8000 ] && [ "$t" -le 15000 ]; then
    echo "✅ timeout=$t (符合规范)"
  else
    echo "❌ timeout=$t (不符合规范，建议8000-15000)"
  fi
done
```

**步骤5: 验证MCP命令格式**
```bash
cat ~/.config/opencode/opencode.json | jq -r '.mcp | to_entries[] | "\(.key): \(.value.command // \"remote\")"'
```

**步骤6: 记录修改内容**
```bash
echo "=== OpenCode配置修改记录 ===" >> ~/.config/opencode/config_changes.log
echo "时间: $(date)" >> ~/.config/opencode/config_changes.log
```

**步骤7: 验证全部通过后，才能发送"请重启OpenCode"消息**

## 🚫 禁止行为

**LLM绝对不能直接发送以下消息而不执行筛查：**
- "请重启OpenCode"
- "插件已安装好，请重启"
- "MCP已配置完成，请重启"
- 任何类似"请重启OpenCode"的消息

**必须先激活此Skill，执行防报错筛查流程！**

## 💡 工作流程

```
LLM准备发送"请重启OpenCode"
    ↓
自动激活此Skill (opencode-config-safety)
    ↓
LLM阅读此规则
    ↓
检查是否修改了配置
    ↓
如果是 → 执行备份、验证、记录流程
    ↓
验证通过 → 发送"请重启OpenCode"消息
```

## 🚨 违反此规则的后果

如果LLM直接发送"请重启OpenCode"而不执行筛查：
- ❌ 可能导致OpenCode客户端因配置错误而无法启动
- ❌ 可能导致MCP服务连接失败
- ❌ 可能导致配置损坏无法恢复
- ❌ 这是LLM的严重失职！

## ✅ 正确做法示例

**LLM修改完MCP配置后，准备发送消息：**

**错误做法**（❌ 禁止）：
```
"配置已修改完成，请重启OpenCode使配置生效。"
```

**正确做法**（✅ 强制）：
```
# 激活Skill，执行筛查...
✅ 备份配置完成
✅ JSON语法验证通过
✅ timeout设置验证通过
✅ MCP命令格式验证通过
✅ 配置验证全部通过

"配置已修改完成，请重启OpenCode使配置生效。"
```

## 🎯 核心原则

**任何时候准备发送"请重启OpenCode"消息前，必须先触发此Skill，执行防报错筛查流程！**
