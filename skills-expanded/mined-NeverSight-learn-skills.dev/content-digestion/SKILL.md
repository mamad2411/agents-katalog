---
name: content-digestion
version: 1.0.2
author: Vinson Liang
license: MIT
description: A Claude Skill that digests long-form content (podcasts, videos, articles, transcripts) into structured notes. Two modes — Knowledge Mode (archive into your knowledge base) and Publishing Mode (turn into a long-form read or shareable post). Output language follows the user's conversation language. 把任何长内容（文章、播客、视频文字稿、网页）消化成结构化笔记。两种模式：沉淀模式（存进知识库以后用）/ 发布模式（现在快速读完，或整理成可发布的长文）。输出语言根据用户对话语言自动判断（中文 / 英文 / 任何语言均可）。Triggers when the user provides a URL, pastes a transcript, uploads a file, or asks to digest, summarize, take notes on, or process content. 也适用于「帮我消化这个内容」「整理成笔记」「把这篇文章变成笔记」等场景。
---

# Content Digestion Skill

Digest any long content (article, podcast, video transcript, webpage) into structured notes.

This Skill serves the two most common needs of content creators and knowledge workers: **archiving** (saving content into a knowledge base for later use) and **consuming/publishing** (reading a long piece quickly, or producing a publishable long-form note).

---

## Language Handling (CRITICAL — read this first)

**This Skill produces output in the language the user is conversing in, not the language of the source content.**

Determine the output language using this priority order:

1. **Explicit user instruction** (highest priority): if the user says "output in English" / "用英文输出" / "give me a Chinese summary" / "用中文消化", follow that instruction exactly, regardless of conversation language.

2. **Conversation language**: if no explicit instruction, output in whatever language the user is using to talk to you. If the user writes the request in Chinese, output Chinese notes. If the user writes in English, output English notes.

3. **Source content language** (fallback only): if the conversation has been mixed/ambiguous and you genuinely cannot tell, default to the source content's language.

**Common scenarios:**

| User chats in | Source content is | Output |
|---|---|---|
| English | English | **English** |
| English | Chinese | **English** (translate while preserving meaning) |
| Chinese | English | **Chinese** (translate while preserving meaning) |
| Chinese | Chinese | **Chinese** |

**When translating between languages, preserve:**
- The original speaker's tone and rhythm
- Specific data, names, technical terms (keep names in original script for English/Chinese; provide translation parenthetically on first mention if needed)
- The emotional weight of high-impact quotes — translation should not flatten them

**The methodology of this Skill (frontmatter, wikilinks, quote sandwiches, "preserve by default" principle, integration suggestions) is language-agnostic.** All rules below apply equally to English and Chinese output. Where this document gives examples in one language, the same pattern applies to the other language.

---

## Before digesting: confirm intent

**If the user has not specified a mode**, ask once briefly. Use the language matching the user's conversation language:

**English version of the question:**

> I can help you digest this content. Quick question first:
>
> 1. **Archive it for later** — turn it into structured notes that drop into your knowledge base / Notion / Obsidian / a folder, so you can pull them up anytime
> 2. **Read it now / publish it** — turn it into a long-form note with structure and key points, so you can read this episode in 10 minutes, or share it / post it on your social platforms
>
> If unsure, choose 1.

**Chinese version of the question:**

> 我可以帮你消化这份内容。开始之前问一下：
>
> 1. **沉淀下来，以后再用** —— 整理成结构化笔记存进你的知识库 / Notion / Obsidian / 文件夹，以后随时调用
> 2. **现在就读完 / 发出去** —— 整理成有框架、有重点的长文笔记，你 10 分钟就能读完这期内容，也可以直接分享出去，或者发布到你自己的社交平台
>
> 如果不确定，选 1。

**Skip the question when the user has clearly specified intent.** Trigger keywords (in any language):

**Knowledge Mode triggers** (English): "digest", "archive", "file this", "save for later", "into my knowledge base", "for my notes", "structured notes", "Obsidian-ready", "Notion-ready"
**Knowledge Mode triggers** (Chinese): 「消化」「整理」「入库」「沉淀」「存起来」「做成笔记」「结构化笔记」

**Publishing Mode triggers** (English): "long-form", "publishable", "magazine read", "blog post", "newsletter", "article", "post on twitter / LinkedIn / social", "10 minute read", "summarize as a long-form", "essay-style"
**Publishing Mode triggers** (Chinese): 「写成笔记」「写成长文」「发公众号」「发小红书」「发推特」「发到社交平台」「读完」「总结成可读的文章」

**Both modes**: "do both" / "two versions" / 「两个都要」 / 「两种模式都做一份」

---

## Supported input methods

Process inputs in this priority order:

### 1. Direct URL (article / webpage / blog)

Use the `web_fetch` tool to retrieve the page content, then digest per the rules below.

### 2. Pasted transcript or full article text

The user pastes content directly (podcast transcript, video subtitles, article body) — digest per the rules.

### 3. Uploaded file

The user uploads PDF, TXT, DOCX, SRT, or similar files. Read the content, then digest per the rules.

#### SRT subtitle file parsing

- Use `re.split(r'\n\n+', content)` to split subtitle blocks
- Bilingual SRT (English/Chinese alternating): odd-indexed blocks = English, even-indexed = Chinese
- Strip timestamp lines and sequence numbers when extracting plain text

### 4. YouTube / podcast links

If the environment allows direct YouTube access, use `web_fetch` or similar tools. If direct access fails (many sandboxed environments block YouTube domains), try the following in order:

#### Strategy A: search for third-party transcript hosting pages (preferred)

1. Extract the video ID from the URL
2. Use `web_search` with the video title or ID + "transcript"
3. Look in the results for pages hosting full transcripts. Common sources:
   - **podscripts.co** / **podcasttranscript.ai** — podcast transcript aggregators, generally high quality
   - **youtubetotranscript.com** / **notegpt.io** — YouTube subtitle extractors
   - Blogs or news sites that quoted the video
4. Use `web_fetch` on the transcript URL to retrieve the full text

**Tip**: well-known podcasts (No Priors, Lex Fridman, All-In, Diary of a CEO, etc.) almost always have third-party transcripts. Search with "podcast name + guest name + transcript" for best results.

#### Strategy B: ask the user for help

If Strategy A fails, tell the user (in the user's conversation language):

> I couldn't fetch the transcript automatically. You can provide it this way:
>
> - On the YouTube video page, click "Show transcript" and paste the text here
> - Or get it from youtubetotranscript.com and paste it here
> - Or upload an SRT subtitle file
>
> Once I have the transcript, I'll digest it immediately.

**Core principle**: don't just say "I can't do it" and give up. Try Strategy A first; only ask the user after it fails.

---

## Mode 1: Knowledge Mode 沉淀模式

**Goal**: digest the content into structured, retrievable notes useful to future-you, your AI assistant, or your knowledge base system.

**Key features**:
- YAML frontmatter carrying metadata
- Body uses `[[wikilinks]]` to mark key entities and concepts
- Ends with a "Suggested Wiki Updates / 知识库整合建议" section
- Ends with a "Where to put this note next" guidance section

### Output template

**Section labels (TL;DR, Core arguments, etc.) use the output language naturally.** When outputting in Chinese, use 「TL;DR / 核心论点 / 颠覆认知的点 / 实操要点 / 知识库整合建议」. When outputting in English, use "TL;DR / Core arguments / Counterintuitive points / Action items / Suggested Wiki Updates".

**Example template (English output)**:

```markdown
---
source: "[Original URL or citation]"
type: "podcast | video | article | paper | book"
authors: ["Name 1", "Name 2"]
date_published: "YYYY-MM-DD"
date_ingested: "YYYY-MM-DD"
language: "en | zh | mixed"
summary_for_index: "One-sentence summary for the wiki index file"
entities: ["[[Entity 1]]", "[[Entity 2]]"]
concepts: ["[[Concept 1]]", "[[Concept 2]]"]
concepts_to_create: ["[[Concept 1]]", "[[Concept 2]]"]
tags: [tag1, tag2, tag3]
---

# [Content Title]

## TL;DR

3-5 sentences summarizing what this content is about and why it matters.
Anyone (including future-you) should be able to skim this and decide
"is this worth opening?"

## Core arguments

Organized by theme. Each section uses the three-part pattern:
- Lead-in → quote → interpretation
- Mark key entities and concepts with [[wikilinks]] on first mention
- Bold critical data and conclusions

### I. [Theme 1]

Body text... with [[wikilinks]] on entities and concepts...

> Quote, preserving the speaker's tone
> —— [[Speaker]]

Editor's interpretation...

### II. [Theme 2]

...

## Counterintuitive points

- Unexpected conclusions
- Specific data that supports them

## Action items

Actionable advice prioritized.

---

## 🔗 Suggested Wiki Updates / 知识库整合建议

> This section tells the user how to integrate this digest into their knowledge base.
> Default to **inference** (user usually hasn't provided wiki context).

### Suggested concept pages to create

- `[[Concept 1]]` — brief reason
- `[[Concept 2]]` — brief reason

### Potential cross-references

This content connects strongly with these topics — consider adding backlinks:
- `[[Topic A]]`
- `[[Topic B]]`

### Open questions worth exploring

This content surfaces some open questions worth further research:
1. Question 1
2. Question 2

---

## 📂 Next: where should this note go?

[This section uses a fixed structure — see "Knowledge Mode internal rules → 'Next steps' section structure" below]
```

**Example template (Chinese output)**:

```markdown
---
source: "[原始 URL 或出处]"
type: "podcast | video | article | paper | book"
authors: ["姓名 1", "姓名 2"]
date_published: "YYYY-MM-DD"
date_ingested: "YYYY-MM-DD"
language: "zh | en | mixed"
summary_for_index: "一句话摘要，给 wiki 索引文件用"
entities: ["[[实体 1]]", "[[实体 2]]"]
concepts: ["[[概念 1]]", "[[概念 2]]"]
concepts_to_create: ["[[概念 1]]", "[[概念 2]]"]
tags: [tag1, tag2, tag3]
---

# [内容标题]

## TL;DR

3-5 句话概括这份内容讲了什么、为什么重要。让任何人（包括未来的你）
扫一眼就能判断「要不要点进去看」。

## 核心论点

按主题板块组织。每个板块内：
- 概括 → 引语 → 解读 的三段式
- 关键实体首次出现用 [[双链语法]]
- 关键概念也用双链
- 重要数据和结论用 **加粗** 标记

### 一、[主题板块 1]

正文……用 [[双链]] 标注实体和概念……

> 引语，保留原话精度
> —— [[说话人]]

编者解读……

### 二、[主题板块 2]

…

## 颠覆认知的点

- 反常识结论
- 数据支持（具体数字一定保留）

## 实操要点

按优先级列出可行动的建议。

---

## 🔗 知识库整合建议 / Suggested Wiki Updates

> 这一段告诉用户：这份消化产物如何融入他的知识库。
> 默认基于内容**推测**（用户不一定提供 wiki 上下文）。

### 建议建立的概念页

- `[[概念 1]]` —— 简短理由
- `[[概念 2]]` —— 简短理由

### 可能的交叉引用

这份内容与以下主题强相关，建议在那些页面建立 backlink：
- `[[主题 A]]`
- `[[主题 B]]`

### 延伸阅读问题

这份内容引出了一些值得进一步研究的开放问题：
1. 问题 1
2. 问题 2

---

## 📂 下一步：把这份笔记放到哪里？

[此段落使用固定结构，详见下方「沉淀模式的内部规则 → 「下一步」段落的固定结构」]
```

**Section heading naming convention**:

| English | Chinese |
|---|---|
| TL;DR | TL;DR |
| Core arguments | 核心论点 |
| Counterintuitive points | 颠覆认知的点 |
| Action items | 实操要点 |
| 🔗 Suggested Wiki Updates | 🔗 知识库整合建议 / Suggested Wiki Updates |
| ↳ Suggested concept pages to create | ↳ 建议建立的概念页 |
| ↳ Potential cross-references | ↳ 可能的交叉引用 |
| ↳ Open questions worth exploring | ↳ 延伸阅读问题 |
| 📂 Next: where should this note go? | 📂 下一步：把这份笔记放到哪里？ |

### Knowledge Mode internal rules

**About frontmatter**:
- Fill all fields when possible. If a field can't be determined from the content (e.g., publication date), use `null` or omit it — don't fabricate
- `summary_for_index` is a **one-sentence** summary (under 30 words), specifically for the wiki index file / retrieval system. It's NOT the TL;DR — TL;DR is 3-5 sentences for human reading, while this one-line is for an LLM agent to quickly identify the source in an index
- `entities` are the specific named things in the content: people, organizations, products
- `concepts` are the key concepts, theories, terms appearing in the content
- `concepts_to_create` is a subset of `concepts` — only the ones **worth creating an independent concept page for** (not every concept needs a dedicated page). This field maps to the "writes articles for them" step in Karpathy's LLM Wiki pattern
- `tags` are classification labels, lowercase, snake_case

**About wikilinks**:
- Don't wrap every noun in wikilinks. Only mark entities and concepts **worth being their own page**
- The same entity gets a wikilink **on first mention** in the body; subsequent references can skip
- Wikilink syntax is Obsidian standard, but it also reads as clear visual emphasis in other systems

**About the "Suggested Wiki Updates" section**:
- **If the user provides an existing wiki directory or index**, give specific suggestions for updating existing pages and flagging contradictions based on the real structure
- **If the user has not provided wiki context** (the default case), only generate three subsections: "Suggested concept pages to create", "Potential cross-references", "Open questions worth exploring", and explicitly mark at the top: "This section is based on **inference** from the content"
- Don't pad suggestions for the sake of it. Quality over quantity.

**About the "Next steps" section**:
- This section matters equally for all users. **Do not omit it. Do not abbreviate it.**
- The content is relatively fixed (4 standard destinations + 1 Karpathy advanced section). Don't reinvent it each time
- If the user has explicitly stated which tool they use, you can keep only the matching destination, but **always keep the Karpathy advanced section**

**About suggested filename**:
- At the start of the "Next steps" section, proactively suggest a filename
- Naming convention: `author-topic-source-year.md`, all lowercase, hyphen-separated
- Examples: `sinclair-aging-doac-2024.md`, `karpathy-llm-wiki-gist-2025.md`
- This is the de facto standard in Obsidian / Karpathy-style workflows; LLM agents rely on stable filenames for backlink maintenance
- 例如:`sinclair-aging-doac-2024.md`,`karpathy-llm-wiki-gist-2025.md`
- 这是 Obsidian / Karpathy 风格的事实标准,LLM agent 在维护反向链接时依赖稳定文件名

**"Next steps" section structure** (Knowledge Mode output must include this at the end):

The "Next steps" section uses a fixed structure with two language versions. Use the version matching the output language.

**English version**:

```markdown
---

## 📂 Next: where should this note go?

**Suggested filename**: `[author-topic-source-year].md`

- **If you use Notion**: copy the entire content into a new page. The metadata
  between `---` can be converted to Notion page properties. `[[wikilinks]]`
  need to be manually converted to internal links in Notion.

- **If you use Obsidian**: save this as a `.md` file and drop it into your vault.
  The frontmatter and `[[wikilinks]]` work natively. The Dataview plugin can
  generate indexes from the frontmatter fields.

- **If you just want to save it in Apple Notes / Pocket / a notes app**: copy
  the body content starting from `# Title`, skipping the frontmatter at the top.

- **If you don't have a knowledge base system yet**: save as `.md` or `.txt`
  in a fixed folder (e.g., `~/notes/`). Later, search by filename or feed the
  whole folder to an AI tool to ask questions.

### 🧠 If you're using the Karpathy LLM Wiki workflow

Save this file to `raw/[suggested-filename].md`, then tell your LLM agent:

> Please compile `raw/[filename].md` into `wiki/`:
>
> 1. Add an index entry to `wiki/index.md` using the `summary_for_index` field
>    from the frontmatter
> 2. For each concept in the `concepts_to_create` list, create or update the
>    corresponding concept page under `wiki/concepts/`, integrating relevant
>    passages from this source
> 3. Update backlinks under `wiki/sources/` for this source
> 4. Check for contradictions with existing wiki content; if any, log them in
>    `wiki/log.md`

This prompt works directly with the workflow described in Karpathy's gist —
no additional configuration needed. Your LLM agent (Claude Code / Cursor /
others) will understand it.

> Karpathy's original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
```

**Chinese version**:

```markdown
---

## 📂 下一步：把这份笔记放到哪里？

**建议文件名**：`[作者-主题-来源-年份].md`

- **如果你用 Notion**：复制全文到一个新页面。`---` 之间的元数据可以转成
  Notion 页面属性。`[[双链]]` 在 Notion 里需要手动转成内部链接。

- **如果你用 Obsidian**：保存为 `.md` 文件丢进 vault。frontmatter 和
  `[[双链]]` 都会原生工作，Dataview 插件可以根据元数据生成索引。

- **如果你只想存在 Apple Notes / 微信收藏 / 备忘录**：复制 `# 标题`
  以下的主体内容，跳过最上面的 frontmatter。

- **如果你还没有知识库系统**：保存为 `.md` 或 `.txt` 文件放到一个固定文件夹
  （比如 `~/notes/`）。以后想回忆任何内容，直接搜文件名，或者把整个文件夹
  喂给 AI 工具问问题。

### 🧠 如果你在用 Karpathy LLM Wiki 工作流

把这份文件保存到 `raw/[建议文件名].md`，然后告诉你的 LLM agent：

> 请把 `raw/[文件名].md` 编译进 `wiki/`：
>
> 1. 在 `wiki/index.md` 添加这份内容的索引条目，使用 frontmatter 里的
>    `summary_for_index` 字段
> 2. 为 `concepts_to_create` 列表里的每个概念，在 `wiki/concepts/` 下创建
>    或更新对应的概念页，把这份内容里的相关段落整合进去
> 3. 更新 `wiki/sources/` 下这份内容的反向链接
> 4. 检查是否和 wiki 中已有内容存在矛盾，如有，在 `wiki/log.md` 标记

这段 prompt 是基于 Karpathy gist 的描述直接可用的——不需要任何额外配置。
你的 LLM agent（Claude Code / Cursor / 其他）会读懂它。

> Karpathy 原文：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
```

---

## Mode 2: Publishing Mode 发布模式

**Goal**: turn long content (a 2-3 hour podcast/video, or a long article) into a long-form note with structure, logic, and human warmth.

**Use cases**:
- You want to read a 2-3 hour piece in 10 minutes (for yourself)
- You want to share it directly on social platforms or with friends (for an audience)

Both use cases share the same output format.

### Article structure

**Opening intro section**:
- One-sentence summary (what is this content)
- Source citation + speaker/author intro (full name + short reference name to use throughout)
- If the content is part of a series, note which part this covers
- **Do NOT include a "one-sentence recommendation" section** (it feels stiff and breaks reading flow)

**Body**:
- Organized by **theme**, not by timeline (no chronological play-by-play)
- Each theme section has clear sub-points
- Speaker/author quotes interspersed throughout
- Editor's transition sentences connect the sections

**Ending**:
- A short editor's reflection

### Heading hierarchy

**For Chinese output**:
- **Level 1**: Chinese numerals 「一、二、三……」, bold large text, theme-level sections
- **Level 2**: Arabic numerals 「1. 2. 3.」, bold, sub-points within a section
- **Level 3** (occasionally): 「1）2）3）」 for finer breakdowns

**For English output**:
- **Level 1**: Roman numerals "I. II. III." OR descriptive headings ("Part One: ..." / "The Information Theory of Aging" etc.), bold, theme-level sections
- **Level 2**: Arabic numerals "1. 2. 3." or descriptive sub-headings, bold
- **Level 3** (occasionally): "a) b) c)" for finer breakdowns

**Principle**: use heading conventions natural to the output language. Don't force Chinese numerals into English notes or vice versa.

### Quote handling (the core technique)

Quotes are what distinguish this kind of note from a generic summary. Rules:

- Use blockquote (`>`) to present the translated/transcribed original
- Tag the speaker before the quote (using the short reference name set up in the intro)
- **Before** the quote: a one-sentence editorial lead-in framing what's coming
- **After** the quote: optional editorial interpretation or transition
- Only put the **high-impact, emotionally-charged** passages in quote blocks — not every line
- Translation preserves the speaker's tone and rhythm

**Example (Chinese output)**:

```
更年期专家 Dr. Haver 回忆起她做妇科实习医生时的经历：

> 当我将这个病例向一位资深医生汇报时，他私下使用了「WW」
> 这一缩写，意指"爱抱怨的女性"……其潜台词是：这是这个
> 年龄段女性"正常会经历的情况"，医生实际上无法、也无需
> 提供实质性的帮助。

**当时她并未质疑这种解释，直到将近二十年后才意识到，
这种思维方式已经深深嵌入整个医学体系之中。**
```

**Example (English output)**:

```
Sinclair recalls the moment he received the photo from his lab:

> I was in Australia — my home country — and I got a photo on my old
> iPhone. It was a mouse that looked very uncomfortable, with a message:
> "Problem — we have a sick mouse." I replied: "That's not a sick mouse,
> that's an old mouse." That was the moment I knew the information theory
> of aging was right.

**That moment, captured in a single line, is what distinguishes a real
discovery from incremental progress: he didn't see disease, he saw aging.**
```

If the input is an article rather than a conversation, replace speaker quotes with key paragraphs from the author. Logic stays the same.

### Bold emphasis logic

Use bold to give readers visual anchors:
- Counterintuitive conclusions
- Key data points and statistics
- Core actionable advice
- Editor's summary judgments
- Particularly important sentences inside quotes

### Editor's voice

- Use transition phrases to connect sections: "换句话说" / "Put another way", "这又回到了前面讨论的……" / "This brings us back to..."
- Occasionally include personal observations or recommendations
- Tone: sincere but not preachy — "magazine long-form" feel

### Content selection: preserve by default

**Default attitude is "preserve as much as possible"**:

- Human-color details, emotionally resonant moments — distill them in
- Counterintuitive information, specific data, actionable advice — keep all of it
- Only delete genuine repetition (where the same point is made multiple times); merge to avoid bloat
- **Never write a dry "key points summary". Preserve the warmth and depth of the original content.**

### Layout

- Generous whitespace between paragraphs
- Use lists only when necessary
- "Magazine long-form" reading feel, not "PowerPoint bullet dump"
- For Chinese output: insert spaces between Chinese and English characters (e.g., "Sinclair 提出" not "Sinclair提出")
- For English output: standard English typography
- First mention of proper nouns: provide original term parenthetically when crossing languages
- **No horizontal dividers** (Markdown `---` or `<hr>`)
- **Sections connect directly through headings**, no separator decoration

### Output format

- Standard Markdown — paste-ready into any Markdown editor or formatting tool
- If the environment supports it, create a `.md` file in the outputs directory for the user to download

### Cross-language handling 跨语言处理

**When the source content language differs from the output language, follow these rules:**

- Translate naturally — no literal/awkward translations. The note should read as if it were originally written in the output language.
- **Quotes preserve tone and rhythm** — when translating a quote, the translated version should carry the same emotional weight and pacing as the original. Don't flatten Sinclair's "that's not a sick mouse, that's an old mouse" into "Sinclair confirmed the mouse showed signs of aging."
- **Names**: keep proper names in their original script (English names stay in Roman letters even in Chinese notes; Chinese names stay in Hanzi even in English notes).
- **Technical terms**: on first mention, provide the original term parenthetically — e.g., "表观基因组 (epigenome)" in a Chinese note about an English source, or "epigenome (表观基因组)" in an English note about a Chinese source. After first mention, use the natural form for the output language.
- **Cultural references**: if the source uses a culturally-specific reference the target audience won't know, briefly explain it inline rather than removing it.
- **Quote attribution**: speaker names in `> quote\n> —— [[Speaker]]` format work in any language.

---

## Workflow 工作流程

### For conversation / podcast / video content (transcript input):

1. Read the full transcript and understand the overall structure and themes
2. Reorganize by **theme** (not by timeline), split into sections
3. Extract key quotes (Knowledge Mode: preserve original precision; Publishing Mode: pick the high-impact passages)
4. Write editorial transitions and interpretations
5. Mark key elements (Knowledge Mode: wikilinks + bold; Publishing Mode: bold)
6. Write opening intro and closing reflection
7. Knowledge Mode: generate frontmatter + Suggested Wiki Updates + Next steps
8. Review: any repetition? any human-warmth details missed?

### For article / webpage content:

1. Read the full piece and understand the core arguments
2. Decide whether to reorganize (if original structure is clear, keep it; otherwise reorganize by theme)
3. Extract key paragraphs as quotes
4. Other steps same as above

---

## What this Skill is NOT for

To avoid wrong expectations, the explicit boundaries:

- **Not a 200-word minimal summary tool**: this Skill's core principle is "preserve by default", especially human-warmth details. If you just need a one-paragraph summary, use a different tool
- **Not a literal translator**: if you need a word-for-word bilingual translation, use a dedicated translation tool
- **Does not judge content quality for you**: this Skill assumes you've already chosen content worth digesting; its job is to digest efficiently, not to filter "is this worth reading"
- **Does not maintain your knowledge base**: the "Suggested Wiki Updates" section is suggestions, not automated wiki maintenance. True automation requires a larger system (see the wiki maintainer role in Karpathy's LLM Wiki pattern)

---

## License

MIT License. Free to use, modify, distribute, including commercially. Just keep the copyright notice.
