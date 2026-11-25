---
name: fusion-experiment-log
description: "标准化放电日志记录——直接上传或读取本地图片、语音和文字，产出带 YAML frontmatter 的 Markdown 放电日志；记录 shot 号体系、机器参数（Ip/Bt/位形 κ,δ/加热功率/密度目标/边缘位形 LSN·USN·DN）与诊断配置；可选集成飞书 CLI 与 Obsidian。触发词：放电日志、shot 记录、放电记录、实验日志、放电索引、破裂记录、异常放电、诊断配置记录。"
license: MIT
metadata:
  author: Jiahao8595
  hermes:
    tags: [fusion, tokamak, discharge-log, shot, diagnostics, feishu, obsidian]
    related_skills: [fusion-lit-pipeline, fusion-data, fusion-machine-ops]
---

# experiment-log — 放电日志标准化 (Discharge Log)

本 skill 把放电实验的原始材料整理为可追溯的放电日志。核心不变（输入→提取→确认→输出→归档→索引→异常），但领域内容全部聚变化：以 shot 号体系为主键，机器参数写入 YAML frontmatter，诊断配置单独记录。

## 输入方式

用户通过以下任一方式提交放电实验原始材料时自动加载：

- **直接上传** — 在当前会话提交图片、音频、语音转录或文字（波形截图、控制台截图、值班记录等）。
- **本地材料** — 提供本地文件或文件夹路径，由 agent 读取并整理。
- **飞书群** — 通过可选的 `feishu-cli-integration` 读取群消息和附件。

## 输出方式

- **本地 Markdown** — 将日志和原始附件保存到用户指定的普通本地文件夹；未指定目录时，先返回可保存的 Markdown，不擅自选择路径。
- **Obsidian vault** — 通过可选的 `obsidian` skill 写入 vault，并使用附带模板建立放电索引、异常记录和诊断配置追踪。

核心流程不要求安装飞书或 Obsidian。使用飞书群输入时，才需要 bot 已加入目标群并具备 `im:message`、`im:message.group_msg` 和 `im:resource` 权限。

## 处理流程

1. 接收上传材料、读取本地文件，或从已配置的飞书群获取材料。
2. 通过 vision_analyze 和文本解析提取结构化信息（shot 号、时间片、机器参数、诊断状态、异常现象）。
3. 对缺失或模糊字段向用户确认，不猜测放电参数或实验结果。
4. 确认输出方式和目标目录，核对 shot 号与装置、日期、实验目的。
5. 写出 `{OUTPUT_ROOT}/放电日志/{装置}/{shot}.md`（或用户指定命名）。
6. 将原始附件归档到 `{OUTPUT_ROOT}/raw/discharges/YYYY.MM.DD_装置_shot/`，并在日志中建立引用。
7. 如启用索引模板，更新放电索引；发现破裂/异常时追加异常记录。
8. 告知用户生成文件及原始材料的具体位置。

模糊信息（Ip 记不清、shot 号不明、诊断标定状态未知）主动询问，不猜测写入。

## shot 号体系 (Shot Number System)

shot 号由装置控制系统按实验日/实验季顺序分配，日志必须记录 shot 号及其元数据，不得自编 shot 号。

| 字段 | 说明 |
|------|------|
| `shot` | 装置分配的放电号（主键之一，与日期共同定位） |
| `date` | 放电日期 YYYY-MM-DD |
| `machine` | 装置名（EAST / DIII-D / KSTAR / W7-X / JET 等，见 `../fusion-shared/core/machine-database.md`） |
| `purpose` | 实验目的（如 L-H 转换、位形扫描、破裂缓解、诊断标定） |

一次实验（实验日/实验季）的 shot 清单用 `templates/shot-index.md` 维护，方便 dataview 汇总。

## 机器参数 YAML frontmatter

放电日志的 frontmatter 记录本次放电的目标机器参数（符号与单位以 `../fusion-shared/core/parameter-definitions.md` 和 `../fusion-shared/core/terminology-ledger.md` 为准）：

| 字段 | 符号 | 单位 | 说明 |
|------|------|------|------|
| `shot` | — | — | 放电号 |
| `date` | — | — | 放电日期 |
| `machine` | — | — | 装置名 |
| `Ip` | I_p | MA | 等离子体电流 |
| `Bt` | B_t | T | 环向磁场 |
| `kappa` | κ | — | 拉长比 |
| `delta` | δ | — | 三角变形 |
| `heating` | P_aux | MW | 辅助加热功率（NBI / ECRH / ICRH / LHCD 分项） |
| `density_target` | n_e | 10^19 m^-3 | 密度目标（可附 n_GW 份额） |
| `configuration` | — | — | 边缘位形 LSN / USN / DN（单零/上单零/下单零/双零） |
| `diagnostics` | — | — | 启用的诊断列表（见诊断配置记录） |

## 诊断配置记录 (Diagnostics Configuration)

记录本次放电启用的诊断及其标定状态、采样率（见 `templates/equipment-tracking.md`）：

| 字段 | 说明 |
|------|------|
| `name` | 诊断名（TS / ECE / CXRS / MSE / bolometry / 中子诊断 / 反射仪 / 朗缪尔探针 等，术语见 terminology-ledger.md 第 6 节） |
| `enabled` | 是否启用 |
| `calibration_status` | 标定状态（绝对标定 / 相对标定 / 未标定） |
| `sampling_rate` | 采样率（Hz 或时间分辨率 Δt） |
| `notes` | 备注（视场、通道数、异常） |

## 目录结构

```
/vault/
├── raw/discharges/                        ← 原始层（归档）
│   └── YYYY.MM.DD_装置_shot/
│       ├── 笔记.md
│       ├── 图片/
│       └── 语音/
│
wiki/放电日志/                              ← 标准层（产出）
├── 放电索引.md          (templates/shot-index.md)
├── 异常记录.md          (templates/anomaly-log.md)
├── {装置}/              (EAST / DIII-D / KSTAR ...)
│   ├── {shot}.md
│   └── ...
└── 公共/
    └── 诊断配置记录.md   (templates/equipment-tracking.md)
```

## 放电日志文件命名规则

```
{shot}_{日期}_{目的}.md
  │      │      └─ 实验目的简写（如 LH-transition, config-scan, disruption-mitigation）
  │      └─ 日期 YYMMDD
  └─ 装置分配的 shot 号
```

示例：`60001_260529_LH-transition.md`。shot 号来自装置控制系统，agent 不生成、不自增，缺失时向用户确认。

## 可选的 Obsidian 集成

本 skill 可以只向普通本地文件夹输出 Markdown，也可以与 [Obsidian](https://obsidian.md) vault 配合使用。Obsidian 是一个基于本地 Markdown 文件的笔记系统，配合 [Dataview](https://github.com/blacksmithgu/obsidian-dataview) 插件可实现放电数据的动态查询和仪表盘。

**为什么用 Obsidian：**
- 所有日志为纯文本 Markdown，可版本控制、可全文搜索
- YAML frontmatter 结构使 dataview 可自动生成放电列表、异常汇总、诊断使用记录
- 本地存储，无云依赖性，数据安全

**安装 skill 后需在 vault 中创建以下文件：**

| 文件 | 模板 | 用途 |
|------|------|------|
| `放电日志/放电索引.md` | `templates/shot-index.md` | Dataview 查询仪表盘（shot 清单） |
| `放电日志/异常记录.md` | `templates/anomaly-log.md` | 破裂/异常放电记录 |
| `放电日志/公共/诊断配置记录.md` | `templates/equipment-tracking.md` | 诊断配置与标定追踪 |

将模板文件复制到你的 Obsidian vault 对应位置即可使用。

## 参考示例

`references/` 目录包含放电日志完整示例：

| 文件 | 类型 |
|------|------|
| `references/example-discharge.md` | 完整放电日志示例（虚构 shot，格式演示） |

示例包含完整的 YAML frontmatter 和 Markdown 正文，可直接作为模板修改使用。

## 可选的飞书 CLI 集成

需要从飞书群获取材料时，使用 `feishu-cli-integration` skill：

- 拉消息：`lark-cli im +chat-messages-list --chat-id oc_*** --page-size 30 --sort asc`
- 下载图片：`lark-cli im +messages-resources-download --message-id *** --file-key *** --type image --output <相对路径>`
- ⚠️ `--output` 只接受相对路径，先 `cd` 到 `raw/discharges/` 归档目录

群 ID 和 bot 权限按 `feishu-cli-integration` skill 的配置获取。

## 自定义指南

- **装置**：按你的实验装置（EAST / DIII-D / KSTAR / W7-X / JET …）在 `wiki/放电日志/{装置}/` 下建目录
- **YAML 字段**：模板是建议结构，可增删字段（如补 β_N、q_95、储能 W_MHD）
- **诊断清单**：按装置实际启用的诊断扩展
- **输出根目录**：可以是普通本地文件夹，也可以是 Obsidian vault 根目录

## 相关文件

| 文件 | 用途 |
|------|------|
| `references/example-discharge.md` | 完整放电日志示例 |
| `wiki/放电日志/放电索引.md` | Dataview 仪表盘（shot 清单） |
| `wiki/放电日志/异常记录.md` | 破裂/异常放电记录格式 |
| `wiki/放电日志/公共/诊断配置记录.md` | 诊断配置与标定追踪 |
| `../fusion-shared/core/parameter-definitions.md` | 参数符号/单位/定义 |
| `../fusion-shared/core/machine-database.md` | 装置参数库 |
