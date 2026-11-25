---
name: vital-preset-generator
description: Generate and modify Vital synthesizer presets (.vital files). Use when the user wants to create synth presets, modify sound parameters, set up modulations, work with wavetables, add filters, effects, or ANY other knob/setting/parameter in Vital synthesizer.
---

# Vital Preset Generator

## Resources

Consult these references when needed:
- [VITAL_USER_MANUAL.md](VITAL_USER_MANUAL.md) — UI layout, signal flow, and feature explanations
- [SYNTHESIZER_COOKBOOK.md](SYNTHESIZER_COOKBOOK.md) — Sound design recipes with parameter values

## Instructions

These are your CRITICAL instructions, make sure to follow them PERFECTLY AND DO NOT MAKE ANY MISTAKES:
1. When the user asks to create or modify a Vital preset, generate a complete JSON preset following the below schema.
2. You will receive an input JSON of the current preset, along with the descriptions of what parameters to modify or what kind of sound patch to create.
3. Be honest with the user if they are asking for a setting that doesn't exist in Vital. Check the schema closely to understand what knobs/parameters are available.
4. Even if you are not sure what parameters to update, try your best to find the most relevant parameters to the user's request, and update them accordingly.

# Schema Reference

Vital preset files are **JSON files** with the `.vital` extension. They contain all synthesizer state including parameter values, modulations, wavetables, LFO shapes, and samples. You can programmatically read, modify, and generate these files.

---

## Top-Level Structure

```json
{
    "author": "Your Name",
    "comments": "Description of the preset",
    "macro1": "CUTOFF",
    "macro2": "RESONANCE",
    "macro3": "MACRO 3",
    "macro4": "MACRO 4",
    "preset_name": "My Preset",
    "preset_style": "Lead",
    "settings": {
        /* All synth state */
    },
    "synth_version": "1.0.7"
}
```

**Note:** The `synth_version` field appears at the **end** of the JSON file. Fields are typically alphabetically ordered within `settings`.

**Preset Style Options:** Bass, Lead, Keys, Pad, Percussion, Sequence, Experiment, SFX, Template

---

## Settings Object

The `settings` object contains:

1. **Control values** - All parameter key-value pairs
2. **modulations** - Array of 64 modulation connection slots
3. **wavetables** - Array of 3 wavetable definitions
4. **lfos** - Array of 8 LFO shapes
5. **sample** - Sample data (if used)

**Note on Default Values:** Parameters with default values may be omitted from preset files. When loading, Vital applies defaults for missing parameters. When writing presets programmatically, you can include all parameters or just non-default ones.

---

## 1. Parameter Values (Control Map)

All parameters are stored as direct key-value pairs in `settings`. Here's the complete parameter list with ranges:

### Global Parameters

```json
{
    "beats_per_minute": 2.0, // Actually stores beats-per-second! 0.333-5.0 BPS × 60 = 20-300 BPM
    "bypass": 0.0, // 0=off, 1=on (bypass entire synth)
    "volume": 5473.0404, // sqrt scale, 0 to 7399.4404 (-80dB to ~0dB)
    "polyphony": 8.0, // 1-32 voices
    "oversampling": 1.0, // 0=1x, 1=2x, 2=4x, 3=8x
    "legato": 0.0, // 0=off, 1=on
    "velocity_track": 0.0, // -1.0 to 1.0 (-100% to 100%)
    "pitch_bend_range": 2.0, // 0-48 semitones
    "mpe_enabled": 0.0, // 0=off, 1=on (enable MPE mode)
    "pitch_wheel": 0.0, // -1.0 to 1.0 (current pitch wheel state)
    "mod_wheel": 0.0, // 0.0 to 1.0 (current mod wheel state)
    "view_spectrogram": 0.0 // 0=off, 1=on, 2=? (spectrogram display)
}
```

### Voice Settings (Advanced Panel)

```json
{
    "voice_tune": 0.0, // -1.0 to 1.0 (-100 to +100 cents)
    "voice_transpose": 0.0, // -48 to +48 semitones
    "voice_amplitude": 1.0, // 0.0 to 1.0
    "voice_priority": 4.0, // Voice priority mode (see below)
    "voice_override": 0.0, // Voice override mode (see below)
    "stereo_routing": 1.0, // 0.0 to 1.0 (stereo spread amount)
    "stereo_mode": 0.0 // 0=Spread, 1=Rotate
}
```

**Voice Priority Values:**
- 0: Newest (steal newest voice)
- 1: Oldest (steal oldest voice)
- 2: Highest (steal highest pitch)
- 3: Lowest (steal lowest pitch)
- 4: Round Robin (cycle through voices)

**Voice Override Values:**
- 0: Kill (hard cut)
- 1: Steal (soft takeover)

### Portamento

```json
{
    "portamento_time": -10.0, // exponential: -10 to 4 (very fast to 16 secs)
    "portamento_slope": 0.0, // -8.0 to 8.0
    "portamento_scale": 0.0, // 0=off, 1=on (scale by interval)
    "portamento_force": 0.0 // 0=off, 1=on (always glide)
}
```

### Oscillators (X = 1, 2, or 3)

```json
{
    "osc_X_on": 1.0, // 0=off, 1=on
    "osc_X_transpose": 0.0, // -48 to +48 semitones
    "osc_X_transpose_quantize": 0.0, // 0-8191 (scale snap)
    "osc_X_tune": 0.0, // -1.0 to 1.0 (-100 to +100 cents)
    "osc_X_pan": 0.0, // -1.0 to 1.0
    "osc_X_level": 0.707, // 0.0 to 1.0 (quadratic)

    // Wavetable
    "osc_X_wave_frame": 0.0, // 0-256 (wavetable position)
    "osc_X_frame_spread": 0.0, // -128 to +128

    // Unison
    "osc_X_unison_voices": 1.0, // 1-16
    "osc_X_unison_detune": 4.472, // 0-10 (quadratic)
    "osc_X_unison_blend": 0.8, // 0.0 to 1.0
    "osc_X_detune_power": 1.5, // -5.0 to 5.0
    "osc_X_detune_range": 2.0, // 0-48 semitones
    "osc_X_stereo_spread": 1.0, // 0.0 to 1.0
    "osc_X_stack_style": 0.0, // 0-10 (see stack types below)
    "osc_X_spectral_unison": 1.0, // 0=off, 1=on

    // Phase
    "osc_X_phase": 0.5, // 0.0 to 1.0 (0-360 degrees)
    "osc_X_distortion_phase": 0.5, // 0.0 to 1.0
    "osc_X_random_phase": 1.0, // 0.0 to 1.0

    // Distortion (Wave Distortion)
    "osc_X_distortion_type": 0.0, // 0-12 (see types below)
    "osc_X_distortion_amount": 0.5, // 0.0 to 1.0
    "osc_X_distortion_spread": 0.0, // -0.5 to 0.5

    // Spectral Morph
    "osc_X_spectral_morph_type": 0.0, // 0-11 (see types below)
    "osc_X_spectral_morph_amount": 0.5, // 0.0 to 1.0
    "osc_X_spectral_morph_spread": 0.0, // -0.5 to 0.5

    // Routing
    "osc_X_destination": 0.0, // 0-13 (see destinations below)
    "osc_X_midi_track": 1.0, // 0=off, 1=on
    "osc_X_smooth_interpolation": 0.0, // 0=off, 1=on
    "osc_X_view_2d": 1.0 // 0=3D, 1=2D, 2=Spectrogram
}
```

**Stack Style Values:**

-   0: Unison, 1: Center Drop 12, 2: Center Drop 24
-   3: Octave, 4: 2x Octave, 5: Power Chord, 6: 2x Power Chord
-   7: Major Chord, 8: Minor Chord, 9: Harmonics, 10: Odd Harmonics

**Distortion Type Values:**

-   0: None, 1: Sync, 2: Formant, 3: Quantize, 4: Bend, 5: Squeeze, 6: Pulse
-   7: FM <- Osc A, 8: FM <- Osc B, 9: FM <- Sample
-   10: RM <- Osc A, 11: RM <- Osc B, 12: RM <- Sample

**Spectral Morph Type Values:**

-   0: None, 1: Vocode, 2: Formant Scale, 3: Harmonic Stretch
-   4: Inharmonic Stretch, 5: Smear, 6: Random Amplitudes
-   7: Low Pass, 8: High Pass, 9: Phase Disperse, 10: Shepard Tone, 11: Skew

**Destination Values:**

-   0: Filter 1, 1: Filter 2, 2: Filter 1+2, 3: Effects, 4: Direct Out
-   5: Chorus, 6: Compressor, 7: Delay, 8: Distortion, 9: EQ
-   10: FX Filter, 11: Flanger, 12: Phaser, 13: Reverb

### Sample Section

```json
{
    "sample_on": 0.0, // 0=off, 1=on
    "sample_transpose": 0.0, // -48 to +48
    "sample_transpose_quantize": 0.0,
    "sample_tune": 0.0, // -1.0 to 1.0
    "sample_level": 0.707, // quadratic
    "sample_pan": 0.0,
    "sample_destination": 3.0, // same as osc destinations
    "sample_loop": 1.0, // 0=off, 1=on
    "sample_bounce": 0.0, // 0=off, 1=on
    "sample_keytrack": 0.0, // 0=off, 1=on
    "sample_random_phase": 0.0 // 0=off, 1=on
}
```

### Filters (X = 1, 2, or fx)

```json
{
    "filter_X_on": 0.0, // 0=off, 1=on
    "filter_X_model": 0.0, // 0-7 (see models below)
    "filter_X_style": 0.0, // 0-4 (model-dependent)
    "filter_X_cutoff": 60.0, // 8-136 semitones
    "filter_X_resonance": 0.5, // 0.0 to 1.0
    "filter_X_drive": 0.0, // 0-20 dB
    "filter_X_mix": 1.0, // 0.0 to 1.0
    "filter_X_blend": 0.0, // 0-2 (LP->BP->HP)
    "filter_X_keytrack": 0.0, // -1.0 to 1.0

    // Formant filter specific
    "filter_X_formant_x": 0.5,
    "filter_X_formant_y": 0.5,
    "filter_X_formant_transpose": 0.0, // -12 to +12
    "filter_X_formant_resonance": 0.85, // 0.3 to 1.0
    "filter_X_formant_spread": 0.0, // -1.0 to 1.0

    // Comb filter specific
    "filter_X_blend_transpose": 42.0, // 0-84 semitones

    // Input routing (filters 1 and 2 only)
    "filter_1_osc1_input": 1.0, // default: osc1 -> filter1
    "filter_1_osc2_input": 0.0, // 0=off, 1=on
    "filter_1_osc3_input": 0.0,
    "filter_1_sample_input": 0.0,
    "filter_2_osc1_input": 0.0,
    "filter_2_osc2_input": 1.0, // default: osc2 -> filter2
    "filter_2_osc3_input": 0.0,
    "filter_2_sample_input": 0.0,
    "filter_X_filter_input": 0.0 // serial routing (filter_1 only)
}
```

**Note:** Filter input parameters are named `filter_X_oscY_input` (no underscore between "osc" and the number). Default routing sends osc1 to filter1 and osc2 to filter2. These parameters may be omitted from presets when at default values.

**Filter Model Values:**

| Value | Model | Description |
|-------|-------|-------------|
| 0 | Analog | Classic analog-modeled filter |
| 1 | Dirty | Aggressive analog with saturation |
| 2 | Ladder | Moog-style ladder filter |
| 3 | Digital | Clean digital filter |
| 4 | Diode | Diode ladder filter |
| 5 | Formant | Vowel/formant filter (uses formant_x, formant_y) |
| 6 | Comb | Comb filter (uses blend_transpose) |
| 7 | Phaser | Phaser-style allpass filter |

**Filter Style Values (Model-Dependent):**

For Analog/Dirty/Ladder/Digital models:
- 0: 12dB slope
- 1: 24dB slope
- 2: Notch Blend
- 3: Notch Spread
- 4: B/P/N (Bandpass/Notch morphing)

For Diode model:
- 0: Low Shelf
- 1: Low Cut

For Comb model:
- 0: Low High Comb
- 1: Low High Flange+
- 2: Low High Flange-
- 3: Band Spread Comb
- 4: Band Spread Flange+
- 5: Band Spread Flange-

### Envelopes (X = 1 to 6)

```json
{
    "env_X_delay": 0.0, // 0-4 seconds (quartic)
    "env_X_attack": 0.1495, // 0-32 seconds (quartic)
    "env_X_attack_power": 0.0, // -20 to +20
    "env_X_hold": 0.0, // 0-4 seconds (quartic)
    "env_X_decay": 1.0, // 0-32 seconds (quartic)
    "env_X_decay_power": -2.0, // -20 to +20
    "env_X_sustain": 1.0, // 0.0 to 1.0
    "env_X_release": 0.5476, // 0-32 seconds (quartic)
    "env_X_release_power": -2.0 // -20 to +20
}
```

### LFOs (X = 1 to 8)

```json
{
    "lfo_X_frequency": 1.0, // exponential: -7 to 9 Hz (when sync=0)
    "lfo_X_sync": 1.0, // Sync mode (see below)
    "lfo_X_tempo": 7.0, // Tempo division (see below)
    "lfo_X_sync_type": 0.0, // Retrigger behavior (see below)
    "lfo_X_phase": 0.0, // 0.0 to 1.0 (start phase)
    "lfo_X_fade_time": 0.0, // 0-8 seconds
    "lfo_X_delay_time": 0.0, // 0-4 seconds
    "lfo_X_stereo": 0.0, // -0.5 to 0.5 (phase offset between L/R)
    "lfo_X_smooth_mode": 1.0, // 0=Fade In, 1=Smooth
    "lfo_X_smooth_time": -7.5, // exponential: -10 to 4
    "lfo_X_keytrack_transpose": -12.0, // -60 to +36 (for keytrack mode)
    "lfo_X_keytrack_tune": 0.0 // -1.0 to 1.0 (fine tune for keytrack)
}
```

**LFO Sync Mode Values (`lfo_X_sync`):**
- 0: Seconds (free-running Hz)
- 1: Tempo (synced to BPM)
- 2: Tempo Dotted
- 3: Tempo Triplets
- 4: Keytrack (frequency follows MIDI note)

**LFO Tempo Division Values (`lfo_X_tempo`):**
| Value | Division |
|-------|----------|
| 0 | Freeze |
| 1 | 32/1 |
| 2 | 16/1 |
| 3 | 8/1 |
| 4 | 4/1 |
| 5 | 2/1 |
| 6 | 1/1 |
| 7 | 1/2 |
| 8 | 1/4 |
| 9 | 1/8 |
| 10 | 1/16 |
| 11 | 1/32 |
| 12 | 1/64 |

**LFO Sync Type Values (`lfo_X_sync_type`):**
- 0: Trigger (restart on note)
- 1: Sync (sync to playhead)
- 2: Envelope (one-shot, stops at end)
- 3: Sustain Envelope (holds at sustain point)
- 4: Loop Point (loops from marked point)
- 5: Loop Hold (loops while note held)

### Random LFOs (X = 1 to 4)

```json
{
    "random_X_frequency": 1.0, // exponential: -7 to 9 Hz
    "random_X_sync": 1.0, // 0=Seconds, 1=Tempo, 2=Dotted, 3=Triplets, 4=Keytrack
    "random_X_tempo": 8.0, // 0-12 (same as LFO tempo divisions)
    "random_X_style": 0.0, // Random style (see below)
    "random_X_stereo": 0.0, // 0=off, 1=on (independent L/R values)
    "random_X_sync_type": 0.0, // 0=off, 1=on (sync to note)
    "random_X_keytrack_transpose": -12.0, // -60 to +36
    "random_X_keytrack_tune": 0.0 // -1.0 to 1.0
}
```

**Random Style Values:**
- 0: Perlin (smooth noise)
- 1: Sample & Hold (stepped random)
- 2: Sine Interpolate (sinusoidal transitions)
- 3: Lorenz Attractor (chaotic/organic)

### Macros (1 to 4)

```json
{
    "macro_control_1": 0.0, // 0.0 to 1.0
    "macro_control_2": 0.0,
    "macro_control_3": 0.0,
    "macro_control_4": 0.0
}
```

### Effects

#### Chorus

```json
{
    "chorus_on": 0.0,
    "chorus_dry_wet": 0.5,
    "chorus_frequency": -3.0, // exponential
    "chorus_sync": 1.0,
    "chorus_tempo": 4.0,
    "chorus_voices": 4.0, // 1-4
    "chorus_feedback": 0.4, // -0.95 to 0.95
    "chorus_mod_depth": 0.5,
    "chorus_delay_1": -9.0, // exponential (ms)
    "chorus_delay_2": -7.0,
    "chorus_cutoff": 60.0, // filter cutoff
    "chorus_spread": 1.0 // filter spread
}
```

#### Compressor

```json
{
    "compressor_on": 0.0,
    "compressor_mix": 1.0, // 0.0 to 1.0
    "compressor_attack": 0.5, // 0.0 to 1.0
    "compressor_release": 0.5, // 0.0 to 1.0
    "compressor_enabled_bands": 0.0, // 0=Multiband, 1=Low Band, 2=High Band, 3=Single Band

    // Low band parameters
    "compressor_low_upper_threshold": -28.0, // -80 to 0 dB
    "compressor_low_lower_threshold": -35.0, // -80 to 0 dB
    "compressor_low_upper_ratio": 0.9, // 0.0 to 1.0
    "compressor_low_lower_ratio": 0.8, // -1.0 to 1.0
    "compressor_low_gain": 16.3, // -30 to +30 dB

    // Band (mid) parameters
    "compressor_band_upper_threshold": -25.0,
    "compressor_band_lower_threshold": -36.0,
    "compressor_band_upper_ratio": 0.857,
    "compressor_band_lower_ratio": 0.8,
    "compressor_band_gain": 11.7,

    // High band parameters
    "compressor_high_upper_threshold": -30.0,
    "compressor_high_lower_threshold": -35.0,
    "compressor_high_upper_ratio": 1.0,
    "compressor_high_lower_ratio": 0.8,
    "compressor_high_gain": 16.3
}
```

**Compressor Band Mode Values:**
- 0: Multiband (all three bands active)
- 1: Low Band only
- 2: High Band only
- 3: Single Band (full spectrum)

#### Delay

```json
{
    "delay_on": 0.0,
    "delay_dry_wet": 0.3334,
    "delay_feedback": 0.5, // -1.0 to 1.0
    "delay_frequency": 2.0, // exponential
    "delay_aux_frequency": 2.0,
    "delay_sync": 1.0,
    "delay_tempo": 9.0,
    "delay_aux_sync": 1.0,
    "delay_aux_tempo": 9.0,
    "delay_style": 0.0, // 0=Mono, 1=Stereo, 2=PingPong, 3=MidPingPong
    "delay_filter_cutoff": 60.0,
    "delay_filter_spread": 1.0
}
```

#### Distortion

```json
{
    "distortion_on": 0.0,
    "distortion_type": 0.0, // 0-5 (SoftClip, HardClip, LinFold, SineFold, BitCrush, DownSample)
    "distortion_drive": 0.0, // dB
    "distortion_mix": 1.0,
    "distortion_filter_order": 0.0, // 0=None, 1=Pre, 2=Post
    "distortion_filter_cutoff": 80.0,
    "distortion_filter_resonance": 0.5,
    "distortion_filter_blend": 0.0
}
```

#### EQ

```json
{
    "eq_on": 0.0,
    "eq_low_mode": 0.0, // 0=Shelf, 1=HighPass
    "eq_low_cutoff": 40.0,
    "eq_low_gain": 0.0,
    "eq_low_resonance": 0.3163,
    "eq_band_mode": 0.0, // 0=Shelf, 1=Notch
    "eq_band_cutoff": 80.0,
    "eq_band_gain": 0.0,
    "eq_band_resonance": 0.4473,
    "eq_high_mode": 0.0, // 0=Shelf, 1=LowPass
    "eq_high_cutoff": 100.0,
    "eq_high_gain": 0.0,
    "eq_high_resonance": 0.3163
}
```

#### Flanger

```json
{
    "flanger_on": 0.0,
    "flanger_dry_wet": 0.5,
    "flanger_frequency": 2.0,
    "flanger_sync": 1.0,
    "flanger_tempo": 4.0,
    "flanger_feedback": 0.5,
    "flanger_mod_depth": 0.5,
    "flanger_center": 64.0,
    "flanger_phase_offset": 0.333
}
```

#### Phaser

```json
{
    "phaser_on": 0.0,
    "phaser_dry_wet": 1.0,
    "phaser_frequency": -3.0,
    "phaser_sync": 1.0,
    "phaser_tempo": 3.0,
    "phaser_feedback": 0.5,
    "phaser_center": 80.0,
    "phaser_mod_depth": 24.0,
    "phaser_phase_offset": 0.333,
    "phaser_blend": 1.0
}
```

#### Reverb

```json
{
    "reverb_on": 0.0,
    "reverb_dry_wet": 0.25,
    "reverb_decay_time": 0.0, // exponential
    "reverb_size": 0.5,
    "reverb_delay": 0.0, // pre-delay 0-0.3 secs
    "reverb_pre_low_cutoff": 0.0,
    "reverb_pre_high_cutoff": 110.0,
    "reverb_low_shelf_cutoff": 0.0,
    "reverb_low_shelf_gain": 0.0,
    "reverb_high_shelf_cutoff": 90.0,
    "reverb_high_shelf_gain": -1.0,
    "reverb_chorus_amount": 0.223607, // quadratic
    "reverb_chorus_frequency": -2.0
}
```

#### Effect Chain Order

```json
{
    "effect_chain_order": 0.0 // 0 to 362879 (9! - 1 factorial encoding)
}
```

The effect chain order is encoded as a factorial number representing the permutation of 9 effects:

**Effects in Default Order (value=0):**
0. Chorus
1. Compressor
2. Delay
3. Distortion
4. EQ
5. Filter FX
6. Flanger
7. Phaser
8. Reverb

The value encodes which permutation of these effects to use. To decode/encode:

```python
import math

def decode_effect_order(value, num_effects=9):
    """Decode factorial encoding to effect order"""
    order = []
    remaining = list(range(num_effects))
    for i in range(num_effects - 1, -1, -1):
        factorial = math.factorial(i)
        index = int(value // factorial)
        value = value % factorial
        order.append(remaining.pop(index))
    return order

def encode_effect_order(order, num_effects=9):
    """Encode effect order to factorial value"""
    remaining = list(range(num_effects))
    value = 0
    for i, effect in enumerate(order):
        index = remaining.index(effect)
        remaining.remove(effect)
        value += index * math.factorial(num_effects - 1 - i)
    return value
```

---

## 2. Modulations Array

The modulations array has **64 slots** (indices 1-64). Empty slots have empty strings:

```json
{
    "modulations": [
        {
            "source": "env_1",
            "destination": "filter_1_cutoff"
        },
        {
            "source": "lfo_1",
            "destination": "osc_1_level"
        },
        {
            "source": "macro_control_1",
            "destination": "delay_filter_spread",
            "line_mapping": {
                "name": "Linear",
                "num_points": 2,
                "points": [0.0, 1.0, 1.0, 0.0],
                "powers": [2.815950393676758, 0.0],
                "smooth": false
            }
        },
        { "source": "", "destination": "" }
        // ... 64 total slots
    ]
}
```

**Line Mapping (Optional Modulation Curve):**

The `line_mapping` field allows custom modulation curves instead of linear mapping:

```json
{
    "name": "Linear",           // Display name
    "num_points": 2,            // Number of control points (2-50+)
    "points": [x1, y1, x2, y2, ...], // Pairs of x,y coordinates
    "powers": [p1, p2, ...],    // Curve power per segment
    "smooth": false             // Whether to use smooth interpolation
}
```

**Modulation Sources (Complete List):**

| Source | Description | Default Bipolar |
|--------|-------------|-----------------|
| `env_1` through `env_6` | Envelopes 1-6 | No |
| `lfo_1` through `lfo_8` | LFOs 1-8 | Yes |
| `random_1` through `random_4` | Random LFOs 1-4 | Yes |
| `macro_control_1` through `macro_control_4` | Macro controls 1-4 | No |
| `velocity` | Note velocity (0-1) | No |
| `aftertouch` | Channel aftertouch (0-1) | No |
| `note` | Note number as percentage | No |
| `note_in_octave` | Note within octave (0-1) | No |
| `pitch_wheel` | Pitch bend wheel (-1 to 1) | Yes |
| `mod_wheel` | Modulation wheel (0-1) | No |
| `stereo` | Stereo position (L=-1, R=1) | Yes |
| `random` | Per-voice random value | Yes |
| `slide` | MPE slide (Y-axis) | No |
| `lift` | MPE lift (release velocity) | No |

**Note:** Sources prefixed with `lfo`, `stereo`, `random`, or `pitch` default to bipolar modulation.

**Modulation Destinations (Complete Categories):**

Any parameter in the settings can be a modulation destination. Common categories:

**Oscillators (osc_1, osc_2, osc_3):**
- `osc_X_wave_frame`, `osc_X_frame_spread` - Wavetable position
- `osc_X_level`, `osc_X_pan` - Volume and panning
- `osc_X_transpose`, `osc_X_tune` - Pitch
- `osc_X_unison_detune`, `osc_X_unison_blend` - Unison
- `osc_X_distortion_amount`, `osc_X_distortion_phase`, `osc_X_distortion_spread` - Wave distortion
- `osc_X_spectral_morph_amount`, `osc_X_spectral_morph_spread` - Spectral morph

**Filters (filter_1, filter_2, filter_fx):**
- `filter_X_cutoff`, `filter_X_resonance`, `filter_X_drive`, `filter_X_mix`
- `filter_X_blend`, `filter_X_blend_transpose` - For comb filter
- `filter_X_keytrack` - Keyboard tracking
- `filter_X_formant_x`, `filter_X_formant_y`, `filter_X_formant_transpose` - Formant filter

**Envelopes (env_1 through env_6):**
- `env_X_attack`, `env_X_decay`, `env_X_sustain`, `env_X_release`
- `env_X_delay`, `env_X_hold`
- `env_X_attack_power`, `env_X_decay_power`, `env_X_release_power`

**LFOs (lfo_1 through lfo_8):**
- `lfo_X_frequency`, `lfo_X_tempo`, `lfo_X_phase`
- `lfo_X_fade_time`, `lfo_X_delay_time`
- `lfo_X_smooth_time`

**Effects:**
- Reverb: `reverb_dry_wet`, `reverb_decay_time`, `reverb_size`, `reverb_delay`, `reverb_chorus_amount`
- Delay: `delay_dry_wet`, `delay_feedback`, `delay_tempo`, `delay_aux_tempo`, `delay_filter_cutoff`
- Chorus: `chorus_dry_wet`, `chorus_frequency`, `chorus_mod_depth`, `chorus_feedback`
- Phaser: `phaser_dry_wet`, `phaser_center`, `phaser_mod_depth`, `phaser_feedback`
- Flanger: `flanger_dry_wet`, `flanger_center`, `flanger_mod_depth`, `flanger_feedback`
- Distortion: `distortion_drive`, `distortion_mix`, `distortion_filter_cutoff`
- EQ: `eq_low_gain`, `eq_band_gain`, `eq_high_gain`, `eq_band_cutoff`
- Compressor: `compressor_low_gain`, `compressor_band_gain`, `compressor_high_gain`

**Sample:**
- `sample_level`, `sample_pan`, `sample_transpose`, `sample_tune`

**Voice/Global:**
- `voice_tune`, `voice_transpose`, `voice_amplitude`

**Meta-Modulation:**
- `modulation_X_amount` - Modulate other modulation depths (where X = 1-64)

**Modulation Parameters (stored separately):**

```json
{
    "modulation_X_amount": 0.0, // -1.0 to 1.0
    "modulation_X_power": 0.0, // -10 to 10
    "modulation_X_bipolar": 0.0, // 0=off, 1=on
    "modulation_X_stereo": 0.0, // 0=off, 1=on
    "modulation_X_bypass": 0.0 // 0=off, 1=on
}
```

Where X = 1 to 64 (slot index)

---

## 3. LFO Shapes Array

```json
{
    "lfos": [
        {
            "name": "Triangle",
            "num_points": 3,
            "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
            "powers": [0.0, 0.0, 0.0],
            "smooth": false
        }
        // ... 8 total LFOs
    ]
}
```

**Points format:** `[x1, y1, x2, y2, ..., xN, yN]` where x is 0.0-1.0 (position in cycle) and y is 0.0-1.0 (value). The `powers` array has one value per segment controlling curve shape (0=linear, positive=exponential, negative=logarithmic).

---

## 4. Wavetables Array

Each oscillator has a corresponding wavetable definition (3 total for osc_1, osc_2, osc_3).

**IMPORTANT:** There are two ways to define waveforms in Vital:

1. **Line Source (PREFERRED)** - Defines waveforms using control points and curves. This is the recommended approach for programmatic preset generation as it uses simple numeric data.

2. **Wave Source** - Uses base64-encoded raw audio samples. This is used when loading existing presets or importing audio files, but is NOT recommended for programmatic generation.

### Wavetable Top-Level Structure

```json
{
    "wavetables": [
        {
            "name": "My Wavetable",
            "author": "",
            "full_normalize": true,
            "remove_all_dc": true,
            "version": "1.0.7",
            "groups": [
                {
                    "components": [
                        // Source component (Line Source or Wave Source)
                        // Optional modifier components
                    ]
                }
            ]
        }
        // ... 3 total wavetables (one per oscillator)
    ]
}
```

**Wavetable Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name for the wavetable |
| `author` | string | Optional author name |
| `full_normalize` | boolean | Normalize waveform amplitudes (recommended: true) |
| `remove_all_dc` | boolean | Remove DC offset (recommended: true for most sounds) |
| `version` | string | Vital version string |
| `groups` | array | Array of wavetable groups containing components |

---

### Line Source (PREFERRED for Programmatic Generation)

The **Line Source** component defines waveforms using control points, exactly like LFO shapes. This is the recommended approach for generating presets programmatically because:
- No base64 encoding required
- Human-readable point definitions
- Easy to define mathematically
- Same format used for LFO shapes

#### Line Source Structure

```json
{
    "type": "Line Source",
    "num_points": 3,
    "keyframes": [
        {
            "position": 0,
            "pull_power": 0.0,
            "line": {
                "name": "Saw",
                "num_points": 3,
                "points": [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
                "powers": [0.0, 0.0, 0.0],
                "smooth": false
            }
        }
    ]
}
```

#### Line Generator Format

The `line` object uses the same format as LFO shapes:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name (e.g., "Saw", "Square", "Triangle") |
| `num_points` | int | Number of control points (2-100+) |
| `points` | array | Flat array of [x1, y1, x2, y2, ...] coordinate pairs |
| `powers` | array | Curve power for each point (0 = linear) |
| `smooth` | boolean | If true, applies smooth (sinusoidal) interpolation between points |

**Coordinate System:**
- **X axis (position):** 0.0 = start of waveform cycle, 1.0 = end of cycle
- **Y axis (amplitude):** 0.0 = minimum (-1.0 audio), 1.0 = maximum (+1.0 audio)
- Note: Y values are internally converted as `audio_value = y * 2.0 - 1.0`

**Power Values:**
- `0.0` = Linear interpolation between points
- Positive values = Exponential curve (accelerates toward target)
- Negative values = Logarithmic curve (decelerates toward target)

---

### Common Waveform Definitions (Line Source)

These definitions are derived from the Vital source code (`line_generator.cpp`):

#### Saw Wave (Rising)

```json
{
    "name": "Saw Down",
    "num_points": 3,
    "points": [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
    "powers": [0.0, 0.0, 0.0],
    "smooth": false
}
```

Produces a classic sawtooth wave that rises linearly then resets.

#### Saw Wave (Falling)

```json
{
    "name": "Saw Up",
    "num_points": 3,
    "points": [0.0, 1.0, 1.0, 0.0, 1.0, 1.0],
    "powers": [0.0, 0.0, 0.0],
    "smooth": false
}
```

Produces an inverted sawtooth that falls linearly then resets.

#### Triangle Wave

```json
{
    "name": "Triangle",
    "num_points": 3,
    "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
    "powers": [0.0, 0.0, 0.0],
    "smooth": false
}
```

Rises to peak at 50%, then falls back down.

#### Square Wave

```json
{
    "name": "Square",
    "num_points": 5,
    "points": [0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0],
    "powers": [0.0, 0.0, 0.0, 0.0, 0.0],
    "smooth": false
}
```

Instant transition between high and low at 0% and 50%.

#### Sine Wave

```json
{
    "name": "Sin",
    "num_points": 3,
    "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
    "powers": [0.0, 0.0, 0.0],
    "smooth": true
}
```

Same points as triangle, but with `smooth: true` for sinusoidal interpolation.

#### Pulse Wave (25% Duty Cycle)

```json
{
    "name": "Pulse",
    "num_points": 5,
    "points": [0.0, 1.0, 0.0, 0.0, 0.25, 0.0, 0.25, 1.0, 1.0, 1.0],
    "powers": [0.0, 0.0, 0.0, 0.0, 0.0],
    "smooth": false
}
```

Like square but with asymmetric duty cycle.

#### Custom Waveform Example

```json
{
    "name": "Custom Soft Saw",
    "num_points": 4,
    "points": [0.0, 0.0, 0.8, 0.9, 1.0, 1.0, 1.0, 0.0],
    "powers": [2.0, -1.0, 0.0, 0.0],
    "smooth": false
}
```

A saw-like wave with curved attack (power=2.0) and slight rolloff (power=-1.0).

---

### Complete Line Source Wavetable Example

A full wavetable definition using Line Source:

```json
{
    "name": "Basic Saw",
    "author": "Generated",
    "full_normalize": true,
    "remove_all_dc": true,
    "version": "1.0.7",
    "groups": [
        {
            "components": [
                {
                    "type": "Line Source",
                    "num_points": 3,
                    "keyframes": [
                        {
                            "position": 0,
                            "pull_power": 0.0,
                            "line": {
                                "name": "Saw",
                                "num_points": 3,
                                "points": [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
                                "powers": [0.0, 0.0, 0.0],
                                "smooth": false
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

---

### Morphing Wavetables (Multiple Keyframes)

You can create wavetables that morph between shapes by adding multiple keyframes at different positions (0-256):

```json
{
    "type": "Line Source",
    "num_points": 3,
    "keyframes": [
        {
            "position": 0,
            "pull_power": 0.0,
            "line": {
                "name": "Saw",
                "num_points": 3,
                "points": [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
                "powers": [0.0, 0.0, 0.0],
                "smooth": false
            }
        },
        {
            "position": 128,
            "pull_power": 0.0,
            "line": {
                "name": "Square",
                "num_points": 5,
                "points": [0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0],
                "powers": [0.0, 0.0, 0.0, 0.0, 0.0],
                "smooth": false
            }
        },
        {
            "position": 256,
            "pull_power": 0.0,
            "line": {
                "name": "Sine",
                "num_points": 3,
                "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
                "powers": [0.0, 0.0, 0.0],
                "smooth": true
            }
        }
    ]
}
```

**Note:** When using multiple keyframes with different `num_points`, set the Line Source's top-level `num_points` to match the maximum used in any keyframe.

**Pull Power:** Controls interpolation speed between keyframes (0.0 = linear, positive = slower start, negative = faster start).

---

### Wave Source (For Reference Only)

The **Wave Source** component uses base64-encoded raw waveform data. This is primarily used when:
- Loading existing presets created in Vital's UI
- Importing audio files as wavetables
- Working with complex wavetables that can't be expressed as line shapes

**Note:** Wave Source is NOT recommended for programmatic preset generation. Use Line Source instead.

```json
{
    "type": "Wave Source",
    "interpolation": 1,
    "interpolation_style": 1,
    "keyframes": [
        {
            "position": 0,
            "wave_data": "base64_encoded_float_array...",
            "interpolation": 0
        }
    ]
}
```

**Wave Data Format:**
- Base64-encoded array of 2048 float values (one waveform cycle)
- Each float represents an amplitude sample (-1.0 to 1.0)
- Total size: 2048 × 4 bytes = 8192 bytes before encoding

**Interpolation Styles:**
- 0: Time interpolation (linear blend in time domain)
- 1: Frequency interpolation (spectral morphing - recommended)

---

### Wavetable Component Types Reference

**Source Types (one required per group):**
| Type Name | Description | Recommended |
|-----------|-------------|-------------|
| `"Line Source"` | Point-based waveform generation | **Yes** |
| `"Wave Source"` | Base64-encoded raw waveform data | No (use for imports only) |
| `"Audio File Source"` | Waveform from imported audio | No |
| `"Shepard Tone Source"` | Shepard tone generator | No (deprecated) |

**Modifier Types (optional, applied after source):**
| Type Name | Description |
|-----------|-------------|
| `"Phase Shift"` | Shifts the phase of the waveform |
| `"Wave Window"` | Applies amplitude windowing/envelope |
| `"Frequency Filter"` | Spectral filtering (LP, HP, BP) |
| `"Slew Limiter"` | Limits rate of change (smoothing) |
| `"Wave Folder"` | Wave folding distortion |
| `"Wave Warp"` | Time-domain warping |

---

## 5. Sample Data

The sample object is stored inside `settings`. Unlike wavetables (which can use Line Source), samples **require base64-encoded audio data** as there is no point-based alternative.

```json
{
    "sample": {
        "name": "my_sample.wav",
        "length": 44100,
        "sample_rate": 44100,
        "samples": "base64_encoded_pcm_data",
        "samples_stereo": "base64_encoded_pcm_data"
    }
}
```

**Sample encoding:** PCM data is stored as base64-encoded 16-bit signed integer arrays. Stereo samples have a separate `samples_stereo` field for the right channel.

**Note:** `sample_rate` also appears at the top level of `settings` (typically 44100) as a global reference.

**Recommendation:** For programmatic preset generation, consider using the Sample oscillator only when you have actual audio files to embed. For synthesized sounds, use the three main oscillators with Line Source wavetables instead.

---

## 6. Python Examples

### Example 1: Modify an Existing Preset

```python
import json

# Load preset
with open("my_preset.vital", "r") as f:
    preset = json.load(f)

# Modify parameters
preset["settings"]["osc_1_level"] = 0.5
preset["settings"]["filter_1_cutoff"] = 80.0
preset["settings"]["reverb_on"] = 1.0
preset["settings"]["reverb_dry_wet"] = 0.3

# Find an empty modulation slot (modulations is a 64-item array)
def find_empty_slot(modulations):
    for i, mod in enumerate(modulations):
        if mod.get("source", "") == "" and mod.get("destination", "") == "":
            return i
    return None

slot = find_empty_slot(preset["settings"]["modulations"])
if slot is not None:
    # Set the modulation connection
    preset["settings"]["modulations"][slot] = {
        "source": "env_2",
        "destination": "osc_1_wave_frame"
    }
    # Set modulation amount (1-indexed)
    preset["settings"][f"modulation_{slot + 1}_amount"] = 0.5
    preset["settings"][f"modulation_{slot + 1}_bipolar"] = 1.0

# Save preset
with open("modified_preset.vital", "w") as f:
    json.dump(preset, f)
```

### Example 2: Create Wavetables Using Line Source

```python
import json

# Common waveform definitions (from Vital's line_generator.cpp)
WAVEFORMS = {
    "saw_up": {
        "name": "Saw Up",
        "num_points": 3,
        "points": [0.0, 1.0, 1.0, 0.0, 1.0, 1.0],
        "powers": [0.0, 0.0, 0.0],
        "smooth": False
    },
    "saw_down": {
        "name": "Saw Down",
        "num_points": 3,
        "points": [0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
        "powers": [0.0, 0.0, 0.0],
        "smooth": False
    },
    "triangle": {
        "name": "Triangle",
        "num_points": 3,
        "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
        "powers": [0.0, 0.0, 0.0],
        "smooth": False
    },
    "square": {
        "name": "Square",
        "num_points": 5,
        "points": [0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0],
        "powers": [0.0, 0.0, 0.0, 0.0, 0.0],
        "smooth": False
    },
    "sine": {
        "name": "Sin",
        "num_points": 3,
        "points": [0.0, 1.0, 0.5, 0.0, 1.0, 1.0],
        "powers": [0.0, 0.0, 0.0],
        "smooth": True  # smooth=True creates sinusoidal curves
    }
}

def create_line_source_wavetable(name, waveform_key, author=""):
    """Create a wavetable using Line Source (no base64 needed)."""
    waveform = WAVEFORMS[waveform_key]
    return {
        "name": name,
        "author": author,
        "full_normalize": True,
        "remove_all_dc": True,
        "version": "1.0.7",
        "groups": [
            {
                "components": [
                    {
                        "type": "Line Source",
                        "num_points": waveform["num_points"],
                        "keyframes": [
                            {
                                "position": 0,
                                "pull_power": 0.0,
                                "line": waveform
                            }
                        ]
                    }
                ]
            }
        ]
    }

def create_morphing_wavetable(name, waveform_keys, author=""):
    """Create a wavetable that morphs between multiple waveforms."""
    num_waveforms = len(waveform_keys)
    max_points = max(WAVEFORMS[k]["num_points"] for k in waveform_keys)
    
    keyframes = []
    for i, key in enumerate(waveform_keys):
        position = int((i / (num_waveforms - 1)) * 256) if num_waveforms > 1 else 0
        keyframes.append({
            "position": position,
            "pull_power": 0.0,
            "line": WAVEFORMS[key]
        })
    
    return {
        "name": name,
        "author": author,
        "full_normalize": True,
        "remove_all_dc": True,
        "version": "1.0.7",
        "groups": [
            {
                "components": [
                    {
                        "type": "Line Source",
                        "num_points": max_points,
                        "keyframes": keyframes
                    }
                ]
            }
        ]
    }

# Example: Create a preset with Line Source wavetables
preset = {
    "author": "Generated",
    "comments": "Programmatically generated preset",
    "preset_name": "Generated Pad",
    "preset_style": "Pad",
    "synth_version": "1.0.7",
    "settings": {
        # Basic oscillator settings
        "osc_1_on": 1.0,
        "osc_1_level": 0.707,
        "osc_1_unison_voices": 4.0,
        "osc_1_unison_detune": 2.0,
        
        # Filter settings
        "filter_1_on": 1.0,
        "filter_1_cutoff": 80.0,
        "filter_1_resonance": 0.3,
        
        # Envelope
        "env_1_attack": 0.5,
        "env_1_decay": 1.0,
        "env_1_sustain": 0.7,
        "env_1_release": 1.0,
        
        # Create wavetables using Line Source
        "wavetables": [
            create_line_source_wavetable("Saw Osc 1", "saw_up"),
            create_morphing_wavetable("Morph Osc 2", ["sine", "triangle", "square"]),
            create_line_source_wavetable("Triangle Osc 3", "triangle")
        ],
        
        # Empty modulations array (64 slots)
        "modulations": [{"source": "", "destination": ""} for _ in range(64)],
        
        # Default LFO shapes
        "lfos": [WAVEFORMS["triangle"].copy() for _ in range(8)]
    }
}

# Save the preset
with open("generated_preset.vital", "w") as f:
    json.dump(preset, f, indent=2)

print("Preset created successfully!")
```

### Example 3: Create Custom Waveforms

```python
def create_custom_waveform(points_xy, smooth=False, name="Custom"):
    """
    Create a custom waveform from a list of (x, y) tuples.
    
    Args:
        points_xy: List of (x, y) tuples where:
                   - x is 0.0-1.0 (position in cycle)
                   - y is 0.0-1.0 (amplitude, 0.5 = zero crossing)
        smooth: If True, use sinusoidal interpolation
        name: Display name
    
    Returns:
        Line generator dict for use in wavetables
    """
    flat_points = []
    for x, y in points_xy:
        flat_points.extend([x, y])
    
    return {
        "name": name,
        "num_points": len(points_xy),
        "points": flat_points,
        "powers": [0.0] * len(points_xy),
        "smooth": smooth
    }

# Example: Create a "soft pulse" waveform
soft_pulse = create_custom_waveform([
    (0.0, 0.5),   # Start at zero
    (0.1, 1.0),   # Quick rise to max
    (0.4, 1.0),   # Hold at max
    (0.5, 0.5),   # Return to zero
    (0.6, 0.0),   # Quick fall to min
    (0.9, 0.0),   # Hold at min
    (1.0, 0.5)    # Return to zero
], smooth=True, name="Soft Pulse")

# Example: Create an asymmetric triangle
asymmetric_tri = create_custom_waveform([
    (0.0, 1.0),   # Start at max
    (0.3, 0.0),   # Quick fall to min (30% of cycle)
    (1.0, 1.0)    # Slow rise back to max (70% of cycle)
], smooth=False, name="Asymmetric Triangle")
```

---

## 7. Value Scaling Reference

Different parameters use different scaling modes to convert stored values to actual values:

### Scaling Types

| Type | Formula | Example Parameters |
|------|---------|-------------------|
| Linear | `actual = stored` | cutoff, resonance, pan |
| Quadratic | `actual = stored²` | osc_level, sample_level, unison_detune |
| Square Root | `actual = √stored` | volume |
| Exponential | `actual = 2^stored` | frequency, portamento_time, delay_frequency |
| Quartic | `actual = stored⁴` | env_attack, env_decay, env_release |
| Indexed | `actual = round(stored)` | polyphony, tempo, style enums |

### Common Parameter Ranges

```python
# Volume: stored 0-7399.4404, actual -80dB to 0dB
# Formula: dB = 20 * log10(sqrt(stored / 7399.4404))
volume_db = 20 * math.log10(math.sqrt(stored / 7399.4404))

# BPM: stored 0.333-5.0, actual 20-300 BPM
bpm = stored * 60

# Cutoff: stored 8-136, actual MIDI note number
# 60 = middle C, each unit = 1 semitone
cutoff_hz = 440 * 2**((stored - 69) / 12)

# Envelope times: stored 0-2.378, actual 0-32 seconds
# Formula: actual = stored⁴ * 32
env_time_seconds = (stored ** 4) * 32
```

