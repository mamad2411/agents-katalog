---
name: wechat-delivery
description: 公众号端到端交付——把任意选题在 30 分钟内变成可直接粘贴的桌面 8 文件交付物（标题/正文/封面/4 配图），用户手动 30 秒发布。适用场景：用户说"写公众号"/"公众号文章"/"配公众号"/"公众号配图"/自己的公众号名。覆盖 v3.18 launch 实战验证的 5 步流程 + 7 段黄金模板 + 桌面文件夹 + mavis browser 自动化天花板 + 反模式。
---

# 公众号内容交付 / WeChat Desktop Delivery

> 把"在公众号发一篇文章"从纯人肉 10h 流程改造成 **30 min（Mavis）+ 30s（用户粘贴）** 的标准化端到端交付。

## 🔗 相关资源（双向互链）

| 端 | 路径 | 用途 |
|---|---|---|
| **公共方法论** | `pretty-skills/内容创作/杂志风公众号品鉴/`（GitHub 公开） | 16 条铁律 + 4 张参考图 + 7 问自检（公开方法论）|
| **本地实操** | `references/magazine-style-16-rules.md`（本 skill） | Mavis 写公众号时直接加载的 16 条铁律 |
| **7 维心法** | `references/writing-craft-7d-rubric.md`（本 skill） | 写完 1 分钟 7 问自检 |
| **5 段钩子** | `references/wechat-hook-chain.md`（本 skill） | knowhub 5 段叙事钩子链 |
| **主题库**（v3.23 待办）| `pretty-skills/视觉创作/gzh-design公众号排版主题库/`（GitHub 公开）| 7 套起步主题 + 5 步排版 pipeline + 10 条反模式 |
| **主题库指针** | `references/theme-library-pointer.md`（本 skill） | 指向 pretty-skills 主题库 case 的加载入口 |

**互链原则**：pretty-skill 公共 case 是「方法论源头」，本 skill references/ 是「Mavis 自动加载的可执行版本」。两者内容 90% 相同，**只维护 1 处**（GitHub 远端公共 case），本地 reference 引用远端路径。

> **核心约束**：Mavis **不**自动化插入公众号编辑器（React 富文本，`mavis browser` 工具栈打不进去）→ 改为桌面文件夹交付。

## Trigger / 触发词

用户说以下任意一种情况时调用：

| 触发词 | 行为 |
|--------|------|
| 写公众号 | 启动完整 5 步流程 |
| 公众号文章 | 同上 |
|（用户的公众号名）| 默认填这个公众号名 + 同上 |
| 配公众号 / 公众号配图 | 只走 Step 3 出图（用户已有正文）|
| 公众号排版 / 公众号封面 | 同上 |

**不**触发的场景：
- 「帮我看看这个公众号文章写得怎么样」→ 这不是交付，是 review，不在本 skill 范围
- 「公众号涨粉怎么办」→ 这是运营问题，不在本 skill 范围
- 「把网页内容转载到公众号」→ 走转载流程，需要先和用户对齐版权

## 5 步交付流程（v3.18 launch 验证 · 30 min）

### 配图硬规则（v3.21 · 公众号封面 2.35:1 + 1:1 兼容）

公众号封面有 **2.35:1（消息列表）+ 1:1（转发卡片/公众号主页）** 两种展示形式，**必须用一张图同时满足两种效果**：

| 位置 | 内容 | 比例 |
|------|------|------|
| 顶部 30% | 标题文字（深棕大字 · 居中）| 留白 |
| 中心 60% | 主体插画（手绘马卡龙 · 一图一概念）| 2.35:1 截中央 / 1:1 截中央 |
| 底部 10% | 副标题 / 副信息（小字）| 留白 |

**设计原则**：
- ❌ 不要装饰边框 / 阴影 / 渐变背景
- ❌ 不要底部放主体（裁剪后会丢）
- ✅ 标题字号大、字数少（≤ 10 字）
- ✅ 主体在画面**垂直中心靠下**（不是底部！）
- ✅ 大量留白（cream paper 背景）

> 参考案例：pretty-skill/assets/readme-1-banner.png（v3.22 README banner）就是按这个规则出的。

```
[Step 1 调研] → [Step 1.5 evidence 链] → [Step 2 写] → [Step 2.5 8 维 rubric] → [Step 3 出图] → [Step 4 桌面交付] → [Step 5 用户粘贴]
   (30s)         (5 min · v3.24)         (30 min)      (1 min · v3.24)         (10 min)         (10s)              (30s)
```

> **v3.24 升级**：在 Step 1 调研后增加 **Step 1.5 evidence 链**（5 min），写完后增加 **Step 2.5 8 维 rubric**（1 min）——借鉴 CyberPPT + dashiai-ppt 三段式，**先过证据关再过视觉关**。详见 `references/evidence-template.md`。

### Step 1 · 调研需求（30 秒 · 必问 1 个问题）

按用户硬规则「出最终方案前先问 1 个关键问题」：

> **「这篇文章的读者是谁 + 你想让他们看完拿走什么？」**

不要问「你想写什么话题」「字数多少」「风格」—— 这些会被默认值吞。

### Step 1.5 · evidence 链（5 min · v3.24 新立）

**目的**：写之前先过"证据关"——每段必填 `conclusion` + `evidence[]` + `source`。

**流程**：

1. 打开 `references/evidence-template.md`
2. 7 段（标题/钩子/总纲/解法/疗效/CTA/写在最后）每段填 evidence 字段
3. 跑 5 问自检（每问 ≤ 10 秒）
4. **5/5 PASS → 进 Step 2 · 3-4 → 微调 evidence · ≤ 2 → 重写 evidence 链**

**为什么先 evidence 后写作**：借鉴 dashiai-ppt slides[].evidence——PPT 怕"瞎编页面"，公众号怕"瞎编段落"，同一个解法：**先过证据关，再过视觉/排版关**。

### Step 2 · 写（30 min · 7 段黄金模板）

详见 `references/golden-template-7-sections.md`（v3.24 evidence 字段已加到每段）。

**v3.24 必做（写完 1 分钟自检）**：

- 打开 `references/writing-craft-7d-rubric.md` → **8 维 rubric**（v3.24 新增第 0 维 evidence 链）
- **第 0 维 evidence 链先过**（5/5 PASS 才进后续）
- 7 问过一遍（每问 ≤ 8 秒）
- **第 0 维 evidence ≤ 3 → 重写 evidence · 其他 7 维 < 5 → 重写 · 5-6 → 微调 · 7 → 进 Step 3**

### Step 3 · 出图（10 min · matrix MCP 并行）

5 张图：1 封面 + 4 配图。风格默认锁定「手绘马卡龙」。

**v3.21 硬规则**（少字 + 留白 + 大字）：
- minimal Chinese text on image（少字 · ≤ 1 行）
- dark brown handwritten font only for short title（深棕手写体大字）
- lots of white space around main illustration（留白 ≥ 30% 面积）
- centered composition, no decorative borders（中心构图，无装饰边框）
- 封面要按 **2.35:1 + 1:1 兼容规则**（主体居中靠下 · 顶部 30% 留给标题）

详见 `references/image-prompt-craft.md`。

### Step 4 · 桌面交付（10 秒 · Mavis 自动）

路径：`~/Desktop/公众号/<name>-<YYYY-MM-DD>/`，8 文件结构：

```
公众号-<name>-YYYY-MM-DD/
├── README.md             # 0.粘贴指南（先读这个）
├── 标题.txt              # 复制 → 输入框
├── 正文.txt              # 复制 → 富文本编辑器
├── 封面.png              # 上传 → 封面位
├── 配图1.png              # 插入正文（位置见 README）
├── 配图2.png
├── 配图3.png
└── 配图4.png
```

### Step 5 · 用户粘贴（30 秒 · 用户的 5 个动作）

1. 复制 `标题.txt` → 输入标题框
2. 复制 `正文.txt` → 粘贴到富文本编辑器
3. 上传 `封面.png`（拖拽到封面位）
4. 按 README 标注位置插入 4 张配图
5. 点群发 / 发布

**总耗时**：30 min（Mavis 端） + 30 秒（用户端）

---

## 工作流（Mavis 接到任务后做什么）

```bash
# 1. 读用户原始输入（选题 + 需求）
# 2. 必问 1 个问题：读者 + 想让读者拿走什么（按用户硬规则）
# 3. 写 7 段正文（content.md 第 2 段起，按 golden template）
# 4. 写 5 个图 prompt（references/image-prompt-craft.md）
# 5. matrix MCP 并行出图（5 张 ~ 30s 总耗时，2K 手绘马卡龙）
# 6. 跑 scripts/build_delivery.py 自动生成桌面 8 文件 + README
# 7. 通知用户：「桌面交付物已建好，打开 Finder 看 README」
# 8. 收尾：用户粘贴完成后，沉淀 case 到 knowhub + pretty-skill
```

---

## mavis browser 6 类失败清单（不要尝试自动化插入）

实测新版公众号编辑器（React 富文本，不是 iframe UEditor），`mavis browser` 工具栈天花板：

| 工具 | 失败原因 |
|------|----------|
| `type` | 只能打到 input/textarea；公众号正文编辑器是 `<div>` 非 typable |
| `press_key Cmd+V` | React 组件捕获不到系统级粘贴事件（不冒泡到 native listener） |
| `set_file_input` | 只能触达 file input；公众号封面位不是 file input（是点击触发 modal） |
| `click 菜单/按钮` | 编辑器菜单是 React 动态渲染，selector 改了页面就失效 |
| `iframe` | 公众号编辑器**不在 iframe 里**（v3.18 后废弃了 UEditor） |
| `screenshot + 坐标点击` | 每次页面渲染后坐标会偏移，且编辑器会随内容重排 |

**结论**：`mavis browser` 在 React 富文本场景下**放弃**。价值是「填表/上传/读」等明确 file input 场景。

---

## 3 个反模式（必避坑）

### 反模式 1：关键 UI 流程被默认值吞掉

走"自动插入公众号" → React 编辑器点不动 → 浪费 2 小时。
**正确做法**：影响最终产物的参数默认 = None，不传 → 弹 picker 或 fail-fast。

### 反模式 2：营销首页浪费 token

把同样内容同时套到营销首页、飞书贴、小红书 → 每改一次要在 3 个地方同步。
**正确做法**：单一交付物（桌面文件夹），用户自己分发。

### 反模式 3：picker 被默认吞

调研阶段曾试图做"风格 picker"让用户选 → picker 在自动化流程里被默认走了第一项。
**正确做法**：picker 只用在「用户明确要求做 PPT / 出图」的场景，写作流程里不弹。

---

## 量化疗效

| 阶段 | 之前 | 现在 | 倍速 |
|------|------|------|------|
| 写（含调研） | 4h | 30min | 8x |
| 出图 | 3h | 10min | 18x |
| 发布（含上传） | 5h | 30s | 600x |
| **总** | **10h** | **30min** | **20x** |

**用户拿到后**：每天能发 1 篇公众号；如果是 v3.18 launch 级，每月能出 1 个有体系的产品发布。

---

## 数据来源 / 沉淀

- pretty-skill case：`pretty-skill/Agent知识/公众号内容交付方法论/`（13 页 · commit `3c897a6`）
- knowhub case：`~/.mavis/knowledge/knowhub/domains/ai-agent/cases/2026-07-10-wechat-delivery-flow.md`（150 行 · commit `14de5c1`）

## 工具栈

| 用途 | 工具 |
|------|------|
| 写 | Mavis 自己 + 7 段黄金模板 |
| 出图 | matrix MCP（MiniMax Token plan 套餐）|
| 桌面交付 | `scripts/build_delivery.py`（一键建 8 文件 + Finder 打开） |
| 沉淀 | pretty-skill + knowhub 双仓库 |

## 相关参考文档

```text
references/golden-template-7-sections.md    # 7 段写作模板（v3.24 evidence 必填）
references/evidence-template.md             # v3.24 新立 · evidence 字段定义 + 自检 5 问
references/wechat-hook-chain.md              # knowhub 5 段钩子链（痛点 + 翻转 + 范式 + 案例 + CTA）
references/posting-format-v322.md           # v3.22 排版硬规则
references/image-prompt-craft.md            # 出图 prompt 工艺 + 2.35:1+1:1 兼容
references/desktop-folder-structure.md      # 8 文件细节
references/wechat-editor-react-tips.md      # mavis browser 在公众号场景的 6 类失败
references/writing-craft-7d-rubric.md      # 优质公众号 8 维心法（v3.23 7 维 + v3.24 第 0 维 evidence 链）
references/magazine-style-16-rules.md     # 杂志风 16 条铁律（v3.23 新立 · 反 AI 味实操）
```

## 7 段骨架 + 5 段肉 + 4 图闭环（v3.23 合并版）

每次写公众号时，Mavis 自动跑：

| 段 | 字数 | 内容 |
|---|---|---|
| **P0 标题** | 30 字 | 痛 + 量化 + 场景（3 filter 自检）|
| **P1 钩子** ← 痛点 + 翻转 | 200-300 字 | 戳真痛点 + 「你不是没灵感，你是没工具」类金句 |
| **P2 总纲** | 80-120 字 | ① ② ③ 3 个具体能力 |
| **P3 解法** ← 范式落地 | 1500-2000 字 | before/after 对比表 + 流程图 + 3 件事细节 |
| **P4 案例背书** ← 3 真实场景 | 400-600 字 | 个人 + 团队 + 长期数据，每个：场景 + 痛点 + 量化 |
| **P5 疗效** | 200-300 字 | 省时/省钱/提质 简洁段落 |
| **P6 CTA** ← 三分钟上手 | 50-80 字 | 装 + 用 + 发 + 适用/不适用 |
| **P7 写在最后** | 30-50 字 | 自然过渡 · 不用「金句」标签 |

**4 图闭环**（按段位）：
- p0_cover → P0 封面位（2.35:1+1:1 兼容）
- p1_pain → P1 钩子后
- p2_paradigm → P3 解法后
- p3_cases → P4 案例后

**风格纪律**（刘润式 · knowhub 5 段钩子链要求）：
- 禁 emoji / 禁话题标签 / 禁「欢迎评论区」套话
- 克制 > 华丽
- 「金句」改「写在最后」自然过渡

**风格纪律 v2（杂志风 16 条铁律 · 2026-07-13 整合）**：

从原公众号「推荐好用的 PPT skill」2026-06-30 提炼的 16 条反 AI 味铁律。**写完 1 篇公众号时，跑 1 分钟 7 问自检**：

| 维度 | 规则 | 反 AI 味标志 |
|---|---|---|
| 排版 6 条 | 0 emoji + 0 分割线 + H2/H3 + 1-3 句段 + 加粗整句 + 反引号 | emoji 满天飞 / 长段落 / bullet 转折 |
| 叙事 5 段 | 日常+反差 → 分类 → 精炼 → 痛点转折 → 顺势不抢戏 | "在当今时代..." 套话 / 不分维度 |
| 配图 5 类 | 多宫格 + 黑底矩阵 + 工具高亮 + 风格样图 + 小水印 | 1 张配图撑场 / 满屏标注 |

**反 AI 味 7 问自检**：
1. emoji 出现几次？0 = 通过
2. 段落最长几句？≤ 3 = 通过
3. 加粗整句 ≥ 1？= 通过
4. 配图 ≥ 4？= 通过
5. 有多宫格图？= 通过
6. 转折是加粗整句？= 通过
7. 标题有"反 AI 味"自检？= 通过

**判定**：7/7 = 杂志风 · 5-6 = 微调 · < 5 = 重写

完整 16 条 + 实战示例 → `references/magazine-style-16-rules.md`（v3.23 必读）

## 同步来源

knowhub 仓库 `domains/ai-agent/cases/2026-07-10-wechat-delivery-flow.md`，单一来源 `~/.mavis/knowledge/knowhub/`，本文件为执行镜像。任何 case 升级 → 同步更新本 SKILL.md。