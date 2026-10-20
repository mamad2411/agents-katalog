---
name: craft-slides
description: "基于 Slidev 端到端制作演示文稿:把主题/大纲生成规范的 slides.md、后台起预览、导出 PDF/PPTX/PNG。适用于做幻灯片、做 PPT、写 Slidev、生成演示文稿、craft slides、slidev export、导出 PDF/PPTX;不用于编辑非 Slidev 的 PowerPoint 二进制源文件、纯图片海报设计或视频制作。"
---

# Craft Slides

> 自包含的"脚手架 → 写规范 slides.md → 后台预览 → 导出 PDF/PPTX/PNG"端到端工具,基于 [Slidev](https://sli.dev)(用 Markdown 写演示)。
> skill 内自带 `scripts/slidev.sh`(生命周期封装)、`reference/syntax.md`(语法速查)、`templates/slides.md`(可套用骨架)。

后文 `$SKILL_DIR` 指本 skill 安装目录:`<项目>/.claude/skills/craft-slides`(或 `.codex/skills/craft-slides`)。

---

## 适用场景

- 把一个主题 / 大纲 / 讲稿做成一套可演讲、可导出的演示
- 在已有 Slidev `slides.md` 上增改页、调布局、加动画
- 预览(本地 dev server)与导出(PDF / PPTX / PNG)
- 开发者向演示:需要代码高亮、Live Coding、Mermaid 图、LaTeX 公式

## 不适用场景

- 编辑 `.pptx` / `.key` 二进制源文件 → 用 PowerPoint / Keynote
- 单张海报 / 社媒图等纯视觉设计 → 用设计工具
- 视频 / 动画渲染

---

## 前置条件

- Node ≥ 20.12(Slidev 要求)
- `npx slidev` 首次会自动拉 `@slidev/cli`(`new` 出来的项目 `npm install` 后即就绪)
- **主题包**:Slidev v52 起 default 主题也是独立 npm 包。`new` 会把 headmatter 的 `theme` 对应包写进 `package.json`;`dev`/`export` 前脚本也会按 headmatter 预装(后台 nohup 模式无法交互式安装,缺包会让 dev 启动即退出)
- **导出依赖**:`export` 子命令幂等装 `playwright-chromium`(npm 包,Slidev 导出由它驱动)+ `npx playwright install chromium`(浏览器二进制)
- **彩色 emoji 字体**:预览/导出用 Chromium 渲染,系统需装有 emoji 字体(如 `fonts-noto-color-emoji`),否则 slides 里的 emoji 全部显示成 □ 豆腐块。Debian/Ubuntu:`apt-get install -y fonts-noto-color-emoji`;装不了就别在内容里用 emoji
- dev 默认端口 **3030**(被占用时 Slidev 自增到 3030~4000,脚本以日志里的真实 URL 为准)

---

## 端到端工作流

### Step 0: 选主题(每次做演示必做)

开始做演示前,**先把下面 5 套精选主题列给用户,请其选择**(不要替用户预设、不要跳过)。用户已明确风格(深色 / 科技感 / 某主题名)则直接匹配并简要确认;用户说"你定"则用 `seriph`。

| 菜单标签 | `--theme` 短名 | 配色 | 气质 / 适用 |
|----------|---------------|------|-------------|
| Seriph | `seriph` | 深色 | 衬线·极简,正式分享、理念阐述 |
| Vercel / Geist | `geist` | 亮色 | 现代科技,产品 / 技术发布 |
| Nord | `nord` | 深色 | 冷色石板灰,长篇技术讲解 |
| Apple Basic | `apple-basic` | 亮色 | 仿 Keynote 极简,通用 |
| Dracula | `dracula` | 深色 | 紫色开发风,代码多 |

> 这 5 套各自带一份适配模板 `templates/slides.<短名>.md`(已配好 `theme` + `colorSchema` + 中文友好排版),`new --theme <短名>` 会自动套用对应模板;其它社区主题短名也支持,只是回退到通用 `slides.md` 模板。

### Step 1: 脚手架(新建项目)

```bash
bash "$SKILL_DIR/scripts/slidev.sh" new my-deck --theme <用户选的短名>
cd my-deck && npm install
```

生成最小项目:`package.json`(deps = `@slidev/cli` + 所选主题对应的主题包)+ `slides.md`(来自该主题的适配模板;无 `--theme` 或无匹配模板时用通用模板)。
已有 Slidev 项目则跳过本步,直接进项目目录。

### Step 2: 写内容(核心价值)

读 `reference/syntax.md` 作为语法依据,把大纲映射成规范 `slides.md`:

- 用 `---`(**前后空行**)分页;首个 frontmatter 是全局 headmatter(`theme` / `title` / `transition`)
- 每页可加 per-slide frontmatter 选布局:`cover` / `section` / `center` / `two-cols` / `image-right` / `end` 等
- 渐进展示用 `<v-clicks>` 包列表、`<v-click>` 包块;代码块行高亮 ```` ```ts {2,4-6} ````
- 图表用 ```` ```mermaid ````,公式用 `$$ … $$`
- 每页末尾的 `<!-- … -->` 是演讲者备注

> 内容原则:**一页一个主题**;标题动词化(讲"做了什么"而非名词堆);代码块控制在 ~12 行内,用行高亮聚焦关键行;正文给要点不给段落。

> ⚠️ 几个实测易踩的坑(详见 `reference/syntax.md` 与下方排错):
> - **慎开 `mdc: true`**:开了之后 ASCII 冒号紧跟单词(如 `分布:POST`)会被当成 MDC 内联组件,触发 `Failed to resolve component` 且该段文字丢失。不写 `{.class}` 这类 MDC 行内语法就别开 mdc;要写中文冒号用全角 `:`,或英文冒号后补空格。
> - **一页只有一屏**:Slidev 页面**不滚动**,超出部分直接被裁掉且无提示。一页塞不下就拆页 / 调小字号 / 用局部 `<style>` 压缩(如表格行高)。
> - **深层 Mermaid 竖向流程图(`flowchart TD`)极易超高**被裁;层级多时改用 HTML 卡片布局,或 `flowchart LR` / 调小 `{scale}`。

### Step 3: 预览 + 渲染自检

```bash
bash "$SKILL_DIR/scripts/slidev.sh" dev          # 默认 slides.md
# 返回形如:dev 就绪: http://localhost:3030/
```

把返回的 URL 贴给用户;改完 `slides.md` 会热更新,无需重启。

> 建议对**信息密度高 / 用了 Mermaid 或 emoji** 的页做一次截图自检(浏览器访问 `http://localhost:3030/<页码>` 截图回看),重点查:内容是否超出一屏被裁、emoji 是否豆腐块、Mermaid 是否溢出。
> 注意:`<v-clicks>` / `<v-click>` 的内容在**未点击的首屏是隐藏的**,截图看到"空白"多半是正常的渐进动画 —— PDF 导出会展开所有点击态,不要误判为渲染坏了。

### Step 4: 导出

```bash
bash "$SKILL_DIR/scripts/slidev.sh" export --format pdf     # 或 pptx / png
```

回报 Slidev 打印的 `✓ exported to <path>`。需要可托管网页版则 `slidev.sh build`(出 `dist/`)。

---

## AI 行为约定（看到触发就跑对应子命令,不要手敲 nohup / npx 底层）

| 用户说 | 跑 |
|--------|----|
| "做一套关于 X 的幻灯片 / 用 slidev 做 PPT" | **先列 5 套主题清单让用户选**(Step 0)→ `new --theme <短名>` 建项目 → Step 2 写 `slides.md` → 起 `dev` 贴 URL |
| "预览 / 看看效果 / 起服务" | `slidev.sh dev`,贴真实 URL |
| "在跑吗 / 停 / 重启" | `slidev.sh status` / `stop`(重启 = stop 后再 dev) |
| "导出 PDF / 导出 PPT / 导出图片" | `slidev.sh export --format pdf\|pptx\|png`,贴输出路径 |
| "构建 / 部署版 / 静态站" | `slidev.sh build` |
| "加一页讲 X / 把第 N 页改成两栏" | 直接编辑 `slides.md`(dev 在跑则自动热更) |

**AI 不要做**:

- 不手敲 `nohup npx slidev …` —— 绕过 `slidev.sh` 的 PID / 日志 / URL 管理
- 不改 `$SKILL_DIR` 内的脚本与模板当工作文件 —— 它们是 skill 资产;产出写到用户的项目目录
- 不在浏览器里替用户演讲操作 —— 那是用户的事
- 演讲者备注、动画切分等内容判断由 AI 在写 `slides.md` 时完成,不要让脚本去猜

---

## 数据位置约定

- 演示源(`slides.md`、`public/`、`components/`、`package.json`)= **用户项目目录**,跟着用户仓库走。
- 运行时状态(dev 的 PID / 日志 / 真实 URL)写**当前项目根** `.slidev-craft/`,与 skill 代码解耦;可用 `SLIDEV_CRAFT_HOME` 覆盖。
- 建议在项目仓库根 `.gitignore` 加:`.slidev-craft/` 和 Slidev 产物 `dist/`、`*-export.pdf`。

---

## 排错快查

| 症状 | 根因 | 修复 |
|------|------|------|
| `dev` 报"找不到入口文件" | cwd 不是 Slidev 项目 | `cd` 进项目目录,或先 `slidev.sh new` |
| `dev` 启动即退出 + 日志 `theme "…" was not found and cannot prompt for installation` | 主题包没装,后台模式无法交互式安装 | 新版脚本 `dev`/`export` 会自动预装;手动 `npm i @slidev/theme-<name>`(社区主题为 `slidev-theme-<name>`)后重试 |
| `dev` 启动后立即退出(其他) | 依赖没装 / `slides.md` 语法错 | `npm install`;看 `.slidev-craft/.dev.log` |
| 浏览器打开是 3031 而非 3030 | 3030 被占,Slidev 自增 | 正常;以脚本回报的真实 URL 为准 |
| `export` 报 `please install it via npm i -D playwright-chromium` | 只装了浏览器二进制,缺 `playwright-chromium` npm 包 | 新版 `export` 已幂等装;手动 `npm i -D playwright-chromium` |
| `export` 报缺少浏览器 | chromium 浏览器未安装 | `npx playwright install chromium` 后重试 |
| emoji 显示成 □ 豆腐块(预览和导出都是) | 系统缺彩色 emoji 字体 | `apt-get install -y fonts-noto-color-emoji`;或移除内容里的 emoji |
| 控制台 `Failed to resolve component: Xxx` 且对应文字丢失 | `mdc: true` 把 `:Xxx`(冒号紧跟单词)当成 MDC 内联组件 | 关掉 headmatter `mdc`;或冒号改全角 `:` / 英文冒号后加空格 |
| 内容下半部被裁、看不全 | 单页超过一屏,Slidev 页面不滚动 | 拆页 / 调小字号 / 局部 `<style>` 压缩行高;截图自检 |
| `export --format pptx` 页数比预期多 | pptx 默认 `--with-clicks` 展开点击 | 想要一页一张加 `--per-slide` 关掉,或不用 clicks |
| 分页没生效,全挤一页 | `---` 前后缺空行 | 分隔符独占一行且前后留空行 |
| 改了 `slides.md` 不刷新 | dev 没在跑 | `slidev.sh status` 确认;没跑就 `dev` |

---

## 反模式

### 内容层

- ❌ 把整篇文章 / 长段落塞进一页 —— 一页一个主题,正文给要点
- ❌ 一页塞到超出屏幕还不拆 —— Slidev 不滚动,超出即被裁且无提示;拆页或压缩
- ❌ 代码块几十行还不做行高亮 —— 用 `{行号}` 聚焦,必要时拆多页或 magic-move
- ❌ 标题用名词堆("架构""方案") —— 动词化讲清"做了什么 / 结论是什么"
- ❌ 无脑开 `mdc: true` —— 不用 MDC 行内语法就别开,否则 `:Word` 会被误当组件吞掉文字
- ❌ 用深层 `flowchart TD` 画多级决策树 —— 极易超高被裁,改 HTML 卡片 / `LR` / 调 `{scale}`
- ❌ 忘了演讲者备注 —— 关键页在末尾 `<!-- -->` 写讲稿提示

### 工具层

- ❌ 跳过选主题直接 `new` —— 每次做演示先列 5 套精选主题清单让用户选(Step 0;用户已指定风格除外)
- ❌ 手敲 `nohup npx slidev` 起服务 —— 走 `slidev.sh dev`,否则 PID / URL 失管
- ❌ 导出前不确认 chromium / playwright-chromium 就报错甩给用户 —— `export` 子命令已幂等装两者,仍失败再给手动指引
- ❌ 内容里大量用 emoji 却没确认系统有 emoji 字体 —— 先装 `fonts-noto-color-emoji`,否则全是豆腐块
- ❌ 信息密集 / 含图表的页不截图自检就交付 —— 容易漏掉超屏被裁、豆腐块、Mermaid 溢出
- ❌ 把 `.slidev-craft/` 或 `dist/` 提交进 git —— 运行时 / 产物,加进 `.gitignore`
- ❌ 凭记忆写 Slidev 命令参数 —— 以 `reference/syntax.md` 或 `npx slidev <cmd> --help` 为准

### skill 使用层

- ❌ 改 `$SKILL_DIR` 内的 `templates/slides.md` 当作给用户的演示 —— 模板是骨架来源,产出写用户项目
- ❌ 为"起一次 dev / 导一次 PDF"建工程任务 —— 这是工具调用,不是工程任务
