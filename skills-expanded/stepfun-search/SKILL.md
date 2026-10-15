---
name: stepfun-search
description: StepFun Search API - 实时网络搜索工具。通过 StepFun API 进行互联网搜索，获取最新信息和研究资源。使用场景：用户说"联网搜索 XXX"、"网络搜索 XXX"、"搜索 XXX" 时触发。Triggers: "联网搜索", "网络搜索", "搜索".
---

# StepFun Search Skill

基于 StepFun API 的实时网络搜索工具。支持多分类搜索、结果过滤和格式化输出。

## Configuration

API configuration is stored in `~/.openclaw/openclaw.json` using the **skills** format:

```json
{
  "skills": {
    "entries": {
      "stepfun-search": {
        "enabled": true,
        "env": {
          "STEPFUN_API_KEY": "YOUR_API_KEY"
        }
      }
    }
  }
}
```

The API key is loaded from the `STEPFUN_API_KEY` environment variable, which is automatically set by OpenClaw's skill system.

### 📝 Migration Note (2026-03-09)

**Previous configuration (❌ DEPRECATED):**
```json
{
  "tools": {
    "web": {
      "search": {
        "apiKey": "YOUR_API_KEY"
      }
    }
  }
}
```

**New configuration (✅ CURRENT):**
- Moved from `tools.web.search.apiKey` to `skills.entries.stepfun-search.env.STEPFUN_API_KEY`
- Reason: OpenClaw core only supports `tools.web` natively. Custom search APIs are better managed as skills.
- Benefit: Cleaner config, proper skill isolation, easier to manage multiple API keys

### ⚠️ Important Note

**Do NOT use `tools.stepfun` or similar!** Use the **skills** format above for all custom tool APIs.

## Core Features

### 1. Research Search (学术搜索)

Find academic papers, research reports, and technical documentation.

**Category:** `research` (默认)

**Best for:**
- 学术论文 (academic papers)
- 研究报告 (research reports)
- 技术文档 (technical docs)
- 白皮书 (whitepapers)

### 2. Programming Search (编程搜索)

Find code snippets, documentation, and programming solutions.

**Category:** `programming`

**Best for:**
- 代码示例 (code examples)
- 技术文档 (technical docs)
- API 参考 (API reference)
- 教程和指南 (tutorials)

### 3. Business Search (商业搜索)

Find business news, market insights, and company information.

**Category:** `business`

**Best for:**
- 商业新闻 (business news)
- 市场分析 (market analysis)
- 公司信息 (company info)
- 行业报告 (industry reports)

### 4. Government Search (政府搜索)

Find government documents, policies, and official information.

**Category:** `gov`

**Best for:**
- 政府文件 (government docs)
- 政策法规 (policies)
- 官方信息 (official info)

## Usage Examples

### CLI Usage

```bash
# 学术搜索（默认）
python3 scripts/stepfun_search.py "transformer attention mechanism" 5 research json

# 编程搜索
python3 scripts/stepfun_search.py "Python asyncio tutorial" 5 programming json

# 商业搜索
python3 scripts/stepfun_search.py "AI startup funding" 5 business markdown

# 政府搜索
python3 scripts/stepfun_search.py "data privacy regulation" 5 gov text
```

### Output Formats

- **JSON**: Full structured data (default)
- **Markdown**: Formatted for documents and chat
- **Text**: Plain text, no markup

## Search Tips

### ✅ Good Search Queries

- **Specific and clear**: "Stable Diffusion fine-tuning guide"
- **Domain-specific**: Use category parameter (research/programming/business/gov)
- **Keyword-based**: "Python async tutorial" (not "How do I learn Python async?")
- **Combined terms**: "PyTorch image classification" (focused, not broad)

### ❌ Avoid

- **Too broad**: "Image", "Data" (use more specific terms)
- **Full sentences**: Use keywords instead
- **Overly long**: Keep under 200 characters for best results

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| `STEPFUN_API_KEY not set` | Check `~/.openclaw/openclaw.json` skills config |
| `Authorization failed` | Verify API key is valid and active |
| `Timeout (>30s)` | Retry or simplify query |
| `No results found` | Try different keywords or change category |

## Rate Limiting

- **Default quota**: Up to 100 requests/day (free tier)
- **Request timeout**: 30 seconds per request
- **Max results**: 10 per query

## Performance Notes

- First request: 2-5 seconds (API processing)
- Cached results: <100ms (15-minute cache TTL)
- Result quality improves with specific queries

## Integration with OpenClaw

This skill is integrated with OpenClaw's:
- **Natural language triggers** - "联网搜索", "网络搜索"
- **Agent system** - Automatically called via skill dispatcher
- **Context persistence** - Results cached within session
- **Output formatting** - Markdown support for chat display

## Advanced: API Reference

See `references/api-reference.md` for:
- Full API endpoint documentation
- Authentication details
- Request/response schemas
- Error codes and handling
