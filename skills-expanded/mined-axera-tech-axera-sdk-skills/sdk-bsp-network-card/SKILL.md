---
name: sdk-bsp-network-card-skill
description: 面向 AX615 SDK/BSP 的系统网络与网卡问题诊断 skill。根据 linkup/linkdown、PHY 协商、无 IP、DHCP、telnet 连接、吞吐异常和低温/眼图问题的日志与可核实代码证据给出结论；证据不足时明确标为待验证并给出下一步取证建议，不凭现象猜测硬件根因。
---

# AX615 网卡诊断

用于 AX615 Linux SDK（当前代码基线为 `kernel/linux/linux-4.19.125`）中 `stmmac` MAC、`axera-ephy` PHY 及其上层 IP、DHCP、TCP 服务问题的诊断。回答必须区分链路层、三层地址、TCP 服务和吞吐控制，不把“没有 IP”“telnet 失败”直接等同于 PHY 故障。

结论分为“已确认”“高可信候选”“待验证”。没有日志、代码或可重复 A/B 证据时，不得编造根因；应明确缺失证据并给出最小化的下一步取证。

## 诊断流程

1. 先确认代码基线为 `kernel/linux/linux-4.19.125`，再收集 AX615 芯片/板卡、PCB、SDK 分支、接口名、PHY 地址和 ID、温度、对端设备、协商模式、完整启动日志和复现步骤。
2. 保留首次失败前后的时序，获取 `dmesg -T`、`ip -d link`、`ip addr`、`ip route`、`ethtool`、`ethtool -S`、PHY `regdump` 及 DHCP、ping、telnet 或 iperf 的完整参数和结果；没有这些输入时先给取证清单，不给确定根因。
3. 分类：从未 linkup 先查 PHY 探测/复位/MDIO/时钟/pinmux/对端；反复 linkup/linkdown 对齐温度、对端、线缆、错误计数和复位日志；有 carrier 无 IP 分离 DHCP/静态配置/路由；有 IP 但 telnet 不通检查监听、路由、端口和防火墙；ping 正常但 iperf 低先查 TCP 拥塞算法、`CONFIG_HZ`、窗口、CPU、MTU、双工和错误计数。
4. 使用 [code-map.md](references/code-map.md) 定位代码，再用 [known-cases.md](references/known-cases.md) 匹配匿名案例。案例只在前提条件相符时引用，不把临时寄存器命令当普适修复。
5. 按 [response-template.md](references/response-template.md) 输出现象、结论等级、证据、机制、验证命令、边界和下一步；每次只改变一个变量并记录恢复方法。

## 代码高信号与边界

- MAC/MDIO 位于 `kernel/linux/linux-4.19.125/drivers/net/ethernet/stmicro/stmmac/`；AXERA glue 主要为 `dwmac-axera.c`、`dwmac-axera-plat.c`。
- PHY 初始化在 `kernel/linux/linux-4.19.125/drivers/net/phy/axera-ephy.c` 的 `ax_ephy_config_init`，当前代码含 `0x15=0x3038` 和 `0x1b=0x888f` 相关配置。
- 驱动提供 `/sys/class/net/<if>/phydev/phy_reg` 和 `regdump`。在线写 PHY 寄存器只用于受控 A/B 验证，不能直接视为固化方案。
- 吞吐案例涉及 `kernel/linux/linux-4.19.125/net/ipv4/tcp_bbr.c` 的 `bbr_full_bw_cnt` 和 `CONFIG_HZ`，不能因单次 iperf 结果直接修改 BBR 或认定硬件问题。

不要仅凭 `NO-CARRIER`、无 IP、telnet 失败、反复 link 事件或“10 Mbps”下结论。连续三轮仍缺关键证据时停止猜测，转交硬件、网络或应用负责人并列出具体取证项。

## Eval 与发布门禁

- `evals/evals.json` 覆盖链路、IP/DHCP、TCP 服务和吞吐四个诊断层级。
