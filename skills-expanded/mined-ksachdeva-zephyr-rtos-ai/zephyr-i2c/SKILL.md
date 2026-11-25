---
name: zephyr-i2c
description: "Comprehensive Zephyr I2C subsystem expertise for Inter-Integrated Circuit bus communication. Use when: (1) Configuring I2C controllers or devices via devicetree or Kconfig, (2) Implementing synchronous I2C transfers with i2c_transfer/i2c_read/i2c_write, (3) Using register access helpers like i2c_reg_read_byte/i2c_reg_write_byte, (4) Implementing asynchronous I2C with i2c_transfer_cb or RTIO, (5) Setting up I2C speed modes (standard 100kHz, fast 400kHz, fast-plus 1MHz), (6) Implementing I2C target/slave mode with callbacks, (7) Using SMBus protocol functions, (8) Troubleshooting I2C communication issues (NACK, bus stuck, clock stretching)."
---

# Zephyr I2C

Expert guidance for Zephyr's I2C driver subsystem covering synchronous and asynchronous transfer APIs, target/slave mode, devicetree configuration, and common usage patterns.

## Table of Contents

1. [API Selection](#api-selection)
2. [Getting Device Reference](#getting-device-reference)
3. [Common Workflows](#common-workflows)
4. [Configuration](#configuration)
5. [Target Mode](#target-mode)
6. [Error Handling](#error-handling)
7. [Troubleshooting](#troubleshooting)

---

## API Selection

Zephyr provides multiple I2C access methods. Choose based on requirements:

| API | Kconfig | Use Case | Blocking? |
|-----|---------|----------|-----------|
| **Synchronous** | (default) | Simple transfers, blocking until complete | Yes |
| **Async Callback** | `CONFIG_I2C_CALLBACK` | Non-blocking with completion callback | No |
| **RTIO** | `CONFIG_I2C_RTIO` | Real-time I/O subsystem integration | No |
| **Target Mode** | `CONFIG_I2C_TARGET` | Act as I2C peripheral/slave device | N/A |

### Decision Tree

```
Simple blocking transfer? -> Synchronous (i2c_transfer, i2c_write_read)
Register read/write? -> Helpers (i2c_reg_read_byte, i2c_reg_write_byte)
Need non-blocking? -> Async callback (i2c_transfer_cb)
RTIO integration? -> RTIO API (i2c_rtio_copy)
Respond to controller? -> Target mode (i2c_target_register)
SMBus protocol? -> SMBus API (smbus_byte_data_read, etc.)
```

---

## Getting Device Reference

### From Devicetree (Preferred - for I2C Devices)

Use `I2C_DT_SPEC_GET` to get a complete I2C specification including bus and address:

```c
#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>

/* Define the I2C device from devicetree */
#define MY_I2C_DEVICE DT_NODELABEL(my_sensor)

static const struct i2c_dt_spec i2c_dev = I2C_DT_SPEC_GET(MY_I2C_DEVICE);

/* Runtime check (in main or init) */
if (!i2c_is_ready_dt(&i2c_dev)) {
    printk("I2C device not ready\n");
    return -ENODEV;
}
```

### Direct Controller Access

```c
/* Get I2C controller directly */
const struct device *i2c = DEVICE_DT_GET(DT_NODELABEL(i2c0));

if (!device_is_ready(i2c)) {
    return -ENODEV;
}

/* Use with explicit address */
#define SENSOR_ADDR 0x48
ret = i2c_read(i2c, buf, sizeof(buf), SENSOR_ADDR);
```

### From Device Node on Bus

```c
/* Device defined as child of I2C controller in DTS */
#define CODEC_NODE DT_NODELABEL(wm8731)

const struct device *i2c_bus = DEVICE_DT_GET(DT_BUS(CODEC_NODE));
uint16_t addr = DT_REG_ADDR(CODEC_NODE);
```

---

## Common Workflows

### 1. Simple Write

```c
#include <zephyr/drivers/i2c.h>

uint8_t data[] = {0x01, 0x02, 0x03};

/* Using i2c_dt_spec */
int ret = i2c_write_dt(&i2c_dev, data, sizeof(data));
if (ret < 0) {
    printk("I2C write error: %d\n", ret);
}

/* Using device + address */
ret = i2c_write(i2c, data, sizeof(data), SENSOR_ADDR);
```

### 2. Simple Read

```c
uint8_t rx_buf[4];

int ret = i2c_read_dt(&i2c_dev, rx_buf, sizeof(rx_buf));
if (ret < 0) {
    printk("I2C read error: %d\n", ret);
}
```

### 3. Write-Then-Read (Most Common Pattern)

Combined transaction with RESTART condition - typical for register access:

```c
uint8_t reg_addr = 0x00;  /* Register to read */
uint8_t rx_data[2];

int ret = i2c_write_read_dt(&i2c_dev, &reg_addr, 1, rx_data, sizeof(rx_data));
if (ret < 0) {
    printk("I2C write-read error: %d\n", ret);
}
```

### 4. Register Access Helpers

Convenient functions for single-byte register operations:

```c
uint8_t value;

/* Read register */
ret = i2c_reg_read_byte_dt(&i2c_dev, 0x0F, &value);  /* Read WHO_AM_I */

/* Write register */
ret = i2c_reg_write_byte_dt(&i2c_dev, 0x20, 0x47);  /* Write CTRL_REG1 */

/* Read-modify-write with mask */
ret = i2c_reg_update_byte_dt(&i2c_dev, 0x20, 0x07, 0x05);  /* Update bits 0-2 */
```

### 5. Burst Read/Write (Multi-byte Register Access)

```c
uint8_t data[6];

/* Read 6 bytes starting from register 0x28 */
ret = i2c_burst_read_dt(&i2c_dev, 0x28, data, sizeof(data));

/* Write 4 bytes starting from register 0x20 */
uint8_t config[] = {0x47, 0x00, 0x00, 0x88};
ret = i2c_burst_write_dt(&i2c_dev, 0x20, config, sizeof(config));
```

### 6. Multi-Message Transfer (Scatter-Gather)

For complex transactions requiring multiple operations in one bus lock:

```c
struct i2c_msg msgs[2];

uint8_t cmd = 0x9F;  /* Command byte */
uint8_t rx_buf[4];

/* First message: write command */
msgs[0].buf = &cmd;
msgs[0].len = 1;
msgs[0].flags = I2C_MSG_WRITE;

/* Second message: read response */
msgs[1].buf = rx_buf;
msgs[1].len = sizeof(rx_buf);
msgs[1].flags = I2C_MSG_RESTART | I2C_MSG_READ | I2C_MSG_STOP;

int ret = i2c_transfer_dt(&i2c_dev, msgs, ARRAY_SIZE(msgs));
if (ret < 0) {
    printk("I2C transfer error: %d\n", ret);
}
```

### 7. Async Transfer with Callback

Requires `CONFIG_I2C_CALLBACK=y`:

```c
#include <zephyr/drivers/i2c.h>

static volatile bool transfer_done;
static int transfer_result;

void i2c_callback(const struct device *dev, int result, void *userdata)
{
    transfer_result = result;
    transfer_done = true;
}

int async_transfer(void)
{
    struct i2c_msg msgs[1];
    uint8_t data[] = {0x01, 0x02};

    msgs[0].buf = data;
    msgs[0].len = sizeof(data);
    msgs[0].flags = I2C_MSG_WRITE | I2C_MSG_STOP;

    transfer_done = false;

    int ret = i2c_transfer_cb(i2c_dev.bus, msgs, 1, i2c_dev.addr,
                              i2c_callback, NULL);
    if (ret < 0) {
        return ret;
    }

    /* Do other work while transfer is in progress */

    /* Wait for completion */
    while (!transfer_done) {
        k_yield();
    }

    return transfer_result;
}
```

- **Full async API details**: See [references/api.md](references/api.md)

---

## Configuration

### Kconfig Essentials

```kconfig
CONFIG_I2C=y                    # Enable I2C driver subsystem
CONFIG_I2C_CALLBACK=y           # Enable async callback API
CONFIG_I2C_RTIO=y               # Enable RTIO API (experimental)
CONFIG_I2C_TARGET=y             # Enable target/slave mode
CONFIG_I2C_SHELL=y              # Enable I2C shell for debugging
CONFIG_I2C_DUMP_MESSAGES=y      # Log all I2C transactions (debug)
```

- **Full Kconfig reference**: See [references/kconfig.md](references/kconfig.md)

### Devicetree Essentials

#### I2C Controller

```dts
&i2c0 {
    status = "okay";
    pinctrl-0 = <&i2c0_default>;
    pinctrl-names = "default";
    clock-frequency = <I2C_BITRATE_FAST>;  /* 400 kHz */

    my_sensor: sensor@48 {
        compatible = "vendor,sensor";
        reg = <0x48>;                       /* 7-bit I2C address */
    };
};
```

#### Speed Constants (clock-frequency)

| Constant | Speed |
|----------|-------|
| `I2C_BITRATE_STANDARD` | 100 kHz |
| `I2C_BITRATE_FAST` | 400 kHz |
| `I2C_BITRATE_FAST_PLUS` | 1 MHz |
| `I2C_BITRATE_HIGH` | 3.4 MHz |
| `I2C_BITRATE_ULTRA` | 5 MHz |

- **Full devicetree reference**: See [references/devicetree.md](references/devicetree.md)

### Message Flags

Common flags for `i2c_msg.flags`:

| Flag | Description |
|------|-------------|
| `I2C_MSG_WRITE` | Write operation (0) |
| `I2C_MSG_READ` | Read operation |
| `I2C_MSG_STOP` | Send STOP after this message |
| `I2C_MSG_RESTART` | Send RESTART before this message |
| `I2C_MSG_ADDR_10_BITS` | Use 10-bit addressing |

---

## Target Mode

I2C target (slave) mode allows the device to respond to an external controller.

### Target Callbacks Setup

```c
#include <zephyr/drivers/i2c.h>

static uint8_t rx_buffer[32];
static uint8_t tx_buffer[32];
static size_t rx_index;

/* Called when controller initiates write */
static int target_write_requested(struct i2c_target_config *cfg)
{
    rx_index = 0;
    return 0;
}

/* Called for each byte received */
static int target_write_received(struct i2c_target_config *cfg, uint8_t val)
{
    if (rx_index < sizeof(rx_buffer)) {
        rx_buffer[rx_index++] = val;
    }
    return 0;
}

/* Called when controller initiates read */
static int target_read_requested(struct i2c_target_config *cfg, uint8_t *val)
{
    *val = tx_buffer[0];
    return 0;
}

/* Called after each byte sent to controller */
static int target_read_processed(struct i2c_target_config *cfg, uint8_t *val)
{
    *val = tx_buffer[1];  /* Next byte to send */
    return 0;
}

/* Called on STOP condition */
static int target_stop(struct i2c_target_config *cfg)
{
    /* Process received data */
    return 0;
}

static struct i2c_target_callbacks target_callbacks = {
    .write_requested = target_write_requested,
    .write_received = target_write_received,
    .read_requested = target_read_requested,
    .read_processed = target_read_processed,
    .stop = target_stop,
};

static struct i2c_target_config target_cfg = {
    .address = 0x60,
    .callbacks = &target_callbacks,
};

/* Register as target */
const struct device *i2c_bus = DEVICE_DT_GET(DT_NODELABEL(i2c0));

if (i2c_target_register(i2c_bus, &target_cfg) < 0) {
    printk("Failed to register I2C target\n");
}
```

### Using EEPROM Target Driver

Zephyr provides a virtual EEPROM target driver:

```dts
&i2c0 {
    eeprom0: eeprom@52 {
        compatible = "zephyr,i2c-target-eeprom";
        reg = <0x52>;
        size = <256>;
    };
};
```

```c
const struct device *eeprom = DEVICE_DT_GET(DT_NODELABEL(eeprom0));

if (i2c_target_driver_register(eeprom) < 0) {
    printk("Failed to register EEPROM target\n");
}
```

---

## Error Handling

### Return Values

| Value | Meaning |
|-------|---------|
| `0` | Success |
| `-ENOTSUP` | Operation not supported |
| `-EINVAL` | Invalid parameter |
| `-EIO` | I/O error (NACK, bus error) |
| `-EBUSY` | Bus busy |
| `-ETIMEDOUT` | Transfer timeout |

### Robust Error Handling Pattern

```c
int read_sensor_data(const struct i2c_dt_spec *dev, uint8_t reg, uint8_t *data, size_t len)
{
    int ret;
    int retries = 3;

    while (retries--) {
        ret = i2c_burst_read_dt(dev, reg, data, len);
        if (ret == 0) {
            return 0;
        }
        if (ret == -ETIMEDOUT || ret == -EIO) {
            /* Try bus recovery */
            i2c_recover_bus(dev->bus);
            k_msleep(10);
            continue;
        }
        return ret;  /* Non-recoverable error */
    }
    return -EIO;
}
```

### Bus Recovery

```c
/* Attempt to recover stuck bus (9 clock pulses) */
int ret = i2c_recover_bus(i2c_dev.bus);
if (ret < 0) {
    printk("Bus recovery failed: %d\n", ret);
}
```

---

## Troubleshooting

### Quick Reference

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| No ACK / -EIO | Wrong address, device not powered | Verify address (7-bit), check power |
| Bus stuck | Device holding SDA low | Call `i2c_recover_bus()` |
| Timeout | Clock stretching too long | Increase timeout config |
| Garbled data | Speed too high | Reduce `clock-frequency` |
| Device not found | Wrong controller | Verify DT node hierarchy |
| `-ENOTSUP` | Missing driver feature | Check Kconfig options |

### Debug Checklist

1. **Device ready?** Check `i2c_is_ready_dt(&spec)` or `device_is_ready(dev)`
2. **Address correct?** I2C uses 7-bit addresses (0x00-0x7F)
3. **Pins configured?** Verify pinctrl in devicetree
4. **Pull-ups present?** I2C requires pull-up resistors on SDA/SCL
5. **Speed valid?** Start with `I2C_BITRATE_STANDARD` (100kHz)
6. **Power sequence?** Some devices need power-on delay

### I2C Shell Commands

Enable with `CONFIG_I2C_SHELL=y`:

```shell
# Scan for devices on bus
i2c scan i2c@40003000

# Read register
i2c read_byte i2c@40003000 0x48 0x00

# Write register
i2c write_byte i2c@40003000 0x48 0x20 0x47

# Recover bus
i2c recover i2c@40003000
```

---

## References

- [references/api.md](references/api.md) - Full API function reference with async and RTIO
- [references/devicetree.md](references/devicetree.md) - Devicetree properties and examples
- [references/kconfig.md](references/kconfig.md) - All I2C Kconfig options

## Source Locations

Key files in Zephyr source tree:
- `include/zephyr/drivers/i2c.h` - Public API header
- `include/zephyr/drivers/smbus.h` - SMBus API header
- `drivers/i2c/` - Driver implementations
- `dts/bindings/i2c/i2c-controller.yaml` - Controller DTS binding
- `dts/bindings/i2c/i2c-device.yaml` - Device DTS binding
- `samples/drivers/i2c/` - Sample applications
