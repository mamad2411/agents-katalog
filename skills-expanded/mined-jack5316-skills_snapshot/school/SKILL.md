---
name: school
description: Discover interesting facts and celebrate your alma maters - Xi'an Jiaotong-Liverpool University (XJTLU) and University College London (UCL). Use when you want to learn about your schools, their history, notable alumni, achievements, or just feel a sense of school pride.
---

# School Information Skill (/school)

Celebrate your academic journey by exploring fascinating facts about your alma maters. This skill brings to life the rich history, notable alumni, impressive achievements, and fun trivia about Xi'an Jiaotong-Liverpool University and University College London.

## Quick Start

```bash
python3 _scripts/school_info.py
```

## What It Does

1. **Dual School Coverage** - Information about both XJTLU and UCL
2. **AI-Enhanced Content** - Curated facts enhanced with engaging AI presentation
3. **Celebratory Tone** - Focus on pride and achievement
4. **Structured Output** - Organized in easy-to-read sections

## Features

- **Quick Facts** - Essential info about each university
- **What Makes It Special** - Unique characteristics and history
- **Famous & Impressive Alumni** - Notable graduates and their achievements
- **Amazing Achievements** - Research breakthroughs, awards, and recognition
- **Fun Trivia & Hidden Gems** - Interesting stories and little-known facts
- **A Moment of Pride** - Reflective conclusion about your academic heritage

## Options

- `--school [xjtlu|ucl|both]`: Which school to show (default: both)
- `--save`: Save output to vault

## Examples

```bash
# Show info about both schools
python3 _scripts/school_info.py

# Show info about XJTLU only
python3 _scripts/school_info.py --school xjtlu

# Show info about UCL only
python3 _scripts/school_info.py --school ucl

# Save output to vault
python3 _scripts/school_info.py --save
```

## Output

- **Terminal**: Markdown-formatted school information
- **Saved note**: `Sources/School Pride - YYYY-MM-DD.md`

## Why This Matters

- **School Pride**: Celebrate your academic achievements and heritage
- **Conversation Starters**: Interesting facts to share about your alma maters
- **Inspiration**: Learn about what other graduates have accomplished
- **Connection**: Feel part of something larger than yourself

## Schools Covered

### Xi'an Jiaotong-Liverpool University (XJTLU)
- Founded: 2006
- Location: Suzhou, China
- Partnership: Xi'an Jiaotong University + University of Liverpool
- Special: First Sino-British university with independent legal entity status

### University College London (UCL)
- Founded: 1826
- Location: London, United Kingdom
- Status: Part of Russell Group, top 10 global university
- Special: 30 Nobel Prize winners among alumni/staff
