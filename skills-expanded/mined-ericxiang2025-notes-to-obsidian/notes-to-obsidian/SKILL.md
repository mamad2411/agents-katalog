---
name: notes-to-obsidian
description: 把散落在得到大脑、腾讯ima、飞书文档/妙记、Plaud等录音卡、钉钉闪记、通义听悟、讯飞、Notion、印象笔记里的笔记和录音逐字稿汇总到本地，用 AI 按企业提效、自媒体两条线分类，生成带看板的 Obsidian 个人知识库，数据全在自己电脑上；装好后带小白上手，能用知识库整理客户需求、会议待办、SOP，或按固定框架写短视频口播逐字稿。用户说“把笔记做成知识库”“把录音卡/妙记/ima/得到的内容导进 Obsidian”“搭个人知识库”“第二大脑”“更新知识库”“用知识库写口播”“用知识库提效”时使用。不用于在原平台新建、修改或删除笔记。
---

# 全平台笔记 → 本地 Obsidian 知识库

把用户分散在各个 App 里的笔记、会议录音、录音卡转写，汇总成一个分好类、带「企业提效看板」和「自媒体选题库」的 Obsidian 知识库，全部存在用户自己电脑上。效果标准见「验收」。用户多是 AI 小白：说人话，一次只问一件事，能给选项就给选项，命令都由你来跑。

本文件里的 `SKILL_DIR` 指本 Skill 目录，`KB` 指知识库数据目录（默认当前工作目录下的 `notes_kb`），命令一律用绝对路径。Windows 上把 `python3` 换成 `python`。

已经建好知识库、用户来用它的：
- 写口播、找选题、规划一周内容 → 读 [references/koubo-framework.md](references/koubo-framework.md)
- 整理客户、会议、SOP、复盘，或问「知识库怎么用」→ 读 [references/after-install-guide.md](references/after-install-guide.md)
- 「更新知识库」「再加一个来源」→ 跳到本文「更新知识库」

## 第一步：开场

先用这段话（按情况微调），然后从第 1 项开始要：

> 我来帮你把散在各个 App 里的笔记和录音，整理成一个随时能查、还能直接拿来干活的个人知识库 📚 数据都存在你自己电脑上。
> 整个过程大约 30-60 分钟，大部分时间是我在后台整理，你只需要：
> 1. 选一下你更想用它做什么
> 2. 告诉我怎么称呼你、做什么工作
> 3. 勾一下你的笔记都在哪些 App 里
> 4. 按我的提示点授权，或者导出文件给我
> 5. 确认一下我帮你归纳的业务方向
> 不会弄的地方直接说「不会」，我来想办法。我们开始吧～

## 第二步：逐项索要

规则：
- 一次只要一项。能用选择题就用选择题。
- 用户发来后先自己检查，不合格就说清哪里不行、怎么补。
- 安装软件、运行命令都由你来做。用户只需要回答问题、点授权、导出文件、确认。
- 用户说「没有」「不会」时，按该项的「没有怎么办」处理，不要卡住。
- 第 1-4 项要齐后，用列表复述一遍收到的内容，并说明「我会帮你安装免费的 Obsidian（如果还没装）」「知识库会放在你的『文稿』文件夹」，让用户回复「对」再开工。第 5、6 项在制作过程中要。

### 1. 你想用知识库做什么（必需）
- 为什么要：决定分类时侧重什么、首页放哪个看板、装好后先教哪种用法。
- 怎么给：回复字母就行——
  - A. 企业提效：整理客户需求、会议待办，把经验变成 SOP 和话术
  - B. 自媒体：从笔记里找选题，写短视频口播逐字稿
  - C. 两个都要（推荐，大多数人既要提效也要做内容获客）
- 合格的样子：A、B 或 C。
- 没有怎么办：拿不准就选 C。A→`enterprise`，B→`media`，C→`dual`。

### 2. 怎么称呼你（必需）
- 为什么要：知识库会叫「XX的知识库」，分类时也要认出笔记里哪个是你本人。
- 怎么给：直接打字，比如「王老师」。再问一句：「别人还会怎么叫你？比如全名、英文名、团队名」。
- 合格的样子：一个称呼，加 0-5 个别称。
- 没有怎么办：用当前账号昵称；知识库名默认「我的知识库」。

### 3. 用几句话介绍你的工作（必需）
- 为什么要：AI 要靠它判断一条录音是「客户沟通」还是「内部会议」，不给的话分类会乱。
- 怎么给：直接打字或发语音转文字，回答三个问题：你是做什么的（行业、职位）？主要卖什么、帮谁解决什么问题？公司、品牌或团队叫什么？
- 合格的样子：「我在杭州做女装批发，自己有两个门店，最近在做视频号带货，团队叫小鹿服饰。」
- 没有怎么办：说「那我先看看你的笔记标题，猜一下你是做什么的，你帮我改」——拿到第一个来源的数据后读 50 条标题，写一段介绍给用户确认。

### 4. 你的笔记都在哪些地方（必需，可多选）
- 为什么要：每个来源拿数据的方法不一样，有的点一下授权就行，有的要你导出文件。
- 怎么给：回复数字，可以多选——
  1. 得到大脑（得到 App 里的 AI 笔记、录音卡）
  2. 飞书（云文档、知识库、妙记会议录音）
  3. 腾讯 ima（笔记、知识库）
  4. Plaud 或其他录音卡
  5. 钉钉闪记 / AI 听记
  6. 通义听悟、讯飞听见
  7. Notion、印象笔记、有道云笔记、Apple 备忘录
  8. 电脑里的一堆 Word / PDF / TXT
  9. 其他（告诉我叫什么）
- 合格的样子：至少一项。
- 没有怎么办：用户说不清，就问「你平时开会、听课、记灵感都用什么 App 录？」再对照上面的列表。

### 5. 授权或导出（每个来源一次，必需）
- 为什么要：没有授权或导出文件就读不到内容。只读，不会在原平台新建、修改或删除任何东西。
- 怎么给：按 [references/sources-guide.md](references/sources-guide.md) 里该来源的步骤，一个来源一个来源来，先做最省事的（得到大脑），每次只给用户一个动作：
  - 能自动的（得到大脑；飞书、ima、Plaud 的官方 CLI/API）：你来装工具、发起授权，用户在浏览器里点「授权」。
  - 要手动的：把导出步骤写成 1、2、3 发给用户，请用户把导出的文件放进一个文件夹，告诉你文件夹在哪（或直接把文件拖进对话）。
- 合格的样子：得到大脑 `getnote auth status` 已登录；其他来源 import_files.py 导入后条数和用户说的大致对得上，录音有逐字稿。
- 没有怎么办：某个来源卡住（比如飞书要管理员审批），先跳过，用其他来源把知识库建起来，之后用「更新知识库」补上。

### 6. 确认你的业务方向（必需，拿到数据后问）
- 为什么要：每条笔记会打上「业务线」标签，以后能按业务筛选。
- 怎么给：读 `KB/work/batch_*.jsonl` 里的全部标题，结合第 3 项，拟 3-10 条业务线，用编号列给用户：「你的笔记大概分这几块业务，对吗？要加、要删、要改名直接说。」
- 合格的样子：「1 门店零售 2 视频号带货 3 加盟招商 4 员工培训」。
- 没有怎么办：用户说「你定就好」，就用你拟的。

## 第三步：制作

按顺序做，每步看输出确认成功再往下。耗时长的步骤开始前告诉用户大概要多久。

### 1. 建工作目录和配置
在 `KB` 写 `config.json`（UTF-8）：

```json
{
  "owner": "王老师",
  "kb_name": "王老师的知识库",
  "mode": "dual",
  "vault": "/Users/用户名/Documents/王老师的知识库",
  "self_names": ["王老师", "王小明", "小明"],
  "people_alias": {},
  "org_alias": {}
}
```

vault 默认放在用户「文稿/Documents」文件夹下、以 kb_name 命名；目录已存在且不是之前生成的仓库时，先问用户。

### 2. 拉取得到大脑（第 4 项选了 1 才做）
1. `node -v`。没有 Node：macOS 有 Homebrew 用 `brew install node`，Windows 用 `winget install OpenJS.NodeJS.LTS`；都不行就请用户从 nodejs.org 下载 LTS 安装包。
2. `npm install -g @getnote/cli@latest`，然后 `getnote version`。
3. 后台运行 `getnote auth login`，从输出里取 `https://biji.com/openapi/oauth/authorize?code=...` 链接发给用户：「浏览器里会出现得到大脑的授权页，没登录先用手机号登录，然后点『授权』，好了回我一声。」
4. 用户说好了以后，跑 `getnote doctor -o json` 和 `getnote notes --limit 1 -o json`，确认能读到最近一条笔记。
5. 两个进程并行下载，都在后台跑。第二个要等第一个打印出「笔记共 N 条」再启动：
   ```bash
   python3 SKILL_DIR/scripts/fetch_getnote.py --kb KB
   python3 SKILL_DIR/scripts/fetch_getnote.py --kb KB --reverse --no-list
   ```
   每条约 0.5-1.5 秒，400 条约 10 分钟，等待时去做其他来源。两个都打印 `done` 后看 `详情已下载 X/Y`：X 小于 Y 就再跑一次第一条命令（已下载的跳过）。最后跑一次 `--normalize-only`，确保统一格式文件是全量的。

### 3. 拉取飞书（第 4 项选了 2 才做）
按 [references/sources-guide.md](references/sources-guide.md)「飞书」一节装好 lark-cli、请用户在浏览器授权，然后：
```bash
python3 SKILL_DIR/scripts/fetch_feishu.py --kb KB
```
它会只读导出知识库、云空间文档和上传的 PDF/Word，并自动导入。约每篇 1-2 秒。看结尾的「非文档节点不导出」和「下载失败」两行，告诉用户哪些没导、为什么。

### 4. 拉取腾讯 ima（第 4 项选了 3 才做）
1. 请用户打开 https://ima.qq.com/agent-interface 生成 Client ID 和 API Key，告诉用户「不要发给我，等下会弹出输入框让你自己粘贴」。
2. `python3 SKILL_DIR/scripts/setup_ima.py`：用户在弹窗里粘贴，脚本保存并测连接，打印出知识库列表才算成功。
3. `python3 SKILL_DIR/scripts/fetch_ima.py --kb KB`：只读导出全部笔记和知识库文件，并自动导入。

### 5. 拉取其他来源
每个来源按 [references/sources-guide.md](references/sources-guide.md) 操作：
- 能自动导出的：你按「落地格式」把每条笔记写成 md 放进 `KB/inbox/<来源key>/`。标 ⚠️ 的接口第一次先导 3-5 条，打开文件确认标题、时间、正文都对，再全量。
- 手动导出的：用户给的文件夹直接用，不用复制。

然后每个来源跑一次：
```bash
python3 SKILL_DIR/scripts/import_files.py --kb KB --source <来源key> --dir "<文件夹>"
```
看输出：导入条数、录音转写条数、找不到日期的条数、读不出的文件。录音转写是 0 但用户说有录音，多半是只导了摘要没导原文，请用户补导。

### 6. 写分类规范
把 [references/taxonomy-template.md](references/taxonomy-template.md) 复制到 `KB/work/taxonomy.md`，用第 1、2、3、6 项填好所有【填写：…】。

### 7. AI 分类
1. `python3 SKILL_DIR/scripts/build_catalog.py --kb KB`，把所有来源合在一起按每批 50 条切成 `KB/work/batch_XX.jsonl`。这时问第 6 项。
2. 每批开一个子 agent，可以同时开（一次最多 8 个），任务写：「读 KB/work/taxonomy.md 和 KB/work/batch_XX.jsonl，按规范给每一条分类，结果写到 KB/work/out_XX.jsonl，每行一个 JSON，不得遗漏」。没有子 agent 就自己一批一批做。
3. 全部子 agent 结束后运行 `python3 SKILL_DIR/scripts/merge_classified.py --kb KB`。打印 `MISSING` 或 `BAD` 时，只把对应批次重新分类，再合并，直到退出码为 0。

### 8. 生成知识库数据
```bash
python3 SKILL_DIR/scripts/build_kb.py --kb KB
python3 SKILL_DIR/scripts/search.py --kb KB 客户
```
输出里「待分类」应为 0；检索能搜到结果。

### 9. 检查敏感信息
在 `KB/索引/notes.jsonl` 里搜密码、密钥、token、`sk-`、身份证号、银行卡号这类内容。找到就把笔记标题、日期和来源告诉用户（不要复述内容本身），建议去原平台删掉或改掉那一段。

### 10. 统一人名写法
`python3 SKILL_DIR/scripts/build_obsidian.py --kb KB --entities` 预览人物和机构。同一人或同一机构的不同写法（错别字、中英文、简称）写进 config.json 的 `people_alias` / `org_alias`，如 `{"Big Apple": "BigApple"}`；值写 `null` 表示丢弃。拿不准的问用户。一定要在第 11 步之前做：已生成的笔记不会再覆盖。

### 11. 装 Obsidian、生成仓库并打开
1. 没装 Obsidian：macOS `brew install --cask obsidian`，Windows `winget install Obsidian.Obsidian`；都不行就请用户去 obsidian.md 下载安装。
2. `python3 SKILL_DIR/scripts/build_obsidian.py --kb KB`
3. 完全退出 Obsidian（macOS：`osascript -e 'quit app "Obsidian"'`），再运行 `python3 SKILL_DIR/scripts/register_vault.py --kb KB`。
4. 启动 Obsidian（macOS `open -a Obsidian`），在仓库里打开首页「🏠 kb_name」。第一次打开会问「是否信任此仓库的作者」，告诉用户点「信任」。

### 12. 带用户上手
读 [references/after-install-guide.md](references/after-install-guide.md)，按第 1 节的三步话术带用户看首页、看板，并让用户马上试一个玩法。

## 更新知识库

用户说「更新知识库」「把新笔记加进来」「再加一个来源」时：
1. 得到大脑：`python3 SKILL_DIR/scripts/fetch_getnote.py --kb KB`（只下载新笔记）；飞书：`fetch_feishu.py --kb KB`；ima：`fetch_ima.py --kb KB`（都只下载改过的）。
2. 其他来源：自动导出的重新导出到同一个 inbox 文件夹；手动的请用户把新导出的文件放进**原来那个文件夹**，再对每个来源重跑 import_files.py。新来源按第三步 3-5 加进来。
3. `python3 SKILL_DIR/scripts/build_catalog.py --kb KB --only-new`，把新批次按第三步 7 分类，再跑 `merge_classified.py`。
4. 重跑 `build_kb.py` 和 `build_obsidian.py`（用户在 Obsidian 改过、移动过的笔记会跳过，不会被覆盖）。
5. 告诉用户新增了几条、来自哪些来源、分别在哪个分类，有没有新的高潜力选题。

## 踩过的坑

- `getnote setup` 报 `EBADENGINE` 或 `node:zlib does not provide an export named crc32`：setup 需要 Node 22.20 以上。本流程用不到 setup，只用 `getnote auth login`，Node 20 就够。
- `getnote doctor` 提示某些 AI 工具没装 Skill：不影响导出，只要登录和 API 连通正常就继续。
- 得到大脑列表接口不带正文：每条都要单独读详情，录音还要单读逐字稿，fetch_getnote.py 已处理。读接口每天上限约 2 万次，超过 8000 条笔记分两天跑。中途网络报错或后台进程被杀，直接重跑，已下载的跳过。
- 空白录音读逐字稿会报 `audio transcript is not available`：已写成空逐字稿占位，重跑不会反复重试。
- 录音类平台（Plaud、通义听悟、钉钉、飞书妙记）的总结和逐字稿常是**两个文件**：都导出、放同一文件夹、别改「_原文」「_转写」这类后缀，import_files.py 会合成一条。
- 文件里找不到日期时用文件修改时间，通常是导出那天，按日期看会扎堆：请用户导出时保留文件名里的日期。
- 改文件名或换文件夹后再导入，会被当成新笔记：同一来源的文件一直放同一个文件夹，别改名。
- 飞书 lark-cli 不加 `--as user` 会用机器人身份，看不到个人文档；`wiki +space-list` 不返回个人文档库，`wiki +node-list` 不递归，云空间和知识库是两套接口——fetch_feishu.py 都处理了。
- 飞书 `drive +download --output` 只接受当前目录下的相对路径，给绝对路径报 `unsafe output path`。
- 飞书妙记转存到云空间后是「智能纪要：X」「文字记录：X」两篇文档，fetch_feishu.py 会合成一条录音笔记。
- 不要让用户把 API Key、密码贴进聊天：ima 用 setup_ima.py 弹窗让用户自己粘贴。用户已经贴进聊天的 Key 不要用，请他重新生成。
- ima 的 Client ID 和 API Key 小白很容易粘反：setup_ima.py 会按「Client ID 是 32 位十六进制」自动对调。
- ima 笔记取纯文本会丢分段，fetch_ima.py 取 JSON 再转 Markdown；没写标题的笔记标题是一个退格符，已用正文开头代替。
- 子 agent 还在写的时候就合并，会少几十条：等所有子 agent 都报告结束再跑 merge_classified.py。
- 分类没覆盖到的笔记会进 `00_待分类`，不会悄悄进「空白无效」；看到待分类就补分类。
- 搜两个字的词（如「保险」）FTS 搜不到：trigram 分词至少要 3 个字，search.py 已自动改用 LIKE。
- 笔记里的图片链接带签名、几天后失效，所以图片都去掉了；要看图点笔记里的「原笔记」回原平台看。
- 仓库没登记时，`obsidian://` 链接和直接打开都没反应：用 register_vault.py 登记后再启动。Obsidian 运行中改 obsidian.json 没用，它退出时会覆盖回去，先完全退出再登记。
- 笔记和逐字稿同名时 `[[链接]]` 会指错：逐字稿文件名固定带 `_逐字稿` 后缀，不要改名。
- 「文稿」文件夹在 Mac 上常开 iCloud 同步，客户信息会跟着上云：交付时告诉用户。

## 验收

交付前逐条检查，不通过就修：
- [ ] 第 4 项选的每个来源都已导入，或已告诉用户哪个来源卡住、怎么补
- [ ] 得到大脑：`fetch_getnote.py` 显示详情已下载数 = 笔记总数，`errors=0`
- [ ] 飞书：`fetch_feishu.py` 结尾没有「下载失败」，或已告诉用户哪几篇没权限
- [ ] ima：`setup_ima.py --check` 显示已连接，`fetch_ima.py` 结尾没有「失败」
- [ ] 其他来源：每个 import_files.py 的导入条数和用户预期大致相符，有录音的来源录音转写条数 > 0
- [ ] `merge_classified.py` 退出码 0；`build_kb.py` 显示待分类 0
- [ ] `search.py` 搜一个用户业务里的词能搜到笔记
- [ ] 仓库里笔记数 = 所有来源合计；每条有逐字稿的录音笔记都能点开「逐字稿：打开」
- [ ] 首页显示各来源条数和分类导航表，看板和第 1 项选的方向一致（dual 两个，enterprise 只有企业提效看板，media 只有自媒体选题库）
- [ ] 自媒体选题库里有「口播潜力高」的选题（dual / media）；企业提效看板里有「可沉淀成方法/SOP」（dual / enterprise）
- [ ] 再跑一次 `build_obsidian.py`，显示 `notes added=0`
- [ ] Obsidian 已打开这个仓库并显示首页
- [ ] 已告诉用户敏感信息检查结果和 iCloud 同步情况

## 交付

告诉用户：
1. 知识库叫什么、共多少条笔记（按来源分别多少）、多少条录音逐字稿、各分类各多少条
2. Obsidian 仓库的绝对路径和数据目录 KB 的绝对路径（裸路径，一行一个）
3. AI 没把握的有几条，在「待复核的分类」页；没导成功的来源和补救办法
4. 然后按 after-install-guide 第 1 节带用户上手
