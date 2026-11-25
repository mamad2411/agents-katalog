---
name: stm32-instrument
description: Add gated SWO/ITM observability while writing STM32 C/C++ firmware, using low-overhead events at decisions, errors, ISR boundaries, and state transitions. Pair with stm32-debug for capture. / 编写 STM32 C/C++ 固件时加入受控 SWO/ITM 可观测性，在决策点、错误路径、ISR 边界和状态迁移处记录低开销事件，并与 stm32-debug 配合采集。
---

# Instrument STM32 firmware for debuggability / 为 STM32 固件加入可调试性

Add observability while writing code so later failures already have evidence. Capture it over
the SWO pin with `setup_swo` and `logging(channel="swo")`, avoiding an extra
instrument/reflash cycle.

在编写代码时就加入可观测性，使后续故障发生时已有证据。通过 SWO 引脚配合 `setup_swo` 和
`logging(channel="swo")` 采集，避免临时加日志再烧录。

Use the bundled `swo_trace.h` and `swo_trace.c`:

使用本 skill 中的 `swo_trace.h` 和 `swo_trace.c`：

| Macro / 宏 | Cost / 开销 | Use / 用途 |
|---|---|---|
| `SWO_EVENT(code)` | 1 byte, non-blocking, drop-on-full / 1 字节、非阻塞、满时丢弃 | ISRs and hot loops / ISR 与热点循环 |
| `SWO_MARK(port, val)` | 1 word, non-blocking / 1 个 word、非阻塞 | Counters, IDs, states / 计数器、ID、状态 |
| `SWO_LOG("fmt", ...)` | Formatted text, may block / 格式化文本、可能短暂阻塞 | Init, state changes, errors / 初始化、状态变化、错误路径 |

## Instrumentation discipline / 插桩纪律

1. **Gate every trace.** All macros disappear unless built with
   `-DSWO_TRACE_ENABLED=1`. Never add bare `printf` or `ITM_SendChar`.
   Release builds must have zero trace code and cost.
   / **所有追踪都必须受开关控制。** 未定义 `SWO_TRACE_ENABLED` 时宏应完全消失；
   不要直接调用 `printf` 或 `ITM_SendChar`，release 构建不得保留追踪代码和开销。
2. **Never use `SWO_LOG` in an ISR or hot loop.** Formatted output can block while the
   FIFO drains and create timing faults. Use drop-on-full `SWO_EVENT` or `SWO_MARK`.
   / **ISR 或热点循环中禁止使用 `SWO_LOG`。** 格式化输出可能阻塞并改变时序；
   改用满时丢弃的 `SWO_EVENT` 或 `SWO_MARK`。
3. **Instrument decisions, not lines.** Prefer sparse evidence at:
   / **记录决策点，而不是逐行记录。** 优先放在：
   - state transitions / 状态机迁移
   - error and early-return paths / 错误与提前返回路径
   - assert and fault handlers / 断言与故障处理函数
   - ISR entry/exit / ISR 入口与出口
   - peripheral initialization results / 外设初始化结果
   - owned RTOS task-switch or blocking points / 可控的 RTOS 切换或阻塞点
4. Define a small event enum so host-side output remains readable:
   / 定义精简事件枚举，便于主机端解释：

   ```c
   enum { EVT_BOOT=1, EVT_ISR_UART=2, EVT_DMA_DONE=3, EVT_STATE_ERR=0xEE };
   ```

5. Keep messages short. The SWO link is finite; prefer event codes for frequent paths.
   / 保持消息简短。SWO 带宽有限，高频路径优先使用事件码。

## Add it to a project / 接入项目

1. Copy `swo_trace.h` and `swo_trace.c` into the firmware project and add the C file
   to the build. / 复制两个文件到固件项目，并将 C 文件加入构建。
2. Enable a debug build with
   `-DSWO_TRACE_ENABLED=1 -DSWO_TRACE_INCLUDE="\"stm32l4xx.h\""` using the correct
   CMSIS device header. / 在 debug 构建中启用宏，并替换为正确的 CMSIS 器件头文件。
3. Ensure the SWO pin, commonly PB3/TRACESWO, is routed to the probe. Nucleo and
   Discovery boards usually have it connected; custom boards may not.
   / 确认 SWO 引脚（常见为 PB3/TRACESWO）连接到探针。Nucleo/Discovery 通常已连接，
   自定义板必须核对原理图。
4. Firmware-side ITM initialization is normally unnecessary because `setup_swo`
   configures TPIU and ITM through the debugger. /
   一般无需在固件中初始化 ITM，`setup_swo` 会通过调试器配置 TPIU 和 ITM。

## Capture from the debugger / 从调试器采集

```text
setup_swo(hclk_hz=<actual core clock>)
logging(action=start, channel="swo", file="swo_itm.log")
# reproduce / 复现问题
logging(action=get, channel="swo")
```

Use the measured/actual HCLK, not a guessed nominal clock. For "where is execution spending
time?", prefer `sample_pc`; it needs no firmware instrumentation or SWO pin.

使用实测或确认过的 HCLK，不要猜标称频率。若问题只是“CPU 时间花在哪里”，优先使用
`sample_pc`，它不需要修改固件，也不依赖 SWO 引脚。

## When not to instrument / 不应插桩的情况

- Do not add trace when one breakpoint plus `capture_state` answers the question. /
  一个断点和 `capture_state` 即可回答的问题，不要额外加追踪。
- Do not put `SWO_LOG` in tight DSP/control loops; at most use a deliberate
  `SWO_MARK`, or sample externally. /
  紧密 DSP/控制循环中不要使用 `SWO_LOG`；最多使用经过评估的 `SWO_MARK`，或从外部采样。
- Do not ship ungated debug output. / 不要发布未受开关控制的调试输出。

## Optional repository rule / 可选仓库规则

Add this to the firmware project's agent rules when automatic instrumentation is desired:

需要 AI 自动插桩时，可将以下规则加入固件项目：

> Use `SWO_EVENT`, `SWO_MARK`, and `SWO_LOG` at state transitions, error paths, and ISR
> boundaries. Gate all trace behind `SWO_TRACE_ENABLED`; never use bare `printf`, and never
> call `SWO_LOG` in an ISR.
>
> 在状态迁移、错误路径和 ISR 边界使用上述宏；所有追踪必须受 `SWO_TRACE_ENABLED` 控制，
> 禁止裸 `printf`，禁止在 ISR 中调用 `SWO_LOG`。
