---
name: verification-before-completion
description: 标记工作完成前的最终验证清单。确认：测试全绿、规范合规、代码质量、文件整洁、文档同步。触发词：验证、检查、确认完成、verify、checklist。
agent_created: true
---

# 完成前验证

## 概述

在声明"完成"之前，必须逐项过这个验证清单。任何一项不通过 = 未完成。

**开始时声明：** "我将用 verification-before-completion 技能做最终验证。"

## 验证清单

### 1. 测试验证
- [ ] 所有测试通过（全量套件，非仅新增）
- [ ] 新增测试覆盖所有新功能
- [ ] 边界情况和错误路径有测试
- [ ] 测试用真实代码（mock 只在不可避时）

```bash
# Python
pytest -q --cov

# Node/TS
pnpm test -- --coverage
```

### 2. 规范合规
- [ ] 所有规格要求已实现
- [ ] 没有规格外的功能（YAGNI）
- [ ] 行为和设计文档描述一致

### 3. 代码质量
- [ ] 无死代码
- [ ] 无重复代码（DRY）
- [ ] 命名清晰
- [ ] 错误处理完整
- [ ] Lint 干净

```bash
# Python
ruff check .

# Node/TS
npx eslint .
```

### 4. 文件整洁
- [ ] 无临时文件、调试日志
- [ ] 无注释掉的代码
- [ ] 无 `console.log` / `print` 遗留

### 5. 文档同步
- [ ] 相关文档已更新
- [ ] 如有 README，已反映变更
- [ ] 如有 API 变更，已记录

### 6. Git 状态
- [ ] 所有变更已提交
- [ ] 提交信息清晰
- [ ] 无遗漏的未跟踪文件

```bash
git status
git log --oneline -5
```

## 不通过的处理

任何一项不通过：
1. 列出问题清单
2. 逐项修复
3. 重新运行完整验证
4. 全部通过后才说"完成"

## 通过后

- 移交 `finishing-a-development-branch` 做分支收尾
