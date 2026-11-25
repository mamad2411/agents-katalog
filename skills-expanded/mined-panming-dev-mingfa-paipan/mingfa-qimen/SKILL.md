---
name: mingfa-qimen
description: Perform high-precision Qimen Dunjia (Mingfa/Flying Disc tradition) arrangements using astronomical junction offsets and True Solar Time correction.
---

# Mingfa Qimen Skill

This skill allows an agent to perform professional Qimen Dunjia arrangements using the stabilized Mingfa Qimen Engine. It supports precise solar term junction detection and the "Fixed-Term Anchor" rule for Ju determination.

## When to Use
- When the user asks for a Qimen Dunjia (奇门遁甲) arrangement.
- When the user provides a birth date, time, and optionally longitude, and asks for a "Flying Disc" (飞盘) or "Mingfa" (鸣法) analysis.
- When performing advanced Chinese metaphysical analysis that requires a stable Qimen board.

## How to Invoke

The engine is located at `src/index.js` in the project root.

```javascript
const { mingfaPaipan } = require('./src/index');

const params = {
  year: 2024,
  month: 12,
  day: 13,
  hour: 9,
  minute: 31,
  longitude: 121.47 // Recommended for True Solar Time calculation
};

const result = mingfaPaipan(params);
```

## Response Formatting
The agent should present the 3x3 grid results clearly to the user. Use the following visual format for the 9-palace grid (4-9-2, 3-5-7, 8-1-6):

```text
  ┌──────────────┬──────────────┬──────────────┐
  │ [Spirit]  [P4] │ [Spirit]  [P9] │ [Spirit]  [P2] │
  │ [Star]   [Stem] │ [Star]   [Stem] │ [Star]   [Stem] │
  │ [Door]   [Stem] │ [Door]   [Stem] │ [Door]   [Stem] │
  ├──────────────┼──────────────┼──────────────┤
  │ ...          │ ...          │ ...          │
  └──────────────┴──────────────┴──────────────┘
```

## Guidelines
1. **Time Precision**: Always ask for the minute and longitude if possible to ensure "True Solar Time" accuracy.
2. **Lineage**: Specify that this is the **Mingfa (鸣法) / Flying Disc (飞盘)** tradition, which differs from the standard Rotating Disc (转盘) tradition in its Ju sequences and spirit mappings.
3. **Internal Logic**: The Ju is determined by the **Junction-Anchor Rule**. The 15-day term is anchored to the day branch at the moment of solar term introduction.
