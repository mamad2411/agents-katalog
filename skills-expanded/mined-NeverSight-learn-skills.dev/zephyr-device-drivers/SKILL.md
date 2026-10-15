---
name: zephyr-device-drivers
description: "Comprehensive Zephyr device driver expertise covering driver model, device instances, initialization levels, power management, and bus-specific patterns (I2C, SPI, UART, GPIO). Use this skill when you need to: (1) Create custom device drivers from scratch, (2) Use existing driver APIs (GPIO, I2C, SPI, UART, ADC, PWM, etc.), (3) Understand DEVICE_DT_DEFINE and device model concepts, (4) Write sensor drivers using the sensor subsystem, (5) Implement bus-specific device drivers, (6) Test drivers with Ztest, emulators, or fakes, (7) Debug driver initialization or runtime issues."
---

# Zephyr Device Drivers

Expert guidance on Zephyr's device driver model, creating custom drivers, using existing driver APIs, and implementing bus-specific device patterns.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Concepts](#core-concepts)
3. [Using Existing Drivers](#using-existing-drivers)
4. [Creating Custom Drivers](#creating-custom-drivers)
5. [Bus-Specific Patterns](#bus-specific-patterns)
6. [Sensor Subsystem](#sensor-subsystem)
7. [Testing Drivers](#testing-drivers)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Using an Existing Driver

```c
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

/* Get device from devicetree */
const struct device *gpio_dev = DEVICE_DT_GET(DT_NODELABEL(gpio0));

/* Check device is ready */
if (!device_is_ready(gpio_dev)) {
    printk("GPIO device not ready\n");
    return -ENODEV;
}

/* Use driver API */
gpio_pin_configure(gpio_dev, 13, GPIO_OUTPUT_ACTIVE);
gpio_pin_set(gpio_dev, 13, 1);
```

### Minimal Custom Driver Structure

```c
#define DT_DRV_COMPAT vendor_mydevice

struct mydevice_config {
    /* Immutable config from devicetree */
};

struct mydevice_data {
    /* Runtime mutable state */
};

static int mydevice_init(const struct device *dev)
{
    return 0;
}

#define MYDEVICE_INIT(inst)                                     \
    static struct mydevice_data mydevice_data_##inst;           \
    static const struct mydevice_config mydevice_config_##inst; \
    DEVICE_DT_INST_DEFINE(inst, mydevice_init, NULL,            \
                          &mydevice_data_##inst,                \
                          &mydevice_config_##inst,              \
                          POST_KERNEL,                          \
                          CONFIG_KERNEL_INIT_PRIORITY_DEVICE,   \
                          NULL);

DT_INST_FOREACH_STATUS_OKAY(MYDEVICE_INIT)
```

---

## Core Concepts

### Device Model Overview

Zephyr's device model provides:
- **Static device definitions** at compile time via devicetree
- **Lazy initialization** based on initialization levels
- **API abstraction** through driver API structures
- **Power management** integration

For complete device model details: See [driver-model.md](references/driver-model.md)

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| `struct device` | Runtime device handle | `const struct device *dev` |
| Config structure | Immutable HW config | Base address, IRQ, pins |
| Data structure | Mutable runtime state | Buffers, locks, counters |
| Driver API | Subsystem operations | `gpio_driver_api`, `i2c_driver_api` |

### Initialization Levels

Devices initialize in order:

| Level | Typical Use |
|-------|-------------|
| `EARLY` | Architecture-specific, before main memory |
| `PRE_KERNEL_1` | Drivers without dependencies |
| `PRE_KERNEL_2` | Drivers depending on PRE_KERNEL_1 |
| `POST_KERNEL` | Most drivers (default) |
| `APPLICATION` | Application-specific init |

---

## Using Existing Drivers

### Device Acquisition Pattern

```c
/* Method 1: From node label (most common) */
const struct device *dev = DEVICE_DT_GET(DT_NODELABEL(my_sensor));

/* Method 2: From alias */
const struct device *dev = DEVICE_DT_GET(DT_ALIAS(led0));

/* Method 3: From chosen node */
const struct device *dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));

/* Method 4: From compatible (first match) */
const struct device *dev = DEVICE_DT_GET_ANY(bosch_bme280);

/* ALWAYS check readiness */
if (!device_is_ready(dev)) {
    return -ENODEV;
}
```

### Common Driver APIs

| Subsystem | Header | Key Functions |
|-----------|--------|---------------|
| GPIO | `<zephyr/drivers/gpio.h>` | `gpio_pin_configure()`, `gpio_pin_set()`, `gpio_pin_get()` |
| I2C | `<zephyr/drivers/i2c.h>` | `i2c_write()`, `i2c_read()`, `i2c_transfer()` |
| SPI | `<zephyr/drivers/spi.h>` | `spi_transceive()`, `spi_write()`, `spi_read()` |
| UART | `<zephyr/drivers/uart.h>` | `uart_poll_out()`, `uart_irq_rx_enable()` |
| ADC | `<zephyr/drivers/adc.h>` | `adc_channel_setup()`, `adc_read()` |
| PWM | `<zephyr/drivers/pwm.h>` | `pwm_set_pulse_dt()` |
| Sensor | `<zephyr/drivers/sensor.h>` | `sensor_sample_fetch()`, `sensor_channel_get()` |

For detailed API usage: See [driver-apis.md](references/driver-apis.md)

---

## Creating Custom Drivers

### Driver File Structure

```
drivers/mydriver/
├── CMakeLists.txt          # Build integration
├── Kconfig                 # Configuration options
├── mydriver.c              # Driver implementation
└── dts/bindings/           # Devicetree bindings (optional location)
    └── vendor,mydriver.yaml
```

### Step-by-Step Guide

1. **Define DT binding** (YAML)
2. **Create Kconfig** for driver
3. **Implement driver** with DEVICE_DT_INST_DEFINE
4. **Add devicetree node** to board/overlay
5. **Enable in prj.conf**

For complete walkthrough: See [driver-creation.md](references/driver-creation.md)

### Critical Macros

```c
/* MUST define before includes */
#define DT_DRV_COMPAT vendor_device_name

/* Get instance count */
#define NUM_INSTANCES DT_NUM_INST_STATUS_OKAY(DT_DRV_COMPAT)

/* Access instance properties */
DT_INST_PROP(inst, property_name)
DT_INST_REG_ADDR(inst)
DT_INST_IRQ(inst, irq)

/* Define device for each instance */
DEVICE_DT_INST_DEFINE(inst, init_fn, pm, data, config, level, prio, api);

/* Iterate all instances */
DT_INST_FOREACH_STATUS_OKAY(MACRO_NAME)
```

---

## Bus-Specific Patterns

### I2C Device Driver

```c
#define DT_DRV_COMPAT vendor_i2c_sensor

struct sensor_config {
    struct i2c_dt_spec i2c;
};

static int sensor_init(const struct device *dev)
{
    const struct sensor_config *cfg = dev->config;

    if (!i2c_is_ready_dt(&cfg->i2c)) {
        return -ENODEV;
    }
    /* Read chip ID, configure, etc. */
    return 0;
}

#define SENSOR_INIT(inst)                                       \
    static const struct sensor_config sensor_config_##inst = {  \
        .i2c = I2C_DT_SPEC_INST_GET(inst),                      \
    };                                                          \
    DEVICE_DT_INST_DEFINE(inst, sensor_init, NULL, NULL,        \
                          &sensor_config_##inst, POST_KERNEL,   \
                          CONFIG_SENSOR_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(SENSOR_INIT)
```

### SPI Device Driver

```c
#define DT_DRV_COMPAT vendor_spi_device

struct device_config {
    struct spi_dt_spec spi;
};

static int device_init(const struct device *dev)
{
    const struct device_config *cfg = dev->config;

    if (!spi_is_ready_dt(&cfg->spi)) {
        return -ENODEV;
    }
    return 0;
}

#define DEVICE_INIT(inst)                                       \
    static const struct device_config device_config_##inst = {  \
        .spi = SPI_DT_SPEC_INST_GET(inst,                       \
                   SPI_WORD_SET(8) | SPI_TRANSFER_MSB, 0),      \
    };                                                          \
    DEVICE_DT_INST_DEFINE(inst, device_init, NULL, NULL,        \
                          &device_config_##inst, POST_KERNEL,   \
                          CONFIG_SPI_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(DEVICE_INIT)
```

For GPIO, UART, and more patterns: See [bus-drivers.md](references/bus-drivers.md)

---

## Sensor Subsystem

Sensors use a standardized API with channels and triggers.

### Implementing a Sensor Driver

```c
#define DT_DRV_COMPAT vendor_temp_sensor

static int sensor_sample_fetch(const struct device *dev,
                               enum sensor_channel chan)
{
    /* Read raw data from hardware */
    return 0;
}

static int sensor_channel_get(const struct device *dev,
                              enum sensor_channel chan,
                              struct sensor_value *val)
{
    if (chan != SENSOR_CHAN_AMBIENT_TEMP) {
        return -ENOTSUP;
    }
    /* Convert to sensor_value (val1=integer, val2=micro) */
    val->val1 = 25;
    val->val2 = 500000;  /* 25.5 degrees */
    return 0;
}

static const struct sensor_driver_api sensor_api = {
    .sample_fetch = sensor_sample_fetch,
    .channel_get = sensor_channel_get,
};
```

For triggers, emulators, and more: See [sensor-drivers.md](references/sensor-drivers.md)

---

## Testing Drivers

### Ztest for Drivers

```c
#include <zephyr/ztest.h>
#include <zephyr/device.h>

ZTEST(driver_tests, test_device_ready)
{
    const struct device *dev = DEVICE_DT_GET(DT_NODELABEL(test_device));
    zassert_true(device_is_ready(dev), "Device not ready");
}

ZTEST_SUITE(driver_tests, NULL, NULL, NULL, NULL, NULL);
```

### Using Emulators

Enable emulation in `prj.conf`:
```
CONFIG_EMUL=y
CONFIG_I2C_EMUL=y
```

For test fixtures, fakes, and more: See [driver-testing.md](references/driver-testing.md)

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `device_is_ready()` returns false | Device not initialized | Check `status = "okay"`, Kconfig enabled |
| `__device_dts_ord_N` linker error | Driver not linked | Enable driver Kconfig, check CMakeLists.txt |
| `DT_N_...` undefined | Missing DT node | Add node to devicetree/overlay |
| Init returns `-ENODEV` | Bus not ready | Check parent bus device, init order |
| Wrong init order | Dependency not ready | Use correct init level/priority |

### Debugging Checklist

1. **Check devicetree**: `build/zephyr/zephyr.dts`
2. **Check generated macros**: `build/zephyr/include/generated/devicetree_generated.h`
3. **Check Kconfig**: `build/zephyr/.config`
4. **Check init order**: Add printk in init function
5. **Check bus parent**: Ensure parent device initializes first

---

## Resource Locations

For finding drivers, examples, and bindings in Zephyr: See [locations.md](references/locations.md)

## Complete Examples

For full working examples (GPIO LED, I2C sensor, SPI device, sensor driver): See [examples.md](references/examples.md)

## Related Skills

- **zephyr-devicetree**: DT syntax, bindings, overlays
- **zephyr-kconfig**: Driver configuration options
- **zephyr-kernel-synchronization**: Locks in interrupt-driven drivers
- **zephyr-power-management**: System PM, runtime PM usage patterns, and low-power design constraints
