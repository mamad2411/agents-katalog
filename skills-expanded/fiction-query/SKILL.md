---
name: fiction-query
description: |
  查询项目设定、角色、力量体系、势力、伏笔等信息。支持角色历史状态、实体关系、
  世界规则、伏笔/open-loop 查询。只读操作，不修改任何项目文件。
  触发方式：/fiction-query {查询内容}、「查角色」「查伏笔」「查设定」「什么状态」「那个角色叫啥来着」「进展到哪了」。
---
# fiction-query：信息查询

查询项目中的设定、状态、关系信息。只读，不修改任何文件。

## 查询分类

| 查询类型 | 关键词 | 工具 |
|---------|--------|------|
| 角色历史状态 | 某角色在第 N 章时的境界/状态变化 | 读取 `追踪/角色状态.md`、正文与 commit |
| 实体关系 | 关系/敌友/师徒/阵营归属 | 读取 `设定集/关系.md` 或相关角色卡 |
| 世界规则 | 力量规则/设定铁律/境界体系约束 | 读取 `设定集/世界观.md` 与底本 |
| 伏笔 / open loop | 伏笔/紧急伏笔/未闭合悬念 | 读取 `追踪/伏笔.md` |
| 综合 / 复杂 | 跨多种类型 | 按需组合上述只读来源 |
| 静态设定 | 角色卡/力量体系/世界观/标签格式 | 直接读取设定集并保留路径/行号 |

## 执行流程

### 1. 解析项目根

```bash
# SCRIPTS_DIR 由安装宿主指向本仓库或已安装的 scripts/ 目录。
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CODEX_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}" where)"
```

### 2. 识别查询类型

按关键词匹配上表分类。

### 3. 调用对应工具

```bash
# 查询由 AI agent 直接读取项目文件完成；本 skill 没有独立的 entity-state 等命令。
```

静态设定直接从设定集读取；底本存在时，用 commit/章节产物交叉核对。

### 4. 格式化输出

按结构化模板输出，包含：匹配类型、数据源（真源/投影层）、详细信息（含文件路径和行号）。

## 数据源优先顺序

查询时按以下顺序定位真源：
1. `.story-system/MASTER_SETTING.json` — 全局主设定
2. `.story-system/volumes/*.json` — 卷级底本
3. `.story-system/chapters/*.json` — 章级底本
4. `.story-system/commits/chapter_*.commit.json` — 写后事实
5. `.novel/state.json` / 设定集 / 追踪 — 日常查询投影层

如果 `.story-system/` 底本缺失，必须显式说明查询已降级到投影层。

## 边界

- 只读操作，不修改任何项目文件
- 数据源缺失时明确告知用户缺什么文件
- 查询无匹配时返回空结果并建议检查范围
- 不同时加载两个以上 reference，除非用户请求明确跨多种类型
- 静态设定不加载到 context，直接用 Grep 定位行号再 Read 片段
- 不带入上下文窗口，仅输出结果

---

## 参考

数据流优先序来自本项目的 `references/artifact-protocols.md` 与状态追踪约定。
伏笔、标签和多线分析按需读取相应参考，不声称存在未安装的外部查询命令。
以上参考按查询类型按需加载，不预读。
参考路径规则：`references/` 指 skill 私有；当前仓库没有 `shared/` 查询服务目录。新增参考放在 `skills/fiction-query/references/` 下。

```
fiction-query/            # 本技能目录
├─ SKILL.md
├─ references/          # 按需加载的参考文件
│   ├─ foreshadowing.md # 伏笔分析（可选）
│   └─ tag-specification.md # 标签规范
└─ (共享参考从共用位置读取)
```

查询时的参考加载遵循"识别类型后才加载"原则，不预读全部。
综合/复杂查询才会同时加载多于一个 reference。
静态设定查询不加载 reference，直接用 Grep 定位。

---

## 使用示例

```
> /fiction-query 沈夜在第 10 章时的境界

查询结果：沈夜

概要
- 匹配类型：角色历史状态
- 数据源：追踪/角色状态.md、相关章节正文和 commit（按存在情况列明）
- 匹配数量：1 条

详细信息
- 第 10 章时：筑基期三层
- 第 8 章时：筑基期二层（提升）
- 驱动事件：吸收灵脉（第 9 章）
```

```
> /fiction-query 未回收的伏笔

查询结果：未回收伏笔

概要
- 匹配类型：伏笔 / open loop
- 数据源：追踪/伏笔.md
- 匹配数量：3 条

详细信息
1. 李四的会计是谁 → 已回收（第 7 章）
2. 主角父亲的死因 → 未回收（埋设于第 5 章）
3. 神秘的匿名信 → 未回收（埋设于第 10 章）
```

```
> /fiction-query 世界观/力量体系

查询结果：力量体系

详细信息（从设定集/力量体系.md 读取）
- 境界划分：练气 → 筑基 → 金丹 → 元婴
- 当前主角境界：筑基期三层（从追踪/角色状态.md 读取）
```
---

## 致谢

本 skill 的开发参考了以下开源项目的思路与实现：

- [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer)
- [worldwonderer/oh-story-claudecode](https://github.com/worldwonderer/oh-story-claudecode)

感谢原作者的开源贡献。
