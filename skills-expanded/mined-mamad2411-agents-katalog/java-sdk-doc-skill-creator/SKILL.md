---
name: "java-sdk-doc-skill-creator"
description: "Read Java source, convert Javadoc into a coding-agent-friendly SDK skill. Trigger when user mentions Java doc generation, SDK doc creation/update, or javadoc-to-skill conversion."
---

# Java SDK 文档 Skill 生成器

从 Java 源码生成可加载的 SDK 文档 skill。两轮遍历：第一轮构建类型索引，第二轮按代码包结构生成文档文件。适用于生成和增量更新场景。

## 执行步骤

### 步骤 1：确定输入范围

接受单个 `.java` 文件或目录（递归扫描）。忽略 `target/`、`src/test/`、非 `.java` 文件。

### 步骤 2：构建类型索引

扫描所有目标文件，构建符号表：记录每个类/接口/枚举的全限定名、类型、泛型参数、修饰符、父类/接口、Lombok 注解；建立 `简单类名→全限定名` 和 `全限定名→文件路径` 映射。

### 步骤 3：生成 skill 内容

对每个 Java 文件：解析类结构 → 提取 public 成员 → 识别 Lombok → 浓缩 Javadoc → 生成示例 → 格式化。

输出目录结构（按代码包结构组织）：

```
docs/jsf-skills/<module-name>-doc/
├── SKILL.md                              # 入口：frontmatter + 模块概述 + 类索引 + 依赖引入
└── references/
    └── <package-name>/                   # 包名原样作为单级目录名（含点号）
        └── <ClassName>.md               # 每个类一个文件
```

包目录命名规则：Java 包名原样保留（含 `.`）作为单级目录名，**不要**按 `/` 拆分为多级子目录。
- ✅ `io.soil.waf.config/`
- ❌ `io/soil/waf/config/`

### 步骤 4：用户确认（⚠️ 必须等待，不可跳过）

输出摘要表后**必须停止，等待用户回复**：

| 列 | 说明 |
|----|------|
| 类名 | 处理的类/接口/枚举名 |
| 包 | 所属包名 |
| 方法数 | public 方法数量 |
| 字段数 | public 字段数量 |
| Lombok | 识别的注解（无标 `-`） |

同时输出 skill 概要：名称、description、输出路径、总类数、包目录数。

- 用户确认 → 步骤 5
- 用户要求调整 → 修改后重新展示，再次等待
- 用户取消 → 终止

### 步骤 5：输出 skill 文件

1. skill 名称：`<模块名>-doc`（如 `jsf-waf-doc`）
2. 输出路径：`docs/jsf-skills/<模块名>-doc/`
3. SKILL.md — 入口文件，包含 frontmatter + 模块概述 + 类索引表 + 依赖引入信息
4. references/`<package-name>`/`<ClassName>`.md — 每个类一个文件，按包分组
5. frontmatter description：`"Use when coding with <模块名> SDK, need API reference for <模块概要>."`

> 📖 完整输出模板和格式规则详见 [references/output-template.md](references/output-template.md)

### 步骤 6：增量更新（已有 skill 时）

目标 skill 已存在时，增量更新而非全量重写：

1. 按文件粒度检测变更（每个 `<ClassName>.md` 独立检测）

| 变更 | 检测方式 | 操作 |
|------|----------|------|
| 新增类 | 源码有，对应 .md 不存在 | 创建新文件 |
| 删除类 | .md 存在，源码已无对应类 | 删除文件；包目录为空则一并移除 |
| 修改类 | 签名或 Javadoc 变化 | 覆盖对应 .md |
| 无变化 | 均未变 | 跳过 |

2. 同步更新 SKILL.md 中的类索引表
3. 新文件格式与已有文件保持一致

## 提取规则

仅提取 `public` 修饰的成员：

| 元素 | 提取内容 |
|------|---------|
| 类/接口/枚举 | 类名、泛型参数、父类、实现接口、Javadoc |
| 方法 | 签名（含泛型）、返回值、参数、异常、Javadoc |
| 字段 | 字段名、类型、Javadoc |
| 常量 | 常量名、类型、值 |

### Lombok 注解

| 注解 | 生成说明 |
|------|---------|
| `@Data` | 所有字段 getter/setter，一行概括，不逐个列出 |
| `@Getter`/`@Setter` | 类级别=所有字段，字段级别=该字段 |
| `@Builder`/`@SuperBuilder` | 独占"Builder 模式"节，输出链式调用示例（@SuperBuilder 含父类字段） |
| `@AllArgs`/`@NoArgs`/`@RequiredArgs`Constructor | 列入构造表 |
| `@Value` | 同 @Data 但不可变，标注"不可变类" |
| `@With` | 生成 withXxx()，返回新实例 |

标注 `[Lombok 生成]`。

### 类型引用

同包内 → `#ClassName`，跨包 → `../<package-name>/ClassName.md` 相对链接，标准库 → 简单类名，泛型递归解析。

## 转换规则

### 浓缩

核心原则：**动词开头、去元话语、合并同义句**。保留原文语言（英文 Javadoc 保持英文，中文 Javadoc 保持中文），仅精炼表达，不做翻译。

典型转换：

| 原始 | 浓缩后 |
|------|--------|
| "This method is used to get X" / "Returns the X" | "Get X" / "Return X" |
| "@param name the name of the user" | "`name` — user name" |
| "@throws X if Y occurs" / "Please note that X" | "X" / X |

### 省略与保留

**省略**：`@author`、`@since`、`@version`、`@see #method`、`@deprecated` API、Object 默认方法（显式覆写且有 Javadoc 除外）、重复 @param、内部实现细节。

**保留**：`@throws`/`@exception`、`@see` 指向项目内类（转链接）、显式覆写的 Object 方法、空描述成员签名（标 `*(无描述)*`）。

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 步骤 4 输出摘要后直接写入文件 | 必须停止等待用户确认 |
| 所有类塞进单个 SKILL.md | 按包结构拆分，每个类一个 .md 文件 |
| 包目录按路径拆分为多级 | 包名原样作为单级目录名（如 `io.soil.waf.config/`） |
| 逐个列出 @Data 的 getter/setter | 一行概括"所有字段均有 getter/setter" |
| Javadoc 原文照搬不浓缩 | 深度浓缩为精炼表达 |
| 增量更新时全量重写 | 仅覆盖变更类的 .md 文件 |
| 输出文件带 BOM 头 | 所有文件必须 UTF-8 无 BOM 编码 |