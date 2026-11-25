---
name: github-release
description: 'Publish a GitHub release using gh CLI. Use when creating a new version tag, writing release notes, or fixing garbled/corrupted characters in release notes. Covers standard release flow, ASCII-safe notes file approach, and Unicode homoglyph prevention.'
argument-hint: 'target version tag, e.g. v1.2.1'
---

# GitHub Release

## When to Use

- Publishing a new version (patch / minor / major)
- Writing or updating release notes for an existing tag
- Fixing garbled characters (question marks, mojibake) in release notes caused by Unicode homoglyphs

## Procedure

### Step 1: Collect changes since last tag

```sh
git log --oneline <last-tag>..HEAD
git diff <last-tag>..HEAD --stat
gh release view <last-tag>   # reference previous notes format
```

### Step 2: Create and push tag

```sh
git tag -a <new-tag> -m "release: <new-tag>"
git push origin <new-tag>
```

### Step 3: Write release notes to a temp file

Write notes to `.release_notes_tmp.md` using `create_file` tool -- never inline in the shell command.

See [release-notes-template.md](./references/release-notes-template.md) for the recommended structure.

### Step 4: Verify pure ASCII (required)

```sh
python3 -c "
import sys
data = open('.release_notes_tmp.md', encoding='utf-8').read()
bad = [(i, c, ord(c)) for i, c in enumerate(data) if ord(c) > 127]
print(f'Non-ASCII count: {len(bad)}')
for idx, ch, cp in bad:
    print(f'  index {idx}: U+{cp:04X}  repr={ch!r}')
if bad: sys.exit(1)
"
```

Expected output: `Non-ASCII count: 0` and exit code 0.  
If any characters are found, consult [ascii-replacements.md](./references/ascii-replacements.md) and fix before continuing.

### Step 5: Create release

```sh
gh release create <new-tag> --title "<new-tag>" --notes-file .release_notes_tmp.md
```

### Step 6: Cleanup

```sh
rm .release_notes_tmp.md
```

### Step 7 (fix existing release): Edit release notes

```sh
gh release edit <tag> --notes-file .release_notes_tmp.md
rm .release_notes_tmp.md
```

## Key Constraints

- **Never** pass AI-generated text as an inline `--notes "..."` argument -- Unicode homoglyphs (e.g. Cyrillic `a` U+0430 disguised as Latin `a`) survive copy-paste and corrupt the published notes.
- **Always** use `--notes-file` with a file that has passed the ASCII verification step.
- Keep `.release_notes_tmp.md` out of version control (add to `.gitignore`).

## References

- [release-notes-template.md](./references/release-notes-template.md) -- recommended notes structure
- [ascii-replacements.md](./references/ascii-replacements.md) -- common Unicode-to-ASCII replacement table
