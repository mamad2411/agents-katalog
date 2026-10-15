---
name: strudel-music-programming
description: Create programmatic music with Strudel, a JavaScript port of Tidal Cycles. Use this skill when writing live-coded music, algorithmic compositions, or pattern-based audio sequences. Covers mini-notation syntax, sound samples, notes, scales, audio effects, signals, and pattern manipulation.
---

# Strudel Music Programming

Strudel is a JavaScript library for creating dynamic, algorithmic music through code. Use the [Strudel REPL](https://strudel.cc/) to run code, or see the [documentation](https://strudel.cc/workshop/getting-started/) for more details.

## When to Use This Skill

- Writing live-coded music patterns
- Creating algorithmic or generative compositions
- Building rhythm sequences with mini-notation
- Applying audio effects (filters, reverb, delay)
- Working with scales, notes, and Euclidean rhythms
- Integrating music via MIDI or OSC

## Core Concepts

### Cycles

All patterns operate within **cycles** (default: 2 seconds per cycle). Events within a sequence are distributed evenly across the cycle. Set tempo with `setcpm(cycles_per_minute)` - default is 30 cpm (120 BPM in 4/4).

### Mini-Notation

Strudel uses a compact text-based notation for defining rhythmic patterns:

| Symbol | Purpose | Example |
|--------|---------|---------|
| `space` | Sequence events | `"bd sd hh cp"` |
| `[]` | Sub-sequence (subdivide time) | `"bd [hh hh] sd"` |
| `<>` | Alternate one per cycle | `"<bd sd cp>"` |
| `*` | Speed up/multiply | `"bd*4"` or `"[hh sd]*2"` |
| `/` | Slow down/divide | `"[bd sd hh cp]/2"` |
| `~` or `-` | Rest/silence | `"bd ~ sd ~"` |
| `,` | Play in parallel (polyphony) | `"bd, hh*4"` |
| `:` | Sample number | `"hh:2"` |
| `@` | Elongate (weight) | `"c@3 e"` (c is 3x longer) |
| `!` | Replicate | `"c!3 e"` (c plays 3 times) |
| `?` | Random removal (50% chance) | `"bd*8?"` |
| `\|` | Random choice | `"bd \| sd \| cp"` |
| `()` | Euclidean rhythm | `"bd(3,8)"` (3 beats over 8 steps) |

## Playing Sounds

```javascript
// Play a sound sample
sound("casio")
s("casio")  // shorthand

// Play drum sounds
sound("bd hh sd oh")  // bass drum, hihat, snare, open hihat

// Select sample number
sound("casio:1")  // second sample in casio set

// Change drum bank
sound("bd sd").bank("RolandTR909")
```

**Common drum sounds**: `bd` (bass drum), `sd` (snare), `hh` (hihat), `oh` (open hihat), `cp` (clap), `rim` (rimshot), `lt/mt/ht` (toms), `rd` (ride), `cr` (crash)

**Drum banks**: `RolandTR909`, `RolandTR808`, `RolandTR707`, `AkaiLinn`, `RhythmAce`

## Playing Notes

```javascript
// Notes as MIDI numbers (36-84 typical range)
note("48 52 55 59").sound("piano")

// Notes as letters (a-g, with octave)
note("c e g b").sound("piano")
note("c4 e4 g4 b4").sound("piano")  // with octave

// Sharps and flats
note("c# d# f# g# a#").sound("piano")  // sharps
note("db eb gb ab bb").sound("piano")  // flats
```

## Using Scales

```javascript
// Use scale degrees instead of note names
n("0 2 4 6").scale("C:minor").sound("piano")

// Common scales: major, minor, dorian, mixolydian, pentatonic
n("0 1 2 3 4 5 6 7").scale("C:major:pentatonic").sound("piano")

// Automate scales
n("0 2 4 6").scale("<C:major D:minor>/4").sound("piano")
```

## Sample Selection with `n`

```javascript
// Select sample numbers separately from sound
n("0 1 4 2 3").sound("jazz")

// Equivalent to:
sound("jazz:0 jazz:1 jazz:4 jazz:2 jazz:3")
```

## Tempo and Timing

```javascript
// Set cycles per minute (cpm)
setcpm(60)  // 60 cycles per minute

// Relationship: 120 BPM in 4/4 = setcpm(120/4) = setcpm(30)

// Speed up pattern
sound("bd sd").fast(2)  // plays twice as fast

// Slow down pattern  
sound("bd sd").slow(2)  // plays half speed
```

## Audio Effects

### Filters

```javascript
// Low-pass filter (cut high frequencies)
sound("bd sd").lpf(800)           // cutoff at 800Hz
sound("bd sd").lpf("<200 800 2000>")  // pattern the filter

// High-pass filter (cut low frequencies)
sound("bd sd").hpf(500)

// Band-pass filter
sound("bd sd").bpf(1000)

// Vowel filter
note("c3 e3 g3").sound("sawtooth").vowel("<a e i o u>")
```

### Dynamics

```javascript
// Gain (volume)
sound("hh*8").gain("[.25 1]*4")

// Velocity
sound("hh*8").velocity(".4 1")
```

### ADSR Envelope

```javascript
// Individual parameters
note("c3 e3 g3").sound("sawtooth")
  .attack(.1)    // time to reach peak
  .decay(.2)     // time to reach sustain level
  .sustain(.5)   // sustain level (0-1)
  .release(.3)   // time to fade after note off

// Shorthand
note("c3 e3 g3").sound("sawtooth").adsr(".1:.2:.5:.3")
```

### Spatial Effects

```javascript
// Reverb
sound("bd cp").room(.5)           // reverb amount (0-1)
sound("bd cp").room(.8).rsize(4)  // with room size

// Delay
sound("bd cp").delay(.5)                    // delay amount
sound("bd cp").delay(".5:.25")              // amount:time
sound("bd cp").delay(".5:.25:.6")           // amount:time:feedback

// Panning
sound("bd hh sd hh").pan("0 .5 1 .5")  // 0=left, 1=right

// Stereo effects
sound("bd hh sd hh").jux(rev)  // reverse in right channel
```

### Distortion & Modulation

```javascript
// Distortion
sound("bd sd").distort(2)
sound("bd sd").crush(4)   // bit crusher

// Phaser
note("c e g").sound("sawtooth").phaser(2)

// Speed (pitch shift)
sound("bd sd").speed("<1 2 -1 -2>")  // negative = reverse
```

## Signals & Modulation

Use continuous signals for smooth parameter changes:

```javascript
// Basic waveforms: sine, saw, square, tri
sound("hh*16").gain(sine)

// Random signals: rand, perlin
sound("hh*16").lpf(perlin.range(200, 2000))

// Set range
sound("hh*16").lpf(sine.range(200, 4000))

// Change speed
note("c2 c3").sound("sawtooth").lpf(sine.range(100, 2000).slow(4))
```

## Pattern Manipulation

### Combining Patterns

```javascript
// Stack patterns (play simultaneously with $:)
$: sound("bd*4")
$: sound("hh*8")
$: note("c3 e3 g3 b3").sound("piano")

// Mute a pattern with _$
_$: sound("bd*4")  // muted

// Within mini-notation using comma
sound("bd*4, hh*8, cp*2")
```

### Pattern Transformations

```javascript
// Reverse
sound("bd hh sd hh").rev()

// Every n cycles, apply function
sound("bd hh sd hh").every(4, rev)

// Sometimes apply function
sound("bd hh sd hh").sometimes(rev)

// Iterate through pattern
sound("bd hh sd hh").iter(4)
```

## Euclidean Rhythms

Distribute beats evenly across steps:

```javascript
// Basic: beats, steps
sound("bd(3,8)")   // 3 beats over 8 steps (popular "tresillo" rhythm)
sound("bd(5,8)")   // 5 beats over 8 steps

// With offset: beats, steps, offset
sound("bd(3,8,2)") // start from position 2

// Combined with other patterns
sound("bd(3,8), hh*8, cp(2,8)")
```

## Complete Examples

### Basic Beat

```javascript
setcpm(120/4)
sound("bd*4, [~ sd]*2, hh*8").bank("RolandTR909")
```

### House Pattern

```javascript
sound("bd*4, [~ cp]*2, [~ hh]*4").bank("RolandTR909")
```

### Melodic Pattern with Effects

```javascript
$: note("<[c2 c3]*4 [bb1 bb2]*4 [f2 f3]*4 [eb2 eb3]*4>")
   .sound("sawtooth").lpf(800)

$: n("<0 2 4 6>*4").scale("C4:minor").sound("piano")
   .room(.3).delay(.25)

$: sound("bd*4, [~ sd]*2, hh*8").bank("RolandTR909")
```

### Dub Techno

```javascript
$: note("[~ [<[d3,a3,f4]!2 [d3,bb3,g4]!2> ~]]*2")
   .sound("gm_electric_guitar_muted").delay(.5)

$: sound("bd rim").bank("RolandTR707").delay(.5)

$: n("<4 [3@3 4] [<2 0> ~@16] ~>")
   .scale("D4:minor").sound("gm_accordion:2")
   .room(2).gain(.5)
```

### Ambient Pattern

```javascript
setcpm(15)
$: n("<0 2 4 7>").scale("C:minor:pentatonic")
   .sound("gm_pad_warm")
   .attack(.5).release(2)
   .room(.8).rsize(8)
   .lpf(sine.range(400, 2000).slow(8))
```

## Quick Reference

### Sound Sources

- **Samples**: `sound("casio")`, `s("bd")`
- **Synths**: `"sawtooth"`, `"square"`, `"triangle"`, `"sine"`
- **GM Sounds**: `"gm_acoustic_bass"`, `"gm_electric_guitar_muted"`, `"piano"`

### Essential Functions

| Function | Purpose |
|----------|---------|
| `sound()` / `s()` | Play samples |
| `note()` | Play pitched notes |
| `n()` | Select sample/scale degree |
| `scale()` | Set musical scale |
| `bank()` | Change sample bank |
| `setcpm()` | Set tempo |
| `fast()` / `slow()` | Change speed |
| `gain()` | Volume |
| `lpf()` / `hpf()` | Filters |
| `room()` / `delay()` | Reverb/Delay |
| `pan()` | Stereo position |
| `$:` | Play pattern in parallel |

### Keyboard Shortcuts (REPL)

- `Ctrl+Enter` - Play/Update
- `Ctrl+.` - Stop
- `Ctrl+Shift+Enter` - Play from beginning

## Tips

1. **Start simple**: Begin with one sound, then layer patterns
2. **Use `<>` for variation**: Alternate between values each cycle
3. **Pattern everything**: Most parameters accept mini-notation patterns
4. **Explore samples**: Try different `:n` numbers to find variations
5. **Use signals for movement**: `sine`, `saw`, `perlin` add life to static values
6. **The REPL visualizes**: Watch the pianoroll to understand your patterns
