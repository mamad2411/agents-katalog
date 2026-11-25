---
name: common-skill-l2
description: "当其它基础仓颉 Skills（例如 cangjie-array 等）无法命中知识点、答案不准确/过时/不适用，或工程出现编译错误、构建失败、运行异常、报错信息难以理解时，应调用 common-skill-l2，使用 L1→L3 混合检索获取对应的仓颉知识点、示例代码和错误排查思路。"
---

# 仓颉混合检索 SKILL

## 目的

当仓颉通用基础 Skills 检索失效时，进行 L1 RAG 知识库检索与 L3 官方文档全量查询的混合检索。

## 重要提示：脚本路径与执行方式

- **L1 RAG 查询脚本**（位于 `.opencode/skills/cangjie-dev-harmonyos/scripts/ask_cangjie.py`）：通过 `python .opencode/skills/cangjie-dev-harmonyos/scripts/ask_cangjie.py "待查询的技术关键词"` 命令执行，用于 L1 阶段检索知识库。

**注意**：L1 RAG 功能需要在 `.env` 文件中配置有效的 `SILICONFLOW_API_KEY` 才能使用，否则脚本会输出 `NO_RAG_RESULT` 并跳过 L1。

- **经验记录文档**: `.opencode/skills/cangjie-evolution/Evolution.md`：用于记录踩过的坑

## L1: RAG 知识检索

**目的:** 获取仓颉语言原生的标准代码片段、API 用法和规范。

**操作:** 当仓颉通用的基础检索失效时，调用 bash/terminal 工具执行 Python 脚本检索知识库。

**策略:** 优先使用提炼出的纯技术词汇，最好使用纯英文API名称，让关键词匹配发挥最大效果。

### L1 查询执行策略
**强制调用规范:**
 你必须明确调用你的 bash/terminal 工具，执行以下命令：
```bash
python .opencode/skills/cangjie-dev-harmonyos/scripts/ask_cangjie.py "<核心关键词>"
```

- **纯英文关键词**: 先直接使用不添加中文后缀的英文API名称检索
- **单词精准**: 一个关键词（如 "HTTP"）可匹配该组件的所有相关信息
- **中文关键词**: 如果英文关键词检索结果不完整或不相关，可以尝试使用中文关键词或添加中文后缀检索
- **分步检索**: 如果项目涉及多个技术点，必须分多次执行该命令，每次一个核心关键词
- **结果展示**: **必须将L1查询结果贴出来供用户查看**，不要隐藏查询过程

如果项目复杂，包含多个不同的技术点（例如既有文件读写，又有JSON解析），你可以分多次执行该命令。

### 绝对禁止行为 (Stop and Wait):
执行完检索命令后，必须立刻停止生成。严禁在没有看到终端返回结果的情况下，就开始凭空编写仓颉代码。

### L1 评估 (Self-Reflection):

- 终端返回了可用的知识点或代码片段 -> 仔细阅读，进入 下一阶段

- 终端返回的知识点不相关或用不上 -> 进入 L3: 官方文档全量检索兜底

## L3: 官方文档全量检索兜底

### 目的

在仓颉通用基础检索与 L1 的 RAG 检索都没查到有用的知识情况下，通过读取本地索引文件定位目标 API 文档，随后读取完整文档以获取官方标准实现和上下文，用官方文档来兜底，严禁凭空想象仓颉代码！

### 核心原则

根据分析出的核心技术关键词，查询官方文档目录，锁定索引文件，提取目标文档路径，并读取目标文档内容。

### 核心检索逻辑说明

**必须严格遵守此推理顺序：**

1. 提取前面阶段未检索到的“核心技术关键词”。
2. 扫描下方的**分类大纲目录**，寻找与关键词最相关的“知识点/模块”（例如：关键词有 HTTPS，对应找到 `stdx.net.http` 模块）。
3. 确定该知识点属于哪一个具体的“目标索引文件”（例如：属于 `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/stdx.md`）。
4. 调用 `Read` 工具全文读取那个选中的索引文件。
5. 在读入的索引文件中，利用刚刚确定的“知识点/模块”定位，找出具体文档的相对路径（例如：`libs_stdx/net/http/http_package_overview.md` 的路径），然后根据文档文件夹所在路径如`.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/stdx`拼接为具体路径`.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/stdx/libs_stdx/net/http/http_package_overview.md`。
6. 最后，调用 `Read` 工具读取该具体文档，学习代码写法。

#### 步骤 1：锁定目标索引文件 (Determine Target Index)
所有官方文档的目录索引均位于 `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/` 目录下。根据上述逻辑，用 L0 关键词对比以下四个目录大纲，锁定你需要查阅的**知识点**以及它对应的**索引文件**：

1. **语言基础特性与语法** -> 目标索引: `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/syntax.md`

    基本概念(标识符, 程序结构, 表达式, 函数)

    基础数据类型(基本操作符, 整数类型, 浮点类型, 布尔类型, 字符类型, 字符串类型, 元组类型, 数组类型, 区间类型, Unit 类型, Nothing 类型)

    函数(定义函数, 调用函数, 函数类型, 嵌套函数, Lambda 表达式, 闭包, 函数调用语法糖, 函数重载, 操作符重载, const 函数和常量求值)

    结构类型(定义 struct 类型, 创建 struct 实例, mut 函数)

    枚举类型和模式匹配(枚举类型, Option 类型, 模式概述, 模式的 Refutability, match 表达式, 其他使用模式的地方)

    类和接口(类, 接口, 属性, 子类型关系, 类型转换)

    泛型(泛型概述, 泛型函数, 泛型接口, 泛型类, 泛型结构体, 泛型枚举, 泛型类型的子类型关系, 类型别名, 泛型约束)

    扩展(扩展概述, 直接扩展, 接口扩展, 访问规则)

    Collection 类型(基础 Collection 类型概述, ArrayList, HashSet, HashMap, Iterable 和 Collections)

    包(包的概述, 包的声明, 顶层声明的可见性, 包的导入, 程序入口)

    异常处理(定义异常, throw 和处理异常, 常见运行时异常, 使用 Option)

    并发编程(并发概述, 创建线程, 访问线程, 终止线程, 同步机制, 线程睡眠指定时长 sleep)

    基础 I/O 操作(I/O 流概述, I/O 节点流, I/O 处理流)

    网络编程(网络编程概述, Socket 编程, HTTP 编程, WebSocket 编程)

    宏(宏的简介, Tokens 相关类型和 quote 表达式, 语法节点, 宏的实现, 编译、报错与调试, 宏包定义和导入, 内置编译标记, 实用案例)

    反射和注解(动态特性, 注解)

    跨语言互操作(仓颉-C 互操作)

    编译和构建(`cjc` 使用, `cjpm` 介绍, 条件编译)

    部署和运行(部署仓颉运行时, 运行仓颉可执行程序)

    附录(`cjc` 编译选项, Linux 版本工具链的支持与安装, runtime 环境变量使用手册, 关键字, 操作符, 操作符函数, TokenKind 类型, 仓颉包兼容性检查)


2. **标准库 (stdlib)** -> 目标索引: `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/stdlib.md`

    std.core(函数, 类型别名, 内置类型, 接口, 类, 枚举, 结构体, 异常类)

    std.argopt(函数, 类, 枚举, 结构体, 异常类)

    std.ast(函数, 接口, 类, 枚举, 结构体, 异常类)

    std.binary(接口)

    std.collection(函数, 接口, 类, 异常类)

    std.collection.concurrent(类型别名, 接口, 类)

    std.console(类)

    std.convert(接口)

    std.crypto.cipher(接口)

    std.crypto.digest(函数, 接口)

    std.database.sql(接口, 类, 枚举, 异常类)

    std.deriving(宏)

    std.env(函数, 类, 异常类)

    std.fs(函数, 类, 枚举, 结构体, 异常类)

    std.io(函数, 接口, 类, 枚举, 异常类)

    std.math(接口, 函数, 枚举)

    std.math.numeric(函数, 枚举, 结构体)

    std.net(接口, 类, 枚举, 结构体, 异常类)

    std.objectpool(类)

    std.overflow(接口, 异常类)

    std.posix(常量&变量, 函数)

    std.process(函数, 类, 枚举, 异常类)

    std.random(类)

    std.ref(类, 枚举)

    std.reflect(函数, 类型别名, 类, 枚举, 异常类)

    std.regex(类, 枚举, 结构体, 异常类)

    std.runtime(函数, 结构体)

    std.sort(函数, 接口)

    std.sync(常量&变量, 接口, 类, 枚举, 结构体, 异常类)

    std.time(类, 枚举, 结构体, 异常类)

    std.unicode(接口, 枚举)

    std.unittest(函数, 类型别名, 接口, 类, 枚举, 结构体, 异常类)

    std.unittest.mock(函数, 接口, 类, 枚举, 异常类)

    std.unittest.mock.mockmacro(宏)

    std.unittest.testmacro(宏)

    std.unittest.common(常量&变量, 函数, 接口, 类, 枚举, 结构体, 异常类)

    std.unittest.diff(接口)

    std.unittest.prop_test(函数, 接口, 类, 结构体)

3. **扩展库 (stdx)** -> 目标索引: `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/stdx.md`

    stdx.aspectCJ(类, 示例教程: AOP 开发示例)

    stdx.compress.zlib(类, 枚举, 异常类, 示例教程: Deflate 格式数据的压缩和解压/Gzip 格式数据的压缩和解压)

    stdx.crypto.crypto(类, 结构体, 异常类, 示例教程: SecureRandom 使用/SM4 使用)

    stdx.crypto.digest(类, 结构体, 异常类, 示例教程: digest 使用)

    stdx.crypto.keys(类, 枚举, 结构体, 示例教程: keys 使用)

    stdx.crypto.x509(类型别名, 接口, 类, 枚举, 结构体, 异常类, 示例教程: x509 使用)

    stdx.encoding.base64(函数, 示例教程: Byte 数组和 Base64 互转)

    stdx.encoding.hex(函数, 示例教程: Byte 数组和 Hex 互转)

    stdx.encoding.json(接口, 类, 枚举, 异常类, 示例教程: JsonArray 使用示例/JsonValue 和 String 互相转换/JsonValue 与 DataModel 的转换)

    stdx.encoding.json.stream(接口, 类, 枚举, 结构体, 示例教程: 使用 Json Stream 进行反序列化/使用 Json Stream 进行序列化/WriteConfig 使用示例)

    stdx.encoding.url(类, 异常类, 示例教程: Form 的构造使用/URL 解析函数 parse 的使用)

    stdx.fuzz.fuzz(常量&变量, 类, 异常类, 示例教程: 测试猜测字符功能/使用 DataProvider 功能进行测试/使用 FakeCoverage 避免 DataProvider 模式下 Fuzz 异常终止/打印 fuzz 使用方法/实验性特性-覆盖率信息打印/栈回溯缺失的处理方案)

    stdx.log(类型别名, 函数, 接口, 类, 结构体, 异常类, 示例教程: 日志打印示例)

    stdx.logger(类, 示例教程: 日志打印示例)

    stdx.net.http(函数, 接口, 类, 枚举, 结构体, 异常类, 示例教程: client/cookie/log/server/webSocket/h1_gzip)

    stdx.net.tls(类, 枚举, 结构体, 异常类, 示例教程: 服务端证书及公钥在一份文件中/客户端示例/证书热更新/服务端示例)

    stdx.serialization.serialization(函数, 接口, 类, 异常类, 示例教程: class 序列化和反序列化/HashSet 和 HashMap 序列化)

    stdx.unittest.data(函数, 类)

4. **编译构建与命令行工具** -> 目标索引: `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/tools.md`
   
    项目管理工具
    
    调试工具
    
    格式化工具
    
    静态检查工具
    
    覆盖率统计工具
    
    语言服务器工具
    
    CHIR 反序列化工具
    
    异常堆栈信息还原工具
    
    性能分析工具

#### 步骤 2：读取索引文件提取目标路径 (Extract Target Path)
锁定目标索引文件后，**警告：严禁臆测 API 文档路径！** 必须严格执行以下操作：
1. 明确调用自带的 `Read` 工具，将步骤 1 锁定的**索引文件**（如 `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/index/stdx.md`）全文读入。
2. 在读入的索引文件内容中，寻找你在步骤 1 确定的“知识点/模块”（例如找 `stdx.net.http`）。
3. 提取该模块下对应文档的真实相对路径（即 Markdown 链接括号 `()` 内的路径片段）。

#### 步骤 3：读取目标文档 (Read Target Document)
获取相对路径后，执行以下操作：
1. **防 API 阻断强制约束**：为了防止 API Payload 过大导致 400 报错，**每次调用 Read 工具最多只允许读取 1 到 2 个最核心的文档**！严禁一次性读取 3 个及以上文件。**尽量不要读取名称包含 `_classes.md`、`_funcs.md` 或 `_interfaces.md` 的巨型 API 字典文件！** 你**尽量**寻找并读取名称包含 `_samples.md`（示例代码）或 `_overview.md` 的文件。

2. 拼接绝对读取路径：根据索引文件来源拼接路径：
   - `syntax.md` 索引 → `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/syntax/{相对路径}`
   - `stdlib.md` 索引 → `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/stdlib/{相对路径}`
   - `stdx.md` 索引 → `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/stdx/{相对路径}`
   - `tools.md` 索引 → `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/tools/{相对路径}`

   例如：从 `stdx.md` 索引中提取到路径 `libs_stdx/net/http/http_samples/http_client.md`，则拼接为 `.opencode/skills/cangjie-dev-harmonyos/scripts/hm-docs/stdx/libs_stdx/net/http/http_samples/http_client.md`。
3. 明确调用自带的 `Read` 工具，将拼接后的目标文档全文读入上下文。
4. 提取文档中的包导入声明（import）及 API 调用示例等实用知识点。
5. 在后续工程构建阶段，所生成的代码架构与语法必须 100% 遵照该官方文档的规范。