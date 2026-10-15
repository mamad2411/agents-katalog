---
name: kindle-weread-setup
description: Identify a Kindle model, firmware, computer platform, and connection mode; verify a currently supported jailbreak route; then guide backup, KOReader, and the third-party WeRead plugin through explicit safety gates. Use for Kindle 微信读书、Kindle 越狱、KOReader 安装、型号固件判断、Mac/Windows/Linux 连接或安装失败排查；不要用于 DRM 移除或批量获取书籍内容。
---

# Kindle 微信读书安装向导

把任务当成有门禁的设备维护流程。不得从“Kindle Paperwhite”或一张外观照片直接推断路线。先完成问诊，再查当日来源；一次只推进一个阶段，每阶段都要有可观察的成功标志。

## 第一轮必须先问诊

在任何下载、复制、联网或设备操作前，读取 `references/intake-and-routing.md`，一次性收集：

- Kindle 市场名称/代际；不确定时收集序列号前缀，最多前 6 位
- 固件完整版本
- 电脑系统与版本：macOS / Windows / Linux
- 连接方式：磁盘挂载、MTP、仅充电或尚未连接；若已挂载，记录明确路径/盘符
- 电量、飞行模式、Amazon 注册状态
- 剩余空间和重要书籍/批注是否已有独立备份

缺少型号或序列号前缀、固件、电脑系统中的任一项时，先指导用户打开“设备信息”页，不进入安装。照片公开前遮挡完整序列号、MAC、账号名、二维码和验证码。

## 维护状态卡

在对话中持续维护，不把个人状态默认写回 Skill：

- 设备档案：型号/代际、序列号前缀、固件
- 主机档案：系统、连接模式、路径/盘符
- 当前阶段：问诊 / 路由 / 备份 / 防更新 / 越狱 / KOReader / WeRead / 验收
- 证据：用户提供 / 来源已核对 / 文件已校验 / 真机通过 / 失败 / 待验证
- 安全状态：电量、飞行模式、更新残留、备份、是否允许当前写入

不要显示或保存完整序列号、MAC、API Key、Cookie、二维码登录结果或四位验证码。

## 当日来源与路由门禁

进入越狱、KOReader 或插件阶段前都要联网重查，不只依赖本 Skill：

1. 型号与固件：`https://kindlemodding.org/kindle-models`
2. 越狱入口/向导：`https://kindlemodding.org/jailbreaking/`
3. 具体越狱项目的原始仓库与 Release
4. KOReader Kindle Wiki 与 Release：`https://github.com/koreader/koreader/wiki/Installation-on-Kindle-devices`
5. WeRead 插件仓库与 Release：`https://github.com/finlater/weread.koplugin`

记录访问日期、匹配到的型号/固件范围、所选路线和发布版本。两个高优先级来源冲突、版本不在支持范围或无法唯一识别设备时，停止写入并向用户展示冲突。

设备案例只证明该组合曾经跑通，不能覆盖当日兼容性来源。`references/macos-pw4-5.14.1.md` 仅是一个真机案例，不是默认路线。

## 电脑与连接模式

读取 `references/platform-access.md`。优先使用用户现有系统，不要求为了安装改用 Windows 或 Mac：

- 文件系统挂载：可使用跨平台 Python 脚本或平台原生文件管理器。
- MTP/非挂载设备：不要假装存在普通路径；改用平台文件传输界面，并把自动脚本标为不可用。
- 仅充电或频繁断连：先解决数据线、端口或驱动问题，不继续。

跨平台脚本需要显式路径时，用户或 Codex 必须先确认该路径确实包含 Kindle 的 `documents` 目录。

## 安全边界

- 不自动升级、降级、恢复出厂、注销设备、拆机、短接或修改分区。
- 不在 Skill 内捆绑越狱包、KOReader、WeRead 插件、书籍、账号文件或凭据。
- 下载仅来自当日原始项目发布页；记录版本和发布方提供的校验值。没有官方校验值时，记录本次下载指纹但不要冒充官方校验。
- 每次创建备份、写入设备、联网、触发越狱、重启、删除或恢复更新能力前，说明目标和影响并取得明确确认。
- 删除前用只读检查解析唯一目标；禁止未解析变量、通配符和宽泛目录。只删除当前阶段明确创建且已确认的目标。
- 不承诺不会变砖、不会封号或适用所有 Kindle。
- 不协助 DRM 移除、传播书籍、预配置账号或短时间批量抓取内容。

完整停止条件读取 `references/safety-and-routing.md`。

## 分阶段工作流

1. **问诊**：完成第一轮信息卡；只做读操作。
2. **路由**：查当日来源并形成唯一的“设备 + 固件 + 越狱 + 电脑访问方式”路线。
3. **检测与备份**：文件系统挂载时优先运行 `scripts/device_audit.py` 与 `scripts/backup_visible_storage.py`；否则按平台参考手动备份。核对源/备份文件数与逻辑字节。
4. **防更新**：只有当前路线明确要求时才执行。空间目标必须取自当日指南，不使用脚本内缓存阈值。
5. **暂存越狱文件**：从原始 Release 下载，检查压缩包结构和指纹；用户确认后写入。验证规则必须来自当前 Release，不能靠旧文件名补齐。
6. **设备端触发**：一次只给当前屏幕动作；保留完整提示。重启不是充分成功证据，须查该路线的成功标志。
7. **越狱后收尾**：确认持久化/OTA 状态及更新残留后，才清理临时填充文件。
8. **KOReader**：读取 `references/koreader-weread.md`，按当前 Wiki 选择 KPM、Scriptlet、Booklet 或 KUAL。KPM 失败必须先检查是否落盘，再决定手动回退；不连续重装。
9. **WeRead 插件**：检查最低 KOReader 版本、Release 结构、外联与更新边界；写入后运行阶段验证。
10. **验收**：测试 KOReader 启动/退出、插件加载、扫码登录、书架、一本短书、离线阅读、进度同步。长期耗电、待机与账号风险未实测就明确标为待验证。

文件系统挂载时可运行：

```text
python3 scripts/device_audit.py <Kindle路径或盘符>
python3 scripts/backup_visible_storage.py <Kindle路径或盘符> <备份父目录>
python3 scripts/verify_stage.py <winterbreak2|koreader|weread> <Kindle路径或盘符>
```

若环境没有 Python，使用平台文件管理器和 `references/platform-access.md` 的手工核对，不要求用户额外安装运行时。

## 参考资料路由

- 第一轮问题与分流：`references/intake-and-routing.md`
- 通用门禁、证据优先级与停止条件：`references/safety-and-routing.md`
- macOS / Windows / Linux / MTP：`references/platform-access.md`
- KOReader、KPM 回退与 WeRead：`references/koreader-weread.md`
- 报错与恢复判断：`references/troubleshooting.md`
- PW4 + 5.14.1 + macOS 真机案例：`references/macos-pw4-5.14.1.md`，仅在设备精确匹配或研究已知案例时读取

## 沟通与交付

- 每轮只给一个操作阶段，先说目标、风险、成功标志和停止条件。
- 用“来源已核对 / 文件已校验 / 真机通过 / 尚未验证”区分证据层级。
- 出错时保留现场，先读取错误、目录和日志；不要连续切换越狱或安装方式。
- 完成后交付一份脱敏验收记录：设备/固件/系统、采用路线和版本、成功项、失败回退、待验证项、回退注意事项。
