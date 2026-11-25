---
name: zephyr-uart
description: "Comprehensive Zephyr UART subsystem expertise for serial communication. Use when: (1) Configuring UART peripherals via devicetree or Kconfig, (2) Implementing polling-based UART read/write with uart_poll_in/uart_poll_out, (3) Implementing interrupt-driven UART with uart_irq_* functions and callbacks, (4) Implementing async DMA-based UART with uart_tx/uart_rx_enable and event callbacks, (5) Choosing between polling, interrupt, or async APIs for a use case, (6) Troubleshooting UART communication issues (baud rate, flow control, errors), (7) Understanding UART configuration structures (parity, stop bits, data bits, flow control)."
---

# Zephyr UART

Expert guidance for Zephyr's UART driver subsystem covering three API modes: polling, interrupt-driven, and asynchronous (DMA).

## Table of Contents

1. [API Selection](#api-selection)
2. [Getting Device Reference](#getting-device-reference)
3. [Common Workflows](#common-workflows)
4. [Configuration](#configuration)
5. [Error Handling](#error-handling)
6. [Troubleshooting](#troubleshooting)

---

## API Selection

Zephyr provides three UART access methods. Choose based on requirements:

| API | Kconfig | Use Case | Blocking? |
|-----|---------|----------|-----------|
| **Polling** | (default) | Simple, low-throughput, debug output | Yes (TX), No (RX) |
| **Interrupt-driven** | `CONFIG_UART_INTERRUPT_DRIVEN` | Background RX, medium throughput | No |
| **Async (DMA)** | `CONFIG_UART_ASYNC_API` | High throughput, zero-copy, low CPU | No |

### Decision Tree

```
Need simple debug output? → Polling
Need background receive? → Interrupt-driven
Need high throughput + low CPU? → Async (DMA)
Need both RX and TX without blocking? → Interrupt-driven or Async
```

### API Mutual Exclusivity

**WARNING**: Interrupt-driven and Async APIs must NOT be used simultaneously on the same peripheral. Both require hardware interrupts. `CONFIG_UART_EXCLUSIVE_API_CALLBACKS=y` (default) ensures only one callback type is active.

---

## Getting Device Reference

### From Devicetree (Preferred)

```c
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>

/* Using chosen node (common for console) */
#define UART_NODE DT_CHOSEN(zephyr_shell_uart)
static const struct device *const uart_dev = DEVICE_DT_GET(UART_NODE);

/* Using specific node label */
#define UART_NODE DT_NODELABEL(uart0)
static const struct device *const uart_dev = DEVICE_DT_GET(UART_NODE);

/* Runtime check (in main or init) */
if (!device_is_ready(uart_dev)) {
    printk("UART device not ready\n");
    return -ENODEV;
}
```

---

## Common Workflows

### 1. Polling API (Simplest)

Best for debug output or simple blocking TX.

```c
#include <zephyr/drivers/uart.h>

/* TX: Blocking - waits until character sent */
void print_uart(const char *str)
{
    while (*str) {
        uart_poll_out(uart_dev, *str++);
    }
}

/* RX: Non-blocking - returns -1 if no data */
int read_char(void)
{
    unsigned char c;
    if (uart_poll_in(uart_dev, &c) == 0) {
        return c;
    }
    return -1;
}
```

- **Full API details**: See [references/polling.md](references/polling.md)

### 2. Interrupt-Driven API

Best for background receive with message queues.

```c
#include <zephyr/drivers/uart.h>

K_MSGQ_DEFINE(uart_msgq, 32, 10, 4);
static char rx_buf[32];
static int rx_pos;

void uart_isr(const struct device *dev, void *user_data)
{
    if (!uart_irq_update(dev)) return;
    if (!uart_irq_rx_ready(dev)) return;

    uint8_t c;
    while (uart_fifo_read(dev, &c, 1) == 1) {
        if (c == '\n' || c == '\r') {
            rx_buf[rx_pos] = '\0';
            k_msgq_put(&uart_msgq, rx_buf, K_NO_WAIT);
            rx_pos = 0;
        } else if (rx_pos < sizeof(rx_buf) - 1) {
            rx_buf[rx_pos++] = c;
        }
    }
}

int setup_uart_irq(void)
{
    int ret = uart_irq_callback_user_data_set(uart_dev, uart_isr, NULL);
    if (ret < 0) return ret;
    uart_irq_rx_enable(uart_dev);
    return 0;
}
```

- **Full ISR patterns & TX handling**: See [references/interrupt.md](references/interrupt.md)

### 3. Async API (DMA)

Best for high throughput with minimal CPU usage.

```c
#include <zephyr/drivers/uart.h>

uint8_t rx_buf[2][64];
volatile int rx_buf_idx;

void uart_async_cb(const struct device *dev, struct uart_event *evt, void *data)
{
    switch (evt->type) {
    case UART_TX_DONE:
        /* TX complete - buffer can be reused */
        break;
    case UART_RX_RDY:
        /* Data available: evt->data.rx.buf + evt->data.rx.offset, len: evt->data.rx.len */
        process_data(evt->data.rx.buf + evt->data.rx.offset, evt->data.rx.len);
        break;
    case UART_RX_BUF_REQUEST:
        /* Provide next buffer for continuous reception */
        uart_rx_buf_rsp(dev, rx_buf[rx_buf_idx], sizeof(rx_buf[0]));
        rx_buf_idx = rx_buf_idx ? 0 : 1;
        break;
    case UART_RX_DISABLED:
        /* RX stopped - can re-enable */
        break;
    default:
        break;
    }
}

int setup_uart_async(void)
{
    uart_callback_set(uart_dev, uart_async_cb, NULL);
    rx_buf_idx = 1;
    return uart_rx_enable(uart_dev, rx_buf[0], sizeof(rx_buf[0]), 100 /* timeout_us */);
}
```

- **Full event handling & buffer management**: See [references/async.md](references/async.md)

---

## Configuration

### Kconfig Essentials

```kconfig
CONFIG_SERIAL=y                    # Enable serial driver subsystem
CONFIG_UART_INTERRUPT_DRIVEN=y     # Enable interrupt API
CONFIG_UART_ASYNC_API=y            # Enable async/DMA API
CONFIG_UART_USE_RUNTIME_CONFIGURE=y # Runtime baud/parity changes
CONFIG_UART_LINE_CTRL=y            # Line control (RTS/CTS/DTR)
```

- **Full Kconfig reference**: See [references/kconfig.md](references/kconfig.md)

### Devicetree Essentials

```dts
&uart0 {
    status = "okay";
    current-speed = <115200>;
    hw-flow-control;  /* Enable RTS/CTS */
    pinctrl-0 = <&uart0_default>;
    pinctrl-names = "default";
};
```

- **Full devicetree reference**: See [references/devicetree.md](references/devicetree.md)

### Runtime Configuration

```c
struct uart_config cfg = {
    .baudrate = 115200,
    .parity = UART_CFG_PARITY_NONE,
    .stop_bits = UART_CFG_STOP_BITS_1,
    .data_bits = UART_CFG_DATA_BITS_8,
    .flow_ctrl = UART_CFG_FLOW_CTRL_NONE,
};
uart_configure(uart_dev, &cfg);
```

---

## Error Handling

### Error Types

| Error | Value | Cause |
|-------|-------|-------|
| `UART_ERROR_OVERRUN` | 0x01 | Data lost - not read fast enough |
| `UART_ERROR_PARITY` | 0x02 | Parity mismatch |
| `UART_ERROR_FRAMING` | 0x04 | Stop bit not detected |
| `UART_BREAK` | 0x08 | Break condition (line held low) |
| `UART_ERROR_COLLISION` | 0x10 | RS-485 TX/RX collision |
| `UART_ERROR_NOISE` | 0x20 | Noise on line |

### Checking Errors

```c
int err = uart_err_check(uart_dev);
if (err & UART_ERROR_OVERRUN) {
    /* Handle overrun */
}
```

---

## Troubleshooting

### Quick Reference

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| No data received | Wrong baud rate | Verify `current-speed` in DTS matches sender |
| Garbled data | Baud rate mismatch | Check both ends use same baud rate |
| TX hangs | Flow control mismatch | Disable `hw-flow-control` or connect CTS |
| RX callback not called | IRQ not enabled | Call `uart_irq_rx_enable()` |
| `-ENOTSUP` from API | API not enabled | Enable `CONFIG_UART_INTERRUPT_DRIVEN` or `CONFIG_UART_ASYNC_API` |
| `-EBUSY` on rx_enable | RX already active | Call `uart_rx_disable()` first |
| Overrun errors | Not reading fast enough | Increase buffer size, use async API |

### Debug Checklist

1. **Device ready?** Check `device_is_ready(uart_dev)`
2. **Pins correct?** Verify pinctrl in devicetree
3. **Baud rate match?** Both ends must match
4. **Flow control?** If enabled, CTS must be asserted for TX
5. **API enabled?** Check Kconfig for required API

---

## References

- [references/polling.md](references/polling.md) — Polling API functions and patterns
- [references/interrupt.md](references/interrupt.md) — Interrupt-driven API, ISR patterns, TX handling
- [references/async.md](references/async.md) — Async/DMA API, event handling, buffer management
- [references/kconfig.md](references/kconfig.md) — All UART Kconfig options
- [references/devicetree.md](references/devicetree.md) — Devicetree properties and examples

## Source Locations

Key files in Zephyr source tree:
- `include/zephyr/drivers/uart.h` — Public API header
- `drivers/serial/` — Driver implementations
- `dts/bindings/serial/uart-controller.yaml` — Base DTS binding
- `samples/drivers/uart/` — Sample applications
