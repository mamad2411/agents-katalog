---
name: ship-google-play
description: Google Play 发布：把 Unity 游戏打成签名 AAB，从注册 Play 开发者账号、创建应用、填应用内容和商品详情、封闭测试送审、凑满 12 名测试者连续 14 天，一直推进到申请正式版并提审。用户要发布、上架、提审到 Google Play；要接 Play 游戏服务（登录、成就、排行榜、云存档）、AdMob 广告、应用内评价或更新、内购；Play 审核被拒、送审被拦、测试人数不够；或者问 AdMob、Play 的钱怎么收（PIN 码、银行账户、税务信息）时使用。
---

# Google Play：从注册开发者账号推到提审

目标：先把**封闭测试**版本推到「审核中」（实测当天就能过审），再按个人账号的测试要求凑满测试者，最后把**正式版**推到「审核中」。

**先做**：确认 [ship-my-game](../ship-my-game/SKILL.md) 的第 1～4 步已完成（进度档案、渠道、体检、浏览器），没完成就先读它。本渠道的进度写在进度档案的 `## google-play` 一节。

**开工先问用户这五件事**，答案写进进度档案 `[实测：问诊清单]`：
1. 有没有 Play 开发者账号？个人还是组织？大概什么时候注册的？
2. 人在哪个国家或地区？这决定商家账号能不能收款 [官方](https://support.google.com/googleplay/android-developer/answer/9306917)。
3. 打算怎么赚钱：广告、内购、付费下载，还是不赚钱？这会影响公开哪些个人信息，以及交易者身份怎么声明。
4. 隐私政策放在哪个公开 https 网址？商店上公开的联系邮箱用哪个？
5. 有没有 AdMob 账号？建议和 Play 开发者账号用同一个 Google 账号。

**然后告诉用户三件事**：
1. **测试门槛**：2023-11-13 之后注册的个人账号，正式上线前要有至少 12 名真人测试者**连续** 14 天参加封闭测试，然后申请正式版（审核通常 7 天内）[官方](https://support.google.com/googleplay/android-developer/answer/14151465?hl=zh-Hans)。所以从封闭测试过审到正式上线，最少要两周多。
2. **会公开的信息**：
   - 个人账号会公开法定全名、国家、开发者邮箱；
   - 开始在 Google Play 上创收（付费应用、内购）后，会公开完整地址；
   - 声明为「交易者」的个人账号还会公开电话和地址。
   
   注册前按 [onboarding.md](references/onboarding.md) 第 1 节讲清楚。
3. **AAB 上传**：AAB 通常几十 MB，浏览器工具单次只能传 10 MB，所以首个 AAB 要用户拖进网页。之后可以走 Developer API（本仓库未实测），见 [automation.md](references/automation.md)。

## 本人事项

| 事项 | 阶段 |
|---|---|
| 注册：付 US$25、身份证件、邮箱和电话验证码、Android 实体设备验证（用 Play 管理中心移动应用扫码）、交易者身份声明 | P1 |
| 勾选同意：《开发者分发协议》；创建应用时的「开发者计划政策」「美国出口法律」声明；IARC 使用条款；PGS 和 Google Cloud 的条款（点「使用」时）；《Google API 服务：用户数据政策》 | P1、P3、P6 |
| 把 AAB 拖进网页的上传框 | P4，之后每次更新（不走 API 时） |
| 「提交 N 项更改以供审核」：用户说「提交」后由你点；被权限系统拦下时由用户点 | P4、P7 |
| 创建 Google 群组时的人机验证；在 Reddit 等社区发帖、互测；用自己的账号加入测试 | P5 |
| 在真机上确认声音、PGS 登录和整体手感 | P2、P6 |
| OAuth 同意屏幕的「发布应用」、PGS 的「发布游戏项目」 | P6 |
| 注册 AdMob：国家、条款、人机验证、付款和税务资料 | P6 |
| 同意把隐私政策、app-ads.txt 发布到用户的网站；托管需要付费时由用户决定 | P2、P6 |
| 收款：AdMob 的身份证件、PIN 码、收款方式、美国税务信息；Play 的商家付款资料和银行账户 | 上线后 |

## 工程要求

ship-my-game 第 3 步按这张表列差距。细节见 [references/build.md](references/build.md)。

| 项 | 要求 | 依据 |
|---|---|---|
| Unity | 目标 API 36 需要 6000.0.46f1+ 或 2022.3.62f1+；16 KB 页需要 6000.0.38f1+ 或 2022.3.56f1+，Burst 1.8.21+。实测用 6000.6.5f1 | [官方](https://docs.unity3d.com/6000.0/Documentation/Manual/android-requirements-and-compatibility.html)；`[实测]` |
| 模块 | Android Build Support（含 OpenJDK、SDK、NDK） | — |
| targetSdk | 36（2026-08-31 起；延期的截止日 2026-11-01 已过）。minSdk 不低于 24，实测 26 | [官方](https://support.google.com/googleplay/android-developer/answer/11926878)；`[实测]` |
| 架构和格式 | IL2CPP、ARM64 + ARMv7、AAB；符号表打进 AAB | `[实测]`，由 `scripts/ShipAndroidBuild.cs` 设置 |
| 16 KB 内存页 | 含原生库（Unity 都含）的包必须 16 KB 对齐，构建后检查 | [官方](https://developer.android.com/guide/practices/page-sizes) |
| 签名 | 上传密钥由 `scripts/make_upload_keystore.sh` 生成，放在工程外；应用签名密钥由 Google 托管 | `[实测]` |
| 声音 | 每个会启动的场景有且只有一个 `AudioListener` | `[实测-失败]` 两款游戏都因此无声上线过 |
| 广告 | 封闭测试期一律用 Google 测试广告 ID，拿不到广告时隐藏入口 | `[实测]` |
| 内购 | Unity IAP ≥ 4.14.0 或 5.x（Play 结算库 ≥ 8） | [官方](https://developer.android.com/google/play/billing/deprecation-faq) |
| 隐私政策 | 公开 https 网页，Play 后台和游戏里都放链接；模板 `templates/privacy-policy.en.html` | [官方](https://support.google.com/googleplay/android-developer/answer/9859455)；`[实测]` |
| 敏感权限 | 合并后的清单里不要有用不到的照片、视频、通讯录、位置等权限 | [官方](https://support.google.com/googleplay/android-developer/answer/14115180) |

## 阶段

命令和链接里的相对路径（`scripts/…`、`../ship-my-game/…`）都以本 skill 目录为起点。后台路径用 Play 管理中心中文界面的原文。

### P1 账号（已有就跳到完成标准逐项核对）

1. 打开 https://play.google.com/console ，读页面判断有没有开发者账号、是个人还是组织。
2. 没有账号时：先讲 [onboarding.md](references/onboarding.md) 第 1 节「会公开哪些信息」，用户同意后带他注册。付费、证件、验证码、设备验证都由用户做 [官方](https://support.google.com/googleplay/android-developer/answer/6112435)。
3. 交易者身份：新账号创建时就要声明（「管理账号 → 账号详情 → 关于您」），已有账号最晚 2027-02-01。由用户如实决定，你讲清判断标准和后果 [官方](https://support.google.com/googleplay/android-developer/answer/17594752?hl=zh-Hans)。
4. 在「首页」清掉验证类待办，并确认「Android 开发者验证」状态（新应用创建时会自动登记包名）[官方](https://developer.android.com/developer-verification/guides/google-play-console)。

完成标准：
- 首页没有待完成的验证任务。
- 进度档案写明账号类型、注册时间（判断是否适用 12 人 × 14 天）、交易者身份。

### P2 工程、上传密钥、首个 AAB

1. 按「工程要求」改工程：把 `scripts/ShipAndroidBuild.cs` 复制到 `Assets/Editor/`，检查每个场景的 AudioListener。
2. 生成上传密钥：`bash scripts/make_upload_keystore.sh <包名>`，然后提醒用户备份 `~/.shipmygame/keys/<包名>/` `[实测]`。
3. 构建：`../ship-my-game/scripts/unity_build.sh <工程目录> Android ShipAndroidBuild.Aab release -shipVersion 1.0.0 -shipVersionCode 1`。
   - `[实测]`：本脚本在空工程上构建出过调试 APK；同样配置的构建脚本在两款游戏上产出过签名 AAB。
4. 自检：用 bundletool 看清单（targetSdk 36、测试广告 App ID），确认符号已打进 AAB，检查 16 KB 对齐。命令见 build.md 第 4 节。
5. 用 `ShipAndroidBuild.Apk` 打一个调试 APK，请用户装到手机上，确认有声音 `[实测：模拟器测不出声音]`。
6. 按 `templates/privacy-policy.en.html` 生成隐私政策：替换全部 `{{占位符}}`，删掉游戏用不到的 AdMob、PGS、内购段落。用户同意后发布到公开 https 网址，用 `curl` 确认返回 200 `[实测]`。

完成标准：
- 有一个签名 AAB，versionCode 和自检结果都记进了进度档案。
- 用户在真机上确认过有声音。
- 隐私政策网址返回 200。

### P3 创建应用、应用内容、商店资料

1. 「首页 → 创建应用」：填名称、包名（先点「检查可用性」）、默认语言、游戏、免费或付费；两项声明由用户勾选。逐字段见 [console.md](references/console.md) 第 1 节 `[实测]`。
2. 信息中心「完成游戏设置」的 11 项逐项填完：隐私权政策、登录详细信息、广告、内容分级、目标受众群体、数据安全、政府应用、金融产品和服务、健康、类别和联系信息、商品详情。答案见 console.md 第 2 节 `[实测]`。
3. 「监控和改进 → 政策和计划 → 应用内容」：把所有「开始声明」清零，**尤其是「广告 ID」**。它不在 11 项里，不填送审会被拦 `[实测-失败 → 已修复]`。
4. 「商店发布 → 商店设置」：类别、最多 5 个标签、联系信息（网站要用 app-ads.txt 所在的域名）`[实测]`。
5. 「商店发布 → 商品详情」：文字、图标、置顶大图、截图、AI 资源声明。多语言用「使用 AI 导入译文」，导入后逐语种核对。见 [listing.md](references/listing.md) `[实测]`。

完成标准：
- 信息中心的「完成游戏设置」整块消失。
- 「应用内容」没有待处理项。
- 商品详情状态是「可以送审」，素材源文件都在 `publish/google-play/`。

### P4 封闭测试首发（提审闸门）

1. 「测试和发布 → 测试 → 封闭式测试」（默认轨道「封闭式测试 - Alpha」）：
   - 国家/地区选「全选」；
   - 测试人员选 Google 群组（推荐）或邮件列表，二者只能选一种；
   - 填反馈邮箱。
   
   见 console.md 第 5 节 `[实测]`。
2. 「创建新的发布版本」：先填版本名称和多语言版本说明，点「保存为草稿」。再请用户把 AAB 拖进上传框，你轮询页面，等出现「1 (1.0.0)」这样的条目 `[实测]`。
3. 「下一步」→ 读「展开验证详情」→「保存」→「发布概览」，等快速检查跑完（最多约 14 分钟），报问题先修 `[实测]`。
4. 按[提审闸门](../ship-my-game/SKILL.md)把内容列给用户。用户说「提交」后点「提交 N 项更改以供审核」→「将更改内容送审」；被权限系统拦下就请用户点。详见 [review.md](references/review.md) 第 1 节 `[实测]`。

完成标准：
- 发布概览显示「正在审核中的更改」。
- 进度档案记下了提交时间和预计时长（实测 10～42 分钟，官方说通常 7 天内），以及去「发布概览」看结果。

### P5 招募测试者，等满 14 天（个人账号；可与 P6 并行）

1. 过审后到「测试人员」标签页，从复制按钮的 aria-label 里取两个加入链接 `[实测]`。
2. 用 `templates/testers-recruitment.md` 写招募文案。建 Google 群组时最后的人机验证由用户过；社区帖子由用户发 `[实测]`。见 review.md 第 2 节。
3. 每天读信息中心「申请正式版发布权限」卡片：「目前有 N 名测试人员已持续参与 M 天」`[实测：卡片原文]`。
4. 根据反馈发更新：versionCode 加 1，走 P4 的第 2～4 步，或用 [automation.md](references/automation.md) 的 API。改动攒齐一次提交，因为重新送审会取消正在进行的审核 `[实测]`。
5. 把「监控和改进 → 评分和评价 → 测试反馈」里的反馈和对应的修复记进进度档案，留给 P7 的问卷用 [官方](https://support.google.com/googleplay/android-developer/answer/14151465?hl=zh-Hans)。

完成标准：卡片上「至少 12 名测试人员」「至少 14 天」两项都打勾；进度档案里有反馈和修复记录。

### P6 平台能力（与 P5 并行）

1. Play 游戏服务：
   - 后台：配置、OAuth 同意屏幕、凭据（**所有签名证书的 SHA-1 都要建**）、成就（至少 10 个）、排行榜、测试人员；
   - Unity：`scripts/ShipPgsSetup.cs` 和 `scripts/ShipPlayGames.cs`；
   - 「发布应用」和「发布游戏项目」由用户点。
   
   见 [capabilities.md](references/capabilities.md) 第 1 节 `[实测：后台配置]`。
2. AdMob：
   - 建应用和广告单元，`scripts/ShipAds.cs`（UMP 同意 → 初始化 → 激励、插屏、横幅）；
   - 发布 GDPR 消息，准备 app-ads.txt；
   - 测试期用测试 ID，正式上线后再关联商店。
   
   见 capabilities.md 第 2 节 `[实测：后台配置]`。
3. 应用内评价、应用内更新：`scripts/ShipPlayReview.cs`；内购：Unity IAP。见 capabilities.md 第 3、4 节 [官方]。
4. 每接一项，都同步更新数据安全申报和隐私政策，跟下一个版本一起送审（P4 第 2～4 步）`[实测]`。

完成标准：
- 接入的每个能力都由用户在真机上、从测试轨道安装后验证过。
- PGS 配置已发布；数据安全申报和隐私政策已经和功能一致。
- 正式广告 ID 只记在进度档案里，没有放进测试包。

### P7 申请正式版并发布正式版（提审闸门）

1. 卡片上三项都打勾后，先到模板列出的页面查测试数据，再按 `templates/production-access-answers.md` 起草三部分问卷（共 9 题，每道文字题最多 300 个字符），交给用户逐条确认 `[实测]`。
2. 按提审闸门列给用户：问卷答案、测试人数和天数、预计 7 天内出结果。用户说「提交」后，在「信息中心 → 申请正式版发布权限」点「申请发布正式版」，前两步点「下一步」，最后一步点「应用」。页面出现「我们已收到您的正式版发布权限申请」才算交上 `[实测]`。进度档案记下提交时间，结果看邮件和信息中心卡片。
3. 获批后（邮件通知账号所有者），按 [review.md](references/review.md) 第 6 节准备正式版：
   - 换上正式广告 ID 和 App ID，versionCode 加 1（可以在等结果时先打好包，这个包只发正式版）；
   - 先发布 PGS 配置，至少 2 小时后再上线游戏；
   - 「测试和发布 → 正式版 →『创建新的发布版本』」。
4. 再走一次提审闸门，把正式版送审，读页面确认进入「审核中」。

完成标准：
- 发布概览里，正式版那一项显示在「正在审核中的更改」下。
- 进度档案记下了提交时间、预计时长和查看位置（发布概览、邮件）。

## 等待期与上线后

- **等封闭测试审核**（实测几十分钟）：去做商店素材、PGS 和 AdMob 的后台配置。
- **等 14 天**：每天看卡片上的人数和天数；按反馈发 1～2 个更新；能力接入放在这段时间做。
- **等正式版权限审核**（约 7 天）：打好正式广告包并核对清单（review.md 第 6 节）；准备商店推广素材。
- **上线后**：在 AdMob 关联商店并完成 app-ads.txt 验证（capabilities.md 第 2.7 节）；封闭测试的测试人员也会收到正式版和真实广告，暂停测试轨道挡不住（review.md 第 6 节）；在 Android vitals 里盯崩溃率和 ANR。2027-02 起会考核内存，DEX 超过 50 MB 的游戏还要做代码优化（[官方](https://support.google.com/googleplay/android-developer/answer/17492799)）。每次更新都加 versionCode，改动攒齐一次送审。
- **收款**：AdMob 余额满 10 美元要验证身份和地址（PIN 码平邮，约 3 周），满 100 美元后每月 21 日前后付款；卖内购要先建商家付款资料、加银行账户，每月 15 日起付上月的收入。见 [payouts.md](references/payouts.md)。
- **被拒或被拦**：见 [review.md](references/review.md) 第 4 节和 [troubleshooting.md](references/troubleshooting.md)。
