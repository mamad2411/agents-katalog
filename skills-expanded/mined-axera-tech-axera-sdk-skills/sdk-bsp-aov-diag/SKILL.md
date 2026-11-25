---
name: sdk-bsp-aov-diag-skill
description: >
  诊断 AX615 Linux suspend/resume 中 wakeup_count 与低功耗 GPIO（gpio_lp）唤醒中断相关的问题。
  当用户遇到 AX615 在未使用 /sys/power/wakeup_count 时短时 GPIO 唤醒丢中断、使用
  `cat /sys/power/wakeup_count > /sys/power/wakeup_count` 后无法进入休眠、GPIO 唤醒延迟变长、
  `AX_SYS_Sleep` 返回失败，或日志出现 `PM: suspend entry (deep)` 后立即退出、`Freezing of tasks aborted`
  等现象时，优先使用本 Skill。只要现象同时涉及 `wakeup_count`、
  `gpio_lp`/低功耗 GPIO 和 suspend/resume，也应使用本 Skill。
---

# AX615：wakeup_count 与 gpio_lp 唤醒异常排查

## 1. 适用范围

本 Skill 用于 AX615 BSP 的深度休眠（deep suspend）场景，重点覆盖：

- 应用层不执行 wakeup-count 协议时，短时间 GPIO 唤醒可能丢失；
- 应用层执行 `wakeup_count` 协议后，GPIO 唤醒能够生效但系统无法进入休眠；
- 修复 GPIO 低功耗唤醒源后，出现唤醒时间变长；
- `AX_SYS_Sleep` 返回非零，或 suspend 在冻结任务阶段被中止。

本 Skill 参考一组历史问题资料，客户、工单与内部项目元数据已脱敏。
- 影响版本和修复版本以当前设备的实际发布记录为准；历史资料中的版本仅作参考。

## 2. 通用诊断约束

本 Skill 采用模板中的证据驱动方法，但不把历史案例自动当作当前设备事实：

- 证据优先级依次为：可重复的修复前后或单变量 A/B 结果；与运行镜像一致的代码、配置和构建产物；完整日志、时间线和统计计数；条件相符的 Jira/变更记录；单次现象或经验推测。
- 按问题层级定位：上电、复位、时钟、电源、pinmux、DDR 和板级信号属于硬件/Boot；probe、IRQ、DMA、设备树和 PM 属于 kernel/driver；daemon、IPC、文件系统和资源限制属于系统服务；VIN/ISP、SDK API、业务状态机和并发时序属于中间件/应用。
- 每个候选结论都要给出支持证据、反证条件和最小 A/B 验证。缺失的版本、日志、代码或构建信息写“未提供，不能判断”，不要用经验补全。
- 寄存器写入、驱动卸载、修改启动参数、重启、刷写和断电只用于受控验证；执行前记录原值、影响范围和恢复方法。代码中存在修复不等于运行镜像已包含修复。

## 3. 先给出结论

当低功耗 GPIO 中断是系统的唤醒源时，GPIO 的 IRQ handler 必须把已经到达的唤醒事件
同步到 Linux PM wakeup-source 机制。否则，事件可能只被 GPIO 驱动自己的等待队列消费，
而没有及时更新 PM 的 wakeup-event 状态；在 suspend 过渡窗口内，应用层读取和回写
`/sys/power/wakeup_count` 可能与 GPIO 事件发生产生竞态，造成短时唤醒丢失或 suspend
状态判断异常。

本案例的关键修复是：

1. 在 `wakeup_gpio_lp_handler()` 检测到有效 GPIO 低功耗中断后调用：

   ```c
   __pm_wakeup_event(gpio_lp->ws, 0);
   ```

2. 在驱动 remove 路径注销由 `wakeup_source_register()` 创建的 wakeup source：

   ```c
   if (gpio_lp->ws)
           wakeup_source_unregister(gpio_lp->ws);
   ```

第一项是修复唤醒事件未进入 PM wakeup-source 路径的核心改动；第二项用于资源生命周期
完整性，避免驱动卸载或重新 probe 时遗留 wakeup source。

## 4. 现象识别

### 3.1 典型现象组合

优先检查以下组合是否同时出现：

| 场景 | 观察结果 |
| --- | --- |
| 不执行应用层 wakeup_count，依赖系统内部机制 | 约 1~8 ms 的 GPIO 唤醒可能丢信号；约 8~500 ms 的唤醒通常正常 |
| 执行 `cat /sys/power/wakeup_count > /sys/power/wakeup_count` | 约 1~500 ms 的 GPIO 唤醒均可生效，但系统可能无法进入休眠 |
| 应用执行 `AX_SYS_Sleep` | 首次可能成功，后续返回非零，例如 `0x800b0715` |
| suspend 日志 | 出现 `PM: suspend entry (deep)`，随后可能出现 `Freezing of tasks aborted` 或 `PM: suspend exit` |
| 应用同时运行 VIN/AOV 采集 | GPIO pulse 后 `GetDevFrame` 结果与 suspend 时序相关，不能单独作为 PM 根因判断 |

上述时间范围来自历史实验记录，实际数值会受硬件、内核配置、任务负载和唤醒源配置影响，
不可作为固定阈值。

### 3.2 关键日志

重点保留以下日志上下文，不要只截取单行错误：

```text
PM: suspend entry (deep)
Freezing user space processes ...
Freezing of tasks aborted ...
PM: suspend exit
AX_SYS_Sleep ret=0x...
GetDevFrame #... ret=0x...
```

GPIO 唤醒触发前后至少保留一个完整 suspend 周期，并记录 GPIO pulse 的时间戳、
`wakeup_count` 读写结果以及 `AX_SYS_Sleep` 返回值。

## 5. 排查流程

### 步骤 1：确认平台和版本

记录以下信息：

- SoC：AX615；
- SDK/BSP 版本、kernel commit 和构建配置；
- 影响版本是否接近 `AX615_SDK_V2.0.0_P8`；
- 是否已经包含 `gpio_lp.c` 的 PM wakeup-source 修复；
- 使用的低功耗 GPIO 编号、触发类型和设备树 `lp-gpios` 配置；
- suspend 类型是否为 `deep`。

推荐命令：

```sh
uname -a
cat /proc/version
cat /sys/power/state
cat /sys/power/wakeup_count
cat /proc/ax_proc/power/wakeup_source/timer32/enable
cat /proc/ax_proc/power/wakeup_source/timer32/time
```

如果系统不提供某个 `/proc` 节点，记录“节点不存在”以及对应 BSP 配置，不要据此直接判定
为本案例。

### 步骤 2：建立不带 wakeup_count 的基线

先在相同硬件、相同 GPIO 脉冲间隔和相同业务负载下测试，不要同时修改驱动和应用。

记录：

- GPIO pulse 的触发时间；
- 系统是否进入 `PM: suspend entry (deep)`；
- 是否在预期时间唤醒；
- 是否出现丢中断、丢帧或 `AX_SYS_Sleep` 非零；
- 连续测试次数和成功次数。

应用层测试不要把 `GetDevFrame` 超时误当成 GPIO 唤醒失败；需要结合 kernel PM 日志和
GPIO 驱动事件共同判断。

### 步骤 3：单独验证 wakeup_count 协议

Linux 的标准协议是：

1. 在进入休眠准备阶段读取 `/sys/power/wakeup_count` 并保存读数；
2. 完成用户空间自己的休眠准备；
3. 将原读数写回 `/sys/power/wakeup_count`；
4. 写回失败时，不应继续写 `/sys/power/state`；
5. 写回成功后再请求 suspend。

最小观测示例：

```sh
count=$(cat /sys/power/wakeup_count) || exit 1
printf '%s\n' "$count" > /sys/power/wakeup_count
printf 'wakeup_count=%s\n' "$count"
```

不要把以下写法当作完整的业务休眠实现：

```sh
cat /sys/power/wakeup_count > /sys/power/wakeup_count
```

该写法可用于复现历史资料中的读写路径，但业务代码仍需正确处理读写失败、并发唤醒和
随后写入 `/sys/power/state` 的时序。

### 步骤 4：检查 gpio_lp 是否注册为 PM wakeup source

在源码中确认以下三点：

1. probe/init 路径创建了 wakeup source，例如：

   ```c
   gpio_lp->ws = wakeup_source_register("wake_int");
   ```

2. IRQ handler 在确认 `int_status` 非零后调用：

   ```c
   __pm_wakeup_event(gpio_lp->ws, 0);
   ```

3. remove、probe 错误回滚路径都能注销该 wakeup source，并将指针置空或保证不会重复注销。

如果只存在第 1 项而不存在第 2 项，优先按本案例处理；如果 IRQ handler 调用了第 2 项，
则继续检查是否使用了错误的 wakeup source、GPIO 中断状态是否真正置位、以及设备树触发
配置是否正确。

### 步骤 5：区分三类失败

#### A. GPIO 事件没有进入 PM 机制

特征：

- GPIO 自身的等待队列或字符设备可能仍能收到事件；
- `/sys/power/wakeup_count` 相关 suspend 判定却不稳定；
- 短时唤醒更容易丢失。

检查：

- `gpio_lp_int_status()` 是否返回非零；
- handler 是否执行 `__pm_wakeup_event(gpio_lp->ws, 0)`；
- `gpio_lp->ws` 是否为空或已失效。

#### B. wakeup_count 写回失败

特征：

- 写 `/sys/power/wakeup_count` 返回错误；
- 同一时间窗口有其他 wakeup event；
- 继续请求 suspend 会违反用户空间协议。

检查：

- 保存原始 read 值和 write 返回值；
- 是否有并发 GPIO、timer、网络或其他唤醒源；
- 是否在写回成功前就写了 `/sys/power/state`。

#### C. suspend 冻结阶段失败

特征：

```text
Freezing of tasks aborted after ...
<task> not frozen
PM: suspend exit
```

这不等同于 wakeup_count 竞态。此时应先确认是否存在持续运行的用户任务、内核线程或驱动
worker；只有在冻结成功且随后发生 GPIO 唤醒异常时，才继续归入本案例的 wakeup-source 路径。

### 步骤 6：应用修复并验证

在 `linux-4.19.125/drivers/soc/axera/wakeup_source/gpio_lp.c` 中：

- 在 `wakeup_gpio_lp_handler()` 的 `int_status` 分支内、唤醒等待队列之前调用
  `__pm_wakeup_event(gpio_lp->ws, 0)`；
- 在 `axera_gpio_lp_remove()` 中注销 `gpio_lp->ws`；
- 检查 probe 错误回滚路径，确保创建成功的 wakeup source 总能被注销。

不要仅在应用层增加重试、延长 suspend 延时或屏蔽 `wakeup_count`；这些措施可能改变现象，
但不能修复 GPIO 事件与 PM wakeup-source 状态之间的竞态。

## 6. 验证方案

### 5.1 功能验证矩阵

至少执行以下组合：

| 组合 | 预期结果 |
| --- | --- |
| 修复前 + 不使用应用层 wakeup_count | 记录短时唤醒丢失基线 |
| 修复前 + 使用应用层 wakeup_count | 记录无法进入休眠或写回失败基线 |
| 修复后 + 不使用应用层 wakeup_count | GPIO 唤醒事件不应因短时序列稳定性而丢失 |
| 修复后 + 正确使用应用层 wakeup_count | 能进入休眠；GPIO 唤醒后能正常恢复 |
| 修复后 + 多次 probe/remove（若产品支持） | 不应出现重复 wakeup source 或资源泄漏 |

每种组合建议至少进行多轮测试，并记录 GPIO pulse 延时，例如 1 ms、8 ms、15 ms、
几十毫秒和 500 ms 等代表性时序。不要只凭一次成功判断修复完成。

### 5.2 通过判据

同时满足以下条件才判定通过：

- 预期 GPIO 唤醒均能被系统观察到，不能只看应用是否偶尔拿到一帧；
- suspend 能在无并发唤醒事件时进入 deep sleep；
- `wakeup_count` 写回失败时，用户空间不会错误地继续进入 suspend；
- kernel 日志没有持续的 `Freezing of tasks aborted`；
- `AX_SYS_Sleep` 返回值符合平台 API 的成功定义；
- 修复不引入不可接受的唤醒延迟回归。

历史实验记录显示，使用 `gpio_lp.diff` 后“不再丢中断”，但同时出现唤醒时间变长：
去掉应用层 wakecount 的实验约为 46 ms，保留应用层 wakecount 的实验约为 50 ms。
因此验证时必须同时关注“唤醒可靠性”和“唤醒延迟”，不能只验证前者。

## 7. 常见误判

- **把 `GetDevFrame` 超时直接当成 GPIO 唤醒失败**：VIN、ISP、MIPI 或帧队列也可能导致取帧超时，必须结合 PM 和 GPIO 证据。
- **只看 `wakeup_count` 数值变化**：数值变化不能证明正确的 suspend 时序，必须检查读、准备、写回、请求 suspend 的完整协议。
- **只增加 suspend 前延时**：延时可能避开竞态窗口，但不是根因修复。
- **只修改应用层**：应用层无法替代 GPIO 驱动将中断事件上报为 PM wakeup event。
- **忽略 `Freezing of tasks aborted`**：冻结失败时系统根本没有完成正常 suspend，不应直接归因于 GPIO 唤醒。
- **只增加 `wakeup_source_register()` 而不在 IRQ 中调用 `__pm_wakeup_event()`**：注册对象本身不会自动记录 GPIO 中断事件。

## 8. 排查结果汇报模板

> 以下专用模板用于完整案例复盘、修复评审和结果沉淀。证据仍不完整或需要快速输出时，使用 [`references/response-template.md`](references/response-template.md)；代码入口和取证命令见 [`references/code-map.md`](references/code-map.md)，案例边界见 [`references/jira-cases.md`](references/jira-cases.md)。

```text
Jira/Skill：历史问题 / sdk-bsp-aov-diag-skill
平台与版本：
硬件与低功耗 GPIO：
是否使用应用层 wakeup_count：
复现次数/成功次数：

现象：
关键日志：
- 

wakeup_count 读写结果：
GPIO IRQ 状态及 gpio_lp handler 证据：
是否调用 __pm_wakeup_event：
是否出现 Freezing of tasks aborted：

判断：
- [ ] GPIO 事件未同步到 PM wakeup source
- [ ] wakeup_count 写回因并发事件失败
- [ ] suspend 冻结阶段失败
- [ ] VIN/ISP/帧队列独立问题

根因：
修复内容：
验证结果（唤醒可靠性/延迟）：
未解决问题：
```

## 9. 参考资料

- 代码入口、运行时节点、取证清单和日志关联：[`references/code-map.md`](references/code-map.md)
- 历史问题资料的案例元信息、适用边界和反证条件：[`references/jira-cases.md`](references/jira-cases.md)
- 快速诊断和证据不足时的结构化输出模板：[`references/response-template.md`](references/response-template.md)
- 详细的 Linux PM `wakeup_count` 机制、AX615 调试命令、复现实验和修复评审：[`references/diagnosis-flow.md`](references/diagnosis-flow.md)
- 历史问题资料中的原始标题和客户信息已移除。
- Jira 附件修复重点：`gpio_lp.c` IRQ handler 增加 `__pm_wakeup_event()`，remove 路径注销 wakeup source
