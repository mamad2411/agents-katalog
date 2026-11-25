---
name: user-manual-sync
description: Use when adding, changing, or removing a user-facing a2wave feature (new page/route, new capability, changed user flow, new trigger/integration) — keeps the in-app User Manual (Wiki) at /wiki in sync. Keywords 使用手册, wiki, 用户手册, 帮助文档.
---

# User Manual (Wiki) Sync

## Overview

a2wave 的「使用手册」是 Web 内置的 `/wiki` 页面,面向**终端用户**讲解平台功能怎么用。
内容是一组 Markdown,由 Vite 在构建时打包进前端 —— **没有后端 API,不读 `docs/`,不进运行镜像之外的任何源**。

| 关注点 | 位置 |
|--------|------|
| 章节正文(中文) | `apps/web/src/content/manual/zh/NN-slug.md` |
| 章节正文(英文,可选) | `apps/web/src/content/manual/en/NN-slug.md` |
| 加载/排序逻辑 | `apps/web/src/lib/manual.ts` |
| 页面组件(左目录+右正文) | `apps/web/src/pages/wiki.tsx` |
| 路由 `/wiki` `/wiki/:slug` | `apps/web/src/app.tsx` |
| 侧栏入口 + 文案 | `apps/web/src/components/layout.tsx`、`apps/web/src/locales/{zh,en}.json` |
| E2E | `e2e/tests/pages/wiki.spec.ts`、`e2e/utils/test-constants.ts` |

> 区分:这里说的是「面向用户的产品使用手册」,不是开发者文档(`docs/`)、也不是平台 Skill 功能。

**当前结构(v2):** 共 15 章,落地页(`/wiki` 首屏)是 `01-overview.md`(slug `overview`,标题「概览与导航」),含「按场景 / 按角色速查」两张表;其后是 `getting-started`、`concepts`,各功能章,末尾 `faq`、`glossary`。读者定位为「终端用户 + 集成开发者」,触发方式等章含真实调用示例。

## When to Use

新功能开发完成 / 改动触及**用户可感知行为**时,必须走一遍本 skill 判断手册是否要更新:

- 新增页面、路由、导航项
- 新增或改变某项能力的用法(Agent / Provider / MCP / Skill / 代码源 / 知识库 / 运行记录)
- 新增或调整触发方式、外部集成、鉴权方式
- 改变面向用户的操作流程、术语、限制(铁律)

仅内部重构、不影响用户用法时,可不更新,但要在 PR/commit 里说明「无用户可见变更,手册无需更新」。

## Core Workflow

```
判断影响范围 → 选择动作(改/增章节) → 遵守命名与交叉链接约定 → 校验 → 同步 E2E
```

### 1. 判断该改哪一章

对照现有章节(`apps/web/src/content/manual/zh/` 下 `01..NN`)。功能属于已有主题就**改对应文件**;是全新主题就**新增一章**。

### 2A. 改现有章节(最常见)

直接编辑对应 `zh/NN-slug.md`,用面向用户的口吻补充「这是什么 / 怎么用 / 注意什么」。**不要**写实现细节、文件路径、内部 API。

### 2B. 新增章节

1. 在 `apps/web/src/content/manual/zh/` 新建 `NN-slug.md`:
   - `NN`(数字前缀)决定目录排序;要插在中间用如 `025-xxx.md`(`Number('025')=25`)。
   - `slug` 即路由,访问地址为 `/wiki/<slug>`,用小写连字符。
   - **第一行必须是一级标题** `# 标题`,loader 取它作为目录项名称。
2. 不需要改 `manual.ts` / `app.tsx` / `layout.tsx` / i18n —— `import.meta.glob` 在构建时自动发现新文件。
3. **同步落地页**:在 `01-overview.md` 的「按场景速查 / 按角色速查」表里补一行,链接到新章节(`/wiki/<slug>`),否则新功能在总览页不可发现。

### 3. 约定

- **交叉链接**用站内路径:`[成员管理](/wiki/members)`,slug 与目标文件名后半段一致。`MarkdownContent` 会把 `/` 开头(但 `/api/` 除外)的链接渲染成 React Router `<Link>` **原地跳转**;`/api/*`(服务端路由,如 `/api/docs`)与外部 `http(s)://` 走普通 `<a>` 新开标签——所以站内一律写 `/wiki/<slug>`,别写成完整 URL;指向 `/api/docs` 等服务端地址直接写该路径即可。
- **口吻**:终端用户视角,简洁、可操作;善用表格与有序步骤。
- **硬约束相关**(铁律,以及「飞书一 App 一单连接」这类实现约束)若涉及,务必准确转述,可参考 `AGENTS.md` 的产品铁律与 `docs/PRODUCT.md`,但**重写为用户口吻**,不要直接粘贴开发文档。
- **提示卡片(callout)**:需要强调时用 GFM alert 语法,`MarkdownContent` 会渲染成彩色卡片:`> [!NOTE]`(说明/蓝)、`> [!TIP]`(建议/绿)、`> [!IMPORTANT]`(重要/主色)、`> [!WARNING]`(注意/琥珀)、`> [!CAUTION]`(警告/红);标记单独一行,内容写在其后的 `>` 行。普通引用仍用不带标记的 `>`。
- **标题锚点**:H2/H3 自动生成 id 与悬停锚点;章节有 ≥3 个 H2 时,正文顶部会自动出现「本页大纲」(直接读渲染后 DOM 的 h2[id],无需另维护)。无需手动维护,正常写 `##` / `###` 即可。
- **作用域**:上述「站内链接原地跳转 / callout / 标题锚点」仅在 wiki 生效——`wiki.tsx` 给 `MarkdownContent` 传了 `wiki` prop。其它复用点(changelog、run/test 抽屉的 agent 输出)默认关闭这些增强,保持普通 `<a target=_blank>`、无 callout/锚点。在别处复用 `MarkdownContent` 时按需自行决定是否传 `wiki`。
- **英文**:有精力就在 `en/` 放同名 `NN-slug.md`(slug 与 zh 一致,便于切语言保持同章节);没有则留空,运行时自动回退中文。

### 4. 仅在这些情况才改代码/文案

| 情况 | 改动点 |
|------|--------|
| 改侧栏入口名/图标 | `layout.tsx` 的 `nav.wiki` 项 + `locales/{zh,en}.json` 的 `nav.wiki` |
| 改页面标题/副标题/目录抬头 | `locales/{zh,en}.json` 的 `wiki.*`(zh/en 键必须对齐) |
| 改排序规则、frontmatter、多语言策略 | `apps/web/src/lib/manual.ts` |

### 5. 校验(提交前)

- `pnpm --filter @a2wave/web typecheck`、`pnpm lint`(改 `.md` 一般无类型影响,但保持习惯)。
- 本地 `pnpm run dev` 看 `/wiki`:目录出现新/改章节、切换正常、深链 `/wiki/<slug>` 可直达。
- 可选 `pnpm --filter @a2wave/web build` 确认内容被打包(`wiki-*.js` 体积应随内容变化)。

### 6. 同步 E2E(硬性约定)

- `e2e/tests/pages/wiki.spec.ts` 断言了:落地页首屏一级标题是**「概览与导航」**(`01-overview.md`)、TOC 含「快速开始」、深链 `/wiki/triggers`→「触发方式」、`/wiki/agents`→「Agent 管理」,以及正文站内链接**原地跳转、不开新标签**。若你改了这些被断言的标题/落地页/链接行为,或删了对应章节,**必须同步更新 spec**;只是新增其它章节则不受影响。
- 若新增/改名了顶级导航,更新 `e2e/utils/test-constants.ts` 的 `NAV_ITEMS`/`ROUTES`。

## Checklist

- [ ] 判断本次改动是否产生用户可见变化
- [ ] 改/增对应 `zh/NN-slug.md`,首行 `# 标题`,口吻面向用户
- [ ] 新增章节已在 `01-overview.md` 速查表补链接
- [ ] 交叉链接用 `/wiki/<slug>`(原地跳转)、术语、铁律转述准确
- [ ] (可选)补 `en/` 同名文件
- [ ] 仅必要时改 nav/i18n/loader,且 zh/en 文案键对齐
- [ ] typecheck / lint / `/wiki` 自测通过
- [ ] 受影响的 `wiki.spec.ts` / `test-constants.ts` 已同步
