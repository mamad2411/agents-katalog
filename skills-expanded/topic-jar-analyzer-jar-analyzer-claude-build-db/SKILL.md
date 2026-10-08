---
name: build-db
description: 使用 jar-analyzer-engine 从 JAR/WAR/Class 文件构建 SQLite 分析数据库。这是进行 Java 代码安全审计、方法调用分析的第一步。
---

# build-db — 构建 Jar Analyzer 分析数据库

## 概述

使用内置的 `jar-analyzer-engine-1.2.0.jar` 对目标 JAR/WAR/Class 文件进行静态分析，
生成 SQLite 数据库（`jar-analyzer.db`）。该数据库包含类信息、方法定义、方法调用关系、
继承关系、字符串常量、Spring 组件信息等，是后续所有分析操作的数据基础。

## 引擎位置

```
<plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar
```

> `<plugin_dir>` 是本插件的安装目录（即包含 `bin/`、`skills/` 的目录）。
> 运行前请确认 Java 8+ 已安装且在 PATH 中。

## 命令参考

```
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar [options]
```

### 必选参数

| 参数 | 说明 |
|:-----|:-----|
| `--jar <path>`, `-j <path>` | 目标 JAR/WAR 文件或包含 class 文件的目录路径（**必需**） |

### 可选参数

| 参数 | 说明 | 默认值 |
|:-----|:-----|:-------|
| `--quick`, `-q` | 快速模式：仅分析方法调用关系，跳过继承/字符串/Spring 分析 | `false` |
| `--inner-jars` | 解析 JAR 内嵌套的 JAR（如 Spring Boot FatJar） | `false` |
| `--fix-class` | 使用 FixClassVisitor 修复类名 | `false` |
| `--no-fix-impl` | 禁用自动方法实现修复（不推荐） | `false` |
| `--rt <path>` | 指定 rt.jar 路径（用于 JDK 类分析） | 无 |
| `--white-list <text>`, `-w <text>` | 类/包白名单（仅分析匹配的类），支持文本或文件路径 | 无 |
| `--white-list-file <path>` | 白名单文件路径 | 无 |
| `--black-list <text>`, `-b <text>` | 类/包黑名单（排除匹配的类），支持文本或文件路径 | 无 |
| `--black-list-file <path>` | 黑名单文件路径 | 无 |
| `--log-level <level>` | 日志级别：DEBUG, INFO, WARN, ERROR | `INFO` |
| `--decompile <class>`, `-d <class>` | 反编译模式：反编译指定类并输出源码（不构建数据库） | 无 |
| `--help`, `-h` | 显示帮助信息 | — |

### 黑白名单说明

- 使用 `/` 分隔的包名格式（如 `com/example/app`）
- 白名单：**仅**分析匹配的包/类
- 黑名单：**排除**匹配的包/类
- 支持直接传入文本，或指定一个文件路径（每行一个包名/类名）
- 黑白名单不能同时使用

## 输出

| 产出 | 路径 | 说明 |
|:-----|:-----|:-----|
| SQLite 数据库 | `jar-analyzer.db`（当前工作目录） | 包含全部分析结果 |
| 临时目录 | `jar-analyzer-temp/`（当前工作目录） | 解压的 class 文件，分析完成后可清理 |

## 数据库包含的信息

| 数据类型 | 说明 |
|:---------|:-----|
| 类信息 | 类名、父类、接口、注解、访问修饰符 |
| 方法信息 | 方法名、描述符、注解、访问修饰符 |
| 成员变量 | 字段名、类型、访问修饰符 |
| 方法调用关系 | 调用者 → 被调用者的完整映射 |
| 继承/实现关系 | 类继承链、接口实现关系 |
| 方法实现 | 接口方法 → 实现方法的映射 |
| 字符串常量 | LDC 指令加载的字符串及其所在方法 |
| 注解字符串 | 注解中的字符串值 |
| Spring 组件 | Controller、Mapping、参数信息（如适用） |
| Class 文件 | 原始 class 文件的二进制数据 |

## 标准操作流程（SOP）

### 1. 确认环境

```bash
java -version
# 确保 Java 8+ 可用
```

### 2. 确认目标文件

向用户确认待分析的 JAR/WAR 文件路径或目录路径。

### 3. 选择分析模式

根据场景选择合适的参数组合：

**完整分析**（推荐，适合安全审计）：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path>
```

**快速分析**（仅方法调用关系，速度更快）：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path> -q
```

**FatJar 分析**（Spring Boot 等嵌套 JAR）：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path> --inner-jars
```

**指定范围分析**（仅分析特定包）：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path> -w "com/example/app"
```

**排除第三方库**：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path> -b "org/apache"
```

### 4. 执行构建

运行命令并观察输出，关注以下关键信息：
- `totalJar`: 发现的 JAR 文件数量
- `totalClass`: 分析的类数量
- `totalMethod`: 分析的方法数量
- `dbSize`: 生成的数据库大小
- `Progress: 100%`: 构建完成
- `Time elapsed`: 构建耗时

### 5. 验证结果

确认 `jar-analyzer.db` 已生成，并告知用户：
- 数据库路径
- 分析的类/方法数量
- 数据库大小
- 可以使用 `do-analyze` skill 进行后续分析

### 6. 反编译模式（可选）

如果用户只需要快速查看某个类的源码，可以使用反编译模式：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j <target_path> -d <fully.qualified.ClassName>
```

例如：
```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar -j app.jar -d com.example.MyController
```

> 注意：反编译模式不会构建数据库，仅输出反编译后的 Java 源码到控制台。

## 注意事项

- 当 JAR 数量较多或体积较大时，数据库文件和临时目录可能非常大，请确保磁盘有足够空间
- 构建过程中会在当前目录创建 `jar-analyzer-temp/` 临时目录
- 如果数据库已存在，重新运行会**覆盖**旧数据库
- 建议在目标项目目录或专门的分析目录下执行命令
- Windows 环境下路径使用 `\` 或 `/` 均可
