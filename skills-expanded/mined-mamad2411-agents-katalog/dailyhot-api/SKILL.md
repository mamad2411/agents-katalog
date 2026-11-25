---
name: dailyhot-api
description: "全网热榜聚合 API 服务 — 基于 DailyHotApi 开源项目，本地自动部署，零配置获取 40+ 平台实时热搜数据。覆盖抖音、微博、知乎、B站、百度、今日头条、快手等主流平台。触发词：热点、热搜、趋势、热榜、trending、hot topics。"
version: "1.0.0"
license: MIT
author: tiktok-drama-trend-automator
requires:
  bins: [node, npm]
metadata:
  {
    "openclaw": {
      "emoji": "📡",
      "requires": {
        "bins": ["node", "npm"]
      },
      "installSpec": {
        "bins": ["node", "npm"]
      }
    }
  }
---

# 全网热榜聚合 API

**来源**：[imsyy/DailyHotApi](https://github.com/imsyy/DailyHotApi) · 本地自部署，零成本，零配置

本地运行的全网热榜聚合服务，覆盖 40+ 平台实时热搜数据。安装 agent 时自动部署，用户无需任何额外操作。

---

## 关键规则

- 调用前必须确保服务已启动（执行 `bash scripts/ensure_running.sh`）
- 所有 HTTP 请求添加超时：`-m 15`
- 请求失败不重试 — 报告错误并提示用户
- 默认端口：6688，可通过环境变量 `DAILYHOT_PORT` 修改

---

## 服务管理

### 确保服务运行（每次使用前调用）

```bash
bash scripts/ensure_running.sh
```

自动完成以下操作：
1. 检查 DailyHotApi 是否已安装，未安装则自动 `npm install`
2. 检查服务是否运行中，未运行则自动启动
3. 等待服务就绪并返回状态

### 停止服务

```bash
bash scripts/stop.sh
```

---

## 支持的平台（40+）

| 平台 | 接口路径 | 类别 |
|------|---------|------|
| 抖音 | `/douyin` | 热点榜 |
| 微博 | `/weibo` | 热搜榜 |
| 知乎 | `/zhihu` | 热榜 |
| B站 | `/bilibili` | 热门榜 |
| 百度 | `/baidu` | 热搜榜 |
| 今日头条 | `/toutiao` | 热榜 |
| 快手 | `/kuaishou` | 热点榜 |
| 豆瓣电影 | `/douban-movie` | 新片榜 |
| 百度贴吧 | `/tieba` | 热议榜 |
| 腾讯新闻 | `/qq-news` | 热点榜 |
| 新浪新闻 | `/sina-news` | 热点榜 |
| 网易新闻 | `/netease-news` | 热点榜 |
| 澎湃新闻 | `/thepaper` | 热榜 |
| 36氪 | `/36kr` | 热榜 |
| 虎嗅 | `/huxiu` | 24小时 |
| IT之家 | `/ithome` | 热榜 |
| 少数派 | `/sspai` | 热榜 |
| 稀土掘金 | `/juejin` | 热榜 |

---

## 数据获取

### 获取单平台热榜

```bash
curl -s -m 15 "http://localhost:6688/douyin"
```

### 返回格式

```json
{
  "code": 200,
  "name": "douyin",
  "title": "抖音",
  "type": "热点榜",
  "total": 50,
  "updateTime": "2026-03-31T08:09:47.743Z",
  "data": [
    {
      "id": "2449453",
      "title": "热点标题",
      "hot": 12115951,
      "url": "https://www.douyin.com/hot/2449453"
    }
  ]
}
```

### 批量获取多平台热榜（推荐用于趋势收集）

```bash
# 在脚本中批量调用
python3 scripts/collect_trends.py --platforms douyin weibo toutiao zhihu bilibili baidu
```

---

## 趋势收集工作流

本 skill 在流水线中的位置：**阶段 1 — 趋势收集**

```
确保服务运行 → 批量请求多平台热榜 → 汇总并格式化 → 输出到阶段 2
```

### 采集策略

每次采集从以下平台拉取数据（可在 config.json 中自定义）：
- **短视频平台**：抖音、快手、B站
- **社交媒体**：微博、知乎、百度贴吧
- **新闻资讯**：今日头条、百度、腾讯新闻、澎湃新闻
- **科技财经**：36氪、虎嗅、IT之家

---

## 错误处理

| 情况 | 处理 |
|------|------|
| 服务未启动 | 自动执行 `ensure_running.sh` 启动 |
| 单平台请求失败 | 跳过该平台，继续采集其他平台 |
| 返回数据为空 | 记录警告，不影响整体流程 |
| 端口被占用 | 自动尝试 6689-6699 端口 |
