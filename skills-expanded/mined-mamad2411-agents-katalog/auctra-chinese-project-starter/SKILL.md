---
name: auctra-chinese-project-starter
description: Use when starting or onboarding a Chinese Auctra creator project, especially Chinese novels with zh-CN/chinese-novel layout, scenario doctor/gate checks, materials, outlines, character setup, first chapter planning, and review/export boundaries.
---

# Auctra 中文项目启动器

把中文创作者从空目录带到可审稿、可生成、可导出的 Auctra 项目。默认用中文沟通，但命令、flag、JSON 字段和 agent facts 保持英文。

## 输入

- 项目类型：中文小说、短篇、连载、内容运营、改编或平台内容。
- 作品标题、类型、目标读者、风格、已有素材、是否已有 Auctra 项目。
- 需要的起步阶段：新建项目、迁移布局、素材入库、大纲/人物/首章规划、scenario doctor、gate check 或导出准备。

## 工作流

1. 确认项目路径和阶段；已有项目先建议 `auctra project status --path <path> --json` 和 `auctra project next --path <path> --json`。
2. 新中文小说项目使用：

```bash
auctra project init ./chichao --title "赤巢备案" --genre "玄幻悬疑" --locale zh-CN --layout chinese-novel --json
cd ./chichao
```

3. 解释目录：`章节/` 放导入章节 Markdown，`素材/` 放研究/设定/摘录，`大纲/`、`人物/`、`设定/` 放作者可读 planning 文件，`导出/` 放 manual handoff。`.auctra/` 是机器真源，不手写。
4. 安装或检查场景时使用真实命令：

```bash
auctra scenario doctor --json
auctra gate check --before chapter_write --json
```

5. 素材先入库，再规划：

```bash
auctra material add --kind note --title "备案制度" --from 素材/备案制度.md --json
auctra chapter import markdown ./章节
auctra project next --json
```

6. 若需要原创首章而不是导入旧稿，先交给 `chinese-novel-brief-architect`、`chinese-novel-outline-architect`、`chinese-novel-character-architect` 或 `chinese-novel-scene-card-writer` 形成可执行 brief/scene card，再走 Auctra generation/review。
7. 生成或分析使用 fixture/real runtime 明确区分：

```bash
auctra chapter analyze ch_001 --fixture --json
auctra chapter generate ch_001 --fixture --json
auctra review list --status pending --json
```

8. 导出只作为人工交付：`auctra chapter export markdown` 默认写入 `导出/`；不得自动发布到任何平台。

## 交付格式

- 当前项目状态和缺口。
- 建议命令块，必须真实可运行。
- 需要补的作者素材：读者承诺、主角欲望/伤口、反派压力、世界规则、首章冲突、章尾钩子。
- Gate/review/export 边界和下一步。

## 边界

- 不直接编辑 `.auctra/**`、SQLite rows、review decisions、run evidence 或 export metadata。
- 不让 AI candidate 自动覆盖正文；必须进入 review queue。
- 不声称 scenario ready/first-support，除非 gate、review evidence、export/handoff 和 integration evidence 已完成。
- 不伪造真实平台发布、读者反馈、商业数据或素材来源。

## 验证

- 项目命令改动后运行窄 Go 测试和 `openspec validate auctra-i18n-workspace-layout --strict`。
- Skill 改动后运行 `python3 scripts/validate_skills.py`；宿主 profile、同步和 runtime 校验由接入该仓库的宿主项目负责。
