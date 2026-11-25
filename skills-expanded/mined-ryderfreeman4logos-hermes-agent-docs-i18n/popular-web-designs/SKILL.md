---
name: popular-web-designs
description: 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS.
version: 1.0.0
author: Hermes Agent + Teknium (design systems sourced from VoltAgent/awesome-design-md)
license: MIT
tags: [design, css, html, ui, web-development, design-systems, templates]
platforms: [linux, macos, windows]
triggers:
  - build a page that looks like
  - make it look like stripe
  - design like linear
  - vercel style
  - create a UI
  - web design
  - landing page
  - dashboard design
  - website styled like
---

# 流行网页设计模板

共有54套可直接用于生成HTML/CSS的实际设计系统。每套模板都完整涵盖了网站的视觉规范：色彩方案、字体层级、组件样式、间距系统、阴影效果、响应式设计行为，以及包含精确CSS值的实用提示语。

## 相关设计技能

- **`claude-design`** — 用于把控设计*流程与风格*（明确需求范围、生成多种设计方案、验证本地HTML文件质量、避免AI设计产生的低劣结果）。当用户希望打造一个经过精心设计、且风格需参照特定品牌时，可将该技能与本技能结合使用：`claude-design`负责推动整个工作流程，而本技能则提供所需的视觉规范。
- **`design-md`** — 适用于需要生成正式的DESIGN.md格式规范文件而非渲染后的实际网页的场景。

## 使用方法

1. 从下方的目录中选择一款设计模板
2. 加载模板：`skill_view(name="popular-web-designs", file_path="templates/<site>.md")`
3. 在生成HTML时使用这些设计规范和组件参数
4. 可与`generative-widgets`技能搭配，通过cloudflared隧道输出最终结果

每套模板顶部都包含**Hermes实现说明**板块，其中包含：
- 可直接复用的CDN字体替代方案及Google Fonts `<link>`标签
- 主字体与等宽字体的CSS字体系列配置
- 关于使用`write_file`功能创建HTML文件以及`browser_vision`功能进行验证的提示

## HTML生成流程

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <!-- Paste the Google Fonts <link> from the template's Hermes notes -->
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
  <style>
    /* Apply the template's color palette as CSS custom properties */
    :root {
      --color-bg: #ffffff;
      --color-text: #171717;
      --color-accent: #533afd;
      /* ... more from template Section 2 */
    }
    /* Apply typography from template Section 3 */
    body {
      font-family: 'Inter', system-ui, sans-serif;
      color: var(--color-text);
      background: var(--color-bg);
    }
    /* Apply component styles from template Section 4 */
    /* Apply layout from template Section 5 */
    /* Apply shadows from template Section 6 */
  </style>
</head>
<body>
  <!-- Build using component specs from the template -->
</body>
</html>
```

使用 `write_file` 函数写入文件，通过 `generative-widgets` 工作流（结合 cloudflared 隧道）进行展示，并利用 `browser_vision` 工具验证结果，以确保视觉呈现的准确性。

## 字体替换参考

大多数网站使用的都是无法通过 CDN 获取的专有字体。每个模板都对应了一个可在 Google Fonts 中找到的替代字体，这些替代字体能在保留原有设计风格的同时满足使用需求。常见映射关系如下：

| 专有字体 | CDN替代字体 | 设计特点 |
|---|---|---|
| Geist / Geist Sans | Google Fonts 中的 Geist | 几何感强，字符间距经过压缩处理 |
| Geist Mono | Google Fonts 中的 Geist Mono | 纯净的等宽字体，支持连字显示 |
| sohne-var（Stripe使用） | Source Sans 3 | 轻盈优雅的风格 |
| Berkeley Mono | JetBrains Mono | 专为技术场景设计的等宽字体 |
| Airbnb Cereal VF | DM Sans | 圆润友好的几何风格 |
| Circular（Spotify使用） | DM Sans | 具有几何感且色调温暖的字体 |
| figmaSans | Inter | 简洁的人文主义风格 |
| Pin Sans（Pinterest使用） | DM Sans | 友好且线条圆润的字体 |
| NVIDIA-EMEA | Inter（或 Arial system） | 工业风设计，风格简洁 |
| CoinbaseDisplay/Sans | DM Sans | 具有几何感且给人以可靠感的字体 |
| UberMove | DM Sans | 字体粗壮，排列紧凑 |
| HashiCorp Sans | Inter | 企业级风格，色调中性 |
| waldenburgNormal（Sanity使用） | Space Grotesk | 具有几何感，字符略显紧凑 |
| IBM Plex Sans/Mono | Google Fonts 中的 IBM Plex Sans/Mono | 可在 Google Fonts 中获取 |
| Rubik（Sentry使用） | Google Fonts 中的 Rubik | 可在 Google Fonts 中获取 |

当模板的 CDN 字体与原始字体相同（如 Inter、IBM Plex、Rubik、Geist）时，不会造成设计风格上的损失。而当使用替代字体时（如用 DM Sans 代替 Circular，用 Source Sans 3 代替 sohne-var），则需严格遵循模板中规定的字体粗细、大小及字距设置——因为这些参数比具体的字体类型更能决定页面的视觉风格。

## 设计主题库

### AI与机器学习领域

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `claude.md` | Anthropic Claude | 以暖色调陶土色为点缀，布局简洁专业 |
| `cohere.md` | Cohere | 生动渐变色彩，具备丰富数据展示的仪表盘风格 |
| `elevenlabs.md` | ElevenLabs | 深色电影感界面，搭配音频波形设计元素 |
| `minimax.md` | Minimax | 浓郁深色界面，辅以霓虹色调点缀 |
| `mistral.ai.md` | Mistral AI | 法国风格极简设计，整体色调为紫色系 |
| `ollama.md` | Ollama | 以终端界面为主，采用单色简约风格 |
| `opencode.ai.md` | OpenCode AI | 以开发者为中心的深色主题，全等宽字体显示 |
| `replicate.md` | Replicate | 简洁的白色背景，以代码展示为核心 |
| `runwayml.md` | RunwayML | 具有电影感的深色界面，布局丰富且包含大量媒体元素 |
| `together.ai.md` | Together AI | 技术感强，采用蓝图风格的设计 |
| `voltagent.md` | VoltAgent | 以纯黑背景为底，搭配翠绿色点缀，完全基于终端风格设计 |
| `x.ai.md` | xAI | 极简单色设计，充满未来感，全等宽字体显示 |

### 开发工具与平台类

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `cursor.md` | Cursor | 流畅的深色界面，搭配渐变色彩点缀 |
| `expo.md` | Expo | 深色主题，字距紧凑，以代码展示为核心 |
| `linear.app.md` | Linear | 极简深色模式，设计精准，配有紫色点缀 |
| `lovable.md` | Lovable | 鲜艳的渐变色彩，营造友好的开发者体验 |
| `mintlify.md` | Mintlify | 设计简洁，以绿色为点缀，便于阅读 |
| `posthog.md` | PostHog | 标识鲜明，拥有对开发者友好的深色界面 |
| `raycast.md` | Raycast | 光滑的深色铬金属质感，搭配鲜艳的渐变色彩 |
| `resend.md` | Resend | 极简深色主题，以等宽字体为设计特色 |
| `sentry.md` | Sentry | 深色仪表盘风格，数据展示密集，配有粉紫色点缀 |
| `supabase.md` | Supabase | 深色翠绿色主题，以代码为核心的开发者工具风格 |
| `superhuman.md` | Superhuman | 高端深色界面，以键盘操作为核心，带有紫色光效 |
| `vercel.md` | Vercel | 黑白对比鲜明，采用 Geist 字体系统 |
| `warp.md` | Warp | 类似 IDE 的深色界面，采用块状命令输入方式 |
| `zapier.md` | Zapier | 暖橙色调，搭配友好的插图元素 |

### 基础设施与云服务类

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `clickhouse.md` | ClickHouse | 以黄色为点缀，采用技术文档风格的界面设计 |
| `composio.md` | Composio | 现代深色风格，搭配多彩的集成图标 |
| `hashicorp.md` | HashiCorp | 企业级简洁风格，以黑白配色为主 |
| `mongodb.md` | MongoDB | 以绿色树叶作为品牌标识，侧重于技术文档风格 |
| `sanity.md` | Sanity | 红色作为点缀元素，采用以内容为核心的编辑布局 |
| `stripe.md` | Stripe | 独特的紫色渐变色彩，搭配300号字体带来的优雅感 |

### 设计与生产力工具类

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `airtable.md` | Airtable | 颜色丰富，风格友好，注重结构化数据展示 |
| `cal.md` | Cal.com | 简洁的中性风格界面，注重开发者使用的便捷性 |
| `clay.md` | Clay | 采用有机形状设计，搭配柔和渐变色彩，整体布局富有艺术感 |
| `figma.md` | Figma | 鲜艳的多色搭配，风格既有趣味性又专业严谨 |
| `framer.md` | Framer | 以黑色和蓝色为主色调，注重动态效果与设计感 |
| `intercom.md` | Intercom | 友好的蓝色调色板，采用对话式界面设计 |
| `miro.md` | Miro | 以亮黄色为点缀，营造无限画布般的视觉体验 |
| `notion.md` | Notion | 温暖的极简风格，标题采用衬线字体，界面整体柔和 |
| `pinterest.md` | Pinterest | 红色作为点缀元素，采用网格布局，以图片展示为核心 |
| `webflow.md` | Webflow | 蓝色作为点缀色调，呈现出精致的营销网站风格 |

### 金融科技与加密货币领域

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `coinbase.md` | Coinbase | 清新的蓝色品牌标识，注重建立信任感，具有机构级专业氛围 |
| `kraken.md` | Kraken | 深色界面以紫色为点缀，仪表盘设计中数据信息密集 |
| `revolut.md` | Revolut | 流畅的深色界面，卡片设计采用渐变效果，体现金融科技领域的精准感 |
| `wise.md` | Wise | 以亮绿色为点缀，风格友好且清晰易懂 |

### 企业级与消费类品牌

| 模板文件 | 对应网站 | 设计风格 |
|---|---|---|
| `airbnb.md` | Airbnb | 暖色调珊瑚色作为点缀，以摄影内容为核心，界面设计圆润柔和 |
| `apple.md` | Apple | 采用高品质的留白设计，使用 SF Pro 字体，搭配电影感强的视觉元素 |
| `bmw.md` | BMW | 深色高端质感界面，体现精准的工程设计理念 |
| `ibm.md` | IBM | 采用 Carbon 设计系统，搭配有序的蓝色色调方案 |
| `nvidia.md` | NVIDIA | 绿色与黑色相结合，展现出强大的技术力量感 |
| `spacex.md` | SpaceX | 极简的黑白配色，全幅展示视觉元素，充满未来感 |
| `spotify.md` | Spotify | 深色背景上搭配鲜艳的绿色色调，字体粗壮，以专辑封面作为设计核心 |
| `uber.md` | Uber | 黑白对比鲜明，字体排列紧凑，充满都市活力 |

## 如何选择合适的设计风格

需根据内容类型来匹配合适的主题风格：

- **开发工具/数据仪表盘类**：Linear、Vercel、Supabase、Raycast、Sentry
- **文档/内容网站类**：Mintlify、Notion、Sanity、MongoDB
- **营销/落地页类**：Stripe、Framer、Apple、SpaceX
- **深色模式界面**：Linear、Cursor、ElevenLabs、Warp、Superhuman
- **浅色/简洁界面**：Vercel、Stripe、Notion、Cal.com、Replicate
- **活泼友好风格**：PostHog、Figma、Lovable、Zapier、Miro
- **高端奢华风格**：Apple、BMW、Stripe、Superhuman、Revolut
- **数据密集型/仪表盘类**：Sentry、Kraken、Cohere、ClickHouse
- **等宽字体/终端风格**：Ollama、OpenCode、x.ai、VoltAgent