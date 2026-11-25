---
name: erwa-api
description: 二娃聚合群 API — 聚合 38+ 飞书群组，提供群聊AI总结、CA合约追踪、KOL观点、市场快讯的 Web3 数据服务
---

# 二娃聚合群 API

聚合 38+ 飞书群组，提供群聊AI总结、CA合约追踪、KOL观点、市场快讯的 Web3 数据服务。

---

## 安装

```bash
npx skills add hengxuZ/erwaAPI
```

---

## 认证

所有接口使用 Bearer Token 认证：

```
Authorization: Bearer <your-token>
```

获取 Token：联系管理员微信 **erwaNFT**

**Base URL**: `http://88.222.241.169`

---

## 接口总览

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| CA追踪 | `/api/v1/group_ca/by-ca/{ca}` | GET | 根据CA查群组来源 |
| CA追踪 | `/api/v1/group_ca` | GET | CA列表（支持多维筛选） |
| CA追踪 | `/api/v1/group_ca/popular` | GET | 热门CA统计 |
| CA追踪 | `/api/v1/group_ca/latest` | GET | 最新CA记录 |
| CA追踪 | `/api/v1/group_ca/by-username/{name}` | GET | 按用户名查CA |
| 群聊总结 | `/api/v1/summaries` | GET | AI群聊总结 |
| 群聊总结 | `/api/v1/summaries/narratives` | GET | 每日热门叙事 |
| KOL观点 | `/api/v1/second_kol` | GET | 二级KOL输出数据 |
| KOL观点 | `/api/v1/second_kol/latest` | GET | 最新KOL数据 |
| KOL观点 | `/api/v1/second_kol/kol/{name}` | GET | 指定KOL数据 |
| KOL观点 | `/api/v1/second_kol/kol_names` | GET | KOL名称列表 |
| 快讯 | `/api/v1/newsflash/today` | GET | 今日快讯 |
| 快讯 | `/api/v1/newsflash/date/{date}` | GET | 指定日期快讯 |
| 快讯 | `/api/v1/newsflash/latest` | GET | 最新快讯 |
| 系统 | `/api/v1/token/usage` | GET | Token使用次数 |
| WebSocket | `/ws/new_ca` | WS | 全局新CA实时推送 |
| WebSocket | `/ws/group_ca` | WS | 群组/用户/CA订阅 |
| WebSocket | `/ws/popular_ca` | WS | 热门CA实时排行 |

---

## 核心接口详情

### 1. 根据CA查群组

输入CA地址，返回所有发过该CA的群组列表。

**Endpoint**: `GET /api/v1/group_ca/by-ca/{ca_address}`

```bash
curl "http://88.222.241.169/api/v1/group_ca/by-ca/7m3HtU4RDiXWpAt546HHC7Lho3Qzvz6tx2MiAmLiHpLn" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
{
  "ca": "7m3HtU4RDiXWpAt546HHC7Lho3Qzvz6tx2MiAmLiHpLn",
  "total_groups": 3,
  "groups": ["crazySen聊天", "孙哥聊天", "测试群组"]
}
```

---

### 2. CA列表

**Endpoint**: `GET /api/v1/group_ca`

**Query Parameters**:
- `ca` (string): CA地址模糊搜索
- `http` (string): HTTP链接模糊搜索
- `username` (string): 用户名筛选
- `group_name` (string): 群组名称筛选
- `limit` (int): 返回数量，默认20，最大1000
- `skip` (int): 跳过记录数
- `date` (date): 按日期筛选 (YYYY-MM-DD)
- `only_http` (bool): 仅返回HTTP链接

```bash
# 按CA搜索
curl "http://88.222.241.169/api/v1/group_ca?ca=0x6106c7d9&limit=10" \
  -H "Authorization: Bearer <token>"

# 按用户名搜索
curl "http://88.222.241.169/api/v1/group_ca?username=白菜&limit=10" \
  -H "Authorization: Bearer <token>"

# 按群组搜索
curl "http://88.222.241.169/api/v1/group_ca?group_name=区块日记&limit=10" \
  -H "Authorization: Bearer <token>"

# 仅返回今天的HTTP链接
curl "http://88.222.241.169/api/v1/group_ca?only_http=true&limit=10" \
  -H "Authorization: Bearer <token>"
```

**Response** (每条记录字段):
```json
{
  "id": 78146,
  "ca": "0x6106c7d92308bbe4204667a59f9b570288954444",
  "username": "白菜",
  "group_name": "区块日记群",
  "create_time": "2026-03-13T11:34:24",
  "http": null,
  "symbol": "代币符号",
  "chain": "bsc",
  "token_name": "代币名字",
  "market_cap": "6.4K",
  "age": 7,
  "total_mentions": 5,
  "twitter": "https://twitter.com/token123",
  "telegram": "https://t.me/token123",
  "website": "https://token123.io",
  "summary": "这是一个meme代币，社区活跃...",
  "m5_buys": 10,
  "h1_buys": 50,
  "h6_buys": 200,
  "h24_buys": 500,
  "mc_change": {
    "first_mc": "2.1K",
    "current_mc": "6.4K",
    "change_pct": 204.76
  }
}
```

**字段说明**:
- `market_cap`: 市值（>=1000用K，>=1000K用M，>=1000M用B）
- `age`: 代币从创建到被提及的时间（分钟）
- `total_mentions`: 48h内提及次数
- `mc_change`: 首次提及 vs 当前市值变化（仅 total_mentions>1 时返回）
- `chain`: 公链（bsc/sol/base/eth）

**展示建议**: 按 `total_mentions` 排序，询问"今日金狗"按 `mc_change.change_pct` 排序

---

### 3. 热门CA统计

**Endpoint**: `GET /api/v1/group_ca/popular`

**Query Parameters**:
- `date` (date): 统计日期，默认当天
- `min_count` (int): 最小提及次数阈值，默认10
- `group_name` (string): 群组名称筛选
- `limit` (int): 返回数量，默认100
- `skip` (int): 跳过记录数

```bash
# 默认当天（>=10次）
curl "http://88.222.241.169/api/v1/group_ca/popular" \
  -H "Authorization: Bearer <token>"

# 昨日
curl "http://88.222.241.169/api/v1/group_ca/popular?date=$(date -v-1d +%F)" \
  -H "Authorization: Bearer <token>"

# 自定义阈值
curl "http://88.222.241.169/api/v1/group_ca/popular?min_count=20" \
  -H "Authorization: Bearer <token>"
```

---

### 4. 最新CA记录

**Endpoint**: `GET /api/v1/group_ca/latest`

**Query Parameters**:
- `limit` (int): 返回数量，默认1，最大100

```bash
curl "http://88.222.241.169/api/v1/group_ca/latest?limit=20" \
  -H "Authorization: Bearer <token>"
```

只返回 `ca` 不为 null 且 `http` 为 null 的记录。

---

### 5. 按用户名查CA

**Endpoint**: `GET /api/v1/group_ca/by-username/{username}`

```bash
curl "http://88.222.241.169/api/v1/group_ca/by-username/白菜" \
  -H "Authorization: Bearer <token>"
```

最多返回50条。

---

### 6. AI群聊总结

**Endpoint**: `GET /api/v1/summaries`

**Query Parameters**:
- `group_name` (string): 群组名称（模糊匹配）
- `date` (date): 日期，默认今天
- `hour` (int): 指定小时 (0-23)
- `start_date` / `end_date` (datetime): 时间范围
- `limit` (int): 返回数量，默认100

```bash
# 今天所有群组总结
curl "http://88.222.241.169/api/v1/summaries" \
  -H "Authorization: Bearer <token>"

# 指定群组+日期
curl "http://88.222.241.169/api/v1/summaries?group_name=crazySen群&date=2026-03-07" \
  -H "Authorization: Bearer <token>"
```

**群组分类参考**:

| 类型 | 群组 |
|------|------|
| Meme/土狗 | cryptoD、0xSun、GDC、James、金蛙、985、镭射猫、crazySen、0xAA、AD、区块日记 |
| 空投 | leng、P总、小鑫、十一地主、十一空投、3D群 |
| 打新 | 中国万岁、AKAKAY、Meta |

---

### 7. 每日热门叙事

**Endpoint**: `GET /api/v1/summaries/narratives`

```bash
curl "http://88.222.241.169/api/v1/summaries/narratives" \
  -H "Authorization: Bearer <token>"

curl "http://88.222.241.169/api/v1/summaries/narratives?date=2026-03-06" \
  -H "Authorization: Bearer <token>"
```

返回提及次数最多的前10条CA的 `summary`（代币叙事）字段。

---

### 8. 二级KOL数据

**Endpoint**: `GET /api/v1/second_kol`

**Query Parameters**:
- `kol_name` (string): KOL名称
- `token` (string): Token筛选
- `start_date` / `end_date` (date): 时间范围
- `limit` (int): 返回数量，默认50
- `skip` (int): 跳过数量

```bash
# 最新KOL数据（自动过滤屏蔽词）
curl "http://88.222.241.169/api/v1/second_kol" \
  -H "Authorization: Bearer <token>"

# 按KOL名称查询
curl "http://88.222.241.169/api/v1/second_kol?kol_name=KOL张三" \
  -H "Authorization: Bearer <token>"

# 按token查询
curl "http://88.222.241.169/api/v1/second_kol?token=ABC123" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
[
  {
    "kol_name": "KOL张三",
    "content": "这是一个关于某代币的分析...",
    "token": "ABC123",
    "image_urls": ["https://example.com/img1.png"],
    "sent_at": "2026-03-08T15:30:00"
  }
]
```

**其他KOL接口**:
- `GET /api/v1/second_kol/latest?limit=20` — 最新KOL数据
- `GET /api/v1/second_kol/kol/{kol_name}` — 指定KOL数据
- `GET /api/v1/second_kol/kol_names` — 所有KOL名称列表

> 自动过滤包含屏蔽词（如 bitget）的内容，@everyone 不是代币 ONE

---

### 9. 快讯

| 接口 | 说明 |
|------|------|
| `GET /api/v1/newsflash/today` | 今日快讯 |
| `GET /api/v1/newsflash/date/{date}` | 指定日期快讯 |
| `GET /api/v1/newsflash/latest` | 最新快讯 |

```bash
curl "http://88.222.241.169/api/v1/newsflash/today?limit=20" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
[
  {
    "add_time": 1741252800,
    "title": "比特币突破新高",
    "content": "比特币价格突破10万美元大关...",
    "url": "https://example.com/news/12345"
  }
]
```

---

### 10. Token使用次数

**Endpoint**: `GET /api/v1/token/usage`

```bash
curl "http://88.222.241.169/api/v1/token/usage" \
  -H "Authorization: Bearer <token>"
```

```json
{
  "token": "aaa3b7ad****b1c",
  "token_name": "API Token 500次/年",
  "daily_limit": 500,
  "used_today": 45,
  "remaining_today": 455,
  "reset_time": "2026-03-09 00:00:00"
}
```

---

## WebSocket 实时推送

**Base URL**: `ws://88.222.241.169`

连接时通过 URL 参数传递 Token：`ws://88.222.241.169/ws/new_ca?token=YOUR_TOKEN`

### WS 1. 全局新CA推送

**Endpoint**: `ws://88.222.241.169/ws/new_ca`

连接即开始接收所有新CA，无需订阅。每5秒检查数据库。

```javascript
const ws = new WebSocket('ws://88.222.241.169/ws/new_ca?token=YOUR_TOKEN');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'new_ca') {
    console.log('新CA:', data.data.ca, '群组:', data.data.group_name);
  }
};

// 心跳
setInterval(() => ws.send('ping'), 30000);
```

### WS 2. 群组/用户/CA订阅

**Endpoint**: `ws://88.222.241.169/ws/group_ca`

```javascript
const ws = new WebSocket('ws://88.222.241.169/ws/group_ca?token=YOUR_TOKEN');

ws.onopen = () => {
  // 订阅群组
  ws.send(JSON.stringify({ action: 'subscribe_group', group_name: '区块日记群' }));
  // 订阅用户
  ws.send(JSON.stringify({ action: 'subscribe_username', username: '白菜' }));
  // 订阅特定CA
  ws.send(JSON.stringify({ action: 'subscribe_ca', ca: '0x6106c7d9...' }));
};
```

**订阅动作**:
- `subscribe_group` — 订阅群组
- `subscribe_username` — 订阅用户
- `subscribe_ca` — 订阅特定CA
- `ping` — 心跳（建议每30秒）

### WS 3. 热门CA排行

**Endpoint**: `ws://88.222.241.169/ws/popular_ca`

每30秒自动推送热门CA排行：

```json
{
  "type": "popular_ca_update",
  "data": [
    {"ca": "0x123...", "count": 25, "rank": 1},
    {"ca": "0x456...", "count": 18, "rank": 2}
  ],
  "timestamp": "2026-03-30T10:30:00"
}
```

---

## 链上数据分析工具

以下为外部工具，无需 Token，直接访问。

| 工具 | URL | 用途 |
|------|-----|------|
| DexScreener | `https://dexscreener.com/search?q={CA}` | 市值、流动性、K线 |
| DexScreener API | `https://api.dexscreener.com/latest/dex/tokens/{CA}` | 交易对数据 |
| GMGN.ai | `https://r.jina.ai/http://gmgn.ai/{chain}/token/{CA}` | 安全审计、持仓分布 |
| Binance叙事 | `https://web3.binance.com/...?chainId={id}&contractAddress={CA}` | AI叙事分析 |
| X平台搜索 | `https://fapi.uk/api/base/apitools/search?words={CA}` | Twitter讨论热度 |

**Chain参数**: `sol` / `bsc` / `base` / `eth`

**Binance Chain ID**: solana=`CT_501`, bsc=`56`, base=`8453`

> 若外部网页被阻断，可在 URL 前加 `https://r.jina.ai/` 作为只读代理

---

## 错误处理

所有响应头包含 `X-Admin-Contact: wechat:erwaNFT`

| Code | 说明 |
|------|------|
| 401 | 缺少Token / Token无效 |
| 403 | Token已过期/被禁用 |
| 404 | 未找到记录 |
| 429 | 已达到每日调用限制 |

```json
{ "detail": "错误描述信息" }
```

---

## 数据表说明

### group_ca（约33万条，实时同步）
CA合约地址记录，包含代币信息、市值、买卖数据、市值变化等。

### ai_summary（约219条，每日更新）
飞书群组AI总结内容。

### send_kol
二级KOL发布消息，含内容、Token、图片链接。

### newsflash
快讯消息，含标题、内容、链接。

---

## 联系方式

微信：**erwaNFT**

API地址：http://88.222.241.169
