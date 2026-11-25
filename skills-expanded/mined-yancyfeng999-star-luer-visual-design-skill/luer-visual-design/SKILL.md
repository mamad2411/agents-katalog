---
name: luer-visual-design
description: 鹿尔花园VI规范执行、标识标牌设计、活动主画面设计及主题乐园竞品视觉研究。每周自动生成带案例图片的竞品分析报告，融合gpt-image-2生图能力完成主题字艺术设计和整体主画面设计。
tags: [luer, vi-system, signage, theme-park, visual-design, competitive-analysis, gpt-image-2, branding]
related_skills:
  - name: luer-content-engine
    github: https://github.com/yancyfeng999-star/luer-content-engine
  - name: DPXX gpt-image-2 v1.0.11
    github: https://github.com/yancyfeng999-star/dpxx-gpt-image-skill
    requires_env: ROOTFLOWAI_API_KEY
  - name: ckm:brand
    note: Hermes 内置 skill（ui-design 分类），无需单独安装
  - name: ckm:design
    note: Hermes 内置 skill（ui-design 分类），无需单独安装
---

# 鹿尔花园视觉设计系统 Luer Visual Design

柔水文旅·鹿尔花园品牌视觉设计 skill。覆盖：
- VI 规范执行（标识标牌、导视系统、宣传物料）
- 活动主画面设计（主题字艺术设计 + 整体视觉）
- 竞品视觉研究（主题乐园/亲子活动主画面周报）
- 与 gpt-image-2 深度集成的自动化设计流程

---

## 一、鹿尔花园 VI 规范速查

### 1.1 品牌色系统

| 色彩名称 | Hex | RGB | 应用场景 |
|---|---|---|---|
| **主色·森林绿** | `#2E7D32` | 46,125,50 | Logo、标题、主按钮 |
| **辅色·暖黄** | `#F9A825` | 249,168,37 | 强调、引导、活动装饰 |
| **背景·米白** | `#FAFAF0` | 250,250,240 | 底色、卡片背景 |
| **文字·深灰** | `#424242` | 66,66,66 | 正文、说明 |
| **点缀·湖蓝** | `#0288D1` | 2,136,209 | 水上活动、夏季主题 |

**色彩使用铁律**：
- 主色占比 60%（导视系统、标识标牌）
- 辅色占比 30%（装饰元素、节日氛围）
- 点缀色占比 10%（特殊活动、季节限定）

### 1.2 字体规范

**中文字体系统**：

| 字体名称 | 用途 | 获取方式 | 替代方案 |
|---|---|---|---|
| **思源黑体 Bold** | 标题、标识标牌主文字 | Google Fonts / Adobe Fonts | 阿里巴巴普惠体 Bold |
| **思源黑体 Regular** | 正文、说明文字 | 同上 | 苹方 Regular |
| **站酷快乐体** | 活动主题字（儿童向）| 站酷网免费下载 | 庞门正道标题体 |
| **汉仪菱心体** | 优雅场景（婚礼/节日）| 汉仪字库商业授权 | 优设标题黑 |

**英文/数字字体**：
- 标题：**Montserrat Bold**
- 正文：**Roboto Regular**
- 装饰：**Pacifico**（手写风格，节日活动）

**字体使用红线**：
- 标识标牌禁止使用花哨字体（宋体/楷体/手写体仅限活动主题字）
- 所有对外物料必须使用已获授权字体
- 安全距离：字高 ≥ 40mm（室外标牌），≥ 12pt（印刷品）

### 1.3 Logo 使用规范

**Logo 标准组合**：
```
[鹿头图形标志] + [鹿尔花园 | Luer Garden]
```

**安全空间**：Logo 四周预留 ≥ Logo 高度的 0.5 倍空白
**最小使用尺寸**：
- 印刷品：20mm 宽
- 屏幕：80px 宽
- 标识标牌：300mm 宽

**禁止行为**：
- 拉伸变形
- 旋转（除非整体画面需要）
- 添加描边/阴影/渐变（标准版已定）
- 放在复杂背景上（对比度 < 4.5:1）

### 1.4 图形元素库

**核心图形 IP**：
- 鹿头剪影（几何化，3种变体：正面/侧面/跃起）
- 叶片装饰（圆角三角形组合，象征森林）
- 波浪纹理（代表溪流/水上项目）

**应用示例**：
- 标识标牌边框装饰
- 指示牌图标系统
- 宣传物料底纹

---

## 二、标识标牌设计执行

### 2.1 导视系统分类

| 类型 | 尺寸标准 | 材质 | 设计要点 |
|---|---|---|---|
| **一级导视**（园区入口） | 2000×1200mm | 不锈钢+亚克力发光字 | Logo+园区名称，夜间可识别 |
| **二级导视**（功能分区） | 1200×800mm | 铝板烤漆 | 图标+中英文，箭头指示 |
| **三级导视**（具体设施） | 600×400mm | PVC板/木质 | 简洁图标+名称 |
| **安全警示牌** | 400×300mm | 反光材质 | 红色边框+警示图标 |

### 2.2 标识标牌设计流程

```
步骤 1：明确标牌类型和安装位置
  → 拍摄现场照片（环境、光线、视距）
  → 记录尺寸要求、材质限制
  
步骤 2：提取文案和图标需求
  → 标题文字（中英文）
  → 辅助说明（营业时间/注意事项）
  → 图标（从 references/icon-library.md 选择或新绘）
  
步骤 3：选择设计模板
  → 对于标准类型，使用 templates/signage-templates/
    - entry-sign.ai（入口标识）
    - direction-sign.ai（方向指示）
    - facility-sign.ai（设施说明）
    - warning-sign.ai（安全警示）
  → 非标准需求，从零设计（遵循 VI 规范）
  
步骤 4：生成设计稿
  方式A：直接修改 AI/Figma 模板（人工）
  方式B：使用 gpt-image-2 生成设计稿（AI辅助）
  
  使用 gpt-image-2 时，调用流程：
  1. 加载 DPXX gpt-image-2 skill
  2. 确定分辨率（印刷用 2K/4K）
  3. 确定比例（横版标牌用 3:2 或 16:9）
  4. 使用模板 T05 Logo/品牌识别 或 T13 UI/界面
  5. Prompt 结构：
     """
     A professional park signage design for Luer Garden theme park.
     
     Layout: [horizontal/vertical] format, clean and modern
     Background: soft cream white (#FAFAF0)
     
     Main elements:
     - Top: Luer Garden deer logo in forest green (#2E7D32)
     - Center: [标牌标题] in bold Siyuan Heiti, 60pt
     - Icons: [描述图标内容] in simple line style
     - Bottom: [辅助说明文字]
     
     Color scheme: primary green #2E7D32, accent yellow #F9A825
     Style: minimalist, nature-inspired, family-friendly
     Typography: clean sans-serif, high contrast for outdoor readability
     
     No watermarks, no decorative frames, no photorealistic textures.
     """
  
步骤 5：输出制作文件
  → 矢量格式：AI/PDF（给制作商）
  → 预览格式：PNG 300dpi（内部审核）
  → 标注文件：尺寸/材质/安装说明（Word/Markdown）
```

### 2.3 常见标识标牌速查表

| 标牌名称 | 中文文案 | 英文文案 | 图标 | 模板 |
|---|---|---|---|---|
| 游客中心 | 游客中心·咨询服务 | Visitor Center | ℹ️ | facility-sign.ai |
| 卫生间 | 卫生间 | Restroom | 🚻 | facility-sign.ai |
| 餐饮区 | 餐饮休息区 | Dining Area | 🍴 | facility-sign.ai |
| 水上项目 | 水上乐园·需更衣 | Water Park | 💧 | facility-sign.ai |
| 禁止入内 | 员工专用·游客止步 | Staff Only | 🚫 | warning-sign.ai |
| 紧急出口 | 紧急出口 | Emergency Exit | 🚪→ | warning-sign.ai |

---

## 三、活动主画面设计系统

### 3.1 主画面设计三阶段

```
阶段 1：主题字艺术设计（核心）
  → 提取活动关键词（2-6个字）
  → 确定字体风格方向（见 1.2 字体规范）
  → 使用 gpt-image-2 生成主题字设计
  
阶段 2：视觉元素配套
  → 根据主题字风格，设计辅助图形
  → 确定配色方案（基于 VI 色系+季节调整）
  
阶段 3：整体主画面合成
  → 主题字 + 活动信息 + 背景氛围
  → 多尺寸输出（海报/易拉宝/横幅/朋友圈）
```

### 3.2 主题字艺术设计 Prompt 公式

**公式结构**：
```
A creative typography design for [活动主题] event at Luer Garden theme park.

Main text: "[活动主题字]" in Chinese characters
Style direction: [风格关键词]
Visual treatment: [视觉手法]

Background: [背景描述]
Color palette: [配色方案]
Decorative elements: [装饰元素]

Output: logo-style text design, square format 1:1, high contrast, suitable for large-format printing.
Constraints: No English text, no watermarks, no unrelated graphics.
```

**风格关键词库**：

| 活动类型 | 风格关键词 | 字体建议 | 视觉手法 |
|---|---|---|---|
| 亲子活动 | playful, colorful, rounded | 站酷快乐体 | 3D立体字，卡通装饰 |
| 节日庆典 | festive, elegant, traditional | 汉仪菱心体 | 灯笼/烟花元素，金色点缀 |
| 夏日水上 | refreshing, dynamic, splash | 思源黑体 Bold | 水滴/波浪纹理，蓝色渐变 |
| 露营野营 | natural, rustic, adventure | 庞门正道标题体 | 树叶/篝火图标，棕绿配色 |
| 团建拓展 | energetic, modern, teamwork | Montserrat Bold | 几何图形组合，撞色设计 |
| 冬季活动 | cozy, warm, glowing | 优设标题黑 | 雪花/灯光效果，暖色调 |

**季节配色调整**：

| 季节 | 主色调整 | 辅助色 | 氛围关键词 |
|---|---|---|---|
| 春季（3-5月） | 森林绿 + 嫩绿 #8BC34A | 粉色 #E91E63 | fresh, blooming, gentle |
| 夏季（6-8月） | 湖蓝 #0288D1 + 青绿 #00ACC1 | 亮黄 #FDD835 | vibrant, cooling, energetic |
| 秋季（9-11月） | 橙黄 #FF6F00 + 棕色 #795548 | 红色 #D32F2F | harvest, warm, nostalgic |
| 冬季（12-2月） | 深蓝 #1565C0 + 银灰 #90A4AE | 金色 #FFD700 | glowing, festive, cozy |

### 3.3 主画面设计完整工作流

```bash
# 示例：鹿尔花园「夏日萤火虫之夜」活动主画面设计

步骤 1：确定活动信息
  活动名称：夏日萤火虫之夜
  活动时间：2026年7月20日-8月20日
  活动亮点：夜间观萤、星空露营、亲子互动
  目标人群：3-12岁家庭
  
步骤 2：主题字设计（调用 gpt-image-2）
  加载 DPXX gpt-image-2 skill
  分辨率：2K（海报印刷）
  比例：1:1（主题字方形构图）
  模板：T05 Logo/品牌识别
  
  Prompt：
  """
  A creative Chinese typography design for summer firefly night event.
  
  Main text: "萤火虫之夜" in bold artistic style
  Style: magical, glowing, nature-inspired
  Visual treatment: characters integrated with firefly light trails, 
  soft glow effects around strokes
  
  Background: deep navy blue gradient (#1A237E to #0D47A1)
  Color palette: 
  - Text: warm yellow #F9A825 with white glow
  - Accents: soft green #8BC34A for nature elements
  Decorative elements: scattered firefly dots, leaf silhouettes
  
  Output: square logo-style text design, high contrast, magical night atmosphere
  Constraints: No English text, no watermarks, no human figures
  """
  
  输出：output/活动主画面/2026-07-萤火虫之夜-主题字.png
  
步骤 3：整体主画面设计（调用 gpt-image-2）
  分辨率：2K
  比例：2:3（竖版海报）或 16:9（横幅）
  模板：T04 海报/KV
  
  Prompt：
  """
  A summer night event poster for Luer Garden theme park firefly watching activity.
  
  Layout (vertical 2:3):
  - Top 30%: Event title "夏日萤火虫之夜" in glowing yellow typography
  - Middle 40%: Illustration of fireflies glowing in forest, children silhouettes 
    watching in wonder, Luer Garden deer logo subtly in background
  - Bottom 30%: 
    * Event dates: July 20 - Aug 20, 2026
    * Time: 19:30-21:30
    * Ticket info
  
  Color scheme:
  - Background: deep night blue gradient (#1A237E → #0D47A1)
  - Fireflies: warm yellow glow #F9A825
  - Forest: dark green #2E7D32 with silhouette treatment
  - Text: white with soft glow for readability
  
  Style: magical realism, family-friendly, sense of wonder
  Mood: enchanting summer night, nature discovery, family bonding
  
  Typography: Bold sans-serif for title, clean readable font for details
  
  Constraints: No watermarks, no URL text, no cluttered design
  """
  
  输出：output/活动主画面/2026-07-萤火虫之夜-主画面.png
  
步骤 4：多尺寸衍生（批量生成）
  使用相同 prompt，调整 --size 参数：
  - 朋友圈海报：1:1
  - 易拉宝：9:16
  - 横幅/户外：21:9
  - 小红书封面：3:4
  
步骤 5：人工精修（可选）
  → 导入 Figma/AI，调整文字细节
  → 添加 Logo、二维码、联系方式
  → 输出印刷文件（PDF + 出血 3mm）
```

### 3.4 活动主画面素材库管理

**完整目录结构**（保存所有过程文件）：
```
output/
├── 活动主画面/
│   ├── 2026-07-萤火虫之夜/
│   │   ├── 设计方案.md ✅（完整设计规范文档）
│   │   ├── 交付总结.md ✅（交付包说明）
│   │   ├── README.md ✅（文件总览）
│   │   ├── 执行日志.md ✅（任务记录）
│   │   ├── 展示页面.html ✅（HTML可视化展示）
│   │   ├── 主题字.png ✅（方形，纯字体设计）
│   │   ├── 主画面-竖版.png ✅（2:3 海报）
│   │   ├── 主画面-横版.png（16:9 横幅）
│   │   ├── 朋友圈.png（1:1）
│   │   ├── 小红书.png（3:4）
│   │   ├── prompts/
│   │   │   ├── 主题字-prompt.txt ✅（可复用Prompt）
│   │   │   └── 主画面-prompt.txt ✅（可复用Prompt）
│   │   ├── iterations/
│   │   │   ├── v1-主题字.png（第一版）
│   │   │   ├── v2-主题字-调整色彩.png（迭代版）
│   │   │   └── feedback.md（用户反馈记录）
│   │   └── archive/
│   │       ├── api-response.json（API返回数据）
│   │       └── generation-log.txt（生成日志）
│   ├── 2026-08-中秋游园会/
│   └── ...
├── 标识标牌/
│   ├── 2026-08-游客中心标牌/
│   │   ├── 设计稿.png
│   │   ├── 设计说明.md
│   │   ├── 制作规格.md（尺寸/材质/安装说明）
│   │   └── prompt.txt
│   └── ...
└── 竞品研究/
    ├── weekly-2026-W29.md
    ├── images/
    │   ├── disney-summer-2026.jpg
    │   └── ...
    └── archive/
        └── raw-data.md（原始采集数据）
```

**文件保存原则**：
1. **设计文档必存**：方案/总结/README/日志
2. **Prompt必存**：每个生成任务的完整Prompt保存到prompts/目录
3. **迭代版本必存**：所有中间版本保存到iterations/目录
4. **展示页必存**：HTML可视化展示页
5. **原始数据必存**：API返回/日志保存到archive/目录

---

## 四、竞品视觉研究（周度自动报告）

### 4.1 研究对象

**国内主题乐园标杆**（按优先级）：

| 乐园名称 | 研究重点 | 数据来源 |
|---|---|---|
| 上海迪士尼 | 节日主题装饰、季节性活动主画面 | 官网、小红书、微信公众号 |
| 北京环球影城 | IP联动设计、沉浸式场景营造 | 官网、抖音、大众点评 |
| 长隆欢乐世界 | 亲子活动视觉、吉祥物应用 | 官网、小红书 |
| 成都融创文旅城 | 本地竞品、区域营销风格 | 官网、本地媒体 |
| 麓湖生态城 | 高端亲子活动、自然教育视觉 | 小红书、官方公众号 |

**亲子活动/大型活动参考**：
- 樊登小读者·线下活动
- 宝贝王·主题派对
- KK集团·亲子市集
- 各地博物馆儿童教育活动

### 4.2 采集维度

每个案例记录以下信息：

```markdown
### [乐园名称]·[活动名称]

**活动时间**：YYYY-MM-DD  
**活动类型**：[节日/季节/IP联动/常规]  
**目标人群**：[亲子/青少年/全家庭]  

**主画面分析**：
- **主题字设计**：[字体风格/视觉手法/创意亮点]
- **色彩方案**：[主色/辅色/情绪表达]
- **构图特点**：[布局方式/视觉焦点]
- **图形元素**：[装饰图案/IP角色/场景插画]

**可借鉴点**：
- ✅ [具体可复用的设计手法]
- ✅ [值得学习的视觉策略]

**避坑点**：
- ⚠️ [设计过于复杂/成本过高]
- ⚠️ [风格不符合鹿尔定位]

**参考图片**：
![主画面](图片URL或本地路径)
![现场布置](图片URL或本地路径)

**数据来源**：[官网链接/小红书笔记链接]
```

### 4.3 周度报告自动生成流程

**执行时机**：每周一早上 9:00 自动触发（通过 cronjob）

```bash
# Cron 配置示例
schedule: "0 9 * * 1"  # 每周一 9:00
prompt: |
  执行鹿尔花园竞品视觉周报采集与生成：
  
  1. 搜索国内主题乐园近7天发布的活动主画面（优先：迪士尼/环球影城/融创）
  2. 小红书搜索"主题乐园活动海报""亲子活动设计"等关键词，采集前10条热门内容
  3. 按 references/competitive-analysis-template.md 格式整理
  4. 生成周报 Markdown 文件：output/竞品研究/weekly-YYYY-WW.md
  5. 提取3个最值得借鉴的设计手法，生成行动建议
  
  使用 luer-visual-design skill 执行。
```

**报告结构模板**：见 `references/competitive-analysis-template.md`

### 4.4 采集工具调用示例

```bash
# 搜索最近活动
web_search("上海迪士尼 活动海报 2026年7月 site:shanghaidisneyresort.com")
web_search("site:xiaohongshu.com 主题乐园活动 海报设计 after:2026-07-14")

# 如需截图（需已登录的本地浏览器）
terminal(command='open -a "Google Chrome" "https://www.shanghaidisneyresort.com/events/"')
computer_use(action="wait", seconds=5)
computer_use(action="capture", app="Google Chrome", mode="vision", 
             question="列出页面上所有活动的名称和海报设计风格")

# 保存图片（从搜索结果中提取）
terminal(command='curl -o "output/竞品研究/images/disney-summer-2026.jpg" "[图片URL]"')
```

### 4.5 周报输出示例

见 `output/竞品研究/weekly-2026-W29.md`（示例周报）

---

## 五、完整工作流程（保存所有过程）

### 5.1 活动主画面完整流程

```
步骤 1：创建项目目录
  mkdir -p output/活动主画面/YYYY-MM-[活动名]/{prompts,iterations,archive}
  
步骤 2：撰写设计方案文档
  write_file(path="output/活动主画面/YYYY-MM-[活动名]/设计方案.md", content="...")
  ✅ 保存完整设计规范（10章节）
  
步骤 3：准备Prompt并保存
  write_file(path="output/活动主画面/YYYY-MM-[活动名]/prompts/主题字-prompt.txt", content="...")
  write_file(path="output/活动主画面/YYYY-MM-[活动名]/prompts/主画面-prompt.txt", content="...")
  ✅ 保存可复用Prompt
  
步骤 4：生成主题字（保存到iterations/如需迭代）
  调用 gpt-image-2 生成
  ✅ 保存 theme-text-01.png
  ✅ 保存 API响应到 archive/theme-text-response.json
  
步骤 5：生成主画面
  调用 gpt-image-2 生成
  ✅ 保存 poster-01.png
  ✅ 保存 API响应到 archive/poster-response.json
  
步骤 6：如需迭代（保存所有版本）
  使用 edit_image.py 局部修改
  ✅ 保存 iterations/v2-poster-调整背景.png
  ✅ 保存 iterations/feedback.md（记录用户反馈）
  
步骤 7：生成多尺寸版本
  批量生成横幅/朋友圈/小红书版本
  ✅ 保存所有尺寸到主目录
  
步骤 8：创建交付文档
  write_file(path="交付总结.md", content="...")
  write_file(path="README.md", content="...")
  write_file(path="执行日志.md", content="...")
  ✅ 保存完整交付文档
  
步骤 9：生成HTML展示页
  使用 templates/html-showcase.html 模板
  ✅ 保存展示页面.html
  
步骤 10：归档原始数据
  ✅ 保存生成日志到 archive/generation-log.txt
  ✅ 保存所有中间文件
```

### 5.2 快速执行命令

**设计标识标牌**：
```
使用 luer-visual-design skill，设计 [标牌类型]，
文案：[中文] / [英文]，
尺寸：[宽×高]mm，
材质：[材质要求]
```

**生成活动主画面**：
```
使用 luer-visual-design skill，设计活动主画面：
活动名称：[名称]
活动时间：[时间]
活动亮点：[3-5个关键词]
输出尺寸：[海报/横幅/朋友圈/全套]
```

**生成竞品周报**：
```
使用 luer-visual-design skill，生成本周竞品视觉研究报告
```

### 5.2 与其他 Skill 的协作

| 场景 | 协作 Skill | 分工 |
|---|---|---|
| 活动推广全案 | luer-content-engine | 内容引擎负责文案/长图布局，视觉设计负责主画面/海报 |
| 品牌升级项目 | ckm:brand | ckm 提供品牌战略，luer 执行视觉落地 |
| 设计系统搭建 | ckm:design-system | ckm 定义 token，luer 应用到实际物料 |

---

## 六、输出目录与文件命名

所有产出保存到：
`/Users/yancyfeng/Desktop/觅无界项目/hermes skill/luer-visual-design/output/`

**命名规范**：
- 标识标牌：`signage-[类型]-[位置]-v[版本].png`  
  例：`signage-direction-entrance-v1.png`
- 活动主画面：`campaign-[YYYY-MM]-[活动名]-[尺寸].png`  
  例：`campaign-2026-07-萤火虫之夜-poster.png`
- 竞品周报：`weekly-[YYYY]-W[周数].md`  
  例：`weekly-2026-W29.md`

---

## 七、品质红线

- ❌ 禁止使用未授权字体（商用场景）
- ❌ 禁止抄袭竞品设计（只借鉴手法/风格）
- ❌ 禁止违背 VI 规范（色彩/Logo 使用）
- ❌ 禁止低分辨率输出（印刷品 < 300dpi）
- ✅ 所有设计稿必须保留源文件（AI/Figma/PSD）
- ✅ 主画面设计需人工复核后才能发布
- ✅ 竞品研究必须标注数据来源

---

## 八、常见问题

**Q1：gpt-image-2 生成的主题字不符合预期怎么办？**  
A：迭代 3 次原则：
1. 第一次：验证构图和风格方向
2. 第二次：调整色彩和细节（使用 edit_image.py 局部修改）
3. 第三次：如仍不满意，切换到人工设计（Figma/AI）

**Q2：竞品图片版权问题？**  
A：竞品研究仅用于内部学习，不对外发布。图片来源标注清楚，仅截图缩略图用于分析，不用于商业传播。

**Q3：标识标牌设计如何控制成本？**  
A：
- 使用标准模板减少设计时间
- 批量制作（同一批次 5 块以上可谈折扣）
- 材质选择：PVC < 铝板 < 不锈钢，根据位置重要性选择

**Q4：活动主画面需要多久出稿？**  
A：
- AI 辅助设计：2-4 小时（含迭代）
- 纯人工设计：1-2 天
- 建议：提前 14 天启动设计，留足改稿时间

**Q5：gpt-image-2 生图超时或等待时间过长怎么办？**  
A：**实战验证的最佳实践**（2026-07-21 七夕星光夜案例）：

**策略优先级**：
1. **先交付设计文档，再生成图片**
   - 完整的设计规范文档（含 Prompt、色彩、构图、执行时间线）比单纯 AI 生图更有价值
   - 设计方案可让团队立即并行工作（人工设计/物料准备/内容策划）
   - 实际案例：七夕活动方案 13,588 字 + 交付总结 10,475 字，完整可执行

2. **使用后台模式运行生图**
   ```python
   terminal(
       command='cd ~/.hermes/skills/content-generation/gpt-image-2 && python3 scripts/generate_image.py ...',
       background=True,
       notify_on_complete=True
   )
   ```
   - 避免前台超时（默认60秒限制）
   - 多任务可并行生成（主题字 + 主画面同时启动）
   - 通过 `process(action='list')` 监控进度

3. **分辨率分阶段验证**
   - 首次验证：1K（15-30秒）→ 快速确认构图和风格
   - 确认满意后：升级 2K（30-40秒）或 4K（60-180秒）
   - 避免直接 4K 浪费时间和额度

4. **Prompt 文件化避免 shell 转义**
   ```bash
   cat > /tmp/prompt.txt <<'EOF'
   [你的完整 Prompt，可含特殊字符]
   EOF
   python3 scripts/generate_image.py --prompt "$(cat /tmp/prompt.txt)" ...
   ```

**生图耗时数据**（实测 2026-07-21）：
- 1K 分辨率：15-30 秒（本次主题字实测：约 60 秒完成，2.2MB）
- 2K 分辨率：30-40 秒（预估）
- 4K 分辨率：60-180 秒（复杂 Prompt 可达 300-600 秒）

**交付优先级**：
1. 设计方案文档（立即可交付，含完整 Prompt 供后续使用）
2. 1K 预览图（快速验证）
3. 2K 高清版（印刷/发布）
4. 多尺寸衍生（横幅/方图/小红书）

---

## 九、技能依赖与环境

**必需 Skill**：
- `DPXX gpt-image-2 v1.0.11`（生图核心）→ https://github.com/yancyfeng999-star/dpxx-gpt-image-skill
  - 环境变量：`ROOTFLOWAI_API_KEY`（count lane，传入方式：`--api-key` 参数）

**推荐 Skill**：
- `luer-content-engine`（内容协作）→ https://github.com/yancyfeng999-star/luer-content-engine
- `ckm:brand`（品牌策略）— Hermes 内置，无需单独安装
- `ckm:design`（设计系统）— Hermes 内置，无需单独安装

**工具**：
- Figma / Adobe Illustrator（矢量编辑）
- 本地浏览器（竞品采集）

**关键参考文档**（必读）：
- `references/lessons-learned.md` — **10条核心经验与避坑指南**（实战总结）
- `references/case-qixi-2026.md` — **七夕星光夜完整案例**（95分，27分钟，可复用Prompt）
- `references/vi-quickref.md` — VI规范速查（品牌色/字体/Logo）
- `references/icon-library.md` — 53种标准图标库

---

## 十、更新日志

### v1.2 (2026-07-21) - P0优化

**新增参考文档**：
- `references/prompt-templates.md` - 结构化Prompt模板库
  - 7段式Prompt框架（STYLE/SUBJECT/COMPOSITION/LIGHTING/COLOR/QUALITY/CONSTRAINTS）
  - 6种场景模板（节日浪漫型/传统节庆型/自然户外型/竖版海报/横版横幅/标识图标）
  - Prompt优化技巧（权重调整/负面Prompt/参考风格/情绪关键词/技术术语）
  - 质量检查清单
  
- `references/file-naming.md` - 文件版本命名规范
  - 3种命名格式（带时间戳/简化版/完整描述版）
  - 推荐目录结构（最终版/iterations/prompts/archive）
  - 版本号规则和迭代管理
  - 命名禁忌和最佳实践
  
- `references/quality-checklist.md` - 设计质量检查清单
  - 7大检查维度（VI规范/设计质量/信息完整性/技术规格/品牌合规/用户体验/AI生成质量）
  - 96分制评分系统
  - A+/A/B/C/D质量等级划分
  - 常见问题速查

**优化点**：
- ✅ 结构化Prompt提升AI生成准确度
- ✅ 统一文件命名提升团队协作效率
- ✅ 系统化质量检查确保交付质量
- ✅ 基于七夕星光夜实战案例优化

### v1.1 (2026-07-21)

- **完整过程保存机制**：新增prompts/iterations/archive三层目录结构
- **新增实战案例**：references/case-qixi-2026.md（七夕星光夜完整案例）
- **新增HTML模板**：templates/html-showcase.html
- **完整工作流程**：明确10步保存所有过程文件

### v1.0 (2026-07-21)

- **初始版本**：VI规范系统、53种图标库、活动主画面设计流程、竞品研究机制
- **完整过程保存机制**：新增 prompts/iterations/archive 三层目录结构，确保零丢失
- **10步规范化工作流**：每步明确文件保存要求，从设计到归档完整覆盖
- **实战验证完成**：七夕星光夜项目 95 分质量，27 分钟交付，输出 11 个文件 6MB
- **文档资产完善**：新增介绍文档(258行)、详细教程(356行含实战案例)、实战经验总结
- **HTML展示模板**：可复用的可视化展示页模板（templates/html-showcase.html）
- **文件保存原则**：5 条强制规则（设计文档必存/Prompt必存/迭代版本必存/展示页必存/原始数据必存）
- **实战案例文档**：references/case-qixi-2026.md 完整记录七夕项目执行过程、成果、评分、可复用价值
- **经验教训库**：references/lessons-learned.md 总结 10 条核心经验和避坑指南

### v1.0 (2026-07-21)
- skill 创建，定义 VI 规范、标识标牌设计流程、活动主画面设计系统、竞品研究机制
