---
name: vps-clash-autopilot
description: "Use when asked to configure an authorized BandwagonHost/KiwiVM and existing 3X-UI VPS with computer use: preserve VLESS Reality, add IPv6/Hysteria2 (HY2), configure Clash Verge/Mihomo, export Shadowrocket QR codes, verify connectivity, switch proxy groups together, or roll back. 搬瓦工、3X-UI/3xu、Clash 自动配置、IPv6 节点、HY2 备用节点、小火箭二维码、代理组统一切换。Not for purchasing, payments, OS reinstall/reset, CAPTCHA bypass, or unrelated network changes."
---

# VPS 与 Clash 自动配置

用户准备好后台后，由你检查、操作、验证和交付；不要把执行工作变成让用户抄命令的教程。能力来自宿主 Agent，安装 Skill 不会授予电脑控制、SSH 或管理员权限。

## 开始

1. 阅读 [准备清单](references/preflight.md)，发现实际可用的浏览器、电脑控制、终端与管理入口。没有能力时诚实说明缺口，不猜工具 API 或操作另一台看不到的电脑。
2. 锁定 VPS、面板、Clash Profile 和原节点。只读取明确需要的配置；不读 `.env`、SSH 私钥或浏览器 Cookie。凭据仅经本机受限文件/安全输入流转，不输出到聊天、公开截图或仓库。
3. 给出具体改动、影响、备份和回滚边界，一次取得对应授权。授权覆盖的步骤连续推进；新增费用、升级、重装或扩大范围重新确认。密码、CAPTCHA、管理员授权按宿主规则交还本人。

## 执行

- 按 [执行流程](references/workflow.md) 识别并复用现有资源、备份、切备用网络、启用 IPv6、创建 HY2 和客户端、配置 Clash、验证、收尾。页面状态优先于历史坐标；API/SSH 可用且已授权时用于确定性操作。禁止直接改面板数据库或覆盖未知运行配置。
- 使用 `scripts/autopilot.py --help`；输入和限制见 [辅助脚本](references/helpers.md)。`inspect` → `prepare` 只生成私有候选与计划；确认后才 `apply --approve`。此标志只是操作者声明，不能替代用户授权。写入后回读并通过 Clash UI 重载。
- 保留原节点、分流规则和 DNS；名称冲突或他人改动立即停止。重复调用复用相同节点，不重复建入站或轮换密钥。IPv6 不可用时按分支交付 IPv4，不能标记全部成功。
- HY2 使用有效证书或固定 SHA256 校验；禁止无校验连接。Reality 参数必须来自同一入站。服务器私钥永不进入客户端。参考 [故障分支](references/troubleshooting.md)。

## 验收与交付

- 每个节点至少三次新请求；核实实际 Profile、代理链和出口，再测 TUN 路径及 Google/YouTube/ChatGPT 实际页面。显式代理 curl 成功不证明 TUN 正常；403 不算 ChatGPT 可用；端口通不证明握手成功。
- 固定指纹要做错误指纹的隔离反向测试，确认拒绝，再恢复正确配置。不要在正在使用的配置中注入故障。
- `switch` 统一操作明确的代理组并回读；不会创建后台自动故障切换。已有长连接可能仍走旧线路。
- 手机交付离线 QR/链接；没有手机控制或用户暂缓时记录未验收，不擅自改手机原规则。
- 返回完成/未完成项、改动、真实验证、受限本地文件与备份路径、默认选择、回滚办法。结束临时测试，恢复约定入口，释放电脑控制。见 [安全说明](references/security.md)。

Do not use for payments, purchasing, OS reinstall/reset, CAPTCHA bypass, or unrelated network changes.

维护验证见 [验证记录](docs/VALIDATION.md) 与 `evals/`；本地 `reports/` 为不公开的治理输出，不能作为真机验收凭据。
