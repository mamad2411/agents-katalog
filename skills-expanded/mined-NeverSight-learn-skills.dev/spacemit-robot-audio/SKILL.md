---
name: spacemit-robot-audio
description: components/multimedia/audio 的构建、PR 测试、手动音频设备 smoke 与 C++/Python API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/multimedia/audio
    primary_docs:
      - components/multimedia/audio/README.md
      - components/multimedia/audio/test.yaml
      - components/multimedia/audio/package.xml
      - components/multimedia/audio/include/audio_base.hpp
    build_hint: single_package_first
---

# SpacemiT Robot Audio

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、测试或调试 `components/multimedia/audio`。
- 用户要接入 AudioCapture、AudioPlayer、Duplex、resampler 或 Python `spacemit_audio`。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/multimedia/audio`。
- PR 测试只验证 resampler 和无设备错误路径，不要求麦克风或扬声器。
- 真实录音/播放只能在确认设备和人工看护后设置 `AUDIO_MANUAL_RUN=1` 跑 `manual` scope。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 构建时执行 `cd components/multimedia/audio && mm`。
4. 测试前执行 `./scripts/test/robot-test list components/multimedia/audio`。
5. PR 验证执行 `./scripts/test/robot-test run components/multimedia/audio --scope pr`。
6. 用户要求真实设备测试时，执行 manual scope 前先列出 ALSA 设备并说明会录音或播放；没有设备时不要运行 manual。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令并返回命令、结果、日志路径和失败点。

## 禁止事项

- 不要在 PR 测试里依赖真实音频设备。
- 不要默认写死 target；需要 target 时按 shared 规则确认。
- 不要在未确认人工看护时播放音频或占用麦克风。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 audio | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/multimedia/audio && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/multimedia/audio` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/multimedia/audio --scope pr` |
| 跑手动设备 smoke | `cd "$SROBOTIS_ROOT" && AUDIO_MANUAL_RUN=1 ./scripts/test/robot-test run components/multimedia/audio --scope manual` |
| 列出设备 | `arecord -l && aplay -l` |
