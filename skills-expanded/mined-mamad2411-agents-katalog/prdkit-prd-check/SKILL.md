---
name: prdkit-prd-check
description: 当用户要求审查、review、检查、挑问题、补漏洞、给改进建议，且对象是 PRD、需求文档、产品方案、系统设计文档时使用。该 skill 先通过 prdkit CLI 定位目标 PRD，再完成产品定型与适用性判断，随后按 14 个维度逐项输出 findings，最后汇总重大风险、优先级问题清单和 Top 改进建议。
allowed-tools:
  - Read
  - Grep
  - Glob
  - LS
  - Bash(command -v prdkit)
  - Bash(prdkit info*)
  - Bash(prdkit prd list*)
  - Bash(prdkit prd check*)
---

# 审查 PRD

## 目标

为 `prdkit` 项目中的 PRD 提供结构化评审闭环：

1. 先用 CLI 定位目标 PRD
2. 再做产品定型与适用性判断
3. 按 14 个维度逐项输出发现
4. 最后汇总重大风险、问题优先级和改进建议

## 渐进加载原则

不要一次性读取所有参考资料。按阶段加载：

1. 阶段 0：
   - [references/framework/review-path.md](references/framework/review-path.md)
2. 阶段 1：
   - 仅加载当前正在评审的维度文件
3. 阶段 2：
   - [references/appendices/veto-checklist.md](references/appendices/veto-checklist.md)
   - [references/appendices/report-template.md](references/appendices/report-template.md)

## 工作流程

### 阶段 0：定位 PRD 与产品定型

1. 从项目根目录开始，先检查 `prdkit` 和项目状态：
   - `command -v prdkit`
   - `prdkit info`
2. 定位要审查的 PRD：
   - 如果用户给了标题、文件名或路径，优先执行：

```bash
prdkit prd check "<target>"
```

   - 如果用户没给明确目标，执行：

```bash
prdkit prd list
prdkit prd check
```

3. 读取目标 PRD 全文，再结合 [references/framework/review-path.md](references/framework/review-path.md) 完成产品定型：
   - 商业属性：商业化产品 / 企业自研系统
   - 功能类型：业务型管理软件 / 工具型软件 / 交易型平台 / 基础服务型
   - 文档范围：0-1 系统级规划 / 迭代需求 / 模块级需求
   - 是否涉及 AI 功能
4. 标记不适用维度，不要硬套统一标准。

### 阶段 1：逐维度审查

5. 严格按以下顺序逐维度检查，每完成一个维度就立即输出，不要攒到最后：
   - 01 业务分析质量
   - 02 产品类型适配性
   - 03 产品定位合理性
   - 04 场景分析与用户旅程
   - 05 文档结构完整性
   - 06 架构设计质量
   - 07 数据建模质量
   - 08 流程与角色设计
   - 09 交互设计质量
   - 10 商业分析深度
   - 11 MVP 策略与演进蓝图
   - 14 运营方案与效果跟踪
   - 12 异常处理与健壮性设计
   - 13 AI 功能设计质量
6. 每个维度只加载对应的参考文件。
7. 每个维度至少输出：
   - 评级：优秀 / 合格 / 待改进 / 严重缺失
   - 3 条具体发现，或 3 条明确说明为何没有问题
   - 隐性问题推断
8. 发现必须锚定到 PRD 的真实章节、流程、页面、字段，或明确说明“文档缺少该证据”。

### 阶段 2：重大风险与汇总报告

9. 所有维度检查完成后，加载 [references/appendices/veto-checklist.md](references/appendices/veto-checklist.md)，检查 R1-R8 重大风险项。
10. 再按 [references/appendices/report-template.md](references/appendices/report-template.md) 输出汇总报告：
   - 产品定型说明
   - 各维度发现摘要
   - 重大风险项
   - P0-P3 问题清单
   - 亮点记录
   - Top 10 改进建议

## 单维度输出格式

```md
## 维度[编号] - [名称] ｜ 评级：[优秀 / 合格 / 待改进 / 严重缺失]

### 具体发现

**发现 1：[问题标题]** [P0/P1/P2/P3]
- PRD定位：第X节 / [功能名]
- 问题描述：...
- 改进示例：...

### 隐性问题推断
- ...
```

## 约束规则

- 必须先完整阅读 PRD，再开始逐维度评审
- 必须先做产品定型，再判断维度适用性
- 每个维度都要即时输出，不能只给最终总结
- 不要把“证据不足”伪装成“文档没问题”
- 对 `09 交互设计质量`，需要逐个核对 PRD 中出现的关键页面、弹窗、表单和关键操作
