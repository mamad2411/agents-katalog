---
name: stm32-debug
description: Debug STM32 firmware on real hardware through stm32-gdb-mcp. Use for flash, execution control, memory/register/RTOS inspection, HardFaults, hangs, reproducible hardware bugs, and programmable-USB-hub work (wedged probes, cold boot, rack channels, power measurement). / 通过 stm32-gdb-mcp 在真实硬件上调试 STM32，适用于烧录、执行控制、内存/寄存器/RTOS 检查、HardFault、卡死、可复现硬件故障，以及可编程 USB Hub 相关操作（探针卡死、冷启动、机架通道、功耗测量）。
---

# STM32 hardware debugging / STM32 硬件调试

Drive `stm32-gdb-mcp` as a senior embedded-debug loop:
**observe → orient (symbolize) → hypothesize → act safely → verify**.

按资深嵌入式工程师的闭环使用 `stm32-gdb-mcp`：
**观察 → 定位（符号化）→ 提出假设 → 安全操作 → 验证**。

## Golden rules / 核心规则

- **Run `self_check` immediately after `start_debug_session`.** It validates byte order,
  Cortex-M core, and expected MCU family before later evidence is trusted.
  / **`start_debug_session` 后立即运行 `self_check`。** 在信任后续证据前先验证字节序、
  Cortex-M 内核和预期 MCU 系列。
- **Reads require a HALTED core.** If a read returns `target_unresponsive`, call
  `halt_execution` first. `run_and_wait` leaves the core running on timeout.
  / **读取要求内核已暂停。** 遇到 `target_unresponsive` 先调用 `halt_execution`；
  `run_and_wait` 超时后内核仍在运行。
- **A breakpoint timeout means the path was not reached.** Halt, run `capture_state`,
  inspect `breakpoint(action=list)` and its `hit_count`, then read the gating state.
  Move the breakpoint earlier, drive the required stimulus, or use a condition; do not
  repeat the same wait.
  / **断点超时表示代码路径未到达。** 暂停后执行 `capture_state`，检查断点 `hit_count`
  和门控状态，再前移断点、驱动输入或使用条件断点；不要原样重试。
- Prefer composites such as `flash_and_run`, `debug_until`, `capture_state`, and
  `run_for_duration` to reduce round trips. /
  优先使用组合工具，减少 MCP 往返和中间状态。
- **Writes are guarded.** Option bytes, IWDG, and WWDG are blocked by default.
  Use `write_guard(action=policy)` for explicit access or dry-run simulation, and
  `write_guard(action=audit)` for the record.
  / **写操作受保护。** option bytes、IWDG 和 WWDG 默认禁止；显式放行或模拟时使用
  `write_guard(action=policy)`，审计记录使用 `write_guard(action=audit)`。
- On `probe_unavailable` or `connection_lost`, use `recover_session`. A `probe_busy`
  error means another process owns the probe. `target_unreachable`,
  `debug_auth_required`, and `invalid_target_config` need changed conditions, not an
  identical retry.
  / 遇到 `probe_unavailable` 或 `connection_lost` 使用 `recover_session`；
  `probe_busy` 表示探针被占用。`target_unreachable`、`debug_auth_required` 和
  `invalid_target_config` 需要改变条件，不能同参重试。
- **ST-Link SWD is exclusive.** Do not start a second OpenOCD/GDB while a session is
  active. Reset with `reset_target`. The ST-Link virtual COM port is a separate endpoint
  and can coexist with SWD.
  / **ST-Link SWD 是独占连接。** 会话活跃时不要启动第二个 OpenOCD/GDB；使用
  `reset_target` 复位。ST-Link 虚拟串口是独立端点，可与 SWD 共存。
- Follow `suggested_next_actions`. Reach hidden tools with `call`, inspect schemas with
  `tool_help`, and report an apparent MCP defect with `report_issue`.
  / 遵循 `suggested_next_actions`；用 `call` 调用隐藏工具、用 `tool_help` 查询 schema，
  疑似 MCP 缺陷使用 `report_issue`。

## Bring-up from ELF / 从 ELF 启动调试

Use the profile as the single source of truth. A one-round-trip recipe is:

以调试 profile 作为唯一事实源。单轮往返配方：

```text
batch(steps=[
  {"tool": "debug_config", "args": {"action": "load", "path": "mcp/board.yaml"}},
  {"tool": "start_debug_session", "args": {}},
  {"tool": "self_check", "args": {}}
], stop_on_error=true)
```

If no config exists, call `detect_probe`, then obtain validated OpenOCD arguments with
`suggest_server_args`, start the session, run `self_check`, and set
`debug_profile(action=set, mcu=..., elf_path=..., svd_path=...)`. Auto-selection is allowed
only for one detected probe. Only call `flash_and_run` after flashing is explicitly intended.

若没有配置文件，先调用 `detect_probe`，再用 `suggest_server_args` 获取已验证的 OpenOCD 参数，
启动后立即 `self_check`，再设置 MCU、ELF 和 SVD profile。只有检测到唯一探针时才允许自动选择；
只有明确要烧录时才调用 `flash_and_run`。

See / 参见：`scenarios/bringup.json`。

## Programmable USB hub (optional) / 可编程 USB Hub（可选）

Applies only with the `[hub]` extra and a hub configured in the profile. Start with the
read-only `hub(action=describe)` (also reachable through `call_read`): it reports each port's
power/data state, voltage/current on ADC models, the mapped labels, and recent hub actions.

仅在安装 `[hub]` extra 且 profile 中配置了 Hub 时适用。先调用只读的 `hub(action=describe)`
（也可经 `call_read` 调用）：返回各端口电源/数据线状态、带 ADC 型号的电压电流、映射标签和最近操作。

**Which channel is this board? / 当前板卡在哪个通道？**

- One board: `debug_profile(action=set, hub={"channel": N})`. A rack: one YAML with
  `hub.map: {N: {label: <session name>}}`, loaded into **every** session with
  `debug_config(action=load, path=..., session="<name>")`. A label matches the debug
  session name exactly; the profile is per-session and in-memory. /
  单板用 `hub.channel`；机架用 `hub.map`，label 必须与会话名完全一致，且要给**每个**会话分别加载
  （profile 按会话隔离、只在内存中）。
- `power`, `data`, `cycle`, and `measure` results carry `channel_source` (`argument`,
  `profile`, `map_label`, `map_serial`). Check it instead of assuming the right port was
  chosen. / 这几个操作的结果都带 `channel_source`，以它为准，不要想当然。
- `hub(action=discover, apply=true)` maps probes to channels by toggling data lines. It is
  slow (one `detect_probe` per channel) and refuses while a session is live: with the
  shared hub daemon, any session on the rack; in `local` mode, this one. Under the daemon it
  also holds the whole rack while it runs. /
  `discover` 逐通道切数据线来映射探针：很慢，有活跃会话时拒绝运行（守护进程模式下指机架上任何会话，
  `local` 模式下指当前会话）；守护进程模式下运行期间占用整个机架。

**Wedged probe / 探针卡死**

- Use `recover_session`. With a hub it escalates on its own: soft retries → toggle the
  port's data lines → power-cycle the port (`deep=true` adds a long power cycle). It only
  escalates for `probe_busy`, `probe_unavailable`, `target_unresponsive`,
  `connection_lost`, and `target_unreachable`. Read the returned `steps`: they say what was
  physically done to the board. Never hard-kill OpenOCD. /
  使用 `recover_session`：有 Hub 时会自动逐级升级（软重试 → 切数据线 → 端口断电重启，`deep=true`
  再加一次长时间断电），只对上述错误码升级。返回的 `steps` 写明了对硬件实际做了什么。不要强杀 OpenOCD。

**Cold boot / 冷启动**

- `reset_target(strategy="cold")` stops the session, cuts the port's power, restores it,
  and resets. Check `browned_out` in the result. `false` means the rail never collapsed
  (bulk capacitance, a coin cell, another supply), so the board did **not** cold-boot:
  retry with a longer `off_ms` or find the second supply. `null` means no load was
  measured before the cut (empty port, deep sleep, or a transient current-sense reading of
  0 mA); re-read and compare with a loaded channel before concluding anything. /
  `reset_target(strategy="cold")` 会先停会话再断电、上电、复位。检查 `browned_out`：`false` 表示电源轨
  没掉下去、板子**并未**冷启动，应加长 `off_ms` 或排查其他供电；`null` 表示断电前测不到负载（空端口、
  深度休眠或电流采样暂时读 0），先复测并与有负载的通道对比，再下结论。

**Cutting power or data by hand / 手动断电或断数据线**

- `hub(action=power|data|cycle)` needs `confirm=true` in the default `confirm` guard mode,
  and in **every** mode while a live GDB server sits on that channel. With the shared hub
  daemon that covers every session on every MCP server on the rack, and the refusal names
  whose session it is. Do not add `confirm=true` reflexively to get past that refusal:
  cutting power mid-flash can brick a board. Ask the user. /
  默认 `confirm` 模式下必须传 `confirm=true`；该通道上有活跃 GDB 时任何模式都必须。共享守护进程会检查
  机架上所有 MCP 服务器的会话，拒绝信息会写明是谁。不要为了绕过拒绝条件反射地加 `confirm=true`：
  烧录中途断电可能把板子变砖，应询问用户。
- `hub(action=data, exclusive=true)` leaves exactly one probe enumerated. If the result
  is the `hub_isolation_incomplete` error, isolation did not take: do not start a session
  on the strength of it. /
  `exclusive=true` 只保留一个探针可见；若返回 `hub_isolation_incomplete`，说明隔离没成功，不能据此启动会话。
- Flashing one board on a rack needs no isolation: `flash_and_run(file_path=...,
  hub_channel=N)` pins the session to that channel's probe by USB position. /
  在机架上烧录某一块板不需要隔离：`flash_and_run(file_path=..., hub_channel=N)` 按 USB 位置锁定该通道的探针。

**Power evidence / 功耗证据**

- `hub(action=measure, duration_sec=..., interval_sec=...)` samples the port's voltage and
  current while the core runs, with no SWD traffic. Use it to verify low-power claims: an
  MCU that entered Stop and one that only thinks it did look identical over SWD and differ
  by orders of magnitude here. /
  `hub(action=measure)` 在内核运行时采样端口电压电流，不产生 SWD 流量。用它验证低功耗：真正进入 Stop
  和"以为进入了"在 SWD 上看起来一样，在这里电流相差几个数量级。

**Several MCP servers on one rack / 多个 MCP 服务器共用一个 Hub**

- With the `[hub]` extra installed, a shared hub daemon owns the hub; nothing changes in how
  you call `hub(...)`. `hub_busy` means another server's write held that channel for the
  whole `max_wait_sec`, so yours was **not** executed. Re-check `hub(action=describe)` and
  retry only if the action is still wanted. /
  装了 `[hub]` extra 时由共享守护进程独占 Hub，调用方式不变。`hub_busy` 表示另一服务器的写操作
  占住了该通道直到超时，你的操作**没有**执行；先 `describe` 复查，仍需要时再重试。
- `hub(action=dashboard)` returns the URL of a read-only live page (per-port V/I history,
  every server's sessions, a timeline of hub actions) for the human to watch. /
  `hub(action=dashboard)` 返回只读实时看板的地址（各端口电压电流历史、所有服务器的会话、操作时间线），供用户查看。

## HardFault or crash / HardFault 或崩溃

1. Break on `HardFault_Handler` (or the relevant handler), then `run_and_wait`; if the
   target is already faulted, halt it. /
   在 `HardFault_Handler` 或对应处理函数设置断点并运行；若目标已故障则直接暂停。
2. Run `reconstruct_fault_context`. It decodes fault registers, selects MSP/PSP through
   EXC_RETURN, reconstructs the stacked frame, recovers the true faulting PC, and resolves
   it to `file:line`. /
   运行 `reconstruct_fault_context`：解码故障寄存器，通过 EXC_RETURN 选择 MSP/PSP，
   重建异常栈帧并把真实故障 PC 解析到源码行。
3. Inspect `frame(action=source)`, `frame(action=variables)`, and `read_call_stack` around
   that PC. Explain the root cause from evidence, not only the handler location. /
   围绕该 PC 检查源码、局部变量和调用栈；根因必须来自证据，不能只报告处理函数位置。

See / 参见：`scenarios/hardfault.json`。

## Hang or livelock / 卡死或活锁

1. If running, call `halt_execution`, then `capture_state` and `read_call_stack`. /
   若目标仍运行，先暂停，再采集状态和调用栈。
2. For RTOS firmware, use `snapshot(scope=rtos)` and `read_freertos(what="tasks")`;
   inspect queues, mutexes, and heap for blockers. /
   RTOS 固件使用 `snapshot(scope=rtos)` 和任务列表，并检查队列、互斥量和堆。
3. Use `sample_pc` for a non-intrusive, symbolized PC hot-spot histogram. A high
   `unsampleable` count usually means the target is halted or asleep. /
   使用 `sample_pc` 获取非侵入式符号化热点；`unsampleable` 很高通常表示目标暂停或休眠。
4. For SWO text, run `setup_swo(hclk_hz=<actual HCLK>)`, then
   `logging(action=start, channel="swo", file="swo_itm.log")`. /
   SWO 文本先按实际 HCLK 配置 `setup_swo`，再启动 SWO 日志。

## Stack overflow / 栈溢出

A large local buffer or deep recursion can drive SP below the stack limit and later cause
a stacking fault. Do not single-step blindly.

大局部数组或深递归会让 SP 越过栈边界，并在之后触发压栈故障。不要盲目单步。

1. Orient with `inspect_project`, load the ELF, and find likely functions using
   `inspect_symbol(what=functions, regex="Flash|Write|Read")`. /
   用项目检查、ELF 符号和函数搜索定位可疑函数。
2. Catch `HardFault_Handler`, or set a write watchpoint at the stack limit to stop at the
   overflow moment. /
   捕获 HardFault，或在栈边界设置写 watchpoint 以抓住越界瞬间。
3. Reproduce the operation, then run `analyze_stack(stack_size=<map value>)`.
   A breakpoint at function entry may stop before the prologue allocates the local array;
   break inside the function or step past the prologue. /
   复现后按 map 中的栈大小运行 `analyze_stack`。函数入口断点可能停在栈帧分配前，
   应在函数内部断下或越过 prologue。
4. Confirm with `reconstruct_fault_context` (`STKERR`/`MSTKERR`), `read_call_stack`,
   and FreeRTOS stack high-water marks. /
   用故障标志、调用栈和 FreeRTOS 栈余量交叉确认。
5. Move large buffers to static storage or increase the proven stack budget, rebuild,
   flash with approval, and rerun the saved scenario. /
   将大缓冲区移到静态存储或增加有依据的栈预算；经批准后重建烧录并回放场景。

See / 参见：`scenarios/stack_overflow.json`。

## Peripheral not working / 外设不工作

Most dead peripherals reduce to clock, pin mux, or control-register configuration.

大多数外设失效可归结为时钟、引脚复用或控制寄存器配置。

1. Load the profile SVD so registers decode by name. / 加载 profile 中的 SVD。
2. Check the RCC enable bit first. A clock-gated peripheral often reads zero and cannot
   accept configuration. / 先检查 RCC 使能位；时钟关闭时外设通常读零且配置不生效。
3. Check GPIO `MODER` and `AFRL`/`AFRH` against the intended pin and AF number. /
   核对 GPIO 模式、引脚和 AF 编号。
4. Decode the peripheral control/status registers and compare baud, prescaler, enable,
   and status fields with the intended setup. /
   解码外设控制/状态寄存器，并核对波特率、分频、使能和状态字段。

See / 参见：`scenarios/peripheral_check.json`。

## Heap exhaustion or leak / 堆耗尽或泄漏

1. For FreeRTOS, run `read_freertos(what="heap")`; near-zero minimum-ever-free bytes
   prove that exhaustion occurred. /
   FreeRTOS 使用堆检查；历史最小剩余空间接近零可证明曾发生耗尽。
2. Trend a free-byte counter with `run_for_duration(..., sample={...})`. A monotonic
   decline under a repeatable workload is leak evidence. Use SWO/ring-buffer telemetry
   if running-target reads disturb timing. /
   在可重复负载下采样空闲字节；单调下降是泄漏证据。若调试器读取影响时序，改用 SWO 或环形缓冲。
3. Trap allocator/free calls or watch the free-heap counter to locate unmatched
   allocations. / 在分配/释放点断下，或 watch 空闲堆计数以定位未配对分配。

See / 参见：`scenarios/heap_check.json`。

## Assert or configASSERT / 断言触发

Break on `assert_failed`, `__aeabi_assert`, `vAssertCalled`, or the project's
`configASSERT` target. Run to it, inspect `frame(action=variables)` for file/line/expression,
then use `read_call_stack` to find the caller.

在项目实际使用的断言处理函数上设置断点，命中后读取 file/line/expression 参数，再通过调用栈定位调用者。

See / 参见：`scenarios/assert_check.json`。

## Minimal reproducible logic bug / 最小化复现逻辑故障

- Use `debug_until(location="fn", condition="state == BAD")` to set the hypothesis trap,
  run, and return decoded context in one call. /
  用 `debug_until` 一次完成假设断点、运行和上下文采集。
- Save the sequence as `run_scenario` steps and export a sanitized report with
  `export_debug_report`. /
  将序列保存为可回放场景，并导出脱敏报告。

## Verify the fix / 验证修复

Use `expressions(action=compare)` or `expressions(action=assert)` and replay the same
scenario. Do not rely on visual inspection alone.

使用表达式比较/断言并回放同一场景；不要只凭肉眼判断。

## Determinism and evidence / 可复现性与证据

Every tool call is journaled. Review `get_session(view="timeline")` or
`get_session(view="metrics")`, then use `export_debug_report` for a shareable,
sanitized artifact.

所有工具调用都会记入日志。通过 timeline/metrics 复核过程，再导出可共享且已脱敏的报告。

## Reference / 参考

- `reference/tool-map.md`: tools grouped by purpose / 按用途整理的工具索引
- `scenarios/*.json`: replayable templates / 可回放场景模板
