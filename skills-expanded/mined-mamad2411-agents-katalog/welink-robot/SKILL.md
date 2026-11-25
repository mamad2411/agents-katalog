---
name: welink-robot
description: 华为 WeLink 机器人消息发送工具，支持发送文本消息、@指定用户、@所有人。用于快速发送通知、集成到 CI/CD 流程、或在代码中调用 API。
---

# WeLink Robot

Quick start

```bash
cd scripts && go run . -msg="Hello World"
```

## CLI 使用

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| WE_LINK_TOKEN | Webhook Token | 4831fb96239747d7988ac94e93889eda |
| WE_LINK_CHANNEL | Channel 类型 | standard |

### 命令行参数

```bash
welink -msg="消息内容" [-at="user1,user2"] [-all]
```

- `-msg`: 必须，发送的消息内容
- `-at`: 可选，需要 @ 的用户 ID，多个用逗号分隔
- `-all`: 可选，是否 @ 所有人

## 开发指南

```
welink-robot/
├── SKILL.md           # Skill 说明
└── scripts/          # Go 项目代码
    ├── main.go       # 入口
    ├── config/      # 配置
    ├── client/     # 客户端
    └── go.mod     # 依赖
```

### 项目结构（scripts 目录）

```
scripts/
├── main.go           # 入口，命令行解析
├── config/config.go  # 配置加载 (环境变量)
└── client/client.go  # API 客户端，Message 定义
```

### 代码解读

**config/config.go**
- `Config` 结构体：Token 和 Channel 字段
- `Load()` 函数：从环境变量加载配置，支持默认值

**client/client.go**
- `Message` 结构体：消息内容，包含 MessageType、Content、TimeStamp、Uuid、IsAt、IsAtAll、AtAccounts
- `NewMessage(text, ...Option)`：创建消息，支持函数式选项
- `Option` 类型：函数式选项模式
- `WithAtUsers([]string)`：@指定用户
- `WithAtAll()`：@所有人
- `Client` 结构体：HTTP 客户端，封装 token 和 channel
- `Send(*Message) error`：发送消息到 WeLink API

### 扩展开发

添加新消息类型：
1. 在 `client/client.go` 添加新的 MessageType 常量
2. 添加新的 Content 结构体
3. 更新 Message 结构体
4. 添加新的 Option 函数（如 WithImage、WithLink 等）

示例：
```go
// 添加图片消息类型
const MessageTypeImage MessageType = "image"

type ImageContent struct {
    ImageURL string `json:"imageUrl,omitempty"`
}

func WithImage(url string) Option {
    return func(m *Message) {
        m.MessageType = string(MessageTypeImage)
        // 处理图片内容
    }
}
```

### 测试

```bash
# 运行所有测试
go test ./...

# 运行特定包测试
go test ./config
go test ./client

# 详细输出
go test -v ./...
```