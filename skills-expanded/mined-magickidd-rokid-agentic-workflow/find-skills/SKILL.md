---
name: find-skills
description: "Skills 发现、安装与安全审核。当需要查找可用 Skills、搜索新 Skills、添加第三方 Skills、或审核 Skill 安全性时使用。触发词：查找skills、搜索skills、安装skill、添加skill、skill安全审核、find skills。"
version: 1.1.0
---

# Find Skills - 发现、安装与安全审核

查找本地可用 Skills，搜索并安全安装第三方 Skills。

## 仓库信息

- **本地路径**: `~/.cursor/skills/`
- **远程仓库**: https://github.com/<your-org>/<your-skills-repo>
- **分支**: main
- **搜索日志**: `~/.cursor/skills/.search-log.jsonl`

---

## 一、查找本地 Skills

### 1.1 列出所有 Skills（带触发说明）

扫描所有 SKILL.md，自动提取 `description` 字段，输出格式：

```
Use <skill-path>/SKILL.md — <description>
```

执行方式（AI 代为执行）：

```bash
cd ~/.cursor/skills && find . -name "SKILL.md" -type f | sort | while read f; do
  desc=$(grep -m1 "^description:" "$f" 2>/dev/null | sed 's/^description: *//;s/^"//;s/"$//')
  if [ -n "$desc" ]; then
    echo "Use $f — $desc"
  else
    echo "$f"
  fi
done
```

### 1.2 按关键词搜索（同时搜索内容和路径）

```bash
PATTERN="关键词"
cd ~/.cursor/skills && {
  grep -E -r -l -- "$PATTERN" --include="SKILL.md" 2>/dev/null || true
  find . -name "SKILL.md" -type f 2>/dev/null | grep -E -- "$PATTERN" 2>/dev/null || true
} | sort -u | while read f; do
  desc=$(grep -m1 "^description:" "$f" 2>/dev/null | sed 's/^description: *//;s/^"//;s/"$//')
  if [ -n "$desc" ]; then
    echo "Use $f — $desc"
  else
    echo "$f"
  fi
done
```

### 1.3 搜索日志（发现缺失的 Skill 需求）

每次搜索自动记录到日志文件，用于追踪高频搜索和未匹配的需求：

```bash
# 记录搜索（AI 每次搜索时自动执行）
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"query\":\"$PATTERN\",\"results\":$COUNT}" \
  >> ~/.cursor/skills/.search-log.jsonl

# 查看搜索历史
cat ~/.cursor/skills/.search-log.jsonl

# 分析高频但无结果的搜索（发现需要创建的 Skill）
grep '"results":0' ~/.cursor/skills/.search-log.jsonl
```

**为什么要记录**：如果某个关键词被反复搜索但找不到匹配的 Skill，说明应该创建一个新的 Skill 来覆盖这个需求。

### 1.4 搜索策略

| 需求 | 搜索方式 |
|------|---------|
| 知道 Skill 名称 | 直接读取 `~/.cursor/skills/<name>/SKILL.md` |
| 知道功能关键词 | 用 1.2 的关键词搜索（内容 + 路径） |
| 浏览所有可用 | 用 1.1 列出所有（带 description） |
| 按类别浏览 | `ls ~/.cursor/skills/` 查看顶级目录 |
| 分析需求缺口 | 用 1.3 查看搜索日志中的未命中记录 |

---

## 二、安装第三方 Skills（必须遵循安全流程）

### 2.1 安装原则

1. **逐个审核** - 不允许批量无差别添加
2. **只添加 SKILL.md** - 默认只复制 Markdown 和数据文件（CSV/JSON/YAML）
3. **脚本需审核** - 任何可执行文件（.py/.sh/.js/.ts）必须经过安全扫描
4. **来源可信** - 优先选择高 star 数、知名组织维护的仓库

### 2.2 安全审核清单（每个 Skill 必检）

在安装任何第三方 Skill 之前，**必须逐项检查**：

#### 第一步：来源验证

- [ ] 确认仓库来源（GitHub URL、作者、star 数、fork 数）
- [ ] 检查是否有 LICENSE 文件
- [ ] 查看最近提交记录，确认活跃维护
- [ ] 检查 Issues 中是否有安全相关的报告

#### 第二步：内容扫描

对所有文件进行恶意代码扫描，检测以下危险模式：

```bash
# 在临时目录中对 skill 进行安全扫描
grep -r -E \
  "subprocess|os\.system|eval\(|exec\(|requests\.|urllib|shutil\.rm|os\.remove|import socket|curl |wget |rm -rf|sudo |nc |netcat|/dev/tcp|base64\.decode|pickle\.load|__import__|compile\(" \
  /tmp/skill_to_review/ \
  --include="*.py" --include="*.sh" --include="*.js" --include="*.ts"
```

#### 第三步：危险等级判定

| 危险等级 | 特征 | 处理方式 |
|---------|------|---------|
| **安全** | 纯 Markdown（SKILL.md），无脚本 | 直接安装 |
| **低风险** | 包含数据文件（CSV/JSON/YAML） | 检查数据内容后安装 |
| **中风险** | 包含 Python/Shell 脚本 | 逐行审核脚本后决定 |
| **高风险** | 包含网络请求、文件删除、系统调用 | 仅复制 SKILL.md，丢弃脚本 |
| **拒绝** | 包含混淆代码、base64 编码、pickle | 不安装，警告用户 |

#### 第四步：安装决策

- **安全/低风险**: 完整复制
- **中风险**: 复制 SKILL.md + 审核通过的脚本
- **高风险**: 仅复制 SKILL.md 和安全的数据文件
- **拒绝**: 不安装，输出安全报告

### 2.3 安装流程

```
1. 克隆到临时目录     → /tmp/skill_to_review/
2. 执行安全扫描       → 按清单逐项检查
3. 输出安全报告       → 告知用户风险等级
4. 用户确认后安装     → 复制到 ~/.cursor/skills/
5. 提交并同步         → git add + commit + push
6. 清理临时目录       → rm -rf /tmp/skill_to_review/
```

### 2.4 标准安装命令

```bash
# 1. 克隆到临时目录
git clone --depth 1 <repo-url> /tmp/skill_to_review

# 2. 安全扫描（必须执行）
grep -r -E "subprocess|os\.system|eval\(|exec\(|requests\.|urllib|curl |wget |rm -rf|sudo " \
  /tmp/skill_to_review/ \
  --include="*.py" --include="*.sh" --include="*.js" --include="*.ts"

# 3. 安全的话，只复制 SKILL.md 和数据文件
mkdir -p ~/.cursor/skills/<skill-name>
cp /tmp/skill_to_review/path/to/SKILL.md ~/.cursor/skills/<skill-name>/

# 4. 提交同步
cd ~/.cursor/skills && git add -A && \
  git commit -m "feat: 添加 <skill-name>（已审核安全）" && \
  git push origin main

# 5. 清理
rm -rf /tmp/skill_to_review
```

---

## 三、推荐的可信 Skill 来源

| 来源 | URL | 信任度 | 说明 |
|------|-----|--------|------|
| **Anthropic 官方** | https://github.com/anthropics/skills | 最高 | 官方示例 Skills |
| **Anthropic Claude Code** | https://github.com/anthropics/claude-code | 最高 | 官方插件中的 Skills |
| **obra/superpowers** | https://github.com/obra/superpowers-skills | 高 | 49K stars，社区顶级 |
| **K-Dense-AI** | https://github.com/K-Dense-AI/claude-scientific-skills | 高 | 8K stars，科学领域 |
| **ComposioHQ** | https://github.com/ComposioHQ/awesome-claude-skills | 中 | 33K stars，但包含大量脚本需审核 |
| **SkillsMP 市场** | https://skillsmp.com/ | 中 | 17万+ Skills，需逐个审核 |

### 不可信来源特征（拒绝安装）

- 无 LICENSE 文件
- star 数 < 10 且无知名组织背书
- 包含混淆代码或 base64 编码的可执行文件
- Issues 中有未解决的安全报告
- 要求设置环境变量中的 API Key/Token（可能窃取凭证）

---

## 四、创建自定义 Skill

### 4.1 最小 Skill 结构

```
skill-name/
└── SKILL.md          # 必须：包含 YAML frontmatter + Markdown 指令
```

### 4.2 SKILL.md 模板

```markdown
---
name: skill-name
description: "简明描述 Skill 的功能和使用场景。触发词：关键词1、关键词2。"
version: 1.0.0
---

# Skill 名称

简要说明 Skill 的用途。

## 使用场景

- 场景 1
- 场景 2

## 操作指南

[具体的操作步骤和指令]
```

### 4.3 创建后必须同步

```bash
cd ~/.cursor/skills && git add -A && \
  git commit -m "feat: 创建 <skill-name>" && \
  git push origin main
```

---

## 五、Skills 管理规范

### 5.1 目录结构约定

```
~/.cursor/skills/
├── .git/                      # Git 仓库
├── README.md                  # Skills 总览
├── _global_rules/             # 全局规则（非 Skill）
├── brainstorming/             # 头脑风暴
├── claude-scientific-skills/  # 科学领域 Skills（142个子技能）
├── document-skills/           # 文档处理（docx/pdf/pptx/xlsx）
├── expert-collaboration/      # 专家协作
├── expert-debate/             # 专家辩论
├── find-skills/               # 本 Skill：发现与安全安装
├── frontend-design/           # 前端设计（Anthropic 官方）
├── internalized-cognition/    # 内化认知
├── kaizen/                    # 持续改进
├── llm-test-standard/         # LLM 测试标准
├── my-repositories/           # 个人仓库管理
├── planning-with-files/       # 文件规划
├── project-documentation/     # 项目文档
├── prompt-engineering/        # 提示工程
├── skill-creator/             # Skill 创建指南
├── software-architecture/     # 软件架构
├── subagent-driven-development/ # 子代理驱动开发
├── superpowers/               # Superpowers 技能集
├── sync-skills/               # 同步 Skills
├── test-driven-development/   # TDD
└── ui-ux-pro-max-skill/       # UI/UX 设计智能
```

### 5.2 变更后必须同步

任何 Skill 的增删改后，执行：

```bash
cd ~/.cursor/skills && \
  git add -A && \
  git commit -m "<type>: <描述>" && \
  git push origin main
```

Commit 类型：
- `feat`: 新增 Skill
- `fix`: 修复 Skill
- `docs`: 更新文档
- `refactor`: 重构 Skill
- `chore`: 清理/维护

### 5.3 在新电脑上恢复

```bash
git clone https://github.com/<your-org>/<your-skills-repo>.git ~/.cursor/skills
```

---

## 六、安全审核报告模板

安装第三方 Skill 后，必须输出以下格式的审核报告：

```
## 安全审核报告

- **Skill 名称**: xxx
- **来源**: https://github.com/xxx/xxx
- **Star 数**: xxx
- **危险等级**: 安全 / 低风险 / 中风险 / 高风险
- **扫描结果**: 未发现 / 发现 N 处可疑代码
- **处理方式**: 完整安装 / 仅安装 SKILL.md / 拒绝安装
- **安装文件**: 列出实际复制的文件
- **排除文件**: 列出被排除的文件及原因
```
