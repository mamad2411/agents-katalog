---
name: eliteforge-java-coding-spec
description: 统一璀璨工坊 Java 编码规范，覆盖代码风格、注释规范、POJO/枚举/工具类、控制语句、日志、并发、MyBatis-Plus、事务、Spring、服务间调用、Maven、数据库、网关、接口管理、工程结构等。用户提到"Java规范""编码规范""代码风格""枚举写法""POJO规范""日志规范""事务处理""服务间调用""接口前缀""领域模型""Maven版本""国际化"时使用。
---

# EliteForge Java 编码规范 v1.0.0

## 目标

在 Java 开发任务中，依据规范提供明确的决策指引：什么应该做、什么禁止做、什么必须用什么工具/写法。引用规范条款时给出对应的 spec 行号。

## 执行原则

1. 命中即强制执行  
   规范中标注为"禁止"的条款，任何场景都不得妥协；标注为"必须"的条款不得降级替代。

2. 代码示例优先取规范原文  
   需要示例时，先从 `references/java-coding-spec-v1.md` 中提取对应条款的原文示例，不自行臆造。

3. 最小化加载  
   先用检索定位 spec 行号，再局部读取；避免整篇加载。

4. 明确标注来源  
   回答中标注对应的 spec 条款编号（如 `§3.2 POJO类`）。

## 快速检索

```bash
# 查看 spec 行号索引
cat references/toc.md

# 按关键字定位条款
rg -n "禁止|必须|推荐|使用|Spring|POJO|枚举|日志|事务|并发|MyBatis|服务间调用|Maven|国际化|网关|接口管理|工程" references/java-coding-spec-v1.md

# 按行号读取条款（示例：100-200行）
sed -n '100,200p' references/java-coding-spec-v1.md
```

## 高频问题映射

| 用户问题 | 规范条款 | 核心结论 |
| ------- | ------- | -------- |
| 枚举怎么写 | §3.3 | Enum后缀 + implements BizEnum + @Getter/@RequiredArgsConstructor |
| POJO 类怎么写 | §3.2 | UpperCamelCase + Serializable + serialVersionUID + @Accessors(chain=true) |
| 工具类用什么 | §3.4 | Apache Commons / JDK / 统一框架工具，禁止 hutool |
| 日志怎么打 | §3.6 | @Slf4j + 占位符，禁止 e.printStackTrace() |
| 循环里能调接口吗 | §3.5 | 禁止，必须封装批量接口 |
| 线程池怎么创建 | §3.7 | ThreadPoolExecutor + TransmittableThreadLocal，禁止 Executors |
| MyBatis-Plus 怎么用 | §3.8 | 禁用注解，复杂查询用 xml，keepGlobalFormat=true |
| 事务怎么处理 | §3.9 | public 方法，seata TCC，围住最小必要代码 |
| RestTemplate 能用吗 | §3.10 | 禁止，必须用 RestClient |
| Bean 怎么注入 | §3.10 | @RequiredArgsConstructor，禁止 @Autowired |
| 服务间调用用什么 | §3.11 | HttpExchangeClient + RestClient，统一框架 starter |
| Maven 版本要求 | §3.12 | JDK21 + Maven 3.9.10+ + maven wrapper |
| Controller 怎么分层 | §7.2/§7.3 | Param入参/Vo出参，分离 api/innerapi/openapi |
| 接口路径前缀 | §7.1 | /api 前端 /inner-api 内部 /open-api 开放 |
| 数据库表设计 | §4 | 主键 id + 审计字段 + tenant_id/archived/version 按需 |
| 国际化文件放哪 | §7.6 | biz/resources/i18n/ |
| smart-doc 配置 | §6 | smart-doc.json / smart-doc-innerapi.json / smart-doc-openapi.json |
| 数据库适配 SQL 放哪 | §7.7 | resources/mapper/{mysql,dm,kingbase,oceanbase}/ |

## 核心约束速查

### 禁止清单（任何场景均不得妥协）

| 禁止项 | 必须替代 | 条款 |
| ------ | -------- | ---- |
| hutool | Apache Commons / JDK / 统一框架工具 | §3.4 |
| e.printStackTrace() / System.out | @Slf4j + log 占位符 | §3.6 |
| 循环/递归里调接口 | 批量接口封装 | §3.5 |
| Executors 创建线程池 | ThreadPoolExecutor | §3.7 |
| RestTemplate | Spring6 RestClient | §3.10 |
| @Value 注解读 yaml | Properties 类 | §3.10 |
| @Select/@Insert/@Update 注解 | MyBatis xml | §3.8 |
| context-path | yaml 路由配置 | §3.10 |
| lambdaQuery 多次单表查询 | xml 复杂查询 | §3.8 |
| Controller 层写业务逻辑 | Manager/Service 层 | §3.10 |
| @author JavaDoc | @since | §3.1 |
| 覆盖方式替换框架 Configuration | 扩展类或 yaml 配置 | §3.10 |

### 必须清单

| 必须项 | 说明 | 条款 |
| ------ | ---- | ---- |
| serialVersionUID | POJO 实现 Serializable 时必须定义 | §3.2 |
| @Accessors(chain=true) | Vo/Param/Dto 必须 | §3.2 |
| @since | 新增内容必须标识版本 | §3.1 |
| JSpecify 注解 | @Nullable/@NonNull/@NullMarked | §3.1 |
| 每成员 javadoc | POJO 枚举字段必须 | §3.1/§3.2/§3.3 |
| BizEnum | 前端/Entity 用枚举必须实现 | §3.3 |
| ResVo<T> | Controller 和服务间调用统一响应 | §3.2/§3.11 |
| HttpExchangeClient | 服务间调用必须 | §3.11 |
| keepGlobalFormat=true | @TableField 必须 | §3.8 |
| 函数式 wrapper | MyBatis-Plus wrapper 必须 | §3.8 |
| seata TCC | 分布式事务必须 | §3.9 |
| JDK21 + Maven 3.9.10+ | 必须版本 | §3.12 |
| maven wrapper | 必须使用项目 wrapper | §3.12 |
| 审计字段 | 业务表必须有 | §4 |
| api/inner-api/open-api 前缀 | Controller 路径必须 | §7.1 |
| 前端接口 Param入参/Vo出参 | Controller 必须 | §7.2 |
| 内部接口 Param入参/Dto出参 | InnerController 必须 | §7.2 |
| 开放接口独立 Dto/Param | OpenController 必须 | §7.2 |
| 并发修改加 version | 数据库必须有乐观锁字段 | §4 |

### 工具链速查

| 场景 | 工具 | 条款 |
| ---- | ---- | ---- |
| 字符串拼接 | `java.lang.String.join()` | §3.4 |
| 集合判空 | `CollectionUtils.isEmpty()` / `MapUtils.isEmpty()` | §3.4 |
| 数组判空 | `ArrayUtils.isEmpty()` | §3.4 |
| 字符串判空 | `StringUtils.isBlank()` / `isNotBlank()` | §3.4 |
| 字符串相等 | `Strings.CS.equals()` / `Strings.CI.equals()` | §3.4 |
| 二维元组 | `org.apache.commons.lang3.tuple.Pair<L,R>` | §3.4 |
| 时间工具 | `cn.cisdigital.elite.forge.infra.commons.util.TimeUtils` | §3.4 |
| JSON 工具 | `JsonUtils` | §3.4 |
| 国际化 | `I18nUtils` | §3.4 |
| 上下文 | `ContextStore` | §3.4 |
| 服务间调用 | `cisdigital-elite-forge-infra-httpexchange-spring-boot3-starter` | §3.11 |
| 线程上下文 | `TransmittableThreadLocal` + `TtlExecutors` | §3.7 |
| 日期格式化 | `DateTimeFormatter`（非 SimpleDateFormat） | §3.7 |

## 分层模型速查

### POJO 类分层

```
Entity    → ORM 实体映射，实现 Serializable
Dto       → 内部数据传输
Param     → Controller 入参，必须 jsr 303 validation
Vo        → Controller 出参
```

### 各层入参出参约束

| 层级 | 入参 | 出参 |
| ---- | ---- | ---- |
| repository | Param / Dto | Entity / Dto |
| service | Param / Dto | Dto / Vo |
| 前端接口 Controller | Param | Vo |
| 内部接口 InnerController | Param | Dto |
| 开放接口 OpenController | Param | Dto |

### Maven 模块结构

```
<service>-model        POJO + MapStruct
<service>-client       HttpExchangeClient 接口定义
<service>-xxx-starter  业务相关 starter
<service>-xxx-sdk      业务相关 sdk
<service>-biz          业务模块（controller/service/repository）
<service>-boot         启动模块
```

### biz 代码分层

```
- biz/common/exception
- biz/common/util
- biz/模块A/controller/{innerapi, api, openapi}
- biz/模块A/service/xxxService
- biz/模块A/repository/{mapper/xxxMapper, xxxRepository}
```

### 接口路径前缀

- `/api` → 前端接口（需网关鉴权）
- `/inner-api` → 服务间内部调用（无需鉴权）
- `/open-api` → 开放接口（需开放平台鉴权）

## 输出约束

- 回答时必须标注规范条款编号（§章节号）
- 涉及代码示例时，从 `references/java-coding-spec-v1.md` 对应条款提取，不自行编写
- 涉及框架/工具选型时，优先引用统一框架能力，参见 `eliteforge-framework-specification`
- 涉及版本号时引用规范原文，不臆造具体版本
- 规范未覆盖的场景，标注"需用户补充或需外部确认"

## 参考资料

- 规范全文（行号索引）：`references/toc.md`
- 规范全文：`references/java-coding-spec-v1.md`
