---
name: quark-search-save
description: >-
  对话里找网盘资源并一句话转存到夸克网盘。先调 PanSou 聚合搜索找夸克分享链接，转存前用官方 share-detail 剔除失效链接，再调夸克官方 Skill 的 saveas 全自动转存（可只存选中文件、可追更新增内容），全程不抓 cookie、不手动点、不部署新应用。触发词：找资源、搜课件、找一下 XX、帮我存到夸克、帮我把 XX 存到夸克网盘、把 XX 保存到夸克、只存第几章、这个分享有更新吗、把更新存下来、quark search / save。Find cloud-drive resources in chat and save them to Quark Drive: search PanSou for Quark share links, then transfer them with the official Quark Drive skill's saveas. Use when the user asks to find a resource and save it to Quark Drive.
license: MIT
metadata:
  version: "1.3.6"
  repository: https://github.com/TTNAN/quark-skill
---

# Quark Search & Save（夸克搜索转存）

用户在对话里说一句“帮我把 XX 存到夸克网盘”，你去搜、让他挑版本、用夸克官方 Skill 直接转存进他的夸克网盘，存完回查确认。

下文 `<本 Skill 目录>` 指这个 SKILL.md 所在的目录；脚本都在它的 `scripts/` 下，不要去仓库根目录或当前工作目录找。

## 前置条件（缺一不可，缺了先停下来告诉用户）

1. **夸克官方 Skill（`quarkclouddrive`）已安装并已登录授权。** 没装的话由你帮用户装，不要让他自己去折腾。
   先定位它的 CLI，不要凭经验猜路径：

   ```bash
   python3 <本 Skill 目录>/scripts/find_quark_cli.py --json
   ```

   - `ok: true`：记下 `cli`（即 `<quark-cli>`）和 `skill_dir`（即 `<quark-skill-dir>`），本次对话复用。脚本已经跑过 `node <cli> --help` 验证能用；有多份时取的是版本最高的。
   - `ok: false` 但有 `broken`：装过，但跑不起来（常见是没装 node 或文件不完整）。告诉用户原因，问他要不要重装；同意后对那个目录运行 `python3 <本 Skill 目录>/scripts/install_quark_skill.py --json --dir <broken[0].skill_dir> --force`，官方安装脚本会补装 Node.js 并自检。
   - `ok: false`：告诉用户“转存要用夸克官方的网盘 Skill，你还没装”，**问他要不要现在从夸克官方地址帮他装**。他同意后运行：

     ```bash
     python3 <本 Skill 目录>/scripts/install_quark_skill.py --json
     ```

     脚本会向夸克官方接口查最新版下载地址（只接受 `quark.cn` 的地址），下载官方 zip，解压到本 Skill 的同级目录 `quarkclouddrive`，再运行官方的 `scripts/install.sh`（检查并安装 Node.js 16+、安装 CLI、自检）。本仓库不附带任何夸克的文件。
     - `ok: true`：用返回的 `cli`、`skill_dir` 作为 `<quark-cli>`、`<quark-skill-dir>`。然后**先读一遍 `<quark-skill-dir>/SKILL.md` 和 `<quark-skill-dir>/references/auth.md`**（官方 Skill 是刚装的，你还没加载它的规则），按官方规则输出首次安装的欢迎语，并用 `node <quark-cli> login` 引导用户登录授权（浏览器打不开时按官方流程让用户把授权码贴进对话，再 `login --token`）。登录成功后接着做用户原来的请求，不要让他再说一遍。
     - `ok: false`：把 `error` 原文告诉用户，附上 `official_page` 让他按官方页面手动安装，然后停下。
     - 用户想装到别的位置（例如 Codex 的 `~/.codex/skills`）时，加 `--dir <目录>/quarkclouddrive`。官方要求装在智能体的**全局** skills 目录，不要装进项目目录。
     - 用户不同意安装：停下，告诉他转存这一步需要官方 Skill；也可以设置环境变量 `QUARK_SKILL_DIR` 指向已有的安装目录。
2. **搜索用 PanSou。** 默认用公共实例 `https://so.252035.xyz`，不用 key；报“需要认证令牌”时告诉用户该实例要 token，用户自部署时才用 `PANSOU_URL`（可用逗号写多个）/ `PANSOU_TOKEN`。

## 调官方 CLI 的公共规则（每条命令都适用）

- `--session-input` 和 `--session-id` 是官方 CLI 所有子命令的公共参数，**每次调用都必传**。
  `--session-input` 逐字复制用户原始提问，禁止改写或摘要；
  `--session-id` 在本次对话第一次调 CLI 时生成（如 `1784035443-a1b2c3`，即 `<unix 秒>-<6 位随机字母数字>`），同一对话后续复用。
- 每次用户输入后，第一次调官方 CLI 前先跑一次官方自检：`bash <quark-skill-dir>/scripts/install.sh`。
  返回 `success: true` 且 `updated: true` 时，本次业务命令额外带 `--skill-updated`，否则不带。
  （`install.sh` 是官方 Skill 的脚本，本仓库没有这个文件。）
- 官方 CLI 每次返回的非空 `notice.text`，在业务结果之后另起一段原样展示，不得省略、概括或改写。
- 下文命令里的 `<公共参数>` 指 `--session-input "<用户原话>" --session-id "<会话 ID>"`（以及需要时的 `--skill-updated`）。

## 工作流（缺一步都不算完成）

### 第 1 步：搜索

**先告诉用户要等一会儿。** 通常半分钟以内；冷门词要重试、换实例时，搜索最坏约两分钟，预检最坏约一分半，合计最坏三四分钟。开始前说一句“正在搜，一般半分钟左右，冷门的可能要三四分钟”；两个脚本都会把进度打到 stderr（正在搜索哪个实例、第几次重试、第几条链接验完），等得久时把最新一条进度转告用户，别让他以为卡住了。

```bash
python3 <本 Skill 目录>/scripts/pansou_search.py --kw "<关键词>" --limit 10 --json > <临时目录>/qs-search.json
```

**关键词怎么取：** 从用户原话里取出资源的核心名称本身——片名、书名、课程名。

- 去掉书名号《》、引号，去掉“帮我找”“存到夸克”这类指令词。
- 去掉版本号、年份、出版社、清晰度等修饰词（例如“第五版”“2024”“4K”），这些放到第 3 步挑选时再用。
- 用户点名只要某一部分（例如“第 3 章”“只要 PDF”），这部分也不放进关键词，留到第 4 步。
- 不要加用户没说过的词，不要换同义词、不要翻译。

**结果怎么读：**

- 脚本已经只保留夸克链接、按 URL 去重、按日期从新到旧排好序。
- 脚本在结果为空时会**自动用同一关键词退避重试；配了多个实例时还会依次换实例**。你不需要、也不允许再自己换词重搜。
- `ok: false`：把 `error` 原文告诉用户，停下。
- `quark_links` 为空：直接告诉用户搜不到。**不许换词重搜、不许编链接。** 可以建议他换个说法，或自部署 PanSou 实例。

### 第 2 步：预检链接（剔除失效的）

```bash
python3 <本 Skill 目录>/scripts/check_links.py --cli <quark-cli> --session-input "<用户原话>" --session-id "<会话 ID>" --input <临时目录>/qs-search.json --keep 5
```

脚本对每条候选调官方 `share-detail`（客态模式，不需要登录），只剔除**明确失效**的分享（已知失效码 41004 / 41006 / 41007，或分享里一个文件都没有），保留最多 5 条。网络抖动、限流、提取码问题等拿不准的情况一律标 `unknown`，留给用户决定。需要 `--skill-updated` 时也加上。

- `shown`：要给用户看的候选，顺序不变。每条的 `check.status` 为 `valid`（附 `share_title`、`file_num` 首层条目数、`preview` 前几个文件名；有的话还附 `total_files` 分享里的文件总数和 `total_size` 总大小）或 `unknown`（没验出来，`check.msg` 是原因，照样可选）。
- `invalid`：被剔除的条目，只需在表格下方用一句话说明“另有 N 条已失效，已略过”。
- `check_skipped: true`：官方 CLI 当前不可用（`reason` 原文），跳过预检，直接用 `shown`，流程照旧。
- `notices` 非空：按公共规则原样展示。
- `shown` 为空（全部失效）：告诉用户“搜到的这几条都失效了”，可以建议他换个说法后再让你搜。

### 第 3 步：挑一个，让用户确认

把 `shown` 做成表格给用户看：序号、标题、日期、文件数（优先 `total_files`，没有再用 `file_num`）、大小（`total_size`，没有就省略这一栏）、内容预览（`preview` 前 2–3 个文件名；分享只有一个顶层文件夹时，预览就是那个文件夹名）、链接。`unknown` 的条目文件数一栏写“未验证”。

- 没有用户明确选中的那一条就不要转存。用户说“就第一个”“要带课件的那个”时按他说的来。
- 用户提过的版本、年份、清晰度等修饰条件，用来在结果里帮他标出最匹配的一条，推荐后等他点头。

### 第 4 步（可选）：只存需要的文件

用户只要分享里的一部分（“只要第 3 章”“只要 PDF”“不要视频”），或者分享很大、他想先看看里面有什么时：

- 有明确关键词：`node <quark-cli> share-search --url "<分享链接>" --keyword "<关键词>" <公共参数>`
- 想浏览：`node <quark-cli> share-detail --url "<分享链接>" <公共参数>`（进子目录加 `--pdir-fid <文件夹 fid>`，翻页加 `--page`）。带提取码的链接加 `--passcode`。

把返回的 `files` 列成表格（文件名、大小、类型），让用户选，记下所选文件的 `fid`。`file_type` 是字符串，`"0"` 表示文件夹（显示成“文件夹”，大小写“—”）。`share-search` 没搜到时返回 `code: 0` 且 `files` 为空，不是报错：告诉用户分享里没有匹配的文件，改用 `share-detail` 浏览让他挑。用户没有提出这类要求时，跳过这一步，整个分享一起存。

### 第 5 步：转存（全自动）

用户确认后，用官方 Skill 的 `saveas`：

```bash
# 整个分享
node <quark-cli> saveas --url "<分享链接>" <公共参数>
# 只存第 4 步选中的文件
node <quark-cli> saveas --url "<分享链接>" --fid-list "<fid1>,<fid2>" <公共参数>
```

- 提取码：`needs_passcode: true` 时加 `--passcode "<password>"`；URL 里已有 `?pwd=` 时不用传。
- 用户没有明确指定目录时，**严禁**传 `--to-pdir-path`、`--to-pdir-fid` 或 `"0"`，必须省略，让 CLI 用默认位置。
  用户明确说了目录才传 `--to-pdir-path "<目录路径>"`；目录不存在就先用官方 `search` 定位目录 fid 再传 `--to-pdir-fid`。

### 第 6 步：回查确认

转存成功（`code: 0`）后，用官方 Skill 的 `search` 按文件名查一遍，确认文件真的进了网盘，再告诉用户保存位置（用成功结果里 `data.save_path` 的原文）。最后可以提一句：“这个分享以后有更新的话，跟我说‘看看有没有更新’就能只补新增的。”

## 追更：只转存分享里新增的内容

适用于连载课程、每周更新的资料这类**已经转存过**的分享。用户说“这个链接有更新吗”“把更新存下来”时：

1. 查更新：`node <quark-cli> get-share-update-files --url "<分享链接>" <公共参数>`。有更新时，按官方规则用表格（文件名、文件大小、文件类型）列出最多 5 项，再原样展示返回的 `msg`；没有更新时原样展示 `msg`。用户没要求就不翻页。
2. 用户同意存全部更新：`node <quark-cli> saveas-update --url "<分享链接>" <公共参数>`，成功后原样展示 `msg`，不要自动再调一次。
3. 用户只要其中几个：先 `get-share-saved-dir --url "<分享链接>" <公共参数>` 拿上次的目录 `pdir_fid`，再 `saveas --url ... --fid-list "<选中的 fid>" --to-pdir-fid <pdir_fid>`；拿不到 `pdir_fid` 时省略目录参数。不要用 `saveas-update`。
4. 返回 `41043`（从没转存过）：告诉用户这个链接还没存过，没法查更新；他想存就走第 5 步的 `saveas`。

想定时追更（例如“每天晚上 10 点帮我看看有没有更新”）：如果你所在的智能体支持定时任务，用它定时执行上面的“查更新”；不支持就如实告诉用户。完整规则以 `<quark-skill-dir>/references/file-saveas.md` 和 `references/file-share.md` 为准。

## 失败处理

- `saveas` 返回 `code != 0`：把 `msg` 原文告诉用户，停下来，不许静默重试、不许换办法绕过去。
- **例外：分享链接本身不可用**（`msg` 表明分享已失效、已取消、不存在、被封禁或提取码错误）：
  1. 先把 `msg` 原文告诉用户，说明是这条分享的问题，不是他的账号问题。
  2. 如果第 3 步的表格里还有其他候选，把**下一条**（标题、日期、链接）推荐给他，问他要不要换这条。
  3. 等用户明确同意后，再用新链接走第 5 步；用户不同意就停下。
  - 一次只推荐一条，不许自动连续尝试多条，不许重新搜索、不许换关键词。
  - 候选用完了就直说“这几条都失效了”，可以建议他换个说法后再让你搜。
- 报错是未授权 / 认证 / token 问题：先展示 `msg`，再引导用户重新走官方 Skill 的 `login`，不要直接重跑 `saveas`。
- 转存同一链接的“更新内容”才用 `saveas-update`（见“追更”）；首次转存一律用 `saveas`。

## 明确不做的事

- 不抓浏览器 cookie、不逆向夸克网页接口、不绕过官方 Skill 的环境检测。
- 不附带、不修改夸克官方 Skill 的任何文件；只在用户同意后，从夸克官方地址下载安装官方 Skill。
- 不部署应用、不跑 Docker、不开常驻服务。本 Skill 只是两段现成能力的拼接：PanSou 搜索 + 夸克官方转存。
- 不提供、不托管任何资源。请只转存用户有权保存的内容。
