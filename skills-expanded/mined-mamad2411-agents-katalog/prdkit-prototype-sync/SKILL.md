---
name: prdkit-prototype-sync
description: 当用户要求把 prototype 反哺到 PRD、把原型更新同步回需求文档、把 mark 内容沉淀到指定 PRD、根据原型修订具体需求描述、补原型链接、生成 PRD 修订记录时使用。该 skill 通过 prdkit CLI 定位目标 PRD 和 prototype，读取 marks，识别 PRD 中实际对应的需求章节，对比现有内容差异，并把修订结果直接写回 PRD。
allowed-tools:
  - Read
  - Grep
  - Glob
  - LS
  - Bash(command -v prdkit)
  - Bash(prdkit info*)
  - Bash(prdkit prd list*)
  - Bash(prdkit prd check*)
  - Bash(prdkit prototype list*)
  - Bash(prdkit mark list*)
  - Bash(prdkit mark get*)
  - Bash(prdkit serve status*)
  - Edit
  - MultiEdit
  - Write
---

# 将 Prototype 反哺到 PRD

## 目标

把指定 prototype 的最新结构和标记内容沉淀回指定 PRD，并留下明确的修订痕迹：

1. 定位目标 PRD
2. 定位目标 prototype
3. 收集 prototype 链接和所有 mark 内容
4. 更新 PRD 中实际对应的需求描述章节
5. 把 mark 信息沉淀为功能点、交互点、约束点或待确认项
6. 对比本次回写前后的文档差异
7. 在 PRD 中追加修订记录

## 渐进加载原则

不要一次性读取全部参考资料。按阶段加载：

1. 阶段 0：
   - [references/workflow.md](references/workflow.md)
2. 阶段 1：
   - [references/requirement-sync-contract.md](references/requirement-sync-contract.md)
3. 阶段 2：
   - [references/revision-log-template.md](references/revision-log-template.md)

## 工作流程

### 阶段 0：定位 PRD 与 Prototype

1. 从项目根目录开始，先检查 `prdkit` 与项目状态：
   - `command -v prdkit`
   - `prdkit info`
2. 定位目标 PRD：
   - 优先使用用户提供的标题、文件名或路径：

```bash
prdkit prd check "<target-prd>"
```

   - 如果用户没说清楚，先执行：

```bash
prdkit prd list
```

3. 定位目标 prototype：

```bash
prdkit prototype list
```

4. 如果用户给了明确 prototype 路径，直接使用；否则根据 PRD 内容、标题和上下文选择最相关的 prototype，并在输出中说明这个映射是假设还是确认事实。

### 阶段 1：收集原型与标记信息

5. 获取 prototype 下的 marks：

```bash
prdkit mark list --prototype <prototype-path> --json
```

6. 对每个 mark 继续取详情：

```bash
prdkit mark get <mark-id> --prototype <prototype-path> --json
```

7. 生成 prototype 链接：
   - 优先执行 `prdkit serve status`
   - 如果服务运行中，生成本地预览链接：
     - `http://localhost:<port>/prototypes/<prototype-path>/index.html`
   - 如果服务未运行，回退为仓库相对路径：
     - `workspace/prototypes/<prototype-path>/index.html`
8. 读取目标 PRD 全文，特别关注：
   - `## 7. 功能需求`
   - 页面 / 模块 / 功能点对应的小节
   - 现有 prototype / 原型链接
   - 现有修订记录

### 阶段 2：生成回写内容

9. 根据 marks 把 prototype 内容整理成 PRD 可读的结构：
   - 页面 / 模块标题
   - prototype 链接
   - 对应标记摘要
   - 提炼出的需求描述增量
   - 交互要求
   - 业务规则 / 约束
   - 待确认项
10. 不要把 mark 原文整段机械粘贴进 PRD，要做归纳：
   - 直接描述页面目标的 mark -> 归入功能点
   - 描述交互行为的 mark -> 归入交互要求
   - 描述边界、限制或说明的 mark -> 归入规则 / 风险 / 待确认项
11. 不要假设 PRD 里有固定的 `Feature List` 模块。应先按 [references/requirement-sync-contract.md](references/requirement-sync-contract.md) 识别本次 prototype 最应该回填到哪些现有需求章节：
   - 已有模块 / 页面需求小节
   - 已有交互要求小节
   - 已有业务规则 / 流程小节
   - 已有待确认项 / 开放问题小节
12. 如果 PRD 已经有对应页面或模块的小节，不是整段重写，而是先对比：
   - 新增了哪些需求点
   - 更新了哪些需求描述
   - 删除或不再体现哪些内容
13. 把差异整理成“本次修订摘要”，用于修订记录。

### 阶段 3：回写 PRD 与追加修订记录

14. 直接更新目标 PRD：
   - 在最匹配的需求章节中新增或更新该 prototype 对应内容
   - 同步 prototype 链接
   - 将 mark 沉淀为结构化需求描述
15. 如果 PRD 没有“修订记录”区域，则创建：
   - 优先放在标题和正文之间
   - 标题使用 `## 修订记录`
16. 按 [references/revision-log-template.md](references/revision-log-template.md) 追加一条修订记录，至少包含：
   - 修订日期
   - 修订人
   - 修订明细
   - 修订明细中需包含来源 prototype、prototype 链接、mark 数量与本次差异摘要
17. 修改完成后，向用户汇报：
   - 更新了哪个 PRD
   - 使用了哪个 prototype
   - 沉淀了多少个 mark
   - 本次修订的差异摘要

## 约束规则

- 必须先通过 CLI 定位 PRD 和 prototype，再读文件
- 必须使用 `mark list` + `mark get`，不要跳过 mark 明细
- 不要把 mark Markdown 生硬拼接进 PRD，必须先归纳
- 必须生成或更新 prototype 链接
- 必须对比旧内容和新内容，再写修订记录
- 必须把修订记录写进 PRD，而不是只在回复里说明
- 不要预设固定的 `Feature List` 区块，优先复用 PRD 里现有的具体需求描述结构
- 如果同一个 PRD 对应多个 prototype，默认一次只同步一个 prototype，除非用户明确要求批量同步
