---
name: Sequential Thinking
description: 深度思考引擎模块，实现动态渐进式问题解决。支持线性推进、分支探索与自我修正。
version: 0.9.0
---

# Sequential Thinking 操作手册

## 功能概览
深度思考引擎（Sequential Thinking）是一个动态渐进式问题解决工具，支持：
- **线性推进**：按步骤分析问题，逐步深入
- **分支探索**：从某一步骤分叉探索不同路径
- **自我修正**：回顾并修正之前的思考步骤
- **假设验证**：生成假设并基于思考链验证
- **线程隔离**：多客户端并发隔离（线程局部存储）

## 注册工具
- **sequentialthinking** : 动态渐进式问题解决引擎

## 参数详解

### 必填参数
| 参数 | 类型 | 说明 |
|------|------|------|
| `thought` | string | 当前思考步骤内容 |
| `nextThoughtNeeded` | boolean | 是否需要更多思考步骤 |
| `thoughtNumber` | integer | 当前步骤编号（从 1 开始） |
| `totalThoughts` | integer | 预估总步骤数（可动态调整） |

### 可选参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `isRevision` | boolean | false | 是否为修正步骤 |
| `revisesThought` | integer | null | 被修正的步骤编号 |
| `branchFromThought` | integer | null | 分支起点步骤编号 |
| `branchId` | string | null | 分支标识符 |
| `needsMoreThoughts` | boolean | false | 是否需要更多思考（即使已达预估总数） |

## 使用场景
- **复杂问题分解**：将大问题拆分为多个小步骤
- **规划与设计**：需要灵活调整的架构设计
- **分析推理**：需要多轮验证的复杂分析
- **调试定位**：逐步排查问题的根因分析
- **假设验证**：生成假设并基于证据链验证

## 响应结构
```json
{
  "thoughtNumber": 3,
  "totalThoughts": 8,
  "nextThoughtNeeded": true,
  "branches": ["branch_1", "branch_2"],
  "thoughtHistoryLength": 3
}
```

## 注意事项
1. `totalThoughts` 可根据实际需要动态调整（增加或减少）
2. `thoughtNumber` 超过 `totalThoughts` 时，系统自动更新总数
3. 分支探索通过 `branchFromThought` 和 `branchId` 标识
4. 修正步骤需指定 `isRevision=true` 和 `revisesThought`
5. 每个线程/会话独立维护状态（线程局部存储）

## 配置常量
- `DEFAULT_TOTAL_THOUGHTS`: 5（默认预估步骤数）
- `MAX_HISTORY_LENGTH`: 1000（防止内存溢出）
- `DISABLE_THOUGHT_LOGGING`: false（是否禁用终端日志）
