---
name: ship-steam
description: Steam 发布（规划中：注册、收款和税务已实测，建应用之后还没走过）：把 Unity 游戏做成 Windows 版发到 Steam，从注册 Steamworks（Steam Direct）、签协议、付 100 美元注册费、填银行和 W-8BEN 税务信息，到建应用、商店页、上传构建、提审。用户要发布、上架、提审到 Steam；问 Steamworks 怎么注册、Steam 的钱怎么收、W-8BEN 怎么填、身份验证要传哪些证件；或者问在 Mac 上怎么给 Steam 打 Windows 包时使用。
---

# Steam：从注册 Steamworks 推到提审（规划中）

**状态**：本渠道在「规划中」，还没有真实走到「审核中」。

- `[实测]` 走过的：P1 账号、P2 收款、税务和身份验证（2026-11-03，中国大陆个人开发者，证件已上传，在等 Steam 审核）。P3 的打包脚本只在空工程上跑通过。
- 没走过的：P4 以后，只有提纲和官方链接。走到这些步骤时以后台页面为准，和这里不一样的地方记进进度档案的「与 skill 不符」。

**先做**：确认 [ship-my-game](../ship-my-game/SKILL.md) 的第 1～4 步已完成（进度档案、渠道、体检、浏览器），没完成就先读它。本渠道的进度写在进度档案的 `## steam` 一节。

**保密**：Steamworks 后台页面都标着 Valve 保密，《Steam 分销协议》的条款本身也是保密信息。后台上读到的内容可以讲给用户听，但不要抄进本仓库、进度档案或任何会公开的地方。本 skill 只写公开文档里的规则和操作经验。

**开工先问用户这三件事**，答案写进进度档案：
1. 用哪个 Steam 账号注册？新开的账号是「受限账户」，账号的商店国家由第一次购买时所在的位置决定，见 [onboarding.md](references/onboarding.md) 第 1 节。
2. 收款用哪个账户：国内银行（SWIFT 电汇），还是第三方平台的美国收款账户？**在 P1 填法定英文名称之前，先拿到这个账户认的英文户名**，Steam 里照它原样填。两边不一致，银行信息存不进去，姓和名的顺序不同也不行 `[实测-失败 → 已修复]`；名字填进 Steam 以后再改，Steam 这边要从头注册（税务问卷交了的，还得先请客服取消税务问卷和身份验证），收款平台那边要截图审核补登记，都慢。Payoneer 认哪些名字、在哪看，见 [onboarding.md](references/onboarding.md) 第 2 节。
3. 拿哪个游戏上 Steam？游戏里有没有广告？Steam 不接受以广告为商业模式的应用 [官方](https://partner.steamgames.com/doc/gettingstarted/onboarding)。

**然后告诉用户时间线**：

| 事项 | 时长 | 依据 |
|---|---|---|
| 银行、税务、身份审核 | 15～30 天；实测提交税务信息后，后台提示最长约 30 个工作日 | [官方](https://partner.steamgames.com/steamdirect)；`[实测]` |
| 交注册费到可以发售 | 21 天。Steam Direct 页面以前写 30 天，2026-11 改成了和入门文档一样的 21 天 | [Steam Direct](https://partner.steamgames.com/steamdirect)、[入门文档](https://partner.steamgames.com/doc/gettingstarted/onboarding)（2026-11-09 读取） |
| 「即将推出」页面公开 | 至少 2 周才能发售 | [官方](https://partner.steamgames.com/doc/store/coming_soon) |
| 商店页审核 | 一般 3～5 个工作日，建议在想上线的日子前至少 7 天提交 | [官方](https://partner.steamgames.com/doc/store/releasing) |
| 构建审核 | 1～5 天 | [官方](https://partner.steamgames.com/steamdirect) |

## 本人事项

| 事项 | 阶段 |
|---|---|
| 建 Steam 账号；登录 Steam 和 Steamworks（密码、Steam 令牌扫码） | P1 |
| 签保密协议和《Steam 分销协议》：你先用三五句话讲要点，用户自己勾选、输验证码 | P1 |
| 付 100 美元注册费 | P1 |
| 填银行账号和外国税号；签 W-8BEN；拍证件照片和手持证件的自拍并上传 | P2 |
| 在第三方收款平台补登记户名写法（需要时） | P2 |
| 提交商店页和构建审核、点发行：用户说「提交」后由你点，被权限系统拦下时由用户点 | P4～P6 |

## 工程要求

ship-my-game 第 3 步按这张表列差距。细节见 [references/build.md](references/build.md)。

| 项 | 要求 | 依据 |
|---|---|---|
| 平台 | Windows 64 位 | — |
| 脚本后端 | 在 Mac 上只能用 Mono：Unity 不支持从 macOS 交叉编译 Windows 版 IL2CPP，Mac 版 Hub 也只提供「Windows Build Support (Mono)」模块。要 IL2CPP 就得在 Windows 上打 | [官方](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/scripting-backends/il2cpp/il2cpp-introduction)；`[实测]` |
| 模块 | Windows Build Support (Mono)，装法见 build.md 第 2 节 | `[实测：6000.6.5f1]` |
| 场景列表 | Build Settings 的场景列表不能为空；`scripts/ShipSteamBuild.cs` 遇到空列表直接报错 | `[实测-失败 → 已修复]` |
| 广告 | Steam 版去掉广告 SDK 和广告入口 | [官方](https://partner.steamgames.com/doc/gettingstarted/onboarding) |
| Steamworks SDK | 成就、云存档等能力未实测 | — |

## 阶段

命令和链接里的相对路径（`scripts/…`、`../ship-my-game/…`）都以本 skill 目录为起点。

### P1 账号：Steamworks 合作伙伴、两份协议、注册费 `[实测]`

1. 按 [onboarding.md](references/onboarding.md) 第 1 节准备 Steam 账号和网络。**建号和付注册费时都不要开代理**，否则账号的商店国家会被定成别的国家。
2. 拿到收款账户认的英文户名（开工第 2 问），定下法定英文名称的写法：和户名一字不差，姓和名的顺序、空格都一样。见 onboarding.md 第 2 节。
3. 打开 https://partner.steamgames.com/ ，请用户登录（手机 Steam App 扫码最快）。点「加入 Steamworks」，按 onboarding.md 第 2 节填法定英文名称、公司形式、当前地址，然后签保密协议。
4. 回到主面板，从「添加功能」进入「游戏或软件销售」的注册：签《Steam 分销协议》，再付注册费。见 onboarding.md 第 3 节。

完成标准：
- 公司信息页的法定名称和收款账户认的某个户名一字不差。
- 公司信息页的「已签署协议」里有保密协议和软件分销协议两条。
- 注册费已付，付费日期写进了进度档案（21 天的发售等待从这天算）。
- 账号的商店国家和用户实际居住的国家一致。

### P2 收款、税务和身份验证 `[实测：证件已上传，等审核]`

1. 银行信息：先选银行账户所在国家，表单字段会跟着变。收款人英文名必须和法定英文名称一字不差。见 [payouts.md](references/payouts.md) 第 2、3 节。
2. 税务问卷（第三方 Tax Identity，生成 W-8BEN）：邮箱必须填 Steam 账号绑定的邮箱；外国税号填 18 位身份证号。逐页见 payouts.md 第 4 节。
3. 身份证件：提交税务信息后，主面板会出现上传证件的待办（实测当天就出现）。把请求页的要求逐条读给用户；证件照片和手持证件的自拍一次传齐，30 天内传完。见 payouts.md 第 5 节。

完成标准：
- 银行信息已保存，税务信息已提交，证件照片和自拍已上传，并且收到了上传确认。
- 进度档案的「等待中」写了证件上传日期、预计结束日期（最长约 30 个工作日），以及去 Steamworks 主面板看结果。
- 用第三方收款平台时：Steam 的法定英文名称在平台认的户名列表里（Payoneer 在美元账户详情的「其他收款人名称」里看）。

### P3 Windows 构建 `[实测：空工程]`

1. 装 Windows Build Support (Mono) 模块，见 [build.md](references/build.md) 第 2 节。
2. 把 `scripts/ShipSteamBuild.cs` 复制到游戏的 `Assets/Editor/`，然后构建：
   ```bash
   ../ship-my-game/scripts/unity_build.sh <工程目录> Win64 ShipSteamBuild.Win64 steam-win64 -shipVersion 1.0.0
   ```
3. 自检：日志里有 `[ShipSteam] Succeeded`；`file Builds/Steam/Windows/<产品名>.exe` 显示 `PE32+ executable (GUI) x86-64`；同一目录下有 `MonoBleedingEdge`。
4. Steam 版去掉广告。Mac 上没法运行 Windows 包：有 Windows 电脑时请用户实际玩一遍，这一步本仓库还没实测。

完成标准：有一个 64 位 Windows 包；进度档案记下了版本号、包体大小和是否在 Windows 上跑过。

### P4 建应用和商店页（未实测）

- 主面板的「创建新应用」会用掉注册费换来的额度，先建好应用。
- 填商店页、上传图形素材、设价格，提交商店页审核。通过后以「即将推出」公开，至少 2 周后才能发售。
- 依据：[即将推出](https://partner.steamgames.com/doc/store/coming_soon)、[商店图形素材](https://partner.steamgames.com/doc/store/assets)、[发行流程](https://partner.steamgames.com/doc/store/releasing)。

完成标准：商店页进入审核。这是本渠道第一个「审核中」，走到这里后，按 MAINTAINING.md 考虑把 Steam 列进 README 的「已收录」。

### P5 上传构建（未实测）

- 用 SteamPipe 把 P3 的构建上传到应用，再提交构建审核。
- 依据：[上传到 Steam](https://partner.steamgames.com/doc/sdk/uploading)、[审核流程](https://partner.steamgames.com/doc/store/review_process)。

完成标准：构建进入审核。

### P6 发售（未实测）

- 商店页和构建都通过审核、「即将推出」满 2 周、交费满 21 天之后，按[提审闸门](../ship-my-game/SKILL.md)把要发售的内容列给用户；用户说「发售」后再点。
- 依据：[发行流程](https://partner.steamgames.com/doc/store/releasing)。

## 等待期

- **等 Steam 审核账号**（最长约 30 个工作日）：不要重传证件，也不要重做税务问卷，否则会排到队尾。这段时间做 Steam 版构建（去广告、改成适合 PC 的操作），准备商店素材和文案。实测审核期间，主面板上已经能创建新应用 `[实测]`。
- **等第三方平台审核户名**（实测第二次提交当天通过）：通过后到美元账户详情的「其他收款人名称」里确认新写法在列表里，见 payouts.md 第 3 节。
- **收款**：Valve 每月付上个月的收入，默认攒到 100 美元才付，只付美元，见 payouts.md 第 1 节。钱进了国内以后的结汇和个税，见 [payouts-china.md](../ship-my-game/references/payouts-china.md)。
