---
name: sharecrm
description: Use when the user needs to query, create, or manage ShareCRM data, knowledge, solutions, approvals, files, schedules, or other ShareCRM product capabilities through the `sharecrm` CLI.
license: MIT
metadata:
  agentSupport: true
  author: "zengww9500@fxiaoke.com"
  version: "1.1.0"
  requires:
    bins: ["sharecrm"]
  cliHelp: "sharecrm data -h"
---

# 纷享销客全产品 Skill

通过 `sharecrm` 命令管理纷享产品能力。

## 严格禁止 (NEVER DO)
- 不要使用 sharecrm 命令以外的方式操作（禁止 curl、HTTP API、浏览器）
- 不要编造 UUID、ID 等标识符，必须从命令返回中提取
- 不要猜测字段名/参数值，操作前必须先查询确认

## 严格要求 (MUST DO)
- 危险操作必须先向用户确认，用户同意后才加 `--yes` 执行
- 单次批量操作不超过 30 条记录
- 所有命令必须**严格遵循**对应产品参考文档里面规定的参数格式（如：如果有参数值，则参数和参数值之间至少用一个空格隔开）

## 前置条件
- 已安装 `sharecrm`，可通过 `sharecrm -V` 确认是否安装，如果未安装 MUST 请先用 Read 工具读取 [`references/shareCrmInstall.md`](references/shareCrmInstall.md)内容，并完成sharecrm安装
- 已通过 `sharecrm auth login` 完成登录授权
- **CRITICAL — 开始前 MUST 先用 Read 工具读取 [`references/userAuth.md`](references/userAuth.md)，其中包含登录授权、身份认证**
- 登录用户具有对应数据操作的权限 scope

> **注意：** 产品命令的使用方法可以通过 `sharecrm <product> -h` 查看，命令帮助信息可以通过 `sharecrm <product> <command> -h` 查看,命令帮助信息中会列出所有参数。

## 产品总览

| 产品             | 用途                                      | 命令帮助信息查                     | 参考文档                                     |
|----------------|-----------------------------------------|-----------------------------|------------------------------------------|
| `knowledge`    | 知识与检索：                                  | `sharecrm  knowledge -h`    |                                          |
| `solution`     | 内容与方案：                                  | `sharecrm  solution -h`     |                                          |
| `enterprise`   | 企业与行业：                                  | `sharecrm  enterprise -h`   |                                          |
| `sales`        | CRM与销售：                                 | `sharecrm  sales -h`        |                                          |
| `marketing`    | 营销与增长：                                  | `sharecrm  marketing -h`    |                                          |
| `service`      | 服务与工单：                                  | `sharecrm  service -h`      |                                          |
| `visit`        | 外勤与拜访：外勤/外勤记录/外勤审批/外勤审批表单               | `sharecrm  visit -h`        |                                          |
| `bi`           | BI分析：                                   | `sharecrm  bi -h`           |
| `approval`     | 审批：审批工单，审批工单查询，审批工单创建，审批工单修改，审批工单删除     | `sharecrm  approval -h`     |                                          |
| `bpm`          | BPM：                                    | `sharecrm  bpm -h`          |                                          |
| `flow`         | 流程：流程创建，流程查询，流程修改，流程删除                  | `sharecrm  flow -h`         |                                          |
| `data`         | 对象与数据：CRM通用对象数据操作，包括查询，新建，编辑，根据SQL查询等   | `sharecrm  data -h`         | [data.md](./references/products/data.md) |
| `describe`     | 对象描述：CRM对象描述的基本操作，包括查询对象ApiName，查询对象描述等 | `sharecrm  contact -h`      |                                          |
| `file`         | 文件与网盘：                                  | `sharecrm  file -h`         |                                          |
| `utility`      | 通用函数：                                   | `sharecrm  utility -h`      |                                          |
| `work`         | 日程任务：                                   | `sharecrm  work -h`         |                                          |
| `tag`          | 标签：                                     | `sharecrm  tag -h`          |                                          |
| `usergroup`    | 用户组：                                    | `sharecrm  usergroup -h`    |                                          |
| `stage`        | 阶段：                                     | `sharecrm  stage -h`        |                                          |
| `notice`       | 通知：                                     | `sharecrm  notice -h`       |                                          |
| `mail`         | 邮件：                                     | `sharecrm  mail -h`         |                                          |
| `channel`      | 渠道协同：                                   | `sharecrm  channel -h`      |                                          |
| `conversation` | 群组与会话：                                  | `sharecrm  conversation -h` |                                          |

## 意图判断决策树

- 用户提到"知识/知识库/知识检索/知识库检索/知识查询/知识搜索" → `knowledge`
- 用户提到"解决方案/方案/内容/内容方案/方案检索/方案搜索" → `solution`
- 用户提到"企业信息/行业信息/行业检索/行业查询/行业搜索" → `enterprise`
- 用户提到"销售/CRM" → `sales`
- 用户提到"营销/增长/推广/推广渠道/推广渠道管理/推广渠道分析/推广渠道效果/推广渠道效果分析" → `marketing`
- 用户提到"售后/售后服务/售后支持/售后处理/服务工单/售后工单" → `service`
- 用户提到"外勤/外勤记录/外勤审批/外勤审批表单/拜访/拜访记录/拜访审批/拜访审批表单" → `visit`
- 用户提到"BI/BI报表/数据分析/数据可视化/数据统计/数据统计分析/数据统计效果/数据统计效果分析/数据可视化/数据可视化分析" → `bi`
- 用户提到"审批/审批表单/审批流程/审批工单" → `approval`
- 用户提到"BPM/业务流程/BPM流程/BPM流程定义/BPM流程实例/BPM流程任务/BPM流程任务节点" → `bpm`
- 用户提到"对象/对象数据/对象数据查询/对象数据检索/对象数据创建/对象数据修改/对象数据删除" → `data`
- 用户提到"文件/网盘/文件管理/文件检索/文件查询/文件上传/文件下载/文件分享/文件收藏/文件收藏夹/文件收藏夹创建/文件收藏夹删除" → `file`
- 用户提到"函数/APL函数/通用函数/通用函数定义/通用函数实例/通用函数任务/通用函数任务节点" → `utility`
- 用户提到"日程/日程任务/日程任务节点/日程任务实例/日程任务定义" → `work`
- 用户提到"标签/标签管理/标签创建/标签删除" → `tag`
- 用户提到"用户组/用户组管理/用户组创建/用户组删除" → `usergroup`
- 用户提到"阶段/阶段管理/阶段创建/阶段删除" → `stage`
- 用户提到"通知/通知查看/通知检索/通知管理/通知创建/通知删除" → `notice`
- 用户提到"邮件/邮件管理/邮件创建/邮件删除" → `mail`
- 用户提到"渠道/渠道协同/渠道管理/渠道创建/渠道删除" → `channel`
- 用户提到"群组/群组管理/群组创建/群组删除" → `conversation`

> 

## 危险操作确认

以下操作为不可逆或高影响操作，执行前**必须先向用户展示操作摘要并获得明确同意**，同意后才加 `--yes` 执行。

| 产品 | 命令                     | 说明             |
|------|------------------------|----------------|
| `data` | `data CreateRecords`   | 创建对象数据         |

### 确认流程
```
Step 1 → 展示操作摘要（操作类型 + 目标对象 + 影响范围）
Step 2 → 用户明确回复确认（如 "确认" / "好的"）
Step 3 → 加 --yes 执行命令
```

## 核心流程
作为一个智能助手，你的首要任务是**理解用户的真实、完整的意图**，而不是简单地执行命令。在选择 `sharecrm` 的产品命令前，必须严格遵循以下四步流程：

1. 意图分类：首先，判断用户指令的核心 动词/动作 属于哪一类。这比关注名词更重要。
2. 歧义处理与信息追问：如果用户指令模糊或包含多个产品的关键字，严禁猜测。必须主动向用户追问以澄清意图。这是你作为智能助手而非命令执行器的核心价值。
3. 精准产品映射：在完成前两步，意图已经清晰后，参考产品总览和意图判断决策树 来选择产品。
4. 充分阅读产品参考文件，通过编写代码或直接调用指令实现用户意图。

## 错误处理
1. 遇到错误，加 `--debug` 重试一次
2. 仍然失败，报告完整错误信息给用户，禁止自行尝试替代方案
3. 认证失败时，参考 [userAuth](references/userAuth.md) 中的认证章节处理


## 详细参考 (按需读取)
- [sharecrm程序安装](references/shareCrmInstall.md) — sharecrm程序安装
- [sharecrm授权登录](references/userAuth.md) — 全局标志、认证、输出格式
- [纷享CRM对象清单](references/objectApiNames.md) — 各数据对象 API 名称
