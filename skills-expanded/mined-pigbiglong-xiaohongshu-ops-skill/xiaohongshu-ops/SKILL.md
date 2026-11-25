---
name: xiaohongshu-ops
title: 小红书全链路运营（Hermes 适配版）
description: 把 Hermes Agent 变成你的小红书运营助手 — 首页分析、账号诊断、选题灵感、内容创作、自动发布、评论回复、爆款复刻、知识库沉淀。全链路 SOP 覆盖，基于浏览器自动化（CDP）。
tags:
  - xiaohongshu
  - 小红书
  - content-ops
  - social-media
  - browser-automation
  - full-chain
---

# 小红书全链路运营（Hermes 适配版）

> 基于 [Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill) (1.7k⭐) 适配为 Hermes Agent 原生 Skill

## 前置要求

### 1. Chrome CDP 调试端口
```bash
# 启动调试模式 Chrome（独立 profile）
chrome-debug

# 在 Hermes 中连接
# 运行:  /browser connect
# 确认 browser.cdp_url = http://localhost:9222
```

### 2. 登录小红书创作平台
```bash
# 在已连接的浏览器中导航到创作平台
browser_navigate('https://creator.xiaohongshu.com')

# 扫码登录（首次）
# 使用手机小红书 App 扫码
# 登录成功后 cookie 持久化在 debug profile 中，后续无需重复登录
```

### 3. 知识库目录（自动创建）
```bash
mkdir -p ~/xhs-knowledge-base/{accounts,topics,patterns,actions,reviews}
```

---

## 工作流总览

```
┌─────────────────────────────────────────────────────┐
│                    入口                              │
│  自然语言指令 → 自动路由到对应工作流                   │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ 首页推荐流分析    │  │  账号分析 & 诊断  │  │  选题灵感生成     │
│ (workflow 1)    │  │  (workflow 2)    │  │  (workflow 3)    │
└─────────────────┘  └──────────────────┘  └──────────────────┘
        │                    │                      │
        └────────────────────┼──────────────────────┘
                             ▼
              ┌─────────────────────────────┐
              │       内容创作 & 发布         │
              │  (workflow 4)               │
              │  集成 xiaohongshu-emotional  │
              │  -content + flux-image-gen  │
              └─────────────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │  评论回复 & 互动             │
              │  (workflow 5)               │
              └─────────────────────────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │  知识库沉淀                  │
              │  (workflow 6)               │
              │  + 爆款复刻 (workflow 7)    │
              └─────────────────────────────┘
```

---

## Workflow 1: 首页推荐流分析

### 触发词
- "帮我分析一下我小红书首页推荐流"
- "看看首页在推什么"
- "首页推荐有什么趋势"

### 步骤

**Step 1: 打开小红书首页**
```
browser_navigate('https://www.xiaohongshu.com/explore')
```
确认当前页面是推荐流（不是搜索页/个人页/消息页）。

**Step 2: 采样首页前 10-20 条内容**
```python
# 方案 A: 标准方式（browser_snapshot 可用时）
browser_scroll(direction='down')
browser_snapshot(full=true)

# 方案 B: CDP 直连（推荐，更可靠 — 避免 Gemini/Glic 干扰）
# 先用 Target.getTargets 找到正确 tab
tabs = browser_cdp(method='Target.getTargets', params={})
page_tab = [t for t in tabs['result']['targetInfos']
            if t['type'] == 'page' and 'xiaohongshu.com' in t.get('url', '')]
if page_tab:
    tab_id = page_tab[0]['targetId']
    # 滚动加载更多
    browser_cdp(method='Runtime.evaluate', target_id=tab_id,
        params={'expression': 'window.scrollBy(0, 3000)', 'returnByValue': True})
    # 提取标题
    titles = browser_cdp(method='Runtime.evaluate', target_id=tab_id,
        params={'expression': '''
            [...document.querySelectorAll('a[href*="explore/"]')]
              .filter(a => a.textContent?.trim().length > 3 && !a.href.includes('channel_id'))
              .map(a => a.textContent?.trim())
              .filter(Boolean)
              .slice(0, 30)
        ''', 'returnByValue': True})
```

每条卡片记录字段：
- `title`：标题原文
- `hook`：首屏钩子
- `cover_text`：封面大字或主文案
- `cover_type`：图文 / 视频 / 文字配图
- `account_type`：达人 / 普通用户 / 品牌
- `likes`、`comments`、`collects`（若可见）
- `tags`：话题标签

**Step 3: 分析框架**
使用以下 4 维度分析每条内容：
1. **推荐触发**：为什么它出现在首页？
2. **停留钩子**：标题/封面/情绪点
3. **传播机制**：收藏型/转发型/评论型/对号入座型
4. **结构模板**：开头-展开-反转-收口节奏

**Step 4: 输出格式**
```
## 首页画像
- 主导主题：XXX
- 常见情绪：XXX
- 高频内容类型：XXX

## 高信号样本（3-5 条）
1. 标题：XXX
   钩子：XXX
   结构：XXX
   互动：XXX
   可复用点：XXX

## 可复用模式
- 模式 1：XXX
- 模式 2：XXX

## 下步动作
- 建议继续观察：XXX
- 建议尝试选题：XXX
```

**Step 5: 沉淀到知识库**
```
# 写入 ~/xhs-knowledge-base/patterns/
write_file(path='~/xhs-knowledge-base/patterns/<date>-<topic>.md', content='...')
write_file(path='~/xhs-knowledge-base/topics/<date>-topic-ideas.md', content='...')

# 同步到 Holographic Memory
fact_store(action='add', content='...', category='general', tags='xhs,pattern')
```

---

## Workflow 2: 账号分析 & 诊断

### 触发词
- "帮我分析这个账号"
- "看看我的账号表现"
- "账号诊断"

### 步骤

**Step 1: 打开目标账号主页**
```python
# 方式 A: 标准导航
browser_navigate('https://www.xiaohongshu.com/user/profile/<user_id>')

# 方式 B: CDP 直连（当 browser_navigate 被 Gemini 拦截时）
tabs = browser_cdp(method='Target.getTargets', params={})
page_tab = [t for t in tabs['result']['targetInfos']
            if t['type'] == 'page' and 'xiaohongshu.com' in t.get('url', '')]
if page_tab:
    tab_id = page_tab[0]['targetId']
    browser_cdp(method='Page.navigate', target_id=tab_id,
        params={'url': 'https://www.xiaohongshu.com/user/profile/<user_id>'})
    # 等页面加载后用 CDP 提取数据
    import time; time.sleep(2)
    info = browser_cdp(method='Runtime.evaluate', target_id=tab_id,
        params={'expression': 'document.body.innerText.slice(0, 3000)',
                'returnByValue': True})
```

**Step 2: 采样最近 9-15 篇内容**
记录：头像、昵称、简介、粉丝量、获赞收藏总量
每篇：标题、封面、类型、发布时间、点赞/评论/收藏、话题、角度

**Step 3: 五维评分诊断**
| 维度 | 1-5分 | 说明 |
|------|-------|------|
| 定位清晰度 | x/5 | 能否一句话说清账号 |
| 内容结构力 | x/5 | 标题/封面/正文是否稳定 |
| 互动转化力 | x/5 | 评论区是否有被引导 |
| 账号辨识度 | x/5 | 是否像"同一个账号" |
| 增长可持续性 | x/5 | 爆款是否依赖偶发 |

**Step 4: 输出**
```
## 账号快照
- 一句话定位：XXX
- 内容支柱：XXX
- 当前状态：增长期 / 摸索期 / 混乱期 / 稳定期

## 五维评分（带理由）
## 诊断结论
## 下步动作（至少 3 条，按优先级）
```

---

## Workflow 3: 选题灵感生成（平台搜索驱动）

### 触发词
- "给我 5 条小红书选题"
- "最近有什么好发的"
- "结合我的定位给选题"
- "情感赛道最近有哪些方向"
- "搜一下XX方向的热门内容"

### 方法
混合三类信号，通过**小红书内部搜索**获取实时数据：

### Step 1: 多关键词搜索 — 获取平台信号

用 CDP 直连在浏览器中执行搜索（避免 Gemini 干扰）：

```python
# 1. 找到正确的 tab
tabs = browser_cdp(method='Target.getTargets', params={})
page_tab = [t for t in tabs['result']['targetInfos']
            if t['type'] == 'page' and 'xiaohongshu.com' in t.get('url', '')]
if not page_tab:
    # 如果没有小红书 tab，先导航过去
    browser_navigate('https://www.xiaohongshu.com')
    tabs = browser_cdp(method='Target.getTargets', params={})
    page_tab = [t for t in tabs['result']['targetInfos']
                if t['type'] == 'page' and 'xiaohongshu.com' in t.get('url', '')]
tab_id = page_tab[0]['targetId']

# 2. 搜索关键词（URL 中 keyword 要 URL encode）
search_url = 'https://www.xiaohongshu.com/search_result/?keyword=%s&sort=general&type=general'
browser_cdp(method='Page.navigate', target_id=tab_id,
    params={'url': search_url % '情感疗愈'})

# 3. 提取搜索结果（搜索页与 explore 页 DOM 不同！用 body.innerText）
import time; time.sleep(2)
results = browser_cdp(method='Runtime.evaluate', target_id=tab_id,
    params={'expression': 'document.body.innerText.slice(0, 4000)',
            'returnByValue': True})
# 结果中会按顺序显示：标题 + 作者 + 日期 + 互动数
```

**搜索策略：** 至少搜 2-3 个不同角度的关键词

| 目的 | 关键词示例 | 说明 |
|------|-----------|------|
| 赛道全景 | 情感疗愈、两性关系 | 看整体热度分布 |
| 子方向深挖 | 分手、内耗、原生家庭 | 看细分方向竞争 |
| 验证蓝海 | 分离 情感、告别 爱 | 看是否有竞品 |

### Step 2: 解析搜索信号

从搜索结果中提取：
- **标题原文** — 记录爆款标题的句式、情绪词、标点符号（❗🔥等）
- **赞数** — 8.3万、17.4万、5043 等，判断赛道的"天花板"
- **作者类型** — 大V还是素人（素人高赞说明内容质量>账号体量）
- **相关搜索词** — 小红书搜索页底部的相关推荐词（如「释怀文案」「体面告别」「焦虑缓解」）
- **内容类型** — 图文/视频/文字配图

### Step 3: 竞争分析 — 判断红海/蓝海

| 信号 | 红海 | 蓝海 |
|------|------|------|
| 高赞条数 | 前 10 条都有 5000+ | 前 10 条只有几百 |
| 作者体量 | 全是 10万+ 粉大V | 素人也能出爆款 |
| 内容深度 | 全是"被这段话治愈了"同质化 | 找不到"心理学+情感"结合内容 |
| 某一关键词 | 分手 有 1.3万+ | 分离 几乎没有结果 |

### Step 4: 生成选题清单

每个方向产出 **3-5 条**选题，每条包含：

```
1. 选题标题：
   选题角度：支持 / 反对 / 中立 / 争议点
   目标人群：
   互动钩子：
   内容结构：3段式大纲
   风险提示：是否容易引战/踩线
   依据：xx条搜索结果中 xx赞的爆款结构复用
```

### Step 5: 给出起号策略

根据账号阶段（新号/老号/转型号）给出发布顺序建议：

**新号/转型号推荐策略：**
```
第1-3篇   蹭赛道热度型（用已验证的爆款标题骨架，快速拿初始流量）
  ↓
第4-5篇   差异化深度型（展示独特视角，留人）
  ↓
第7篇     个人IP型（建人设辨识度，让人记住你是谁）
  ↓
后续       混发，形成稳定的"XX+XX"内容支柱
```

### 已知标题骨架（经验证有效）

情感赛道已验证的标题公式：
```
突然被这段话[治愈/点醒/平复]了
句句不提[爱/感情]，却句句都是[爱/感情]
原来真的有人[分手/放弃]不是因为不爱了
放下一个人的[超绝/最好]心态
是时候该[放手/结束]了…
你哭的不是[他/那个人]，是[安全感/自己]的崩塌
```

### 输出格式

```markdown
## 赛道全景
- 所属大赛道：情感疗愈
- 子方向热度：方向A(⭐⭐⭐) 方向B(⭐⭐) 方向C(⭐)
- 最大爆款天花板：17.4万赞
- 竞争格局：蓝海信号 / 红海警告

## 推荐选题（按优先级）
1. 标题：XXX
   依据：XXX方向搜索中YYY赞的模式复用
   互动钩子：XXX
   结构：XXX

## 起号策略
第1篇 → 第3篇 → 第7篇 → 后续
```

> **情感赛道深度选题分析模板**：见 `references/topic-analysis-template.md`，包含完整输出结构、搜索策略、蓝海验证方法论。

---

## Workflow 4: 内容创作 & 发布

### 触发词
- "帮我发布一篇笔记"
- "创作一篇关于XX的内容"
- "写一篇小红书"

### 内容创作
根据内容类型路由：

**情感方向** → 集成 `xiaohongshu-emotional-content` skill
- 5 段式结构：Hook → 故事 → 转折 → 真相 → 金句收尾
- 心理学理论支撑（依恋理论/客体关系/存在孤独等）
- 暗色调温暖视觉风格

**通用方向** → 使用通用模板
- 标题（≤20字）
- 正文（短句+换行，max 3行/段）
- 封面文案
- 互动CTA

**封面图生成** → 集成 `flux-image-generation` skill
```
# 使用 FLUX.1-schnell 生成封面
# 提示词：精简英文，2-3句
# 尺寸：1024×1024
# 压缩后上传：768px JPEG quality=90
```

### 发布流程（via 创作平台）

**Step 1: 打开创作平台**
```
browser_navigate('https://creator.xiaohongshu.com/publish/publish')
```

**Step 2: 选择发布类型**
- 图文（默认推荐）
- 视频
- 长文

**Step 3: 上传素材**
```
# 图文上传 — 使用 CDP 处理文件上传
browser_click(ref='@upload-btn')   # 点击上传按钮
# CDP: DOM.setFileInputFiles 或通过 Input.dispatchFileChooserEvent
browser_cdp(method='DOM.setFileInputFiles', params={
  'objectId': '...',
  'files': ['/path/to/image.jpg']
})
```

**Step 4: 填写内容**
```
browser_type(ref='@title-input', text='标题（≤20字）')
browser_type(ref='@body-input', text='正文内容...')
```

**Step 5: 三要素校验 & 停在发布按钮**
确认三项齐全：
- ✅ 封面
- ✅ 标题（≤20字）
- ✅ 正文

**停在「发布」按钮，等待用户确认后点击**

---

## Workflow 5: 评论回复 & 互动

### 触发词
- "帮我看看最新评论"
- "回复评论"

### 流程
**Step 1: 打开通知页**
```
browser_navigate('https://creator.xiaohongshu.com/notifications')
```

**Step 2: 抓取最新评论**
记录：用户名、评论文本、时间

**Step 3: 输出检查结果**
- 新评论条数
- 最新 3-5 条摘要
- 高风险信号（辱骂、钓鱼、违规）

**Step 4: 用户确认后回复**
按照 `persona` 设定的语气逐条回复

**风控规则：**
- 默认一次只发 1 条
- 连续回复间隔 8-15 秒
- 遇到"操作频繁/请稍后再试"立即停止
- 回复 ≤280 字

---

## Workflow 6: 知识库沉淀

### 目录结构
```
~/xhs-knowledge-base/
├── README.md           # 总览入口
├── accounts/           # 账号定位、诊断、竞品分析
├── topics/             # 选题、标题骨架、内容方向
├── patterns/           # 爆款结构、封面模板、互动钩子
├── actions/            # 发布、回复、下载、复刻记录
└── reviews/            # 复盘、失败原因、下次调整
```

### 文件命名
```
accounts/2026-03-19-account-analysis-xxx.md
topics/2026-03-19-topic-ideas-xxx.md
patterns/2026-03-19-title-hook-pattern.md
actions/2026-03-19-publish-xxx.md
reviews/2026-03-19-reply-retro.md
```

### 同时同步到 Holographic Memory
```python
from hermes_tools import fact_store, write_file
# 结构化记录写文件
write_file(path='~/xhs-knowledge-base/...', content='...')
# 关键结论同步到 fact_store
fact_store(action='add', content='...', category='general', tags='xhs,pattern')
```

---

## Workflow 7: 爆款笔记复刻

### 触发词
- "帮我复刻这篇爆款"
- "复制这个笔记的风格"

### 四步流程
1. **输入** 爆款笔记 URL
2. **分析** 爆款因素（标题/封面/正文/互动机制）
3. **生成** 新封面（使用 FLUX，style-only 模式）
4. **发布** 新笔记

### 封面抓取规则
```
// 轮播页强制使用 active slide
const activeImg = document
  .querySelector('.swiper-slide-active:not(.swiper-slide-duplicate) .swiper-container img')
  ?.currentSrc;
```

### 改写规则
- **保留**：同主题、同互动机制、同内容结构
- **替换**：具体措辞、案例细节、表达顺序
- **禁止**：逐句照抄、原图二次使用、作者专属信息迁移

---

## Persona 设置

默认 persona 适用于通用运营。**如果你运行情感赛道**，请先加载 `xiaohongshu-emotional-content` skill，它会覆盖内容风格设置。

可以通过以下方式自定义 persona：
```
# 写入自定义 persona
write_file(path='~/xhs-knowledge-base/persona.md', content='
# 我的小红书人设
- 身份：XXX
- 气质：XXX
- 语气：短句/有温度/直接
- 禁忌：XXX
')
```

---

### 失败降级策略

| 问题 | 处理方式 |
|------|---------|
| 页面结构变化 | 先 `browser_snapshot` 刷新 ref，不盲跑旧路径 |
| 连续 2 次点击失败 | 停止盲试，告诉用户"页面结构可能变了" |
| 上传路径错误 | 先复制文件到 `/tmp/xhs-uploads/` 再上传 |
| 发布页元素失效 | snapshot 刷新引用，仍失败则让用户手动点"发布" |
| 采样不足 | 标注"样本偏少，结论仅供试跑" |
| 登录失效 | 提示重新扫码登录 |
| 评论过于频繁 | 停止，等待 15 分钟后再试 |
| `browser_navigate` 失败(`ERR_BLOCKED_BY_CLIENT`) | Chrome Gemini/Glic 侧栏干扰。先用 `Target.getTargets` 找到正确 tab ID，切到 CDP 直连：`browser_cdp(method='Target.activateTarget', params={'targetId': tab_id})`，再 `browser_cdp(method='Page.navigate', target_id=tab_id, params={'url': '...'})` |
| `browser_snapshot` 返回 Gemini 面板而非页面 | 说明 Gemini 侧栏正在覆盖页面。关闭方法：在 `Target.getTargets` 中找到 `type: 'webview'`、url 含 `glic` 或 title 含 `Gemini` 的 target → `Target.closeTarget`；然后激活正确的页面 tab 继续操作 |
| Gemini 干扰下提取数据 | 放弃 `browser_snapshot`，直接用 CDP：`browser_cdp(method='Runtime.evaluate', target_id=page_tab_id, params={'expression': '...', 'returnByValue': true})`。**必须传 `target_id`**——即使 Gemini 被关闭后 Chrome 也会自动重启 Glic，不传会 hit 错误 target 导致 `'Runtime.evaluate' wasn't found`。每次调用前用 `Target.getTargets` 确认目标 tab 的 targetId 仍然有效 |

---

## 快速启动检查清单

- [ ] Chrome 调试模式运行中（`chrome-debug`）
- [ ] Hermes CDP 已连接（`/browser connect` 或 config 自动）
- [ ] 已登录 `creator.xiaohongshu.com`（首次扫码）
- [ ] `~/xhs-knowledge-base/` 目录已创建
- [ ] 如果是情感赛道：已加载 `xiaohongshu-emotional-content`
- [ ] 如果需要封面图：已加载 `flux-image-generation`

---

## ⚠️ Chrome 147+ Gemini/Glic 覆盖层问题

Chrome 147 以上版本内置的 Gemini 助手（chrome://glic/）会在标签页上叠加一层 AI 面板，导致 `browser_navigate` 失败（`ERR_BLOCKED_BY_CLIENT`）、`browser_snapshot` 只返回 Gemini 面板而不是页面内容。

**判断方法：**
- `browser_snapshot()` 返回的 `frame_tree.top` 为 `null`
- snapshot 内容只剩 Gemini 面板的按钮和文字
- `browser_navigate(url)` 返回 `net::ERR_BLOCKED_BY_CLIENT`

**解决方案（分两步）：**

### Step 1: 关闭 Gemini 并重新导航
```python
# 1. 用 CDP 探索所有标签页，找到并关闭 Gemini/Glic
tabs_result = browser_cdp(method='Target.getTargets', params={})
for tab in tabs_result['result']['targetInfos']:
    if 'glic' in tab.get('url', '') or 'Gemini' in tab.get('title', ''):
        browser_cdp(method='Target.closeTarget', params={'targetId': tab['targetId']})

# 2. 激活小红书标签页（如果已存在）
for tab in tabs_result['result']['targetInfos']:
    if 'xiaohongshu.com' in tab.get('url', ''):
        target_id = tab['targetId']
        browser_cdp(method='Target.activateTarget', params={'targetId': target_id})
        break

# 3. 用 CDP 直接导航
browser_cdp(method='Page.navigate', target_id=target_id, params={'url': 'https://www.xiaohongshu.com/explore'})

# 4. 用 CDP evaluate 提取数据
data = browser_cdp(method='Runtime.evaluate', target_id=target_id, params={
    'expression': 'document.title',
    'returnByValue': True
})
```

### Step 2: 切换到 CDP 直连模式
如果 Gemini 反复出现，直接切换到 CDP 模式：
- 用 `Target.getTargets` 获取标签页列表
- 用 `Target.activateTarget` 激活目标页
- 用 `Page.navigate` 导航
- 用 `Runtime.evaluate` 提取数据
- 用 `document.body.innerText` 获取搜索列表

---

## 引用

- 原始项目：[Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill)
- MCP 底座：[xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)
