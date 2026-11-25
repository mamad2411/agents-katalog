---
name: jisai-storybook
description: >
  从故事、主题、人物/宠物照片、孩子涂鸦、已有角色或风格参考制作可逐页审校的完整绘本：封面、扉页、正文、封底，每页一张成品图，再合成整本 PDF 和翻页网页。正文支持代码排版或模型画进图里，用卡司定妆锚、风格锚、走位账、小样、单页重抽和断点续跑控制质量。用户请求“做绘本/图画书/storybook/picture book/把故事做成绘本/给孩子做一本书/出版级绘本/用照片或涂鸦当主角/做上一册的续集”，或修改已有绘本时使用。单张配图、只写故事、只翻译、纯印前文件处理不用本 Skill；漫画分格是实验能力，不保证自动达到出版验收标准。
metadata:
  version: 1.2.0
  author: 极思狂想
---

# 绘本工坊

把用户的故事和素材做成一本可逐页审校的书。图像模型负责插画及指定的图中文字，代码负责页序、排版、合成与机械检查。追求出版所需的画面与文字质量，仍需人工验收；不做出血、折缝、条码、书脊等印前工程。

## 开始前

- 从用户项目目录工作，产物放 `.storybook/<slug>/`，不写进 Skill 目录。
- 下文命令里的 `scripts/` 指本技能安装目录下的脚本；从用户工作区执行时换成实际绝对路径，`python` 指已安装 `requirements.txt` 的环境。
- 生图前说明用哪个后端、会发送哪些提示词和参考图、重试可能的费用；只采用用户已确认的素材使用范围。
- **生图按能力选**：当前 Agent 自己有能出图的工具（如 Codex 的 `imagegen`），就用它，不用问；自己不能出图（如 Claude Code），才用 `scripts/image_gen.py` 走外部服务，默认 Labnana · GPT Image 2。细则见 `references/image_backend_policy.md`。
- **看图**：下文“看图”指用宿主能直接查看图片的工具（Codex 的 `view_image`、Claude Code 的 Read 等）亲眼看一遍，不靠文件名或脚本结论代替。
- **等待用户**：简报页和预览页都是“起服务”与“等提交”两条命令。给出地址后这一轮不结束，一直等到确认信号；能挂后台任务的宿主把等待命令放后台，不能的在同一个命令会话里反复读输出。细节见 `references/brief_confirm.md` 的“启动与等待”。
- 按需读参考：每本必读 `project_contract.md`；第 1 步前读 `brief_confirm.md`；写故事与分镜前读 `storycraft.md`；定妆和逐页生图前读 `consistency.md`、`image_backend_policy.md`；验收前读 `quality_gates.md`；成书前读 `book_production.md`；用途影响页数与交付时读 `delivery_profiles.md`；出图卡住（同一问题修了两次没好、多页同类返工、单页尝试到 4 次）先读 `escalation.md`。

## 不可破坏的纪律

- 串行推进，四个 ⛔ 确认点必须停：**简报 → 翻页小样 → 定妆 → 校样**；字多、标注多的书在定妆后多一个 **方案比选** ⛔（第 4.5 步）。小样没确认不定妆，定妆没确认不画正文。确认点都在网页上完成，聊天里只说一句话加地址，不把分镜表、定妆图贴进对话。
- 简报确认前不建项目、不写分镜、不生图。
- 每次生图前重读 `style_lock.md`；逐页提示词一律用 `gen_all.py next` 给的，不自己另写一套。
- 同一本书锁定同一后端/模型/分辨率，不为某一页更好看临时换。锁定发生在方案比选之后（没有比选的书在定妆时锁定）；要改锁定，回到方案比选，并先问用户。
- 同一个修法最多用两次，不成就按 `escalation.md` 升一层（换配置 → 方案比选 → 换文字方式）。新做法先拿最难的一页跑通，再批量。
- 从简报起就是同一个地址：简报页确认后原地变成预览页。每个确认点由 `gate.py open` 送到用户眼前，聊天里不用再让用户点链接。
- 只存相对路径；真人素材与风格参考分通道，真人照片绝不能进 `styleAnchor`。
- 文字分工：唯一的选择是正文怎么上图。`book.textStrategy: typeset`（默认，“印上去”）由代码排在分镜设计好的文字区里，字号按页宽比例（正文约 4.4%）；`integrated`（“画进图里”）由模型按同一个 box 画进画面。封面书名、拟声字、场景招牌始终由模型画；扉页、封面署名、封底简介始终由代码排。任何时候都不允许“统一压在底部的字幕条”。
- 走位、数量、道具状态写进数据（`blocking`），穿帮靠改数据修，不靠换说法重抽。

## 1. 创作简报 ⛔

简报问五件事：讲什么故事、给谁读、主角是谁、什么画风、书做成什么样（页数、横竖、正文印上去还是画进图里）。逐件对照用户已经说的话：

- 五件都已经定了，跳过页面，用一句话复述这五件后直接建项目；
- 缺任何一件就起页面，已经说过的项预选好。“帮我构思一个故事”“20 页左右、日系画风”都属于缺项；
- 只在起不了本地页面（没有 Python 或浏览器）或用户明确说“就在聊天里定”时，才在聊天里逐项列出五件、等用户回复。

先从用户已给的故事、素材、用途里提炼推荐，写入 `.storybook/.brief/<slug>/brief.recommendations.json`，再起页面并等待：

```sh
python scripts/brief_confirm.py .storybook/.brief/<slug> --daemon
python scripts/brief_confirm.py .storybook/.brief/<slug> --wait --wait-timeout 540
```

- 三张故事方向卡，一张标推荐，每张带 `copy_policy`。用户给了完整故事时三张卡是“忠于原稿 / 轻度润色 / 创作性改编”。
- `text_mode` 默认 `typeset`；用户想要手作感、字和画融为一体时推荐 `integrated`，并说明偶尔写错要重画。
- 画风填 `recommend.style_id`，页面自动列出内置十种。用户点名了十种以外的画风，起页面前先画一张同场景样图：`brief_confirm.py <session> --style-new --name <6 字内> --core "<中文画法要点>" --masters "<画家 · 画家>"`，自己能出图就按输出的 `STYLE_PROMPT` 画到 `out` 再 `--style-done <id> --image <out>`，不能出图的加 `--draw` 一步画完。`--core` 只写笔触、线条、配色、材质；`--masters` 写所属画家或作品谱系。
- `backend.external`：自己能出图写 `false`，走外部服务写 `true`。页面不写服务和模型名，用哪家在聊天里说。
- 等待命令的输出：`BRIEF_CONFIRMED` 进入第 2 步；`BRIEF_STYLE_REQUEST {...}` 是用户在页面上要看新画风，按 `desc` 画样图（流程同上，带 `--style-id <id>`，画不出来就 `--style-fail`），再带 `--accept-existing` 接着等；`BRIEF_TIMEOUT` 就带 `--accept-existing` 续等。`--wait-timeout` 不超过 540。

## 2. 建项目

确认后创建 `.storybook/<slug>/`，按 `project_contract.md` 写 `project.json`（schemaVersion 4）、`style_lock.md`、`storyboard.md`，复制素材到 `assets/`。再生成页序（封面 → 扉页 → 正文 → 封底）：

```sh
python scripts/book_plan.py init .storybook/<slug> --pages 12
```

## 3. 故事、分镜与翻页小样 ⛔

按 `storycraft.md` 先写故事账（`story.want / obstacle / change / setups`），再按页序写每个单元：

- `prompt` 只写这一页画什么，一两句；风格、角色、约束由装配器加。
- `blocking`：地点、时间、`cut`、每个角色的位置和朝向、要数准的东西、会变化的道具状态。方位词和动作要写实，小样草图就是从这里推出来的。
- `textBlocks`：正文写 `box`（页面内归一化坐标，常用上部 `[0.08,0.06,0.84,0.14]`、下部 `[0.08,0.8,0.84,0.14]`）；封面书名、拟声、招牌另写 placement/container/typography。
- `entities` 主角第一；`risk` 标风险（只决定补抽额度，每页都只先画一张）。
- 扉页、版权、封底简介所需信息写进 `book.colophon`。

检查、出小样、估算，然后送到预览页：

```sh
python scripts/validate_project.py .storybook/<slug>
python scripts/continuity.py check .storybook/<slug>
python scripts/layout_book.py proof .storybook/<slug>
python scripts/estimate.py .storybook/<slug>
python scripts/gate.py open .storybook/<slug> proof
python scripts/watch_submit.py .storybook/<slug> --serve --check   # 起预览,马上返回地址
python scripts/watch_submit.py .storybook/<slug> --timeout 540     # 等用户提交,TIMEOUT 就重跑
```

「翻页小样」面板顶部是故事账三句话和登场名单，每页一张由 `blocking` 和动作词推出的火柴人示意（推错的页写 `page.sketch` 覆盖，见 `project_contract.md`），右栏可直接改这页的字，「连起来读」顺读全书正文。用户提交后监听器输出 `SUBMIT {"scope":"gate",...}`，Agent 跑：

```sh
python scripts/gate.py apply .storybook/<slug>
```

它把页面上改过的字写回 `project.json`，打印用户意见和下一步。`confirm` 进入第 4 步；`revise` 按意见改分镜后再 `gate.py open ... proof`。处理完删掉 `submit.signal`，重挂监听器。

## 4. 锁风格与全员定妆 ⛔

风格核心用 `brief.result.json` 的 `style_core`，画家谱系用 `style_masters`，分别写进 `project.json.styleCore`、`styleMasters` 和 `style_lock.md`；`custom_style` 里的微调补在风格核心后面。简报页样图就是用这两项画的，用户选的就是看到的。也可从 1–3 张参考图提炼高层风格；现画画风的样图（`style_sample`）可当风格锚的参考图。

出现 ≥2 次的角色、物体、环境全部登记 `cast`（写 `descriptorZh`），各生成一张定妆锚；另生成只含空场景的 `anchor/style.png`。`python scripts/cast.py check` 必须通过。照片/涂鸦主角另做 identity 确认，用户未确认前 `identityApproved` 不得为 true。续作先 `python scripts/library.py list` 复用已有卡司与风格。

每张锚画完都先看图。全部画完后送到预览页确认：

```sh
python scripts/gate.py open .storybook/<slug> cast --message "定妆画好了：N 个角色加 1 张风格锚"
```

收到 `SUBMIT {"scope":"gate"}` 后跑 `gate.py apply`：`confirm` 进入整本生成；`revise` 只重画 `redo` 里那几张（带上意见），画完再 `gate.py open ... cast`。

## 4.5 方案比选 ⛔（字多、标注多的书）

认知书、标注图、每页十来块图中字的书，定妆确认后先拿 1–2 页最难的页比几种配置，开跑前告诉用户这要花几次生图：

```sh
python scripts/trial.py run .storybook/<slug> --page p10 --config gpt-image-2@2K --config gpt-image-2@4K --config gemini-3-pro-image@4K
python scripts/trial.py note .storybook/<slug> gpt-image-2-4K --text-errors 0 --struct-errors 1 --note "红包箭头指到了波波"
python scripts/gate.py open .storybook/<slug> trial
```

每一张都逐块核对字、数量和指向并 `note`，没核对完 `gate.py open trial` 会拒绝打开。用户选定后 `gate.py apply` 把 `provider`、`imageModel`、`imageSize`、`imageQuality` 锁进 `project.json`。几种都不行时，下一层是“模型画场景、代码画标签”（`scripts/label_overlay.py`），同样先拿一页跑通再批量。

## 5. 整本生成

预览一直开着（没开就 `watch_submit.py <project> --serve --check`），用户在那里看进度。队列一次给一个完整 job：

```sh
python scripts/gen_all.py next .storybook/<slug>
```

job 里有装配好的中文 `prompt`、`aspectRatio`、`references`（主角锚在前；同地连续页自动带上一页成图）和需要画进图里的字。对每个 job：重读 `style_lock.md` → 用锁定的后端出图 → 落到 `job.candidate` → `quality_gate.py` → 看图按核对单检查 → 记录结论：

```sh
python scripts/gen_all.py record <project> <page> --candidate <file> --backend <job.backend> --model <job.model> --qa pass
```

`pass` 的单图页自动落稿；`fail` 按风险额度重抽；`review` 留给用户在预览里定。job 或 `gen_all.py summary` 出现 `escalate` 就停止重抽，按 `escalation.md` 换路。重复 `next` 直到 `{"done": true}`，中断后重跑 `next` 即续。走外部服务时可以用 `gen_all.py run-scriptable` 批量出候选（一页失败会整轮退出）。

## 6. 逐页 QA

按 `quality_gates.md`：机械关卡（比例、空白、OCR、文字区够不够静）+ 看图核对单（角色标志与配色、对照 `continuity.py ledger` 的朝向/位置/数量/道具、文字区无物无字且没露白纸、图中字逐字正确）。失败理由写具体，留进 meta。画错的图中字先定点改，最多两次；仍失败就整页重画一次，再不行按 `escalation.md` 升级。

## 7. 校样与回改 ⛔

```sh
python scripts/make_book.py .storybook/<slug>
```

依次：校验 → 连续性 → 缺页检查 → 排版出 `book/NN-<id>.png` → `exports/<书名>.pdf` → `book.html` → `exports/preflight.json`，校样在 `layout/index.html`。

用户在预览页看校样、写意见、提交后：`set_status.py ... working` → 读 `review.json` 与 `submit.signal` → 按 `workflows/regen_page.md` 只重抽相关页 → 重跑 `make_book.py` → 写 `done`、删 signal、重挂 watcher。不为救一页改全书 `style_lock.md`。

**跨回合接续**：书没交付前，每个回合先跑 `python scripts/watch_submit.py .storybook/<slug> --check`。有 `SUBMIT {...}` 就处理（`scope: gate` 走 `gate.py apply`，其余是改图意见）；`NO_PENDING` 就继续；输出 `PREVIEW restarted ...` 时把新地址告诉用户。

## 8. 交付

`preflight.json` 的“必须改”清零才交付；“看一眼”逐条确认（常见是文字底下偏花、字体只适合打样）。交付前机械盘点 `book/` 页数，打开校样逐页看一遍。公开发布含真人形象时提醒肖像权，由用户决定。

## 参考与脚本

- `references/`：`brief_confirm.md` 简报页与等待 · `project_contract.md` 字段 · `storycraft.md` 故事与分页 · `book_production.md` 页序、文字分工、版式 · `consistency.md` 锚点、走位账、提示词装配 · `image_backend_policy.md` 后端与落盘 · `quality_gates.md` 质检 · `delivery_profiles.md` 用途与导出 · `escalation.md` 升级梯子与止损 · `models.md` 外部后端
- 简报与确认点：`brief_confirm.py` · `gate.py` · `trial.py`
- 项目与校验：`book_plan.py` · `validate_project.py` · `cast.py` · `continuity.py` · `estimate.py` · `library.py`
- 生成：`gen_all.py` · `prompt_build.py` · `image_gen.py` · `collect_builtin_output.py` · `quality_gate.py` · `contact_sheet.py` · `label_overlay.py`
- 成书：`layout_book.py` · `make_book.py` · `bookgeom.py` · `assemble_book.py` · `export.py`
- 预览与回改：`watch_submit.py` · `preview_book.py` · `ui_server.py` · `set_status.py` · `workflows/regen_page.md`
