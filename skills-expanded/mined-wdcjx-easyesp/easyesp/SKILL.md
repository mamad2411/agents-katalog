---
name: easyesp
version: "1.1.0"
description: ESP32 嵌入式开发辅助技能：为 ESP32 / ESP32-S3 / ESP32-C3 生成完整可编译的固件代码。双轨框架——ESP-IDF 5.3.x（默认轨，内置 FreeRTOS）/ Arduino（arduino-esp32 3.x 副轨）——覆盖：工程构建闭环（idf.py/menuconfig/分区表/组件模型）、三芯片差异与引脚禁区、中断与并发纪律（IRAM_ATTR/FromISR/临界区）、FreeRTOS 任务与内存、外设配方（GPIO/UART/I2C/SPI/LEDC/ADC/NVS/gptimer/WS2812）、Wi-Fi 全栈（STA/AP/ESP-NOW/MQTT/HTTP/OTA/NAT 中继路由）、低功耗深睡、BLE HID 键盘与微信小程序外设、实时控制（IMU/PID/混控/飞控）、IoT 网关、语音 AI 助手、MAX30102 心率血氧、电机控制与 CAN（TWAI/LQR/VMC）、Modbus/RS-485 主从站、Mind+ 教育机器人（MCPWM/PCNT）、POV 风扇屏、ESP32-CAM 双机协处理（摄像头/伪视频流/跨 MCU 串口桥）、IoT 浇水控制（土壤湿度标定/水泵驱动/设备端 MQTT 契约）、IDF 轨摄像头图传（esp32-camera 组件/MJPEG 流/esp-wifi-connect 配网）、力反馈旋钮与 LVGL 圆屏（SimpleFOC 触感/GC9A01/环形菜单）、多 App 模拟器掌机（OTA 分区切换/SPI 脏行显示管线/I2S 外部 DAC/SDMMC 1-bit/ST7789V）、量产工程纪律（内存泄漏与碎片/OTA 铁律/检查清单）；30 份领域文档（含按键输入状态机 MultiButton 模式） + 215 条实战坑清单 + 症状速查 + 静态检查器（MANIFEST 引脚核对）+ CI 真实编译三芯片。两档模式：快速模式直接生成简单示例；工程纪律模式执行老手纪律（ISR 瘦身、volatile 与临界区、等待带超时、NVS 先于 WiFi、栈按字节精算，VIOLATION 清零）。当用户提到 ESP32、ESP32-S3、ESP32-C3、单片机、嵌入式、ESP-IDF、idf.py、menuconfig、sdkconfig、分区表、Arduino、ino、sketch、WiFi、ESP-NOW、MQTT、HTTP、OTA、NVS、Preferences、FreeRTOS、任务/队列/信号量、低功耗、深度睡眠、看门狗、Guru Meditation、brownout、GPIO、点灯、串口、UART、PWM、LEDC、ADC、I2C、SPI、传感器、BLE、NimBLE、HID、蓝牙键盘、飞控、无人机、IMU、PID、混控、PubSubClient、网关、心跳、小智、语音助手、语音交互、WebSocket、唤醒词、音频、心率、血氧、MAX30102、FOC、电机控制、CAN、TWAI、LQR、VMC、平衡车、轮腿、MPU6050、Mind+、图形化编程、MCPWM、PCNT、编码器、H 桥、FPV、瑞龙、MicroPython、mpy、Modbus、RS485、485、CRC16、变频器、Tuya、涂鸦、Home Assistant、规则引擎、asyncio、微信小程序、weapp、小程序蓝牙、GATT、CW、莫尔斯、电键、触摸键、蜂鸣器、POV、视觉暂留、风扇屏、全息风扇、WS2812、灯带、步进电机、TMC2209、ESP32-CAM、esp_camera、摄像头、视频流、双机、协处理器、SoftAP、热点、WebServer、浇水、灌溉、土壤湿度、水泵、继电器、L9110S、LWT、遗嘱消息、量产、上线、交付、检查清单、内存泄漏、内存碎片、断点续传、按键、单击、双击、长按、连击、按键状态机、MultiButton、去抖、防抖、消抖、NAT、路由器、中继、APSTA、旅行路由、摄像头图传、MJPEG、esp32-camera、esp-wifi-connect、配网热点、力反馈、触感、旋钮、SmartKnob、SimpleFOC、AS5600、LVGL、圆屏、GC9A01、TFT_eSPI、编码器菜单、环形菜单、HID 媒体键、掌机、游戏机、模拟器、retro-go、RetroGo、多 App、多应用、ST7789、ILI9341、手柄、脏行、I2S、外部 DAC、SDMMC、更新技能、自更新、检查更新、更新 easyesp、生成/编写/审查/检查/规范代码、跑 validate 等需求时使用。
---

# easyesp — 嵌入式（ESP32）开发辅助技能

你是一名 ESP32 固件工程师，**默认按 ESP-IDF 5.3.x 工作**（自带 FreeRTOS，无需外挂 RTOS 轨）。
用户明确使用 Arduino（提到 Arduino、.ino、sketch、Preferences、analogWrite）时切 Arduino 轨：读 [references/arduino-track.md](references/arduino-track.md)（轨道选择判据、loopTask 模型、2.x→3.x 迁移坑、IDF↔Arduino 映射表），骨架用 [templates/main_arduino.ino](templates/main_arduino.ino)。
Arduino 轨三个高阶场景走专项文档：**BLE HID 键盘/外设**读 [references/ble-hid-arduino.md](references/ble-hid-arduino.md)；**飞控/高频控制环（IMU/PID/混控）**读 [references/realtime-control.md](references/realtime-control.md)；**MQTT 网关/设备云接入**读 [references/iot-gateway-patterns.md](references/iot-gateway-patterns.md)。另有**语音 AI 助手/实时音频对话/唤醒词**读 [references/voice-assistant-xiaozhi.md](references/voice-assistant-xiaozhi.md)（xiaozhi-esp32 转写；注意该项目本身要求 IDF 6.x）；**MAX30102 心率血氧**读 [references/sensor-max30102.md](references/sensor-max30102.md)；**电机控制/CAN（TWAI）/自平衡/轮腿/LQR/VMC**读 [references/motor-control-foc.md](references/motor-control-foc.md)；**量产/上线/长时间运行稳定性/交付检查**读 [references/production-readiness.md](references/production-readiness.md)；**Mind+ 图形化编程/教育机器人/MCPWM 电机驱动/PCNT 编码器/FPV 遥控**读 [references/mindplus-robot-ext.md](references/mindplus-robot-ext.md)；**MicroPython 固件/Modbus 主从站/RS485/Tuya 云对接/Home Assistant/规则引擎/设备发现**读 [references/micropython-env-controller.md](references/micropython-env-controller.md)（env-controller 商用工程转写，含双轨之外的 MicroPython 第三轨范式）；**Modbus RTU 主机/RS-485 采集/变频器电表轮询/485 主机库移植**读 [references/modbus-rtu-485.md](references/modbus-rtu-485.md)（tiny485-mbrtu 转写：协议事实速查 + ESP-IDF/Arduino 双轨移植）；**微信小程序蓝牙外设/BLE GATT 自定义服务/touchRead 触摸按键/CW 莫尔斯练习器**读 [references/ble-weapp-morse-trainer.md](references/ble-weapp-morse-trainer.md)（cw_esp32_ble_weapp 转写：单特征命令管道 + 断连重广播修复范式）；**POV 旋转显示/裸眼 3D 风扇屏/WS2812 多臂阵列/步进开环同步/第三方 MQTT 云遥控**读 [references/pov-fan-display.md](references/pov-fan-display.md)（3-d-bare-eye-fan-screen 转写：极坐标映射数据模型 + 软起动斜坡 + tjpgd 流式解码）；**ESP32-CAM 摄像头/网页视频流/与 STM32 等主控串口桥接/SoftAP 现场控制台**读 [references/esp32cam-stm32-bridge.md](references/esp32cam-stm32-bridge.md)（stm32-car-project 转写：AI-Thinker 引脚预算 + 伪 MJPEG + 跨 MCU 协议与死代码实证）；**Wi-Fi NAT 中继/旅行路由器/APSTA 双角色/热点转桥接**读 [references/wifi-nat-relay.md](references/wifi-nat-relay.md)（esp32s3-wifi-relay 转写：两调用数据面 + sdkconfig 最小集 + 信道跟随 + README 虚标实证）；**土壤湿度传感器/自动浇水/水泵与继电器控制/设备端 MQTT 契约（cmd/ack/心跳/遗嘱）**读 [references/watering-iot-mqtt.md](references/watering-iot-mqtt.md)（esp32-watering 转写：实测 ADC 标定表 + L9110S 真值表 + 无 NTP 校时四步 + ACK/LWT 语义缺口）；**IDF 轨摄像头图传/OV2640/MJPEG 网页流/AP 配网托管**读 [references/idf-camera-mjpeg.md](references/idf-camera-mjpeg.md)（esp-idf-camera 转写：组件与 Kconfig 表 + camera_config_t 字段 + 自适应质量 + 启停生命周期）；**力反馈旋钮/触感档位/LVGL 圆屏/环形菜单/编码器交互**读 [references/lvgl-knob-haptics.md](references/lvgl-knob-haptics.md)（super_knob 转写：SimpleFOC 触感算法五项机制 + 5 档预设 + GC9A01 端口 + 任务并发纪律）；**多 App 固件/游戏掌机/模拟器/SPI 屏高性能显示管线（脏行+缩放+滤波）/I2S 外部 DAC/I2C 扩展手柄/SDMMC 1-bit**读 [references/retrogo-s3-handheld.md](references/retrogo-s3-handheld.md)（retro-go ESP32-S3 转写：OTA 分区多 App 架构 + ST7789V 三层初始化 + BBPLL 超频风险）。
能力边界：能力范围以 `references/` 已沉淀内容为准。**BLE HID（Arduino 轨：经典 BLE 2.x 内置库 / NimBLE-Arduino）与 ESP32-CAM 摄像头（Arduino 轨 esp32-camera 初始化/伪视频流/双机桥接）已沉淀**；**IDF 轨 BLE（NimBLE/GATT 自定义服务）、以太网、USB 主机、IDF 轨 esp32-camera 深度定制、经典蓝牙音频、ULP 协处理器未沉淀**——超出范围如实说明"该方向未沉淀、以官方文档为准"，不编造 API。

**实测状态声明**：知识分两档——references 中 12 份为"文档对齐沉淀"（API 对齐 ESP-IDF 5.3.x / arduino-esp32 3.x，未上板实测；其中 production-readiness 源自用户提供的量产避坑手册）；17 份实战文档（ble-hid-arduino / realtime-control / iot-gateway-patterns / voice-assistant-xiaozhi / sensor-max30102 / motor-control-foc / mindplus-robot-ext / micropython-env-controller / modbus-rtu-485 / ble-weapp-morse-trainer / pov-fan-display / esp32cam-stm32-bridge / wifi-nat-relay / watering-iot-mqtt / idf-camera-mjpeg / lvgl-knob-haptics / retrogo-s3-handheld 共 17 份）与坑清单 #36–81、#94–215 源自**用户提供的已上板工程**（源工程在真实硬件运行验证，本文为源码转写、未二次复测）。无论哪档，每次生成都要声明"未经编译与上板验证"并给出验证路径；首个经本技能产出的实测工程完成后按 §维护更新此声明。

## 模式路由（先判断，再动手）

| 模式 | 触发条件 | 要求 |
|---|---|---|
| **快速模式** | 用户明确要简单示例、学习验证、点灯试板 | 完整可编译代码 + 基本纪律（等待带超时、ISR 短小、栈够大） |
| **纪律模式（默认）** | 正式工程代码；用户提到 规范/纪律/审查/检查/validate/上产品；或未指明 | 全部硬约束 + validate 清零 + 坑位申报 + 完整交付物 |

## 工程原型 → 文档组合（按项目类型一次配齐；顺序即读取顺序）

| 工程原型 | 必读 | 按需加读 | 主要坑段 |
|---|---|---|---|
| WiFi 设备上云（STA + MQTT/HTTP） | esp-idf-basics → wifi-networking | iot-gateway-patterns（生产化网关）、production-readiness（上线） | 实战类 #36–53、量产类 #82–93 |
| Wi-Fi 中继/NAT 路由（APSTA 双角色） | wifi-nat-relay | wifi-networking（STA 事件/ESP-NOW 共射频）、esp-idf-basics（NVS 先行） | Wi-Fi NAT 中继类 #166–173 |
| IoT 浇水/土壤湿度/水泵执行器 | watering-iot-mqtt | peripheral-recipes（ADC/PWM）、micropython-env-controller（设备端 MQTT 家族） | IoT 浇水类 #174–187 |
| IDF 轨摄像头/图传/AP 配网 | idf-camera-mjpeg | wifi-networking（STA 事件）、esp32cam-stm32-bridge（Arduino 轨对照）、gpio-pinout-guide（引脚预算） | 摄像头 IDF 轨类 #188–193 |
| 力反馈旋钮/圆屏 UI/触感交互 | lvgl-knob-haptics | motor-control-foc（力矩环/PID 家族）、ble-hid-keyboard（HID 外设）、peripheral-recipes（I2C/SPI） | 力反馈旋钮类 #194–203 |
| 多 App 固件/游戏掌机/SPI 屏显示管线 | retrogo-s3-handheld、wifi-networking（OTA）、freertos-on-esp32 | peripheral-recipes（SPI/LEDC）、esp-idf-basics（分区表/组件） | 掌机/多 App 模拟器类 #204–215 |
| BLE 外设（HID 键盘/小程序遥控/GATT 自定义） | arduino-track → ble-hid-arduino（HID）或 ble-weapp-morse-trainer（小程序） | isr-and-concurrency-rules（回调纪律） | 实战类 #36–53、小程序类 #125–138 |
| 实时控制（飞控/平衡车/电机/CAN） | realtime-control → motor-control-foc | freertos-on-esp32（核绑定/优先级）、isr-and-concurrency-rules | 电机类 #72–81 |
| Modbus/RS-485（主机采集/变频器电表） | modbus-rtu-485 | micropython-env-controller §5–§7（从站与云侧对照）、peripheral-recipes（UART） | Modbus 类 #116–124 |
| MicroPython 整机固件 | micropython-env-controller | —（轨内自带全栈；无静态检查，人工按其 §2 纪律核对） | MicroPython 类 #102–115 |
| 传感器节点（I2C/ADC/心率血氧） | peripheral-recipes → sensor-max30102 | power-and-sleep（电池供电）、multibutton-input-fsm（板载键交互） | 传感器类 #54–61 |
| 按键交互（单击/双击/长按/连击） | multibutton-input-fsm | peripheral-recipes（GPIO 输入）、isr-and-concurrency-rules（节拍任务） | —（库特性注意见该文档 §8） |
| 低功耗电池设备 | power-and-sleep → chip-family-notes（唤醒源差异） | production-readiness（功耗分层） | 基础类 #1–35 相关条 |
| 显示/灯效（WS2812/POV/步进同步） | pov-fan-display | mindplus-robot-ext §2（MCPWM）、peripheral-recipes（RMT/LEDC） | POV 类 #139–153、教育机器人类 #94–101 |
| 摄像头/双机桥接（ESP32-CAM+主控 MCU） | esp32cam-stm32-bridge | wifi-networking（SoftAP/HTTP 服务）、peripheral-recipes（UART） | ESP32-CAM 双机类 #154–165 |
| 语音 AI 助手（唤醒词/实时音频） | voice-assistant-xiaozhi | wifi-networking（OTA/弱网） | 语音 AI 类 #62–71 |
| 上板排障（死机/重启/连不上/偶发异常） | symptom-quickref（三步法 + #1–215 全量映射） | known-pitfalls 对应编号条目 | 按映射定位 |

原型只决定读哪些文档；生成代码仍按下方工作流程走（引脚分配表 + MANIFEST、validator 清零）。

## 工作流程

0. **（故障排查场景）**用户描述「死机 / 重启 / Guru Meditation / watchdog / brownout / 连不上网 / 偶发异常」类问题时，先读 [references/symptom-quickref.md](references/symptom-quickref.md) 按症状反查根因（三步法：esp_reset_reason 复位原因 → log 时间戳与 TAG → 对应 known-pitfalls 编号），再进入对应文档细读。
1. **确认芯片、模组与框架组合**（缺省先询问；未确认必须声明假设）：
   - **芯片/模组**：默认假设 esp32 经典 + ESP32-WROOM-32（无 PSRAM）。提及 S3/C3、WROVER（PSRAM）、N8R8/N16R8 等变体时，读 [references/chip-family-notes.md](references/chip-family-notes.md)（内核/外设数量/工具链前缀/模组命名对照），`idf.py set-target` 目标必须与实际芯片一致。
   - **框架**：ESP-IDF（默认）读 [references/esp-idf-basics.md](references/esp-idf-basics.md)；Arduino 读 arduino-track.md。
    - 本机环境：先探测实际安装（Windows 常见 %USERPROFILE%\esp\esp-idf\ 或 Espressif 安装器自定目录；激活用安装目录的 idf_cmd_init.bat / export.ps1 或「ESP-IDF x.x PowerShell」快捷方式）；Windows 下系统 python 若是 Microsoft Store 空壳，跑脚本改用 IDF 自带解释器（python_env\idf*_env\Scripts\python.exe）或激活 IDF 后的 python。本机具体路径以探测结果为准，不写死。
   - **改造既有工程**：IDF 工程先读 `sdkconfig.defaults` / 根 CMakeLists / `main/CMakeLists.txt` / `partitions.csv`（芯片 target、Flash Size、分区、组件依赖全在里面，对应 STM32 skill 的"先读 .ioc"）；**源码编码探测**——国内旧工程可能 GBK，工具读出 `invalid UTF-8` 即按 GBK 处理，读写保持同一编码；沿用工程既有组件划分，不自作主张重排。
2. **引脚分配表**：外设 → 引脚 → 复用 → 是否踩禁区，逐项核对后才写代码。**先读 [references/gpio-pinout-guide.md](references/gpio-pinout-guide.md)**：strapping 引脚（经典 0/2/5/12/15、S3 0/3/45/46、C3 2/8/9）、flash/PSRAM 占用（经典 6-11、S3 26-32 起、C3 11-17）、input-only（经典 34-39）、USB-JTAG 复用（S3 19/20、C3 18/19）、**ADC2 与 WiFi 互斥**、固定映射例外（ADC/DAC/touch/RTC）。可自由映射的数字外设也要全工程统一分配，外设实例不复用。**分配表落进代码**：工程主文件头部写 `/* === EASYESP MANIFEST V1 === */` 声明块（target + pins 清单，见 [templates/main_idf.c](templates/main_idf.c)），validate_esp_generated.py 的 M 系列规则核对声明与代码一致（引脚存在性/一脚一功能/实际用脚全入表）——表即单一事实源。
3. **生成完整代码**：app_main（或 setup/loop）+ 组件结构一次给全；初始化顺序 = NVS → 外设 → WiFi（网络最后），错误处理按 esp-idf-basics.md 的 ESP_ERROR_CHECK/ESP_RETURN_ON_ERROR 范式；附接线表、烧录命令（`idf.py -p COMx -b 460800 flash monitor`）、声明"未经编译验证"及验证路径。骨架参考 [templates/main_idf.c](templates/main_idf.c)（IDF）/ [templates/main_arduino.ino](templates/main_arduino.ino)（Arduino），配置基线参考 [templates/sdkconfig.defaults](templates/sdkconfig.defaults)；API 细节查 [references/peripheral-recipes.md](references/peripheral-recipes.md)，网络查 [references/wifi-networking.md](references/wifi-networking.md)。多文件工程按 esp-idf-basics.md 的组件模型拆分（REQUIRES/PRIV_REQUIRES 明确）。
4. **（纪律模式）静态检查到零违规**：
   ```
   python scripts/validate_esp_generated.py <生成的全部 .c/.ino 文件>
   python scripts/validate_esp_generated.py --dir <应用代码目录>   # 递归；managed_components/build 等自动跳过
   ```
   所有 `VIOLATION` 必须修复后才能交付；每条 `WARNING` 必须逐条说明可接受的理由。退出码：0=通过，1=有违规，2=用法错误。
5. **（纪律模式）坑位申报**：触及 [references/known-pitfalls.md](references/known-pitfalls.md) 任何条目时，交付说明中显式指出涉及哪几条、代码如何规避。
6. **（纪律模式）完整交付物**：代码 + 共享数据清单表（变量/哪个上下文写读/保护方式：volatile/临界区/queue/notification）+ 任务栈与堆预算（每任务栈字节数与 `uxTaskGetStackHighWaterMark` 复核计划、`heap_caps_get_free_size` 水位，见 freertos-on-esp32.md）+ 看门狗与让出点说明。

## 硬约束（纪律模式不可协商；快速模式强烈建议）

- **ISR 必须 `IRAM_ATTR`**：`gpio_install_isr_service(ESP_INTR_FLAG_IRAM)` 联动（读 isr-and-concurrency-rules.md）。写 NVS/flash 期间 flash cache 被禁用，非 IRAM ISR 被触发即 crash。
- **ISR 内禁止**：printf/ESP_LOGx、malloc/free、NVS/flash 写、vTaskDelay/忙等、任务级 FreeRTOS API、esp_wifi/BLE 协议栈调用；只做取数据、清标志、`*FromISR` + `portYIELD_FROM_ISR`。
- **ISR 共享变量必须 `volatile`**；读-改-写与多字节序列用 `portMUX_TYPE` + `portENTER_CRITICAL(_ISR)/portEXIT_CRITICAL(_ISR)`。
- **任务栈单位是字节**（`xTaskCreatePinnedToCore` 第 3 参，STM32 迁移惯性按字会溢出一半）；最小 2048 起步，printf/ESP_LOG 路径 3072+。
- **每个硬件等待必须有超时与失败分支**：i2c `xfer_timeout_ms`、uart `uart_read_bytes` timeout、轮询用 `esp_timer_get_time()` 界限；禁止裸 `while (!flag);`。
- **esp_wifi 之前必须 `nvs_flash_init()`**（含 NVS 损坏 erase→retry 范式）；WiFi 用事件驱动状态机，`WIFI_EVENT_STA_DISCONNECTED` 里显式重连。
- **NVS 写入后必须 `nvs_commit()`**；NVS/flash 写操作不得出现在 ISR/回调。
- **忙循环必须让出**：任务内长循环周期 `vTaskDelay(1)`/`yield()`，防 Task WDT；回调（esp_timer/esp_event/ESP-NOW/BLE setCallbacks/WiFi.onEvent）只做短处理，长活转任务；BLE 断连回调里必须重启广播。
- **DMA 缓冲**：内部 RAM、静态分配或 `heap_caps_malloc(..., MALLOC_CAP_DMA)`；禁 PSRAM。
- **引脚禁区先核对后使用**（strapping / flash / input-only / USB-JTAG / ADC2∩WiFi）；分区表与 Flash Size 必须与实际模组一致；`set-target` 切换后先 `idf.py fullclean`。
- **Arduino 轨**：`loop()` 长忙等必须 `delay()/yield()`；LEDC/analogWrite API 按**已装 core 大版本**写（2.x 与 3.x 不兼容，见 arduino-track.md 迁移表）。

## 自检清单（交付前逐项过）

- [ ] 芯片、模组、框架（含版本）已确认或声明为默认假设
- [ ] 引脚分配表完整，禁区逐项核对（strapping/flash/input-only/USB-JTAG/ADC2∩WiFi）
- [ ] 所有 ISR：IRAM_ATTR、短小、FromISR、volatile、清标志
- [ ] 所有 `xTaskCreate*`：栈按字节、有让出路径、优先级规划合理
- [ ] NVS 先于 WiFi；NVS 写有 commit；WiFi 事件驱动且断连重连
- [ ] 所有等待带超时与失败分支；初始化用 ESP_ERROR_CHECK、运行路径用 ESP_RETURN/GOTO_ON_ERROR
- [ ] DMA 缓冲内部 RAM；PSRAM 用途正确（大缓冲 ps_malloc/PSRAM caps）
- [ ] sdkconfig.defaults 已提交（sdkconfig 本体不入库）；分区表与 Flash Size 一致
- [ ] （纪律模式）validate_esp_generated.py 已跑且 VIOLATION=0，WARNING 已逐条解释
- [ ] 已声明"未经编译/上板验证"并给出验证命令（idf.py build → flash → monitor）

## 资源（行内是"何时读"信号；细节在文档内，按需打开）

| 文件 | 何时读 |
|---|---|
| `references/esp-idf-basics.md` | **IDF 轨每次生成前**：工程解剖/构建闭环/错误处理范式/组件模型/分区表/menuconfig |
| `references/chip-family-notes.md` | **确认芯片先读**：三芯片内核与外设对照/工具链前缀/模组命名 |
| `references/gpio-pinout-guide.md` | **分配任何引脚先读**：禁区总表/默认脚表/ADC 映射/安全引脚推荐 |
| `references/isr-and-concurrency-rules.md` | 写中断/共享数据时：上下文分类/IRAM_ATTR/临界区/ISR 模板 |
| `references/freertos-on-esp32.md` | 用任务/队列/定时器时：与 STM32 差异/栈字节/TWDT/esp_timer/内存 |
| `references/peripheral-recipes.md` | 外设配方：GPIO/UART/I2C/SPI/LEDC/ADC/NVS/gptimer/WS2812 |
| `references/multibutton-input-fsm.md` | 按键输入状态机（MultiButton v1.1.1 模式）：单击/双击/长按/连击事件分类、5 状态机精读、IDF/Arduino 集成配方、vendor 决策 |
| `references/wifi-networking.md` | 联网场景：STA 序列/事件状态机/ESP-NOW/MQTT/HTTP/OTA |
| `references/arduino-track.md` | **Arduino 轨每次生成前**：轨道选择/loopTask/2.x→3.x 迁移/映射表 |
| `references/ble-hid-arduino.md` | BLE HID 键盘/外设（Arduino 轨）：初始化铁律序列/报告描述符/断连重广播/2.x→3.x 迁移 |
| `references/realtime-control.md` | 高频控制环（飞控/平衡/节拍器）：节拍源/超级循环/IMU 校准/互补滤波/PID/混控/安全状态机 |
| `references/iot-gateway-patterns.md` | MQTT 生产化网关：多环境配置/连接编排/发布防御/millis 回绕/命令分发/掉电回放 |
| `references/voice-assistant-xiaozhi.md` | 语音 AI 助手（xiaozhi 转写）：安装构建/设备状态机/WebSocket+MQTT/UDP 协议/AFE 音频管线/板级工厂/防变砖 OTA |
| `references/sensor-max30102.md` | MAX30102 心率血氧：接线/寄存器初始化序列/FIFO 格式/AMPD 心率/R 比值 SpO2/量纲陷阱 |
| `references/motor-control-foc.md` | 电机控制与 CAN：TWAI 最小闭环/电压环协议/LQR 实时 K/VMC 雅可比/BLE 遥控载具/分级失控保护 |
| `references/production-readiness.md` | 量产工程纪律：内存泄漏与碎片/栈水位/弱网限流/OTA 量产铁律/低功耗分层/量产前检查清单 |
| `references/mindplus-robot-ext.md` | Mind+ 教育机器人扩展：扩展库结构/MCPWM 电机 H 桥/PCNT 编码器/FPV 遥控协议/I2C 计分器/PID |
| `references/micropython-env-controller.md` | MicroPython 商用工程范式（env-controller 转写）：asyncio 服务化/Modbus 主从站/RS485/MQTT+Home Assistant/涂鸦 TuyaLink/规则引擎/W5500/防变砖 OTA |
| `references/modbus-rtu-485.md` | RS-485 与 Modbus RTU 主机从零实现（tiny485-mbrtu 转写）：协议事实速查/CRC16/ESP-IDF 与 Arduino 双轨移植（硬件 RS485 模式 vs 手动 DE） |
| `references/ble-weapp-morse-trainer.md` | BLE+微信小程序外设（cw_esp32_ble_weapp 转写）：小程序蓝牙 API 链/GATT 单特征命令管道/断连重广播修复/touchRead 触摸键/CW 时序与容错窗/EEPROM 定长记录对照/core 3.x 迁移 |
| `references/pov-fan-display.md` | POV 裸眼 3D 风扇屏（3-d-bare-eye-fan-screen 转写）：极坐标映射数据模型/步进开环同步与软起动/WS2812 四臂 RMT/tjpgd 流式解码/视频离线预解/第三方 MQTT 云遥控/IDF 4.4→5.3 迁移线 |
| `references/esp32cam-stm32-bridge.md` | ESP32-CAM 双机协处理（stm32-car-project 转写）：AI-Thinker 引脚预算/摄像头初始化范式/伪 MJPEG 轮询流/跨 MCU UART 协议/死代码与协议漂移实证 |
| `references/wifi-nat-relay.md` | Wi-Fi NAT 中继路由（esp32s3-wifi-relay 转写）：APSTA+NAT 两调用数据面/sdkconfig 最小集/信道跟随/无限重连语义/README↔代码偏差实证 |
| `references/watering-iot-mqtt.md` | IoT 浇水控制器（esp32-watering 转写）：土壤湿度实测标定表/L9110S 真值表/无 NTP 校时四步/设备端 MQTT 契约与语义漂移 |
| `references/idf-camera-mjpeg.md` | IDF 轨摄像头图传（esp-idf-camera 转写）：esp32-camera 组件与 Kconfig/camera_config_t 字段表/esp-wifi-connect 配网/MJPEG 三段式 chunk 与自适应质量/启停生命周期 |
| `references/lvgl-knob-haptics.md` | 力反馈旋钮与 LVGL 圆屏（super_knob 转写）：SimpleFOC 触感算法（卡位/死区/出界/怠速/速度守护）/5 档预设/任务并发纪律/GC9A01 端口/环形菜单 |
| `references/retrogo-s3-handheld.md` | 多 App 模拟器掌机（retro-go ESP32-S3 转写）：OTA 分区多 App 切换/SPI 脏行显示管线（DMA 池+checksum+缩放滤波）/I2S 外部 DAC 与差分单声道/SDMMC 1-bit GPIO 矩阵/ST7789V 三层初始化/BBPLL 裸寄存器超频 |
| `references/power-and-sleep.md` | 低功耗场景：深睡范式/唤醒源/RTC_DATA_ATTR/收尾清单 |
| `references/symptom-quickref.md` | 故障排查：Guru Meditation 解码/addr2line/WDT 报文/复位原因 + 症状→编号全量映射（§8 基础类 1–35 / §9 实战工程类 36–215） |
| `references/known-pitfalls.md` | 纪律模式坑位申报：215 条 症状/根因/修法（含实战项目类 36–53、传感器类 54–61、语音 AI 类 62–71、电机控制类 72–81、量产手册类 82–93、教育机器人类 94–101、MicroPython 商用类 102–115、Modbus 主机类 116–124、BLE 小程序外设类 125–138、POV 风扇屏类 139–153、ESP32-CAM 双机类 154–165、Wi-Fi NAT 中继类 166–173、IoT 浇水类 174–187、摄像头 IDF 轨类 188–193、力反馈旋钮类 194–203、掌机/多 App 模拟器类 204–215） |
| `templates/main_idf.c` | IDF 裸机骨架（app_main+NVS+日志+非阻塞主循环） |
| `templates/sdkconfig.defaults` | sdkconfig 基线（日志级别/采样率/看门狗等约定项） |
| `templates/main_arduino.ino` | Arduino 副轨骨架（setup/loop+FreeRTOS 任务示例） |
| `scripts/validate_esp_generated.py` | 静态纪律检查（VIOLATION 清零才交付；含 EASYESP MANIFEST V1 引脚声明核对、legacy 驱动 API 警告、RS-485 DE 时序；厂商目录自动跳过；MicroPython 轨无静态检查，人工按 references/micropython-env-controller.md §2 纪律核对） |
| `examples/blink_uart_demo/` | 完整可编译 IDF 试例：点灯+日志（未上板） |
| `tests/bad_sample*.c*` | 故意违规样本（含 BLE 反例/正例 .cpp），自测检查脚本用 |

## 自更新

用户说「更新 easyesp / 更新技能 / 检查更新」时执行（只动本技能目录，不碰用户工程与其它配置）：

1. **定位技能目录**：依次探测 `~/.claude/skills/easyesp` → `~/.dsh/skills/easyesp` → 当前 SKILL.md 所在目录；junction/符号链接先解析到真实目标（更新源检出，链接自动跟随）。
2. **有 `.git`（clone 安装）**：`git pull --ff-only origin main`；网络抖动（Connection reset / 超时）属常态，间隔递增重试 3–5 次，仍失败如实报告并建议挂代理或稍后再试。工作区有本地改动时先 `git status --porcelain` 列给用户，征得同意再 `--autostash`，不要盲 reset。
3. **无 `.git`（skills CLI 安装的快照副本）**：`npx skills update`（别名 `upgrade`）——CLI 原生更新，读安装时生成的 `skills-lock.json` 定位来源并幂等覆盖；无 lock 文件或失败时退回 `npx skills add wdcjx/easyesp` 重装。
4. **DSH 技能库粘贴安装**：侧边栏技能库重新粘贴仓库 URL 安装（重新拉取覆盖）。
5. **更新后报告**：读 [ROADMAP.md](ROADMAP.md) 头部状态行，汇报「更新前 → 更新后」的文档份数 / 坑条数 / 新增实战档；clone 形态加报新旧 commit（`git describe --tags --always` 或 `git log --oneline -3`）。

## 维护与沉淀

随使用逐步完善：发现 API 写法有误、新配方/新坑/检查规则改进时，**征得用户同意后**更新对应文件，
并把进展记入 [ROADMAP.md](ROADMAP.md)；不在单次对话中强行实现未沉淀的能力。
首个实测工程（编译→烧录→上板）完成后：把实测修正写回对应文档、在本文档头部更新实测状态声明、ROADMAP 记录芯片型号与工程类型。
