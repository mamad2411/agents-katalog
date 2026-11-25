---
name: amazon-listing-alexa-optimizer
description: 检查和优化亚马逊 Listing，适配 Alexa for Shopping / AI 购物时代的要求。当用户提供 Amazon Listing 内容（标题、Item Highlights、五点描述、A+、后台属性、Q&A、评论等）请求检查、优化、改写、诊断、评分时调用。覆盖 2026 标题 75 字符新规、Item Highlights 125 字符、AI 可理解信号构建、场景化表达、后台属性完整性、广告 Prompts 等 8 大维度，输出详细评分报告与改写建议。
---

# Amazon Listing 优化检查器

本 skill 用于在 Alexa for Shopping / AI 购物时代下，对亚马逊 Listing 做全面检查与优化。核心目标：让 Listing 从"关键词堆砌"升级为"可理解的商品信号"，使 AI 导购能理解、引用、比较并推荐该产品。

## 何时触发

当用户出现以下意图时调用：
- 提供 Listing 内容（标题/五点/Item Highlights/A+/后台属性等）请求"检查""优化""诊断""评分""改写"
- 询问标题 75 字符新规、Item Highlights、Alexa for Shopping、AI 购物相关 Listing 调整
- 提供竞品 Listing 请求对比分析
- 询问 Listing 是否"被 Alexa 推荐""适合 AI 购物"

## 核心理念

AI 导购（Alexa for Shopping）推荐产品的标准不是"关键词最多"或"标题最长"，而是：**它能理解、能解释、能比较、能让用户放心下单的产品**。

AI 看完 Listing 后必须能回答四个问题：
1. **你到底是什么产品？**
2. **你适合什么人、什么场景？**
3. **你解决了什么具体问题？**
4. **你和同类产品相比，凭什么值得推荐？**

四个问题回答不清楚，Alexa 很难把该产品放进推荐。

## 数据采集工作流（强制 v3，2026/8/5 修订）

**核心原则**：Amazon 反爬机制会拦截所有简单 HTTP 请求（webReader / WebFetch / curl 等），返回的只是 footer 文本。**必须使用真实浏览器自动化爬取数据**，否则报告基于残缺数据，评分失真。

### 采集方式优先级（按顺序尝试）

#### 优先级 1：用户主动提供 Listing 文本（最佳）

用户直接粘贴或上传：
- Listing 页面截图（含标题、五点、A+、产品详情）
- Seller Central 后台字段截图
- Listing 文本（标题、五点、A+ 文案）

→ 直接进入分析流程，跳过爬取。

#### 优先级 2：浏览器自动化爬取（默认路径）

当用户只提供 Amazon URL 而未提供 Listing 文本时，**必须启动浏览器自动化**：

**首选工具：`browser_use` subagent**
```
Task(
  subagent_type="browser_use",
  description="浏览器爬取Amazon Listing",
  query="打开浏览器访问 [Amazon URL]，完整提取以下内容：
    1. 标题（完整文本+字符数）
    2. 品牌
    3. Item Highlights（2026 新字段）
    4. 五点描述（5 条完整文本）
    5. A+ 内容（文案/图片说明/场景模块）
    6. Product Information 表格全部字段
    7. 价格
    8. 评论统计（星级+数量）
    9. BSR 排名
    10. Q&A 内容
    11. 变体信息
    12. Amazon's Choice 标签
    
    注意：
    - 用真实浏览器导航，模拟人类操作
    - 如遇 CAPTCHA，等待几秒后重试，或截图说明
    - 等待元素加载完成
    - 字段不存在标注'未找到'
    - 最后给出页面截图"
)
```

**次选工具：`kimi-webbridge` skill**
- 优势：使用用户真实浏览器的登录会话，反爬最少
- 适用：用户已安装 Kimi WebBridge daemon

**禁止工具**：
- ❌ `webReader`（Z.ai 内置）—— 被 Amazon 反爬拦截，只返回 footer
- ❌ `WebFetch` —— 同上，被反爬拦截
- ❌ `curl` / `wget` / `httpx` 等命令行 HTTP 工具 —— 同上
- ❌ `WebSearch` 找第三方聚合数据 —— 数据不完整，A+/Item Highlights/Q&A 等关键字段缺失

#### 优先级 3：第三方聚合数据（兜底，仅限无法启动浏览器时）

**仅在以下条件全部满足时使用**：
1. 浏览器自动化启动失败 ≥2 次
2. 用户明确表示无法提供 Listing 文本
3. 已在报告中明确标注"数据基于第三方，需核实"

可用数据源：
- `device.report/en/amazon-com/[ASIN]`
- `bigbangprice.com` 等聚合站

**使用时必须**：
- 在报告"执行摘要"标注："⚠️ 数据基于第三方聚合，A+/Item Highlights/后台 Search Terms/Q&A 等字段可能不完整，建议登录 Seller Central 核实"
- 评分时按 N/A 处理（5/10 中性分），不假设最差
- 行动清单第一项必须是"登录 Seller Central 核实本报告标注的 N/A 字段"

### 浏览器爬取执行规范

#### 启动前检查
- [ ] 确认 URL 是 Amazon 商品详情页（含 `/dp/[ASIN]`）
- [ ] 确认是哪个站点（.com / .co.uk / .de / .fr / .co.jp / .it / .es 等）
- [ ] 确认是否需要登录（评论详情、Q&A 全文可能需要）

#### 爬取字段清单（必须完整提取）

| 字段 | 必需 | 来源位置 |
|------|------|---------|
| 标题 | ✅ | 页面顶部 `#productTitle` |
| 品牌 | ✅ | 标题上方 `a-lineitem` |
| Item Highlights | ✅ | 标题下方（2026 新字段） |
| 五点描述 | ✅ | `#feature-bullets` |
| A+ 内容 | ✅ | `#aplus` 或 `#aplus_feature_div` |
| Product Information | ✅ | `#productDetails_techSpec_section_1` 或 `#detailBulletsWrapper` |
| 价格 | ✅ | `#priceblock_ourprice` 或 `#corePrice_feature_div` |
| 评论统计 | ✅ | `#acrCustomerReviewText` + `#acrPopover` |
| BSR 排名 | ✅ | Product Information 表格中 |
| Q&A 内容 | 视情况 | `/ask-questions/asin/[ASIN]` |
| 变体信息 | 视情况 | `#twister` 或 `#variation_style_name` |
| Amazon's Choice | 视情况 | `#acBadge_feature_div` |
| 上架日期 | ✅ | Product Information 中 Date First Available |

#### 反爬应对
- 遇到 CAPTCHA：等待 5-10 秒，让浏览器自动化工具自动处理或截图说明
- 遇到 "Type the characters above"：使用 `kimi-webbridge`（用户真实浏览器有 cookie）
- 遇到 "Robot Check"：换用 `browser_use` subagent（自动化浏览器有真实指纹）
- 页面加载慢：等待 `#productTitle` 元素出现后再提取
- 字段不存在：标注"未找到"，不要假设

#### 数据验证
爬取完成后必须验证：
- [ ] 标题字符数与页面显示一致
- [ ] 五点描述至少 3 条（少于 3 条可能是反爬截断）
- [ ] Product Information 表格至少 5 个字段
- [ ] 评论星级 + 数量都拿到了
- [ ] BSR 排名拿到了

若验证失败，重试 1 次后仍失败，降级到优先级 3（第三方聚合数据）。

---

## 工作流程

按以下顺序执行，不要跳步：

1. **采集 Listing 信息** —— 按"数据采集工作流（强制）"段落执行。用户提供 URL 时必须启动浏览器自动化爬取，不得使用 webReader / WebFetch。信息不全时主动询问，缺失字段要在报告中标注为"未提供/待补"。
2. **读取背景知识** —— 阅读 [references/background.md](references/background.md) 理解 Alexa for Shopping 机制与新规，作为检查依据。
3. **8 维度逐项检查** —— 对每个维度按 [references/check-rubric.md](references/check-rubric.md) 的评分标准打分（0-10 分）并记录问题。
4. **参照案例对照** —— 对照 [references/examples.md](references/examples.md) 中同品类的"旧写法 vs 新写法"判断当前 Listing 处于哪个阶段。
5. **生成优化报告** —— 按"输出格式"产出结构化报告，含总分、各维度得分、问题清单、改写建议、优先级排序。
6. **给出改写示例** —— 对标题、Item Highlights、五点至少给出一个改写前后对照（参考 examples.md 的风格）。
7. **输出行动清单** —— 引用 [references/self-check-plan.md](references/self-check-plan.md) 给出 7 天落地计划与误区提醒。

## 输入要求

理想情况下用户应提供以下全部字段。缺失时标注"未提供"并提示用户补充，但不要因此中断检查：

| 字段 | 必需 | 说明 |
|------|------|------|
| 标题 (Title) | 是 | 完整标题文本 |
| 品牌 (Brand) | 是 | 用于标题公式检查 |
| Item Highlights | 视情况 | 2026 新规字段，最多 125 字符 |
| 五点描述 (Bullets) | 是 | 全部 5 条 |
| A+ 页面内容 | 视情况 | 文案/图片说明/场景模块 |
| 后台属性 (Backend Attributes) | 是 | 材质/尺寸/颜色/容量/兼容型号/功率/电压/防水/包装数量/目标人群/使用场景等 |
| Search Terms (后台) | 视情况 | 关键词布局 |
| Q&A 内容 | 视情况 | 常见问题与回答 |
| Review 摘要 | 视情况 | 高频正面词 / 高频负面词 |
| 产品类目 | 是 | 用于判断场景词与属性字段 |
| 目标市场 | 是 | 默认美国站，注意 75 字符新规生效范围 |
| 广告 Prompts 报告 | 可选 | AI 生成的问题、点击、订单数据 |

## 8 维度检查框架

每个维度按 0-10 分评分，详见 [references/check-rubric.md](references/check-rubric.md)。下面是核心要点。

### 维度 1：买家问题清单（Intent Coverage）

检查 Listing 是否能回答买家真实会问的问题。

- 列出该品类买家最可能问的 10-20 个问题（来自评论、Q&A、竞品差评、搜索词报告）
- 逐条核对 Listing 中是否有对应答案
- 重点检查"边界问题"：兼容性、容量、尺寸、适用人群、使用限制、注意事项
- **红线**：如果 Listing 无法回答"我这种场景能不能用"，扣分严重

### 维度 2：标题（Title）

2026 年 7 月 27 日起，美国站大多数非媒体类目标题要求 ≤ 75 字符。

- 字符数检查：≤ 75 字符（硬性）；前 50 字符能否说清产品是谁
- 公式检查：`品牌名 + 核心产品词 + 关键属性 + 核心场景`
- 是否关键词堆砌（同义词重复、竞品词、无关词）
- 是否有人能读懂、AI 能提取的核心信号
- **红线**：标题承担所有信息、超过 75 字符、堆砌同义词

参考改写：
- 旧：`65W USB C Charger Fast Charger for MacBook Pro iPad iPhone Samsung Type C Wall Charger Foldable Plug GaN Charger Adapter`
- 新：`VoltPro 65W GaN USB-C Charger, Foldable Plug`

### 维度 3：Item Highlights

2026 新增字段，最多 125 字符，可搜索、可展示在搜索结果与详情页。

- 字符数 ≤ 125
- 是否覆盖：材料 / 推荐用途 / 适用场景 / 兼容范围 / 核心差异点 / 人群或尺寸
- 是否比标题里堆国家名/型号更有价值
- **红线**：未填写、重复标题内容、堆关键词

示例（欧洲转换插头）：
`For Italy, France, Spain and Germany travel; 2 outlets and USB-C ports for phones, tablets and cameras.`

### 维度 4：五点描述（Bullets）

从"卖点堆砌"改为"问题回答"。每条 bullet 最好只回答一个问题。

建议结构：
1. 产品核心用途
2. 适用场景
3. 关键功能
4. 材质和安全
5. **注意事项和边界**（重要）

检查项：
- 是否避免"high quality / easy to use / perfect gift"等空话
- 边界信息是否清楚（是不是电压转换器、容量、适用犬型、兼容设备、功率限制、护肤品是否避免医疗宣称）
- AI 推荐最怕信息不清，边界越清楚系统越敢推荐
- **红线**：五点全是形容词、没有边界说明、重复标题

### 维度 5：A+ 页面（场景证明）

A+ 应承担"场景证明"作用，不只是放好看的图。

检查是否覆盖：
- 谁在用 / 在哪里用 / 为什么用 / 怎么用 / 和普通款有什么区别
- 场景拆解（如露营灯：帐篷 / 停电 / 车载应急 / 户外桌面 / 续航亮度对比）
- 是否提供 AI 可总结的结构化信息（对比表、兼容设备表、尺寸图）
- **红线**：纯图片无文字说明、无场景拆解、无对比信息

### 维度 6：Q&A 与评论（训练信号）

评论和 Q&A 是 AI 的训练信号，不只看星级。

- 高频正面词是否被强化进 Listing（如"不漏水""适合徒步""放背包没问题"）
- 高频负面词是否已用于优化产品和页面说明（如"尺寸不准""说明不清""不适合某设备"）
- Q&A 是否回答了边界问题
- **红线**：只看星级不看内容、负面高频问题未在 Listing 中说明

### 维度 7：后台属性（结构化字段）

AI 购物助手不只看标题和五点，也看结构化字段。

必须填完整的字段（按品类适用）：
- 材质 / 尺寸 / 颜色 / 容量 / 适配型号 / 适用年龄 / 功率 / 电压 / 是否防水 / 包装数量 / 目标人群 / 使用场景

- 逐项核对缺失字段
- 字段值是否准确（不是乱填或留空）
- **红线**：后台属性乱填或不填、与前台文案矛盾

### 维度 8：广告 Prompts 与关键词布局

Sponsored Products/Bands Prompts 会利用商品详情页等信号生成对话入口。

- 关键词是否分层组织：核心词→标题、场景词→Item Highlights、痛点词→五点、长尾词→A+/Q&A/后台 Search Terms、属性词→后台结构化字段
- 是否无脑重复关键词
- Prompts 报告（如提供）：AI 生成问题是否准确、哪些有点击订单、哪些烧钱不转化、是否暴露 Listing 信息不清
- **红线**：关键词全堆标题、后台 Search Terms 重复前台词、Prompts 暴露信息缺口未修复

## 五大常见误区（检查时必须排查）

1. **"拿到 Amazon's Choice 就一定被 Alexa 推荐"** —— 仍有参考价值但非唯一答案，还要看信息完整度、Review 支持度、价格竞争力、配送稳定性、页面是否回答用户问题、Prompts 是否带出有效对话。
2. **"AI 购物来了关键词不重要"** —— 错。关键词角色变了：从"堆"变成"组织语义"。核心词放标题、场景词放 Item Highlights、痛点词放五点、长尾词放 A+/Q&A/后台。
3. **"Listing 写得越像聊天越好"** —— 不完全对。既要自然也要结构化，既要人能读懂也要机器能提取，既要场景化也要有明确参数。"非常适合旅行"太空，要写"适合欧洲旅行，适用于 Italy/France/Spain/Germany，带 2 个 AC 插孔和 3 个 USB 口，不支持电压转换"。
4. **"标题变短流量一定掉"** —— 不一定。信息重新分配到标题/Item Highlights/五点/A+/后台字段，反而更适合移动端和 AI 理解。只砍短不补才会掉。
5. **"Prompts 是广告团队的事 Listing 不用管"** —— 错。Prompts 利用商品详情页信号生成对话，Listing 写不清 AI 也问不出好问题。Listing 是 AI 广告的素材库。

## 输出格式

严格按以下模板输出报告：

```markdown
# Amazon Listing 优化诊断报告

## 一、执行摘要
- 产品：[品牌 + 核心产品词]
- 目标市场：[美国站/其他]
- 综合得分：[X/100] —— [优秀/良好/需优化/高风险]
- 核心结论：[1-2 句话说明最关键的问题与机会]
- AI 四问覆盖度：[能回答 X/4 个] —— [列出未覆盖的问题]

## 二、各维度评分

| 维度 | 得分 | 状态 | 关键问题 |
|------|------|------|----------|
| 1. 买家问题清单 | X/10 | ✅/⚠️/❌ | ... |
| 2. 标题 | X/10 | ... | ... |
| 3. Item Highlights | X/10 | ... | ... |
| 4. 五点描述 | X/10 | ... | ... |
| 5. A+ 页面 | X/10 | ... | ... |
| 6. Q&A 与评论 | X/10 | ... | ... |
| 7. 后台属性 | X/10 | ... | ... |
| 8. 关键词与 Prompts | X/10 | ... | ... |

状态说明：✅ 达标 / ⚠️ 需优化 / ❌ 严重问题

## 三、详细问题清单

按优先级 P0/P1/P2 排序：

### [P0] [问题标题]
- **位置**：[标题/五点第X条/后台属性X字段]
- **现状**：[引用原文]
- **问题**：[违反哪条规则/缺失什么信号]
- **影响**：[对 AI 理解/推荐/转化的具体影响]
- **建议**：[具体改法]

（重复列出所有问题）

## 四、改写示例

### 标题
- 旧：[原文]（[X] 字符）
- 新：[改写]（[X] 字符）
- 理由：[为什么这样改]

### Item Highlights
- 旧：[原文或未提供]
- 新：[改写]（[X] 字符）
- 理由：[...]

### 五点（至少示范 1-2 条）
- 第X条 旧：[原文]
- 第X条 新：[改写]
- 理由：[...]

## 五、买家问题清单（维度 1 产出）

列出该品类买家最可能问的 10-20 个问题，逐条标注 Listing 是否能回答：

| # | 买家问题 | Listing 是否能回答 | 答案位置 | 备注 |
|---|----------|-------------------|----------|------|
| 1 | ... | ✅/❌ | 标题/五点X/A+ | ... |
| ... | ... | ... | ... | ... |

## 六、7 天行动清单

（引用 references/self-check-plan.md，结合本 Listing 实际问题定制）

- 第 1 天：[具体动作]
- 第 2 天：[具体动作]
- ...
- 第 7 天：[具体动作]

## 七、误区排查

逐条核对五大误区在本 Listing 中的表现：
1. ... 
2. ...

## 八、参考资源
- [references/background.md] Alexa for Shopping 背景与新规
- [references/check-rubric.md] 详细评分标准
- [references/examples.md] 好坏案例对照
- [references/self-check-plan.md] 7 天自查表与误区
```

## 检查规则速查

### 标题硬性规则
- 美国站非媒体类目：≤ 75 字符（2026/7/27 起）
- 前 50 字符说清产品是谁
- 公式：品牌名 + 核心产品词 + 关键属性 + 核心场景
- 禁：同义词重复、竞品词、无关词、承担所有信息

### Item Highlights 硬性规则
- ≤ 125 字符
- 可搜索、可展示
- 覆盖：材料/推荐用途/适用场景/兼容范围/核心差异点/人群或尺寸

### 五点结构建议
1. 核心用途 2. 适用场景 3. 关键功能 4. 材质安全 5. 注意事项与边界

### 后台属性必填（按品类）
材质/尺寸/颜色/容量/适配型号/适用年龄/功率/电压/是否防水/包装数量/目标人群/使用场景

## 资源文件

- [references/background.md](references/background.md) —— Alexa for Shopping 机制、2026 新规、底层逻辑。检查前阅读。
- [references/check-rubric.md](references/check-rubric.md) —— 8 维度详细评分标准（0-10 分细则）。打分时阅读。
- [references/examples.md](references/examples.md) —— 充电器/转换插头/宠物水杯/露营灯等品类的旧写法 vs 新写法对照。改写时阅读。
- [references/self-check-plan.md](references/self-check-plan.md) —— 7 天自查表与五大误区详解。生成行动清单时阅读。

## 重要约束

- 不要给出"这样写一定被 Alexa 推荐"的绝对承诺。亚马逊未公开"Alexa 优先推荐算法公式"。
- 所有建议基于已确认的变化：标题 75 字符新规、Item Highlights 字段、AI Prompts、Alexa for Shopping 能力整合。
- 改写示例要具体到字符数和措辞，不要只说"建议优化标题"。
- 报告必须包含买家问题清单（维度 1），这是整个检查的基础。
- 边界信息（兼容性/限制/注意事项）缺失要重点提示，AI 推荐最怕信息不清。

## 评分与报告约束（v2，2026/8/5 修订）

### N/A 字段处理（强制）

无法从外部抓取或用户未提供的字段（A+ 完整内容、后台 Search Terms、Prompts 报告、Item Highlights 是否填写等）：

1. 在报告中明确标注 "N/A — 未提供"
2. 评分时按 **5/10 中性分** 计入（详见 [references/check-rubric.md](references/check-rubric.md) 评分总则）
3. 不得因 N/A 而假设最差并扣分
4. 不得因 N/A 而触发红线或一票否决
5. 行动清单第一项必须是 "登录 Seller Central 核实本报告标注的 N/A 字段"

### 过渡期评分（2026/7/27 – 2026/9/30）

新规刚生效，市场上大多数 Listing 尚未适配。过渡期内：
- 标题 75-150 字符但产品身份清晰：给 4-5 分（不直接 0-2）
- Item Highlights 未填：给 4 分（标注"待补"），不直接 0-2
- 2026/9/30 后恢复严格评分

详见 [references/check-rubric.md](references/check-rubric.md)。

### 评分必须以市场表现为锚点

避免把"市场头部品"和"差品"打成同一分：
- 4.5★+ 且 ≥10,000 评论 → 维度 6 应得 9-10 分
- BSR 大类 Top 1000 或子类 Top 10 → 加分项 +3
- Amazon's Choice 标签 → 加分项 +3
- 4.0★ 以下或评论 <10 条 → 不能进入"良好"等级

详见 [references/check-rubric.md](references/check-rubric.md) 加分项机制。

### 改写示例合规性（强制）

改写示例必须遵守亚马逊 Style Guide：

1. **不得包含竞品品牌名 / ASIN / 型号**
   - ❌ "Compare with Xvive U2, Getaria M5, Boss WL-20"
   - ❌ A+ 中 "Amazon Basics vs Anker 735 vs UGREEN 65W"
   - ✅ "Compare with leading 2.4GHz wireless systems"
   - ✅ A+ 中 "vs leading competitor"

2. **不得使用未验证的技术参数**
   - ❌ 推测充电时间 "~2-hour recharge"（原 Listing 没说）
   - ❌ 推测电池容量 "3.7V 600mAh"（未核实）
   - ✅ 仅使用原 Listing 已确认的参数
   - ✅ 如必须建议补参数，标注 "[需卖家实测]"

3. **不得使用特殊字符与 emoji**（™ ® © ✔ ✅ ❌ 🎸 等）

4. **不得使用促销语言**（"Best Seller""Free Shipping""Sale""Guaranteed"）

5. **字符数必须精确计算**——不要把 60 字符的标题标为 74 字符

### 风险措辞约束（强制）

报告"风险预警"段落必须有事实依据，不得夸大：

| 禁止措辞 | 替代表述 |
|---------|---------|
| "可能触发 CPSC 合规风险" | "建议在包装和说明书上加窒息警告（CPSC 16 CFR 1500.19）" |
| "可能引发 EU 站点批量下架" | "建议关注 FR 站评论主题，若涉及频段合规可补充区域说明" |
| "确定被搜索权重压制" | "新规生效后超长标题可能影响搜索表现，建议 A/B 测试" |
| "AI 不会推荐" | "AI 推荐可能因信号不全而受限" |

### 数据来源说明

凡报告基于第三方聚合数据（device.report / bigbangprice 等）：
1. 在"执行摘要"标注 "数据基于第三方，A+/Item Highlights/后台 Search Terms 等字段需用户登录 Seller Central 核实"
2. 评分时按 N/A 处理
3. 行动清单第一项必须是 "登录 Seller Central 核实本报告标注的 N/A 字段"

### Prompts 报告建议有前置条件

不要无脑建议"拉取 Prompts 报告"。先问用户"是否跑 SP/SB 广告"：
- 跑广告 → 建议复盘 Prompts 报告
- 不跑广告 → 跳过 Prompts 建议，仅在"长期优化"中提及

### 行动清单合理化

7 天行动清单必须按优先级分批：
- **P0 必做**：48 小时内
- **P1 建议做**：1-2 周内
- **P2 长期做**：1 个月内

不要求 7 天全做完。大品牌卖家标注跨团队动作（如"标题修改需合规团队审"），中小卖家标注"如果只有 3 天时间，必须做这 3 项"。
