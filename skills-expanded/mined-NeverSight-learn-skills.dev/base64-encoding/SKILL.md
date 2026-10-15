---
name: base64-encoding
description: Encoding and decoding utilities — base64, URL encoding, hex, and hashing. Use when user mentions "base64", "encode", "decode", "url encode", "urlencode", "hex", "hash", "sha256", "md5", "checksum", "jwt decode", "binary to text", or converting between encoding formats.
---

# Encoding and Decoding Utilities

## Base64 Encode/Decode

### String

```bash
# Encode
echo -n 'hello world' | base64

# Decode (macOS)
echo 'aGVsbG8gd29ybGQ=' | base64 -D

# Decode (Linux)
echo 'aGVsbG8gd29ybGQ=' | base64 -d
```

### File

```bash
# Encode a file
base64 < input.bin > output.b64

# Decode to file (macOS)
base64 -D < output.b64 > restored.bin

# Decode to file (Linux)
base64 -d < output.b64 > restored.bin
```

### Stdin pipe

```bash
curl -s https://example.com/image.png | base64
```

### macOS vs Linux

| Operation | macOS          | Linux          |
|-----------|----------------|----------------|
| Decode    | `base64 -D`    | `base64 -d`    |
| Wrap cols | `base64 -b 76` | `base64 -w 76` |

Portable: `base64 --decode 2>/dev/null || base64 -D`

## URL Encoding/Decoding

```bash
# Python 3
python3 -c "import urllib.parse; print(urllib.parse.quote('hello world&foo=bar'))"
python3 -c "import urllib.parse; print(urllib.parse.unquote('hello%20world%26foo%3Dbar'))"

# Node.js
node -e "console.log(encodeURIComponent('hello world&foo=bar'))"
node -e "console.log(decodeURIComponent('hello%20world%26foo%3Dbar'))"
```

## Hex Encode/Decode

```bash
# String to hex
echo -n 'hello' | xxd -p
# Output: 68656c6c6f

# Hex to string
echo '68656c6c6f' | xxd -r -p
# Output: hello

# File to hex dump
xxd input.bin

# Compact hex (no formatting)
xxd -p input.bin

# Using od
echo -n 'hello' | od -A n -t x1 | tr -d ' \n'

# Hex to bytes with printf
printf '\x68\x65\x6c\x6c\x6f'
```

## Hashing

### String hashing

```bash
# MD5
echo -n 'hello' | md5sum          # Linux
echo -n 'hello' | md5             # macOS

# SHA-1
echo -n 'hello' | sha1sum         # Linux
echo -n 'hello' | shasum -a 1     # macOS

# SHA-256
echo -n 'hello' | sha256sum       # Linux
echo -n 'hello' | shasum -a 256   # macOS

# SHA-512
echo -n 'hello' | sha512sum       # Linux
echo -n 'hello' | shasum -a 512   # macOS
```

Use `echo -n` to avoid hashing the trailing newline.

### File hashing

```bash
sha256sum myfile.tar.gz           # Linux
shasum -a 256 myfile.tar.gz       # macOS
```

### OpenSSL (cross-platform)

```bash
openssl dgst -sha256 myfile.tar.gz
echo -n 'hello' | openssl dgst -sha256
```

## Verify File Integrity with Checksums

```bash
# Generate checksum file
sha256sum release.tar.gz > release.sha256

# Verify (Linux)
sha256sum -c release.sha256

# Verify (macOS)
shasum -a 256 -c release.sha256

# Quick inline comparison
EXPECTED="e3b0c44298fc1c149afbf4c8996fb924..."
ACTUAL=$(sha256sum downloaded.tar.gz | awk '{print $1}')
[ "$EXPECTED" = "$ACTUAL" ] && echo "OK" || echo "MISMATCH"
```

## JWT Decode Without a Library

A JWT has three dot-separated base64url segments: header, payload, signature.

```bash
JWT="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

# Decode header
echo "$JWT" | cut -d. -f1 | tr '_-' '/+' | base64 -d 2>/dev/null || \
echo "$JWT" | cut -d. -f1 | tr '_-' '/+' | base64 -D

# Decode payload
echo "$JWT" | cut -d. -f2 | tr '_-' '/+' | base64 -d 2>/dev/null || \
echo "$JWT" | cut -d. -f2 | tr '_-' '/+' | base64 -D
```

Base64url uses `-` and `_` instead of `+` and `/`. The `tr` call converts back. Add padding if needed:

```bash
decode_b64url() {
  local d="$1" pad=$(( 4 - ${#1} % 4 ))
  [ "$pad" -lt 4 ] && d="${d}$(printf '%0.s=' $(seq 1 $pad))"
  echo "$d" | tr '_-' '/+' | base64 -d 2>/dev/null || echo "$d" | tr '_-' '/+' | base64 -D
}
decode_b64url "$(echo "$JWT" | cut -d. -f2)"
```

## Generate Random Strings

```bash
# Alphanumeric, 32 chars
cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | head -c 32

# Hex string, 32 chars
openssl rand -hex 16

# Base64 string
openssl rand -base64 24

# URL-safe random string
openssl rand -base64 32 | tr '+/' '-_' | tr -d '='

# UUID-like
cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen
```

## HTML Entity Encode/Decode

```bash
# Encode (Python)
python3 -c "import html; print(html.escape('<div class=\"x\">&</div>'))"
# Output: &lt;div class=&quot;x&quot;&gt;&amp;&lt;/div&gt;

# Decode (Python)
python3 -c "import html; print(html.unescape('&lt;div&gt;hello&lt;/div&gt;'))"

# Decode (Perl)
perl -MHTML::Entities -e 'print decode_entities("&lt;p&gt;hello&lt;/p&gt;")'
```

## Unicode Escape/Unescape

```bash
# Unescape \uXXXX sequences (Python)
python3 -c "print('\\u0048\\u0065\\u006c\\u006c\\u006f')"

# Escape string to \uXXXX
python3 -c "print(''.join(f'\\\\u{ord(c):04x}' for c in 'Hello'))"

# Unescape JSON unicode (jq)
echo '"\\u0048\\u0065\\u006c\\u006c\\u006f"' | jq -r .

# UTF-8 hex bytes to character
printf '\xc3\xa9'    # prints: e with accent (é)

# Character to UTF-8 hex
echo -n 'é' | xxd -p
```

## Common Patterns

### Encode a file for JSON embedding

```bash
BASE64=$(base64 < image.png | tr -d '\n')
echo "{\"image\": \"data:image/png;base64,${BASE64}\"}"
```

### Decode a base64 field from an API response

```bash
curl -s https://api.example.com/data | jq -r '.content' | base64 -d
```

### Verify a download checksum

```bash
curl -LO https://example.com/release.tar.gz
curl -sL https://example.com/release.sha256 | sha256sum -c -
```

### Generate an API key

```bash
openssl rand -base64 32 | tr -d '\n'
openssl rand -hex 32
```

### Encode credentials for Basic Auth

```bash
echo -n 'user:password' | base64
# Use in header: Authorization: Basic dXNlcjpwYXNzd29yZA==
```

## Quick Reference

| Task                        | Command                                          |
|-----------------------------|--------------------------------------------------|
| Base64 encode string        | `echo -n 'text' \| base64`                       |
| Base64 decode (macOS)       | `echo 'data' \| base64 -D`                       |
| Base64 decode (Linux)       | `echo 'data' \| base64 -d`                       |
| URL encode                  | `python3 -c "import urllib.parse; print(urllib.parse.quote('...'))"` |
| URL decode                  | `python3 -c "import urllib.parse; print(urllib.parse.unquote('...'))"` |
| Hex encode                  | `echo -n 'text' \| xxd -p`                       |
| Hex decode                  | `echo 'hex' \| xxd -r -p`                        |
| MD5 hash                    | `echo -n 'text' \| openssl dgst -md5`            |
| SHA-256 hash                | `echo -n 'text' \| openssl dgst -sha256`         |
| SHA-256 file                | `openssl dgst -sha256 file.tar.gz`               |
| Verify checksum             | `sha256sum -c checksums.sha256`                   |
| JWT decode payload          | `echo $JWT \| cut -d. -f2 \| tr '_-' '/+' \| base64 -d` |
| Random hex (32 chars)       | `openssl rand -hex 16`                            |
| Random base64               | `openssl rand -base64 24`                         |
| HTML encode                 | `python3 -c "import html; print(html.escape('...'))"`   |
| HTML decode                 | `python3 -c "import html; print(html.unescape('...'))"` |
| Unicode unescape            | `python3 -c "print('\\u0048\\u0065')"`            |
| Basic Auth header           | `echo -n 'user:pass' \| base64`                  |
