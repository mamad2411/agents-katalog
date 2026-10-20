---
description: MicroPython Coding Standards for ESP32
alwaysApply: false
globs:
  - "esp32/**/*.py"
metadata:
  environments: cloud
---

# MicroPython Standards (ESP32)

This file applies only to MicroPython code for ESP32 hardware.

## Memory Constraints (CRITICAL)

```
ESP32 RAM: ~100KB available for MicroPython
Flash: 4MB (code + filesystem)

AVOID:
  - Large imports (import only what you need)
  - Heavy libraries (requests, asyncio extensive use)
  - Large data structures in memory
  
USE:
  - Lightweight u-prefixed libraries
  - Streaming for large data
  - Garbage collection when needed (import gc; gc.collect())
```

## Library Selection

**Standard library → u-prefixed version:**

```python
# ✓ Correct
import urequests
import ujson
import utime

# ✗ Wrong (these don't exist in MicroPython)
import requests
import json
import time
```

**Common libraries:**
- `urequests` - HTTP requests (lightweight)
- `ujson` - JSON encoding/decoding
- `utime` - Time functions
- `machine` - Hardware control (GPIO, Pin, etc.)
- `network` - WiFi connectivity

## Async/Concurrency

```
⚠️ LIMITED asyncio support

AVOID:
  - Complex asyncio patterns
  - Multiple concurrent tasks
  - AsyncIO-based libraries
  
OK:
  - Simple asyncio.run() for single async function
  - time.sleep() for delays (blocking is fine)
  
PREFER:
  - Synchronous, blocking code
  - Simple loops with time.sleep()
```

## Error Handling

**ALWAYS catch exceptions:**

```python
# ✓ Good
try:
    response = urequests.post(url, data=data)
    print(f'Success: {response.status_code}')
    response.close()
except Exception as e:
    print(f'Error: {e}')
    # Continue or retry
```

**No tracebacks in production:**
- MicroPython prints full tracebacks
- Catch exceptions to prevent ugly errors
- Log errors for debugging

**Implement reconnection logic:**

```python
def connect_wifi():
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            wlan.connect(SSID, PASSWORD)
            # wait for connection
            return True
        except Exception as e:
            print(f'WiFi error: {e}')
            retry_count += 1
            utime.sleep(5)
    
    return False
```

## Hardware Access

**Pin configuration:**

```python
from machine import Pin

# Output (LED, relay)
led = Pin(2, Pin.OUT)
led.on()
led.off()

# Input (button, sensor)
button = Pin(0, Pin.IN, Pin.PULL_UP)
state = button.value()
```

**DS18B20 Temperature Sensor:**

```python
import machine
import onewire
import ds18x20

dat = machine.Pin(4)
ds = ds18x20.DS18X20(onewire.OneWire(dat))
roms = ds.scan()

ds.convert_temp()
utime.sleep_ms(750)
temp = ds.read_temp(roms[0])
```

## Network Operations

**WiFi connection:**

```python
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
while not wlan.isconnected():
    utime.sleep(1)

print(f'Connected: {wlan.ifconfig()[0]}')
```

**HTTP POST:**

```python
import urequests
import ujson

data = {'sensor_id': 'esp32_001', 'value': 25.5}

response = urequests.post(
    'https://example.com/api',
    headers={'Content-Type': 'application/json'},
    data=ujson.dumps(data),
    timeout=10
)

print(f'Status: {response.status_code}')
response.close()  # Always close!
```

## Before Writing MicroPython Code

Self-check:

```
[ ] Using u-prefixed libraries (urequests, ujson)?
[ ] Memory usage considered?
[ ] Avoid complex asyncio?
[ ] Exception handling implemented?
[ ] WiFi reconnection logic?
[ ] HTTP response.close() called?
```

## Common Mistakes

```
✗ Using standard Python libraries (requests, json)
✗ Not closing HTTP responses (memory leak)
✗ Complex asyncio patterns
✗ No exception handling
✗ No WiFi reconnection logic
✗ Large data structures in RAM
```

## Debugging

**Print debugging:**

```python
print(f'Temperature: {temp:.2f}C')
print(f'WiFi status: {wlan.isconnected()}')
print(f'Free memory: {gc.mem_free()} bytes')
```

**REPL access:**
- Connect via USB serial (e.g., screen, picocom)
- Test code interactively
- Check errors immediately

**Soft reset:**

```python
import machine
machine.soft_reset()
```
