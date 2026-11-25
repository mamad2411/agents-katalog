---
name: esp32-uart-and-serial
description: Use when serial communication misbehaves - logs interleave with protocol bytes, a half-duplex bus echoes, the FIFO overflows at high baud, or the board will not boot with something on UART0. Covers pin choice, flow control, RS485 direction and log flooding.
license: MIT
---

# UART on ESP32

Every ESP32 project ends up with at least two UARTs: one for the log and one for a
device. Mixing them is where it goes wrong.

## UART0 belongs to the bootloader

GPIO1 (TX) and GPIO3 (RX) carry the ROM boot messages and the flashing protocol.
Anything you connect there must be silent at reset, and must not pull the line in
a way the bootloader reads as a command. A device that holds RX low during reset
is a board that will not flash.

If a design needs those two pins for something else, the console has to move
(`CONFIG_ESP_CONSOLE_UART_NUM`) or be disabled - not just "left alone".

## Logs are a protocol too

`printf` from an ISR, or from several tasks at once, produces interleaved lines
that look like corruption. Two fixes that actually hold:

- Route the log through one mutex-protected writer.
- Turn the log level down for production (`CONFIG_LOG_DEFAULT_LEVEL_WARN`), and
  never log per-packet at 115200 - 20 characters at 10 Hz is 2 kbit/s of pure
  noise on a 11.5 kbit/s link.

## The FIFO is 128 bytes

The hardware FIFO is small, and the driver's ring buffer is what saves you. At
921600 baud a 1 ms stall is 92 bytes: fine. At 3 Mbaud it is 300 bytes and the
overflow is silent unless you check the event. For anything above 1 Mbaud use
DMA (`uart_driver_install` with a large buffer) and a task that never blocks on
anything else.

## RS485 is UART with a direction pin

Half duplex needs the transceiver's DE/RE driven around the frame:

- Assert DE, wait for the transceiver to settle (a few microseconds, more on slow
  opto-isolated parts), then write.
- Wait until the last byte has actually left the shifter (`uart_wait_tx_done`),
  then release DE. Releasing on "write returned" truncates the last byte.
- In receive, the ESP32 sees its own transmission unless RE is tied to DE. That
  echo is the usual cause of a protocol that answers itself.

## Flow control

RTS/CTS is not optional at high baud with a device that bursts. Without it the
only backpressure is the FIFO, and the failure mode is dropped bytes that look
like a framing error.

| Symptom | Usually |
|---|---|
| first bytes of every frame are lost | DE asserted after the first write, or too late |
| last byte truncated | DE released before `uart_wait_tx_done` |
| board will not enter download mode | something driving GPIO0/GPIO3 at reset |
| data looks byte-shifted | baud off by a few percent (cheap crystal), or 5 V levels |
| works alone, corrupt with Wi-Fi on | log task starving the UART task, or no flow control |
