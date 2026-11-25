---
name: chinese-poem-generator-manus-familytools-fullinstr-v2-skill
description: Family-scoped SkillLearnBench skill for chinese-poem-generator using latest full-instruction v2 family injection.
allowed-tools:
  - char_count_check
  - pinyin_rhyme_check
  - read_file
  - regulated_verse_lint
  - run_python
  - write_file
  - write_text_artifact
metadata:
  benchmark: SkillLearnBench
  generator: Manus
  baseline: manus_familytools_fullinstr_v2
  generation_constraints: slb_no_instance_memory_familytools_v2
  allowed_gold_input: familytools_full_instruction_v2
  skill_injection_scope: family_scoped
  date: "2026-05-23"
---

# Skill: Chinese Poem Generator

## 1. When to use this skill
Use this skill for the `chinese-poem-generator` family tasks in SkillLearnBench. Apply it when instructed to act as an ancient Chinese poet and compose a seven-character regulated verse (七言律诗) based on a specific theme, perspective, and emotional tone. The output must strictly follow the structural and rhyming rules of a seven-character regulated verse using modern Mandarin pronunciation.

## 2. Visible input and artifact inventory
- **Visible Input**: The task instruction specifying the theme (e.g., peace, reunion), perspective (e.g., village wife, traveler), and emotional tone.
- **Artifact Inventory**: A single text file, typically `/root/poem.txt`. It must contain exactly 9 lines: the title on line 1, and the 8-line poem on lines 2-9.

## 3. Execution procedure for the current task
1. **Analyze Instruction**: Extract the theme, perspective, tone, and exact output file path from the prompt.
2. **Draft Poem**: Compose an 8-line poem. Each line must have exactly 7 Chinese characters (excluding punctuation). Reflect the requested theme and perspective.
3. **Format Output**: Place the title on the first line, followed by the 8 poem lines.
4. **Validate**: Use provided tools to check character count, pinyin rhyme scheme, and regulated verse structure.
5. **Write Artifact**: Save the validated text to the specified path.

## 4. Family tool routing and useful placeholder snippets
- **`regulated_verse_lint`**: Check adherence to seven-character regulated verse rules, including tonal patterns (平仄).
- **`char_count_check`**: Verify each of the 8 lines has exactly 7 characters.
- **`pinyin_rhyme_check`**: Ensure even-numbered lines rhyme based on modern Mandarin pinyin.
- **`write_file` / `write_text_artifact`**: Save the final poem to the required path.

*Drafting Snippet:*
```text
[Title]
[Line 1: 7 chars]
[Line 2: 7 chars, rhymes]
[Line 3: 7 chars]
[Line 4: 7 chars, rhymes]
[Line 5: 7 chars]
[Line 6: 7 chars, rhymes]
[Line 7: 7 chars]
[Line 8: 7 chars, rhymes]
```

## 5. Validation checks before final submission
- **File Path**: Does the file exist at the exact specified path (e.g., `/root/poem.txt`)?
- **Line Count**: Are there exactly 9 lines (1 title + 8 poem lines)?
- **Character Count**: Does each poem line have exactly 7 characters?
- **Rhyme Scheme**: Do even lines rhyme in modern Mandarin?
- **Thematic Alignment**: Does the poem match the requested theme and perspective?

## 6. Common failure modes and repair actions
- **Failure**: Incorrect line length.
  - **Repair**: Rewrite lines to exactly 7 characters. Verify with `char_count_check`.
- **Failure**: Rhyme check fails.
  - **Repair**: Replace non-rhyming characters at the end of even lines with ones sharing the same pinyin vowel ending. Verify with `pinyin_rhyme_check`.
- **Failure**: Wrong file path or name.
  - **Repair**: Move/rename the file to match the instruction exactly.
- **Failure**: Extra text in file.
  - **Repair**: Remove all text except the 9 required lines.

## 7. A finalizer capsule for restoring the minimum required artifact or answer shape near max-step
If nearing the maximum step limit without a perfect poem, prioritize the minimum viable artifact:
1. Generate a simple 8-line poem, 7 characters per line.
2. Ensure even lines rhyme in modern Mandarin.
3. Add a title on the first line.
4. Immediately write this 9-line text to the required path (e.g., `/root/poem.txt`) using `write_file`.
5. Skip advanced tonal (平仄) checks; focus only on character count and basic rhyming.
