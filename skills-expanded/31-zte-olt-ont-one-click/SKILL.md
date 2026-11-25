---
name: 31-zte-olt-ont-one-click
description: 手动注册：必须写入真实 GPON SN；T-CONT→onu→GEM/vport/service-port→pon-onu-mng。非 PnP。须 WRITE；write 可选。
---

# ZTE OLT · 手动一键开通（写真实 SN）

## 适用范围

导航适用于 ZXA10 C300 / C320 / C600 / C650 等。字面已观测只读锚点为 **C650 / V1.1.2**；下列开通序列来自常见字段脚本，标为 **`[DISCOVERY]` / `[字段示例]`**，**不得**升为 C650 `[已确认]`，直至本机 `?` 与试跑成功。

## 与 PnP（Skill 32）的核心区别

| | **本 Skill（31）手动注册** | **Skill 32 PnP 注册** |
|--|---------------------------|------------------------|
| SN | **必须写真实 SN**（`onu … sn ${ONU_SN}`） | 预置 **`sn 十二位全0`**（占位） |
| 绑定方式 | 运维事先知道光猫 SN，手工写入 | 口上 **`pnp enable`**；光猫上电后 **OLT 自动把占位 SN 替换为真实 SN** |
| 典型命令 | `onu 1 type ZTE-F621 sn FHTT…`（真实值来自 SoT） | `onu 1 type ZTE-F620 sn 十二位全0` + `pnp enable` |

不要混用：手动流程不要用全 0 SN；PnP 流程不要在预置阶段强行写真实 SN（除非局方另有规定）。

## 目标

在显式 WRITE 授权下，**已知真实 SN** 时按固定骨架快速注册一台 ONU，并挂上互联网 + TR069（或局方等价）多业务流。

## 何时使用

- 用户已提供（或 SoT 已有）**真实 SN**，要求开通
- 已有同类局点模板，只需换参套用

不要在仅 READ/排障任务中使用本 Skill。关联查询用 `22-zte-c600-ont-correlation`。  
**占位 SN + `pnp enable` 自动替换** 见 `32-zte-olt-onu-pnp`。

## 前置条件

1. `21-zte-c650-baseline`：`show software` 身份一致
2. 现行任务含 **WRITE**；**真实 SN** 与 VLAN 来自 Source of Truth（勿从公开仓库推断）
3. 已查空闲 ONU-ID、现网 T-CONT 模板名是否已存在
4. 回滚思路已备（`no onu`、删 service-port 等须本机 `?`）
5. **默认不 `write`**；仅用户明确要求时再落盘

## 参数（必须替换）

| 参数 | 含义 | 示例占位 |
|------|------|----------|
| `${SHELF}/${SLOT}/${PORT}` | OLT PON | `1/3/1` |
| `${ONU_ID}` | ONU 编号 | `1` |
| `${ONU_TYPE}` | 类型字符串 | `ZTE-F621` |
| `${ONU_SN}` | **真实** GPON SN（禁止用 `十二位全0` 冒充手动注册） | 仅存 SoT |
| `${TCONT_INET}` / `${TCONT_TR069}` | T-CONT 模板名 | `GPON-1G` / `GPON-1M` |
| `${VLAN_INET}` / `${UVLAN_INET}` | 上网 CVLAN / user-vlan | `41` / `41` |
| `${VLAN_TR069}` / `${UVLAN_TR069}` | 管理等 | `46` / `4015` |
| `${VLAN_IPTV}` / `${UVLAN_IPTV}` | 可选组播/IPTV | `46` / `46` |
| `${VLAN_VOIP}` / `${UVLAN_VOIP}` | 可选语音 | `46` / `193` |

真实序列号、客户描述、局点 VLAN **禁止**写入公开证据。

## 一键骨架（字段示例 · DISCOVERY）

下列接口名采用常见 `gpon-olt_` / `gpon-onu_` 形式；若本机拒绝，用 `?` 改发现 `gpon_olt-` 等变体（C650 只读证据多见后者）。

### 0) 只读预检

```cli
show software
show gpon profile tcont
show gpon onu state
```

若 `${TCONT_INET}` / `${TCONT_TR069}` 已存在，**跳过**建模板，直接用现网名。

### 1) T-CONT 模板（仅缺失时创建）

```cli
configure terminal
gpon
profile tcont ${TCONT_INET} type 3 assured 200000 maximum 1024000
profile tcont ${TCONT_TR069} type 3 assured 1024 maximum 20000
exit
exit
show gpon profile tcont
```

带宽单位与 type 取值以本机为准；上表数值仅为字段常用示例。

### 2) OLT 口 UP + **手动**注册 ONU（真实 SN）

```cli
configure terminal
interface gpon-olt_${SHELF}/${SLOT}/${PORT}
no shutdown
onu ${ONU_ID} type ${ONU_TYPE} sn ${ONU_SN}
exit
```

`${ONU_SN}` 必须是 SoT 中的**真实**序列号。若要用 `十二位全0` + `pnp enable` 自动替换，改走 Skill 32。

### 3) ONU 侧 T-CONT / GEM / vport / service-port

四业务示例（上网 + TR069 相关三流）；局点可减为 1～2 条，**勿照抄无关 VLAN**。

```cli
interface gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
sn-bind enable sn
tcont 1 name INTERNET profile ${TCONT_INET}
tcont 2 name TR069 profile ${TCONT_TR069}
gemport 1 name INTERNET tcont 1 queue 1
gemport 2 name TR0692 tcont 2 queue 2
gemport 3 name TR0693 tcont 2 queue 2
gemport 4 name TR0694 tcont 2 queue 2
switchport mode hybrid vport 1
switchport mode hybrid vport 2
switchport mode hybrid vport 3
switchport mode hybrid vport 4
service-port 1 vport 1 user-vlan ${UVLAN_INET} vlan ${VLAN_INET}
service-port 2 vport 2 user-vlan ${UVLAN_TR069} vlan ${VLAN_TR069}
service-port 3 vport 3 user-vlan ${UVLAN_IPTV} vlan ${VLAN_IPTV}
service-port 4 vport 4 user-vlan ${UVLAN_VOIP} vlan ${VLAN_VOIP}
exit
```

### 4) OMCI / pon-onu-mng 业务绑定

```cli
pon-onu-mng gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
service 1 gemport 1 vlan ${VLAN_INET}
service 2 gemport 2 vlan ${UVLAN_TR069}
service 3 gemport 3 vlan ${UVLAN_IPTV}
service 4 gemport 4 vlan ${UVLAN_VOIP}
exit
exit
```

说明：字段脚本里 `service N` 的 vlan 有时填 user-vlan、有时填 CVLAN；**以局方模板与本机验收为准**，冲突时停并 DISCOVERY，勿混用两套映射。

### 5) 验收（必做）

```cli
show gpon onu state
show gpon onu detail-info gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
show gpon onu tcont gpon-olt_${SHELF}/${SLOT}/${PORT}
show gpon onu gemport gpon-olt_${SHELF}/${SLOT}/${PORT}
show service-port interface gpon-onu_${SHELF}/${SLOT}/${PORT}:${ONU_ID}
```

期望：ONU `working`（或局方等价）、service-port 使能；再测上层业务。

### 6) 落盘（可选 · 默认跳过）

```cli
write
```

- **禁止**开通成功后自动 `write`
- 仅当用户明确说「保存 / write / 落盘」时执行
- 与华为 `save` 同属可选 PERSIST；见消费方策略

## LLM 一键编排提示

```text
1. 收集参数表（缺参则问用户，禁止编造 SN/VLAN）
2. READ 预检 → 决定是否建 T-CONT 模板
3. 按 2→3→4 顺序 WRITE（遇拒立即停，? 发现，不盲改）
4. 跑验收 show
5. 询问是否 write；默认否
```

用户说「按标准模板开通」且 SoT 已有局点 VLAN/模板名时，可一次给出完整拟执行脚本供确认，**确认后再下发**。

## 精简变体（仅上网）

若只要互联网单业务：保留 T-CONT1 + gemport1 + vport1 + service-port1 + `service 1`，删除 2～4 及相关 TR069/IPTV/语音 VLAN。

## 开局/PnP / QinQ 变体

若要用 **`sn 十二位全0` + `pnp enable`**（OLT 上电后自动替换真实 SN），必须改用 **`32-zte-olt-onu-pnp`**，不要在本 Skill 里写全 0 冒充「手动注册」。

本 Skill（手动）仅在已知真实 SN 时使用。QinQ / IGMP / traffic-limit 等业务细节可与 32 文档对照，按需叠加（仍为 DISCOVERY）：

- `gemport 1 traffic-limit downstream ${TRAFFIC_PROFILE}`
- `service-port … user-vlan ${UV} vlan ${CV} svlan ${SV}`
- `igmp version v3 vport 1` / `igmp fast-leave enable vport 1`

## 已知风险

- 接口命名方言（`gpon-onu_` vs `gpon_onu-`）导致整段失败
- 复用已存在的 T-CONT 名但带宽不符
- ONU-ID / SN 冲突
- service-port vlan 与 pon-onu-mng vlan 不一致导致业务不通
- 过早 `write` 固化错误开通

## 回滚（DISCOVERY）

须本机 `?` 后逆序清理，示例方向（非已确认命令）：

- `pon-onu-mng` 下 `no service …`
- `interface gpon-onu_…` 下 `no service-port` / `no gemport` / `no tcont`
- `interface gpon-olt_…` 下 `no onu ${ONU_ID}`
- 勿删仍被其他 ONU 引用的全局 `profile tcont`

## 依赖

- `21-zte-c650-baseline`、`22-zte-c600-ont-correlation`、`32-zte-olt-onu-pnp`（PnP/开局）
- `network-device-access`；落盘策略遵循 ACCESS-GUARDRAILS `PERSIST`

## 禁止事项

- 无 WRITE 授权不开通
- 不把示例 SN/VLAN 当生产事实
- 不自动 `write` / `save`
- 不跨机型把本骨架标为 `[已确认]`

## 来源

- 字段运维开通脚本（脱敏结构化）
- 只读锚点：ZXA10 C650 / V1.1.2（`show gpon profile tcont` 等）
- 设备 CLI 优先于本文
