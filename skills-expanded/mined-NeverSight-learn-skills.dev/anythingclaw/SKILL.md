---
name: anythingclaw
description: 批量抓取 URL 列表并生成可视化画板。当用户需要：(1) 粘贴一组网址让 AI 帮忙浏览整理，(2) 收集设计灵感/参考图/产品截图，(3) 汇总多个页面的标题、图片、摘要到一个 HTML 瀑布流画板，(4) 研究竞品或做资料调研时使用。支持 agent-browser 真实浏览器抓取（可渲染 SPA）和 WebFetch 轻量抓取两种模式，自动检测可用工具并选择最佳方案。生成卡片式画板并自动在浏览器打开。抓不到的网站会如实标注失败原因。
---

# Anythingclaw

一把"什么都能抓回来"的爪子——把 URL 列表变成可浏览的可视化画板。

## 核心理念

- **双轨抓取**：agent-browser 能渲染 SPA，WebFetch 轻快兜底，自动择优
- **如实汇报**：抓不到就标注失败，不编造内容
- **设计师友好**：输出是 HTML 画板，不是 JSON/CSV
- **场景感知**：内置建筑/设计行业常用站点的抓取策略（参考 `references/architecture_sites.md`）

## 阶段 0：工具检测

在开始抓取前，先检测当前环境有哪些抓取能力：

### 检测 agent-browser

通过 Bash 执行：

```bash
agent-browser --version
```

- **命令成功返回版本号** → 标记 `HAS_AGENT_BROWSER = true`，优先用浏览器模式
- **命令失败（not found）** → 标记 `HAS_AGENT_BROWSER = false`，降级到 WebFetch

如果 agent-browser 不可用，**在对话中告知用户**：

```
提示：当前未检测到 agent-browser，将使用 WebFetch 模式。
WebFetch 无法渲染 SPA 站点（如 Behance、Pinterest），这类网站可能抓取失败。

如需完整浏览器抓取能力，可安装 agent-browser：
  npm install -g agent-browser
  agent-browser install
安装后即可使用，无需重启。
```

然后继续用 WebFetch 执行任务，不要中断。

## 阶段 1：接收输入

用户可能以多种方式提供 URL：

1. 直接粘贴 URL 列表（每行一个或逗号分隔）
2. 在对话中说"帮我看看这几个网站：xxx, yyy, zzz"
3. 指向一个本地文件，例如 `urls.txt`

**解析规则**：
- 提取所有以 `http://` 或 `https://` 开头的字符串
- 去重，保持原始顺序
- 如果用户只给了 1 个 URL，仍然走完整流程（画板会只有一张卡片）

## 阶段 1.5：准备输出目录

在开始抓取前，确保输出目录存在：

```bash
mkdir -p output/screenshots
```

## 阶段 2：逐个抓取

对每个 URL，根据阶段 0 的检测结果选择抓取方式。

### 方式 A：agent-browser 浏览器抓取（优先）

当 `HAS_AGENT_BROWSER = true` 时使用此方式。agent-browser 是 Vercel 出品的 Rust 原生浏览器 CLI，专为 AI Agent 设计，通过 Bash 直接调用。

**每个 URL 的操作步骤**：

1. **导航到页面**：
   ```bash
   agent-browser navigate "<URL>"
   ```
   - 如果导航失败或返回 404/403，**立即标记失败并跳到下一个 URL**，不要浪费时间在死链上。
   - 超时阈值：如果 navigate 超过 15 秒没响应，标记为"HTTP 超时"并跳过。

2. **等待页面加载**（给 SPA 的 JS 渲染留时间）：
   ```bash
   agent-browser wait 3000
   ```

3. **处理弹窗和遮罩**：
   先做一次 `agent-browser snapshot -i`（只看可交互元素），检查是否有 Cookie 同意弹窗或订阅弹窗。常见模式：
   - "Accept" / "同意" / "确定" / "Accept All" / "I Agree" 按钮 → 用 `agent-browser click <ref>` 点掉
   - 右上角关闭按钮（X）→ 点掉
   - 如果弹窗无法关闭，不要卡住，继续提取能拿到的内容

4. **获取页面快照**：
   ```bash
   agent-browser snapshot
   ```
   从快照中提取：标题、描述、作者、标签等文本信息。
   快照返回带 Ref 编号的元素列表（如 `@e1: heading "标题"`），非常紧凑。

5. **提取结构化数据**（通过 JS 执行精确提取）：
   ```bash
   agent-browser eval "JSON.stringify({title:document.querySelector('meta[property=\"og:title\"]')?.content||document.title,description:document.querySelector('meta[property=\"og:description\"]')?.content||'',heroImage:document.querySelector('meta[property=\"og:image\"]')?.content||'',favicon:document.querySelector('link[rel=\"icon\"]')?.href||''})"
   ```
   如果需要提取图片列表，单独执行：
   ```bash
   agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('img')).map(i=>i.src).filter(s=>s&&!s.includes('avatar')&&!s.includes('icon')).slice(0,6))"
   ```

6. **截取页面截图**：
   ```bash
   agent-browser screenshot --full output/screenshots/<domain>-<slug>.png
   ```
   **注意**：路径直接作为位置参数，不用 `-o` 标志。`--full` 表示全页截图。

7. **组装结构化数据**：Agent 根据快照、eval 结果和截图，按照输出数据结构格式整理。

8. **关闭页面**（准备抓下一个）：
   ```bash
   agent-browser close
   ```

**关于超时和重试**：
- 如果某个 URL 的整个抓取流程（navigate → eval → screenshot）超过 30 秒还没完成，直接标记失败跳过
- 不要重试失败的 URL，除非用户明确要求
- 网络超时（如 Dezeen 等海外站）是常见情况，直接标记"HTTP 超时"即可

### 方式 B：WebFetch 轻量抓取（兜底）

当 `HAS_AGENT_BROWSER = false` 时使用此方式。

对每个 URL：

1. 调用 `WebFetch` 工具，获取页面内容

2. **提取优先级**（参考 `references/extraction_guide.md`）：
   - `og:title` / `og:description` / `og:image` 优先
   - 其次 Twitter Card 标签
   - 再次 JSON-LD 结构化数据
   - 最后才是正文 HTML

3. **处理相对 URL**：所有图片路径必须转换为绝对 URL

### 抓取失败处理（两种方式通用）

- 如实记录失败原因（超时 / 403 / SPA 无内容 / 需要登录 / 其他）
- 在画板中单独列出"抓取失败"区域，展示 URL + 失败原因
- **绝不编造数据**

**快速失败原则**：
- **404 / 403 / 5xx**：导航后立即发现就跳过，不浪费 eval/snapshot 步骤
- **空白页面**：snapshot 如果只返回极少元素（< 3 个），大概率是 SPA 空壳或反爬页
- **不要自行替换 URL**：如果用户给的 URL 是 404，标记失败即可。不要自作主张去首页找替代文章——那不是用户想看的内容

### 站点特殊策略

抓取前先检查 URL 的域名，对照 `references/architecture_sites.md` 中的站点列表：
- 如果有该站点的专属策略，按策略执行
- 如果域名匹配"已知反爬极高"的站点（如小红书、Pinterest），提前告知用户该站点抓取成功率较低

## 阶段 3：生成画板

1. 读取 `assets/gallery_template.html` 作为模板
2. 把结构化数据以 **合法 JSON** 格式注入到 `<script type="application/json" id="gallery-data">` 标签中（替换 `__GALLERY_DATA__`）
3. 把任务元数据以 **合法 JSON** 格式注入到 `<script type="application/json" id="meta-data">` 标签中（替换 `__META_DATA__`）
4. **关键：JSON 字符串转义规则**（不遵守会导致画板空白！）：
   - 所有字符串值中的双引号 `"` 必须转义为 `\"`
   - 所有字符串值中的反斜杠 `\` 必须转义为 `\\`
   - 所有字符串值中的换行符必须转义为 `\n`
   - 所有字符串值中的 `</script>` 必须替换为 `<\/script>`（防止提前关闭标签）
   - **推荐做法**：先在脑中组装好标准 JSON 对象，确保是合法 JSON 后再写入文件。不要手动拼接字符串。
5. 如果使用了 agent-browser 截图，截图文件路径使用相对路径 `screenshots/xxx.png`
6. 生成的文件保存到 `output/` 目录
   - 文件名格式：`gallery-{YYYYMMDD-HHmmss}.html`
   - 例如：`gallery-20260424-1030.html`

## 阶段 4：打开画板

Windows 环境下用以下命令打开：

```bash
start "" "output/gallery-xxx.html"
```

或者在 Git Bash 中：

```bash
cmd //c start "" "output/gallery-xxx.html"
```

如果命令执行受限，则**在对话中直接给出绝对路径**，让用户手动点开。

## 阶段 5：交互迭代

用户看完画板后可能提出：

- "再加几个网址"：追加到同一画板或新建
- "第 3 张卡片的图不对"：重抓该 URL
- "按主题分组"：重新生成画板，按 tag 分区块
- "导出图片到文件夹"：下载 hero_image 到 `output/images-{timestamp}/`
- "用浏览器重新抓一下这个"：对特定 URL 切换到 agent-browser 模式重试

按用户意图做定点修改，**不要每次都全部重跑**。

## 输出数据结构

每张卡片的标准 JSON 结构（这是画板消费的格式）：

```json
{
  "url": "https://example.com/article",
  "domain": "example.com",
  "favicon": "https://example.com/favicon.ico",
  "title": "...",
  "description": "...",
  "hero_image": "https://example.com/cover.jpg",
  "screenshot": "screenshots/example-com-20260424-103000.png",
  "images": ["url1", "url2"],
  "author": "...",
  "tags": ["design", "minimal"],
  "published_date": "2026-03-15",
  "project_type": "住宅",
  "location": "深圳",
  "architect": "某某建筑事务所",
  "materials": ["清水混凝土", "玻璃幕墙"],
  "status": "success",
  "fetch_mode": "agent-browser",
  "error": null
}
```

**建筑设计扩展字段**（如果能从页面中提取到）：
- `project_type`：项目类型（住宅/商业/公共/景观/室内/装置）
- `location`：项目所在地
- `architect`：建筑师/事务所名称
- `materials`：主要材料标签
- `year`：建成年份

这些字段是可选的——能提取到就填，提取不到不要编造。

失败的卡片：

```json
{
  "url": "https://example.com/broken",
  "domain": "example.com",
  "status": "failed",
  "fetch_mode": "webfetch",
  "error": "403 Forbidden / 该站点需要登录 / SPA 无静态内容"
}
```

## 关键原则

1. **不编造**：抓不到就说抓不到，永远不自己脑补页面内容
2. **不过度工程**：一次任务通常 5-30 个 URL，不需要并发池、不需要缓存
3. **不打扰用户**：除非 URL 列表明显有问题，否则不要中途追问，跑完直接出画板
4. **视觉优先**：画板要像设计师会喜欢的那种——大图、留白、好字体
5. **快速可用**：整个流程目标在 1-3 分钟内出结果（取决于 URL 数量和抓取模式）
6. **优雅降级**：agent-browser 不可用时用 WebFetch，WebFetch 也失败时如实报告

## 常见场景

### 场景 A：建筑设计师收集灵感

用户：`帮我看看这几个项目：archdaily.cn/xxx, gooood.cn/yyy, dezeen.com/zzz`

做法：识别为建筑设计站点 → 用 agent-browser 抓取 → 提取项目图片、建筑师、材料标签 → 大图瀑布流画板。

### 场景 B：SPA 站点抓取

用户：`抓一下 Behance 上这几个作品`

做法：检测 agent-browser 可用 → navigate → wait → snapshot + eval 提取 → screenshot → 画板中用截图作为封面。

### 场景 C：混合站点批量抓取

用户给了 15 个 URL，其中有静态站也有 SPA。

做法：统一用 agent-browser（如果可用），否则用 WebFetch 尽力抓取，失败的如实标注。

### 场景 D：产品调研

用户：`分析这 10 个竞品官网的首屏设计`

做法：抓取每个首页 → 提取 hero_image 和 h1 文案 → 画板展示 → 可在末尾附一个"共性观察"总结区块。

## 技术注意事项

### agent-browser 的能力

- **能渲染 SPA**：Behance、Dribbble、Pinterest（登录墙前的公开内容）等
- **能截图**：即使图片有防盗链，截图也能保留视觉信息
- **能执行 JS**：通过 `agent-browser eval` 提取懒加载后的图片 URL
- **Token 极省**：snapshot 返回精简 Ref 列表，比 Playwright MCP 省 80%+ 上下文
- **无需 MCP 配置**：直接 Bash 调用，装好即用
- **限制**：需要登录的内容仍然看不到

### agent-browser 常用命令速查

```bash
agent-browser navigate "<url>"              # 导航到页面
agent-browser snapshot                       # 获取精简页面快照（带 Ref）
agent-browser snapshot -i                    # 只返回可交互元素（用于检测弹窗）
agent-browser screenshot ./path.png          # 截图（路径直接跟后面，不用 -o）
agent-browser screenshot --full ./path.png   # 全页截图（--full 不是 --full-page）
agent-browser screenshot --annotate          # 带标号的截图（调试用）
agent-browser eval "<js>"                   # 执行 JavaScript
agent-browser wait <ms>                      # 等待毫秒
agent-browser click <ref>                   # 点击元素（如 @e1）
agent-browser close                          # 关闭当前页面
```

### WebFetch 的能力边界

- **能抓**：静态 HTML、服务端渲染的页面、大部分带 OG 标签的网站
- **可能抓不到**：
  - 纯客户端渲染的 SPA（内容靠 JS 加载）
  - 需要登录的页面
  - 有严格反爬的网站（Cloudflare challenge 等）
  - 图片防盗链（hero_image 能拿到 URL 但画板显示会 403）

### 相对 URL 处理

从 HTML 中提取到类似 `/images/cover.jpg` 的路径时，必须拼接域名变成 `https://example.com/images/cover.jpg`。

### favicon 获取

标准位置：`https://<domain>/favicon.ico`

如果页面 head 中有 `<link rel="icon">`，优先用那个。

### 截图存储（agent-browser 模式）

截图保存到 `output/screenshots/` 目录，文件名格式：`{domain}-{slug}.png`（slug 取自 URL 路径的关键词，简短易识别）。
命令示例：`agent-browser screenshot --full output/screenshots/gooood-uber-hq.png`
画板 HTML 中引用截图使用相对路径 `screenshots/xxx.png`。

### 输出目录

所有生成物都放在 Skill 目录下的 `output/` 里。这个目录在 `.gitignore` 中已排除，不会污染仓库。

## 故障排查

**agent-browser 不可用**：运行 `npm install -g agent-browser && agent-browser install` 安装。

**全部 URL 抓取失败**：检查网络连接。如果是 SPA 站点且没有 agent-browser，建议安装。

**画板打开是空白页（0 总计 0 成功 0 失败）**：大概率是 JSON 数据中有未转义的双引号导致 JS 报错。用浏览器 F12 控制台查看错误信息。检查 `<script type="application/json" id="gallery-data">` 中的 JSON 是否合法——特别注意抓取回来的 description 等文本字段可能包含引号。

**图片显示破损**：大概率是防盗链。agent-browser 模式下可以用截图替代。WebFetch 模式下如实告知用户。

**截图文件找不到**：确认 `output/screenshots/` 目录存在，且画板 HTML 和截图在同一个 `output/` 父目录下。
