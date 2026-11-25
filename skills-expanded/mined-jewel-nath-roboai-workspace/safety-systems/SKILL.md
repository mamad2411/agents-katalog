---
name: safety-systems
description: Robot safety and security with functional safety (ISO 10218), SROS2, DDS security, E-stops, watchdogs, and risk assessment.
category: architecture
tags: [safety, security, sros2, functional-safety, iso10218, estop, watchdog, risk-assessment]
version: "1.0.0"
---

# Safety Systems

Safety and security for robotic systems. This skill covers functional safety standards, SROS2, E-stops, and risk assessment.

## Security: robot attack surface

Cyber vulnerabilities on robots become physical risks (unauthorized motion, sensor spoofing). Key vectors:

| Vector | Impact |
|--------|--------|
| Unauthenticated `/cmd_vel` | Robot moves unexpectedly — injury or damage |
| Sensor spoofing (`/scan`, `/camera/image`) | Wrong decisions, collisions |
| Open DDS discovery | Full topic graph visible to anyone on the network |
| USB/serial physical access | Root shell, firmware flash |
| Unsigned firmware OTA | Persistent backdoor in motor controllers |

SROS2 adds DDS authentication, encryption, and access control. Use it for production and multi-tenant networks.

## When to Use

- Designing emergency stop systems
- Implementing safety-rated monitored stops
- Configuring SROS2 and DDS security
- Performing risk assessments per ISO 10218
- Implementing safety controllers
- Securing robot communication
- Adding watchdogs and safety monitors

## Quick Start

```bash
# Install SROS2
sudo apt install ros-humble-sros2

# Generate security artifacts
ros2 security create_keystore ~/sros2_keystore
ros2 security create_enclave ~/sros2_keystore /robot/navigation
```

Create one enclave per fully-qualified node name. Set `ROS_SECURITY_KEYSTORE` and `ROS_SECURITY_STRATEGY=Enforce` when launching nodes. Use governance XML to require encryption and authentication; use permissions XML to allow only specific topics/services per enclave.

## Core Concepts

### 1. Emergency Stop Systems

Hardware and software E-stop implementation.

```cpp
// Safety controller with E-stop
class SafetyController {
public:
    enum class SafetyState {
        NORMAL,      // Normal operation
        PROTECTIVE,  // Protective stop (recoverable)
        EMERGENCY    // Emergency stop (requires reset)
    };
    
    SafetyController() : state_(SafetyState::NORMAL) {
        // Configure GPIO for E-stop input
        gpio_export(E_STOP_PIN);
        gpio_set_direction(E_STOP_PIN, "in");
        gpio_set_edge(E_STOP_PIN, "falling");
        
        // Safety-rated output
        gpio_export(SAFETY_OUT_PIN);
        gpio_set_direction(SAFETY_OUT_PIN, "out");
        gpio_set_value(SAFETY_OUT_PIN, 1);  // Enable motion
    }
    
    void update() {
        // Read E-stop (dual channel for safety rating)
        bool estop_ch1 = gpio_get_value(E_STOP_PIN_1);
        bool estop_ch2 = gpio_get_value(E_STOP_PIN_2);
        
        // Both channels must agree
        if (estop_ch1 == 0 && estop_ch2 == 0) {
            trigger_emergency_stop("E-stop pressed");
        } else if (estop_ch1 != estop_ch2) {
            // Fault - channels disagree
            trigger_emergency_stop("E-stop fault");
        }
        
        // Check other safety inputs
        check_joint_limits();
        check_collision_detected();
        check_safety_zone_violation();
        
        // Update safety output
        if (state_ == SafetyState::NORMAL) {
            gpio_set_value(SAFETY_OUT_PIN, 1);
        } else {
            gpio_set_value(SAFETY_OUT_PIN, 0);
            stop_all_motion();
        }
    }
    
    void trigger_emergency_stop(const std::string& reason) {
        if (state_ != SafetyState::EMERGENCY) {
            state_ = SafetyState::EMERGENCY;
            RCLCPP_ERROR(logger_, "EMERGENCY STOP: %s", reason.c_str());
            
            // Immediate hardware stop
            halt_all_actuators();
            
            // Software stop
            publish_safety_state();
        }
    }
    
    bool reset_emergency_stop() {
        // Require manual reset with verification
        if (gpio_get_value(RESET_PIN) == 0) {
            // Check all safety conditions cleared
            if (is_safe_to_reset()) {
                state_ = SafetyState::NORMAL;
                return true;
            }
        }
        return false;
    }

private:
    SafetyState state_;
    rclcpp::Logger logger_ = rclcpp::get_logger("SafetyController");
};
```

### 2. SROS2 Security

Secure ROS2 communication.

```bash
# Create security keystore
ros2 security create_keystore ~/sros2_keystore

# Create keys for nodes
ros2 security create_key ~/sros2_keystore /robot/vision
ros2 security create_key ~/sros2_keystore /robot/navigation
ros2 security create_key ~/sros2_keystore /robot/manipulation

# List keys
ros2 security list_keys ~/sros2_keystore

# Launch with security
ROS_SECURITY_KEYSTORE=~/sros2_keystore \
ROS_SECURITY_ENABLE=true \
ROS_SECURITY_STRATEGY=Enforce \
ros2 launch robot_bringup secure_launch.py
```

```xml
<!-- secure_launch.xml -->
<launch>
  <env name="ROS_SECURITY_KEYSTORE" value="$(env HOME)/sros2_keystore"/>
  <env name="ROS_SECURITY_ENABLE" value="true"/>
  
  <node pkg="vision" exec="camera_node" 
        security="enable"
        enclave="/robot/vision"/>
  
  <node pkg="nav2" exec="navigation_node"
        security="enable"
        enclave="/robot/navigation"/>
</launch>
```

### 3. Watchdogs

Hardware and software watchdogs prevent runaway conditions.

```cpp
#include <linux/watchdog.h>

class WatchdogManager {
public:
    WatchdogManager() {
        // Open hardware watchdog
        fd_ = open("/dev/watchdog", O_RDWR);
        if (fd_ < 0) {
            throw std::runtime_error("Failed to open watchdog");
        }
        
        // Set timeout (seconds)
        int timeout = 5;
        ioctl(fd_, WDIOC_SETTIMEOUT, &timeout);
        
        // Start watchdog thread
        running_ = true;
        watchdog_thread_ = std::thread(&WatchdogManager::watchdog_loop, this);
    }
    
    void pet_watchdog() {
        std::lock_guard<std::mutex> lock(mutex_);
        last_pet_time_ = std::chrono::steady_clock::now();
    }
    
    void register_monitor(const std::string& name, 
                         std::function<bool()> health_check) {
        monitors_[name] = health_check;
    }

private:
    void watchdog_loop() {
        while (running_) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            
            // Check all monitors
            bool all_healthy = true;
            for (const auto& [name, check] : monitors_) {
                if (!check()) {
                    RCLCPP_ERROR(logger_, "Health check failed: %s", name.c_str());
                    all_healthy = false;
                }
            }
            
            // Check timeout
            auto elapsed = std::chrono::steady_clock::now() - last_pet_time_;
            if (elapsed > std::chrono::seconds(3)) {
                RCLCPP_ERROR(logger_, "Watchdog timeout - system will reset");
                // Don't pet - let watchdog trigger
                return;
            }
            
            if (all_healthy) {
                // Pet hardware watchdog
                ioctl(fd_, WDIOC_KEEPALIVE, 0);
            }
        }
    }
    
    int fd_;
    std::atomic<bool> running_;
    std::thread watchdog_thread_;
    std::mutex mutex_;
    std::chrono::steady_clock::time_point last_pet_time_;
    std::map<std::string, std::function<bool()>> monitors_;
    rclcpp::Logger logger_ = rclcpp::get_logger("Watchdog");
};
```

### 4. Risk Assessment

ISO 10218 compliant risk assessment.

```python
class RiskAssessment:
    def __init__(self):
        self.hazards = []
        self.risk_matrix = {
            'severity': {'negligible': 1, 'minor': 2, 'major': 3, 'critical': 4},
            'probability': {'unlikely': 1, 'possible': 2, 'likely': 3, 'frequent': 4}
        }
    
    def identify_hazards(self, robot_system):
        """Identify hazards per ISO 10218."""
        hazards = [
            {
                'id': 'H001',
                'description': 'Unexpected robot motion',
                'source': 'Control system fault',
                'severity': 'critical',
                'probability': 'unlikely',
                'mitigations': ['E-stop', 'Safety limits', 'Redundant sensors']
            },
            {
                'id': 'H002',
                'description': 'Collision with operator',
                'source': 'Presence in workspace',
                'severity': 'major',
                'probability': 'possible',
                'mitigations': ['Safety scanner', 'Light curtain', 'Reduced speed']
            },
            # ... more hazards
        ]
        return hazards
    
    def calculate_risk_level(self, severity, probability):
        """Calculate risk level from severity and probability."""
        s = self.risk_matrix['severity'][severity]
        p = self.risk_matrix['probability'][probability]
        risk = s * p
        
        if risk <= 4:
            return 'low'
        elif risk <= 8:
            return 'medium'
        elif risk <= 12:
            return 'high'
        else:
            return 'unacceptable'
    
    def generate_report(self):
        """Generate risk assessment report."""
        report = {
            'standards': ['ISO 10218-1', 'ISO 10218-2', 'ISO/TS 15066'],
            'hazards': self.hazards,
            'residual_risks': [],
            'mitigation_status': {}
        }
        
        for hazard in self.hazards:
            risk = self.calculate_risk_level(
                hazard['severity'], 
                hazard['probability']
            )
            hazard['risk_level'] = risk
            
            if risk in ['high', 'unacceptable']:
                report['residual_risks'].append(hazard)
        
        return report
```

## Configuration Reference

| Safety Level | Stop Category | Performance Level | Use Case |
|--------------|---------------|-------------------|----------|
| Emergency | 0 (uncontrolled) | PL e | Life-threatening |
| Protective | 1 (controlled) | PL d | Collision risk |
| Operational | 2 (soft) | PL c | Normal limits |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| False E-stops | EMI on E-stop line | Shield cables, use filtered inputs |
| Watchdog reset | Task taking too long | Increase timeout, optimize code |
| SROS2 fails | Certificate expired | Regenerate keys, check permissions |

## Common Patterns

### Watchdog Timer Pattern

A software watchdog that monitors a set of named subsystems. Each subsystem must call `pet()` within its deadline or the watchdog triggers a safe shutdown.

```python
import threading
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SoftwareWatchdog:
    """Per-subsystem software watchdog with configurable deadlines.

    Each registered subsystem must call pet() within its deadline_sec.
    If any deadline is missed the on_timeout callback fires immediately.

    Args:
        on_timeout: callable(subsystem_name) invoked on first timeout
    """

    def __init__(self, on_timeout):
        self._on_timeout = on_timeout
        self._monitors: dict[str, dict] = {}  # name -> {deadline, last_pet}
        self._lock = threading.Lock()
        self._running = False
        self._thread: threading.Thread | None = None

    def register(self, name: str, deadline_sec: float) -> None:
        """Register a new subsystem with the given deadline."""
        with self._lock:
            self._monitors[name] = {
                "deadline": deadline_sec,
                "last_pet": time.monotonic(),
            }

    def pet(self, name: str) -> None:
        """Reset the deadline for a subsystem. Call this from your control loop."""
        with self._lock:
            if name in self._monitors:
                self._monitors[name]["last_pet"] = time.monotonic()

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _loop(self) -> None:
        while self._running:
            now = time.monotonic()
            with self._lock:
                for name, info in self._monitors.items():
                    elapsed = now - info["last_pet"]
                    if elapsed > info["deadline"]:
                        # Fire callback outside the lock to avoid deadlock
                        threading.Thread(
                            target=self._on_timeout, args=(name,), daemon=True
                        ).start()
            time.sleep(0.05)  # Check at 20 Hz


class WatchdogNode(Node):
    """ROS 2 node that integrates SoftwareWatchdog with diagnostics."""

    def __init__(self):
        super().__init__("watchdog_node")

        self._watchdog = SoftwareWatchdog(self._handle_timeout)
        # cmd_vel must arrive within 500 ms
        self._watchdog.register("cmd_vel", deadline_sec=0.5)
        # Hardware heartbeat must arrive within 1 s
        self._watchdog.register("hardware_heartbeat", deadline_sec=1.0)
        self._watchdog.start()

        self._cmd_sub = self.create_subscription(
            String, "/cmd_vel_raw", self._cmd_cb, 10
        )
        self._heartbeat_sub = self.create_subscription(
            String, "/hardware/heartbeat", self._heartbeat_cb, 10
        )

        self._estop_pub = self.create_publisher(String, "/safety/estop", 10)
        self.get_logger().info("WatchdogNode ready")

    def _cmd_cb(self, _msg) -> None:
        self._watchdog.pet("cmd_vel")

    def _heartbeat_cb(self, _msg) -> None:
        self._watchdog.pet("hardware_heartbeat")

    def _handle_timeout(self, name: str) -> None:
        self.get_logger().error(f"Watchdog timeout: {name} — triggering e-stop")
        msg = String()
        msg.data = f"TIMEOUT:{name}"
        self._estop_pub.publish(msg)
```

---

### Safe Mode FSM

A finite-state machine with five safety states. Transitions are one-way toward safety; recovery requires explicit operator action.

```python
from enum import Enum, auto
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SafetyState(Enum):
    INIT = auto()         # Startup — no motion allowed
    OPERATIONAL = auto()  # Normal robot operation
    REDUCED = auto()      # Speed/workspace restricted (e.g. human detected)
    SAFE_STOP = auto()    # Controlled deceleration to zero velocity
    EMERGENCY = auto()    # Uncontrolled stop — requires operator reset


# Allowed transitions: source -> set of valid destinations
_TRANSITIONS: dict[SafetyState, set[SafetyState]] = {
    SafetyState.INIT:        {SafetyState.OPERATIONAL},
    SafetyState.OPERATIONAL: {SafetyState.REDUCED, SafetyState.SAFE_STOP, SafetyState.EMERGENCY},
    SafetyState.REDUCED:     {SafetyState.OPERATIONAL, SafetyState.SAFE_STOP, SafetyState.EMERGENCY},
    SafetyState.SAFE_STOP:   {SafetyState.OPERATIONAL, SafetyState.EMERGENCY},
    SafetyState.EMERGENCY:   set(),  # No automatic recovery
}


class SafetyFSM(Node):
    """Safety state machine node.

    Publishes current state on /safety/state every 100 ms and
    accepts transition commands on /safety/command.
    """

    def __init__(self):
        super().__init__("safety_fsm")
        self._state = SafetyState.INIT

        self._state_pub = self.create_publisher(String, "/safety/state", 10)
        self._cmd_sub = self.create_subscription(
            String, "/safety/command", self._on_command, 10
        )
        self._timer = self.create_timer(0.1, self._publish_state)
        self.get_logger().info("SafetyFSM initialised in INIT state")

    # ------------------------------------------------------------------
    def transition(self, target: SafetyState, reason: str = "") -> bool:
        """Attempt a state transition. Returns True on success."""
        if target not in _TRANSITIONS[self._state]:
            self.get_logger().warning(
                f"Illegal transition {self._state.name} → {target.name} ignored"
            )
            return False
        self.get_logger().info(
            f"Safety state: {self._state.name} → {target.name}  reason='{reason}'"
        )
        self._state = target
        self._publish_state()
        self._on_state_entry(target)
        return True

    def request_emergency_stop(self, reason: str = "unknown") -> None:
        """Unconditional emergency stop — bypasses normal transition guard."""
        if self._state is not SafetyState.EMERGENCY:
            self.get_logger().fatal(f"EMERGENCY STOP requested: {reason}")
            self._state = SafetyState.EMERGENCY
            self._on_state_entry(SafetyState.EMERGENCY)
            self._publish_state()

    # ------------------------------------------------------------------
    def _on_state_entry(self, state: SafetyState) -> None:
        """Side-effects executed when entering a state."""
        if state == SafetyState.EMERGENCY:
            self._halt_all_actuators()
        elif state == SafetyState.SAFE_STOP:
            self._begin_controlled_deceleration()
        elif state == SafetyState.REDUCED:
            self._apply_speed_limits(max_linear=0.3, max_angular=0.5)

    def _halt_all_actuators(self) -> None:
        self.get_logger().error("Halting all actuators immediately")
        # Publish zero cmd_vel; motor driver also reads safety GPIO
        from geometry_msgs.msg import Twist
        zero = Twist()
        pub = self.create_publisher(Twist, "/cmd_vel", 1)
        pub.publish(zero)

    def _begin_controlled_deceleration(self) -> None:
        self.get_logger().warning("Beginning controlled deceleration")

    def _apply_speed_limits(self, max_linear: float, max_angular: float) -> None:
        self.get_logger().warning(
            f"Reduced mode: vmax={max_linear} m/s  ωmax={max_angular} rad/s"
        )

    # ------------------------------------------------------------------
    def _on_command(self, msg: String) -> None:
        cmd = msg.data.upper()
        mapping = {
            "OPERATIONAL": SafetyState.OPERATIONAL,
            "REDUCED":     SafetyState.REDUCED,
            "SAFE_STOP":   SafetyState.SAFE_STOP,
            "EMERGENCY":   SafetyState.EMERGENCY,
        }
        if cmd in mapping:
            self.transition(mapping[cmd], reason="operator command")
        else:
            self.get_logger().warning(f"Unknown safety command: {msg.data}")

    def _publish_state(self) -> None:
        msg = String()
        msg.data = self._state.name
        self._state_pub.publish(msg)
```

---

### E-Stop Chain Implementation

A ROS 2 node that reads a dual-channel hardware e-stop and propagates it through the software stack. This implements a Category 0 stop (power removal) for the emergency state and a Category 1 stop (controlled deceleration) for the protective state.

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from std_msgs.msg import Bool, String
import RPi.GPIO as GPIO


# GPIO pin numbers (BCM numbering)
ESTOP_CH1_PIN = 17  # Normally-closed, pulled high
ESTOP_CH2_PIN = 27  # Redundant second channel
RESET_BTN_PIN = 22  # Momentary reset button
SAFETY_OUT_PIN = 23  # Drives safety relay (LOW = motors off)


class EStopChain(Node):
    """Hardware e-stop chain with dual-channel monitoring.

    Publishes /safety/estop_active (latched) so that any subscriber
    can react to the stop. The chain is only cleared by a deliberate
    RESET after both hardware channels read safe.
    """

    def __init__(self):
        super().__init__("estop_chain")

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ESTOP_CH1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(ESTOP_CH2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RESET_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SAFETY_OUT_PIN, GPIO.OUT, initial=GPIO.HIGH)  # relay energised = safe

        # Latched QoS — subscribers always receive the last state
        latched_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            depth=1,
        )
        self._estop_pub = self.create_publisher(Bool, "/safety/estop_active", latched_qos)
        self._reason_pub = self.create_publisher(String, "/safety/estop_reason", latched_qos)

        self._active = False
        self._reason = ""

        # Poll GPIO at 200 Hz — fast enough for human response
        self.create_timer(0.005, self._poll)
        self.get_logger().info("EStopChain ready (dual-channel monitoring)")

    def _poll(self) -> None:
        ch1 = GPIO.input(ESTOP_CH1_PIN)  # 0 = pressed (NC contact opened)
        ch2 = GPIO.input(ESTOP_CH2_PIN)

        if not ch1 and not ch2:
            self._trigger("E-stop button pressed")
        elif ch1 != ch2:
            # Channel discrepancy — wiring fault or single-channel failure
            self._trigger(f"E-stop channel mismatch CH1={ch1} CH2={ch2}")
        elif self._active:
            # Check for manual reset
            reset_pressed = not GPIO.input(RESET_BTN_PIN)
            if reset_pressed and self._channels_clear():
                self._clear_estop()

    def _trigger(self, reason: str) -> None:
        if not self._active:
            self._active = True
            self._reason = reason
            GPIO.output(SAFETY_OUT_PIN, GPIO.LOW)  # De-energise relay — motors off
            self.get_logger().fatal(f"E-STOP TRIGGERED: {reason}")
        self._publish()

    def _clear_estop(self) -> None:
        self._active = False
        self._reason = ""
        GPIO.output(SAFETY_OUT_PIN, GPIO.HIGH)
        self.get_logger().info("E-stop cleared — motion permitted")
        self._publish()

    def _channels_clear(self) -> bool:
        return bool(GPIO.input(ESTOP_CH1_PIN) and GPIO.input(ESTOP_CH2_PIN))

    def _publish(self) -> None:
        self._estop_pub.publish(Bool(data=self._active))
        self._reason_pub.publish(String(data=self._reason))

    def destroy_node(self) -> None:
        GPIO.cleanup()
        super().destroy_node()
```

---

### Heartbeat Monitoring

Monitor that multiple safety-critical nodes are alive and publishing. If a node stops heartbeating, the monitor escalates to a safe stop.

```python
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool


class HeartbeatMonitor(Node):
    """Monitors heartbeat topics from safety-critical nodes.

    Each monitored node must publish a std_msgs/String to
    /heartbeat/<node_name> at its declared rate. If the interval
    between beats exceeds deadline_sec the monitor calls for a safe stop.

    Usage
    -----
    monitor = HeartbeatMonitor()
    monitor.register("hardware_node",   topic="/heartbeat/hardware_node",   deadline_sec=0.2)
    monitor.register("navigation_node", topic="/heartbeat/navigation_node", deadline_sec=1.0)
    rclpy.spin(monitor)
    """

    def __init__(self):
        super().__init__("heartbeat_monitor")
        self._nodes: dict[str, dict] = {}
        self._safe_stop_pub = self.create_publisher(Bool, "/safety/request_safe_stop", 10)
        # Check deadlines at 50 Hz
        self.create_timer(0.02, self._check_deadlines)

    def register(self, name: str, topic: str, deadline_sec: float) -> None:
        self._nodes[name] = {
            "deadline": deadline_sec,
            "last_beat": time.monotonic(),
            "missed_count": 0,
            "sub": self.create_subscription(
                String, topic,
                lambda msg, n=name: self._beat(n),
                10,
            ),
        }
        self.get_logger().info(f"Monitoring heartbeat: {name} on {topic} ({deadline_sec}s deadline)")

    def _beat(self, name: str) -> None:
        if name in self._nodes:
            self._nodes[name]["last_beat"] = time.monotonic()
            self._nodes[name]["missed_count"] = 0

    def _check_deadlines(self) -> None:
        now = time.monotonic()
        for name, info in self._nodes.items():
            elapsed = now - info["last_beat"]
            if elapsed > info["deadline"]:
                info["missed_count"] += 1
                self.get_logger().warning(
                    f"Heartbeat missed: {name} ({elapsed:.2f}s > {info['deadline']}s)"
                    f" — miss #{info['missed_count']}"
                )
                if info["missed_count"] >= 3:
                    self.get_logger().error(f"Node {name} presumed dead — requesting safe stop")
                    self._safe_stop_pub.publish(Bool(data=True))
```

---

### Fault Isolation

Decorator and context manager that catch subsystem exceptions and degrade gracefully rather than crashing the whole process.

```python
import functools
import traceback
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def fault_isolated(fallback=None, publish_fault: bool = True):
    """Decorator that isolates faults in ROS 2 callbacks.

    Args:
        fallback: value to return when an exception is caught (default None)
        publish_fault: if True, publishes fault info to /safety/faults

    Usage
    -----
    class MyNode(Node):
        @fault_isolated(fallback=None, publish_fault=True)
        def _lidar_cb(self, msg):
            # Exception here will not crash the node
            process_scan(msg)
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except Exception as exc:
                tb = traceback.format_exc()
                logger = getattr(self, "get_logger", lambda: None)()
                if logger:
                    logger.error(f"Fault in {fn.__name__}: {exc}\n{tb}")
                if publish_fault and hasattr(self, "_fault_pub"):
                    msg = String()
                    msg.data = f"{fn.__name__}:{type(exc).__name__}:{exc}"
                    self._fault_pub.publish(msg)
                return fallback
        return wrapper
    return decorator


class FaultIsolatedNode(Node):
    """Base class providing fault isolation infrastructure."""

    def __init__(self, node_name: str):
        super().__init__(node_name)
        self._fault_pub = self.create_publisher(String, "/safety/faults", 10)
        self._fault_count: dict[str, int] = {}

    def record_fault(self, subsystem: str) -> int:
        """Record a fault and return the cumulative count for that subsystem."""
        self._fault_count[subsystem] = self._fault_count.get(subsystem, 0) + 1
        count = self._fault_count[subsystem]
        if count >= 5:
            self.get_logger().error(
                f"Subsystem '{subsystem}' has faulted {count} times — consider disabling it"
            )
        return count
```

---

## Anti-Patterns

### ❌ No timeout on e-stop subscriber

```python
# WRONG: if /safety/estop topic stops arriving, the robot keeps moving
class MotorDriver(Node):
    def __init__(self):
        self.estop_active = False
        self.create_subscription(Bool, "/safety/estop_active", self._estop_cb, 10)

    def _estop_cb(self, msg):
        self.estop_active = msg.data

    def _control_loop(self):
        if not self.estop_active:
            self._send_velocity_command()  # Runs even if topic dies!
```

### ✅ Use a latched subscription with a deadline watchdog

```python
class MotorDriver(Node):
    """If the e-stop topic goes silent for more than 200 ms, treat it as active."""

    ESTOP_DEADLINE_SEC = 0.2

    def __init__(self):
        super().__init__("motor_driver")
        self._estop_active = True          # Fail-safe: assume stopped until confirmed safe
        self._last_estop_msg = 0.0

        latched_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            depth=1,
        )
        self.create_subscription(Bool, "/safety/estop_active", self._estop_cb, latched_qos)
        self.create_timer(0.05, self._control_loop)  # 20 Hz

    def _estop_cb(self, msg: Bool) -> None:
        self._estop_active = msg.data
        self._last_estop_msg = self.get_clock().now().nanoseconds * 1e-9

    def _control_loop(self) -> None:
        now = self.get_clock().now().nanoseconds * 1e-9
        topic_stale = (now - self._last_estop_msg) > self.ESTOP_DEADLINE_SEC
        if self._estop_active or topic_stale:
            self._send_zero_velocity()
        else:
            self._send_velocity_command()

    def _send_zero_velocity(self) -> None:
        from geometry_msgs.msg import Twist
        self.create_publisher(Twist, "/cmd_vel", 1).publish(Twist())

    def _send_velocity_command(self) -> None:
        pass  # Normal motion control
```

---

### ❌ Single point of failure in the safety chain

```python
# WRONG: one node checks collision AND publishes e-stop AND drives motors
# If this process crashes, nothing stops the robot
class AllInOneSafetyNode(Node):
    def __init__(self):
        self._collision_sub = self.create_subscription(...)
        self._motor_pub = self.create_publisher(...)

    def _collision_cb(self, msg):
        if msg.data:
            self._motor_pub.publish(zero_twist)  # Single point of failure
```

### ✅ Separate safety monitor, e-stop chain, and motor driver processes

```python
# CORRECT: three independent processes with a hardware relay as the final backstop
#
# Process 1 — safety_monitor:   reads sensors, publishes /safety/estop_active
# Process 2 — estop_chain:      reads hardware GPIO + /safety/estop_active,
#                                drives safety relay GPIO
# Process 3 — motor_driver:     reads /cmd_vel, checks /safety/estop_active
#                                before forwarding to firmware
#
# Hardware relay provides a physical backstop if all three processes crash.
# Each process is launched as a separate OS process via a launch file:

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package="orbibot_safety", executable="safety_monitor",
             respawn=True, respawn_delay=0.5),
        Node(package="orbibot_safety", executable="estop_chain",
             respawn=True, respawn_delay=0.5),
        Node(package="orbibot_hardware", executable="motor_driver",
             respawn=True, respawn_delay=0.5),
    ])
```

---

### ❌ Blocking operations inside a safety callback

```python
# WRONG: a slow ROS service call inside the e-stop callback delays
# the callback thread and can cause missed messages
class UnsafeNode(Node):
    def _estop_cb(self, msg):
        if msg.data:
            # Service call can block for seconds — NEVER do this in a safety callback
            future = self._log_client.call_async(LogRequest(reason="estop"))
            rclpy.spin_until_future_complete(self, future)   # BLOCKS
            self._halt_motors()
```

### ✅ Do the minimum in the callback; delegate slow work to a separate thread

```python
import queue
import threading

class SafeNode(Node):
    def __init__(self):
        super().__init__("safe_node")
        self._work_queue: queue.Queue = queue.Queue()
        self._worker = threading.Thread(target=self._background_worker, daemon=True)
        self._worker.start()

    def _estop_cb(self, msg: Bool) -> None:
        if msg.data:
            self._halt_motors()                     # Immediate — no blocking I/O
            self._work_queue.put(("log_estop", {})) # Delegate logging to worker

    def _halt_motors(self) -> None:
        from geometry_msgs.msg import Twist
        self.create_publisher(Twist, "/cmd_vel", 1).publish(Twist())

    def _background_worker(self) -> None:
        while True:
            task, kwargs = self._work_queue.get()
            if task == "log_estop":
                # Slow service call is fine here — not on the callback thread
                self._call_log_service()
```

---

### ❌ Ignoring sensor fault flags

```python
# WRONG: LiDAR scan is used even if the driver reports a hardware error
def _scan_cb(self, msg: LaserScan) -> None:
    distances = [r for r in msg.ranges if not math.isnan(r)]
    self._update_costmap(distances)  # Uses bad data if sensor is failing
```

### ✅ Check sensor status before using data

```python
from diagnostic_msgs.msg import DiagnosticArray

class SafeSensorNode(Node):
    def __init__(self):
        super().__init__("safe_sensor")
        self._lidar_healthy = False
        self.create_subscription(
            DiagnosticArray, "/diagnostics", self._diag_cb, 10
        )
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)

    def _diag_cb(self, msg: DiagnosticArray) -> None:
        for status in msg.status:
            if "rplidar" in status.name.lower():
                # DiagnosticStatus.OK == 0
                self._lidar_healthy = status.level == 0

    def _scan_cb(self, msg: LaserScan) -> None:
        if not self._lidar_healthy:
            self.get_logger().warning("Ignoring scan: LiDAR reports unhealthy", throttle_duration_sec=5.0)
            return
        distances = [r for r in msg.ranges if math.isfinite(r)]
        self._update_costmap(distances)
```

---

### ❌ Resetting emergency stop automatically

```python
# WRONG: auto-reset after a timeout re-enables motion without operator confirmation
def _estop_cb(self, msg):
    if msg.data:
        self._estop_active = True
        self.create_timer(5.0, lambda: setattr(self, "_estop_active", False))  # BAD
```

### ✅ Always require an explicit operator reset

```python
class SafeMotorController(Node):
    """E-stop can only be cleared by a deliberate service call from the operator."""

    def __init__(self):
        super().__init__("safe_motor_controller")
        self._estop_active = False
        self.create_subscription(Bool, "/safety/estop_active", self._estop_cb, 10)
        self.create_service(
            std_srvs.srv.Trigger, "/safety/reset_estop", self._reset_cb
        )

    def _estop_cb(self, msg: Bool) -> None:
        if msg.data and not self._estop_active:
            self._estop_active = True
            self.get_logger().fatal("E-stop latched — operator must call /safety/reset_estop")

    def _reset_cb(self, _req, response):
        if self._estop_active:
            # Verify hardware channel is clear before allowing reset
            if self._hardware_channels_clear():
                self._estop_active = False
                response.success = True
                response.message = "E-stop cleared"
            else:
                response.success = False
                response.message = "Hardware e-stop still active — cannot reset"
        else:
            response.success = True
            response.message = "No active e-stop"
        return response

    def _hardware_channels_clear(self) -> bool:
        # Read GPIO or query hardware driver
        return True  # Replace with actual GPIO read
```

---

## Configuration Reference

### Safety Level vs. Stop Category

| Safety Level | Stop Category (IEC 60204) | Performance Level (ISO 13849) | Typical Use Case |
|---|---|---|---|
| Emergency | 0 — uncontrolled, immediate power removal | PL e (SIL 3) | Life-threatening hazard |
| Protective | 1 — controlled deceleration to zero, then power removal | PL d (SIL 2) | Collision risk, proximity |
| Operational limit | 2 — controlled deceleration, power maintained | PL c (SIL 1) | Speed/workspace limits |

### Watchdog Parameters

| Parameter | Type | Recommended | Description |
|---|---|---|---|
| `cmd_vel_deadline_sec` | float | 0.5 | Max interval between `/cmd_vel` messages before safe stop |
| `heartbeat_deadline_sec` | float | 1.0 | Max interval for node heartbeat topics |
| `hardware_deadline_sec` | float | 0.2 | Max interval for firmware heartbeat |
| `hw_watchdog_timeout_sec` | int | 5 | Linux `/dev/watchdog` hardware timeout |
| `estop_poll_hz` | float | 200 | GPIO polling rate for hardware e-stop |
| `health_check_hz` | float | 20 | Rate at which watchdog checks all monitors |

### SROS2 Security Parameters

| Parameter | Values | Description |
|---|---|---|
| `ROS_SECURITY_ENABLE` | `true` / `false` | Enable DDS security |
| `ROS_SECURITY_STRATEGY` | `Enforce` / `Permissive` | `Enforce` refuses unsigned nodes |
| `ROS_SECURITY_KEYSTORE` | path | Path to the keystore directory |
| `ROS_SECURITY_ENCLAVE_SEARCH_PATHS` | path | Override enclave discovery path |
| `governance.xml` — `rtps_protection_kind` | `ENCRYPT` / `SIGN` / `NONE` | Wire-level protection |

### Safe-Mode Speed Limits

| Mode | Max Linear (m/s) | Max Angular (rad/s) | Trigger |
|---|---|---|---|
| OPERATIONAL | 1.0 | 2.0 | Normal operation |
| REDUCED | 0.3 | 0.5 | Human in zone / low battery |
| SAFE_STOP | 0.0 | 0.0 | E-stop or watchdog timeout |
| EMERGENCY | 0.0 | 0.0 | Hardware e-stop, fault |

---

## Troubleshooting

| Symptom | Cause | Solution |
|---|---|---|
| False e-stop triggers intermittently | EMI on normally-closed e-stop cable | Use shielded cable, add 10 nF filter capacitor on GPIO input, increase software debounce to 3 consecutive samples |
| Linux hardware watchdog resets the system unexpectedly | Main control loop blocked by a ROS spin that takes >3 s (log write, heavy computation) | Move slow work to a background thread; increase `/dev/watchdog` timeout with `WDIOC_SETTIMEOUT`; confirm `watchdog_thread_` is petting within deadline |
| Safety state transitions to EMERGENCY on every startup | `_estop_active` initialised to `True` but the latched `/safety/estop_active` topic has not yet delivered its first message | Add a startup delay or check that the e-stop node starts before the motor driver; alternatively, subscribe with `TRANSIENT_LOCAL` durability so the last value is replayed |
| SROS2 nodes refuse to communicate after key rotation | Old DDS participant cache still holds expired certificates | Restart all DDS participants (kill and relaunch all nodes); set `CYCLONEDDS_URI` to clear discovery cache |
| Watchdog `pet()` call has no effect — node resets anyway | `pet()` is called from a ROS callback, but the executor is blocked by a slow subscriber on the same thread | Use `MultiThreadedExecutor` with separate `MutuallyExclusiveCallbackGroup` for the watchdog pet call and the slow callback |
| E-stop channel discrepancy detected (CH1 ≠ CH2) on every boot | Wiring fault: one channel is not connected or pull-up resistor is missing | Measure both GPIO pins with a multimeter; verify normally-closed contact wiring and matching pull-up resistors on both channels |
| Safety relay de-energises correctly but motors do not stop | Motor driver firmware ignores `/cmd_vel` of zeros; firmware watchdog also times out | Check that firmware PID output is gated by the relay (hardware-level cut); verify `cmd_timeout` parameter in `hardware_params.yaml` |
| HeartbeatMonitor fires after a system sleep/resume | Monotonic clock does not stop during suspend; `last_beat` timestamp becomes very stale | Reset `last_beat` to `time.monotonic()` on wake-up; subscribe to `/system/wake` event from systemd via a ROS topic bridge |

---

## Workflow Integration

This skill sits at the intersection of hardware control and software architecture. Use it together with the following skills:

- **`robot-bringup`** — configure `systemd` service restart policies for safety-critical nodes (`Restart=always`, `RestartSec=0.5`); the e-stop chain node and hardware watchdog must start before any motion-capable node.
- **`deployment-fleet`** — publish `DiagnosticStatus` from the `SafetyFSM` and `HeartbeatMonitor` so that the robot dashboard shows safety state in real time; use `diagnostic_updater.Updater` to report per-channel e-stop status.
- **SROS2, above** — apply SROS2 enclaves to the safety topic namespace (`/safety/*`); set `governance.xml` to `ENCRYPT` for `/safety/estop_active` and `/cmd_vel` so these cannot be spoofed over the network.
- **`realtime_motor_control`** — run the e-stop GPIO polling loop under `SCHED_FIFO` (PREEMPT_RT) to guarantee sub-millisecond response time; pin the watchdog thread to an isolated CPU core to prevent scheduler jitter.
- **`ros2_lifecycle`** — model the motor driver as a Lifecycle Node; on `on_deactivate()` publish zero velocity and de-energise the safety relay; reject `on_activate()` if the SafetyFSM is not in `OPERATIONAL` state.
- **`microcontrollers`** — implement a firmware-level watchdog in the STM32 (`IWDG`) that cuts PWM output if the host fails to send a keep-alive byte within 500 ms; this provides a hardware backstop independent of the Linux OS.

### Typical Integration Sequence

```
1. robot-bringup launches safety_monitor and estop_chain first (ordered startup).
2. SafetyFSM initialises in INIT state — no motion commands forwarded.
3. robot-bringup waits for /safety/state == "OPERATIONAL" before launching nav stack.
4. HeartbeatMonitor confirms hardware_node and navigation_node are alive.
5. Operator confirms workspace clear, sends /safety/command = "OPERATIONAL".
6. Normal operation. Watchdog pets firmware IWDG every 200 ms.
7. On fault: SafetyFSM → SAFE_STOP → EMERGENCY; estop_chain de-energises relay.
8. Operator inspects, clears fault, calls /safety/reset_estop service.
9. SafetyFSM → OPERATIONAL after hardware channels confirm clear.
```

---

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering E-stops, SROS2, watchdogs, risk assessment