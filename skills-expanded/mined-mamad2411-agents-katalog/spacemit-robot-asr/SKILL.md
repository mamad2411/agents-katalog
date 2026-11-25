---
name: spacemit-robot-asr
description: components/model_zoo/asr 的构建、PR 测试、模型可选 smoke、C++/Python ASR API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/model_zoo/asr
    primary_docs:
      - components/model_zoo/asr/README.md
      - components/model_zoo/asr/test.yaml
      - components/model_zoo/asr/package.xml
      - components/model_zoo/asr/include/asr_service.h
    build_hint: single_package_first
---

# SpacemiT Robot ASR

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、测试或调试 `components/model_zoo/asr`。
- 用户要接入 `include/asr_service.h`、Python `spacemit_asr`、SenseVoice、Zipformer 或 Qwen3-ASR。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/model_zoo/asr`。
- PR 测试只验证 presets、config validator、音频 chunk 和错误路径，不要求模型。
- 有模型或 Qwen3-ASR 服务时才跑真实识别 smoke；缺模型不能作为 PR 失败。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 构建时执行 `cd components/model_zoo/asr && mm`。
4. 测试前执行 `./scripts/test/robot-test list components/model_zoo/asr`。
5. PR 验证执行 `./scripts/test/robot-test run components/model_zoo/asr --scope pr`。
6. 用户要求真实识别时，先检查模型、demo/wheel 或远端服务是否存在。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令并返回命令、结果、日志路径和失败点。

## 禁止事项

- 不要把模型下载、真实语音识别或音频设备依赖放进 PR 必跑条件。
- 不要默认写死 target；需要 target 时按 shared 规则确认。
- 不要在缺模型或缺服务时伪造识别结果。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 ASR | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/model_zoo/asr && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/model_zoo/asr` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/model_zoo/asr --scope pr` |
| 检查 SenseVoice 模型 | `test -d ~/.cache/models/asr/sensevoice && echo found || echo missing` |
| Python 导入检查 | `python -c "import spacemit_asr; print(spacemit_asr.__version__)"` |
