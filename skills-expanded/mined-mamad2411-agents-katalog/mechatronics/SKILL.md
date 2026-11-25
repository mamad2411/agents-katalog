---

## name: mechatronics
description: >
  Expert mechatronics assistant for engineers and researchers. Use this skill whenever the user needs:
  designing mechatronic systems, integrating sensors and actuators, PLC programming, control systems, system modeling,
  or any rigorous academic treatment of mechatronics. Covers electromechanical systems, automation, and robotics.
license: MIT
compatibility: opencode
metadata:
  audience: engineers, designers, integrators
  category: engineering

# Mechatronics — Academic Research Assistant

Covers: **System Integration · Sensors · Actuators · Control Systems · PLC Programming · Motor Control · Industrial Communication · System Design**

---

## System Architecture

### Mechatronic System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL SYSTEM                            │
│                    (PLC, MCU, PC)                          │
└─────────────────────────┬───────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
    ┌───────────┐ ┌───────────┐ ┌───────────┐
    │  Sensors  │ │ Actuation │ │  HMI/     │
    │  Input   │ │  Output   │ │  Display  │
    └───────────┘ └───────────┘ └───────────┘
```

### Real-Time Control Loop

```python
class MechatronicSystem:
    """Mechaetronic system architecture"""
    
    def __init__(self, loop_rate=1000):  # Hz
        self.loop_rate = loop_rate
        self.dt = 1.0 / loop_rate
        self.sensors = {}
        self.actuators = {}
        self.controller = None
        self.running = False
    
    def add_sensor(self, name, sensor):
        """Register sensor with system"""
        self.sensors[name] = {
            'device': sensor,
            'value': None,
            'timestamp': None
        }
    
    def add_actuator(self, name, actuator):
        """Register actuator with system"""
        self.actuators[name] = {
            'device': actuator,
            'command': 0,
            'timestamp': None
        }
    
    def read_all_sensors(self):
        """Poll all sensors"""
        for name in self.sensors:
            self.sensors[name]['value'] = \
                self.sensors[name]['device'].read()
            self.sensors[name]['timestamp'] = self.get_timestamp()
        
        return {name: s['value'] for name, s in self.sensors.items()}
    
    def control_loop(self):
        """Execute one control cycle"""
        # Read sensors
        sensor_data = self.read_all_sensors()
        
        # Compute control
        if self.controller:
            commands = self.controller.compute(sensor_data, self.dt)
        
        # Actuate
        self.actuate(commands)
        
        return sensor_data
    
    def actuate(self, commands):
        """Send commands to actuators"""
        for name, value in commands.items():
            if name in self.actuators:
                self.actuators[name]['device'].set_value(value)
                self.actuators[name]['command'] = value
                self.actuators[name]['timestamp'] = self.get_timestamp()
```

---

## Sensors

### Sensor Types and Interfaces

|Category|Examples|Interface|Output|
|--------|--------|----------|------|
|Position|Encoder, LVDT, Potentiometer|Analog/Digital|mm, degrees|
|Velocity|Tachometer, Encoder|Analog/Digital|RPM, m/s|
|Force|Strain gauge, Load cell|Bridge|Force (N)|
|Pressure|Strain gauge, Piezoresistive|Pressure (Pa)|
|Temperature|RTD, Thermocouple, Thermistor|Various|Temperature|
|Proximity|Inductive, Capacitive, Photoelectric|Digital|On/Off|
|Level|Ultrasonic, Capacitive|Analog|Distance|

```python
class SensorInterfaces:
    """Common sensor interfaces"""
    
    # Analog input (0-10V, 4-20mA)
    ADC_RESOLUTION = {
        "8-bit": 256,
        "10-bit": 1024,
        "12-bit": 4096,
        "16-bit": 65536
    }
    
    def read_analog_voltage(self, adc_value, vref, resolution):
        """Convert ADC to voltage"""
        return (adc_value / resolution) * vref
    
    def read_current_loop(self, adc_value, vref, resolution, current_range=20):
        """Convert 4-20mA loop to mA"""
        voltage = self.read_analog_voltage(adc_value, vref, resolution)
        # 4mA = 0%, 20mA = 100%
        return 4 + (voltage / vref) * (current_range - 4)
    
    # Encoder interface
    class RotaryEncoder:
        """Quadrature encoder"""
        
        def __init__(self, pin_a, pin_b, pulses_per_revolution):
            self.pin_a = pin_a
            self.pin_b = pin_b
            self.ppr = pulses_per_revolution
            self.count = 0
            self.position = 0
        
        def update(self, state_a, state_b):
            """Update from interrupt"""
            # Gray code decoding
            if state_a != state_b:
                self.count += 1 if state_a else -1
            
            self.position = (self.count / self.ppr) * 360
        
        def velocity(self, dt, prev_count):
            """Calculate RPM"""
            return ((self.count - prev_count) / self.ppr) / dt * 60
```

---

## Actuators

### Actuator Comparison

|Actuator|Control|Method|Power Density|Applications|
|--------|--------|------|-------------|------------|
|DC Motor|PWM, H-Bridge|Voltage|Medium|Mobile robots|
|Stepper|Open-loop|Step/Dir|Medium|Precision positioning|
|Servo|PWM|Position feedback|Robotics, CNC|
|AC Motor|VFD|Frequency|Servo drives|Industrial|
|Hydraulic|Proportional|Flow/Pressure|Very high|Heavy industry|
|Pneumatic|On/Off, Proportional|Pressure|Medium|Fast cycling|
|Piezoelectric|High voltage|Displacement|Very low|Precision|

```python
class DCMotorControl:
    """DC motor control methods"""
    
    def __init__(self, pwm_pin, dir_pin, encoder_ppr=512):
        self.pwm = pwm_pin
        self.dir = dir_pin
        self.encoder_ppr = encoder_ppr
        self.pwm_frequency = 20000  # Hz
    
    def set_speed(self, speed):
        """speed: -1.0 to 1.0"""
        # Direction
        if speed > 0:
            self.dir.write(1)
        else:
            self.dir.write(0)
        
        # PWM duty cycle
        self.pwm.write_duty_cycle(abs(speed) * 100)
    
    def pid_controller(self, setpoint, measurement, kp, ki, kd, dt):
        """PID velocity controller"""
        error = setpoint - measurement
        
        # Integral with anti-windup
        self.integral += error * dt
        if abs(self.integral) > self.integral_limit:
            self.integral = self.integral_limit * np.sign(self.integral)
        
        # Derivative
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        
        # Output
        output = kp * error + ki * self.integral + kd * derivative
        
        self.prev_error = error
        
        return np.clip(output, -1, 1)


class StepperMotorControl:
    """Stepper motor microstepping"""
    
    MICROSTEP_MODES = {
        "full": 1,
        "half": 2,
        "quarter": 4,
        "eighth": 8,
        "sixteenth": 16,
        "thirty-second": 32
    }
    
    def calculate_steps_per_revolution(self, steps_per_rev, microstepping):
        """Calculate total microsteps per revolution"""
        return steps_per_rev * self.MICROSTEP_MODES[microstepping]
    
    def rpm_to_pps(self, rpm, steps_per_rev, microstepping):
        """Convert RPM to pulses per second"""
        return (rpm * steps_per_rev * self.MICROSTEP_MODES[microstepping]) / 60
```

---

## PLC Programming

### IEC 61131-3 Languages

|Language|Type|Visual/Text|Use Case|
|--------|-----|-----------|--------|
|Ladder Diagram (LD)|Visual|Yes|Discrete logic|
|Function Block (FBD)|Visual|Yes|Process control|
|Structured Text (ST)|Text|No|Complex logic|
|Sequential Function Chart (SFC)|Visual|Yes|Sequential processes|
|Instruction List (IL)|Text|No|Low-level|

```python
class LadderLogic:
    """Ladder logic programming"""
    
    def __init__(self):
        self.coils = {}
        self.contacts = {}
        self.timers = {}
        self.counters = {}
    
    # Ladder elements
    def contact(self, address, normally_open=True):
        """Input contact"""
        return {
            "type": "contact",
            "address": address,
            "normally_open": normally_open,
            "state": False
        }
    
    def coil(self, address, latching=False):
        """Output coil"""
        return {
            "type": "coil",
            "address": address,
            "latching": latching,
            "state": False
        }
    
    def timer(self, preset, timer_type="TON"):
        """
        Timer types:
        - TON: Timer On-Delay
        - TOF: Timer Off-Delay
        - TP: Pulse
        """
        return {
            "type": "timer",
            "preset": preset,
            "timer_type": timer_type,
            "accumulated": 0,
            "done": False
        }
    
    def counter(self, preset, count_type="CTU"):
        """
        Counter types:
        - CTU: Count Up
        - CTD: Count Down
        - CTUD: Count Up/Down
        """
        return {
            "type": "counter",
            "preset": preset,
            "counter_type": count_type,
            "accumulated": 0,
            "done": False
        }
    
    # Example: Motor start/stop with overload
    """
    | I:0/0   I:0/1    O:0/0   |
    |----[ )[ ]----[ ]/( )----|
    
    I:0/0 = Start button (NO)
    I:0/1 = Stop button (NC)
    O:0/0 = Motor coil
    """


class StructuredText:
    """Structured text programming"""
    
    def motor_control_example(self, start_button, stop_button, 
                            overload, motor_on):
        """Motor control in ST"""
        
        # Latch motor on
        IF start_button AND NOT stop_button AND NOT overload THEN
            motor_on := TRUE;
        END_IF
        
        # Unlatch
        IF stop_button OR overload THEN
            motor_on := FALSE;
        END_IF
        
        return motor_on
    
    def pid_control(self, setpoint, process_variable, 
                   kp, ki, kd, dt):
        """PID in ST"""
        
        error := setpoint - process_variable;
        
        integral := integral + error * dt;
        
        derivative := (error - prev_error) / dt;
        
        output := kp * error + ki * integral + kd * derivative;
        
        prev_error := error;
        
        return output;
```

---

## Industrial Communication

### Protocols

|Protocol|Medium|Speed|Deterministic|Application|
|--------|------|-----|-------------|-----------|
|Ethernet/IP|Ethernet|100 Mbps|Yes|Allen-Bradley|
|Profinet|Ethernet|100 Mbps|Yes|Siemens|
|EtherCAT|Ethernet|100 Mbps|Yes|High-speed|
|CAN Bus|Serial|1 Mbps|Yes|Automotive|
|Modbus RS-485|Serial|115 kbps|No|General|
|Profibus|Serial|12 Mbps|Yes|Siemens|

```python
class IndustrialProtocols:
    """Protocol implementations"""
    
    # Modbus RTU frame
    MODBUS_RTU = {
        "function_codes": {
            1: "Read Coils",
            3: "Read Holding Registers",
            6: "Write Single Register",
            16: "Write Multiple Registers"
        }
    }
    
    # CANopen object dictionary
    CANOPEN = {
        "TPDO1": {"COB-ID": 0x200, "transmission": "SYNC"},
        "RPDO1": {"COB-ID": 0x200, "transmission": "ACYCLIC"},
        "TPDO2": {"COB-ID": 0x300, "transmission": "SYNC"},
        "SDO": {"COB-ID": 0x600, "server/client": "requested"}
    }
```

---

## Common Errors to Avoid

1. **Ignoring sensor noise** — Always filter appropriately
2. **Oversimplifying models** — Real systems have nonlinearities
3. **Not considering response time** — Sensor/actuator delays matter
4. **Ignoring electrical noise** — Grounding, shielding critical
5. **Poor PLC program structure** — Use proper organization
6. **Forgetting safety circuits** — Hardwired overrides essential
7. **Not tuning PID** — Wrong gains cause instability
8. **Ignoring thermal effects** — Motors, electronics heat up

