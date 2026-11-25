---
name: generate-slide
description: PPT 生成 Skill，根据需求生成 YAML 并上传到 slide-ai 网站
---

# generate-slide

根据用户的主题描述，生成一套完整的 PPT YAML 配置，上传到 slide-ai 后端服务。

## 使用方式

```
/generate-slide <主题描述>
```

示例：
```
/generate-slide 面纱规则系统技术介绍，包含背景、架构、算法三个部分
/generate-slide 2024年Q3业务数据汇报，5页
```

---

## 执行步骤

### 1. 理解需求

从用户描述中提取：
- 主题和受众
- 大致页数（未指定默认 5-8 页）
- 内容结构（章节划分）

### 2. 阅读参考资料

在生成前必须阅读所需的布局和组件说明：

**布局（layouts）**
- [`references/layouts/title.md`](references/layouts/title.md) — title / section / quote / qa
- [`references/layouts/single.md`](references/layouts/single.md) — single（单内容区布局）
- [`references/layouts/split.md`](references/layouts/split.md) — split（左右分栏，适合对比）
- [`references/layouts/header-body.md`](references/layouts/header-body.md) — header-body（顶部说明 + 主体内容）
- [`references/layouts/compose.md`](references/layouts/compose.md) — compose（多列/多区布局）

**内容块（blocks）**
- [`references/blocks/bullets.md`](references/blocks/bullets.md) — 要点列表
- [`references/blocks/markdown.md`](references/blocks/markdown.md) — Markdown 文本
- [`references/blocks/kpi.md`](references/blocks/kpi.md) — 关键指标卡片
- [`references/blocks/table.md`](references/blocks/table.md) — 表格
- [`references/blocks/image.md`](references/blocks/image.md) — 图片
- [`references/blocks/arch.md`](references/blocks/arch.md) — 架构层次图
- [`references/blocks/flow.md`](references/blocks/flow.md) — ReactFlow 流程图
- [`references/blocks/swimlane.md`](references/blocks/swimlane.md) — 泳道图
- [`references/blocks/timeline.md`](references/blocks/timeline.md) — 时间线（横向/竖向）

**SmartArt**
- [`references/blocks/cycle.md`](references/blocks/cycle.md) — 循环图
- [`references/blocks/linear.md`](references/blocks/linear.md) — 线性流程图
- [`references/blocks/radial.md`](references/blocks/radial.md) — 辐射图
- [`references/blocks/pyramid.md`](references/blocks/pyramid.md) — 金字塔图
- [`references/blocks/funnel.md`](references/blocks/funnel.md) — 漏斗图
- [`references/blocks/matrix.md`](references/blocks/matrix.md) — 四象限矩阵图

**示例**
- `skill/generate-slide/examples/` — 各类组件完整示例

### 3. 规划页面结构

典型结构（可根据内容调整）：
```
1. title      — 封面
2. section    — 章节过渡页（如有多章节）
3. single     — 内容页（bullets / arch / cycle / linear 等）
4. ...
5. qa         — 结尾
```

选择组件原则：
- 流程、步骤 → `linear`
- 循环、迭代 → `cycle`
- 层级架构 → `arch`
- 对比、矩阵 → `matrix`
- 漏斗、转化 → `funnel`
- 时间线、路线图 → `timeline`
  - 事件较少（3-6 个）→ `direction: horizontal`
  - 事件较多（7+）→ `direction: vertical`
- 关键数据 → `kpi`
- 文字说明 → `bullets` / `markdown`

### 4. 生成 YAML 文件

**deck id**：用英文小写+连字符，如 `mask-master-intro`

**`_meta.yml`**：
```yaml
title: "PPT 标题"
author: <用户名>
slides:
  - title
  - section-1
  - page-1
  - ...
  - qa
```

每页单独一个 `.yml` 文件，文件名与 slides 列表对应。

严格遵循 `references/layouts/` 和 `references/blocks/` 中的 schema，不得使用文档未定义的字段。

### 5. 保存文件

将所有 YAML 文件写入当前工作目录的 `decks/<deck-id>/` 下：

```
decks/
└── <deck-id>/
    ├── _meta.yml
    ├── title.yml
    ├── page-1.yml
    └── ...
```

如需写到其他位置，记录完整路径，在下一步上传时作为第二个参数传入即可。

### 6. 上传到服务

使用 `skill/generate-slide/client.py` 上传：

```bash
# 默认从 decks/<deck-id>/ 读取
python skill/generate-slide/client.py <deck-id>

# 指定自定义目录
python skill/generate-slide/client.py <deck-id> /path/to/deck
```

输出示例：
```
[upload] mask-master-intro (decks/mask-master-intro) ...
[ok] 面纱规则系统介绍 · 6 页
[link] http://slide.liamzheng.cn/?deck=mask-master-intro
```

环境变量：
- `SLIDE_AI_URL` — 服务地址，默认 `http://slide.liamzheng.cn`
- `SLIDE_AI_API_KEY` — 手动指定 API Key，不设置时自动注册并保存到 `~/.slide-ai/config.json`

### 7. 返回结果

告知用户：
- 生成了几页
- 访问链接：`http://slide.liamzheng.cn/?deck=<deck-id>`
- 如需调整，可直接修改 `decks/<deck-id>/` 下的 YAML 文件

---

## 账号与 API Key

### API Key

首次运行 `client.py` 时会自动匿名注册，生成一个 API Key 并保存到 `~/.slide-ai/config.json`：

```json
{
  "api_key": "d766c14a180f4108894bb7feef538dbf"
}
```

API Key 是上传 deck 的凭证，每次上传时自动使用，无需手动填写。

如需在多台设备使用同一账号，可通过环境变量指定：

```bash
export SLIDE_AI_API_KEY=<your-api-key>
```

### 注册账号（可选）

匿名用户可以上传和分享 deck，但无法通过网页查看自己的 deck 列表。
注册账号后可在网页登录，查看所有历史 deck。

1. 访问 `http://slide.liamzheng.cn` 注册账号
2. 在 CLI 执行绑定，将本地 api_key 切换到该账号：

```bash
python skill/generate-slide/client.py bind --user <username>
# 或直接传入密码，省去交互提示
python skill/generate-slide/client.py bind --user <username> --passwd <password>
```

输入注册时的密码即可，之后上传的 deck 均归入该账号。

### 分享 deck

上传后返回的链接格式为：

```
http://slide.liamzheng.cn/?deck=<deck-id>&token=<access-token>
```

链接自带访问 token，他人无需登录即可查看该 deck。
登录用户访问自己的 deck 时，播放页有"返回"按钮可回到列表页。

---

## 注意事项

- 内容要简洁，每页不超过 5 个要点
- 标题用中文，技术术语保留英文
- 优先使用图形化组件（arch/cycle/linear），避免纯文字堆砌
- `_meta.yml` 的 `slides` 列表顺序决定页面顺序，必须与文件名对应
