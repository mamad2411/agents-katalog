---
name: app-ui-spec-from-record-zh
description: 子 Skill：将 runs/app/manual-*/steps.jsonl 转为 specs/app/draft JSON 与 run_code_app 建议。触发词：录制生成用例、finalize、根据录制、steps.jsonl 转 spec。
disable-model-invocation: true
---

# 录制 → 测试用例草案

由 **app-ui-record-orchestrator-zh** 在「停止录制」后调用。

## 生成命令

```bash
python scripts/tools/record_app_manual.py --finalize runs/app/manual-<runId>-<slug> --name "demo-settings-wifi"
```

产出：

- `runs/app/manual-.../generated-spec.json`
- `runs/app/manual-.../操作步骤.md`
- `specs/app/draft/<runId>-<slug>.json`

## 校验

```bash
python scripts/tools/validate_app_spec.py specs/app/draft/<runId>-<slug>.json
```

## 录制 → spec 转换规则（Agent 必须校对）

1. **以真实手势为准**：读 `steps.jsonl` 的 `操作类型`、`手势`、`定位`、`控件`
2. **剔除噪音步**：`Activity` 含 `launcher`、包名非目标 App 的步骤删除
3. **分层步骤**：
   - 稳定短文案 → `点击` + `稳定定位值: text:xxx`
   - 底部 Tab、OEM 差异菜单 → `执行代码` + `@scripts/run_code_app/...`
4. **优先复用 Demo 脚本**：`examples/app/run_code_app/demo_tap_wifi.py`

## 草案结构

参考 `examples/app/specs/demo-open-settings-wifi.json`：

- `平台`: `android`
- `启动配置`: `@examples/app/launches/android-settings.json`
- 末步：`断言当前包名` → `com.android.settings`

## 禁止

- 未校对直接 promote 终版
- Appium
