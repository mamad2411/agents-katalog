---
name: link-all-skills
description: "批量链接并安装一个仓库中的全部活跃 Skills。当用户说链接所有 skills、link all skills、批量安装或初始化整个 skills 仓库时使用。"
---

# 批量链接 Skills

## 优先路径

如果当前仓库根目录存在经过审计的 `install.sh`，优先执行它：

```bash
./install.sh --all
```

`jacky-skills/install.sh` 会：

1. 检查 Node.js 与 `j-skills`。
2. 扫描 `plugins/`、`skills/` 和 `harness/` 中的 `SKILL.md`。
3. 排除 `archived/`。
4. 逐个核对 registry 和软链接目标。
5. 已正确链接时跳过；发现链接冲突时停止，不覆盖。
6. 安装到 `J_SKILLS_ENVS` 指定的环境，默认为 `claude-code,codex`。

覆盖目标环境：

```bash
J_SKILLS_ENVS=claude-code,codex,cursor ./install.sh --all
```

只安装一个 Skill 或 Plugin 时使用：

```bash
./install.sh --skill <skill-name>
./install.sh --plugin <plugin-name>
```

## 通用仓库回退流程

当仓库没有自带脚本时，按以下步骤执行。

### 1. 发现 Skill

```bash
find plugins skills \
  -type d -name archived -prune -o \
  -type f -name SKILL.md -print
```

不得扫描或安装 `archived/` 下的 Skill。

### 2. 逐个链接

对每个 `SKILL.md` 读取 frontmatter `name`，再执行：

```bash
j-skills link /path/to/skill --json
```

链接前先用以下命令检查同名项：

```bash
j-skills link --list --json
```

- 同名项指向当前 Skill 目录：跳过链接。
- 同名项指向其他目录：报告“链接冲突”并停止，不自动 unlink 或覆盖。

### 3. 逐个安装

```bash
j-skills install skill-name --global --env claude-code,codex --json
```

要安装到更多环境时，修改逗号分隔的 `--env` 值。

### 4. 验证

```bash
j-skills link --list --json
j-skills list --global --json
```

核对项：

- 发现的 Skill 数与链接数一致。
- 每个链接指向预期源目录。
- 目标 Agent 环境中存在对应 Skill。
- 不包含任何 `archived/` Skill。

## 约束

- 不假设 `j-skills` 支持批量选项；0.1.0 需要逐 Skill 执行。
- 不吞掉链接或安装失败。
- 不因“批量”而扩大到全局清理、删除或覆盖现有 Skill。
- 不在未确认目标环境时猜测安装位置。
