---
name: app-ui-heal-zh
description: 子 Skill：App 失败后自愈，改 draft/run_code_app 重跑。默认最多 20 轮（HEAL_MAX_ROUNDS 可调）。触发词：App 自愈、定位失败、登录失败、剪贴板、u2 Timeout。
disable-model-invocation: true
---

# App 用例失败自愈

由 **app-ui-orchestrator-zh** 调用；与 **playwright-ui-heal-zh** 对称，**只改 App draft**。

## 轮次上限

- 默认 **20 轮**（环境变量 `HEAL_MAX_ROUNDS`；代码常量 `MAX_HEAL_ROUNDS` 见 `scripts/framework/pipeline.py`）
- 用户要求更多：设 `HEAL_MAX_ROUNDS=50` 等；**跑通即停**

**必读**：[app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md)

## 何时用

- `run_app_case` 非 0 退出
- 日志成功但界面未变
- 编排迭代：改 `specs/app/draft/`，勿动终版直至 promote

## 输入（按序）

1. **`runs/app/<runId>/heal-context.json`**（推荐）
2. `runs/app/<runId>/failure.json`
3. `runs/app/<runId>/steps/flow-records.json`
4. `runs/app/<runId>/run-log.md` 与 `steps/*.png`
5. 终端 adb / u2 报错

## 分诊树

1. **包名不对 / 停在桌面** → 检查 `启动配置`、是否需 `--launch`
2. **text / resourceId 找不到** → dump 核对；改用 `textContains`、等待、滚动
3. **u2 Timeout** → 加 `等待`、关动画；调试首轮勿 `--fast`
4. **Wi-Fi / WLAN 菜单文案** → 编辑 `demo_tap_wifi.py` 候选列表
5. **剪贴板 / IME 工具栏** → `app_text_input.write_text_to_field`；`probe_app_input.py`
6. **红圈位置偏** → 检查横屏/分辨率

## 自愈策略（轮次）

| 轮次 | 策略 |
|------|------|
| 第 1 轮 | 读 flow-records + 分诊树；最小改动 |
| 第 2 轮起 | **优先分段脚本** |

```bash
python examples/app/run_code_app/demo_tap_wifi.py
```

通过后再 `run_app_case` 全量回归。

## 重跑命令

```bash
python scripts/run_app_case.py specs/app/draft/<file>.json
python scripts/run_app_case.py specs/app/draft/<file>.json --launch   # 仅怀疑进程卡死
python scripts/run_app_case.py specs/app/<用例名称>.json              # 终版回归
```

## 完成定义

- 退出码 0
- `flow-records.json` 符合用户 NL
- `reports/app/.../report.html` 步骤与截图符合目标
