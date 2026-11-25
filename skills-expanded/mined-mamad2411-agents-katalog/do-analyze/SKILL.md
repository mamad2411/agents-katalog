---
name: do-analyze
description: 对 jar-analyzer-engine 构建的 SQLite 数据库执行安全审计分析查询。支持方法调用搜索、调用链追踪、Spring 组件分析、字符串搜索、漏洞模式检测等。
---

# do-analyze — Jar Analyzer 数据库分析与安全审计

## 概述

在 `build-db` skill 构建好 `jar-analyzer.db` 后，使用本 skill 对数据库进行各类安全分析查询。
通过 SQL 查询 + 反编译验证的方式，实现方法调用搜索、调用链追踪、漏洞模式检测等功能。

## 前提条件

- 已使用 `build-db` skill 构建了 `jar-analyzer.db` 数据库
- 当前工作目录下存在 `jar-analyzer.db` 文件
- Java 8+ 可用（用于反编译验证）

## 数据库表结构

> **不要在本文件中重复描述数据库表结构。**
> 请参考 `<plugin_dir>/references/DATABASE.md` 获取完整的数据库 Schema、字段说明、表关联关系和常用查询模式。

## 重要约定

### 方法唯一标识（四元组）

任何方法节点必须通过 **四元组** 唯一标识：
```
(jar_id, class_name, method_name, method_desc)
```

> **禁止**仅用方法名进行 join 或追链，因为方法重载很常见。

### 类名格式

数据库中的类名使用 `/` 分隔（JVM 内部格式），而非 `.` 分隔：
- ✅ `com/example/controller/UserController`
- ❌ `com.example.controller.UserController`

### 方法描述符格式

使用 JVM 方法描述符格式：
- `(Ljava/lang/String;)V` = `void method(String)`
- `(Ljava/lang/String;I)Ljava/lang/String;` = `String method(String, int)`
- `()V` = `void method()`

## 分析操作流程（SOP）

### 执行 SQL 查询的方式

**优先使用 `sqlite3` 命令行工具**（直接、高效）：

```bash
# 单条查询
sqlite3 jar-analyzer.db "SELECT COUNT(*) FROM method_table;"

# 格式化输出（带表头、列对齐）
sqlite3 -header -column jar-analyzer.db "SELECT class_name, method_name FROM method_table LIMIT 10;"

# 多条查询
sqlite3 -header -column jar-analyzer.db <<'EOF'
SELECT 'JAR文件' AS type, COUNT(*) AS count FROM jar_table
UNION ALL
SELECT '类', COUNT(*) FROM class_table
UNION ALL
SELECT '方法', COUNT(*) FROM method_table;
EOF

# 输出为 CSV
sqlite3 -header -csv jar-analyzer.db "SELECT * FROM spring_method_table;" > routes.csv
```

**如果 `sqlite3` 不可用，使用 Python 作为备选**：

```python
import sqlite3

conn = sqlite3.connect('jar-analyzer.db')
cursor = conn.execute("SQL_QUERY_HERE")
for row in cursor:
    print(row)
conn.close()
```

> 将上述代码写入临时 `.py` 文件执行，分析完成后删除临时文件。

### 常用分析场景与 SQL

#### 1. 项目概览 — 了解分析目标的基本信息

```sql
SELECT 'JAR文件' AS type, COUNT(*) AS count FROM jar_table
UNION ALL
SELECT '类', COUNT(*) FROM class_table
UNION ALL
SELECT '方法', COUNT(*) FROM method_table
UNION ALL
SELECT '方法调用', COUNT(*) FROM method_call_table
UNION ALL
SELECT '字符串常量', COUNT(*) FROM string_table
UNION ALL
SELECT 'Spring Controller', COUNT(*) FROM spring_controller_table
UNION ALL
SELECT 'Spring 映射', COUNT(*) FROM spring_method_table
UNION ALL
SELECT 'Servlet/Filter', COUNT(*) FROM java_web_table;
```

#### 2. 方法调用搜索 — 查找谁调用了某个方法

```sql
-- 查找谁调用了某个特定类的方法（精确搜索）
SELECT DISTINCT
    caller_class_name, caller_method_name, caller_method_desc
FROM method_call_table
WHERE callee_class_name = 'java/lang/Runtime'
  AND callee_method_name = 'exec';

-- 模糊搜索
SELECT DISTINCT
    caller_class_name, caller_method_name,
    callee_class_name, callee_method_name
FROM method_call_table
WHERE callee_class_name LIKE '%ClassName%'
  AND callee_method_name LIKE '%methodName%';
```

#### 3. 方法定义搜索 — 查找某个方法定义在哪里

```sql
-- 精确搜索
SELECT class_name, method_name, method_desc, is_static, line_number
FROM method_table
WHERE method_name = 'execute';

-- 模糊搜索
SELECT class_name, method_name, method_desc, line_number
FROM method_table
WHERE method_name LIKE '%upload%'
   OR method_name LIKE '%file%';
```

#### 4. 反向调用链追踪 — 从 sink 回溯到 entry

```sql
-- 使用 SQLite 递归 CTE 追踪调用链（推荐）
WITH RECURSIVE call_chain AS (
    SELECT caller_class_name, caller_method_name, caller_method_desc,
           callee_class_name, callee_method_name, callee_method_desc, 1 AS depth
    FROM method_call_table
    WHERE callee_class_name = 'java/lang/Runtime' AND callee_method_name = 'exec'
    UNION ALL
    SELECT mc.caller_class_name, mc.caller_method_name, mc.caller_method_desc,
           mc.callee_class_name, mc.callee_method_name, mc.callee_method_desc, cc.depth + 1
    FROM method_call_table mc
    JOIN call_chain cc ON mc.callee_class_name = cc.caller_class_name
                      AND mc.callee_method_name = cc.caller_method_name
                      AND mc.callee_method_desc = cc.caller_method_desc
    WHERE cc.depth < 10
)
SELECT DISTINCT caller_class_name, caller_method_name, depth
FROM call_chain
ORDER BY depth;
```

> 也可以编写 Python 脚本实现 DFS/BFS 调用链追踪，灵活度更高。

#### 5. Spring 入口分析

```sql
-- 列出所有 Spring Controller
SELECT class_name FROM spring_controller_table;

-- 列出所有 HTTP 映射（API 入口）
SELECT class_name, method_name, restful_type, path
FROM spring_method_table
ORDER BY path;

-- 查找特定 URL 模式的处理方法
SELECT class_name, method_name, method_desc, restful_type, path
FROM spring_method_table
WHERE path LIKE '%user%' OR path LIKE '%admin%';
```

#### 6. Java Web 组件分析

```sql
-- 列出所有 Servlet/Filter/Listener
SELECT type_name, class_name FROM java_web_table;

-- 只看 Filter（可能是安全过滤器）
SELECT class_name FROM java_web_table WHERE type_name = 'Filter';
```

#### 7. 字符串搜索 — 敏感信息检测

```sql
-- 搜索包含关键字的字符串（如密码、密钥等）
SELECT class_name, method_name, value
FROM string_table
WHERE value LIKE '%password%'
   OR value LIKE '%secret%'
   OR value LIKE '%key%'
   OR value LIKE '%token%';

-- 搜索 JNDI/LDAP/RMI 相关字符串
SELECT class_name, method_name, value
FROM string_table
WHERE value LIKE '%jndi%' OR value LIKE '%ldap://%' OR value LIKE '%rmi://%';

-- 搜索 SQL 语句（可能有 SQL 注入风险）
SELECT class_name, method_name, value
FROM string_table
WHERE value LIKE '%SELECT%FROM%'
   OR value LIKE '%INSERT%INTO%'
   OR value LIKE '%UPDATE%SET%'
   OR value LIKE '%DELETE%FROM%';

-- 搜索 IP 地址和 URL
SELECT class_name, method_name, value
FROM string_table
WHERE value LIKE '%://%'
   OR value LIKE '%.%.%.%';
```

#### 8. 继承关系分析

```sql
-- 查找某个类的所有子类
SELECT class_name, super_class_name
FROM class_table
WHERE super_class_name LIKE '%AbstractController%';

-- 查找某个接口的所有实现类
SELECT class_name, interface_name
FROM interface_table
WHERE interface_name LIKE '%Serializable%';

-- 查找方法实现（接口方法 → 具体实现）
SELECT class_name, method_name, method_desc, impl_class_name
FROM method_impl_table
WHERE method_name = 'doFilter';
```

#### 9. 注解分析

```sql
-- 查找所有带特定注解的类/方法
SELECT class_name, method_name, anno_name
FROM anno_table
WHERE anno_name LIKE '%RequestMapping%'
   OR anno_name LIKE '%GetMapping%'
   OR anno_name LIKE '%PostMapping%';

-- 查找 Controller 类注解
SELECT class_name, anno_name
FROM anno_table
WHERE method_name IS NULL
  AND anno_name LIKE '%Controller%';
```

#### 10. 漏洞 Sink 检测

> **Sink 定义文件**：`<plugin_dir>/references/dfs-sink.json`
>
> 该 JSON 文件包含完整的危险方法（sink）列表，每个条目包含 `className`、`methodName`、`methodDesc` 三个字段。
> 进行漏洞检测时，**必须读取并解析该文件**，然后基于其中的 sink 定义构造 SQL 查询。

**Sink 检测流程**：

1. 读取 `<plugin_dir>/references/dfs-sink.json` 文件
2. 解析 JSON 获取所有 sink 条目
3. 对每个 sink，查询 `method_call_table` 中是否存在调用：

```sql
-- 通用 sink 查询模板（根据 dfs-sink.json 中的条目填充参数）
SELECT DISTINCT
    caller_class_name, caller_method_name, caller_method_desc
FROM method_call_table
WHERE callee_class_name = '<sink.className>'
  AND callee_method_name = '<sink.methodName>'
  AND callee_method_desc = '<sink.methodDesc>';
```

**dfs-sink.json 覆盖的漏洞类型**包括但不限于：

| 漏洞类型 | 典型 Sink |
|:---------|:----------|
| RCE（远程代码执行） | `Runtime.exec`、`ProcessBuilder.start`、`ScriptEngine.eval` |
| JNDI 注入 | `InitialContext.lookup`、`Context.lookup` |
| LDAP 注入 | `DirContext.search`、`LdapContext.search` |
| SQL 注入 | `Statement.execute/executeQuery/executeUpdate`、`Connection.prepareStatement/prepareCall` |
| 反序列化 | `ObjectInputStream.readObject`、`XMLDecoder.readObject`、`Yaml.load`、`JSON.parseObject`、`XStream.fromXML` 等 |
| 文件操作 | `FileInputStream/FileOutputStream/RandomAccessFile` 构造、`File.delete` |
| SSRF | `URL.openConnection`、`HttpURLConnection.connect` |
| 类加载 | `BCEL ClassLoader.loadClass` |

> 注意：dfs-sink.json 中的 `methodDesc` 是精确匹配的，确保查询时使用完整的描述符。

**批量 Sink 检测示例（Python）**：

```python
import json
import sqlite3

# 读取 sink 定义
with open('<plugin_dir>/references/dfs-sink.json', 'r') as f:
    sinks = json.load(f)

conn = sqlite3.connect('jar-analyzer.db')

for sink in sinks:
    cursor = conn.execute("""
        SELECT DISTINCT caller_class_name, caller_method_name, caller_method_desc
        FROM method_call_table
        WHERE callee_class_name = ?
          AND callee_method_name = ?
          AND callee_method_desc = ?
    """, (sink['className'], sink['methodName'], sink['methodDesc']))
    
    results = cursor.fetchall()
    if results:
        print(f"\n=== {sink['boxName']} ===")
        for row in results:
            print(f"  {row[0]}.{row[1]} {row[2]}")

conn.close()
```

### 反编译验证（关键步骤）

> **重要**：SQL 查询只能发现方法调用关系，无法判断数据流和上下文。
> **必须使用 `--decompile` 反编译可疑类的源码，从具体代码中确认问题是否真实存在。**

当通过 SQL 分析发现可疑调用后，使用反编译功能查看完整源码：

```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar \
    -j <target_jar_path> \
    -d <fully.qualified.ClassName>
```

> 类名使用 `.` 分隔格式（如 `com.example.MyController`），而非数据库中的 `/` 分隔格式。
> 数据库中查到的类名是 `/` 分隔的，需要替换为 `.` 再传给 `-d` 参数。

**反编译确认要点**：

- 查看可疑方法的完整实现，确认外部输入是否能到达危险调用
- 检查是否有参数校验、白名单过滤、安全沙箱等防护措施
- 确认调用路径上是否存在条件分支导致实际不可达
- 对于调用链中的每一跳，都建议反编译查看中间方法的逻辑

**示例**：SQL 查询发现 `com/example/controller/FileController` 的 `upload` 方法调用了 `FileOutputStream.<init>`，反编译确认：

```bash
java -jar <plugin_dir>/bin/jar-analyzer-engine-1.2.0.jar \
    -j app.jar \
    -d com.example.controller.FileController
```

查看反编译结果中 `upload` 方法是否对文件名做了路径穿越防护、文件类型校验等。

## 分析工作流建议

### 基本流程

1. **了解目标**：执行概览查询，了解项目规模和技术栈
2. **识别入口**：分析 Spring 映射、Servlet/Filter 等 HTTP 入口点
3. **检测 Sink**：读取 `dfs-sink.json`，批量检测所有已知危险方法调用
4. **追踪链路**：从 sink 向上追踪调用链，检查是否可从入口可达
5. **反编译确认**：**对链路上的关键类使用 `--decompile` 查看源码**，确认数据流是否可控、是否有安全防护
6. **字符串辅助**：搜索敏感字符串作为补充线索
7. **形成报告**：汇总发现的安全问题

### 优先级建议

| 优先级 | 漏洞类型 | 危害程度 |
|:-------|:---------|:---------|
| P0 | RCE（命令执行）、反序列化 | 严重 |
| P1 | SQL 注入、JNDI 注入、SpEL 注入 | 高 |
| P2 | SSRF、XXE、任意文件读写 | 高 |
| P3 | 文件上传、路径穿越 | 中 |
| P4 | 信息泄露、硬编码密钥 | 中 |

## 注意事项

- SQL 查询中的类名使用 `/` 分隔格式
- 反编译命令中的类名使用 `.` 分隔格式
- `method_desc` 是精确匹配的关键，避免因方法重载导致误判
- `callee_jar_id = -1` 表示被调用方法来自 JDK/外部库（不在分析的 JAR 中）
- 大型数据库查询可能较慢，建议使用 `LIMIT` 限制结果数量
- 优先使用 `sqlite3` 命令行查询，不可用时再使用 Python
- 分析完成后请删除临时脚本文件
