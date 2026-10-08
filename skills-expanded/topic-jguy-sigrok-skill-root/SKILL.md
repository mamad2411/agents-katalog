---
name: sigrok
description: >
  Use when the user mentions logic analyzers, signal capture, waveform
  acquisition, protocol decoding, sigrok, sigrok-cli, .sr files, bus traces,
  or debugging digital signals on hardware — including I2C, SPI, UART, JTAG,
  1-Wire, I3C, MCTP, and DDR5 SPD/PMIC traffic.
---

# Sigrok Logic Analyzer Skill

Control logic analyzers through sigrok-cli. This skill handles: device setup,
signal capture, protocol decoding, and output analysis.

## Capture-First Principle

**ALWAYS capture raw data to a `.sr` file first, then decode offline.**

sigrok-cli is single-threaded. Running protocol decoders during live capture at
high sample rates overwhelms the pipeline and causes dropped samples or early
termination. The two-phase approach (capture → decode) prevents this.

## Workflow

### Mode Selection

**Interactive (default):** Use when the setup is new or the user hasn't specified
all parameters. Walk through each step, confirm with the user.

**Autonomous:** Use when the user gives a complete request with all needed info
(protocol, channels, rate, duration). Skip confirmations, go straight to
capture→decode→analyze. Still ask for save location.

### Steps

1. **Detect device**
   ```bash
   sigrok-cli --scan
   ```
   Parse the output to identify the connected device. Then find the matching
   device profile: list the files in this skill's `devices/` directory and
   read the one whose **Driver** field matches the driver name in the scan
   output. The profile gives device-specific capabilities (sample rates,
   channel naming, voltage threshold, trigger support, quirks).

   If no device found, check if running on WSL:
   ```bash
   grep -qi microsoft /proc/version && echo "WSL" || echo "native"
   ```
   On WSL, the USB device must be forwarded from Windows via usbipd-win. Run
   the attach script from this skill's `scripts/` directory (relative to the
   skill's base directory):
   ```bash
   bash scripts/slogic-attach
   ```
   Then retry `sigrok-cli --scan`. If the script fails or is missing, run the
   steps manually — note that `bind` requires an elevated (administrator)
   shell on Windows:
   ```bash
   "/mnt/c/Program Files/usbipd-win/usbipd.exe" list    # find the device
   "/mnt/c/Program Files/usbipd-win/usbipd.exe" bind --busid <BUSID>
   "/mnt/c/Program Files/usbipd-win/usbipd.exe" attach --wsl --busid <BUSID>
   ```

   On native Linux: check USB connection, suggest USB 3.0 port, check
   permissions (`sudo sigrok-cli --scan`).

2. **Ask save location**
   Ask the user where to save capture files. Suggest a timestamped filename
   like `<protocol>_capture_YYYYMMDD_HHMMSS.sr`.

3. **Configure channels** (interactive mode)
   Ask which device channels are connected to which signals. Use the device
   profile's channel naming convention. Example for I2C:
   - "Which channels are SCL and SDA connected to? (e.g., D0 and D1)"

4. **Configure protocol settings** (interactive mode)
   Ask for protocol-specific parameters:
   - I2C: bus speed (100k/400k/1M) — affects sample rate choice
   - I3C: SCL/SDA polarity, IBI/Hot-Join detection, bus hang threshold
   - SPI: CPOL, CPHA, word size, bit order, CS polarity
   - UART: baud rate, parity, data bits, stop bits, inversion
   - JTAG: just channel mapping (no protocol options)
   - MCTP/SPD5/PMIC5: stacked on I3C — ask for target addresses

5. **Configure triggers** (optional)
   Ask if the user wants to trigger on a specific condition:
   - Rising edge (`r`), falling edge (`f`), any edge (`e`)
   - High level (`1`), low level (`0`)
   - Which channel to trigger on
   Example: "Trigger on D1 falling edge to catch I2C START conditions"

   If triggers are used, add `--wait-trigger` to suppress pre-trigger data
   unless the user wants pre-trigger context.

6. **Select sample rate**
   Use the Sample Rate Selection Guide below. Validate the rate against the
   device profile's supported rates. **Never use a rate not in the device
   profile's list.**

7. **Capture**
   ```bash
   sigrok-cli -d <driver> \
     --config samplerate=<rate> \
     --channels <channel-spec> \
     --time <duration> \
     -o <output-file>.sr
   ```
   Add trigger flags if configured. Use `--samples` instead of `--time` if the
   user specified a sample count.

8. **Decode**
   ```bash
   sigrok-cli -i <capture-file>.sr \
     -P <decoder-stack> \
     -A <annotation-filter>
   ```
   Use the Protocol Decode Recipes below for correct syntax.

9. **Analyze**
   Read the decoded output and summarize findings:
   - I2C: addresses seen, NACKs, register read/write patterns
   - SPI: data exchanged, CS activity
   - UART: text content, framing errors
   - JTAG: state transitions, IR/DR values
   - I3C: addresses, CCCs, ENTDAA results, IBI/Hot-Join events, transaction summary
   - MCTP: packet headers, EIDs, message types, PEC errors, reassembled messages
   - SPD5: register accesses, field decodes, temperature, part numbers
   - PMIC5: register accesses, field-level status decodes

## Protocol Decode Recipes

Decoder option names can differ between libsigrokdecode versions. If an option
is rejected, run `sigrok-cli --protocol-decoders <id> --show` — that output is
the ground truth for the installed version.

### I2C

**Capture:**
```bash
sigrok-cli -d <driver> \
  --config samplerate=10m \
  --channels D0=SCL,D1=SDA \
  --time 3s \
  -o i2c_capture.sr
```

**Decode (addresses + data):**
```bash
sigrok-cli -i i2c_capture.sr \
  -P i2c:scl=SCL:sda=SDA \
  -A i2c=address-read:address-write:data-read:data-write
```

**Check for NACKs:**
```bash
sigrok-cli -i i2c_capture.sr \
  -P i2c:scl=SCL:sda=SDA \
  -A i2c=nack
```

**With stacked decoder (e.g., EEPROM):**
```bash
sigrok-cli -i i2c_capture.sr \
  -P i2c:scl=SCL:sda=SDA,eeprom24xx \
  -A eeprom24xx
```

**Options:** `address_format` = shifted (default) | unshifted

**Annotation classes:** start, repeat-start, stop, ack, nack, bit,
address-read, address-write, data-read, data-write, warning

### SPI

**Capture:**
```bash
sigrok-cli -d <driver> \
  --config samplerate=50m \
  --channels D0=CS,D1=CLK,D2=MOSI,D3=MISO \
  --time 2s \
  -o spi_capture.sr
```

**Decode:**
```bash
sigrok-cli -i spi_capture.sr \
  -P spi:clk=CLK:mosi=MOSI:miso=MISO:cs=CS \
  -A spi
```

**Options:** `cs_polarity` (active-low | active-high), `cpol` (0 | 1),
`cpha` (0 | 1), `bitorder` (msb-first | lsb-first), `wordsize` (1-64,
default 8)

**Annotation classes:** miso-data, mosi-data, miso-bit, mosi-bit, warning,
miso-transfer, mosi-transfer

### UART

**Capture (TX only):**
```bash
sigrok-cli -d <driver> \
  --config samplerate=5m \
  --channels D0=TX \
  --time 5s \
  -o uart_capture.sr
```

**Decode:**
```bash
sigrok-cli -i uart_capture.sr \
  -P uart:rx=TX:baudrate=115200 \
  -A uart=rx-data
```

**Bidirectional:**
```bash
sigrok-cli -i uart_capture.sr \
  -P uart:rx=RX:tx=TX:baudrate=115200 \
  -A uart=rx-data:tx-data
```

**Raw binary output:**
```bash
sigrok-cli -i uart_capture.sr \
  -P uart:rx=TX:baudrate=115200 \
  -B uart=rx
```

**Options:** `baudrate` (default 115200), `parity` (none | odd | even | ignore),
`data_bits` (5-9), `stop_bits` (0.0 | 0.5 | 1.0 | 1.5 | 2.0), `bit_order`
(lsb-first | msb-first), `invert_rx` / `invert_tx` (yes | no),
`format` (ascii | hex | oct | bin), `sample_point` (% of bit width, default 50)

Older libsigrokdecode releases name these `parity_type` / `num_data_bits` /
`num_stop_bits` — check with `--show` if the options are rejected.

### JTAG

**Capture:**
```bash
sigrok-cli -d <driver> \
  --config samplerate=10m \
  --channels D0=TCK,D1=TMS,D2=TDI,D3=TDO \
  --time 5s \
  -o jtag_capture.sr
```

**Decode:**
```bash
sigrok-cli -i jtag_capture.sr \
  -P jtag:tck=TCK:tms=TMS:tdi=TDI:tdo=TDO \
  -A jtag
```

### 1-Wire

**Capture:**
```bash
sigrok-cli -d <driver> \
  --config samplerate=5m \
  --channels D0=OWR \
  --time 5s \
  -o onewire_capture.sr
```

**Decode:**
```bash
sigrok-cli -i onewire_capture.sr \
  -P onewire_link:owr=OWR,onewire_network \
  -A onewire_network
```

### I3C

**IMPORTANT:** The I3C decoder and its stacked decoders (MCTP, SPD5, PMIC5) are
custom decoders, not part of the upstream sigrok distribution. Set
`SIGROKDECODE_DIR` to include the decoder directory. The decoder source is at
https://github.com/jguy/i3c-decoder (decoder/ directory).

```bash
# Point sigrok-cli at the custom decoders
export SIGROKDECODE_DIR=/path/to/i3c-decoder/decoder
```

**Capture:**
```bash
sigrok-cli -d <driver> \
  --config samplerate=100m \
  --channels D0=SCL,D1=SDA \
  --time 3s \
  -o i3c_capture.sr
```

**Decode (addresses + data):**
```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA \
  -A i3c=address-read:address-write:data-read:data-write
```

**Transactions only (high-level view):**
```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA \
  -A i3c=txfr-write:txfr-read:txfr-ccc:txfr-entdaa:txfr-ibi:txfr-hot-join
```

**CCC commands only:**
```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA \
  -A i3c=ccc
```

**Warnings (bus errors, hangs):**
```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA \
  -A i3c=warning
```

**Options:** `scl_pol` (normal | inverted), `sda_pol` (normal | inverted),
`ibi_detection` (enabled | disabled), `hotjoin_detection` (enabled | disabled),
`bus_hang_ms` (integer, 0=off, default 10)

**Annotation classes:** start, repeat-start, stop, ack, sdr-parity, bit,
address-read, address-write, data-read, data-write, warning, bit9, debug,
entdaa-data, hdr-exit, hdr-restart, hdr-crc, hdr-preamble, hdr-parity,
hdr-cmd, reset, ccc, ibi, hot-join, txfr-write, txfr-read, txfr-ccc,
txfr-entdaa, txfr-ibi, txfr-hot-join

**Annotation rows:**
- `bits` — individual bit values
- `addr-data` — addresses, data bytes, CCCs, start/stop/restart, HDR, ENTDAA
- `warnings` — warnings and debug
- `transactions` — high-level transfer summary (Private R/W, CCC, ENTDAA, IBI, Hot-Join)

### I3C Stacked Decoders

These stack on top of the I3C decoder using its OUTPUT_PYTHON events.

#### MCTP over I3C (DMTF DSP0233)

```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA,mctp \
  -A mctp
```

**Filter to specific target addresses:**
```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA,mctp:mctp_addrs=30,31 \
  -A mctp
```

**Options:** `mctp_addrs` (hex, comma-separated, blank=decode all),
`pec_check` (enabled | disabled)

**Annotation classes:** mctp-packet, mctp-field, mctp-ibi, mctp-reassembled, warning

**What it decodes:** MCTP transport header (version, dest/src EID, SOM/EOM/PSN/TO/Tag),
message types (Control, PLDM, NC-SI, NVMe-MI, SPDM, etc.), PEC CRC-8 validation,
multi-packet reassembly, IBI with MDB=0xAE (MCTP response-available)

#### DDR5 SPD5 Hub (JESD300-5)

```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA,spd5 \
  -A spd5
```

**Options:** `spd_addrs` (hex, comma-separated, blank=auto-detect 0x50-0x57)

**Annotation classes:** reg-write, reg-read, field, eeprom-data, temperature,
part-number, warning, transaction

#### DDR5 PMIC5030 (JEDEC JC-40.1)

```bash
SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -i i3c_capture.sr \
  -P i3c:scl=SCL:sda=SDA,pmic5 \
  -A pmic5
```

**Options:** `pmic_addrs` (hex, comma-separated, blank=auto-detect 0x48-0x4B)

**Annotation classes:** reg-write, reg-read, field, warning, status

### Multi-Protocol (parallel decode from single capture)

```bash
# Capture all needed channels
sigrok-cli -d <driver> \
  --config samplerate=10m \
  --channels D0=SCL,D1=SDA,D2=TX,D3=CS,D4=SCLK,D5=MOSI \
  --time 5s \
  -o multi_capture.sr

# Decode all protocols in parallel
sigrok-cli -i multi_capture.sr \
  -P i2c:scl=SCL:sda=SDA \
  -P uart:rx=TX:baudrate=115200 \
  -P spi:clk=SCLK:mosi=MOSI:cs=CS
```

## Triggering

```bash
sigrok-cli -d <driver> \
  --config samplerate=10m \
  --channels D0=SCL,D1=SDA \
  --triggers D1=f \
  --wait-trigger \
  --time 500ms \
  -o triggered_capture.sr
```

Trigger types: `0` (low), `1` (high), `r` (rising), `f` (falling), `e` (edge).

Check device profile for supported trigger types — not all devices support all
types.

## Sample Rate Selection Guide

Pick at least 4x the signal frequency (10x is better for clean edges).

| Protocol     | Signal Freq | Recommended Rate |
|-------------|-------------|-----------------|
| I2C 100 kHz | 100 kHz     | 5-10 MHz        |
| I2C 400 kHz | 400 kHz     | 5-10 MHz        |
| I2C 1 MHz   | 1 MHz       | 10 MHz          |
| I3C OD      | 1-4 MHz     | 20-50 MHz       |
| I3C SDR     | 12.5 MHz    | 50-100 MHz      |
| I3C HDR-DDR | 12.5 MHz    | 100-200 MHz     |
| SPI ≤5 MHz  | 5 MHz       | 20-50 MHz       |
| SPI ≤10 MHz | 10 MHz      | 50-100 MHz      |
| SPI ≤25 MHz | 25 MHz      | 100-200 MHz     |
| UART 115200 | ~115 kHz    | 5 MHz           |
| UART 1 Mbaud| 1 MHz       | 5-10 MHz        |
| JTAG ≤10 MHz| 10 MHz      | 50-100 MHz      |

**Validate the chosen rate against the device profile's supported list.**

## Output Formats

| Flag | Format | Use |
|------|--------|-----|
| `-o file.sr` | Session file | Default. Recommended for all captures. |
| `-O binary` | Raw binary | High-speed streaming, piping. |
| `-O csv` | CSV | Import to spreadsheets/scripts. Options: `dedup`, `header`, `time`. |
| `-O hex` | Hex display | Quick visual check. Option: `width=N`. |
| `-O bits` | Bit display | Quick logic level check. Option: `width=N`. |

## CLI Quick Reference

| Command | Purpose |
|---------|---------|
| `sigrok-cli --scan` | Find connected devices |
| `sigrok-cli -d <drv> --show` | Show device capabilities |
| `sigrok-cli -i file.sr --show` | Inspect capture file metadata |
| `sigrok-cli --protocol-decoders <id> --show` | Show decoder options/signals |
| `sigrok-cli -L` | List all drivers, formats, decoders |

### Additional Decode Flags

| Flag | Purpose |
|------|---------|
| `--protocol-decoder-samplenum` | Include sample numbers in annotations (for timing) |
| `--protocol-decoder-ann-class` | Show annotation class names in output |
| `--protocol-decoder-jsontrace` | Output in Google Trace Event JSON format |
| `-M <decoder>=<meta>` | Show decoder meta output (e.g., baud rate detection) |
| `-B <decoder>=<class>` | Raw binary decoder output to stdout |

Some of these flags (e.g., `--protocol-decoder-jsontrace`) only exist in newer
sigrok-cli builds — check `sigrok-cli --help` if a flag is rejected.

## Available Protocol Decoders

Run `sigrok-cli -L` for the authoritative decoder list on this installation —
the set varies by libsigrokdecode version (130+ on current builds). Use
`sigrok-cli --protocol-decoders <id> --show` for any decoder's options,
required channels, and annotation classes.

**Commonly used:** uart, spi, i2c, onewire_link + onewire_network, jtag, swd,
can, lin, flexray, modbus, ps2, i2s, parallel, usb_signalling + usb_packet,
spiflash, eeprom24xx, sdcard_spi, sdcard_sd, ir_nec, pwm, timing, counter,
jitter, guess_bitrate

**I3C (custom, requires SIGROKDECODE_DIR):** i3c, mctp, spd5, pmic5

## Troubleshooting

**Device not found:**
1. On WSL: USB device must be forwarded via usbipd-win (see "Detect device" step above)
2. Use USB 3.0 port (not a hub)
3. Check udev rules on Linux (vendor-specific — see device profile)
4. Try `sudo sigrok-cli --scan`

**Empty or no data:**
1. Verify physical wiring matches channel assignments
2. Check voltage threshold vs signal voltage (see device profile)
3. Ensure sample rate is high enough
4. If using triggers, test without `--wait-trigger` first

**Garbled decode:**
1. Increase sample rate (at least 4x signal frequency)
2. Verify protocol settings (baud, CPOL, CPHA, etc.)
3. Check channel-to-signal mapping in `-P`
4. For UART, try `invert_rx=yes` if signal is inverted

**Capture terminates early:**
1. Use capture-first pattern (no `-P` during live capture)
2. Reduce sample rate or channel count
3. Use binary output for high-speed streaming

**I3C decoder not found:**
1. Set `SIGROKDECODE_DIR` to the directory containing the `i3c/` decoder folder
2. The i3c-decoder repo's `decoder/` directory is the correct path
3. Verify: `SIGROKDECODE_DIR=/path/to/decoder sigrok-cli -P i3c --show`
4. Stacked decoders (mctp, spd5, pmic5) need the same `SIGROKDECODE_DIR`

**I3C decode shows no transactions:**
1. Ensure sample rate is at least 50 MHz for SDR (100 MHz preferred)
2. Verify channel mapping: D0=SCL, D1=SDA (not swapped)
3. Check polarity options if signals are inverted
4. If IBI/Hot-Join annotations are unexpected, disable with
   `ibi_detection=disabled` or `hotjoin_detection=disabled`

**MCTP stacked decoder shows no output:**
1. MCTP silently skips non-MCTP traffic (packets <6 bytes or version != 0x01)
2. Use `mctp_addrs` to filter to known MCTP target addresses
3. Check I3C base decoder output first to confirm traffic is being decoded
