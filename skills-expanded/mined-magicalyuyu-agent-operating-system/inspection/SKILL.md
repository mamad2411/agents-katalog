---
name: inspection
description: "[治理] 定期巡检/缓存清理/系统健康度检查时使用。触发条件：用户要求巡检、清理缓存、检查健康度；或距上次轻审超过 4 周；或距上次深审超过 12 周。社区调研后从季度制改为双频制。"
---

# 巡检（v2.1 实测版）

## 一键巡检（标准入口）

```bash
# 结构+落位合规（自动跑完 5 项检查）
python scripts/check_placement.py

# 环境对齐+能力抽检
python scripts/align_environment.py

# 多机协同（可选扩展）：状态速览见 docs/design-rationale.md 扩展点说明
```
两个命令跑完 = 巡检框架层完成 80%。人工判断只处理违规项。

## 深度巡检（手动触发，12 周级）

1. **缓存生命周期**：上述脚本输出 + 05_CACHE 创建时间超 90 天条目 → 清理清单 → 用户确认 → 归档/删除
2. **宪章合规**：check_placement 已覆盖四禁令+根层+07 孤立；补充检查 08_INBOX 未归位存量
3. **AGENTS.md 防蠕变**：行数 ≤200；**逐条打标四分类**（ACTIVE/REDUNDANT/CONFLICTED/UNKNOWN，社区调研吸收）→ REDUNDANT/CONFLICTED 条目删除或合并 → 新增规则前先问"能否删一条旧的？"
4. **引用健康**：grep 活文档对已归档路径（历史归档目录）的残留引用
5. **gotchas 审计**：各 skill gotchas 是否有重复/过时条目（合并入对应 skill 或删除）
6. **skill 触发率回顾**：在 06_LOGS/aos/ 各日志中 grep 每个 skill 名（如 `grep "file-placement" 06_LOGS/aos/*.log`），统计最近 30 天提及次数。零提及 = 巡检候选（检查 description 触发词是否模糊或该 skill 是否已无场景）。**注意"很少用≠没用"**——应急类 skill 低频是正常的
7. **TIE 监控**（工具调用膨胀检测，上下文退化先导指标）：对比最近 3 个同类任务的工具调用次数，如果环比增长 >50% → 上下文可能退化（指令不清晰导致反复尝试），触发冲刷或压缩
8. 输出一页报告至 07_EXPORTS/aos_system/，事件记 06_LOGS/aos/

## 巡检范围铁律

仅框架层面，不深入 01_PROJECTS 各项目 src/ 内部

## gotchas

- 08_INBOX 中未归位内容：先问"归宿在哪"（项目 docs/、09_REFERENCE、归档），迁移后在原处留去向指针
- 清理清单交低成本批量模型执行，主会话复核 manifest
- 巡检自身低频（双频制），不要做成常驻仪式——v1 的每日巡检制度死于执行成本
