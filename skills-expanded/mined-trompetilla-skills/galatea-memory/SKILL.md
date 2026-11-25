---
name: galatea-memory
version: 1.0.0
description: "Galatea 记忆管理增强系统 - 实现分层记忆、自动检查点和关键信息标记"
author: Galatea
keywords: [memory, galatea, checkpoint, hierarchy, key-info, cache]
---

# Galatea Memory Manager 🧠

Galatea 专属的记忆管理增强系统，实现三项核心功能：

1. **分层记忆系统** - 工作记忆 → 短期记忆 → 长期记忆
2. **自动检查点** - 定期自动保存会话状态
3. **关键信息标记** - 智能识别并归档重要信息

## 架构

```
┌─────────────────────────────────────────┐
│          Galatea Memory Manager         │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐                      │
│  │  工作记忆     │ ← 当前会话上下文     │
│  │  (Model RAM) │                      │
│  └──────┬───────┘                      │
│         │ 自动同步                      │
│         ▼                               │
│  ┌──────────────┐                      │
│  │  短期记忆     │ ← memory/cache.json │
│  │  (cache.json)│   最近 50 条         │
│  └──────┬───────┘                      │
│         │ 定期归档                      │
│         ▼                               │
│  ┌──────────────┐                      │
│  │  长期记忆     │ ← memory/YYYY-MM-DD │
│  │  (Files)     │   + Notion           │
│  └──────────────┘                      │
│                                         │
│  ┌──────────────┐                      │
│  │  检查点       │ ← checkpoints/      │
│  │  Checkpoints │   保留 10 个         │
│  └──────────────┘                      │
│                                         │
│  ┌──────────────┐                      │
│  │  关键信息     │ ← key_facts.md      │
│  │  Key Facts   │   + Notion 同步      │
│  └──────────────┘                      │
│                                         │
└─────────────────────────────────────────┘
```

## 安装

```bash
# 确保目录存在
mkdir -p /root/.openclaw/workspace/skills/galatea-memory

# 复制文件
cp memory_manager.py /root/.openclaw/workspace/skills/galatea-memory/
cp SKILL.md /root/.openclaw/workspace/skills/galatea-memory/

# 创建 CLI 链接
ln -sf /root/.openclaw/workspace/skills/galatea-memory/memory_manager.py /usr/local/bin/memory-manager
chmod +x /usr/local/bin/memory-manager
```

## CLI 使用

### 短期记忆管理

```bash
# 添加条目到短期记忆
memory-manager cache --add "用户偏好深色模式"

# 列出最近条目
memory-manager cache --list
memory-manager cache --limit 5

# 搜索短期记忆
memory-manager cache --search "偏好"

# 清空缓存
memory-manager cache --clear
```

### 检查点管理

```bash
# 创建检查点
memory-manager checkpoint --create "完成用户认证模块" \
  --decisions "使用 JWT" "密码 bcrypt 加密" \
  --todos "添加邮箱验证" "实现密码重置"

# 列出所有检查点
memory-manager checkpoint --list

# 查看检查点详情
memory-manager checkpoint --load checkpoint_2026-02-05_14-30

# 恢复到检查点状态
memory-manager checkpoint --restore checkpoint_2026-02-05_14-30
```

### 关键信息管理

```bash
# 手动添加关键信息
memory-manager key --add "我对青霉素过敏" --tags #health #allergy

# 列出关键信息
memory-manager key --list

# 按类别筛选
memory-manager key --list --category health
```

### 统计信息

```bash
memory-manager stats
```

## 自动触发

### 检查点自动创建

以下情况会自动创建检查点：
1. 任务完成时（调用 `auto_checkpoint_on_task_complete`）
2. 每 30 分钟（需外部 cron/heartbeat 触发）
3. 会话结束时

### 关键信息自动标记

检测以下触发词：
- "记住这个"
- "这很重要"
- "以后要记住"
- "记一下"
- "别忘了"
- "重要"

自动分类：
- `#health` - 健康相关信息
- `#preference` - 用户偏好
- `#task` - 任务/待办
- `#contact` - 联系人信息
- `#project` - 项目相关
- `#decision` - 决策记录

## Python API

```python
from memory_manager import MemoryManager, Priority

# 初始化
mm = MemoryManager()

# 短期记忆
mm.add_to_short_term("重要信息", priority=Priority.HIGH)
memories = mm.get_short_term_memories(limit=5)

# 检查点
checkpoint_id = mm.create_checkpoint(
    task="完成 API 设计",
    decisions=["使用 REST", "JSON 格式"],
    todos=["实现端点", "添加测试"]
)

# 关键信息
entry_id = mm.mark_key_info(
    content="服务器密码: xxxxxx",
    tags=["#credential", "#server"]
)

# 检测触发词
is_key, content = mm.detect_key_triggers("记住这个：明天开会")
if is_key:
    mm.mark_key_info(content)
```

## 文件结构

```
workspace/
├── memory/
│   ├── cache.json              # 短期记忆 (50条)
│   ├── key_facts.md            # 关键信息记录
│   ├── 2026-02-05.md           # 每日归档
│   └── ...
├── checkpoints/
│   ├── checkpoint_2026-02-05_14-30.json
│   ├── checkpoint_2026-02-05_14-00.json
│   └── ... (最多10个)
└── skills/
    └── galatea-memory/
        ├── memory_manager.py
        ├── SKILL.md
        └── README.md
```

## 集成到 Agent

在 `AGENTS.md` 中添加：

```markdown
## Memory Management

### 会话开始
1. 读取 `memory/cache.json` 恢复短期记忆
2. 检查最近检查点状态

### 会话中
1. 检测用户消息中的关键信息触发词
2. 任务完成时自动创建检查点
3. 重要决策写入短期记忆

### 会话结束
1. 创建最终检查点
2. 归档短期记忆到每日文件
```

## 与现有系统集成

- **elite-longterm-memory**: 作为补充层，cache.json 对应 HOT RAM
- **Notion**: 关键信息自动同步 (需配置 API key)
- **memory/YYYY-MM-DD.md**: 自动归档目标
- **SESSION-STATE.md**: 与检查点系统协同

## 配置

环境变量：
```bash
export GALATEA_WORKSPACE=/root/.openclaw/workspace
```

## 注意事项

- cache.json 最大 50 条，超出自动归档
- checkpoints 保留 10 个，超出自动删除最旧的
- key_facts.md 使用 Markdown 格式，便于人工阅读
- Notion 同步需要额外配置 API key
