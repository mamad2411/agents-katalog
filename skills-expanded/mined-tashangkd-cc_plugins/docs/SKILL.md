---
name: docs
description: 活文档维护。智能分析项目代码，维护 docs/ 核心文档和 README.md，包含健康检查、自动更新、质量评分功能。用户提到更新文档、同步文档时使用。
user-invocable: true
---

# /docs - 活文档维护

> **代码即真相，文档跟随代码**

智能分析项目代码，维护 `docs/` 核心文档和 `README.md`

---

## 用法

```bash
/docs                 # 健康检查（默认）
/docs file            # 更新指定文件
/docs init            # 初始化文档骨架
/docs score           # 质量评分
```

---

## 1. 健康检查

执行 `/docs` 显示文档健康状态：

```
📊 文档健康状态

| 文档 | 状态 | 最后更新 | 相关代码变更 |
|------|------|----------|-------------|
| CLAUDE.md | ✅ 新鲜 | 今天 09:30 | 无 |
| README.md | ✅ 新鲜 | 2天前 | 无 |
| docs/architecture.md | ⚠️ 过时 | 今天 14:30 | src/auth.py 新增 OAuth |
```

---

## 2. 初始化文档骨架

```bash
/docs init
```

自动创建：

```
docs/
├── architecture.md     # 架构设计
├── components.md       # 组件清单
├── development.md      # 开发指南
├── testing.md          # 测试策略
└── contributing.md     # 贡献指南
```

---

## 3. 智能更新

| 代码变更 | 自动更新 |
|----------|----------|
| 新增模块 | components.md |
| 修改导入关系 | architecture.md |
| 修改配置文件 | development.md |
| 新增测试 | testing.md |

```bash
/docs                        # 更新所有过时文档
/docs docs/architecture.md   # 更新指定文档
/docs --preview              # 预览变更
```

---

## 4. 质量评分

```bash
/docs score
```

输出：

```
📊 文档质量评分

| 维度 | 得分 | 目标 | 状态 |
|------|------|------|------|
| 覆盖度 | 75% | ≥80% | ⚠️ |
| 新鲜度 | 60% | ≥70% | ❌ |
| 完整性 | 85% | ≥80% | ✅ |

总体评分: C+ (79.5/100)
```

---

## 5. 核心文档清单

| 文件 | 维护方式 | 内容 |
|------|----------|------|
| `CLAUDE.md` | `/init` | 项目指令、工作流 |
| `README.md` | `/docs` | 项目概述、安装 |
| `docs/architecture.md` | `/docs` | 系统架构、模块关系 |
| `docs/components.md` | `/docs` | 组件清单、职责边界 |

---

## 6. Git 提交规范

| 场景 | 前缀 | 示例 |
|------|------|------|
| 更新核心文档 | `docs:` | `docs: 更新架构文档` |
| 更新项目指令 | `chore:` | `chore: 更新 CLAUDE.md` |

---

**文档过时 = 项目失活**
