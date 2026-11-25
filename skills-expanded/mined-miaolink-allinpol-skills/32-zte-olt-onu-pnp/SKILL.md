---
name: 32-zte-olt-onu-pnp
description: PnP 注册：onu 预置 sn 十二位全0 + pnp enable，光猫上电后 OLT 自动替换为真实 SN；含 onu-pnp/模板/QinQ/IGMP。须 WRITE；write 可选。
---

# ZTE OLT · ONU PnP 注册（占位 SN → 自动替换）

## 适用范围

ZXA10 C300 / C320 / C600 / C650 等。只读锚点仍为 C650 / V1.1.2。下列来自字段 **开局/PnP** 脚本，一律 **`[DISCOVERY]` / `[字段示例]`**，须本机 `?` 后执行；不得标为 `[已确认]`。

## 与手动注册（Skill 31）的核心区别

| | **Skill 31 手动注册** | **本 Skill（32）PnP 注册** |
|--|----------------------|---------------------------|
| SN 写法 | 配置里写死 **真实 SN** | 配置里写 **`sn 十二位全0`**（占位/未配置） |
| 谁填真实 SN | 运维/LLM 在下发前写入 | 光猫上电、口上 **`pnp enable`** 后，**OLT 自动把占位 SN 替换为实际上线 SN** |
| 适用 | 装维已扫码/已知 SN | 预开通槽位、即插即用、先配业务后等终端 |

**一句话：** 手动 = 你写 SN；PnP = 先写全 0 + `pnp enable`，OLT 替你换成真 SN。

## 目标

按「开局/PnP 骨架」落地：模板 → onu-type → **onu-pnp** → OLT 口预置占位 ONU + **`pnp enable`** →（可选）精细业务 / 上联；**默认不 `write`**。

## 何时使用

- 用户说「PnP」「即插即用」「占位 SN」「十二位全0」「pnp enable」
- 要先占 ONU-ID/业务，等光猫上电自动绑定真实 SN
- 附带 QinQ / IGMP / 上联 trunk 开局（仍须单独授权高风险项）

已知真实 SN、要求当场绑死 → 用 `31-zte-olt-ont-one-click`，不要走占位 SN。

## 前置条件

1. WRITE 授权；SoT 提供 PON、VLAN/SVLAN、模板名、onu-type（**预置阶段不要求真实 SN**）
2. `show software` 指纹一致
3. 已盘点现网是否已有同名 `profile tcont` / `profile traffic` / `onu-type`（有则复用）
4. 回滚与上联影响已评估
5. **禁止自动 `write`**

## 参数

| 参数 | 含义 |
|------|------|
| `${SHELF}/${SLOT}/${PORT}` | PON，如 `1/4/1` |
| `${ONU_TYPE}` | 如 `ZTE-F620`、`ZTEG-F601` |
| `${PNP_SN}` | PnP 占位 SN，字段惯例 **`十二位全0`**（勿改成真 SN，除非局方另有规定） |
| `${TCONT_*}` / `${TRAFFIC_*}` | 模板名 |
| `${UVLAN}` / `${CVLAN}` / `${SVLAN}` | user-vlan / 内层 / 外层（QinQ） |
| `${MC_VLAN}` | 组播 VLAN |
| `${UPLINK_IF}` / `${SMARTGROUP}` | 上联（高风险） |
| `${TRUNK_VLANS}` | 上联放行列表（来自 SoT） |

## 可取结构（从开局脚本提炼）

### A. T-CONT + traffic 模板族

字段常见：多档 type1/3/4 T-CONT，以及 `profile traffic` 的 sir/pir，供 GEM 下行限速引用。

```cli
configure terminal
gpon
profile tcont ${TCONT_10M} type 3 assured 10240 maximum 102400
profile tcont ${TCONT_100M} type 3 assured 102400 maximum 102401
profile tcont ${TCONT_30M} type 1 fixed 30720
profile tcont ${TCONT_20M} type 4 maximum 102400
profile tcont ${TCONT_50M} type 3 assured 51200 maximum 51201
profile traffic ${TRAFFIC_LAN} sir 20000 pir 500000
profile traffic ${TRAFFIC_30M} sir 30720 pir 30720
profile traffic ${TRAFFIC_20M} sir 20000 pir 20000
profile traffic ${TRAFFIC_50M} sir 50000 pir 50000
exit
exit
show gpon profile tcont
```

- type1 fixed / type3 assured+max / type4 maximum：按局方 DBA 策略选，勿混用未经验证的数值
- `maximum` 比 `assured` 大 1 的写法见于字段脚本，**含义以本机文档为准**，复制前确认

### B. onu-pnp（核心）

```cli
configure terminal
onu-pnp
bandwidth gpon ${PNP_BW}
onu-type-default gpon ${PNP_DEFAULT_VENDOR_OR_TYPE}
onu-vlan gpon-olt_${SHELF}/${SLOT}/${PORT} mode transparent
olt-vlan transparent gpon-olt_${SHELF}/${SLOT}/${PORT}
onu-uni-vlan gpon-olt_${SHELF}/${SLOT}/${PORT} eth_0/1 mode tag vlan ${UVLAN}
exit
```

要点：

- **按 PON 口**配置透明/打标，不是全局一句完事
- `onu-uni-vlan … eth_0/1 mode tag vlan …`：PnP 默认把 UNI 打成指定 VLAN（常与上网 user-vlan 对齐）
- 先 `onu-pnp ?` / `onu-vlan ?`；透明与 tag 策略冲突时停

### C. onu-type 能力声明

```cli
configure terminal
pon
onu-type ${ONU_TYPE} gpon description ${ONU_TYPE_DESC}
onu-type ${ONU_TYPE} gpon max-tcont 8
onu-type ${ONU_TYPE} gpon max-gemport 32
onu-type ${ONU_TYPE} gpon max-switch-perslot 8
onu-type ${ONU_TYPE} gpon max-flow-perswitch 8
onu-type-if ${ONU_TYPE} eth_0/1
onu-type-if ${ONU_TYPE} eth_0/2
onu-type-if ${ONU_TYPE} eth_0/3
onu-type-if ${ONU_TYPE} eth_0/4
! 按需 pots_0/1 pots_0/2 等
uncfg-onu-display-info sn pw
exit
```

未声明的 type 可能导致 `onu … type …` 失败；与 31 的 `type ZTE-F621` 同类，开局应先备齐。

### D. OLT 口：占位 SN + `pnp enable`（PnP 注册关键）

```cli
configure terminal
interface gpon-olt_${SHELF}/${SLOT}/${PORT}
onu 1 type ${ONU_TYPE} sn ${PNP_SN}
onu 2 type ${ONU_TYPE} sn ${PNP_SN}
pnp enable
exit
exit
```

其中 `${PNP_SN}` 字段惯例为 **连续 12 个数字字符 `0`**（下文称「十二位全0」）：

1. 预先占用 ONU-ID，并可先配好 `gpon-onu` / `pon-onu-mng` 业务  
2. 口上 **`pnp enable`**  
3. 光猫上电后，**OLT 自动将占位 SN 替换为实际上线光猫的真实 SN**（无需再手工改 SN）

验收时用 `show gpon onu state` / `baseinfo` 确认占位已变为真实 SN。若长期仍为全 0：查光纤、PON、`onu-pnp` 策略、`pnp enable` 是否生效。

**禁止**把本步骤写成手动注册：手动注册见 Skill 31，必须一开始就写真实 SN，且通常不依赖「全 0 + 自动替换」。

### E. 单 ONU 精细业务（QinQ / 多 service-port / IGMP）

在 PnP 或手工注册后，常再进 `gpon-onu` 固化：

```cli
configure terminal
interface gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
tcont 1 profile ${TCONT_20M}
tcont 1 gap mode2
gemport 1 name g1 unicast tcont 1 dir both
gemport 1 traffic-limit downstream ${TRAFFIC_LAN}
switchport mode hybrid vport 1
service-port 1 vport 1 user-vlan ${UVLAN} vlan ${CVLAN} svlan ${SVLAN}
service-port 2 vport 1 user-vlan ${MC_VLAN} vlan ${MC_VLAN}
service-port 3 vport 1 user-vlan ${OTHER_UVLAN} vlan ${OTHER_CVLAN}
igmp version v3 vport 1
igmp fast-leave enable vport 1
exit
pon-onu-mng gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
service 1 gemport 1
vlan port eth_0/1 mode tag vlan ${UNI_VLAN_1}
vlan port eth_0/2 mode tag vlan ${UNI_VLAN_2}
vlan port eth_0/3 mode tag vlan ${UNI_VLAN_3}
vlan port eth_0/4 mode tag vlan ${UNI_VLAN_4}
multicast vlan add vlanlist ${MC_VLAN}
exit
exit
```

相对 Skill 31 的增量：

- **`svlan` QinQ**
- **`gemport … traffic-limit downstream`** 引用 traffic 模板
- **`tcont … gap mode2`**
- **IGMP v3 + fast-leave**
- **UNI 口分别打 tag** + **multicast vlanlist**

### F. 上联（高风险 · 单独确认）

```cli
! 示例结构 — VLAN 列表必须来自 SoT
interface ${SMARTGROUP}
smartgroup mode 802.3ad
switchport mode trunk
switchport vlan ${TRUNK_VLANS} tag
exit
interface ${UPLINK_IF}
no shutdown
smartgroup ${SMARTGROUP_ID} mode active
switchport mode trunk
switchport vlan ${TRUNK_VLANS} tag
exit
```

- 改上联 trunk 可能影响整局；须单独 HIGH-IMPACT 确认
- 对端若是 ZXR10 交换机，交叉 `46-zte-switch-lacp-smartgroup`（DISCOVERY）
- 开局脚本里的 `1000-2009` 等区间**禁止**当作本仓库已确认生产事实

## LLM 编排顺序

```text
1. 确认场景：PnP 开局 vs 单台手工开通（后者转 31）
2. READ：show software / profile tcont / 目标 PON 状态
3. 缺什么建什么：tcont/traffic → onu-type → onu-pnp → pnp enable
4. 若需 QinQ/IGMP/UNI 明细：再配 gpon-onu + pon-onu-mng
5. 上联仅在用户明确要求且授权时动
6. 验收 show（onu state / service-port / 按需 igmp）
7. 询问是否 write（默认否）
```

## 验收（DISCOVERY）

```cli
show gpon onu state
show gpon profile tcont
show service-port interface gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
! 本机发现：onu-pnp / pnp 状态、igmp、上联 trunk 相关 show
```

## 配置保存

与华为侧相同原则：**开通/开局成功 ≠ 自动 `write`**。仅用户明确要求时执行 `write`。

## 风险

- 占位 SN 被业务当成真实终端；或手动流程误用全 0 导致永不绑定
- PnP 开启后多台同时上电抢占错误 ONU-ID（按局方发现/排队规则处理）
- QinQ svlan 与上联未放行导致不通
- 组播 vlanlist / IGMP 配错冲击 IPTV
- 误改 smartgroup trunk 导致大面积中断

## 依赖

`21-zte-c650-baseline`、`22-zte-c600-ont-correlation`、`31-zte-olt-ont-one-click`（手工一键）、`network-device-access`

## 禁止事项

- 无 WRITE 不改 PnP / 上联
- 不自动 `write`
- 不把字段 VLAN 区间、占位 SN 写入公开证据当事实
- 不把本骨架升为 C650 `[已确认]`

## 来源

- 字段开局脚本（ONU PnP + 模板 + QinQ/IGMP + 上联结构，已参数化）
- 只读锚点：C650 V1.1.2
- 设备 CLI 优先
