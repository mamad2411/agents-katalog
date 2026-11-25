---
name: rpc-design
description: 为 Go 后端设计或评审 gRPC 接口：proto 契约、调用模式（unary / 流）、错误码、deadline 与重试、兼容性检查，并按分层实现与测试。用户说「加 gRPC 接口」「新增 RPC 方法」「设计 proto」「改 proto 字段」「服务间调用」「gRPC 报错／超时／负载不均」时使用。只修改已有 handler 内部的业务逻辑、不涉及契约与调用配置时不使用。
---

# gRPC 接口设计

逐条规则在 `.claude/rules/rpc/proto.md` 与 `.claude/rules/rpc/grpc-go.md`，编辑对应文件时自动加载。兼容性实测见 `references/proto.md`，服务端／客户端／测试模板与实测依据见 `references/grpc-go.md`。

## 1. 确认用不用 gRPC

| 调用方 | 选择 |
|---|---|
| 内部服务之间、需要强类型契约或流 | gRPC |
| 浏览器或第三方直接调用 | HTTP/JSON，由 FiberHouse HTTP handler 调用同一 service；不引入 grpc-gateway、Connect 等转码层（项目已有时沿用） |
| 只有一个调用方、调用量小 | 沿用项目现有方式，不为此引入 gRPC |

项目已有 RPC 方案时沿用；引入 gRPC 或网关属于选型，写 ADR。

## 2. 选调用模式

默认 unary。只有以下情况考虑流，并在设计中写明代价：

| 信号 | 模式 |
|---|---|
| 数据陆续产生（订阅、进度、日志跟随）或结果集过大不宜一次返回 | server streaming |
| 客户端分批上传、服务端最后汇总 | client streaming |
| 长连接双向通道（指令下发与回执） | bidi streaming |

流的代价：一条流固定在一个后端实例（扩容后不会自动分流）；中断后要重建并处理已消费部分，不能像 unary 一样直接重试；每条活跃流占用服务端 goroutine 与缓冲；`GracefulStop` 会一直等流结束。分页能解决的大结果集优先用分页 unary。

## 3. 写契约

逐项写进设计文档（`docs/design/<模块>-rpc.md`）或 proto 注释：

| 项目 | 要回答的问题 |
|---|---|
| 命名 | package、服务、方法、Request / Response 是否符合 `rules/rpc/proto.md` |
| 字段 | 哪些标量需要区分「未设置」（`optional`）；更新接口是否用 `FieldMask`；时间与金额类型 |
| 错误 | 每个方法可能返回的 code 及触发条件；哪些带 details |
| 幂等 | 写方法能否安全重试；不能时用什么去重（`idempotency_key` + 唯一约束） |
| 时间预算 | 调用方 deadline 多少；本方法再调哪些下游，各占多少 |
| 重试 | 哪些方法配 `retryPolicy`（只限幂等），可重试的 code |
| 大小 | 请求与响应的最大体积；超过 4MiB 的改为分页、流或对象存储引用；文本类大响应可按方法开 gzip（`grpc.UseCompressor`），已压缩的数据不开 |

## 4. 兼容性检查

改已有 proto 前对照 `references/proto.md` 的兼容性表；项目有 `buf.yaml` 时运行 `buf lint` 与 `buf breaking`。新项目 `buf.yaml` 的 breaking 用 `FILE`（buf 默认）：淘汰字段标 `[deprecated = true]` 保留，不删除；破坏性变更走新版本 package，与旧版本并存到调用方全部迁移。

## 5. 实现

1. 生成代码（项目的 `buf generate` / `make proto`）。
2. 传输层 handler：pb ↔ dto 转换、调用 service、按错误映射表返回 status（模板见 `references/grpc-go.md`）。
3. service、repository 按 `rules/go/layering.md` 实现，不感知 gRPC。
4. 服务端装配：recovery 拦截器在最前、健康检查、keepalive 策略、优雅关闭。
5. 调用方：复用 `ClientConn`、service config（负载均衡、超时、重试）、转发需要的 metadata。

## 6. 测试

- 用 bufconn 起进程内服务端，覆盖：正常返回、每种业务错误的 code、参数缺失、deadline 到期。
- 流式方法覆盖：正常结束（`io.EOF`）、中途出错、客户端取消。

## 7. 自查清单

- [ ] 每个出站调用都有 deadline，handler 把收到的 `ctx` 传给下游
- [ ] handler 只返回 `status` 错误，`Internal` 不泄露内部错误文本
- [ ] 非幂等写方法没有配置自动重试，或有幂等键去重
- [ ] 删除的字段已 `reserved` 号与名，没有改已有字段的类型、名字或 `oneof` 归属
- [ ] 需要转发的 metadata（request id 等）已显式写入出站 context
- [ ] 长耗时处理与流的发送循环检查 `ctx.Done()`
- [ ] 新服务已注册健康检查，关闭流程有超时兜底
- [ ] 依赖 `round_robin` 的调用方使用 headless Service 或 L7 代理（运维面见 dev-ops 的 `middleware-ops`）
