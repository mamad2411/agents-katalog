---
name: spacemit-robot-tts
description: components/model_zoo/tts 的构建、PR 测试、模型可选 smoke、C++/Python TTS API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/model_zoo/tts
    primary_docs:
      - components/model_zoo/tts/README.md
      - components/model_zoo/tts/test.yaml
      - components/model_zoo/tts/package.xml
      - components/model_zoo/tts/include/tts_service.h
    build_hint: single_package_first
---

# SpacemiT Robot TTS

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、测试或调试 `components/model_zoo/tts`。
- 用户要接入 `include/tts_service.h`、Python `spacemit_tts`、Matcha 或 Kokoro TTS。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/model_zoo/tts`。
- PR 测试只验证 presets、builder、音频 chunk 转换和错误路径，不要求模型。
- 有模型和 demo/wheel 时才跑真实合成 smoke；缺模型不能作为 PR 失败。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 构建时执行 `cd components/model_zoo/tts && mm`。
4. 测试前执行 `./scripts/test/robot-test list components/model_zoo/tts`。
5. PR 验证执行 `./scripts/test/robot-test run components/model_zoo/tts --scope pr`。
6. 用户要求真实合成时，先检查模型、demo/wheel 和输出目录。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令并返回命令、结果、日志路径和失败点。

## 禁止事项

- 不要把模型下载、真实语音合成或音频播放依赖放进 PR 必跑条件。
- 不要默认写死 target；需要 target 时按 shared 规则确认。
- 不要在缺模型或缺样本文本时伪造音频结果。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 TTS | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/model_zoo/tts && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/model_zoo/tts` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/model_zoo/tts --scope pr` |
| 检查 Matcha 模型 | `test -d ~/.cache/models/tts/matcha-tts && echo found || echo missing` |
| Python 导入检查 | `python -c "import spacemit_tts; print(spacemit_tts.__version__)"` |
