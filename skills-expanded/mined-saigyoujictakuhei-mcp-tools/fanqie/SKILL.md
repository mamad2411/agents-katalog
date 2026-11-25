---
name: FanQie (番茄小说)
description: 番茄小说 MCP 工具模块，支持书籍搜索、目录获取、内容解析、评论管理与设备池管理
---

# FanQie (番茄小说) 操作手册

## 功能概览
FanQie 模块提供番茄小说平台的完整工具集，支持：
- **书籍搜索**：搜索书籍/听书/漫画/短剧
- **书籍详情**：获取详细信息、完整目录、简化目录
- **内容获取**：章节内容、统一内容接口（支持多种类型）
- **评论管理**：获取评论列表（支持分页）
- **设备池管理**：设备池状态、设备注册、平台状态查询

## 注册工具（10 个）

### 搜索 (1 个)
- `fanqie_search_books` : 搜索番茄小说书籍/听书/漫画/短剧

### 书籍详情 (3 个)
- `fanqie_get_book_detail` : 获取指定书籍的详细信息
- `fanqie_get_book_directory` : 获取书籍的完整章节目录列表
- `fanqie_get_simple_directory` : 获取书籍的简化目录信息

### 内容获取 (2 个)
- `fanqie_get_chapter_content` : 获取指定章节的文本内容（简化接口）
- `fanqie_get_content` : 统一内容获取接口（支持小说/听书/短剧/漫画/批量）

### 评论与设备 (4 个)
- `fanqie_get_comments` : 获取书籍或内容的评论列表（支持分页）
- `fanqie_get_device_pool_status` : 查看设备池的整体状态
- `fanqie_register_device` : 注册新设备到设备池
- `fanqie_get_device_status` : 查看指定平台的设备状态

## API 端点
| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/search` | GET | 搜索接口 |
| `/api/detail` | GET | 详情接口 |
| `/api/book` | GET | 目录接口 |
| `/api/directory` | GET | 简化目录接口 |
| `/api/content` | GET | 内容接口 |
| `/api/chapter` | GET | 章节接口 |
| `/api/comment` | GET | 评论接口 |
| `/api/device/pool` | GET | 设备池状态 |
| `/api/device/register` | GET | 设备注册 |
| `/api/device/status` | GET | 设备状态 |

## 错误码说明
| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常返回 data 字段 |
| 400 | 请求参数错误 | 检查参数格式和必填项 |
| 403 | 未授权或授权已过期 | 刷新授权 token |
| 404 | 资源不存在 | 检查 ID 是否正确 |
| 500 | 服务器内部错误 | 重试或联系管理员 |

## 使用示例

### 搜索书籍
```json
{
  "key": "斗破苍穹",
  "tab_type": 3,
  "offset": 0
}
```

### 获取书籍详情
```json
{
  "book_id": "123456"
}
```

### 获取章节内容
```json
{
  "item_id": "chapter_001"
}
```
