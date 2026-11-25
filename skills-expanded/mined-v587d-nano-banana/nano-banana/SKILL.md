---
name: nano-banana
description: >-
  Generates images using Google Gemini via Chrome browser automation (Chrome MCP Server).
  Takes a text prompt, navigates to gemini.google.com, inputs the prompt for image generation,
  waits for the generated image to appear, extracts the blob URL and returns it.
  Trigger when user wants to: generate an image, create AI artwork, use Gemini to draw/paint,
  make a picture with AI, generate visual content via Gemini, 生成图片, 画图, AI绘画,
  Gemini画图, 图片生成, 用Gemini生成图像, make an image of, create a picture of.
  This skill handles the full browser automation pipeline from prompt to blob URL return.
---

# NanoBanana — Gemini 图片生成器

通过 Chrome MCP Server 驱动浏览器，在 Google Gemini 上自动化图片生成流程。

## 核心原则（必读）

**本 skill 的唯一输出目标：提取 Gemini 生成的图片 blob URL，返回该 URL。到此为止。**

- 图片生成后，`<generated-image>` 元素中的 `<img>` 标签的 `src` 即为 blob URL（格式：`blob:https://gemini.google.com/<uuid>`）
- 你的任务就是：轮询等待 `<generated-image>` 出现 → 提取 blob URL → 返回 URL
- **禁止**点击下载按钮——这会触发 OS 层"另存为"对话框，无法用 MCP 工具处理
- **禁止**查找 Downloads 目录、移动文件、截图、canvas 转 base64、网络捕获等操作
- **禁止**在拿到 blob URL 后做任何后续处理

---

## 前置条件

### Chrome MCP Server

本 skill 需要 Chrome MCP Server 已配置并正常运行。所有浏览器操作通过 Chrome MCP 工具完成：

| 工具 | 用途 |
|------|------|
| `chrome_navigate` | 导航到 Gemini |
| `chrome_switch_tab` | 切换到 Gemini 标签页（确保前台激活） |
| `chrome_read_page` | 读取页面无障碍树，定位元素 |
| `chrome_fill_or_select` | 填充输入框 |
| `chrome_click_element` | 点击按钮/元素 |
| `chrome_keyboard` | 键盘输入（Enter 提交等） |
| `chrome_javascript` | 执行 JS（输入提示语、检测生成状态等） |
| `chrome_console` | 读取浏览器控制台（调试用） |

### Google 账号

需要在 Chrome 中已登录 Google 账号。Gemini 需要登录态才能生成图片。首次使用前确认：

1. 打开 Chrome，访问 `https://gemini.google.com/app`（或已有的 session 链接如 `https://gemini.google.com/app/a2b9fee5d6ff2e8f`）
2. 确认已登录 Google 账号（页面右上角有头像）
3. 如未登录，手动完成 Google 登录（含 2FA 如有）

> **注意**：登录态可能因长时间不活动而过期（24-48小时）。如果生成时遇到认证问题，需要手动重新登录。

---

## 触发条件

**触发**（用户意图匹配以下任一）：
- "生成一张...的图片" / "用 Gemini 画..."
- "帮我画一个..." / "create an image of..."
- "generate an image" / "make a picture"
- "AI 绘画" / "图片生成"
- "用 Gemini 生成图像"
- "make me a visual of..."

**不触发**：
- 纯文本对话、代码生成、翻译等非图像任务
- 用户已指定其他工具（如 Stable Diffusion、Midjourney 等）
- 用户只是询问 Gemini 的能力而非实际生成

---

## NanoBanana Prompt 工程指南

> **你的任务**：将用户的自然语言需求，转化为 NanoBanana（Gemini 2.5 Flash Image）能精准理解的高质量 prompt。**本指南教你如何写出好 prompt。**

### Prompt 构造公式

按以下维度逐层叠加，描述越具体，结果越接近预期：

```
主体(Subject) + 动作/姿态(Action/Pose) + 环境/背景(Setting) + 风格(Style)
  + 光照(Lighting) + 构图与相机(Composition & Camera)
  + 色彩(Color Palette) + 氛围/情绪(Mood) + 宽高比(Aspect Ratio)
```

### 七大核心原则（Phil Schmid / Google 官方）

| # | 原则 | 说明 | 错误示例 | 正确示例 |
|---|------|------|---------|---------|
| 1 | **极度具体** | 每个名词都加形容词；每个形容词都加修饰语 | `fantasy armor` | `ornate elven plate armor, etched with silver leaf patterns, high collar, pauldrons shaped like falcon wings` |
| 2 | **提供意图与上下文** | 说明图片用途和受众，帮助模型理解场景逻辑 | `Create a logo` | `Create a logo for a high-end minimalist skincare brand targeting women aged 25-40` |
| 3 | **描述"要什么"而非"不要什么"** | 用正向描述替代否定词（语义负提示） | `no cars, no rain` | `an empty sun-drenched road with clear blue sky` |
| 4 | **迭代精炼** | 第一张不满意→补充细节→再生成。不指望一次完美 | 发现风格漂移后继续在同一会话中硬调 | 风格漂移→新会话+详细描述+参考图锚定 |
| 5 | **复杂场景分步指令** | 大场景拆成：背景→前景→主体→细节 | 一句话塞入所有要求 | `First, create a misty forest at dawn. Then add a moss-covered stone altar in the foreground. Finally, place a glowing sword on top.` |
| 6 | **控制相机** | 使用摄影/电影术语 | `take a photo` | `wide-angle shot, 85mm portrait lens, f/1.8 aperture, shallow depth of field, low-angle perspective` |
| 7 | **角色一致性修复** | 编辑多轮后角色漂移→新会话+详细文字描述重置 | 在同一长会话中反复编辑 | 新会话 + `maintain exact character design: [详细描述]` |

### Prompt 元素详解

#### 1. 主体 (Subject)
把人/物/场景描述到"闭眼能看见"的程度：
- 物理特征：纹理、材质、颜色、尺寸、形状
- 独特细节：标志性特征、瑕疵、配件
- 空间位置：前景/中景/背景

```
❌ a cat
✅ a fluffy orange tabby cat with white chest and paws, emerald green eyes,
   a small notch on its left ear, sitting on a velvet cushion
```

#### 2. 动作/姿态 (Action/Pose)
用动态动词描述主体的状态：
- `running energetically`, `arms bent and legs lifted high`
- `leaning forward with a curious expression`
- `mid-jump, dust particles suspended in air`

#### 3. 环境/背景 (Setting)
描述具体而非泛化：
```
❌ in a city
✅ on a rain-slicked Tokyo alleyway at night, neon signs reflecting in puddles,
   steam rising from a ramen shop vent in the background
```

#### 4. 风格 (Style)
直接指定艺术风格、媒介、参考：
- **写实**：`photorealistic`, `hyperrealistic`, `award-winning wildlife photograph`
- **插画**：`watercolor painting`, `oil on canvas`, `digital illustration`, `vector art`
- **动漫**：`anime style, Studio Ghibli inspired`, `manga panel, screentone shading`
- **概念**：`cyberpunk`, `steampunk`, `fantasy concept art`, `brutalist architecture`
- **特殊**：`pixel art 16-bit`, `claymation`, `flat vector illustration`, `isometric`, `technical blueprint`
- **摄影流派**：`street photography`, `editorial fashion`, `architectural photography`

> ⚠️ NanoBanana 的**风格迁移（style transfer）较弱**。建议用文字描述风格而非依赖参考图做风格转移。直接在 prompt 中描述风格效果更好。

#### 5. 光照 (Lighting)
光照决定氛围和真实感：
- 方向：`backlit`, `side-lit`, `overhead lighting`
- 质量：`soft diffused light`, `harsh direct sunlight`, `golden hour glow`
- 色温：`warm candlelight`, `cool fluorescent`, `neutral 3PM daylight`
- 特效：`volumetric lighting`, `god rays`, `rim light`, `cinematic lighting`
- 摄影棚：`studio lighting with softbox`, `three-point lighting`

```
❌ good lighting
✅ warm golden hour sunlight streaming through a window, casting long soft shadows,
   dust motes floating in the light beams, cinematic rim light on the subject
```

#### 6. 构图 (Composition)
使用摄影和美术术语精确控制布局：
- **摄影**：`rule of thirds`, `leading lines`, `negative space`, `symmetrical`, `frame within a frame`
- **透视**：`top-down`, `bird's eye view`, `worm's eye view`, `dutch angle`, `isometric`
- **景深**：`shallow depth of field (DOF)`, `bokeh background`, `everything in sharp focus`
- **距离**：`close-up`, `medium shot`, `wide shot`, `extreme wide shot`, `macro`
- **画幅**：`16:9`, `1:1 square`, `9:16 vertical`, `4:3`, `3:2`

#### 7. 色彩 (Color Palette)
```
❌ colorful
✅ pastel color palette with mint green, soft pink, and lavender accents
✅ muted earth tones with teal highlights
✅ vibrant neon colors: hot pink (#FF1493), electric blue (#00FFFF), lime green (#32CD32)
```

> ✅ **Hex 色号有效**：`#9F2B68`、`#00FF00` 等 hex 颜色代码可被 NanoBanana 识别。

#### 8. 氛围/情绪 (Mood)
```
eerie and unsettling | peaceful and serene | energetic and chaotic
nostalgic and melancholic | luxurious and opulent | gritty and raw
```

#### 9. 图片内文字 (Text in Image)
NanoBanana 支持在图片中嵌入文字，需**指明文字位置和呈现方式**：
```
❌ add text "SALE"
✅ The text 'SALE' is written on a red hangtag attached to the handle, bold white font
✅ A neon sign on the wall reads 'OPEN 24 HOURS' in pink cursive script
✅ The word 'AERO' is embossed in gold letters on the backrest
```

> ⚠️ NanoBanana（2.5 Flash Image）仍有文字拼写错误风险。简短文字效果更好。如需完美文字，考虑 NanoBanana Pro（Gemini 3 Pro Image）。

#### 10. 宽高比 (Aspect Ratio)
在 prompt 中显式声明：
- `16:9` — 横屏/桌面壁纸
- `9:16` — 竖屏/手机壁纸/Story
- `1:1` — 正方形/社交媒体头像
- `4:3` — 传统照片比例
- `2:1` — 全景

### NanoBanana 特有技巧

#### 1. ALL CAPS 强调关键约束
用大写标记不可违反的要求（NanoBanana 的 autoregressive 架构对大小写敏感）：
```
All characters MUST have heterochromatic eye colors matching their fur colors.
The composition MUST follow the rule of thirds EXACTLY.
NEVER include any text, watermarks, or line overlays.
```

#### 2. Markdown 列表做编辑指令
NanoBanana 能理解 Markdown 格式的编辑列表：
```markdown
Make ALL of the following edits to the image:
- Put a strawberry in the left eye socket.
- Change the plate to a plate-shaped chocolate-chip cookie.
- Add happy people to the background.
```

#### 3. 摄影专业术语提升质量
NanoBanana 的文本编码器理解摄影术语，加入后可显著提升构图和真实感：
```
shot with a Canon EOS 90D DSLR camera
85mm portrait lens at f/1.8
neutral diffuse 3PM lighting
natural uniform depth of field (DOF)
viral 4K HD video still
```

#### 4. Buzzword 魔法词
一些"魔法词"能触发更高品质的输出（NanoBanana 训练数据中包含对这些词的认知）：
- `Pulitzer-prize-winning cover photo for The New York Times`
- `cover profile for Vanity Fair`
- `award-winning National Geographic photograph`
- `cinematic still from an Oscar-winning film`

> ⚠️ Google 系统 prompt 中有 "YOU WILL BE PENALIZED FOR USING" buzzwords 的约束，但实测中高质量 buzzwords 仍能改善构图。

#### 5. 参考图锚定一致性
多张生成要保持风格/角色一致：
- 上传一张已满意的图作为参考锚
- prompt 中添加：`using the exact art style, color palette, and line work of the reference image`
- 长会话中角色漂移 → 开新会话 + 详细文字描述重置

#### 6. 反向 Prompt 工程
不知道如何描述风格？让 Gemini 自己分析：
```
prompt: "Analyze this image and provide a detailed text description of its art style,
lighting, artistic medium, and color palette. Give me 5-10 specific style keywords
that would recreate this aesthetic."
```
把返回的关键词作为后续 prompt 的固定后缀。

#### 7. JSON 结构化描述
对复杂角色设计，JSON 格式可保持精确：
```json
{
  "hair": "voluminous midnight-blue curls cascading past shoulders",
  "attire": "tailored doublet of emerald Italian silk with polished chrome shoulderplates",
  "pose": "right hand resting on ornate cutlass hilt, left holding golden espresso tamper"
}
```

### 常见风格关键词速查

| 目标风格 | 推荐关键词 |
|---------|-----------|
| 写实摄影 | `photorealistic, hyperrealistic, 85mm portrait lens, natural lighting, 8K` |
| 赛博朋克 | `cyberpunk, neon lights, rain-slicked streets, high tech low life, blade runner aesthetic` |
| 吉卜力/动漫 | `Studio Ghibli inspired, hand-drawn animation, soft watercolor backgrounds, anime style` |
| 油画质感 | `oil on canvas, visible brushstrokes, impasto texture, Rembrandt lighting` |
| 极简矢量 | `flat vector illustration, minimalist, clean lines, pastel palette, geometric shapes` |
| 复古胶片 | `35mm film photography, Kodak Portra 400, light leaks, vintage grain, nostalgic` |
| 概念艺术 | `fantasy concept art, matte painting, epic scale, dramatic lighting, artstation` |
| UI/产品 | `product photography, studio lighting, white background, e-commerce, minimal` |
| 像素风 | `16-bit pixel art, retro game sprite, limited color palette, SNES style` |
| 水墨画 | `traditional Chinese ink wash painting, sumi-e, rice paper texture, minimalist brushwork` |

### Prompt 对比：差 → 好

**场景：一只猫**
```
❌ 差: a cat
✅ 好: a fluffy orange tabby cat with bright emerald eyes and a white chest,
      sitting regally on a velvet burgundy cushion, soft morning light streaming
      through a nearby window, shallow depth of field, 85mm portrait lens, photorealistic
```

**场景：城市夜景**
```
❌ 差: city at night
✅ 好: a cyberpunk Tokyo alleyway at midnight, neon kanji signs reflecting in
      rain puddles, steam rising from street vents, a solitary figure in a
      translucent raincoat silhouetted against pink and blue neon, cinematic
      low-angle shot, volumetric lighting, blade runner aesthetic, 16:9
```

**场景：产品图**
```
❌ 差: a coffee cup on a table
✅ 好: flat-lay product photography of a ceramic latte cup on a distressed
      wooden table, delicate latte art in a fern pattern, scattered coffee beans
      and a cinnamon stick in the frame, warm morning sunlight from the left
      creating soft shadows, 85mm macro lens, minimal and cozy aesthetic, 1:1
```

**场景：Logo**
```
❌ 差: create a logo for a bakery
✅ 好: create a minimalist logo for an artisanal sourdough bakery called 'Crust & Crumb',
      wheat grain icon integrated into a circular badge, warm terracotta and cream
      color palette, refined serif typography, clean vector style, white background
```

---

## 核心工作流

### Step 1：确保在 Gemini 页面

**首先检查当前是否已在 Gemini 页面**。如果用户已在某个 Gemini session 中（地址栏显示 `gemini.google.com/app/...`），跳过导航，直接用当前页面。

判断方法：
```
用 chrome_get_windows_and_tabs 或 chrome_read_page 检查当前标签页 URL 是否匹配:
  https://gemini.google.com/app
  https://gemini.google.com/app/<session_id>
```

**如果已在 Gemini 页面 → 跳到 Step 2。**

**如果不在**，才需要导航：

```
chrome_navigate(url="https://gemini.google.com/app")
```

> Gemini URL 格式：`https://gemini.google.com/app` 或 `https://gemini.google.com/app/<session_id>`。
> 两种格式均可用。如果用户提供了具体的 session 链接，直接导航到该链接。

等待页面加载完成后（2-3 秒），用 `chrome_read_page` 确认页面状态。

### Step 2：确认登录状态

用 `chrome_read_page` 检查页面元素。确认以下任一信号表示已登录：

| 信号 | 含义 |
|------|------|
| 页面上有输入框（`.ql-editor` 或 `[contenteditable="true"]`） | 已登录，可以开始 |
| 右上角有 Google 头像 `img[aria-label*="Google Account"]` | 已登录 |
| 页面显示 "Sign in" 按钮 | **未登录，需要手动处理** |

如果未登录：
1. 告知用户需要手动登录
2. 用 `chrome_navigate(url="https://accounts.google.com")` 打开登录页
3. 等待用户确认登录完成后继续

### Step 3：构造并输入 Prompt

> ⚠️ **重要**：输入的 prompt 质量直接决定生成图片的质量。在构造 prompt 前，**必须先阅读并遵循上方的「NanoBanana Prompt 工程指南」**——特别是七大核心原则和 prompt 元素详解。

**快速要点**：
- 以 `Generate an image of...` 或 `生成一张...的图片` 明确开头
- 使用**自然段落叙述**而非逗号分隔的关键词列表（NanoBanana 是 autoregressive 模型，不是 diffusion 模型）
- 描述要极度具体：主体、动作、环境、风格、光照、构图、相机、宽高比—每个维度都不要省略
- 英文优先（英文 prompt 效果更好），但中文 prompt 也可用
- 用 ALL CAPS 标记关键约束（如`MUST`、`EXACTLY`、`NEVER`）
- 使用摄影术语（如 `85mm lens, f/1.8, golden hour`）可大幅提升真实感

**Prompt 构造公式**：
```
主体 + 动作/姿态 + 环境/背景 + 风格 + 光照 + 构图与相机 + 色彩 + 氛围 + 宽高比
```

**输入方式**：

> ⚠️ **TrustedHTML 限制**：Gemini 页面启用了 TrustedHTML 安全策略，`innerHTML` 赋值会抛出 `TypeError`。
> **必须使用 `textContent` + `createElement` 方式，不要尝试 `innerHTML`。**

用 `chrome_javascript` 输入（唯一可靠方式）：

```javascript
// ✅ 正确：textContent + createElement（绕过 TrustedHTML）
chrome_javascript(code=`
  const editor = document.querySelector('.ql-editor');
  if (editor) {
    editor.textContent = '';
    const p = document.createElement('p');
    p.textContent = 'PROMPT_TEXT_HERE';
    editor.appendChild(p);
    editor.dispatchEvent(new Event('input', { bubbles: true }));
    return 'prompt set';
  }
  return 'editor not found';
`)

// ❌ 错误：innerHTML 会因 TrustedHTML 策略报错，绝对不要用
// ❌ 错误：chrome_fill_or_select 不支持 contenteditable div，绝对不要用
```

### Step 4：提交提示语

**方式一**：用 `chrome_keyboard` 按 Enter：
```
chrome_keyboard(keys="Enter")
```

**方式二**：用 `chrome_click_element` 点击发送按钮：
```
// 按优先级尝试以下选择器
selector="button[data-testid='send-button']"
selector="button[aria-label*='Send']"
selector="[data-mat-icon-name='send']"
```

### Step 5：等待图片生成

图片生成通常需要 **15-60 秒**。用轮询方式等待图片出现。

> ⚠️ **关键**：Gemini 标签页必须在**前台激活状态**，否则 Chrome 会节流后台标签页的图片渲染。如果 Gemini 在**无痕窗口**中，`chrome_switch_tab` 可能无法跨窗口激活。

**步骤**：

```
1. 尝试切换到 Gemini 标签页：
   chrome_switch_tab(tabId=<当前tabId>)

2. 用 chrome_javascript 轮询检测（每 5 秒一次，带重试计数）：
   - 每次检测：查询 <generated-image> img，若 blob URL 存在则 scrollIntoView + 读 naturalWidth
   - 若 blob URL 存在但 naturalWidth 持续为 0，累计重试次数
    - 重试 5 次后仍为 0 → **仍返回 blob URL**，同时告知用户："图片地址已获取，请在 Gemini 标签页中打开查看。"
   - 用户确认已切换后，重新轮询
```

**重试上限与用户介入**：

```
重试次数 | naturalWidth 状态 | 动作
    1-4  | 0×0              | 继续重试（每次间隔 5 秒）
    5    | 0×0              | ⚠️ 返回 blob URL + 提示用户切换到 Gemini 标签页查看
 用户确认 | —                 | 完成（URL 已在用户手中）
```

**轮询检测 JS**（每 5 秒执行一次）：

```javascript
chrome_javascript(code=`
  (() => {
    const genImg = document.querySelector('generated-image img');
    if (genImg && genImg.src.startsWith('blob:')) {
      genImg.scrollIntoView({ block: 'center' });
      return {
        ready: genImg.naturalWidth > 0,
        signal: 'generated_image',
        url: genImg.src,
        width: genImg.naturalWidth,
        height: genImg.naturalHeight
      };
    }
    const error = document.querySelector('[role="alert"], .error-message');
    if (error) return { ready: false, error: error.textContent };
    return { ready: false };
  })()
`, tabId=<当前tabId>)
```

> ⚠️ **lazy loading**：图片 `loading="lazy"`，必须 `scrollIntoView` 触发加载。  
> ⚠️ **无痕模式**：`chrome_switch_tab` 在无痕与普通窗口之间切换有限制。5 次重试无果后，blob URL 仍然有效，直接返回给用户即可。blob URL 是图片的最终地址，与是否在本标签页渲染无关。

**错误信号检测**：
- "Can't create it right now" → 认证问题
- "Image Generation Limit Reached" → 日限额已满
- "Something went wrong" → 重试或换提示语

### Step 6：获取图片地址

图片生成完成后，不通过下载按钮保存到本地，而是直接提取图片的 blob URL。
**blob URL 无需 OS 层交互，不受 Chrome 下载设置影响。**

**步骤**：

```
1. 用 chrome_javascript 提取 <generated-image> 中的图片 blob URL（Step 5 已 scrollIntoView 过，图片已加载完成）：
   chrome_javascript(code=`
     const img = document.querySelector('generated-image img');
     return img ? {
       url: img.src,
       width: img.naturalWidth,
       height: img.naturalHeight
     } : null;
   `, tabId=<当前tabId>)

2. 返回 blob URL（格式：blob:https://gemini.google.com/<uuid>）。完成。
```

**关于 blob URL**：
- 仅在 Gemini 页面打开期间有效（页面刷新或关闭后失效）
- 可在浏览器地址栏直接打开（需在同一 Gemini 标签页中）
- 如需永久保存，用户可在浏览器中打开该 URL 后右键另存为
- **不需要**与 OS 交互，没有"另存为"对话框问题

**简要版**：

```
→ chrome_javascript: querySelector('generated-image img').src
→ 返回 blob URL
→ 结束。
```

---

## 错误处理

| 错误现象 | 原因 | 处理方式 |
|---------|------|---------|
| 页面提示 "Sign in" | 登录态过期 | 提示用户手动登录，等待确认后重试 |
| 输入框无法填充 | Gemini 自定义编辑器 + TrustedHTML | 使用 `chrome_javascript` + `textContent` + `createElement`（见 Step 3） |
| 等待 180 秒仍未出现图片 | 生成超时 | 用 `chrome_read_page` 检查页面状态，查看是否有错误信息 |
| "Image Generation Limit Reached" | 达到日限额 | 告知用户，建议换账号或等待次日 |
| "Can't create it right now" | 认证/区域限制 | 检查账号状态和网络 |
| `<generated-image>` 元素找不到 | UI 变更或生成失败 | 用 `chrome_read_page` 重新探测页面结构，检查是否有错误提示 |
| 图片 blob URL 已存在但尺寸持续为 0（5 次重试后） | Gemini 标签页在后台未渲染（尤其无痕窗口） | **仍返回 blob URL**，提示用户切换到 Gemini 标签页查看 |
| 页面弹出随机对话框 | Gemini 的确认弹窗 | 用 `chrome_read_page` 识别弹窗，用 `chrome_click_element` 或 `chrome_handle_dialog` 处理 |

---

## 使用示例

### 示例 1：高质量图片生成（展示完整 prompt 工程）

```
用户: "帮我用 Gemini 生成一张赛博朋克风格的东京夜景图片"

构造的高质量 prompt:
"Generate a cyberpunk Tokyo alleyway at midnight, neon kanji signs reflecting 
in rain puddles on the asphalt, steam rising from street vents and ramen shop 
exhausts, a solitary figure in a translucent raincoat silhouetted against pink 
and electric blue neon, wet surfaces gleaming under harsh artificial light, 
cinematic low-angle wide shot, volumetric lighting, blade runner aesthetic, 
shot with 24mm wide lens, 16:9 aspect ratio"

执行流程:
1. 不在 Gemini → chrome_navigate(url="https://gemini.google.com/app")
2. chrome_javascript → 输入上面的 prompt
3. chrome_keyboard(keys="Enter") 或点击发送按钮
4. 轮询等待 → <generated-image> 出现
5. chrome_javascript → querySelector('generated-image img').src
6. 返回 blob URL → 结束
```

### 示例 2：中文提示语

```
用户: "画一张水墨画风格的山间小径"

构造的高质量 prompt:
"Generate a traditional Chinese ink wash painting (sumi-e style) of a winding 
stone path through misty mountains, ancient pine trees clinging to cliffs, 
a small wooden bridge over a stream, layers of fog creating depth, minimalist 
brushwork with expressive ink splashes, rice paper texture, muted black and 
grey tones with subtle ochre accents, vertical 9:16 composition"

执行流程:
1. 导航 → Gemini
2. 输入上面的 prompt（英文效果更好）
3. 提交并等待
4. 提取 blob URL → 返回
```

### 示例 3：产品图 + 图片内文字

```
用户: "做一张咖啡品牌的产品图，图片上要有 'Good Morning' 文字"

构造的高质量 prompt:
"Create a flat-lay Instagram photo for a specialty coffee brand. A ceramic 
latte cup with fern-pattern latte art on a distressed wooden table, scattered 
coffee beans and a cinnamon stick, warm morning sunlight from 10 o'clock 
creating soft shadows. The text 'Good Morning' appears in the coffee foam 
in elegant cursive script. Minimalist, cozy aesthetic, 85mm macro lens, 
shallow depth of field, warm Kodak Portra 400 color palette, 1:1 square format"
```

### 示例 4：批量生成

```
用户: "用 Gemini 分别生成：一只猫、一只狗、一只兔子"

执行流程:
按顺序执行三次完整的 Step 1-6 流程，每次修改 prompt：
- "a fluffy orange tabby cat with emerald eyes, sitting on a velvet cushion, 
   morning window light, 85mm portrait lens, photorealistic, 1:1"
- "a golden retriever puppy running through a field of wildflowers, golden hour 
   backlighting, motion blur on tail, 50mm lens, photorealistic, 16:9"
- "a white rabbit with floppy ears on a moss-covered log in an enchanted forest, 
   soft diffused sunlight through leaves, macro shot, fairy tale aesthetic, 1:1"

每次生成完毕后提取 blob URL，依次返回三个 URL。
```

### 示例 5：编辑已有图片（多指令）

```
用户: "把这张图片的背景换成海滩，加上 'SUMMER' 文字"

构造的高质量 prompt:
"Make ALL of the following edits to the image:
- Replace the background with a sunny tropical beach, turquoise water, 
  white sand, palm trees on the left
- Add the text 'SUMMER' in bold white sans-serif font in the top-right 
  corner of the sky
- Increase the overall warmth and saturation for a summer vibe
Maintain: original subject lighting direction, subject sharpness, and composition.
NEVER change: the subject's appearance, pose, or clothing."
```

---

## 最佳实践

### Prompt 相关

1. **叙事优先，拒绝关键词堆砌**：NanoBanana 是 autoregressive 语言模型，处理 prompt 时如创意总监读 brief——用自然段落描述场景，而非逗号分隔的标签列表（那是 Midjourney/Stable Diffusion 的做法）。
2. **极度具体**：每个名词加形容词，每个形容词加修饰语。`fantasy armor` → `ornate elven plate armor, etched with silver leaf patterns, pauldrons shaped like falcon wings`。
3. **正向描述替代否定**：「描述你要什么，而非你不要什么」。不说 `no cars`，说 `an empty sun-drenched road`。
4. **摄影术语加持**：`85mm f/1.8 portrait lens`、`golden hour`、`Kodak Portra 400`、`shallow depth of field` 等术语能显著提升真实感和构图质量。
5. **ALL CAPS 标记关键约束**：用 `MUST`、`EXACTLY`、`NEVER` 强调不可违反的要求。
6. **英文优先**：英文 prompt 在 Gemini 中的识别精度和效果通常优于中文。中英混合策略最优——技术参数用英文，文化情感用中文。
7. **宽高比显式声明**：在 prompt 中明确 `16:9`、`1:1`、`9:16` 等。如宽高比失效，用参考图 trick（上一张正确比例的图做锚）。
8. **迭代精炼**：第一张不满意→补充细节→再生成。风格漂移时开新会话，用详细文字描述重置。
9. **图片内文字精准定位**：`The text 'SALE' is written on a red hangtag attached to the handle`，而非 `add text "SALE"`。

### 操作相关

10. **轮询间隔**：每 3-5 秒检查一次，避免过于频繁的 DOM 查询。
11. **超时设置**：图片生成最多等待 180 秒，超过则报告超时。
12. **登录态检查**：每次运行前检查登录态，避免生成失败后才排查。
13. **选择器优先级**：优先使用 `generated-image img` 和 `data-test-id` 选择器，它们跨语言更稳定。
14. **速率控制**：Gemini 有日额度限制（免费约 20 张/天），批量生成时注意间隔（每次间隔 5-10 秒）。
15. **新会话重置**：长会话中角色漂移或风格偏航时，开新会话 + 完整 prompt 描述重置。
16. **Blob URL 优先**：不点击下载按钮、不查文件系统。直接提取 `<generated-image>` 中的 blob URL 即可。
17. **处理 lazy loading**：Gemini 图片使用 `loading="lazy"`，检测 blob URL 后先 `scrollIntoView` 再读 `naturalWidth`，否则始终为 0。
18. **保持标签页激活**：轮询前用 `chrome_switch_tab` 激活 Gemini。无痕窗口下切换可能受限，5 次重试（~25秒）无果后提示用户手动介入。

---

## 注意事项

- **唯一目标**：提取生成的图片 blob URL → 返回 URL。到此为止，不做任何后续处理。
- **不要操作下载按钮**：不点击下载、不查 Downloads 目录、不移动文件——这些操作依赖 OS 层，不可靠。
- **不要直接操作 Gemini 的 API**（如 Gemini API Key 调用）—— 本 skill 专门通过浏览器 UI 自动化完成。
- **不要假设选择器永远有效** —— Google 频繁更新 UI。如果主选择器失效，使用 `chrome_read_page` 重新探测页面结构。
- **水印问题**：Gemini 生成的图片包含 SynthID 数字水印（不可见），这是 Google 的设计，无法且不应移除。
- **生成速度**：受网络状况、Gemini 服务器负载、提示语复杂度影响，15-60 秒是正常范围。
- **Blob URL 生命周期**：仅在 Gemini 页面打开期间有效。页面刷新/关闭后 URL 失效。用户如需永久保存，可在浏览器中打开 blob URL 后手动另存为。

---

## 参考资源

- [selectors.md](references/selectors.md) — Gemini UI DOM 选择器完整参考
