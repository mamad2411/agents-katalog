---
name: spacemit-robot-doa
description: components/multimedia/audio_process/doa 的构建、PR 测试、手动多麦 smoke 与 DOA API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/multimedia/audio_process/doa
    primary_docs:
      - components/multimedia/audio_process/doa/README.md
      - components/multimedia/audio_process/doa/test.yaml
      - components/multimedia/audio_process/doa/package.xml
      - components/multimedia/audio_process/doa/include/doa_service.h
    build_hint: single_package_first
---

# SpacemiT Robot DOA

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、测试或调试 `components/multimedia/audio_process/doa`。
- 用户要接入 SoundLocator、MultiSoundLocator、GCC-PHAT、TDOA 或多麦声源定位。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/multimedia/audio_process/doa`。
- PR 测试使用合成音频和错误路径，不要求真实麦克风。
- 真实多麦定位只在确认设备通道数、麦克风几何和人工看护后设置 `DOA_MANUAL_RUN=1` 跑 `manual` scope。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 构建时执行 `cd components/multimedia/audio_process/doa && mm`。
4. 测试前执行 `./scripts/test/robot-test list components/multimedia/audio_process/doa`。
5. PR 验证执行 `./scripts/test/robot-test run components/multimedia/audio_process/doa --scope pr`。
6. 用户要求真实定位时，先确认 `ssl_demo`、输入设备、通道数和麦克风布局；没有设备时不要运行 manual。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令并返回命令、结果、日志路径和失败点。

## 禁止事项

- 不要在 PR 测试里依赖真实麦克风。
- 不要默认写死 target 或麦克风几何；需要时按用户设备确认。
- 不要在未确认通道映射时解释真实角度结果。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 DOA | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/multimedia/audio_process/doa && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/multimedia/audio_process/doa` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/multimedia/audio_process/doa --scope pr` |
| 跑手动多麦 smoke | `cd "$SROBOTIS_ROOT" && DOA_MANUAL_RUN=1 ./scripts/test/robot-test run components/multimedia/audio_process/doa --scope manual` |
| 检查 demo | `test -x "$SROBOTIS_ROOT/output/staging/bin/ssl_demo" && echo found || echo missing` |
