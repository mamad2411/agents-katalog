# Amazon Selling Partner API SDK for Go - Cursor Rules

## 项目概述
这是一个完整的 Amazon Selling Partner API (SP-API) Go SDK，提供类型安全、易于使用的 API 客户端。

## 代码风格和规范

### Go 语言规范
- 遵循 Go 官方代码规范 (gofmt, golint)
- 使用 Go 1.21+ 语法特性
- 包名使用小写，避免下划线
- 函数名使用驼峰命名法
- 常量使用大写字母和下划线
- 错误处理必须显式处理，不能忽略

### 项目结构
```
├── apis/           # API 客户端实现
│   ├── catalog/    # Catalog API
│   ├── feeds/      # Feeds API
│   ├── inventory/  # Inventory API
│   ├── listings/   # Listings API
│   ├── orders/     # Orders API
│   └── reports/    # Reports API
├── auth/           # 认证相关
├── client/         # 基础客户端
├── examples/       # 示例代码
│   ├── sandbox/    # 沙盒环境示例
│   └── production/ # 生产环境示例
└── vendor/         # 依赖包
```

### API 实现规范
- 每个 API 包必须包含 `*_api.go` 和 `types.go` 文件
- API 方法必须接受 `context.Context` 作为第一个参数
- 请求和响应结构体必须定义在 `types.go` 中
- 错误处理必须返回详细的错误信息
- 支持超时和重试机制

### 认证和配置
- 使用 LWA (Login with Amazon) 认证
- 支持环境变量配置
- 支持缓存机制
- 支持多区域配置

### 测试规范
- 每个 API 包都应该有对应的测试
- 测试分为沙盒环境和生产环境
- 使用 `t.Run()` 进行子测试
- 测试必须包含错误处理场景
- 环境变量配置测试

### 错误处理
- 定义自定义错误类型
- 提供详细的错误上下文
- 支持错误分类 (认证、验证、频率限制等)
- 包含重试建议

### 文档规范
- 所有导出的函数必须有注释
- 使用中文注释，便于理解
- 示例代码必须可运行
- README 包含完整的使用说明

## 开发指南

### 添加新的 API
1. 在 `apis/` 目录下创建新的包
2. 实现 `*_api.go` 和 `types.go`
3. 添加对应的测试
4. 更新 README 文档
5. 添加示例代码

### 环境配置
- 开发时使用 `.env.sbx` (沙盒环境)
- 生产测试使用 `.env.prod` (生产环境)
- 敏感信息不要提交到版本控制

### 依赖管理
- 使用 `go mod` 管理依赖
- 定期更新依赖版本
- 提交 `go.mod` 和 `go.sum` 文件
- vendor 目录包含在版本控制中

### 发布流程
1. 确保所有测试通过
2. 更新版本号和更新日志
3. 注释掉 go.mod 中的 replace 指令
4. 创建 git tag
5. 推送到 GitHub

## 注意事项

### 安全
- 不要硬编码 API 密钥
- 使用环境变量管理敏感信息
- 定期轮换认证凭据

### 性能
- 实现请求缓存机制
- 支持连接池
- 处理频率限制

### 兼容性
- 保持向后兼容性
- 版本号遵循语义化版本控制
- 废弃的功能要提供迁移指南

## 常用命令

```bash
# 运行所有测试
go test ./...

# 运行特定测试
go test ./examples/sandbox/...

# 格式化代码
go fmt ./...

# 检查代码规范
golint ./...

# 更新依赖
go mod tidy

# 构建项目
go build ./...
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 编写测试
4. 更新文档
5. 提交 Pull Request

## 联系信息

- 项目主页: https://github.com/kenee/amazon-sp-api-sdk-go
- 问题反馈: https://github.com/kenee/amazon-sp-api-sdk-go/issues
- 文档: README.md 