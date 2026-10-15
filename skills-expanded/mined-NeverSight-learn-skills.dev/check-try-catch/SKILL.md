---
name: check-try-catch
description: 提供代码审查指南，识别并修复空catch块和纯console日志catch块问题
dependency:
  python: []
  system: []
---

# Check Try-Catch 代码审查指南

## 任务目标
- 识别代码中的空 catch 块（没有实际处理逻辑）
- 识别 catch 块中只有 console.log/print 等日志语句
- 提供修复建议和最佳实践
- 支持多语言代码审查

## 前置准备
无特殊依赖，本指南适用于人工代码审查或智能体辅助审查。

## 操作步骤

### 标准流程

1. **识别问题代码模式**
   - 搜索代码中的 try-catch 或 try-except 结构
   - 检查 catch/except 块的内容

2. **评估问题严重性**
   - 空 catch：高严重性，错误被完全忽略
   - 纯 console 日志：中严重性，错误被记录但未处理

3. **应用修复策略**
   - 参考 [references/patterns.md](references/patterns.md) 中的修复模式
   - 根据具体场景选择合适的处理方式

4. **验证修复结果**
   - 确保每个 catch/except 块都有明确的错误处理意图

## 资源索引
- 模式参考: [references/patterns.md](references/patterns.md) (何时读取:需要具体的错误示例、修复策略和检查清单时)

## 注意事项
- 本指南适用于 JavaScript/TypeScript 和 Python 代码
- 代码审查应结合业务上下文判断错误的处理策略
- 建议在代码评审阶段执行此检查
- 可以配合静态分析工具自动化检测

## 使用示例

**场景 1：人工代码审查**
```bash
# 在代码评审时，按照本指南检查提交的代码
# 重点关注新增或修改的 try-catch 块
```

**场景 2：智能体辅助审查**
```
请按照 check-try-catch 指南审查以下代码：
[粘贴代码]

智能体将：
1. 识别所有 try-catch 结构
2. 检测空 catch 和纯 console 日志 catch
3. 提供具体的修复建议
```
