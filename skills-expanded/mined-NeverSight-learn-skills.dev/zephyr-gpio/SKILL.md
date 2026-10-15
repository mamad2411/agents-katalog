---
name: zephyr-gpio
description: GPIO driver implementation guidance for Zephyr RTOS. Use when working with digital I/O pins, LEDs, buttons, or any GPIO-controlled peripherals. Covers pin configuration, reading/writing, interrupts, and devicetree bindings.
---

# Zephyr GPIO Skill

## Overview

This skill provides guidance for implementing GPIO functionality in Zephyr RTOS applications. GPIO (General Purpose Input/Output) is fundamental to embedded systems for controlling LEDs, reading buttons, and interfacing with digital peripherals.

## API Selection Decision Tree

```
Need GPIO?
├── Single pin from devicetree?
│   └── Use gpio_dt_spec + _dt() functions (RECOMMENDED)
│       └── GPIO_DT_SPEC_GET(node, prop) → gpio_pin_configure_dt() → gpio_pin_set_dt()/gpio_pin_get_dt()
│
├── Multiple pins, same port?
│   └── Use gpio_port_*() functions for efficiency
│       └── gpio_port_set_masked() / gpio_port_get()
│
└── Runtime-determined pin?
    └── Use raw API with device + pin number
        └── DEVICE_DT_GET() → gpio_pin_configure() → gpio_pin_set()/gpio_pin_get()
```

## Getting Device Reference

### From Devicetree (Preferred)

```c
/* For nodes with gpios property (e.g., gpio-leds, gpio-keys) */
#define LED_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED_NODE, gpios);

/* Check device readiness before use */
if (!gpio_is_ready_dt(&led)) {
    return -ENODEV;
}
```

### gpio_dt_spec Structure

```c
struct gpio_dt_spec {
    const struct device *port;  /* GPIO controller device */
    gpio_pin_t pin;             /* Pin number (0-31 typically) */
    gpio_dt_flags_t dt_flags;   /* Flags from devicetree (e.g., GPIO_ACTIVE_LOW) */
};
```

## Common Workflows

### 1. Basic LED Blinky

```c
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

#define LED_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED_NODE, gpios);

int main(void)
{
    if (!gpio_is_ready_dt(&led)) {
        return -ENODEV;
    }

    int ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
    if (ret < 0) {
        return ret;
    }

    while (1) {
        gpio_pin_toggle_dt(&led);
        k_msleep(1000);
    }
    return 0;
}
```

### 2. Button Input (Polled)

```c
#define BUTTON_NODE DT_ALIAS(sw0)
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(BUTTON_NODE, gpios);

int main(void)
{
    if (!gpio_is_ready_dt(&button)) {
        return -ENODEV;
    }

    gpio_pin_configure_dt(&button, GPIO_INPUT);

    while (1) {
        int val = gpio_pin_get_dt(&button);
        if (val > 0) {
            /* Button pressed (handles ACTIVE_LOW automatically) */
        }
        k_msleep(100);
    }
}
```

### 3. Button with Interrupt

```c
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);
static struct gpio_callback button_cb_data;

void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    /* ISR context - keep short, use k_work for heavy processing */
    printk("Button pressed at %" PRIu32 "\n", k_cycle_get_32());
}

int main(void)
{
    if (!gpio_is_ready_dt(&button)) {
        return -ENODEV;
    }

    gpio_pin_configure_dt(&button, GPIO_INPUT);
    gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);

    gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
    gpio_add_callback(button.port, &button_cb_data);

    /* Main loop or other work */
    while (1) {
        k_msleep(1000);
    }
}
```

### 4. Multiple Pins Configuration

```c
/* Define multiple GPIO specs */
static const struct gpio_dt_spec leds[] = {
    GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios),
    GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios),
    GPIO_DT_SPEC_GET(DT_ALIAS(led2), gpios),
};

int init_leds(void)
{
    for (int i = 0; i < ARRAY_SIZE(leds); i++) {
        if (!gpio_is_ready_dt(&leds[i])) {
            return -ENODEV;
        }
        int ret = gpio_pin_configure_dt(&leds[i], GPIO_OUTPUT_INACTIVE);
        if (ret < 0) {
            return ret;
        }
    }
    return 0;
}
```

### 5. Bidirectional Pin (Input/Output switching)

```c
static const struct gpio_dt_spec data_pin = GPIO_DT_SPEC_GET(DT_NODELABEL(data_gpio), gpios);

void send_data(uint8_t bit)
{
    gpio_pin_configure_dt(&data_pin, GPIO_OUTPUT);
    gpio_pin_set_dt(&data_pin, bit);
}

int read_data(void)
{
    gpio_pin_configure_dt(&data_pin, GPIO_INPUT);
    return gpio_pin_get_dt(&data_pin);
}
```

## Configuration

### Essential Kconfig

```kconfig
CONFIG_GPIO=y                    # Enable GPIO driver subsystem (required)
# CONFIG_GPIO_LOG_LEVEL_DBG=y    # Enable for debugging
```

### Devicetree Examples

**LED definition:**
```dts
/ {
    aliases {
        led0 = &green_led;
    };

    leds {
        compatible = "gpio-leds";
        green_led: led_0 {
            gpios = <&gpio0 13 GPIO_ACTIVE_LOW>;
            label = "Green LED";
        };
    };
};
```

**Button definition:**
```dts
/ {
    aliases {
        sw0 = &user_button;
    };

    buttons {
        compatible = "gpio-keys";
        user_button: button_0 {
            gpios = <&gpio0 11 (GPIO_PULL_UP | GPIO_ACTIVE_LOW)>;
            label = "User Button";
        };
    };
};
```

**Generic GPIO:**
```dts
/ {
    my_gpios {
        compatible = "gpio-leds";  /* Reuse for any GPIO */
        data_gpio: data {
            gpios = <&gpio0 5 GPIO_ACTIVE_HIGH>;
        };
    };
};
```

## GPIO Flags Reference

| Flag | Value | Description |
|------|-------|-------------|
| `GPIO_INPUT` | 0x1 | Pin configured as input |
| `GPIO_OUTPUT` | 0x2 | Pin configured as output |
| `GPIO_OUTPUT_INACTIVE` | 0x2 | Output initially inactive |
| `GPIO_OUTPUT_ACTIVE` | 0x3 | Output initially active |
| `GPIO_ACTIVE_LOW` | 0x10 | Logical active = physical low |
| `GPIO_PULL_UP` | 0x100 | Enable internal pull-up |
| `GPIO_PULL_DOWN` | 0x200 | Enable internal pull-down |

### Interrupt Flags

| Flag | Description |
|------|-------------|
| `GPIO_INT_EDGE_RISING` | Trigger on rising edge |
| `GPIO_INT_EDGE_FALLING` | Trigger on falling edge |
| `GPIO_INT_EDGE_BOTH` | Trigger on both edges |
| `GPIO_INT_EDGE_TO_ACTIVE` | Edge toward active (respects ACTIVE_LOW) |
| `GPIO_INT_EDGE_TO_INACTIVE` | Edge toward inactive |
| `GPIO_INT_LEVEL_ACTIVE` | Level active interrupt |

## Interrupt Handling Pattern

### With Work Queue (Recommended for complex handling)

```c
static struct k_work button_work;
static const struct gpio_dt_spec button = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);

void button_work_handler(struct k_work *work)
{
    /* Safe to do complex operations here */
    printk("Button handled in work queue\n");
}

void button_isr(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    k_work_submit(&button_work);
}

int main(void)
{
    k_work_init(&button_work, button_work_handler);

    gpio_pin_configure_dt(&button, GPIO_INPUT);
    gpio_pin_interrupt_configure_dt(&button, GPIO_INT_EDGE_TO_ACTIVE);

    static struct gpio_callback cb;
    gpio_init_callback(&cb, button_isr, BIT(button.pin));
    gpio_add_callback(button.port, &cb);

    return 0;
}
```

### Debouncing with Delayed Work

```c
static struct k_work_delayable debounce_work;
#define DEBOUNCE_MS 50

void debounce_handler(struct k_work *work)
{
    int val = gpio_pin_get_dt(&button);
    if (val > 0) {
        /* Confirmed button press */
    }
}

void button_isr(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
    k_work_reschedule(&debounce_work, K_MSEC(DEBOUNCE_MS));
}
```

## Error Handling

All GPIO functions return negative errno on failure:

```c
int ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
if (ret < 0) {
    LOG_ERR("Failed to configure GPIO: %d", ret);
    return ret;
}
```

Common errors:
- `-ENODEV`: Device not ready or not found
- `-ENOTSUP`: Configuration not supported by hardware
- `-EINVAL`: Invalid pin number or flags

## Troubleshooting

| Issue | Check |
|-------|-------|
| `gpio_is_ready_dt()` returns false | Verify devicetree node exists, GPIO controller enabled in Kconfig |
| Pin doesn't toggle | Check ACTIVE_LOW flag matches hardware, verify pin not used elsewhere |
| Interrupt not firing | Confirm `gpio_pin_interrupt_configure_dt()` called, check callback registered |
| Wrong logic level | Active-low LEDs need `GPIO_ACTIVE_LOW` in devicetree |
| Multiple callbacks not working | Each callback struct must be unique, use BIT(pin) correctly |

## References

- [references/api.md](references/api.md) - Complete GPIO API function reference
- [references/devicetree.md](references/devicetree.md) - Devicetree bindings and properties
- [references/kconfig.md](references/kconfig.md) - All GPIO Kconfig options
