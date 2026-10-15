---
name: freertos-diagnose
description: FreeRTOS/RTOS 任务诊断与运行时分析工具。通过 GDB/J-Link/OpenOCD 连接目标设备，分析任务栈使用、CPU 占用率、死锁检测、队列/信号量/定时器状态、内存分配追踪。当用户提到 FreeRTOS、RTOS、任务栈、栈溢出、死锁、CPU 使用率、任务诊断、vTaskList、uxTaskGetStackHighWaterMark、queue、semaphore、mutex、timer 时自动触发。也兼容 /freertos-diagnose 显式调用。
---

# FreeRTOS Diagnose

FreeRTOS 运行时任务诊断、栈分析、死锁检测。

## 前置条件

- 目标设备运行 FreeRTOS，编译时开启调试 Hook：
  - `configUSE_TRACE_FACILITY = 1`
  - `configUSE_STATS_FORMATTING_FUNCTIONS = 1`
  - `configCHECK_FOR_STACK_OVERFLOW = 2`
- 通过 GDB (J-Link / OpenOCD / probe-rs) 连接目标

## 诊断工作流

### 1. 连接与挂起

```gdb
# 通过 J-Link GDB Server
arm-none-eabi-gdb -ex "target remote localhost:2331" firmware.elf
```

```gdb
monitor halt
```

### 2. 任务列表

```gdb
# 打印 FreeRTOS 任务列表（需 configUSE_TRACE_FACILITY）
call vTaskList((char*)0x20000000)
x/s 0x20000000
```

解析输出格式：
```
Task        State  Priority  Stack  Task#
IDLE        R      0         118    1
Task1       B      2         256    2
Task2       R      3         512    3
```

State: R=Running, B=Blocked, S=Suspended, D=Deleted

### 3. 栈高水位分析

```gdb
# 查看各任务栈高水位
call uxTaskGetStackHighWaterMark(Task1_Handle)
```

### 4. CPU 使用率

```gdb
# 打印运行时统计
call vTaskGetRunTimeStats((char*)0x20000000)
x/s 0x20000000
```

需要 `configGENERATE_RUN_TIME_STATS = 1` 并实现 `portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()`

### 5. 死锁检测

- 检查所有任务状态：若全部 BLOCKED 且等待互斥量/信号量 → 疑似死锁
- 检查 `uxQueueMessagesWaiting` 对每个队列
- 检查互斥量持有者：`pxCurrentTCB` vs `pxMutexHolder`

### 6. 队列/信号量检查

```gdb
# 查看队列中消息数
call uxQueueMessagesWaiting(Queue_Handle)
# 查看队列剩余空间
call uxQueueSpacesAvailable(Queue_Handle)
```

### 7. 任务控制块 (TCB) 直接检查

```gdb
# 查看当前 TCB
print *pxCurrentTCB
# 查看 TCB 关键字段
print/x pxCurrentTCB->pxTopOfStack
print/x pxCurrentTCB->ulRunTimeCounter
print   pxCurrentTCB->pcTaskName
```

## 常见问题与解决方案

| 症状 | 可能原因 | 检查方法 |
|------|---------|---------|
| HardFault | 栈溢出 | 检查栈高水位，确认 `configCHECK_FOR_STACK_OVERFLOW=2` |
| 任务不运行 | 优先级过低/死锁 | 检查 vTaskList 中 State 和 Priority |
| 内存耗尽 | 堆不足 | 检查 `xPortGetFreeHeapSize()` |
| 定时不准 | 时钟配置 | 检查 `xTaskGetTickCount()` 递增速度 |

## 脚本

- `scripts/gdb_freertos_dump.py` — 通过 GDB Python API 批量导出任务信息
- `scripts/stack_watermark.py` — 分析栈高水位历史数据
