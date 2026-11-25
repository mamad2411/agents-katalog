---
name: fde-mock-knowledge-base
description: 创建 FDE 共学营美妆零售知识库 Mock 材料并通过飞书 CLI 导入用户的飞书文档库。用户要求生成美妆零售知识文档、知识检索与客服问答大作业素材时使用。
---

# FDE 美妆零售知识库 Mock

创建 5 篇脱敏模拟美妆零售知识文档和 1 篇目录索引。只提供原始业务材料，不生成测试问题、预期答案或验收结果。

## 工作流

1. 将包含本文件的目录记为 `SKILL_DIR`。
2. 运行 `python3 "$SKILL_DIR/scripts/preflight.py"`。
3. 按 [飞书环境处理](references/lark-setup.md) 处理预检结果；环境未就绪时不要继续。
4. 不询问行业、角色、文档目录、规模或测试集，直接运行预览：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_docs.py" --dry-run
```

5. 告诉用户将直接在“我的文档库”创建 6 篇美妆零售新文档，不修改或删除现有数据，并请求一次写入确认。
6. 用户确认后运行：

```bash
python3 "$SKILL_DIR/scripts/create_feishu_docs.py" --yes
```

7. 返回脚本输出中的目录和文档链接；明确材料是脱敏模拟内容，不代表真实企业制度或专业意见。

## 约束

- 不要替学员生成知识库测试问题、预期答案、是否通过或准确率。
- 不要要求用户提供目标文件夹、Wiki Token 或文档目录。
- 不要提供制造业或医药材料，也不要根据用户身份改写预置材料；目标角色由学员在 Day 1 自行定义。
- 写入部分失败时，报告已创建链接和错误；不要自动删除任何飞书资源。
- 只使用脚本提供的公开来源整理材料，不抓取或复制报告全文。

## 资源

- [飞书 CLI 安装与授权](references/lark-setup.md)
- [知识文档结构与资产范围](references/data-schema.md)
