---
name: search-zego-doc-fragments
description: Searches ZEGO documentation for specific API info, error codes, error messages, and parameters. Use when the user asks about error code/error mesage meanings, API parameters, or feature support. Use when troubleshooting ZEGO SDK issues or checking platform compatibility. Use when the user mentions 错误码, 这个参数什么意思, API怎么用, does ZEGO support, or debugging RTC/ZIM/Express SDK problems. Do NOT use this skill when the user wants to integrate or implement ZEGO products/features - use integrate-zego-product instead.
version: 1.0.4
---

## ZEGO Knowledge Base Search

This skill provides RAG-based search capabilities for ZEGO documentation. Use this skill to find specific, point-in-time information from ZEGO's knowledge base.

## Core Characteristic

**This skill uses RAG (Retrieval-Augmented Generation) to search vector databases and returns knowledge base fragments, NOT complete documentation.**

This approach is ideal for:
- **Point queries:** Error codes, specific API parameters, configuration options
- **Quick lookups:** Feature availability, permission requirements, platform support
- **Troubleshooting:** Error meanings, common issues, solutions

This approach is NOT suitable for:
- **Complete workflows:** Integration guides, Quick Start tutorials
- **End-to-end processes:** Step-by-step implementation
- **Comprehensive understanding:** Full feature documentation

**For integration workflows, use the `integrate-zego-product` skill instead.**

## When to Use This Skill

Trigger this skill when users ask:

| Query Type | Example Questions |
|------------|-------------------|
| Error codes | "What does error code 1230004 mean?", "错误码 1230004 是什么意思？" |
| API usage | "How to use loginRoom?", "createEngine 参数说明" |
| Feature check | "Does RTC support screen sharing?", "ZIM 支持群聊吗？" |
| Configuration | "How to set video resolution?", "如何配置音频编码参数？" |
| Platform support | "Does RTC support Flutter?", "Linux 平台支持吗？" |

## Search Workflow

### Step 0: Get Available Datasets

After confirming user intent, identify which knowledge bases to search:

```
Call: mcp__plugin_zego-assistant_ZEGO__get_zego_product_datasets
Returns: All ZEGO products with their dataset IDs
```


### Step 1: Confirm User Intent (CRITICAL)

Before executing any search, confirm the following information with the user if not already specified:

**Required Information:**
1. **Product** - Which ZEGO product?
   List from `get_zego_product_datasets` tool returned list

2. **Platform** (if applicable) - Which platform?
   List from `get_platforms_by_product` tool returned list(name parameter can not contain underscores and hyphens, probably contains Chinese. For example (实时音视频, 实时互动 AI Agent) can not use (real_time_video_rtc, aiagent_rtc))


**When to ask:**
- User query is generic (e.g., "What does error 1230004 mean?")
- User doesn't specify product (e.g., "How to use loginRoom?")
- User doesn't specify platform (e.g., "Does it support screen sharing?")
- Multiple products could match the query

**Example confirmation:**
```
To search accurately, please specify:
1. Which ZEGO product? (Real time audio/video(RTC), In-app Chat(ZIM), AI Agent, etc.)
2. Which platform? (iOS, Android, Web, etc.)
```

**Skip confirmation if:**
- User explicitly mentions product (e.g., "Real time audio/video(RTC) error 1230004")
- User explicitly mentions platform (e.g., "iOS loginRoom")
- Context clearly identifies product/platform
- Error code is product-specific (prefix identifies product)


### Step 2: Select Relevant Datasets

From the returned results, filter for relevant products:
- `real_time_video_*` - RTC products
- `zim_*` - In-app Chat (ZIM)
- `aiagent_*` - AI Agent
- `live_streaming_*` - Live Streaming
- Other product-specific datasets

### Step 3: Execute Search

```
Call: mcp__plugin_zego-assistant_ZEGO__search_zego_docs
Parameters:
- query: Search text (error code, API name, feature description)
- dataset_ids: Array of selected dataset IDs
```

**Critical: Use the `id` field, NOT the `name` field!**

When calling `search_zego_docs`, use the **`id`** field from `get_zego_product_datasets` output:

```json
{
  "name": "云端播放器",
  "description": "【英文名Cloud Player】云端播放器...",
  "datasets": [
    {
      "id": "a6ce5daa960911f085fd76185b8a64f0",
      "name": "cloud_player_zh"
    },
    {
      "id": "a7803c00960911f0962376185b8a64f0",
      "name": "cloud_player_server_zh"
    }
  ]
}
```

**Correct:** `dataset_ids = ["a6ce5daa960911f085fd76185b8a64f0"]`
**Wrong:** `dataset_ids = ["cloud_player_zh"]` ❌ (this is the name, not the ID!)

**Rules for dataset_ids parameter:**
1. Use the **`id`** field value (32-character hexadecimal string)
2. Never use the **`name`** field value
3. Always call `get_zego_product_datasets` first to get valid IDs
4. Copy the `id` value exactly as returned

### Step 4: Present Results

Present the RAG fragments returned from the search. Explain that these are knowledge base excerpts and recommend consulting complete documentation for comprehensive understanding.

## Common Search Scenarios

### Error Code Lookup

**Scenario:** User asks "What does error code 1230004 mean?"

**With missing context:**
```
0. Confirm: "Which ZEGO product? (Real time audio/video(RTC), In-app Chat(ZIM), AI Agent, etc.)"
1. Get datasets: call get_zego_product_datasets
2. Filter for: datasets for specified product
3. Search: query="1230004" with relevant dataset_ids
4. Present: Error meaning and suggested solutions
```

**With explicit product:** "Real time audio/video(RTC) error 1230004"
```
0. Skip confirmation (product already specified)
1. Get datasets: call get_zego_product_datasets
2. Filter for: real_time_video datasets
3. Search: query="1230004" with relevant dataset_ids
4. Present: Error meaning and suggested solutions
```

### API Usage Query

**Scenario:** User asks "How to use loginRoom?"

**With missing context:**
```
0. Confirm: "Which product and platform? (e.g., Real time audio/video(RTC) iOS)"
1. Get datasets: call get_zego_product_datasets
2. Filter for: datasets for specified product/platform
3. Search: query="loginRoom" with relevant dataset_ids
4. Present: API usage fragments, parameter descriptions
5. Note: For complete API reference, use get_doc_links + WebFetch
```

**With explicit context:** "How to use loginRoom on Android Real time audio/video(RTC)?"
```
0. Skip confirmation (product and platform specified)
1. Get datasets: call get_zego_product_datasets
2. Filter for: real_time_video Android datasets
3. Search: query="loginRoom" with relevant dataset_ids
4. Present: API usage fragments, parameter descriptions
```

### Feature Availability Check

**Scenario:** User asks "Does Real time audio/video(RTC) support screen sharing?"

**With explicit product:**
```
0. Skip confirmation (product already specified)
1. Get datasets: real_time_video datasets
2. Search: query="screen sharing" with relevant dataset_ids
3. Present: Feature support information from results
```

## Available MCP Tools

**Discovery:**
- `mcp__plugin_zego-assistant_ZEGO__get_zego_product_datasets` - List products and datasets
- `mcp__plugin_zego-assistant_ZEGO__get_platforms_by_product` - Get supported platforms

**Search:**
- `mcp__plugin_zego-assistant_ZEGO__search_zego_docs` - RAG-based search (primary tool for this skill)

**Documentation (for complete docs):**
- `mcp__plugin_zego-assistant_ZEGO__get_doc_links` - Get full documentation URLs

## Best Practices

1. **Confirm user intent before searching (CRITICAL)**
   - Ask for product if not specified (RTC, ZIM, AI Agent, etc.)
   - Ask for platform if not specified (iOS, Android, Web, etc.)
   - Skip confirmation only when context is explicit
   - This improves accuracy and reduces unnecessary searches

2. **Validate dataset IDs before searching**
   - Only use the `id` field from `get_zego_product_datasets`
   - Never use the `name` field (e.g., "cloud_player_zh")
   - Dataset IDs are 32-character hexadecimal strings

3. **Use specific, focused queries**
   - "error code 1230004" ✅
   - "how to integrate RTC" ❌ (use integrate-zego-product instead)

4. **Include context in queries**
   - Specify product, platform, and feature when possible
   - "RTC iOS loginRoom timeout" vs "loginRoom"

5. **Prioritize non-FAQ results**
   - FAQ knowledge bases may not be as current
   - API references and guides are more authoritative

6. **Know the limitations**
   - RAG returns fragments, not complete documentation
   - For integration workflows, always use integrate-zego-product skill

## Search Result Interpretation

When presenting RAG results:

1. **Acknowledge the source**
   - "Based on ZEGO knowledge base search results..."
   - "According to the documentation fragments..."

2. **Provide context**
   - Explain what the fragments mean
   - Connect fragments to user's question

3. **Suggest next steps**
   - "For complete API documentation, refer to..."
   - "For integration guidance, use integrate-zego-product skill"

## Integration vs Search Decision Tree

```
User Request
    │
    ├─ Needs to integrate ZEGO product?
    │   └─ Yes → Use integrate-zego-product skill
    │
    ├─ Has error code?
    │   └─ Yes → Use this skill (search-zego-doc-fragments)
    │
    ├─ Needs specific API usage?
    │   └─ Yes → Use this skill (search-zego-doc-fragments)
    │
    ├─ Checking feature support?
    │   └─ Yes → Use this skill (search-zego-doc-fragments)
    │
    └─ Needs complete guide?
        └─ No → Use this skill (search-zego-doc-fragments)
```

## Avoid These Mistakes

1. **Don't skip user intent confirmation**
   - Always ask for product/platform when not specified
   - Searching without context produces poor results
   - Confirmation takes less time than re-searching

2. **Don't use RAG for integration workflows**
   - Complete guides require reading full documentation
   - RAG fragments cannot provide end-to-step workflows

3. **Don't use invalid dataset IDs**
   - Always use the `id` field from `get_zego_product_datasets`
   - Never use the `name` field (e.g., "cloud_player_zh")
   - Dataset IDs are 32-character hexadecimal strings like "a6ce5daa960911f085fd76185b8a64f0"

4. **Don't ignore product context**
   - Include product name in queries when possible
   - Filter datasets to relevant products only

5. **Don't present fragments as complete documentation**
   - Always clarify these are knowledge base excerpts
   - Recommend full documentation for comprehensive understanding
