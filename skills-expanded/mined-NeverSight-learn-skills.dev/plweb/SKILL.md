---
name: plweb-skill
description: 物理实验室 AR（Physics-Lab-AR / 烧杯实验室）官方社区 API 调用技能。当用户需要与物理实验室社区平台physics-lab交互，或者开发plweb2遇到API相关信息获取时交互时，包括：登录账号（邮箱登录/匿名登录/Token 登录）、查询与获取实验作品、获取实验详情与摘要、获取衍生作品、发布/删除实验、发表/删除评论、获取评论列表、点赞/收藏作品、获取支持者列表、发送与获取站内信、获取通知消息、获取用户资料、关注/取关用户、获取粉丝/关注列表、获取社区首页/资料页/讨论区/实验区内容、获取头像与封面图、修改昵称与个人信息、领取活动奖励、封禁/解封用户（管理员）等。适用于自动化操作物理实验室社区、批量管理作品、数据采集、机器人（Bot）开发、社区互动自动化等场景。API 域名为 physics-api-cn.turtlesim.com（中国区），基于 HTTPS POST JSON 请求
---

# 物理实验室 AR 社区 API 调用技能

本技能封装了「物理实验室 AR」（Physics-Lab-AR，又称烧杯实验室 / Quantum Lab）社区平台的完整 HTTP API 调用方法。该平台是一个在线物理实验模拟与分享社区，用户可以在其中创建电学/天体物理实验并发布到社区分享。

## 一、API 概览

### 基础信息

| 项目 | 值 |
|------|-----|
| 协议 | HTTPS（端口 443） |
| 中国区域名 | `physics-api-cn.turtlesim.com` |
| 请求方法 | 绝大多数为 `POST`，少数为 `GET` |
| 请求体格式 | JSON（`Content-Type: application/json`） |
| 响应体格式 | JSON |
| 字符编码 | UTF-8 |
| 响应可能启用 | gzip 压缩 |

### 响应统一结构

所有接口返回统一的 JSON 结构：

```json
{
  "Status": 200,
  "Message": "",
  "Data": { ... }
}
```

- `Status`：HTTP 风格状态码，`200` 表示成功，其他值表示失败
- `Message`：成功时为空字符串；失败时为错误标识符（如 `"Login.Password.Invalid"`、`"Input.Field.Missing"`）
- `Data`：成功时为数据对象或数组；失败时通常为 `null`

**常见错误 Message：**
- `Login.Password.Invalid` — 邮箱或密码错误
- `Input.Field.Missing` — 请求体缺少必填字段
- `Content.Not.Exists` — 内容不存在
- `Permission.Denied` — 权限不足

> **注意**：列表类接口返回的 `Data` 通常带有 `$type` 和 `$values` 字段，实际数据在 `Data["$values"]` 数组中。

### 身份认证

登录成功后，响应体会返回 `Token` 和 `AuthCode` 两个字段（位于顶层，不在 `Data` 内）。后续所有需要认证的接口都需在请求头中携带：

```
x-API-Token: <Token>
x-API-AuthCode: <AuthCode>
```

匿名登录也会返回 `AuthCode`（`Token` 可能为 `null`），可用于访问部分公开接口。

## 二、登录认证

### 1. 邮箱登录（Users/Authenticate）

```http
POST /Users/Authenticate
Content-Type: application/json
```

**请求体：**
```json
{
  "Login": "user@example.com",
  "Password": "yourpassword",
  "Version": 2411,
  "Device": {
    "Identifier": "7db01528cf13e2199e141c402d79190e",
    "Language": "Chinese"
  }
}
```

**成功响应（Status 200）：**
```json
{
  "Status": 200,
  "Message": "",
  "Token": "xxxxxxxxxxxx",
  "AuthCode": "xxxxxxxxxxxx",
  "Data": {
    "User": {
      "ID": "5d0f4390ca68215906d1a0fd",
      "Nickname": "用户昵称",
      "Signature": "个性签名",
      "Gold": 350,
      "Diamond": 0,
      "Level": 1,
      "Experience": 0,
      "Avatar": 0,
      "AvatarRegion": 0,
      "Decoration": 0,
      "Verification": null,
      "IsBinded": true
    },
    "DeviceToken": "...",
    "Statistic": { ... }
  }
}
```

### 2. 匿名登录

将 `Login` 和 `Password` 设为 `null` 即可匿名登录，返回一个匿名用户身份，可访问公开内容。

### 3. Token 登录（免密续期）

在请求头中携带已有的 `x-API-Token` 和 `x-API-AuthCode`，同时请求体中 `Login`/`Password` 设为 `null`，即可刷新登录状态。

> **Version 字段**：对应物理实验室客户端版本号，格式为 `YYMM`（如 `2411` 表示 2024 年 11 月版本）。版本过旧可能导致登录被拒。

## 三、核心接口速查

### 用户相关（Users）

| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| 登录认证 | `Users/Authenticate` | POST | 邮箱/匿名/Token 登录 |
| 获取用户 | `Users/GetUser` | POST | 按用户名或 ID 查询用户资料 |
| 关注用户 | `Users/Follow` | POST | 关注/取关指定用户 |
| 修改昵称 | `Users/Rename` | POST | 修改当前用户昵称 |
| 修改信息 | `Users/ModifyInformation` | POST | 修改个人签名等信息 |
| 领取奖励 | `Users/ReceiveBonus` | POST | 领取活动奖励 |
| 封禁用户 | `Users/Ban` | POST | 管理员封禁用户 |
| 解封用户 | `Users/Unban` | POST | 管理员解封用户 |
| 获取关系 | `Users/GetRelations` | POST | 获取粉丝/关注列表 |

### 内容相关（Contents）

| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| 查询实验 | `Contents/QueryExperiments` | POST | 按条件搜索实验/讨论 |
| 获取实验 | `Contents/GetExperiment` | POST | 获取实验完整内容 |
| 获取摘要 | `Contents/GetSummary` | POST | 获取实验摘要信息 |
| 获取衍生 | `Contents/GetDerivatives` | POST | 获取改编/衍生作品 |
| 获取支持者 | `Contents/GetSupporters` | POST | 获取点赞/支持者列表 |
| 点赞内容 | `Contents/Star` | POST | 点赞/取消点赞。支持作品也在此 |
| 获取评论 | `Contents/GetComments` | POST | 获取内容评论列表 |
| 发表评论 | `Contents/PostComment` | POST | 发表评论/回复 |
| 删除评论 | `Contents/RemoveComment` | POST | 删除指定评论 |
| 确认发布 | `Contents/ConfirmExperiment` | POST | 确认实验发布（底层） |
| 删除实验 | `Contents/RemoveExperiment` | POST | 删除已发布实验 |
| 上传图片 | `Contents/UploadImage` | POST | 上传实验封面/图片 |
| 获取资料页 | `Contents/GetProfile` | POST | 获取用户主页内容 |
| 获取社区库 | `Contents/GetLibrary` | POST | 获取首页/讨论区/实验区 |

### 消息相关（Messages）

| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| 获取消息列表 | `Messages/GetMessages` | POST | 获取站内通知列表 |
| 获取单条消息 | `Messages/GetMessage` | POST | 获取指定消息详情 |

### 公开接口（无需认证）

| 接口 | 路径 | 方法 | 说明 |
|------|------|------|------|
| 社区首页 | `Users` | GET | 获取首页导航数据 |
| 获取头像/封面 | `https://<domain>/Avatars/...` | GET | 获取用户头像或实验封面图 |

## 四、枚举值参考

### Category（内容分类）
- `"Experiment"` — 实验区
- `"Discussion"` — 讨论区（黑洞）

### Tag（社区标签）
**实验区标签：** `知识库`、`精选`、`小学`、`初中`、`高中`、`大学`、`专科`、`娱乐实验`、`小作品`、`教学实验`、`禁止改编`、`精选申请`

**讨论区标签：** `BUG`、`交流`、`小说专区`、`聊天`、`问与答`

**历史标签：** `逻辑电路`、`直流电路`、`交流电路`、`电子电路`、`兴趣`

### Sort（排序方式，QueryExperiments 用）
- `0` — 最新
- `1` — 最热（热门）

### MessageCategoryID（消息分类）
- `0` — 全部
- `1` — 系统邮件
- `2` — 关注与粉丝
- `3` — 评论与回复
- `4` — 作品通知
- `5` — 管理记录

### DisplayType（关系类型，GetRelations 用）
- `"Follower"` — 粉丝
- `"Following"` — 关注

## 五、调用示例

```bash
# 登录
curl -k -X POST "https://physics-api-cn.turtlesim.com/Users/Authenticate" \
  -H "Content-Type: application/json" \
  -d '{"Login":"user@example.com","Password":"password","Version":2411,"Device":{"Identifier":"7db01528cf13e2199e141c402d79190e","Language":"Chinese"}}'

# 查询实验（需替换 TOKEN 和 AUTHCODE）
curl -k -X POST "https://physics-api-cn.turtlesim.com/Contents/QueryExperiments" \
  -H "Content-Type: application/json" \
  -H "x-API-Token: TOKEN" \
  -H "x-API-AuthCode: AUTHCODE" \
  -d '{"Query":{"Category":"Experiment","Languages":[],"ExcludeLanguages":[],"Tags":null,"ExcludeTags":null,"ModelTags":null,"ModelID":null,"ParentID":null,"UserID":null,"Special":null,"From":null,"Skip":0,"Take":10,"Days":0,"Sort":0,"ShowAnnouncement":false}}'
```

## 六、详细接口文档

各接口的完整请求/响应字段说明请参阅 `docs/` 目录下的详细文档：

- [`docs/authentication.md`](docs/authentication.md) — 登录认证详解
- [`docs/users.md`](docs/users.md) — 用户接口详解
- [`docs/content.md`](docs/content.md) — 内容/实验接口详解
- [`docs/messages.md`](docs/messages.md) — 消息接口详解
- [`docs/comments.md`](docs/comments.md) — 评论接口详解
- [`docs/market.md`](docs/market.md) — 社区/资料页接口详解
- [`docs/enums.md`](docs/enums.md) — 枚举值完整参考
- [`docs/examples.md`](docs/examples.md) — 完整代码示例（Python / Node.js / curl）

## 七、注意事项

1. **域名选择**：中国区使用 `physics-api-cn.turtlesim.com`，国际区可能使用不同域名，请根据用户所在区域选择。
2. **HTTPS 证书**：由于域名与证书可能不匹配，请求时需关闭 SSL 证书验证（Python 中使用 `ssl._create_unverified_context()`，curl 中使用 `-k`）。
3. **Token 有效期**：Token 有有效期，过期后需重新登录或使用 Token 登录刷新。
4. **频率限制**：API 可能有频率限制，批量操作时建议适当间隔请求。
5. **Version 字段**：登录时的 `Version` 字段需与当前客户端版本匹配，过旧版本可能被拒绝登录。
6. **列表数据**：列表类接口返回数据在 `Data["$values"]` 数组中，注意解析时取该字段。
7. **管理员接口**：`Ban`、`Unban` 等接口需要管理员权限，普通用户调用会返回权限错误。
8. **实验内容格式**：实验内容（`GetExperiment` 返回的 `Data`）为序列化的电路/天体物理模型 JSON，结构复杂，修改时需保留原有结构。
