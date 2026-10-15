---
name: fde-mock-expense-tickets
description: 创建 FDE 共学营企业报销预审场景的模拟报销制度和 200 条 Mock Ticket，并通过飞书 CLI 写入飞书文档和多维表格。用户要求生成报销审核、财务预审或异常 Ticket 大作业素材时使用。
---

# FDE 报销预审 Mock

创建 1 篇脱敏模拟报销制度和 1 个包含 200 条 Ticket 的飞书多维表格。只提供原始材料，不提供问题标签、标准审核结果或测试集。

## 工作流

1. 将包含本文件的目录记为 `SKILL_DIR`。
2. 运行 `python3 "$SKILL_DIR/scripts/preflight.py"`。
3. 按 [飞书环境处理](references/lark-setup.md) 处理预检结果；环境未就绪时不要继续。
4. 不询问公司规模、月份、Ticket 数量或目标目录，直接运行预览：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_resources.py" --dry-run
```

5. 告诉用户将创建 1 篇新文档、1 个新 Base 和 200 条记录，不修改或删除现有数据，并请求一次写入确认。
6. 用户确认后运行：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_resources.py" --yes
```

7. 返回报销制度和 Base 链接，报告回读验证到的记录数。

## 约束

- 不要输出每条 Ticket 的问题标签、预期结论、是否通过或测试答案。
- 不要替学员选择验收样本或计算项目准确率。
- 不要要求用户提供目标文件夹、Base Token 或数量参数。
- 写入部分失败时，报告已创建资源和错误；不要自动删除任何飞书资源。
- 明确所有员工、商户、票据和金额均为模拟数据，不代表真实财务或税务意见。

## 资源

- [飞书 CLI 安装与授权](references/lark-setup.md)
- [报销制度与 Ticket 数据结构](references/data-schema.md)
