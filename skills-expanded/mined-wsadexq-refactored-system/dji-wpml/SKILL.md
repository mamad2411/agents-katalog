---
name: dji-wpml
description: 处理大疆 WPML 航线文件（template.kml / waylines.wpml / .kmz 归档）的生成、解析、修改与校验。当用户提到"大疆航线文件""DJI wayline""WPML""KMZ 航线""template.kml""waylines.wpml"、或要求生成/解析/修改/检查航点、建图航拍、倾斜摄影、航带飞行、目标检测巡逻等航线文件时使用。
---

# DJI WPML 航线文件

WPML（WayPoint Markup Language）是大疆基于 KML 2.2 扩展的航线文件格式标准，航线文件一律以 `.kmz` 后缀归档（ZIP 格式）。本技能帮助你按已整理的规则生成、解析和修改航线文件，并用校验脚本检查已覆盖的结构与字段；脚本不覆盖全部规则、资源引用或机型兼容性，正式开发仍须以对应官方文档为准。

## 安装后的路径与文档定位

- 从已加载技能的实际目录读取 `reference/`，并使用该目录下脚本的绝对路径执行命令；任务当前目录不一定是技能目录。
- 安装版自带 `KNOWLEDGE_SOURCES.md`、`THIRD_PARTY_NOTICES.md` 与 `INSTALLATION.md`；源码模式的这些文件在仓库根目录。不要假设安装版父目录仍是源码仓库。
- 深度查询前，运行安装版 `scripts/locate_dji_docs.py`（源码模式用仓库根目录的同名脚本）。用户明确提供路径时传 `--docs-root`；否则依次检查 `DJI_CLOUD_API_DOCS` 和任务当前目录的 `docs/Cloud-API-Doc`。明确配置无效时停止回退并报告。
- 定位成功仅证明路径存在；核对官方目录 Git HEAD 与来源说明基准后，再读取对应官方章节。未核对时不声称是最新或固定版本。
- 缺少官方文档时可依据现有笔记解释和运行离线校验，明确说明来源及覆盖范围；无法核实的字段或兼容性请用户提供官方目录，不猜测、不自动联网下载。

## 何时使用

- 生成新的航线文件（航点飞行 / 建图航拍 / 倾斜摄影 / 航带飞行 / 目标检测巡逻）
- 解析或修改已有的 `template.kml` / `waylines.wpml`
- 打包或解包 `.kmz` 归档
- 校验航线文件是否合法、能否被 DJI Pilot 2 / 司空 2 正确解析

## 基础知识

### 文件结构

一个标准 WPML `.kmz` 解压后包含：

| 文件/目录 | 名称 | 职责 |
|---|---|---|
| `template.kml` | 模板文件 | 定义业务属性，方便用户快速调整编辑（测区、重叠率、模板参数） |
| `waylines.wpml` | 执行文件 | 定义明确的飞行与负载动作指令，由软件依据模板参数演算生成，供无人机执行 |
| `res/` | 资源目录 | 航线所需辅助资源（精准复拍参考照片 / 目标检测区域 / 仿地 DSM 高程） |

航线名称即文件名（`new_waypoints.kmz` 的航线名是 `new_waypoints`）。**内部各文件/文件夹命名必须遵循此规范，否则航线文件读取失败。**

### XML 头部与命名空间（两个文件都必须）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:wpml="http://www.dji.com/wpmz/1.0.2">
```

### 两种高度体系（最容易出错，务必分清）

- **template.kml 用 `wpml:heightMode` + `wpml:height`**（编辑体系）：`EGM96`（海拔高）/ `relativeToStartPoint`（相对起飞点）/ `aboveGroundLevel`（AGL，仅司空2）/ `realTimeFollowSurface`（实时仿地，仅建图航拍模版，M3E/M3T/M3M）
- **waylines.wpml 用 `wpml:executeHeightMode` + `wpml:executeHeight`**（执行体系）：`WGS84`（椭球高）/ `relativeToStartPoint`（相对起飞点高）/ `realTimeFollowSurface`（仅 M3E/M3T/M3M）
- `ellipsoidHeight` 与 `height` 是同一位置不同高程参考平面的表达，需配合使用
- 若数据来自非椭球坐标系（如 EGM96），转换为 WGS84 需做高程转换，否则飞行高度不准

## 硬性规则

1. **文件头**：XML 声明必须是 `<?xml version="1.0" encoding="UTF-8"?>`，根元素必须是带上述两个命名空间的 `<kml>`
2. **航点序号**：`wpml:index` 必须从 0 开始**单调连续递增**，在一条航线内唯一，范围 [0, 65535]
3. **模板/航线/动作 ID**：`wpml:templateId`、`wpml:waylineId`、`wpml:actionGroupId`、`wpml:actionId` 建议从 0 开始单调连续递增，范围 [0, 65535]
4. **必需字段**：`missionConfig` 下的 `flyToWaylineMode`、`finishAction`、`exitOnRCLost`、`takeOffSecurityHeight`、`globalTransitionalSpeed`、`globalRTHHeight` 必填；`droneInfo`/`payloadInfo` 必填
5. **枚举值**：所有枚举字段必须使用官方文档定义的值（如 `finishAction` 只能是 `goHome`/`noAction`/`autoLand`/`gotoFirstWaypoint`），禁止自造枚举
6. **坐标格式**：`<coordinates>经度,纬度</coordinates>`（经度在前、纬度在后），经度 [-180,180]、纬度 [-90,90]
7. **条件必需**：注意"当且仅当"类规则，例如 `wpml:height`/`ellipsoidHeight` 仅在 `useGlobalHeight=0` 时必需，`waypointSpeed` 仅在 `useGlobalSpeed=0` 时必需，`executeRCLostAction` 仅在 `exitOnRCLost=executeLostAction` 时必需
8. **数值范围**：速度 [1,15] m/s、`takeOffSecurityHeight` 遥控器 [1.2,1500]/机场 [8,1500] m、重叠率 [0,100] 等，超范围值会导致解析失败
9. **生成后必须校验**：生成或修改文件后，运行 `scripts/validate_wayline.py` 检查

校验脚本检查已实现的结构、字段、有限数值及 KMZ 内 `templateId` 关联，不覆盖全部规则、资源引用或机型兼容性。通过后仍须按对应参考文档核对未覆盖字段。

## 安全与隐私边界（重要）

本技能会生成**实际控制无人机飞行的航线文件**，以下边界必须严格执行，不能只依赖校验脚本：

1. **执行前用户确认**：航线执行前，必须由用户确认坐标、飞行高度、返航高度（`globalRTHHeight`）、失控动作（`exitOnRCLost`/`executeRCLostAction`）等关键参数
2. **不写入用户真实航线**：不得把用户提供/导出的真实航线数据写入示例文件或文档；示例必须使用虚构坐标
3. **脱敏义务**：坐标、设备 SN、Token、密钥、日志等敏感信息在输出前必须先脱敏（替换为占位符或虚构值）
4. **高风险动作再次确认**：涉及远程起飞、返航、指飞、目标检测等动作时，必须再次向用户确认后才能执行
5. **校验通过 ≠ 飞行安全**：`validate_wayline.py` 只验证格式与字段合法性，不代表飞行安全或符合当地法规；生成者需自行确认作业区域适航性
6. **不主动提权**：未经用户明确要求，不得尝试连接设备、读取日志或进行任何网络操作

## 工作流

1. 明确用户要生成哪种模板：`waypoint`（航点飞行）/ `mapping2d`（建图航拍）/ `mapping3d`（倾斜摄影）/ `mappingStrip`（航带飞行）/ `targetdetection`（目标检测巡逻）
2. 按需加载对应参考文档（见下方"按需加载"）
3. 生成文件内容，遵守上述硬性规则
4. 用校验脚本验证：`python scripts/validate_wayline.py <file>`
5. 如需打包 KMZ，用 `python scripts/package_kmz.py <template.kml> <waylines.wpml> -o <输出.kmz> [--res <res目录>]`（详见 `reference/kmz-archive.md`）

## 按需加载

- **要核对来源或适用版本** → 查看所用参考文档顶部的来源分类、固定提交基准与适用范围；完整更新流程见仓库 `KNOWLEDGE_SOURCES.md`。本地文档未同步时不得声称使用最新规范；目标检测导出观察缺少版本证据，不作为通用官方规则
- **要生成或修改 template.kml** → 加载 `reference/template-kml.md`
- **要生成或修改 waylines.wpml** → 加载 `reference/waylines-wpml.md`
- **要查询共用元素**（droneInfo/payloadInfo/actionGroup/偏航角/转弯参数/动作参数） → 加载 `reference/common-elements.md`
- **要打包/解包 KMZ 归档** → 加载 `reference/kmz-archive.md`（配合 `scripts/package_kmz.py` 打包、`scripts/validate_wayline.py` 校验）
- **涉及目标检测巡逻（targetdetection）** → 加载 `reference/template-kml.md` + `reference/common-elements.md` + `reference/kmz-archive.md`（`res/area` 区域与 `res/dsm` 高程）

## 模板速查

| 模板 | `wpml:templateType` | 关键结构 |
|---|---|---|
| 航点飞行 | `waypoint` | `Folder` 下多个 `Placemark(Point)`，每个含 `index`/高度/速度/偏航/转弯参数，可挂 `actionGroup` |
| 建图航拍 | `mapping2d` | `Placemark` 内 `Polygon` 定义测区，含 `overlap`/`direction`/`margin`/`shootType`/`height` 等 |
| 倾斜摄影 | `mapping3d` | 同建图航拍，另有 `inclinedGimbalPitch`/`inclinedFlightSpeed`，生成 5 条航线（1 正射 + 4 倾斜） |
| 航带飞行 | `mappingStrip` | `LineString` 定义航带，含 `singleLineEnable`/`cuttingDistance`/`leftExtend`/`rightExtend` 等 |
| 目标检测巡逻 | `targetdetection` | 测区 `Polygon` + `targetDetectionActionEnable` + `targetDetection` 动作（含 `targetParam` 模型参数），可选仿地（`dsmFile`） |
