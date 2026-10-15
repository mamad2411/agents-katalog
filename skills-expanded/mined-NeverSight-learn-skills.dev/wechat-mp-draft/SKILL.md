---
name: wechat-mp-draft
description: 代写微信公众号文章并保存到公众号草稿箱。使用场景：用户需要撰写公众号文章并直接发布到微信公众号后台草稿箱；或排查公众号草稿箱里的「标题在文章顶部重复显示两次」「标题行既出现在 title 字段又出现在 body」等 markdown-renderer 标题重复问题。触发词："写公众号文章"、"保存到公众号草稿"、"微信文章"、"公众号发文"、"标题重复"、"草稿标题显示两次"。
---

# 微信公众号草稿 Skill

编写微信公众号文章并保存到草稿箱，流程如下：


1. 基于用户输入，调用SKILL `/jackyshen-write-wechat-article` 或其他类似的技能，改写为微信公众号风格的文章，md格式（首行为 `# 标题`）
2. **从 markdown 中删除首行 `# 标题`**，避免标题在 body 里重复显示（详见「问题 5」）
3. 调用SKILL `/wechat-markdown-html-render` 来分别渲染文本和代码样式，得到html格式的输出文件。
4. 调用SKILL `/huny-img` 或其他任何可用的文生图片(image generation)SKILL来配**1张封面图**（ar 2.35:1）
5. 调用SKILL `/huny-img` 或其他任何可用的文生图片(image generation)SKILL来生成 **2 张新生成的内容图片**，然后插入渲染后的正文 HTML 中。位置一般在头部一张（为了尽早吸引读者兴趣），中部一张（让读者保持兴趣继续读），具体位置和图片主题由 AI 根据文章内容来建议。
6. 继续调用本SKILL的工作流程来访问微信公众号文章草稿箱，标题作为 `title` 参数传入，body 只包含正文（`add_draft.sh` 也会自动剥离 body 开头 H1 作为最后一道防线）


## 前置条件

需要以下凭证（需自行配置）：
- AppID: `wxYOUR_APPID_HERE`
- AppSecret: `YOUR_SECRET_HERE`

**获取方式：** 微信公众平台 → 设置与开发 → 基本配置

**重要：** 服务器 IP 必须添加到公众号后台的 IP 白名单中。

## 工作流程

### 1. 获取 Access Token

```bash
./scripts/get_access_token.sh
```

### 2. 上传封面图片（获取 thumb_media_id）

**封面图片是必填项！**

```bash
./scripts/upload_image.sh <access_token> <图片路径>
```

返回示例：
```json
{"media_id":"xxx","url":"http://mmbiz.qpic.cn/..."}
```

### 3. 将撰写的文章HTML保存到草稿箱

**⚠️ 标题分离规则（防止标题在 body 里重复显示）：**

- 微信公众号后台从 `title` 字段渲染文章标题，并自动显示在文章顶部
- 如果 markdown 源文件以 `# 标题` 开头（来自 `/jackyshen-write-wechat-article` 的标准输出），`/wechat-markdown-html-render` 会把它渲染成 body 里的 `<h1>`
- 必须**只把标题传给 `title` 参数**，**不能让它留在 body 里**，否则用户会在文章顶部看到两次标题
- `add_draft.sh` 已内置**自动剥离 body 开头 H1** 的 sanitizer，作为最后一道防线：即使你没注意把 `# 标题` 留在了 markdown 里，脚本也会自动剥离并打印 ✅ `标题去重` 提示

```bash
./scripts/add_draft.sh <access_token> <标题> <HTML内容> <thumb_media_id> [AUTHOR] [摘要]
```

### 4. 在正文 HTML 中插入 2 张新生成的内容图片

> **为什么必须用本接口**：微信规定正文里的图片 url 必须来自 `cgi-bin/media/uploadimg`，外部图片 url 会被过滤掉。本步骤会调 `/huny-img` 生图 → 下载到本地 → 上传获取永久 URL → 按 AI 建议位置插入 HTML。

#### 4.1 调用 `/huny-img` 生成图片（获取临时 URL，1 小时内有效）

```bash
~/.pyenv/versions/py312-huny-img/bin/python ~/.agents/skills/huny-img/scripts/hunyuan3-text-to-image.py \
  -p "<AI 根据文章上下文设计的第一张图 prompt>" \
  -r 16:9
```

输出形如 `图片URL: https://...`，记录备用。

#### 4.2 下载到本地（临时 URL 1 小时后过期，必须立刻下载）

```bash
curl -s -o /tmp/content_img_1.jpg "<huny-img 返回的临时 URL>"
```

#### 4.3 调用 `upload_content_image.sh` 上传到微信（获取正文可用 URL）

```bash
RESP=$(./scripts/upload_content_image.sh "$TOKEN" /tmp/content_img_1.jpg)
URL_1=$(echo "$RESP" | jq -r '.url')
```

> 与 `upload_image.sh`（封面永久素材）的区别：本接口返回 `url` 字段（不是 `media_id`），且**不占公众号 10 万永久素材额度**。仅支持 JPG/PNG，文件 ≤1MB。

重复 4.1–4.3 得到第二张图的 `URL_2`。

#### 4.4 用 `insert_content_image.py` 按 AI 建议的位置插入到 HTML

AI 先通读 HTML，挑选 2 个插入点（一般在文章中部、与上下文自然衔接处），可用以下任一方式指定：

**单张插入（命令行）**

```bash
# 在第 N 个 <p> 段落后插入
./scripts/insert_content_image.py \
  --input article.html --output article_with_imgs.html \
  --url "$URL_1" --after-paragraph 3

# 或在指定 marker（HTML 子串）后插入
./scripts/insert_content_image.py \
  --input article_with_imgs.html --output article_final.html \
  --url "$URL_2" --after-marker "<h2>核心观点</h2>"
```

**批量插入（JSON spec，一次完成多张）**

```bash
cat > /tmp/img_spec.json <<EOF
[
  {"url": "$URL_1", "after_paragraph": 3},
  {"url": "$URL_2", "after_marker": "<h2>核心观点</h2>"}
]
EOF

./scripts/insert_content_image.py \
  --input article.html --output article_final.html \
  --spec /tmp/img_spec.json
```

> 生成的 `<img>` 标签**紧凑无多余空格**：`<img src="URL"/>`，直接可用。

#### 4.5 将含图的最终 HTML 提交草稿

```bash
FINAL_CONTENT=$(cat article_final.html)
./scripts/add_draft.sh "$TOKEN" "标题" "$FINAL_CONTENT" "$THUMB_ID" "作者" "摘要"
```

## 关键问题与解决方案

### ❌ 问题 1：40007 invalid media_id

**两种触发场景：**
- **封面 `thumb_media_id`：** 是必填字段；封面图片必须是**永久素材**（通过 `add_material` 接口上传），不能直接用外部 URL。
- **草稿 `media_id` 已失效：** 草稿在公众号后台被打开 / 编辑 / 删除后，`media_id` 立即失效（即使是几分钟前刚返回的）。`draft/update` 和 `draft/get` 都会返回 40007。

**解决：**
- 封面图：先上传永久素材：
  ```bash
  curl -F "media=@cover.jpg" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=image"
  ```
- 草稿失效：调 `cgi-bin/draft/batchget` 拿当前 id 列表（可能为空，说明被删了），再决定是 `update` 已有还是重新 `add`：
  ```bash
  curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=$TOKEN" \
    -H "Content-Type: application/json" -d '{"offset":0,"count":10,"no_content":1}'
  ```

### ❌ 问题 2：IP 不在白名单（40164）

**解决：** 登录微信公众平台 → 设置与开发 → **基本配置** → 公众号开发信息 → IP白名单 → 添加服务器 IP

**注意：** 不要错加到「**安全中心** → 登录IP白名单」—— 那个只控制后台登录，对 `cgi-bin/token` API 无效。新加的 IP 通常立即生效，但偶尔有 1–2 分钟传播延迟，失败时先等再重试。如果 IP、AppID、白名单位置都核对过仍然失败，多半是 IP 添加到了错误的公众号账号（多账号情况），需对照 `config.sh` 里的 AppID 前缀重新检查。

### ❌ 问题 3：HTML 内容格式错误

**解决：**
- HTML 中的换行符会导致 JSON 解析失败
- 必须将换行符替换为空格
- 使用 `tr '\n' ' '` 处理

### ❌ 问题 4：有序/无序列表在公众号编辑器里渲染异常

公众号编辑器的 HTML ingester 有两个非标准行为，会让 `<ol>` / `<ul>` 列表静默崩坏。`add_draft.sh` 已内置防御性 sanitizer 处理后者并对前者发出警告，但理解病根才能不再踩坑：

| 症状 | 根因 | 修复 |
|---|---|---|
| 项目左侧没有 `1. 2. 3.` 编号或 `•` 符号，行间还多出空行 | `<li>` 内含块级子元素 `<section>` —— marker 被嵌套块"抢走"，section 的 `margin-top/bottom` 还顶出空行 | `<li>` 直接放文字，section 样式合并到 `<li>` 上 |
| 编号有了但变成 `1. (空) / 2. real / 3. (空) / 4. real / …`，N 个真实项目渲染成 ~2N+1 行 | `<ol>` / `<ul>` 内 `<li>` 兄弟之间的空白文本节点（空格、换行、Tab）被当成额外空 `<li>` | `<ol>↔<li>`、`</li>↔<li>`、`</li>↔</ol>` 三处空白全部 strip，**只 strip `\n` 不够**，普通空格也会触发 bug |

正确做法是用 [wechat-markdown-html-render](../wechat-markdown-html-render/) 渲染（该 skill 已内置这两条规则）。如果 HTML 来自其他源，`add_draft.sh` 会自动 strip 列表内空白，并在检测到 `<li><section>` 时打印 WARN（不会阻断发布，因为有时是有意为之）。

**辨别 marker 是否真的缺失：** 从公众号编辑器复制出来的纯文本本来就**不带** `1. 2. 3.` —— 那些是 CSS `::marker` 伪元素生成的、不参与剪贴板。一定要看编辑器**视觉预览区**，不要拿复制出的文本下结论。

### ❌ 问题 5：标题在 body 里重复显示（顶部出现两次）

**症状：** 公众号草稿里，文章顶部标题下面，紧接着又出现一行大号彩色「标题」字样；视觉上同一行字渲染了两次。

**根因：** markdown 源文件以 `# 标题` 开头（来自 `/jackyshen-write-wechat-article` 的标准输出），`/wechat-markdown-html-render` 把这个 H1 渲染进 body 里的 `<h1>` 节点；但 `add_draft.sh` 又把同一字符串作为 `title` 字段传给 API。公众号后台把 `title` 字段渲染为文章标题、把 `content` 字段直接显示在标题下面 —— 所以同一标题出现两次。

**解决：** 永远只把标题作为 `title` 参数传入，body 必须从非 H1 内容开始。`add_draft.sh` 已内置自动剥离：检测到 body 开头是 `<h1>`（可能嵌在 `<section id="nice">` 包装里）就把它移除，并打印：

```
==> Title-h1 self-check: {"h1_stripped_from_body": "xxx", "matches_title_param": true}
✅ 标题去重: body 顶部的 <h1> 已自动剥离（与 title 参数一致），避免重复显示
```

**不要绕过这个剥离。** 如果你想在 body 顶部显示一个不同的大标题（例如「卷首语」或栏目名），用 `## 二级标题` 写 —— 它不会被剥离，也不会和 `title` 冲突。

**辨别脚本是否真的没剥离：** `add_draft.sh` 输出的 JSON payload 里搜 `<h1` —— 应该是 0 次。

## 完整使用示例

```bash
# 1. 获取 token
TOKEN=$(./scripts/get_access_token.sh | jq -r '.access_token')

# 2. 上传封面图
THUMB_RESPONSE=$(./scripts/upload_image.sh "$TOKEN" /path/to/cover.jpg)
THUMB_ID=$(echo "$THUMB_RESPONSE" | jq -r '.media_id')

# 3. 准备文章内容（HTML 格式，body 不能含 <h1>，见「问题 5」）
CONTENT='<p>这里是文章内容...</p>'

# 4. 保存草稿（标题仅作为 title 参数传入）
./scripts/add_draft.sh "$TOKEN" "文章标题" "$CONTENT" "$THUMB_ID" "作者" "摘要"
```

## API 参数说明

### 新增草稿必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 标题，不超过32字 |
| content | string | 是 | HTML内容，不超过2万字符 |
| thumb_media_id | string | 是 | 封面图片永久素材ID |
| author | string | 否 | 作者，不超过16字 |
| digest | string | 否 | 摘要，不超过128字 |
| show_cover_pic | number | 否 | 是否显示封面，0/1 |
| need_open_comment | number | 否 | 是否打开评论，0/1 |
| only_fans_can_comment | number | 否 | 是否仅粉丝可评论，0/1 |

### 支持的 HTML 标签

- `<p>` - 段落
- `<br>` - 换行
- `<section>` - 区块
- `<img>` - 图片（正文 url 必须来自 `media/uploadimg`，外部 url 会被过滤）
- `<strong>`, `<b>` - 加粗
- `<span style="...">` - 带样式的文本
- `<a href="...">` - 链接
- `<h1>`-`<h6>` - 标题

## 错误码速查

| 错误码 | 说明 | 解决 |
|--------|------|------|
| 40001 | access_token 过期 | 重新获取 |
| 40005 | 文件类型非法（uploadimg） | 仅支持 JPG/PNG |
| 40007 | media_id 无效 | 检查封面图是否上传正确 |
| 40009 | 图片尺寸非法（uploadimg） | 压缩图片至 ≤1MB |
| 40164 | IP 不在白名单 | 添加 IP 到白名单 |
| 44002 | POST 数据为空 | 检查请求体 |
| 47001 | 数据格式错误 | 检查 JSON 格式 |

## 注意事项

1. **token 有效期 2 小时**，过期需重新获取
2. **封面图必须先上传**，不能直接引用外部 URL
3. **HTML 内容需转义**，避免 JSON 解析失败
4. **IP 白名单必须配置**，否则无法调用 API
5. **内容大小限制**：正文 < 2万字符，< 1MB
6. **OL/UL 列表会被公众号编辑器篡改**：`add_draft.sh` 已内置 sanitizer 自动 strip 列表内空白；若用其他渠道上传，必须确保 `<li>` 内**不嵌套块级元素**（特别是 `<section>`），并且 `<ol>/<ul>` 与 `<li>` 之间、`<li>` 兄弟之间**零空白**。详见「问题 4」。
7. **草稿 `media_id` 在用户后台操作后立即失效**：`draft/update` 链路只在「同一会话、刚 add 完、用户未介入」时可靠；间隔较长或不确定时，先 `batchget` 再决定 update 还是 add。
8. **标题分离**（核心约定）：标题**只**作为 `title` 参数传入，**不允许**以 `<h1>` 形式留在 body 里。`/jackyshen-write-wechat-article` 输出的 markdown 第一行 `# 标题` 既是标题来源，也必须被剔除。`add_draft.sh` 会自动剥离 body 开头的 `<h1>`（即使嵌在 `<section id="nice">` 包装里），但更稳妥的做法是**渲染前手动从 markdown 中删除 `# 标题` 行**。详见「问题 5」。
9. **正文图片 url 必须来自 `media/uploadimg`**，外部图片 url 会被微信过滤

## 文件结构

```
wechat-mp-draft/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── get_access_token.sh     # 获取 token
│   ├── upload_image.sh         # 上传封面图片（永久素材）
│   ├── upload_content_image.sh # 上传正文图片（获取可在 <img> 中使用的 URL）
│   ├── insert_content_image.py # 将 <img> 标签按指定位置插入 HTML
│   └── add_draft.sh            # 保存草稿
└── references/
    └── api_reference.md        # API 详细文档
```
