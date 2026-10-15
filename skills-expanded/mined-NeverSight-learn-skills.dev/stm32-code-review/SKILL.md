---
name: stm32-code-review
description: This skill should be used when the user asks to "review STM32 code", "check my firmware", "find bugs in embedded code", "validate peripheral initialization", "audit interrupt configuration", "check DMA setup", "review HAL code", "code quality check", or needs an STM32-specific code quality and correctness review.
version: 1.0.0
---

# STM32 Code Review

Perform STM32-specific code review focusing on hardware correctness, peripheral configuration, and embedded best practices.

## Review Process

1. **Read the code** to be reviewed (all relevant source files)
2. **Identify STM32-specific concerns** using the checklist categories below
3. **Check against documentation** if available (reference manual in `docs/reference-manual/`)
4. **List issues by severity**: Critical (will cause failure), High (likely causes bugs), Medium (bad practice)
5. **Regenerate the code with all fixes applied**

## Review Checklist Categories

### 1. Clock Configuration
- RCC PLL settings produce the intended SYSCLK frequency
- Flash wait states (FLASH_ACR LATENCY) match the HCLK frequency
- APB1 prescaler respects maximum APB1 frequency
- APB2 prescaler respects maximum APB2 frequency
- Peripheral clocks are enabled BEFORE accessing peripheral registers
- HSE/HSI startup timeout is checked before proceeding

### 2. Peripheral Initialization Order
- GPIO port clock enabled before GPIO configuration
- Peripheral clock enabled before peripheral register access
- GPIO configured as alternate function BEFORE peripheral enable
- NVIC configured AFTER peripheral is set up
- DMA configured BEFORE peripheral DMA request is enabled
- Peripheral enable bit set LAST in the initialization sequence

### 3. Interrupt Configuration
- NVIC priority group is set once at startup (consistent grouping)
- Interrupt priorities are within valid range for the MCU's `__NVIC_PRIO_BITS`
- FreeRTOS boundary respected: ISR priority >= `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY` if calling FreeRTOS APIs
- All enabled interrupts have corresponding handler implementations
- Pending flags are cleared BEFORE enabling the interrupt
- No shared IRQ handler that only handles one source (check all flags)

### 4. DMA Configuration
- DMA stream/channel matches the peripheral (verify against RM DMA request mapping)
- Two peripherals do not share the same DMA stream (conflict)
- Transfer direction is correct (peripheral-to-memory, memory-to-peripheral, memory-to-memory)
- Data sizes match (peripheral and memory data width alignment)
- Circular mode used correctly (buffer overwrite considerations)
- DMA transfer complete flag is cleared before starting new transfer
- FIFO threshold is compatible with burst size (if FIFO enabled)
- DMA buffers are in DMA-accessible SRAM (NOT in CCM/TCM)
- DMA buffers are properly aligned (`__attribute__((aligned(4)))`)

### 5. Memory and Volatile
- `volatile` keyword on ALL hardware register access variables
- `volatile` on ALL variables shared between ISR and main context
- Proper memory barriers where needed (`__DSB()`, `__ISB()` after SCB writes)
- DMA buffers not in CCM/DTCM RAM (these are not DMA-accessible)
- Stack size sufficient for worst-case call depth + ISR nesting
- Heap size adequate for dynamic allocations
- No buffer overflows in ISR context

### 6. HAL-Specific Patterns (if using HAL)
- `HAL_*_MspInit()` callbacks properly implemented
- Error callbacks registered (`HAL_*_ErrorCallback`)
- `HAL_Delay()` not called from ISR context (will hang)
- `HAL_GetTick()` returns correct time (SysTick/timer properly configured)
- HAL lock mechanism not causing deadlocks
- `HAL_*_IRQHandler()` called from the correct IRQHandler function

### 7. Register-Level Patterns (if bare-metal)
- Read-modify-write sequences use |= for set, &= ~ for clear (not direct assignment unless intentional)
- Bit positions use defined constants, not magic numbers
- Status flags cleared correctly (some clear on read, some write-1-to-clear)
- Reserved bits not modified (preserve with read-modify-write)

### 8. Timing and Watchdog
- SystemCoreClock matches actual clock frequency
- Delay functions account for instruction cycles at the configured frequency
- Watchdog fed in main loop and/or critical tasks
- Timeout mechanisms in polling loops (no infinite wait on hardware flags)

### 9. Security
- RDP level appropriate for the deployment stage
- Debug interface disabled in production builds (if required)
- Stack canaries enabled for security-critical code
- No sensitive data in unprotected Flash sectors

## Severity Levels

- **Critical**: Will cause hard fault, data corruption, peripheral malfunction, or security breach
- **High**: Will likely cause intermittent bugs, race conditions, or incorrect behavior
- **Medium**: Bad practice, maintainability issue, or potential for future bugs

## Output Format

```
## Code Review Results

### Critical Issues
1. **[File:Line]** [Description]
   - **Problem**: [What's wrong]
   - **Impact**: [What will happen]
   - **Fix**: [How to fix it]

### High Issues
1. **[File:Line]** [Description]
   ...

### Medium Issues
1. **[File:Line]** [Description]
   ...

### Summary
- Critical: [count]
- High: [count]
- Medium: [count]

## Fixed Code
[Regenerated code with all fixes applied]
```

## Additional Resources

- **`references/review-checklist.md`** - Exhaustive per-category checklist with pass/fail criteria and common STM32 bugs
