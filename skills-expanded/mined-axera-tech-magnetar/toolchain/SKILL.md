---
name: toolchain
description: Hidden stage for magnetar. Ensure Pulsar2 and the chip-specific C++ BSP/cross-compilation toolchain are available for compile and SDK validation.
---

# TOOLCHAIN

## 执行
`pulsar_image = magnetar.stages.toolchain.run()`

## LLM 分支（model_route=llm）

- 额外确认 `pulsar2 llm_build2 -h` 可用（Pulsar2 ≥ 6.0）；不可用 → blocked，
  提示升级独立包（`./scripts/install_pulsar2.sh` 默认安装 8.0）；
- 准备 ax-llm-build 工具：`magnetar.stages.llm.ensure_axllm_build_tools(task_dir)`
  （默认经 `GH_PROXY` 克隆 `https://github.com/AXERA-TECH/ax-llm-build.git` 到
  `TASK_DIR/cache/ax-llm-build`）；
- Pulsar2 只使用独立安装包（强制不用 Docker）：未设置 `PULSAR2_HOME` 时，
  `magnetar.pulsar2_util.ensure_pulsar2_package` 自动获取 **8.0**
  `*_package.tar.gz` 并解压到 `~/.cache/magnetar/pulsar2/<版本>/`
  （仓库 `AXERA-TECH/Pulsar2`：下载 URL ModelScope 优先、hf-mirror 兜底；
  `PULSAR2_VERSION` 可固定版本、`PULSAR2_PACKAGE=lite|full` 可选变体）；
- BSP/runtime 下载地址以 ax-pipeline `scripts/build_common.sh` 为唯一来源
  （按芯片取 `MSP_URL_DEFAULT` / `TOOLCHAIN_URL_DEFAULT`，`CXX_BSP_URL` /
  `CXX_TOOLCHAIN_URL` 可覆盖），不再去 ax-knowledge / ModelScope 翻 SDK 直链；
- 记录板端 axllm 安装方式（官方 `install.sh`，axllm 分支）到 task.md。

## 验证
- Pulsar2 独立包可用（`bin/pulsar2` 存在且 `pulsar2 --version` 正常，非 Docker）
- AX8860：Pulsar2 必须 ≥ 8.0；BSP 缺失只降级 C++ SDK，不阻塞模型编译
- C++ BSP 交叉编译器存在（AX650: msp_50 + Arm GNU 9.2 aarch64；AX630C: msp_20e +
  Arm GNU 9.2 aarch64；AX620Q/AX620E: msp_20e + ax620q_bsp_sdk uclibc）
- LLM 分支：`pulsar2 llm_build2 -h` 正常；ax-llm-build 工具就绪

## STOP
- Pulsar2 独立包不可用且无法从 ModelScope/HF AXERA-TECH/Pulsar2 获取
- BSP/交叉编译器缺失且无法下载
- LLM 分支：Pulsar2 无 `llm_build2` 且无法升级 → blocked
