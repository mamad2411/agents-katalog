---
name: canvas-to-social
description: 当需要把 flipbook-skill 画册（按 canvasId）转成社交平台图文时使用 —— 包括把节点图片+文案导出为素材包，以及把内容发布到抖音（creator.douyin.com）。触发词：画册发抖音、export canvas to social、发布到抖音、canvas 转图文。
---

# 画册转社交图文 (canvas-to-social)

## 概述
有意拆成两个独立阶段：
1. **导出（确定性、可脚本化、平台无关）**：从 flipbook-skill 数据存储读取一个画册，生成
   `social-export/<主题>/` 包——图片按阅读顺序重命名，外加 `文案.md`（主帖正文+逐图说明）
   和 `manifest.json`。这份导出包与具体平台无关，可复用于任意目标平台。
2. **发布（浏览器自动化、需人工判断、按平台不同）**：操作已登录的创作者中心网页，上传图片、
   填标题/正文、选音乐/话题、可选地选合集——然后**停下来，让用户自己点「发布」**。

支持的发布平台（细节见各自的 reference）：
- **抖音**：`references/publishing-douyin.md`（creator.douyin.com，图片 ≤ 35 张，可选 BGM/合集）。

> 目前仅抖音发布流程已实测可用。未来要新增平台（如小红书）时，按本目录的
> `publishing-douyin.md` 结构新增一份 `publishing-<平台>.md`，并在上表登记即可——
> 导出阶段无需改动。

## 何时使用
- "把某画册/canvas 发成抖音图文" / "export canvas to social" / "发布到抖音"。
- 你拿到了一个 `canvasId`（位于 `server/data/canvases/` 下的文件夹）。
- 只要图片+文案时，单独用阶段一；要自动填充帖子时，再加上阶段二（按目标平台选对应 reference）。

## 阶段一 —— 导出（平台无关）

运行脚本（仅用标准库，无第三方依赖）。`--data-root` 默认是 `server/data`；如果当前
工作目录不是 app 根目录则需覆盖。
```bash
python3 scripts/export_canvas.py <canvasId> \
  --data-root /path/to/app/server/data \
  --limit 35 \
  --hashtags "#话题1 #话题2"
```
- BFS（根节点优先）排序 → 图片命名为 `01-标题.png` … `NN-标题.png`。
- `--limit 35` 强制套用抖音图文上限；超过 35 会打印警告。
- 输出目录默认 `social-export/<主题>`；脚本最后会打印 `OUT_DIR=...`。

随后和用户一起打磨文案：原始图说偏百科书面语。主动提议：(a) 挑出最佳 N 张图，
(b) 改写成口语化、有钩子的短文案 + 吸睛标题。务必遵守目标平台的字数/图片上限
（抖音：**标题 ≤ 20 字、正文 ≤ 1000 字、图片 ≤ 35 张**，详见 references/publishing-douyin.md）。

## 阶段二 —— 发布（可选，按平台分流）

**必须**：用 `browser` SKILL（CDP）驱动用户已登录的 Chrome。
`browser-harness` 命令需已在 `$PATH` 上（单独安装）。

按目标平台打开对应 reference 逐步执行：

| 目标平台 | reference | 图片上限 | 关键差异 |
|----------|-----------|----------|----------|
| 抖音 | `references/publishing-douyin.md` | 35 | 有 BGM、有「图解世界」合集 |

抖音发布骨架（细节严格按 `references/publishing-douyin.md` 第 1-7 步）：

| 步骤 | 操作 | 关键坑 |
|------|------|--------|
| 1 | 打开 creator.douyin.com → 发布图文 | 按文字定位入口，别用固定坐标 |
| 2 | 上传图片 | 用 harness 的 `upload_file(选择器, 排序列表)`，别手写 raw cdp |
| 3 | 标题（≤20字） | 用 prototype value setter + 派发 input/change 事件 |
| 4 | 正文（≤1000字） | contenteditable 用 `execCommand('insertText')`；话题写成纯文本 `#词` |
| 5 | 音乐 | 「使用」按钮只在悬停某行时出现；派发 hover 事件后再 `.click()` |
| 6 | 合集（可选） | 存在「图解世界」就选，否则跳过；绝不自动新建 |
| 7 | 校验 + 停手 | 报告状态；定位「发布」按钮但**绝不点击** |

## 唯一铁律
**永远不点最终的「发布」按钮。** 它不可逆且对外公开。填好所有内容、校验，然后把
最后一步交给用户。「存草稿」仅在用户明确要求时才点。

## 不要读图
**不要用 Read 工具去查看/识别导出的图片本身。** 文案一律基于 `文案.md` 的文字图说改写，
图片只按 `manifest.json` 的阅读顺序原样上传。无需打开、预览或多模态识别任何 `.png`。
（核对上传结果时也用 `js()` 读取页面 DOM/计数，而非看图。）

## 常见错误
- **跨步骤复用坐标。** 页面会滚动和重渲染；每次点击前都按文字/placeholder 重新查询
  元素位置。
- **往标题/正文里用 `type_text`。** React/Semi 输入框会丢键或截断。改用对应 reference 里的
  value-setter / `execCommand` 写法。
- **手写 `cdp("DOM.setFileInputFiles", …)` 加手动遍历节点树。** 很脆弱，且 `cdp()`
  helper 会拒绝带 `sessionId` 的键。用 `upload_file`。
- **未经确认就发布。** 不要。停在发布前那一步。
- **导出超过平台上限还全部上传。** 抖音上限 35；超出会被拒收/截断。
