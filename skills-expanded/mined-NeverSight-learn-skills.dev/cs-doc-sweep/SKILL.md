---
name: cs-doc-sweep
description: 手动触发的 CodeStable 文档熵清理工作流。用于用户明确要求"清理旧设计文档"、"做文档熵检查"、"分析 features/issues/refactors 哪些还有效"、"这个新 feature 推翻了旧方案"、"全项目扫一遍旧 spec 是否重复/过期"时。不会由 feature-accept、issue-fix、refactor 等工作流主动触发。
---

# cs-doc-sweep

## 启动必读

开始任何判断或动作前，先读取 `.codestable/attention.md`；缺失则视为骨架不完整，提示先补齐或运行 `cs-onboard`，不要回退到外部 AI 入口文件。

`cs-doc-sweep` 是**手动维护技能**。只有用户明确要求清理 / 分析文档有效性时才运行；其他 `cs-*` 工作流完成后不主动推荐、不自动触发。

本技能处理的是：`.codestable/features/`、`.codestable/issues/`、`.codestable/refactors/` 里的单次动作 spec 越积越多，旧方案被新方案吸收或推翻后仍被检索到，导致人和 AI 误判当前设计。

---

## 两种模式

| 模式 | 用户意图 | 产物 |
|---|---|---|
| **anchor** | 围绕某个已完成 feature / issue / refactor，清理它吸收或推翻的旧文档 | 新锚点同目录的 `{slug}-doc-sweep.md` |
| **project** | 深度探索整个项目文档，分析每份 spec 当前是否还有效，并纠正文档生命周期标记 | `.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md` |

用户没有指定模式时先问一句：是围绕某个完成项清理，还是全项目扫一遍。

---

## 清理不是删除

feature / issue / refactor 是"单次动作"证据。即使旧设计已经不是当前设计，也可能解释当时为什么这么做、为什么后来推翻。

默认动作：

- **有效**：仍能表达独立历史事实或仍是当前设计背景；不改
- **被吸收**：旧文档说的是同一个需求 / 问题，新文档已完整覆盖；旧文档标 `lifecycle: absorbed`
- **被取代**：新文档明确否定旧设计 / 修复路径 / 重构方案；旧文档标 `lifecycle: superseded`
- **相关但不清理**：有背景关系，但不是同一件事；只在报告里列相关
- **不确定**：证据不足；不改，交给用户决定

物理删除只允许在用户明确要求，且目标是空目录、未确认草稿、临时 spike 这类无追溯价值内容。否则只标记不删。

---

## 文件放哪儿

anchor 模式：

```text
.codestable/
├── features/YYYY-MM-DD-{slug}/
│   ├── {slug}-acceptance.md 或 {slug}-ff-note.md   ← 新锚点
│   └── {slug}-doc-sweep.md                         ← 本技能产物
├── issues/YYYY-MM-DD-{slug}/
│   ├── {slug}-fix-note.md                          ← 新锚点
│   └── {slug}-doc-sweep.md
└── refactors/YYYY-MM-DD-{slug}/
    ├── {slug}-apply-notes.md 或 {slug}-refactor-note.md
    └── {slug}-doc-sweep.md
```

project 模式：

```text
.codestable/doc-sweeps/YYYY-MM-DD-{slug}/
└── index.md
```

`doc-sweeps/` 不存在就创建。它是维护报告目录，不放 feature / issue / refactor 的原始 spec。

---

## 工作流

### Phase 1：确定模式和范围

**anchor 模式**：

1. 读用户指定的新 feature / issue / refactor 目录；未指定就从最近完成的目录里让用户确认一个。
2. 验证锚点已完成：acceptance checks 全 `passed`、ff-note 完整、fix-note 完整、apply-notes 完整。
3. 提取关键词：slug、summary、tags、requirement、roadmap_item、涉及模块、主要文件路径。

**project 模式**：

1. 确认范围：全 `.codestable/`，还是只扫 features / issues / refactors 某一类。
2. 读取 `.codestable/reference/shared-conventions.md`、`architecture/` 总入口、`requirements/VISION.md`（如有）、roadmap items（如有）。
3. 为本次维护生成 slug，如 `spec-validity`、`auth-doc-sweep`。

### Phase 2：建立文档清单

用工具拿清单，再用 `rg` 补漏。只扫描实际存在的目录；缺失目录视为空集合，并在报告的"扫描范围"里记一句：

```bash
for d in .codestable/features .codestable/issues .codestable/refactors; do
  [ -d "$d" ] && python .codestable/tools/search-yaml.py --dir "$d" --json
done

rg -n "doc_type:|feature:|issue:|refactor:|lifecycle:" \
  .codestable/features .codestable/issues .codestable/refactors 2>/dev/null || true
```

project 模式要把清单按 `requirement` / `roadmap` / `tags` / 模块路径 / 关键术语聚类。先处理最相关或最高风险的簇，避免一次扫成大而空的报告。

### Phase 3：判定有效性

逐个候选读关键文件，不靠文件名猜。

| 关系 | 判据 | 动作 |
|---|---|---|
| `valid` | 文档仍表达独立历史事实，或仍是当前设计背景 | 不改 |
| `absorbed` | 旧文档和新目标解决同一个需求 / 问题，新目标完整覆盖旧内容 | 标旧文档 `lifecycle: absorbed` + `absorbed_by` |
| `superseded` | 新目标明确推翻旧设计、旧修法、旧重构路径 | 标旧文档 `lifecycle: superseded` + `superseded_by` |
| `related` | 有背景关系但不是同一件事，也未被推翻 | 不改，只列相关 |
| `uncertain` | 看起来重叠但证据不足 | 不改，列给用户决定 |

判定必须写一句证据：旧文档的具体主张 + 当前有效文档 / 当前代码 / architecture 如何覆盖或否定它。

### 判定例子

- 旧 feature 设计"导出 CSV 由同步接口直接生成"，新 feature 验收后变成"异步任务 + 下载中心"且覆盖同一个导出需求 → `superseded`
- 旧 issue 记录"空列表导出报错"，新 feature 的导出重构已覆盖空列表 / 大列表 / 权限失败三类场景 → `absorbed`
- 旧 refactor 拆过同一模块 helper，新 feature 只是新增调用点，没有否定旧拆分 → `related`
- 两份文档都提到"权限"，但一个是登录态校验，一个是资源授权策略 → `valid`，不是同一主题

### Phase 4：用户 review

先给用户一张表，不直接改：

| 旧文档 | 关系 | 证据 | 建议动作 |
|---|---|---|---|

用户可以改判。用户没确认前不写文件。

### Phase 5：落生命周期标记

对用户确认清理的旧文档：

1. 保留原 `status`，不要用 `status` 表示过期；它仍表示原工作流阶段。
2. 在 frontmatter 补字段：
   ```yaml
   lifecycle: absorbed | superseded
   absorbed_by: path/to/current-anchor.md      # absorbed 时
   superseded_by: path/to/current-anchor.md    # superseded 时
   lifecycle_note: "一句话说明为什么"
   ```
3. 在正文 frontmatter 后、标题前加提示：
   ```markdown
   > 本文档已被 {current-anchor} 吸收/取代。当前实现与设计以新文档及 architecture / requirement 为准。
   ```
4. 在当前有效文档 frontmatter 补：
   ```yaml
   supersedes:
     - path/to/old.md
   absorbs:
     - path/to/old.md
   ```

project 模式里找不到明确 current-anchor 时，不写生命周期字段，只在报告列为 `uncertain` 或 `related`。

### Phase 6：写报告

anchor 模式写 `{slug}-doc-sweep.md`；project 模式写 `index.md`。模板：

```markdown
---
doc_type: doc-sweep
mode: anchor | project
anchor: path/to/current-anchor.md  # project 模式可空
date: YYYY-MM-DD
status: completed
---

# {slug} doc sweep

## 扫描范围

## 聚类 / 候选

## 判定结果

## 已修改文件

## 保留未改

## 未决
```

未决项不阻塞完成，但要明确告诉用户：这些旧文档还可能造成检索噪音，建议之后单独判断。

---

## 与相邻工作流的边界

| 技能 | 边界 |
|---|---|
| `cs-feat-accept` / `cs-issue-fix` / `cs-refactor` | 它们完成实现闭环；本技能只在用户手动要求时事后维护旧 spec 生命周期 |
| `cs-arch` / `cs-req` | 维护当前系统地图和能力愿景；本技能不重写它们，但可引用它们判断 spec 是否仍有效 |
| `cs-decide` | 记录长期决定；本技能不替代决策归档，只标记历史 spec 的生命周期 |
| `cs-audit` | 主动发现代码问题；本技能扫描文档有效性，不做代码审计 |

---

## 退出条件

- [ ] 已确认 anchor / project 模式和范围
- [ ] features / issues / refactors 目标范围已建立清单
- [ ] 每个候选都有关系判定和一句证据
- [ ] 用户 review 过清理表
- [ ] 确认清理的旧文档已加 `lifecycle` 标记和正文提示
- [ ] 当前有效文档补了 `supersedes` / `absorbs`（有明确锚点时）
- [ ] anchor 模式 `{slug}-doc-sweep.md` 已写，或 project 模式 `index.md` 已写

---

## 容易踩的坑

- 在 feature / issue / refactor 收尾时主动推销本技能；它必须由用户手动触发
- 把历史文档直接删掉，导致决策来源丢失
- 用 `status: outdated` 覆盖旧 design 的 `status: approved`，破坏原工作流语义
- 只按标题相似就判 absorbed，不读旧文档正文
- project 模式没有明确 current-anchor 却强行标 absorbed / superseded
- 不写 sweep 报告，三个月后没人知道为什么旧文档被标记

---

## 相关文档

- `.codestable/reference/shared-conventions.md` — `lifecycle` 字段、目录结构
- `.codestable/reference/tools.md` — `search-yaml.py` / `validate-yaml.py` 用法
- `.codestable/reference/system-overview.md` — CodeStable 技能路由总览
- `.codestable/attention.md` — 启动必读的项目注意事项
