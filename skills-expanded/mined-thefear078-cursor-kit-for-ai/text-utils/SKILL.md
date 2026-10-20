---
name: text-utils
description: Text diff, case conversion, slugify, regex test/explain, lorem ipsum, text statistics, and string obfuscation. Use when comparing outputs, generating slugs, debugging regex, or analyzing copy length.
---

# Text Utilities

Common string operations developers reach for daily — precise, reproducible, with before/after shown. Label old vs new in diffs; state regex flavor explicitly.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Compare outputs | "Diff these two config snippets" |
| Naming conventions | "Convert APIResponse to snake_case" |
| URL slugs | "Slugify 'Hello, World! 2024'" |
| Regex debugging | "Why doesn't this pattern match?" |
| Content metrics | "Word count and reading time" |
| Demo data | "Obfuscate emails in this log" |

## Phase Checklist

```
[ ] 1. Identify operation (diff, case, slug, regex, stats, obfuscate)
[ ] 2. Capture input exactly (preserve whitespace unless trimming requested)
[ ] 3. Apply transform with documented rules
[ ] 4. Show before/after with clear labels
[ ] 5. For regex: test multiple cases including edge cases
[ ] 6. For diff: label OLD vs NEW sides
[ ] 7. Report metrics and warnings
```

---

## Diff Operations

### Line Diff (Unified Format)

```python
import difflib

def line_diff(old: str, new: str, context: int = 3) -> str:
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    return "".join(difflib.unified_diff(
        old_lines, new_lines,
        fromfile="OLD", tofile="NEW",
        n=context,
    ))

old = "line one\nline two\nline three\n"
new = "line one\nline TWO modified\nline three\nline four\n"
print(line_diff(old, new))
```

```bash
# File diff (if diff command available)
diff -u old.txt new.txt

# Side-by-side (if available)
diff -y old.txt new.txt | head -40
```

### Word Diff (Short Strings)

```python
import difflib

def word_diff(old: str, new: str) -> str:
    old_words = old.split()
    new_words = new.split()
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    parts = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            parts.extend(old_words[i1:i2])
        elif op == "delete":
            parts.extend(f"[-{w}-]" for w in old_words[i1:i2])
        elif op == "insert":
            parts.extend(f"[+{w}+]" for w in new_words[j1:j2])
        elif op == "replace":
            parts.extend(f"[-{w}-]" for w in old_words[i1:i2])
            parts.extend(f"[+{w}+]" for w in new_words[j1:j2])
    return " ".join(parts)
```

**Rule:** For structured data (JSON, YAML), prefer `format-convert` structural diff over text diff.

---

## Case Conversion

```python
import re

def to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.replace("-", "_").replace(" ", "_").lower()

def to_camel(s: str) -> str:
    parts = re.split(r"[_\-\s]+", s)
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])

def to_pascal(s: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[_\-\s]+", s))

def to_kebab(s: str) -> str:
    return to_snake(s).replace("_", "-")

def to_constant(s: str) -> str:
    return to_snake(s).upper()

tests = {
    "hello_world": "helloWorld",
    "APIResponse": "apiResponse",
    "HTTPStatus": "httpStatus",
    "getHTTPResponseCode": "getHttpResponseCode",
}
for inp, expected_camel in tests.items():
    print(f"{inp:30} → camel: {to_camel(inp):25} snake: {to_snake(inp)}")
```

### Case Conversion Table

| Mode | Input | Output |
|------|-------|--------|
| lower | Hello World | hello world |
| UPPER | Hello World | HELLO WORLD |
| camelCase | hello_world | helloWorld |
| PascalCase | hello_world | HelloWorld |
| snake_case | HelloWorld | hello_world |
| kebab-case | HelloWorld | hello-world |
| CONSTANT_CASE | helloWorld | HELLO_WORLD |
| Title Case | hello world | Hello World |

**Acronym handling:** `APIResponse` is ambiguous (`apiResponse` vs `aPIResponse`). Ask user or document conservative rule used.

---

## Slugify

```python
import re
import unicodedata

def slugify(text: str, max_length: int = 80, separator: str = "-") -> str:
    # Transliterate non-ASCII
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", separator, text).strip(separator)
    if len(text) > max_length:
        text = text[:max_length].rsplit(separator, 1)[0]
    return text

print(slugify("Hello, World! 2024"))       # hello-world-2024
print(slugify("Café au Lait"))             # cafe-au-lait
print(slugify("  Multiple   Spaces  "))    # multiple-spaces
```

### Slugify Options

| Option | Default | Purpose |
|--------|---------|---------|
| separator | `-` | Word boundary character |
| max_length | 80 | Truncate at word boundary |
| transliterate | yes | ASCII-friendly URLs |
| lowercase | yes | URL convention |

For URL-safe encoding of slugs with special chars, see `encode-decode`.

---

## Regex Test & Explain

```python
import re

def test_regex(pattern: str, strings: list[str], flags: int = 0) -> None:
    pat = re.compile(pattern, flags)
    print(f"Pattern: {pattern}")
    print(f"Flags: {re.UNICODE if flags & re.UNICODE else ''}")
    for s in strings:
        m = pat.search(s)
        if m:
            print(f"  ✓ '{s}' → match={m.group()!r} groups={m.groups()}")
        else:
            print(f"  ✗ '{s}' → no match")

test_regex(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    ["user@example.com", "invalid@", "user@domain", "a@b.co"],
)
```

### Regex Workflow

1. **State flavor:** Python `re` (PCRE-like), JavaScript, Go RE2
2. **Test cases:** include match, non-match, edge cases user provides
3. **Explain pattern:** break into tokens in plain language
4. **Groups:** show capture groups and named groups
5. **ReDoS warning:** flag nested quantifiers `(a+)+`, `(a*)*`

```python
# Named groups example
pat = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
m = pat.match("2024-06-15")
print(m.groupdict())  # {'year': '2024', 'month': '06', 'day': '15'}
```

### Common Pattern Reference

| Pattern | Matches |
|---------|---------|
| `^\d+$` | Integers only |
| `^[a-f0-9]{32}$` | MD5 hex string |
| `^[\w.-]+@[\w.-]+\.\w+$` | Simple email (not RFC-complete) |
| `^(https?://)?([\w.-]+)(:\d+)?(/.*)?$` | Basic URL structure |

---

## Text Statistics

```python
import re
from collections import Counter

def text_stats(text: str) -> dict:
    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"[.!?]+", text.strip())
    sentences = [s for s in sentences if s.strip()]
    chars = len(text)
    chars_no_space = len(text.replace(" ", "").replace("\n", ""))
    lines = text.count("\n") + 1 if text else 0
    wpm = 200
    reading_min = len(words) / wpm

    return {
        "characters": chars,
        "characters_no_spaces": chars_no_space,
        "words": len(words),
        "lines": lines,
        "sentences": len(sentences),
        "reading_time_min": round(reading_min, 1),
        "avg_word_length": round(sum(len(w) for w in words) / max(len(words), 1), 1),
    }

sample = "Hello world. This is a sample paragraph for analysis."
print(text_stats(sample))
```

### Word Frequency (Optional)

```python
STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for"}
words = re.findall(r"\b\w+\b", text.lower())
freq = Counter(w for w in words if w not in STOP_WORDS)
print(freq.most_common(10))
```

---

## Lorem Ipsum Generation

```python
LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
)

def lorem_paragraphs(n: int = 1) -> str:
    return "\n\n".join(LOREM for _ in range(n))
```

Generate placeholder text for mockups. Specify paragraph count, word count, or byte length as requested.

---

## Obfuscate / Demo Data

```python
import re

def obfuscate_emails(text: str, placeholder: str = "[EMAIL]") -> str:
    return re.sub(r"[\w.-]+@[\w.-]+\.\w+", placeholder, text)

def obfuscate_preserve_length(text: str, char: str = "•") -> str:
    return "".join(char if c not in " \n\t" else c for c in text)

log = "Contact admin@example.com or support@company.org for help."
print(obfuscate_emails(log))
# Contact [EMAIL] or [EMAIL] for help.
```

**Rules:**
- Reversible only if user explicitly requests (store mapping separately)
- Preserve string length/format when testing UI layouts
- Never obfuscate and present as "secure" — this is demo masking only

---

## Worked Examples

### Example 1: API field rename diff

```
OLD: "user_name": "alice"
NEW: "userName": "alice"
Note: Structural rename — see format-convert for JSON key migration
```

### Example 2: Slug collision

```
Input:  "FAQ" and "faq" → both slugify to "faq"
Action: Append suffix or use UUID from token-generator
```

### Example 3: Regex ReDoS warning

```
Pattern: (a+)+$
Input:   aaaaaaaaaaaaaaaaaaaaaX
Warning: Catastrophic backtracking risk — simplify to a+$
```

---

## Output Template

```markdown
## {operation}

| Property | Value |
|----------|-------|
| Input | `{preview}` |
| Output | `{result}` |

### Details
| Metric | Value |
|--------|-------|
| Characters | 142 |
| Words | 24 |
| Reading time | ~0.1 min |

### Diff (OLD → NEW)
```diff
- old line
+ new line
```
```

---

## Anti-Patterns

- Slugify stripping non-ASCII without transliteration when URL needs readable form
- Regex tested on one example only — always include edge cases
- Diff without labeling which side is old/new
- Using text diff for JSON/YAML (use `format-convert`)
- Reversible obfuscation presented as encryption
- Title-casing acronyms incorrectly (`Api` instead of `API`)

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| Structured JSON/YAML diff | `format-convert` |
| URL-safe encoding | `encode-decode` |
| Generate unique slug suffix | `token-generator` |
| SQL identifier quoting | `sql-format` |
| Hex color in text | `color-convert` |
| Cron expression in comments | `cron-builder` |
