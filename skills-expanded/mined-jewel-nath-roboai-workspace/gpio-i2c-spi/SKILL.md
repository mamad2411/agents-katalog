---
name: gpio-i2c-spi
description: GPIO, PWM, interrupts, I2C device communication, SPI protocol, and hardware abstraction for robotics sensors and actuators on Linux embedded platforms.
category: hardware
tags: [gpio, i2c, spi, pwm, interrupts, linux, embedded, rpi, sensors]
version: "1.0.0"
---

# GPIO / I2C / SPI

Hardware communication is the foundation of robot sensing and actuation. This skill covers GPIO control, PWM generation, interrupt-driven event handling, I2C sensor communication, and SPI protocol — all on Linux embedded platforms (primarily Raspberry Pi 5) with ROS2 integration patterns.

## When to Use

- Reading digital sensors (buttons, limit switches, encoders)
- Controlling LEDs, relays, or digital outputs
- Generating PWM for servo motors, ESCs, or brushed motor drivers
- Detecting hardware events via interrupts (encoder pulses, LIDAR triggers)
- Communicating with I2C sensors: IMUs, barometers, ToF distance sensors, OLED displays
- Communicating with SPI devices: ADCs, DACs, IMUs with SPI interface, display controllers
- Writing a ROS2 node that publishes sensor data read directly from GPIO/I2C/SPI
- Abstracting hardware access with a HAL for testability
- Working with Raspberry Pi 5 (RP1 chip, new gpiod-based GPIO)
- Debouncing switches and buttons in software

## Quick Start

```bash
# Install system tools
sudo apt update
sudo apt install -y gpiod libgpiod-dev i2c-tools python3-smbus2 python3-spidev

# Enable I2C and SPI on Raspberry Pi
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Detect I2C devices (bus 1 is the standard header bus on RPi)
i2cdetect -y 1

# List GPIO chips (RPi 5 has gpiochip4 from RP1)
gpiodetect
# gpiochip0 [pinctrl-rp1] (54 lines)   ← RPi 5 (RP1 chip)

# Query a single line
gpioinfo gpiochip0 | grep "line 17"

# Install Python libraries
pip install gpiod smbus2 spidev lgpio

# Minimal GPIO output example (blink LED on GPIO 17)
python3 - <<'EOF'
import gpiod
import time

chip = gpiod.Chip('gpiochip0')
line = chip.get_line(17)
line.request(consumer='led-test', type=gpiod.LINE_REQ_DIR_OUT)

for _ in range(5):
    line.set_value(1)
    time.sleep(0.5)
    line.set_value(0)
    time.sleep(0.5)

line.release()
chip.close()
EOF
```

## Core Concepts

### 1. Linux GPIO Interfaces (sysfs vs gpiod vs lgpio)

Three interfaces exist; choose based on platform and Python version.

| Interface | Library | RPi 5 | Thread-safe | Interrupts | Recommended |
|-----------|---------|-------|-------------|------------|-------------|
| sysfs (`/sys/class/gpio`) | file I/O | Deprecated | No | Poll only | No — legacy |
| libgpiod v1 | `gpiod` Python | Yes | Yes | Yes | Yes for RPi 5 |
| lgpio | `lgpio` Python | Yes | Yes | Yes | Yes for RPi 5 |
| RPi.GPIO | `RPi.GPIO` | Broken on RPi 5 | No | Yes (callback) | No — RPi 4 only |
| pigpio | `pigpio` | Partial | Yes | Yes | Not for RPi 5 |

**Raspberry Pi 5 note**: RPi 5 uses the RP1 I/O chip. The old `/dev/gpiomem` interface does not work. Use `gpiod` (libgpiod) or `lgpio`.

```python
# gpiod (libgpiod) — correct approach for RPi 5
import gpiod
from gpiod.line import Direction, Value, Edge, Bias

# Open chip — RPi 5 exposes gpiochip0 from RP1
with gpiod.Chip('/dev/gpiochip0') as chip:
    info = chip.get_info()
    print(f"Chip: {info.name}, label: {info.label}, lines: {info.num_lines}")
```

```python
# lgpio — alternative for RPi 5
import lgpio
import time

h = lgpio.gpiochip_open(0)          # Open chip 0
lgpio.gpio_claim_output(h, 17)       # Claim GPIO 17 as output
lgpio.gpio_write(h, 17, 1)           # Set HIGH
time.sleep(1)
lgpio.gpio_write(h, 17, 0)           # Set LOW
lgpio.gpiochip_close(h)
```

### 2. GPIO Input, Output, and Pull Resistors

```python
import gpiod
import time

# Constants for pin assignments
BUTTON_PIN = 18
LED_PIN = 17
ENCODER_A_PIN = 22
ENCODER_B_PIN = 23

def setup_gpio_io():
    """Configure GPIO lines for mixed input/output use."""
    chip = gpiod.Chip('/dev/gpiochip0')

    # Output: LED (push-pull, no bias needed)
    led = chip.get_line(LED_PIN)
    led.request(
        consumer='led-control',
        type=gpiod.LINE_REQ_DIR_OUT,
        default_vals=[0]
    )

    # Input with pull-up (button to GND)
    button = chip.get_line(BUTTON_PIN)
    button.request(
        consumer='button-read',
        type=gpiod.LINE_REQ_DIR_IN,
        flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
    )

    # Input with pull-up for encoder
    enc_a = chip.get_line(ENCODER_A_PIN)
    enc_a.request(
        consumer='encoder-a',
        type=gpiod.LINE_REQ_DIR_IN,
        flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
    )

    return chip, led, button, enc_a

chip, led, button, enc_a = setup_gpio_io()

# Read button (active-low with pull-up: 0 = pressed)
pressed = (button.get_value() == 0)
print(f"Button pressed: {pressed}")

# Drive LED
led.set_value(1 if pressed else 0)

chip.close()
```

### 3. PWM — Hardware vs Software

Hardware PWM is essential for servo control and motor speed; software PWM is acceptable for slow LEDs only.

```python
# Hardware PWM via sysfs (always prefer this for servos/motors)
# RPi 5: GPIO 12, 13, 18, 19 support hardware PWM

import os
import time

PWM_CHIP = 0          # /sys/class/pwm/pwmchip0
PWM_CHANNEL = 0       # Channel 0 (GPIO 12 on RPi 5)

def pwm_export(chip, channel):
    path = f'/sys/class/pwm/pwmchip{chip}/pwm{channel}'
    if not os.path.exists(path):
        with open(f'/sys/class/pwm/pwmchip{chip}/export', 'w') as f:
            f.write(str(channel))
    time.sleep(0.1)    # Wait for kernel to create files
    return path

def pwm_set(path, period_ns, duty_ns, enable=True):
    """Set PWM period and duty cycle in nanoseconds."""
    # Must disable before changing period
    with open(f'{path}/enable', 'w') as f:
        f.write('0')
    with open(f'{path}/period', 'w') as f:
        f.write(str(period_ns))
    with open(f'{path}/duty_cycle', 'w') as f:
        f.write(str(duty_ns))
    with open(f'{path}/enable', 'w') as f:
        f.write('1' if enable else '0')

# Servo: 50 Hz period, 1000–2000 µs pulse width
SERVO_PERIOD_NS = 20_000_000     # 20 ms = 50 Hz
SERVO_MIN_NS    = 1_000_000      # 1 ms = 0 degrees
SERVO_MID_NS    = 1_500_000      # 1.5 ms = 90 degrees
SERVO_MAX_NS    = 2_000_000      # 2 ms = 180 degrees

path = pwm_export(PWM_CHIP, PWM_CHANNEL)
pwm_set(path, SERVO_PERIOD_NS, SERVO_MID_NS)
print("Servo at center position")
time.sleep(1)

def angle_to_duty(angle_deg):
    """Convert 0-180 degrees to nanosecond pulse width."""
    fraction = angle_deg / 180.0
    return int(SERVO_MIN_NS + fraction * (SERVO_MAX_NS - SERVO_MIN_NS))

pwm_set(path, SERVO_PERIOD_NS, angle_to_duty(45))
print("Servo at 45 degrees")
```

```c
/* Hardware PWM via Linux PWM sysfs from C */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define PWM_PATH "/sys/class/pwm/pwmchip0/pwm0"

static void pwm_write(const char *attr, long value) {
    char path[128];
    char buf[32];
    snprintf(path, sizeof(path), "%s/%s", PWM_PATH, attr);
    int fd = open(path, O_WRONLY);
    if (fd < 0) { perror("pwm_write open"); return; }
    snprintf(buf, sizeof(buf), "%ld", value);
    write(fd, buf, strlen(buf));
    close(fd);
}

void servo_set_angle(float angle_deg) {
    long period_ns = 20000000L;          /* 20 ms */
    long duty_ns = (long)(1000000L + (angle_deg / 180.0f) * 1000000L);
    pwm_write("enable", 0);
    pwm_write("period", period_ns);
    pwm_write("duty_cycle", duty_ns);
    pwm_write("enable", 1);
}
```

### 4. Interrupts and Edge Detection

```python
import gpiod
import threading
import time
from collections import deque

ENCODER_A = 22
ENCODER_B = 23
DEBOUNCE_US = 1000    # 1 ms debounce for buttons

class EncoderReader:
    """Quadrature encoder using gpiod edge events."""

    def __init__(self, chip_path='/dev/gpiochip0', pin_a=ENCODER_A, pin_b=ENCODER_B):
        self._count = 0
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

        self._chip = gpiod.Chip(chip_path)
        self._line_a = self._chip.get_line(pin_a)
        self._line_b = self._chip.get_line(pin_b)

        # Request both edges on A, input-only on B
        self._line_a.request(
            consumer='encoder-a',
            type=gpiod.LINE_REQ_EV_BOTH_EDGES,
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
        )
        self._line_b.request(
            consumer='encoder-b',
            type=gpiod.LINE_REQ_DIR_IN,
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
        )

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        self._line_a.release()
        self._line_b.release()
        self._chip.close()

    def get_count(self):
        with self._lock:
            return self._count

    def _poll_loop(self):
        while self._running:
            # Wait up to 100 ms for an event
            if self._line_a.event_wait(sec=0, nsec=100_000_000):
                event = self._line_a.event_read()
                b_val = self._line_b.get_value()

                # Quadrature decode: rising edge on A
                if event.type == gpiod.LineEvent.RISING_EDGE:
                    direction = 1 if b_val == 0 else -1
                else:
                    direction = -1 if b_val == 0 else 1

                with self._lock:
                    self._count += direction


class DebouncedButton:
    """Button with software debounce using gpiod."""

    def __init__(self, chip_path, pin, debounce_ms=20):
        self._debounce_s = debounce_ms / 1000.0
        self._last_event_time = 0.0
        self._callback = None
        self._running = False

        self._chip = gpiod.Chip(chip_path)
        self._line = self._chip.get_line(pin)
        self._line.request(
            consumer='button',
            type=gpiod.LINE_REQ_EV_FALLING_EDGE,     # Active-low button
            flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
        )

    def on_press(self, callback):
        """Register a callback for button press events."""
        self._callback = callback

    def start(self):
        self._running = True
        t = threading.Thread(target=self._event_loop, daemon=True)
        t.start()

    def _event_loop(self):
        while self._running:
            if self._line.event_wait(sec=0, nsec=50_000_000):
                event = self._line.event_read()
                now = time.monotonic()
                # Ignore events within debounce window
                if (now - self._last_event_time) > self._debounce_s:
                    self._last_event_time = now
                    if self._callback:
                        self._callback()
```

### 5. I2C — Device Communication

```python
import smbus2
import time
import struct

# I2C bus numbers: 1 = standard 40-pin header (GPIO 2/3), RPi 5 also has bus 4, 5, 6
I2C_BUS = 1

# Common I2C device addresses
ICM20948_ADDR  = 0x68    # IMU (AD0 low) or 0x69 (AD0 high)
BMP388_ADDR    = 0x77    # Barometric pressure
VL53L1X_ADDR   = 0x29    # ToF distance sensor
SSD1306_ADDR   = 0x3C    # OLED display

# ICM-20948 register map
ICM_WHO_AM_I    = 0x00
ICM_PWR_MGMT_1  = 0x06
ICM_ACCEL_XOUT_H = 0x2D
ICM_GYRO_XOUT_H  = 0x33
ICM_EXPECTED_ID  = 0xEA

def i2c_read_byte(bus, addr, reg):
    return bus.read_byte_data(addr, reg)

def i2c_write_byte(bus, addr, reg, value):
    bus.write_byte_data(addr, reg, value)

def i2c_read_block(bus, addr, reg, length):
    return bus.read_i2c_block_data(addr, reg, length)

class ICM20948:
    """ICM-20948 9-DoF IMU over I2C."""

    ACCEL_SCALE = 9.81 / 16384.0    # ±2g full-scale → m/s²
    GYRO_SCALE  = (1.0 / 131.0) * (3.14159265 / 180.0)   # ±250°/s → rad/s

    def __init__(self, bus_num=I2C_BUS, addr=ICM20948_ADDR):
        self._addr = addr
        self._bus = smbus2.SMBus(bus_num)
        self._verify_device()
        self._init_device()

    def _verify_device(self):
        who_am_i = i2c_read_byte(self._bus, self._addr, ICM_WHO_AM_I)
        if who_am_i != ICM_EXPECTED_ID:
            raise RuntimeError(
                f"ICM-20948 WHO_AM_I returned 0x{who_am_i:02X}, expected 0x{ICM_EXPECTED_ID:02X}. "
                "Check wiring and I2C address."
            )

    def _init_device(self):
        # Wake up from sleep (bit 6 = sleep)
        i2c_write_byte(self._bus, self._addr, ICM_PWR_MGMT_1, 0x01)
        time.sleep(0.1)

    def read_accel(self):
        """Return (ax, ay, az) in m/s²."""
        raw = i2c_read_block(self._bus, self._addr, ICM_ACCEL_XOUT_H, 6)
        ax, ay, az = struct.unpack('>hhh', bytes(raw))
        return ax * self.ACCEL_SCALE, ay * self.ACCEL_SCALE, az * self.ACCEL_SCALE

    def read_gyro(self):
        """Return (gx, gy, gz) in rad/s."""
        raw = i2c_read_block(self._bus, self._addr, ICM_GYRO_XOUT_H, 6)
        gx, gy, gz = struct.unpack('>hhh', bytes(raw))
        return gx * self.GYRO_SCALE, gy * self.GYRO_SCALE, gz * self.GYRO_SCALE

    def close(self):
        self._bus.close()


# I2C with smbus2 context manager and repeated start (write-then-read)
def i2c_read_with_repeated_start(bus_num, device_addr, reg_addr, length):
    """Perform a write+read without a STOP condition between them."""
    with smbus2.SMBus(bus_num) as bus:
        # Build a write message for the register address
        write_msg = smbus2.i2c_msg.write(device_addr, [reg_addr])
        # Build a read message for the data
        read_msg = smbus2.i2c_msg.read(device_addr, length)
        # Execute both in a single transfer (repeated START)
        bus.i2c_rdwr(write_msg, read_msg)
        return list(read_msg)
```

```c
/* I2C from C using Linux i2c-dev */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>

#define I2C_BUS_PATH   "/dev/i2c-1"
#define ICM20948_ADDR  0x68
#define ICM_WHO_AM_I   0x00
#define ICM_EXPECTED   0xEA

typedef struct {
    int fd;
    uint8_t addr;
} i2c_device_t;

int i2c_open(i2c_device_t *dev, const char *bus_path, uint8_t addr) {
    dev->addr = addr;
    dev->fd = open(bus_path, O_RDWR);
    if (dev->fd < 0) return -1;
    if (ioctl(dev->fd, I2C_SLAVE, addr) < 0) {
        close(dev->fd);
        return -1;
    }
    return 0;
}

int i2c_write_reg(i2c_device_t *dev, uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    return write(dev->fd, buf, 2) == 2 ? 0 : -1;
}

int i2c_read_reg(i2c_device_t *dev, uint8_t reg, uint8_t *data, size_t len) {
    /* Repeated START via I2C_RDWR ioctl */
    struct i2c_msg msgs[2];
    struct i2c_rdwr_ioctl_data transfer;

    msgs[0].addr  = dev->addr;
    msgs[0].flags = 0;          /* write */
    msgs[0].len   = 1;
    msgs[0].buf   = &reg;

    msgs[1].addr  = dev->addr;
    msgs[1].flags = I2C_M_RD;  /* read */
    msgs[1].len   = len;
    msgs[1].buf   = data;

    transfer.msgs  = msgs;
    transfer.nmsgs = 2;

    return ioctl(dev->fd, I2C_RDWR, &transfer) < 0 ? -1 : 0;
}

int main(void) {
    i2c_device_t imu;
    if (i2c_open(&imu, I2C_BUS_PATH, ICM20948_ADDR) < 0) {
        perror("Failed to open I2C device");
        return 1;
    }

    uint8_t id;
    i2c_read_reg(&imu, ICM_WHO_AM_I, &id, 1);
    printf("WHO_AM_I: 0x%02X (expected 0x%02X)\n", id, ICM_EXPECTED);

    close(imu.fd);
    return 0;
}
```

### 6. SPI — Protocol and Device Communication

```python
import spidev
import time

# SPI bus and device (CS)
SPI_BUS    = 0     # /dev/spidev0.x
SPI_DEVICE = 0     # CS0

# SPI modes
# Mode 0: CPOL=0, CPHA=0 — idle LOW, sample on rising  (most common)
# Mode 1: CPOL=0, CPHA=1 — idle LOW, sample on falling
# Mode 2: CPOL=1, CPHA=0 — idle HIGH, sample on falling
# Mode 3: CPOL=1, CPHA=1 — idle HIGH, sample on rising

# MCP3208 — 8-channel 12-bit SPI ADC (Mode 0)
MCP3208_VREF = 3.3

class MCP3208:
    """12-bit 8-channel SPI ADC."""

    def __init__(self, bus=SPI_BUS, device=SPI_DEVICE, speed_hz=1_000_000):
        self._spi = spidev.SpiDev()
        self._spi.open(bus, device)
        self._spi.max_speed_hz = speed_hz
        self._spi.mode = 0b00             # Mode 0
        self._spi.bits_per_word = 8
        self._spi.lsbfirst = False        # MSB first

    def read_channel(self, channel):
        """Read a single-ended channel (0-7). Returns raw 12-bit value."""
        if not 0 <= channel <= 7:
            raise ValueError(f"Channel must be 0-7, got {channel}")

        # MCP3208 protocol:
        # Byte 1: start bit (bit 2) + single/diff (bit 1) + D2 (MSB of channel)
        # Byte 2: D1:D0 of channel (bits 7:6)
        # Byte 3: don't care (clocks out the 12-bit result)
        cmd_byte1 = 0x06 | (channel >> 2)       # 0b00000110 | channel[2]
        cmd_byte2 = (channel & 0x03) << 6        # channel[1:0] in top bits

        response = self._spi.xfer2([cmd_byte1, cmd_byte2, 0x00])

        # Result: response[1] bits [3:0] = high nibble, response[2] = low byte
        raw = ((response[1] & 0x0F) << 8) | response[2]
        return raw

    def read_voltage(self, channel):
        """Read voltage on a channel (0–VREF)."""
        raw = self._read_channel(channel)
        return (raw / 4095.0) * MCP3208_VREF

    def close(self):
        self._spi.close()


# ICM-20948 via SPI (Mode 0, CS active-low, max 7 MHz)
ICM_WHO_AM_I_REG = 0x00
ICM_READ_FLAG    = 0x80      # Set bit 7 for read operations

class ICM20948SPI:
    """ICM-20948 IMU over SPI."""

    def __init__(self, bus=0, device=0, speed_hz=7_000_000):
        self._spi = spidev.SpiDev()
        self._spi.open(bus, device)
        self._spi.max_speed_hz = speed_hz
        self._spi.mode = 0b00

    def _read_register(self, reg, length=1):
        """Read one or more registers. Reg address with read flag."""
        cmd = [reg | ICM_READ_FLAG] + [0x00] * length
        resp = self._spi.xfer2(cmd)
        return resp[1:]  # First byte is garbage (address phase)

    def _write_register(self, reg, value):
        """Write a single register."""
        self._spi.xfer2([reg & ~ICM_READ_FLAG, value])

    def who_am_i(self):
        return self._read_register(ICM_WHO_AM_I_REG)[0]

    def close(self):
        self._spi.close()
```

```c
/* SPI from C using Linux spidev */
#include <stdint.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <string.h>

#define SPI_DEVICE     "/dev/spidev0.0"
#define SPI_SPEED_HZ   7000000
#define SPI_MODE       SPI_MODE_0
#define SPI_BITS       8

typedef struct {
    int fd;
} spi_device_t;

int spi_open(spi_device_t *dev) {
    dev->fd = open(SPI_DEVICE, O_RDWR);
    if (dev->fd < 0) return -1;

    uint8_t mode  = SPI_MODE;
    uint8_t bits  = SPI_BITS;
    uint32_t speed = SPI_SPEED_HZ;

    ioctl(dev->fd, SPI_IOC_WR_MODE, &mode);
    ioctl(dev->fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    ioctl(dev->fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

    return 0;
}

int spi_transfer(spi_device_t *dev, const uint8_t *tx, uint8_t *rx, size_t len) {
    struct spi_ioc_transfer tr = {
        .tx_buf        = (unsigned long)tx,
        .rx_buf        = (unsigned long)rx,
        .len           = len,
        .speed_hz      = SPI_SPEED_HZ,
        .bits_per_word = SPI_BITS,
        .delay_usecs   = 0,
        .cs_change     = 0,
    };
    return ioctl(dev->fd, SPI_IOC_MESSAGE(1), &tr);
}

uint8_t spi_read_reg(spi_device_t *dev, uint8_t reg) {
    uint8_t tx[2] = { reg | 0x80, 0x00 };    /* read flag */
    uint8_t rx[2] = { 0 };
    spi_transfer(dev, tx, rx, 2);
    return rx[1];
}

void spi_write_reg(spi_device_t *dev, uint8_t reg, uint8_t value) {
    uint8_t tx[2] = { reg & 0x7F, value };    /* write: clear read flag */
    uint8_t rx[2];
    spi_transfer(dev, tx, rx, 2);
}
```

### 7. ROS2 Integration — Publishing Sensor Data from Hardware

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
import smbus2
import gpiod
import struct
import time

IMU_BUS      = 1
IMU_ADDRESS  = 0x68
IMU_WHO_AM_I = 0x00

# Sensor QoS: high-frequency, best-effort
SENSOR_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    depth=5
)


class ImuPublisherNode(Node):
    """ROS2 node that reads ICM-20948 over I2C and publishes sensor_msgs/Imu."""

    ACCEL_SCALE = 9.81 / 16384.0
    GYRO_SCALE  = (1.0 / 131.0) * (3.14159265 / 180.0)

    def __init__(self):
        super().__init__('imu_publisher')

        self.declare_parameter('publish_rate_hz', 50.0)
        self.declare_parameter('frame_id', 'imu_link')
        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('i2c_address', 0x68)

        rate  = self.get_parameter('publish_rate_hz').value
        self._frame_id = self.get_parameter('frame_id').value
        bus   = self.get_parameter('i2c_bus').value
        addr  = self.get_parameter('i2c_address').value

        self._bus = smbus2.SMBus(bus)
        self._addr = addr
        self._init_imu()

        self._imu_pub = self.create_publisher(Imu, '/imu/data_raw', SENSOR_QOS)
        self._timer = self.create_timer(1.0 / rate, self._publish_imu)

        self.get_logger().info(
            f'ImuPublisherNode started — rate: {rate} Hz, I2C bus: {bus}, addr: 0x{addr:02X}'
        )

    def _init_imu(self):
        who = self._bus.read_byte_data(self._addr, ICM_WHO_AM_I)
        if who != 0xEA:
            raise RuntimeError(f"IMU WHO_AM_I = 0x{who:02X}, expected 0xEA")
        # Wake device
        self._bus.write_byte_data(self._addr, 0x06, 0x01)
        time.sleep(0.05)

    def _read_raw(self, reg, count=6):
        write_msg = smbus2.i2c_msg.write(self._addr, [reg])
        read_msg  = smbus2.i2c_msg.read(self._addr, count)
        self._bus.i2c_rdwr(write_msg, read_msg)
        return struct.unpack('>hhh', bytes(list(read_msg)))

    def _publish_imu(self):
        try:
            ax, ay, az = self._read_raw(0x2D)    # ACCEL_XOUT_H
            gx, gy, gz = self._read_raw(0x33)    # GYRO_XOUT_H

            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self._frame_id

            msg.linear_acceleration.x = ax * self.ACCEL_SCALE
            msg.linear_acceleration.y = ay * self.ACCEL_SCALE
            msg.linear_acceleration.z = az * self.ACCEL_SCALE

            msg.angular_velocity.x = gx * self.GYRO_SCALE
            msg.angular_velocity.y = gy * self.GYRO_SCALE
            msg.angular_velocity.z = gz * self.GYRO_SCALE

            # Unknown orientation — fill covariance diagonal with -1
            msg.orientation_covariance[0] = -1.0

            self._imu_pub.publish(msg)

        except Exception as e:
            self.get_logger().error(f'IMU read error: {e}', throttle_duration_sec=5.0)

    def destroy_node(self):
        self._bus.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = ImuPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Common Patterns

### Pattern 1: GPIO-based Limit Switch Safety Stop (ROS2)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import gpiod
import threading

LIMIT_SWITCH_PINS = {
    'front': 17,
    'rear':  27,
    'left':  22,
    'right': 10,
}

class LimitSwitchNode(Node):
    """Publishes limit switch state, halts robot on trigger."""

    def __init__(self):
        super().__init__('limit_switch_monitor')
        self._chip = gpiod.Chip('/dev/gpiochip0')
        self._lines = {}
        self._state = {name: False for name in LIMIT_SWITCH_PINS}
        self._lock = threading.Lock()

        for name, pin in LIMIT_SWITCH_PINS.items():
            line = self._chip.get_line(pin)
            line.request(
                consumer=f'limit-{name}',
                type=gpiod.LINE_REQ_EV_BOTH_EDGES,
                flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
            )
            self._lines[name] = line

        self._pub = self.create_publisher(Bool, '/orbibot/limit_switch_triggered', 10)

        # Poll thread for all lines
        t = threading.Thread(target=self._event_loop, daemon=True)
        t.start()
        self.get_logger().info('LimitSwitchNode started — monitoring 4 switches')

    def _event_loop(self):
        while rclpy.ok():
            for name, line in self._lines.items():
                if line.event_wait(sec=0, nsec=10_000_000):
                    event = line.event_read()
                    triggered = (event.type == gpiod.LineEvent.FALLING_EDGE)
                    with self._lock:
                        self._state[name] = triggered
                    self.get_logger().warn(
                        f'Limit switch [{name}] {"TRIGGERED" if triggered else "released"}'
                    )
                    msg = Bool()
                    msg.data = any(self._state.values())
                    self._pub.publish(msg)

    def destroy_node(self):
        for line in self._lines.values():
            line.release()
        self._chip.close()
        super().destroy_node()
```

### Pattern 2: Multi-Device I2C Bus Scanner and HAL

```python
import smbus2

KNOWN_DEVICES = {
    0x29: 'VL53L1X (ToF distance)',
    0x3C: 'SSD1306 (OLED display)',
    0x68: 'ICM-20948 (IMU, AD0=LOW)',
    0x69: 'ICM-20948 (IMU, AD0=HIGH)',
    0x76: 'BMP388 (barometer, SDO=LOW)',
    0x77: 'BMP388 (barometer, SDO=HIGH)',
}

def scan_i2c_bus(bus_num=1):
    """Scan I2C bus and identify connected devices."""
    found = {}
    with smbus2.SMBus(bus_num) as bus:
        for addr in range(0x08, 0x78):
            try:
                bus.read_byte(addr)
                label = KNOWN_DEVICES.get(addr, 'Unknown device')
                found[addr] = label
                print(f'  0x{addr:02X}: {label}')
            except OSError:
                pass
    if not found:
        print('  No I2C devices found. Check wiring and bus number.')
    return found


class I2CBus:
    """Thread-safe I2C bus abstraction."""

    def __init__(self, bus_num=1):
        import threading
        self._bus = smbus2.SMBus(bus_num)
        self._lock = threading.Lock()

    def read_byte_data(self, addr, reg):
        with self._lock:
            return self._bus.read_byte_data(addr, reg)

    def write_byte_data(self, addr, reg, value):
        with self._lock:
            self._bus.write_byte_data(addr, reg, value)

    def read_i2c_block_data(self, addr, reg, length):
        with self._lock:
            return self._bus.read_i2c_block_data(addr, reg, length)

    def i2c_rdwr(self, *msgs):
        with self._lock:
            self._bus.i2c_rdwr(*msgs)

    def close(self):
        self._bus.close()
```

### Pattern 3: SPI ADC with Rate-Limited ROS2 Publishing

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import spidev

class AnalogSensorNode(Node):
    """Reads 8-channel SPI ADC (MCP3208) and publishes voltages."""

    VREF      = 3.3
    MAX_COUNTS = 4095     # 12-bit ADC

    def __init__(self):
        super().__init__('analog_sensor_node')
        self.declare_parameter('sample_rate_hz', 100.0)
        self.declare_parameter('channels', [0, 1, 2])
        self.declare_parameter('spi_bus', 0)
        self.declare_parameter('spi_device', 0)
        self.declare_parameter('spi_speed_hz', 1_000_000)

        rate      = self.get_parameter('sample_rate_hz').value
        channels  = self.get_parameter('channels').value
        bus       = self.get_parameter('spi_bus').value
        device    = self.get_parameter('spi_device').value
        speed     = self.get_parameter('spi_speed_hz').value

        self._channels = channels
        self._spi = spidev.SpiDev()
        self._spi.open(bus, device)
        self._spi.max_speed_hz = speed
        self._spi.mode = 0b00

        self._pub = self.create_publisher(Float32MultiArray, '/analog/voltages', 10)
        self._timer = self.create_timer(1.0 / rate, self._sample_and_publish)
        self.get_logger().info(
            f'AnalogSensorNode — channels: {channels}, rate: {rate} Hz'
        )

    def _read_mcp3208(self, channel):
        cmd = [0x06 | (channel >> 2), (channel & 0x03) << 6, 0x00]
        response = self._spi.xfer2(cmd)
        raw = ((response[1] & 0x0F) << 8) | response[2]
        return raw

    def _sample_and_publish(self):
        voltages = []
        for ch in self._channels:
            raw = self._read_mcp3208(ch)
            voltage = (raw / self.MAX_COUNTS) * self.VREF
            voltages.append(voltage)

        msg = Float32MultiArray()
        msg.data = voltages
        self._pub.publish(msg)

    def destroy_node(self):
        self._spi.close()
        super().destroy_node()
```

### Pattern 4: I2C + GPIO Combined Sensor with ROS2

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import gpiod
import smbus2
import time

# VL53L1X ToF distance sensor
# XSHUT pin (active-low) controls power. ADDR select via XSHUT sequencing.
VL53_DEFAULT_ADDR = 0x29
VL53_WHO_AM_I_REG = 0x010F
VL53_EXPECTED_ID  = 0xEACC

class ToFSensorNode(Node):
    """VL53L1X time-of-flight sensor with XSHUT control via GPIO."""

    def __init__(self):
        super().__init__('tof_distance_sensor')
        self.declare_parameter('xshut_pin', 4)
        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('new_addr', 0x29)
        self.declare_parameter('publish_rate_hz', 30.0)

        xshut_pin = self.get_parameter('xshut_pin').value
        bus_num   = self.get_parameter('i2c_bus').value
        rate      = self.get_parameter('publish_rate_hz').value

        # Control XSHUT: LOW = sensor off, HIGH = sensor on
        self._chip = gpiod.Chip('/dev/gpiochip0')
        self._xshut = self._chip.get_line(xshut_pin)
        self._xshut.request(consumer='vl53-xshut', type=gpiod.LINE_REQ_DIR_OUT)

        # Power cycle to reset
        self._xshut.set_value(0)
        time.sleep(0.01)
        self._xshut.set_value(1)
        time.sleep(0.01)

        self._bus = smbus2.SMBus(bus_num)
        self._init_sensor()

        self._pub = self.create_publisher(Range, '/range/front', 10)
        self._timer = self.create_timer(1.0 / rate, self._publish_range)
        self.get_logger().info('ToFSensorNode started')

    def _init_sensor(self):
        # Read model ID (2-byte register, big-endian)
        raw = self._bus.read_i2c_block_data(VL53_DEFAULT_ADDR, 0x01, 2)
        model_id = (raw[0] << 8) | raw[1]
        self.get_logger().info(f'VL53L1X model ID: 0x{model_id:04X}')

    def _read_distance_mm(self):
        """Simplified distance read — implement full API for production."""
        raw = self._bus.read_i2c_block_data(VL53_DEFAULT_ADDR, 0x0096, 2)
        return ((raw[0] << 8) | raw[1])

    def _publish_range(self):
        try:
            dist_mm = self._read_distance_mm()
            msg = Range()
            msg.header.stamp    = self.get_clock().now().to_msg()
            msg.header.frame_id = 'tof_front_link'
            msg.radiation_type  = Range.INFRARED
            msg.field_of_view   = 0.436    # ~25 degrees
            msg.min_range       = 0.04     # 4 cm
            msg.max_range       = 4.0      # 4 m
            msg.range           = dist_mm / 1000.0
            self._pub.publish(msg)
        except OSError as e:
            self.get_logger().error(f'I2C read failed: {e}', throttle_duration_sec=2.0)

    def destroy_node(self):
        self._xshut.set_value(0)     # Power off sensor
        self._xshut.release()
        self._chip.close()
        self._bus.close()
        super().destroy_node()
```

## Anti-Patterns

### ❌ Using RPi.GPIO on Raspberry Pi 5
RPi.GPIO uses `/dev/gpiomem` which does not exist on RPi 5 (RP1 chip). It will fail silently or raise `RuntimeError: No access to /dev/mem`.

```python
# WRONG — broken on RPi 5
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)
```

```python
# CORRECT — use gpiod or lgpio on RPi 5
import gpiod
with gpiod.Chip('/dev/gpiochip0') as chip:
    line = chip.get_line(17)
    line.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
    line.set_value(1)
    line.release()
```

### ❌ Software PWM for Motor or Servo Control
Software PWM is subject to Linux scheduling jitter, causing servo jitter or inconsistent motor speeds. Jitter of ±1 ms on a 1–2 ms servo pulse = full range of motion error.

```python
# WRONG — software PWM via lgpio for servos
import lgpio, time
h = lgpio.gpiochip_open(0)
lgpio.tx_pwm(h, 18, 50, 7.5)    # 50 Hz, 7.5% duty (1.5 ms) — JITTER!
```

```python
# CORRECT — hardware PWM via sysfs
# GPIO 18 (pin 12) is PWM0 on RPi, works with /sys/class/pwm/pwmchip2/pwm0
def servo_to_center():
    path = '/sys/class/pwm/pwmchip2/pwm0'
    with open(f'{path}/period', 'w')     as f: f.write('20000000')
    with open(f'{path}/duty_cycle', 'w') as f: f.write('1500000')
    with open(f'{path}/enable', 'w')     as f: f.write('1')
```

### ❌ Not Releasing GPIO Lines
Unreleased lines leave consumer tags in the kernel and may prevent other processes from requesting the same line.

```python
# WRONG — line never released
chip = gpiod.Chip('/dev/gpiochip0')
line = chip.get_line(17)
line.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
line.set_value(1)
# Process exits without releasing — kernel holds the line

# CORRECT — use context managers or explicit release in finally
chip = gpiod.Chip('/dev/gpiochip0')
line = chip.get_line(17)
try:
    line.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
    line.set_value(1)
finally:
    line.release()
    chip.close()
```

### ❌ Polling GPIO in the ROS2 Timer Callback
Blocking GPIO event_wait inside a timer callback blocks the executor thread.

```python
# WRONG — blocks the ROS2 executor
class BadNode(Node):
    def __init__(self):
        super().__init__('bad')
        self._timer = self.create_timer(0.01, self._cb)

    def _cb(self):
        # This blocks for up to 100 ms — freezes other callbacks
        if self._line.event_wait(sec=0, nsec=100_000_000):
            event = self._line.event_read()
```

```python
# CORRECT — read hardware in a separate daemon thread; publish via thread-safe queue
import queue, threading

class GoodNode(Node):
    def __init__(self):
        super().__init__('good')
        self._event_queue = queue.Queue(maxsize=32)
        t = threading.Thread(target=self._hw_thread, daemon=True)
        t.start()
        self._timer = self.create_timer(0.01, self._process_events)

    def _hw_thread(self):
        while rclpy.ok():
            if self._line.event_wait(sec=0, nsec=10_000_000):
                event = self._line.event_read()
                try:
                    self._event_queue.put_nowait(event)
                except queue.Full:
                    pass

    def _process_events(self):
        while not self._event_queue.empty():
            event = self._event_queue.get_nowait()
            # Publish ROS2 message here
```

### ❌ Using I2C Clock Speeds Higher Than Device Supports
Many sensors default to 100 kHz and will fail at 400 kHz Fast mode without explicit support. Data corruption is silent.

```bash
# WRONG — setting 400 kHz for a sensor that supports only 100 kHz
# In /boot/firmware/config.txt:
# dtparam=i2c_arm_baudrate=400000

# CORRECT — check sensor datasheet max clock. Use 100 kHz for unknown devices.
# dtparam=i2c_arm_baudrate=100000   ← safe default
# Or verify per-device: ICM-20948 supports 400 kHz Fast mode and 3.4 MHz HS mode
```

### ❌ Ignoring I2C Clock Stretching
Some slow sensors hold SCL LOW to stall the master (clock stretching). Without a HAL that supports it, reads will be corrupt.

```python
# WRONG — reading too fast without giving sensor time to prepare
bus.write_byte_data(addr, TRIGGER_REG, 0x01)
data = bus.read_i2c_block_data(addr, DATA_REG, 2)  # Too soon!

# CORRECT — add delay after triggering measurement, or use repeated-start
bus.write_byte_data(addr, TRIGGER_REG, 0x01)
time.sleep(0.05)    # Give sensor 50 ms to complete measurement
data = bus.read_i2c_block_data(addr, DATA_REG, 2)
```

## Configuration Reference

### Raspberry Pi 5 GPIO Chip Mapping (RP1)

| GPIO Range | Chip | Device |
|------------|------|--------|
| GPIO 0–27 (header) | gpiochip0 | `/dev/gpiochip0` |
| GPIO 28–53 (compute) | gpiochip0 | `/dev/gpiochip0` |

> RPi 5 exposes one chip (`pinctrl-rp1`) with 54 lines via `/dev/gpiochip0`.

### I2C Bus Numbers (Raspberry Pi)

| Bus | GPIO Pins | Device | Notes |
|-----|-----------|--------|-------|
| 1 | GPIO 2 (SDA), GPIO 3 (SCL) | `/dev/i2c-1` | Standard 40-pin header |
| 3 | GPIO 4 (SDA), GPIO 5 (SCL) | `/dev/i2c-3` | RPi 5 extra |
| 4 | GPIO 8 (SDA), GPIO 9 (SCL) | `/dev/i2c-4` | RPi 5 extra |

### SPI Bus and CS Mapping (Raspberry Pi)

| Bus | CS | GPIO Pins | Device |
|-----|----|-----------|--------|
| SPI0 | CE0 | GPIO 10 (MOSI), 9 (MISO), 11 (SCLK), 8 (CE0) | `/dev/spidev0.0` |
| SPI0 | CE1 | GPIO 10, 9, 11, 7 (CE1) | `/dev/spidev0.1` |
| SPI1 | CE0 | GPIO 20 (MOSI), 19 (MISO), 21 (SCLK), 18 (CE0) | `/dev/spidev1.0` |

### Hardware PWM Channels (Raspberry Pi 5)

| PWM | GPIO | Chip/Channel | Note |
|-----|------|--------------|------|
| PWM0 | GPIO 12 | pwmchip2/pwm0 | Available after RPi 5 kernel 6.6 |
| PWM1 | GPIO 13 | pwmchip2/pwm1 | |
| PWM2 | GPIO 18 | pwmchip4/pwm2 | |
| PWM3 | GPIO 19 | pwmchip4/pwm3 | |

> RPi 5 changes: pwmchip numbering differs from RPi 4. Run `ls /sys/class/pwm/` to confirm.

### ImuPublisherNode Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `publish_rate_hz` | double | `50.0` | IMU publish frequency (Hz) |
| `frame_id` | string | `imu_link` | TF frame for IMU messages |
| `i2c_bus` | int | `1` | Linux I2C bus number |
| `i2c_address` | int | `0x68` | ICM-20948 I2C address (0x68 or 0x69) |

### SPI Mode Reference

| Mode | CPOL | CPHA | Idle Clock | Sample On | Devices |
|------|------|------|------------|-----------|---------|
| 0 | 0 | 0 | LOW | Rising | MCP3208, ICM-20948, many ADCs |
| 1 | 0 | 1 | LOW | Falling | Some Microchip ICs |
| 2 | 1 | 0 | HIGH | Falling | Some Nordic ICs |
| 3 | 1 | 1 | HIGH | Rising | MCP2515 (CAN), some displays |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| `RuntimeError: No access to /dev/gpiomem` on RPi 5 | Using RPi.GPIO which is incompatible with RP1 chip | Replace with `gpiod` or `lgpio`. Do not use RPi.GPIO on RPi 5. |
| `i2cdetect` shows no devices | I2C not enabled, wiring error, or wrong pull-up voltage | Run `sudo raspi-config nonint do_i2c 0`; check SDA/SCL, 3.3 V pull-ups, device address |
| I2C read returns all zeros or garbage | Missing pull-up resistors or clock speed too high | Add 4.7 kΩ pull-ups to 3.3 V; reduce clock with `dtparam=i2c_arm_baudrate=100000` |
| `OSError: [Errno 121] Remote I/O error` | Wrong I2C address, device not powered, or wiring broken | Verify address with `i2cdetect -y 1`; check Vcc and GND |
| SPI data always reads 0xFF | CS not asserted, MISO not connected, or wrong SPI mode | Check CS line state; verify MISO wiring; try all 4 SPI modes |
| Servo jittering with software PWM | Linux scheduler preempts the PWM thread causing timing variability | Use hardware PWM via `/sys/class/pwm/`; PWM jitter should be < 1 µs |
| `gpiod.LineEvent.RISING_EDGE` never fires | Line not configured for edge events, or wrong edge type | Request with `LINE_REQ_EV_RISING_EDGE` or `LINE_REQ_EV_BOTH_EDGES` |
| Encoder count drifts or misses steps | Polling thread too slow, or bounce on encoder signal | Increase thread priority; add 100 nF decoupling capacitor across encoder outputs |
| `PermissionError: [Errno 13] Permission denied: '/dev/spidev0.0'` | User not in `spi` group | `sudo usermod -a -G spi $USER` then log out/in |
| `/sys/class/pwm/pwmchip0` does not exist | PWM overlay not loaded | Add `dtoverlay=pwm-2chan` to `/boot/firmware/config.txt` and reboot |
| `ValueError: invalid literal` reading sysfs PWM | Period not set before duty cycle | Always write `period` before `duty_cycle`; set `enable=0` before changing period |
| I2C clock stretching causes data corruption | Master reads before slave is ready | Add `time.sleep()` after trigger commands; use repeated-start with sufficient delay |

## Workflow Integration

- Before integrating GPIO/I2C/SPI sensors, read `microcontrollers` to understand the firmware side communicating over UART/SPI with the Linux host.
- For sensor data that feeds into SLAM or EKF, see `sensor-fusion-slam` for ROS2 topic conventions and QoS profiles.
- Hardware PWM patterns here complement `realtime-motor-control` — use this skill for Linux-side GPIO/PWM, and `realtime-motor-control` for closed-loop PID on embedded targets.
- When writing ROS2 nodes that interface hardware, follow `ros2-node-creation` patterns (executor choice, callback groups, QoS profiles).
- For I2C/SPI sensors on an STM32 or ESP32 that then communicate with ROS2 via micro-ROS, see `rtos-micro-ros`.
- Deploy hardware nodes as systemd services with udev rules using the `robot-bringup` skill.
