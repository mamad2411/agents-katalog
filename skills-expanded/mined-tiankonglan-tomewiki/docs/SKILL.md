# Agent Skill：第一轮建站

本文给**人**看：克隆模板之后，怎样用自带 skill 把「Example Game」换成自己的站。

给 Agent 执行的步骤在：

- [`.claude/skills/tomtwiki-quick-start/SKILL.md`](../.claude/skills/tomtwiki-quick-start/SKILL.md)（Claude Code）
- [`.cursor/skills/tomtwiki-quick-start/SKILL.md`](../.cursor/skills/tomtwiki-quick-start/SKILL.md)（Cursor）
- [`.agents/skills/tomtwiki-quick-start/SKILL.md`](../.agents/skills/tomtwiki-quick-start/SKILL.md)（Codex）

三份随仓库走，不用再装 marketplace skill。手工改配置见 [QUICKSTART.md](./QUICKSTART.md)。

## 它做什么

第一轮只做**站身份**，不做内容生产：

| 会改 | 不会改 |
|------|--------|
| 站名、域名、游戏名、免责声明 | 路由、组件、`src/app/**` |
| 首页文案（积木结构不变） | 登录、数据库、支付 |
| SEO title / description / keywords | `content/guides/`、`content/entities/` 里的种子正文 |
| 主题预置 + 品牌色 | 分类文件夹 slug |
| logo / favicon / OG 图 | 编造 Steam ID、官宣口吻 |

跑完你得到的是「看起来像这个游戏的空壳」，攻略和资料库还要自己填。

## 环境

- Node.js 24、pnpm 10.34.5（与 CI 一致）
- **Cursor**、**Claude Code** 或 **Codex** 打开的是克隆后的仓库根目录（能看见 `.claude/skills/` / `.agents/skills/`）

```bash
git clone https://github.com/tiankonglan/tomtwiki.git my-game-wiki
cd my-game-wiki
pnpm install
```

## 怎么唤起

在对话里用自然语言即可。skill 的 `description` 里带了「建站 / 快速接入 / 改成自己的站 / Example Game」，Agent 应能自己选中。

没被选中时：

- Cursor：`/` 或 `@` 技能列表里找 `tomtwiki-quick-start`
- Claude Code：`/tomtwiki-quick-start`
- Codex：`$tomtwiki-quick-start`

### 提示词模板

最少只要游戏名和域名：

```text
把这个模板改成《Hades II》的非官方攻略站。
域名 hades2.wiki。
```

信息越全，第一轮越少 `TODO:`：

```text
把这个模板改成《Hades II》的非官方粉丝攻略站。

- 域名：hades2.wiki
- 简称：Hades 2
- 一句话：构筑、Boss 机制、热更新对照表
- 品牌色：#C45C26
- 主题：tactical
- 当前版本：1.0
- 状态：Early Access（可留空）
- Steam App ID：1145350（没有就不要编）
- 发行商：Supergiant Games（免责声明用）
- 不要加登录或数据库
```

主题只能是：`tactical`（默认）/ `pixel` / `neon` / `aurora` / `sakura`。含义见 [THEMES.md](./THEMES.md)。

## 你需要准备什么

| 字段 | 必须？ | 说明 |
|------|--------|------|
| 游戏全名 | 是 | |
| 域名 | 是 | 只写 hostname，不要 `https://` |
| 简称、tagline、版本 | 否 | 有默认 |
| 品牌色、主题 | 否 | 未给则按品类猜，可事后改 |
| Steam ID | 否 | **禁止猜测** |
| logo / 方形 emblem | 否 | 没有则跑仓库自带 `scripts/gen-brand-assets.mjs` |
| Key art、实机截图、预告片 URL | 否 | Key art 用 `cover-split`，干净实机截图用 `gameplay-panel`，预告片用 `video-center` |
| 分析 ID | 否 | 没给就留空 |

## 第一轮会动哪些文件

完整白名单在 skill 的 [`references/07-checklist.md`](../.claude/skills/tomtwiki-quick-start/references/07-checklist.md)。概要：

- `.env`、`wrangler.jsonc`（Worker 名）
- `src/generated/game-config.ts`、`homepage.ts`、`site-locales.ts` 等生成配置
- `src/config/locale/messages/en/common.json`
- `src/components/site/brand.css`、主题入口 CSS/字体
- `public/logo.png`、`favicon.png`、`og-image.png`

**不要**让 Agent 为了「好看一点」去改 `src/app/**` 或 `template-contract.json`。那是扩大范围，第一轮不做。

## 怎样算成功

Agent 结束时应做到：

1. `pnpm validate:site` 通过
2. `pnpm build` 通过
3. `pnpm dev` 打开后，顶栏/标题不再是 Example Game；logo 不是模板默认图

若新 logo 不出现，删掉 `.next` 再 `pnpm dev`（Next 会缓存 `public/` 里的旧图）。

仍是 Example Game、或首页链到不存在的路径，把 `pnpm validate:site` 的报错贴回对话即可。

## 第一轮之后

- 攻略：`content/guides/<分类>/*.mdx`（分类须已在 `src/config/guides.ts` 登记）
- 资料：`content/entities/<种类>/*.json`，见 [ENTITIES.md](./ENTITIES.md)
- 多语言：见 [QUICKSTART.md](./QUICKSTART.md) 第 7 节，并删掉 `// scaffold-default:en-only`
- 部署：`pnpm cf:deploy` 或 Vercel；自定义域名在 Cloudflare 绑定
- 上线前扫一遍 [PITFALLS.md](./PITFALLS.md)

## 维护这三份 skill

改流程时 **`.claude/skills/`、`.cursor/skills/` 与 `.agents/skills/` 必须一起改**，保持字节级相同，否则 Cursor、Claude Code 和 Codex 行为会漂。
