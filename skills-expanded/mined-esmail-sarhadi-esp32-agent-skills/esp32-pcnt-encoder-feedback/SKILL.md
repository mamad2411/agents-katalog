---
name: esp32-pcnt-encoder-feedback
description: Use when counting pulses, measuring frequency or decoding incremental encoder feedback with ESP32 PCNT; especially when counts drift, glitches appear or counters overflow during long runs.
license: MIT
---

# PCNT pulse counting and encoder feedback

PCNT is a hardware pulse counter with configurable edge and level actions plus a glitch filter.
It is useful for flow meters, tachometers and incremental encoders, but its limits are target-specific.

## Confirm the peripheral and signal contract

- Record the SoC, board, ESP-IDF release, encoder electrical interface and maximum input frequency.
- Check the target's PCNT unit/channel count, counter width, filter clock and interrupt behavior.
- Determine whether the encoder is open-collector, push-pull, differential or line-driver output.
- Add the correct external pull-up, termination or receiver; never connect an industrial differential encoder directly to a 3.3 V GPIO.
- Define A/B phase order, direction convention, counts per revolution and x1/x2/x4 decoding expectation.

## Configure counting deliberately

- Select edge actions and level actions from a truth table; test forward and reverse rotation.
- Configure the glitch filter from the shortest legitimate pulse and the longest expected noise spike.
- Check the filter clock source and maximum representable filter duration for the selected chip.
- Set a counter limit and handle limit events or accumulation extensions explicitly.
- Use hardware watch points/limits where available; do not assume the raw hardware counter is an unbounded integer.
- Clear and restart counters only at defined synchronization points.

## Quadrature decoding

- Build a four-state transition table for A/B; illegal transitions indicate noise or missed edges.
- Test both directions and transitions where one channel changes before the other.
- If using two PCNT channels, verify the level-control polarity and channel routing against the driver documentation.
- Do not use a large debounce interval that suppresses valid high-speed transitions.
- For index/Z signals, capture the index separately and define whether it resets or snapshots the position.

## Frequency and speed estimation

- Use a monotonic timestamp and a fixed measurement window for frequency estimation.
- At low speed, period measurement can outperform counting in a short fixed window.
- At high speed, count deltas over a fixed interval and calculate with a sufficiently wide integer type.
- State whether counts are edges, pulses, quadrature transitions or mechanical shaft revolutions.
- Apply gear ratio and pulses-per-revolution exactly once; avoid double multiplying by four.
- Detect stopped/stale feedback separately from a numeric zero speed.

## Concurrency and overflow

- Read and clear counters through the driver API; avoid unsynchronized direct register access.
- Protect shared accumulated counts if an ISR and task both modify them.
- Use a 64-bit software accumulator when long-running totals can exceed the hardware counter.
- Prove the wrap/limit extension logic with boundary tests around positive and negative limits.
- Keep ISR callbacks bounded and defer formatting or network publishing to a task.

## Verification

1. Generate a known pulse train with a signal generator or second MCU.
2. Compare PCNT counts at low, nominal and maximum expected rates.
3. Inject narrow glitches and verify the configured filter rejects only invalid pulses.
4. Reverse A/B phase order and prove direction changes sign.
5. Run across counter limits and verify accumulated totals remain monotonic.
6. Test with Wi-Fi active and during CPU load; compare against an external reference counter.

## Acceptance criteria

- The example states SoC, counter mode, input electrical level and max pulse rate.
- Host tests cover quadrature transitions, scaling, overflow extension and stale feedback.
- Hardware validation records the reference generator, pulse width, frequency and count error.
- No maximum-frequency claim is made without target-specific measurement.

## References

- ESP-IDF PCNT: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/pcnt.html
- ESP-IDF GPIO: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html
- ESP-IDF technical reference manuals: https://www.espressif.com/en/support/documents/technical-documents
