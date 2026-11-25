---
name: rtos-micro-ros
description: FreeRTOS task scheduling, real-time patterns, micro-ROS integration for STM32/ESP32, and bridging microcontrollers to ROS2 via micro-ROS agent.
category: embedded
tags: [freertos, rtos, micro-ros, stm32, esp32, real-time, scheduling, microcontroller]
version: "1.0.0"
---

# RTOS / micro-ROS

FreeRTOS provides deterministic task scheduling on microcontrollers. micro-ROS extends the ROS2 communication model to STM32, ESP32, and other constrained MCUs. Together they let robot firmware publish sensor data and receive commands over the same DDS graph as the rest of the ROS2 system — without a custom serial protocol.

## When to Use

- Writing firmware with multiple concurrent tasks (motor control, IMU, communication)
- Needing deterministic timing guarantees that a bare loop cannot provide
- Replacing a custom serial protocol with ROS2-native pub/sub from firmware
- Publishing encoder counts, IMU data, or battery voltage directly as ROS2 topics
- Subscribing to `cmd_vel` or other ROS2 topics directly in firmware
- Calling ROS2 services from firmware (e.g., requesting a parameter)
- Setting up micro-ROS on STM32 via UART transport (FreeRTOS + STM32 HAL / CubeMX)
- Setting up micro-ROS on ESP32 via WiFi UDP transport
- Running the micro-ROS agent on a Raspberry Pi as a bridge to the ROS2 network
- Debugging stack overflows, priority inversions, or deadline misses in FreeRTOS tasks

## Quick Start

```bash
# ── Raspberry Pi (agent side) ──────────────────────────────────────────────

# Option A: Run micro-ROS agent via Docker (fastest)
docker run -it --rm \
  --net=host \
  microros/micro-ros-agent:jazzy \
  serial --dev /dev/motordriver --baud 115200

# Option B: Build micro-ROS agent natively
sudo apt install ros-jazzy-micro-ros-agent
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/motordriver --baud 115200

# ── PlatformIO project (MCU side) ─────────────────────────────────────────

# Add to platformio.ini:
# lib_deps = https://github.com/micro-ROS/micro_ros_platformio

# Build and upload
~/.platformio/penv/bin/pio run --target upload

# Verify topics appear in ROS2 graph
ros2 topic list
# /orbibot/encoders
# /imu/data_raw
# /cmd_vel_firmware
```

## Core Concepts

### 1. FreeRTOS Task Model

Every FreeRTOS task is an infinite loop with a stack and priority. Higher-priority numbers mean higher priority in FreeRTOS (opposite of Unix).

```c
/* tasks.h — FreeRTOS task priorities for OrbiBot firmware */
#define PRIORITY_MOTOR_CONTROL   5    /* Highest — 100 Hz PID loop */
#define PRIORITY_IMU_SAMPLING    4    /* 50 Hz IMU read */
#define PRIORITY_MICRO_ROS       3    /* micro-ROS spin + serial */
#define PRIORITY_TELEMETRY       2    /* Status aggregation */
#define PRIORITY_IDLE            0    /* FreeRTOS idle task (built-in) */

/* Stack sizes in WORDS (4 bytes each on Cortex-M) */
#define STACK_MOTOR_CONTROL   256     /* 1 KB — simple PID, no printf */
#define STACK_IMU_SAMPLING    512     /* 2 KB — SPI + float math */
#define STACK_MICRO_ROS      2048     /* 8 KB — micro-ROS needs headroom */
#define STACK_TELEMETRY       512
```

```c
#include "FreeRTOS.h"
#include "task.h"
#include "orbibot_config.h"

/* Task function signature: void task_fn(void *params) */
void motor_control_task(void *params);
void imu_sampling_task(void *params);
void micro_ros_task(void *params);

/* Task handles — used for notifications and deletion */
static TaskHandle_t motor_task_handle = NULL;
static TaskHandle_t imu_task_handle   = NULL;
static TaskHandle_t ros_task_handle   = NULL;

void firmware_init_tasks(void) {
    BaseType_t rc;

    rc = xTaskCreate(
        motor_control_task,       /* Task function */
        "MotorCtrl",              /* Name (debug only, max configMAX_TASK_NAME_LEN) */
        STACK_MOTOR_CONTROL,      /* Stack size in WORDS */
        NULL,                     /* pvParameters — pass struct pointer if needed */
        PRIORITY_MOTOR_CONTROL,   /* Priority */
        &motor_task_handle        /* Handle out — NULL if unused */
    );
    configASSERT(rc == pdPASS);

    rc = xTaskCreate(imu_sampling_task, "ImuSample", STACK_IMU_SAMPLING,
                     NULL, PRIORITY_IMU_SAMPLING, &imu_task_handle);
    configASSERT(rc == pdPASS);

    rc = xTaskCreate(micro_ros_task, "MicroROS", STACK_MICRO_ROS,
                     NULL, PRIORITY_MICRO_ROS, &ros_task_handle);
    configASSERT(rc == pdPASS);

    /* Start the scheduler — never returns */
    vTaskStartScheduler();

    /* Should never reach here. If it does, heap is exhausted. */
    for (;;) { /* spin */ }
}
```

### 2. Precise Timing: vTaskDelay vs vTaskDelayUntil

`vTaskDelay` delays relative to when the call is made — drift accumulates. `vTaskDelayUntil` delays relative to a fixed wake time — use this for control loops.

```c
#include "FreeRTOS.h"
#include "task.h"

#define MOTOR_PERIOD_MS   10    /* 100 Hz */
#define IMU_PERIOD_MS     20    /* 50 Hz */

/* BAD — vTaskDelay causes drift because execution time is not accounted for */
void bad_motor_task(void *params) {
    for (;;) {
        pid_update();                         /* Takes ~200 µs */
        vTaskDelay(pdMS_TO_TICKS(10));        /* Waits 10 ms after pid_update */
        /* Actual period = 10 ms + 200 µs — accumulates over time */
    }
}

/* GOOD — vTaskDelayUntil gives period-accurate execution */
void motor_control_task(void *params) {
    TickType_t last_wake = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(MOTOR_PERIOD_MS);

    for (;;) {
        pid_update_all_motors();
        encoder_publish_counts();

        /* Block until exactly last_wake + period — corrects for execution time */
        vTaskDelayUntil(&last_wake, period);
    }
}

void imu_sampling_task(void *params) {
    TickType_t last_wake = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(IMU_PERIOD_MS);

    for (;;) {
        imu_read_accel_gyro();
        imu_read_magnetometer();
        /* Madgwick filter runs here or in ROS2 (Madgwick is cheaper in ROS2) */

        vTaskDelayUntil(&last_wake, period);
    }
}
```

### 3. Queues — Safe Inter-Task Communication

Queues are the primary inter-task data exchange mechanism. Never share global variables between tasks without protection.

```c
#include "FreeRTOS.h"
#include "queue.h"
#include <string.h>

/* ── Shared data types ───────────────────────────────────────────────────── */
typedef struct {
    int32_t counts[4];        /* [FL, BL, FR, BR] */
    uint32_t timestamp_ms;
} encoder_sample_t;

typedef struct {
    float vx;
    float vy;
    float omega;
} cmd_vel_t;

/* ── Queue handles (created before scheduler starts) ─────────────────────── */
static QueueHandle_t encoder_queue = NULL;
static QueueHandle_t cmd_vel_queue = NULL;

void queues_init(void) {
    /* Queue of 4 encoder samples — producer: motor_control_task, consumer: micro_ros_task */
    encoder_queue = xQueueCreate(4, sizeof(encoder_sample_t));
    configASSERT(encoder_queue != NULL);

    /* Queue of 1 cmd_vel — only latest matters, use overwrite pattern */
    cmd_vel_queue = xQueueCreate(1, sizeof(cmd_vel_t));
    configASSERT(cmd_vel_queue != NULL);
}

/* Producer: motor control task writes encoder data */
void motor_control_task(void *params) {
    TickType_t last_wake = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(10);

    for (;;) {
        encoder_sample_t sample;
        encoder_read_all(sample.counts);
        sample.timestamp_ms = xTaskGetTickCount() * portTICK_PERIOD_MS;

        /* Non-blocking: drop sample if queue full (micro-ROS fell behind) */
        xQueueSend(encoder_queue, &sample, 0);

        vTaskDelayUntil(&last_wake, period);
    }
}

/* Consumer: micro-ROS task reads and publishes */
void micro_ros_task(void *params) {
    encoder_sample_t sample;

    for (;;) {
        /* Block up to 50 ms waiting for a new sample */
        if (xQueueReceive(encoder_queue, &sample, pdMS_TO_TICKS(50)) == pdTRUE) {
            publish_encoder_msg(&sample);
        }
        /* Spin micro-ROS to handle incoming cmd_vel */
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1));
    }
}

/* cmd_vel callback from micro-ROS — writes to queue for motor task */
void cmd_vel_callback(const void *msg_in) {
    const geometry_msgs__msg__Twist *twist = (const geometry_msgs__msg__Twist *)msg_in;
    cmd_vel_t vel = {
        .vx    = (float)twist->linear.x,
        .vy    = (float)twist->linear.y,
        .omega = (float)twist->angular.z,
    };
    /* Overwrite: motor control always sees the latest command */
    xQueueOverwrite(cmd_vel_queue, &vel);
}
```

### 4. Semaphores and Mutexes

Use mutexes to protect shared hardware (SPI bus, UART). Use binary semaphores to signal events from ISRs.

```c
#include "FreeRTOS.h"
#include "semphr.h"

/* Mutex: protects the SPI bus shared between IMU and encoder tasks */
static SemaphoreHandle_t spi_mutex = NULL;

/* Binary semaphore: signaled by timer ISR to wake the control task */
static SemaphoreHandle_t control_tick_sem = NULL;

void semaphores_init(void) {
    spi_mutex = xSemaphoreCreateMutex();
    configASSERT(spi_mutex != NULL);

    control_tick_sem = xSemaphoreCreateBinary();
    configASSERT(control_tick_sem != NULL);
}

/* Hardware timer ISR — runs at 100 Hz */
void TIM6_DAC_IRQHandler(void) {
    BaseType_t higher_priority_woken = pdFALSE;

    if (__HAL_TIM_GET_FLAG(&htim6, TIM_FLAG_UPDATE)) {
        __HAL_TIM_CLEAR_IT(&htim6, TIM_IT_UPDATE);

        /* Wake the motor control task — ISR-safe API */
        xSemaphoreGiveFromISR(control_tick_sem, &higher_priority_woken);

        /* If a higher-priority task was unblocked, yield immediately */
        portYIELD_FROM_ISR(higher_priority_woken);
    }
}

/* Motor control task — woken by ISR for deterministic 100 Hz execution */
void motor_control_task(void *params) {
    for (;;) {
        /* Block indefinitely until ISR fires — no busy-wait */
        xSemaphoreTake(control_tick_sem, portMAX_DELAY);
        pid_update_all_motors();
    }
}

/* SPI read protected by mutex */
int imu_read_protected(float *ax, float *ay, float *az) {
    if (xSemaphoreTake(spi_mutex, pdMS_TO_TICKS(10)) != pdTRUE) {
        return -1;    /* Timeout — another task holds the bus */
    }
    int rc = spi_read_accel(ax, ay, az);
    xSemaphoreGive(spi_mutex);
    return rc;
}
```

### 5. micro-ROS Setup on STM32 with UART Transport

```c
/* main.c — micro-ROS publisher/subscriber on STM32 + FreeRTOS */
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32_multi_array.h>
#include <geometry_msgs/msg/twist.h>
#include <micro_ros_utilities/type_utilities.h>

/* ── micro-ROS transport: UART via STM32 HAL ─────────────────────────────── */
#include <uxr/client/transport.h>

extern UART_HandleTypeDef huart2;    /* CubeMX generated */

bool cubemx_transport_open(struct uxrCustomTransport *transport);
bool cubemx_transport_close(struct uxrCustomTransport *transport);
size_t cubemx_transport_write(struct uxrCustomTransport *transport,
                               const uint8_t *buf, size_t len, uint8_t *err);
size_t cubemx_transport_read(struct uxrCustomTransport *transport,
                               uint8_t *buf, size_t len, int timeout, uint8_t *err);

/* ── Global micro-ROS entities ───────────────────────────────────────────── */
static rcl_node_t node;
static rcl_publisher_t encoder_pub;
static rcl_subscription_t cmd_vel_sub;
static rclc_executor_t executor;
static rclc_support_t support;
static rcl_allocator_t allocator;

static std_msgs__msg__Int32MultiArray encoder_msg;
static geometry_msgs__msg__Twist cmd_vel_msg;

/* ── Helper macro to check return codes ─────────────────────────────────── */
#define RCCHECK(fn) { \
    rcl_ret_t rc = (fn); \
    if (rc != RCL_RET_OK) { \
        error_handler(__FILE__, __LINE__, rc); \
    } \
}

static void error_handler(const char *file, int line, rcl_ret_t rc) {
    /* Flash LED and loop — visible failure indication */
    HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_SET);
    for (;;) { HAL_Delay(200); }
    (void)file; (void)line; (void)rc;
}

void cmd_vel_callback(const void *msg_in) {
    const geometry_msgs__msg__Twist *twist = (const geometry_msgs__msg__Twist *)msg_in;
    /* Apply to motor controller — called from micro-ROS executor context */
    motor_set_velocities(
        (float)twist->linear.x,
        (float)twist->linear.y,
        (float)twist->angular.z
    );
}

void micro_ros_task(void *params) {
    /* ── Transport configuration ─────────────────────────────────────────── */
    rmw_uros_set_custom_transport(
        true,                          /* framing enabled */
        (void *)&huart2,
        cubemx_transport_open,
        cubemx_transport_close,
        cubemx_transport_write,
        cubemx_transport_read
    );

    allocator = rcl_get_default_allocator();

    /* Wait until the agent is connected (up to 10 attempts × 100 ms) */
    while (rmw_uros_ping_agent(100, 10) != RCL_RET_OK) {
        HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
    }
    HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);

    /* ── Init support, node, publishers, subscribers ─────────────────────── */
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

    RCCHECK(rclc_node_init_default(&node, "orbibot_firmware", "", &support));

    /* Publisher: encoder counts */
    RCCHECK(rclc_publisher_init_best_effort(
        &encoder_pub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32MultiArray),
        "/orbibot/encoders"
    ));

    /* Subscriber: velocity commands */
    RCCHECK(rclc_subscription_init_best_effort(
        &cmd_vel_sub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
        "/cmd_vel"
    ));

    /* Allocate encoder message array (4 wheels) */
    encoder_msg.data.capacity = 4;
    encoder_msg.data.size     = 4;
    encoder_msg.data.data     = (int32_t *)pvPortMalloc(4 * sizeof(int32_t));
    configASSERT(encoder_msg.data.data != NULL);

    /* Executor with 1 handle (the subscription) */
    RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
    RCCHECK(rclc_executor_add_subscription(
        &executor, &cmd_vel_sub, &cmd_vel_msg, &cmd_vel_callback, ON_NEW_DATA
    ));

    /* ── Main loop ───────────────────────────────────────────────────────── */
    TickType_t last_wake = xTaskGetTickCount();
    const TickType_t period = pdMS_TO_TICKS(20);    /* 50 Hz publish rate */

    for (;;) {
        /* Publish encoder counts */
        encoder_msg.data.data[0] = encoder_get_count(MOTOR_FL);
        encoder_msg.data.data[1] = encoder_get_count(MOTOR_BL);
        encoder_msg.data.data[2] = encoder_get_count(MOTOR_FR);
        encoder_msg.data.data[3] = encoder_get_count(MOTOR_BR);
        rcl_publish(&encoder_pub, &encoder_msg, NULL);

        /* Process incoming messages for up to 1 ms */
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1));

        vTaskDelayUntil(&last_wake, period);
    }
}
```

### 6. micro-ROS on ESP32 via WiFi UDP (PlatformIO)

```ini
; platformio.ini for ESP32 + micro-ROS + WiFi UDP
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
board_microros_transport = wifi
board_microros_distro = jazzy
lib_deps =
  https://github.com/micro-ROS/micro_ros_platformio
monitor_speed = 115200
```

```cpp
// main.cpp — micro-ROS on ESP32 with WiFi UDP transport
#include <Arduino.h>
#include <WiFi.h>
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <sensor_msgs/msg/imu.h>
#include <geometry_msgs/msg/twist.h>

// WiFi and agent configuration
const char *WIFI_SSID    = "YourSSID";
const char *WIFI_PASS    = "YourPassword";
const char *AGENT_IP     = "192.168.1.100";    // Raspberry Pi IP
const uint16_t AGENT_PORT = 8888;

static rcl_node_t        node;
static rcl_publisher_t   imu_pub;
static rcl_subscription_t cmd_vel_sub;
static rclc_support_t    support;
static rcl_allocator_t   allocator;
static rclc_executor_t   executor;

static sensor_msgs__msg__Imu       imu_msg;
static geometry_msgs__msg__Twist   cmd_vel_msg;

#define RCCHECK(fn) { if ((fn) != RCL_RET_OK) { error_loop(); } }

void error_loop() {
    while (true) { digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN)); delay(100); }
}

void cmd_vel_callback(const void *msg_in) {
    auto *twist = (const geometry_msgs__msg__Twist *)msg_in;
    // Forward to motor controller
    set_motor_velocities(twist->linear.x, twist->linear.y, twist->angular.z);
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    // Connect to WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
    Serial.println("WiFi connected: " + WiFi.localIP().toString());

    // Configure micro-ROS UDP transport
    set_microros_wifi_transports(WIFI_SSID, WIFI_PASS, AGENT_IP, AGENT_PORT);
    delay(2000);

    allocator = rcl_get_default_allocator();
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
    RCCHECK(rclc_node_init_default(&node, "orbibot_esp32", "", &support));

    RCCHECK(rclc_publisher_init_best_effort(
        &imu_pub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, Imu),
        "/imu/data_raw"
    ));

    RCCHECK(rclc_subscription_init_best_effort(
        &cmd_vel_sub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
        "/cmd_vel"
    ));

    RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
    RCCHECK(rclc_executor_add_subscription(
        &executor, &cmd_vel_sub, &cmd_vel_msg, &cmd_vel_callback, ON_NEW_DATA
    ));

    // Set IMU frame
    micro_ros_string_utilities_set(imu_msg.header.frame_id, "imu_link");
    Serial.println("micro-ROS initialized");
    digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
    static unsigned long last_pub = 0;

    if (millis() - last_pub >= 20) {    // 50 Hz
        last_pub = millis();

        // Read IMU (implement imu_read_accel / imu_read_gyro)
        float ax, ay, az, gx, gy, gz;
        imu_read_accel(&ax, &ay, &az);
        imu_read_gyro(&gx, &gy, &gz);

        imu_msg.header.stamp = rmw_uros_epoch_nanos();
        imu_msg.linear_acceleration.x = ax;
        imu_msg.linear_acceleration.y = ay;
        imu_msg.linear_acceleration.z = az;
        imu_msg.angular_velocity.x = gx;
        imu_msg.angular_velocity.y = gy;
        imu_msg.angular_velocity.z = gz;
        imu_msg.orientation_covariance[0] = -1.0;   // Unknown orientation

        rcl_publish(&imu_pub, &imu_msg, NULL);
    }

    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1));
}
```

### 7. FreeRTOS Memory Management

```c
/* FreeRTOSConfig.h — key memory settings */

/* Heap model: heap_4 = best-fit with coalescing, suitable for most robots */
/* heap_1: no free (fastest, no fragmentation — use for static-only systems) */
/* heap_4: best-fit + coalescing (use this unless RAM < 8 KB) */
#define configUSE_HEAP_SCHEME 4

/* Total FreeRTOS heap — leave room for stack of each task */
/* STM32F103: 20 KB RAM total — be conservative */
/* STM32H743: 1 MB RAM — more generous */
#define configTOTAL_HEAP_SIZE ((size_t)(32 * 1024))    /* 32 KB */

/* Stack overflow detection: 1 = watermark, 2 = write-then-check (safer) */
#define configCHECK_FOR_STACK_OVERFLOW 2

/* Called when stack overflow is detected — DO NOT return */
void vApplicationStackOverflowHook(TaskHandle_t xTask, char *pcTaskName) {
    (void)xTask;
    /* Log the offending task name to UART before halting */
    char msg[64];
    snprintf(msg, sizeof(msg), "STACK OVERFLOW: %s\r\n", pcTaskName);
    HAL_UART_Transmit(&huart2, (uint8_t *)msg, strlen(msg), 100);
    taskDISABLE_INTERRUPTS();
    for (;;) { /* halt */ }
}

/* Called when pvPortMalloc fails */
void vApplicationMallocFailedHook(void) {
    HAL_UART_Transmit(&huart2, (uint8_t *)"MALLOC FAILED\r\n", 15, 100);
    taskDISABLE_INTERRUPTS();
    for (;;) {}
}

/* Static allocation: declare stack and TCB storage at file scope */
static StaticTask_t motor_task_tcb;
static StackType_t  motor_task_stack[STACK_MOTOR_CONTROL];

TaskHandle_t create_motor_task_static(void) {
    return xTaskCreateStatic(
        motor_control_task,
        "MotorCtrl",
        STACK_MOTOR_CONTROL,
        NULL,
        PRIORITY_MOTOR_CONTROL,
        motor_task_stack,
        &motor_task_tcb
    );
}
```

### 8. Watchdog Timer in FreeRTOS

```c
/* Independent Watchdog (IWDG) — feeds from a dedicated FreeRTOS task */
#include "iwdg.h"    /* CubeMX generated */

/* Watchdog feeder task — lowest priority.
 * If any higher-priority task starves this one, IWDG resets the MCU.
 * This detects deadlocks and infinite loops in critical tasks. */
#define WATCHDOG_FEED_PERIOD_MS 500    /* Must be < IWDG timeout (1000 ms) */

void watchdog_task(void *params) {
    TickType_t last_wake = xTaskGetTickCount();

    for (;;) {
        HAL_IWDG_Refresh(&hiwdg);
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(WATCHDOG_FEED_PERIOD_MS));
    }
}

/* Alternative: per-task watchdog using task notifications */
typedef struct {
    TaskHandle_t handles[4];
    uint32_t last_alive[4];
    uint32_t timeout_ms;
} task_watchdog_t;

static task_watchdog_t task_wdg;

void task_watchdog_init(task_watchdog_t *wdg, uint32_t timeout_ms) {
    wdg->timeout_ms = timeout_ms;
    memset(wdg->last_alive, 0, sizeof(wdg->last_alive));
}

void task_watchdog_kick(task_watchdog_t *wdg, uint8_t task_idx) {
    wdg->last_alive[task_idx] = xTaskGetTickCount() * portTICK_PERIOD_MS;
}

bool task_watchdog_check(task_watchdog_t *wdg) {
    uint32_t now = xTaskGetTickCount() * portTICK_PERIOD_MS;
    for (int i = 0; i < 4; i++) {
        if (wdg->handles[i] && (now - wdg->last_alive[i]) > wdg->timeout_ms) {
            return false;    /* Task missed its deadline */
        }
    }
    return true;
}
```

## Common Patterns

### Pattern 1: Complete STM32 + FreeRTOS + micro-ROS PlatformIO Project

```ini
; platformio.ini
[env:rosmaster_v3]
platform = ststm32
board = genericSTM32F103RC
framework = stm32cube
board_microros_transport = serial
board_microros_distro = jazzy

lib_deps =
  https://github.com/micro-ROS/micro_ros_platformio
  stm32duino/STM32duino FreeRTOS@^10.3.1

build_flags =
  -DUSE_HAL_DRIVER
  -DSTM32F103xE
  -IincludeI

; Custom linker to increase heap for micro-ROS
board_build.ldscript = STM32F103RCTX_FLASH.ld
```

```c
/* FreeRTOSConfig.h — minimal config for micro-ROS on STM32F103 */
#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

#define configUSE_PREEMPTION                1
#define configUSE_IDLE_HOOK                 0
#define configUSE_TICK_HOOK                 0
#define configCPU_CLOCK_HZ                  72000000UL
#define configTICK_RATE_HZ                  1000U        /* 1 ms tick */
#define configMAX_PRIORITIES                8
#define configMINIMAL_STACK_SIZE            128
#define configTOTAL_HEAP_SIZE               (32 * 1024)  /* 32 KB of 64 KB RAM */
#define configMAX_TASK_NAME_LEN             12
#define configUSE_TRACE_FACILITY            0
#define configUSE_STATS_FORMATTING_FUNCTIONS 0
#define configUSE_16_BIT_TICKS              0
#define configIDLE_SHOULD_YIELD             1
#define configUSE_MUTEXES                   1
#define configUSE_RECURSIVE_MUTEXES         0
#define configUSE_COUNTING_SEMAPHORES       1
#define configQUEUE_REGISTRY_SIZE           8
#define configUSE_QUEUE_SETS                0
#define configUSE_TIME_SLICING              1
#define configCHECK_FOR_STACK_OVERFLOW      2
#define configUSE_MALLOC_FAILED_HOOK        1
#define INCLUDE_vTaskDelay                  1
#define INCLUDE_vTaskDelayUntil             1
#define INCLUDE_uxTaskGetStackHighWaterMark 1
#define INCLUDE_xTaskGetHandle              1

/* Cortex-M interrupt priority configuration */
#define configPRIO_BITS                     4
#define configLIBRARY_LOWEST_INTERRUPT_PRIORITY      15
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY  5
#define configKERNEL_INTERRUPT_PRIORITY      (configLIBRARY_LOWEST_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))
#define configMAX_SYSCALL_INTERRUPT_PRIORITY (configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS))

#endif /* FREERTOS_CONFIG_H */
```

### Pattern 2: micro-ROS Agent Launch on Raspberry Pi

```bash
# Method 1: Docker with auto-reconnect
docker run -it --rm \
  --net=host \
  --device=/dev/motordriver \
  microros/micro-ros-agent:jazzy \
  serial --dev /dev/motordriver --baud 115200 -v4

# Method 2: Native agent as a systemd service
sudo tee /etc/systemd/system/micro-ros-agent.service > /dev/null <<'EOF'
[Unit]
Description=micro-ROS Agent (UART bridge to STM32)
After=network.target
Requires=dev-motordriver.device

[Service]
Type=simple
User=orbibot
ExecStart=/opt/ros/jazzy/lib/micro_ros_agent/micro_ros_agent serial \
  --dev /dev/motordriver --baud 115200
Restart=on-failure
RestartSec=2
Environment=ROS_DOMAIN_ID=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable micro-ros-agent
sudo systemctl start micro-ros-agent
sudo systemctl status micro-ros-agent

# Verify STM32 topics appear in ROS2
ros2 topic list
ros2 topic hz /orbibot/encoders    # Should show ~50 Hz
```

### Pattern 3: Task Runtime Statistics for Deadline Monitoring

```c
/* Print FreeRTOS task stats via UART — useful for CPU profiling */
/* Requires: configGENERATE_RUN_TIME_STATS=1, configUSE_STATS_FORMATTING_FUNCTIONS=1 */
/* Also requires a free-running counter faster than the tick (e.g., TIM2 at 1 MHz) */

#include "task.h"
#include <stdio.h>

#define STATS_BUFFER_SIZE 1024

void print_task_stats_task(void *params) {
    static char stats_buf[STATS_BUFFER_SIZE];

    for (;;) {
        vTaskList(stats_buf);
        /* Format: Name, State, Priority, Stack remaining (words), Task number */
        HAL_UART_Transmit(&huart2, (uint8_t *)"\r\nTask List:\r\n", 14, 100);
        HAL_UART_Transmit(&huart2, (uint8_t *)stats_buf, strlen(stats_buf), 200);

        vTaskGetRunTimeStats(stats_buf);
        HAL_UART_Transmit(&huart2, (uint8_t *)"\r\nRuntime Stats:\r\n", 18, 100);
        HAL_UART_Transmit(&huart2, (uint8_t *)stats_buf, strlen(stats_buf), 200);

        vTaskDelay(pdMS_TO_TICKS(5000));    /* Print every 5 seconds */
    }
}

/* Check stack headroom for all tasks */
void check_stack_usage(void) {
    TaskStatus_t task_array[10];
    uint32_t total_runtime;
    UBaseType_t n = uxTaskGetSystemState(task_array, 10, &total_runtime);

    for (UBaseType_t i = 0; i < n; i++) {
        char msg[80];
        snprintf(msg, sizeof(msg),
                 "%-12s pri=%u stack_remaining=%u words\r\n",
                 task_array[i].pcTaskName,
                 task_array[i].uxCurrentPriority,
                 task_array[i].usStackHighWaterMark);
        HAL_UART_Transmit(&huart2, (uint8_t *)msg, strlen(msg), 100);
    }
}
```

### Pattern 4: ROS2 Node on RPi That Bridges firmware Encoders to Odometry

```python
# ros_encoder_bridge.py — subscribes to /orbibot/encoders from micro-ROS
# and republishes as /odom using mecanum kinematics
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import tf2_ros
import math

# Physical constants — must match firmware orbibot_config.h
WHEEL_RADIUS        = 0.05      # metres
ENCODER_CPR         = 1320      # counts per revolution
LX                  = 0.13      # half wheelbase (front-rear half distance)
LY                  = 0.18      # half track (left-right half distance)
METRES_PER_COUNT    = (2.0 * math.pi * WHEEL_RADIUS) / ENCODER_CPR


class EncoderBridgeNode(Node):
    """Convert encoder counts from micro-ROS firmware to /odom Odometry."""

    def __init__(self):
        super().__init__('encoder_bridge')
        self._prev_counts = [0, 0, 0, 0]    # [FL, BL, FR, BR]
        self._x = self._y = self._yaw = 0.0

        self._odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self._tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.create_subscription(
            Int32MultiArray, '/orbibot/encoders',
            self._encoder_callback, 10
        )
        self.get_logger().info('EncoderBridgeNode ready')

    def _encoder_callback(self, msg: Int32MultiArray):
        if len(msg.data) != 4:
            return

        counts = list(msg.data)
        delta = [counts[i] - self._prev_counts[i] for i in range(4)]
        self._prev_counts = counts

        # Convert tick deltas to metres
        d_fl = delta[0] * METRES_PER_COUNT
        d_bl = delta[1] * METRES_PER_COUNT
        d_fr = delta[2] * METRES_PER_COUNT
        d_br = delta[3] * METRES_PER_COUNT

        # Mecanum forward kinematics (velocity → displacement)
        dx    = (d_fl + d_bl + d_fr + d_br) / 4.0
        dy    = (-d_fl + d_bl + d_fr - d_br) / 4.0
        dtheta = (-d_fl - d_bl + d_fr + d_br) / (4.0 * (LX + LY))

        # Integrate pose in odom frame
        self._x   += dx * math.cos(self._yaw) - dy * math.sin(self._yaw)
        self._y   += dx * math.sin(self._yaw) + dy * math.cos(self._yaw)
        self._yaw += dtheta

        now = self.get_clock().now().to_msg()
        self._publish_odom(now, dx, dy, dtheta)
        self._publish_tf(now)

    def _publish_odom(self, stamp, dx, dy, dtheta):
        msg = Odometry()
        msg.header.stamp    = stamp
        msg.header.frame_id = 'odom'
        msg.child_frame_id  = 'base_footprint'
        msg.pose.pose.position.x = self._x
        msg.pose.pose.position.y = self._y
        # Quaternion from yaw (simplified — full quat conversion for production)
        msg.pose.pose.orientation.z = math.sin(self._yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(self._yaw / 2.0)
        self._odom_pub.publish(msg)

    def _publish_tf(self, stamp):
        t = TransformStamped()
        t.header.stamp    = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id  = 'base_footprint'
        t.transform.translation.x = self._x
        t.transform.translation.y = self._y
        t.transform.rotation.z = math.sin(self._yaw / 2.0)
        t.transform.rotation.w = math.cos(self._yaw / 2.0)
        self._tf_broadcaster.sendTransform(t)
```

## Anti-Patterns

### ❌ Calling rcl_publish from Multiple Tasks Without Synchronization
micro-ROS internals are NOT thread-safe. Publishing from two tasks simultaneously corrupts the serial stream.

```c
/* WRONG — two tasks calling rcl_publish concurrently */
void motor_task(void *p) {
    for (;;) {
        rcl_publish(&encoder_pub, &encoder_msg, NULL);    /* Race! */
        vTaskDelay(10);
    }
}
void imu_task(void *p) {
    for (;;) {
        rcl_publish(&imu_pub, &imu_msg, NULL);            /* Race! */
        vTaskDelay(20);
    }
}
```

```c
/* CORRECT — all micro-ROS calls from a single dedicated task */
/* Other tasks use queues to pass data to the micro-ROS task */
static QueueHandle_t encoder_q;

void motor_task(void *p) {
    for (;;) {
        encoder_sample_t s;
        encoder_read_all(s.counts);
        xQueueSend(encoder_q, &s, 0);    /* Non-blocking enqueue */
        vTaskDelay(10);
    }
}

void micro_ros_task(void *p) {
    encoder_sample_t s;
    for (;;) {
        if (xQueueReceive(encoder_q, &s, pdMS_TO_TICKS(20))) {
            memcpy(encoder_msg.data.data, s.counts, 4 * sizeof(int32_t));
            rcl_publish(&encoder_pub, &encoder_msg, NULL);    /* Safe — single task */
        }
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1));
    }
}
```

### ❌ Using vTaskDelay for a Control Loop (Drift Accumulates)
`vTaskDelay` counts from when the delay is called. Execution time of the loop body adds to the period.

```c
/* WRONG — period = 10 ms + execution_time (accumulates) */
void bad_control_loop(void *p) {
    for (;;) {
        pid_update();                    /* Takes 200 µs */
        vTaskDelay(pdMS_TO_TICKS(10));   /* Waits 10 ms after pid_update */
        /* Actual period ≈ 10.2 ms — drifts by 2 % */
    }
}
```

```c
/* CORRECT — vTaskDelayUntil compensates for execution time */
void good_control_loop(void *p) {
    TickType_t last_wake = xTaskGetTickCount();
    for (;;) {
        pid_update();
        vTaskDelayUntil(&last_wake, pdMS_TO_TICKS(10));  /* Exact 10 ms period */
    }
}
```

### ❌ Allocating Large Buffers on the Task Stack
Stack overflows are silent on platforms without `configCHECK_FOR_STACK_OVERFLOW`. A large local array corrupts adjacent memory.

```c
/* WRONG — 1 KB buffer on a 256-word (1 KB) stack = instant overflow */
void bad_task(void *p) {
    uint8_t buffer[1024];     /* Stack overflow! */
    memset(buffer, 0, sizeof(buffer));
}
```

```c
/* CORRECT — use static or heap allocation for large buffers */
static uint8_t buffer[1024];     /* Static — allocated once at link time */

void good_task(void *p) {
    memset(buffer, 0, sizeof(buffer));    /* Safe — not on stack */
}
```

### ❌ Forgetting to Handle micro-ROS Reconnection
The micro-ROS agent can restart or disconnect. Without reconnection logic the firmware publishes into the void indefinitely.

```c
/* WRONG — no reconnection on agent loss */
void micro_ros_task(void *p) {
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "orbibot", "", &support);
    for (;;) {
        rcl_publish(&pub, &msg, NULL);    /* Silently fails after disconnect */
        vTaskDelay(20);
    }
}
```

```c
/* CORRECT — state machine with reconnection */
typedef enum { WAITING_AGENT, AGENT_AVAILABLE, AGENT_CONNECTED, AGENT_DISCONNECTED } agent_state_t;

void micro_ros_task(void *p) {
    agent_state_t state = WAITING_AGENT;

    for (;;) {
        switch (state) {
        case WAITING_AGENT:
            if (rmw_uros_ping_agent(100, 1) == RCL_RET_OK)
                state = AGENT_AVAILABLE;
            break;

        case AGENT_AVAILABLE:
            if (micro_ros_init() == RCL_RET_OK)    /* init node/pub/sub */
                state = AGENT_CONNECTED;
            else
                state = WAITING_AGENT;
            break;

        case AGENT_CONNECTED:
            if (rmw_uros_ping_agent(100, 1) != RCL_RET_OK) {
                micro_ros_destroy();                /* cleanup entities */
                state = AGENT_DISCONNECTED;
                break;
            }
            rcl_publish(&encoder_pub, &encoder_msg, NULL);
            rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1));
            break;

        case AGENT_DISCONNECTED:
            state = WAITING_AGENT;
            break;
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}
```

### ❌ Setting configTOTAL_HEAP_SIZE Larger Than Available RAM
FreeRTOS places its heap in BSS. If the total exceeds RAM, the linker fails silently and the firmware boots into HardFault.

```c
/* WRONG — STM32F103 has 20 KB RAM, this exceeds it when combined with code/stack */
#define configTOTAL_HEAP_SIZE ((size_t)(48 * 1024))    /* Will HardFault */

/* CORRECT — leave headroom for ISR stacks and static data */
/* Rule of thumb: FreeRTOS heap ≤ 60% of total RAM */
#define configTOTAL_HEAP_SIZE ((size_t)(10 * 1024))    /* 10 KB of 20 KB */
```

## Configuration Reference

### FreeRTOSConfig.h Key Parameters

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| `configTICK_RATE_HZ` | `1000` | 1 ms tick resolution; use 100 for power-limited MCUs |
| `configMAX_PRIORITIES` | `8` | Keep low — each priority adds a ready list overhead |
| `configTOTAL_HEAP_SIZE` | ≤ 60% RAM | Leave room for ISR stacks and linker symbols |
| `configMINIMAL_STACK_SIZE` | `128` (words) | Minimum for idle task |
| `configCHECK_FOR_STACK_OVERFLOW` | `2` | Always enable in development; 2 = write-then-check |
| `configUSE_MALLOC_FAILED_HOOK` | `1` | Always enable |
| `configUSE_MUTEXES` | `1` | Required for SPI bus sharing |
| `configUSE_COUNTING_SEMAPHORES` | `1` | Useful for buffer pools |
| `configGENERATE_RUN_TIME_STATS` | `1` (dev) | Disable in production to save RAM |

### Task Stack Sizing Guide

| Task Type | Min Stack (words) | Typical (words) | Notes |
|-----------|------------------|-----------------|-------|
| Simple math, no printf | 128 | 256 | PID loop, encoder read |
| SPI/I2C driver + float | 256 | 512 | IMU sampling |
| micro-ROS spin | 1024 | 2048 | Needs serialization buffer |
| micro-ROS with large msgs | 2048 | 4096 | PointCloud2, images |
| Printf debugging | +256 | — | stdio adds stack usage |

> Rule: set stack to 2× what you think you need. Use `uxTaskGetStackHighWaterMark()` to tune in production.

### micro-ROS Transport Options

| Transport | MCU Interface | Agent Command | Max Bandwidth | Latency |
|-----------|--------------|---------------|--------------|---------|
| Serial (UART) | UART (115200–921600 baud) | `serial --dev /dev/ttyUSB0` | ~90 KB/s | < 5 ms |
| Serial (USB CDC) | USB virtual COM | `serial --dev /dev/ttyACM0` | ~500 KB/s | < 2 ms |
| UDP (WiFi) | ESP32 WiFi | `udp4 --port 8888` | ~1 MB/s | 5–20 ms |
| UDP (Ethernet) | W5500 SPI Ethernet | `udp4 --port 8888` | ~1 MB/s | < 3 ms |
| CAN FD | CAN transceiver | custom transport | ~64 KB/s | < 1 ms |

### micro-ROS QoS Profiles in C

| Profile | C Constant | Use Case |
|---------|-----------|---------|
| Best effort | `rmw_qos_profile_sensor_data` | IMU, encoders, sensors |
| Reliable | `rmw_qos_profile_default` | cmd_vel, parameters |
| Keep last (1) | `rmw_qos_profile_parameters` | Configuration |

### PlatformIO micro-ROS Transport Flags

| `board_microros_transport` | Description |
|---------------------------|-------------|
| `serial` | UART/USB serial transport |
| `wifi` | ESP32 WiFi UDP |
| `ethernet` | W5500 Ethernet UDP |
| `native_ethernet` | STM32 built-in Ethernet |
| `custom` | User-defined transport callbacks |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Firmware enters `vApplicationStackOverflowHook` | Task stack too small | Increase `STACK_*` constant for the named task; check with `uxTaskGetStackHighWaterMark()` |
| `vApplicationMallocFailedHook` fires on startup | `configTOTAL_HEAP_SIZE` too large or micro-ROS message too big | Reduce heap size; use `micro_ros_utilities_get_dynamic_size()` before allocating |
| `rmw_uros_ping_agent` never returns `RCL_RET_OK` | Agent not running, wrong port, or UART wiring incorrect | Verify `ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/motordriver --baud 115200`; check TX/RX not swapped |
| Topics appear in `ros2 topic list` but no data | micro-ROS executor not spinning, or publish rate too low | Ensure `rclc_executor_spin_some` runs regularly in the micro-ROS task loop |
| Encoder counts jitter or freeze | Queue overflow — micro-ROS task not consuming fast enough | Increase queue depth; lower publish rate; use `xQueueOverwrite` for latest-value queues |
| HardFault on startup after changing heap size | `configTOTAL_HEAP_SIZE` exceeds physical RAM | Reduce heap to ≤ 60% of RAM; check linker map for actual RAM usage |
| vTaskDelayUntil returns immediately (busy loop) | Wake time already elapsed — task ran too long or tick wrapped | Ensure execution time < period; check for priority inversion blocking the task |
| micro-ROS publishes stop after agent restart | No reconnection logic — old session entities become invalid | Implement state machine: WAITING_AGENT → AVAILABLE → CONNECTED → DISCONNECTED |
| SPI data corruption during micro-ROS publish | SPI mutex not taken — micro-ROS task and IMU task both access SPI | Wrap all SPI access in `xSemaphoreTake(spi_mutex, portMAX_DELAY)` / `Give` |
| FreeRTOS task never runs despite being created | Priority inversion — higher-priority task never yields | Check all higher-priority tasks call `vTaskDelay` or a blocking API; reduce priorities or use time-slicing |
| ESP32 micro-ROS UDP drops messages over WiFi | WiFi interference or agent queue overflow | Use `-v5` on agent to inspect drops; add retry logic; reduce publish frequency; switch to Ethernet |
| `rcl_publish` returns `RCL_RET_ERROR` | Publisher or node in invalid state after disconnect | Tear down and reinit all rcl entities; follow reconnection state machine pattern |

## Workflow Integration

- Use this skill alongside `microcontrollers` which covers STM32 peripheral setup (timers, DMA, SPI) needed before writing FreeRTOS tasks.
- For the Linux (Raspberry Pi) side receiving micro-ROS topics, see `gpio-i2c-spi` for reading additional sensors and `ros2-node-creation` for writing the bridge nodes.
- Once firmware publishes `/odom` and `/imu/data_raw`, see `sensor-fusion-slam` to fuse them into `/odometry/filtered` using `robot_localization`.
- For production deployment of the micro-ROS agent as a systemd service, see `robot-bringup`.
- When the firmware implements E-stop or safety logic in FreeRTOS tasks, see `safety-systems` for functional safety design at the system level.
- For serial transport alternatives (plain UART without micro-ROS), see `serial-can-protocols`.
