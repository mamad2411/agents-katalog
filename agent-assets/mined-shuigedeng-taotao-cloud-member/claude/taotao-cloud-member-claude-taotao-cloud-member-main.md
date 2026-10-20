# taotao-cloud-member — 会员领域 DDD 单体服务

会员中心，基于 Spring Boot 4.1.1 / JDK 25 / Gradle 9.5 的六边形架构 + DDD 服务。

## WHAT — 项目地图

### 技术栈

| 组件 | 版本 |
|------|------|
| Java / Gradle | 25 (--enable-preview) / 9.5 |
| Spring Boot / Cloud / Alibaba | 4.1.1 / 2025.1.1 / 2025.1.0.0 |
| MyBatis-Plus / Knife4j / Redisson | 3.5.16 / 4.5.0 / 4.3.1 |
| MapStruct / Lombok / Querydsl | 1.6.3 / 1.18.46 / 5.1.0 |
| RocketMQ / Netty | 5.2.4 / 4.2.12.Final |

### 8 模块结构

```
taotao-cloud-member/
├── api/               RPC/gRPC 接口 + DTO（纯定义，零依赖）
├── application/       应用层：编排、事务、DTO 转换
├── assembly/          启动器 + 环境配置
├── common/            公共枚举、常量
├── domain/            ★ 领域层（零外部依赖）
├── facade/            防腐层 ACL（独立 Gradle Module）
├── infrastructure/    持久化、MQ、事件、缓存、任务
└── interfaces/        REST / RPC / gRPC 实现
```

包路径：`com.taotao.cloud.member.{layer}.{sub}`

### WHERE TO LOOK

| 你要做什么 | 去哪个目录 |
|-----------|-----------|
| 新增业务功能 | `application/service/command/` 定义 + `interfaces/controller/{role}/` 实现 |
| 修改领域模型 | `domain/aggregate/` 或 `domain/entity/` |
| 值对象（final + 无 setter） | `domain/valobj/` |
| 领域事件 | `domain/event/` — 聚合内 registerEvent，仓储 flush 发布 |
| 仓储接口 / 实现 | `domain/repository/` → `infrastructure/repository/domain/*Impl` |
| JPA PO / MyBatis Mapper | `infrastructure/persistent/persistence/` / `mapper/` |
| API 定义 | `api/rpc/` 或 `api/inner/` |
| REST 实现 | `interfaces/controller/{buyer,seller,manager,inner}/` |
| 防腐层适配 | `facade/` (acl/ + ClientProxy/ + assembler/) |
| 消息监听 / 定时任务 | `infrastructure/event/` / `infrastructure/job/` |

## WHY — 架构决策

### 分层依赖（不可逆）

```
api → interfaces → application → domain ← infrastructure
                        ↓
                    facade (ACL)
```

| 层 | 依赖规则 |
|----|---------|
| **domain** | 零外部依赖。不依赖 Spring，不依赖数据库，纯 Java |
| **application** | 只依赖 domain + facade 接口。不依赖 infrastructure |
| **infrastructure** | 依赖 domain（实现仓储）+ application（事件订阅） |
| **interfaces** | 只依赖 application。不含业务逻辑 |
| **api** | 纯 DTO + 接口，不依赖任何业务模块 |

### 关键决策

- **Controller 四端隔离**：buyer / seller / manager / inner，各端 API 完全独立
- **防腐层独立模块**：facade 是独立 Gradle Module，内含 ACL + ClientProxy
- **三 Repository 分层**：domain 接口 → DomainRepositoryImpl → ApplicationRepository → SuperRepository
- **多事件总线**：同时支持 Kafka / RocketMQ / Redis PubSub / Guava / GreenRobot 五种机制
- **领域事件驱动**：聚合根内 `registerEvent()`，仓储 `save()` 时自动 flush 发布
- **模型分离**：domain entity ≠ JPA PO，使用 MapStruct + Record Builder + Lombok

## HOW — 干活指南

### 命令（Windows — 用 `gradlew` 而非 `./gradlew`）

```powershell
# 编译 & 测试
gradlew build
gradlew test
gradlew :taotao-cloud-member-domain:test

# 启动 dev
gradlew :taotao-cloud-member-assembly:bootRun --args='--spring.profiles.active=dev'

# 代码质量（门禁：Checkstyle + SpotBugs + PMD + Spotless + OWASP）
gradlew checkstyleMain spotlessCheck pmdMain spotbugsMain

# 发布
gradlew publishToMavenLocal
```

### 核心约定（ALWAYS 遵循）

- **命名**：命令 `{动词}{名词}Command`，查询 `{名词}Query`，结果 `{名词}Result`
- **事务**：只开在 application 层（`@Transactional`），domain 层不涉及
- **跨聚合**：通过 ID 引用，非对象引用；通过领域事件通信
- **区分后缀**：值对象 `*Val`，持久化对象 `*PO`，数据对象 `*DO`，仓储实现 `*DomainRepositoryImpl`
- **模块化规则**：详见 `.claude/rules/architecture.md`

### NEVER 做这些（ANTI-PATTERNS）

- Controller 中写业务逻辑判断
- 聚合根中注入 Repository 或 Domain Service
- 值对象包含业务行为以外的逻辑或 setter
- Application Service 包含业务规则判断
- domain 层出现任何 Spring 注解或持久化操作
- Application Service 直接调用 Mapper/DAO
- 跨聚合直接操作其他聚合的数据表或内部状态

### 注意事项

| 主题 | 说明 |
|------|------|
| JDK 25 | 预览特性，`--enable-preview` + `--add-exports` |
| 环境 | dev / test / pre / pro 四种配置 |
| BOM | `taotao-cloud-dependencies:2026.10` 未开源，外部构建需私有仓库凭据 |
| 平台 | Windows PowerShell 5.1，所有命令用 `gradlew` |
| 详细规范 | 架构 → `rules/architecture.md`，聚合 → `rules/aggregate-design.md`，值对象 → `rules/value-object.md`，API → `rules/api-conventions.md`，代码风格 → `rules/code-style.md` |
