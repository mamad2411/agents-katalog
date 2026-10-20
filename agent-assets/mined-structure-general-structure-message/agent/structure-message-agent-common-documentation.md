---
name: common-documentation
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 documentation Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/documentation.md`（完整规范）。以下为操作要点：


# 文档管理规范

> 完整规范详见 `wiki/_common/documentation.md`

## 文档目录结构（MUST）

```
docs/
├── overview.md                 # 概要设计（项目定位+架构+技术栈+能力边界）
├── features/                   # 详细设计（每个功能一个 md，含接口/流程/模型设计）
├── {version}/                  # 版本快照（overview + features + changelog）
│   └── changelog/
│       ├── 001.md              # 第 1 次变更记录
│       └── ...
├── README.md                   # 文档索引
```

## AI 开发前置验证（编码前 MUST 执行）

在编写任何代码前，**必须**按以下顺序完成验证：

1. **确认目标版本号**：X/Y/Z 哪段自增？
2. **验证设计文档存在**：`docs/features/` 下是否有对应的详细设计文档？
3. **确认预期交付**：从设计文档提取交付物清单并确认。
4. **MUST NOT**在设计文档不存在或版本号不明确的情况下开始编码。

## Changelog 格式（每次变更 MUST 写入）

`docs/{version}/changelog/{序号}.md`：

```markdown
# 变更 #{序号}
- **类型**: feat / fix
- **日期**: YYYY-MM-DD
- **涉及文件**: xxx.java, xxx.sql, ...
- **原始设计**: [引用详细设计文档]
- **变更内容**: 本次修改的具体内容
- **测试结果**: 通过 / 失败 + 影响范围
- **修改人**: xxx
```

## 交付前终验（MUST）

- 代码变更与设计文档一致
- `docs/{version}/changelog/` 记录完整
- `README.md` 与当前版本代码一致
- 测试结果已填入 changelog

## 红线

- **设计文档缺失** → 禁止编码
- **版本号不明** → 禁止编码
- **changelog 未更新** → 禁止提交

完整规则以 `wiki/_common/documentation.md` 为准。
