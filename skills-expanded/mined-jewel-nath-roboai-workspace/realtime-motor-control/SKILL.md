---
name: realtime-motor-control
description: Real-time motor control with PID tuning, FOC, encoder feedback, PREEMPT_RT Linux, and deterministic control loops for robotics.
category: control
tags: [motor-control, pid, foc, encoder, realtime, preempt-rt, bldc, pmsm, stepper]
version: "1.0.0"
---

# Real-Time Motor Control

Real-time motor control ensures deterministic response for robotic actuators. This skill covers control algorithms, real-time kernels, and hardware interfaces.

## When to Use

- Implementing PID controllers for position/velocity/torque
- Setting up Field-Oriented Control (FOC) for BLDC/PMSM motors
- Configuring encoder feedback and Hall sensors
- Implementing trapezoidal and S-curve motion profiles
- Setting up PREEMPT_RT Linux for real-time control
- Tuning control loops for stability and performance
- Implementing current sensing and protection
- Designing multi-axis synchronized motion

## Quick Start

```bash
# Install motor control libraries
sudo apt install ros-humble-ros2-control ros-humble-joint-trajectory-controller

# For PREEMPT_RT kernel
sudo apt install linux-image-rt

# Install STM32 motor control SDK
# Download from https://www.st.com/en/embedded-software/stsw-stm32100.html

# Build simple motor controller
git clone https://github.com/simplefoc/Arduino-FOC.git
```

## Core Concepts

### 1. Motor Types and Control Methods

Different motors require different control strategies.

| Motor Type | Control Method | Typical Use | Complexity |
|------------|---------------|-------------|------------|
| Brushed DC | PWM duty cycle | Low-cost drives | Low |
| BLDC | Six-step, FOC | Drones, RC | Medium-High |
| PMSM | FOC | Servos, EVs | High |
| Stepper | Step/dir, FOC | 3D printers, CNC | Low-Medium |
| AC Induction | V/f, FOC | Industrial | High |

**Control hierarchy:**

```
Position Loop (50-100 Hz)
    |
    v
Velocity Loop (500-1000 Hz)
    |
    v
Current/Torque Loop (10-20 kHz)
    |
    v
PWM Generation (10-50 kHz)
```

### 2. PID Controller Implementation

Proper PID implementation with anti-windup and filtering.

```cpp
#include <cmath>

class PIDController {
public:
    struct Config {
        float kp = 0.0f;
        float ki = 0.0f;
        float kd = 0.0f;
        float output_min = -1.0f;
        float output_max = 1.0f;
        float integral_limit = 1.0f;
        float derivative_filter = 0.1f;  // 0-1, lower = more filtering
    };
    
    PIDController(const Config& config) : config_(config) {}
    
    float update(float setpoint, float measurement, float dt) {
        float error = setpoint - measurement;
        
        // Proportional term
        float p_term = config_.kp * error;
        
        // Integral term with anti-windup
        integral_ += error * dt;
        integral_ = clamp(integral_, -config_.integral_limit, config_.integral_limit);
        float i_term = config_.ki * integral_;
        
        // Derivative term with filtering
        float derivative = (error - prev_error_) / dt;
        filtered_derivative_ = filtered_derivative_ * (1.0f - config_.derivative_filter) 
                              + derivative * config_.derivative_filter;
        float d_term = config_.kd * filtered_derivative_;
        
        prev_error_ = error;
        
        // Compute output
        float output = p_term + i_term + d_term;
        output = clamp(output, config_.output_min, config_.output_max);
        
        // Conditional integration (anti-windup)
        if (output != p_term + i_term + d_term) {
            integral_ -= error * dt;  // Don't integrate if saturated
        }
        
        return output;
    }
    
    void reset() {
        integral_ = 0.0f;
        prev_error_ = 0.0f;
        filtered_derivative_ = 0.0f;
    }
    
    void setGains(float kp, float ki, float kd) {
        config_.kp = kp;
        config_.ki = ki;
        config_.kd = kd;
    }

private:
    Config config_;
    float integral_ = 0.0f;
    float prev_error_ = 0.0f;
    float filtered_derivative_ = 0.0f;
    
    static float clamp(float val, float min, float max) {
        return std::max(min, std::min(max, val));
    }
};
```

**PID tuning methods:**

```cpp
class PIDTuner {
public:
    // Ziegler-Nichols method
    static void zieglerNichols(float ku, float tu, float& kp, float& ki, float& kd) {
        // Classic ZN
        kp = 0.6f * ku;
        ki = 2.0f * kp / tu;
        kd = kp * tu / 8.0f;
        
        // Or for no overshoot
        // kp = 0.2f * ku;
        // ki = 2.0f * kp / tu;
        // kd = kp * tu / 3.0f;
    }
    
    // Cohen-Coon method (better for lag-dominant systems)
    static void cohenCoon(float K, float tau, float theta, 
                          float& kp, float& ki, float& kd) {
        kp = (1.35 / K) * (tau / theta + 0.185);
        float ti = 2.5f * theta * (tau + 0.185f * theta) / (tau + 0.611f * theta);
        float td = 0.37f * theta * tau / (tau + 0.2f * theta);
        
        ki = kp / ti;
        kd = kp * td;
    }
    
    // Manual tuning procedure
    static void manualTune(PIDController& pid, float& kp, float& ki, float& kd) {
        // Step 1: Set all gains to 0
        kp = ki = kd = 0;
        
        // Step 2: Increase Kp until oscillation
        std::cout << "Increase Kp until sustained oscillation\n";
        // kp = user_input;
        
        // Step 3: Reduce Kp by half, add Ki
        kp = kp * 0.5f;
        ki = kp / 10.0f;  // Start conservative
        
        // Step 4: Increase Ki until acceptable settling
        // Then add Kd for overshoot reduction
        kd = kp / 20.0f;
    }
};
```

### 3. Field-Oriented Control (FOC)

FOC provides optimal torque control for AC motors.

```cpp
#include <cmath>

class FOCController {
public:
    struct MotorParams {
        float pole_pairs;
        float rs;        // Stator resistance (ohm)
        float ld;        // D-axis inductance (H)
        float lq;        // Q-axis inductance (H)
        float flux_linkage;  // PM flux linkage (Wb)
        float max_current;
        float max_voltage;
    };
    
    FOCController(const MotorParams& params) : params_(params) {
        // Initialize current controllers
        float current_bw = 1000.0f;  // 1 kHz bandwidth
        
        // PI gains for current loops
        float kp_i = params.ld * current_bw;
        float ki_i = params.rs * current_bw;
        
        d_controller_.setGains(kp_i, ki_i, 0);
        q_controller_.setGains(kp_i, ki_i, 0);
    }
    
    struct CurrentCommand {
        float i_d;  // D-axis current (flux)
        float i_q;  // Q-axis current (torque)
    };
    
    struct VoltageCommand {
        float v_alpha;
        float v_beta;
    };
    
    VoltageCommand update(float i_a, float i_b, float i_c,
                         float theta, float omega,
                         const CurrentCommand& cmd,
                         float dt) {
        // Clarke transform (3-phase to 2-phase)
        float i_alpha, i_beta;
        clarkeTransform(i_a, i_b, i_c, i_alpha, i_beta);
        
        // Park transform (stationary to rotating)
        float cos_theta = cosf(theta);
        float sin_theta = sinf(theta);
        
        float i_d =  i_alpha * cos_theta + i_beta * sin_theta;
        float i_q = -i_alpha * sin_theta + i_beta * cos_theta;
        
        // Current controllers with decoupling
        float v_d_ff = -omega * params_.lq * i_q;  // Cross-coupling
        float v_q_ff =  omega * (params_.ld * i_d + params_.flux_linkage);
        
        float v_d = d_controller_.update(cmd.i_d, i_d, dt) + v_d_ff;
        float v_q = q_controller_.update(cmd.i_q, i_q, dt) + v_q_ff;
        
        // Voltage limit (circle limiting)
        float v_mag = sqrtf(v_d * v_d + v_q * v_q);
        if (v_mag > params_.max_voltage) {
            float scale = params_.max_voltage / v_mag;
            v_d *= scale;
            v_q *= scale;
        }
        
        // Inverse Park transform
        float v_alpha = v_d * cos_theta - v_q * sin_theta;
        float v_beta  = v_d * sin_theta + v_q * cos_theta;
        
        return {v_alpha, v_beta};
    }
    
    // MTPA (Maximum Torque Per Ampere) for IPMSM
    CurrentCommand mtpaCommand(float torque_ref) {
        CurrentCommand cmd;
        
        if (params_.ld == params_.lq) {  // SPMSM
            // Torque = (3/2) * pp * flux * i_q
            cmd.i_d = 0;
            cmd.i_q = (2.0f / 3.0f) * torque_ref / 
                     (params_.pole_pairs * params_.flux_linkage);
        } else {  // IPMSM
            // Optimal i_d for reluctance torque
            float num = params_.flux_linkage / (params_.lq - params_.ld);
            float denom = sqrtf(1.0f + num * num);
            
            cmd.i_d = num - num / denom;
            cmd.i_q = torque_ref / (1.5f * params_.pole_pairs * 
                     (params_.flux_linkage + (params_.ld - params_.lq) * cmd.i_d));
        }
        
        // Limit currents
        float i_mag = sqrtf(cmd.i_d * cmd.i_d + cmd.i_q * cmd.i_q);
        if (i_mag > params_.max_current) {
            float scale = params_.max_current / i_mag;
            cmd.i_d *= scale;
            cmd.i_q *= scale;
        }
        
        return cmd;
    }

private:
    MotorParams params_;
    PIDController d_controller_{{}};
    PIDController q_controller_{{}};
    
    void clarkeTransform(float a, float b, float c, float& alpha, float& beta) {
        alpha = (2.0f / 3.0f) * (a - 0.5f * b - 0.5f * c);
        beta  = (1.0f / sqrtf(3.0f)) * (b - c);
    }
};
```

**Space Vector PWM (SVPWM):**

```cpp
class SVPWM {
public:
    struct DutyCycles {
        float da, db, dc;  // 0.0 to 1.0
    };
    
    static DutyCycles generate(float v_alpha, float v_beta, float v_dc) {
        // Normalize voltages
        float v_alpha_n = v_alpha / v_dc;
        float v_beta_n = v_beta / v_dc;
        
        // Inverse Clarke to get phase voltages
        float va = v_alpha_n;
        float vb = -0.5f * v_alpha_n + sqrtf(3.0f) / 2.0f * v_beta_n;
        float vc = -0.5f * v_alpha_n - sqrtf(3.0f) / 2.0f * v_beta_n;
        
        // Add zero-sequence for center alignment
        float v_offset = (fminf(fminf(va, vb), vc) + 
                         fmaxf(fmaxf(va, vb), vc)) / 2.0f;
        
        DutyCycles pwm;
        pwm.da = 0.5f + (va - v_offset);
        pwm.db = 0.5f + (vb - v_offset);
        pwm.dc = 0.5f + (vc - v_offset);
        
        // Clamp to valid range
        pwm.da = clamp(pwm.da, 0.0f, 1.0f);
        pwm.db = clamp(pwm.db, 0.0f, 1.0f);
        pwm.dc = clamp(pwm.dc, 0.0f, 1.0f);
        
        return pwm;
    }

private:
    static float clamp(float val, float min, float max) {
        return std::max(min, std::min(max, val));
    }
};
```

### 4. Encoder Interface

High-resolution position feedback for servo control.

```cpp
class QuadratureEncoder {
public:
    struct Config {
        int32_t cpr;           // Counts per revolution
        float sample_time;     // Sampling period (s)
        int32_t gear_ratio;    // Motor:Encoder ratio
    };
    
    QuadratureEncoder(const Config& config) : config_(config) {}
    
    void update(int32_t raw_count) {
        // Handle overflow
        int32_t delta = raw_count - prev_count_;
        if (delta > config_.cpr / 2) {
            delta -= config_.cpr;
        } else if (delta < -config_.cpr / 2) {
            delta += config_.cpr;
        }
        
        total_count_ += delta;
        prev_count_ = raw_count;
        
        // Calculate velocity (counts/sample)
        velocity_ = delta / config_.sample_time;
    }
    
    float getPositionRad() const {
        return 2.0f * M_PI * total_count_ / 
               (config_.cpr * config_.gear_ratio);
    }
    
    float getVelocityRadS() const {
        return 2.0f * M_PI * velocity_ / 
               (config_.cpr * config_.gear_ratio);
    }
    
    void setZero() {
        total_count_ = 0;
    }

private:
    Config config_;
    int32_t prev_count_ = 0;
    int32_t total_count_ = 0;
    float velocity_ = 0.0f;
};
```

**STM32 timer encoder mode:**

```c
void Encoder_Init(TIM_HandleTypeDef* htim) {
    TIM_Encoder_InitTypeDef sConfig = {0};
    
    htim->Instance = TIM2;
    htim->Init.Prescaler = 0;
    htim->Init.CounterMode = TIM_COUNTERMODE_UP;
    htim->Init.Period = 65535;  // Maximum count
    htim->Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    
    sConfig.EncoderMode = TIM_ENCODERMODE_TI12;  // X4 mode
    sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC1Filter = 0;
    sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC2Filter = 0;
    
    HAL_TIM_Encoder_Init(htim, &sConfig);
    HAL_TIM_Encoder_Start(htim, TIM_CHANNEL_ALL);
}

int32_t Encoder_Read(TIM_HandleTypeDef* htim) {
    return (int16_t)__HAL_TIM_GET_COUNTER(htim);  // Sign-extend
}
```

### 5. PREEMPT_RT Linux

Real-time Linux for soft real-time control.

```bash
# Check if running PREEMPT_RT kernel
uname -a | grep PREEMPT_RT

# Install PREEMPT_RT kernel
sudo apt install linux-image-rt

# Configure real-time priorities
sudo groupadd realtime
sudo usermod -aG realtime $USER

# /etc/security/limits.conf
@realtime soft rtprio 99
@realtime soft priority 99
@realtime soft memlock 102400
@realtime hard rtprio 99
```

**Real-time thread example:**

```cpp
#include <pthread.h>
#include <sched.h>
#include <sys/mman.h>

class RealTimeThread {
public:
    bool create(void* (*func)(void*), void* arg, int priority = 80) {
        pthread_attr_t attr;
        struct sched_param param;
        
        // Lock memory to prevent swapping
        if (mlockall(MCL_CURRENT | MCL_FUTURE) == -1) {
            perror("mlockall");
            return false;
        }
        
        // Initialize thread attributes
        pthread_attr_init(&attr);
        
        // Set scheduling policy to FIFO
        pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
        pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
        
        // Set priority
        param.sched_priority = priority;
        pthread_attr_setschedparam(&attr, &param);
        
        // Create thread
        if (pthread_create(&thread_, &attr, func, arg) != 0) {
            perror("pthread_create");
            return false;
        }
        
        pthread_attr_destroy(&attr);
        return true;
    }
    
    void join() {
        pthread_join(thread_, nullptr);
    }

private:
    pthread_t thread_;
};
```

**Cyclic control loop with jitter measurement:**

```cpp
#include <time.h>

class CyclicController {
public:
    void run() {
        struct timespec next_time;
        clock_gettime(CLOCK_MONOTONIC, &next_time);
        
        const int64_t period_ns = 1000000;  // 1 ms = 1 MHz
        
        int64_t min_jitter = INT64_MAX;
        int64_t max_jitter = 0;
        int64_t total_jitter = 0;
        int sample_count = 0;
        
        while (running_) {
            // Calculate next wake time
            next_time.tv_nsec += period_ns;
            if (next_time.tv_nsec >= 1000000000) {
                next_time.tv_sec++;
                next_time.tv_nsec -= 1000000000;
            }
            
            // Sleep until next period
            clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next_time, nullptr);
            
            // Measure actual wake time
            struct timespec actual_time;
            clock_gettime(CLOCK_MONOTONIC, &actual_time);
            
            // Calculate jitter
            int64_t actual_ns = actual_time.tv_sec * 1000000000LL + 
                               actual_time.tv_nsec;
            int64_t expected_ns = next_time.tv_sec * 1000000000LL + 
                                 next_time.tv_nsec;
            int64_t jitter = llabs(actual_ns - expected_ns);
            
            // Statistics
            min_jitter = std::min(min_jitter, jitter);
            max_jitter = std::max(max_jitter, jitter);
            total_jitter += jitter;
            sample_count++;
            
            // Run control algorithm
            controlLoop();
            
            // Print stats every 10 seconds
            if (sample_count % 10000 == 0) {
                printf("Jitter: min=%ld ns, max=%ld ns, avg=%ld ns\n",
                       min_jitter, max_jitter, total_jitter / sample_count);
            }
        }
    }

private:
    bool running_ = true;
    
    void controlLoop() {
        // Read sensors
        // Compute control
        // Output to actuators
    }
};
```

## Common Patterns

### Pattern 1: Cascaded Position-Velocity-Current Control

```cpp
class CascadedMotorController {
public:
    struct Config {
        PIDController::Config pos_pid;
        PIDController::Config vel_pid;
        PIDController::Config cur_pid;
        
        float max_velocity;    // rad/s
        float max_acceleration; // rad/s^2
        float max_current;     // A
    };
    
    CascadedMotorController(const Config& config) 
        : pos_pid_(config.pos_pid),
          vel_pid_(config.vel_pid),
          cur_pid_(config.cur_pid),
          config_(config) {}
    
    float update(float pos_ref, float pos_fb, 
                 float vel_fb, float cur_fb,
                 float dt) {
        // Position loop
        float vel_ref = pos_pid_.update(pos_ref, pos_fb, dt);
        vel_ref = clamp(vel_ref, -config_.max_velocity, config_.max_velocity);
        
        // Velocity loop with feedforward
        float acc = (vel_ref - prev_vel_ref_) / dt;
        acc = clamp(acc, -config_.max_acceleration, config_.max_acceleration);
        
        float cur_ref = vel_pid_.update(vel_ref, vel_fb, dt);
        cur_ref += config_.torque_constant * acc;  // Feedforward
        
        // Current loop
        float voltage = cur_pid_.update(cur_ref, cur_fb, dt);
        
        prev_vel_ref_ = vel_ref;
        
        return voltage;
    }

private:
    PIDController pos_pid_;
    PIDController vel_pid_;
    PIDController cur_pid_;
    Config config_;
    float prev_vel_ref_ = 0.0f;
    
    float clamp(float val, float min, float max) {
        return std::max(min, std::min(max, val));
    }
};
```

### Pattern 2: Motion Profile Generation

```cpp
class TrapezoidalProfile {
public:
    struct State {
        float position;
        float velocity;
        float acceleration;
    };
    
    struct Constraints {
        float max_velocity;
        float max_acceleration;
        float max_jerk;  // 0 for trapezoidal, >0 for S-curve
    };
    
    void plan(float start_pos, float end_pos, 
              float start_vel, float end_vel,
              const Constraints& constraints) {
        float delta_pos = end_pos - start_pos;
        float delta_vel = end_vel - start_vel;
        
        // Calculate acceleration time
        accel_time_ = (constraints.max_velocity - start_vel) / 
                      constraints.max_acceleration;
        
        // Calculate deceleration time
        decel_time_ = (constraints.max_velocity - end_vel) / 
                      constraints.max_acceleration;
        
        // Calculate cruise distance
        float accel_dist = 0.5f * (start_vel + constraints.max_velocity) * 
                          accel_time_;
        float decel_dist = 0.5f * (constraints.max_velocity + end_vel) * 
                          decel_time_;
        float cruise_dist = std::abs(delta_pos) - accel_dist - decel_dist;
        
        if (cruise_dist < 0) {
            // Triangular profile (no cruise)
            // Recalculate...
        }
        
        cruise_time_ = cruise_dist / constraints.max_velocity;
        total_time_ = accel_time_ + cruise_time_ + decel_time_;
        
        direction_ = (delta_pos >= 0) ? 1.0f : -1.0f;
        constraints_ = constraints;
    }
    
    State sample(float t) const {
        State s;
        
        if (t < accel_time_) {
            // Acceleration phase
            s.acceleration = direction_ * constraints_.max_acceleration;
            s.velocity = constraints_.max_acceleration * t;
            s.position = 0.5f * s.acceleration * t * t;
        } else if (t < accel_time_ + cruise_time_) {
            // Cruise phase
            s.acceleration = 0;
            s.velocity = direction_ * constraints_.max_velocity;
            float t_cruise = t - accel_time_;
            s.position = 0.5f * direction_ * constraints_.max_acceleration * 
                        accel_time_ * accel_time_ + 
                        direction_ * constraints_.max_velocity * t_cruise;
        } else if (t < total_time_) {
            // Deceleration phase
            float t_decel = t - accel_time_ - cruise_time_;
            s.acceleration = -direction_ * constraints_.max_acceleration;
            s.velocity = direction_ * constraints_.max_velocity + 
                        s.acceleration * t_decel;
            s.position = /* calculate position */;
        } else {
            // At target
            s.acceleration = 0;
            s.velocity = 0;
            s.position = direction_ * total_distance_;
        }
        
        return s;
    }

private:
    float accel_time_, cruise_time_, decel_time_, total_time_;
    float direction_;
    float total_distance_;
    Constraints constraints_;
};
```

### Pattern 3: Multi-Axis Synchronization

```cpp
class MultiAxisController {
public:
    struct AxisCommand {
        float position;
        float max_velocity;
        float max_acceleration;
    };
    
    void moveLinear(const std::vector<AxisCommand>& commands) {
        // Find limiting axis
        float max_ratio = 0;
        for (size_t i = 0; i < axes_.size(); ++i) {
            float distance = std::abs(commands[i].position - axes_[i]->getPosition());
            float time = distance / commands[i].max_velocity;
            max_ratio = std::max(max_ratio, time);
        }
        
        // Scale all axes to match slowest
        for (size_t i = 0; i < axes_.size(); ++i) {
            float distance = std::abs(commands[i].position - axes_[i]->getPosition());
            float scaled_vel = distance / max_ratio;
            float scaled_acc = commands[i].max_acceleration * 
                              (scaled_vel / commands[i].max_velocity);
            
            axes_[i]->moveTo(commands[i].position, scaled_vel, scaled_acc);
        }
        
        // Wait for all axes to complete
        waitForCompletion();
    }
    
    void moveCircular(int plane_axis1, int plane_axis2,
                     float center1, float center2,
                     float angle, float velocity) {
        // Generate circular interpolation points
        // ...
    }

private:
    std::vector<MotorAxis*> axes_;
    
    void waitForCompletion() {
        bool all_done;
        do {
            all_done = true;
            for (auto& axis : axes_) {
                if (!axis->isMotionComplete()) {
                    all_done = false;
                    break;
                }
            }
        } while (!all_done);
    }
};
```

## Anti-Patterns

### ❌ Open-loop stepping
Driving steppers without feedback causes missed steps.

**What happens:** Position error accumulates, crashes into limits.

### ✅ Closed-loop stepper or servo
```cpp
// Add encoder feedback
encoder.update(readEncoder());
if (step_count != encoder.getPosition()) {
    // Missed steps detected
    recoverPosition();
}
```

### ❌ High PID gains without filtering
Aggressive tuning amplifies noise.

**What happens:** Oscillation, motor heating, mechanical wear.

### ✅ Derivative filtering, current limiting
```cpp
pid_config.derivative_filter = 0.1f;  // 10% filter
pid_config.output_max = motor_max_current;
```

### ❌ Blocking in control loop
I/O operations in ISR cause jitter.

**What happens:** Variable loop time, instability.

### ✅ Pre-fetch data, minimal ISR
```cpp
// Main loop: prepare data
sensor_data = readSensors();

// ISR: just control
void TIM_IRQHandler() {
    output = controller.update(setpoint, feedback, dt);
    setPWM(output);
}
```

### ❌ No current limiting
Motor stall causes overheating.

**What happens:** Burnt motors, fire hazard.

### ✅ Hardware and software protection
```cpp
// Software
if (current > max_current) {
    pwm = 0;
    fault_flag = OVERCURRENT;
}

// Hardware (independent comparator)
// Triggers shutdown regardless of software
```

## Configuration Reference

### Control Loop Rates

| Loop Type | Typical Rate | Max Latency |
|-----------|-------------|-------------|
| Current | 10-20 kHz | 50 µs |
| Velocity | 1-2 kHz | 500 µs |
| Position | 100-500 Hz | 2 ms |
| Trajectory | 50-100 Hz | 10 ms |

### PWM Frequencies

| Motor Type | Frequency | Notes |
|-----------|-----------|-------|
| Brushed DC | 10-20 kHz | Audible range, higher = quieter |
| BLDC | 20-50 kHz | Above audible, lower losses |
| Stepper | 20-50 kHz | Microstepping clock |
| Induction | 2-10 kHz | Limited by switching losses |

### Encoder Resolutions

| Application | CPR (Counts/Rev) | Resolution |
|-------------|-----------------|------------|
| Low-cost | 500-1000 | 0.7-1.4° |
| Standard | 2000-4000 | 0.09-0.18° |
| High-precision | 10000+ | <0.04° |
| After gearbox | 100000+ | <0.004° |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Motor oscillates | High P gain or noise | Reduce gain, add filtering |
| Slow response | Low gains | Increase P, then I |
| Steady-state error | No integral term | Add Ki |
| Overshoot | High I or D | Reduce Ki, increase Kd |
| Encoder noise | Poor grounding | Shield cables, differential signals |
| Current spikes | Poor decoupling | Add capacitors near driver |
| Heat in motor | High current | Check tuning, reduce load |
| Position drift | Encoder slip | Check coupling, increase resolution |

## Workflow Integration

- **Before this:** Use `microcontrollers` for hardware setup
- **With this:** Use `serial-can-protocols` for drive communication
- **After this:** Use `ros2-control` for ROS2 integration
- **Related:** Use `control-systems` for control theory fundamentals

## Further Reading

- "AC Motor Control and Electrical Vehicle Applications" by Nam-Joon Kim
- "Motor Control: Modeling, Analysis and Design" by R. Krishnan
- [SimpleFOC Documentation](https://docs.simplefoc.com/)
- Related skills: `microcontrollers`, `serial-can-protocols`, `ros2-control`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering FOC, PID, encoders, and PREEMPT_RT
- Includes motion profiles and multi-axis control