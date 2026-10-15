---
name: spacemit-robot-voiceprint
description: components/model_zoo/voiceprint 的构建、PR 测试、模型可选 smoke 与说话人识别 API 接入入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/model_zoo/voiceprint
    primary_docs:
      - components/model_zoo/voiceprint/README.md
      - components/model_zoo/voiceprint/test.yaml
      - components/model_zoo/voiceprint/package.xml
      - components/model_zoo/voiceprint/include/vp_service.h
    build_hint: single_package_first
---

# SpacemiT Robot Voiceprint

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。

## 何时使用

- 用户要构建、测试或调试 `components/model_zoo/voiceprint`。
- 用户要接入 `include/vp_service.h`、说话人注册、识别、验证或 embedding 数据库。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/model_zoo/voiceprint`。
- PR 测试使用 fake backend 验证注册、识别、验证和数据库逻辑，不要求模型。
- 有 CAMPPlus 模型和样本音频时才跑真实 voiceprint smoke；缺模型不能作为 PR 失败。

## 固定流程

1. 确认 `$SROBOTIS_ROOT` 指向完整 SDK。
2. 在 SDK 根目录执行 `source build/envsetup.sh`。
3. 构建时执行 `cd components/model_zoo/voiceprint && mm`。
4. 测试前执行 `./scripts/test/robot-test list components/model_zoo/voiceprint`。
5. PR 验证执行 `./scripts/test/robot-test run components/model_zoo/voiceprint --scope pr`。
6. 用户要求真实说话人识别时，先检查模型、demo 和样本音频是否存在。
7. 对“帮我跑一下”“帮我测一下”类请求，必须真实执行命令并返回命令、结果、日志路径和失败点。

## 禁止事项

- 不要把模型下载、真实音频样本或音频设备依赖放进 PR 必跑条件。
- 不要默认写死 target；需要 target 时按 shared 规则确认。
- 不要在缺模型或缺样本时伪造识别、验证或分数结果。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 voiceprint | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/model_zoo/voiceprint && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/model_zoo/voiceprint` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/model_zoo/voiceprint --scope pr` |
| 检查 CAMPPlus 模型 | `test -d ~/.cache/models/vp/campplus && echo found || echo missing` |
| 检查工具 | `command -v register_speaker && command -v identify_speaker` |
