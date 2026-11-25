---
name: appyscript-language
description: "Use when writing, reviewing, or debugging AppyScript (.appy) programs for kids' robots, or when compiling AppyScript to ESP32/Arduino/Pico/micro:bit/CircuitPython. Provides the exact verified grammar (end-block syntax, when/forever/define, move/turn/say/show/wait, let/set/change, sensors), the constructs that FAIL validation despite appearing in docs, per-target sensor availability, generated-code shapes, CLI/MCP validation workflow, and 10 known-valid example programs."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# AppyScript Language — Expert Reference

AppyScript (github.com/rahulbachina/appyscript, MIT, invented by Applaa) is an
English-first programming language for educational robotics. Kids write code that
reads like a story; the compiler emits MicroPython (ESP32/Pico/micro:bit),
Arduino C++, or CircuitPython. Blocks close with `end` — no braces, no semicolons,
no indentation rules. Case-insensitive keywords. `#` starts a comment.

**Prime directive for agents:** every program you produce MUST pass
`npx appyscript validate file.appy` (or the `appyscript_validate` MCP tool)
before you show it to anyone. The grammar below is verified against the real
compiler (`validate()` from the npm package), not against the README — they
differ, and the differences are listed explicitly in the "FAILS validation"
section. Keep programs under 40 lines.

---

## 1. Program structure

A program is a sequence of **top-level blocks** only. Exactly three kinds:

```appyscript
when <trigger>        # event handler ('on' is a synonym for 'when')
  <statements>
end

forever               # top-level background loop (NOT a statement)
  <statements>
end

define <name>         # custom behaviour, called with 'do <name>'
  <statements>
end
```

Anything else at top level is error E010. This includes `let` (must live inside
a block, conventionally `when start`), `every 10s` (must be written
`when every 10s`), and bare statements.

Block-nesting rules that trip everyone:

| Construct | Top level? | Inside a block? |
|---|---|---|
| `when <trigger>` | YES | no |
| `forever` | YES | **NO — "Unknown statement: forever"** |
| `define <name>` | YES | no |
| `if / else`, `repeat N times`, `while` | no | YES |
| `let / set / change / remember` | **NO** | YES |

To loop forever *as the whole program*, use a top-level `forever` block, or
`when start` containing a `while <always-true-comparison>` loop. There is no
`forever` statement inside a handler — rewrite as `while` with a sensor or
variable condition.

---

## 2. Triggers (verified)

```appyscript
when start                      # runs once at boot ('when starts' also works)
when button_a pressed           # 'released' also accepted; bare 'when button_a' works
when button_b pressed
when shaken
when tilted                     # optional direction: when tilted left / right
when every 5s                   # timer; 'when timer 5s' is a synonym
when received                   # radio message arrived ('receives' synonym)
when distance < 30cm            # sensor threshold trigger
when light < 20%
when temperature > 30           # number only — NO unit suffix on temperature
when touch > 0
when acceleration > 2           # esp32 + microbit + circuitpython only
```

Sensor trigger form: `when <sensor> <op> <number><unit?>`.
Operators: `<  >  <=  >=  =  ==` (both `=` and `==` mean equals; `is` is NOT valid).
Units: `cm` for distance, `%` for light/speed, none for temperature/touch/acceleration.
`when temperature > 30c` FAILS — drop the unit.

Sensor triggers compile to a polling loop (every 50 ms on async targets), so
they re-fire while the condition stays true. Use a variable flag if you need
edge-triggered (fire-once) behaviour.

---

## 3. Statements (verified)

### Movement
```appyscript
move forward at 50% for 2s      # speed and duration both optional
move backward at 40% for 300ms  # 'back' = 'backward'
move left at 50% for 300ms      # strafe/curve left (kit-dependent)
move forward at full            # word speeds: full / half / slow / fast (bare word, see gotcha)
move forward                    # defaults: continues until 'stop'
back at 60% for 1s              # 'back' alone as the verb also works
stop
turn left 90°                   # turn = pivot; degree SYMBOL required (see gotcha)
turn right 45°
spin right 360°                 # spin = fast in-place rotation
spin left 90                    # bare number also accepted (degrees implied)
```

**Gotchas:**
- `at full speed` FAILS ("Unknown statement: speed") — write `at full` or `at 100%`.
- `turn left 90 degrees` FAILS — use the `°` symbol or a bare number.
- A `move` without `for <duration>` runs until `stop` — always pair them or the
  robot drives away.

### Output
```appyscript
say "Hello!"                    # TTS / serial print. STRING LITERAL ONLY.
show happy                      # facial expression (see list below)
show text "GO!"                 # text on display. STRING LITERAL ONLY.
play "success"                  # named sound; any string accepted, kit maps it
```

**Hard limitation (verified):** `say` and `show text` accept ONLY a quoted
string. `say score`, `say "Score: " + score`, and `show number n` ALL FAIL
validation. There is currently no way to speak or display a variable's value.
Design around it: use expressions/sounds as feedback (`show excited` when
score is high), or fixed strings per branch:

```appyscript
if score > 4
  say "Amazing score!"
else
  say "Good try!"
end
```

### Expressions (the robot's face)
`happy` · `sad` · `thinking` · `excited` · `angry` · `alert` · `sleep` · `calm` · `confused` · `dizzy`

Exactly these ten. `show love`, `show surprised`, etc. fail. Pick the nearest.

### Timing
```appyscript
wait 500ms
wait 2s
wait 500                        # bare number = milliseconds
```

### Variables
```appyscript
let score = 0                   # declare (inside a block only, usually 'when start')
set score to score + 1          # assign; right side may use + - * / and other vars
set score to score * 2
change score by 1               # increment shorthand (negative: change score by 0 - 1)
remember score                  # persist to device flash/NVS across power cycles
let ok = yes                    # booleans: yes/no/true/false are literals...
```

- Variables declared with `let` inside `when start` are emitted at global scope
  and are visible in every other handler — this is the standard pattern for
  shared state (flags, counters).
- Using a variable never declared with `let` produces warning E021 (still
  compiles, becomes 0). Always `let` first in `when start`.
- **Negative literals FAIL**: `let n = -1` is a parse error. Use `let n = 0`
  then `change n by 0 - 1`, or restructure to count up.
- **Bare booleans cannot be conditions**: `if ok` FAILS — conditions must be
  comparisons. Use numeric flags: `let ringing = 0` ... `if ringing > 0`.

### Control flow
```appyscript
if distance < 20cm              # optional 'then' after the condition
  show alert
else                            # 'otherwise' is a synonym for 'else'
  show calm
end

if distance < 10cm
  show angry
else
  if distance < 25cm            # else-if = nested if inside else (no 'elif')
    show alert
  else
    show calm
  end
end

repeat 3 times
  spin right 90°
  wait 500ms
end

while distance > 50cm           # condition must be a comparison
  move forward at 30%
  wait 10ms                     # ALWAYS wait inside while/forever (W001/W006)
end
```

Conditions combine with `and` / `or` / `not`:
```appyscript
if distance < 20cm and light < 50%
  show alert
end
if not distance < 10cm
  show calm
end
```

### Custom behaviours
```appyscript
define celebrate                # NO parameters — 'define wave(times)' is invalid
  show excited
  say "Yay!"
  spin right 360°
end

when button_a pressed
  do celebrate                  # E020 if the name was never defined
end
```

Defines may call other defines (`do` chains work). Duplicate names = E022.
An unused define = warning W004.

### Radio (paired robots)
```appyscript
send "hello"                    # broadcast a message
when received                   # fires when any message arrives
  say "Got a message!"
end
```
Only on targets with `hasRadio` (esp32, pico, microbit, circuitpython — NOT arduino).

---

## 4. FAILS validation today (despite appearing in docs/examples)

The repo's own README and some bundled examples use constructs the shipped
compiler rejects. **Never emit these** — they are roadmap, not language:

| Construct | Error | Workaround |
|---|---|---|
| `let x = pick random 1 to 6` | E010 "Unknown statement: random" | Derive pseudo-variety from sensor reads (`if light < 50%`) or alternate with a counter flag |
| `let l = list` / `add "x" to l` / `item n of l` | E010 | Use separate if-branches with fixed strings |
| `say "Score: " + score` (string concat) | E010 "+" | Fixed strings per branch |
| `say score` (variable) | "Expected STRING" | Same |
| `show number n` | parse error | Same |
| `every 10s` as a top-level block | "Expected when/forever/define" | `when every 10s` |
| `forever` inside a handler | E010 | Top-level `forever` block, or `while` loop |
| `let` at top level | "Expected when/forever/define" | Move into `when start` |
| `define name(param)` | parse error | No params; make one define per variant |
| `match x / case 1 / default` | E010 | Nested if/else (match exists in lexer only) |
| `repeat until <cond>` | parse error | `while <inverted cond>` |
| `at full speed` | E010 "speed" | `at full` or `at 100%` |
| `turn left 90 degrees` | E010 "degrees" | `turn left 90°` or `spin left 90` |
| `let n = -1` | parse error | `let n = 0` + `change n by 0 - 1` |
| `if flag` (bare variable) | "Expected comparison operator" | `if flag > 0` |
| `if n is 1` | "Expected comparison operator" | `if n = 1` |
| `when temperature > 30c` | E010 "c" | No unit on temperature |
| `when touch pressed` | parse error | `when touch > 0` |

---

## 5. Hardware targets (verified profiles)

| Target ID | Hardware | Runtime | distance | light | temp | touch | accel | Display | Radio | Async | Flash/RAM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `esp32` | ESP32 / M5Stack Core S3 SE | MicroPython | Y | Y | Y | Y | Y | Y | Y | Y | 8 MB / 512 KB |
| `arduino` | Uno / Nano / Mega | C++ | Y | Y | Y | Y | **N** | **N** | **N** | N | 32 KB / 2 KB |
| `pico` | Raspberry Pi Pico W | MicroPython | Y | Y | Y | Y | **N** | **N** | Y | Y | 2 MB / 264 KB |
| `microbit` | BBC micro:bit V2 | MicroPython | **N** | Y | Y | Y | Y | Y (5x5) | Y | N | — |
| `circuitpython` | Adafruit Circuit Playground Bluefruit | CircuitPython | **N** | Y | Y | Y | Y | N | Y | — | — |

Semantic check E023 hard-fails the compile when a sensor isn't on the target:
- `when distance < 30cm` compiles on esp32/arduino/pico, FAILS on microbit and
  circuitpython (no ultrasonic). Use `light`/`acceleration` plots there.
- `when acceleration > 2` and `when shaken` need an IMU — not on arduino/pico
  profiles (`shaken` still parses everywhere; pick esp32/microbit for shake games).
- `show text` needs a display — only esp32 and microbit have one. On other
  targets it degrades to serial print; don't build UX around it.
- `send`/`when received` need radio — not arduino.

When the user hasn't named a chip, default to `esp32` (everything available),
and say so. If the program uses `distance`, never offer microbit/circuitpython.

---

## 6. What the compiler generates (so you can debug flashes)

**esp32 / pico (MicroPython, async):** each `when` becomes an
`async def _handler_*()` task; sensor triggers poll every 50 ms; top-level
`forever` becomes its own task; all gathered under `uasyncio`. Generated code
imports `from applaa_robot import Robot, wait_ms` — the **applaa_robot runtime
library must already be on the board's filesystem** or you get
`ImportError: no module named 'applaa_robot'` at boot. `wait` →
`await asyncio.sleep_ms(n)` (never `time.sleep` — would block all handlers).

**arduino (C++, polling):** single `loop()`; every trigger becomes an `if` check
per iteration; `wait` → `delay(ms)` (blocking — a 3 s wait in one handler stalls
button detection; keep waits short on arduino). Includes `<AppyRobot.h>` — the
AppyRobot Arduino library must be installed in the IDE. `say` → `Serial.println`
+ beep at 115200 baud. Variables from `let` are hoisted to globals above `setup()`.

**microbit:** MicroPython polling loop (no uasyncio on micro:bit V2 MicroPython).
**circuitpython:** CircuitPython idioms for Circuit Playground Bluefruit.

Practical consequences:
- On arduino, `when every 5s` is implemented with millis bookkeeping inside
  `loop()`; long `delay()` calls from other handlers skew the interval.
- Sensor `when` blocks re-enter while true. A robot inside `when distance < 30cm`
  that takes 2 s of actions will immediately re-run if the obstacle is still
  there — intended for alarms, surprising for one-shot greetings. Gate with a flag:

```appyscript
when start
  let greeted = 0
end

when distance < 30cm
  if greeted = 0
    set greeted to 1
    say "Hello there!"
    show happy
  end
end

when distance > 60cm
  set greeted to 0
end
```

---

## 7. Validation workflow for agents (mandatory)

Via MCP (preferred — the server ships in the package, tools:
`appyscript_validate`, `appyscript_compile`, `appyscript_simulate`,
`appyscript_explain`, `appyscript_hardware_info`, `appyscript_list_targets`,
`appyscript_list_keywords`):

1. Draft the program (< 40 lines, comment header with title + what it teaches).
2. `appyscript_validate` → fix every error, then every warning.
3. `appyscript_compile` with the actual target → catches E023 sensor mismatches
   that pure validation can miss for the chosen chip.
4. `appyscript_simulate` with injected sensors to confirm behaviour:
   `{ sensors: { distance: 20 }, buttons: { a: true }, triggerEvents: ["shaken"], maxTicks: 50 }`.

Via CLI:
```bash
npx appyscript validate robot.appy
npx appyscript compile robot.appy --target esp32 --strict   # warnings = errors
npx appyscript simulate robot.appy --sensor-distance=20 --button-a --max-ticks=100
npx appyscript explain robot.appy        # plain-English summary, good for kid-facing output
```

Diagnostic codes you will see:

| Code | Meaning | Fix |
|---|---|---|
| E010 | Unknown statement / unexpected token | Almost always a construct from section 4 — rewrite |
| E020 | `do x` but no `define x` | Add the define or fix spelling |
| E021 (warn) | Variable used before `let` | Add `let` in `when start` |
| E022 | Duplicate `define` name | Rename |
| E023 | Sensor not on target | Change sensor or target |
| W001/W006 | `forever`/`while` with no `wait` | Add `wait 10ms`+ at loop end (100% CPU otherwise) |
| W002 | Redundant `stop` before `move` | Delete the `stop` |
| W004 | Unused define | Call it or delete it |
| W007 | Duplicate event handler | Merge bodies |

---

## 8. Style rules for kid-facing programs

- **< 40 lines** including comments. If it's longer, cut features.
- 2-space indentation inside blocks (cosmetic — parser ignores it — but always do it).
- Open with a 2-line comment: `# Title` and `# What it teaches: ...`.
- Every program starts with a `when start` that says hello and shows an expression —
  kids need immediate proof the robot is alive.
- Pair every `move` with either `for <duration>` or a later `stop`.
- Always `wait` inside `while`/`forever` (10–500 ms).
- Give button_a a fun action and button_b a calm/stop action — kids mash buttons.
- Prefer `show <expression>` over text; expressions work on every target.
- One concept per program (one new loop type, one sensor, one event).

---

## 9. Ten known-valid example programs

All ten below pass `validate()` against the shipped compiler.

### 9.1 Hello World (any target)
```appyscript
# Hello World — first program
when start
  show happy
  say "Hello! I am Appy!"
  wait 1s
  show calm
end
```

### 9.2 Guard Robot (esp32 / arduino / pico — uses distance)
```appyscript
# Guard Robot — barks when someone gets too close
when distance < 30cm
  say "INTRUDER ALERT!"
  show angry
  spin right 180°
  wait 1s
  show alert
end

forever
  if distance > 60cm
    show happy
  end
  wait 500ms
end
```

### 9.3 Dance Robot (esp32 / microbit — uses shaken)
```appyscript
# Dance Robot — performs a routine when shaken
define spin_dance
  spin right 180°
  wait 200ms
  spin left 180°
  wait 200ms
end

define wave
  move left at 50% for 300ms
  move right at 50% for 300ms
  stop
end

when shaken
  show excited
  say "Let's dance!"
  repeat 3 times
    do spin_dance
  end
  do wave
  show happy
end

when button_a pressed
  show calm
  stop
end
```

### 9.4 Night Light (any target — light sensor)
```appyscript
# Night Light — reacts to room brightness
when start
  say "Night light ready!"
  show calm
end

when light < 20%
  show happy
  show text "LIGHT ON"
  play "success"
  say "It's dark, turning on my glow!"
end

when light > 60%
  show sleep
  show text "LIGHT OFF"
  say "Nice and bright, light off."
end
```

### 9.5 Traffic Light (any target — top-level forever)
```appyscript
# Traffic Light — forever loop with timed phases
when start
  say "Traffic light starting!"
end

forever
  show text "RED"
  show angry
  wait 3000ms
  show text "GREEN"
  show happy
  wait 3000ms
  show text "YELLOW"
  show alert
  wait 1000ms
end
```

### 9.6 Pet Robot (any target — timer event, shared variable)
```appyscript
# Pet Robot — keep it happy or it sulks
when start
  let happiness = 5
  show happy
  say "I'm your pet! Press my buttons!"
end

when button_a pressed
  change happiness by 2
  show excited
  play "success"
  say "Yay! I love you!"
end

when button_b pressed
  change happiness by 1
  show happy
  say "Thanks for the pat!"
end

when every 10s
  change happiness by 0 - 1
  if happiness < 3
    show sad
    say "I feel ignored... play with me!"
  end
end
```

### 9.7 Alarm Clock (any target — while loops, numeric flag)
```appyscript
# Alarm Clock — countdown, ring until silenced
when start
  let ringing = 0
  let seconds = 10
  say "Alarm set for 10 seconds!"
  show sleep
  while seconds > 0
    wait 1000ms
    set seconds to seconds - 1
  end
  set ringing to 1
  show alert
  while ringing > 0
    say "WAKE UP!"
    play "success"
    wait 1000ms
  end
  show calm
  say "Good morning!"
end

when button_a pressed
  set ringing to 0
  show happy
end
```

### 9.8 Follow My Hand (esp32 / arduino / pico — distance bands)
```appyscript
# Follow My Hand — keeps a polite distance
when start
  say "Move your hand slowly in front of me!"
  show happy
end

forever
  if distance < 15cm
    back at 40% for 500ms
    show confused
  else
    if distance < 25cm
      stop
      show happy
    else
      move forward at 40% for 500ms
      show thinking
    end
  end
  wait 100ms
end

when button_a pressed
  stop
  say "Okay, taking a break!"
  show calm
end
```

### 9.9 Step Counter (esp32 / microbit — shaken + remember)
```appyscript
# Step Counter — counts shakes, survives power-off
when start
  let steps = 0
  say "Strap me on and start walking!"
  show happy
end

when shaken
  change steps by 1
  remember steps
  if steps > 100
    show excited
    play "success"
  else
    show happy
  end
end

when button_b pressed
  set steps to 0
  remember steps
  say "Counter reset!"
  show calm
end
```

### 9.10 Hot or Cold (any target — temperature + and/or)
```appyscript
# Hot or Cold — comfort monitor
when start
  say "I will watch the temperature!"
  show calm
end

when temperature > 30
  show angry
  say "It's hot! Find some shade!"
end

when temperature < 15
  show confused
  say "Brrr, it's cold!"
end

forever
  if temperature >= 15 and temperature <= 30
    show happy
  end
  wait 2s
end
```

---

## 10. Debugging checklist

Program won't validate:
1. Read the E010 location — 9 times out of 10 it's a section-4 construct
   (random, list, concat, top-level let/every, nested forever, define params).
2. `say`/`show text` argument must be a double-quoted string literal.
3. Conditions must be comparisons — no bare variables, no `is`.
4. `°` symbol (or bare number), never the word `degrees`.

Validates but compiles with errors:
1. E023 → sensor/target mismatch; check the section-5 matrix.
2. `--strict` failing on W001/W006 → add `wait` to the loop.

Compiles but robot misbehaves:
1. ImportError on boot → `applaa_robot.py` (MicroPython) or AppyRobot library
   (Arduino) missing from the board; flash the runtime first.
2. Action repeats forever near an obstacle → sensor triggers re-fire while true;
   add a flag gate (section 6 pattern).
3. Buttons feel dead on arduino → a long `wait`/dance routine is blocking
   `loop()`; shorten waits, or move to esp32 (async handlers).
4. Robot drives off a table → `move` without `for`; add a duration or `stop`.
5. Timer drifts on arduino → blocking `delay()` elsewhere in `loop()`; expected.
6. `remember` value gone after reflash → flashing erases NVS on some boards;
   re-run once to re-seed.

Simulate before hardware, always:
```bash
npx appyscript simulate robot.appy --sensor-distance=10 --max-ticks=100
npx appyscript simulate robot.appy --shaken --button-a
```
Check `events` for the action sequence and `finalState` for variables/expression.
