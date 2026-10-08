---
name: evolve-skill
description: "Analyze OpenClaw session logs and evolve a skill based on usage data"
user-invocable: true
---

# /evolve-skill — 数据驱动 Skill 演化

分析 agent session 日志，找到 skill 的改进机会，生成改进方案。

## 参数

- **skill-name**: 要演化的 skill 名称
- **agent-id** (可选): 目标 agent，默认分析所有 agent
- **days** (可选): 分析时间范围，默认 30 天

## 流程

### 1. 定位 Skill 和 Session 数据

```bash
# 找到 skill
SKILL_PATH=$(find ~/.openclaw/workspace-*/skills -name "$SKILL_NAME" -type d 2>/dev/null | head -1)
# 或从配置找
for ws in $(jq -r '.agents.list[].workspace' ~/.openclaw/openclaw.json); do
  ws=$(eval echo "$ws")
  [ -d "$ws/skills/$SKILL_NAME" ] && SKILL_PATH="$ws/skills/$SKILL_NAME"
done

# 找到 session 日志
SESSION_DIR="$HOME/.openclaw/agents/$AGENT_ID/sessions"
```

### 2. 分析 Session 日志

扫描 `.jsonl` session 文件，提取：

| 指标 | 方法 |
|------|------|
| **触发率** | 搜索 skill name 在 skillsSnapshot 中的出现 |
| **错误率** | 统计 skill 活跃 session 中的 error 事件 |
| **Token 效率** | 比较 skill 活跃 vs 不活跃 session 的 token 消耗 |
| **用户满意度** | 检查 session 是否有重试/rephrasing 模式 |

```bash
# 快速统计
python3 -c "
import json, glob, os
from datetime import datetime, timedelta

sessions_dir = os.path.expanduser('$SESSION_DIR')
cutoff = datetime.now() - timedelta(days=${DAYS:-30})
total, triggered, errors = 0, 0, 0

for f in glob.glob(f'{sessions_dir}/*.jsonl'):
    if datetime.fromtimestamp(os.path.getmtime(f)) < cutoff:
        continue
    total += 1
    with open(f) as fh:
        content = fh.read()
        if '$SKILL_NAME' in content:
            triggered += 1
            errors += content.count('\"type\":\"error\"')

print(f'Sessions: {total}')
print(f'Triggered: {triggered} ({triggered*100//max(total,1)}%)')
print(f'Errors: {errors}')
"
```

### 3. 识别改进机会

基于分析结果，检查：

- **触发率低** → description 缺少触发词，需要扩展
- **错误率高** → skill 指令不够明确，需要添加错误处理
- **Token 消耗高** → skill body 太长或指令冗余，需要精简
- **未触发但相关** → 用户查询匹配但 skill 未被选中

### 4. 生成改进方案

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈  Skill Evolution Report: [skill-name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Metrics (last 30 days)
   Sessions analyzed:  42
   Skill triggered:    28 (67%)
   Errors:             3 (11%)
   Avg tokens:         4.2k

🔍 Findings
   1. Description missing trigger: "how to configure X"
   2. Error pattern: tool "exec" fails when path not found
   3. Unused reference: references/old-guide.md

💡 Proposed Changes
   1. Add to description: "configure X", "set up X"
   2. Add error handling: "If exec fails, check workspace path"
   3. Remove unused reference

📝 Updated SKILL.md
   [Show diff of proposed changes]

⚡ Actions
   - Apply changes? (backup current version to .evolution/)
   - Deploy to agent? (run /deploy-skill)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. 备份 + 应用

```bash
# 备份当前版本
VERSION=$(grep "^version:" "$SKILL_PATH/SKILL.md" | awk '{print $2}')
mkdir -p "$SKILL_PATH/.evolution"
cp "$SKILL_PATH/SKILL.md" "$SKILL_PATH/.evolution/${VERSION:-v0}.md"

# 应用改进 (由 agent 编辑 SKILL.md)
# 然后运行验证
bash scripts/validate-skill.sh "$SKILL_PATH"
```
