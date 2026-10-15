---
name: fde-mock-meeting-transcripts
description: 创建 FDE 共学营会议决策与任务跟踪场景的 Mock 会议字幕，并通过飞书 CLI 创建五篇飞书文档。用户要求生成企业会议字幕、会议决策提取素材、行动项跟踪大作业数据时使用。
---

# FDE 会议字幕 Mock

创建 5 份带时间戳的脱敏仿真企业会议字幕和 1 篇目录索引。只提供字幕材料，不提前提取决策、事项、责任人或日期。

## 工作流

1. 将包含本文件的目录记为 `SKILL_DIR`。
2. 运行 `python3 "$SKILL_DIR/scripts/preflight.py"`。
3. 按 [飞书环境处理](references/lark-setup.md) 处理预检结果；环境未就绪时不要继续。
4. 不询问会议类型、参会角色、日期或目标目录，直接运行预览：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_docs.py" --dry-run
```

5. 告诉用户将直接在“我的文档库”创建 6 篇新文档，不修改或删除现有数据，并请求一次写入确认。
6. 用户确认后运行：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_docs.py" --yes
```

7. 返回目录和 5 篇字幕链接，并说明材料为脱敏仿真内容，不对应真实企业、人员或客户。

## 约束

- 不要提取或补充事项、跟进人、开始日期、预计结束日期和验收答案。
- 不要创建飞书任务或多维表格。
- 不要要求用户提供目标文件夹或日期参数。
- 写入部分失败时，报告已创建链接和错误；不要自动删除任何飞书资源。
- 不要把讨论意见当作正式决策，也不要向字幕中补写缺失责任人和日期。

## 资源

- [飞书 CLI 安装与授权](references/lark-setup.md)
- [会议材料结构](references/data-schema.md)
