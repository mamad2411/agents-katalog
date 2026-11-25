---
name: ship-taptap-minigame
description: TapTap 小游戏发布：把 Unity 游戏导出成 TapTap 小游戏包，从认证开发者、创建游戏、上传包体并通过包体准入测试、前置备案、填商店资料，一直推进到提交审核。用户要发布、上架、提审到 TapTap 小游戏；要接 TapTap 小游戏的登录、成就、排行榜、云存档、分享、广告；问广告收入能不能结算；或 TapTap 包体准入测试失败、前置备案卡住、审核被拒时使用。
---

# TapTap 小游戏：从认证开发者推到提审

目标：把 Unity 游戏以「Tap 小游戏」形态推到 TapTap 后台显示「审核中」。

**先做**：确认 [ship-my-game](../ship-my-game/SKILL.md) 的第 1～4 步已完成（进度档案、渠道、体检、浏览器），没完成就先读它。本渠道的进度写在进度档案的 `## taptap-minigame` 一节。

**开工前先告诉用户三件事**，并写进进度档案：

1. **引擎**：官方建议 Unity 2022+ 或团结引擎 1.2.0+，没有声明支持 Unity 6 [官方](https://developer.taptap.cn/minigameapidoc/dev/engine/unity-adaptation/engine-suggestions/)。本仓库用 Unity 6000.6 实测：前 4 版逐个暴露问题、都没过包体准入测试，第 5 版（1.0.7）通过 `[实测]`。修法已全部写进 `scripts/ShipTapBuild.cs`，另有一条游戏代码规则：TapTap 构建里不能调用 `WeChatWASM.WX`。2022.3 / 团结引擎这条官方路线本仓库还没实测。
2. **个人、没有版号**：只能以「开放试玩」上线，不能内购 `[实测]`；上线前必须做完前置备案，全程约 20 个工作日 [官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/pre-filing/)。
3. **广告**：Unity 小游戏只能接 TapADN（Dirichlet）[官方](https://developer.taptap.cn/minigameapidoc/quick-start/mcp-guide/ad-integration-guide/)。Dirichlet 的协议允许个人结算（个人累计不足 1000 元可暂不结算），但每次结算都要附等额的增值税专用发票；个人能不能代开、Dirichlet 认不认代开的票，**未确认**。详见 [payouts.md](references/payouts.md)。

## 本人事项

| 事项 | 阶段 |
|---|---|
| 实名认证成为「认证开发者」（姓名、身份证正反面扫描件） | P1 |
| 同意《TapTap 小游戏开发者协议》（打开后台时弹出，协议更新会再弹） | P1 |
| 授权 TapTap CLI：在已登录后台的浏览器里打开你给的设备码链接并确认（5 分钟内有效，属于本次「一次登录」） | 用 CLI 时 |
| 手机扫码自测；提供自己的 TapTap 用户 ID，用来加进成就、排行榜的测试名单 | P3、P4 |
| 同意下载准入测试日志（浏览器下载） | P3 失败时 |
| 前置备案：负责人信息和证件照、服务核准承诺书（打印、手写证件号、签字、拍照）、电子化核验扫码、工信部短信 24 小时内核验 | P5 |
| 同意把隐私政策网页发布到公网 | P6 |
| 点被你的权限系统拦下的按钮：包体上传抽屉第 2 步「提交」、最终「提交审核」 | P3、P7 |

## 工程要求

ship-my-game 第 3 步按这张表列差距。细节见 [references/build.md](references/build.md)。

| 项 | 要求 | 依据 |
|---|---|---|
| 引擎 | Unity 6000.x：用本仓库脚本的全部补丁，1.0.7 实测通过准入测试。或官方建议的 Unity 2022.3 LTS / 团结引擎 1.2.0+（官方原文「建议使用 Unity 2022+ 版本，团结引擎 1.2.0+ 版本」），本仓库未实测 | Unity 6 `[实测]`；[官方](https://developer.taptap.cn/minigameapidoc/dev/engine/unity-adaptation/unity-webGL/) |
| 微信适配层 | TapTap 构建里不调用 `WeChatWASM.WX` 的任何接口：存档、窗口信息、胶囊按钮改用 `TapTapMiniGame.Tap` 的同名接口。调用了会在第一帧崩溃黑屏，见 troubleshooting.md 2.3 | `[实测]` 1.0.6 失败、1.0.7 修好 |
| 平台模块 | WebGL Build Support | — |
| SDK | `com.taptap.minigame` 2.0.21，用 `scripts/fetch_tapsdk.sh` 嵌进 `Packages/`；不能和微信小游戏 SDK 在同一个工程里，TapTap 渠道单开 git 分支或工作区 | `[实测]` |
| 图形 | WebGL 2；Linear 色彩空间只能配 WebGL 2 | [官方](https://github.com/taptap/minigame-sdk-unity) |
| 包体 | `game.zip` 按 20 MB 以内准备（包体管理页和审核规范 5.2.2 写 20 MB；接入指南写首包压缩后 < 60 MB；上传框写 < 300 MB）。wasm 代码包（.br）超过 10 MB 必须开 Wasm 分包 | `[实测]` 页面原文；[官方](https://developer.taptap.cn/minigameapidoc/dev/tutorial/performance/launch/wasm-subpackage/) |
| 必接 | TapTap 登录（审核规范 5.2.4；包体管理页「请确保上传包体内已正确接入 TapTap 登录」） | [官方](https://developer.taptap.cn/minigameapidoc/tap-operation/operation-standards/review-standards/) |
| 合规界面 | 首次处理个人信息前弹窗征得同意（不得默认勾选）；启动页放适龄标识和《隐私政策》按钮（按钮不小于 40×40 像素）；适龄提示全文；健康游戏忠告。用 `scripts/ShipCompliance.cs` | [官方](https://developer.taptap.cn/minigameapidoc/tap-operation/operation-standards/behavior-standards/)；代码 `[实测：编译通过，界面未上真机]` |
| 中文字体 | 打包中文字体子集，扫描范围要包括合规文案 | `[实测]` |
| 不能用 | 多线程、`System.Net`、`System.IO.File`、原生插件（.so、.framework、C++ dll）、FMOD/Wwise | [官方](https://developer.taptap.cn/minigameapidoc/dev/engine/unity-adaptation/engine-suggestions/) |
| 建议接 | 「添加到桌面」：文档指引把它列为「必接能力」，审核是否强制未确认 | [官方](https://developer.taptap.cn/minigameapidoc/quick-start/document-guide/) |
| 广告 | 广告位 ID 为空时隐藏所有广告入口，避免出现点了没反应的按钮 | `[实测]` |

## 阶段

命令和链接里的相对路径（`scripts/…`、`../ship-my-game/…`）都以本 skill 目录为起点。

### P1 账号、游戏和 MiniApp ID

1. 打开 https://developer.taptap.cn/ →「进入控制台」，读顶栏的厂商名和「信用等级」。不是认证开发者时，按 [onboarding.md](references/onboarding.md) 带用户完成认证：免费，审核约 2 个工作日 [官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/registration-login/)。
2. 页面被「TapTap小游戏开发者协议」弹窗挡住时：用三五句话讲清要点，请用户滚到底部点同意 `[实测]`。
3. 还没有游戏时：开发者中心 →「创建游戏」→ 游玩提供方式选「小游戏」→「保存并提交」[官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/creation-improvement/)。也可以用 CLI 的 `app create-app`，见 [automation.md](references/automation.md)。
4. 打开「商店 → 游戏包管理 → 小游戏管理 → 小游戏介绍」，确认页面显示「当前已开通」`[实测]`。没开通时按 onboarding.md 处理。
5. 打开「小游戏管理 → 开放能力 → 小游戏基本信息」，复制 MiniApp ID `[实测]`。同一处的 Secret 打包用不到，不要点「查看」，也不要外传。

完成标准：
- 账号是认证开发者，小游戏页面不再弹协议。
- 「小游戏介绍」显示已开通。
- MiniApp ID 已写进 `publish/taptap/build.json`；游戏 ID 和开发者 ID（后台网址 `/<开发者ID>/app/<游戏ID>/` 里的两段）已记进进度档案。

### P2 改工程并导出 game.zip

1. 按「工程要求」定下引擎版本，写进进度档案。Unity 6 工程照常往下走：补丁由脚本自动打；另外在代码里搜 `WeChatWASM.WX`，TapTap 构建里一处都不能留（见 [build.md](references/build.md) 第 4 节）。
2. 在单独的 git 分支或工作区里运行 `bash <本 skill 目录>/scripts/fetch_tapsdk.sh <工程目录>`，并把 `Packages/com.taptap.minigame/` 加进 `.gitignore` `[实测]`。
3. 复制下面三个文件，并替换文案里的全部 `{{占位符}}`：
   - `scripts/ShipTapBuild.cs` 放到 `Assets/Editor/`；
   - `scripts/ShipCompliance.cs` 放到 `Assets/Scripts/`；
   - `templates/compliance.zh-Hans.txt` 放到 `Assets/Resources/ShipCompliance/zh-Hans.txt`。

   然后在启动流程里接好：同意弹窗 → 同意后 TapTap 登录；启动页放适龄标识和隐私政策按钮。代码见 [build.md](references/build.md) `[实测：编译通过，未上真机]`。
4. 用 [`../ship-my-game/scripts/make_cjk_font.py`](../ship-my-game/scripts/make_cjk_font.py) 生成中文字体子集，扫描范围要包括 `Assets/Resources/ShipCompliance/` `[实测]`。
5. 照 `templates/build.json` 写 `publish/taptap/build.json`，版本号要比上一次上传的高。然后运行 `../ship-my-game/scripts/unity_build.sh <工程目录> WebGL ShipTapBuild.Export taptap` `[实测：同一套补丁的 Unity 6000.6 游戏通过准入测试；空工程导出成功；2022.3 未实测]`。
6. 上传前本机预检：`node scripts/tap_boot_test.js <dst>/minigame`。它在 node 里把包启动到 `main()`，能提前发现链接失败、启动顺序和 SystemInfo 问题；第一帧之后的问题看不到 `[实测]`。

完成标准：
- 日志里有 `[Ship] taptap export=SUCCEED`。
- 预检输出 `main() ran after the data package`，退出码 0。
- `<dst>/game.zip` 存在且不超过 20 MB；超了就按 build.md 的「包体大小」一节处理。
- 本次版本号已记进进度档案。

### P3 上传开发版本，通过包体准入测试

1. 上传 `game.zip`，选一种方式：
   - 首选 TapTap CLI：先 `upload-mini-app-package`，再 `submit-mini-app-package`，见 [automation.md](references/automation.md)。上传步骤 `[实测]` 成功。
   - 备选网页：「包体管理 →「上传包体」」两步抽屉，见 [console.md](references/console.md)。超过 10 MB 的文件用[本机中转](../ship-my-game/references/uploads.md) `[实测]`。
2. 创建开发版本（网页抽屉第 2 步的「提交」，或 CLI 的 `submit-mini-app-package --yes`）之前，先告诉用户版本号和改了什么，用户同意再执行。被你的权限系统拦下时，停在那个按钮上，请用户点 `[实测]`。
3. 提交后会自动跑「包体准入测试」。用 CLI 建的开发版本一开始显示「测试异常」（提示请重新测试），在「包体管理」那一行点「重新测试」才会开始 `[实测]`。失败一般 10 分钟内出结果；能启动的版本还要跑满约 10 分钟的性能测试，等得更久。不要一直刷新，隔几分钟看一次那一行的「包体准入测试」列；失败时「消息中心」也会通知 `[实测]`。
4. 点「查看报告」：安卓 5 台，通过线 80%；iOS 那 1 台显示的「通过」只是占位，不代表游戏在 iOS 上能运行 `[实测]`。
5. 没通过：请用户同意后下载失败设备的日志，按 troubleshooting.md 排查，修好后换一个更高的版本号重新上传 `[实测]`。
6. 通过后点该版本的「自测」，把二维码发给用户，请他用最新版 TapTap 扫码，在真机上把游戏玩一遍 `[实测：二维码；真机结果本仓库未记录]`。

完成标准：
- 至少一个开发版本的「包体准入测试」显示通过（安卓至少 4/5）。
- 用户在真机上扫码玩过，并确认声音、中文、登录、存档都正常。
- 版本号和测试结果已记进进度档案。

### P4 隐私保护指引与平台能力（可与 P3、P5 并行）

1. 打开「小游戏管理 → 基础配置 → 隐私保护及权限设置 →「协议配置」」：
   - 按游戏实际调用的接口勾选信息类型。只用公开排行榜、不调 `getUserInfo` 时可以一项不勾。
   - 填联系方式和存储期限。
   - 用户确认后提交。

   逐项填法见 [console.md](references/console.md) 第 5 节 `[实测]`。
2. 要接成就时：在「游戏服务 → 运营工具 → 成就」里创建（至少 5 个才能发布），并在「测试」页签加入用户的 TapTap 用户 ID `[实测]`。
3. 要接排行榜时：在「游戏服务 → 运营工具 → 排行榜」里创建。新榜默认「仅白名单可见」，在「测试白名单」里加入用户 ID `[实测]`。
4. 代码接入，以及云存档、分享、添加到桌面、广告等能力，见 [capabilities.md](references/capabilities.md)。

完成标准：
- 隐私保护指引的状态是「审核中」或已通过。
- 接入的每个能力，都在真机上用测试名单里的账号验证过。
- 成就 ID、排行榜 ID 已写进代码和进度档案。

### P5 前置备案（第一个开发版本上传后马上开始）

1. 打开「小游戏管理 → 小游戏资质 → 小游戏前置备案」，点「提交核准信息」`[实测]`。
2. 你来做：
   - 选一个已上传的包体；
   - 按 `templates/game-content-intro.md` 生成《游戏内容介绍说明》docx 并上传；
   - 填「游戏简介」（一句话，建议 30 字以内）；
   - 把官方《互联网信息服务核准承诺书（个人）》模板做成待签字的 A4 文件，交给用户 `[实测]`。
3. 用户本人做：填负责人信息并上传证件照；打印承诺书，手写证件号、签字后拍照上传；完成电子化核验扫码。详见 [filing.md](references/filing.md) `[实测]` `[官方]`。
4. 用户确认后点「提交核准信息」[官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/pre-filing/)。
5. 进入等待：全程约 20 个工作日。初审通过后工信部会给负责人发短信，24 小时内没完成核验，申请会被退回 [官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/pre-filing/)。

完成标准：
- 备案状态是审核中。
- 进度档案的「等待中」写明开始日期、预计结束日期，并提醒用户留意短信。
- 最终在「查看核准信息」里能看到服务核准号。

### P6 商店资料

1. 打开「商店 → 版本管理 → 未发布版本 V-<日期>」，五个页签逐个填。表单会自动保存 `[实测]`。
2. 基础信息：游戏平台要同时勾「Android APK 下载、App Store」和「小游戏」（取消前者会把小游戏一起取消）；适龄分级要和游戏内的适龄标识一致 `[实测]`。
3. 游戏下载和获取：Android 选「开放试玩」，iOS 选「敬请期待」或「预约」。小游戏包体留到 P7 再选 `[实测]`。
4. 游戏资料：素材和文案按 [listing.md](references/listing.md) 准备。上传竖版实机录屏后，会多出一个必填项「宣传图（1:1）」`[实测]`。
5. 隐私说明：「小游戏隐私设置」要和隐私保护指引一致；「隐私政策链接」填一个 https 公网页面，内容和游戏内的隐私政策一致，发布前征得用户同意 `[实测]`。
6. 其他：如实选择「游戏内是否提供 AI 合成服务」`[实测]`。

完成标准：
- 除「选择小游戏包体」外，所有带 * 的字段都已填写，右下角显示「已保存」。
- 素材源文件都放在 `publish/taptap/` 里。

### P7 提审（提审闸门）

1. 按 [review.md](references/review.md) 第 1 节核对前提：
   - P3 有一个通过准入测试的版本；
   - P5 前置备案已通过（备案没通过时能不能提交未确认，以页面提示为准）[官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/pre-filing/)；
   - 接了成就的，先点「发布普通成就」[官方](https://developer.taptap.cn/docs/sdk/achievement/features/)；
   - 接了排行榜的，关掉「仅白名单可见」并清掉测试数据 [官方](https://developer.taptap.cn/docs/sdk/leaderboard/features/)。
2. 在「游戏下载和获取 → 请选择已上传的小游戏包体」里选通过准入测试的版本。页面原文：「若选择未过审包体，提交游戏资料后，将会自动提审对应包体」`[实测：页面原文]`。
3. 在「发布设置」里选「立即上线」或「定时上线」。新游戏第一次定时，时间要在当前时间 6 小时以后 [官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/creation-improvement/)。
4. 按[提审闸门](../ship-my-game/SKILL.md)把要提交的内容列给用户：
   - 包体版本号和准入测试结果；
   - Android 和 iOS 的游戏状态；
   - 商店文案要点；
   - 隐私设置和隐私政策链接；
   - 有没有广告、有没有 AI 合成服务；
   - 预计 1～3 天出结果。

   用户说「提交」后，点「下一步」→「提交审核」[官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/game-publish/version/)。也可以用 CLI 先预检再提交，见 automation.md。
5. 读页面，确认状态变成「审核中」。详见 [review.md](references/review.md)。

完成标准：
- 版本状态是「审核中」。
- 进度档案记下了提交时间、预计时长（1～3 天），以及查看结果的位置：「商店 → 资质与审核 → 版本审核记录」。

## 等待期与上线后

- **等准入测试（约 10 分钟）**：去做素材和文案。
- **等前置备案（约 20 个工作日）**：去做 P4 和 P6。
- **等审核**：需要改资料时可以「撤销审核」，改完重新提交。
- **审核失败**：在「版本审核记录」里看原因，改完再提交，不要原样重提。见 review.md。
- **上线后**：游戏以「开放试玩」对玩家可见。发新版本的顺序是：上传更高版本号的包体 → 通过准入测试 → 在「版本管理」新建版本 → 选包体 → 提审（更新一般 1 天内出结果）[官方](https://developer.taptap.cn/minigameapidoc/quick-start/guide/creation-improvement/)。
- **收款**：广告收入走 Dirichlet，个人能不能结算还没确认，接广告前先请用户问 Dirichlet 客服，见 [payouts.md](references/payouts.md)。
