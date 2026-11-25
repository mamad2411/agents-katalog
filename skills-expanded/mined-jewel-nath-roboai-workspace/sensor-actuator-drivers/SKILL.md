---
name: sensor-actuator-drivers
description: Custom ROS2 driver development for sensors (IMU, encoders, ultrasonic, ToF) and actuators (motors, servos, LEDs), including driver architecture, calibration, and hardware abstraction layers.
category: hardware
tags: [drivers, sensors, actuators, ros2, hardware-abstraction, imu, encoder, motor, calibration]
version: "1.0.0"
---

# Sensor and Actuator Drivers

Custom ROS2 driver development bridges raw hardware to the ROS2 ecosystem. This skill covers architecture patterns, concrete driver implementations for common sensors and actuators, calibration workflows, and testing without physical hardware.

## When to Use

- Writing a new ROS2 driver node for a sensor not covered by existing packages
- Integrating an IMU (ICM-20948, MPU-6050, BNO055) and publishing `sensor_msgs/Imu`
- Implementing quadrature encoder reading and publishing `sensor_msgs/JointState`
- Adding an ultrasonic or ToF (VL53L0X) range sensor and publishing `sensor_msgs/Range`
- Building a HAL layer to abstract motor PWM + encoder feedback
- Wiring servo angle commands to PWM output with limit enforcement
- Integrating ROS2 diagnostics into a hardware driver
- Testing driver nodes with mock hardware (no physical device required)
- Calibrating sensor bias, axis alignment, or scale factors
- Porting a vendor SDK into a ROS2 node with parameter-driven config

## Quick Start

```bash
# Install ROS2 Jazzy and build dependencies
sudo apt install ros-jazzy-ros-base ros-jazzy-diagnostic-updater \
                 python3-smbus2 python3-serial

# Create a new driver package
cd ~/robot_ws/src
ros2 pkg create my_sensor_driver \
  --build-type ament_python \
  --dependencies rclpy sensor_msgs diagnostic_updater

# Build and run
cd ~/robot_ws
colcon build --packages-select my_sensor_driver
source install/setup.bash
ros2 run my_sensor_driver imu_driver_node
```

**Minimal IMU driver in 30 seconds:**

```python
# my_sensor_driver/imu_driver_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuDriverNode(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self._pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.create_timer(0.02, self._publish)  # 50 Hz

    def _publish(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'
        # Fill accel/gyro from hardware here
        self._pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(ImuDriverNode())
    rclpy.shutdown()
```

## Core Concepts

### 1. Hardware Abstraction Layer (HAL) Pattern

Separate hardware I/O from ROS2 logic. The HAL is a pure Python/C++ class with no ROS2 imports.

```python
# hal/imu_hal.py — no ROS2 imports
import smbus2
import struct

ICM20948_ADDR = 0x68
REG_ACCEL_XOUT_H = 0x2D
REG_GYRO_XOUT_H  = 0x33
REG_WHO_AM_I     = 0x00
WHO_AM_I_EXPECTED = 0xEA

ACCEL_SCALE = 9.81 / 2048.0   # ±16g range → m/s²
GYRO_SCALE  = 0.001065264      # ±2000 dps → rad/s


class Icm20948Hal:
    """Hardware abstraction for ICM-20948 IMU over I2C."""

    def __init__(self, bus: int = 1, address: int = ICM20948_ADDR):
        self._bus = smbus2.SMBus(bus)
        self._addr = address
        self._validate_device()

    def _validate_device(self) -> None:
        who = self._bus.read_byte_data(self._addr, REG_WHO_AM_I)
        if who != WHO_AM_I_EXPECTED:
            raise RuntimeError(
                f"ICM-20948 not found: WHO_AM_I=0x{who:02X}, expected 0x{WHO_AM_I_EXPECTED:02X}"
            )

    def read_accel(self) -> tuple[float, float, float]:
        """Read accelerometer. Returns (ax, ay, az) in m/s²."""
        raw = self._bus.read_i2c_block_data(self._addr, REG_ACCEL_XOUT_H, 6)
        ax, ay, az = struct.unpack('>3h', bytes(raw))
        return ax * ACCEL_SCALE, ay * ACCEL_SCALE, az * ACCEL_SCALE

    def read_gyro(self) -> tuple[float, float, float]:
        """Read gyroscope. Returns (gx, gy, gz) in rad/s."""
        raw = self._bus.read_i2c_block_data(self._addr, REG_GYRO_XOUT_H, 6)
        gx, gy, gz = struct.unpack('>3h', bytes(raw))
        return gx * GYRO_SCALE, gy * GYRO_SCALE, gz * GYRO_SCALE

    def close(self) -> None:
        self._bus.close()
```

```python
# ros2_node/imu_driver_node.py — ROS2 adapter wraps the HAL
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from hal.imu_hal import Icm20948Hal

class ImuDriverNode(Node):
    """ROS2 adapter for ICM-20948 — drives the HAL, publishes sensor_msgs/Imu."""

    def __init__(self):
        super().__init__('imu_driver')

        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('i2c_address', 0x68)
        self.declare_parameter('frame_id', 'imu_link')
        self.declare_parameter('publish_rate', 50.0)

        bus  = self.get_parameter('i2c_bus').value
        addr = self.get_parameter('i2c_address').value
        self._frame_id = self.get_parameter('frame_id').value
        rate = self.get_parameter('publish_rate').value

        self._hal = Icm20948Hal(bus=bus, address=addr)
        self._pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.create_timer(1.0 / rate, self._timer_cb)
        self.get_logger().info(f'IMU driver started at {rate} Hz')

    def _timer_cb(self) -> None:
        ax, ay, az = self._hal.read_accel()
        gx, gy, gz = self._hal.read_gyro()

        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self._frame_id
        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linear_acceleration.z = az
        msg.angular_velocity.x = gx
        msg.angular_velocity.y = gy
        msg.angular_velocity.z = gz
        # -1 means covariance unknown; fill after calibration
        msg.linear_acceleration_covariance[0] = -1.0
        msg.angular_velocity_covariance[0] = -1.0
        msg.orientation_covariance[0] = -1.0
        self._pub.publish(msg)

    def destroy_node(self) -> None:
        self._hal.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = ImuDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### 2. Quadrature Encoder Driver

Encoders require overflow-safe delta computation and velocity estimation.

```python
# hal/encoder_hal.py
import serial
import struct

# Protocol: firmware sends [0xAA, FL_H, FL_L, BL_H, BL_L, FR_H, FR_L, BR_H, BR_L, checksum]
SYNC_BYTE    = 0xAA
PACKET_SIZE  = 10
ENCODER_CPR  = 1320   # counts per revolution (11 PPR × 30 gear × 4 quadrature)
INT32_MAX    = 2147483647


class EncoderHal:
    """Read quadrature encoder counts from serial firmware protocol."""

    def __init__(self, port: str, baudrate: int = 921600):
        self._serial = serial.Serial(port, baudrate, timeout=0.02)
        self._prev_counts = [0, 0, 0, 0]

    def read_counts(self) -> list[int]:
        """Return raw 32-bit signed encoder counts [FL, BL, FR, BR]."""
        self._serial.read_until(bytes([SYNC_BYTE]))
        raw = self._serial.read(PACKET_SIZE - 1)
        if len(raw) < PACKET_SIZE - 1:
            return self._prev_counts
        counts = list(struct.unpack('>4i', raw[:16]))
        self._prev_counts = counts
        return counts

    def compute_deltas(self, new_counts: list[int]) -> list[int]:
        """Compute encoder deltas with 32-bit overflow wrapping."""
        deltas = []
        for new, prev in zip(new_counts, self._prev_counts):
            delta = new - prev
            # Handle overflow: if jump > half INT32 range, it wrapped
            if delta > INT32_MAX:
                delta -= 2 * (INT32_MAX + 1)
            elif delta < -INT32_MAX - 1:
                delta += 2 * (INT32_MAX + 1)
            deltas.append(delta)
        return deltas

    def close(self) -> None:
        self._serial.close()
```

```python
# ros2_node/encoder_driver_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from hal.encoder_hal import EncoderHal, ENCODER_CPR
import math

WHEEL_NAMES = ['front_left_wheel', 'back_left_wheel', 'front_right_wheel', 'back_right_wheel']
TWO_PI = 2.0 * math.pi


class EncoderDriverNode(Node):
    """Publishes wheel joint states from quadrature encoder readings."""

    def __init__(self):
        super().__init__('encoder_driver')

        self.declare_parameter('serial_port', '/dev/motordriver')
        self.declare_parameter('baudrate', 921600)
        self.declare_parameter('publish_rate', 50.0)

        port  = self.get_parameter('serial_port').value
        baud  = self.get_parameter('baudrate').value
        rate  = self.get_parameter('publish_rate').value

        self._hal = EncoderHal(port, baud)
        self._prev_counts = [0, 0, 0, 0]
        self._positions   = [0.0, 0.0, 0.0, 0.0]
        self._prev_time   = self.get_clock().now()

        self._pub = self.create_publisher(JointState, 'joint_states', 10)
        self.create_timer(1.0 / rate, self._timer_cb)

    def _timer_cb(self) -> None:
        now = self.get_clock().now()
        dt  = (now - self._prev_time).nanoseconds * 1e-9
        self._prev_time = now

        counts = self._hal.read_counts()
        deltas = self._hal.compute_deltas(counts)
        self._prev_counts = counts

        velocities = []
        for i, delta in enumerate(deltas):
            angle_delta = (delta / ENCODER_CPR) * TWO_PI
            self._positions[i] += angle_delta
            velocities.append(angle_delta / dt if dt > 0 else 0.0)

        msg = JointState()
        msg.header.stamp = now.to_msg()
        msg.name     = WHEEL_NAMES
        msg.position = list(self._positions)
        msg.velocity = velocities
        self._pub.publish(msg)

    def destroy_node(self) -> None:
        self._hal.close()
        super().destroy_node()
```

### 3. ToF Range Sensor (VL53L0X) over I2C

```python
# hal/vl53l0x_hal.py
import smbus2
import time

VL53L0X_ADDR         = 0x29
REG_SYSRANGE_START   = 0x00
REG_RESULT_RANGE_MM  = 0x1E
REG_IDENTIFICATION   = 0xC0
EXPECTED_MODEL_ID    = 0xEE

RANGE_STATUS_GOOD    = 0x00
OUT_OF_RANGE_MM      = 8190   # Sensor returns this when out of range


class Vl53l0xHal:
    """Hardware abstraction for VL53L0X ToF distance sensor."""

    def __init__(self, bus: int = 1, address: int = VL53L0X_ADDR):
        self._bus  = smbus2.SMBus(bus)
        self._addr = address
        self._init_device()

    def _init_device(self) -> None:
        model_id = self._bus.read_byte_data(self._addr, REG_IDENTIFICATION)
        if model_id != EXPECTED_MODEL_ID:
            raise RuntimeError(f'VL53L0X not found: model_id=0x{model_id:02X}')
        # Single-shot mode: start ranging, read result, repeat
        self._bus.write_byte_data(self._addr, REG_SYSRANGE_START, 0x01)
        time.sleep(0.05)

    def read_range_mm(self) -> tuple[float, bool]:
        """Return (range_mm, is_valid). range_mm is -1.0 on error."""
        # Trigger a measurement
        self._bus.write_byte_data(self._addr, REG_SYSRANGE_START, 0x01)
        time.sleep(0.025)

        data = self._bus.read_i2c_block_data(self._addr, REG_RESULT_RANGE_MM, 2)
        range_mm = (data[0] << 8) | data[1]

        if range_mm >= OUT_OF_RANGE_MM:
            return -1.0, False
        return float(range_mm), True

    def close(self) -> None:
        self._bus.close()
```

```python
# ros2_node/range_driver_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from hal.vl53l0x_hal import Vl53l0xHal
import math

class RangeDriverNode(Node):
    """Publishes sensor_msgs/Range from a VL53L0X ToF sensor."""

    def __init__(self):
        super().__init__('range_driver')

        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('frame_id', 'range_sensor_link')
        self.declare_parameter('min_range', 0.03)    # 30 mm minimum
        self.declare_parameter('max_range', 2.0)     # 2 m maximum
        self.declare_parameter('field_of_view', 0.44)  # ~25 degrees
        self.declare_parameter('publish_rate', 20.0)

        bus  = self.get_parameter('i2c_bus').value
        self._frame_id = self.get_parameter('frame_id').value
        self._min_range = self.get_parameter('min_range').value
        self._max_range = self.get_parameter('max_range').value
        self._fov       = self.get_parameter('field_of_view').value

        self._hal = Vl53l0xHal(bus=bus)
        self._pub = self.create_publisher(Range, 'range', 10)
        self.create_timer(
            1.0 / self.get_parameter('publish_rate').value,
            self._timer_cb
        )

    def _timer_cb(self) -> None:
        range_mm, valid = self._hal.read_range_mm()

        msg = Range()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = self._frame_id
        msg.radiation_type  = Range.INFRARED
        msg.field_of_view   = self._fov
        msg.min_range       = self._min_range
        msg.max_range       = self._max_range
        msg.range           = range_mm / 1000.0 if valid else float('inf')
        self._pub.publish(msg)
```

### 4. Motor Driver Abstraction with PID Feedback

```python
# hal/motor_hal.py
import serial
import struct
import threading

# Serial protocol: [0xFF, motor_id, speed_high, speed_low, checksum]
# speed is int16 in encoder ticks/s (negative = reverse)
SYNC_BYTE   = 0xFF
MAX_SPEED   = 32767   # int16 max


class MotorHal:
    """HAL for a 4-motor driver communicating over serial."""

    def __init__(self, port: str, baudrate: int = 115200):
        self._serial = serial.Serial(port, baudrate, timeout=0.1)
        self._lock   = threading.Lock()

    def set_speeds(self, speeds: list[int]) -> None:
        """Set motor speeds [FL, BL, FR, BR] in encoder ticks/s."""
        assert len(speeds) == 4
        clamped = [max(-MAX_SPEED, min(MAX_SPEED, s)) for s in speeds]
        payload = struct.pack('>4h', *clamped)
        checksum = sum(payload) & 0xFF
        packet = bytes([SYNC_BYTE]) + payload + bytes([checksum])
        with self._lock:
            self._serial.write(packet)

    def stop(self) -> None:
        self.set_speeds([0, 0, 0, 0])

    def close(self) -> None:
        self.stop()
        self._serial.close()
```

```python
# hal/velocity_pid.py — pure Python, no ROS2
import time

class VelocityPid:
    """Discrete PID controller for single-axis velocity control."""

    def __init__(self, kp: float, ki: float, kd: float,
                 output_min: float = -1.0, output_max: float = 1.0):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._output_min = output_min
        self._output_max = output_max
        self._integral    = 0.0
        self._prev_error  = 0.0
        self._prev_time   = time.monotonic()

    def update(self, setpoint: float, measured: float) -> float:
        now = time.monotonic()
        dt  = now - self._prev_time
        if dt <= 0.0:
            return 0.0
        self._prev_time = now

        error = setpoint - measured
        self._integral += error * dt
        derivative = (error - self._prev_error) / dt
        self._prev_error = error

        output = (self._kp * error
                  + self._ki * self._integral
                  + self._kd * derivative)
        return max(self._output_min, min(self._output_max, output))

    def reset(self) -> None:
        self._integral   = 0.0
        self._prev_error = 0.0
```

### 5. Servo Driver with Angle Limits

```python
# hal/servo_hal.py
import RPi.GPIO as GPIO
import time

# Standard hobby servo: 50 Hz, 1 ms (0°) to 2 ms (180°) pulse
PWM_FREQUENCY   = 50        # Hz
PULSE_MIN_US    = 500       # microseconds → 0 degrees
PULSE_MAX_US    = 2500      # microseconds → 180 degrees
ANGLE_MIN_DEG   = 0.0
ANGLE_MAX_DEG   = 180.0


def _angle_to_duty_cycle(angle_deg: float) -> float:
    """Convert angle in degrees to GPIO PWM duty cycle (0-100)."""
    pulse_us = PULSE_MIN_US + (angle_deg / ANGLE_MAX_DEG) * (PULSE_MAX_US - PULSE_MIN_US)
    # Duty cycle = pulse_us / period_us
    period_us = 1_000_000.0 / PWM_FREQUENCY
    return (pulse_us / period_us) * 100.0


class ServoHal:
    """Hardware abstraction for a single PWM servo on Raspberry Pi GPIO."""

    def __init__(self, gpio_pin: int,
                 min_angle: float = ANGLE_MIN_DEG,
                 max_angle: float = ANGLE_MAX_DEG):
        self._pin      = gpio_pin
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._current_angle = 90.0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.OUT)
        self._pwm = GPIO.PWM(gpio_pin, PWM_FREQUENCY)
        self._pwm.start(_angle_to_duty_cycle(self._current_angle))

    def set_angle(self, angle_deg: float) -> float:
        """Move servo to angle_deg. Returns the clamped angle actually set."""
        clamped = max(self._min_angle, min(self._max_angle, angle_deg))
        self._current_angle = clamped
        self._pwm.ChangeDutyCycle(_angle_to_duty_cycle(clamped))
        return clamped

    @property
    def current_angle(self) -> float:
        return self._current_angle

    def close(self) -> None:
        self._pwm.stop()
        GPIO.cleanup(self._pin)
```

```python
# ros2_node/servo_driver_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from hal.servo_hal import ServoHal


class ServoDriverNode(Node):
    """ROS2 driver for a single servo. Subscribes to angle commands."""

    def __init__(self):
        super().__init__('servo_driver')

        self.declare_parameter('gpio_pin', 18)
        self.declare_parameter('min_angle', 0.0)
        self.declare_parameter('max_angle', 180.0)
        self.declare_parameter('initial_angle', 90.0)

        pin         = self.get_parameter('gpio_pin').value
        min_angle   = self.get_parameter('min_angle').value
        max_angle   = self.get_parameter('max_angle').value
        init_angle  = self.get_parameter('initial_angle').value

        self._hal = ServoHal(pin, min_angle, max_angle)
        self._hal.set_angle(init_angle)

        self._cmd_sub = self.create_subscription(
            Float32, 'servo/cmd_angle', self._cmd_cb, 10
        )
        self._pos_pub = self.create_publisher(Float32, 'servo/current_angle', 10)
        self.get_logger().info(f'Servo driver on GPIO {pin}')

    def _cmd_cb(self, msg: Float32) -> None:
        actual = self._hal.set_angle(msg.data)
        out = Float32()
        out.data = actual
        self._pos_pub.publish(out)
        if abs(actual - msg.data) > 0.5:
            self.get_logger().warn(
                f'Servo clamped: requested {msg.data:.1f}° → {actual:.1f}°'
            )

    def destroy_node(self) -> None:
        self._hal.close()
        super().destroy_node()
```

### 6. Driver Diagnostics Integration

All production drivers should publish to `/diagnostics` using `diagnostic_updater`.

```python
# ros2_node/imu_driver_with_diagnostics.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from diagnostic_updater import Updater, DiagnosticStatusWrapper
from hal.imu_hal import Icm20948Hal

OK     = DiagnosticStatusWrapper.OK
WARN   = DiagnosticStatusWrapper.WARN
ERROR  = DiagnosticStatusWrapper.ERROR

STALE_THRESHOLD_S = 1.0   # Declare stale if no read in this many seconds


class ImuDriverWithDiagnostics(Node):
    """IMU driver with diagnostic_updater for /diagnostics topic."""

    def __init__(self):
        super().__init__('imu_driver')

        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('publish_rate', 50.0)
        rate = self.get_parameter('publish_rate').value

        self._hal = Icm20948Hal(bus=self.get_parameter('i2c_bus').value)
        self._pub = self.create_publisher(Imu, 'imu/data_raw', 10)

        self._read_count  = 0
        self._error_count = 0
        self._last_read_time = self.get_clock().now()

        # Diagnostics updater
        self._updater = Updater(self)
        self._updater.setHardwareID('ICM-20948')
        self._updater.add('IMU Status', self._diag_cb)

        self.create_timer(1.0 / rate, self._timer_cb)

    def _timer_cb(self) -> None:
        try:
            ax, ay, az = self._hal.read_accel()
            gx, gy, gz = self._hal.read_gyro()
            self._read_count += 1
            self._last_read_time = self.get_clock().now()

            msg = Imu()
            msg.header.stamp = self._last_read_time.to_msg()
            msg.header.frame_id = 'imu_link'
            msg.linear_acceleration.x = ax
            msg.linear_acceleration.y = ay
            msg.linear_acceleration.z = az
            msg.angular_velocity.x = gx
            msg.angular_velocity.y = gy
            msg.angular_velocity.z = gz
            msg.linear_acceleration_covariance[0] = -1.0
            msg.angular_velocity_covariance[0] = -1.0
            msg.orientation_covariance[0] = -1.0
            self._pub.publish(msg)
        except OSError as e:
            self._error_count += 1
            self.get_logger().error(f'IMU read error: {e}')

    def _diag_cb(self, stat: DiagnosticStatusWrapper) -> DiagnosticStatusWrapper:
        age_s = (self.get_clock().now() - self._last_read_time).nanoseconds * 1e-9
        error_rate = self._error_count / max(self._read_count, 1)

        if age_s > STALE_THRESHOLD_S:
            stat.summary(ERROR, f'No data for {age_s:.1f}s')
        elif error_rate > 0.05:
            stat.summary(WARN, f'Error rate {error_rate:.1%}')
        else:
            stat.summary(OK, 'Operating normally')

        stat.add('Read count',   str(self._read_count))
        stat.add('Error count',  str(self._error_count))
        stat.add('Data age (s)', f'{age_s:.3f}')
        return stat
```

## Common Patterns

### Pattern 1: Complete IMU Node with Bias Calibration

```python
# my_imu_driver/imu_driver_node.py
"""
Complete IMU driver with:
- Static bias calibration on startup
- Axis remapping (hardware → ROS frame)
- Covariance population from calibration data
- Diagnostics
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from diagnostic_updater import Updater, DiagnosticStatusWrapper
from hal.imu_hal import Icm20948Hal
import numpy as np
import json
import os

# ROS convention: X forward, Y left, Z up
# ICM-20948 mounted with X right, Y forward, Z up (example rotation)
# Axis remap matrix: ros_vec = AXIS_REMAP @ hw_vec
AXIS_REMAP = np.array([
    [ 0,  1,  0],   # ROS X = hw Y (forward)
    [-1,  0,  0],   # ROS Y = -hw X (left)
    [ 0,  0,  1],   # ROS Z = hw Z (up)
], dtype=float)

CALIBRATION_SAMPLES = 200   # Samples collected at rest during calibration
CALIBRATION_FILE    = '/tmp/imu_calibration.json'


class ImuDriverNode(Node):
    """Production IMU driver with calibration and diagnostics."""

    def __init__(self):
        super().__init__('imu_driver')

        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('frame_id', 'imu_link')
        self.declare_parameter('publish_rate', 50.0)
        self.declare_parameter('calibrate_on_start', False)
        self.declare_parameter('calibration_file', CALIBRATION_FILE)

        rate   = self.get_parameter('publish_rate').value
        cal_file = self.get_parameter('calibration_file').value

        self._frame_id = self.get_parameter('frame_id').value
        self._hal = Icm20948Hal(bus=self.get_parameter('i2c_bus').value)

        # Bias offsets (rad/s for gyro, m/s² for accel)
        self._gyro_bias  = np.zeros(3)
        self._accel_bias = np.zeros(3)
        self._gyro_var   = np.zeros(3)
        self._accel_var  = np.zeros(3)

        self._load_calibration(cal_file)

        if self.get_parameter('calibrate_on_start').value:
            self._collect_calibration()
            self._save_calibration(cal_file)

        self._pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        self._read_count  = 0
        self._error_count = 0
        self._last_stamp  = self.get_clock().now()

        self._updater = Updater(self)
        self._updater.setHardwareID('ICM-20948')
        self._updater.add('IMU', self._diag_cb)

        self.create_timer(1.0 / rate, self._timer_cb)
        self.get_logger().info('IMU driver ready')

    def _timer_cb(self) -> None:
        try:
            ax_hw, ay_hw, az_hw = self._hal.read_accel()
            gx_hw, gy_hw, gz_hw = self._hal.read_gyro()

            # Apply axis remap
            accel_hw = np.array([ax_hw, ay_hw, az_hw])
            gyro_hw  = np.array([gx_hw, gy_hw, gz_hw])
            accel_ros = AXIS_REMAP @ accel_hw - self._accel_bias
            gyro_ros  = AXIS_REMAP @ gyro_hw  - self._gyro_bias

            now = self.get_clock().now()
            self._last_stamp = now
            self._read_count += 1

            msg = Imu()
            msg.header.stamp    = now.to_msg()
            msg.header.frame_id = self._frame_id
            msg.linear_acceleration.x = accel_ros[0]
            msg.linear_acceleration.y = accel_ros[1]
            msg.linear_acceleration.z = accel_ros[2]
            msg.angular_velocity.x = gyro_ros[0]
            msg.angular_velocity.y = gyro_ros[1]
            msg.angular_velocity.z = gyro_ros[2]
            msg.orientation_covariance[0] = -1.0

            # Diagonal covariance from calibration variance
            cov_a = msg.linear_acceleration_covariance
            cov_g = msg.angular_velocity_covariance
            for i, v in enumerate(self._accel_var):
                cov_a[i * 4] = v
            for i, v in enumerate(self._gyro_var):
                cov_g[i * 4] = v

            self._pub.publish(msg)
        except OSError as e:
            self._error_count += 1
            self.get_logger().error(f'IMU read error: {e}', throttle_duration_sec=2.0)

    def _collect_calibration(self) -> None:
        """Collect static samples to estimate bias and variance."""
        self.get_logger().info(
            f'Calibrating: hold robot still for {CALIBRATION_SAMPLES} samples...'
        )
        accel_samples, gyro_samples = [], []
        for _ in range(CALIBRATION_SAMPLES):
            ax, ay, az = self._hal.read_accel()
            gx, gy, gz = self._hal.read_gyro()
            accel_samples.append([ax, ay, az])
            gyro_samples.append([gx, gy, gz])

        accel_arr = np.array(accel_samples)
        gyro_arr  = np.array(gyro_samples)

        self._accel_bias = accel_arr.mean(axis=0)
        self._gyro_bias  = gyro_arr.mean(axis=0)
        # Remove gravity from Z bias (expect ~9.81 m/s²)
        self._accel_bias[2] -= 9.81

        self._accel_var  = accel_arr.var(axis=0)
        self._gyro_var   = gyro_arr.var(axis=0)
        self.get_logger().info(
            f'Calibration done. Gyro bias: {self._gyro_bias}, '
            f'Accel bias: {self._accel_bias}'
        )

    def _save_calibration(self, path: str) -> None:
        data = {
            'accel_bias': self._accel_bias.tolist(),
            'gyro_bias':  self._gyro_bias.tolist(),
            'accel_var':  self._accel_var.tolist(),
            'gyro_var':   self._gyro_var.tolist(),
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        self.get_logger().info(f'Calibration saved to {path}')

    def _load_calibration(self, path: str) -> None:
        if not os.path.exists(path):
            self.get_logger().warn(f'No calibration file at {path}, using zero bias')
            return
        with open(path) as f:
            data = json.load(f)
        self._accel_bias = np.array(data['accel_bias'])
        self._gyro_bias  = np.array(data['gyro_bias'])
        self._accel_var  = np.array(data.get('accel_var', [0.01, 0.01, 0.01]))
        self._gyro_var   = np.array(data.get('gyro_var', [0.001, 0.001, 0.001]))
        self.get_logger().info(f'Calibration loaded from {path}')

    def _diag_cb(self, stat: DiagnosticStatusWrapper) -> DiagnosticStatusWrapper:
        age_s = (self.get_clock().now() - self._last_stamp).nanoseconds * 1e-9
        if age_s > 1.0:
            stat.summary(DiagnosticStatusWrapper.ERROR, f'Stale ({age_s:.1f}s)')
        elif self._error_count > 0:
            stat.summary(DiagnosticStatusWrapper.WARN, f'{self._error_count} errors')
        else:
            stat.summary(DiagnosticStatusWrapper.OK, 'OK')
        stat.add('Read count',   str(self._read_count))
        stat.add('Error count',  str(self._error_count))
        stat.add('Gyro bias',    str(self._gyro_bias.round(5)))
        stat.add('Accel bias',   str(self._accel_bias.round(4)))
        return stat

    def destroy_node(self) -> None:
        self._hal.close()
        super().destroy_node()


def main():
    rclpy.init()
    node = ImuDriverNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### Pattern 2: Complete Encoder Driver with Launch File

```python
# launch/encoder_driver.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('serial_port', default_value='/dev/motordriver'),
        DeclareLaunchArgument('baudrate',    default_value='921600'),
        DeclareLaunchArgument('publish_rate', default_value='50.0'),

        Node(
            package='my_encoder_driver',
            executable='encoder_driver_node',
            name='encoder_driver',
            output='screen',
            parameters=[{
                'serial_port':  LaunchConfiguration('serial_port'),
                'baudrate':     LaunchConfiguration('baudrate'),
                'publish_rate': LaunchConfiguration('publish_rate'),
            }],
            remappings=[
                ('joint_states', '/joint_states'),
            ],
        ),
    ])
```

### Pattern 3: Mock HAL for Testing Without Hardware

```python
# test/mock_imu_hal.py
"""Mock HAL for unit testing the IMU driver node without hardware."""
import math
import time


class MockIcm20948Hal:
    """Simulates ICM-20948 readings: gravity on Z, sinusoidal gyro."""

    def __init__(self, bus: int = 1, address: int = 0x68):
        self._start = time.monotonic()

    def read_accel(self) -> tuple[float, float, float]:
        """Returns static gravity on Z axis with small noise."""
        t = time.monotonic() - self._start
        return (
            0.01 * math.sin(t),   # ax noise
            0.01 * math.cos(t),   # ay noise
            9.81 + 0.01 * math.sin(2 * t),  # az ≈ gravity
        )

    def read_gyro(self) -> tuple[float, float, float]:
        """Returns near-zero gyro with small drift."""
        t = time.monotonic() - self._start
        return (
            0.001 * math.sin(t * 0.5),
            0.001 * math.cos(t * 0.5),
            0.0005,
        )

    def close(self) -> None:
        pass
```

```python
# test/test_imu_driver.py
import pytest
import rclpy
from sensor_msgs.msg import Imu
from my_imu_driver.imu_driver_node import ImuDriverNode
from test.mock_imu_hal import MockIcm20948Hal


@pytest.fixture(scope='module')
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_imu_publishes_valid_message(ros_context):
    """Verify the IMU node publishes a valid Imu message with correct frame_id."""
    node = ImuDriverNode.__new__(ImuDriverNode)
    # Inject mock HAL before __init__ completes
    ImuDriverNode.__init__.__wrapped__ = None  # Skip actual init
    node._hal = MockIcm20948Hal()
    node._frame_id = 'imu_link'

    # Directly call the timer callback
    received = []
    node._pub = type('pub', (), {'publish': lambda self, m: received.append(m)})()
    node._read_count = 0
    node._error_count = 0

    # Simpler: use dependency injection in constructor
    # See Pattern 4 for the recommended approach


def test_mock_hal_gravity():
    """Verify mock HAL returns reasonable gravity on Z axis."""
    hal = MockIcm20948Hal()
    ax, ay, az = hal.read_accel()
    assert abs(az - 9.81) < 0.1, f'Expected ~9.81 m/s² on Z, got {az}'
    assert abs(ax) < 0.1
    assert abs(ay) < 0.1
```

### Pattern 4: Dependency-Injected Driver (Testable Design)

```python
# my_imu_driver/imu_driver_node.py — dependency injection for testability
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from hal.imu_hal import Icm20948Hal


class ImuDriverNode(Node):
    """IMU driver with injected HAL — easy to unit test."""

    def __init__(self, hal=None):
        super().__init__('imu_driver')

        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('publish_rate', 50.0)
        self.declare_parameter('frame_id', 'imu_link')

        self._frame_id = self.get_parameter('frame_id').value

        # Inject HAL or create from parameters
        if hal is not None:
            self._hal = hal
        else:
            self._hal = Icm20948Hal(bus=self.get_parameter('i2c_bus').value)

        self._pub = self.create_publisher(Imu, 'imu/data_raw', 10)
        rate = self.get_parameter('publish_rate').value
        self.create_timer(1.0 / rate, self._timer_cb)

    def _timer_cb(self) -> None:
        ax, ay, az = self._hal.read_accel()
        gx, gy, gz = self._hal.read_gyro()
        msg = Imu()
        msg.header.stamp    = self.get_clock().now().to_msg()
        msg.header.frame_id = self._frame_id
        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linear_acceleration.z = az
        msg.angular_velocity.x = gx
        msg.angular_velocity.y = gy
        msg.angular_velocity.z = gz
        msg.orientation_covariance[0] = -1.0
        msg.linear_acceleration_covariance[0] = -1.0
        msg.angular_velocity_covariance[0] = -1.0
        self._pub.publish(msg)


# test_imu_driver.py — clean unit test with injected mock
def test_imu_publishes_with_mock_hal(ros_context):
    from test.mock_imu_hal import MockIcm20948Hal
    node = ImuDriverNode(hal=MockIcm20948Hal())
    received = []
    node._pub = type('P', (), {'publish': lambda s, m: received.append(m)})()
    node._timer_cb()
    assert len(received) == 1
    assert received[0].header.frame_id == 'imu_link'
    assert abs(received[0].linear_acceleration.z - 9.81) < 0.2
    node.destroy_node()
```

## Anti-Patterns

### ❌ Reading hardware directly in the callback thread

I2C and serial reads block. Calling them directly in a ROS2 timer callback blocks the executor and causes missed deadlines.

```python
# WRONG — blocks the ROS2 executor thread
def _timer_cb(self):
    data = self._bus.read_i2c_block_data(self._addr, 0x3B, 6)  # may block 50ms
    self._pub.publish(self._parse(data))
```

### ✅ Use a dedicated read thread or async I/O

```python
# CORRECT — read thread decoupled from publish thread
import threading

class ImuDriverNode(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self._latest = None
        self._lock = threading.Lock()

        # Background reader thread
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

        # Timer only publishes pre-fetched data
        self.create_timer(0.02, self._publish_cb)

    def _read_loop(self):
        while rclpy.ok():
            try:
                data = self._hal.read_accel()
                with self._lock:
                    self._latest = data
            except OSError:
                pass

    def _publish_cb(self):
        with self._lock:
            data = self._latest
        if data:
            # Build and publish message
            pass
```

### ❌ Hardcoding I2C bus and address in the node

Hardcoded addresses make the driver unusable when bus changes (e.g., Pi 4 vs Pi 5 pin layout).

```python
# WRONG
class ImuDriverNode(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self._hal = Icm20948Hal(bus=1, address=0x68)  # hardcoded
```

### ✅ Declare all hardware config as ROS2 parameters

```python
# CORRECT — fully configurable via YAML or launch
class ImuDriverNode(Node):
    def __init__(self):
        super().__init__('imu_driver')
        self.declare_parameter('i2c_bus', 1)
        self.declare_parameter('i2c_address', 0x68)
        self.declare_parameter('frame_id', 'imu_link')
        bus  = self.get_parameter('i2c_bus').value
        addr = self.get_parameter('i2c_address').value
        self._hal = Icm20948Hal(bus=bus, address=addr)
```

### ❌ Ignoring 32-bit encoder overflow

Encoder tick registers are 32-bit integers. If the robot drives far enough, they overflow. Naively subtracting current - previous gives a huge spurious delta.

```python
# WRONG — breaks when encoder wraps
delta = new_count - prev_count   # Could be +4 billion on wrap
```

### ✅ Use wrapping subtraction

```python
# CORRECT — wraps safely for int32
INT32_RANGE = 2**32
delta = new_count - prev_count
if delta > INT32_RANGE // 2:
    delta -= INT32_RANGE
elif delta < -(INT32_RANGE // 2):
    delta += INT32_RANGE
```

### ❌ Not populating IMU covariance fields

Publishing `Imu` with all-zero covariances causes `robot_localization` EKF to treat the data as perfect measurements with zero noise — which leads to filter divergence.

```python
# WRONG — all zeros means "perfect, zero noise" to EKF
msg = Imu()
msg.linear_acceleration.x = ax
# covariances left at 0.0 by default
```

### ✅ Set covariance[0] = -1 if unknown, or populate from calibration

```python
# CORRECT — -1 tells EKF to ignore this measurement type
msg = Imu()
msg.linear_acceleration.x = ax
msg.orientation_covariance[0]          = -1.0   # orientation unknown
msg.linear_acceleration_covariance[0]  = -1.0   # or populate with variance
msg.angular_velocity_covariance[0]     = -1.0
```

### ❌ No error handling on hardware access

Unhandled I2C/serial errors crash the driver node permanently.

```python
# WRONG — one glitch kills the node
def _timer_cb(self):
    data = self._hal.read_accel()  # OSError if bus disconnected
```

### ✅ Catch hardware exceptions, log, and continue

```python
# CORRECT — transient errors are logged, node continues
def _timer_cb(self):
    try:
        data = self._hal.read_accel()
    except OSError as e:
        self._error_count += 1
        self.get_logger().error(f'Hardware read failed: {e}',
                                throttle_duration_sec=2.0)
        return
```

## Configuration Reference

### IMU Driver Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `i2c_bus` | int | `1` | Linux I2C bus number (`/dev/i2c-N`) |
| `i2c_address` | int | `0x68` | Device I2C address (0x68 or 0x69) |
| `frame_id` | string | `imu_link` | TF frame for header stamps |
| `publish_rate` | float | `50.0` | Output rate in Hz |
| `calibrate_on_start` | bool | `false` | Run bias calibration on startup |
| `calibration_file` | string | `/tmp/imu_calibration.json` | Path to load/save calibration |

### Encoder Driver Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `serial_port` | string | `/dev/motordriver` | Serial device path |
| `baudrate` | int | `921600` | Serial baud rate |
| `publish_rate` | float | `50.0` | Joint state publish rate in Hz |
| `encoder_cpr` | int | `1320` | Counts per revolution (11×30×4) |
| `wheel_names` | string[] | `[fl, bl, fr, br]` | Joint names in JointState message |

### Range Driver (VL53L0X) Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `i2c_bus` | int | `1` | Linux I2C bus number |
| `frame_id` | string | `range_sensor_link` | TF frame |
| `min_range` | float | `0.03` | Minimum valid range (m) |
| `max_range` | float | `2.0` | Maximum valid range (m) |
| `field_of_view` | float | `0.44` | Sensor FoV in radians (~25°) |
| `publish_rate` | float | `20.0` | Publish rate in Hz |

### Servo Driver Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `gpio_pin` | int | `18` | BCM GPIO pin number |
| `min_angle` | float | `0.0` | Minimum allowed angle (degrees) |
| `max_angle` | float | `180.0` | Maximum allowed angle (degrees) |
| `initial_angle` | float | `90.0` | Angle to set on startup (degrees) |

### Motor Driver Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `serial_port` | string | `/dev/motordriver` | Serial device path |
| `baudrate` | int | `115200` | Serial baud rate |
| `cmd_timeout` | float | `0.5` | Stop motors if no cmd received (s) |
| `max_speed_tps` | int | `32767` | Maximum speed in ticks/s |
| `kp` | float | `1.0` | PID proportional gain |
| `ki` | float | `0.1` | PID integral gain |
| `kd` | float | `0.01` | PID derivative gain |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| `FileNotFoundError: /dev/i2c-1` | I2C not enabled or wrong bus number | Run `sudo raspi-config` → Interface Options → I2C; check `i2c_bus` param |
| `OSError: [Errno 121] Remote I/O error` | Wrong I2C address or device not powered | Verify address with `i2cdetect -y 1`; check wiring and power |
| `WHO_AM_I mismatch` | Wrong sensor variant or register map | Verify sensor part number; update `WHO_AM_I_EXPECTED` constant |
| IMU publishes zeros or NaN | Axis remap matrix error | Print raw HAL values before remap; check `AXIS_REMAP` matrix signs |
| EKF diverges immediately | IMU covariance all-zero | Set `orientation_covariance[0] = -1.0`; populate accel/gyro covariances |
| Encoder delta spikes on startup | `prev_counts` not initialized from first read | Read one sample before starting the delta loop; initialize `_prev_counts` from first read |
| Joint velocity is zero | `dt` is exactly 0 on first callback | Guard with `if dt > 1e-6` before dividing |
| Servo jitters at target angle | PWM resolution too coarse | Use hardware PWM (pigpio) instead of software PWM; tune pulse width |
| Motor driver not responding | Serial framing mismatch | Use a logic analyzer or `screen /dev/motordriver 115200` to verify packet format |
| Driver node crashes on hardware error | Unhandled `OSError` | Wrap all hardware calls in `try/except OSError`; log and continue |
| `/diagnostics` not updating | `Updater` period > 1s | Default updater period is 1s; call `self._updater.force_update()` in timer if needed |
| High CPU from I2C reads | Reads blocking the executor | Move reads to a background thread; publish cached data in timer |

## Workflow Integration

**Before this skill:**
- `microcontrollers` — understand the firmware side that the driver communicates with
- `serial-can-protocols` — understand the UART/I2C/SPI protocol the HAL layer wraps

**After this skill:**
- `sensor-fusion-slam` — fuse IMU, encoder, and LiDAR data with EKF/UKF
- `realtime-motor-control` — add real-time PID loops above the motor HAL
- `ros2-control` — use `hardware_interface::ActuatorInterface` for ros2_control integration
- `deployment-fleet` — extend driver diagnostics with aggregator and rqt_runtime_monitor

**Typical workflow for a new sensor:**
1. Read the hardware datasheet and identify the communication protocol
2. Write and test the HAL class with a standalone Python script (no ROS2)
3. Write the ROS2 driver node wrapping the HAL with parameter-driven config
4. Add diagnostics integration
5. Write mock HAL and unit tests
6. Add launch file and YAML config
7. Test with `ros2 topic echo` and `rqt_plot`
