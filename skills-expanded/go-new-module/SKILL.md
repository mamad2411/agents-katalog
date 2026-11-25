---
name: go-new-module
description: 在 Go 后端项目中按分层结构新增一个业务模块（apivo、api、service、repository、model、entity、dto），并接入路由与注册器。用户说「新增模块」「新建业务模块」「加一个 CRUD 资源」「scaffold module」，或要为新的业务实体建立完整的接口到存储链路时使用。只修改单个已有文件或单层代码时不使用。
---

# 新增 Go 业务模块

按项目已有的分层新建一个模块，依赖只向内：`api / command → service → repository → model`。

## 1. 先确认

动手前确认以下信息，项目中能查到的直接查，查不到再问用户：

- 模块名与业务实体（例如 `order-module`、`Order`）
- 存储：MongoDB、MySQL 或 PostgreSQL；是否需要 Redis 缓存
- 传输层：哪个 HTTP 内核（看 `BootConfig.CoreType` 或 `go.mod`），是否需要 CLI 命令或异步任务
- 接口清单：路由、请求与响应字段、分页与过滤条件

## 2. 参照已有模块

先找一个结构最接近的已有模块作为样板，读它的每一层和注册方式，照同样的命名、文件划分与装配方式写。项目中还没有模块时，以 FiberHouse 的 `example_application/module/example-module/` 为样板（MongoDB），MySQL 参照 `command-module/`。

## 3. 依序建立

| 顺序 | 位置 | 内容 |
|---|---|---|
| 1 | `apivo/<模块>/requestvo/`、`responsevo/` | 请求与响应结构，含校验 tag；先写契约 |
| 2 | `module/<模块>/entity/` | 持久化结构与状态等类型 |
| 3 | `module/<模块>/model/` | 集合或表的访问代码与索引定义 |
| 4 | `module/<模块>/repository/` | 存取接口与实现；把驱动错误转换为领域错误；不接收 `apivo` 类型 |
| 5 | `module/<模块>/cache/`（需要 Redis 时） | 本模块直接 Redis 命令用到的 key 与操作，对外提供有类型的方法；对象整体缓存用通用组件的旁路读取。先读 `/cache-design` 的 `references/layered-examples.md` |
| 6 | `module/<模块>/dto/` | service 的入参与返回结构（需要隔离存储类型，或项目已按 `rules/go/layering.md`「契约类型」升为严格时） |
| 7 | `module/<模块>/service/` | 业务用例，依赖 repository 接口与本模块 `cache/`；入参与返回默认直接用 `apivo` 类型；只接收 `context.Context`，不 import `go-redis` |
| 8 | `module/<模块>/api/` | handler、路由注册、依赖装配；需要 VO 与 DTO 转换时在这里完成 |
| 9 | 注册器 / Provider | 在模块注册器、路由注册 Provider 中接入新模块 |

需要异步任务时在 `module/<模块>/task/` 定义任务名与 handler；领域错误加入集中的错误映射。

## 4. 测试与验证

- service 用表驱动单元测试，repository 以接口替换；依赖真实存储的集成测试用环境变量开启。
- 依赖装配使用 wire 等生成工具时，修改 provider 后运行项目的生成脚本，不手改生成文件。
- 依次运行 `go build ./...`、`go vet ./...`、`go test ./<模块路径>/...`，全部通过后再汇报，并列出新增的路由与文件。
- 项目使用 golangci-lint 且尚未限制 `go-redis`、`apivo` 的使用位置时，把 `references/depguard.yml` 的规则合并进项目的 `.golangci.yml`（`<module>` 换成 `go.mod` 的 module 路径，先向用户说明），再运行 `golangci-lint run ./...`。
