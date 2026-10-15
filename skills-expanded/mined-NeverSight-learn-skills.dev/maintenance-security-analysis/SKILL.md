---
name: maintenance-security-analysis
description: 使用 cloudpss-psa-core 对 CloudPSS 模型执行检修方式下的剩余 N-1 稳态安全校核，通过真实潮流仿真比较正常方式、检修方式和检修叠加线路退运场景，输出电压越限、支路应力、损耗变化和风险排序。当用户需要检修计划安全校核、停运方式下剩余 N-1、计划停电风险评估或检修方式潮流分析时使用。
license: Internal Use Only
compatibility:
  python: ">=3.11"
  requires_env: true
  required_env_vars:
    - SIMSTUDIO_TOKEN
    - CLOUDPSS_API_URL
  notes: The verification script runs real CloudPSS power flow against model/CloudPSS/IEEE39 by default.
metadata:
  owner: cloudpss-team
  category: analysis
  visibility: internal
  maturity: experimental
  entrypoint: scripts/verify_maintenance_security_analysis.py
  dependency_strategy: hybrid
  shared_packages:
    - cloudpss-psa-core
  verification_method: direct_cloudpss_powerflow_maintenance_n1
---

# Maintenance Security Analysis

## When to use

- 需要评估一条线路计划检修后的稳态运行风险。
- 需要在检修方式下继续筛查剩余 N-1 线路退运。
- 需要比较正常方式、检修方式、检修叠加事故方式的电压和损耗变化。
- 需要为检修计划输出最严重剩余事故排序。

## Workflow

1. 调用 `initModelAndCreateSACanvas(cloudpss_model=...)` 初始化真实模型。
2. 运行正常方式潮流，读取母线电压、支路功率和网损摘要。
3. 选择检修线路，默认使用第一条真实交流线路，也可通过 `CLOUDPSS_MAINTENANCE_LINE_KEY` 指定。
4. 在本地工作副本中使用 `project.removeComponent(line_key)` 退运检修线路，并运行真实 CloudPSS 潮流。
5. 在检修方式基础上继续选择剩余候选线路，逐个退运并运行真实潮流。
6. 对每个剩余 N-1 场景统计电压越限、支路 MVA 应力、损耗变化和收敛状态。
7. 生成 `residual_severity_ranking`，按严重度排序。

## Output

- `normal_case`: 正常方式潮流摘要。
- `maintenance_line`: 检修线路元数据。
- `maintenance_case`: 检修方式潮流摘要和相对正常方式的变化。
- `residual_contingencies`: 检修叠加剩余线路退运场景结果。
- `residual_severity_ranking`: 检修方式下最严重剩余 N-1 排序。
- `unsupported`: 当前建模和热稳数据限制说明。

## Constraints

- 默认验证使用官方 `model/CloudPSS/IEEE39`，不依赖个人账号模型。
- 默认只筛查少量剩余线路，数量由 `CLOUDPSS_MAINTENANCE_SECURITY_LIMIT` 控制，默认 2。
- 检修和剩余 N-1 均通过本地工作副本删除线路组件建模，不会保存或污染云端原始模型。
- 热稳百分比只有在支路组件包含 `Irated` 和 `Vbase` 等额定值时才输出，否则以 MVA 应力排序替代。
- maturity 标为 `experimental`，因为“线路删除”等价于“停运”的语义还需要在更多模型中验证。

## Verified script

- `skills/maintenance-security-analysis/scripts/verify_maintenance_security_analysis.py`
