---
name: tracking-setup-e2e
description: 客户新项目启动或新业务场景需要完整数据采集和分析能力时使用
---

# 埋点全链路交付

## 适用场景

- 客户新项目启动，需要从零建立数据采集体系
- 现有业务新增功能，需要补充埋点和分析看板
- 需要将测试环境配置迁移到客户生产环境

## 核心原则（Iron Law）

**必须先完成采集方案设计并经客户确认，再进行后续任何步骤。**

不允许在方案未确认的情况下造数或创建看板。违反此原则会导致返工。

**已有方案时的快速入口：**

| 用户说 | 从哪里开始 |
|--------|-----------|
| 已有确认好的埋点方案 Excel | Phase 3a（生成 business_logic.yaml） |
| 已有 business_logic.yaml | Phase 3b（验证） |
| YAML 已验证通过，要造数 | Phase 3c（造数） |
| 已造好数据，要导入 CDP | Phase 4a |
| 已导入元数据，要造数 | Phase 3 |
| 只需要迁移资产 | Phase 5 |

开始前直接问用户："你现在在哪个阶段？有没有已确认的埋点方案文件？"

## 前置条件

### 项目启动时（一次性配置）

**方式1：命令行参数（推荐，Agent 使用）**
直接在使用脚本时通过参数传递，无需配置文件。

**方式2：.env 配置文件**
在项目根目录复制 `.env.example` 为 `.env`：
```bash
cp .env.example .env
# 编辑 .env，填入相应配置
```

**方式3：交互式提示**
直接运行脚本，根据提示输入配置。

### 配置说明

| 配置项 | 说明 | 示例 | 获取方式 |
|--------|------|------|----------|
| **CDP 地址** | 神策控制台地址 | `https://demo.sensorsdata.cn` | 登录神策后浏览器地址栏 |
| **项目 ID** | 项目标识 | `default` | 登录后 URL 中 `project=` 的值 |
| **Open API 密钥** | 元数据管理密钥 | `#K-jHllJkc...` | 神策后台 → 系统管理 → API 密钥 |
| **数据接收地址** | 数据导入地址 | `https://demo.sensorsdata.cn/sa?project=default` | 神策后台 → 数据接入 → HTTP API |
| **埋点方案路径** | Excel 文件路径 | `./refrences/plan.xlsx` | 客户提供的埋点方案 |

> **注意区分**：
> - **Open API 密钥**：用于元数据导入（创建事件、属性），在「系统管理 → API 密钥」获取
> - **数据接收地址**：用于数据导入，在「数据接入 → HTTP API」获取，是一个完整的 URL

## 执行阶段

### Phase 1：业务目标确认 👤

收集以下信息后才能进入 Phase 2：
- 核心业务场景（用户注册/购买/使用路径等）
- 需要回答的关键业务问题（转化率？留存？活跃度？）
- 分析维度（渠道、用户分群、时间粒度）
- 数据消费方（运营/产品/数据分析师）

输出：业务目标确认单（一页，列出以上四项）

### Phase 2：采集方案设计 👤

基于 Phase 1 输出，设计埋点方案：
- 事件列表（事件名、中文名、触发时机）
- 每个事件的属性列表（属性名、类型、示例值、是否必填）
- 用户属性列表（属性名、类型）

**等待客户确认后才能进入 Phase 3。确认后在 `.env` 中设置 `TRACKING_PLAN_PATH`。**

输出：埋点方案表（Excel，包含 Events / Details（Event） / Users 三个 sheet）

### Phase 3：模拟数据生成 🤖

Phase 3 分三步：生成业务规则 YAML → 验证 → 造数。

#### Step 3a：生成 business_logic.yaml

**这一步由你（agent）完成，不是调脚本。**

读取 `tracking-setup-e2e/rules/YAML_GENERATION_PROMPT.md`，按其中的指南生成 YAML 文件，保存到：

```
tracking-setup-e2e/rules/special/<project_name>/business_logic.yaml
```

两种情况：
- **有业务需求文档**（docx/描述）：读文档提取业务逻辑，结合 Tracking Plan 事件名填写完整 YAML
- **无业务文档**：使用 `YAML_GENERATION_PROMPT.md` 中的默认模板，替换事件名和 `meta.project`

#### Step 3b：验证 YAML

```bash
python3 tracking-setup-e2e/scripts/yaml_validator.py \
  tracking-setup-e2e/rules/special/<project_name>/business_logic.yaml \
  --tracking-plan "<TRACKING_PLAN_PATH>"
```

- 有 **error**：修复 YAML，重新验证，直到 PASSED
- 有 **warning**：逐条确认是否是真实问题，无误后继续
- **PASSED**：进入 Step 3c

#### Step 3c：造数

先询问用户数据规模需求，然后运行：

```bash
# 固定测试账号（UAT 场景验证，默认）
python3 tracking-setup-e2e/scripts/generate_mock_data.py \
  --rules tracking-setup-e2e/rules/special/<project_name>/business_logic.yaml \
  --tracking-plan "<TRACKING_PLAN_PATH>"

# 批量随机用户（大数据量，指定用户数/天数/每日 session 数）
python3 tracking-setup-e2e/scripts/generate_mock_data.py \
  --rules tracking-setup-e2e/rules/special/<project_name>/business_logic.yaml \
  --tracking-plan "<TRACKING_PLAN_PATH>" \
  --users 100 --days 30 --sessions-per-day 5
```

**数据规模参考：**

| 场景 | 参数 | 约估事件量 |
|------|------|-----------|
| UAT 场景验证 | 默认（固定账号） | ~50–100 条 |
| 功能测试 | `--users 50 --days 7` | ~3,000 条 |
| 漏斗/留存分析 | `--users 100 --days 30 --sessions-per-day 5` | ~14 万条 |
| 压测 | `--users 500 --days 30 --sessions-per-day 10` | ~140 万条 |

输出文件（在 `tracking-setup-e2e/mock_data/` 下）：
- `<project>.jsonl` — 每行一条记录
- `<project>_batch.txt` — base64 编码，可直接 POST
- `<project>_identity_map.csv` — 用于校验 ID-Mapping 合并结果
- `uat_validation_report.md` — 业务规则违规报告

### Phase 4a：元数据导入 CDP 🤖

**方式1：命令行参数（推荐，Agent 使用）**
```bash
python3 tracking-setup-e2e/scripts/import_meta_data.py \
  --cdp-url https://demo.sensorsdata.cn \
  --project default \
  --api-key "#K-jHllJkcPOMeRke3Vi5Nokeuc1MDlRZls" \
  --tracking-plan "./refrences/tracking-plan.xlsx"
```

**方式2：交互式提示（手动运行）**
```bash
python3 tracking-setup-e2e/scripts/import_meta_data.py
# 脚本会提示输入各项配置，并给出示例
```

**方式3：.env 配置**
```bash
# 编辑 .env 文件，然后直接运行
python3 tracking-setup-e2e/scripts/import_meta_data.py
```

脚本自动完成：
1. 检查 API 连接
2. 从 Excel 读取事件列表，逐个创建元事件
3. 读取事件属性，写入对应事件
4. 读取用户属性，批量写入

注意：系统保留字段名（如 `Id`、`PersonEmail`）会自动跳过并在输出中列出。

### Phase 4b：模拟数据导入 🤖

**方式1：命令行参数（推荐）**
```bash
python3 tracking-setup-e2e/scripts/import_mock_data.py \
  --data-url "https://demo.sensorsdata.cn/sa?project=default" \
  --jsonl "./mock_data/westk.jsonl"
```

**方式2：自动查找最新数据文件**
```bash
python3 tracking-setup-e2e/scripts/import_mock_data.py \
  --data-url "https://demo.sensorsdata.cn/sa?project=default"
# 会自动查找 mock_data/ 目录下最新的 .jsonl 文件
```

**方式3：交互式提示**
```bash
python3 tracking-setup-e2e/scripts/import_mock_data.py
# 脚本会提示输入数据接收地址
```

### Phase 4c：看板创建 👤

按业务目标创建看板，参考 cdp-operations skill。截图存档。

### Phase 5：资产迁移 🤖

使用神策资产项工具将配置元数据从测试环境迁移到客户生产环境：
1. 导出测试环境资产（看板、标签、事件定义）
2. 检查资产依赖关系
3. 导入客户生产环境
4. 验证迁移结果

输出：资产迁移记录（迁移项清单 + 验证截图）

## 输出模板

```
## 交付物清单

- [ ] 业务目标确认单
- [ ] 埋点方案表（已客户确认）
- [ ] 模拟数据文件
- [ ] 元数据导入确认（import_meta_data.py 输出日志）
- [ ] 看板截图
- [ ] 资产迁移记录
```

## 常见问题

**客户说"先做再确认"：** 坚持 Phase 2 确认门。方案变更后造数和看板全部作废，返工成本远高于等待确认的时间。

**import_meta_data.py 报"缺少必要配置"：** 检查项目根目录是否有 `.env` 文件，以及对应变量是否已填写。

**import_meta_data.py 报"登录态导入失败"：** 确认 Chrome 中已登录目标神策环境（`SA_HOST` 对应的域名）。

**字段创建报 ALREADY_EXISTS：** 正常，脚本自动跳过，不影响其他字段。

**元事件属性写入失败（10005 错误）：** 通常是事件上有特殊关联字段，脚本已自动处理常见情况。如仍报错，检查事件是否有虚拟字段依赖。

**模拟数据不够真实：** 向客户要 1-2 个真实业务场景的描述，更新 `business_logic.yaml` 中的 `event_sequences`，重新验证后造数。

**yaml_validator.py 报 event not found：** YAML 中的事件名与 Tracking Plan 不一致。运行 `python3 -c "import sys; sys.path.insert(0,'scripts'); from tracking_plan import TrackingPlan; [print(e) for e in TrackingPlan('<xlsx>').list_events()]"` 获取合法事件名列表。

**yaml_validator.py 报 ratios sum to X：** 检查 `user_segments` 或 `region_distribution` 各项比例，确保加总精确为 1.0。
