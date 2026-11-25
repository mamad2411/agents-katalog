---
name: app-ui-spec-gen-zh
description: 自然语言 → specs/app/draft + run_code_app。不执行真机。由 app-ui-orchestrator 调用；生成前先复用检测。
disable-model-invocation: true
---

# App 用例生成（NL → draft）

**只生成文件**。执行由 **app-ui-nl2spec-zh** / `run_app_case.py`。

**生成前**：编排 Step 0 + [reuse-matrix.md](../app-ui-orchestrator-zh/reference/reuse-matrix.md)；未命中才新建。

**必读**：[app-pitfalls-zh.md](../app-ui-orchestrator-zh/reference/app-pitfalls-zh.md)

## 输出

| 产物 | 路径 |
|------|------|
| 草案 spec | `specs/app/draft/<runId>-<slug>.json` |
| 业务脚本 | `scripts/run_code_app/`（优先扩展现有，见 reuse-matrix） |

脚本依赖关系：见项目根 `README.zh-CN.md` §脚本入口

## 生成规则

1. [app-case-spec-schema.md](../app-ui-nl2spec-zh/reference/app-case-spec-schema.md)
2. 参考 Demo：`examples/app/specs/demo-open-settings-wifi.json`
3. 根字段：`平台": "android"`、`用例名称`、`用例说明`、`启动配置`、`步骤`
4. `启动配置": "@examples/app/launches/android-settings.json"`（或自建 `specs/app/launches/`)
5. 操作：`启动应用`、`点击`、`填写`、`等待`、`断言*`、`截图`、`执行代码`
6. 长流程 → **执行代码** + `run_code_app`；文本逻辑放 `app_text_input` / 脚本内

## 用例说明模板

```
1.步骤摘要… 2.…
启动: @examples/app/launches/android-settings.json
记录: flow-records.json
执行: python scripts/run_app_case.py specs/app/draft/<runId>-<slug>.json
```

## 校验与交接

```bash
python scripts/tools/validate_app_spec.py specs/app/draft/<runId>-<slug>.json
python scripts/tools/probe_app_input.py
python scripts/run_app_case.py specs/app/draft/<runId>-<slug>.json
```

生成阶段**勿**写 `--launch`（除非用户要求冷启动验证）。

## 禁止

- 不默认跑真机、不写终版 `specs/app/`、不用 Appium
- 未查 reuse-matrix 就新建平行 `run_code_app`
