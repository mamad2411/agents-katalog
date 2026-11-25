---
name: refactor-check
description: 重构后业务逻辑校验。确保代码重构不改变外部行为，用于金融项目的严格验证。在 /refactor 完成后、修改交易/风控/资金代码后、上线前使用。核心目标：业务逻辑零变更。
---

# 重构校验

## 核心原则

**重构后业务逻辑必须零变更**：

- 相同输入 → 相同输出
- 对外接口保持兼容
- 异常处理行为一致
- 副作用行为一致

## 校验流程

```
DETECT → SNAPSHOT → COMPARE → VERIFY → REPORT
   │         │          │        │        │
   ▼         ▼          ▼        ▼        ▼
 检测变更  获取原版   对比差异  逐项验证  输出报告
```

### DETECT（检测变更）

无参数时，自动检测未提交的变更：

```bash
git status --porcelain | grep -E "^[AM ]?[AM]" | cut -c4-
```

### SNAPSHOT（获取原版）

```bash
git show HEAD:文件路径
```

## 详细参考

- **校验方法**: [references/methods.md](references/methods.md)
- **检查清单**: [references/checklist.md](references/checklist.md)

## 快速参考

### 必须检查的项目

| 检查项   | 方法               | 不通过则 |
| -------- | ------------------ | -------- |
| 函数签名 | 对比参数和返回类型 | 阻止     |
| 导出接口 | 对比 export 列表   | 阻止     |
| 输入输出 | 相同输入验证输出   | 阻止     |
| 异常处理 | 验证错误抛出行为   | 阻止     |

### 关键代码识别

以下代码需要**严格校验**：

- 路径含 `trade`、`order`、`position`、`risk`、`balance`
- 涉及资金计算、下单、风控的逻辑
- 对外暴露的 API 接口

### 校验报告模板

```markdown
## 重构校验报告

**检测到 X 个变更文件**：

1. [文件路径] (M/A)

### 校验结果

| 文件     | 签名 | 接口 | 输入输出 | 异常 | 结果   |
| -------- | ---- | ---- | -------- | ---- | ------ |
| file1.ts | pass | pass | pass     | pass | pass   |
| file2.ts | pass | warn | pass     | pass | 需确认 |

### 总结

- X 个文件通过
- Y 个文件需人工确认
- Z 个文件不通过

### 结论

[可以上线 / 需要修复 / 需要人工复核]
```
