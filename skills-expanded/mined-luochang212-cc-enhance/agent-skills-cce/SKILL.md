---
name: agent-skills-cce
description: Skill 管理与市场导航。当需要安装、搜索、删除、备份 skills，查找新技能，管理上下文预算，或用户询问「有什么好用的skill」「怎么装skill」「skill太多了怎么办」时，必须使用此技能。核心纪律：工具箱不是仓库。
---

> 来自 [cc-enhance](https://github.com/luochang212/cc-enhance)。`-cce` 后缀表示此技能由 cc-enhance 项目安装，避免与本地同名技能冲突。

# Skills

## 获取 → 搜索 → 下载 → 存放 → 使用

### 1. 从哪里获取

| 市场 | CLI 工具 | 实测 |
|------|------|------|
| [skills.sh](https://skills.sh) | `npx skills add owner/repo` | ✅ 已测 |
| [lobehub.com/skills](https://lobehub.com/skills) | `@lobehub/market-cli` | ✅ 已测 |
| [modelscope.cn/skills](https://modelscope.cn/skills) | `npx skills add <url>` | ✅ 已测 |
| [skillhub.cn](https://skillhub.cn) | `curl install.sh \| bash` | ⚠️ 脚本已审查，未执行 |

→ 各市场详细命令见 [references/marketplaces.md](references/marketplaces.md)
→ 推荐直接安装的 skill 仓库见 [references/recommended.md](references/recommended.md)

### 2. 如何搜索

**skills.sh**——让 Claude 用搜索工具找：
```
用 Tavily 搜 "site:github.com <功能> skill SKILL.md Claude Code"
```

**LobeHub**——CLI 搜索，返回 stars/installs：
```bash
npx -y @lobehub/market-cli skills search --q "<关键词>"
```

**ModelScope**——网站上按分类浏览，或：
```bash
npx skills find
```

**SkillHub**——网站浏览（skillhub.cn），或搜索工具搜「skillhub.cn <关键词>」。

### 3. 如何下载

```bash
# GitHub 仓库（skills.sh 索引的）
npx skills add stared/vibe-commit

# ModelScope URL
npx skills add https://modelscope.cn/skills/@Alipay/alipay-payment-integration

# LobeHub
npx -y @lobehub/market-cli skills install <identifier> --agent claude-code

# SkillHub
curl -fsSL https://skillhub.cn/install/install.sh | bash
```

### 4. 存放在哪 —— 关键差异

| 工具 | 安装路径 | 机制 |
|------|------|------|
| `npx skills add` | `.agents/skills/<name>/` | 实体文件在此，symlink 到各 agent 目录 |
| `@lobehub/market-cli` | `.claude/skills/<name>/` | 直接安装到 Claude Code 目录 |

### 5. 如何使用

Skill 安装后，Claude Code 会话启动时自动发现并加载。**安装 = 启用**，无需手动激活。

验证：
```bash
ls .agents/skills/                    # npx skills 安装的
ls .claude/skills/                    # LobeHub 安装的
npx skills list                       # 列出所有
head -5 .agents/skills/*/SKILL.md     # 查看 skill 描述
```

---

## 管理：工具箱，不是仓库

### 核心纪律

Skill 目录不是囤积处。每多一个 skill 就多一份上下文开销：
- 每个 SKILL.md 约 1-5K token
- 10 个常驻 skill ≈ 10-50K token 的基础开销

### 备份而非堆积

不常用但想保留的 skill —— 记录来源，删除实体：

```bash
# 备份当前清单
npx skills list > ~/.claude/skills-backup.txt

# 删除不用的
npx skills remove <name>
```

备份记录应包含：skill 名称、安装来源（repo/URL/marketplace）、安装日期、用途。需要时精确找回，不需要时不占上下文。

### 定期审查

- 这个 skill 上次用是什么时候？
- 删了它我现在能完成同样的任务吗？
- 它和另一个 skill 功能重叠吗？

「不记得」「能」「重叠」→ 删除。

## 环境依赖

| 依赖 | 用途 | 安装方式 | 磁盘 | 必需 |
|------|------|----------|------|------|
| npx / Node.js | skill 包管理器，安装/搜索/删除 | 安装 Node.js（含 npx） | ~100MB | 是 |
