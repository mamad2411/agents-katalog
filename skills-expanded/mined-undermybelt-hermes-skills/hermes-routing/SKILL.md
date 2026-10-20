---
name: hermes-routing
description: 配置 Hermes 技能路由与中文关键词触发 — 修改 skill-router.md、project-router.md、skill-index.json，为新技能集添加中文路由映射。
---

# Hermes 路由配置

为新安装的技能集（如 Aegis）添加路由规则和中文关键词触发。

## 触发条件
- 用户要求为新技能集添加路由 / 索引
- 用户说某个技能未命中 / 没用上，需排查路由
- 用户说“帮赫尔墨斯设置这个的。路由规则跟索引，中文关键词触发”

## 路由文件

| 文件 | 用途 |
|------|------|
| `~/.hermes/routing/skill-router.md` | 主路由表，含中文关键词→路由别名映射 |
| `~/.hermes/routing/project-router.md` | 本地仓库覆盖 |
| `~/.hermes/routing/skill-index.json` | 技能索引，含触发词数组 |

## 完整工作流程

### 0. 安装或更新外部 skill 源 repo

当用户要求安装/更新一个 GitHub 上的 skill 包（如 Aegis、Day1Global、UZI-Skill 等）：

```bash
# 克隆或快进源 repo
cd ~/.hermes/external-repos
if [ -d <RepoName> ]; then
  cd <RepoName> && git pull --ff-only
else
  git clone https://github.com/<owner>/<repo>.git <RepoName>
fi
```

**安全审查**：先读 README、install 入口、可执行文件，确认无 `npx`/`pip install`/`setup.sh`/自动部署脚本。标记 `security_review: true` 若含外部 API 调用或本地脚本。

### 0.1 检测新增/变更 skill

```bash
# 比对源 repo 与已安装目录的差异
# 列出源 repo 的 skills
ls -1 ~/.hermes/external-repos/<RepoName>/skills/
# 列出已安装的 skills
ls -1 ~/.hermes/skills/<category>/
# md5 差异检测（发现内容变更）
for skill in <existing-skill-names>; do
  src=$(md5 -q ~/.hermes/external-repos/<RepoName>/skills/$skill/SKILL.md)
  dst=$(md5 -q ~/.hermes/skills/<category>/$skill/SKILL.md)
  [ "$src" != "$dst" ] && echo "DIFF: $skill"
done
```

### 0.2 同步 skill 文件

```bash
# 全量同步（覆盖已有，添加新增）
rsync -a --delete ~/.hermes/external-repos/<RepoName>/skills/ ~/.hermes/skills/<category>/
# 验证数量
ls -1 ~/.hermes/skills/<category>/ | wc -l
```

### 1. 收集技能信息

```bash
ls ~/.hermes/skills/<技能集目录>/
```

读取每个 `SKILL.md` 的 `description:` 行，提取技能描述。

### 2. 更新 skill-router.md

在相应段落下新增路由区块，格式：

```markdown
## <技能集名> quick routes
- <中文关键词1> / <中文关键词2> / <英文触发词> -> `<别名>/<技能名>`
```

- 别名遵循现有项目中的缩写规则（如 `aegis/`）
- 中文关键词覆盖常见任务场景（如“头脑风暴 / 方案构思 / 需求梳理”）
- 放在 `## community oh-story quick routes` 或其他合适位置之后

### 3. 更新 project-router.md

三处必须更新：

**(a) 源 repo 列表**：在 `### External skill/source repos under ~/.hermes/external-repos` 下添加：

```markdown
 - <RepoName>: `~/.hermes/external-repos/<RepoName>`
```

**(b) Runtime skill root**：在 `- Runtime skill roots:` 段添加：

```markdown
 - <技能集名> skills: `~/.hermes/skills/<category>` (<N> skills)
```

**(c) Route aliases**：在 `- Route aliases:` 段添加中文触发映射：

```markdown
 - <技能集名> / <中文关键词> -> `<alias>/<skill-name>`
```

### 4. 更新 skill-index.json

为每个技能新增一条索引记录：

```json
{
  "name": "<alias>/<技能名>",
  "category": "<alias>",
  "original_category": "<alias>",
  "grade": "good",
  "priority": 80,
  "security_review": false,
  "supersedes": [],
  "triggers": ["<中文触发词1>", "<中文触发词2>", ...],
  "description": "<技能描述>",
  "path": "<SKILL.md 绝对路径>",
  "original_path_key": "<alias>/<技能名>",
  "source_repo": "https://github.com/<owner>/<repo>",
  "source_path": "~/.hermes/external-repos/<RepoName>",
  "runtime_path": "<SKILL.md 绝对路径>"
}
```

**使用 execute_code/terminal python3 程序化追加**（避免手动编辑大数据集）：

```python
import json, os

home = os.path.expanduser("~")
index_path = os.path.join(home, ".hermes", "routing", "skill-index.json")

with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

existing_names = {e["name"] for e in index}
for entry in new_entries:
    if entry["name"] not in existing_names:
        index.append(entry)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
```

### 4.1 更新 skill-index.md

`skill-index.md` 是 `skill-index.json` 的 markdown 表格镜像。必须同步新增：

```markdown
## <alias>

| Route | Grade | Priority | Triggers | Path |
|-------|-------|----------|----------|------|
| `<alias>/<skill-name>` | good | 80 | <triggers...> | `/path/to/SKILL.md` |
```

**用 python3 生成行**并追加到文件末尾。

### 5. 验证一致性

四项计数必须对齐：

```bash
# skill 文件数
ls -1 ~/.hermes/skills/<category>/ | wc -l

# index.json 条目数
python3 -c "
import json
d=json.load(open('$HOME/.hermes/routing/skill-index.json'))
print(sum(1 for e in d if e.get('category')=='<alias>'))
"

# 路由文件行数
rg -c '<alias>/' ~/.hermes/routing/skill-router.md
rg -c '<alias>/' ~/.hermes/routing/project-router.md
rg -c '<alias>/' ~/.hermes/routing/skill-index.md

# 路径存在性检查
python3 -c "
import json, os
d=json.load(open('$HOME/.hermes/routing/skill-index.json'))
missing=[e['name'] for e in d if e.get('category')=='<alias>' and not os.path.exists(e['path'])]
print(f'missing_paths={missing}')
"
```

### 5.1 写 project-router.md 协作日志

在文件末尾追加完成记录：

```markdown
### <timestamp> CST - Done - <技能集名> update + Chinese routing/index
- Owner: Hermes CLI.
- Status: Done.
- Source: `<repo URL>`, commit `<hash>`.
- Source root: `<path>`.
- Runtime root: `<path>` (<N> skills).
- Changes: <new/updated/diff summary>.
- Routing artifacts updated: skill-router.md, project-router.md, skill-index.json, skill-index.md.
- Verification: <counts + missing_paths result>.
- Security note: <any security_review flags or "no scripts executed">.
```

### 6. 生效

Hermes `/reset` 或重启会话后，中文关键词自动命中对应路由。

## 中文触发词设计原则

- 每技能 10-15 个中文触发词
- 覆盖：任务场景（如“排错”）、方法论名（如“TDD”）、关键概念（如“基线先行”）
- 同时保留英文原名作为触发词
- 添加简短的助手指令形式（如“为什么不行”“帮我查一下”）

## 已验证案例：Aegis 17 技能路由

| 用户说 | 触发技能 |
|--------|---------|
| 头脑风暴 / 方案构思 | `aegis/brainstorming` |
| 排错 / 调试 / 根因分析 | `aegis/systematic-debugging` |
| TDD / 测试驱动 / 红绿重构 | `aegis/test-driven-development` |
| 验证完成 / 确认无误 | `aegis/verification-before-completion` |
| 长任务 / 断点续传 | `aegis/long-task-continuation` |
| 架构驱动开发 / 基线先行 | `aegis/using-aegis` |
| 写技能 / 创建 skill | `aegis/writing-skills` |

## 已知陷阱

- `skill-index.json` 约 750KB+，不可直接读取全量用于 patch
- 使用 `execute_code`/terminal python3 进行 JSON 操作
- 操作前始终备份原文件（`cp <file> <file>.backup`）
- 不要删除现有条目
- 路由别名全名必须 ≤64 字符（Codex 兼容）
- `skill-index.md` 必须与 `skill-index.json` 同步更新，否则 markdown 镜像会过时
- `project-router.md` 三处必须同时更新：源 repo 列表、runtime root 列表、route aliases 列表
- 协作日志是验证证据的关键载体，必须记录变更摘要和安全审查结果
- `rsync -a --delete` 会删除目标端多余文件——确认目标目录仅含该技能集的文件
- 外部 skill 包可能含安装脚本/可执行文件——只同步 SKILL.md 等文档，不同步 `.sh`/`setup.py`/可执行二进制