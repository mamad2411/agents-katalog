---
name: base64-translator
description: "Use when translating between Base64 and English text. Handles encoding/decoding for data interchange."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [base64, encoding, decoding, data-interchange, conversion]
---

# Base64 Translator

## Overview

Encode and decode Base64 content across multiple contexts: plain text, files (images, PDFs, binaries), data URIs, and Base64-encoded payloads in APIs, JWTs, and configuration files. Provides both one-off conversions and batch processing scripts.

## When to Use

- "Decode this Base64 string" — decoding encoded text or data
- "Encode this text/image to Base64" — creating Base64 representations
- "What's inside this JWT?" — decoding JWT payloads
- "Convert this image to a Base64 data URI" — embedding images in HTML/CSS
- "I have a Base64-encoded file, what is it?" — identifying and extracting encoded content

**Don't use for:** cryptographic operations (Base64 is encoding, not encryption), hashing (use SHA/MD5 skills), or compression (Base64 increases size by ~33%).

## How It Works

**Identify → Decode/Encode → Validate → Present**

Base64 is a binary-to-text encoding that represents binary data as ASCII characters. It uses 64 characters (A-Z, a-z, 0-9, +, /) plus = for padding. Every 3 bytes of input become 4 Base64 characters.

## Steps

### 1. Identify Encoding Context
- **Plain text:** Decode to read the text content
- **Data URI:** `data:[mime-type];base64,...` — extract MIME type and decode the data
- **JWT:** Split on `.`, decode the payload (second segment), present claims as JSON
- **File:** Determine file type from magic bytes after decoding, save with correct extension
- **API payload:** Decode to inspect, re-encode if modifying

### 2. Decode Base64 (Python)
```python
import base64

def decode_base64(encoded_string: str) -> bytes:
    """Decode a Base64 string, handling padding automatically."""
    # Strip data URI prefix if present
    if encoded_string.startswith('data:'):
        encoded_string = encoded_string.split(',', 1)[1]
    # Add padding if missing (some encodings drop = padding)
    missing_padding = len(encoded_string) % 4
    if missing_padding:
        encoded_string += '=' * (4 - missing_padding)
    return base64.b64decode(encoded_string)
```

### 3. Encode to Base64 (Python)
```python
import base64

def encode_base64(data: bytes | str, as_data_uri: bool = False, mime_type: str = "text/plain") -> str:
    """Encode data to Base64, optionally as a data URI."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    encoded = base64.b64encode(data).decode('ascii')
    if as_data_uri:
        return f"data:{mime_type};base64,{encoded}"
    return encoded
```

### 4. JWT Decoding
```python
import base64
import json

def decode_jwt_payload(jwt_token: str) -> dict:
    """Extract and decode the payload from a JWT (without verification)."""
    payload_b64 = jwt_token.split('.')[1]
    # JWT uses URL-safe Base64
    payload_b64 += '=' * (4 - len(payload_b64) % 4)
    payload_bytes = base64.urlsafe_b64decode(payload_b64)
    return json.loads(payload_bytes)
```

### 5. File Identification After Decoding
```python
import base64

def decode_and_identify(encoded: str) -> tuple[bytes, str]:
    """Decode Base64 and identify the file type from magic bytes."""
    data = decode_base64(encoded)
    # Check magic bytes for common formats
    magic_bytes = {
        b'\x89PNG': ('image/png', '.png'),
        b'\xff\xd8\xff': ('image/jpeg', '.jpg'),
        b'GIF8': ('image/gif', '.gif'),
        b'%PDF': ('application/pdf', '.pdf'),
        b'PK': ('application/zip', '.zip'),
    }
    for magic, (mime, ext) in magic_bytes.items():
        if data.startswith(magic):
            return data, ext
    return data, '.bin'
```

## Common Pitfalls

1. **URL-safe vs. standard Base64.** JWTs and some APIs use URL-safe Base64 (`-` and `_` instead of `+` and `/`). Using the wrong variant produces garbled output. Always check which variant is in use.

2. **Missing padding.** Some encoders strip trailing `=` signs. Always pad to a multiple of 4 before decoding.

3. **Data URI prefix confusion.** When someone says "Base64 image," they often mean a data URI (`data:image/png;base64,...`). Strip the prefix before decoding.

4. **Text encoding mismatch.** Decoding Base64 gives bytes, not necessarily UTF-8 text. If the original was UTF-16 or Latin-1, decoding as UTF-8 produces mojibake. Check the source.

5. **Large file handling.** Base64 increases size by ~33%. For files over ~10MB, avoid converting to Base64 in memory — stream the conversion instead.
