---
name: e04
description: Decode Zhuyin (Bopomofo) text typed with English keyboard keys into Chinese characters. ALWAYS try this skill when encountering unrecognized short letter/number sequences mixed with Chinese text that don't look like real English words or acronyms - e.g. "e04", "cl3", "su3", "cp3". Also use when user explicitly mentions 注音文, or asks what a cryptic alphanumeric fragment means in a Chinese context.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# e04 - 注音文解碼器

Decode "注音文" — Chinese text typed as English keyboard keys using the standard Zhuyin (Bopomofo) input method layout.

## When to Use

- Encountering **unrecognized English letter/number sequences** that don't look like real English words
- User sends messages mixing Chinese and random-looking English fragments
- User explicitly mentions 注音文 or asks to decode keyboard input

## Keyboard-to-Zhuyin Mapping Table

### Consonants (聲母)

| Key | Zhuyin | Key | Zhuyin | Key | Zhuyin |
|-----|--------|-----|--------|-----|--------|
| 1   | ㄅ     | r   | ㄐ     | 5   | ㄓ     |
| q   | ㄆ     | f   | ㄑ     | t   | ㄔ     |
| a   | ㄇ     | v   | ㄒ     | g   | ㄕ     |
| z   | ㄈ     | 2   | ㄉ     | b   | ㄖ     |
| w   | ㄊ     | e   | ㄍ     | y   | ㄗ     |
| s   | ㄋ     | d   | ㄎ     | h   | ㄘ     |
| x   | ㄌ     | c   | ㄏ     | n   | ㄙ     |

### Vowels (韻母)

| Key | Zhuyin | Key | Zhuyin | Key | Zhuyin |
|-----|--------|-----|--------|-----|--------|
| 8   | ㄚ     | 9   | ㄞ     | 0   | ㄢ     |
| i   | ㄛ     | o   | ㄟ     | p   | ㄣ     |
| k   | ㄜ     | l   | ㄠ     | ;   | ㄤ     |
| ,   | ㄝ     | .   | ㄡ     | /   | ㄥ     |
| u   | ㄧ     | j   | ㄨ     | m   | ㄩ     |
| -   | ㄦ     |     |        |     |        |

### Tones (聲調)

| Key   | Tone         |
|-------|--------------|
| space | ˉ (一聲，陰平) |
| 6     | ˊ (二聲，陽平) |
| 3     | ˇ (三聲，上聲) |
| 4     | ˋ (四聲，去聲) |
| 7     | ˙ (輕聲)      |

## Decoding Process

1. **Map** each character to its Zhuyin symbol using the tables above
2. **Group** into syllables: tone keys (`3`, `4`, `6`, `7`) mark the END of a syllable. Structure: [consonant] + vowel(s) + tone
3. **Identify** the Chinese character for each syllable
4. **Present** with the Zhuyin breakdown

### Syllable Boundary Rules

- Consonant keys and vowel keys do NOT overlap — each key belongs to exactly one category
- A **tone key** (`3`, `4`, `6`, `7`) always terminates a syllable
- First tone (space/ˉ) is typically **omitted** in 注音文 — detect the boundary when a new consonant appears after a vowel

## Examples

Input: `e04`

1. `e` → ㄍ, `0` → ㄢ, `4` → ˋ
2. Combined: ㄍㄢˋ
3. Result: **幹** — 台灣網路經典注音文

Input: `cl3`

1. `c` → ㄏ, `l` → ㄠ, `3` → ˇ
2. Combined: ㄏㄠˇ
3. Result: **好** (hǎo)

Input: `su3cl3` (multi-syllable)

1. `s` → ㄋ, `u` → ㄧ, `3` → ˇ (syllable break) | `c` → ㄏ, `l` → ㄠ, `3` → ˇ
2. Combined: ㄋㄧˇ ㄏㄠˇ
3. Result: **你好**

## Output Format

When decoding, show:

```
「{input}」→ {zhuyin} → {chinese_character}
```

If a syllable maps to multiple possible characters, list the most common ones and ask the user which they meant (if context is insufficient).

## Notes

- Tone key is always the last character in a syllable group
- Some syllables have no consonant (e.g., `84` = ㄚˋ = 啊)
- Space as tone (一聲) is usually omitted in 注音文, so a syllable may end without a tone key
- Context matters: use surrounding Chinese text to disambiguate which character is intended
- If the sequence clearly IS a valid English word, don't force-decode it as Zhuyin
