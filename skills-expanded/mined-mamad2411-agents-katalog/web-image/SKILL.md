---
name: web-image
description: >
  用前端渲染生成图片 —— 不依赖模型的多模态能力，任何能写 HTML/CSS 的模型
  (DeepSeek / Claude / Kimi / GPT 等) 都能用。

  当用户要「生成/做/画一张图」且属于以下任意一种时使用：头像、图标、公众号封面、
  OG 分享图、Banner/横幅、小红书封面、知识卡片、金句卡、代码片段图、数据卡、
  功能发布图、对比图、步骤图、视频封面/缩略图、幻灯片单页、活动海报、名片、
  二维码卡、配图、题图、缩略图、poster、cover、thumbnail、banner、avatar。

  也用于：批量出多个尺寸/多平台的同一张图；把一段文字/数据/代码变成图；
  给文章配图；做一套风格统一的系列图。

  支持指定视觉风格，共 32 套：手绘/涂鸦/白板、黑板、水彩、拼贴/剪贴、博物图鉴、
  瑞士国际主义、杂志编辑部、报纸、工程蓝图、档案手稿/打字机、包豪斯、装饰艺术 Art Deco、
  双色印刷 Riso、粗野主义、孟菲斯、美漫波普、像素 8-bit、千禧 Y2K、蒸汽波、霓虹赛博朋克、
  街头海报/喷漆、日式侘寂、中式水墨、国潮/新中式、终端 CLI、极光渐变、玻璃拟态、
  奢侈品黑金、极简产品、电影海报、复古未来 70s、极简线条。
  用户没指定时主动报 3~4 个候选让他选；说了库里没有的风格就按四步法拆成 token。

  产出一个可预览的画板工作台页面，多种画幅并排展示，点按钮即可导出 PNG
  (页内零依赖导出 + 本机 Chrome 精确出图两条通道)。

  不适用：需要照片级真实内容的图（人像、风景、材质渲染）—— 那需要真正的图像模型。
---

# web-image · 用网页生成图片

**核心**：浏览器就是渲染引擎。用 HTML/CSS 精确描述画面，导出成真实像素的 PNG。
结果可复现、可微调、可版本管理，而且不需要模型有生图能力。

> 下文的 `$SKILL` 指本 skill 所在目录。Claude Code 下是 `~/.claude/skills/web-image`；
> 装在别处就替换成实际路径（也可以先 `export SKILL=<路径>` 再照抄命令）。

## 流程

### 1. 定尺寸
问清楚**发到哪**（公众号？小红书？X？做封面还是头像？），然后查 `references/formats.md` 取预设像素。
用户没说就默认 `og` 1200×630；说"多个平台"就并排出多张画板，不要做"通用图"。

### 2. 选场景配方
在 `references/scenes.md` 找对应场景，照它的**画面结构**和**文案字数上限**来。
文案先压到额度内，再排版——这一步决定了成图好不好看。

### 3. 定风格（这一步决定成图是"设计"还是"模板"）

**用户指定了风格** —— 在 `references/styles.md` 里按 slug 或别名对号入座，
照抄它的 token 和**签名手法**。签名手法是这套风格的辨识度所在，色值只是入场券，不能只换颜色。
每套还标了「常用画幅」——用户没指定尺寸时优先按它来，风格和画幅是配套的。

**用户没指定** —— 不要默认套一个，也不要报全表。从 `styles.md` 末尾的「推荐话术」里
挑 3~4 个跟他内容气质最近的，一句话一个报出去让他选。比如做技术内容就报
「工程蓝图 / 终端 / 瑞士国际主义 / 粗野主义」，做生活方式就报
「日式侘寂 / 杂志编辑部 / 档案手稿 / 中式水墨」。用户说"你看着办"再自己定。

**用户描述了一个库里没有的风格**（"像 A24 电影海报"、"我们品牌是这样的"）——
按 `styles.md` 末尾的四步法把参照物拆成 token：取 4 个色 / 定字体反差 / 找签名手法 / 定留白比例。

选定后照 `references/design.md` 实现：中文排版、构图、高级感技法、纹理配方都在那里，
最后对照文末的「AI 味清单」自查。

### 4. 生成工作台页面
```bash
mkdir -p out && cp $SKILL/assets/{studio.css,studio.js,export.js} out/
```
以 `assets/studio.html` 为骨架写 `out/index.html`：`:root` 里放主题变量，每张图一个 `.wi-card`。

**画板契约（不要改）**：
```html
<section class="wi-card" id="cover" data-w="1200" data-h="630" data-file="og-cover">
  <div class="wi-head">
    <span class="wi-name">OG 分享图</span>
    <span class="wi-use">用于: 微信/Slack 链接预览</span>
  </div>
  <div class="wi-frame"><div class="board og">…画面…</div></div>
</section>
```
- `data-w/data-h` = 真实导出像素，必填。
- **不要在 CSS 里给 `.board` 写 width/height**，脚本会按 data 属性设置。
- 画面样式写在页面自己的 `<style>` 里，`studio.css` 只管工作台外壳。

### 5. 展示 + 导出
用浏览器打开 `out/index.html`（本会话可用 preview 工具，或 `open out/index.html`）。
页面顶部有：缩放、构图网格、全部导出 1x/2x；每张画板有：导出 2x / 1x / 复制到剪贴板。

需要最终稿或批量出图：
```bash
node $SKILL/scripts/shot.mjs out/index.html --scale 2
```

要把出好的图拼成一张总览（作品集、系列合集）：
```bash
node $SKILL/scripts/contact.mjs out/png/*.png --cols 5 --label
```

## 导出安全清单（写代码时就要遵守）

页内导出走 SVG `foreignObject`，所以：

- ✅ 用系统字体栈（`references/design.md` 里有现成的）
- ✅ 图形用 CSS 渐变 / 内联 `<svg>` / 伪元素 / emoji
- ❌ 不用外链图片（要用就转 data URI）
- ❌ 不用外链 webfont（要用就 base64 内嵌进 `<style id="export-fonts">`）
- ❌ 不用 `backdrop-filter`

违反了也不会崩——页面会提示，并且 `shot.mjs` 那条通道照样能出图。详见 `references/export.md`。

## 出图前自检

1. 这套风格的**签名手法**做出来了吗？（只换了颜色不算）
2. 把预览缩到 **15%** 看一眼——信息流里就是这个大小，主标题读得出来吗？
3. 主标题和最小字号差 **5 倍**了吗？
4. 有**一个**明确的焦点，还是一堆东西一样大？
5. 边距是短边的 6%~9% 吗？关键信息避开了平台遮挡区（见 formats.md 的安全区）吗？
6. 中文标题是手动 `<br>` 断的吗？（`max-width:…ch` 对 CJK 会算错一倍，容易折出孤字）
7. 文案是具体的，还是"赋能/提升效率"这种空话？

## 参考文件

| 文件 | 什么时候读 |
|---|---|
| `references/formats.md` | 定尺寸时。全部预设像素、各平台安全区、打印换算 |
| `references/scenes.md` | 定内容时。16 种高频场景的结构、字数上限、翻车点 |
| `references/styles.md` | **定风格时。32 套风格：出身、气质、token、签名手法、适用场景，末尾有推荐话术** |
| `references/design.md` | 实现时。中文排版、构图、高级感技法、纹理与有机形配方、AI 味清单 |
| `references/export.md` | 导出出问题时。两条通道对比、限制、排错表 |
| `examples/styles.html` | **需要看风格长什么样时。32 套各用最擅长的画幅 + 真实场景文案，7 种画幅，可直接打开对比和导出** |
| `examples/index.html` | 需要多画幅范例时。1:1 / 2.35:1 / 5:2 / 3:4 四种画幅 |
