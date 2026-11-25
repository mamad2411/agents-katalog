---
name: import-claude-skills
description: 将 Claude Code 风格的技能仓库检查、筛选并改造成 Codex 技能。适用于需要查看第三方技能仓库、识别其中可复用的 SKILL.md 工作流、把兼容技能复制到 `~/.codex/skills`，或在迁移前识别 Claude 专属假设与限制的场景。
---

# 导入 Claude 技能

检查本地的 Claude Code 风格技能仓库，并只把真正有价值、兼容的技能迁移到 Codex。

## 快速开始

1. 确认来源已经在本地。优先使用本地克隆仓库或解压后的 ZIP。
2. 运行 `scripts/list_claude_skills.py <repo-path>`，列出候选技能目录及其触发说明。
3. 只读取与你当前目标相关的源 `SKILL.md`。
4. 在导入前检查是否存在 Claude 专属依赖：
   - slash commands 或命令面板
   - Codex 没有的 hooks 或 agent 编排
   - 写死的 `.claude/` 路径
   - 本机并不存在的 MCP 或额外工具要求
5. 用 `scripts/import_skill.py <source-skill-dir>` 导入目标技能。
6. 打开导入后的技能，把描述、路径和流程改造成更适合 Codex 的版本。

## 先判断什么值得迁移

优先迁移这些类型：

- `SKILL.md` 里主要是可执行工作流
- `scripts/` 里有可复用脚本
- `references/` 里有长期有用的参考资料
- `assets/` 里有模板、样例或资源文件

这些要谨慎处理，不要直接照搬：

- 强依赖 Claude 专属命令或 UI 的技能
- 默认采用另一套目录结构的技能
- 严重依赖远程安装器或 shell 别名的技能
- 巨型“技能大仓库”里和当前目标无关的部分

如果来源是 `everything-claude-code`，先读 [ecc-porting-notes.md](./references/ecc-porting-notes.md)。

## 导入流程

### 1. 扫描

运行：

```powershell
python scripts/list_claude_skills.py <repo-path>
```

根据输出，只保留和当前任务真正相关的技能候选。

### 2. 检查

打开入选技能的 `SKILL.md`，重点看：

- 哪些触发描述值得保留
- 哪些脚本和参考资料需要一起带过来
- 哪些仓库专属说明应该重写或删除

不要把一个大仓库里所有文件一口气全读进来。

### 3. 复制

运行：

```powershell
python scripts/import_skill.py <source-skill-dir>
```

导入器只复制常见技能核心内容：

- `SKILL.md`
- `agents/`
- `scripts/`
- `references/`
- `assets/`

会跳过 `README.md`、安装说明、变更记录等仓库噪音。

### 4. 改造

复制完成后，继续把它改成 Codex 可用版本：

- 重写 Claude 专属表达
- 更新路径、例子和命令
- 去掉依赖本机不存在工具的说明
- 保持前置描述里“什么时候使用这个技能”足够明确

### 5. 校验

运行 `skill-creator` 自带校验器：

```powershell
python C:\Users\nd851\.codex\skills\.system\skill-creator\scripts\quick_validate.py <imported-skill-path>
```

把报错修完后，再认为这个技能迁移完成。

## 默认设置

- 默认目标根目录：`C:\Users\nd851\.codex\skills`
- 默认导入方式：使用源技能同名目录
- 默认行为：如果目标已存在则报错，除非显式传入 `--force`

## 使用提醒

- 优先做一个干净、聚焦的 Codex 技能，不要整仓镜像
- 如果用户只给 GitHub 链接，先落地为本地仓库或解压包再使用脚本
- 导入后要继续瘦身，删掉不会帮助 Codex 执行的内容
