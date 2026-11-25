---
name: cloud-api
description: 处理大疆上云 API（DJI Cloud API）的接入、解析、调试与问题定位。当用户提到"大疆上云""Cloud API""云平台对接""大疆机场上云""Pilot 上云""MQTT 设备接入""物模型""HMS 告警""机场直播""OSD 数据""DRC 指飞""航线任务下发""设备拓扑""固件升级"等涉及大疆行业设备（机场/DJI Pilot 2/遥控器/无人机）与第三方云平台通信的场景时使用。
---

# DJI 上云 API

大疆上云 API 是基于大疆行业版无人机（机场、DJI Pilot 2、遥控器、负载）对外提供的云平台接入接口，采用"端-边-云"架构：**无人机不能直接上云**，必须通过网关设备（大疆机场或遥控器）间接接入。

- 网关设备（机场 / 遥控器）→ 第三方云平台，通信协议为 MQTT / HTTPS / WebSocket
- 网关注册登录时会上报飞机与负载的能力（物模型）
- 本技能只处理云平台侧接入与解析，不涉及飞控底层

## 安装后的路径与文档定位

- 从已加载技能的实际目录读取 `reference/`，并使用该目录下脚本的绝对路径执行命令；任务当前目录不一定是技能目录。
- 安装版自带 `KNOWLEDGE_SOURCES.md`、`THIRD_PARTY_NOTICES.md` 与 `INSTALLATION.md`；源码模式的这些文件在仓库根目录。不要假设安装版父目录仍是源码仓库。
- 深度查询前，运行安装版 `scripts/locate_dji_docs.py`（源码模式用仓库根目录的同名脚本）。用户明确提供路径时传 `--docs-root`；否则依次检查 `DJI_CLOUD_API_DOCS` 和任务当前目录的 `docs/Cloud-API-Doc`。明确配置无效时停止回退并报告。
- 定位成功仅证明路径存在；核对官方目录 Git HEAD 与来源说明基准后，再读取对应官方章节。未核对时不声称是最新或固定版本。
- 缺少官方文档时可依据现有笔记解释和运行离线校验，明确说明来源及覆盖范围；无法核实的字段或兼容性请用户提供官方目录，不猜测、不自动联网下载。

## 何时使用

- 部署大疆上云服务端（MQTT 网关 / HTTPS / WebSocket / 对象存储）
- 解析设备上报的物模型数据（OSD 属性 / 事件 / 服务响应）
- 向设备下发指令（航线任务 / 直播 / 媒体 / 固件升级 / HMS 查询）
- 排查设备上下线、拓扑更新、订阅不到数据、错误码等问题
- 区分两种场景：**Dock-to-Cloud**（机场上云，无人值守）与 **Pilot-to-Cloud**（遥控器 + DJI Pilot 2 上云，有人操作）

## 基础架构

```
第三方云平台（你的服务端）
├── MQTT 网关     ← 设备长连接，收发属性/服务/事件/上下线（Broker）
├── HTTPS 服务    ← 短连接接口（航线管理/媒体管理/地图元素/态势感知）
├── WebSocket 服务 ← 服务端向 Pilot/Web 推送（地图元素/态势感知）
└── 对象存储      ← 航线文件/媒体文件存储

设备端
├── 大疆机场（Dock）  → MQTT/HTTPS 上云（Dock-to-Cloud）
├── 遥控器 + DJI Pilot 2 → MQTT/HTTPS/WebSocket/JSBridge 上云（Pilot-to-Cloud）
└── 无人机/负载         → 不直接上云，由网关代理上报
```

## 通信协议速查

| 协议 | 用途 | 关键点 |
|---|---|---|
| MQTT | 设备长连接，属性/服务/事件/上下线/DRC | Topic 前缀 `sys/`（基础）与 `thing/`（物模型），字段按具体 Topic/接口要求携带 `tid`/`bid`/`method`/`data`/`timestamp` |
| HTTPS | 业务短连接（航线/媒体/地图/态势） | `https://{endpoint}/{module}/api/{v}/...`，header 带 `X-Auth-Token`，响应 `{code,message,data}` |
| WebSocket | 服务端→Pilot/Web 推送 | 消息含 `biz_code`/`version`/`timestamp`/`data` |
| JSBridge | Pilot 内嵌 Webview 与原生双向通信 | Web 登录换取 Token/MQTT 地址后传给 Pilot |

## 硬性规则

1. **无人机不能直接上云**：必须经机场或遥控器网关代理；订阅/下发时先区分网关 `gateway_sn` 与被代理设备 `device_sn`
2. **Topic 双层划分**：`sys/product/{gateway_sn}/...`（网关上下线/拓扑）与 `thing/product/{device_sn}/...`（无人机/负载物模型）；网关自身物模型按接口使用 `gateway_sn`，不要混用
3. **osd 与 state 分离**：`osd` 定频上报（pushmode=0），`state` 事件性上报（pushmode=1）
4. **公共字段按 Topic 区分**：普通消息使用 `tid` 事务 UUID（一次通信）和 `bid` 业务 UUID（长流程，如点播/下载），具体必需性查对应接口；DRC 不强制普通消息的 `tid`/`timestamp` 信封。校验脚本不统一强制缺失 `bid`，不得据此省略业务要求的字段
5. **回复检查结果码**：`services_reply`/`events_reply`/`requests_reply`/`status_reply` 的结果在 `data.result`；`property/set_reply` 在 `data.<属性>.result`；DRC 上行在 `data.result`。非 0 表示处理失败，结构合法不代表业务成功
6. **HTTPS 响应统一 `{code,message,data}`**：`code=0` 成功；`message` 为错误描述
7. **错误码 ABCDEF 格式**：A 来源（3/5 设备端，4/6 Pilot）、BC 模块、DEF 自定义；HMS 错误需拼接文案 Key 查 hms.json（见 error-code.md）
8. **物模型三要素**：属性(Property)/服务(Service)/事件(Event)，属性用 `accessMode=rw` 判断是否可写
9. **机场型号差异**：Dock1（如 M30 机场）与 Dock2（如 M3D 机场）的属性/服务主题可能不同，按机型查对应物模型
10. **生成/解析后必须校验**：字段命名、类型、取值范围对照官方物模型，禁止自造字段

## 安全与隐私边界（重要）

本技能涉及真实设备控制与云平台对接，以下边界必须严格执行，不能只依赖校验脚本：

1. **高风险动作再次确认**：远程开机、返航、起飞、指飞（DRC `fly_to_point`/`takeoff_to_point`）、航线任务下发等动作，必须再次向用户确认目标坐标、高度与动作本身后才能执行
2. **不写入用户真实数据**：不得把用户设备 SN、真实坐标、航线、Token 写入示例文件或文档；示例必须使用占位符（`{sn}`、虚构坐标、`xxxxxxxx-...` UUID）
3. **脱敏义务**：坐标、设备 SN、Token、密钥、日志等敏感信息在输出前必须先脱敏；日志文件路径、设备序列号等一律占位化
4. **校验通过 ≠ 控制安全**：`validate_mqtt.py` 只校验公共信封字段与部分关键 method 参数，不代表设备端处理成功或飞行安全，也不代表符合当地法规
5. **不主动提权/不改配置**：未经用户明确要求，不得尝试连接生产环境、修改设备配置、拉取真实日志或进行任何网络操作

## 按需加载

- **要核对来源或适用版本** → 查看所用参考文档顶部的官方路径、固定提交基准、适用范围与校验边界；完整更新流程见仓库 `KNOWLEDGE_SOURCES.md`。本地文档未同步时不得声称使用最新规范，机型支持须核对具体接口表
- **要了解物模型/MQTT/HTTPS/WebSocket/JSBridge 基础概念** → `reference/basic-concepts.md`
- **要处理 MQTT 主题与消息结构**（osd/state/services/events/requests/status/property/drc） → `reference/mqtt-topics.md`
- **要处理遥控器 + DJI Pilot 2 场景**（Pilot 登录、地图元素、态势感知、直播、媒体、航线管理） → `reference/pilot-to-cloud.md`
- **要处理大疆机场场景**（机场上下线、设备管理、直播、媒体、航线任务、HMS、固件升级、远程调试） → `reference/dock-to-cloud.md`
- **要了解功能集与适用机型** → `reference/feature-set.md`
- **要查错误码 / HMS 告警文案** → `reference/error-code.md`
- **要处理 PSDK/喊话器、AirSense、FlySafe 解禁、自定义飞行区、多机场蛙跳、Dock2 遥控器、PSDK/ESDK 透传** → `reference/extended-topics.md`
- **要搭建上云服务端（源码/Docker 部署）、Pilot 登录、MQTTX 调试、日志导出** → `reference/deploy-debug.md`

## 脚本工具

- **`scripts/build_mqtt.py`**：构造标准 MQTT 消息。读入模板 JSON，自动补齐 `tid`/`timestamp`（+`bid`/`gateway`），输出带 `tid`/`bid`/`timestamp`/`gateway` 的完整消息
  ```bash
  python scripts/build_mqtt.py <template.json> [--gateway <sn>] [--bid] [-o <out.json>]
  ```
- **`scripts/validate_mqtt.py`**：校验 MQTT 消息合法性。检查公共字段、UUID 格式、13 位毫秒时间戳、method 必填性，以及普通回复、属性设置回复和 DRC 上行各自的结果结构
  ```bash
  python scripts/validate_mqtt.py <message.json> [--topic <topic>] [--strict]
  ```
  - 退出码：0 通过；1 不通过；2 参数错误
  - 建议显式指定 `--topic`，按完整 Topic 区分请求、回复、属性设置与 DRC；不支持的显式 Topic 返回错误
  - 回复不检查请求参数；属性设置不强制 `method`，属性回复逐属性检查 `result`
  - 不指定 Topic 时只能按内容推断；脚本未覆盖全部 method 的业务参数，不统一强制缺失 `bid`

## 调试速查

| 症状 | 排查方向 |
|---|---|
| 设备不上线 | 检查 MQTT 认证（sn/密钥）、`sys/product/{sn}/status` 是否收到 `update_topo` |
| 订阅不到 OSD | 确认订阅的是 `thing/product/{device_sn}/osd`，且机型物模型存在该属性 |
| 下发指令无响应 | 确认 `tid`/`bid` 与 `method` 正确，检查 `services_reply` 的 `result` |
| 事件重复推送 | 检查 `events` 消息的 `need_reply`，按需回复 `events_reply` |
| HMS 告警看不懂 | 按 HMS 错误码拼接文案 Key，查 `hms.json` 获取文案（见 error-code.md） |
| 文件传不上去 | 检查临时凭证（HTTPS 获取 credentials）与对象存储权限 |
