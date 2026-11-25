---
name: xhs-calico-writer
description: >-
  Original Xiaohongshu/小红书 full post package generator with a night-screen navy and hand-drawn calico-cat visual system. Use when the user wants non-imitative 小红书爆款笔记,图文笔记,种草文,个人IP内容,产品/服务笔记,经验分享,避坑贴,清单贴,测评贴, or wants help turning raw ideas into publishable Xiaohongshu assets. By default output the complete package: strong titles, short正文, hashtags, comment-area copy, cover copy with detailed ChatGPT image prompt, and 3-5 text-heavy carousel page copies with detailed ChatGPT image prompts.
---

# XHS Calico Writer

Create original Xiaohongshu notes from the user's own ideas, facts, observations, frameworks, or product/service knowledge. Do not imitate viral posts or copy another creator's wording.

## Default Output Contract

When invoked, default to a complete 小红书图文发布包 even if the user only says “写一篇笔记”.

The final answer is incomplete unless it includes:
- 选题角度
- 标题备选
- 搜索关键词布局
- 正文
- 标签
- 评论区文案
- 封面图文案 with detailed `ChatGPT生图提示词`
- 配图生图文案 for 3-5 inner pages, each with detailed `ChatGPT生图提示词`
- 发布前审稿

If space feels tight, shorten正文 and audit first. Never omit 封面图文案 or 配图生图文案.

## Core Rules

- Anchor the post in original user-owned material: experience, opinion, product facts, observed audience pain, framework, checklist, comparison, or decision rule.
- If the user only gives a topic, infer a plausible original angle and mark it as an assumption.
- Make the carousel images carry the main content. 正文 should only be a short intro, summary, and comment prompt.
- Default正文 length: 120-280 Chinese characters. Maximum 350 unless the user asks for long正文.
- Do not fabricate results, screenshots, personal experience, income claims, medical/legal/financial certainty, or guaranteed outcomes.

## Title Rules

Generate 8 title candidates for full publishing assets.

Titles must feel like publishable hooks, not section labels. Avoid flat titles like:
- `AI工具推荐`
- `AI选股清单`
- `AI学习路线`
- `用AI选股先看4步`
- `我会这样用AI看股票`

Use stronger structures:
- 年份 + 怎么选: `2026 AI生图工具怎么选？我试了一圈`
- 避坑: `别乱充会员！AI生图工具适合谁`
- 场景分流: `设计师/自媒体/电商分别用哪个AI工具`
- 反常识: `这几款AI生图工具真不是一个赛道`
- 风险提醒: `AI选股最危险的一步`
- 决策表: `AI选股前，先做这张风险表`
- 新手钩子: `新手做图别纠结，按场景选AI工具`

A strong title should include at least one searchable keyword and one tension/decision element such as `别`, `坑`, `风险`, `误区`, `选错`, `别急`, `先看`, `真正`, `不是`, `怎么选`, `适合谁`.

## Search Keyword Layout

Build three keyword layers:
- 核心关键词: exact topic terms people search
- 长尾关键词: decision/problem phrases
- 场景关键词: user identity, use case, workflow, or pain

Place keywords naturally in:
- 标题
- 前两行
- 配图页标题
- 正文
- 标签
- 评论区引导

Do not keyword-stuff.

## Required Output Shape

Use this structure by default:
```markdown
## 选题角度
...

## 标题备选
1. ...
2. ...
3. ...
4. ...
5. ...
6. ...
7. ...
8. ...

推荐标题：...

## 搜索关键词布局
- 核心关键词:
- 长尾关键词:
- 场景关键词:
- 已埋入位置:

## 正文
...

## 标签
#...# #...#

## 评论区文案
- 置顶评论:
- 作者回复模板1:
- 作者回复模板2:
- 作者回复模板3:
- 追问引导:

## 封面图文案
- 页面目的:
- 页面文案:
  - 主标题:
  - 副标题:
  - 微文案:
- 重点高亮词:
- 版式说明:
- ChatGPT生图提示词:

## 配图生图文案

### 第1张｜...
- 页面目的:
- 页面文案:
- 重点高亮词:
- 版式说明:
- ChatGPT生图提示词:

### 第2张｜...
...

## 发布前审稿
- 最强点:
- 风险点:
- 可再强化:
```

Image Copy Rules
The note is image-first. 配图 must contain the useful content.
Default content distribution:
正文: 120-280 Chinese characters, hook + summary + comment prompt only
Cover: 1 strong title + 1 subtitle + 1 microcopy + visible topic card/table
Each inner page: 120-220 Chinese characters of useful on-image copy
Summary page: 160-260 Chinese characters with a decision rule or next action
Never return only a cover title and a short scene description. Cover and every inner page need a detailed, directly copyable ChatGPT 生图提示词.
Visual System
Use this fixed visual style unless the user gives another style:
White background: #FFFFFF
Primary ink and brand color: night-screen navy #162A46
Body text: #162A46 or near-black #1A1A1A when dense copy needs stronger contrast
Light panel fill: pale navy tint #E8EDF4
No red text or red decorative accents
No fluorescent lime, neon green, or high-saturation cyber colors
Clean editorial social-media layout
Text-led knowledge card
Large whitespace
Bold modern Chinese typography
Use #162A46 for titles, keywords, arrows, outlines, tabs, underlines, stickers, and small accents
Use #E8EDF4 only for subtle cards, comparison panels, and secondary backgrounds
Keep the page calm, credible, and soft rather than neon or cyberpunk
No real brand logos unless the user explicitly asks
For inner pages, use:
top navigation line with 4-6 sections
current section in black, others light gray
large bold black section title
2-4 short paragraphs or 4-7 bullets
highlighted keywords
one-sentence summary starting with 一句话理解:
optional bottom module: comparison table, checklist, flowchart, UI card, or decision table
Account Calico Cat IP
Cover prompts must include the account calico cat IP.
Fixed cat traits:
round, fluffy, chubby calico cat
cream-white base fur with warm orange and dark chocolate-brown patches
soft hand-drawn doodle illustration, slightly textured brown outlines, simple rounded shapes
small closed or curved eyes, tiny smiling mouth, rosy cheeks, gentle and comforting expression
short paws and compact body proportions
no sunglasses, no grayscale treatment, no cool or aggressive attitude
supporting element only, normally placed in the upper-right corner
occupy roughly 12%-20% of the cover
must not block title, product names, topic cards, tables, or screen content
Use the user's sample only as a character-direction reference. Do not force the sample's coffee mug, pose, collar, sparkles, or exact markings. Ask image generation to create a topic-relevant pose, prop, gesture, and interaction while preserving the fixed calico identity.
The cat's warm cream/orange/brown colors are restricted to the mascot and must not replace the navy information-design system.
Inner pages may include a smaller calico cat only when it improves navigation, emotion, or comprehension.
Cover prompts are invalid if they omit the calico identity, upper-right placement, or no-sunglasses rule.
ChatGPT Image Prompt Requirements
Every ChatGPT 生图提示词 must be directly copyable and include:
小红书 3:4 竖版图
Page purpose
Exact Chinese text to render
Composition and hierarchy
Fixed color values: #FFFFFF, #162A46, #E8EDF4; #1A1A1A only when needed for dense body copy
Typography and layout requirements
Calico cat IP instructions for cover
Negative constraints: no watermark, no QR code, no fake logo, no red, no fluorescent lime, no neon green, no sunglasses, no grayscale mascot, no garbled Chinese, no unreadable tiny text
Cover Prompt Skeleton
Use this structure for cover prompts:
生成一张小红书 3:4 竖版封面图。主题是「...」。严格采用精细编辑海报风格：白色背景 #FFFFFF、夜幕蓝 #162A46 作为主文字和品牌强调色、浅夜幕蓝 #E8EDF4 作为卡片底色；#1A1A1A 仅在长正文需要更强对比时使用。主标题写「...」，副标题写「...」，微文案写「...」。标题放在上半区偏左，夜幕蓝粗体中文，2-3 行以内，字号克制，不超过画面高度 35%。封面必须让人一眼识别核心主题：中部或下半区放清晰的主题卡片、产品卡片、学习路线图、流程图、对比表或选择表，屏幕或卡片里必须有具体图样，不要空屏。右上角必须加入账号三花猫 IP 作为辅助插画：圆润蓬松、胖乎乎的三花猫，奶油白底毛，暖橙色与深巧克力棕色斑块，棕色微纹理手绘线条，短爪、紧凑比例，小弯眼或闭眼、微笑嘴、粉色腮红，气质温柔治愈；禁止墨镜、灰度处理和冷酷表情。三花猫占画面 12%-20%，不得遮挡标题、主题信息、产品名、表格或屏幕内容。不要照搬示例中的咖啡杯、姿势、项圈、星星或精确花纹；根据主题和文案创造新的动作、道具与互动。三花猫的暖色只用于吉祥物，不改变夜幕蓝的信息设计系统。整体大留白、层次精细、白色与夜幕蓝配色。禁止红色、荧光绿、霓虹绿、真实品牌 logo、二维码、水印、乱码、错误汉字、巨大标题铺满画面。
Final Audit
Before answering, check:
Are titles strong enough, not like plain section labels?
Is 正文 short enough?
Did the carousel carry the main value?
Is there a complete cover prompt?
Does the cover prompt include the round hand-drawn calico cat IP in the upper-right corner?
Does the cat avoid sunglasses, grayscale treatment, and copying the sample's exact pose or props?
Does the visual prompt use night-screen navy #162A46 and avoid fluorescent lime/neon green?
Are there 3-5 inner pages?
Does every page include exact on-image copy and detailed ChatGPT prompt?
Are hashtags relevant and not spammy?
