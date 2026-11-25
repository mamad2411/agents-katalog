---
name: ziwei-chart-reader
description: Use this skill when the user needs an actual Zi Wei Dou Shu chart computed or inspected from birth data, including palaces, major stars, minor stars, body/soul palaces, decadal luck, yearly luck, and palace-level support for career, wealth, relationships, or life transitions. Trigger this skill when interpretation should be grounded in a generated chart rather than only a screenshot or symbolic paraphrase.
---

# Ziwei Chart Reader

## Overview

This skill computes and summarizes Zi Wei Dou Shu charts using the open-source `iztro` library, then helps Codex interpret the result in clear language.

Use it when the user needs:

- a Zi Wei Dou Shu chart generated from birth data
- palace and star support for a conclusion
- yearly or decadal palace movement
- automatic yearly focus summaries for `官禄`, `财帛`, and `迁移`
- a transparent bridge between raw chart output and practical interpretation

## Source

This skill uses the MIT-licensed `iztro` library:

- GitHub: [SylarLong/iztro](https://github.com/SylarLong/iztro)
- npm: [iztro](https://www.npmjs.com/package/iztro)

## When To Use This Skill

Use this skill for:

- exact Zi Wei Dou Shu calculation from date, time, and gender
- validating or replacing app screenshots with script-generated data
- extracting key palaces such as `命宫`, `官禄`, `财帛`, `迁移`, `夫妻`, `福德`
- checking whether career, wealth, or relationship conclusions are supported by the chart
- getting a structured JSON summary that another skill can interpret

Do not use this skill by itself for:

- medical, legal, or financial certainty
- replacing broader context about the user's real life
- pretending that one chart method resolves all ambiguity

## Workflow

### 1. Standardize inputs

Collect:

- solar date in `YYYY-M-D` or `YYYY-MM-DD`
- clock time or already-normalized true solar time
- gender
- whether the time should be treated as already converted to true solar time
- optional target date for yearly or decadal inspection

Important:

- This script does **not** compute true solar time by itself.
- If true solar time matters, normalize it before calling the script.
- If the user is near a day boundary, explain that chart method and time standard matter.

### 2. Ensure dependencies are present

This skill expects the `scripts/` folder dependencies to be installed.

If `node_modules` is missing, run from [scripts](scripts):

```bash
npm install
```

If npm cache permissions are broken in the environment, use a local cache directory.

### 3. Generate the chart summary

Run:

```bash
node generate_ziwei_chart.mjs --date 1994-3-14 --time 00:50 --gender female --target-date 2026-04-28
```

Or pass a pre-normalized time index:

```bash
node generate_ziwei_chart.mjs --date 1994-3-14 --time-index 0 --gender female
```

### 4. Interpret in layers

After you have the generated data:

- identify the key palace or palaces relevant to the user's question
- name the main stars and useful supporting stars
- connect palace structure to the user's real situation
- separate stable natal structure from yearly movement

### 5. Keep the interpretation honest

- Name ambiguous parts plainly
- Do not overclaim from one palace alone
- Prefer converging support across `命宫`, `官禄`, `迁移`, `财帛`, and `福德`
- Use the user's real-life context as primary validation

## Time Handling

The script supports:

- `--time HH:MM`
- `--time-index 0..12`

Time index mapping follows `iztro`:

- `0`: 早子时 `00:00~01:00`
- `1`: 丑时 `01:00~03:00`
- `2`: 寅时 `03:00~05:00`
- `3`: 卯时 `05:00~07:00`
- `4`: 辰时 `07:00~09:00`
- `5`: 巳时 `09:00~11:00`
- `6`: 午时 `11:00~13:00`
- `7`: 未时 `13:00~15:00`
- `8`: 申时 `15:00~17:00`
- `9`: 酉时 `17:00~19:00`
- `10`: 戌时 `19:00~21:00`
- `11`: 亥时 `21:00~23:00`
- `12`: 晚子时 `23:00~00:00`

If true solar time changes the day or moves the birth into early/late rat hour, resolve that before interpreting.

## Output Shape

The script returns JSON with:

- chart metadata
- natal Chinese date string
- soul/body stars
- five-elements class
- key palace summaries
- optional yearly and decadal summary for a target date
- automatic `annualFocus` summaries for yearly career, wealth, and travel/environment movement

## Best Pairing

This skill pairs especially well with `$life-insight-counselor`.

Use this skill first when:

- the user asks for exact Zi Wei support
- the user wants palace-level evidence
- screenshots are unavailable or should be replaced with computed data
