---
name: scan-skill-repos
description: "扫描 GitHub 上符合标准的 Agent Skill 仓库，校验 SKILL.md 布局与 frontmatter，解析版本和分类，并把通过复核的条目合并进 third_party_skill 的中英文目录。用于发现新 skill、刷新目录 Star 与版本、按关键词或星标阈值筛选候选时。"
metadata:
  version: "1.0.1"
---

# 扫描 GitHub 技能仓库

用 `scripts/scan_skill_repos.py` 发现、校验并收录第三方 Agent Skill。脚本只读取公开 GitHub 数据，写入只发生在 `--apply` 时。

## 前置条件

- 已安装并登录 GitHub CLI：`gh auth login`。
- Python 需安装 [scripts/requirements.txt](scripts/requirements.txt) 中的 PyYAML：`python -m pip install -r personal_skill/scan-skill-repos/scripts/requirements.txt`。
- 从当前工作目录向上查找同时包含 `third_party_skill/README.md` 和 `README.en.md` 的目标仓库；技能装在别处时不会把安装目录当作目标。也可用 `--repo <目录>` 显式指定；找不到目标会报错。
- 需要写目录时使用 `--apply`，否则只输出候选清单。

## 工作流

1. **扫描候选**（dry run）：

   ```bash
   python personal_skill/scan-skill-repos/scripts/scan_skill_repos.py \
       --min-stars 10000 --limit 200 --report candidates.md
   ```

   脚本同时用仓库搜索和 `filename:SKILL.md` 代码搜索，因此名称/描述里没有 "skill" 的仓库也能被发现。

2. **人工复核**。重点看两点：
   - 仓库是否以 skill 为主体，而不是产品/工具顺带放了一个 `skills/` 目录；
   - 分类是否合理，说明是否适合目标语言。
   默认解析 YAML，检查 `name`、`description` 的类型/长度、名称与技能目录一致、metadata 的字符串映射及非空正文；不以正文字数判断质量。`--no-verify` 仅用于探索候选，不表示内容已通过校验。

3. **写入目录**：

   ```bash
   python personal_skill/scan-skill-repos/scripts/scan_skill_repos.py \
       --min-stars 10000 --limit 200 --apply
   ```

   已知仓库的中英文说明优先取 [descriptions.json](references/descriptions.json)；没有覆盖时使用上游描述。写入后检查 `git diff`，必要时补充中文说明。

4. **刷新已有条目**：

   ```bash
   python personal_skill/scan-skill-repos/scripts/scan_skill_repos.py \
       --refresh --refresh-stars-only --apply
   ```

   只刷 Star 不查版本；去掉 `--refresh-stars-only` 会同时刷新版本，速度较慢。版本依次取 release、tag、包元数据、提交短 SHA，保留预发布后缀和构建信息。API 失败不会降级覆盖已知版本；刷新会保留旧值、输出失败原因并返回非零状态。

## 常用参数

| 参数 | 作用 |
|---|---|
| `--repo` | 显式指定目标目录仓库，默认从当前工作目录向上查找 |
| `--min-stars` | 星标阈值，默认 2000 |
| `--limit` | 最多校验多少个候选 |
| `--query` | 替换默认搜索词，可重复 |
| `--exclude` | 跳过指定 `owner/repo`，可重复 |
| `--no-code-search` | 关闭 `filename:SKILL.md` 代码搜索 |
| `--code-pages` / `--max-code-repos` | 代码搜索页数与仓库上限 |
| `--apply` | 把候选写入两份目录文档 |
| `--refresh` / `--refresh-stars-only` | 刷新已有条目的 Star/版本 |
| `--json` / `--report` | JSON 输出或 Markdown 报告 |

## 校验与安全

- Agent Skills 不限定技能外层容器名：支持根目录、`skills/`、`personal_skill/`、插件子目录等布局。目录名本身既不能证明有效，也不能证明仿冒，必须读取 SKILL.md 校验。格式有效不等于值得收录，产品附带的技能仍按目录选题人工取舍。
- 默认要求仓库有 LICENSE、未归档、非 fork；`--allow-no-license` 可放开。
- 分类由关键词推断，只作初筛，写入前必须人工确认。
- GitHub 代码搜索最多返回 1000 个文件结果，大规模扫描时调大 `--code-pages` 和 `--max-code-repos`。
- 描述会转义表格管道符并按行宽截断；中文目录用中文说明，英文目录用英文说明。

回归测试：在仓库根目录运行 `python -m unittest discover -s personal_skill/scan-skill-repos/tests`。测试使用临时目录和模拟 GitHub 响应，不修改实际目录、不调用 GitHub。
