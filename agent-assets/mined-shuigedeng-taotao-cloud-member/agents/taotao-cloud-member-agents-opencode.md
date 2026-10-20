# PROJECT KNOWLEDGE BASE

**Generated:** 2026-06-18
**Commit:** `56589ba`
**Platform:** Windows (PowerShell 5.1) / Gradle 9.5 / JDK 25 / Spring Boot 4.1.1

## OVERVIEW

会员领域 DDD 单体服务（taotao-cloud-member），基于 Spring Boot 4.1.1 / JDK 25 / Gradle 9.5 / Spring Cloud Alibaba。严格遵循六边形架构 + 领域驱动设计，作为 taotao-cloud 微服务体系的会员中心。

## STRUCTURE

```
taotao-cloud-member/            ← 8 个 Gradle 模块（六边形架构）
├── api/                        # RPC/gRPC 接口定义 + DTO/Request/Response（纯接口层）
│   ├── rpc/                    # Dubbo/gRPC 服务接口（如 MemberRpcService）
│   └── inner/                  # 内部 Feign API 接口（如 MemberApi, MemberAddressApi）
├── application/                # 应用层：编排、事务、DTO转换
│   ├── service/command/        # 命令服务接口 + 实现（写操作）
│   ├── service/query/          # 查询服务接口 + 实现（读操作）
│   ├── handler/pie/            # Pipeline 模式处理器（goods/category）
│   ├── repository/             # 查询仓储接口（读模型）
│   └── support/                # 业务支撑工具
├── assembly/                   # 启动器 + 环境配置（dev/test/pre/pro）
├── common/                     # 公共枚举、常量、工具类（无业务逻辑）
├── domain/                     # ★ 领域层（零外部依赖，纯业务）
│   ├── aggregate/              # 聚合根：MemberAgg, MemberWalletAgg, MemberNoticeAgg
│   ├── entity/                 # 实体：Member, MemberWallet, MemberNotice
│   ├── valobj/                 # 值对象：MemberVal, MemberWalletVal, MemberNoticeVal
│   ├── event/                  # 领域事件：MemberCreateEvent, MemberWalletCreateEvent, MemberNoticeCreateEvent
│   ├── repository/             # 仓储接口定义
│   ├── service/                # 领域服务接口 + 实现
│   └── assembler/              # 领域层 Assembler（领域内转换）
├── facade/                     # 防腐层（ACL）— 独立 Gradle Module
│   ├── acl/                    # 防腐适配实现（SysAclService, CreditAclService, ConnectAclService）
│   ├── sys/                    # 系统模块 Client Proxy（Dict, Dept）
│   ├── order/                  # 订单模块 Client Proxy（Order, Trade）
│   ├── credit/                 # 信用模块 Client Proxy
│   ├── connect/                # 第三方连接 Client Proxy
│   └── assembler/              # 防腐层 Assembler
├── infrastructure/             # 基础设施层：持久化、MQ、事件、缓存、任务
│   ├── persistent/persistence/ # JPA PO 持久化对象（~20个 PO）
│   ├── persistent/mapper/      # MyBatis-Plus Mapper
│   ├── persistent/repository/  # 超级仓储（SuperRepository）
│   ├── repository/domain/      # 领域仓储实现（*DomainRepositoryImpl）
│   ├── repository/application/ # 应用仓储实现
│   ├── data/dataobj/           # 数据对象 DO
│   ├── data/dataparam/         # 查询参数对象
│   ├── assembler/              # PO ←→ Domain Assembler
│   ├── factory/                # 领域工厂（MemberFactory）
│   ├── event/                  # 事件发布/订阅（Kafka, RocketMQ, Redis, Guava, GreenRobot）
│   ├── configuration/          # 基础设施配置（Redis, RocketMQ, AOP, Cache, Redisson）
│   └── job/                    # 定时任务（XXL-Job）
└── interfaces/                 # REST / RPC / gRPC 实现层
    ├── controller/buyer/       # 买家端 API（Member, Address, Evaluation, Browse, Sign, etc.）
    ├── controller/seller/      # 卖家端 API（MemberEvaluation, Bill, StoreUser）
    ├── controller/manager/     # 管理端 API（Member, Grade, Evaluation, Points, Address）
    ├── controller/inner/       # 内部 Feign 实现（Member, Address, Evaluation, Recharge, Wallet）
    ├── controller/buyer/connect/ # 第三方登录绑定（PC, MiniProgram, WebBind, ConnectBind）
    ├── rpc/                    # Dubbo RPC 实现（DictRpcService）
    └── grpc/                   # gRPC 实现（DictGrpcService）
```

## WHERE TO LOOK

| Task | Location |
|------|----------|
| 新增业务功能 | `application/service/command/` 定义接口 + `interfaces/controller/{role}/` |
| 修改领域模型 | `domain/aggregate/` 或 `domain/entity/` |
| 值对象 | `domain/valobj/` — 所有字段 final，无 setter |
| 领域事件 | `domain/event/` — 聚合内 registerEvent，仓储 flush |
| 仓储接口 | `domain/repository/` |
| 仓储实现 | `infrastructure/repository/domain/` |
| JPA PO 定义 | `infrastructure/persistent/persistence/` |
| MyBatis Mapper | `infrastructure/persistent/mapper/` |
| API 接口定义 | `api/rpc/` 或 `api/inner/` |
| REST 实现 | `interfaces/controller/{buyer,seller,manager,inner}/` |
| 外部接口适配 | `facade/`（防腐层，独立模块） |
| 消息监听 | `infrastructure/event/consumer/` 或 `infrastructure/event/subscribe/` |
| 定时任务 | `infrastructure/job/` |
| 基础设施配置 | `infrastructure/configuration/` |
| 启动入口 | `assembly/` |

## CONVENTIONS

- 分层依赖方向：`api → interfaces → application → domain ← infrastructure`，`facade` 被 `application` 引用
- 跨聚合通过 ID 引用，非对象引用
- 事务边界仅开在 `application/` 层
- Controller 按角色 buyer / seller / manager / inner 分包
- 命令/查询命名：`{动词}{名词}{Command|Query}`（如 `CreateMemberCommand`, `MemberPageQuery`）
- 领域模型与持久化模型分离（domain entity ≠ JPA PO）
- PO（持久化对象）以 `PO` 后缀命名，DO（数据对象）以 `DO` 后缀命名
- 基础设施层仓储实现以 `*DomainRepositoryImpl` 后缀命名

## ANTI-PATTERNS (THIS PROJECT)

- Controller 中写业务逻辑判断
- 聚合根中注入 Repository 或 Domain Service
- 值对象中包含业务行为以外的逻辑
- Application Service 中包含业务规则判断
- 跨聚合直接操作其他聚合的内部状态
- domain 层出现任何 Spring 注解或持久化操作
- Application Service 直接调用 Mapper/DAO

## UNIQUE STYLES

- **API/Interfaces 分离**：`api/` 模块只放接口定义和 DTO，`interfaces/` 模块放实现，区别于常规的单模块做法
- **Controller 四端分层**：buyer / seller / manager / inner 四个子包，各端 API 完全隔离
- **事件驱动仓储**：聚合根内 `registerEvent()`，仓储 `save()` 时自动 flush 发布
- **防腐层独立为模块**：`facade/` 作为独立 Gradle Module，而非 application 的子包，内设 ACL + ClientProxy
- **MapStruct + Record Builder + Lombok 三件套**：减少样板代码的同时保持不可变性
- **Pipeline 模式**：`application/handler/pie/` 使用责任链模式处理复杂业务流程
- **多事件总线**：同时支持 Kafka、RocketMQ、Redis Pub/Sub、Guava EventBus、GreenRobot 五种事件机制
- **三 Repository 分层**：domain 层定义接口，infrastructure 层有 Persistent Repository + Domain Repository Impl + Application Repository

## COMMANDS

```powershell
# 编译（Windows）
gradlew build

# 启动 dev 环境
gradlew :taotao-cloud-member-assembly:bootRun --args='--spring.profiles.active=dev'

# 代码质量检查
gradlew checkstyleMain spotlessCheck pmdMain spotbugsMain

# 运行测试
gradlew test

# 发布到本地 Maven
gradlew publishToMavenLocal
```

## NOTES

- **平台**：Windows（PowerShell 5.1），所有脚本中使用 `gradlew`（非 `./gradlew`）
- **JDK 25** 预览特性，`--enable-preview` + 大量 `--add-exports`
- `taotao-cloud-dependencies:2026.10` BOM 未开源，外部构建需要私有仓库凭据
- 四个环境配置：dev / test / pre / pro
- 代码质量门禁：Checkstyle + SpotBugs + PMD + Spotless + OWASP
- 主包路径：`com.taotao.cloud.member`（非 `order`）
- `.claude/` 目录为历史遗留，新配置以 `.opencode/` 为准
