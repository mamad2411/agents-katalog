---
name: software-defined-radio
description: Deep Software Defined Radio (SDR) expertise for receive, analyze, decode and (authorized) transmit work. Covers DSP fundamentals (sampling, IQ/complex baseband, FFT, filtering, decimation, AGC, timing/carrier recovery), analog and digital modulation/demodulation, hardware selection and quirks (RTL-SDR, HackRF, Airspy, SDRplay, ADALM-Pluto, LimeSDR, BladeRF, USRP, KrakenSDR), GNU Radio flowgraphs, Python DSP with numpy/scipy/SoapySDR/pyrtlsdr, protocol decoding (ADS-B, AIS, ACARS, APRS, POCSAG, DMR, P25, TETRA, NOAA/Meteor satellites, LoRa, rtl_433 ISM sensors, GSM/LTE scanning), signal identification, IQ recording formats and SigMF, antennas and RF front-end, troubleshooting, and spectrum regulations (ITU, FCC, Ofcom, ETSI, Indonesia Komdigi). Use whenever the user mentions SDR, RTL-SDR, HackRF, GNU Radio, IQ samples, spectrum, waterfall, demodulation, radio protocols, RF capture, or any radio receive/transmit experiment.
license: MIT
compatibility: Bundled scripts need Python 3.9+ with numpy; scipy and matplotlib are optional. SDR command-line tools (rtl_sdr, hackrf_transfer, SoapySDRUtil, GNU Radio) are optional and only needed for live hardware work.
metadata:
  author: briannasywa
  version: "1.0.0"
  domain: radio-frequency, dsp, wireless
---

> **移植说明（FutureOS，2026-11-02）**
>
> 上游 `briannasywa/sdr-skills` @ `f6aab2dfbe6d`（MIT），单技能目录原样导入：本文件 +
> 14 篇 `references/` + 8 个工具脚本（另有共享库 `_common.py`）+ 2 个 GNU Radio 模板。
> 除本块外正文逐字节未改；出处、改动范围与完整缺陷清单见同目录 `SOURCE.md`。
>
> **本机实测范围**（Python 3.13.16 / numpy 2.5.4 / scipy 1.18.1 / matplotlib 3.11.2）：
> 9 个 `.py` 全部 `py_compile` 通过、8 个工具 `--help` 全部 exit 0；在合成 IQ 上跑通
> `sdr_calc`(12 子命令)、`iq_info`、`iq_spectrum`(PNG 与 `--ascii`)、`iq_convert`、
> `fm_demod`(WBFM/NBFM/AM，1 kHz 音调还原到 999.8 Hz)、`symbol_rate`(50 kBd 合成 BPSK
> 报 50.000 kBaud)、`sigmf_write`、`probe_devices`。**没有 SDR 硬件，也没有 GNU Radio**：
> `probe_devices` 只验证过「无设备」路径，`references/python-sdr.md` §4 的实流代码块、
> 2 个 GNU Radio 模板、`references/protocols.md` 里的外部解码器命令**未跑通**，只做了语法与
> 参数形态核对。
>
> **三处会直接踩坑的上游缺陷（未改正文，按此处置）**
>
> 1. `iq_convert.py --shift -250e3`（§7 与 `references/iq-formats.md` 的示例写法）会被 argparse
>    当成选项，实测 `exit 2: argument --shift: expected one argument`。改用
>    `--shift=-250e3` 或 `--shift -250000`；`fm_demod.py --offset` 同理，负数一律用 `=`。
> 2. `--decim N` 在 N 不能分解成 ≤8 的整数连乘时**静默少抽取**：`--decim 10` 实际只做 `/8`，
>    却仍打印 `new fs 240.000 kHz`（真实 300 kHz）。`references/python-sdr.md` §2 的 `decim()`
>    是同一 bug。要精确抽取就用 2/4/5/8/16/32/64… 这类因子，或自己写
>    `signal.decimate` + 显式 `[::k]` 并在下游按实际样本数重算 `fs`。
> 3. `sdr_calc.py dbm` 显示重复单位（`10.000 nW W`），数值正确。
>
> 其余小瑕（`cs12` 声明、`utcnow()` 弃用、`sigmf_write` 示例的 cs16+HackRF 矛盾等）见
> `SOURCE.md` 的「上游缺陷」。

# Software Defined Radio (SDR)

You are an SDR engineer. You reason from first principles (sample rate, bandwidth,
SNR, modulation) and then give concrete, runnable commands and parameter values.
This file is the map; the `references/` files hold the depth. Load a reference
only when the task needs it.

## 0. Ground rules (always apply)

1. **Receive-only is the default.** Listening to most signals is legal in most
   countries; transmitting almost always needs a license or an unlicensed-band
   exemption. Never assume the user may transmit. Ask what license/authorization
   they hold when TX is involved.
2. **Never help jam, spoof, replay against systems the user does not own, or
   intercept private communications** (cellular voice/data, encrypted public
   safety, private messaging). Decoding your own devices, broadcast, aviation,
   maritime, amateur, weather satellites and unencrypted telemetry is normal SDR work.
3. **Lab transmit = cable, not antenna.** For replay/emulation experiments on the
   user's own devices: SMA cable + 30-40 dB attenuator into the target, or a
   shielded box. See `references/transmission-lab-safety.md`.
4. **State assumptions explicitly**: hardware, center frequency, sample rate,
   gain, sample format, OS. If unknown, pick a sensible default and say so.
5. When regulations matter, give the concrete rule for the user's country if
   known (`references/regulations.md`), otherwise ITU-region-level guidance.

## 1. Task router

| User wants to... | Read | Run / use |
|---|---|---|
| Understand sampling, IQ, FFT, filters, decimation, SNR, Eb/N0 | `references/dsp-fundamentals.md` | `scripts/sdr_calc.py` |
| Identify an unknown signal on the waterfall | `references/signal-identification.md`, `references/modulation.md` | `scripts/iq_info.py`, `scripts/symbol_rate.py`, `scripts/iq_spectrum.py` |
| Demodulate AM/FM/SSB/FSK/PSK/QAM/OFDM/LoRa | `references/modulation.md` | `scripts/fm_demod.py`, GNU Radio templates in `assets/templates/` |
| Choose or configure hardware | `references/hardware.md` | `scripts/probe_devices.py` |
| Install/choose software, drivers, decoders | `references/software-toolchain.md` | - |
| Build or debug a GNU Radio flowgraph | `references/gnuradio.md` | `assets/templates/gr_*.py` |
| Write Python that reads IQ or streams from an SDR | `references/python-sdr.md` | `scripts/iq_*.py` as starting points |
| Decode a specific protocol (ADS-B, AIS, APRS, POCSAG, DMR, LoRa, rtl_433, satellites...) | `references/protocols.md` | tool listed per protocol |
| Antenna, coax, LNA, filter, link budget | `references/antennas-rf-frontend.md` | `scripts/sdr_calc.py fspl / dipole / friis` |
| Record, convert, or share IQ files (cu8/cs8/cs16/cf32/wav/SigMF) | `references/iq-formats.md` | `scripts/iq_convert.py`, `scripts/sigmf_write.py` |
| Legal question: can I receive/transmit X in country Y | `references/regulations.md` | - |
| Device not found, overruns, drift, spurs, no audio | `references/troubleshooting.md` | `scripts/probe_devices.py` |
| Transmit, replay, emulate in a lab | `references/transmission-lab-safety.md` | - |
| Direction finding, passive radar, ML classification, RFNoC/FPGA | `references/advanced-topics.md` | - |

## 2. Mental model: the SDR receive chain

```
antenna -> [filter] -> [LNA] -> tuner/mixer -> ADC -> (I,Q) samples -> DSP -> demod -> decoder -> data/audio
            RF front-end (analog)             |        software (this skill)
                                     center freq f_c, sample rate f_s
```

Six numbers pin down every SDR task. Always establish them first:

| Number | Meaning | Typical |
|---|---|---|
| `f_c` | Center (tuned) frequency | e.g. 1090 MHz for ADS-B |
| `f_s` | Complex sample rate = usable span (before roll-off) | RTL-SDR 2.4 MS/s, HackRF 10-20 MS/s |
| `BW` | Bandwidth of the signal you want | NBFM 12.5 kHz, WBFM 200 kHz, ADS-B 2 MHz |
| gain | RF/IF/baseband gain staging | RTL-SDR 20-40 dB; avoid clipping |
| ppm | Crystal offset correction | RTL-SDR 0-60 ppm (TCXO models ~1 ppm) |
| format | Sample type on disk/stream | cu8 (rtl_sdr), cs8 (hackrf), cs16 (UHD/Pluto), cf32 (GNU Radio) |

With complex (IQ) sampling the observable span equals `f_s` (from `f_c - f_s/2` to
`f_c + f_s/2`). With real sampling it is `f_s/2`. Decimating by N after a low-pass
filter reduces `f_s` to `f_s/N` and keeps only `+-f_s/(2N)` around the (shifted) center.

## 3. Formula cheat sheet

```
wavelength           lambda = c / f = 299.792458 / f_MHz  [m]
half-wave dipole     L_total ~= 143 / f_MHz [m]   (each leg ~= 71.5/f_MHz; includes ~0.95 end-effect factor)
quarter-wave         L ~= 71.5 / f_MHz [m]
dBm <-> W            P_dBm = 10*log10(P_W*1000);  P_W = 10^((P_dBm-30)/10)
dBm <-> uV (50 ohm)  V_rms = sqrt(P_W*50);  0 dBm = 223.6 mV rms; -107 dBm ~= 1 uV
thermal noise floor  N = -174 dBm/Hz + 10*log10(BW_Hz) + NF_dB    (2 MHz, NF 6 dB -> -105 dBm)
FSPL                 L_dB = 20*log10(d_km) + 20*log10(f_MHz) + 32.44
link budget          P_rx = P_tx + G_tx - L_path - L_cable + G_rx
Friis cascade NF     F = F1 + (F2-1)/G1 + (F3-1)/(G1*G2)   (linear; the first LNA dominates)
Carson rule (FM)     BW ~= 2*(dev + f_m)     NBFM: 2*(2.5k+3k)=11 kHz; WBFM: 2*(75k+15k)=180 kHz
FFT resolution       df = f_s / N_FFT;  time per FFT frame = N_FFT / f_s
processing gain      G_p = 10*log10(f_s / BW_signal)  when narrowing to the signal BW
Eb/N0 <-> SNR        Eb/N0 = SNR_dB - 10*log10(R_b / BW)
Doppler (LEO ~7.5 km/s)  df ~= f*v_r/c ; 137 MHz -> +-3.5 kHz ; 1.7 GHz -> +-40 kHz
symbol rate vs RRC BW    BW ~= R_s*(1+alpha)   (alpha roll-off 0.2-0.5)
file size            bytes = f_s * seconds * bytes_per_complex_sample (cu8 2, cs16 4, cf32 8)
```

`scripts/sdr_calc.py` implements all of these (`python scripts/sdr_calc.py --help`).

## 4. Hardware quick pick

| Need | Pick | Why |
|---|---|---|
| Cheapest start, 24 MHz-1.7 GHz RX | RTL-SDR Blog V4 (or V3) | 8-bit, 2.4 MS/s, TCXO, bias tee, HF via built-in upconverter (V4) |
| Better dynamic range RX, HF-UHF | Airspy R2/Mini, SDRplay RSPdx/RSP1B | 12-14 bit, 6-10 MHz span, strong filtering |
| HF only, very high performance | Airspy HF+ Discovery | 0.5-31 MHz + 60-260 MHz, excellent dynamic range |
| TX + RX, 1 MHz-6 GHz, hobby budget | HackRF One (+ PortaPack) | 8-bit, half-duplex, 20 MS/s, well supported |
| Full-duplex 2x2, 70 MHz-6 GHz, cheap | ADALM-Pluto (after freq hack) | 12-bit, 61.44 MS/s (USB2 limits ~4-5 MS/s sustained), libiio |
| Full-duplex, 47 MHz-6 GHz, more BW | BladeRF 2.0 micro, LimeSDR (Mini) | 12-bit, 61.44 MS/s, USB3, FPGA |
| Research/pro, 70 MHz-6 GHz | USRP B200/B210/B205mini, X310 | UHD, 56 MS/s (B2x0), GPSDO options |
| Direction finding | KrakenSDR (5 coherent RTL-SDR) | MUSIC DoA out of the box |

Details, quirks, and driver names: `references/hardware.md`.

## 5. Software quick pick

| Purpose | Tool |
|---|---|
| General listening / waterfall | SDR++ (all OS), SDRangel, GQRX (Linux/mac), SDR# (Windows), SDRconnect |
| Flowgraph DSP | GNU Radio 3.10.x (GRC) |
| Reverse-engineering a digital signal | Universal Radio Hacker (URH), inspectrum, SigDigger |
| ISM sensors / keyfobs / weather stations | rtl_433 |
| ADS-B | dump1090-fa, readsb |
| AIS | AIS-catcher |
| Pagers, AFSK, FLEX, POCSAG | multimon-ng, PDW |
| APRS/packet | direwolf |
| Digital voice (DMR/P25/NXDN/D-STAR) | SDRTrunk, DSD-FME, OP25 |
| Satellites (NOAA/Meteor/GOES/...) | SatDump, gr-satellites, gpredict (tracking) |
| ACARS / VDL2 | acarsdec, dumpvdl2 |
| LoRa | gr-lora_sdr, LoRa-SDR |
| Python | pyrtlsdr, SoapySDR, pyadi-iio, uhd, numpy/scipy, sigmf |
| Remote / networked SDR | rtl_tcp, SoapyRemote, SpyServer, OpenWebRX+ |

Install recipes per OS: `references/software-toolchain.md`.

## 6. Standard workflows

### 6A. Identify an unknown signal

1. Pin the six numbers. Record 10-30 s of IQ at the narrowest `f_s` that contains the
   whole signal (`rtl_sdr -f <Hz> -s 2400000 -g 30 out.cu8`).
2. Measure: center frequency, occupied bandwidth (-20 dB), burst length/period, duty
   cycle, number of simultaneous channels. `python scripts/iq_info.py out.cu8 --fs 2.4e6 --fc <Hz>`.
3. Look at the waterfall shape (`scripts/iq_spectrum.py` or inspectrum) and match it to the
   signatures table in `references/signal-identification.md`. Cross-check against
   sigidwiki.com by frequency and bandwidth.
4. Estimate symbol rate and modulation order: `python scripts/symbol_rate.py out.cu8 --fs 2.4e6`
   (uses |x|^2 and |x|^4 spectral lines plus autocorrelation).
5. Demodulate to bits in URH or GNU Radio; look for preamble/sync word, packet length,
   CRC. Then search for a known decoder before writing one.
6. Write a signal report (template: `assets/templates/signal-report-template.md`).

### 6B. Receive and decode a known protocol

Pattern: `SDR -> (optional) rtl_tcp/SoapyRemote -> decoder -> viewer/logger`. For every
protocol the reference gives: frequency, modulation, bandwidth, minimum `f_s`, gain hints,
tool + exact command, legal note. Three canonical examples:

```bash
# ADS-B (1090 MHz, PPM, 2 MS/s)
dump1090-fa --device-type rtlsdr --gain 40 --net --lat <lat> --lon <lon>
# ISM sensors (433.92 / 868 / 915 MHz, OOK/FSK)
rtl_433 -f 433.92M -s 250k -F json          # add -f 868M -f 915M -H 60 to hop
# NOAA APT (137 MHz, WBFM ~40 kHz) -> SatDump records + decodes
satdump live noaa_apt out --source rtlsdr --samplerate 1e6 --frequency 137.1e6 --gain 40
```

Full catalog: `references/protocols.md`.

### 6C. Build a GNU Radio flowgraph

Rules that prevent 90% of broken flowgraphs:

1. Track sample rate through every block; write it on the canvas as variables
   (`samp_rate`, `audio_rate`, `decim`). Audio sinks need 48 k or 44.1 k exactly.
2. Match item types: SDR sources emit complex float32 (`cf32`); demods emit float32.
3. Frequency-translate + low-pass + decimate in one block (`Frequency Xlating FIR Filter`).
4. No `Throttle` when a hardware source/sink is present; exactly one Throttle when only
   files/simulated signals are present.
5. Use `Rational Resampler` to get from the SDR rate to the demod rate to the audio rate.
6. For digital: RRC matched filter -> `Symbol Sync` (or Polyphase Clock Sync) -> `Costas Loop`
   (PSK) -> `Constellation Decoder` -> differential decode -> `Correlate Access Code`.
7. Underrun `U` / overrun `O` in the console means the CPU cannot keep up or the USB link
   is starved; reduce `f_s`, decimate earlier, avoid GUI sinks at full rate.

Block-by-block guidance, message passing, OOT modules, Python flowgraphs: `references/gnuradio.md`.
Templates: `assets/templates/gr_wbfm_rx.py`, `assets/templates/gr_fsk_rx.py`.

### 6D. Python DSP on an IQ file (canonical skeleton)

```python
import numpy as np
from scipy import signal

fs, fc = 2.4e6, 100.1e6
raw = np.fromfile("cap.cu8", dtype=np.uint8).astype(np.float32)
iq = (raw[0::2] - 127.5) / 127.5 + 1j * (raw[1::2] - 127.5) / 127.5   # cu8 -> complex
iq -= iq.mean()                                                          # remove DC spike

f_offset = 250e3                                                         # signal at fc+250 kHz
t = np.arange(len(iq)) / fs
iq = iq * np.exp(-2j * np.pi * f_offset * t)                             # shift to 0 Hz
decim = 10                                                               # 2.4 MS/s -> 240 kS/s
iq = signal.decimate(iq, decim, ftype="fir", zero_phase=True)            # LPF + decimate
fs /= decim

audio = np.angle(iq[1:] * np.conj(iq[:-1]))                              # FM discriminator
audio = signal.decimate(audio, 5, ftype="fir")                           # 240k -> 48k
audio /= np.max(np.abs(audio)) + 1e-9
```

Reading every format, live streaming with SoapySDR/pyrtlsdr, PSD/waterfall, PLL, FSK/PSK
demod, SigMF I/O: `references/python-sdr.md`. Working scripts: `scripts/`.

### 6E. Record IQ properly

- Choose `f_s` >= 1.25 x signal BW (plus room for drift); more is not better (file size, CPU).
- Set gain so the peak is 6-10 dB below full scale; check for clipping with `iq_info.py`.
- Always store `f_c`, `f_s`, format, gain, datetime, antenna, and location. Prefer SigMF
  (`scripts/sigmf_write.py`) or the tool's native metadata (SDR++/SDR# WAV headers).
- Name files `YYYYMMDD_HHMMSS_<fc_Hz>_<fs_Hz>_<fmt>.<ext>` when no metadata container is used.
- Sizes: cu8 at 2.4 MS/s = 4.8 MB/s; cs16 at 20 MS/s = 80 MB/s; cf32 at 20 MS/s = 160 MB/s.

Formats and converters: `references/iq-formats.md`.

### 6F. Transmit (only when authorized)

Before any TX command: confirm authorization (amateur license class + band plan, or
unlicensed band limits, or a cabled lab setup). Then: correct antenna/dummy load, low-pass
filter for harmonics, start at minimum gain, never key up on emergency/aviation/GNSS/cellular
frequencies. Details, HackRF/Pluto/USRP TX gain tables, replay method: `references/transmission-lab-safety.md`.

### 6G. Troubleshooting triage

| Symptom | First check |
|---|---|
| Device not found | Windows: Zadig WinUSB; Linux: udev rules + blacklist `dvb_usb_rtl28xxu`; USB cable/hub |
| Audio stutters, `O`/`U` printed | Sample rate too high for CPU/USB; lower `f_s`; direct USB port; no USB2 hub for USB3 devices |
| Signal appears at wrong frequency | ppm correction; check with a known signal (FM pilot, NOAA, GSM `kal`) |
| Big spike at center | DC offset: tune off-center + shift in DSP, or enable offset tuning / DC blocker |
| Mirror copy of a strong signal | IQ imbalance or aliasing; enable IQ correction, add filter, lower gain |
| Whole band full of strong FM stations / ghosts | Front-end overload; add FM notch (88-108 MHz), lower gain, AGC off |
| Nothing but noise | Antenna/coax/bias-tee, wrong band, gain too low, wrong sample format |

Full decision tree: `references/troubleshooting.md`.

## 7. Bundled scripts (Python 3.9+, numpy; scipy/matplotlib optional)

| Script | Purpose | Example |
|---|---|---|
| `sdr_calc.py` | All calculators from section 3 | `python scripts/sdr_calc.py fspl --d-km 10 --f-mhz 915` |
| `iq_info.py` | Detect format, DC offset, clipping, RMS, occupied BW, peak frequency | `python scripts/iq_info.py cap.cu8 --fs 2.4e6 --fc 433.92e6` |
| `iq_spectrum.py` | Welch PSD + waterfall to PNG (or ASCII fallback) | `python scripts/iq_spectrum.py cap.cs8 --fs 8e6 --fc 915e6 -o spec.png` |
| `iq_convert.py` | Convert cu8/cs8/cs16/cf32/cf64/wav to each other, optional shift/decimate/trim | `python scripts/iq_convert.py in.cu8 out.cf32 --fs 2.4e6 --shift -250e3 --decim 10` |
| `sigmf_write.py` | Create `.sigmf-meta` for an existing capture | `python scripts/sigmf_write.py cap.cs16 --fs 4e6 --fc 1090e6 --hw "HackRF One"` |
| `fm_demod.py` | WBFM/NBFM/AM demod from IQ file to WAV | `python scripts/fm_demod.py cap.cu8 --fs 2.4e6 --offset 0 --mode wbfm -o out.wav` |
| `symbol_rate.py` | Symbol-rate and modulation-order hints for digital bursts | `python scripts/symbol_rate.py cap.cu8 --fs 2.4e6` |
| `probe_devices.py` | Enumerate attached SDRs via rtl_test, hackrf_info, SoapySDRUtil, uhd, iio | `python scripts/probe_devices.py` |

All scripts print `--help`, accept `--fs`/`--fc` in Hz or with SI suffixes (`2.4M`, `433.92M`),
and infer sample format from the extension (`.cu8 .cs8 .cs16 .cf32 .cf64 .wav .sigmf-data`).

## 8. Conventions and gotchas

- **Sample format confusion is the number one bug.** rtl_sdr writes unsigned 8-bit (`cu8`,
  127.5 offset). HackRF writes signed 8-bit (`cs8`). Pluto/UHD/SDRplay write signed 16-bit
  (`cs16`, often 12-bit left- or right-justified). GNU Radio file sinks write `cf32`
  little-endian, interleaved I,Q. Nothing on disk tells you which; file size only tells you
  the sample count.
- **`f_s` is the complex rate.** A 2.4 MS/s RTL-SDR shows 2.4 MHz of spectrum, not 1.2 MHz.
- **RTL-SDR usable rates**: 225 001-300 000 and 900 001-3 200 000 Hz; 2.4 MS/s is the top
  reliable rate, 2.56 MS/s usually works, 3.2 MS/s drops samples.
- **HackRF**: minimum stable 2 MS/s (use 8-10 MS/s and decimate); 8-bit means ~48 dB dynamic
  range; RX gain = LNA (0-40, 8 dB steps) + VGA (0-62, 2 dB steps) + amp (14 dB); TX gain 0-47 dB.
- **Pluto**: stock firmware limits 325-3800 MHz; the `ad9364` hack extends to 70-6000 MHz.
  USB2 throughput caps sustained streaming at ~4-5 MS/s; set `rx_buffer_size` large.
- **Gain staging**: too much gain creates intermod products that look like real signals.
  Reduce gain until spurious signals disappear, then add 3 dB.
- **Bias tee**: only turn it on when an LNA is attached; it can damage a DC-shorted antenna
  or the device. RTL-SDR V3/V4: `rtl_biast -b 1` or the `-T` flag in tools.
- **Frequency accuracy**: cheap crystals drift with temperature; TCXO ~0.5-1 ppm; for
  narrowband digital (POCSAG, DMR, LoRa SF12) calibrate ppm first.
- **Windows drivers**: Zadig on the RTL-SDR (`Bulk-In, Interface 0`) installs WinUSB;
  never install it on your mouse. SDR# ships its own driver bundle; GNU Radio on Windows is
  easiest via radioconda.
- **Time**: LEO satellite passes, ADS-B multilateration and TDOA need accurate time; use NTP
  at least, GPSDO/PPS for coherent or timing work.

## 9. How to answer SDR questions

- Lead with the concrete recipe (hardware + frequency + `f_s` + gain + tool + command), then
  explain the why in two or three sentences.
- Quote numbers with units; give both the formula and the evaluated value.
- When the user's hardware is unknown, give the RTL-SDR path first and note what changes
  for HackRF/Pluto/USRP.
- Prefer existing, maintained decoders over writing one; write DSP code when the user is
  learning, reverse-engineering, or nothing exists.
- Add the legal/safety line only when the task actually touches transmission, private
  communications, or a country-specific restriction. One sentence, not a lecture.
- If a claim depends on a tool version or a regulation that changes, say "as of 2026" and
  tell the user how to verify (man page, `--help`, official regulator page).
