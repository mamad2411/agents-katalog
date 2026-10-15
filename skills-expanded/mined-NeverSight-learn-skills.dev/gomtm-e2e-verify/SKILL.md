---
name: gomtm-e2e-verify
description: 真机验证, 三端连通性验证. 真机功能确认. 云端移动设备,browser,gomtm(linux) 真实环境功能确认和验收
---

## 概述

就算所有源码中的测试和功能都通过了测试, 这依然不能确保在生产环境中真实功能正确,因此需要确保三端功能连通切功能正确.

## 何时使用

- 当确认 gomtm, gomtmui, gomtm-android 源码级别测试通过后,认为源码上的实现已经正确后. 需要最终确认功能可以在真实环境中核心功能正确的时候.

## 注意事项

- 如果当前修改还没有进入实际被部署或发布的产物, 真机验证结论就可能失真。`gomtmui` 与 `gomtm-android` 的真实验收通常依赖已经构建并可访问的前端/发布产物, 因此当你处于未部署的 worktree 或分支时, 需要先确认对应变更是否已经通过当前发布链路生效, 再继续做真机验证.

## 提示

1. 远程设备接入/安装/卸载验收应优先确保 `mtmai device install|activate|uninstall|wait` 这套主线正确，重点确认 control-plane 命令围绕 canonical `devices` / `device_events` 推进状态与历史。授权部分若有问题，先研究当前正式激活流程中的屏幕授权与后续 readiness 边界。注意 APK 真相来自外部仓 latest release / pin manifest，不要再把“主仓本地源码未提交所以设备装旧 APK”当作默认前提.

2. 总是允许对前端进行必要的重构和优化,至少目前功能是不完全正确的,特别是v2基于原生视频流部分的功能不完全正确.我没有实际看到实时画面, 可能在授权相关环节有问题.

5. 注意 android 端的 apk 需要确保安装了最新版 release。install 成功语义应收敛为“宿主已安装、可启动，并可进入登录绑定与激活流程”，不是某些旧入网状态名，更不是“远控完整可用”。后续要继续通过 `devices` 最小真相、`runtime_credential + device_runtime_heartbeat(...)`、capability 读模型与真实前端页面确认 accessibility / screen capture / remote usable 到底卡在哪一层。

6. 当前gomtmui 前端使用独立的仓库进行,而且已经配置了 工作流,推送代码后会自动构建. 如果修正了前端代码,确保基于git actions构建成功,让域名对应的网址最终更新.

7. 如果你使用了浏览器工具,请保存截图.
9.(新增) 
  - `mtmai device install <DEVICE_ID>` - 当前远程 Android 设备安装主线.
  - `mtmai device activate <DEVICE_ID>` - 当前远程 Android 设备激活主线.
  - `mtmai device uninstall <DEVICE_ID>` - 当前远程 Android 设备卸载主线.
  - `mtmai device wait <DEVICE_ID>` - 当前远程 Android 设备等待终态主线.
  规格:
      - 若 control-plane 执行路径内部使用了 ADB 连接,应当及时释放连接避免 `adb devices -l` 存在残留连接, 因为这会干扰后续 adb 操作.
10. 注意不要搞错测试用设备. 已有列表可能有其他android连入,但是不一定是测试用设备.
11. 后8位位"HXekBZWx" 不是测试节点,是已有的生成节点,可以忽视这个节点.
12. 优先解决连通性问题.
13. 你可以通过 ADB 的方式进行调试和判断问题, 但是不能使用 ADB 跳过原本应当通过正常流程触发的功能. 因为现在测试的就是正常命令和流程的正确性.
  例如:
  1. 必须通过 `mtmai device install <DEVICE_ID>` 触发正式安装链路，而不是直接使用 `adb` 来辅助安装.
2. 发现节点后,优先通过当前产品真实链路与页面/能力面继续确认授权是否已经成立,而不是通过 adb 命令直接完成授权.
    注意: 当前的授权流程和操作可能有问题,如果这是android自身的特性导致不可能完成,应当主动报告并结束任务,告知原因,并给出解决方案.
14. 不要完全相信单元测试的结果和之前验收的结论.
15. **注意最近的大幅度,对browser 完全放弃 adb scrcpy 前端库的使用使用仅保留v2新版实时屏幕控制的重构.**

## 要求

1. 完整通过真机三端连通性验收.
3. 当依然发现`System is busy, please try again later` 类似的api回应时,必须进行反思阅读官方文档修正代码.因为这不是api真正的问题,而是我们没有正确使用api.

## 验收标准

1. 重新打开当前已部署前端的设备列表页面，例如 `${GOMTMUI_PUBLIC_URL}/dash/devices`，可以看到测试设备的设备记录，并且页面上的在线/离线判断与最近心跳时间一致，不再依赖已删除的旧页面或 peer presence 视图。
2. 若本次任务还涉及远控或实时画面，应通过当前活跃的前端页面与 v2 链路完成验收，而不是回到已删除的 `/dash/p2p` 页面。

## 终端使用约定

使用 tmux 进行任务管理, 因为可能人类搭档或者之前的任务已经启动过tmux, 约定使用`gomtm-e2e-verify`这个会话名称, 这样可以与人类搭档和之前的任务共用相同的tmux会话.

## 关于登录凭据

登录凭据通常在数据库、环境变量或安全凭据管理位置中已经存在。使用管理员账户完成相关验收时，只记录凭据来源，不要把真实账号或默认密码写入技能文档、报告或最终回复。

## 以下情况应当主动完成而不必等待人类确认

1. 修改前端代码,推送前端代码,重新部署前端.
2. 重启 gomtm server, 注意使用 `--force`参数
3. 修改 `gomtm-android` 代码并触发github CICD 工作流完成新版 apk构建和发布,并在测试设备中卸载并重新安装新版.
