---
name: zcode-local-patch-routing
description: 为本仓库的 ZCode local-only 补丁新增发行包适配档案、维护注入锚点或扩展 setup 自动路由时使用。不用于仅安装已有补丁、日常宿主故障排查、普通插件开发或单纯查询上游版本。
---

# 编写 ZCode 补丁适配档案

交付是仓库内的**适配档案（profile）与注册项**。setup 按实际发行包身份选档案，在用户机器现场生成补丁候选；不以完整 ZCode 宿主或独立 app.asar ZIP 作为默认交付。

本技能用于维护适配实现，不自动授权应用到日常宿主、推送、合并或发布。操作范围遵循当前用户指令及仓库 AGENTS.md。

## 入口与按需阅读

下列代码路径均相对仓库根；命令也从仓库根执行。

| 任务 | 入口 |
| --- | --- |
| 确认路由和状态契约 | [自动路由规格](../../../suian-zcode-app-mcp/docs/local-only-routing-spec.md)、`suian-zcode-common/local-only/profiles.mjs` |
| 编写逐包注入 | `suian-zcode-common/local-only/profiles/`；选最接近的已有档案作参考 |
| 读取、重写与核对 asar | `suian-zcode-common/local-only/patch.mjs` 的 `extractAsarFile`、`readFusesFromExe`、四个补丁命令 |
| 核对 setup 与分发 | `suian-zcode-common/setup.ps1`、`suian-zcode-common/build-release.mjs` |
| 学习实际版本迁移 | [3.16.3 档案记录](../../../suian-zcode-app-mcp/docs/local-only/11-windows-3.16.3-candidate.md)，仅作该包的历史证据 |
| 启动或排查原生验证 | [隔离调试技能](../debug-isolated-zcode/SKILL.md)；进入运行验证阶段再读 |

规格中的历史支持清单、旧包摘要与旧记录的“当前版本”不代表最新注册表；用现有代码和对应发行包证据确认本次基线。

## 1. 固定实际发行包

在独立开发工作树记录本次基线。先确认用户要新增发行包、修复已有档案，还是仅应用已支持补丁，避免把安装任务变成开发。

拿到目标平台的**原版运行包**：可以下载解压，也可读取已升级的本机安装。无需先升级日常宿主；只更新上游源码不足以生成正式包补丁，因为注入针对编译产物的精确字节。

- 记录平台、exe 完整 FileVersion、原版 `resources/app.asar` 的 SHA-256 与字节数。
- 先检查是否已有补丁状态或备份；已 patch 的当前摘要不能登记成原版摘要。只有与该包身份一致、摘要核对通过的原版备份可作为来源。
- 确认 asar 实际加载入口，现有 Windows 档案为 `out/main/index.js`；提取该文件到忽略的 `.scratch/{{task}}/`。
- 用 `readFusesFromExe` 核对 Electron 的 asar 完整性开关；若无法确认或校验开启使替换不可行，报告阻断，不绕过检查或修改 exe。
- 上游源码用于解释语义；`sources/` 只读，不为本任务修改或安装其依赖。

**完成判据**：能指出本次原包的精确身份、入口和来源，明确它是否已修改；尚未生成或覆盖用户补丁。

## 2. 逐处重建锚点与变量映射

**锚点**是原版编译产物中用于精确定位替换位置的字符串。先在新主入口定位下列语义，再确定对应的压缩变量和替换内容；不能按旧包变量名全局替换后直接登记。

| 注入点 | 需要确认的新包语义 |
| --- | --- |
| P0 文件导入 | 文件首部加入读取开关文件所需的命名导入；不与已有模块绑定冲突 |
| P1 模式与地址 | relay WS 覆盖变量、完整语句边界、开关与工作区来源、最终 URL 回环校验、本地 token 生成 |
| P2 登录短路 | manager 的 `getLogin` 回调；开关关闭时仍执行原路径 |
| P3 设备标识短路 | `resolveDeviceSid` 回调、注册结果变量与当前会话映射 |
| P4 token 短路 | V2 `getToken` 回调及 HTTP 取令牌路径 |
| P5 账号事件隔离 | `notifyAuthStateChanged` 的参数与 signed-out 撤销分支 |
| P6 自动启动 | manager 引用挂接后的顶层语句边界、manager 变量、排除 CUA 指示窗的窗口列表函数 |

逐一读取命中附近的代码，核对闭包与赋值关系。每个替换锚点必须恰好命中一次；零次或多次时继续分析，不放宽为模糊匹配。新增顶层声明要检查与原包绑定的冲突；注入语句不能落入 var 或逗号表达式中间。

3.16.2 → 3.16.3 的例子：WS 变量由 `sA` 变为 `cA`，manager 由 `li` 变为 `pi`，窗口函数由 `Le` 变为 `Oe`。这些名字仅属于相应字节身份，不能成为以后版本的通用映射。

**完成判据**：每个替换点都有唯一命中和可解释的语义，注入体、锚点、切片前缀及说明中的变量名一致。

## 3. 先写预期，再追加档案

先增加本次行为的契约测试，并确认它因缺少新档案或目标缺陷而失败。测试至少验证精确身份选档案、旧档案保留，以及本次改变的运行体行为；已有测试覆盖的跨包拒绝等契约直接复用。

随后在 `suian-zcode-common/local-only/profiles/` 新增独立模块，核对：

- `SUPPORTED_PACKAGE`：真实包身份；未核实的可选运行时版本不猜测填写。
- `MAIN_ENTRY`：新包实际入口。
- `PATCH_VERSION`：新档案从 1 开始；修复同一档案的注入或锚点时递增该档案修订号。
- `applyInjections`：保留唯一命中、拒绝重复注入的行为，失败不写半成品。

在 `profiles.mjs` 追加稳定档案 ID 和注册项。现有 ID 使用平台、完整 exe 版本和原包摘要前缀；路由实际比较完整摘要。保留旧档案及其修订号，不以版本范围、列表顺序或“最新档案”兜底。现有旧包测试夹具引用 `PATCH_PROFILES[0]`，新增项应追加，避免改变夹具含义。

应用版本、每包补丁修订号、候选/状态格式版本是三个概念，不相互比较。不要把 `patch-env.mjs` 的旧包兼容导出改成新包全局版本源；生产补丁 CLI 不接受 `--package-identity` 绕过注册表。

**完成判据**：新测试由红转绿，新旧身份各自选中正确档案；未改动旧包的注入字节和状态契约。

## 4. 核对 setup 与发布目录

正常新增档案无需在 setup 写版本分支。确认现有链路仍是 `status → prepare → 生成外部应用/还原命令`，setup 本身不执行 apply、不强退宿主；应用必须在目标实例退出后执行。

构建已递归收集 `local-only/profiles/`，仍需核对发布目录实际包含注册表和全部新旧档案。用发布目录中的补丁 CLI 对目标运行包执行只读 status，确认能独立导入并返回正确 `profileId`，不能只证明源码可运行。

```powershell
node suian-zcode-common/build-release.mjs --out ".scratch/{{task}}/common-release"
node ".scratch/{{task}}/common-release/local-only/patch.mjs" status --target "{{install_dir}}"
```

以上构建等耗时命令执行时按仓库约定重定向到日志并记录退出码。没有加载布局或公共协议变化时，不扩展 setup、网关或业务插件。

**完成判据**：setup 契约可复用，发布目录可独立路由新包并继续管理旧包；未额外交付完整宿主。

## 5. 分层验证，分别报告结论

按改动范围复用已有记录，优先执行新档案测试及以下相关测试，不因准备发布或合并再次重复全量：

| 变更或证据 | 核对内容 |
| --- | --- |
| 档案与路由 | `local-only-routing.test.mjs`、`local-only-patch.test.mjs`、`local-only-lifecycle.test.mjs` 及本次档案测试，均在 common `tests/` |
| setup 与分发 | common `tests/setup.test.mjs` 中相关 local-only 用例、`tests/release-build.test.mjs`；按实际影响选取 |
| 真实候选 | prepare 成功、每点唯一命中、提取候选入口后 `node --check` 通过；同输入补丁输出确定 |
| 实际包副本 | apply → status → restore，恢复摘要与本次原包一致；未替换文件及 unpacked 资源保持原样 |
| 旧包兼容 | 识别、历史状态/候选、同包修订升级与还原仍通过；旧档案未修改时复用有效字节证据 |
| 原生运行 | 新包无登录冷启动、官方远控不可达、网关重启恢复和 MCP 闭环；开关关闭时保留官方流程 |

原生验证使用隔离包、独立数据根与专用网关。当前 lab 默认身份仍引用旧包；新包用 `setupLab`/`checkLab` 的 `packageIdentity` 显式传入已核实身份，或按 lab 现有 CLI 能力操作。lab 的身份参数不等于生产补丁 CLI 的支持清单，不能混用。

运行细节转到[隔离调试技能](../debug-isolated-zcode/SKILL.md)。同用户运行副本仍可能改写 Windows 协议或菜单注册，按该技能备份、核对恢复。

**完成判据**：逐项报告已通过、失败及未执行的验证。路由命中、prepare 成功、语法检查、模拟测试或副本还原，均不能替代原生运行验收；未完成时明确称为适配候选，不宣称新版完整兼容。

## 6. 收尾与交付

- 在 `suian-zcode-app-mcp/docs/local-only/` 留脱敏证据：原包身份、档案 ID/修订号、注入位置与语义、候选摘要、基线/提交、检查范围、日志位置及未验项目。原包、候选字节、凭据与用户路径不入库。
- 默认交付仅包括档案、注册项、必要测试与证据；setup 现场准备候选，不生成供用户下载的完整宿主 ZIP。
- 用户要求升版或发布时，再按根 AGENTS.md 与发布约定核对受影响插件版本、市场条目、插件 ZIP 与摘要；本技能不固定版本号、标签、Release 状态，也不自动扩大发布范围。
- 清理本轮临时包副本与无用交付物，保留可复核日志和必要发布凭证；不清理其他会话的工作树或文件。

**最终完成判据**：另一位 Agent 能从仓库定位档案、通过统一 CLI 选中目标包，并从记录判断具体通过了哪些验证、还有哪些运行验收未完成。
