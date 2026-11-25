---
name: optimize-commands
description: "Ultra-fast token-efficient execution. token-turbo + caveman + parallel blast + multi-model routing. Active by default — no command needed."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Write, Agent
---

# optimize-commands — Always-On Default Behavior v3.0

No command needed. Active every session from first prompt.

## MULTI-LLM BURST — DEFAULT ON (every task, every session)

**llm-burst** = 8 models fire in parallel → judge picks best → Claude synthesizes final.

```bash
# Auto-invoked on sub-tasks. Manual use:
~/.claude/bin/llm-burst "your prompt"
~/.claude/bin/llm-burst --models groq,gemini,deepseek,g0dm0d3 "focused prompt"
~/.claude/bin/llm-burst --json "prompt" | jq '.all[] | {model,score}'  # see all scores
```

**Model roster (all fire simultaneously — 15 models total):**
| Model | Strength | Cost |
|---|---|---|
| G0DM0D3 ULTRAPLINIAN | Races 55 models, Liquid Response, auto-upgrades | ~free |
| Groq llama3-70b | Fastest cloud, 8/10 | Free tier |
| Gemini 2.0 Flash | Research, analysis, drafting | Free tier |
| DeepSeek-V3 (OpenRouter) | Reasoning, code, complex tasks | ~$0.001/1k |
| Ollama llama3 | Local, offline, zero cost | Free |
| GPT-4o-mini | Reliable general purpose | ~$0.001/1k |
| GLM-4.5-air | Fast Chinese model, multilingual | Low cost |
| Gemma4-27b:free | Google architecture, OpenRouter free | Free |
| **GPT4All: Meta-Llama-3-8B** | Local Metal-accelerated, offline | **Free forever** |
| **GPT4All: Meta-Llama-3.1-8B** | Latest Llama, better reasoning | **Free forever** |
| **GPT4All: Llama-3.2-3B** | Fast local, lightweight | **Free forever** |
| **GPT4All: Hermes-2-Pro-Mistral-7B** | Instruction following, local | **Free forever** |
| **GPT4All: Mistral-7B** | Fast general purpose, local | **Free forever** |
| **GPT4All: Phi-3-mini** | Microsoft, efficient reasoning | **Free forever** |
| **GPT4All: Qwen2.5-Coder-7B** | Code generation specialist, local | **Free forever** |

> DeepSeek-R1-7B / 1.5B: disabled — pre-tokenizer unsupported by gpt4all 2.8.2 llama.cpp (tokenizer type `deepseek-r1-qwen` unknown)

**Judge scoring:** completeness(25) + structure(10) + actionability(10) + length_balance(30) + G0DM0D3_bonus(+20)
**Winner** = highest score. Top 2-3 synthesized if complementary signals found.

## CODE AGENT SYSTEM — ALWAYS-ON (auto-routes every coding task, no command needed)

Activated automatically on any coding-related prompt. No `/codegen` or `/launch-optimized` required.

**Auto-routing by intent:**
| Prompt contains | Actor → Model | Skill |
|----------------|--------------|-------|
| fix bug / error / traceback / crash | Debugger → Sonnet High | `/bugfix` |
| refactor / optimize / clean up / rewrite | Builder → Sonnet Medium | `/refactor` |
| generate / create / write / build + code | Architect → Sonnet PlanMode → Builder → Sonnet Medium | `/codegen` |
| write tests / add coverage / pytest / jest | Builder → Sonnet Low | `/testdocs mode=tests` |
| write docs / docstring / README / comment | Builder → Sonnet Low | `/testdocs mode=docs` |
| review / audit / check code / security | Curator → Opus High | code-review |
| extract / parse / read file / list imports | Extractor → Haiku Low | extraction |

**Hard laws (enforced on every coding task):**
- PLAN before BUILD — Sonnet PlanMode first, always. Skip = reject
- Opus only for critical/architectural. Never for docs, unit tests, simple bugs.
- Haiku only for extraction/parsing. Never for generation.
- Max 3 exchanges per chat — open fresh chat for next sub-task
- Cite all library/API references: `[SOURCE: name|version|verified:yes/no]`
- Flag unverified claims: `[UNVERIFIED: claim]` or `[ASSUMPTION: reason]`

**Full framework**: `~/Downloads/Claude-Code-Automation-System.md`

---

## REPORT CREATOR — ALWAYS-ON (auto-fires on any report/document task, no command needed)

Professional institutional-grade reports across PDF, DOCX, XLSX, LaTeX, Excel, Dashboards, PPT. Zero tolerance for overlap, spacing issues, or inconsistent formatting.

**Auto-routing by trigger — Template Library:**
| Prompt contains | Output | Template Used | Tools |
|---|---|---|---|
| "create/make/generate/write report" | PDF via ReportLab | `report-creator` standard | `report-creator` |
| "pdf report" / "audit report" / "360 report" | PDF 300+ DPI | `nasa-latex-docs` or ReportLab | `report-creator` + `ads-report-pdf` |
| "technical report" / "nasa style" / "institutional" | LaTeX PDF | `~/.claude/templates/latex/nasa-latex-docs/` | LaTeX compile |
| "corporate report" / "branded report" | LaTeX PDF | `~/.claude/templates/latex/corporate-latex/` | LaTeX compile |
| "academic report" / "research report" | LaTeX PDF | `~/.claude/templates/latex/heitzmann-latex/` | LaTeX compile |
| "excel report" / "kpi" / "data table" / "xlsx" | XLSX | `~/.claude/templates/excel/bizfin-templates/` | `report-creator` + `/xlsx` |
| "sales report" / "sales analysis" / "sales dashboard" | XLSX | `~/.claude/templates/excel/sales-dashboard/` | `report-creator` + `/xlsx` |
| "finance report" / "financial report" / "p&l" | XLSX | `~/.claude/templates/excel/finance-kpi/` | `report-creator` + `/xlsx` |
| "kpi dashboard" / "dynamic dashboard" | Dashboard | `~/.claude/templates/dashboards/dynamic-kpi/` | Python/openpyxl |
| "marketing dashboard" / "performance dashboard" | Dashboard | `~/.claude/templates/dashboards/aduet-dashboards/` | Python/openpyxl |
| "presentation" / "ppt" / "slides" / "deck" | PPTX | `~/.claude/templates/ppt/gbif-ppt/` | `/pptx` |
| "docx" / "word document" / "editable report" | DOCX | Heading hierarchy + TOC | `report-creator` + `/docx` |
| "fix report" / "report layout" / "formatting" | Audit + fix | Current file diagnosed | `report-creator` |

**Template library paths:**
```
~/.claude/templates/
├── latex/
│   ├── nasa-latex-docs/       ← institutional/technical (★★★★★)
│   ├── corporate-latex/       ← branded corporate (★★★★★)
│   ├── heitzmann-latex/       ← academic/research (★★★★½)
│   ├── thomasbenas-report/    ← clean minimal (★★★★)
│   └── chrrel-report/         ← quick start (★★★★)
├── excel/
│   ├── sales-dashboard/       ← sales KPI (★★★★★)
│   ├── bizfin-templates/      ← business finance (★★★★)
│   ├── finance-kpi/           ← finance ops (★★★)
│   └── financial-macros/      ← VBA macros (★★★)
├── dashboards/
│   ├── aduet-dashboards/      ← multi-type dashboards (★★★★)
│   └── dynamic-kpi/           ← interactive KPIs (★★★)
└── ppt/
    └── gbif-ppt/              ← branded presentation (★★★½)
```

**Non-negotiable quality laws (every report):**
- Zero overlapping elements — text never obscures charts/images
- Pre-delivery checklist: spacing ✓ typography ✓ charts labeled ✓ colors accessible ✓ data accurate ✓
- Output always → `~/Downloads/` (never Desktop)
- Brand palette from client URL when available
- ReportLab for PDF (direct — never HTML-to-PDF) | LaTeX for institutional/technical
- Select best-fit template automatically based on report type

**Full skill**: `~/.claude/skills/report-creator/SKILL.md`

---

## AGENCY-AGENTS + N8N AUTO-TRIGGER — ALWAYS-ON

Auto-fires on EVERY task. No command needed. Detects intent → activates right agent + suggests n8n workflow.

**Installed locations:**
- Agents: `~/.claude/agents/` (210 specialists, all active)
- Workflows: `~/installed-repos/n8nworkflows.xyz/workflows/` (8,159 JSONs)
- Index: `~/installed-repos/n8nworkflows.xyz/workflow_index.txt`

**Keyword → Agent + n8n Auto-Routing:**

| Detected Keywords | Agent Activated | n8n Workflow Pool |
|---|---|---|
| ads / ppc / google ads / meta | Paid Media Specialist | Google Drive→FB Ads, ad reporting flows |
| email / outreach / sequence | Email Intelligence Engineer + SDR | 874 Gmail/email automation workflows |
| code / bug / build / deploy | Backend Architect + DevOps Automator | Webhook triggers, CI/CD pipelines |
| seo / content / blog | SEO Specialist + Content Creator | Research collection, blog auto-post |
| lead gen / prospect / crm | Lead Qualification Agent + SDR | 121 lead flows (Apollo, Hunter, LinkedIn) |
| slack / notification / alert | DevOps Automator | 328 Slack automation workflows |
| data / spreadsheet / report | Data Engineer + Finance Agent | Sheets, Airtable, NocoDB pipelines |
| social / instagram / twitter | Social Media Strategist | 197 social automation flows |
| shopify / ecom / stripe | E-com Specialist + Sales Agent | 82 Shopify/WooCommerce workflows |
| strategy / gtm / launch | GTM Strategist + Product Manager | Investor intel, market research flows |
| telegram / bot / chat | Backend Architect | 309 Telegram bot workflows |
| notion / airtable / database | Data Engineer | Notion/Airtable sync flows |

**How to use:**
- Say "Activate [Division] mode" to load a specific agent personality
- `/agency-run` → orchestrator activates ALL relevant agents per division
- `/all-agents` → all 210 agents fire simultaneously
- `grep -i '[topic]' ~/installed-repos/n8nworkflows.xyz/workflow_index.txt` → find n8n workflows

**Agent Divisions (210 total):** Engineering(29) · Marketing(30) · Specialized(41) · Paid Media(7) · Game Dev(10) · Testing(8) · Design(8) · Sales(8) · Project Mgmt(6) · Strategy(6) · Spatial Computing(6) · Support(6) · Finance(5) · Product(5) · Academic(5)

---

## FREE CODING MODELS — AUTO MODEL DETECTOR (always-on)

**Tool**: `free-coding-models` (installed globally at `~/.nvm/versions/node/v24.14.1/bin/free-coding-models`)
**Purpose**: Pings ~170 free AI models across 16 providers in real-time → shows live latency + Stability Score → auto-writes winner into coding tool config (OpenClaw, Aider, Goose, etc.)

**Auto-detect triggers** (no command needed — fires when I detect any of these needs):

| When you say / need | Action |
|---|---|
| "which model is fastest right now" | → Run `free-coding-models` to live-ping all 170 |
| "find me a free model for [task]" | → Run `free-coding-models` + filter by task type |
| "switch my OpenClaw model" | → Run `free-coding-models` → select → auto-writes config |
| "benchmark models" / "model latency" | → Run `free-coding-models --benchmark` |
| "what's the best free coding model" | → Run `free-coding-models` → sort by Stability Score |
| "free api for [Groq/NVIDIA/Cerebras/etc]" | → Point to provider signup + run tool |
| Any model feels slow / timing out | → Run `free-coding-models` to find faster alternative |

**16 providers tracked (170 models):**
```
NVIDIA NIM (42)  · Groq (8)  · Cerebras (4)  · Google AI Studio (6)
GitHub Models (15) · Mistral (7) · Cloudflare Workers AI (15) · OpenRouter (31)
SambaNova (6) · OVHcloud (10) · Codestral (1) · ZAI (2)
Scaleway (10) · Alibaba DashScope (9) · Gemini CLI (6) · OpenCode Zen (8)
```

**Keys already configured** (in `~/.zshrc`):
`GROQ_API_KEY` ✓ · `OPENROUTER_API_KEY` ✓ · `GOOGLE_API_KEY` ✓ · `DASHSCOPE_API_KEY` ✓

**Run anytime in terminal:**
```bash
free-coding-models                          # interactive TUI — pick fastest model
free-coding-models --help                   # all options
```

**Stability Score formula**: p95 latency(30%) + jitter/variance(30%) + spike rate(20%) + uptime(20%)
Use Stability Score, NOT raw avg latency — a model averaging 1s with 6s spikes is worse than 1.5s stable.

**Auto-configure rule**: When a new fastest model is found, `free-coding-models` writes it directly into:
- `~/.openclaw/` (CoWork config)
- `~/.config/opencode/` (OpenCode)
- `~/.aider.conf.yml` (Aider)
- Any other connected coding tool

**Integration with MULTI-LLM BURST**: After running `free-coding-models`, update `llm-burst` default model roster with the new fastest provider for that session.

---

## ADS CREATIVE AI STACK — AUTO-ROUTING (always-on)

Installed at: `~/installed-repos/ads-creative/`

**5 repos — complete AI ad creative production pipeline:**

| Repo | Purpose | Trigger phrases | Path |
|---|---|---|---|
| **uni1-image-ad** | Generate Meta image ads via Luma uni-1 → auto-upload to Meta (paused) | "image ad" / "meta image ad" / "uni1" / "luma ad" / "generate ad creative" | `~/installed-repos/ads-creative/uni1-image-ad/` |
| **arcads-claude-code** | AI marketing videos via Arcads (Sora 2, Veo 3.1, Kling 3.0, Nano Banana) | "arcads" / "ai marketing video" / "sora 2" / "veo 3" / "kling" / "ai video ad" | `~/installed-repos/ads-creative/arcads-claude-code/` |
| **kie-ai-ad-builder** | KIE.ai video+image (Veo 3.1, Sora 2, Kling 3.0, Seedance 2, Nano Banana 2) | "kie.ai" / "kie video" / "seedance" / "kie ad builder" | `~/installed-repos/ads-creative/kie-ai-ad-builder/` |
| **meta-ads-spy** | Scrape competitor ads from Meta Ad Library → Airtable (copy, creatives, targeting) | "spy competitor ads" / "meta ad library" / "ad spy" / "competitor ads" / "ad swipe" | `~/installed-repos/ads-creative/meta-ads-spy/` |
| **codex-plugin-cc** | Run OpenAI Codex code reviews from inside Claude Code (`/codex:review`, `/codex:adversarial-review`) | "codex review" / "codex plugin" / "adversarial review" / "delegate to codex" | `~/installed-repos/ads-creative/codex-plugin-cc/` |

**Ratings:**
| Repo | Rating | Key dependency |
|---|---|---|
| uni1-image-ad | ★★★★★ | `LUMA_API_KEY` ✓ already set + Meta Ads API |
| arcads-claude-code | ★★★★★ | Arcads account (arcads.ai) |
| kie-ai-ad-builder | ★★★★★ | KIE.ai account (kie.ai) |
| meta-ads-spy | ★★★★★ | Meta Ad Library API token + Airtable API |
| codex-plugin-cc | ★★★★ | OpenAI API key / ChatGPT subscription |

**uni1-image-ad quick start** (LUMA_API_KEY already configured ✓):
```bash
cd ~/installed-repos/ads-creative/uni1-image-ad
# Read skills/uni1-image-ad/ — Claude Code skill, just tell it:
# "Generate a Meta image ad for [brand] — use uni-1, clone structure from ad ID [X]"
```

**meta-ads-spy quick start:**
```bash
cd ~/installed-repos/ads-creative/meta-ads-spy
pip install -r requirements.txt
# Set META_AD_LIBRARY_TOKEN + AIRTABLE_API_KEY + AIRTABLE_BASE_ID
python3 discover_competitors.py  # find competitor pages
python3 pull_ads.py              # scrape their ads into Airtable
```

**codex-plugin-cc quick start:**
```bash
cd ~/installed-repos/ads-creative/codex-plugin-cc
npm install
# Copy plugins/ dir to ~/.claude/plugins/
# Then use: /codex:review  /codex:adversarial-review  /codex:rescue
```

---

## MICROSOFT REPO STACK — AUTO-ROUTING (always-on)

Installed at: `~/installed-repos/microsoft/`

**Auto-routing table** (no command needed — fires on keyword detection):

| Prompt intent | Repo used | Path |
|---|---|---|
| "playwright" / "browser automation" / "e2e test" / "web scraping" | playwright | `~/installed-repos/microsoft/playwright/` |
| "playwright mcp" / "browser mcp" / "playwright server" | playwright-mcp | `~/installed-repos/microsoft/playwright-mcp/` |
| "semantic kernel" / "SK plugin" / "SK memory" / "SK planner" / "SK orchestration" | semantic-kernel | `~/installed-repos/microsoft/semantic-kernel/` |
| "ai for beginners" / "learn ai" / "ai curriculum" / "microsoft ai course" | AI-For-Beginners | `~/installed-repos/microsoft/AI-For-Beginners/` |
| "ml for beginners" / "machine learning course" / "learn ml" | ML-For-Beginners | `~/installed-repos/microsoft/ML-For-Beginners/` |
| "generative ai" / "genai course" / "llm for beginners" / "prompt engineering beginner" | generative-ai-for-beginners | `~/installed-repos/microsoft/generative-ai-for-beginners/` |
| "ai agents for beginners" / "build agents" / "agent tutorial" | ai-agents-for-beginners | `~/installed-repos/microsoft/ai-agents-for-beginners/` |
| "data science" / "data science course" / "learn data science" | Data-Science-For-Beginners | `~/installed-repos/microsoft/Data-Science-For-Beginners/` |
| "agent framework" / "microsoft agent framework" / "multi agent microsoft" | agent-framework | `~/installed-repos/microsoft/agent-framework/` |
| "agent365" / "office agent" / "365 dev tools" | Agent365-devTools | `~/installed-repos/microsoft/Agent365-devTools/` |

**Repo ratings & use cases:**

| Repo | Stars | Use for | Rating |
|---|---|---|---|
| playwright | ★★★★★ | Browser automation, scraping, E2E tests, Playwright MCP | ★★★★★ |
| playwright-mcp | ★★★★★ | MCP server for browser control via Claude | ★★★★★ |
| semantic-kernel | ★★★★★ | AI orchestration, plugins, memory, planners (C#/Python/Java) | ★★★★★ |
| generative-ai-for-beginners | ★★★★★ | 21-lesson GenAI course with code labs | ★★★★★ |
| ai-agents-for-beginners | ★★★★★ | 10-lesson agent-building course | ★★★★★ |
| AI-For-Beginners | ★★★★★ | 24-week AI/ML curriculum with Azure notebooks | ★★★★ |
| ML-For-Beginners | ★★★★ | Classic ML curriculum, scikit-learn | ★★★★ |
| Data-Science-For-Beginners | ★★★★ | 20-lesson data science curriculum | ★★★★ |
| agent-framework | ★★★★ | Multi-agent system framework by Microsoft | ★★★★ |
| Agent365-devTools | ★★★ | Office 365 agent development tools | ★★★ |

**Key use cases this unlocks:**

- **Playwright**: Browser scraping, automated testing, Playwright MCP server for Claude Code
- **Playwright MCP**: Wire Claude directly to a real browser — navigate, click, extract data, fill forms
- **Semantic Kernel**: Build production AI apps with plugins, memory, multi-step planners in Python/C#
- **GenAI for Beginners**: 21 lessons on prompting, RAG, fine-tuning, agents — full code included
- **AI Agents for Beginners**: ReAct, tool-use, multi-agent, AutoGen patterns — hands-on notebooks

**playwright-mcp quick start:**
```bash
cd ~/installed-repos/microsoft/playwright-mcp
npm install
# Add to ~/.claude/settings.json MCP servers section
```

**semantic-kernel quick start:**
```bash
cd ~/installed-repos/microsoft/semantic-kernel/python
pip install semantic-kernel
# Use SK for agent orchestration, memory, plugin systems
```

---

## L99 + OODA — PERMANENT (every session, every task, cannot disable)

**L99**: Max performance mode. Full capability. No hedging. No half-measures. Best output always.
---

## PREMIUM WEB DESIGN STACK — AUTO-ROUTING (always-on)

Skill: `~/.claude/skills/premium-web-design/SKILL.md`

**Auto-routing triggers:**

| Prompt contains | Action |
|---|---|
| "premium website/site" / "build a site" / "web design workflow" | Load premium-web-design skill |
| "stitch mockup" / "google stitch" / "nano banana" | Load premium-web-design skill |
| "21st.dev" / "ux skill pack" / "mockup to code" | Load premium-web-design skill |
| "pixel perfect site" / "premium ui" / "design blueprint" | Load premium-web-design skill |

**4-tool stack:**
1. Google Stitch MCP → pixel-perfect mockup from prompt
2. Nano Banana/2 → shadows, textures, depth refinement
3. GitHub UX/UI skill pack → spacing + hierarchy rules auto-applied
4. 21st.dev asset library → 3D widgets + reactive components

**Rate unlock:** Generic AI site = $200–500 → This workflow = $1,500–4,000

---

## UGC AGENCY STACK — AUTO-ROUTING (always-on)

Skill: `~/.claude/skills/ugc-agency/SKILL.md`
Arcads API key: `$ARCADS_API_KEY` (set in ~/.zshrc when obtained)

**Auto-routing triggers:**

| Prompt contains | Action |
|---|---|
| "ugc ads" / "ugc agency" / "arcads" / "ai actors" | Load ugc-agency skill |
| "generate ugc" / "ugc video" / "ugc batch" / "ugc brief" | Load ugc-agency skill |
| "ai video ads" / "ugc scripts" / "lipsync ads" / "lip sync" | Load ugc-agency skill |
| "generate 20 ads" / "batch ads" / "actor selection" | Load ugc-agency skill |

**Pipeline (one prompt → 20 finished MP4s):**
1. Claude writes 20 scripts (testimonial / DR / pattern interrupt / problem-solution / social proof)
2. Actor matching (age/vibe/energy per script)
3. Parallel render to Arcads API (all 20 simultaneously)
4. MP4s land in `~/ugc-output/` named by hook type

**Agency math:** $1,500/mo in · ~$150/mo tools · **90% gross margin**

**Setup:**
```bash
# Get key: arcads.ai → API settings
export ARCADS_API_KEY="your-key"
git clone --depth=1 https://github.com/krusemediallc/arcads-claude-code ~/.claude/skills/arcads/
```

---

## AIRTABLE SDK — AUTO-ROUTING (always-on)

Skill: `~/.claude/skills/airtable-sdk/SKILL.md`
Repo: `~/installed-repos/airtable.js/` (official Airtable JS SDK)
API key: `$AIRTABLE_API_KEY` ✓ configured
Base ID: `$AIRTABLE_BASE_ID` (needed — get from airtable.com/api)

**Triggers:** "airtable" / "airtable base" / "write to airtable" / "sync airtable" / "airtable sdk" / "airtable integration" / "meta ads to airtable"

**Capabilities:**
- Read/create/update/delete records (JS + Python)
- Batch operations (auto-chunks at 10 per Airtable API limit)
- Filter formulas, pagination, upsert
- Meta Ads Spy → Airtable pipeline schema built-in
- pyairtable (Python) + official airtable.js (Node) both documented

---

## KIMI CODE — Moonshot AI CLI (always-on)

Binary: `~/.local/bin/kimi` · Version: 1.41.0
Trigger: "kimi" / "kimi code" / "moonshot" / "kimi cli"

```bash
kimi           # start interactive session
kimi --help    # all commands
```

**Tier 0 routing:** Use Kimi for coding tasks as an alternative to DeepSeek/Groq — free quota, fast.

---

## KIMI — TOKEN-MINIMIZED TIER 0 ROUTING (always-on)

**Rule: Kimi K2.6 replaces Claude Opus for ALL long-context + reasoning sub-tasks.**
**Kimi costs ~95% less than Opus. Same quality on most tasks. Always prefer Kimi first.**

### Auto-routing by task type

| Task | Model | Why |
|---|---|---|
| Quick sub-tasks, short answers | `moonshot-v1-8k` | Cheapest, fastest |
| Long docs, full codebase analysis | `moonshot-v1-128k` | 128K at low cost |
| Reasoning, complex logic, vision | `kimi-k2.5` | 262K, reasoning on |
| Video analysis, multi-modal | `kimi-k2.6` | Best — replaces Opus |
| **Never use** | `claude-opus-4.x` for sub-tasks | 95% more expensive |

### Caveman compression — applied to ALL Kimi calls automatically

Every Kimi API call includes this system prompt (hardcoded in llm-burst):
```
Reply ULTRA SHORT. No filler. No repeat. Bullet points only if needed.
Max 150 words unless code. Never say 'certainly' or 'here is'. Just answer.
```

This gives **40-60% fewer output tokens** on every Kimi call regardless of model.

### How to call Kimi from Claude session

```bash
# Quick (8K — cheapest)
~/.claude/bin/llm-burst --models kimi "your prompt"

# Long context (128K)
~/.claude/bin/llm-burst --models kimi-long "your prompt"

# Reasoning / Opus replacement (262K)
~/.claude/bin/llm-burst --models kimi-k2 "your prompt"

# Race Kimi K2 against Groq + Gemini — pick best
~/.claude/bin/llm-burst --models kimi-k2,groq,gemini "your prompt"
```

### Direct Python (any script)

```python
import openai, os
client = openai.OpenAI(
    api_key=os.environ["KIMI_API_KEY"],
    base_url="https://api.moonshot.ai/v1"
)

CAVEMAN = ("Reply ULTRA SHORT. No filler. No repeat. Max 150 words unless code. "
           "Bullet points only if needed. Just answer.")

def kimi(prompt, model="moonshot-v1-8k"):
    """Auto-compressed Kimi call — works for any model incl. future ones"""
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CAVEMAN},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.3,
    )
    return r.choices[0].message.content

# Usage — same pattern works for ALL current + future Kimi models:
kimi("analyze this ad copy", model="moonshot-v1-8k")      # cheap
kimi("review this codebase", model="moonshot-v1-128k")    # long
kimi("reason through this strategy", model="kimi-k2.5")   # reasoning
kimi("analyze this video ad", model="kimi-k2.6")          # vision+video
kimi("...", model="kimi-k3")                              # future models — just change model name
```

---

## WEBSITE BUILDER — $10K Site From One Prompt (always-on)

Skill: `~/.claude/skills/website-builder/SKILL.md`
Command: `/website-builder-setup` (installed at `~/.claude/commands/website-builder-setup/`)

**Auto-routing triggers:** "build website" / "build a site" / "create website" / "10k website" / "framer motion" / "21st.dev" / "ui.ux pro max" / "deploy vercel" / "next.js site" / "agency website"

**5-Actor Pipeline:**
1. **Brief Extractor** (Kimi 8K) → extract business type, audience, vibe, colors, sections
2. **Design Director** (UI/UX Pro Max) → style system, color palette, font pairing, design spec JSON
3. **Component Selector** (21st.dev MCP / Kimi K2.5) → Hero, Features, Testimonials, Pricing, CTA, Footer
4. **Site Builder** (Claude Code) → Next.js + Tailwind + Framer Motion, full file structure
5. **QA + Deploy** (Kimi K2.6 vision) → Playwright screenshot diff → auto-fix → `npx vercel --prod`

**One-prompt format:**
```
Build me a premium website for [BUSINESS].
Audience: [WHO]. Vibe: [STYLE]. Colors: [HEX or "choose for me"].
Sections: Hero, Features, Testimonials, Pricing, CTA, Footer.
Use Framer Motion animations. Pull components from 21st.dev.
Apply UI/UX Pro Max design system. Output: Next.js + Tailwind. Deploy to Vercel.
```

**Repos:**
- `~/installed-repos/website-builder-setup/` — setup skill
- `~/installed-repos/ui-ux-pro-max-skill-main/` — design system
- `~/.claude/commands/website-builder-setup/` — /website-builder-setup command

**Agency pricing:** Starter $1,500 · Growth $3,500 · Premium $8,000 · Retainer $500/mo

---

## LEAD GEN AI — Automated Lead Extraction (always-on)

Skill: `~/.claude/skills/lead-gen-ai/SKILL.md`

**Auto-routing triggers:** "find leads" / "lead generation" / "extract leads" / "find contacts" / "vibe prospecting" / "apollo leads" / "find [business type] in [city]" / "find emails" / "find phones" / "leads excel"

**5-Actor Pipeline:**
1. **Brief Generator** (Kimi 8K) → structured extraction prompt from rough request
2. **Vibe Prospecting Extractor** (MCP) → `fetch-entities` + `enrich-prospects` + `export-to-csv`
3. **Apollo Enricher** (MCP) → `apollo_mixed_companies_search` + `apollo_people_match` + `apollo_contacts_search`
4. **Data Formatter** (Python/openpyxl) → Excel with Name, Address, Phone, Email, Website, LinkedIn, Instagram, Facebook, Rating, Reviews
5. **Outreach Sequence** (Kimi K2.5) → personalized email + LinkedIn DM + cold DM per lead → Mailchimp CSV

**Quick-start prompts:**
```bash
# Extract:
"Find top 20 [BUSINESS TYPE] in [CITY]. Get phone, email, website, Instagram, Google rating. Export Excel."

# Enrich (add decision makers):
"For each business, find owner/marketing manager name + email via Apollo"

# Generate outreach:
"Write personalized cold email for each lead offering [SERVICE]. Export CSV for Mailchimp."
```

**MCP tools wired:**
- `mcp__Vibe_Prospecting__fetch-entities` — search businesses
- `mcp__Vibe_Prospecting__enrich-prospects` — add contact data
- `mcp__Vibe_Prospecting__export-to-csv` — download dataset
- `mcp__8b8885d8-497d-4b96-be50-89e1511947c7__apollo_mixed_companies_search` — find companies
- `mcp__8b8885d8-497d-4b96-be50-89e1511947c7__apollo_people_match` — find decision makers
- `mcp__8b8885d8-497d-4b96-be50-89e1511947c7__apollo_contacts_search` — filter contacts

**Output:** `~/Downloads/leads.xlsx` — 11-column Excel, auto-width, bold headers
