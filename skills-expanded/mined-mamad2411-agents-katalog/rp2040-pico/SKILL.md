---
name: rp2040-pico
description: "RP2040/Pico embedded C patterns — PIO, DMA, flash, multicore. Use when writing firmware for Raspberry Pi Pico/RP2040."
user-invocable: false
---

# Domain: Rp2040-Pico Design

Raspberry Pi Pico (RP2040) dual-core embedded development with Pico SDK. Extends embedded-c-p10 with RP2040-specific patterns for dual-core safety, inter-core communication, and hardware abstraction.


**Validation:** `rp2040-pico.validate.sh` enforces NEVER/MUST rules. SHOULD rules trigger warnings. GUIDANCE is not mechanically checked.


## Invariants

### NEVER (validator will reject)

1. **No malloc/free** - Never use malloc, free, calloc, or realloc. Static allocation only. Dynamic memory is unpredictable in embedded systems.

   ```
   // BAD
   char *buf = malloc(size);
   // BAD
   free(ptr);

   // GOOD
   static char buffer[MAX_SIZE];
   // GOOD
   uint8_t data[RING_BUFFER_SIZE];
   ```

2. **No printf in Interrupt Handlers** - Never use printf, puts, or print functions inside interrupt handlers (_callback, _isr, _handler, _irq functions). These are not interrupt-safe and can cause undefined behavior.

   ```
   // BAD
   void gpio_callback(uint gpio, uint32_t events) {
     printf("GPIO %d triggered
   ", gpio);  // WRONG
   }
   

   // GOOD
   void gpio_callback(uint gpio, uint32_t events) {
     g_gpio_triggered = true;  // Set flag, handle in main loop
   }
   
   ```

3. **No Recursive Functions** - Never use recursive functions. Recursion makes stack usage unpredictable and can cause stack overflow on embedded systems with limited RAM.

   ```
   // BAD
   uint32_t factorial(uint32_t n) {
     if (n <= 1) return 1;
     return n * factorial(n - 1);  // WRONG - recursive
   }
   

   // GOOD
   uint32_t factorial(uint32_t n) {
     uint32_t result = 1U;
     for (uint32_t i = 2U; i <= n; i++) result *= i;
     return result;
   }
   
   ```

4. **No Direct Register Access** - Never access hardware registers directly via volatile pointers or raw addresses. Use Pico SDK hardware_* APIs for portability and safety.

   ```
   // BAD
   *(volatile uint32_t *)0x40014000 = 0x01;
   // BAD
   uint32_t reg = *(volatile uint32_t *)GPIO_BASE;

   // GOOD
   gpio_put(PIN, 1);
   // GOOD
   uint32_t value = gpio_get(PIN);
   ```

5. **I2C/SPI Must Use Timeout Versions** - Always use timeout versions of I2C/SPI functions. Non-timeout blocking calls can hang forever if hardware fails or bus is stuck.

   ```
   // BAD
   i2c_write_blocking(i2c0, addr, data, len, false);
   // BAD
   spi_read_blocking(spi0, 0, data, len);

   // GOOD
   i2c_write_timeout_us(i2c0, addr, data, len, false, I2C_TIMEOUT_US);
   // GOOD
   spi_write_read_blocking(spi0, tx, rx, len);  // bounded by len
   ```

6. **Arrays Must Have Named Size Constants** - Array sizes must use #define constants, not magic numbers. This ensures buffer sizes are documented and can be changed in one place.

   ```
   // BAD
   uint8_t buffer[64];
   // BAD
   char name[32];

   // GOOD
   #define BUFFER_SIZE 64U
   // GOOD
   uint8_t buffer[BUFFER_SIZE];
   ```

7. **Core 0 Must Use Watchdog** - Core 0 (main.c) must enable and update the hardware watchdog. The watchdog provides system recovery if Core 0 hangs.

   ```
   // BAD
   // main.c without watchdog
   int main(void) {
     while (true) { safety_tick(); }
   }
   

   // GOOD
   int main(void) {
     watchdog_enable(WATCHDOG_TIMEOUT_MS, true);
     while (true) { watchdog_update(); safety_tick(); }
   }
   
   ```

### SHOULD (validator warns)

1. **Review Blocking Calls in Safety/Core0 Files** - Blocking calls in safety-critical code (main.c, safety/, core0) should be reviewed. Core 0 owns safety and should not block indefinitely.

   ```
   // BAD
   // In safety_monitor.c
   // BAD
   sleep_ms(1000);  // Long blocking delay

   // GOOD
   sleep_ms(SAFETY_LOOP_PERIOD_MS);  // Short, documented delay
   ```

2. **Review Float/Double in Safety Files** - Floating point operations in safety-critical paths should be reviewed. Consider using fixed-point math for deterministic timing.

   ```
   // BAD
   // In emergency.c
   // BAD
   float depth = pressure * 0.01f;

   // GOOD
   // Use fixed-point
   // GOOD
   int32_t depth_cm = (pressure * 100) / 10000;
   ```

3. **Review Unbounded Loops** - while(true), while(1), and for(;;) loops should be reviewed to ensure they have proper exit conditions or are intentional main loops.

   ```
   // BAD
   while (1) { process(); }  // Where does this end?

   // GOOD
   // Main loop - intentionally infinite
   while (true) {
     watchdog_update();
     safety_tick();
   }
   
   ```

4. **Multicore Launch Should Have Handshake** - When using multicore_launch_core1, implement a FIFO handshake to ensure Core 1 has initialized before Core 0 continues.

   ```
   // BAD
   multicore_launch_core1(core1_entry);
   // Continue immediately without waiting
   

   // GOOD
   multicore_launch_core1(core1_entry);
   uint32_t handshake = multicore_fifo_pop_blocking();
   ASSERT(handshake == CORE1_READY_SIGNAL);
   
   ```

5. **Shared Volatile State Should Use Spinlocks** - Files with volatile globals (g_*) or static volatile should use spinlocks for thread-safe access between cores.

   ```
   // BAD
   static volatile uint32_t g_counter = 0;
   // No spinlock protection
   

   // GOOD
   static volatile uint32_t g_counter = 0;
   static spin_lock_t *g_counter_lock;
   
   ```

6. **Functions With Pointer Params Should ASSERT Non-null** - Functions that take pointer parameters should ASSERT they are not NULL at the start of the function.

   ```
   // BAD
   status_t read_sensor(sensor_t *sensor) {
     return sensor->read();  // No NULL check
   }
   

   // GOOD
   status_t read_sensor(sensor_t *sensor) {
     ASSERT(sensor != NULL);
     return sensor->read();
   }
   
   ```

7. **Status Return Values Should Be Checked** - Function calls that return status_t should have their return value checked or explicitly cast to (void).

   ```
   // BAD
   read_sensor(sensor);  // Return value ignored

   // GOOD
   status_t result = read_sensor(sensor);
   // GOOD
   (void)read_sensor(sensor);  // Explicitly ignored
   ```

8. **Should Have Dual-Core Structure** - RP2040 projects should have main.c for Core 0 entry and core1.c (or core_1.c) for Core 1 entry.

   ```
   // BAD
   // Only single main.c, no Core 1 separation

   // GOOD
   src/main.c      # Core 0 entry
   // GOOD
   src/core1.c     # Core 1 entry
   ```

9. **Should Have Emergency Handling** - Safety-critical RP2040 projects should have emergency handling code for failure scenarios.

   ```
   // BAD
   // No emergency handling

   // GOOD
   void emergency_surface(emergency_reason_t reason);
   // GOOD
   #define EMERGENCY_DEPTH_EXCEEDED 4
   ```

10. **Should Have Inter-Core Heartbeat** - Dual-core projects should implement a heartbeat mechanism between cores to detect if one core has stalled.

   ```
   // BAD
   // No inter-core monitoring

   // GOOD
   void core1_heartbeat_send(void);
   // GOOD
   bool core0_heartbeat_check(void);
   ```

### GUIDANCE (not mechanically checked)

1. **Dual-Core Startup Pattern** - Follow the standard dual-core startup pattern with proper initialization sequence and handshake.


2. **Inter-Core Heartbeat Pattern** - Implement heartbeat mechanism between cores using spinlock-protected timestamp for stall detection.


3. **Hardware Watchdog Pattern** - Hardware watchdog setup with proper timeout and integration into the safety monitoring loop.


4. **Fixed-Size Ring Buffer Pattern** - Spinlock-protected ring buffer with static allocation for inter-core or interrupt-safe queues.


5. **GPIO with Interrupt Pattern** - GPIO interrupt setup that sets flags only - processing happens in the main loop, not the ISR.


6. **I2C Sensor Read Pattern** - I2C sensor read with timeout, assertions, and proper error handling.


7. **PWM RC Input Pattern** - RC PWM input handling with timeout detection for signal loss.


8. **Status Codes Pattern** - Standard status code enumeration for RP2040 embedded systems.


9. **Emergency Surface Pattern** - Emergency handling for submarine/underwater vehicles. This state cannot be cancelled and requires power cycle.


10. **Project Structure** - Recommended project structure for RP2040 dual-core embedded systems.



## Anti-Patterns

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| malloc/free |  | Static allocation only |
| printf in ISR |  | Set flag, handle in main loop |
| Recursive functions |  | Use iteration |
| Direct register access |  | Use Pico SDK hardware_* APIs |
| _blocking without timeout |  | Use _timeout_us versions |
| Magic number array sizes |  | Use #define constants |
| Volatile without spinlock |  | Protect with spinlocks |
| No watchdog |  | Enable hardware watchdog |
| No heartbeat |  | Implement inter-core heartbeat |
| Float in safety code |  | Use fixed-point math |
