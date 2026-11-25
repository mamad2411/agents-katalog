---
name: serial-can-protocols
description: Serial communication (UART, RS232, RS485), CAN bus (CAN 2.0, CAN FD), and industrial protocols (CANopen, EtherCAT) for robot hardware interfaces.
category: hardware
tags: [serial, can, can-fd, uart, rs485, canopen, ethercat, communication, protocol]
version: "1.0.0"
---

# Serial and CAN Protocols

Industrial robots rely on robust communication protocols. This skill covers serial communication, CAN bus, and industrial fieldbus protocols.

## When to Use

- Implementing UART/RS232/RS485 drivers for sensors and actuators
- Configuring CAN bus (2.0 and FD) for motor drives
- Implementing CANopen for servo controllers
- Setting up EtherCAT for real-time distributed I/O
- Debugging protocol timing and framing issues
- Implementing Modbus RTU/TCP for PLCs
- Configuring J1939 for mobile robotics
- Troubleshooting bus contention and arbitration

## Quick Start

```bash
# Install CAN tools (Linux)
sudo apt install can-utils

# Setup virtual CAN interface
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Send test CAN frame
cansend vcan0 123#DEADBEEF

# Monitor CAN bus
candump vcan0

# Install ROS2 CAN packages
sudo apt install ros-humble-can-msgs
```

## Core Concepts

### 1. Serial Communication (UART)

UART is the foundation of most embedded communication.

**Basic UART configuration:**

```c
// STM32 HAL example
#include "stm32f4xx_hal.h"

UART_HandleTypeDef huart2;

void UART_Init(void) {
    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling = UART_OVERSAMPLING_16;
    
    if (HAL_UART_Init(&huart2) != HAL_OK) {
        Error_Handler();
    }
}

// DMA-based reception with circular buffer
#define RX_BUFFER_SIZE 256
uint8_t rx_buffer[RX_BUFFER_SIZE];

void UART_StartDMAReceive(void) {
    HAL_UART_Receive_DMA(&huart2, rx_buffer, RX_BUFFER_SIZE);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    // Called when half/full buffer complete
    // Process data in rx_buffer
    ProcessReceivedData(rx_buffer, RX_BUFFER_SIZE);
}
```

**Protocol framing (COBS):**

```cpp
// Consistent Overhead Byte Stuffing
// Ensures frame delimiter (0x00) never appears in data

class COBSFramer {
public:
    static std::vector<uint8_t> encode(const uint8_t* data, size_t len) {
        std::vector<uint8_t> encoded;
        encoded.reserve(len + len / 254 + 2);
        
        uint8_t code = 1;
        size_t code_idx = 0;
        encoded.push_back(0);  // Placeholder for code byte
        
        for (size_t i = 0; i < len; ++i) {
            if (data[i] == 0) {
                encoded[code_idx] = code;
                code_idx = encoded.size();
                encoded.push_back(0);
                code = 1;
            } else {
                encoded.push_back(data[i]);
                code++;
                if (code == 0xFF) {
                    encoded[code_idx] = code;
                    code_idx = encoded.size();
                    encoded.push_back(0);
                    code = 1;
                }
            }
        }
        
        encoded[code_idx] = code;
        encoded.push_back(0);  // Frame delimiter
        return encoded;
    }
    
    static std::vector<uint8_t> decode(const uint8_t* data, size_t len) {
        std::vector<uint8_t> decoded;
        decoded.reserve(len);
        
        size_t i = 0;
        while (i < len - 1) {  // Last byte is delimiter
            uint8_t code = data[i++];
            for (uint8_t j = 1; j < code && i < len - 1; ++j) {
                decoded.push_back(data[i++]);
            }
            if (code < 0xFF && i < len - 1) {
                decoded.push_back(0);
            }
        }
        return decoded;
    }
};
```

**Checksum calculation (CRC-16):**

```cpp
uint16_t crc16(const uint8_t* data, size_t len, uint16_t poly = 0x8005) {
    uint16_t crc = 0xFFFF;
    
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (int j = 0; j < 8; ++j) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ poly;
            } else {
                crc <<= 1;
            }
        }
    }
    
    return crc;
}
```

### 2. RS485 Multi-Drop Networks

RS485 enables robust multi-node communication over long distances.

**Hardware configuration:**

```
Master          Node 1          Node 2          Node N
  |               |               |               |
  |---------------|---------------|---------------|  A (Differential +)
  |               |               |               |
  |---------------|---------------|---------------|  B (Differential -)
  |               |               |               |
  [120Ω]        [120Ω]                          [120Ω]  (Termination)
```

**Half-duplex driver:**

```cpp
class RS485Driver {
public:
    RS485Driver(UART_HandleTypeDef* huart, GPIO_TypeDef* de_port, uint16_t de_pin)
        : huart_(huart), de_port_(de_port), de_pin_(de_pin) {
        HAL_GPIO_WritePin(de_port_, de_pin_, GPIO_PIN_RESET);  // Receive mode
    }
    
    void send(const uint8_t* data, size_t len) {
        HAL_GPIO_WritePin(de_port_, de_pin_, GPIO_PIN_SET);  // Transmit mode
        
        // Small delay for driver enable
        for (volatile int i = 0; i < 100; ++i);
        
        HAL_UART_Transmit(huart_, data, len, 100);
        
        // Wait for transmission complete
        while (__HAL_UART_GET_FLAG(huart_, UART_FLAG_TC) == RESET);
        
        HAL_GPIO_WritePin(de_port_, de_pin_, GPIO_PIN_RESET);  // Receive mode
    }
    
    void startReceive(uint8_t* buffer, size_t size) {
        HAL_UART_Receive_DMA(huart_, buffer, size);
    }

private:
    UART_HandleTypeDef* huart_;
    GPIO_TypeDef* de_port_;
    uint16_t de_pin_;
};
```

**Modbus RTU master:**

```cpp
class ModbusMaster {
public:
    enum FunctionCode {
        READ_COILS = 0x01,
        READ_DISCRETE_INPUTS = 0x02,
        READ_HOLDING_REGISTERS = 0x03,
        READ_INPUT_REGISTERS = 0x04,
        WRITE_SINGLE_COIL = 0x05,
        WRITE_SINGLE_REGISTER = 0x06,
        WRITE_MULTIPLE_REGISTERS = 0x10
    };
    
    bool readHoldingRegisters(uint8_t slave_id, uint16_t addr, 
                               uint16_t count, uint16_t* out_data) {
        uint8_t request[8];
        request[0] = slave_id;
        request[1] = READ_HOLDING_REGISTERS;
        request[2] = addr >> 8;
        request[3] = addr & 0xFF;
        request[4] = count >> 8;
        request[5] = count & 0xFF;
        
        uint16_t crc = crc16(request, 6);
        request[6] = crc & 0xFF;
        request[7] = crc >> 8;
        
        rs485_->send(request, 8);
        
        // Wait for response (3.5 char times minimum)
        HAL_Delay(5);
        
        uint8_t response[256];
        size_t expected_len = 5 + 2 * count;  // Header + data + CRC
        
        if (receiveResponse(response, expected_len)) {
            // Verify CRC and parse data
            if (verifyCRC(response, expected_len)) {
                for (uint16_t i = 0; i < count; ++i) {
                    out_data[i] = (response[3 + 2*i] << 8) | response[4 + 2*i];
                }
                return true;
            }
        }
        return false;
    }

private:
    RS485Driver* rs485_;
    
    bool receiveResponse(uint8_t* buffer, size_t expected_len) {
        // Implement with timeout
        return HAL_UART_Receive(huart_, buffer, expected_len, 100) == HAL_OK;
    }
    
    bool verifyCRC(const uint8_t* data, size_t len) {
        uint16_t received_crc = (data[len-1] << 8) | data[len-2];
        uint16_t computed_crc = crc16(data, len - 2);
        return received_crc == computed_crc;
    }
};
```

### 3. CAN Bus (2.0 and FD)

CAN provides robust multi-master communication with automatic arbitration.

**CAN frame structure:**

| Field | Bits | Description |
|-------|------|-------------|
| SOF | 1 | Start of frame |
| Identifier | 11 (std) / 29 (ext) | Message priority |
| RTR | 1 | Remote transmission request |
| IDE | 1 | Identifier extension |
| DLC | 4 | Data length code (0-8 bytes) |
| Data | 0-64 | Payload |
| CRC | 15/17/21 | Cyclic redundancy check |
| ACK | 2 | Acknowledge slot |
| EOF | 7 | End of frame |

**SocketCAN (Linux):**

```cpp
#include <linux/can.h>
#include <linux/can/raw.h>
#include <sys/socket.h>
#include <net/if.h>
#include <unistd.h>

class SocketCAN {
public:
    bool init(const char* interface) {
        sock_ = socket(PF_CAN, SOCK_RAW, CAN_RAW);
        if (sock_ < 0) return false;
        
        struct ifreq ifr;
        strncpy(ifr.ifr_name, interface, IFNAMSIZ - 1);
        ioctl(sock_, SIOCGIFINDEX, &ifr);
        
        struct sockaddr_can addr;
        addr.can_family = AF_CAN;
        addr.can_ifindex = ifr.ifr_ifindex;
        
        if (bind(sock_, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            close(sock_);
            return false;
        }
        
        return true;
    }
    
    bool send(uint32_t id, const uint8_t* data, uint8_t len, bool extended = false) {
        struct can_frame frame;
        frame.can_id = id | (extended ? CAN_EFF_FLAG : 0);
        frame.can_dlc = len;
        memcpy(frame.data, data, len);
        
        return write(sock_, &frame, sizeof(struct can_frame)) == sizeof(struct can_frame);
    }
    
    bool receive(uint32_t& id, uint8_t* data, uint8_t& len, int timeout_ms = -1) {
        if (timeout_ms >= 0) {
            fd_set fds;
            FD_ZERO(&fds);
            FD_SET(sock_, &fds);
            
            struct timeval tv;
            tv.tv_sec = timeout_ms / 1000;
            tv.tv_usec = (timeout_ms % 1000) * 1000;
            
            if (select(sock_ + 1, &fds, nullptr, nullptr, &tv) <= 0) {
                return false;
            }
        }
        
        struct can_frame frame;
        ssize_t nbytes = read(sock_, &frame, sizeof(struct can_frame));
        if (nbytes < 0) return false;
        
        id = frame.can_id & CAN_EFF_MASK;
        len = frame.can_dlc;
        memcpy(data, frame.data, len);
        
        return true;
    }
    
    void close() {
        ::close(sock_);
        sock_ = -1;
    }

private:
    int sock_ = -1;
};
```

**CAN bit timing:**

```cpp
struct CANBitTiming {
    uint32_t bitrate;
    uint32_t prescaler;
    uint32_t ts1;  // Time segment 1 (prop + phase1)
    uint32_t ts2;  // Time segment 2 (phase2)
    uint32_t sjw;  // Synchronization jump width
};

// Sample point at 87.5% is common
CANBitTiming calculateBitTiming(uint32_t can_clock, uint32_t target_bitrate) {
    CANBitTiming timing;
    timing.bitrate = target_bitrate;
    
    const uint32_t sample_point_percent = 875;  // 87.5% * 10
    const uint32_t total_tq = 16;  // Total time quanta
    
    timing.prescaler = can_clock / (target_bitrate * total_tq);
    timing.ts1 = (total_tq * sample_point_percent / 1000) - 1;
    timing.ts2 = total_tq - timing.ts1 - 1;
    timing.sjw = std::min(timing.ts2, 4U);
    
    return timing;
}

// Example: 500 kbps with 42 MHz CAN clock
// prescaler = 42MHz / (500k * 16) = 5.25 -> use 5 or 6
// With prescaler=5: total_tq = 42MHz / (500k * 5) = 16.8 -> 17
// ts1 = 17 * 0.875 - 1 = 13.875 -> 14
// ts2 = 17 - 14 - 1 = 2
// sjw = min(2, 4) = 2
```

**CAN FD configuration:**

```cpp
// CAN FD supports up to 64 bytes and dual bitrates
struct CANFDConfig {
    uint32_t nominal_bitrate = 500000;   // Arbitration phase
    uint32_t data_bitrate = 2000000;     // Data phase
    bool enable_brs = true;              // Bit rate switching
    
    uint32_t nominal_prescaler = 1;
    uint32_t nominal_ts1 = 13;
    uint32_t nominal_ts2 = 2;
    uint32_t nominal_sjw = 2;
    
    uint32_t data_prescaler = 1;
    uint32_t data_ts1 = 5;
    uint32_t data_ts2 = 2;
    uint32_t data_sjw = 2;
};

bool sendCANFD(uint32_t id, const uint8_t* data, uint8_t len) {
    struct canfd_frame frame;
    
    frame.can_id = id;
    frame.len = len;  // CAN FD: len can be 0-64 (not just 0-8)
    frame.flags = CANFD_BRS;  // Enable bit rate switching
    
    memcpy(frame.data, data, len);
    
    return write(sock_, &frame, sizeof(struct canfd_frame)) > 0;
}
```

### 4. CANopen

CANopen provides standardized device profiles for motion control and I/O.

**Object Dictionary structure:**

| Index Range | Description |
|-------------|-------------|
| 0x0000-0x0FFF | Data type definitions |
| 0x1000-0x1FFF | Communication parameters |
| 0x2000-0x5FFF | Manufacturer-specific |
| 0x6000-0x9FFF | Standardized device profile |
| 0xA000-0xFFFF | Reserved |

**Common CANopen objects:**

| Index | Sub | Name | Description |
|-------|-----|------|-------------|
| 0x1000 | 0 | Device Type | Device profile |
| 0x1001 | 0 | Error Register | Current errors |
| 0x1005 | 0 | COB-ID SYNC | Sync message ID |
| 0x100C | 0 | Guard Time | Node guarding |
| 0x100D | 0 | Life Time Factor | Node guarding |
| 0x1016 | 0-3 | Consumer Heartbeat | Expected heartbeats |
| 0x1017 | 0 | Producer Heartbeat | Send interval |
| 0x1018 | 0-4 | Identity | Vendor ID, product code |
| 0x6040 | 0 | Controlword | Device commands |
| 0x6041 | 0 | Statusword | Device status |
| 0x6064 | 0 | Position Actual | Current position |
| 0x60FF | 0 | Target Velocity | Commanded velocity |

**SDO (Service Data Object) - Configuration:**

```cpp
class SDOClient {
public:
    bool read(uint8_t node_id, uint16_t index, uint8_t subindex,
              uint8_t* data, uint32_t& len) {
        // SDO upload request (expedited or segmented)
        uint8_t request[8] = {0};
        request[0] = 0x40;  // Initiate upload request
        request[1] = index & 0xFF;
        request[2] = index >> 8;
        request[3] = subindex;
        
        can_.send(0x600 + node_id, request, 8);
        
        // Wait for response
        uint32_t response_id;
        uint8_t response[8];
        uint8_t response_len;
        
        if (!can_.receive(response_id, response, response_len, 1000)) {
            return false;
        }
        
        if (response_id != 0x580 + node_id) {
            return false;
        }
        
        // Parse response
        uint8_t scs = (response[0] >> 5) & 0x07;  // Server command specifier
        
        if (scs == 2) {  // Initiate upload response
            uint8_t n = (response[0] >> 2) & 0x03;  // Number of bytes not used
            bool e = (response[0] >> 1) & 0x01;     // Expedited transfer
            bool s = response[0] & 0x01;            // Size indicated
            
            if (e) {  // Expedited (data in response)
                len = 4 - n;
                memcpy(data, &response[4], len);
                return true;
            } else {
                // Segmented transfer - continue reading segments
                return readSegmented(node_id, data, len);
            }
        }
        
        return false;
    }
    
    bool write(uint8_t node_id, uint16_t index, uint8_t subindex,
               const uint8_t* data, uint32_t len) {
        uint8_t request[8] = {0};
        
        if (len <= 4) {  // Expedited transfer
            request[0] = 0x23 | ((4 - len) << 2);  // Initiate download request
            request[1] = index & 0xFF;
            request[2] = index >> 8;
            request[3] = subindex;
            memcpy(&request[4], data, len);
            
            can_.send(0x600 + node_id, request, 8);
        } else {
            // Segmented transfer
            // ... implement segmented download
        }
        
        // Wait for confirmation
        uint32_t response_id;
        uint8_t response[8];
        uint8_t response_len;
        
        if (!can_.receive(response_id, response, response_len, 1000)) {
            return false;
        }
        
        return (response[0] & 0xE0) == 0x60;  // Download response
    }

private:
    SocketCAN can_;
};
```

**PDO (Process Data Object) - Real-time data:**

```cpp
// PDO mapping configuration
struct PDOMapping {
    uint16_t cob_id;
    uint8_t transmission_type;  // 0=acyclic, 1-240=cyclic, 255=event-driven
    uint16_t mapped_objects[8]; // Objects to map
    uint8_t num_mapped;
};

// Pre-operational PDO configuration
void configureTPDO(uint8_t node_id, uint8_t pdo_num, const PDOMapping& mapping) {
    SDOClient sdo;
    
    uint16_t cob_id_index = 0x1800 + pdo_num - 1;
    uint16_t mapping_index = 0x1A00 + pdo_num - 1;
    
    // Disable PDO during configuration
    uint32_t disable = mapping.cob_id | 0x80000000;  // Set valid bit to 1
    sdo.write(node_id, cob_id_index, 1, (uint8_t*)&disable, 4);
    
    // Clear mapping
    uint8_t clear = 0;
    sdo.write(node_id, mapping_index, 0, &clear, 1);
    
    // Map objects
    for (uint8_t i = 0; i < mapping.num_mapped; ++i) {
        uint32_t map_entry = mapping.mapped_objects[i];
        map_entry <<= 16;  // Shift to high 16 bits
        map_entry |= 0x0020;  // 32-bit size
        sdo.write(node_id, mapping_index, i + 1, (uint8_t*)&map_entry, 4);
    }
    
    // Set number of mapped objects
    sdo.write(node_id, mapping_index, 0, &mapping.num_mapped, 1);
    
    // Set transmission type
    sdo.write(node_id, cob_id_index, 2, &mapping.transmission_type, 1);
    
    // Enable PDO
    uint32_t enable = mapping.cob_id & 0x7FFFFFFF;  // Clear valid bit
    sdo.write(node_id, cob_id_index, 1, (uint8_t*)&enable, 4);
}

// Receive PDO callback
void onPDOReceived(uint32_t cob_id, const uint8_t* data, uint8_t len) {
    uint8_t node_id = (cob_id - 0x180) >> 4;  // Extract node ID
    uint8_t pdo_num = ((cob_id - 0x180) & 0x0F) + 1;
    
    // Parse based on mapping
    int32_t position = (data[0] << 24) | (data[1] << 16) | 
                       (data[2] << 8) | data[3];
    int32_t velocity = (data[4] << 24) | (data[5] << 16) | 
                       (data[6] << 8) | data[7];
    
    processMotorData(node_id, position, velocity);
}
```

### 5. EtherCAT

EtherCAT provides deterministic real-time communication for distributed systems.

**EtherCAT frame structure:**

```
Ethernet Header (14 bytes)
  |- Destination MAC
  |- Source MAC
  |- EtherType (0x88A4)

EtherCAT Header (2 bytes)
  |- Length (11 bits)
  |- Reserved (1 bit)
  |- Type (4 bits)

Datagrams (variable)
  |- Header (10 bytes per datagram)
  |- Data (variable)
  |- Working Counter (2 bytes)

Ethernet FCS (4 bytes)
```

**SOEM (Simple Open EtherCAT Master) example:**

```cpp
#include "ethercat.h"

class EtherCATMaster {
public:
    bool init(const char* ifname) {
        // Initialize network adapter
        if (ec_init(ifname) <= 0) {
            return false;
        }
        
        // Find and configure slaves
        if (ec_config_init(FALSE) <= 0) {
            return false;
        }
        
        printf("Found %d slaves\n", ec_slavecount);
        
        // Configure distributed clocks
        ec_configdc();
        
        // Map PDOs and transition to operational
        ec_config_map(&IOmap_);
        ec_configdc();
        
        // Request OP state for all slaves
        ec_statecheck(0, EC_STATE_SAFE_OP, EC_TIMEOUTSTATE * 4);
        
        expectedWKC_ = (ec_group[0].outputsWKC * 2) + ec_group[0].inputsWKC;
        
        ec_slave[0].state = EC_STATE_OPERATIONAL;
        ec_writestate(0);
        
        if (ec_statecheck(0, EC_STATE_OPERATIONAL, EC_TIMEOUTSTATE * 4) != EC_STATE_OPERATIONAL) {
            printf("Not all slaves reached operational state\n");
            return false;
        }
        
        operational_ = true;
        return true;
    }
    
    void cyclicTask() {
        if (!operational_) return;
        
        // Receive process data
        ec_receive_processdata(EC_TIMEOUTRET);
        
        // Application logic
        for (int slave = 1; slave <= ec_slavecount; ++slave) {
            processSlaveData(slave);
        }
        
        // Update outputs
        updateSlaveOutputs();
        
        // Send process data
        ec_send_processdata();
    }
    
    void setOutput(uint16_t slave, uint16_t offset, uint32_t value) {
        if (slave > ec_slavecount) return;
        
        uint8_t* outputs = ec_slave[slave].outputs;
        if (outputs == nullptr) return;
        
        memcpy(outputs + offset, &value, sizeof(value));
    }
    
    uint32_t getInput(uint16_t slave, uint16_t offset) {
        if (slave > ec_slavecount) return 0;
        
        uint8_t* inputs = ec_slave[slave].inputs;
        if (inputs == nullptr) return 0;
        
        uint32_t value;
        memcpy(&value, inputs + offset, sizeof(value));
        return value;
    }
    
    void checkStates() {
        ec_readstate();
        
        for (int slave = 1; slave <= ec_slavecount; ++slave) {
            if (ec_slave[slave].state != EC_STATE_OPERATIONAL) {
                printf("Slave %d state: %d, AL status: %d\n",
                       slave, ec_slave[slave].state, 
                       ec_slave[slave].ALstatuscode);
                
                // Attempt recovery
                ec_slave[slave].state = EC_STATE_OPERATIONAL;
                ec_writestate(slave);
            }
        }
    }

private:
    char IOmap_[4096];
    int expectedWKC_;
    bool operational_ = false;
    
    void processSlaveData(int slave) {
        // Read inputs from slave
        uint32_t status = getInput(slave, 0);
        int32_t position = (int32_t)getInput(slave, 4);
        int32_t velocity = (int32_t)getInput(slave, 8);
        
        // Process based on slave type
        if (isMotorDrive(slave)) {
            processMotorDrive(slave, status, position, velocity);
        }
    }
    
    void updateSlaveOutputs(int slave) {
        // Write control words and setpoints
        setOutput(slave, 0, control_word_);
        setOutput(slave, 4, target_position_);
        setOutput(slave, 8, target_velocity_);
    }
};
```

## Common Patterns

### Pattern 1: Protocol State Machine

```cpp
enum class ProtocolState {
    IDLE,
    START_DELIMITER,
    LENGTH,
    DATA,
    CHECKSUM,
    COMPLETE
};

class ProtocolParser {
public:
    void parseByte(uint8_t byte) {
        switch (state_) {
            case ProtocolState::IDLE:
                if (byte == START_BYTE) {
                    state_ = ProtocolState::START_DELIMITER;
                }
                break;
                
            case ProtocolState::START_DELIMITER:
                length_ = byte;
                data_idx_ = 0;
                if (length_ > 0 && length_ <= MAX_DATA_LEN) {
                    state_ = ProtocolState::DATA;
                } else {
                    state_ = ProtocolState::IDLE;  // Invalid length
                }
                break;
                
            case ProtocolState::DATA:
                buffer_[data_idx_++] = byte;
                if (data_idx_ >= length_) {
                    state_ = ProtocolState::CHECKSUM;
                }
                break;
                
            case ProtocolState::CHECKSUM:
                if (verifyChecksum(buffer_, length_, byte)) {
                    processMessage(buffer_, length_);
                }
                state_ = ProtocolState::IDLE;
                break;
                
            default:
                state_ = ProtocolState::IDLE;
        }
    }

private:
    static constexpr uint8_t START_BYTE = 0xAA;
    static constexpr size_t MAX_DATA_LEN = 256;
    
    ProtocolState state_ = ProtocolState::IDLE;
    uint8_t buffer_[MAX_DATA_LEN];
    uint8_t length_ = 0;
    size_t data_idx_ = 0;
};
```

### Pattern 2: CAN Message Queue

```cpp
#include <queue>
#include <mutex>
#include <condition_variable>

template<size_t N>
class CANMessageQueue {
public:
    bool push(const struct can_frame& frame) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (queue_.size() >= N) {
            return false;  // Queue full
        }
        
        queue_.push(frame);
        cv_.notify_one();
        return true;
    }
    
    bool pop(struct can_frame& frame, int timeout_ms) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (!cv_.wait_for(lock, std::chrono::milliseconds(timeout_ms),
                         [this] { return !queue_.empty(); })) {
            return false;  // Timeout
        }
        
        frame = queue_.front();
        queue_.pop();
        return true;
    }
    
    size_t size() {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.size();
    }

private:
    std::queue<struct can_frame> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;
};
```

### Pattern 3: DBC File Parser

```python
import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DBCSignal:
    name: str
    start_bit: int
    length: int
    byte_order: str  # 'little_endian' or 'big_endian'
    is_signed: bool
    scale: float
    offset: float
    min_value: float
    max_value: float
    unit: str
    receivers: List[str]

@dataclass
class DBCMessage:
    id: int
    name: str
    dlc: int
    sender: str
    signals: Dict[str, DBCSignal]

class DBCParser:
    def __init__(self, filename: str):
        self.messages: Dict[int, DBCMessage] = {}
        self.parse(filename)
    
    def parse(self, filename: str):
        with open(filename, 'r') as f:
            content = f.read()
        
        # Parse messages
        msg_pattern = r'BO_ (\d+) (\w+): (\d+) (\w+)'
        for match in re.finditer(msg_pattern, content):
            msg_id = int(match.group(1))
            msg_name = match.group(2)
            dlc = int(match.group(3))
            sender = match.group(4)
            
            self.messages[msg_id] = DBCMessage(
                id=msg_id, name=msg_name, dlc=dlc,
                sender=sender, signals={}
            )
        
        # Parse signals
        sig_pattern = r'SG_ (\w+) : (\d+)\|(\d+)@([01])([+-]) \(([^,]+),([^)]+)\) \[([^|]+)\|([^\]]+)\] "([^"]*)" (\w+)'
        for match in re.finditer(sig_pattern, content):
            sig_name = match.group(1)
            start_bit = int(match.group(2))
            length = int(match.group(3))
            byte_order = 'little_endian' if match.group(4) == '1' else 'big_endian'
            is_signed = match.group(5) == '-'
            scale = float(match.group(6))
            offset = float(match.group(7))
            min_val = float(match.group(8))
            max_val = float(match.group(9))
            unit = match.group(10)
            receivers = match.group(11).split(',')
            
            signal = DBCSignal(
                name=sig_name, start_bit=start_bit, length=length,
                byte_order=byte_order, is_signed=is_signed,
                scale=scale, offset=offset,
                min_value=min_val, max_value=max_val,
                unit=unit, receivers=receivers
            )
            
            # Find message by context (simplified)
            for msg_id, msg in self.messages.items():
                if sig_name not in msg.signals:
                    msg.signals[sig_name] = signal
                    break
    
    def decode(self, msg_id: int, data: bytes) -> Dict[str, float]:
        if msg_id not in self.messages:
            return {}
        
        msg = self.messages[msg_id]
        result = {}
        
        for sig_name, signal in msg.signals.items():
            raw_value = self._extract_bits(data, signal.start_bit, 
                                          signal.length, signal.byte_order)
            
            if signal.is_signed and raw_value >= (1 << (signal.length - 1)):
                raw_value -= (1 << signal.length)
            
            physical_value = raw_value * signal.scale + signal.offset
            result[sig_name] = physical_value
        
        return result
    
    def _extract_bits(self, data: bytes, start: int, length: int, 
                     byte_order: str) -> int:
        # Simplified bit extraction
        value = 0
        for i in range(length):
            bit_pos = start + i
            byte_idx = bit_pos // 8
            bit_idx = bit_pos % 8
            
            if byte_order == 'little_endian':
                bit_idx = 7 - bit_idx
            
            if byte_idx < len(data):
                if (data[byte_idx] >> bit_idx) & 1:
                    value |= (1 << i)
        
        return value
```

## Anti-Patterns

### ❌ Busy-waiting for UART
Polling UART status flags wastes CPU cycles.

**What happens:** High CPU usage, missed data at high baud rates.

### ✅ Use interrupts or DMA
```c
// Enable UART interrupt
HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    // Process byte, re-enable reception
    ring_buffer_write(&rx_ring, rx_byte);
    HAL_UART_Receive_IT(&huart2, &rx_byte, 1);
}
```

### ❌ No CAN bus termination
Missing termination resistors causes signal reflections.

**What happens:** Bit errors, frame loss, intermittent communication.

### ✅ Always terminate bus
```c
// 120Ω termination at both ends
// For short test cables, use 60Ω (two 120Ω in parallel)
```

### ❌ Ignoring CAN bus-off
Not handling bus-off state causes permanent communication loss.

**What happens:** Node stops transmitting, requires manual reset.

### ✅ Automatic bus-off recovery
```c
if (HAL_CAN_GetError(&hcan) == HAL_CAN_ERROR_BOF) {
    // Bus-off detected
    HAL_CAN_ResetError(&hcan);
    HAL_CAN_Start(&hcan);
}
```

### ❌ Blocking SDO requests
Waiting for SDO response blocks entire system.

**What happens:** System unresponsive, missed PDOs.

### ✅ Asynchronous SDO with timeout
```cpp
enum class SDOState { IDLE, REQUEST_SENT, WAITING, COMPLETE, ERROR };

void update() {
    switch (sdo_state) {
        case SDOState::IDLE:
            if (sdo_pending) {
                sendSDORequest();
                sdo_state = SDOState::REQUEST_SENT;
                sdo_timeout = getTick() + SDO_TIMEOUT_MS;
            }
            break;
            
        case SDOState::REQUEST_SENT:
        case SDOState::WAITING:
            if (sdo_response_received) {
                processResponse();
                sdo_state = SDOState::COMPLETE;
            } else if (getTick() > sdo_timeout) {
                sdo_state = SDOState::ERROR;
            }
            break;
            
        case SDOState::COMPLETE:
        case SDOState::ERROR:
            sdo_pending = false;
            sdo_state = SDOState::IDLE;
            break;
    }
}
```

## Configuration Reference

### Serial Port Settings

| Parameter | Common Values | Notes |
|-----------|--------------|-------|
| Baud rate | 9600, 115200, 921600 | Higher = faster, more errors |
| Data bits | 8 | Almost always 8 |
| Stop bits | 1, 2 | 2 for noisy environments |
| Parity | None, Even, Odd | Even for error detection |
| Flow control | None, RTS/CTS, XON/XOFF | RTS/CTS for hardware |

### CAN Bit Timing (500 kbps)

| Clock | Prescaler | TSEG1 | TSEG2 | SJW | Sample Point |
|-------|-----------|-------|-------|-----|--------------|
| 8 MHz | 1 | 13 | 2 | 1 | 87.5% |
| 16 MHz | 2 | 13 | 2 | 1 | 87.5% |
| 42 MHz | 6 | 11 | 2 | 1 | 85.7% |
| 48 MHz | 6 | 12 | 3 | 2 | 81.3% |

### EtherCAT Cycle Times

| Application | Cycle Time | Jitter |
|-------------|-----------|--------|
| Digital I/O | 1-10 ms | <100 µs |
| Analog I/O | 1 ms | <50 µs |
| Servo control | 250-1000 µs | <10 µs |
| Fast motion | 125 µs | <1 µs |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| UART data corruption | Baud rate mismatch | Verify both sides use same baud |
| CAN bus errors | Termination missing | Add 120Ω resistors at both ends |
| CAN bus-off | Short circuit or noise | Check wiring, add filtering |
| EtherCAT WKC error | Slave not responding | Check slave state, wiring |
| SDO timeout | Node not in operational | Transition NMT state first |
| PDO not received | Wrong COB-ID | Verify PDO mapping configuration |
| Modbus CRC error | Noise or timing | Check RS485 termination, increase delay |
| High CAN bus load | Too many messages | Increase bit rate, optimize IDs |

## Workflow Integration

- **Before this:** Use `gpio-i2c-spi` for low-level digital I/O
- **With this:** Use `microcontrollers` for embedded driver implementation
- **After this:** Use `realtime-motor-control` for motor drive integration
- **Related:** Use `sensor-actuator-drivers` for device-specific implementations

## Further Reading

- "CAN System Engineering" from Theory to Practical Applications
- "EtherCAT Technology Group" specifications
- [Linux CAN documentation](https://www.kernel.org/doc/html/latest/networking/can.html)
- Related skills: `microcontrollers`, `realtime-motor-control`, `sensor-actuator-drivers`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering serial, CAN, CANopen, and EtherCAT
- Includes protocol framing, error handling, and debugging