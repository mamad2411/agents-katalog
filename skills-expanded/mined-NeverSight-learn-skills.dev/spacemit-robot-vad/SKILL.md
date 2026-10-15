---
name: spacemit-robot-vad
description: >-
  components/model_zoo/vad 的构建、PR 测试、Silero 模型 smoke、C++/Python
  VAD API 接入与缺模型场景处理入口。
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/model_zoo/vad
    primary_docs:
      - components/model_zoo/vad/README.md
      - components/model_zoo/vad/test.yaml
      - components/model_zoo/vad/package.xml
    build_hint: single_package_first
---

# SpacemiT Robot VAD

先按 [`spacemit-robot-shared`](../spacemit-robot-shared/SKILL.md) 确认 SDK 根路径与通用构建规则。
无 SDK 就转 [`spacemit-robot-sdk-bootstrap`](../spacemit-robot-sdk-bootstrap/SKILL.md)，不要在 `robot-skills` 仓库里直接运行 SDK 命令。

## 何时使用

- 用户要构建、测试或调试 `components/model_zoo/vad`。
- 用户要验证 VAD 配置、流式状态机、回调、错误路径或 Silero ONNX 推理。
- 用户要接入 `include/vad_service.h` 或 Python `spacemit_vad`。

## 默认规则

- `build_hint`: `single_package_first`
- SDK 内模块路径：`$SROBOTIS_ROOT/components/model_zoo/vad`。
- PR 测试默认跑 `test.yaml` 里的无模型 mock/contract 用例；不要要求 docker，也不要要求下载模型。
- 有 `~/.cache/models/vad/silero/silero_vad.onnx` 时，可额外跑真实 Silero smoke；没有模型时只报告跳过真实推理，不能把缺模型当作 PR 失败。
- 不默认先读 README；只有参数、模型路径、API 行为不清或命令失败时，才回读 `primary_docs`、`API.md`、`include/vad_service.h` 或测试源码。

## 固定流程

1. 先确认 SDK 根可用；无 SDK 就转 bootstrap。
2. 在 `$SROBOTIS_ROOT` 下执行 `source build/envsetup.sh`。
3. 需要构建时优先执行 `cd components/model_zoo/vad && mm`。
4. 需要测试时先执行 `./scripts/test/robot-test list components/model_zoo/vad`。
5. PR 验证执行 `./scripts/test/robot-test run components/model_zoo/vad --scope pr`，返回通过情况和日志路径。
6. 用户要求真实 VAD 推理时，先检查模型和 demo/wheel 是否存在；存在就真实运行，缺模型则说明缺失并保留 mock 测试结果。
7. 对“帮我跑一下”“帮我测一下”这类请求，必须真实执行命令并返回结果、命令、环境前置和失败点。

## 专项任务

### 构建组件

```bash
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
cd components/model_zoo/vad
mm
```

构建后优先确认 `vad_simple_demo` 是否在 `PATH` 中；Python wheel 通常输出到 `$SROBOTIS_ROOT/output/dist/`。

### 运行 PR 测试

```bash
cd "$SROBOTIS_ROOT"
./scripts/test/robot-test list components/model_zoo/vad
./scripts/test/robot-test run components/model_zoo/vad --scope pr
```

当前 PR 用例验证 VAD preset/config builder、fake backend 流式状态机、speech start/end 回调、未知 preset 和空音频错误路径；它们不依赖 Silero 模型。

### 真实 Silero smoke

只有模型存在时才跑真实推理：

```bash
test -f ~/.cache/models/vad/silero/silero_vad.onnx
cd "$SROBOTIS_ROOT"
source build/envsetup.sh
vad_simple_demo
```

如果要用真实 WAV 或 Python wheel，优先使用用户给的 WAV；没有样本时不要伪造语音结果。

## 禁止事项

- 不要在 `robot-skills` 仓库目录里直接执行 SDK 测试命令。
- 不要默认写死 target；需要 target 时按 shared 规则确认 board 和 product。
- 不要把模型下载、真实推理或音频设备依赖放进 PR 必跑条件。
- 不要在没有模型或样本时伪造 Silero 推理结果。
- 不要把模型、WAV、日志或构建产物写入 SDK 源码目录。

## 常见任务与命令

| 意图 | 动作 |
| ---- | ---- |
| 构建 VAD | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && cd components/model_zoo/vad && mm` |
| 列出 CI 用例 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test list components/model_zoo/vad` |
| 跑 PR 测试 | `cd "$SROBOTIS_ROOT" && ./scripts/test/robot-test run components/model_zoo/vad --scope pr` |
| 检查模型 | `test -f ~/.cache/models/vad/silero/silero_vad.onnx && echo found || echo missing` |
| 真实 C++ smoke | `cd "$SROBOTIS_ROOT" && source build/envsetup.sh && vad_simple_demo` |
| Python 导入检查 | `python -c "import spacemit_vad; print(spacemit_vad.__version__)"` |
