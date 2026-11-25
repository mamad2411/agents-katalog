---
name: offerclaw
description: "面经爪 (OfferClaw) — 互联网大厂面试经验库 + RAG 智能问答。爬取牛客网/小红书真实面经，用 ChromaDB 建立向量索引，通过 OpenRouter LLM 生成结构化备考建议。Use when: (1) 搜索字节/阿里/腾讯等大厂某岗位面试题, (2) 爬取最新面经并入库, (3) 启动本地面经搜索服务, (4) 查询XXX公司YYY岗位面试怎么准备类问题。Triggers: 面经、面试题、备考、OfferClaw、offerclaw、面试准备."
---

# OfferClaw · 面经爪

面试经验库 + RAG 智能问答，覆盖牛客网双数据源，时效衰减重排。

## 目录结构

```
offerclaw/
├── backend/          FastAPI + ChromaDB + SQLite 后端
│   ├── main.py       API 主入口（端口 8000）
│   ├── config.py     环境变量配置
│   ├── crawler/      爬虫（nowcoder.py）
│   ├── db/           SQLite 存储层
│   └── rag/          ChromaDB 向量索引 + 查询
├── frontend/         Next.js 前端（端口 3000）
├── scripts/          工具脚本
│   └── sample_data.json   种子 URL（约 13 篇面经）
└── start.sh          一键启动脚本
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENROUTER_API_KEY` | 必填，用于 Embedding（text-embedding-3-small）和 LLM（qwen-turbo） |

## 快速启动

```bash
# 1. 安装后端依赖
cd backend && pip install -r requirements.txt

# 2. 安装前端依赖
cd frontend && npm install

# 3. 设置环境变量并启动后端（port 8000）
export OPENROUTER_API_KEY=sk-xxx
cd backend && uvicorn main:app --reload --port 8000

# 4. 启动前端（port 3000）
cd frontend && npm run dev
```

## 主要 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/posts?company=字节跳动&page_size=10` | 列出面经 |
| GET | `/companies` | 已入库公司列表 |
| POST | `/search` | RAG 语义搜索 + LLM 生成建议 |
| POST | `/crawl` | 异步爬取面经（nowcoder） |
| GET | `/tasks/{task_id}` | 查询爬取任务状态 |

### 搜索请求示例

```json
POST /search
{
  "company": "字节跳动",
  "job_title": "前端开发",
  "direction": "2024",
  "question": "会考哪些算法题？",
  "top_k": 5
}
```

### 爬取请求示例

```json
POST /crawl
{
  "company": "字节跳动",
  "job_title": "前端",
  "direction": "2024"
}
```

爬取完成后自动建立 ChromaDB 向量索引，下次 `/search` 即可命中。

## OpenClaw Agent 工作流

### 场景1：查询面经

1. 调用 `GET /posts?company=XXX` 查看已入库数量
2. 若数量 < 5，先 `POST /crawl` 补充数据（等任务 done）
3. `POST /search` 获取 RAG 结果和 LLM 建议
4. 将 `answer` 字段直接呈现给用户，附 `top_chunks` 来源链接

### 场景2：冷启动新公司/岗位

```bash
# 先爬取，再搜索
POST /crawl {"company":"阿里巴巴","job_title":"产品经理","direction":"2024"}
# 轮询任务直到 status=done
GET /tasks/{task_id}
# 然后搜索
POST /search {"company":"阿里巴巴","job_title":"产品经理","question":"核心考点是什么？"}
```

### 场景3：检查服务状态

```bash
curl http://localhost:8000/health
curl http://localhost:3000
```

## RAG 架构说明

- **Embedding**: `openai/text-embedding-3-small`（via OpenRouter）
- **向量库**: ChromaDB（本地持久化 `backend/chroma_db/`）
- **重排策略**: 语义分数×0.6 + 时效衰减×0.3 + 点赞数×0.1
- **LLM**: `qwen/qwen-turbo`（via OpenRouter），温度 0.3
- **数据来源**: 牛客网面经（搜狗搜索 → 正文抽取 → 分块入库）

## 数据稀疏说明

初次使用时 ChromaDB 为空，需先爬取。`scripts/sample_data.json` 包含约 13 个种子 URL 可直接复用。爬取 10+ 篇后 RAG 质量明显提升。
