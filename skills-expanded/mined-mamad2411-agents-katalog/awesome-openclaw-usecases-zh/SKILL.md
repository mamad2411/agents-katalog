---
name: awesome-openclaw-usecases-zh
description: Chinese OpenClaw/AI agent use case reference with 50+ real-world scenarios for automation, content creation, DevOps, and productivity
triggers:
  - how do I build an OpenClaw agent for Chinese platforms
  - show me OpenClaw use cases for Feishu or DingTalk
  - what can I automate with OpenClaw in China
  - OpenClaw examples for WeChat or Xiaohongshu
  - how to set up AI agent for Chinese workflow
  - OpenClaw skills for A-share stock monitoring
  - multi-agent architecture patterns in OpenClaw
  - AI automation for Chinese social media
---

# awesome-openclaw-usecases-zh

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

A comprehensive Chinese-language reference for **OpenClaw** (formerly ClawdBot/MoltBot) use cases, featuring 50+ verified real-world scenarios for AI agent automation. This skill equips AI coding agents with knowledge of OpenClaw patterns, Chinese platform integrations, and production-ready implementations.

## What This Project Provides

**awesome-openclaw-usecases-zh** is a curated collection of OpenClaw use cases designed for Chinese users, including:

- **23 China-specific use cases**: Feishu, DingTalk, WeChat Work, Xiaohongshu, A-share stock monitoring
- **27 international use cases** (many with Chinese adaptations): social media, DevOps, productivity, research
- **Structured format**: Each use case includes pain points, capabilities, required skills, setup steps, and practical tips
- **Agent-readable structure**: Standardized markdown format suitable for AI consumption

## Core Concepts

| Concept | English | Description |
|---------|---------|-------------|
| 工作区 | Workspace | Agent's working directory |
| 灵魂 | SOUL.md | Defines agent personality and boundaries |
| 操作手册 | AGENTS.md | Agent's operational instructions |
| 记忆 | Memory | Persistent context and preferences |
| 技能 | Skill | Reusable knowledge packages |
| 工具 | Tool | Specific capabilities (file ops, search, messaging) |
| 频道 | Channel | Platform connectors (Telegram, Feishu, Discord) |
| 提示词 | Prompt | User instructions to agent |
| 定时任务 | Cron Job | Scheduled automation |
| 心跳 | Heartbeat | Periodic status checks and reports |
| 子智能体 | Sub-agent | Parallel agent spawning |

## Installation & Access

The repository is hosted on GitHub and AtomGit (China mirror):

```bash
# Clone from GitHub
git clone https://github.com/AlexAnys/awesome-openclaw-usecases-zh.git

# Clone from AtomGit (China)
git clone https://atomgit.com/alex_anys/awesome-openclaw-usecases-zh.git
```

## Repository Structure

```
awesome-openclaw-usecases-zh/
├── README.md                 # Main index with 50+ use cases
├── CONTRIBUTING.md           # Contribution guidelines
├── AGENT-GUIDE.md           # Guide for AI agents to use this repo
├── usecases/
│   ├── cn-*.md              # China-specific use cases (23)
│   ├── *.md                 # International use cases (27)
│   └── images/              # Screenshots and diagrams
└── templates/
    └── usecase-template.md  # Standard use case format
```

## Use Case Categories

### 🇨🇳 China-Specific (23 cases)

**Platform Bots (4)**
- `cn-feishu-ai-assistant.md` - Feishu/Lark bot integration
- `cn-feishu-lark-cli.md` - Lark CLI for agent operations (200+ commands)
- `cn-dingtalk-ai-assistant.md` - DingTalk bot (Stream mode)
- `cn-wecom-ai-assistant.md` - WeChat Work bot

**Content Creation (3)**
- `cn-xiaohongshu-automation.md` - Xiaohongshu publishing pipeline
- `cn-wechat-mp-automation.md` - WeChat Official Account automation
- `podcast-production-pipeline.md` - Podcast workflow (Ximalaya/Bilibili)

**Data & Research (7)**
- `cn-a-share-monitor.md` - A-share stock monitoring (AKShare)
- `earnings-tracker.md` - Earnings reports (Chinese stocks)
- `competitive-intelligence.md` - Competitor analysis (Baidu Index, WeChat Index)
- `cn-internet-research-30days.md` - 8 Chinese platform aggregation
- `hf-papers-research-discovery.md` - HuggingFace papers (Chinese mirrors)
- `arxiv-paper-reader-latex-writer.md` - arXiv + LaTeX (Chinese templates)

**Office & Customer Service (4)**
- `cn-office-automation.md` - Email, files, meeting notes (163/QQ/Outlook)
- `meeting-notes-action-items.md` - Meeting transcription (Feishu/Tencent/DingTalk)
- `multi-channel-customer-service.md` - Multi-channel support
- `cn-ecommerce-multi-agent.md` - E-commerce multi-agent architecture

**Personal Assistant (5)**
- `custom-morning-brief.md` - Daily briefing (Chinese news sources)
- `digital-persona-distillation.md` - Personality extraction (12+ platforms)
- `cn-multi-agent-operating-system.md` - Multi-agent OS architecture
- `agent-swarm-dev-team.md` - Agent swarm development team
- `multica-managed-agents.md` - Agent dashboard (web UI)

### 🌐 International (27 cases)

**Social Media (4)** - Reddit, YouTube, X aggregation  
**Creative & Building (3)** - Content pipelines, product building  
**Infrastructure & DevOps (5)** - Server self-healing, observability, workflow orchestration  
**Productivity (16)** - Email, calendar, notes, CRM, personal assistant  
**Research & Learning (9)** - Knowledge bases, market research, competitive analysis  
**Finance & Trading (1)** - Prediction market simulation

## Reading Use Cases

Each use case follows this structure:

```markdown
---
difficulty: ⭐ (copy-paste) | ⭐⭐ (config needed) | ⭐⭐⭐ (technical)
platform: [feishu|dingtalk|wecom|xiaohongshu|...]
tags: [automation, content-creation, ...]
---

# Use Case Title

## 痛点 (Pain Points)
What problem this solves

## 它能做什么 (Capabilities)
- Feature 1
- Feature 2

## 所需技能 (Required Skills)
- Skill package 1
- Skill package 2

## 如何设置 (Setup)
Step-by-step configuration with copy-paste prompts

## 实用建议 (Practical Tips)
Best practices and pitfalls
```

## Key Patterns for AI Agents

### 1. Chinese Platform Integration

**Feishu Bot Example** (`cn-feishu-ai-assistant.md`):

```javascript
// Install official Feishu SDK
npm install @larksuiteoapi/node-sdk

// Initialize bot
const lark = require('@larksuiteoapi/node-sdk');
const client = new lark.Client({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET,
});

// Handle incoming messages
app.post('/webhook', async (req, res) => {
  const { event } = req.body;
  if (event.type === 'message') {
    const { message_id, content } = event.message;
    const userInput = JSON.parse(content).text;
    
    // Send to OpenClaw agent
    const response = await openclawAgent.process(userInput);
    
    // Reply in Feishu
    await client.im.message.reply({
      message_id,
      content: JSON.stringify({ text: response }),
      msg_type: 'text',
    });
  }
  res.json({ ok: true });
});
```

**DingTalk Stream Mode** (`cn-dingtalk-ai-assistant.md`):

```python
# No public IP needed - uses WebSocket
from dingtalk_stream import AckMessage
import dingtalk_stream

def message_handler(dingtalk_client, message):
    content = message.text.content.strip()
    
    # Process with OpenClaw
    response = openclaw_agent.process(content)
    
    # Reply
    dingtalk_client.send_text_message(
        message.sender_id,
        response
    )
    return AckMessage.STATUS_OK

# Start Stream listener
client = dingtalk_stream.DingTalkStreamClient(
    client_id=os.getenv('DINGTALK_CLIENT_ID'),
    client_secret=os.getenv('DINGTALK_CLIENT_SECRET')
)
client.register_callback_handler('chatbot', message_handler)
client.start_forever()
```

### 2. Lark CLI Integration (`cn-feishu-lark-cli.md`)

Agents can use Lark CLI to operate Feishu as the user:

```bash
# Install Lark CLI
pip install lark-cli

# Configure authentication
export LARK_APP_ID="your_app_id"
export LARK_APP_SECRET="your_app_secret"
export LARK_USER_ACCESS_TOKEN="your_token"

# Search documents
lark-cli docx search --keyword "项目文档"

# Read meeting notes
lark-cli meeting-minutes list --date 2026-05-01

# Get calendar events
lark-cli calendar events --start-date 2026-05-16 --end-date 2026-05-17

# Send message
lark-cli message send --user-id "ou_xxx" --text "任务已完成"
```

**OpenClaw Skill Integration**:

```markdown
## Available Tools

- `lark_cli_search`: Search Feishu documents
- `lark_cli_calendar`: Query calendar events
- `lark_cli_message`: Send notifications

## Example Prompt

Search for project documentation related to "AI Agent" in Feishu and summarize the top 3 results.

## Agent Execution

1. Run: `lark-cli docx search --keyword "AI Agent" --limit 3`
2. Parse JSON output
3. For each doc, fetch content: `lark-cli docx get --doc-id {id}`
4. Summarize and return
```

### 3. A-Share Stock Monitoring (`cn-a-share-monitor.md`)

```python
# Using AKShare (free, no API key needed)
import akshare as ak
from datetime import datetime

def get_market_overview():
    """Pre-market briefing"""
    # Get index data
    sh_index = ak.stock_zh_index_daily(symbol="sh000001")
    latest = sh_index.iloc[-1]
    
    # Get sector money flow
    sectors = ak.stock_sector_fund_flow_rank(indicator="今日")
    top_sectors = sectors.head(5)
    
    return {
        "sh_index": {
            "close": latest['close'],
            "change": latest['close'] - latest['open'],
            "volume": latest['volume']
        },
        "top_sectors": top_sectors.to_dict('records')
    }

def post_market_review():
    """Post-market analysis"""
    # Get individual stock rankings
    gainers = ak.stock_zh_a_spot_em().nlargest(10, 'pct_chg')
    losers = ak.stock_zh_a_spot_em().nsmallest(10, 'pct_chg')
    
    return {
        "gainers": gainers[['code', 'name', 'pct_chg']].to_dict('records'),
        "losers": losers[['code', 'name', 'pct_chg']].to_dict('records')
    }

# Cron schedule in OpenClaw
# 8:30 AM: Send pre-market briefing to Feishu
# 3:30 PM: Send post-market review to Feishu
```

### 4. Multi-Agent Architecture (`cn-multi-agent-operating-system.md`)

**Core Pattern**:

```yaml
# workspace/AGENTS.md structure
agents:
  - name: coordinator
    role: Task decomposition and delegation
    memory: Global context
    
  - name: researcher
    role: Information gathering
    skills: [web-search, pdf-reader]
    
  - name: writer
    role: Content generation
    skills: [markdown-writer, seo-optimizer]
    
  - name: publisher
    role: Platform distribution
    skills: [feishu-bot, xiaohongshu-api]

workflow:
  1. User sends request to coordinator
  2. Coordinator spawns sub-agents
  3. Sub-agents report back to coordinator
  4. Coordinator synthesizes final output
```

**Implementation Example**:

```javascript
// Coordinator agent prompt
const coordinatorPrompt = `
You are a coordinator. When given a task:
1. Break it into subtasks
2. Assign each to a specialist sub-agent:
   - @researcher for data collection
   - @writer for content creation
   - @publisher for distribution
3. Collect results and synthesize
4. Return final output

Current task: Create and publish a Xiaohongshu post about OpenClaw
`;

// Spawn sub-agents
const researchResult = await spawnAgent('researcher', {
  task: 'Find trending OpenClaw use cases',
  tools: ['perplexity_search', 'github_trending']
});

const content = await spawnAgent('writer', {
  task: 'Write Xiaohongshu post',
  context: researchResult,
  tools: ['markdown_formatter', 'emoji_suggester']
});

const published = await spawnAgent('publisher', {
  task: 'Publish to Xiaohongshu',
  content: content,
  tools: ['xiaohongshu_api']
});
```

### 5. Xiaohongshu Automation (`cn-xiaohongshu-automation.md`)

```python
# Unofficial API (use with caution, rate limits apply)
from xhs import XhsClient

client = XhsClient(
    cookie=os.getenv('XHS_COOKIE'),  # Get from browser
)

def publish_note(title, content, images, tags):
    """Publish note to Xiaohongshu"""
    # Upload images first
    image_ids = []
    for img_path in images:
        with open(img_path, 'rb') as f:
            result = client.upload_image(f.read())
            image_ids.append(result['image_id'])
    
    # Create note
    note = client.create_note(
        title=title,
        desc=content,
        image_ids=image_ids,
        tags=tags,
        post_time=None,  # Publish immediately, or set timestamp
        is_private=False
    )
    
    return note['note_id']

# OpenClaw scheduled task
# Daily 7PM: Generate trending topic post
# Use DALL-E for cover image
# Auto-publish with optimal hashtags
```

### 6. WeChat Official Account (`cn-wechat-mp-automation.md`)

```python
# Using wechatpy library
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMedia, WeChatMaterial

client = WeChatClient(
    appid=os.getenv('WECHAT_APPID'),
    secret=os.getenv('WECHAT_SECRET')
)

def markdown_to_wechat_html(md_content):
    """Convert Markdown to WeChat-styled HTML"""
    import markdown2
    
    html = markdown2.markdown(md_content, extras=['fenced-code-blocks'])
    
    # Apply WeChat styling
    styled_html = f"""
    <section style="font-size: 16px; color: #333;">
        {html}
    </section>
    """
    return styled_html

def create_draft(title, content, thumb_media_id):
    """Create draft article"""
    articles = [{
        'title': title,
        'author': 'OpenClaw Bot',
        'digest': content[:100],
        'content': markdown_to_wechat_html(content),
        'thumb_media_id': thumb_media_id,
        'show_cover_pic': 1,
    }]
    
    result = client.material.add_news(articles)
    return result['media_id']

# OpenClaw automation
# 1. Agent writes article in Markdown
# 2. Convert to WeChat HTML
# 3. Upload cover image
# 4. Create draft (manual review before publish)
```

### 7. Meeting Notes Automation (`meeting-notes-action-items.md`)

**Feishu Integration**:

```javascript
// Get meeting transcript from Feishu
const getMeetingTranscript = async (meetingId) => {
  const response = await fetch(
    `https://open.feishu.cn/open-apis/vc/v1/meetings/${meetingId}/recording`,
    {
      headers: {
        Authorization: `Bearer ${process.env.FEISHU_TENANT_TOKEN}`,
      },
    }
  );
  const data = await response.json();
  return data.data.recording_url;
};

// Download and transcribe
const transcription = await whisperAPI.transcribe(recordingUrl);

// OpenClaw processes transcript
const prompt = `
Analyze this meeting transcript and generate:
1. Summary (3-5 sentences)
2. Key decisions made
3. Action items with owners and deadlines
4. Follow-up questions

Transcript:
${transcription}
`;

const analysis = await openclawAgent.process(prompt);

// Create Feishu tasks automatically
for (const actionItem of analysis.action_items) {
  await feishuClient.task.create({
    summary: actionItem.task,
    due_date: actionItem.deadline,
    assignee: actionItem.owner,
  });
}
```

### 8. Digital Persona Extraction (`digital-persona-distillation.md`)

```python
# Extract chat history from multiple platforms
def extract_wechat_history():
    """Extract from WeChat PC backup"""
    import sqlite3
    
    conn = sqlite3.connect('WeChat/Msg/Multi/MSG0.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT strftime('%Y-%m-%d', CreateTime, 'unixepoch'), 
               Message, IsSender
        FROM MSG
        WHERE Type = 1  -- Text messages only
        ORDER BY CreateTime DESC
        LIMIT 10000
    """)
    
    messages = cursor.fetchall()
    return [{'date': m[0], 'text': m[1], 'is_sender': m[2]} 
            for m in messages]

def extract_feishu_history():
    """Extract from Feishu via API"""
    messages = lark_client.im.message.list(
        container_id_type='chat',
        container_id=os.getenv('FEISHU_CHAT_ID'),
        page_size=100
    )
    return messages

# Aggregate all sources
all_messages = []
all_messages.extend(extract_wechat_history())
all_messages.extend(extract_feishu_history())
all_messages.extend(extract_telegram_history())  # etc.

# OpenClaw analysis prompt
persona_prompt = f"""
Analyze these {len(all_messages)} messages and extract:

1. Communication Style
   - Tone (formal/casual/humorous)
   - Vocabulary patterns
   - Common phrases

2. Values & Beliefs
   - Recurring themes
   - Priorities
   - Decision-making patterns

3. Interests & Expertise
   - Topics frequently discussed
   - Knowledge domains

4. Behavioral Patterns
   - Response time preferences
   - Message length
   - Emoji usage

Messages:
{json.dumps(all_messages[:1000])}  # Sample for token limits
"""

persona = await openclawAgent.process(persona_prompt)
# Save to SOUL.md for future interactions
```

## Environment Variables Reference

Common environment variables across use cases:

```bash
# Feishu/Lark
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_TENANT_TOKEN=t-xxx
LARK_USER_ACCESS_TOKEN=u-xxx

# DingTalk
DINGTALK_CLIENT_ID=xxx
DINGTALK_CLIENT_SECRET=xxx
DINGTALK_ROBOT_TOKEN=xxx

# WeChat Work
WECOM_CORP_ID=xxx
WECOM_AGENT_ID=xxx
WECOM_SECRET=xxx

# WeChat Official Account
WECHAT_APPID=xxx
WECHAT_SECRET=xxx

# Xiaohongshu
XHS_COOKIE="your_browser_cookie"

# Stock Data (AKShare is free, no key needed)
# But if using alternatives:
TUSHARE_TOKEN=xxx

# OpenClaw
OPENCLAW_WORKSPACE=/path/to/workspace
OPENCLAW_API_KEY=sk-xxx  # If using hosted version

# LLM Providers
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DEEPSEEK_API_KEY=sk-xxx  # Chinese LLM
ZHIPU_API_KEY=xxx  # GLM model
```

## Troubleshooting

### Chinese Platform Rate Limits

**Issue**: Feishu/DingTalk API rate limits  
**Solution**:
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=50)
def call_feishu_api():
    # Your API call
    pass
```

### AKShare Data Reliability

**Issue**: AKShare data sometimes has delays  
**Solution**: Add fallback data sources
```python
def get_stock_data(symbol, retries=3):
    try:
        return ak.stock_zh_a_hist(symbol=symbol)
    except Exception as e:
        if retries > 0:
            time.sleep(2)
            return get_stock_data(symbol, retries - 1)
        else:
            # Fallback to manual data source
            return fetch_from_tushare(symbol)
```

### WeChat Cookie Expiration

**Issue**: Xiaohongshu/WeChat cookies expire frequently  
**Solution**: Implement cookie refresh
```python
import browser_cookie3

def refresh_cookie(domain):
    """Auto-refresh cookie from browser"""
    cookies = browser_cookie3.chrome(domain_name=domain)
    cookie_str = '; '.join([f'{c.name}={c.value}' for c in cookies])
    return cookie_str

# Use in OpenClaw heartbeat
def heartbeat_check():
    global xhs_cookie
    xhs_cookie = refresh_cookie('.xiaohongshu.com')
```

### Multi-Agent Memory Conflicts

**Issue**: Sub-agents overwriting shared memory  
**Solution**: Namespace memory by agent
```javascript
// In AGENTS.md
memory_strategy: {
  coordinator: "workspace/memory/coordinator.json",
  researcher: "workspace/memory/researcher.json",
  writer: "workspace/memory/writer.json",
}

// Code
async function saveAgentMemory(agentName, data) {
  const memoryPath = `workspace/memory/${agentName}.json`;
  await fs.writeFile(memoryPath, JSON.stringify(data, null, 2));
}
```

## Best Practices

1. **Security**: Never hardcode credentials. Use environment variables or secret management tools.

2. **Chinese Text Encoding**: Always use UTF-8
   ```python
   with open('output.txt', 'w', encoding='utf-8') as f:
       f.write(chinese_content)
   ```

3. **Platform Compliance**: Respect platform ToS. Use official APIs when available.

4. **Graceful Degradation**: Handle API failures
   ```python
   try:
       result = feishu_api.call()
   except Exception as e:
       logger.error(f"Feishu API failed: {e}")
       result = fallback_method()
   ```

5. **Prompt Engineering for Chinese**: Use Chinese prompts for better results with Chinese LLMs
   ```python
   # Good
   prompt = "请总结这篇文章的要点"
   
   # Less effective with Chinese LLMs
   prompt = "Please summarize the key points of this article"
   ```

## Contributing

See [CONTRIBUTING.md](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/CONTRIBUTING.md) for guidelines. All use cases should follow the template format and include working code examples.

## Resources

- [OpenClaw Official Docs (Chinese)](https://docs.openclaw.ai/zh-CN)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Feishu Open Platform](https://open.feishu.cn/document/home)
- [DingTalk Open Platform](https://open.dingtalk.com/)
- [AKShare Documentation](https://akshare.xyz/)
- [Lark CLI](https://github.com/larksuite/lark-cli)
