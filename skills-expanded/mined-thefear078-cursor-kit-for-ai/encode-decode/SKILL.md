---
name: encode-decode
description: Encode and decode Base64, URL, HTML entities, hex, binary, Unicode escape sequences, and NATO alphabet. Use when transforming strings between representations, debugging API payloads, or fixing encoding bugs.
---

# Encode & Decode

Transform text between common developer encodings. Always show **algorithm, direction, charset, and variant** (UTF-8 default). Never assume the user knows which encoding was applied — confirm when ambiguous.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| API payload debugging | "Decode this Base64 JWT segment" |
| URL/query string issues | "Why is `%2F` showing up twice?" |
| HTML/XSS context | "Escape these characters for HTML" |
| Binary ↔ text | "Convert this hex dump to UTF-8" |
| Legacy integrations | "NATO phonetic for this callsign" |

## Phase Checklist

```
[ ] 1. Identify encoding type and direction (encode vs decode)
[ ] 2. Confirm variant (Base64 vs Base64URL, standard vs URL-safe)
[ ] 3. Validate input (charset, padding, illegal characters)
[ ] 4. Run transform with documented command
[ ] 5. Verify round-trip when possible (decode → encode → compare)
[ ] 6. Present result with byte length and warnings
```

---

## Supported Operations

| Operation | Encode | Decode | Default charset |
|-----------|--------|--------|-----------------|
| Base64 | text/file → base64 | base64 → bytes/text | UTF-8 |
| Base64URL | JWT-safe variant | Same with `-_` alphabet | UTF-8 |
| URL percent | reserved → `%XX` | `%XX` → chars | UTF-8 |
| HTML entities | `<>&"'` → entities | entities → chars | UTF-8 |
| Hex | bytes → hex string | hex → bytes/text | — |
| Binary | text → 0/1 groups | binary → text | UTF-8 |
| Unicode escapes | codepoints → `\uXXXX` | escapes → text | UTF-8 |
| NATO phonetic | letters → words | words → letters | ASCII |

---

## Base64

### Standard Base64

```bash
# Encode string (no trailing newline)
echo -n "hello world" | base64
# aGVsbG8gd29ybGQ=

# Decode
echo "aGVsbG8gd29ybGQ=" | base64 -d

# Encode file
base64 -w 0 image.png > image.b64   # Linux
base64 -i image.png -o image.b64      # macOS
```

```python
import base64
text = "hello world"
encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
decoded = base64.b64decode(encoded).decode("utf-8")
print(f"Encoded: {encoded}\nDecoded: {decoded}")
```

### Base64URL (JWT, JWK)

Replace `+` → `-`, `/` → `_`, strip padding `=`.

```python
import base64

def b64url_decode(s: str) -> bytes:
    s += "=" * (-len(s) % 4)  # restore padding
    return base64.urlsafe_b64decode(s)

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

# JWT payload segment example
payload_b64 = "eyJzdWIiOiIxMjM0NTY3ODkwIn0"
print(b64url_decode(payload_b64))  # b'{"sub":"1234567890"}'
```

### Edge Cases

| Case | Handling |
|------|----------|
| Newlines in input | Strip whitespace before decode |
| Missing padding | Add `=` to multiple of 4 |
| Binary output | Show hex dump, don't force UTF-8 |
| Double-encoding | Detect `%252F`; decode iteratively with user confirmation |

---

## URL Encoding

```bash
# Python (preferred — handles Unicode correctly)
python -c "import urllib.parse; print(urllib.parse.quote('hello world'))"
# hello%20world

python -c "import urllib.parse; print(urllib.parse.quote('café'))"
# caf%C3%A9

python -c "import urllib.parse; print(urllib.parse.unquote('hello%20world'))"
# hello world

# Query string (key=value pairs)
python -c "
import urllib.parse
params = {'q': 'hello world', 'page': '1'}
print(urllib.parse.urlencode(params))
"
# q=hello+world&page=1
```

### URL Encoding Rules

| Context | Function | Notes |
|---------|----------|-------|
| Path segment | `quote(s, safe="/")` | Preserve slashes |
| Query value | `quote_plus(s)` | Space → `+` |
| Full query | `urlencode(dict)` | Handles multiple keys |
| Fragment | Usually not encoded | Exception: some SPA routers |

**Double-encoding detection:** If decoded text still contains `%XX` patterns, flag likely double-encoding.

---

## HTML Entities

```python
import html

text = '<script>alert("xss")</script>'
escaped = html.escape(text)
# &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;

unescaped = html.unescape("&amp;lt;tag&amp;gt;")
# &lt;tag&gt; (one level only — run again if needed)
```

| Character | Named entity | Numeric |
|-----------|--------------|---------|
| `<` | `&lt;` | `&#60;` |
| `>` | `&gt;` | `&#62;` |
| `&` | `&amp;` | `&#38;` |
| `"` | `&quot;` | `&#34;` |
| `'` | `&#39;` | `&#39;` |

Use `html.escape()` for attribute and text contexts. For full HTML sanitization, recommend a dedicated library — this skill handles entity encoding only.

---

## Hex Encoding

```bash
# String to hex
echo -n "hello" | xxd -p
# 68656c6c6f

# Hex to string
echo "68656c6c6f" | xxd -r -p
# hello

# File hex dump (first 256 bytes)
xxd -l 256 file.bin
```

```python
text = "hello"
hex_str = text.encode("utf-8").hex()
restored = bytes.fromhex(hex_str).decode("utf-8")
print(hex_str, restored)  # 68656c6c6f hello
```

**Validation:** Hex strings must have even length. Strip `0x` prefix and spaces before decode.

---

## Binary Encoding

```python
def text_to_binary(text: str, sep: str = " ") -> str:
    return sep.join(format(b, "08b") for b in text.encode("utf-8"))

def binary_to_text(bits: str) -> str:
    clean = bits.replace(" ", "")
    byte_chunks = [clean[i:i+8] for i in range(0, len(clean), 8)]
    return bytes(int(b, 2) for b in byte_chunks).decode("utf-8")

print(text_to_binary("Hi"))    # 01001000 01101001
print(binary_to_text("01001000 01101001"))  # Hi
```

Group bits in 8-bit bytes. Warn if bit count is not a multiple of 8.

---

## Unicode Escape Sequences

```python
def to_unicode_escapes(text: str, long_form: bool = False) -> str:
    result = []
    for ch in text:
        cp = ord(ch)
        if cp > 0xFFFF:
            result.append(f"\\U{cp:08X}" if long_form else f"\\u{cp:04X}")
        elif cp > 127 or ch in '\\"':
            result.append(f"\\u{cp:04X}")
        else:
            result.append(ch)
    return "".join(result)

# Python literal evaluation
escaped = r"\u0048\u0065\u006C\u006C\u006F"
print(escaped.encode("utf-8").decode("unicode_escape"))  # Hello
```

| Format | Example | Used in |
|--------|---------|---------|
| `\uXXXX` | `\u00E9` | JSON, JavaScript, Python |
| `\UXXXXXXXX` | `\U0001F600` | Python (supplementary) |
| `\xXX` | `\x48` | Python bytes literal |

---

## NATO Phonetic Alphabet

```python
NATO = {
    "A": "Alpha", "B": "Bravo", "C": "Charlie", "D": "Delta",
    "E": "Echo", "F": "Foxtrot", "G": "Golf", "H": "Hotel",
    "I": "India", "J": "Juliet", "K": "Kilo", "L": "Lima",
    "M": "Mike", "N": "November", "O": "Oscar", "P": "Papa",
    "Q": "Quebec", "R": "Romeo", "S": "Sierra", "T": "Tango",
    "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "X-ray",
    "Y": "Yankee", "Z": "Zulu",
}
REVERSE = {v.upper(): k for k, v in NATO.items()}

def to_nato(text: str) -> str:
    return " ".join(NATO.get(c.upper(), c) for c in text if c.isalpha())

def from_nato(words: str) -> str:
    return "".join(REVERSE.get(w.upper(), "?") for w in words.split())

print(to_nato("ABC"))       # Alpha Bravo Charlie
print(from_nato("Alpha Bravo Charlie"))  # ABC
```

Digits use standard spoken forms (not NATO words). Non-alpha characters pass through unchanged.

---

## Workflow Examples

### Example 1: Debug API double-encoding

```
Input:  %252Fapi%252Fv1
Step 1: URL decode → %2Fapi%2Fv1
Step 2: URL decode → /api/v1
Result: Original was double-encoded path
```

### Example 2: JWT header decode

```
Input:  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Step 1: Base64URL decode with padding fix
Step 2: Parse JSON → {"alg":"HS256","typ":"JWT"}
Next:   See hash-crypto for full JWT analysis
```

### Example 3: Invalid UTF-8 after Base64 decode

```
Input:  (base64 of binary PNG header)
Output: Hex dump: 89504e470d0a1a0a...
Note:   Binary data — not valid UTF-8. Do not display as text.
```

---

## Output Template

```markdown
## {Operation}: {direction}

| Property | Value |
|----------|-------|
| Input | `{preview}` ({n} bytes/chars) |
| Output | `{result}` |
| Charset | UTF-8 |
| Variant | standard Base64 / Base64URL / ... |
| Round-trip | ✓ match / ✗ mismatch |

### Notes
- {warnings about binary, double-encoding, padding, etc.}
```

---

## Decision Rubric

| Symptom | Likely encoding | First action |
|---------|-----------------|--------------|
| Ends with `=` or `==` | Base64 | Strip whitespace, decode |
| Contains `%XX` sequences | URL | Percent-decode once, check again |
| Contains `&lt;` or `&#` | HTML entities | `html.unescape()` |
| Only `[0-9a-fA-F]` | Hex | Validate even length, decode |
| Three dot-separated segments | JWT | Base64URL each segment → `hash-crypto` |
| `\uXXXX` in string | Unicode escapes | Python `unicode_escape` codec |

---

## Anti-Patterns

- Decoding unknown binary as UTF-8 and displaying mojibake as success
- URL-encoding an already-encoded string without checking
- Using custom Base64 alphabets without stating variant
- Assuming Latin-1 when UTF-8 was intended
- Decoding JWT payload and treating claims as authenticated (see `hash-crypto`)
- Running `base64 -d` on files without checking output size

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| JWT parse, verify signature, HMAC | `hash-crypto` |
| JSON with `\u` escapes after decode | `format-convert` |
| URL parsing (host, path, query) | `network-utils` |
| Hex output of hash digests | `hash-crypto` |
| URL-safe slug generation | `text-utils` |
| Cron strings in config files | `cron-builder` |
| SQL string literal escaping | `sql-format` |
