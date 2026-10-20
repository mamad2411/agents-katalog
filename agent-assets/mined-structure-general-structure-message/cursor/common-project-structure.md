---
description: |
  当用户要求"新建项目/新建模块/调整目录结构/调整分层"时触发。
  覆盖项目结构约定、多模块项目规范、父子嵌套项目职责分离。

triggers:
  - 项目结构
  - 目录结构
  - 新建项目
  - 新建模块
  - 模块划分
  - 分层
  - structure
  - scaffolding
  - 子目录
  - 目录
  - 新建目录
  - 创建目录

priority: medium
alwaysApply: false

category: project-structure
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/project-structure.md

related-skills:
  - requirement-analysis
  - coding

when-to-use: |
  新建项目、调整目录结构、新增模块、讨论分层目录时
when-not-to-use: |
  仅在现有模块内编码
version: "0.3.0"
since: "2026-08-13"
---

# 项目结构约定

> 完整规范详见 `wiki/project-structure.md`

## 目录类型识别（MUST）⭐

用户说"新建目录/子目录"时 MUST 先判断类型，**禁止默认按"子包"处理**：

| 用户表达 | 目录类型 | 创建位置 | 影响包名 |
|---|---|---|---|
| "新建包 / 子包 / package" | **包目录** | 现有 package 下 | ✅ 影响（package 语句变化） |
| "新建特性 / feature / 业务模块" | **特性目录** | `features/<name>/` 或 `modules/<name>/` | ❌ 不影响（独立目录，跨层组织） |
| "新建文档 / 脚本 / 示例目录" | **非代码目录** | `docs/` `scripts/` `examples/` `assets/` | ❌ 不影响 |
| "新建子目录"（未明确） | **MUST 询问用户** | — | — |

**三种目录的本质区别**：
- **包目录**：Java package 的物理映射，影响 `package` 语句和 `import`
- **特性目录**：按业务特性跨层组织代码（如 `features/user-management/{controller,service,repository}/`），独立目录不影响主包结构
- **非代码目录**：不放 Java 源代码（如 `docs/design/`、`scripts/deploy/`）

**MUST NOT**：
- ❌ 把"子目录"默认理解为"子包"
- ❌ 把"特性目录"创建为 Java 子包
- ❌ 在 `src/main/java/` 下创建非代码目录（如 `src/main/java/docs/`）

**识别困难时 MUST 询问用户**：
> "您说的'子目录'是指：
> a) Java 子包（影响 package 语句）
> b) 特性目录（独立功能，跨层组织）
> c) 非代码目录（文档/脚本/资源）
> 请确认。"

## 核心约束

### 多模块项目（MUST）

- **MUST** 按职责划分模块，避免循环依赖。
- **MUST** 模块命名遵循技术栈约定的命名规范。

### 父子嵌套项目职责分离（MUST）

> 详规见 `wiki/project-structure.md#父子项目约定`
> 核心原则：**有子项目的层负责概括，无子模块的叶子层负责完整细节**。规则递归适用，实际 ≤3 层。

| 层级 | 职责 | 红线 |
|------|------|------|
| **根父项目** | 全局集成关系、架构图、模块清单、全局规范 | **MUST NOT**含详细设计/changelog/代码 |
| **中间层**（N 层，有子模块） | 本级概要设计、本级内模块关系 | **MUST NOT**含详细设计/changelog/代码 |
| **叶子模块**（无子模块） | 概要设计+详细设计+changelog+版本快照+代码+CI/CD | — |

- CI/CD 流水线、Dockerfile 等发布文件 **只在叶子模块**中维护。

### 文档目录（MUST）

```
docs/
├── overview.md                 # 概要设计
├── features/                   # 详细设计
├── {version}/                  # 版本快照
└── README.md                   # 文档索引
```

### 禁止事项

- **MUST NOT** 将生成代码与手写代码混放在同一目录。
- **MUST NOT** 在 commit 中包含临时文件、IDE 配置、构建产物。
- **MUST NOT** 在 `README.md` 中写入超前于代码的内容。
