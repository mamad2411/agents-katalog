---
name: vitepress-course-tools-setup
description: |
  配置与同步 VitePress 课程文档站的 @smart-cs/vitepress-course-tools：侧栏菜单、PDF 封面目录 tocManifest、商品详情 productDetail、npm 导出脚本。
  当用户提到 vitepress-course-tools.config.ts、同步 docs/zh 菜单、tocManifest、productDetail、商品详情 PDF、pdf:export:product、课程 PDF 导出、README 截图配置时使用本 skill，即使用户只说「更新文档站配置」或「对齐侧栏和 PDF 配置」也应触发。
---

# VitePress 课程工具配置

面向使用 `@smart-cs/vitepress-course-tools` 的 VitePress 文档站。目标：磁盘上的 `docs/zh/**/*.md` 与导航、PDF 封面目录、商品详情页保持一致，并补齐 npm 导出命令。

## 涉及文件

| 文件 | 作用 |
|------|------|
| `docs/zh/**/*.md` | 文档真源（以磁盘为准） |
| `docs/.vitepress/config.mts` | 网站侧栏 / 导航 `link` |
| `vitepress-course-tools.config.ts` | PDF、封面、商品详情、截图 |
| `scripts/export-site-utils.ts` | 旧版导出脚本中的 `ZH_*_DOCS` 列表（若存在） |
| `shared/course-theme-class.ts` | 主题 class，勿在 VitePress 客户端 import 完整 config |
| `package.json` | `pdf:*` / `screenshots:*` / `code:pack` 脚本 |

`basePath`（config）须与 `docs/.vitepress/config.mts` 的 `base` 完全一致。

## 工作流

```
进度：
- [ ] 1. 扫描 docs/zh 实际 .md 文件
- [ ] 2. 同步 docs/.vitepress/config.mts 侧栏
- [ ] 3. 同步 vitepress-course-tools.config.ts → cover.tocManifest
- [ ] 4. 同步 scripts/export-site-utils.ts（若项目仍使用该文件）
- [ ] 5. 配置或更新 productDetail
- [ ] 6. 确认 package.json 导出脚本与依赖
- [ ] 7. 校验（可选运行导出）
```

### 1. 扫描 docs/zh

```bash
find docs/zh -name '*.md' | sort
```

区分：
- 根目录技术文档：`index.md`、`00-*.md` … `10-*.md`
- 面试资料：`interview/*.md`

侧栏显示名通常取自文件名（去掉序号前缀与 `.md`），或与现有 `text` 字段风格保持一致。

### 2. 同步侧栏（config.mts）

在 `zhGuideItems` / `zhInterviewItems` 中：

- **link 格式**：`/zh/文件名.md` 或 `/zh/`（index）
- **text**：与文档标题或文件名语义一致
- **顺序**：`index` → 编号技术文档 → `interview/` 子目录按文件名排序

常见错误：`link` 指向已改名/删除的文件（如 `05-八股文-医疗AI专题.md` 实际为 `05-八股文-AI专题.md`）。

英文侧栏 `enGuideItems` 仅在 `docs/en/` 存在对应文件时维护。

### 3. 同步 cover.tocManifest

在 `vitepress-course-tools.config.ts` 的 `cover.tocManifest` 中，条目顺序与侧栏一致：

```ts
{ title: '侧栏 text', routePath: '/zh/路由' }
```

**routePath 规则**（`cleanUrls: true`）：
- `index.md` → `/zh/`
- `00-项目概览.md` → `/zh/00-项目概览`（无 `.md` 后缀）
- `interview/01-简历写法模板.md` → `/zh/interview/01-简历写法模板`

`title` 与侧栏 `text` 对齐；`routePath` 与包内 `sourceFileToRoutePath` 一致。

### 4. 同步 export-site-utils（若存在）

`scripts/export-site-utils.ts` 中的 `ZH_GUIDE_DOCS`、`ZH_INTERVIEW_DOCS` 须与侧栏顺序一致，但值为**相对 `docs/zh/` 的路径**（含 `.md`）：

```ts
'index.md',
'00-项目概览.md',
// ...
'interview/01-简历写法模板.md',
```

`readmeScreenshotTargets` 的 `routePath` 同样用 cleanUrls 格式。

### 5. 配置 productDetail

在 `vitepress-course-tools.config.ts` 增加 `productDetail`（类型 `ProductDetailConfig`）。

**与 cover 的关系**：
- `title` / `subtitle` 可与 `cover.mainTitle` / `subTitle` 对齐
- 未写 `intro` 时导出回退到 `cover.descCn`
- 未写 `tocSections` 时回退到 `pdf.tocGroups` 或自动生成

**intro 写法**（包内渲染规则）：

| 语法 | 效果 |
|------|------|
| 空行 | 分段 |
| 行首 `🔹` / `##` / `【标题】` | 小节标题 |
| 行首 `•` `-` `*` | 列表 |
| 普通行 | 段落 |

**tocSections**：按侧栏分组（如「技术文档」「面试资料」），每项 `{ title, note? }`，标题与 tocManifest 一致，note 为一句卖点。

**gallery**：指向 `screenshotsDir` 下 PNG；路径相对项目根。与 `screenshots` 配置或 `readmeScreenshotTargets` 对齐。图片不存在时包内会回退占位图——正式发版前先跑截图。

**exportVariants**：`['classic', 'minimal', 'card']` 或按需子集。

完整字段说明见 [references/product-detail-fields.md](references/product-detail-fields.md)。

### 6. package.json 脚本

依赖（Git 安装时无 dist，用 `tsx` 直跑 `src/cli`）：

```json
"@smart-cs/vitepress-course-tools": "github:cklwblove/vitepress-course-tools"
```

推荐脚本：

```json
"pdf:export": "tsx node_modules/@smart-cs/vitepress-course-tools/src/cli/pdf-export.ts --phase=all",
"pdf:export:sections": "... --phase=sections",
"pdf:export:cover-toc": "... --phase=cover-toc",
"pdf:export:merge": "... --phase=merge",
"pdf:export:cover": "tsx node_modules/@smart-cs/vitepress-course-tools/src/cli/pdf-cover.ts",
"pdf:export:product": "tsx node_modules/@smart-cs/vitepress-course-tools/src/cli/pdf-product-detail.ts",
"pdf:build": "npm run docs:build && npm run pdf:export",
"screenshots:readme": "tsx scripts/capture-readme-screenshots.ts",
"code:pack": "tsx node_modules/@smart-cs/vitepress-course-tools/src/cli/pack-code.ts"
```

`vitepress-course-tools.config.ts` 顶部类型导入：

- 有 dist：`import type { CourseToolsConfig } from '@smart-cs/vitepress-course-tools'`
- 仅 Git 源码：改引 `./node_modules/@smart-cs/vitepress-course-tools/src/types.ts`

### 7. 校验

```bash
# 侧栏与磁盘一致（人工或 diff）
find docs/zh -name '*.md' | sort

# 整本课程 PDF（需先 build）
npm run docs:build
npm run pdf:export

# 商品详情 PDF（不依赖 build，但 gallery 图需存在）
npm run pdf:export:product
npm run pdf:export:product -- --variant classic

# README 截图 → productDetail.gallery
npm run docs:build && npm run screenshots:readme
```

成品路径：
- 课程 PDF：`artifacts/pdfs/<pdf.name>-guide-zh.pdf`
- 商品详情：`artifacts/pdfs/<pdf.name>-product-*.pdf`

## 新增 / 删除文档时的检查单

1. 在 `docs/zh/` 增删 `.md`
2. 更新 `config.mts` 对应 `zhGuideItems` 或 `zhInterviewItems`
3. 更新 `cover.tocManifest` 同序条目
4. 更新 `productDetail.tocSections`（若有分组目录）
5. 更新 `export-site-utils.ts` 的 `ZH_*_DOCS`（若存在）
6. 新章节若需预览图：加入 `screenshots` / `gallery` / `readmeScreenshotTargets`

## 注意事项

- 勿在 `docs/.vitepress/theme/index.js` 中 import 完整 `vitepress-course-tools.config.ts`（会拖入 Node 依赖导致白屏）；主题 class 用 `shared/course-theme-class.ts`
- `docsBasePath` 在 `export-site-utils.ts` 可能与 `config.mts` 的 `base` 不一致，以 **config.mts 为准** 并统一
- 虚拟商品文案注意平台合规：避免医疗执业、极限词、站外引流；详见项目内 `品文案.md`（若存在）

## 参考

- 包内 README：`node_modules/@smart-cs/vitepress-course-tools/README.md`
- 字段速查：[references/product-detail-fields.md](references/product-detail-fields.md)
- 同步关系图：[references/config-sync-map.md](references/config-sync-map.md)
