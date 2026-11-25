---
name: wechat-mp-publisher
description: 保存或更新微信公众号普通长文草稿，包含 Markdown 排版、本地图片、完整原标题 H1、作者、封面和原生公众号名片。用户说“更新公众号”“把某文章更新到公众号”“同步 Muse 推文”“存草稿”“修复封面名片”“拉取最新推文”或要求检查发布管线时使用。支持双源增量、关键词检索、最新定位和已有草稿原地更新；交付止于草稿箱。
---

# 微信公众号草稿编辑

本机权威代码库为 `C:\Users\Administrator\wechat-mp-publisher-skill`，唯一入口为 `bin/launch-publisher.mjs`。两处已安装同名技能链接到该代码库；不要复制另一套扫描器和状态库。更换设备时先读 [configuration.md](references/configuration.md) 核对本机路径和私有依赖。

## 先核查，再检查，后编辑

1. 读取 [operations.md](references/operations.md) 与实际 CLI 帮助。定时任务同时读 [cron-scheduling-prompt.md](references/cron-scheduling-prompt.md)。
2. **第一件事：先核查待同步推文的真实性与论文/DOI 有效性**（不要把假论文、假 DOI 或半成品写进草稿箱）：

```bash
# 方式一：独立核查待处理推文的论文题目、DOI (Crossref/doi.org)、arXiv 编号、原文链接与本地图片
bun run verify

# 方式二：带 --verify 同步执行只读预检与在线学术真实性核查
node "C:/Users/Administrator/wechat-mp-publisher-skill/bin/launch-publisher.mjs" --check --verify
```

- 正式写入前（非 `--repair` 模式）引擎也会默认并发执行在线核查；发现 **404 假 DOI、DOI/arXiv 解析标题与推文声明严重不符、死链、0 字节损坏图片或占位符残留** 时直接阻断该篇同步。
- **被拦截或告警后的官网二次核验与修复闭环**：被 `--verify` 拦截（如 `doi.org` 404）或告警（如站方 403 / 无 DOI）时，Agent 应进一步前往出版社/期刊/arXiv/Dryad 等**官方页面**直接核实：
  1. 若官网确认论文与 DOI 真实存在，仅因新发表尚未同步至 `doi.org`/Crossref 或遇到反爬 403，确认内容无误后可显式使用 `--id <articleId> --skip-verify` 放行入草稿箱；
  2. 若官网核查出推文存在可据实修正的明确笔误（如 DOI 拼写、期号或链接误写，且具备修正授权），据实修正后重新通过 `--verify` 再保存草稿；修正方式优先使用私有 `content-corrections.json` 映射（`{ articleId: [{ find, replaceWith, note }] }`，引擎在内存中逐字替换，**源文件保持只读**，每次应用均打印审计日志；坏 JSON fail-closed，路径可用 `WECHAT_CONTENT_CORRECTIONS_FILE` 注入）；
  3. 若官网查无此文、存在无法修正的伪造/张冠李戴或关键信息无法核实，坚决拦截，不保存到草稿箱。
- `--strict-verify` 连警告也阻断，`--skip-verify` 仅在人工或官网二次核实确认无误后显式配合 `--id` 使用。

3. 执行只读预检或快捷检索（不写历史/锁/基线，不触碰浏览器）：

```bash
# 全量只读检查（遇缺短题会附内容摘要并继续列出全部候选）
node "C:/Users/Administrator/wechat-mp-publisher-skill/bin/launch-publisher.mjs" --check

# 按关键词快速定位特定文章及当前草稿状态（支持 ID/文件名/标题/正文）
node "C:/Users/Administrator/wechat-mp-publisher-skill/bin/launch-publisher.mjs" --check --search "GEM-15"

# 快速定位最新 N 篇（按批次与修改时间倒序，默认 1 篇）
node "C:/Users/Administrator/wechat-mp-publisher-skill/bin/launch-publisher.mjs" --check --latest
```

`--check` 等价于 `--dry-run`。列出 `needs-title` 时先补短题，不把它当成正文损坏。没有可执行任务就报告退出，仅能说明 PC 当前索引。

3. 为新文（或源内容大幅改写需要换外题的稿件）按核心语义生成 15 字以内外题，使用内置命令原子合并进私有 `titles-override.json`（自动按 Unicode 字符精确计字，英文/数字/连字符计入；坏 JSON 拒写，不覆盖既有映射）：

```bash
bun run titles "<articleId>=<≤15字短标题>"
```

完整原题始终在正文首位 H1 保留。现有外题默认不改，确认文章替换或科学表述有误才显式指定。

4. 核对正文图片完整性与独立封面。无正文图合法，缺封面可准备独立 PNG/JPEG；本机私有 `generate-covers.py` 可用，但不随公开仓库分发。不能为选封面往正文塞图。
5. 执行明确范围，保存后独立重开验收。

## 命令选择

`articleId` 是 `source:batch:prefix`；微信数字 `appmsgid` 是远端草稿 ID，两者不同。

```bash
# 指定单篇处理（自动按指纹选择新建、原地更新或跳过；找不到 ID 报错退出码 1）
node bin/launch-publisher.mjs --id muse:20261113_1105:01 --title-override "GEM-15全球15米高程模型"

# 直接处理最新 1 篇
node bin/launch-publisher.mjs --latest 1 --title-override "<≤15字短标题>"

# 仅修补 H1、作者、外题、封面、名片，保留正文与原图
node bin/launch-publisher.mjs --repair --id <articleId>

# 明确从干净源文重建已有普通长文，仍使用原草稿 ID
node bin/launch-publisher.mjs --refresh-content --id <articleId>

# 批量任务
node bin/launch-publisher.mjs --titles "C:/Users/Administrator/.agents/skills/wechat-md-pipeline/data/titles-override.json"

# 轻量登录态探测（单独使用；仅访问官方后台首页检测当前登录态，不扫描/不改写草稿）
# 平台负责会话期限，不保证续期天数/月数；仅明确登录页才提示人工扫码续期。
# 输出 keepalive-status=healthy|needs-qr|unknown（退出码 0/3/4），unknown 不代表需要扫码。
node bin/launch-publisher.mjs --keepalive
```

只使用 `--help` 实际提供的参数；没有 `--covers` 参数。`--title-override` 仅限单篇模式（未配合 `--id`/`--latest 1`/`--search` 时被门禁拦截退出码 2）。正式写入前启动器自动执行 TypeScript 检查，失败即停止。

已有映射原地更新；旧基线无映射先核对真实正文、论文与图片，不清历史、删基线或另建替代。

## 编辑器与来源约束

- 普通长文正文必须是可见可编辑的 `.rich_media_content .ProseMirror`。标题/摘要可能也有 ProseMirror，图片轮播消息还会保留隐藏长文镜像；“从这里开始写正文”不代表真实空稿。遇到 `unsupported-message-type` 保留原稿并持久化标记，后续全量同步自动跳过不再浪费超时时间（显式 `--id` 仍可单独检测），不改 CSS 或隐藏类型。
- 复用宝玉 browser 路线专用 Profile 和主页，按 Profile 查端口，使用实际 WebSocket。若专用 Profile 尚未运行，统一引擎会以独立脱管进程安全拉起专用实例并保持常驻（不杀其它普通 Edge）。仅关闭本任务标签，不关闭用户标签、不反复开窗或弹二维码图片。公众号登录过期报告 `needs-attention`，与模型服务鉴权分开报告。
- Muse 来源 `F:\同步文件夹\公众号\每日推文` 与本地独立来源 `Z:\自媒体\公众号\每日推文` 保持分离且发布只读。缓存、状态、封面、模板、日志与截图留在私有目录。
- **GitHub 同步通道（可选）**：当远端经私有仓库（如 `ruiduobao/zimeiti-sync`）分发时，先执行 `node scripts/sync-from-github.mjs`（或 `bun run sync:github`）把 `*_本地版.md` 与 `images/**` 增量拉到本地镜像目录，再把 `WECHAT_MUSE_ROOT` 指向该镜像。脚本读取仓库根私有 `.env` 中的 `GITHUB_SYNC_TOKEN/REPO/DEST`，以 blob sha 做增量与删除同步；跳过体积巨大的 `_网页版.html` 与原始大 Markdown。镜像与历史源路径不同时，用 `WECHAT_FP_PATH_FROM`/`WECHAT_FP_PATH_TO` 归一化图片指纹路径，避免误判整批内容变更。
- 完整正文通过原生 HTML 复制粘贴交给微信编辑器，复制页仅包含本次内容，复制后关闭；这会覆盖系统剪贴板，不读取原剪贴板。粘贴后轮询等待整篇规范化文本真正变为新内容，防止读取旧正文快照误判丢占位符。
- 逐图通过原生选区（带抖动短重试）替换唯一文字占位符，核对全篇文本精确差值并上传。残留占位符或选区不稳时停止，不直接改 `textContent` 或 `innerHTML` 假装修复。
- **零缩进与零空行铁律**：渲染预处理自动剥离非代码块正文段落与列表行首多余缩进（空格/Tab/全角 `\u3000`/`&nbsp;`）、归零 `<p>`/`<ul>`/`<ol>`/`<li>` 的左右 `margin`/`padding`/`text-indent`（避免相对 H1 莫名右缩进），展开外层 `section.container` 并清除标签间空白节点；上传图片及插入名片后，通过原生 `Backspace`/`Delete` 按键清除正文内部、H1 后、图片前后及名片前的所有残余空段落。
- 发现多个 H1 或 H1 包含实质正文时，报告 `needs-content-refresh`，按源文原 ID 重建。原生名片必须是真正 `mp-common-profile`，身份正确并居尾；可视 div 不能替代。

现场规则见 [editor-reliability.md](references/editor-reliability.md)，按错误恢复见 [troubleshooting.md](references/troubleshooting.md)。

## 成功判定与报告

保存取得 ID 后先保全 `saved-unverified`，再从独立新标签读取同一 ID（条件轮询等待正文、图片、封面及名片真实解码就绪）：

- 首位唯一完整原标题 H1，作者和外题正确。
- 正文文字与保存前一致，没有占位符、定位标记或本地图片路径；独立重开校验确认**正文零空行且零异常段落缩进**（`emptyParagraphCount === 0` 且 `indentedParagraphCount === 0`）。
- 图片数量准确且全部加载；首先比较合法 qpic `/0`/`/640` 规范化 URL，若微信保存时对同一素材去重或重签名导致 URL 变化，则以 32×32 RGBA 内存像素交叉 MAE 验证各位置内容与顺序完全匹配。不放宽错图或乱序。
- 封面实际非空，末尾正确原生名片仍存在。

自动保存、按钮、toast、编辑态 DOM、回包均不能单独算完成。失败时先持久化自动保存候选 ID，再独立核对；身份核对失败保留候选并阻止重复新建。完整写入未验收保留 `pendingContentUpdate`，重跑继续原 ID 全量更新，不能降级为元数据修补后跳过。元数据修补只推进特性修复记录；完整正文和图片真实保存并复验通过后才能推进 `appliedFingerprint`。

汇报本次唯一新增成功、已有稿更新、原有已验证跳过、待核对、缺图、特殊类型与未验收。新文先失败后修补成功仍只算一篇新增；不要把有 ID 等同于完整源内容已应用，也不要沿用历史固定篇数。

只保存草稿，不发表、群发或通知关注者。源文、映射、名片模板、截图与凭据不进入公开仓库。

## 更新技能后的独立验证

先执行类型检查和回归，再按 [testing.md](references/testing.md) 核验测试矩阵；真实测试选已有映射的普通长文，分别覆盖多图与零图稿，原 ID 保存并独立重开。

```bash
bun run typecheck
bun run test
```

明确报告实测覆盖和未覆盖能力。子 agent 启动失败或工具阻塞不能算独立测试通过；离线通过不能代替网站实测。登录过期或平台变化时明确停止，不承诺永久免登或无条件成功。
