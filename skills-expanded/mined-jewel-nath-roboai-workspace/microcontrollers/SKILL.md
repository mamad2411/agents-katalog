---
name: microcontrollers
description: MCU development with STM32, ESP32, Arduino, Nordic nRF5x. HAL patterns, interrupt handling, timers, DMA, and firmware architecture.
category: embedded
tags: [microcontroller, stm32, esp32, arduino, nordic, mcu, firmware, embedded, hal]
version: "1.0.0"
---

# Microcontrollers

Microcontrollers are the foundation of robot hardware interfaces. This skill covers MCU selection, peripheral configuration, and firmware architecture.

## When to Use

- Selecting MCU for sensor/actuator interfaces
- Configuring GPIO, timers, ADC, DAC, PWM
- Implementing interrupt-driven architectures
- Setting up DMA for high-throughput data
- Managing power modes and sleep states
- Writing bootloader and firmware update systems
- Debugging hard faults and timing issues
- Implementing real-time control loops

## Quick Start

```bash
# Install STM32 tools
sudo apt install gcc-arm-none-eabi openocd

# Install ESP-IDF
git clone -b v5.1 --recursive https://github.com/espressif/esp-idf.git
./esp-idf/install.sh

# Install Arduino CLI
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Install Nordic tools
# Download from https://www.nordicsemi.com/Products/Development-tools/nRF-Command-Line-Tools
```

## Core Concepts

### 1. MCU Selection Criteria

Choose the right MCU for your application.

| Criteria | Light Sensor | Motor Drive | ROS2 MCU |
|----------|-------------|-------------|----------|
| CPU | Cortex-M0+ | Cortex-M4/M7 | Cortex-M7 |
| Clock | 48 MHz | 168 MHz+ | 480 MHz |
| Flash | 64 KB | 512 KB | 2 MB |
| RAM | 8 KB | 128 KB | 1 MB |
| FPU | No | Yes (single) | Yes (double) |
| Ethernet | No | Optional | Yes |
| CAN FD | No | Yes | Yes |
| Cost | $1-3 | $5-15 | $10-25 |

**Decision matrix:**

```python
def select_mcu(requirements):
    candidates = {
        'STM32F103': {'flash': 128, 'ram': 20, 'clock': 72, 'fpu': False, 'cost': 3},
        'STM32F407': {'flash': 1024, 'ram': 192, 'clock': 168, 'fpu': True, 'cost': 8},
        'STM32H743': {'flash': 2048, 'ram': 1024, 'clock': 480, 'fpu': True, 'cost': 15},
        'ESP32-S3': {'flash': 8192, 'ram': 512, 'clock': 240, 'fpu': True, 'cost': 4, 'wifi': True},
        'nRF52840': {'flash': 1024, 'ram': 256, 'clock': 64, 'fpu': True, 'cost': 5, 'ble': True},
    }
    
    scores = {}
    for name, specs in candidates.items():
        score = 0
        
        # Must meet minimum requirements
        if specs['flash'] < requirements['flash']:
            continue
        if specs['ram'] < requirements['ram']:
            continue
            
        # Score based on fit
        score += specs['clock'] / requirements.get('clock', 72)
        score += 2 if specs['fpu'] == requirements.get('fpu', False) else 0
        score -= specs['cost'] / 10  # Cost penalty
        
        # Bonus for connectivity
        if requirements.get('wifi') and specs.get('wifi'):
            score += 5
        if requirements.get('ble') and specs.get('ble'):
            score += 5
            
        scores[name] = score
    
    return max(scores, key=scores.get) if scores else None
```

### 2. STM32 HAL Architecture

Hardware Abstraction Layer provides portable peripheral access.

**Clock configuration (HSE + PLL):**

```c
// STM32F4 system clock: 168 MHz from 8 MHz HSE
void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    // Enable HSE oscillator
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    
    // PLL: 8 MHz / 8 (M) * 336 (N) / 2 (P) = 168 MHz
    RCC_OscInitStruct.PLL.PLLM = 8;
    RCC_OscInitStruct.PLL.PLLN = 336;
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
    RCC_OscInitStruct.PLL.PLLQ = 7;  // 48 MHz for USB
    
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }

    // Configure bus clocks
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK |
                                  RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;   // 168 MHz
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;    // 42 MHz
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;    // 84 MHz

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK) {
        Error_Handler();
    }
}
```

**GPIO configuration:**

```c
void GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Enable GPIO clocks
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();

    // Configure LED (PC13) as output
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    // Configure button (PA0) as input with interrupt
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // Enable and set EXTI interrupt priority
    HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

void EXTI0_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        // Button pressed
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
    }
}
```

**Timer with PWM generation:**

```c
TIM_HandleTypeDef htim2;

void TIM2_Init(void) {
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 84 - 1;  // 84 MHz / 84 = 1 MHz
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 1000 - 1;   // 1 MHz / 1000 = 1 kHz PWM
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_PWM_Init(&htim2);

    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 500;  // 50% duty cycle
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    
    HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}

void setPWM(uint16_t duty_percent) {
    if (duty_percent > 100) duty_percent = 100;
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty_percent * 10);
}
```

### 3. DMA (Direct Memory Access)

DMA enables high-throughput data transfer without CPU intervention.

**DMA for ADC scanning:**

```c
ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

#define ADC_BUFFER_SIZE 4
volatile uint16_t adc_buffer[ADC_BUFFER_SIZE];

void ADC_DMA_Init(void) {
    // Enable DMA2 clock
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    // Configure DMA
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    hdma_adc1.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
    HAL_DMA_Init(&hdma_adc1);
    
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // Configure ADC for multiple channels
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = ENABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    HAL_ADC_Init(&hadc1);
    
    // Configure channels
    ADC_ChannelConfTypeDef sConfig = {0};
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_15CYCLES;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    sConfig.Channel = ADC_CHANNEL_1;
    sConfig.Rank = 2;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Start DMA conversion
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, ADC_BUFFER_SIZE);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    // Called when half buffer is complete (HT) and full buffer (TC)
    // In circular mode, process data while DMA continues
    processADCData(adc_buffer, ADC_BUFFER_SIZE);
}
```

**DMA for UART with circular buffer:**

```c
#define UART_RX_SIZE 256
uint8_t uart_rx_buffer[UART_RX_SIZE];

void UART_DMA_Init(void) {
    // UART initialization...
    
    // Configure DMA in circular mode
    hdma_usart2_rx.Instance = DMA1_Stream5;
    hdma_usart2_rx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart2_rx.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_usart2_rx.Init.Mode = DMA_CIRCULAR;
    hdma_usart2_rx.Init.Priority = DMA_PRIORITY_HIGH;
    HAL_DMA_Init(&hdma_usart2_rx);
    
    __HAL_LINKDMA(&huart2, hdmarx, hdma_usart2_rx);
    
    // Enable idle line detection
    __HAL_UART_ENABLE_IT(&huart2, UART_IT_IDLE);
    
    // Start circular DMA reception
    HAL_UART_Receive_DMA(&huart2, uart_rx_buffer, UART_RX_SIZE);
}

void USART2_IRQHandler(void) {
    if (__HAL_UART_GET_FLAG(&huart2, UART_FLAG_IDLE)) {
        __HAL_UART_CLEAR_IDLEFLAG(&huart2);
        
        // Calculate received data length
        uint16_t data_length = UART_RX_SIZE - __HAL_DMA_GET_COUNTER(huart2.hdmarx);
        
        // Process received data
        processUARTData(uart_rx_buffer, data_length);
        
        // Restart DMA (circular mode continues automatically)
    }
    
    HAL_UART_IRQHandler(&huart2);
}
```

### 4. ESP32 Development

ESP32 combines WiFi/BLE with powerful processing.

**FreeRTOS task structure:**

```cpp
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_log.h"

static const char* TAG = "RobotMCU";

// Task handles
TaskHandle_t sensor_task_handle = NULL;
TaskHandle_t control_task_handle = NULL;

// Queue for inter-task communication
QueueHandle_t sensor_queue;

void sensor_task(void* pvParameters) {
    sensor_data_t data;
    
    while (1) {
        // Read sensors
        data.imu = readIMU();
        data.encoders = readEncoders();
        
        // Send to control task
        xQueueSend(sensor_queue, &data, portMAX_DELAY);
        
        // 1ms period
        vTaskDelay(pdMS_TO_TICKS(1));
    }
}

void control_task(void* pvParameters) {
    sensor_data_t data;
    
    while (1) {
        // Wait for sensor data
        if (xQueueReceive(sensor_queue, &data, portMAX_DELAY)) {
            // Compute control
            float output = computePID(data);
            
            // Output to motors
            setMotorOutput(output);
        }
    }
}

void app_main(void) {
    ESP_LOGI(TAG, "Starting robot MCU firmware");
    
    // Create queue
    sensor_queue = xQueueCreate(10, sizeof(sensor_data_t));
    
    // Create tasks
    xTaskCreatePinnedToCore(
        sensor_task,          // Function
        "sensor_task",        // Name
        4096,                 // Stack size
        NULL,                 // Parameter
        5,                    // Priority
        &sensor_task_handle,  // Handle
        0                     // Core 0
    );
    
    xTaskCreatePinnedToCore(
        control_task,
        "control_task",
        4096,
        NULL,
        10,  // Higher priority
        &control_task_handle,
        1    // Core 1 (for low latency)
    );
}
```

**WiFi and MQTT for telemetry:**

```cpp
#include "esp_wifi.h"
#include "mqtt_client.h"

void wifi_init(void) {
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = "ROBOT_WIFI",
            .password = "secure_password",
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_wifi_start();
}

void mqtt_init(void) {
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = "mqtt://192.168.1.100:1883",
        .credentials.username = "robot",
        .credentials.authentication.password = "mqtt_pass",
    };
    
    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

void publishTelemetry(esp_mqtt_client_handle_t client, const robot_state_t* state) {
    char json[256];
    snprintf(json, sizeof(json),
        "{\"pose\":{\"x\":%.3f,\"y\":%.3f,\"theta\":%.3f},"
        "\"velocity\":{\"v\":%.3f,\"omega\":%.3f},"
        "\"battery\":%.1f}",
        state->x, state->y, state->theta,
        state->v, state->omega, state->battery);
    
    esp_mqtt_client_publish(client, "robot/telemetry", json, 0, 0, 0);
}
```

### 5. Nordic nRF52 (BLE)

Nordic chips excel at low-power wireless applications.

**BLE peripheral with custom service:**

```c
#include "nrf_sdh.h"
#include "nrf_sdh_ble.h"
#include "ble_srv_common.h"

#define ROBOT_SERVICE_UUID_BASE {0x23, 0xD1, 0xBC, 0xEA, 0x5F, 0x78, 0x23, 0x15, \
                                 0xDE, 0xEF, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00}
#define ROBOT_SERVICE_UUID 0x1400
#define MOTOR_CHAR_UUID 0x1401
#define SENSOR_CHAR_UUID 0x1402

typedef struct {
    uint16_t service_handle;
    ble_gatts_char_handles_t motor_handles;
    ble_gatts_char_handles_t sensor_handles;
} robot_service_t;

static robot_service_t m_robot_service;

uint32_t robot_service_init(void) {
    uint32_t err_code;
    ble_uuid_t ble_uuid;
    ble_uuid128_t base_uuid = ROBOT_SERVICE_UUID_BASE;
    
    // Add service UUID
    err_code = sd_ble_uuid_vs_add(&base_uuid, &m_robot_service.service_handle);
    VERIFY_SUCCESS(err_code);
    
    ble_uuid.type = m_robot_service.service_handle;
    ble_uuid.uuid = ROBOT_SERVICE_UUID;
    
    // Add service
    err_code = sd_ble_gatts_service_add(BLE_GATTS_SRVC_TYPE_PRIMARY,
                                        &ble_uuid,
                                        &m_robot_service.service_handle);
    VERIFY_SUCCESS(err_code);
    
    // Add motor control characteristic (writable)
    ble_gatts_attr_md_t attr_md;
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.read_perm);
    BLE_GAP_CONN_SEC_MODE_SET_OPEN(&attr_md.write_perm);
    
    ble_gatts_attr_t attr_char_value;
    ble_uuid.uuid = MOTOR_CHAR_UUID;
    
    uint8_t initial_value[8] = {0};
    attr_char_value.p_uuid = &ble_uuid;
    attr_char_value.p_attr_md = &attr_md;
    attr_char_value.init_len = sizeof(initial_value);
    attr_char_value.init_offs = 0;
    attr_char_value.max_len = sizeof(initial_value);
    attr_char_value.p_value = initial_value;
    
    ble_gatts_char_md_t char_md;
    memset(&char_md, 0, sizeof(char_md));
    char_md.char_props.write = 1;
    char_md.char_props.write_wo_resp = 1;
    
    err_code = sd_ble_gatts_characteristic_add(m_robot_service.service_handle,
                                               &char_md,
                                               &attr_char_value,
                                               &m_robot_service.motor_handles);
    VERIFY_SUCCESS(err_code);
    
    return NRF_SUCCESS;
}

void on_write(ble_evt_t const* p_ble_evt) {
    ble_gatts_evt_write_t const* p_evt_write = &p_ble_evt->evt.gatts_evt.params.write;
    
    if (p_evt_write->handle == m_robot_service.motor_handles.value_handle) {
        // Parse motor commands
        int16_t left_motor = (p_evt_write->data[0] << 8) | p_evt_write->data[1];
        int16_t right_motor = (p_evt_write->data[2] << 8) | p_evt_write->data[3];
        
        setMotorSpeeds(left_motor, right_motor);
    }
}

void send_sensor_data(void) {
    uint8_t data[12];
    int16_t accel[3], gyro[3];
    
    readIMU(accel, gyro);
    
    // Pack data
    for (int i = 0; i < 3; i++) {
        data[i*2] = accel[i] >> 8;
        data[i*2 + 1] = accel[i] & 0xFF;
        data[6 + i*2] = gyro[i] >> 8;
        data[6 + i*2 + 1] = gyro[i] & 0xFF;
    }
    
    // Send notification
    ble_gatts_hvx_params_t hvx_params;
    hvx_params.handle = m_robot_service.sensor_handles.value_handle;
    hvx_params.type = BLE_GATT_HVX_NOTIFICATION;
    hvx_params.offset = 0;
    hvx_params.p_len = &len;
    hvx_params.p_data = data;
    
    sd_ble_gatts_hvx(m_conn_handle, &hvx_params);
}
```

## Common Patterns

### Pattern 1: Circular Buffer for ISR Communication

```c
typedef struct {
    uint8_t buffer[256];
    volatile uint8_t head;
    volatile uint8_t tail;
} CircularBuffer;

void cb_init(CircularBuffer* cb) {
    cb->head = 0;
    cb->tail = 0;
}

bool cb_write(CircularBuffer* cb, uint8_t data) {
    uint8_t next_head = (cb->head + 1) % sizeof(cb->buffer);
    
    if (next_head == cb->tail) {
        return false;  // Buffer full
    }
    
    cb->buffer[cb->head] = data;
    cb->head = next_head;
    return true;
}

bool cb_read(CircularBuffer* cb, uint8_t* data) {
    if (cb->head == cb->tail) {
        return false;  // Buffer empty
    }
    
    *data = cb->buffer[cb->tail];
    cb->tail = (cb->tail + 1) % sizeof(cb->buffer);
    return true;
}

// ISR-safe usage
void USART_IRQHandler(void) {
    if (USART->SR & USART_SR_RXNE) {
        uint8_t data = USART->DR;
        cb_write(&rx_buffer, data);  // Write from ISR
    }
}

// Main loop processing
void process_loop(void) {
    uint8_t data;
    while (cb_read(&rx_buffer, &data)) {  // Read in main loop
        process_byte(data);
    }
}
```

### Pattern 2: Bootloader Implementation

```c
#define APP_START_ADDRESS 0x08008000  // 32KB bootloader
#define BOOTLOADER_MAGIC 0xDEADBEEF

typedef void (*app_function_t)(void);

void jump_to_application(void) {
    // Check if valid application exists
    uint32_t* app_vector_table = (uint32_t*)APP_START_ADDRESS;
    uint32_t app_stack = app_vector_table[0];
    uint32_t app_reset = app_vector_table[1];
    
    // Validate stack pointer (RAM region)
    if ((app_stack & 0x2FFF0000) != 0x20000000) {
        return;  // Invalid application
    }
    
    // Deinitialize peripherals
    HAL_RCC_DeInit();
    HAL_DeInit();
    
    // Disable interrupts
    __disable_irq();
    
    // Set vector table
    SCB->VTOR = APP_START_ADDRESS;
    
    // Set stack pointer
    __set_MSP(app_stack);
    
    // Jump to application
    app_function_t app_reset_fn = (app_function_t)app_reset;
    app_reset_fn();
}

void bootloader_main(void) {
    // Check boot reason
    if (check_firmware_update_request()) {
        enter_dfu_mode();
    }
    
    // Check for valid application
    if (verify_application_checksum()) {
        jump_to_application();
    }
    
    // Stay in bootloader mode
    while (1) {
        process_bootloader_commands();
    }
}

void enter_dfu_mode(void) {
    // Initialize USB or UART for firmware download
    // Receive and flash new firmware
    // Verify and jump to new application
}
```

### Pattern 3: Hard Fault Handler

```c
void HardFault_Handler(void) {
    __asm volatile(
        "TST LR, #4\n"          // Check which stack was used
        "ITE EQ\n"
        "MRSEQ R0, MSP\n"       // Main stack
        "MRSNE R0, PSP\n"       // Process stack
        "B HardFault_Handler_C\n"
    );
}

typedef struct {
    uint32_t r0;
    uint32_t r1;
    uint32_t r2;
    uint32_t r3;
    uint32_t r12;
    uint32_t lr;
    uint32_t pc;
    uint32_t psr;
} stack_frame_t;

void HardFault_Handler_C(stack_frame_t* stack_frame) {
    volatile uint32_t cfsr = SCB->CFSR;
    volatile uint32_t hfsr = SCB->HFSR;
    volatile uint32_t mmfar = SCB->MMFAR;
    volatile uint32_t bfar = SCB->BFAR;
    
    // Log fault information
    printf("Hard Fault!\n");
    printf("CFSR: 0x%08X\n", cfsr);
    printf("HFSR: 0x%08X\n", hfsr);
    printf("MMFAR: 0x%08X\n", mmfar);
    printf("BFAR: 0x%08X\n", bfar);
    printf("PC: 0x%08X\n", stack_frame->pc);
    printf("LR: 0x%08X\n", stack_frame->lr);
    
    // Decode fault reason
    if (cfsr & SCB_CFSR_IACCVIOL_Msk) {
        printf("Instruction access violation\n");
    }
    if (cfsr & SCB_CFSR_DACCVIOL_Msk) {
        printf("Data access violation\n");
    }
    if (cfsr & SCB_CFSR_BUSFAULTSR_Msk) {
        printf("Bus fault\n");
    }
    if (cfsr & SCB_CFSR_USGFAULTSR_Msk) {
        printf("Usage fault\n");
    }
    
    // Optional: Save to flash for post-mortem analysis
    save_fault_report(cfsr, hfsr, stack_frame);
    
    // Reset or halt
    NVIC_SystemReset();
}
```

## Anti-Patterns

### ❌ Busy-waiting in main loop
Polling flags consumes 100% CPU.

**What happens:** Wasted power, missed interrupts, poor responsiveness.

### ✅ Use interrupts and sleep
```c
while (1) {
    if (data_ready) {
        process_data();
    } else {
        __WFI();  // Wait for interrupt, saves power
    }
}
```

### ❌ Disabling interrupts for long periods
Long critical sections cause timing issues.

**What happens:** Missed sensor samples, watchdog resets.

### ✅ Short critical sections
```c
// Bad: long critical section
__disable_irq();
process_large_buffer();  // Takes 10ms
__enable_irq();

// Good: copy data quickly, process outside
__disable_irq();
memcpy(local_buffer, rx_buffer, size);  // Fast copy
rx_ready = false;
__enable_irq();
process_large_buffer(local_buffer);  // Process outside
```

### ❌ Stack overflow
Deep call stacks or large local arrays overflow.

**What happens:** Corrupted data, hard faults, unpredictable behavior.

### ✅ Check stack usage
```c
// Fill stack with pattern
void fill_stack_pattern(void) {
    uint32_t* p = (uint32_t*)stack_bottom;
    while (p < (uint32_t*)stack_top) {
        *p++ = 0xDEADBEEF;
    }
}

// Check maximum stack usage
uint32_t check_stack_usage(void) {
    uint32_t* p = (uint32_t*)stack_bottom;
    while (*p == 0xDEADBEEF && p < (uint32_t*)stack_top) {
        p++;
    }
    return (uint32_t)p - stack_bottom;  // Bytes used
}
```

### ❌ No watchdog
Software hangs without recovery.

**What happens:** Robot stuck in undefined state.

### ✅ Independent watchdog
```c
void IWDG_Init(void) {
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_64;  // 40kHz / 64 = 625 Hz
    hiwdg.Init.Reload = 625;  // 1 second timeout
    HAL_IWDG_Init(&hiwdg);
}

void refresh_watchdog(void) {
    HAL_IWDG_Refresh(&hiwdg);
}

// Call in main loop or timer interrupt
void TIM_IRQHandler(void) {
    refresh_watchdog();
}
```

## Configuration Reference

### Memory Layout (STM32F407)

| Region | Address | Size | Purpose |
|--------|---------|------|---------|
| Bootloader | 0x08000000 | 32 KB | Firmware update |
| Application | 0x08008000 | 976 KB | Main firmware |
| Config | 0x080FF000 | 4 KB | Persistent settings |
| RAM | 0x20000000 | 128 KB | Variables, stack, heap |

### Clock Tree (168 MHz)

```
HSE (8 MHz)
    |
    +--[ / M (8) ]---> 1 MHz
            |
            +--[ x N (336) ]---> 336 MHz
                        |
                        +--[ / P (2) ]---> 168 MHz (SYSCLK)
                        |
                        +--[ / Q (7) ]---> 48 MHz (USB)
```

### Power Modes

| Mode | Current | Wake Time | Use Case |
|------|---------|-----------|----------|
| Run | 100+ mA | - | Active operation |
| Sleep | 50 mA | <1 µs | Brief idle |
| Stop | 500 µA | 10 µs | Long idle |
| Standby | 5 µA | 100 µs | Power off |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Hard fault on startup | Invalid vector table | Check linker script, VTOR setting |
| Watchdog reset | Task not refreshing watchdog | Add watchdog refresh to all tasks |
| DMA corruption | Buffer not aligned | Ensure buffers are 4-byte aligned |
| SPI data wrong | Clock polarity/phase | Match CPOL/CPHA settings |
| I2C NACK | Wrong address or bus busy | Check address, add bus reset sequence |
| High current draw | Floating pins | Configure all unused pins as input pull-down |
| BLE disconnect | Power supply noise | Add decoupling capacitors, check layout |
| Slow WiFi throughput | CPU overloaded | Move tasks to different core, optimize |

## Workflow Integration

- **Before this:** Use `serial-can-protocols` for communication protocol design
- **With this:** Use `realtime-motor-control` for control algorithm implementation
- **After this:** Use `rtos-micro-ros` for ROS2 integration
- **Related:** Use `sensor-actuator-drivers` for device-specific code

## Further Reading

- "The Definitive Guide to ARM Cortex-M3/M4" by Joseph Yiu
- "Mastering STM32" by Carmine Noviello
- [STM32 HAL Reference Manual](https://www.st.com/)
- Related skills: `serial-can-protocols`, `realtime-motor-control`, `rtos-micro-ros`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering STM32, ESP32, Nordic
- Includes HAL patterns, DMA, interrupts, bootloaders